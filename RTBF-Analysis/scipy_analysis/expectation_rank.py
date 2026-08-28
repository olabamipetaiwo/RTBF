"""
Rank expectation options (Q4.4/Q5.4, 7 options) and verification options
(Q4.5/Q5.5, 8 options) by selection rate WITHIN each scenario separately (4
ranked lists total), then test whether the rate differences across options
are real or noise.

Confirmed empirically that both question blocks are genuinely select-all:
60-63% of respondents pick >1 expectation option, ~22% pick >1 verification
option, both scenarios. That makes the options related (not independent)
binary measures on the same subjects, so the omnibus test is COCHRAN'S Q --
not a chi-square goodness-of-fit, which would assume independent trials.

If significant: pairwise McNemar between every option pair, Holm-corrected
-- same omnibus -> post-hoc + Holm pattern used throughout this codebase.

Distinct from what already exists:
  - stats.between_scenario_binary: does EACH option's rate shift less->more
    (paired McNemar per option, already ns). This asks a different question:
    within ONE scenario, do options differ from EACH OTHER.
  - verify.py: does each option's rate differ BY DELETION METHOD. This
    ignores method entirely -- aggregate rate across everyone in the scenario.
"""

import itertools
import numpy as np
import pandas as pd
from scipy import stats

from src.screen import get_bases

from .reporting import save_report
from .correction import holm
from .mcnemar_scipy import mcnemar_p

SCEN = {"less": "Q4", "more": "Q5"}
EXP_OPTS = {1: "permanently deleted", 2: "made invisible", 3: "not ref. current",
            4: "not ref. future", 5: "not used for training", 6: "not sure", 7: "other"}
VER_OPTS = {1: "asked same convo", 2: "asked new convo", 3: "checked settings",
            4: "checked UI", 5: "privacy-portal request", 6: "did NOT know how",
            7: "did NOT want to", 8: "other"}
FAMILIES = {"expectation": (".4", EXP_OPTS), "verification": (".5", VER_OPTS)}


def option_matrix(df, q_prefix, opts):
    """n x k binary DataFrame: 1 if that option was selected, 0 otherwise."""
    cols = {label: df[f"{q_prefix}_{i}"].notna().astype(int) for i, label in opts.items()}
    return pd.DataFrame(cols)


def cochrans_q(matrix):
    X = matrix.values.astype(float)
    n, k = X.shape
    col_sums = X.sum(axis=0)
    row_sums = X.sum(axis=1)
    T = col_sums.sum()
    num = k * (k - 1) * np.sum((col_sums - T / k) ** 2)
    den = k * T - np.sum(row_sums ** 2)
    Q = num / den if den != 0 else np.nan
    dof = k - 1
    p = stats.chi2.sf(Q, dof) if Q == Q else np.nan
    return Q, dof, p


def pairwise_posthoc(matrix):
    labels = matrix.columns.tolist()
    pairs = list(itertools.combinations(range(len(labels)), 2))
    rows, pvals = [], []
    for i, j in pairs:
        a, b = matrix.iloc[:, i].values, matrix.iloc[:, j].values
        both = int(((a == 1) & (b == 1)).sum())
        neither = int(((a == 0) & (b == 0)).sum())
        a_only = int(((a == 1) & (b == 0)).sum())
        b_only = int(((a == 0) & (b == 1)).sum())
        table = [[neither, b_only], [a_only, both]]
        _, p = mcnemar_p(table)
        rows.append((labels[i], labels[j], a_only, b_only, p)); pvals.append(p)
    padj = holm(pvals)
    return pd.DataFrame(
        [{"opt_a": a, "opt_b": b, "a_only": ao, "b_only": bo,
          "p_raw": round(p, 4), "p_holm": round(pa, 4), "sig": "*" if pa < 0.05 else ""}
         for (a, b, ao, bo, p), pa in zip(rows, padj)]
    )


def rank_and_test(bases, scen, family, lines):
    base = SCEN[scen]
    q_suffix, opts = FAMILIES[family]
    df = bases[scen]
    matrix = option_matrix(df, f"{base}{q_suffix}", opts)
    n = len(matrix)

    rates = (matrix.sum(axis=0) / n * 100).sort_values(ascending=False)
    Q, dof, p = cochrans_q(matrix)

    lines.append("\n" + "=" * 66)
    lines.append(f"[{scen}] {family.upper()} (n={n}) -- ranked by selection rate")
    lines.append("=" * 66)
    lines.append(rates.round(1).to_string())
    lines.append(f"\nCochran's Q={Q:.2f}  df={dof}  p={p:.4g}  -> {'SIG' if p < 0.05 else 'ns'}")

    if p >= 0.05:
        lines.append("    -> ns: apparent ranking is not distinguishable from a flat distribution")
        return f"[{scen}] {family}", p

    posthoc = pairwise_posthoc(matrix[rates.index])  # reorder columns by rank for readability
    lines.append(f"\n    post-hoc (pairwise McNemar + Holm across {len(posthoc)} pairs):")
    sig_pairs = posthoc[posthoc["sig"] == "*"]
    lines.append(sig_pairs.to_string(index=False) if len(sig_pairs) else
                 "    (no individual pair survives Holm correction)")
    return f"[{scen}] {family}", p


def cochran_rank(bases, lines=None):
    """4 tests (expectation/verification x less/more). Returns [(label, p_raw)]
    for the global registry -- omnibus only, post-hoc excluded per convention."""
    if lines is None:
        lines = []
    return [rank_and_test(bases, scen, family, lines)
            for scen in SCEN for family in FAMILIES]


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    lines = []
    cochran_rank(bases, lines)

    for line in lines:
        print(line)

    report_path = save_report("expectation_rank", lines)
    print(f"\nreport saved -> {report_path}")
