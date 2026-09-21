"""Round-robin scheduler for the NL-forget-prompt study's 828-cell injection
run (RTBF-Prompt/nl_forget_cell_generator.py; see project memory
nl-forget-pipeline-built-2026-09-11 for full pipeline context). Drives
ChatGPT/Claude/Perplexity/DeepSeek's remaining injections to completion.

METHODOLOGY (documented here, not just in commit history, since this
project is being written up as a paper -- every parameter below has an
empirical or reasoned justification, not an arbitrary default):

1. **Per-cell pacing, 15-70s random delay** (confirmed 2026-09-11, user
   direction): a plain back-to-back loop is trivially distinguishable from
   human interaction by inter-request timing alone. A uniform random delay
   in [15, 70) seconds between each individual cell's injection avoids a
   suspiciously regular cadence without slowing the run to the point of
   impracticality across 552 cells.

2. **Per-platform ADAPTIVE batch sizing, not a fixed 40 everywhere**
   (confirmed 2026-09-11, user direction): ChatGPT's real failure pattern
   (see _nlf_batch_chatgpt.log) went from ~98% success through the first
   ~44 attempts to majority-failure immediately after -- a clean soft-
   throttle signature (37/38 failures were the exact same
   "Locator.click: Timeout 10000ms exceeded" on the send-button), not
   random flakiness. Every platform STARTS at a batch-size assumption of
   BASE_BATCH_SIZE (40, ChatGPT's own observed rough threshold) but
   independently ratchets its own ceiling DOWN if it empirically shows
   throttling before reaching that ceiling -- Claude/Perplexity/DeepSeek
   are not assumed to share ChatGPT's exact threshold.

   Detection rule: a sliding window of the last THROTTLE_WINDOW (5)
   attempts; if THROTTLE_FAILS_IN_WINDOW (2) or more of those fail, the
   batch stops immediately (does not burn through its remaining planned
   cells) and that platform's ceiling for all FUTURE batches becomes
   however many cells it successfully injected in the batch that just
   stopped (floored at MIN_BATCH_SIZE=5, so a single bad-luck failure
   can't collapse a platform to near-zero throughput permanently). A
   batch that completes in full without ever tripping the window is
   POSITIVE evidence the current ceiling is still safe -- the ceiling is
   never automatically increased past its current value, only decreased,
   since we have no positive incentive to push a platform harder once a
   safe operating point is found (conservative by design, matches
   "destructive actions run last"-style caution elsewhere in this
   project).

3. **6-hour cooldown between a platform's own successive batches**
   (confirmed 2026-09-11, user direction -- supersedes an earlier 10-min
   default that was too aggressive; ChatGPT was still tripping the limit
   moments after the shorter cooldown, see project memory
   nl-forget-pipeline-built-2026-09-11's "session capture progress"
   section... actually see notes.md's "NL-forget injection run" section
   for the full incident writeup). Cooldown is measured from the END of a
   platform's last batch, not its start.

4. **Round-robin across platforms, always running whichever platform's
   6h cooldown has elapsed soonest** (not fixed sequential
   platform-by-platform): fills otherwise-idle cooldown time with other
   platforms' batches instead of leaving 3 platforms sitting idle while
   one waits, without ever running two platforms CONCURRENTLY -- see
   run_cell.py's tracking.py/xlsx write-back, which is whole-file
   read-modify-write with no locking (confirmed 2026-09-11 while planning
   this script); concurrent writes from multiple platforms' processes at
   once would silently lose injection records. This scheduler is a single
   process, one platform's one cell at a time, by construction -- there
   is no code path in this file that runs two platforms' injections
   simultaneously.

5. **A failed cell is never marked injected** (inject_cell() in
   run_cell.py only calls tracking.mark_injected() on success), so a
   throttled/failed attempt automatically gets retried in that platform's
   next batch -- no separate retry bookkeeping needed here.

State persisted to data/nlf_scheduler_state.json (per-platform ceiling and
next-ready-time) so the scheduler can be killed and restarted without
losing what it's learned about each platform's safe throughput, or
resetting cooldowns back to "now" (which would re-trigger the exact
throttling this script exists to avoid). Human-readable progress + every
scheduling decision logged to nlf_scheduler.log for the paper's Methods
section.

Usage: python nl_forget_round_robin_scheduler.py
"""
from __future__ import annotations

import json
import random
import time
import traceback
from pathlib import Path

import openpyxl

import config
import tracking
import run_cell as rc

BASE_BATCH_SIZE = 40
MIN_BATCH_SIZE = 5
COOLDOWN_SECONDS = 0  # EXPERIMENT, 2026-09-12: try pure round-robin timing (no
# added idle wait beyond the natural gap from cycling through the other 3
# platforms) instead of a fixed cooldown -- user's reasoning: ChatGPT's
# observed throttle point (~44 requests at ~45-90s cadence, i.e. tripped
# within ~35-65 min of continuous activity) looks like a sliding roughly-
# hourly window, not a "must wait exactly N hours" rule, and a full
# round-robin cycle (4 platforms x ~35-50 min/batch) already takes
# ~2.5-3.5h -- well past that suspected window. UNVERIFIED, being tested
# live: if any platform's failure rate crosses the throttle-detection
# threshold below, that's the signal this assumption was wrong for that
# platform, and COOLDOWN_SECONDS should go back up (90 min was the agreed
# fallback) rather than staying at 0 for that platform specifically.
THROTTLE_WINDOW = 5
THROTTLE_FAILS_IN_WINDOW = 2
DELAY_MIN_SECONDS = 15
DELAY_MAX_SECONDS = 70

# Confirmed live 2026-09-12: after ~1h45m and ~350+ sequential
# sync_playwright() launches in one long-running process, Playwright's sync
# wrapper can get into a corrupted state ("It looks like you are using
# Playwright Sync API inside the asyncio loop") where EVERY subsequent
# launch fails identically, regardless of platform -- confirmed it hit
# ChatGPT and Perplexity back-to-back in the same few seconds, and that a
# freshly-started process (not the failing one) launches sync_playwright()
# fine immediately. This is process-local corruption, not a platform rate
# limit, but it produces the exact same "attempt fails" signal the
# throttle-window detector watches for -- it had already caused one false
# ceiling drop (ChatGPT 35->5) before being caught and reverted by hand.
# Detecting this signature and aborting the whole process (rather than
# letting it count toward any platform's throttle window) forces the only
# actual fix -- a fresh process -- instead of drawing a wrong conclusion
# about a platform's real throughput limit.
ENVIRONMENT_ERROR_SIGNATURES = ("asyncio loop",)

STATE_PATH = config.TESTER_ROOT / "data" / "nlf_scheduler_state.json"
LOG_PATH = config.TESTER_ROOT / "nlf_scheduler.log"

PLATFORMS = ["claude", "perplexity", "deepseek", "chatgpt", "copilot", "gemini"]  # start order per user direction 2026-09-11; copilot added 2026-09-12 after the first 4 finished (552/552); gemini added 2026-09-12 once its nlforget session export finally worked -- see project memory nl-forget-adaptive-scheduler-2026-09-11
PREFIX = {"chatgpt": "CH", "claude": "CL", "gemini": "GE", "copilot": "CO", "perplexity": "PE", "deepseek": "DE"}


def log(msg: str) -> None:
    line = f"[{time.strftime('%Y-%m-%dT%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG_PATH.open("a") as f:
        f.write(line + "\n")


def load_state() -> dict:
    # ChatGPT already has a real observed data point (throttling started
    # around attempt ~44-50) -- seed it below BASE_BATCH_SIZE from the
    # start rather than re-discovering the same thing live again.
    now = time.time()
    defaults = {p: {"batch_size": (35 if p == "chatgpt" else BASE_BATCH_SIZE), "next_ready_at": now} for p in PLATFORMS}
    if not STATE_PATH.exists():
        return defaults
    state = json.loads(STATE_PATH.read_text())
    # Backfill any platform added to PLATFORMS after this state file was
    # first written (e.g. Copilot added 2026-09-12) so a new platform
    # doesn't KeyError instead of just starting fresh at BASE_BATCH_SIZE.
    for p, d in defaults.items():
        state.setdefault(p, d)
    return state


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2))


def get_cell_ids(platform: str) -> list[str]:
    wb = openpyxl.load_workbook(config.MASTER_XLSX_PATH, data_only=True)
    ws = wb["NL FORGET"]
    prefix = PREFIX[platform]
    return [row[0] for row in ws.iter_rows(min_row=2, values_only=True) if row[0] and row[0].startswith(f"{prefix}-NLF-")]


def remaining_cell_ids(platform: str) -> list[str]:
    return [c for c in get_cell_ids(platform) if tracking.get(c) is None]


def run_one_batch(platform: str, state: dict) -> None:
    """Runs up to state[platform]['batch_size'] cells for this platform,
    stopping early (and lowering the ceiling) if the throttle window trips.
    Sleeps a random human-like delay between every cell, throttled or not."""
    ceiling = state[platform]["batch_size"]
    remaining = remaining_cell_ids(platform)
    if not remaining:
        log(f"{platform}: nothing left to inject (0 remaining) -- removing from rotation")
        return
    planned = remaining[:ceiling]
    log(f"{platform}: starting batch, ceiling={ceiling}, {len(remaining)} total remaining, planning up to {len(planned)} this batch")

    results: list[bool] = []  # True=success, False=failure, in order
    succeeded = 0
    throttled = False

    for i, cell_id in enumerate(planned):
        try:
            rc.inject_cell(cell_id)
            results.append(True)
            succeeded += 1
            log(f"{platform}: OK {cell_id} ({i + 1}/{len(planned)})")
        except Exception as e:
            if any(sig in str(e) for sig in ENVIRONMENT_ERROR_SIGNATURES):
                log(f"{platform}: ENVIRONMENT ERROR (not a platform throttle) on {cell_id}: {e}")
                log(traceback.format_exc())
                log("Process-local Playwright corruption detected -- aborting scheduler so a fresh "
                    "process can be started (do NOT let this count toward any platform's throttle "
                    "window or ceiling; that cell is untouched/unmarked and will retry normally).")
                raise SystemExit(1)
            results.append(False)
            log(f"{platform}: FAIL {cell_id} ({i + 1}/{len(planned)}): {e}")
            log(traceback.format_exc())

        window = results[-THROTTLE_WINDOW:]
        if len(window) >= THROTTLE_WINDOW and window.count(False) >= THROTTLE_FAILS_IN_WINDOW:
            throttled = True
            log(
                f"{platform}: THROTTLE DETECTED -- {window.count(False)}/{THROTTLE_WINDOW} failures in last "
                f"{THROTTLE_WINDOW} attempts, stopping batch early after {succeeded} successful injections "
                f"(planned {len(planned)})"
            )
            break

        # Human-like pacing -- applied between every attempt, success or
        # failure, not just successes (a failed attempt still represents a
        # real request the platform saw).
        if i < len(planned) - 1:
            delay = random.uniform(DELAY_MIN_SECONDS, DELAY_MAX_SECONDS)
            time.sleep(delay)

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


def main() -> None:
    state = load_state()
    log(f"=== scheduler start, state={state} ===")

    while True:
        active = [p for p in PLATFORMS if remaining_cell_ids(p)]
        if not active:
            log("=== all platforms complete -- scheduler exiting ===")
            break

        now = time.time()
        ready = [p for p in active if state[p]["next_ready_at"] <= now]

        if ready:
            # Among platforms ready right now, prefer the one that's been
            # waiting longest (earliest next_ready_at) -- keeps the
            # rotation fair rather than always favoring PLATFORMS' fixed
            # order once multiple are simultaneously ready.
            platform = min(ready, key=lambda p: state[p]["next_ready_at"])
            run_one_batch(platform, state)
        else:
            next_platform = min(active, key=lambda p: state[p]["next_ready_at"])
            wait_s = state[next_platform]["next_ready_at"] - now
            log(f"no platform ready -- sleeping {wait_s:.0f}s until {next_platform} is ready")
            time.sleep(max(1.0, wait_s))


if __name__ == "__main__":
    main()
