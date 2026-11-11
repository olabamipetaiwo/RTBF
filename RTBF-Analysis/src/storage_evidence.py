"""
Storage evidence behind the recall-failed test cases (paper: Outcome Measures, "Of the 232 recall
failed test cases, storage was shown by an interface notification in 225, confirmed only by the
agent in three, and established by direct injection into a saved-memory page in four").

Base: outputs/tables/audit_outcomes_provisional.csv, recoverability NOT RECOVERED. The `retention`
column records the storage signal at injection: `shown` (interface notification), `claimed` (the
agent said it saved the fact); anything else on a recall-failed case can only come from the R2
rule, i.e. an I2/I3 fact injected straight into the saved-memory page whose page was empty at recall
(docs/audit_outcomes.md). The script checks that assumption and fails loudly if it does not hold.

    .venv/bin/python -m src.storage_evidence
"""

import pandas as pd

from src.reporting import save_report

TABLE = "outputs/tables/audit_outcomes_provisional.csv"


def main() -> None:
    d = pd.read_csv(TABLE)
    d = d[d["recoverability"] == "NOT RECOVERED"]
    shown = d[d["retention"] == "shown"]
    claimed = d[d["retention"] == "claimed"]
    direct = d[~d["retention"].isin(["shown", "claimed"])]
    bad = direct[~(direct["injection"].isin(["I2", "I3"]) & (direct["r2"] == "NOT FOUND"))]
    if not bad.empty:
        raise ValueError(f"recall-failed cases with no storage route: {bad['cell_id'].tolist()}")
    lines = [
        f"Base: {len(d)} recall-failed test cases ({TABLE}).",
        f"Shown by an interface notification: {len(shown)}",
        f"Confirmed only by the agent: {len(claimed)}",
        f"Direct injection into a saved-memory page, page empty at recall: {len(direct)} "
        f"({', '.join(direct['cell_id'])})",
    ]
    print(save_report("storage_evidence", lines))


if __name__ == "__main__":
    main()
