"""Recall scheduler for the NL-forget-prompt study's cells (2026-10-18).
Runs `run_cell.recall_cell()` over every due NL-forget cell on the chosen
platforms, one process per platform, all platforms in parallel.

Usage:
    python nlf_recall_scheduler.py --platforms chatgpt,claude,perplexity,deepseek [--limit N]
    python nlf_recall_scheduler.py --platform chatgpt [--limit N]     (one platform, foreground)

`--limit N` caps how many cells each platform recalls in this run (the
pilot uses --limit 2). Gemini and Copilot are run separately, later:
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
from datetime import datetime, timezone

import config
import tracking
import run_cell as rc

PLATFORM_PREFIX = {"chatgpt": "CH", "claude": "CL", "perplexity": "PE", "deepseek": "DE"}

MESSAGES_PER_CELL = 5
MESSAGE_BUDGET = 35
BASE_BATCH_CELLS = MESSAGE_BUDGET // MESSAGES_PER_CELL
MIN_BATCH_CELLS = 2
COOLDOWN_SECONDS = 10 * 60
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


def _due_now(platform: str, state: dict) -> list[str]:
    cells = _nlf_cells(platform)
    now = datetime.now(timezone.utc)
    return [
        c for c in state["order"]
        if c not in state["failed"]
        and cells.get(c, {}).get("status") == "erased"
        and datetime.fromisoformat(cells[c]["recall_due_at"]) <= now
    ]


def _next_due_at(platform: str, state: dict) -> datetime | None:
    cells = _nlf_cells(platform)
    pending = [
        datetime.fromisoformat(cells[c]["recall_due_at"]) for c in state["order"]
        if c not in state["failed"] and cells.get(c, {}).get("status") == "erased"
    ]
    return min(pending) if pending else None


def run_platform(platform: str, limit: int | None) -> None:
    state = load_state(platform)
    done_this_run = 0
    log(platform, f"=== start (limit={limit}, batch={state['batch_cells']} cells, failed so far={len(state['failed'])}) ===")

    while limit is None or done_this_run < limit:
        due = _due_now(platform, state)
        if not due:
            next_at = _next_due_at(platform, state)
            if next_at is None:
                log(platform, "=== nothing left to recall -- exiting ===")
                return
            wait_s = max(60.0, (next_at - datetime.now(timezone.utc)).total_seconds())
            if wait_s > MAX_WAIT_SECONDS:
                log(platform, f"=== next cell not due until {next_at.isoformat()} (>24h) -- exiting ===")
                return
            log(platform, f"no cell due yet; sleeping {wait_s:.0f}s until {next_at.isoformat()}")
            time.sleep(wait_s)
            continue

        batch = due[: state["batch_cells"]]
        if limit is not None:
            batch = batch[: limit - done_this_run]
        log(platform, f"batch of {len(batch)} (ceiling {state['batch_cells']}, {len(due)} due now)")

        results: list[bool] = []
        for i, cell_id in enumerate(batch):
            try:
                rc.recall_cell(cell_id)
                results.append(True)
                state["recalled"] += 1
                done_this_run += 1
                log(platform, f"OK {cell_id} ({i + 1}/{len(batch)})")
            except Exception as exc:
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
                time.sleep(random.uniform(DELAY_MIN_SECONDS, DELAY_MAX_SECONDS))

        if limit is not None and done_this_run >= limit:
            break
        log(platform, f"batch done; cooling down {COOLDOWN_SECONDS}s")
        time.sleep(COOLDOWN_SECONDS)

    log(platform, f"=== stop: {done_this_run} recalled this run, {len(state['failed'])} failed in total ===")


def launch_parallel(platforms: list[str], limit: int | None) -> None:
    args = ["--limit", str(limit)] if limit is not None else []
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
    ns = parser.parse_args()

    if ns.platform:
        run_platform(ns.platform, ns.limit)
        return
    platforms = [p.strip() for p in ns.platforms.split(",")]
    unknown = [p for p in platforms if p not in PLATFORM_PREFIX]
    if unknown:
        parser.error(f"unknown platform(s): {unknown}; choose from {sorted(PLATFORM_PREFIX)}")
    launch_parallel(platforms, ns.limit)


if __name__ == "__main__":
    main()
