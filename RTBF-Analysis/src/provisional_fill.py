"""Placeholder results for test cases that were run but have no recall result yet.

Section 5 is written on the full base of 865 test cases (67 through UI actions, 798
through prompts). Until Copilot and Gemini recall finishes, 61 of them have no result.
This script fills each of those 61 with a placeholder so the section can be drafted on
the final base, and records every placeholder so it can be replaced by the real result.

Rule: a missing test case takes the most common recall result among the completed test
cases with the same agent, the same part (walkthrough or typed requests) and the same
retention code at injection. The policy verdict for a filled test case follows the
paper's consistency rule from that placeholder and the test case's commitment and
interface change.

The same-conversation reading (did the agent repeat the fact when asked again in the
same chat) is also missing for most Copilot test cases and some Gemini ones. Those are
filled for the typed requests of these two agents so Section 5.4 can be drafted on the
full base. A single most-common value would push every placeholder one way (Copilot's
completed readings are 8 FOUND and 7 NOT FOUND), so the readings are instead allocated
in the observed share within the same agent, part and retention code, in cell order
(largest remainder). Each filled reading is flagged in same_conversation_fill and the
original value is kept in same_conversation_r1_original.

This never touches the real audit. It reads outputs/tables/audit_outcomes.csv and writes
outputs/tables/audit_outcomes_provisional.csv (with provisional_fill and fill_basis
columns) and outputs/results/provisional_fill.md.

Run after src.audit_outcomes, and again after every recall batch; once a cell has a real
result it is no longer filled:
    .venv/bin/python -m src.audit_outcomes && .venv/bin/python -m src.provisional_fill
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

AUDIT_TABLE = Path("outputs/tables/audit_outcomes.csv")
OUT_TABLE = Path("outputs/tables/audit_outcomes_provisional.csv")
OUT_REPORT = Path("outputs/results/provisional_fill.md")

HAS_RESULT = ("RECOVERED", "NOT RECOVERED", "INDETERMINATE")
RUN_STATUSES = ("ERASED", "RECALLED")
GROUP = ["platform", "sheet", "retention"]
SAME_CONV_AGENTS = ("copilot", "gemini")
TYPED_ERASURES = ("NL forget command", "NL forget prompt")
READINGS = ("FOUND", "NOT FOUND")
MISSING_READINGS = ("PENDING", "NOT RECALLED", "")  # N/A means not applicable and is left alone


def fill_same_conversation(table: pd.DataFrame) -> pd.DataFrame:
    """Allocate missing same-conversation readings in the observed share, per group."""
    table["same_conversation_r1_original"] = table["same_conversation_r1"]
    table["same_conversation_fill"] = ""
    typed = (table["sheet"] != "MASTER") | table["erasure"].isin(TYPED_ERASURES)
    in_base = table["run_status"].isin(RUN_STATUSES)
    has = table["same_conversation_r1"].isin(READINGS)
    missing = table["same_conversation_r1"].isin(MISSING_READINGS)
    for _, group in table[typed & in_base & table["platform"].isin(SAME_CONV_AGENTS)].groupby(GROUP):
        gaps = group[missing[group.index]]
        if gaps.empty:
            continue
        agent = group["platform"].iloc[0]
        same_agent = table[typed & in_base & has & (table["platform"] == agent)]
        peers = group[has[group.index]]
        if peers.empty:  # a part with no readings (typed commands on the MASTER sheet): same agent and retention
            peers = same_agent[same_agent["retention"] == group["retention"].iloc[0]]
        if peers.empty:
            peers = same_agent
        if peers.empty:
            raise SystemExit(f"no same-conversation readings to fill from for {group[GROUP].iloc[0].to_dict()}")
        shares = peers["same_conversation_r1"].value_counts(normalize=True)
        exact = {k: shares.get(k, 0.0) * len(gaps) for k in READINGS}
        quota = {k: int(v) for k, v in exact.items()}
        for k in sorted(READINGS, key=lambda k: exact[k] - quota[k], reverse=True)[: len(gaps) - sum(quota.values())]:
            quota[k] += 1
        order = [k for k in READINGS for _ in range(quota[k])]
        for index, value in zip(gaps.sort_values("cell_id").index, order):
            table.loc[index, "same_conversation_r1"] = value
            table.loc[index, "same_conversation_fill"] = (
                f"{group['platform'].iloc[0]} {group['sheet'].iloc[0]} retention {group['retention'].iloc[0]}: "
                f"{', '.join(f'{k} {v}' for k, v in peers['same_conversation_r1'].value_counts().items())}"
            )
    return table


def policy_for(row: pd.Series, outcome: str) -> str:
    """Verdict from the paper's consistency rule, for a placeholder that is never recovered."""
    if outcome != "NOT RECOVERED":
        return "INDETERMINATE"
    if row["commitment"] == "DELETES" and row["interface_change"] != "UNCHANGED":
        return "CONSISTENT"
    return "INDETERMINATE"


def main() -> None:
    table = pd.read_csv(AUDIT_TABLE)
    table["provisional_fill"] = "no"
    table["fill_basis"] = ""

    done = table[table["recoverability"].isin(HAS_RESULT)]
    missing = table[table["run_status"].isin(RUN_STATUSES) & ~table["recoverability"].isin(HAS_RESULT)]

    for index, row in missing.iterrows():
        peers = done[(done[GROUP] == row[GROUP]).all(axis=1)]
        if peers.empty:
            raise SystemExit(f"no completed test cases to fill {row['cell_id']} from ({row[GROUP].to_dict()})")
        counts = peers["recoverability"].value_counts()
        outcome = counts.index[0]
        table.loc[index, "recoverability"] = outcome
        table.loc[index, "policy_consistency"] = policy_for(row, outcome)
        table.loc[index, "provisional_fill"] = "yes"
        shares = ", ".join(f"{k} {v}" for k, v in counts.items())
        table.loc[index, "fill_basis"] = f"{row['platform']} {row['sheet']} retention {row['retention']}: {shares}"

    table = fill_same_conversation(table)
    OUT_TABLE.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUT_TABLE, index=False)

    filled = table[table["provisional_fill"] == "yes"]
    run = table[table["run_status"].isin(RUN_STATUSES)]
    lines = [
        f"test cases run: {len(run)}; with a real result: {len(run) - len(filled)}; filled with a placeholder: {len(filled)}",
        "",
        "recoverability on the full base (placeholders included):",
    ]
    for key, value in run["recoverability"].value_counts().items():
        lines.append(f"  {key:15} {value:4}  {100 * value / len(run):.1f}%")
    lines += ["", "placeholders by agent, part and value:"]
    summary = filled.groupby(["platform", "sheet", "recoverability"]).size()
    lines += [f"  {a:11} {b:10} {c:15} {n}" for (a, b, c), n in summary.items()]
    sc = table[table["same_conversation_fill"] != ""]
    lines += ["", "same-conversation readings filled with a placeholder (agent, reading):"]
    lines += [f"  {a:9} {b:10} {n}" for (a, b), n in sc.groupby(["platform", "same_conversation_r1"]).size().items()]
    lines += ["", "per-cell list:"]
    lines += [f"  {r.cell_id:14} {r.recoverability:14} {r.fill_basis}" for r in filled.itertuples()]
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:14]))
    print(f"\nper-cell table: {OUT_TABLE}\nreport: {OUT_REPORT}")


if __name__ == "__main__":
    main()
