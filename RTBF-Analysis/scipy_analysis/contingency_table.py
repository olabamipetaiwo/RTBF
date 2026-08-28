"""
Contingency table: deletion method x expectation (Yao Li item 5, descriptive
half). Rows = expectation option (Q4.4/Q5.4, select-all), columns = deletion
method (Q4.2/Q5.2), cell = raw count of respondents who used that method AND
selected that expectation option.

Purely descriptive -- no new hypothesis test. The significance test for this
same pairing (per-option chi-square/Fisher, Holm-corrected) already exists in
verify.py; see scipy_analysis/outputs/results/verify.md.
"""

import numpy as np
import pandas as pd
from scipy import stats
from src.screen import get_bases

from .reporting import save_report
from .correction import holm
from .verify import cramers_v, rc_exact_p

N_FLOOR = 14
SCEN = {"less": ("Q4.2", "Q4.4"), "more": ("Q5.2", "Q5.4")}
EXP_OPTS = {
    1: "permanently deleted (DB+backups)", 2: "made invisible / hidden",
    3: "not referenced in current convo", 4: "not referenced in future convo",
    5: "no longer used for training", 6: "not sure what happens", 7: "other",
}


def contingency(df, method_col, q_prefix, opts):
    """rows = expectation option, cols = method, cell = raw count selected."""
    df = df[df[method_col] != "Other (Please specify)"]
    methods = df[method_col].value_counts().index.tolist()

    header = {}
    for m in methods:
        n = int((df[method_col] == m).sum())
        header[m] = n

    rows = []
    for i, label in opts.items():
        col = f"{q_prefix}_{i}"
        row = {"expectation": label}
        for m in methods:
            row[m] = int(df.loc[df[method_col] == m, col].notna().sum())
        row["Total"] = sum(row[m] for m in methods)
        rows.append(row)

    table = pd.DataFrame(rows)
    col_labels = {
        m: f"{m}{'*' if header[m] < N_FLOOR else ''} (n={header[m]})"
        for m in methods
    }
    display = table.rename(columns=col_labels)
    return display, table


def pooled_expectation_frame(bases):
    """Deduped pooling -- same per-respondent mechanism as pooling.py's
    pooled_method_scores (task 1/2's convention), adapted from averaging a
    continuous scale score to averaging a binary select-all indicator:

      - stayer (same method both scenarios): ONE observation in that
        method's group; each expectation option's indicator is the average
        of its less- and more-scenario 0/1 value (so 0, 0.5, or 1).
      - switcher (different method per scenario) or solo (answered only one
        scenario): each scenario answered becomes its own observation in
        its own method's group, un-averaged (0/1 per option) -- nothing
        double-counted within a group, matching pooling.py exactly.

    Uses bases["paired"] (n=177), not naive less+more concatenation.
    """
    paired = bases["paired"]

    def opt_vals(row, prefix):
        return {j: (1 if pd.notna(row[f"{prefix}_{j}"]) else 0) for j in EXP_OPTS}

    rows = []
    for i in paired.index:
        r = paired.loc[i]
        m_less, m_more = r["Q4.2"], r["Q5.2"]
        has_less = pd.notna(m_less) and m_less != "Other (Please specify)"
        has_more = pd.notna(m_more) and m_more != "Other (Please specify)"

        if has_less and has_more and m_less == m_more:
            less_v, more_v = opt_vals(r, "Q4.4"), opt_vals(r, "Q5.4")
            row = {"method": m_less}
            row.update({f"exp_{j}": (less_v[j] + more_v[j]) / 2 for j in EXP_OPTS})
            rows.append(row)
        else:
            if has_less:
                row = {"method": m_less}
                row.update({f"exp_{j}": v for j, v in opt_vals(r, "Q4.4").items()})
                rows.append(row)
            if has_more:
                row = {"method": m_more}
                row.update({f"exp_{j}": v for j, v in opt_vals(r, "Q5.4").items()})
                rows.append(row)

    return pd.DataFrame(rows)


def pooled_contingency(pooled, opts):
    """rows = expectation option, cols = method, cell = summed indicator
    (fractional where a stayer's averaged 0.5 lands in that cell)."""
    methods = pooled["method"].value_counts().index.tolist()
    n_per_method = pooled["method"].value_counts().to_dict()

    rows = []
    for j, label in opts.items():
        col = f"exp_{j}"
        row = {"expectation": label}
        for m in methods:
            row[m] = round(pooled.loc[pooled["method"] == m, col].sum(), 1)
        row["Total"] = round(sum(row[m] for m in methods), 1)
        rows.append(row)

    table = pd.DataFrame(rows)
    col_labels = {
        m: f"{m}{'*' if n_per_method[m] < N_FLOOR else ''} (n={n_per_method[m]})"
        for m in methods
    }
    display = table.rename(columns=col_labels)
    return display, table


def pooled_pct_table(pooled, opts):
    """rows = method, cols = expectation option %, normalized by that
    method's own pooled n so methods with very different n's are
    comparable (raw counts in pooled_contingency() scale with method
    popularity and aren't directly comparable across methods)."""
    n_per_method = pooled["method"].value_counts()
    rows = []
    for m, n in n_per_method.items():
        sub = pooled[pooled["method"] == m]
        row = {"method": m, "n": n}
        for j, label in opts.items():
            row[label] = round(100 * sub[f"exp_{j}"].sum() / n, 1)
        rows.append(row)
    return pd.DataFrame(rows)


def pooled_test_family(pooled, opts):
    """Same test_family() logic as verify.py (chi2 if all expected >= 5,
    else Fisher exact, Holm-corrected within the option family), applied to
    the pooled/deduped table. Fisher needs integer counts, so each method's
    selected-count is rounded to the nearest int before building the 2xk
    table; not-selected = that method's pooled n minus the rounded selected
    count, so rows still sum exactly to n. Methods below N_FLOOR are
    dropped first, same as verify.py."""
    n_per_method = pooled["method"].value_counts()
    kept = n_per_method[n_per_method >= N_FLOOR].index.tolist()

    rows, pvals = [], []
    for j, label in opts.items():
        col = f"exp_{j}"
        table = []
        for m in kept:
            n = int(n_per_method[m])
            selected = int(round(pooled.loc[pooled["method"] == m, col].sum()))
            table.append([selected, n - selected])
        table = np.array(table)
        if table[:, 0].sum() == 0:
            rows.append((label, "skip(0 sel)", np.nan, np.nan)); pvals.append(1.0); continue
        exp = stats.chi2_contingency(table, correction=False)[3]
        if (exp >= 5).all():
            p = stats.chi2_contingency(table, correction=False)[1]; test = "chi2"
        else:
            p = rc_exact_p(table); test = "fisher"
        rows.append((label, test, p, round(cramers_v(table), 3))); pvals.append(p)

    padj = holm(pvals)
    out = []
    for (label, test, p, v), pa in zip(rows, padj):
        out.append({"option": label, "test": test,
                    "p_raw": round(p, 4) if p == p else np.nan,
                    "p_holm": round(pa, 4), "cramers_v": v,
                    "sig": "*" if pa < 0.05 else ""})
    return pd.DataFrame(out), kept


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    lines = ["(* = method n < 14; see verify.md for the significance test on this pairing)"]

    for scen, (mcol, qexp) in SCEN.items():
        df = bases[scen]
        lines.append("\n" + "=" * 70)
        lines.append(f"{scen.upper()} SENSITIVE — method x expectation ({mcol} x {qexp})")
        lines.append("=" * 70)

        display, raw = contingency(df, mcol, qexp, EXP_OPTS)
        lines.append(display.to_string(index=False))

        out_path = f"scipy_analysis/outputs/tables/contingency_{scen}.csv"
        raw.to_csv(out_path, index=False)
        lines.append(f"\nsaved -> {out_path}")

    lines.append("\n" + "=" * 70)
    lines.append("POOLED (deduped per respondent, same mechanism as pooling.py) — method x expectation")
    lines.append("=" * 70)
    pooled = pooled_expectation_frame(bases)
    display, raw = pooled_contingency(pooled, EXP_OPTS)
    lines.append(display.to_string(index=False))
    out_path = "scipy_analysis/outputs/tables/contingency_pooled.csv"
    raw.to_csv(out_path, index=False)
    lines.append(f"\nsaved -> {out_path}")

    lines.append("\n" + "-" * 70)
    lines.append("POOLED, % of each method's own n (comparable across methods; raw")
    lines.append("counts above scale with method popularity and are not)")
    lines.append("-" * 70)
    pct = pooled_pct_table(pooled, EXP_OPTS)
    lines.append(pct.to_string(index=False))
    pct_path = "scipy_analysis/outputs/tables/contingency_pooled_pct.csv"
    pct.to_csv(pct_path, index=False)
    lines.append(f"\nsaved -> {pct_path}")

    lines.append("\n" + "-" * 70)
    lines.append("READING (descriptive)")
    lines.append("-" * 70)
    lines.append(
        "No strong tendency overall: 'permanently deleted', 'not referenced in\n"
        "current convo', and 'not referenced in future convo' are the top 3\n"
        "expectations for every method, and 'not sure'/'other' stay rare for\n"
        "every method -- a flat ranking across methods, consistent with\n"
        "verify.md's finding that no expectation option survives Holm\n"
        "correction against method in either scenario (less or more)."
    )
    lines.append(
        "\nOne pattern flagged above: the heavier-touch methods (Clear all\n"
        "saved memories, Privacy dashboard, both n=11) run ~25-30pt higher on\n"
        "'not referenced in future convo' (77% both) than the lighter methods\n"
        "(single-conversation delete 51%, clear history 45%). Both are below\n"
        "N_FLOOR=14 and dropped from the significance test below -- see that\n"
        "test for the 4 methods it can actually speak to."
    )

    sig, kept = pooled_test_family(pooled, EXP_OPTS)
    lines.append("\n" + "=" * 70)
    lines.append("POOLED significance test (method x expectation, per option)")
    lines.append(
        "Same test_family() logic as verify.py (chi2 if all expected>=5 else\n"
        "Fisher, Holm-corrected within family). Pooled cells rounded to the\n"
        "nearest int for Fisher's integer requirement. Methods with n<14\n"
        "dropped first (same floor as everywhere else in this repo):\n"
        f"kept = {kept}"
    )
    lines.append("=" * 70)
    lines.append(sig.to_string(index=False))
    sig_path = "scipy_analysis/outputs/tables/contingency_pooled_sig.csv"
    sig.to_csv(sig_path, index=False)
    lines.append(f"\nsaved -> {sig_path}")

    for line in lines:
        print(line)

    report_path = save_report("contingency_table", lines)
    print(f"\nreport saved -> {report_path}")
