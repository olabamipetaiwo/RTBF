"""
Scenario-order check (task C5). The two scenario blocks (LS weather, MS health)
were shown in random order by a Qualtrics block randomizer; the 2026-10-19
re-export records each respondent's order in FL_20_DO_WeatherScenario
("1" = weather/LS shown first, "2" = health/MS shown first).

Standard check for a two-condition within-subject design with randomized order:
  1. balance of the split: scipy.stats.binomtest against 0.5;
  2. order effect on the scenario shift: each participant's MS - LS difference,
     compared between the two order groups with scipy.stats.mannwhitneyu
     (a scenario x order interaction), Holm across the four rating outcomes;
  3. method switching between scenarios by order: scipy.stats.fisher_exact.
A null in (2) and (3) means the order participants saw the scenarios in did
not change the scenario differences the paper reports.
"""

import pandas as pd
from scipy import stats

from src.screen import get_bases
from src.stats import SCALES, scale_score, rank_biserial_indep

from .correction import holm
from .reporting import save_report
from .willingness import WILLING

ORDER_COL = "FL_20_DO_WeatherScenario"
ORDER = {"1": "LS first", "2": "MS first"}


def shifts(paired):
    """Per-participant MS - LS difference for willingness and the three scales."""
    out = {"willingness": paired["Q5.10"].map(WILLING) - paired["Q4.10"].map(WILLING)}
    for scale, (q, k) in SCALES.items():
        out[scale] = scale_score(paired, "Q5", q, k) - scale_score(paired, "Q4", q, k)
    return pd.DataFrame(out)


def main():
    paired = get_bases(verbose=False)["paired"]
    order = paired[ORDER_COL].astype(str).map(ORDER)
    lines = ["=== Scenario order check (LS = weather, MS = health) ==="]

    counts = order.value_counts()
    n_ls, n = int(counts.get("LS first", 0)), int(order.notna().sum())
    missing = len(paired) - n
    bt = stats.binomtest(n_ls, n, 0.5)
    lines.append(f"\n1. Split (n={n} of {len(paired)} paired; order missing for {missing})")
    lines.append(f"   LS first: {n_ls}   MS first: {n - n_ls}")
    lines.append(f"   binomial test vs 50/50: p={bt.pvalue:.4f}  -> {'UNEVEN' if bt.pvalue < 0.05 else 'even'}")

    lines.append("\n2. Scenario shift (MS - LS) by order: Mann-Whitney U, Holm x4")
    d = shifts(paired)
    rows, pvals = [], []
    for col in d.columns:
        ls_first = d.loc[order == "LS first", col].dropna()
        ms_first = d.loc[order == "MS first", col].dropna()
        u, p = stats.mannwhitneyu(ls_first, ms_first, alternative="two-sided")
        rows.append((col, len(ls_first), ls_first.mean(), len(ms_first), ms_first.mean(), u,
                     rank_biserial_indep(ls_first, ms_first), p))
        pvals.append(p)
    for (col, n1, m1, n2, m2, u, r, p), pa in zip(rows, holm(pvals)):
        lines.append(f"   [{col}] mean shift LS-first={m1:+.3f} (n={n1})  MS-first={m2:+.3f} (n={n2})")
        lines.append(f"       U={u:.1f}  r={r}  p_raw={p:.4f}  p_holm={pa:.4f}  -> {'SIG' if pa < 0.05 else 'ns'}")

    lines.append("\n3. Changed method between scenarios, by order: Fisher's exact")
    switched = paired["Q4.2"] != paired["Q5.2"]
    tab = pd.crosstab(order, switched).reindex(index=["LS first", "MS first"], columns=[False, True], fill_value=0)
    odds, p = stats.fisher_exact(tab.values)
    for grp in tab.index:
        k, tot = int(tab.loc[grp, True]), int(tab.loc[grp].sum())
        lines.append(f"   {grp}: switched {k}/{tot} ({100 * k / tot:.1f}%)")
    lines.append(f"   odds ratio={odds:.3f}  p={p:.4f}  -> {'SIG' if p < 0.05 else 'ns'}")

    holm_max = max(holm(pvals))
    lines.append("\nAs reported in the paper (Methods, Missingness and aggregation):")
    lines.append(f"   {n_ls} LS first, {n - n_ls} MS first; binomial p={bt.pvalue:.2f}".replace("0.", "."))
    lines.append(f"   shift by order: all p_Holm={holm_max:.2f} (lowest {min(holm(pvals)):.2f})".replace("0.", "."))
    lines.append(f"   changed method by order: Fisher's exact p={p:.2f}".replace("0.", "."))

    for line in lines:
        print(line)
    print(f"report saved -> {save_report('scenario_order', lines)}")


if __name__ == "__main__":
    main()
