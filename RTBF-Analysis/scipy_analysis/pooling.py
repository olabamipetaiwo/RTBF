"""
Task 2 -- pool each method's respondents across both scenarios into one
long-format dataset, for the next task's pooled (both-scenarios) Kruskal-
Wallis. Naive concatenation of less+more would double-count any respondent
who used the SAME method in both scenarios (breaks KW's independent-
observations assumption). Per-respondent rule (paired base, n=177):

  - same method in both scenarios (a "stayer"): average their less- and
    more-scenario scale scores into ONE observation in that method's group.
  - different method per scenario (a "switcher"): less-scenario rating and
    more-scenario rating are genuinely about two different methods, so each
    becomes its own independent observation in its own method's group --
    nothing double-counted within a group.
  - "Other (Please specify)" is filtered per scenario independently (same
    convention as stats.between_method / stats.method_switching), so a
    respondent who answered "Other" in one scenario but a real method in
    the other still contributes that scenario's observation.

Residual caveat (documented, not solved): a switcher still contributes to
TWO different groups. Milder than double-counting within one group, and an
unavoidable feature of pooling within-subject data -- reported alongside
the pooled n's below, not silently absorbed.
"""

import pandas as pd

from src.screen import get_bases
from src.stats import SCALES, scale_score, SCEN

from .reporting import save_report
from .mcnemar import METHODS, SHORT

OTHER = "Other (Please specify)"


def pooled_method_scores(bases):
    """Long-format DataFrame: one row per pooled observation.

    Columns: method, protection, effort, benefit_loss, source
    ("stayed" | "switched_less" | "switched_more" | "less_only" | "more_only").
    """
    paired = bases["paired"]
    less_base = SCEN["less"][0]   # "Q4"
    more_base = SCEN["more"][0]   # "Q5"
    less_scores = {s: scale_score(paired, less_base, q, k) for s, (q, k) in SCALES.items()}
    more_scores = {s: scale_score(paired, more_base, q, k) for s, (q, k) in SCALES.items()}

    rows = []
    for i in paired.index:
        m_less, m_more = paired.at[i, "Q4.2"], paired.at[i, "Q5.2"]
        has_less = pd.notna(m_less) and m_less != OTHER
        has_more = pd.notna(m_more) and m_more != OTHER

        if has_less and has_more and m_less == m_more:
            row = {"method": m_less, "source": "stayed"}
            for s in SCALES:
                row[s] = (less_scores[s].loc[i] + more_scores[s].loc[i]) / 2
            rows.append(row)
        else:
            if has_less:
                row = {"method": m_less, "source": "switched_less" if has_more else "less_only"}
                row.update({s: less_scores[s].loc[i] for s in SCALES})
                rows.append(row)
            if has_more:
                row = {"method": m_more, "source": "switched_more" if has_less else "more_only"}
                row.update({s: more_scores[s].loc[i] for s in SCALES})
                rows.append(row)

    return pd.DataFrame(rows)


def pooled_n_summary(pooled, bases):
    """Per-method: n_less, n_more (original, unfiltered-by-N_FLOOR), n_stayed,
    n_switched, n_solo, n_pooled -- the caveat-documenting table."""
    less_n = bases["less"][bases["less"]["Q4.2"] != OTHER]["Q4.2"].value_counts()
    more_n = bases["more"][bases["more"]["Q5.2"] != OTHER]["Q5.2"].value_counts()
    rows = []
    for m in METHODS:
        sub = pooled[pooled["method"] == m]
        n_stayed = (sub["source"] == "stayed").sum()
        n_switched = sub["source"].isin(["switched_less", "switched_more"]).sum()
        n_solo = sub["source"].isin(["less_only", "more_only"]).sum()
        rows.append({
            "method": SHORT[m],
            "n_less": int(less_n.get(m, 0)),
            "n_more": int(more_n.get(m, 0)),
            "n_stayed": int(n_stayed),
            "n_switched": int(n_switched),
            "n_solo": int(n_solo),
            "n_pooled": len(sub),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    pooled = pooled_method_scores(bases)
    summary = pooled_n_summary(pooled, bases)

    lines = ["\n" + "=" * 70, "TASK 2  POOLED METHOD GROUPS (less+more, deduped per respondent)", "=" * 70]
    lines.append("\n" + summary.to_string(index=False))
    lines.append(
        "\nn_pooled = n_stayed (1 obs, averaged) + n_switched (1 obs each, "
        "un-averaged) + n_solo (answered only one scenario's method question). "
        "Caveat: a switcher contributes to TWO different method groups -- milder "
        "than double-counting within one group, unavoidable for pooled "
        "within-subject data."
    )

    for line in lines:
        print(line)

    report_path = save_report("pooling", lines)
    print(f"\nreport saved -> {report_path}")

    table_path = "scipy_analysis/outputs/tables/pooled_method_scores.csv"
    pooled.to_csv(table_path, index=False)
    print(f"pooled table saved -> {table_path}")
