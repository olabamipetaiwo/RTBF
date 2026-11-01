"""
Assumption checks for the cross-platform analysis (platforms/plan/cross-platform.md).

Run BEFORE any cross-platform test. Nothing here tests the research claims; each
check asks whether a planned test (Cochran's Q, pairwise McNemar, Fisher's exact,
Wilson intervals) is valid on this data. Outcome = "retrieved in a new
conversation": RECOVERED = 1; NOT RECOVERED or INDETERMINATE (recalled, nothing
found) = 0; NOT RECALLED and PENDING REVIEW are excluded, never counted as 0.

Checks, in the order of the report:
  1. Design integrity: one shared prompt id per platform, outcome coverage.
  2. Complete cases: how many prompts survive each platform subset.
  3. Selection: do complete-case prompts differ from the dropped ones.
  4. Independence of prompts: one account per platform, the sibling rule,
     injection order, near-duplicate prompts, cross-platform correlation.
  5. Power: discordant pairs per platform pair, degenerate (constant) platforms.
  6. What "not retrieved" means: retention at injection among the zeros.
  7. Section 2 (erasure scope): is scope confounded with platform or injection.

Only audit_outcomes.csv carries outcomes. The prompt table, cells table and run
tracking supply design facts (prompt text, account, injection time).

AS IT STANDS: re-run after each recall batch:
    .venv/bin/python -m src.cross_platform_assumptions
"""

import difflib
import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact, spearmanr
from statsmodels.stats.contingency_tables import StratifiedTable
from statsmodels.stats.multitest import multipletests

from src.expectation_gap import PLATFORM_NAMES, PLATFORMS, md_table
from src.outcome_by_prompt_features import FEATURES, coded_prompts
from src.reporting import save_report

AUDIT = Path("outputs/tables/audit_outcomes.csv")
PROMPTS = Path("../RTBF-Prompt/data/nl_forget_prompts_138_final.csv")
CELLS = Path("../RTBF-Prompt/data/nl_forget_cells.csv")
TRACKING = Path("../tester/data/run_tracking.json")

OUTCOME = {"RECOVERED": 1, "NOT RECOVERED": 0, "INDETERMINATE": 0}
SUBSETS = {
    "all six platforms": PLATFORMS,
    "without Copilot": [p for p in PLATFORMS if p != "copilot"],
    "without Copilot and Gemini": ["chatgpt", "claude", "perplexity", "deepseek"],
    "without Copilot, Gemini and DeepSeek": ["chatgpt", "claude", "perplexity"],
}
SCOPE_GROUPS = {"DELETES": "deletes", "DOES NOT DELETE": "does not delete or unrelated", "UNRELATED": "does not delete or unrelated"}
SCOPE_ORDER = ["deletes", "does not delete or unrelated"]
NEAR_DUPLICATE = 0.90
LOW_DISCORDANT = 10
PERMUTATIONS = 10_000
SEED = 2026


def pct(k: int, n: int) -> str:
    return f"{k} of {n} ({100 * k / n:.0f}%)" if n else "-"


def load_nlf() -> pd.DataFrame:
    d = pd.read_csv(AUDIT)
    d["retrieved"] = d["recoverability"].map(OUTCOME)
    nlf = d[d["sheet"] == "NL FORGET"].copy()
    nlf["item_id"] = nlf["cell_id"].str.split("-").str[-1]
    return nlf


def design_integrity(nlf: pd.DataFrame, cells: pd.DataFrame) -> list[str]:
    ids_per_platform = nlf.groupby("platform")["item_id"].nunique()
    platforms_per_id = nlf.groupby("item_id")["platform"].nunique()
    tokens_per_id = cells.groupby("item_id")["token"].nunique()
    lines = [
        "## 1. Design integrity",
        "",
        f"- Prompt ids per platform: {', '.join(f'{PLATFORM_NAMES[p]} {ids_per_platform[p]}' for p in PLATFORMS)}.",
        f"- Prompt ids present on all six platforms: {(platforms_per_id == 6).sum()} of {len(platforms_per_id)}.",
        f"- Prompt ids whose disclosed fact (token) differs between platforms: {(tokens_per_id > 1).sum()}.",
        "",
        "Outcome coverage per platform (138 prompts each):",
        "",
    ]
    rows = []
    for p in PLATFORMS:
        g = nlf[nlf["platform"] == p]
        yes, no = int((g["retrieved"] == 1).sum()), int((g["retrieved"] == 0).sum())
        rows.append([PLATFORM_NAMES[p], yes, no, len(g) - yes - no, f"{yes / (yes + no):.2f}" if yes + no else "-"])
    return lines + md_table(["Platform", "Retrieved", "Not retrieved", "No usable recall (excluded)", "Retrieval rate on usable"], rows) + [""]


def complete_cases(wide: pd.DataFrame) -> tuple[list[str], dict[str, pd.Index]]:
    rows, kept = [], {}
    for name, plats in SUBSETS.items():
        ids = wide.index[wide[plats].notna().all(axis=1)]
        kept[name] = ids
        sub = wide.loc[ids, plats]
        constant = [PLATFORM_NAMES[p] for p in plats if sub[p].nunique() < 2]
        rows.append([name, len(ids), ", ".join(constant) or "none"])
    lines = ["## 2. Complete cases", "",
             "Cochran's Q uses only prompts with a usable recall on every platform in the comparison.", ""]
    return lines + md_table(["Platforms compared", "Prompts usable on all of them", "Platforms with no variation in that set"], rows) + [""], kept


def perm_chi2(labels: pd.Series, in_set: pd.Series, rng: np.random.Generator) -> tuple[float, float]:
    """Pearson chi-square of label x membership, with a permutation p (small expected counts)."""
    def stat(member: np.ndarray) -> float:
        table = pd.crosstab(labels.to_numpy(), member)
        return chi2_contingency(table, correction=False)[0]

    member = in_set.to_numpy()
    observed = stat(member)
    exceed = sum(stat(rng.permutation(member)) >= observed for _ in range(PERMUTATIONS))
    return observed, (exceed + 1) / (PERMUTATIONS + 1)


def selection(wide: pd.DataFrame, kept: dict[str, pd.Index], prompts: pd.DataFrame) -> list[str]:
    """`prompts` holds the final human coding of each prompt (coded_prompts())."""
    lines = ["## 3. Selection: do complete-case prompts differ from the dropped ones?", "",
             "For each subset, a platform's retrieval rate among the kept prompts is compared with its rate among the "
             "prompts that were dropped (usable on that platform but missing on another). Fisher's exact test. A "
             "difference would mean the complete cases are not representative of the 138.", ""]
    rows = []
    for name, ids in kept.items():
        if name == "all six platforms" and len(ids) < 20:
            rows.append([name, "-", f"only {len(ids)} prompts kept, no comparison", "-", "-"])
            continue
        for p in SUBSETS[name]:
            col = wide[p].dropna()
            inside, outside = col[col.index.isin(ids)], col[~col.index.isin(ids)]
            if len(outside) < 5 or col.nunique() < 2:
                continue
            table = [[int(inside.sum()), int((inside == 0).sum())], [int(outside.sum()), int((outside == 0).sum())]]
            rows.append([name, PLATFORM_NAMES[p], pct(table[0][0], len(inside)), pct(table[1][0], len(outside)), f"{fisher_exact(table)[1]:.3f}"])
    lines += md_table(["Subset", "Platform", "Retrieved, kept prompts", "Retrieved, dropped prompts", "Fisher p"], rows) + [""]

    rng = np.random.default_rng(SEED)
    name = "without Copilot"
    member = prompts.index.isin(kept[name])
    lines += [f"Final human coding of the kept set ({name}, {member.sum()} of {len(prompts)}) against the dropped prompts. "
              f"Pearson chi-square with a permutation p ({PERMUTATIONS:,} shuffles, seed {SEED}).", ""]
    rows = []
    for feat in FEATURES:
        stat, p = perm_chi2(prompts[feat].astype(str), pd.Series(member, index=prompts.index), rng)
        counts = prompts.groupby(prompts[feat].astype(str)).apply(lambda g: f"{int(np.isin(g.index, kept[name]).sum())}/{len(g)}", include_groups=False)
        rows.append([feat, "; ".join(f"{k} {v}" for k, v in counts.items()), f"{stat:.2f}", f"{p:.3f}"])
    return lines + md_table(["Feature", "Kept / all, by level", "Chi-square", "Permutation p"], rows) + [""]


def independence(nlf: pd.DataFrame, wide: pd.DataFrame, cells: pd.DataFrame, prompts: pd.DataFrame) -> list[str]:
    lines = ["## 4. Independence of prompts", "", "### 4a. Accounts", ""]
    accounts = cells.groupby("platform")["email"].nunique()
    lines += [f"- Accounts used for the 138 typed requests: {', '.join(f'{PLATFORM_NAMES[p]} {accounts[p]}' for p in PLATFORMS)}.",
              "- With one account per platform, every prompt on a platform shares that account's memory. Prompts on one platform "
              "are therefore not strictly independent. The sibling rule and the order check below measure how much this matters.", ""]

    lines += ["### 4b. Sibling rule", "",
              "Cells scored RECOVERED because their token surfaced in another cell's recall (direct evidence of cross-prompt leakage).", ""]
    rows = []
    for p in PLATFORMS:
        g = nlf[nlf["platform"] == p]
        sib = g["recoverability_reason"].fillna("").str.contains("sibling")
        yes, no = int((g["retrieved"] == 1).sum()), int((g["retrieved"] == 0).sum())
        rows.append([PLATFORM_NAMES[p], int(sib.sum()), pct(yes, yes + no), pct(yes - int(sib.sum()), yes + no - int(sib.sum()))])
    lines += md_table(["Platform", "Sibling-rule cells", "Retrieval rate, as scored", "Retrieval rate, sibling cells removed"], rows) + [""]

    lines += ["### 4c. Injection order", "",
              "Spearman correlation between a cell's position in its platform's injection sequence and whether it was retrieved. "
              "A correlation would mean earlier or later prompts behave differently, as accumulating memory would produce. "
              "Holm correction across the platforms tested.", ""]
    tracking = json.loads(TRACKING.read_text())
    rows, pvals, names = [], [], []
    for p in PLATFORMS:
        g = nlf[(nlf["platform"] == p) & nlf["retrieved"].notna()].copy()
        g["injected_at"] = g["cell_id"].map(lambda c: tracking.get(c, {}).get("injected_at"))
        g = g.dropna(subset=["injected_at"])
        if len(g) < 20 or g["retrieved"].nunique() < 2:
            rows.append([PLATFORM_NAMES[p], len(g), "-", "-", "no variation or too few timestamps"])
            continue
        rho, pval = spearmanr(pd.to_datetime(g["injected_at"]).rank(), g["retrieved"])
        rows.append([PLATFORM_NAMES[p], len(g), f"{rho:+.2f}", f"{pval:.3f}", ""])
        pvals.append(pval)
        names.append(PLATFORM_NAMES[p])
    if pvals:
        adjusted = dict(zip(names, multipletests(pvals, method="holm")[1]))
        for r in rows:
            if r[0] in adjusted:
                r[4] = f"Holm p = {adjusted[r[0]]:.3f}"
    lines += md_table(["Platform", "Cells with a timestamp", "Spearman rho", "p", "Note"], rows) + [""]

    lines += ["### 4d. Near-duplicate prompts", ""]
    texts = prompts["original_prompt"].str.lower().str.strip()
    exact = int(texts.duplicated().sum())
    close = [(a, b, r) for a, b in combinations(prompts.index, 2) if (r := difflib.SequenceMatcher(None, texts[a], texts[b]).ratio()) >= NEAR_DUPLICATE]
    lines += [f"- Prompts whose text repeats an earlier prompt exactly: {exact}.",
              f"- Pairs with text similarity of at least {NEAR_DUPLICATE:.2f} (difflib ratio): {len(close)}.",
              f"- Repeated referents (the thing disclosed): {int(prompts['referent'].duplicated().sum())}.", ""]
    for a, b, r in close[:10]:
        lines.append(f"  - {a} / {b} ({r:.2f}): \"{texts[a]}\" / \"{texts[b]}\"")
    if close:
        lines.append("")

    lines += ["### 4e. Do the same prompts behave alike across platforms?", "",
              "Phi coefficient (Pearson on 0/1) between platforms, on prompts usable on both. A value near 0 means the prompt "
              "has little to do with the outcome, and pairing adds little. A large value means the pairing is doing real work.", ""]
    rows = []
    for a, b in combinations(PLATFORMS, 2):
        pair = wide[[a, b]].dropna()
        if pair[a].nunique() < 2 or pair[b].nunique() < 2:
            rows.append([PLATFORM_NAMES[a], PLATFORM_NAMES[b], len(pair), "no variation"])
        else:
            rows.append([PLATFORM_NAMES[a], PLATFORM_NAMES[b], len(pair), f"{pair[a].corr(pair[b]):+.2f}"])
    return lines + md_table(["Platform A", "Platform B", "Prompts", "Phi"], rows) + [""]


def power(wide: pd.DataFrame) -> list[str]:
    lines = ["## 5. Power for the pairwise McNemar tests", "",
             "McNemar uses only discordant prompts (retrieved on one platform and not the other). "
             f"With fewer than {LOW_DISCORDANT} discordant prompts the test has little power, and the exact version is required.", ""]
    rows = []
    for a, b in combinations(PLATFORMS, 2):
        pair = wide[[a, b]].dropna()
        both = int(((pair[a] == 1) & (pair[b] == 1)).sum())
        only_a = int(((pair[a] == 1) & (pair[b] == 0)).sum())
        only_b = int(((pair[a] == 0) & (pair[b] == 1)).sum())
        neither = int(((pair[a] == 0) & (pair[b] == 0)).sum())
        flag = "low power" if only_a + only_b < LOW_DISCORDANT else ""
        rows.append([PLATFORM_NAMES[a], PLATFORM_NAMES[b], len(pair), both, only_a, only_b, neither, flag])
    return lines + md_table(["A", "B", "Paired prompts", "Both", "A only", "B only", "Neither", "Flag"], rows) + [""]


def zeros_meaning(nlf: pd.DataFrame) -> list[str]:
    lines = ["## 6. What \"not retrieved\" means", "",
             "A zero can mean the platform erased or never used the fact, or that it never stored it. Retention at injection "
             "(coded when the fact was disclosed) separates the two: shown or claimed means the platform visibly kept it.", ""]
    levels = ["shown", "claimed", "acknowledged", "denied", "no_signal"]
    rows = []
    for p in PLATFORMS:
        g = nlf[(nlf["platform"] == p) & (nlf["retrieved"] == 0)]
        counts = g["retention"].value_counts()
        rows.append([PLATFORM_NAMES[p], len(g), *[int(counts.get(lv, 0)) for lv in levels], int(g["retention"].isna().sum())])
    return lines + md_table(["Platform", "Not retrieved", *levels, "uncoded"], rows) + [""]


def scope_strata(main: pd.DataFrame) -> list[np.ndarray]:
    """One 2x2 (group x retrieved) per platform that has both groups and both outcomes."""
    tables = []
    for p in PLATFORMS:
        g = main[main["platform"] == p]
        t = [[int(g[g["group"] == grp]["retrieved"].sum()), int((g[g["group"] == grp]["retrieved"] == 0).sum())] for grp in SCOPE_ORDER]
        if min(sum(t[0]), sum(t[1])) > 0 and (t[0][0] + t[1][0]) > 0 and (t[0][1] + t[1][1]) > 0:
            tables.append(np.array(t))
    return tables


def scope_confounding(d: pd.DataFrame) -> list[str]:
    main = d[(d["sheet"] == "MASTER") & d["retrieved"].notna()].copy()
    lines = ["## 7. Section 2 (erasure scope): is scope confounded?", "",
             f"Main-grid cells with a usable recall: {len(main)}. Commitment types present: "
             f"{', '.join(f'{k} {v}' for k, v in main['commitment'].value_counts().items())}.", ""]
    main["group"] = main["commitment"].map(SCOPE_GROUPS)
    left_out = main[main["group"].isna()]
    lines += [f"- Left out of the two groups: {len(left_out)} cells ({', '.join(f'{k} {v}' for k, v in left_out['commitment'].value_counts().items()) or 'none'}).", ""]
    main = main.dropna(subset=["group"])

    lines += ["Cells per platform and group, with the number retrieved:", ""]
    rows = []
    for p in PLATFORMS:
        g = main[main["platform"] == p]
        cols = []
        for grp in ["deletes", "does not delete or unrelated"]:
            s = g[g["group"] == grp]
            cols.append(f"{int(s['retrieved'].sum())} of {len(s)}" if len(s) else "-")
        rows.append([PLATFORM_NAMES[p], *cols])
    lines += md_table(["Platform", "Deletes: retrieved", "Does not delete or unrelated: retrieved"], rows) + [""]

    lines += ["Cells per injection type and group (injection type changes how likely a fact is to be stored):", ""]
    inj = pd.crosstab(main["injection"], main["group"])
    lines += md_table(["Injection", *inj.columns], [[i, *inj.loc[i]] for i in inj.index]) + [""]

    crude = [[int(main[(main["group"] == g)]["retrieved"].sum()), int((main[(main["group"] == g)]["retrieved"] == 0).sum())] for g in ["deletes", "does not delete or unrelated"]]
    lines += [f"Crude (pooled over platforms) Fisher p = {fisher_exact(crude)[1]:.4f}; odds ratio = {fisher_exact(crude)[0]:.2f}.", ""]

    tables = scope_strata(main)
    lines += [f"Platforms usable as strata (both groups present, both outcomes present): {len(tables)} of {len(PLATFORMS)}."]
    if len(tables) >= 2:
        strat = StratifiedTable(tables)
        cmh = strat.test_null_odds(correction=True)
        lines += [f"Cochran-Mantel-Haenszel across those platforms: pooled odds ratio = {strat.oddsratio_pooled:.2f}, p = {cmh.pvalue:.4f}.",
                  "If the crude and stratified results agree in direction and size, platform is not driving the scope effect; "
                  "if they diverge, the pooled Fisher test is confounded and cannot be used on its own."]
    else:
        lines += ["Fewer than two usable strata: a platform-adjusted comparison is not possible, so the pooled Fisher test cannot be separated from a platform effect."]
    return lines + [""]


if __name__ == "__main__":
    cells = pd.read_csv(CELLS)
    prompts = pd.read_csv(PROMPTS).set_index("item_id")
    nlf = load_nlf()
    wide = nlf.pivot(index="item_id", columns="platform", values="retrieved")[PLATFORMS]

    report = ["Assumption checks for the cross-platform tests. Outcome: retrieved in a new conversation (1) or not (0); "
              "cells with no usable recall are excluded. Source of outcomes: `outputs/tables/audit_outcomes.csv`.", ""]
    report += design_integrity(nlf, cells)
    section, kept = complete_cases(wide)
    report += section
    report += selection(wide, kept, coded_prompts())
    report += independence(nlf, wide, cells, prompts)
    report += power(wide)
    report += zeros_meaning(nlf)
    report += scope_confounding(pd.read_csv(AUDIT).assign(retrieved=lambda x: x["recoverability"].map(OUTCOME)))

    print("\n".join(report))
    save_report("cross_platform_assumptions", report, fenced=False)
