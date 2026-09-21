"""Round-robin batch scheduler for the erasure phase (48h post-injection),
across the full battery: the original 78-cell study (`MASTER`/`FILE
SUBSTUDY`) plus the 828-cell NL-forget-prompt study (`NL FORGET` sheet, see
`RTBF-Prompt/nl_forget_cell_generator.py`). Companion to
`nl_forget_round_robin_scheduler.py` (injection); reuses that script's
per-platform adaptive batch-sizing / throttle-detection / human-like pacing
design close to verbatim -- same platforms, same underlying rate-limit
risk, no reason to re-derive different numbers (see that file's docstring
for the full empirical justification, not repeated here).

The one thing injection never needed and this script adds: erasure is
DESTRUCTIVE, so cells sharing an account must run in a safe ORDER, not
just a safe rate.

DESTRUCTIVE-ACTIONS-RUN-LAST (see project memory
`destructive-actions-run-last` / `flag-and-isolate-contamination-risk`):
within any single account, a broad/blanket erasure (MAXIMAL, "clear all
X", a bulk delete) must not run before a narrower erasure sharing that
same account -- the broad action can silently wipe the narrower cell's
own not-yet-erased data before its turn. This exact failure already
happened once for real during manual erasure runs (see project memory
`check-all-account-mates-before-broad-erasure`: a broad `CH-I1-E6` run
wiped three still-pending narrower cells sharing its account).

The project's account design (`config.py`'s `MAXIMAL_ACCOUNT_LABEL` /
`accounts.md`) already isolates almost every genuine broad-vs-narrow
conflict onto its own dedicated account ahead of this script ever running
-- the sort below is deliberate defense-in-depth, not the primary
safeguard, since a manual audit already did the real isolation work (see
`PROJECT_STATUS.md`'s "'Structural conflict' cells identified" and "Check
ALL account mates" sections).

Ordering mechanics: every due cell gets a `_breadth_rank()` (lower =
narrower = runs first), derived from its own E-number / erasure
description text, and the whole cross-platform-and-account queue is
sorted by `(rank, cell_id)` -- NOT grouped by account first. This is
sufficient, not just convenient: for any two cells A, B sharing one
account, a pure global rank sort still places A before B whenever A's
rank is lower than B's, regardless of what other accounts' cells are
interleaved between them in the overall queue. Intra-account order is
exactly what the destructive-last rule requires; cross-account order is
unconstrained and irrelevant to safety, so there is no need to group by
account explicitly.

Known caveat, not special-cased here (see accounts.md / project memory
`copilot-batch-2026-09-13`): `CO-I1-E6` was held on 2026-09-13 because its
account was stuck in Microsoft's "Temporary" chat mode. If that is still
unresolved, this scheduler will attempt it like any other due cell, it
will fail with a non-throttle error, and that failure will count toward
Copilot's throttle window like a real one -- worth checking that account's
state before a live run reaches it, rather than adding a hardcoded skip
for one cell.

Run `python erasure_scheduler.py --dry-run` first to print the full
planned order (platform, rank, cell_id) with NO erasure calls made --
recommended before ever running this for real, since it is about to
trigger real destructive actions against ~830 cells across many live
accounts. Plain `python erasure_scheduler.py` runs it for real.

State/log kept in separate files (erasure_scheduler_state.json /
erasure_scheduler.log) so this run's learned per-platform ceilings don't
collide with the injection run's (`nlf_scheduler_state.json`). Ceilings
are NOT seeded from the injection run's learned state -- erasure is a
different UI interaction (different clicks/dialogs/timing) on the same
platforms, so its own safe throughput is not assumed to match injection's
without live evidence; each platform starts from the same conservative
defaults injection did (ChatGPT already-observed-throttled seed of 35,
everyone else BASE_BATCH_SIZE) and ratchets down from there independently
if warranted.

Usage:
    python erasure_scheduler.py --dry-run   # print planned order, no erasures
    python erasure_scheduler.py             # run for real
"""
from __future__ import annotations

import functools
import json
import random
import re
import sys
import time
import traceback

import config
import tracking
import run_cell as rc

BASE_BATCH_SIZE = 40
MIN_BATCH_SIZE = 5
# Carried over from the injection scheduler's last validated live setting
# (2026-09-12, pure round-robin timing, no added idle wait beyond the
# natural gap from cycling through other platforms) -- NOT independently
# re-validated for erasure yet, since erasure hasn't been run in bulk
# before this script. If any platform's failure rate crosses the
# throttle-detection threshold below during a real erasure run, that's
# the signal this assumption doesn't transfer and COOLDOWN_SECONDS should
# go back up (90 min was the agreed injection-side fallback).
COOLDOWN_SECONDS = 0
THROTTLE_WINDOW = 5
THROTTLE_FAILS_IN_WINDOW = 2
DELAY_MIN_SECONDS = 15
DELAY_MAX_SECONDS = 70

# Same process-local Playwright corruption signature the injection
# scheduler guards against (confirmed live 2026-09-12) -- see that file's
# docstring for the full incident. Detecting it here aborts the whole
# process instead of drawing a wrong conclusion about a platform's real
# erasure throughput.
ENVIRONMENT_ERROR_SIGNATURES = ("asyncio loop",)

# A cell whose erase_cell() call fails specifically because it's still
# blocked_on_prompt_set (missing erasure_request_text) is a permanent,
# non-throttle-related skip for THIS run -- excluded from future batches
# so it doesn't loop forever re-attempting and doesn't pollute any
# platform's throttle window with a failure that has nothing to do with
# rate limiting. In-memory only (not persisted): if it's still blocked on
# the next process start, it'll be rediscovered and skipped again, which
# is fine and cheap.
PERMANENTLY_BLOCKED: set[str] = set()
BLOCKED_ERROR_SUBSTRING = "depends on the qualitative-coding"

# Platforms skipped for the rest of THIS run after a batch that failed
# outright (0 successes before throttle-detect tripped) -- see run_one_batch.
# In-memory only, not persisted: a fresh process re-tries every platform.
DEAD_PLATFORMS: set[str] = set()

STATE_PATH = config.TESTER_ROOT / "data" / "erasure_scheduler_state.json"
LOG_PATH = config.TESTER_ROOT / "erasure_scheduler.log"

PLATFORMS = ["claude", "perplexity", "deepseek", "chatgpt", "copilot", "gemini"]

# Keywords that mark an erasure as account-wide/blanket regardless of its
# E-number -- a fallback safety net for any cell whose numbering doesn't
# follow the usual narrow-E1-through-broad-E7 convention. Matched against
# the erasure type/description text, lowercased.
BROAD_KEYWORDS = (
    "maximal", "clear all", "delete all", "bulk",
    "privacy dashboard", "all threads", "all memor", "all activit", "all chat",
)


def log(msg: str) -> None:
    line = f"[{time.strftime('%Y-%m-%dT%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG_PATH.open("a") as f:
        f.write(line + "\n")


def load_state() -> dict:
    now = time.time()
    defaults = {p: {"batch_size": (35 if p == "chatgpt" else BASE_BATCH_SIZE), "next_ready_at": now} for p in PLATFORMS}
    if not STATE_PATH.exists():
        return defaults
    state = json.loads(STATE_PATH.read_text())
    for p, d in defaults.items():
        state.setdefault(p, d)
    return state


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2))


# Cache load_cell() results for the lifetime of this process -- a cell's
# platform/erasure-description shape doesn't change once injected, so
# re-parsing the shared xlsx (openpyxl, whole-workbook load) on every
# scheduling decision for the same cell_id would be pure waste across a
# ~830-cell queue re-sorted on every loop iteration.
_load_cell_cached = functools.lru_cache(maxsize=None)(rc.load_cell)

# NL-forget cells' erasure_type_text/erasure_desc are always the fixed
# dispatch key ("NL forget prompt"/"NL forget command") -- the real prompt
# text never appears there, so the generic BROAD_KEYWORDS text-match below
# can't see it. The study's own authoritative deletion_locus coding
# (RTBF-Prompt/data/nl_forget_prompts_138_final.csv, keyed by item_id) is
# the real signal: 18/138 items are coded account_all -- e.g. "delete all
# my data", "clear any instance of it in my account". Those are exactly as
# destructive as MASTER's MAXIMAL cells and must rank last, not first.
NLF_PROMPTS_CSV = config.RTBF_ROOT / "RTBF-Prompt" / "data" / "nl_forget_prompts_138_final.csv"


@functools.lru_cache(maxsize=1)
def _nlf_deletion_locus_map() -> dict[str, str]:
    import csv
    with NLF_PROMPTS_CSV.open() as f:
        return {row["item_id"]: row["deletion_locus"] for row in csv.DictReader(f)}


def _breadth_rank(cell_id: str) -> int:
    """Lower = narrower = should run first on a shared account. See the
    module docstring's DESTRUCTIVE-ACTIONS-RUN-LAST section."""
    if "-NLF-" in cell_id:
        item_id = cell_id.split("-NLF-", 1)[1]
        locus = _nlf_deletion_locus_map().get(item_id)
        if locus == "account_all":
            return 100  # account-wide NL-forget request -- as broad as MAXIMAL
        if locus is None:
            log(f"WARNING: {cell_id}'s item_id {item_id!r} not found in {NLF_PROMPTS_CSV.name} -- defaulting to a mid rank, safer than assuming narrow")
            return 50
        return 1  # conversation/memory/backend_db/prospective/unspecified -- narrow, targets this cell's own token
    try:
        plan = _load_cell_cached(cell_id)
    except Exception as e:
        log(f"WARNING: could not load {cell_id} to rank it ({e}) -- defaulting to a mid rank, safer than assuming narrow")
        return 50

    text = f"{plan.erasure_type_text} {plan.erasure_desc}".lower()
    if cell_id.endswith("-E-MAX") or any(k in text for k in BROAD_KEYWORDS):
        return 100
    if cell_id.endswith("-E-CONV"):
        return 2  # FILE substudy's conversation-scoped delete -- narrow

    m = re.search(r"-E(\d+)$", cell_id)
    if m:
        return int(m.group(1))

    log(f"WARNING: {cell_id} doesn't match any known erasure-code shape -- defaulting to a mid rank")
    return 50


def _is_held_back_nlf_account_all(cell_id: str) -> bool:
    """The 18/138 account_all NL-forget cells (per platform) are held out
    of every erasure run until each gets its own dedicated account -- even
    with the destructive-last rank fix, the first of the 18 to run still
    wipes the shared account and voids the other 17's own attribution (see
    project memory `deletion-location-reconciliation` follow-up,
    2026-09-17). Not run at all for now; not a throttle-related skip, so
    excluded up front rather than via PERMANENTLY_BLOCKED."""
    if "-NLF-" not in cell_id:
        return False
    item_id = cell_id.split("-NLF-", 1)[1]
    return _nlf_deletion_locus_map().get(item_id) == "account_all"


NLF_ONLY = False  # set via --nlf-only; scopes a run to just the "NL FORGET" sheet's cells, skipping any due MASTER/FILE cell
EXCLUDE_PLATFORMS: set[str] = set()  # set via --skip <platform>[,<platform>...]; excluded outright for this run, not even attempted


def remaining_cell_ids(platform: str) -> list[str]:
    if platform in EXCLUDE_PLATFORMS:
        return []
    due = [
        cid for cid in tracking.due_for_erasure()
        if rc.PLATFORM_PREFIX.get(cid[:2]) == platform
        and cid not in PERMANENTLY_BLOCKED
        and not _is_held_back_nlf_account_all(cid)
        and (not NLF_ONLY or "-NLF-" in cid)
    ]
    return sorted(due, key=lambda cid: (_breadth_rank(cid), cid))


def run_one_batch(platform: str, state: dict) -> None:
    ceiling = state[platform]["batch_size"]
    remaining = remaining_cell_ids(platform)
    if not remaining:
        log(f"{platform}: nothing left to erase (0 due) -- removing from rotation")
        return
    if platform in DEAD_PLATFORMS:
        return
    planned = remaining[:ceiling]
    log(
        f"{platform}: starting erasure batch, ceiling={ceiling}, {len(remaining)} total due, "
        f"planning up to {len(planned)} this batch, order={planned}"
    )

    results: list[bool] = []
    succeeded = 0
    throttled = False

    for i, cell_id in enumerate(planned):
        try:
            rc.erase_cell(cell_id)
            results.append(True)
            succeeded += 1
            log(f"{platform}: OK erased {cell_id} ({i + 1}/{len(planned)})")
        except Exception as e:
            if any(sig in str(e) for sig in ENVIRONMENT_ERROR_SIGNATURES):
                log(f"{platform}: ENVIRONMENT ERROR (not a platform throttle) on {cell_id}: {e}")
                log(traceback.format_exc())
                log("Process-local Playwright corruption detected -- aborting scheduler so a fresh "
                    "process can be started (do NOT let this count toward any platform's throttle "
                    "window or ceiling; that cell is untouched/unmarked and will retry normally).")
                raise SystemExit(1)
            if BLOCKED_ERROR_SUBSTRING in str(e):
                PERMANENTLY_BLOCKED.add(cell_id)
                log(f"{platform}: {cell_id} still blocked_on_prompt_set -- permanently skipping for this run, not counted toward throttle window: {e}")
                continue
            results.append(False)
            log(f"{platform}: FAIL {cell_id} ({i + 1}/{len(planned)}): {e}")
            log(traceback.format_exc())

        window = results[-THROTTLE_WINDOW:]
        if len(window) >= THROTTLE_WINDOW and window.count(False) >= THROTTLE_FAILS_IN_WINDOW:
            throttled = True
            log(
                f"{platform}: THROTTLE DETECTED -- {window.count(False)}/{THROTTLE_WINDOW} failures in last "
                f"{THROTTLE_WINDOW} attempts, stopping batch early after {succeeded} successful erasures "
                f"(planned {len(planned)})"
            )
            break

        if i < len(planned) - 1:
            delay = random.uniform(DELAY_MIN_SECONDS, DELAY_MAX_SECONDS)
            time.sleep(delay)

    if throttled and succeeded == 0:
        # Every attempt in this batch failed before even one success -- unlike
        # a normal mid-batch throttle (some successes, then rate-limited), this
        # looks like the platform isn't reachable at all for this run (dead/
        # expired session, UI change, hard block). Retrying it every cooldown
        # cycle for hours while unattended just burns time -- skip it for the
        # rest of this run instead; the run continues on every other platform.
        # Not persisted -- a fresh scheduler run will try it again from scratch.
        DEAD_PLATFORMS.add(platform)
        log(
            f"{platform}: 0/{len(planned)} succeeded before throttle-detect tripped -- looks like a dead "
            f"session or hard block, not ordinary rate-limiting. SKIPPING {platform} for the rest of this "
            f"run (other platforms continue). Check sessions/{platform}__nlforget.json before the next run."
        )

    if throttled:
        new_ceiling = max(MIN_BATCH_SIZE, succeeded)
        if new_ceiling < ceiling:
            log(f"{platform}: lowering batch-size ceiling {ceiling} -> {new_ceiling} based on this batch's observed throttle point")
            state[platform]["batch_size"] = new_ceiling
    else:
        log(f"{platform}: batch completed in full ({succeeded}/{len(planned)} succeeded) without tripping the throttle window -- ceiling stays at {ceiling}")

    state[platform]["next_ready_at"] = time.time() + COOLDOWN_SECONDS
    save_state(state)
    log(f"{platform}: batch done, next ready at {time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(state[platform]['next_ready_at']))}")


def dry_run() -> None:
    print("=== erasure scheduler dry run -- planned order, no erasures will be sent ===")
    total = 0
    total_held_back = 0
    for platform in PLATFORMS:
        queue = remaining_cell_ids(platform)
        total += len(queue)
        held_back = sorted(
            cid for cid in tracking.due_for_erasure()
            if rc.PLATFORM_PREFIX.get(cid[:2]) == platform and _is_held_back_nlf_account_all(cid)
        )
        total_held_back += len(held_back)
        print(f"\n{platform}: {len(queue)} due, {len(held_back)} held back (NLF account_all, no dedicated account yet)")
        for cid in queue:
            rank = _breadth_rank(cid)
            print(f"  rank={rank:>3}  {cid}")
        for cid in held_back:
            print(f"  HELD BACK  {cid}")
    print(f"\nTotal due across all platforms: {total} (+ {total_held_back} held back, not run)")


def main() -> None:
    state = load_state()
    log(f"=== erasure scheduler start, state={state} ===")

    while True:
        pending = [p for p in PLATFORMS if remaining_cell_ids(p)]
        active = [p for p in pending if p not in DEAD_PLATFORMS]
        if not active:
            if pending:
                log(f"=== no live platforms left -- {sorted(DEAD_PLATFORMS)} marked dead this run with cells still due, "
                    f"everyone else is done. Exiting; re-run after fixing those sessions. ===")
            else:
                log("=== all due cells erased -- scheduler exiting ===")
            break

        now = time.time()
        ready = [p for p in active if state[p]["next_ready_at"] <= now]

        if ready:
            platform = min(ready, key=lambda p: state[p]["next_ready_at"])
            run_one_batch(platform, state)
        else:
            next_platform = min(active, key=lambda p: state[p]["next_ready_at"])
            wait_s = state[next_platform]["next_ready_at"] - now
            log(f"no platform ready -- sleeping {wait_s:.0f}s until {next_platform} is ready")
            time.sleep(max(1.0, wait_s))


if __name__ == "__main__":
    if "--nlf-only" in sys.argv:
        NLF_ONLY = True
    if "--skip" in sys.argv:
        EXCLUDE_PLATFORMS = set(sys.argv[sys.argv.index("--skip") + 1].split(","))
        unknown = EXCLUDE_PLATFORMS - set(PLATFORMS)
        if unknown:
            raise SystemExit(f"--skip: unknown platform(s) {sorted(unknown)}, expected from {PLATFORMS}")
    if "--dry-run" in sys.argv:
        dry_run()
    else:
        main()
