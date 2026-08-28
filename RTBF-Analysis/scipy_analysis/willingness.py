"""
Scipy-only reimplementation of src/willingness.py. scenario_shift uses
scipy.stats.wilcoxon + effects.matched_rank_biserial (was pingouin.wilcoxon);
willingness_by_method uses kruskal (already scipy) + scipy_analysis.dunn
(was scikit-posthocs).
"""

import itertools
import pandas as pd
from scipy import stats

from src.screen import get_bases
from src.stats import eps2, rank_biserial_indep, N_FLOOR, SCEN as METHOD_SCEN

from .reporting import save_report
from .dunn import dunn_test
from .effects import matched_rank_biserial

WILLING = {"Definitely not": 1, "Probably not": 2, "Might or might not": 3,
           "Probably yes": 4, "Definitely yes": 5}
WILLING_COL = {"less": "Q4.10", "more": "Q5.10"}


def scenario_shift(paired):
    less = paired["Q4.10"].map(WILLING)
    more = paired["Q5.10"].map(WILLING)
    m = pd.concat([less, more], axis=1).dropna()
    m.columns = ["less", "more"]

    d = (m["more"] - m["less"])
    w_stat, p = stats.wilcoxon(m["more"], m["less"])
    rbc = matched_rank_biserial(d.values)
    mean_diff = d.mean()

    lines = ["=== Willingness to delete: less vs more sensitive (paired Wilcoxon) ==="]
    lines.append(f"n pairs        : {len(m)}")
    lines.append(f"mean willing (less): {m['less'].mean():.3f}   (more): {m['more'].mean():.3f}")
    lines.append(f"mean_diff      : {mean_diff:+.3f}  ({'more>less' if mean_diff>0 else 'less>more'})")
    lines.append(f"W              : {float(w_stat):.1f}")
    lines.append(f"p-value        : {p:.4f}   RBC r={rbc:+.3f}")
    lines.append(f"verdict        : {'SIG' if p < 0.05 else 'ns'}")

    lines.append("\nwillingness distribution (count):")
    dist = pd.DataFrame({
        "less": m["less"].value_counts().reindex(range(1, 6), fill_value=0).values,
        "more": m["more"].value_counts().reindex(range(1, 6), fill_value=0).values,
    }, index=[k for k, _ in sorted(WILLING.items(), key=lambda x: x[1])])
    lines.append(dist.to_string())
    return lines, [("[scenario shift] willingness", p)]


def willingness_by_method(bases):
    lines = ["\n" + "=" * 60, "WILLINGNESS BY METHOD (Kruskal-Wallis -> Dunn's + Holm)", "=" * 60]
    pvals = []
    for scen, (_, mcol) in METHOD_SCEN.items():
        df = bases[scen].copy()
        df = df[df[mcol] != "Other (Please specify)"]
        df["_w"] = df[WILLING_COL[scen]].map(WILLING)
        counts = df[mcol].value_counts()
        kept = counts[counts >= N_FLOOR].index.tolist()
        groups = {m: df.loc[df[mcol] == m, "_w"].dropna().values for m in kept}
        H, p = stats.kruskal(*groups.values())
        n_tot = sum(len(v) for v in groups.values())
        sig = p < 0.05
        pvals.append((f"[{scen}] willingness by method KW", p))
        lines.append(f"\n[{scen}] KW  H={H:.2f}  p={p:.4f}  "
                      f"eps2={eps2(H, n_tot, len(kept))}  -> {'SIG' if sig else 'ns'}")
        if not sig:
            continue
        long = df[df[mcol].isin(kept)][[mcol, "_w"]].dropna()
        dunn = dunn_test(long, val_col="_w", group_col=mcol)
        for m1, m2 in itertools.combinations(kept, 2):
            pv = dunn.loc[m1, m2]
            if pv < 0.05:
                r = rank_biserial_indep(groups[m1], groups[m2])
                lines.append(f"    * {m1[:28]:28} vs {m2[:28]:28} "
                              f"p_holm={pv:.4f}  r={r}")
    return lines, pvals


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    paired = bases["paired"]

    lines, _p1 = scenario_shift(paired)
    more_lines, _p2 = willingness_by_method(bases)
    lines += more_lines

    for line in lines:
        print(line)

    report_path = save_report("willingness", lines)
    print(f"\nreport saved -> {report_path}")
