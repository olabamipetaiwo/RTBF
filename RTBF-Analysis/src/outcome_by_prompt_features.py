"""
Did the wording of a typed forget request change whether the fact came back?

NL-forget study only (the main battery uses one fixed command per platform, so
it has no wording variation to test). Each cell's prompt is joined to the final
human coding of the 138 prompts (Compare/Prompts/Fourth Pass/Prompts_Coding_Final.xlsx)
through RTBF-Prompt/data/nl_forget_prompts_138_final.csv (item_id -> original
prompt, exact text). Outcome = recoverability from src.audit_outcomes (paper rule).

Follows platforms/plan/wording.md.

A. For every platform and coded feature, each level shows came back / known
   outcome with a Wilson 95% interval. Levels with fewer than MIN_LEVEL known
   cells show counts only, and the range over levels uses only levels with at
   least MIN_LEVEL (Rupp et al., PoPETs 2022). No tests: with so little
   variation a non-significant test shows little (Altman and Bland 1995).
   Gemini and DeepSeek are left out (every cell is can't tell). Perplexity's
   outcome is gave versus withheld the name over all its recalled cells.
C. Refusals against what is asked (evidence only, counts, no tests): each cell
   is retrieved, declined citing the request (human-reviewed refusals only,
   ChatGPT and Perplexity), or not retrieved.

AS IT STANDS: re-run after each recall batch:
    .venv/bin/python -m src.outcome_by_prompt_features
"""

import csv
from datetime import date
from pathlib import Path

import openpyxl
import pandas as pd
from statsmodels.stats.proportion import proportion_confint

from src.expectation_gap import PLATFORM_NAMES, PLATFORMS, audit_rows, md_table
from src.recall_refusals import reviewed_codes
from src.reporting import save_report

CODING = Path("../Compare/Prompts/Fourth Pass/Prompts_Coding_Final.xlsx")
PROMPTS = Path("../RTBF-Prompt/data/nl_forget_prompts_138_final.csv")
FEATURES = ["deletion_location", "what", "mood", "tone", "verb", "justification", "accompanying_request"]
KNOWN = ("RECOVERED", "NOT RECOVERED")
MIN_LEVEL = 6
LEFT_OUT = {"gemini": "Gemini", "deepseek": "DeepSeek"}
GAVE_NAME = {"perplexity"}
ANALYSED = [p for p in PLATFORMS if p not in LEFT_OUT]
NAMED_LOCATIONS = ["memory", "backend_db", "account_all"]
REFUSAL_FEATURES = ["deletion_location", "what"]
REFUSAL_PLATFORMS = ["chatgpt", "perplexity"]


def coded_prompts() -> pd.DataFrame:
    """The final human coding of the 138 prompts, one row per item_id, one column per feature."""
    ws = openpyxl.load_workbook(CODING, read_only=True, data_only=True)["Coding"]
    rows = list(ws.iter_rows(values_only=True))
    codes = pd.DataFrame(rows[1:], columns=rows[0]).set_index("prompt")
    with PROMPTS.open(newline="") as f:
        item_prompt = {r["item_id"]: r["original_prompt"] for r in csv.DictReader(f)}
    unmatched = sorted(i for i, text in item_prompt.items() if text not in codes.index)
    if unmatched:
        raise ValueError(f"prompts with no final coding: {unmatched[:10]}")
    return pd.DataFrame({feat: {i: str(codes.loc[text, feat]) for i, text in item_prompt.items()} for feat in FEATURES})


def coded_cells() -> pd.DataFrame:
    prompts = coded_prompts()
    audit = audit_rows()
    nlf = audit[(audit["sheet"] == "NL FORGET") & audit["run_status"].isin(["ERASED", "RECALLED"])].copy()
    nlf["item_id"] = nlf["cell_id"].str.split("-").str[-1]
    unmatched = nlf[~nlf["item_id"].isin(prompts.index)]
    if not unmatched.empty:
        raise ValueError(f"cells with no coded prompt: {sorted(unmatched['cell_id'])[:10]}")
    for feat in FEATURES:
        nlf[feat] = nlf["item_id"].map(prompts[feat])
    return nlf


def with_outcome(df: pd.DataFrame) -> pd.DataFrame:
    """Cells with an outcome for the wording tables, as `came_back`.

    Perplexity's outcome is gave the name (RECOVERED) against withheld it, over all
    recalled cells; every other platform uses known outcomes only (can't tell is left out).
    """
    usable = df["recoverability"].isin(KNOWN) | (df["platform"].isin(GAVE_NAME) & (df["recoverability"] == "INDETERMINATE"))
    return df[usable].assign(came_back=lambda x: x["recoverability"] == "RECOVERED")


def level_text(k: int, n: int) -> str:
    if not n:
        return "–"
    if n < MIN_LEVEL:
        return f"{k} of {n}"
    lo, hi = proportion_confint(k, n, method="wilson")
    return f"{k} of {n} ({100 * lo:.0f} to {100 * hi:.0f}%)"


def level_row(g: pd.DataFrame, feat: str, levels: list[str]) -> tuple[list[str], str]:
    cells, rates = [], []
    for lv in levels:
        s = g[g[feat] == lv]
        k, n = int(s["came_back"].sum()), len(s)
        cells.append(level_text(k, n))
        if n >= MIN_LEVEL:
            rates.append(k / n)
    return cells, f"{100 * min(rates):.0f}% to {100 * max(rates):.0f}%" if rates else "–"


def level_table(df: pd.DataFrame, feat: str) -> list[str]:
    prompts = df.drop_duplicates("item_id")
    levels = list(prompts[feat].value_counts().index)
    rows = []
    for p in ANALYSED:
        cells, spread = level_row(df[df["platform"] == p], feat, levels)
        rows.append([PLATFORM_NAMES[p] + (" (gave the name)" if p in GAVE_NAME else ""), *cells, spread])
    header = ["Platform", *[f"{lv} ({(prompts[feat] == lv).sum()} prompts)" for lv in levels], f"Range over levels with {MIN_LEVEL}+ cells"]
    return md_table(header, rows)


def named_locations_table(df: pd.DataFrame) -> list[str]:
    missing = [lv for lv in NAMED_LOCATIONS if lv not in set(df["deletion_location"])]
    if missing:
        raise ValueError(f"deletion_location levels not in the coding: {missing}; found {sorted(set(df['deletion_location']))}")
    rows = [[PLATFORM_NAMES[p] + (" (gave the name)" if p in GAVE_NAME else ""), *level_row(df[df["platform"] == p], "deletion_location", NAMED_LOCATIONS)[0]] for p in ANALYSED]
    return md_table(["Platform", *NAMED_LOCATIONS], rows)


def refusal_tables(df: pd.DataFrame) -> list[str]:
    """Retrieved / declined citing the request / not retrieved, by what is asked. Reviewed refusals only."""
    reviewed = reviewed_codes()
    cells = df[df["platform"].isin(REFUSAL_PLATFORMS) & df["recoverability"].isin(KNOWN + ("INDETERMINATE",))].copy()
    cells["result"] = "not retrieved"
    cells.loc[cells["recoverability"] == "RECOVERED", "result"] = "retrieved"
    cells.loc[(cells["result"] == "not retrieved") & (cells["cell_id"].map(reviewed) == "REFUSAL"), "result"] = "declined"
    lines = []
    for p in REFUSAL_PLATFORMS:
        g = cells[cells["platform"] == p]
        unreviewed = int(((g["result"] == "not retrieved") & ~g["cell_id"].isin(reviewed)).sum())
        lines += [f"**{PLATFORM_NAMES[p]}**: {len(g)} cells with a recall, {(g['result'] == 'declined').sum()} reviewed refusals, "
                  f"{unreviewed} not-retrieved cells without a review (counted as not retrieved).", ""]
        for feat in REFUSAL_FEATURES:
            rows = [[lv, *[int(((s["result"]) == r).sum()) for r in ("retrieved", "declined", "not retrieved")]] for lv, s in g.groupby(feat)]
            lines += md_table([feat.replace("_", " ").capitalize(), "Retrieved", "Declined citing the request", "Not retrieved"], rows) + [""]
    return lines


def main() -> None:
    df = coded_cells()
    known = df[df["recoverability"].isin(KNOWN)]
    outcomes = with_outcome(df)
    lines = [
        "# Does the wording of a forget request change the outcome?",
        "",
        f"> **AS IT STANDS ({date.today().isoformat()}).** NL-forget study, {len(df)} erased cells "
        f"({len(known)} with a known outcome). Re-run after each recall batch "
        "(`.venv/bin/python -m src.outcome_by_prompt_features`).",
        "",
        "## A. Outcome at each level of each coded feature",
        "",
        "Wording features are the final human coding of the 138 prompts. Each cell reads "
        "**came back of known** (the fact came back in a new conversation, out of cells with a known outcome) "
        f"with a Wilson 95% interval. Levels with fewer than {MIN_LEVEL} cells show counts only and are left out of the range. "
        "\"–\" means no known outcome. Can't tell is not folded into either result. No tests: with so little variation "
        "a non-significant test shows little. "
        f"{' and '.join(LEFT_OUT.values())} are left out because every cell is can't tell. "
        "Copilot's recall is still in progress, so its levels hold few cells. "
        "Perplexity's outcome is gave versus withheld the name, over all its recalled cells.",
        "",
    ]
    for feat in FEATURES:
        lines += [f"### {feat.replace('_', ' ').capitalize()}", "", *level_table(outcomes, feat), ""]
        if feat == "deletion_location":
            lines += ["Named cases (deletion from memory, from the backend database, of the whole account):", "",
                      *named_locations_table(outcomes), ""]
    lines += ["## C. Refusals against what is asked", "",
              "Each cell is retrieved, declined citing the request (human-reviewed refusals only), or not retrieved. Counts only, no tests.", "",
              *refusal_tables(df)]
    for line in lines:
        print(line)
    print(f"report saved -> {save_report('outcome_by_prompt_features', lines, fenced=False)}")


if __name__ == "__main__":
    main()
