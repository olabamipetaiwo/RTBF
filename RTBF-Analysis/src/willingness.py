"""
Step 7 (remaining piece): willingness-to-delete across scenarios and across methods.
Q4.10/Q5.10 = single 5-point ordinal item ("Definitely not"..."Definitely yes").

  Q1 (scenario): are users more willing to delete when the data is more sensitive?
     Same 177 respondents -> paired Wilcoxon signed-rank, matched rank-biserial effect.
  Q2 (method, new): does willingness differ by WHICH deletion method someone used?
     Independent groups (method choice), per scenario -> Kruskal-Wallis + Dunn's/Holm,
     mirroring stats.py's between_method design for protection/effort/benefit_loss.

The other step-7 pieces (score Wilcoxon, expectation/verification McNemar,
method-shift transition matrix + Stuart-Maxwell) are already in stats_all.py.
"""

import itertools
import pandas as pd
import pingouin as pg
from scipy import stats
import scikit_posthocs as sp
from src.screen import get_bases
from src.reporting import save_report
from src.stats import eps2, rank_biserial_indep, N_FLOOR, SCEN as METHOD_SCEN

WILLING = {"Definitely not": 1, "Probably not": 2, "Might or might not": 3,
           "Probably yes": 4, "Definitely yes": 5}
WILLING_COL = {"less": "Q4.10", "more": "Q5.10"}


def scenario_shift(paired):
    less = paired["Q4.10"].map(WILLING)
    more = paired["Q5.10"].map(WILLING)
    m = pd.concat([less, more], axis=1).dropna()
    m.columns = ["less", "more"]

    res = pg.wilcoxon(m["more"], m["less"])
    p = float(res["p_val"].iloc[0]) if "p_val" in res else float(res["p-val"].iloc[0])
    rbc = float(res["RBC"].iloc[0])
    mean_diff = (m["more"] - m["less"]).mean()

    lines = ["=== Willingness to delete: less vs more sensitive (paired Wilcoxon) ==="]
    lines.append(f"n pairs        : {len(m)}")
    lines.append(f"mean willing (less): {m['less'].mean():.3f}   (more): {m['more'].mean():.3f}")
    lines.append(f"mean_diff      : {mean_diff:+.3f}  ({'more>less' if mean_diff>0 else 'less>more'})")
    lines.append(f"W              : {float(res['W_val'].iloc[0]):.1f}")
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
        dunn = sp.posthoc_dunn(long, val_col="_w", group_col=mcol, p_adjust="holm")
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