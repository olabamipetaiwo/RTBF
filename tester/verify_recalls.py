"""Independent per-cell check of a recall run against a baseline snapshot
(2026-10-18, written for the NL-forget recall run; see
nlf_recall_scheduler.py). Run alongside the scheduler; every --interval
seconds it re-reads run_tracking.json, the workbook and the transcripts and
checks every cell recalled since the baseline:

  source of truth
    - run_tracking.json and the workbook both load (neither is corrupt)
    - the workbook still has the baseline's sheets
    - no cell other than newly recalled ones changed in run_tracking.json
    - no workbook row other than newly recalled cells' rows changed
  each newly recalled cell
    - tracking: status "recalled" with a recalled_at timestamp
    - workbook row: RECALLED, R1/R2/R3/same-conversation/outcome all filled
    - 03_recall_new_conversation.json: all four R3/R1 replies non-empty,
      each different from the reply before it in the same conversation
    - 04_recall_same_conversation.json (typed erasures): reply non-empty and
      not identical to the cell's earlier erase or inject reply (the stale
      read fixed 2026-10-18)
    - at least 5 recall screenshots

On any violation it prints VIOLATION lines and, with --kill, creates the
scheduler's stop file (data/nlf_recall.STOP) so every platform exits after
its current cell, never mid-cell (changed 2026-10-18 from pkill, which cut
CH-NLF-I0371 off between probes). A same-conversation probe that failed
and was recorded as "ERROR (...)" in the workbook is reported as a WARNING
and does not stop the run: nothing was mis-scored, and the reply can be
re-read from the conversation afterwards.

Usage:
    python verify_recalls.py --snapshot <dir>          (take the baseline)
    python verify_recalls.py --baseline <dir> [--interval 120] [--kill]
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

import openpyxl

import config
import tracking
from sibling_tokens import breadcrumb as sibling_breadcrumb, find_sibling_tokens

XLSX = Path(config.MASTER_XLSX_PATH)
SHEETS = ("MASTER ", "NL FORGET")
SCHEDULER_PATTERN = "nlf_recall_scheduler"
STOP_PATH = config.TESTER_ROOT / "data" / "nlf_recall.STOP"
NEW_CONV_KEYS = ("r3_reply", "r3_followup_reply", "r1_open_reply", "r1_open_followup_reply")
PLATFORMS = {"CH": "chatgpt", "CL": "claude", "PE": "perplexity", "DE": "deepseek",
             "GE": "gemini", "CO": "copilot"}


def snapshot(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(tracking.TRACKING_PATH, dest / "run_tracking.json")
    shutil.copy2(XLSX, dest / XLSX.name)
    print(f"baseline saved to {dest}")


def _rows(path: Path) -> tuple[list[str], dict[tuple[str, str], tuple]]:
    wb = openpyxl.load_workbook(path, data_only=True)
    rows = {}
    for name in SHEETS:
        for r in wb[name].iter_rows(min_row=2, values_only=True):
            if r and r[0]:
                rows[(name, r[0])] = r
    return wb.sheetnames, rows


def _json(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def check_cell(cell: str, entry: dict, row: tuple | None, sheet: str) -> list[str]:
    """Problems are plain strings; ones starting with "WARNING" do not stop the run."""
    bad = []
    if not entry.get("recalled_at"):
        bad.append("tracking has no recalled_at")
    if row is None:
        return bad + ["no workbook row"]
    nlf = sheet == "NL FORGET"
    cols = (8, 9, 10, 11, 12, 16) if nlf else (9, 10, 11, 12, 13, 19)
    status, r1, r2, r3, same, outcome = (row[c - 1] for c in cols)
    if status != "RECALLED":
        bad.append(f"workbook run status is {status!r}")
    for name, val in (("R1", r1), ("R2", r2), ("R3", r3), ("same-conv", same), ("outcome", outcome)):
        if not val:
            bad.append(f"workbook {name} empty")

    d = config.TRANSCRIPTS_DIR / PLATFORMS[cell[:2]] / cell
    new = _json(d / "json" / "03_recall_new_conversation.json")
    if not new:
        bad.append("03_recall_new_conversation.json missing")
    else:
        replies = [new.get(k) or "" for k in NEW_CONV_KEYS]
        for k, v in zip(NEW_CONV_KEYS, replies):
            if not v.strip():
                bad.append(f"{k} empty")
        if replies[0].strip() and replies[0].strip() == replies[1].strip():
            bad.append("WARNING R3 follow-up identical to R3: a genuine repeat passes run_cell._send_fresh only if a new reply appeared; check the screenshots")
        if replies[2].strip() and replies[2].strip() == replies[3].strip():
            bad.append("WARNING R1 follow-up identical to R1: a genuine repeat passes run_cell._send_fresh only if a new reply appeared; check the screenshots")
    same_json = d / "json" / "04_recall_same_conversation.json"
    probe_error = str(same).startswith("ERROR")
    if probe_error:
        bad.append(f"WARNING same-conversation probe recorded as {str(same)[:120]!r}; re-read it afterwards")
    if same and not str(same).startswith(("N/A", "ERROR", "DEFERRED")):
        sc = _json(same_json)
        reply = (sc.get("r1_reply") or "").strip()
        if not reply:
            bad.append("same-conversation reply empty")
        earlier = [_json(d / "json" / f).get(k) or "" for f, k in
                   (("02_erase.json", "reply_text"), ("01_inject.json", "reply"), ("01_inject.json", "reply_text"))]
        if reply and any(reply == e.strip() for e in earlier if e):
            bad.append("same-conversation reply identical to an earlier erase/inject reply (stale read)")
    hits = find_sibling_tokens(cell, d / "json")
    if hits:
        bad.append(f"WARNING {sibling_breadcrumb(hits)}")
        notes = str(row[(15 if nlf else 16) - 1] or "")
        if "SIBLING TOKEN EXPOSURE" not in notes:
            bad.append("sibling token in replies but not recorded in the workbook Notes")
    shots = list((d / "screenshots").glob("0[34]_recall_*.png"))
    if len(shots) < (4 if probe_error else 5):
        bad.append(f"only {len(shots)} recall screenshots")
    return bad


def run_check(base: Path) -> tuple[int, list[str]]:
    violations = []
    try:
        cur_t = tracking.load()
    except Exception as exc:
        return 0, [f"run_tracking.json unreadable: {exc}"]
    try:
        cur_sheets, cur_rows = _rows(XLSX)
    except Exception as exc:
        return 0, [f"workbook unreadable: {exc}"]
    base_t = json.loads((base / "run_tracking.json").read_text())
    base_sheets, base_rows = _rows(base / XLSX.name)

    if cur_sheets != base_sheets:
        violations.append(f"workbook sheets changed: {base_sheets} -> {cur_sheets}")
    newly = {c for c, e in cur_t.items()
             if e.get("status") == "recalled" and base_t.get(c, {}).get("status") != "recalled"}
    for c in set(base_t) | set(cur_t):
        if base_t.get(c) != cur_t.get(c) and c not in newly:
            violations.append(f"{c}: tracking changed but cell was not newly recalled")
    # Already-recalled siblings whose token a newly recalled cell surfaced get
    # their outcome updated (sibling_tokens.py outcome rule); allow exactly those.
    surfaced_siblings = set()
    for c in newly:
        d = config.TRANSCRIPTS_DIR / PLATFORMS.get(c[:2], "") / c / "json"
        surfaced_siblings |= {h["sibling"] for h in find_sibling_tokens(c, d)} if d.exists() else set()
    for key in set(base_rows) | set(cur_rows):
        if base_rows.get(key) != cur_rows.get(key) and key[1] not in newly | surfaced_siblings:
            violations.append(f"{key[1]} ({key[0].strip()}): workbook row changed but cell was not newly recalled")
    for c in sorted(newly):
        sheet = "NL FORGET" if "-NLF-" in c else "MASTER "
        for problem in check_cell(c, cur_t[c], cur_rows.get((sheet, c)), sheet):
            violations.append(f"{c}: {problem}")
    return len(newly), violations


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--baseline", type=Path)
    ap.add_argument("--interval", type=int, default=120)
    ap.add_argument("--kill", action="store_true")
    ap.add_argument("--once", action="store_true")
    ns = ap.parse_args()
    if ns.snapshot:
        snapshot(ns.snapshot)
        return
    warned: set[str] = set()
    while True:
        n, problems = run_check(ns.baseline)
        if any("WARNING" not in p for p in problems):
            # Recording a recall writes run_tracking.json first and the
            # workbook a moment later; a check landing in between sees a
            # recalled cell with an empty row (false stop on CL-NLF-I0240,
            # 2026-10-18). Only act on problems that are still there 30 s later.
            time.sleep(30)
            n, problems = run_check(ns.baseline)
        stamp = datetime.now().strftime("%H:%M:%S")
        violations = [p for p in problems if "WARNING" not in p]
        for w in (p for p in problems if "WARNING" in p and p not in warned):
            warned.add(w)
            print(f"[{stamp}] {w}", flush=True)
        if violations:
            for v in violations:
                print(f"[{stamp}] VIOLATION {v}", flush=True)
            if ns.kill:
                STOP_PATH.touch()
                print(f"[{stamp}] stop file written after {n} newly recalled cells; "
                      "each platform exits after its current cell", flush=True)
            return
        print(f"[{stamp}] OK: {n} newly recalled cells, all checks pass", flush=True)
        running = subprocess.run(["pgrep", "-f", SCHEDULER_PATTERN], capture_output=True).returncode == 0
        if ns.once or not running:
            return
        time.sleep(ns.interval)


if __name__ == "__main__":
    main()
