"""
What each recall check (R1 direct, R2 settings page, R3 indirect) adds, for the
paper's justification of the three checks (Methods, recall checks).

Reads outputs/tables/audit_outcomes.csv (run src.audit_outcomes first). For the
cells scored recall success (RECOVERED) it counts which checks found the token,
and how many cells only one check found. The remaining recall-success cells were
settled by the sibling rule (a sibling cell's token surfaced), not by a check.

    .venv/bin/python -m src.recall_check_value
"""

import pandas as pd

from src.reporting import save_report

TABLE = "outputs/tables/audit_outcomes.csv"


def main() -> None:
    d = pd.read_csv(TABLE)
    for c in ("r1", "r2", "r3"):
        d[c.upper()] = d[c].eq("FOUND")
    lines = ["Which recall checks found the token (recall-success cells only)."]
    for sheet, g in d[d.recoverability.eq("RECOVERED")].groupby("sheet"):
        by_check = g[g.R1 | g.R2 | g.R3]
        lines += [
            "",
            f"-- {sheet.strip()} --",
            f"recall success cells: {len(g)}",
            f"settled by a check: {len(by_check)}; settled by the sibling rule: {len(g) - len(by_check)}",
            f"found by R1: {int(by_check.R1.sum())}",
            f"found by R2: {int(by_check.R2.sum())}",
            f"found by R3: {int(by_check.R3.sum())}",
            f"found by R1 only: {int((by_check.R1 & ~by_check.R2 & ~by_check.R3).sum())}",
            f"found by R2 only: {int((by_check.R2 & ~by_check.R1 & ~by_check.R3).sum())}",
            f"found by R3 only: {int((by_check.R3 & ~by_check.R1 & ~by_check.R2).sum())}",
            f"R1 missed, found by R2 or R3: {int((~by_check.R1).sum())}",
        ]
    lines += ["", "R2 scoring across all cells (platform: not applicable / found):"]
    for p, g in d.groupby("platform"):
        na = int(g.r2.isna().sum() + g.r2.fillna("").str.startswith(("N/A", "NOT RECALL")).sum())
        lines.append(f"  {p}: no R2 result {na}, found {int(g.R2.sum())} of {len(g)}")
    print("\n".join(lines))
    print(f"report saved -> {save_report('recall_check_value', lines)}")


if __name__ == "__main__":
    main()
