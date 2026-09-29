"""Reports rows in accounts.md that disagree with config.py or run_tracking.json.

accounts.md is hand-written and drifted from the code (stale sessions and
emails after the 2026-09-09 account moves, "Not yet set up" on erased cells).
The rows have too many shapes to generate safely, so this checks instead of
rewriting. Run after any account move or erasure; exit code 1 means drift.

    python check_accounts_md.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import config

ROOT = Path(__file__).parent
PLATFORM_PREFIX = {
    "CO": "copilot",
    "CH": "chatgpt",
    "CL": "claude",
    "GE": "gemini",
    "PE": "perplexity",
    "DE": "deepseek",
}
CELL_RE = re.compile(r"`((?:CO|CH|CL|GE|PE|DE)-[A-Z0-9-]+)`")
STRUCK_RE = re.compile(r"~~.*?~~")


def check_row(line_no: int, line: str, tracking: dict) -> list[str]:
    """Checks one table row against the config and tracking for its own cell,
    the first cell ID in the row (later IDs are the cells it conflicts with)."""
    match = CELL_RE.search(line)
    if not match or match.group(1) not in tracking:
        return []
    if any(match.start() >= m.start() and match.end() <= m.end() for m in STRUCK_RE.finditer(line)):
        return []  # struck-through: a row kept only to mark it stale
    struck = STRUCK_RE.sub("", line)
    cell = match.group(1)
    platform = PLATFORM_PREFIX[cell[:2]]
    label = config.MAXIMAL_ACCOUNT_LABEL.get(cell)
    problems: list[str] = []

    if label:
        sessions = re.findall(r"sessions/(\w+?)__(\w+)\.json", struck)
        if sessions and sessions[0][1] != label:
            problems.append(f"session {sessions[0][1]!r}, config says {label!r}")
        email = config.MAXIMAL_ACCOUNT_EMAIL.get((platform, label), "")
        if email and email not in struck:
            problems.append(f"email {email!r} from config is not in the row")

    status = tracking[cell]["status"]
    if re.search(r"not yet set up", struck, re.IGNORECASE) and status != "pending":
        problems.append(f"says 'Not yet set up' but tracking status is {status!r}")
    return [f"accounts.md:{line_no} {cell}: {p}" for p in problems]


def main() -> int:
    tracking = json.loads((ROOT / "data" / "run_tracking.json").read_text())
    lines = (ROOT / "accounts.md").read_text().splitlines()
    problems = [
        p
        for n, line in enumerate(lines, 1)
        if line.startswith("|")
        for p in check_row(n, line, tracking)
    ]
    print("\n".join(problems) if problems else "accounts.md matches config.py and run_tracking.json")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
