"""
Cross-platform analysis (platforms/plan/cross-platform.md).

Outcome = "retrieved in a new conversation" (src.cross_platform_assumptions.OUTCOME):
RECOVERED = 1; NOT RECOVERED or INDETERMINATE (recalled, nothing found) = 0; cells
with no usable recall are excluded. This is retrieval, never an erasure rate: for
Gemini, Perplexity, DeepSeek and Copilot a zero can also mean the fact was never
stored (see section 6 of cross_platform_assumptions.md).

1. Typed requests, same 138 prompts on every platform (paired).
   Rates with Wilson 95% intervals; Cochran's Q; exact McNemar for every platform
   pair on the prompts usable on both, Holm-corrected over all 15 pairs. A pair
   with no discordant prompt has identical outcomes: reported, p = 1, not a result.
2. Erasure scope, main grid only. Groups from the coded commitment type:
   deletes against does not delete or unrelated. NO COMMITMENT cells fit neither
   group (the help page says nothing about scope) and are reported as their own row.
   Fisher's exact overall; per platform descriptive; Mantel-Haenszel as the
   platform-adjusted check.
3. Do the user's checks track the outcome? Descriptive only.
4. Policy verdicts per platform. Descriptive only. Refusals are counted by
   src.recall_refusals (one source), not here.

Gemini's 13 account-wide prompts are not recalled yet, so every result that includes
Gemini leaves those prompts out; the usable count per platform in section 1 shows it.

AS IT STANDS: re-run after every recall batch:
    .venv/bin/python -m src.audit_outcomes && .venv/bin/python -m src.cross_platform
"""

from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest, fisher_exact
from statsmodels.stats.contingency_tables import StratifiedTable, cochrans_q
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint

from src.cross_platform_assumptions import AUDIT, OUTCOME, SCOPE_GROUPS, SCOPE_ORDER, load_nlf, scope_strata
from src.expectation_gap import PLATFORM_NAMES, PLATFORMS, md_table
from src.reporting import save_report

OUT_TEX_RETRIEVAL = Path("outputs/tables/retrieval_by_platform.tex")
OUT_TEX_POLICY = Path("outputs/tables/policy_verdicts.tex")
DOC_GROUPS = {"DELETES": "deletes", "DOES NOT DELETE": "does not delete"}  # anything else: silent or unrelated
VERDICTS = ["CONSISTENT", "CONTRADICTED", "INDETERMINATE", "NOT RECALLED"]

Q_SETS = {
    "without Copilot (Gemini included, so its 13 account-wide prompts are out)": [p for p in PLATFORMS if p != "copilot"],
    "without Copilot and Gemini": ["chatgpt", "claude", "perplexity", "deepseek"],
}


def wilson(k: int, n: int) -> str:
    if not n:
        return "-"
    lo, hi = proportion_confint(k, n, method="wilson")
    return f"{k} of {n} ({100 * k / n:.0f}%, 95% CI {100 * lo:.1f} to {100 * hi:.1f})"


def rates_table(wide: pd.DataFrame) -> list[str]:
    rows = []
    for p in PLATFORMS:
        col = wide[p].dropna()
        rows.append([PLATFORM_NAMES[p], wilson(int(col.sum()), len(col)), len(wide) - len(col)])
    return md_table(["Platform", "Fact came back (usable prompts)", "Prompts without a usable recall"], rows)


def cochran_rows(wide: pd.DataFrame) -> list[list[object]]:
    rows = []
    for name, plats in Q_SETS.items():
        sub = wide[plats].dropna().astype(int)
        res = cochrans_q(sub.to_numpy())
        rows.append([name, len(sub), f"{res.statistic:.1f}", res.df, f"{res.pvalue:.2e}"])
    return rows


def pairwise_rows(wide: pd.DataFrame) -> list[list[object]]:
    rows, pvals = [], []
    for a, b in combinations(PLATFORMS, 2):
        pair = wide[[a, b]].dropna()
        both = int(((pair[a] == 1) & (pair[b] == 1)).sum())
        only_a = int(((pair[a] == 1) & (pair[b] == 0)).sum())
        only_b = int(((pair[a] == 0) & (pair[b] == 1)).sum())
        neither = int(((pair[a] == 0) & (pair[b] == 0)).sum())
        discordant = only_a + only_b
        p = binomtest(only_a, discordant, 0.5).pvalue if discordant else 1.0
        rows.append([PLATFORM_NAMES[a], PLATFORM_NAMES[b], len(pair), both, only_a, only_b, neither, p])
        pvals.append(p)
    adjusted = multipletests(pvals, method="holm")[1]
    return [[*r[:7], f"{r[7]:.2e}", f"{adj:.2e}", "identical outcomes, no test" if r[4] + r[5] == 0 else ""] for r, adj in zip(rows, adjusted)]


def overlap_line(wide: pd.DataFrame) -> str:
    pair = wide[["chatgpt", "perplexity"]].dropna()
    t = [[int(((pair.chatgpt == x) & (pair.perplexity == y)).sum()) for y in (1, 0)] for x in (1, 0)]
    phi = pair["chatgpt"].corr(pair["perplexity"])
    return (f"ChatGPT and Perplexity are the only two platforms where the fact came back for some prompts and not others. "
            f"On the {len(pair)} prompts usable on both: both {t[0][0]}, ChatGPT only {t[0][1]}, Perplexity only {t[1][0]}, "
            f"neither {t[1][1]}. Phi = {phi:+.2f}, Fisher's exact p = {fisher_exact(t)[1]:.3f}: a prompt that came back on one "
            f"platform is no more likely to come back on the other.")


def section_typed(nlf: pd.DataFrame) -> list[str]:
    wide = nlf.pivot(index="item_id", columns="platform", values="retrieved")[PLATFORMS]
    lines = ["## 1. Typed requests: the same 138 prompts on every platform", "",
             "Outcome: the fact came back in a new conversation. Retrieval, not erasure.", "", *rates_table(wide), "",
             "Cochran's Q asks whether the platforms differ at all. Platforms with no variation still count in the totals.", ""]
    lines += md_table(["Platforms compared", "Prompts usable on all", "Q", "df", "p"], cochran_rows(wide)) + [""]
    lines += ["Exact McNemar test for every pair of platforms, on the prompts usable on both. Holm correction over all 15 pairs.", ""]
    lines += md_table(["A", "B", "Prompts", "Both", "A only", "B only", "Neither", "p", "Holm p", "Note"], pairwise_rows(wide)) + ["", overlap_line(wide), ""]
    return lines


def section_scope(d: pd.DataFrame) -> list[str]:
    main = d[(d["sheet"] == "MASTER") & d["retrieved"].notna()].copy()
    main["group"] = main["commitment"].map(SCOPE_GROUPS)
    grouped = main.dropna(subset=["group"])
    lines = ["## 2. Erasure scope (main grid)", "",
             f"Cells with a usable recall: {len(main)}. Groups follow the commitment coded from each help page.", ""]
    rows = []
    for grp in SCOPE_ORDER:
        s = grouped[grouped["group"] == grp]
        rows.append([grp, wilson(int(s["retrieved"].sum()), len(s))])
    other = main[main["group"].isna()]
    for com, s in other.groupby("commitment"):
        rows.append([f"{com.lower()} (not in the test)", wilson(int(s["retrieved"].sum()), len(s))])
    lines += md_table(["Group", "Fact came back"], rows) + [""]

    table = [[int(grouped[grouped["group"] == g]["retrieved"].sum()), int((grouped[grouped["group"] == g]["retrieved"] == 0).sum())] for g in SCOPE_ORDER]
    odds, p = fisher_exact(table)
    lines += [f"Fisher's exact test, deletes against the rest: odds ratio {odds:.2f}, p = {p:.4f}.", ""]

    strata = scope_strata(grouped)
    if len(strata) >= 2:
        strat = StratifiedTable(strata)
        lines += [f"Platform-adjusted check (Mantel-Haenszel over the {len(strata)} platforms that have both groups and both outcomes): "
                  f"pooled odds ratio {strat.oddsratio_pooled:.2f}, p = {strat.test_null_odds(correction=True).pvalue:.4f}.", ""]

    rows = []
    for plat in PLATFORMS:
        g = grouped[grouped["platform"] == plat]
        cols = [f"{int(g[g['group'] == grp]['retrieved'].sum())} of {(g['group'] == grp).sum()}" if (g["group"] == grp).any() else "-" for grp in SCOPE_ORDER]
        rows.append([PLATFORM_NAMES[plat], *cols])
    lines += ["Per platform (descriptive only, groups too small to test):", ""] + md_table(["Platform", "Deletes", "Does not delete or unrelated"], rows) + [""]
    return lines


def same_conversation_rows(d: pd.DataFrame) -> list[list[object]]:
    known = d[d["same_conversation_r1"].isin(["FOUND", "NOT FOUND"]) & d["retrieved"].notna()]
    rows = []
    for plat in PLATFORMS:
        g = known[known["platform"] == plat]
        if g.empty:
            continue
        yes, hit = g["same_conversation_r1"] == "FOUND", g["retrieved"] == 1
        right = int((yes & hit).sum() + (~yes & ~hit).sum())
        rows.append([PLATFORM_NAMES[plat], len(g), int((yes & hit).sum()), int((yes & ~hit).sum()), int((~yes & hit).sum()), int((~yes & ~hit).sum()), wilson(right, len(g))])
    return rows


def section_checks(d: pd.DataFrame) -> list[str]:
    d = d.copy()
    d["retrieved_r1r3"] = np.where(d[["r1", "r3"]].eq("FOUND").any(axis=1), 1.0, np.where(d[["r1", "r3"]].isin(["FOUND", "NOT FOUND"]).all(axis=1), 0.0, np.nan))
    header = ["Platform", "Cells", "Check says yes, fact came back", "Check says yes, did not come back", "Check says no, fact came back", "Check says no, did not come back", "Check right"]
    lines = ["## 3. Do the checks a user can make track the outcome? (descriptive)", "",
             "Same-conversation check: after the forget request, the user asks about the fact in the same chat (typed requests only). "
             "\"Check says yes\" means the chat still produced the fact. \"Check says no, fact came back\" is the dangerous direction: "
             "the user is told it is gone and it is not.", ""]
    lines += md_table(header, same_conversation_rows(d)) + [""]
    cant_tell = int(((d["interface_change"] == "CHANGED") & (d["recoverability"] == "INDETERMINATE")).sum())
    lines += ["Interface check (cells erased through the interface), known outcomes only: \"changed\" means the screen showed the item gone. "
              f"Cells where the screen showed it gone and the outcome is can't tell are not counted here ({cant_tell}).", ""]
    ui = d[d["interface_change"].isin(["CHANGED", "UNCHANGED"]) & d["recoverability"].isin(["RECOVERED", "NOT RECOVERED"])]
    rows = [[PLATFORM_NAMES[p], len(g), int(((g.interface_change == "CHANGED") & (g.retrieved == 1)).sum()), int(((g.interface_change == "CHANGED") & (g.retrieved == 0)).sum()),
             int(((g.interface_change == "UNCHANGED") & (g.retrieved == 1)).sum()), int(((g.interface_change == "UNCHANGED") & (g.retrieved == 0)).sum())]
            for p, g in ui.groupby("platform")]
    lines += md_table(["Platform", "Cells", "Changed, fact came back", "Changed, did not come back", "Unchanged, fact came back", "Unchanged, did not come back"], rows) + [""]
    lines += ["Memory-page check (R2): the fact appears on the memory page, against whether the new-conversation questions (R1 and R3 only) found it.", ""]
    mem = d[d["r2"].isin(["FOUND", "NOT FOUND"]) & d["retrieved_r1r3"].notna()]
    rows = [[PLATFORM_NAMES[p], len(g), int(((g.r2 == "FOUND") & (g.retrieved_r1r3 == 1)).sum()), int(((g.r2 == "FOUND") & (g.retrieved_r1r3 == 0)).sum()),
             int(((g.r2 == "NOT FOUND") & (g.retrieved_r1r3 == 1)).sum()), int(((g.r2 == "NOT FOUND") & (g.retrieved_r1r3 == 0)).sum())]
            for p, g in mem.groupby("platform")]
    return lines + md_table(["Platform", "Cells", "On page, fact came back", "On page, did not come back", "Not on page, fact came back", "Not on page, did not come back"], rows) + [""]


def section_policy(d: pd.DataFrame) -> list[str]:
    lines = ["## 4. Withholding and policy (descriptive)", "",
             "Refusals that cite the user's earlier request are counted by `src.recall_refusals` (one source); see its report.", "",
             "Policy verdicts per platform. Can't tell includes every cell whose commitment is no commitment or unrelated.", ""]
    rows = []
    for plat in PLATFORMS:
        g = d[(d["platform"] == plat) & (d["policy_consistency"] != "NOT RECALLED")]
        c = g["policy_consistency"].value_counts()
        rows.append([PLATFORM_NAMES[plat], len(g), int(c.get("CONSISTENT", 0)), int(c.get("CONTRADICTED", 0)), int(c.get("INDETERMINATE", 0)), int((g["commitment"] == "NO COMMITMENT").sum())])
    return lines + md_table(["Platform", "Cells recalled", "Kept", "Broken", "Can't tell", "of which no commitment"], rows) + [""]


def latex_retrieval_rows(wide: pd.DataFrame) -> list[str]:
    """Paper table: retrieval of the typed requests per platform, with Wilson 95% intervals."""
    rows = []
    for p in PLATFORMS:
        col = wide[p].dropna()
        k, n = int(col.sum()), len(col)
        lo, hi = proportion_confint(k, n, method="wilson")
        rows.append(f"{PLATFORM_NAMES[p]} & {n} & {k} & {100 * k / n:.0f} ({100 * lo:.1f} to {100 * hi:.1f}) & {len(wide) - n} \\\\")
    return rows


def latex_policy_rows(d: pd.DataFrame) -> list[str]:
    """Paper table: what each platform's documentation says about the tested method, and the verdicts."""
    d = d.assign(doc=d["commitment"].map(DOC_GROUPS).fillna("silent or unrelated"))
    docs = pd.crosstab(d["platform"], d["doc"]).reindex(columns=["deletes", "does not delete", "silent or unrelated"], fill_value=0)
    verdicts = pd.crosstab(d["platform"], d["policy_consistency"]).reindex(columns=VERDICTS, fill_value=0)
    table = pd.concat([docs, verdicts], axis=1)
    rows = [f"{PLATFORM_NAMES[p]} & " + " & ".join(str(int(v)) for v in table.loc[p]) + " \\\\" for p in PLATFORMS]
    rows.append(f"All {len(d)} & " + " & ".join(str(int(v)) for v in table.sum()) + " \\\\")
    return rows


if __name__ == "__main__":
    d = pd.read_csv(AUDIT).assign(retrieved=lambda x: x["recoverability"].map(OUTCOME))
    report = ["Cross-platform analysis. Outcome: the fact came back in a new conversation (retrieval, not erasure). "
              "Cells with no usable recall are excluded. Source: `outputs/tables/audit_outcomes.csv`. "
              "Assumption checks: `outputs/results/cross_platform_assumptions.md`.", ""]
    report += section_typed(load_nlf())
    report += section_scope(d)
    report += section_checks(d)
    report += section_policy(d)

    OUT_TEX_RETRIEVAL.write_text("\n".join(latex_retrieval_rows(load_nlf().pivot(index="item_id", columns="platform", values="retrieved")[PLATFORMS])) + "\n")
    OUT_TEX_POLICY.write_text("\n".join(latex_policy_rows(d)) + "\n")

    print("\n".join(report))
    save_report("cross_platform", report, fenced=False)
