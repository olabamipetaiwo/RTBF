"""
Recall outcomes for every agent and data deletion method (rebuttal table, not in the paper).

Base: the 865 test cases in outputs/tables/audit_outcomes_provisional.csv, loaded through
src.outcomes_by_agent.load(). Each cell reads recall success / recall failed / can't tell; a dash
means the method was not tested on that agent. The deletion-request prompt row holds the 798
prompt-based test cases plus the 13 UI-action cases requested through chat (811 in all), as in
Table tab:expectation-outcome. The script checks that the cells add up to 162 / 232 / 471.

    .venv/bin/python -m src.outcomes_agent_by_method
"""

import pandas as pd

from src.outcomes_by_agent import ORDER, load
from src.expectation_gap import PLATFORM_NAMES, TYPED
from src.reporting import save_report

ROWS = {  # label -> predicate on the loaded frame, in report order
    "Deletion-request prompt": lambda d: d["method"] == TYPED,
    "Deleting a single conversation": lambda d: d["method"] == "Delete this single conversation.",
    "Clearing all conversation history": lambda d: d["method"] == "Clear all conversation history.",
    "Deleting a specific saved memory": lambda d: d["method"] == "Delete a specific saved memory or fact.",
    "Clearing all saved memories": lambda d: d["method"] == "Clear all saved memories.",
    "Account-level privacy dashboard": lambda d: d["method"].str.startswith("Privacy dashboard"),
    "Most extensive deletion procedure": lambda d: d["erasure"] == "MAXIMAL",
    "Clearing custom instructions": lambda d: d["erasure"] == "Clear custom instructions",
}
EXPECTED = {"success": 162, "failed": 232, "cant": 471}


def cell(d: pd.DataFrame) -> str:
    if d.empty:
        return "–"
    c = d["outcome"].value_counts()
    return f"{c.get('success', 0)} / {c.get('failed', 0)} / {c.get('cant', 0)}"


def main() -> None:
    df = load()
    covered = pd.Series(False, index=df.index)
    lines = [
        f"Base: {len(df)} test cases. Cells: recall success / recall failed / can't tell; – = not tested.",
        "",
        "| Method | " + " | ".join(PLATFORM_NAMES[p] for p in ORDER) + " |",
        "|---|" + "---|" * len(ORDER),
    ]
    for label, pick in ROWS.items():
        mask = pick(df)
        covered |= mask
        lines.append(f"| {label} | " + " | ".join(cell(df[mask & (df["platform"] == p)]) for p in ORDER) + " |")
    if not covered.all() or covered.sum() != len(df):
        raise ValueError(f"test cases in no row: {df.loc[~covered, 'cell_id'].tolist()}")
    totals = df["outcome"].value_counts().to_dict()
    if totals != EXPECTED:
        raise ValueError(f"totals {totals} differ from the paper's {EXPECTED}")
    lines += ["", f"Totals: {totals['success']} / {totals['failed']} / {totals['cant']} (matches the paper)."]
    print(save_report("outcomes_agent_by_method", lines))


if __name__ == "__main__":
    main()
