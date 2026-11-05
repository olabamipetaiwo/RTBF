"""Section 5.4 table: what participants expected, beside what the test found, by method.

For each of the four most chosen data deletion methods (the four Section 4 reports),
shows the share of Pooled survey responses that expected the fact not to come up in
future conversations, next to the outcomes of the test cases that used the same method.
The expectation is the one a recall test in a new conversation can speak to: recall
success contradicts it, recall failed is consistent with it. The two bases differ
(responses vs test cases), so the percentages are not compared directly.

Reads outputs/tables/pooled_obs_expectation_pct.csv (survey) and, through
src.outcomes_by_agent, outputs/tables/audit_outcomes_provisional.csv (placeholders
included). Writes:
    outputs/tables/expectation_vs_outcome.tex   (body rows for the Section 5.4 table)
    outputs/results/expectation_vs_outcome.md   (every number quoted in Section 5.4 paragraph 1)

AS IT STANDS: re-run after every recall batch:
    .venv/bin/python -m src.audit_outcomes && .venv/bin/python -m src.provisional_fill \
        && .venv/bin/python -m src.expectation_vs_outcome
"""

from datetime import datetime
from pathlib import Path

import pandas as pd

from src.expectation_gap import TYPED
from src.outcomes_by_agent import UI_METHODS, counts, load

SURVEY = Path("outputs/tables/pooled_obs_expectation_pct.csv")
OUT_TEX = Path("outputs/tables/expectation_vs_outcome.tex")
OUT_MD = Path("outputs/results/expectation_vs_outcome.md")
FUTURE = "not referenced in future convo"
PERMANENT = "permanently deleted"

# (row label, survey method, test-case method key), in the order Section 4 reports them
METHODS = [
    ("Delete a single conversation", UI_METHODS["Deleting a single conversation"], UI_METHODS["Deleting a single conversation"]),
    ("Clear all conversation history", UI_METHODS["Clearing all conversation history"], UI_METHODS["Clearing all conversation history"]),
    ("Delete a specific saved memory", UI_METHODS["Deleting a specific saved memory"], UI_METHODS["Deleting a specific saved memory"]),
    ("Send a deletion-request prompt", TYPED, TYPED),
]


def main() -> None:
    survey = pd.read_csv(SURVEY).set_index("method")
    df = load()
    rows, md = [], []
    for label, survey_key, test_key in METHODS:
        s = survey.loc[survey_key]
        c = counts(df[df["method"] == test_key])
        n = int(c.sum())
        rows.append(
            f"{label} & {s[FUTURE]:.1f}\\% & {c['success']} & {c['failed']} & {c['cant']} & {n} \\\\"
        )
        md.append(
            f"| {label} | {int(s['n_obs'])} | {s[FUTURE]:.1f}% | {s[PERMANENT]:.1f}% | {n} | "
            f"{c['success']} | {c['failed']} | {c['cant']} |"
        )
    OUT_TEX.write_text("\n".join(rows) + "\n")
    future = [survey.loc[k][FUTURE] for _, k, _ in METHODS]
    perm = [survey.loc[k][PERMANENT] for _, k, _ in METHODS]
    lines = [
        "# expectation_vs_outcome",
        "",
        f"_Run at {datetime.now().isoformat(timespec='seconds')}_",
        "",
        f"Sources: {SURVEY} (Pooled responses) and the provisional audit table (placeholders included).",
        "",
        "| Method | Responses | Expect not in future conversations | Expect permanent deletion | Test cases | Recall success | Recall failed | Can't tell |",
        "|---|---|---|---|---|---|---|---|",
        *md,
        "",
        f"Expect not in future conversations: {min(future):.1f}% to {max(future):.1f}% across the four methods.",
        f"Expect permanent deletion: {min(perm):.1f}% to {max(perm):.1f}%.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
