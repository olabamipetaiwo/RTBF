"""
Between-method tests on expectation/verification options (categorical analogue
of the Kruskal-Wallis steps in stats_all.py).

  Q: Does selection rate for a given option differ across deletion methods?
  For each option x scenario, build a method x {selected, not} contingency table
  (kept methods only, n>=N_FLOOR), then:
    - chi-square test of independence if all expected counts >= 5
    - else r x c Fisher exact (Freeman-Halton); Monte-Carlo fallback if
      the installed scipy can't do r x c
  Effect size: Cramer's V (categorical analogue of eps^2 / rank-biserial).
  Correction: Holm across the options WITHIN each family
              (expectation-less, expectation-more, verification-less, verification-more).

Expect most options to wash out; the visibility-driven verification options
("asked in same conversation", "did not know how to check") are the ones likely
to survive. Nulls at these cell sizes = underpowered, NOT "no difference".
"""

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
from src.screen import get_bases
from src.reporting import save_report

N_FLOOR = 14
SCEN = {"less": ("Q4.2", "Q4.4", "Q4.5"), "more": ("Q5.2", "Q5.4", "Q5.5")}
EXP_OPTS = {1: "permanently deleted", 2: "made invisible", 3: "not ref. current",
            4: "not ref. future", 5: "not used for training", 6: "not sure", 7: "other"}
VER_OPTS = {1: "asked same convo", 2: "asked new convo", 3: "checked settings",
            4: "checked UI", 5: "privacy-portal request", 6: "did NOT know how",
            7: "did NOT want to", 8: "other"}


def cramers_v(table):
    chi2 = stats.chi2_contingency(table, correction=False)[0]
    n = table.sum()
    k = min(table.shape) - 1
    return np.sqrt(chi2 / (n * k)) if n and k else np.nan


def rc_exact_p(table):
    """r x c Fisher (Freeman-Halton); Monte-Carlo permutation fallback."""
    try:
        return stats.fisher_exact(table)[1]     # scipy >=1.15 supports r x c
    except Exception:
        # Monte-Carlo: permute the binary column labels, compare chi2 stats
        obs = stats.chi2_contingency(table, correction=False)[0]
        rows = []
        for r_i, row in enumerate(table):
            rows += [r_i] * int(row.sum())
        sel_total = int(table[:, 0].sum())
        rng = np.random.default_rng(0)
        rows = np.array(rows); B = 5000; count = 0
        for _ in range(B):
            perm = rng.permutation(len(rows))
            sel_rows = rows[perm[:sel_total]]
            t = np.zeros_like(table)
            for r_i in range(table.shape[0]):
                s = int((sel_rows == r_i).sum())
                t[r_i, 0] = s; t[r_i, 1] = int((rows == r_i).sum()) - s
            try:
                st = stats.chi2_contingency(t, correction=False)[0]
                if st >= obs - 1e-9:
                    count += 1
            except Exception:
                count += 1
        return (count + 1) / (B + 1)


def test_family(df, method_col, q_prefix, opts):
    counts = df[method_col].value_counts()
    kept = counts[counts >= N_FLOOR].index.tolist()
    sub = df[df[method_col].isin(kept)]
    rows, pvals = [], []
    for i, label in opts.items():
        col = f"{q_prefix}_{i}"
        table = np.array([[int(sub.loc[sub[method_col] == m, col].notna().sum()),
                           int(sub.loc[sub[method_col] == m, col].isna().sum())]
                          for m in kept])
        if table[:, 0].sum() == 0:            # nobody selected this option
            rows.append((label, "skip(0 sel)", np.nan, np.nan)); pvals.append(1.0); continue
        exp = stats.chi2_contingency(table, correction=False)[3]
        if (exp >= 5).all():
            p = stats.chi2_contingency(table, correction=False)[1]; test = "chi2"
        else:
            p = rc_exact_p(table); test = "fisher"
        rows.append((label, test, p, round(cramers_v(table), 3))); pvals.append(p)
    padj = multipletests(pvals, method="holm")[1]
    out = []
    for (label, test, p, v), pa in zip(rows, padj):
        out.append({"option": label, "test": test,
                    "p_raw": round(p, 4) if p == p else np.nan,
                    "p_holm": round(pa, 4), "cramers_v": v,
                    "sig": "*" if pa < 0.05 else ""})
    return pd.DataFrame(out)


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    lines = []
    for scen, (mcol, qexp, qver) in SCEN.items():
        df = bases[scen]
        lines.append("\n" + "=" * 66)
        lines.append(f"{scen.upper()} SENSITIVE — EXPECTATION by method ({qexp})")
        lines.append("=" * 66)
        lines.append(test_family(df, mcol, qexp, EXP_OPTS).to_string(index=False))

        lines.append("\n" + "=" * 66)
        lines.append(f"{scen.upper()} SENSITIVE — VERIFICATION by method ({qver})")
        lines.append("=" * 66)
        lines.append(test_family(df, mcol, qver, VER_OPTS).to_string(index=False))

    for line in lines:
        print(line)

    report_path = save_report("verify", lines)
    print(f"\nreport saved -> {report_path}")