"""
Step 8 stats: calibration & gaps, now tested, both scenarios (follow-up to
calibration.py's descriptive cross-tabs).

8a. Confidence -> verification: does verification rate trend with confidence?
    Ordinal trend test (statsmodels Table.test_ordinal_association, the
    Cochran-Armitage-style linear-by-linear association test), confidence
    scored 1-5, verified scored 0/1.

8b. Used vs ideal, per method: paired McNemar (same respondents; "used" = Q4.2/
    Q5.2 single-select, "ideal" = Q4.13/Q5.13 select-all), Holm-corrected
    across the 7 methods within each scenario. "File a request." excluded —
    no Q4.2/Q5.2 counterpart to pair against (see calibration.py's IDEAL_MAP
    note).
"""

import numpy as np
import pandas as pd
from statsmodels.stats.contingency_tables import Table, mcnemar
from statsmodels.stats.multitest import multipletests
from src.screen import get_bases
from src.reporting import save_report
from src.calibration import CONF_ORDER, METHODS, IDEAL_MAP, SCEN

CONF_SCORE = {c: i + 1 for i, c in enumerate(CONF_ORDER)}
CONF_LABEL = {v: k for k, v in CONF_SCORE.items()}


def confidence_trend(df, conf_col, verify_prefix):
    verify_yes = [f"{verify_prefix}_{i}" for i in range(1, 6)]
    conf = df[conf_col].map(CONF_SCORE)
    verified = df[verify_yes].notna().any(axis=1).astype(int)
    tab = pd.crosstab(conf, verified).reindex(index=sorted(CONF_SCORE.values()), fill_value=0)
    t = Table(tab.values)
    res = t.test_ordinal_association(
        row_scores=np.array(tab.index, dtype=float),
        col_scores=np.array(tab.columns, dtype=float),
    )
    return tab, res


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
        p = mcnemar(table, exact=(used_only + ideal_only) < 25).pvalue
        rows.append((METHODS[method], used_only, ideal_only, used_only + ideal_only, p))
        pvals.append(p)

    padj = multipletests(pvals, method="holm")[1]
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
        tab, res = confidence_trend(df, conf_col, verify_prefix)
        disp = tab.rename(index=CONF_LABEL, columns={0: "did NOT verify", 1: "verified"})
        lines.append(disp.to_string())
        lines.append(f"\ntrend statistic={res.statistic:.3f}  z={res.zscore:.3f}  p={res.pvalue:.4f}  "
                     f"-> {'SIG (verification rises with confidence)' if res.pvalue < 0.05 else 'ns'}")

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
