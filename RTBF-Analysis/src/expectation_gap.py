"""
Expectation-to-outcome tables, method by method (task D8, carries D7).

Table A, one row per erasure method:
  survey expectation (Q4.4/Q5.4) -> documented commitment -> acknowledgment
  (coded at erasure) -> recall outcome (recoverability from audit_outcomes).
Table B, platform x method: recall outcome per cell group.

Expected feedback (Q7.1 current, Q7.2 wanted) was asked once per participant,
not per method, so it is reported as its own block, never spread across rows.

Survey side: pooled over both scenarios, base = 354 observations (177 paired
participants x 2 scenarios); Q7 base = 177 participants.
Audit side: recoverability comes from src.audit_outcomes.derive, so the rules
(what counts as RECOVERED / NOT RECOVERED / INDETERMINATE) live in one place.
A Table B cell reads "recovered/decided", where decided = RECOVERED + NOT
RECOVERED; cells that are indeterminate, waiting, held or gated are counted
beside it, never folded into the fraction.

Two readings of recall, side by side (exploratory, 2026-10-20; the paper's rule is
still the strict one):
  strict          audit_outcomes as is: a miss counts only where the injection
                  reply showed or claimed a save ("shown"/"claimed").
  platform-level  a miss also counts on a platform that has, elsewhere in this
                  data, brought back a fact it never announced saving (a RECOVERED
                  cell with retention outside "shown"/"claimed"). Silence at
                  injection is not evidence of non-storage on such a platform.
                  "denied" cells stay indeterminate; platforms with no such
                  evidence (e.g. DeepSeek, no cross-chat memory) stay strict.

Re-run after every recall batch:
    .venv/bin/python -m src.expectation_gap
"""

from collections import Counter
from pathlib import Path

import pandas as pd

from src.audit_outcomes import RETAINED, derive, load_cells
from src.reporting import save_report
from src.screen import get_bases

OUT_METHODS = Path("outputs/tables/expectation_gap_methods.csv")
OUT_PLATFORM = Path("outputs/tables/expectation_gap_platform.csv")
OUT_TEX_METHOD = Path("outputs/tables/expectation_gap_method.tex")
OUT_TEX_PLATFORM = Path("outputs/tables/expectation_gap_platform.tex")

SCEN = {"less": ("Q4.2", "Q4.4"), "more": ("Q5.2", "Q5.4")}
EXPECT_OPTS = {  # Q4.4/Q5.4 option suffix -> short label
    4: "no future-chat reference",
    1: "permanently deleted",
    6: "not sure",
}
TYPED = "Type a message asking the AI Chatbot to forget it."

# Survey method (Q4.2/Q5.2 text) -> audit erasure labels (workbook "Erasure desc" / "Erasure").
# Copilot "Conversation history deletion" is the per-conversation sidebar delete
# (tester/flows/copilot.py, note 4), and Gemini "Delete all activity" clears all chats.
SURVEY_TO_ERASURES: dict[str, set[str]] = {
    "Delete this single conversation.": {
        "Delete conversation", "Delete single conversation", "Delete single thread",
        "Conversation history deletion",
    },
    "Clear all conversation history.": {
        "Clear all chat history (bulk)", "Delete all threads", "Delete all activity", "Delete all history",
    },
    "Delete a specific saved memory or fact.": {
        "Delete individual memory edit", "Delete individual memory", "Delete single Saved info item",
        "Granular facts editor",
    },
    TYPED: {"NL forget command", "NL forget prompt"},
    "Clear all saved memories.": {"Clear all memories", "Delete all Saved info", "Delete all memory"},
    "Privacy dashboard or account-level data management page.": {"Privacy Dashboard"},
    "Delete my account entirely.": set(),
}
AUDIT_ONLY = {"MAXIMAL", "Clear custom instructions"}  # no survey counterpart
PLATFORMS = ["chatgpt", "claude", "gemini", "copilot", "perplexity", "deepseek"]
PLATFORM_NAMES = {
    "chatgpt": "ChatGPT", "claude": "Claude", "gemini": "Gemini",
    "copilot": "Copilot", "perplexity": "Perplexity", "deepseek": "DeepSeek",
}
EXTRA_LABELS = {"INDETERMINATE": "can't tell", "waiting": "waiting", "held": "held", "gated": "gated"}
# Kept in the CSVs but left out of the short report: Privacy dashboard is parked
# (2026-10-20), delete account is survey-only, the two audit-only rows have no survey side.
REPORT_SKIP = {
    "Privacy dashboard or account-level data management page.", "Delete my account entirely.",
    "(audit only) Clear custom instructions", "(audit only) MAXIMAL",
}
SHORT = {  # report row names
    "Delete this single conversation.": "Delete one conversation",
    "Clear all conversation history.": "Clear all conversations",
    "Delete a specific saved memory or fact.": "Delete one saved memory",
    f"{TYPED} [138 participant prompts]": "Type \"forget\" (138 participant prompts)",
    f"{TYPED} [battery command]": "Type \"forget\" (battery command)",
    "Clear all saved memories.": "Clear all saved memories",
    "Privacy dashboard or account-level data management page.": "Privacy dashboard",
    "Delete my account entirely.": "Delete account",
    "(audit only) Clear custom instructions": "Clear custom instructions (audit only)",
    "(audit only) MAXIMAL": "MAXIMAL, all methods combined (audit only)",
}


def row_label(survey_method: str, sheet: str) -> str:
    """Typed erasure splits in two: the battery's fixed command vs the 138 participant prompts."""
    if survey_method != TYPED:
        return survey_method
    return f"{TYPED} [battery command]" if sheet == "MASTER" else f"{TYPED} [138 participant prompts]"


def audit_rows() -> pd.DataFrame:
    erasure_to_survey = {e: m for m, es in SURVEY_TO_ERASURES.items() for e in es}
    rows = [derive(c) for c in load_cells()]
    df = pd.DataFrame(rows)
    unknown = set(df["erasure"]) - set(erasure_to_survey) - AUDIT_ONLY
    if unknown:
        raise ValueError(f"erasure labels with no mapping, add them to SURVEY_TO_ERASURES or AUDIT_ONLY: {unknown}")
    df["survey_method"] = df["erasure"].map(erasure_to_survey).fillna("(no survey counterpart)")
    df["method"] = [
        row_label(m, s) if m != "(no survey counterpart)" else f"(audit only) {e}"
        for m, s, e in zip(df["survey_method"], df["sheet"], df["erasure"])
    ]
    return df


def silent_retainers(audit: pd.DataFrame) -> dict[str, list[str]]:
    """Platforms with at least one RECOVERED cell whose injection reply announced no save."""
    silent = audit[
        (audit["recoverability"] == "RECOVERED")
        & ~audit["retention"].isin([*RETAINED, "file", ""])
    ]
    return {p: sorted(g["cell_id"]) for p, g in silent.groupby("platform")}


def add_platform_level(audit: pd.DataFrame, retainers: dict[str, list[str]]) -> pd.DataFrame:
    counts = (
        (audit["recoverability"] == "INDETERMINATE")
        & audit["platform"].isin(retainers)
        & (audit["retention"] != "denied")
    )
    audit["recoverability_platform"] = audit["recoverability"].where(~counts, "NOT RECOVERED")
    return audit


def outcome_class(run_status: str, recov: str) -> str:
    """Bucket a cell for Table B. Every empty-looking cell gets its own reason."""
    if run_status == "NOT RUN":
        return "gated"        # structurally impossible (Perplexity free tier)
    if run_status == "INJECTED":
        return "held"         # injected, erasure not run by design (frozen NL-forget prompts)
    if recov in ("RECOVERED", "NOT RECOVERED", "INDETERMINATE"):
        return recov
    return "waiting"          # erased, recall not recorded or still in review


def summarize(g: pd.DataFrame, col: str = "recoverability") -> dict[str, int | str]:
    c = Counter(outcome_class(s, r) for s, r in zip(g["run_status"], g[col]))
    rec, notrec = c["RECOVERED"], c["NOT RECOVERED"]
    extras = [f"{c[k]} {EXTRA_LABELS[k]}" for k in EXTRA_LABELS if c[k]]
    shown = f"{rec} of {rec + notrec}" if rec + notrec else "none known"
    return {
        "cells": len(g), "recovered": rec, "not_recovered": notrec, "indeterminate": c["INDETERMINATE"],
        "waiting": c["waiting"], "held": c["held"], "gated": c["gated"],
        "cell": shown + (f" ({', '.join(extras)})" if extras else ""),
        "decided": shown,
    }


def survey_expectations() -> tuple[pd.DataFrame, int]:
    bases = get_bases(verbose=False)
    obs = []
    for mcol, qexp in SCEN.values():
        df = bases["paired"]
        part = pd.DataFrame({"survey_method": df[mcol]})
        for i in EXPECT_OPTS:
            part[EXPECT_OPTS[i]] = df[f"{qexp}_{i}"].notna()
        obs.append(part)
    pooled = pd.concat(obs, ignore_index=True)
    n_obs = len(pooled)
    out = pooled.groupby("survey_method").agg(
        n=("survey_method", "size"), **{lab: (lab, "mean") for lab in EXPECT_OPTS.values()}
    )
    for lab in EXPECT_OPTS.values():
        out[lab] = (100 * out[lab]).round(1)
    return out, n_obs


def feedback_block() -> list[str]:
    """Q7.2 feedback wanted (asked once per participant, select-all). Labels read from the cells."""
    df = get_bases(verbose=False)["paired"]
    n = len(df)
    rows = []
    for col in [c for c in df.columns if c.startswith("Q7.2_") and not c.endswith("_TEXT")]:
        vals = df[col].dropna()
        if len(vals):
            rows.append((100 * len(vals) / n, vals.iloc[0]))
    rows.sort(reverse=True)
    return md_table(["Feedback wanted", "Share of 177 participants"], [[label, f"{pct:.0f}%"] for pct, label in rows])


def counts_str(series: pd.Series) -> str:
    vc = series.replace("", "(not coded)").value_counts()
    return "; ".join(f"{k} {v}" for k, v in vc.items())


def ack_summary(g: pd.DataFrame) -> str:
    """Hand-coded acknowledgment of erased cells, most frequent first; UI erasures have no reply."""
    erased = g[g["run_status"].isin(["ERASED", "RECALLED"])]["acknowledgment"]
    codes = erased[(erased != "") & (erased != "NO REPLY (UI ACTION)")]
    if codes.empty:
        return "no reply (button or setting)" if (erased == "NO REPLY (UI ACTION)").any() else "no erased cells"
    names = {"COMPLIED": "said it was done", "PARTIAL": "partly done or hedged",
             "DEFLECTED": "sent the user elsewhere", "REFUSED": "refused",
             "SILENTLY IGNORED": "ignored the request", "OTHER": "other"}
    return ", ".join(f"{names.get(k, k.lower())} {v}" for k, v in codes.value_counts().items())


def build_table_a(audit: pd.DataFrame, survey: pd.DataFrame) -> pd.DataFrame:
    rows = []
    order = [*SURVEY_TO_ERASURES, "(no survey counterpart)"]
    for survey_method in order:
        sub = audit[audit["survey_method"] == survey_method]
        labels = sorted(sub["method"].unique()) or [survey_method]
        for label in labels:
            g = sub[sub["method"] == label]
            row: dict[str, object] = {"method": label}
            if survey_method in survey.index:
                s = survey.loc[survey_method]
                row["survey_n"] = int(s["n"])
                for lab in EXPECT_OPTS.values():
                    row[f"expect: {lab} %"] = s[lab]
            else:
                row["survey_n"] = 0
            row["platforms"] = ", ".join(p for p in PLATFORMS if p in set(g["platform"]))
            row["commitment"] = counts_str(g["commitment"]) if len(g) else "(not in audit)"
            erased = g[g["run_status"].isin(["ERASED", "RECALLED"])]
            row["acknowledgment"] = counts_str(erased["acknowledgment"]) if len(erased) else "-"
            row.update(summarize(g) if len(g) else {"cell": "(not in audit)"})
            row["cell_platform"] = summarize(g, "recoverability_platform")["cell"] if len(g) else "(not in audit)"
            rows.append(row)
    return pd.DataFrame(rows)


def build_table_b(audit: pd.DataFrame, col: str = "recoverability") -> tuple[pd.DataFrame, pd.DataFrame]:
    methods = build_order(audit)
    table = pd.DataFrame(index=methods, columns=PLATFORMS, dtype=object)
    long_rows = []
    for m in methods:
        for p in PLATFORMS:
            g = audit[(audit["method"] == m) & (audit["platform"] == p)]
            if g.empty:
                table.loc[m, p] = "not tested"   # platform has no such method in the audit design
                continue
            s = summarize(g, col)
            table.loc[m, p] = s["decided"]
            long_rows.append({"method": m, "platform": p, "reading": col, **s})
    return table, pd.DataFrame(long_rows)


PAPER_ROWS = {  # survey method -> row name in the paper's tables (both typed-forget sets are one row)
    "Delete this single conversation.": "Delete one conversation",
    "Clear all conversation history.": "Clear all history",
    "Delete a specific saved memory or fact.": "Delete one saved memory",
    TYPED: "Ask the chatbot to forget",
    "Clear all saved memories.": "Clear all saved memories",
}
ACK_SHORT = {
    "COMPLIED": "done", "PARTIAL": "partly done", "DEFLECTED": "sent elsewhere",
    "REFUSED": "refused", "SILENTLY IGNORED": "ignored", "OTHER": "other",
}


def paper_ack(g: pd.DataFrame) -> str:
    """Compact platform reply at deletion for the paper table; buttons give no reply."""
    erased = g[g["run_status"].isin(["ERASED", "RECALLED"])]["acknowledgment"]
    codes = erased[(erased != "") & (erased != "NO REPLY (UI ACTION)")]
    if codes.empty:
        return "No reply (button)"
    codes = codes.map(lambda k: ACK_SHORT.get(k, k.lower()))
    return "; ".join(f"{k} {v}" for k, v in codes.value_counts().items())


def latex_method_table(audit: pd.DataFrame, survey: pd.DataFrame) -> list[str]:
    """Paper Table A: survey expectation, documented commitment, platform reply and recall, per method."""
    rows = []
    for survey_method, name in PAPER_ROWS.items():
        g = audit[audit["survey_method"] == survey_method]
        s, c = survey.loc[survey_method], summarize(g)
        pending = c["waiting"] + c["held"] + c["gated"]
        rows.append(
            f"{name} & {int(s['n'])} & {s[EXPECT_OPTS[4]]:.0f} & {s[EXPECT_OPTS[1]]:.0f} "
            f"& {(g['commitment'] == 'DELETES').sum()} of {len(g)} & {paper_ack(g)} "
            f"& {c['recovered']} & {c['not_recovered']} & {c['indeterminate']} & {pending} \\\\"
        )
    return rows


def latex_platform_table(audit: pd.DataFrame) -> list[str]:
    """Paper Table B: recall success out of known outcomes, per method and platform."""
    rows = []
    for survey_method, name in PAPER_ROWS.items():
        cells = []
        for platform in PLATFORMS:
            g = audit[(audit["survey_method"] == survey_method) & (audit["platform"] == platform)]
            cells.append("n/a" if g.empty else summarize(g)["decided"].replace("none known", "--"))
        rows.append(f"{name} & " + " & ".join(cells) + " \\\\")
    return rows


def build_order(audit: pd.DataFrame) -> list[str]:
    order = []
    for survey_method in [*SURVEY_TO_ERASURES, "(no survey counterpart)"]:
        order += sorted(audit.loc[audit["survey_method"] == survey_method, "method"].unique())
    return order


def md_table(header: list[str], rows: list[list[object]]) -> list[str]:
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(v) for v in r) + " |" for r in rows]
    return out


def platform_table(table: pd.DataFrame) -> list[str]:
    rows = [[SHORT.get(m, m), *table.loc[m]] for m in table.index if m not in REPORT_SKIP]
    return md_table(["Method", *[PLATFORM_NAMES[p] for p in PLATFORMS]], rows)


def main() -> None:
    audit = audit_rows()
    retainers = silent_retainers(audit)
    audit = add_platform_level(audit, retainers)
    survey, n_obs = survey_expectations()
    table_a = build_table_a(audit, survey)
    table_b, long_strict = build_table_b(audit)
    table_b_platform, long_platform = build_table_b(audit, "recoverability_platform")
    table_b_long = pd.concat([long_strict, long_platform], ignore_index=True)

    OUT_METHODS.parent.mkdir(parents=True, exist_ok=True)
    table_a.to_csv(OUT_METHODS, index=False)
    OUT_TEX_METHOD.write_text("\n".join(latex_method_table(audit, survey)) + "\n")
    OUT_TEX_PLATFORM.write_text("\n".join(latex_platform_table(audit)) + "\n")
    table_b_long.to_csv(OUT_PLATFORM, index=False)

    deletes = audit.groupby("method")["commitment"].apply(lambda c: f"{(c == 'DELETES').sum()} of {len(c)}")
    report_a = table_a[~table_a["method"].isin(REPORT_SKIP)]
    rows_a, rows_sens, reply_lines = [], [], []
    for _, r in report_a.iterrows():
        name = SHORT.get(r["method"], r["method"])
        g = audit[audit["method"] == r["method"]]
        sens = summarize(g, "recoverability_platform")
        rows_a.append([
            name, f"{r[f'expect: {EXPECT_OPTS[4]} %']:.0f}%", deletes[r["method"]],
            int(r["recovered"]), int(r["not_recovered"]),
        ])
        rows_sens.append([name, sens["recovered"], sens["not_recovered"]])
        reply_lines.append(f"- **{name}:** {ack_summary(g)}")

    lines = [
        "# What users expect vs. what happened",
        "",
        "**How to read this report.** About a month after erasure, we asked for the fact in a new conversation.",
        "",
        "- **Recall success**: the token was retrieved, so the erasure failed.",
        "- **Recall failed**: the token was not retrieved, and the platform had shown or said it saved the fact, "
        "so the erasure succeeded.",
        "- Cells where we can't tell (the platform never showed or said it saved the fact) and cells not "
        "recalled yet are left out of the counts.",
        "",
        "## 1. By method",
        "",
        "**Users who expect it gone** is the share of survey answers (354 observations) that chose this method "
        "and expect the fact never to come up in future chats. **Policy says it deletes** counts the cells where "
        "the platform's own documentation says the method deletes the data.",
        "",
        *md_table(
            ["Method", "Users who expect it gone", "Policy says it deletes", "Recall success", "Recall failed"],
            rows_a,
        ),
        "",
        "## 2. What the platform replied at erasure",
        "",
        "Hand-coded replies to the erasure (two coders, Gwet's AC1 = 0.969). Buttons and settings give no reply.",
        "",
        *reply_lines,
        "",
        "## 3. By platform",
        "",
        "Each cell reads **recall success out of all cells with a known outcome**. "
        "\"none known\" = tested, but no cell has a known outcome yet; \"not tested\" = the platform has no such "
        "method in the audit.",
        "",
        *platform_table(table_b),
        "",
        "## 4. Sensitivity check (exploratory, not the paper's rule)",
        "",
        "If a platform has ever retrieved a fact it never said it saved, we assume it can keep facts silently, "
        "so its can't-tell cells count as recall failed.",
        "",
        "By method:",
        "",
        *md_table(["Method", "Recall success", "Recall failed"], rows_sens),
        "",
        "By platform (recall success out of all cells with a known outcome):",
        "",
        *platform_table(table_b_platform),
        "",
        "## 5. Feedback users want after deleting (asked once per participant)",
        "",
        *feedback_block(),
        "",
        f"Full detail (waiting, held, can't tell, cell lists): `{OUT_METHODS}`, `{OUT_PLATFORM}`",
    ]

    path = save_report("expectation_gap", lines, fenced=False)
    print(f"report saved -> {path}")



if __name__ == "__main__":
    main()
