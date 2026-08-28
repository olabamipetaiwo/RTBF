"""
Scipy-only reimplementation of src/calibration_stats.py (step 8 stats).

8a. Confidence -> verification: statsmodels' Table.test_ordinal_association
    (linear-by-linear / Cochran-Armitage-style trend test) reimplemented by
    hand with numpy + scipy.stats.norm. NOTE: statsmodels' Table defaults to
    shift_zeros=True (replace zero cells with 0.5 before testing) -- matched
    here for parity, though the observed tables have no zero cells.
8b. Used vs ideal, per method: mcnemar_scipy (was statsmodels), Holm via
    scipy_analysis.correction (was statsmodels.multitest).
"""

import numpy as np
import pandas as pd
from scipy.stats import norm

from src.screen import get_bases
from src.calibration import CONF_ORDER, METHODS, IDEAL_MAP, SCEN

from .reporting import save_report
from .correction import holm
from .mcnemar_scipy import mcnemar_p

CONF_SCORE = {c: i + 1 for i, c in enumerate(CONF_ORDER)}
CONF_LABEL = {v: k for k, v in CONF_SCORE.items()}


def _ordinal_association(table, row_scores, col_scores):
    table = np.asarray(table, dtype=float)
    if table.min() == 0:
        # statsmodels Table(..., shift_zeros=True) default
        table = table.copy()
        table[table == 0] = 0.5

    statistic = row_scores @ table @ col_scores
    n_obs = table.sum()
    rtot = table.sum(1)
    ctot = table.sum(0)
    um = row_scores @ rtot
    u2m = (row_scores ** 2) @ rtot
    vn = col_scores @ ctot
    v2n = (col_scores ** 2) @ ctot

    e_stat = um * vn / n_obs
    v_stat = (u2m - um ** 2 / n_obs) * (v2n - vn ** 2 / n_obs) / (n_obs - 1)
    sd_stat = np.sqrt(v_stat)

    zscore = (statistic - e_stat) / sd_stat
    pvalue = 2 * norm.cdf(-np.abs(zscore))
    return statistic, zscore, pvalue


def confidence_trend(df, conf_col, verify_prefix):
    verify_yes = [f"{verify_prefix}_{i}" for i in range(1, 6)]
    conf = df[conf_col].map(CONF_SCORE)
    verified = df[verify_yes].notna().any(axis=1).astype(int)
    tab = pd.crosstab(conf, verified).reindex(index=sorted(CONF_SCORE.values()), fill_value=0)
    row_scores = np.array(tab.index, dtype=float)
    col_scores = np.array(tab.columns, dtype=float)
    statistic, zscore, pvalue = _ordinal_association(tab.values, row_scores, col_scores)
    return tab, statistic, zscore, pvalue


def used_vs_ideal_mcnemar(df, used_col, ideal_prefix):
    rows, pvals = [], []
    for i, method in IDEAL_MAP.items():
        used = df[used_col] == method
        ideal = df[f"{ideal_prefix}_{i}"].notna()
        both = int((used & ideal).sum())
        neither = int((~used & ~ideal).sum())
        used_only = int((used & ~ideal).sum())
        ideal_only = int((~used & ideal).sum())
        table = [[neither, ideal_only], [used_only, both]]
        _, p = mcnemar_p(table)
        rows.append((METHODS[method], used_only, ideal_only, used_only + ideal_only, p))
        pvals.append(p)

    padj = holm(pvals)
    out = pd.DataFrame(
        [(name, uo, io, disc,
          "used>ideal" if uo > io else ("ideal>used" if io > uo else "-"),
          round(p, 4), round(pa, 4), "*" if pa < 0.05 else "")
         for (name, uo, io, disc, p), pa in zip(rows, padj)],
        columns=["method", "used_only", "ideal_only", "discordant", "dir", "p_raw", "p_holm", "sig"],
    )
    return out.sort_values("discordant", ascending=False)


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    lines = []
    for scen, (conf_col, verify_prefix, used_col, ideal_prefix) in SCEN.items():
        df = bases[scen]

        lines.append("\n" + "=" * 60)
        lines.append(f"{scen.upper()} SENSITIVE — 8a. Confidence -> verification: ordinal trend test")
        lines.append("=" * 60)
        tab, statistic, zscore, pvalue = confidence_trend(df, conf_col, verify_prefix)
        disp = tab.rename(index=CONF_LABEL, columns={0: "did NOT verify", 1: "verified"})
        lines.append(disp.to_string())
        lines.append(f"\ntrend statistic={statistic:.3f}  z={zscore:.3f}  p={pvalue:.4f}  "
                     f"-> {'SIG (verification rises with confidence)' if pvalue < 0.05 else 'ns'}")

        lines.append(f"\n{scen.upper()} SENSITIVE — 8b. Used vs ideal, per method: paired McNemar + Holm")
        lines.append("=" * 60)
        out = used_vs_ideal_mcnemar(df, used_col, ideal_prefix)
        lines.append(out.to_string(index=False))

    lines.append("\nused_only  = used it but did NOT mark it ideal")
    lines.append("ideal_only = marked it ideal but did NOT use it  (this is the gap direction)")
    lines.append("Holm across 7 methods, within each scenario. 'File a request.' excluded: no Q4.2/Q5.2 counterpart.")

    for line in lines:
        print(line)

    report_path = save_report("calibration_stats", lines)
    print(f"\nreport saved -> {report_path}")
