"""Recall scheduler for the NL-forget-prompt study's cells (2026-10-18).
Runs `run_cell.recall_cell()` over every due NL-forget cell on the chosen
platforms, one process per platform, all platforms in parallel.

Usage:
    python nlf_recall_scheduler.py --platforms chatgpt,claude,perplexity,deepseek [--limit N]
    python nlf_recall_scheduler.py --platform chatgpt [--limit N]     (one platform, foreground)

`--limit N` caps how many cells each platform recalls in this run (the
pilot uses --limit 2). `--min-days D` (default 31) treats a cell as due
D days after its erasure; the user set D=30 on 2026-10-18 (the study's
recall point is "about a month"; 31 was the scheduled value), so every
cell recalled at 30 days or later counts as on time. When D < 31 the
scheduler passes force=True to recall_cell(), whose own check is the
31-day recall_due_at. Gemini and Copilot are run separately, later:
Gemini waits on the Selenium flow, Copilot runs over CDP in the user's
own Chrome.

METHODOLOGY (documented here because the project is written up as a paper;
mirrors nl_forget_round_robin_scheduler.py, with the differences noted):

1. **Parallel across platforms, one process each.** Each platform has its
   own browser and its own NL-forget account session, and nearly all the
   time per cell is spent in the browser. The only shared state is
   data/run_tracking.json and the workbook, and every write to them now
   runs under shared_files.write_lock() with an atomic save (stress-tested
   2026-10-18: 8 processes, no lost writes with the lock; 34% of JSON and
   70% of workbook writes lost without it). The injection scheduler ran
   platforms strictly in sequence only because that lock did not exist.

2. **Random cell order within each platform**, drawn once with a logged
   seed and stored in this platform's state file, so a restart keeps the
   same order. With 120 cells per platform the run spans more than a day;
   randomizing keeps that extra delay after the 31-day due date from being
   tied to prompt order (cell index).

3. **Batches sized in messages, not cells.** A recall sends 5 messages (2
   R3 + 2 R1 in new conversations, plus the same-conversation R1 every
   NL-forget cell gets as a typed erasure). The injection run's throttle
   point on ChatGPT was ~44 single-message attempts, so a recall batch is
   capped at MESSAGE_BUDGET (35) messages = 7 cells, followed by a
   COOLDOWN_SECONDS (10 min) pause. Same throttle detection as injection:
   2 failures in the last 5 cells stops the batch and lowers that
   platform's ceiling (never below MIN_BATCH_CELLS).

4. **Random 15-70 s delay between cells**, as in the injection run, so the
   request timing is not machine-regular.

5. **A failed cell is never retried automatically.** Unlike injection, a
   recall that fails partway may already have sent some of its probes;
   re-running it would send that cell's probes twice and break the
   one-recall-per-cell design. recall_cell() only marks a cell recalled on
   success, so a failed cell stays "erased"; this scheduler records it in
   the state file's "failed" list and skips it from then on. A person
   decides each one from its per-probe screenshots.

6. **Graceful stop.** Creating data/nlf_recall.STOP makes every platform
   process exit after its current cell finishes (checked between cells and
   during sleeps), so a stop never leaves a cell half-recalled. Added
   2026-10-18 after verify_recalls.py's pkill interrupted CH-NLF-I0371
   between its R3 and R1 probes.

State: data/nlf_recall_state_<platform>.json (one file per platform, so
the processes never share it). Log: data/nlf_recall_<platform>.log.
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import time
import traceback
import urllib.request
from datetime import datetime, timedelta, timezone

import config
import tracking
import run_cell as rc

PLATFORM_PREFIX = {"chatgpt": "CH", "claude": "CL", "perplexity": "PE", "deepseek": "DE", "copilot": "CO", "gemini": "GE"}

MESSAGES_PER_CELL = 5
MESSAGE_BUDGET = 35
BASE_BATCH_CELLS = MESSAGE_BUDGET // MESSAGES_PER_CELL
MIN_BATCH_CELLS = 2
COOLDOWN_SECONDS = 10 * 60
# Per-platform pacing (user direction 2026-10-18, replacing the earlier
# 3-cells-per-batch settings): ChatGPT 20 cells and Claude 15 cells per
# batch, a random 1-3 minute wait between cells, and a 15-minute break
# between batches. Basis: ChatGPT's soft limit tripped at ~25 messages in
# ~11 minutes (CH-NLF-I0293), and this pace is ~15 messages per 11 minutes;
# Claude's free tier capped out at ~105 messages per 5 hours (CL-NLF-I0334),
# so 15 cells (~75 messages) per batch stays under it. Both flows also wait
# out their limit banner before each prompt if it still appears.
PLATFORM_BATCH_CELLS = {"chatgpt": 20, "claude": 15, "copilot": 10, "gemini": 10}
PLATFORM_DELAY_SECONDS = {"chatgpt": (60, 180), "claude": (60, 180), "copilot": (60, 180), "gemini": (30, 90)}
# Gemini (2026-10-18, user: a flat uniform wait looks robotic): the wait
# between cells is usually short, but with this chance it is a long break.
PLATFORM_LONG_DELAY = {"gemini": ((150, 300), 0.15)}
# Claude: 15 cells (~75 messages) per batch, then ~4 h so each batch lands in
# a fresh 5-hour window (its cap refuses messages silently when exhausted,
# seen 2026-10-18 12:00-16:00: chats created but empty, no dialog).
PLATFORM_COOLDOWN_SECONDS = {"chatgpt": 15 * 60, "claude": 4 * 3600 + 10 * 60, "copilot": 15 * 60, "gemini": 15 * 60}

# Copilot runs over CDP in the user's own Chrome (--cdp): the flow uses
# whatever account that browser is signed into and does not check it, and a
# stale tab once showed the previous account after a switch (2026-10-18). So
# before every Copilot batch the page is reloaded and the Settings name must
# contain this account's Copilot display name ("astra" = astrataiwo@gmail.com,
# the nlforget account; the other Copilot accounts are "Ola Coder", "Ogunwale
# Pelumi", "Ayomide NoReply").
CDP_URL = "http://localhost:9222"
# Gemini can run either way (2026-10-18): "cookies" = the default exported-
# cookie flow (run_cell.FLOW_REGISTRY), "cdp" = flows/gemini_cdp.py attached to
# the user's own signed-in Chrome on 9223. Chosen with --gemini-method.
GEMINI_CDP_URL = "http://localhost:9223"
# Platforms whose same-conversation question waits for a later pass (see
# run_cell.DEFERRED_SAME_CONVERSATION): Copilot, for its daily message cap.
DEFER_SAME_CONVERSATION = {"copilot"}
GEMINI_METHOD = "cookies"
EXPECTED_ACCOUNT_NAME = {"copilot": "astra"}
DELAY_MIN_SECONDS = 15
DELAY_MAX_SECONDS = 70
THROTTLE_WINDOW = 5
THROTTLE_FAILS_IN_WINDOW = 2
# Wait for cells that come due soon (DeepSeek's 32 due 2026-10-19), but
# exit rather than sleep for days on the 13 Group 1 cells due 2026-10-24.
MAX_WAIT_SECONDS = 24 * 3600

# Same process-local Playwright corruption signature the injection
# scheduler treats as an environment error, not a platform throttle.
ENVIRONMENT_ERROR_SIGNATURES = ("cannot switch to a different thread",)
# "no new reply appeared" = a prompt got no answer at all (Claude's silent
# cap, Copilot's daily limit): stop the platform instead of failing cell after
# cell; the stopped cell is resumed or re-run later. Gemini's flow words the
# same failure "no new response appeared" (missed 2026-10-18 on GE-NLF-I0012,
# when the run went on to the next cell until stopped by hand).
PLATFORM_BACKOFF_SIGNATURES = (
    "still overloaded", "unusual-traffic", "no new reply appeared", "no new response appeared", "daily limit active",
    "prompt not submitted", "did not land in the composer",
)

# Connection problems while opening the browser (2026-10-19: WiFi drops failed
# 27 Gemini and 8 Claude cells overnight, none with anything sent, and tripped
# Claude's throttle detection). A cell that fails this way before any prompt
# (run_cell.FlowNotStarted) stays in the queue instead of the failed list and
# does not count as throttling. "No gemini.google.com tab" is how the CDP flow
# sees the Gemini tab while Chrome shows its offline page.
NETWORK_ERROR_SIGNATURES = ("net::ERR_", "Timeout 30000ms exceeded", "No gemini.google.com tab")
# Same not-started failure this many cells in a row while the internet check
# passes = something else is wrong (tab closed, signed out): stop the platform.
MAX_NOT_STARTED_IN_A_ROW = 5
INTERNET_CHECK_URL = "https://www.example.com"
INTERNET_POLL_SECONDS = 60


STOP_PATH = config.TESTER_ROOT / "data" / "nlf_recall.STOP"


def _internet_up() -> bool:
    try:
        with urllib.request.urlopen(INTERNET_CHECK_URL, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


def _wait_for_internet(platform: str) -> bool:
    """Returns once the internet is reachable (False if a stop was requested
    meanwhile). No cell is touched while waiting."""
    if _internet_up():
        return True
    log(platform, "INTERNET DOWN -- waiting before the next cell, nothing attempted")
    started = time.time()
    while not _internet_up():
        if not _sleep(platform, INTERNET_POLL_SECONDS):
            return False
    log(platform, f"internet back after {time.time() - started:.0f}s")
    return True


def _stop_requested(platform: str) -> bool:
    if STOP_PATH.exists():
        log(platform, f"stop file found ({STOP_PATH.name}) -- exiting before the next cell")
        return True
    return False


def _sleep(platform: str, seconds: float) -> bool:
    """Sleeps in 5s steps; returns False if a stop was requested meanwhile."""
    end = time.time() + seconds
    while time.time() < end:
        if STOP_PATH.exists():
            return False
        time.sleep(min(5.0, end - time.time()))
    return True


def _state_path(platform: str):
    return config.TESTER_ROOT / "data" / f"nlf_recall_state_{platform}.json"


def _log_path(platform: str):
    return config.TESTER_ROOT / "data" / f"nlf_recall_{platform}.log"


def log(platform: str, msg: str) -> None:
    line = f"[{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}] {platform}: {msg}"
    print(line, flush=True)
    with _log_path(platform).open("a") as f:
        f.write(line + "\n")


def _nlf_cells(platform: str) -> dict[str, dict]:
    prefix = f"{PLATFORM_PREFIX[platform]}-NLF-"
    return {c: e for c, e in tracking.load().items() if c.startswith(prefix)}


def load_state(platform: str) -> dict:
    path = _state_path(platform)
    if path.exists():
        return json.loads(path.read_text())
    seed = random.SystemRandom().randrange(2**32)
    order = sorted(c for c, e in _nlf_cells(platform).items() if e.get("status") == "erased")
    random.Random(seed).shuffle(order)
    state = {"seed": seed, "order": order, "batch_cells": BASE_BATCH_CELLS, "failed": {}, "recalled": 0}
    save_state(platform, state)
    log(platform, f"new state: {len(order)} erased cells shuffled with seed {seed}")
    return state


def save_state(platform: str, state: dict) -> None:
    _state_path(platform).write_text(json.dumps(state, indent=2) + "\n")


def _due_at(entry: dict, min_days: int) -> datetime:
    return datetime.fromisoformat(entry["erased_at"]) + timedelta(days=min_days)


def _pending(platform: str, state: dict) -> dict[str, dict]:
    cells = _nlf_cells(platform)
    return {
        c: cells[c] for c in state["order"]
        if c not in state["failed"] and cells.get(c, {}).get("status") == "erased"
    }


def _due_now(platform: str, state: dict, min_days: int) -> list[str]:
    now = datetime.now(timezone.utc)
    return [c for c, e in _pending(platform, state).items() if _due_at(e, min_days) <= now]


def _next_due_at(platform: str, state: dict, min_days: int) -> datetime | None:
    pending = [_due_at(e, min_days) for e in _pending(platform, state).values()]
    return min(pending) if pending else None


def _copilot_account_name() -> str:
    from flows.copilot import CopilotFlow
    with CopilotFlow(cdp_url=CDP_URL) as flow:
        flow.page.goto(flow.BASE_URL, wait_until="domcontentloaded")
        flow.page.wait_for_timeout(5000)
        flow._open_settings_dialog()
        dialog = flow.page.locator('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"])').first
        dialog.locator('[role="tab"]').filter(has_text="General").click()
        flow.page.wait_for_timeout(1500)
        text = dialog.inner_text()
        flow.page.keyboard.press("Escape")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return lines[lines.index("Name") + 1] if "Name" in lines else ""


def _account_ok(platform: str) -> bool:
    expected = EXPECTED_ACCOUNT_NAME.get(platform)
    if expected is None:
        return True
    name = _copilot_account_name()
    if expected.lower() in name.lower():
        log(platform, f"account check OK: signed in as {name!r}")
        return True
    log(platform, f"ACCOUNT MISMATCH: signed in as {name!r}, expected {expected!r} -- stopping, nothing sent")
    return False


def run_platform(platform: str, limit: int | None, min_days: int) -> None:
    state = load_state(platform)
    if platform in PLATFORM_BATCH_CELLS:
        state["batch_cells"] = PLATFORM_BATCH_CELLS[platform]
    delay_min, delay_max = PLATFORM_DELAY_SECONDS.get(platform, (DELAY_MIN_SECONDS, DELAY_MAX_SECONDS))
    done_this_run = 0
    not_started_streak = 0
    force = min_days < tracking.RECALL_DELAY.days
    if platform == "gemini":
        log(platform, f"gemini method: {GEMINI_METHOD}" + (f" ({GEMINI_CDP_URL})" if GEMINI_METHOD == "cdp" else ""))
    log(platform, f"=== start (limit={limit}, min_days={min_days}, batch={state['batch_cells']} cells, "
                  f"failed so far={len(state['failed'])}) ===")

    while limit is None or done_this_run < limit:
        if _stop_requested(platform):
            break
        due = _due_now(platform, state, min_days)
        if not due:
            next_at = _next_due_at(platform, state, min_days)
            if next_at is None:
                log(platform, "=== nothing left to recall -- exiting ===")
                return
            wait_s = max(60.0, (next_at - datetime.now(timezone.utc)).total_seconds())
            if wait_s > MAX_WAIT_SECONDS:
                log(platform, f"=== next cell not due until {next_at.isoformat()} (>24h) -- exiting ===")
                return
            log(platform, f"no cell due yet; sleeping {wait_s:.0f}s until {next_at.isoformat()}")
            if not _sleep(platform, wait_s):
                continue
            continue

        # A platform-specific batch size replaces the saved ceiling; throttle
        # detection below can still lower it for the rest of this run.
        ceiling = state["batch_cells"]
        batch = due[:ceiling]
        if not _account_ok(platform):
            break
        if limit is not None:
            batch = batch[: limit - done_this_run]
        log(platform, f"batch of {len(batch)} (ceiling {ceiling}, {len(due)} due now)")

        results: list[bool] = []
        for i, cell_id in enumerate(batch):
            if _stop_requested(platform) or not _wait_for_internet(platform):
                break
            try:
                rc.recall_cell(cell_id, force=force, cdp_url=_cdp_url(platform),
                               defer_same_conversation=platform in DEFER_SAME_CONVERSATION)
                results.append(True)
                state["recalled"] += 1
                done_this_run += 1
                not_started_streak = 0
                log(platform, f"OK {cell_id} ({i + 1}/{len(batch)})")
            except Exception as exc:
                if (isinstance(exc, rc.FlowNotStarted)
                        and any(sig in str(exc) for sig in NETWORK_ERROR_SIGNATURES)
                        and not any(sig in str(exc) for sig in PLATFORM_BACKOFF_SIGNATURES)):
                    not_started_streak += 1
                    log(platform, f"NOT STARTED {cell_id} ({i + 1}/{len(batch)}): connection problem while "
                                  f"opening, nothing sent; left in the queue: {exc}")
                    if not_started_streak >= MAX_NOT_STARTED_IN_A_ROW and _internet_up():
                        log(platform, f"BACKOFF: {not_started_streak} cells in a row could not open although "
                                      f"the internet is up -- stopping {platform}, nothing sent")
                        save_state(platform, state)
                        return
                    _sleep(platform, INTERNET_POLL_SECONDS)
                    continue
                if any(sig in str(exc) for sig in PLATFORM_BACKOFF_SIGNATURES):
                    # Gemini overloaded again after its one re-ask, or Google's
                    # unusual-traffic page (user direction 2026-10-18: back
                    # off as soon as these appear). Stop this platform rather
                    # than push on to the next cell.
                    state["failed"][cell_id] = f"{type(exc).__name__}: {exc}"[:500]
                    save_state(platform, state)
                    log(platform, f"BACKOFF: {exc} -- stopping {platform}; {cell_id} left for resume")
                    return
                if any(sig in str(exc) for sig in ENVIRONMENT_ERROR_SIGNATURES):
                    log(platform, f"ENVIRONMENT ERROR on {cell_id}, aborting this process: {exc}")
                    log(platform, traceback.format_exc())
                    save_state(platform, state)
                    raise SystemExit(1)
                results.append(False)
                state["failed"][cell_id] = f"{type(exc).__name__}: {exc}"[:500]
                log(platform, f"FAIL {cell_id} ({i + 1}/{len(batch)}), not retried: {exc}")
                log(platform, traceback.format_exc())
            save_state(platform, state)

            window = results[-THROTTLE_WINDOW:]
            if len(window) >= THROTTLE_WINDOW and window.count(False) >= THROTTLE_FAILS_IN_WINDOW:
                new_ceiling = max(MIN_BATCH_CELLS, results.count(True))
                log(platform, f"THROTTLE DETECTED ({window.count(False)}/{THROTTLE_WINDOW} failed); "
                              f"ceiling {state['batch_cells']} -> {new_ceiling}")
                state["batch_cells"] = min(state["batch_cells"], new_ceiling)
                save_state(platform, state)
                break

            if i < len(batch) - 1:
                long_range, long_chance = PLATFORM_LONG_DELAY.get(platform, ((delay_min, delay_max), 0.0))
                pause = random.uniform(*long_range) if random.random() < long_chance else random.uniform(delay_min, delay_max)
                _sleep(platform, pause)

        if limit is not None and done_this_run >= limit:
            break
        if STOP_PATH.exists():
            continue
        cooldown = PLATFORM_COOLDOWN_SECONDS.get(platform, COOLDOWN_SECONDS)
        log(platform, f"batch done; cooling down {cooldown}s")
        _sleep(platform, cooldown)

    log(platform, f"=== stop: {done_this_run} recalled this run, {len(state['failed'])} failed in total ===")


def _cdp_url(platform: str) -> str | None:
    if platform == "copilot":
        return CDP_URL
    if platform == "gemini" and GEMINI_METHOD == "cdp":
        return GEMINI_CDP_URL
    return None


def launch_parallel(platforms: list[str], limit: int | None, min_days: int) -> None:
    args = ["--min-days", str(min_days), "--gemini-method", GEMINI_METHOD]
    args += ["--limit", str(limit)] if limit is not None else []
    procs = {
        p: subprocess.Popen([sys.executable, __file__, "--platform", p, *args], cwd=config.TESTER_ROOT)
        for p in platforms
    }
    for p, proc in procs.items():
        print(f"{p}: exited with code {proc.wait()}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--platform", choices=PLATFORM_PREFIX)
    group.add_argument("--platforms", help="comma-separated, e.g. chatgpt,claude,perplexity,deepseek")
    parser.add_argument("--limit", type=int, default=None, help="max cells per platform this run")
    parser.add_argument("--min-days", type=int, default=tracking.RECALL_DELAY.days,
                        help="days after erasure a cell counts as due (default 31)")
    parser.add_argument("--gemini-method", choices=("cookies", "cdp"), default="cookies",
                        help="cookies = exported-session flow (default); cdp = the user's Chrome on 9223")
    ns = parser.parse_args()
    global GEMINI_METHOD
    GEMINI_METHOD = ns.gemini_method

    if ns.platform:
        run_platform(ns.platform, ns.limit, ns.min_days)
        return
    platforms = [p.strip() for p in ns.platforms.split(",")]
    unknown = [p for p in platforms if p not in PLATFORM_PREFIX]
    if unknown:
        parser.error(f"unknown platform(s): {unknown}; choose from {sorted(PLATFORM_PREFIX)}")
    launch_parallel(platforms, ns.limit, ns.min_days)


if __name__ == "__main__":
    main()
