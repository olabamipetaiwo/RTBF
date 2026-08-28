"""
Expectations & verifications per method (descriptive; Yao Li item 5).

Q4.4/Q5.4 = what users EXPECT deletion does (7 options, select-all)
Q4.5/Q5.5 = whether/how users VERIFIED (8 options, select-all)

Select-all: a cell is non-null iff that option was selected. Percentages are
per-option (% of a method's respondents who ticked it) against that method's n;
they DO NOT sum to 100. Methods with n<N_FLOOR are shown but flagged.
"""

import pandas as pd
from src.screen import get_bases
from src.reporting import save_report

N_FLOOR = 14
SCEN = {"less": ("Q4.2", "Q4.4", "Q4.5"), "more": ("Q5.2", "Q5.4", "Q5.5")}

EXP_OPTS = {
    1: "permanently deleted (DB+backups)", 2: "made invisible / hidden",
    3: "not referenced in current convo", 4: "not referenced in future convo",
    5: "no longer used for training", 6: "not sure what happens", 7: "other",
}
VER_OPTS = {
    1: "asked in same conversation", 2: "asked in new conversation",
    3: "checked memory/data settings", 4: "checked UI visibility",
    5: "submitted privacy-portal request", 6: "did NOT know how to check",
    7: "did NOT want to check", 8: "other",
}


def pct_table(df, method_col, q_prefix, opts):
    """rows = method, cols = option %, plus n and flag."""
    df = df[df[method_col] != "Other (Please specify)"]
    rows = []
    for method, g in df.groupby(method_col):
        n = len(g)
        row = {"method": method, "n": n}
        for i, label in opts.items():
            col = f"{q_prefix}_{i}"
            sel = g[col].notna().sum()
            row[label] = round(100 * sel / n, 1) if n else 0.0
        row["flag"] = "" if n >= N_FLOOR else f"n<{N_FLOOR}"
        rows.append(row)
    return pd.DataFrame(rows).sort_values("n", ascending=False).reset_index(drop=True)


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    lines = []
    for scen, (mcol, qexp, qver) in SCEN.items():
        df = bases[scen]
        lines.append("\n" + "=" * 70)
        lines.append(f"{scen.upper()} SENSITIVE — EXPECTATIONS ({qexp}, % per option)")
        lines.append("=" * 70)
        exp = pct_table(df, mcol, qexp, EXP_OPTS)
        lines.append(exp.to_string(index=False))
        exp.to_csv(f"outputs/tables/expectations_{scen}.csv", index=False)

        lines.append("\n" + "=" * 70)
        lines.append(f"{scen.upper()} SENSITIVE — VERIFICATIONS ({qver}, % per option)")
        lines.append("=" * 70)
        ver = pct_table(df, mcol, qver, VER_OPTS)
        lines.append(ver.to_string(index=False))
        ver.to_csv(f"outputs/tables/verifications_{scen}.csv", index=False)

    lines.append("\nsaved -> outputs/tables/expectations_{less,more}.csv, verifications_{less,more}.csv")

    for line in lines:
        print(line)

    report_path = save_report("expectation", lines)
    print(f"\nreport saved -> {report_path}")