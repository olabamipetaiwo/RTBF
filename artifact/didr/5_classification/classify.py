"""Stage 5: classify each recalled test case (paper, Section 5).

recall success: the value was found by any new-conversation prompt or the UI check.
recall failed:  nothing found, and Storage evidence starts with "yes".
can't tell:     nothing found, and storage was not shown.
"""

from __future__ import annotations

from pathlib import Path

from didr import workbook

RECALL_COLUMNS = ("UI-based check result", "Indirect recall result", "Direct recall result")


def classify_row(results: dict[str, str | None], storage_evidence: str | None) -> str:
    values = [(results.get(c) or "").upper() for c in RECALL_COLUMNS]
    evidence = (storage_evidence or "").strip().lower()
    if any(v.startswith("TOKEN FOUND") for v in values):
        return "recall success"
    if any(v.startswith(("REVIEW", "PARTIAL", "ERROR")) for v in values) or evidence.startswith("review"):
        return "needs review"
    return "recall failed" if evidence.startswith("yes") else "can't tell"


def classify(path: Path | None = None) -> dict[str, int]:
    updates, counts = {}, {}
    for tc in workbook.test_cases(path):
        if tc["Status"] in ("recalled", "classified"):
            outcome = classify_row({c: tc[c] for c in RECALL_COLUMNS}, tc["Storage evidence"])
            updates[tc.id] = {"Recall outcome": outcome, "Status": "classified"}
            counts[outcome] = counts.get(outcome, 0) + 1
    if updates:
        workbook.update(updates, path)
    print(", ".join(f"{k}: {v}" for k, v in sorted(counts.items())) or "No recalled test cases yet.")
    return counts
