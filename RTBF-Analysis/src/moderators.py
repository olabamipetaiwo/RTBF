"""
Step 9: moderator analysis.

  Q: Do age group or ChatGPT tenure predict outcomes, independent of scenario/method?

Continuous outcomes (protection/effort/benefit_loss/willingness) x
{age group (Q2.1), ChatGPT tenure (Q3.1_1, "Never used" excluded)}, per scenario:
  Kruskal-Wallis (+ Dunn's/Holm post-hoc if significant) — same design as
  stats.py's between_method / willingness.py's willingness_by_method.
  Groups below N_FLOOR (age 65+, n=3) excluded, same floor used throughout.

Method choice (categorical, Q4.2/Q5.2) x {age group, ChatGPT tenure}, per scenario:
  chi-square / r x c Fisher exact (Freeman-Halton) — same design as verify.py.

Holm correction across the 4 outcomes within each (moderator, scenario) family.
"""

import itertools
import pandas as pd
from scipy import stats
import scikit_posthocs as sp
from statsmodels.stats.multitest import multipletests
from src.screen import get_bases
from src.reporting import save_report
from src.stats import scale_score, SCALES, SCEN as METHOD_SCEN, N_FLOOR, eps2, rank_biserial_indep
from src.willingness import WILLING, WILLING_COL
from src.verify import cramers_v, rc_exact_p

MODERATORS = {
    "age_group": ("Q2.1", None),
    "chatgpt_tenure": ("Q3.1_1", "Never used"),
}


def continuous_outcomes(df, scen):
    base, _ = METHOD_SCEN[scen]
    out = {name: scale_score(df, base, q, k) for name, (q, k) in SCALES.items()}
    out["willingness"] = df[WILLING_COL[scen]].map(WILLING)
    return out


def test_moderator_continuous(df, group_col, exclude_val, outcomes):
    sub = df if exclude_val is None else df[df[group_col] != exclude_val]
    counts = sub[group_col].value_counts()
    kept = counts[counts >= N_FLOOR].index.tolist()
    dropped = [g for g in counts.index if g not in kept]

    rows, pvals = [], []
    for name, series in outcomes.items():
        s = series.loc[sub.index]
        groups = {g: s[sub[group_col] == g].dropna().values for g in kept}
        H, p = stats.kruskal(*groups.values())
        n_tot = sum(len(v) for v in groups.values())
        rows.append((name, H, p, eps2(H, n_tot, len(kept))))
        pvals.append(p)

    padj = multipletests(pvals, method="holm")[1]
    out = pd.DataFrame(
        [(name, round(H, 2), round(p, 4), round(pa, 4), e, "*" if pa < 0.05 else "")
         for (name, H, p, e), pa in zip(rows, padj)],
        columns=["outcome", "H", "p_raw", "p_holm", "eps2", "sig"],
    )
    return out, kept, dropped


def posthoc_for_sig(df, group_col, outcome_series, kept):
    sub = pd.DataFrame({"g": df[group_col], "v": outcome_series.loc[df.index]}).dropna()
    sub = sub[sub["g"].isin(kept)]
    dunn = sp.posthoc_dunn(sub, val_col="v", group_col="g", p_adjust="holm")
    groups = {g: sub.loc[sub["g"] == g, "v"].values for g in kept}
    lines = []
    for g1, g2 in itertools.combinations(kept, 2):
        pv = dunn.loc[g1, g2]
        if pv < 0.05:
            r = rank_biserial_indep(groups[g1], groups[g2])
            lines.append(f"        * {str(g1)[:20]:20} vs {str(g2)[:20]:20} p_holm={pv:.4f}  r={r}")
    return lines


def test_moderator_method(df, group_col, exclude_val, method_col):
    sub = df if exclude_val is None else df[df[group_col] != exclude_val]
    sub = sub[sub[method_col] != "Other (Please specify)"]
    g_counts = sub[group_col].value_counts()
    kept_g = g_counts[g_counts >= N_FLOOR].index.tolist()
    m_counts = sub[method_col].value_counts()
    kept_m = m_counts[m_counts >= N_FLOOR].index.tolist()
    sub = sub[sub[group_col].isin(kept_g) & sub[method_col].isin(kept_m)]

    table = pd.crosstab(sub[group_col], sub[method_col]).values
    exp = stats.chi2_contingency(table, correction=False)[3]
    if (exp >= 5).all():
        p = stats.chi2_contingency(table, correction=False)[1]; test = "chi2"
    else:
        p = rc_exact_p(table); test = "fisher"
    v = cramers_v(table)
    return test, p, round(v, 3), kept_g, kept_m


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    lines = []
    for scen in METHOD_SCEN:
        _, method_col = METHOD_SCEN[scen]
        df = bases[scen]
        outcomes = continuous_outcomes(df, scen)

        for mod_name, (group_col, exclude_val) in MODERATORS.items():
            lines.append("\n" + "=" * 66)
            lines.append(f"[{scen}] {mod_name} ({group_col}) -> protection/effort/benefit_loss/willingness")
            lines.append("=" * 66)
            out, kept, dropped = test_moderator_continuous(df, group_col, exclude_val, outcomes)
            lines.append(out.to_string(index=False))
            if dropped:
                lines.append(f"    (dropped groups below n>={N_FLOOR}: {dropped})")
            for _, row in out.iterrows():
                if row["sig"] == "*":
                    lines.append(f"    -- post-hoc for {row['outcome']} --")
                    lines += posthoc_for_sig(df, group_col, outcomes[row["outcome"]], kept)

            lines.append(f"\n[{scen}] {mod_name} ({group_col}) -> method choice ({method_col})")
            test, p, v, kept_g, kept_m = test_moderator_method(df, group_col, exclude_val, method_col)
            sig = "SIG" if p < 0.05 else "ns"
            lines.append(f"    {test}  p={p:.4f}  cramers_v={v}  -> {sig}")
            lines.append(f"    groups tested: {kept_g}")

    for line in lines:
        print(line)

    report_path = save_report("moderators", lines)
    print(f"\nreport saved -> {report_path}")
