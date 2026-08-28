"""
Scipy-only reimplementation of src/stats.py (steps 1-6), for cross-checking
against the original pipeline. Data prep (scale scoring, N_FLOOR, effect-size
formulas that are already scipy-based) is reused from src.stats -- only the
test/post-hoc/correction layer is reimplemented here:

  Kruskal-Wallis      -> scipy.stats.kruskal              (same as original)
  Dunn's post-hoc     -> scipy_analysis.dunn               (was scikit-posthocs)
  Shapiro / paired-t  -> scipy.stats.shapiro / ttest_rel    (same as original)
  Wilcoxon + RBC      -> scipy.stats.wilcoxon + effects.matched_rank_biserial
                         (was pingouin.wilcoxon)
  McNemar             -> mcnemar_scipy.mcnemar_p            (was statsmodels)
  Stuart-Maxwell      -> hand-rolled (numpy + scipy.stats.chi2)
                         (was statsmodels SquareTable.homogeneity)
  Holm correction     -> scipy_analysis.correction.holm     (was statsmodels)

Same section numbering and (family, label) strings as src/stats.py so results
join row-for-row in compare.py.
"""

import itertools
import numpy as np
import pandas as pd
from scipy import stats

from src.screen import get_bases
from src.stats import scale_score, SCALES, SCEN, N_FLOOR, eps2, rank_biserial_indep

from .reporting import save_report
from .dunn import dunn_test
from .correction import holm
from .mcnemar_scipy import mcnemar_p
from .effects import matched_rank_biserial


# ---------- 1 & 2 : between-method ----------
def between_method(bases, lines):
    lines.append("\n" + "=" * 70)
    lines.append("STEPS 1-2  BETWEEN-METHOD (Kruskal-Wallis -> Dunn's + Holm)")
    lines.append("=" * 70)
    omnibus_pvals = []
    for scen, (base, mcol) in SCEN.items():
        df = bases[scen].copy()
        df = df[df[mcol] != "Other (Please specify)"]
        counts = df[mcol].value_counts()
        kept = counts[counts >= N_FLOOR].index.tolist()
        for scale, (q, k) in SCALES.items():
            df["_s"] = scale_score(df, base, q, k)
            groups = {m: df.loc[df[mcol] == m, "_s"].dropna().values for m in kept}
            H, p = stats.kruskal(*groups.values())
            n_tot = sum(len(v) for v in groups.values())
            sig = p < 0.05
            omnibus_pvals.append((f"[{scen}|{scale}] method KW", p))
            lines.append(f"\n[{scen} | {scale}] KW  H={H:.2f}  p={p:.4f}  "
                          f"eps2={eps2(H, n_tot, len(kept))}  -> {'SIG' if sig else 'ns'}")
            if not sig:
                continue
            long = df[df[mcol].isin(kept)][[mcol, "_s"]].dropna()
            dunn = dunn_test(long, val_col="_s", group_col=mcol)
            for m1, m2 in itertools.combinations(kept, 2):
                pv = dunn.loc[m1, m2]
                if pv < 0.05:
                    r = rank_biserial_indep(groups[m1], groups[m2])
                    lines.append(f"    * {m1[:28]:28} vs {m2[:28]:28} "
                                  f"p_holm={pv:.4f}  r={r}")
    return omnibus_pvals


# ---------- 3 & 4 : between-scenario, Likert ----------
def between_scenario_likert(paired, lines):
    lines.append("\n" + "=" * 70)
    lines.append("STEPS 3-4  BETWEEN-SCENARIO Likert (Shapiro -> t/Wilcoxon, Holm x3)")
    lines.append("=" * 70)
    pvals, results = [], []
    for scale, (q, k) in SCALES.items():
        less = scale_score(paired, "Q4", q, k)
        more = scale_score(paired, "Q5", q, k)
        d = (more - less).dropna()
        _, p_norm = stats.shapiro(d)
        normal = p_norm > 0.05
        if normal:
            t, p = stats.ttest_rel(more.loc[d.index], less.loc[d.index])
            dz = round(d.mean() / d.std(ddof=1), 3)
            test, stat, es = "paired-t", round(t, 3), f"dz={dz}"
        else:
            w_stat, p = stats.wilcoxon(more.loc[d.index], less.loc[d.index])
            rb = round(matched_rank_biserial(d.values), 3)
            test, stat, es = "Wilcoxon", round(float(w_stat), 1), f"r={rb}"
        pvals.append(p)
        results.append((scale, test, normal, stat, es, d.mean()))
    padj = holm(pvals)
    for (scale, test, normal, stat, es, mdiff), p_adj, p_raw in zip(results, padj, pvals):
        arrow = "more>less" if mdiff > 0 else "less>more"
        lines.append(f"\n[{scale}] shapiro_normal={normal}  {test}  stat={stat}  "
                      f"{es}  mean_diff={mdiff:+.3f} ({arrow})")
        lines.append(f"    p_raw={p_raw:.4f}  p_holm={p_adj:.4f}  "
                      f"-> {'SIG' if p_adj < 0.05 else 'ns'}")
    return [(f"[{scale}] scenario {test}", p) for (scale, test, *_r), p in zip(results, pvals)]


# ---------- 5 : between-scenario, binary (McNemar) ----------
def between_scenario_binary(paired, lines):
    lines.append("\n" + "=" * 70)
    lines.append("STEP 5  BETWEEN-SCENARIO binary: McNemar per option")
    lines.append("=" * 70)
    blocks = {"expectation (Q4.4/Q5.4)": ("Q4.4", "Q5.4", 7),
              "verification (Q4.5/Q5.5)": ("Q4.5", "Q5.5", 8)}
    all_pvals = []
    for label, (a, b, nopt) in blocks.items():
        lines.append(f"\n-- {label} --")
        rows, pvals = [], []
        for i in range(1, nopt + 1):
            la, lb = f"{a}_{i}", f"{b}_{i}"
            sel_less = paired[la].notna().astype(int)
            sel_more = paired[lb].notna().astype(int)
            b_cell = int(((sel_less == 1) & (sel_more == 0)).sum())
            c_cell = int(((sel_less == 0) & (sel_more == 1)).sum())
            tbl = [[int(((sel_less == 0) & (sel_more == 0)).sum()), c_cell],
                   [b_cell, int(((sel_less == 1) & (sel_more == 1)).sum())]]
            _, p = mcnemar_p(tbl)
            rows.append((i, b_cell, c_cell, p)); pvals.append(p)
            all_pvals.append((f"[scenario shift] {label} opt{i}", p))
        padj = holm(pvals)
        for (i, bcell, ccell, _), pa in zip(rows, padj):
            direction = "more>less" if ccell > bcell else "less>more"
            flag = "SIG" if pa < 0.05 else "ns"
            lines.append(f"    opt{i}: less-only={bcell:3d} more-only={ccell:3d} "
                          f"({direction})  p_holm={pa:.4f}  {flag}")
    return all_pvals


# ---------- 6 : method switching ----------
def _stuart_maxwell(tab):
    tab = tab.astype(float).copy()
    if tab.min() == 0:
        # statsmodels SquareTable(..., shift_zeros=True) (the default used by
        # the original pipeline) replaces zero cells with 0.5 before testing.
        tab[tab == 0] = 0.5
    r = tab.shape[0]
    row_sum = tab.sum(axis=1).astype(float)
    col_sum = tab.sum(axis=0).astype(float)
    d = (row_sum - col_sum)[:-1]
    V = np.zeros((r - 1, r - 1))
    for i in range(r - 1):
        V[i, i] = row_sum[i] + col_sum[i] - 2 * tab[i, i]
        for j in range(r - 1):
            if i != j:
                V[i, j] = -(tab[i, j] + tab[j, i])
    stat = float(d @ np.linalg.inv(V) @ d)
    df = r - 1
    p = stats.chi2.sf(stat, df)
    return stat, df, p


def method_switching(paired, lines):
    lines.append("\n" + "=" * 70)
    lines.append("STEP 6  METHOD SWITCHING (Q4.2->Q5.2): Stuart-Maxwell + transitions")
    lines.append("=" * 70)
    d = paired[["Q4.2", "Q5.2"]].dropna()
    d = d[(d["Q4.2"] != "Other (Please specify)") & (d["Q5.2"] != "Other (Please specify)")]
    cats = sorted(set(d["Q4.2"]) | set(d["Q5.2"]))
    tab = pd.crosstab(d["Q4.2"], d["Q5.2"]).reindex(index=cats, columns=cats, fill_value=0)
    stayed = int(np.trace(tab.values)); total = int(tab.values.sum())
    lines.append(f"\nstayed on same method: {stayed}/{total} ({100*stayed/total:.0f}%)  "
                  f"switched: {total-stayed} ({100*(total-stayed)/total:.0f}%)")
    sm_pval = None
    try:
        stat, df, p = _stuart_maxwell(tab.values.astype(float))
        sm_pval = p
        lines.append(f"Stuart-Maxwell marginal homogeneity: stat={stat:.3f}  "
                      f"df={df}  p={p:.4f}  "
                      f"-> {'SIG (choices shift)' if p < 0.05 else 'ns'}")
    except np.linalg.LinAlgError as e:
        lines.append(f"Stuart-Maxwell could not run: {e}")
    lines.append("\ntransition matrix (rows=less, cols=more), short labels:")
    short = {c: c.split(".")[0].split(" ")[0][:6] + "…" for c in cats}
    t2 = tab.rename(index=short, columns=short)
    lines.append(t2.to_string())
    return [("[method switching] Stuart-Maxwell", sm_pval)] if sm_pval is not None else []


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    paired = bases["paired"]

    lines = [f"paired base n = {len(paired)}"]
    between_method(bases, lines)
    between_scenario_likert(paired, lines)
    between_scenario_binary(paired, lines)
    method_switching(paired, lines)

    for line in lines:
        print(line)

    report_path = save_report("stats", lines)
    print(f"\nreport saved -> {report_path}")
