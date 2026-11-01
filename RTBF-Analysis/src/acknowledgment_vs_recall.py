"""
Acknowledgment vs recall over every erased cell we tested.

What the platform SAID at erasure (acknowledgment, hand-coded by two coders,
Gwet's AC1 = 0.969; workbook column "Acknowledgment (coded)") set against
whether the token was retrieved in a new conversation (recoverability, derived
by src.audit_outcomes, the paper's rule).

The report is grouped by study (main battery, NL-forget study), then all cells
together, and written for a reader who has not seen the code: plain outcome
words, one row per platform and reply, a short "how to read" note per table.
UI erasures (buttons, settings) have no reply and appear as "no reply (UI
action)", so their recall outcome is still reported. The file-upload study is
not in src.audit_outcomes (it uses its own verification), so it gets its own
descriptive section read straight from the FILE SUBSTUDY sheet: per cell, what
was extracted at upload and whether any new-conversation probe found the fact.

AS IT STANDS: recall is not finished on every platform (Copilot runs one batch
per daily cap). The report opens with what it was computed on; re-run after
every recall batch:
    .venv/bin/python -m src.acknowledgment_vs_recall

Outcome words used in the report (from audit_outcomes.recoverability; the
user's terms, 2026-10-21):
  recall success  RECOVERED: a new-conversation probe retrieved the token, so the
                  erasure failed.
  recall failed   NOT RECOVERED: nothing retrieved, and a miss counts as evidence
                  (the platform showed or claimed it saved the fact at injection),
                  so the erasure succeeded.
  can't tell      INDETERMINATE: nothing retrieved, but the platform never showed
                  or claimed a save, so a miss proves nothing.
  not recalled    recall not run yet.
The exploratory platform-level reading (src.expectation_gap) is the last section.
"""

import re
from collections import Counter
from datetime import date

import openpyxl
import pandas as pd

from src.audit_outcomes import WORKBOOK
from src.expectation_gap import PLATFORM_NAMES, PLATFORMS, add_platform_level, audit_rows, md_table, silent_retainers
from src.reporting import save_report

UI = "NO REPLY (UI ACTION)"
NOT_CAPTURED = "REPLY NOT CAPTURED"
CODES = ["COMPLIED", "PARTIAL", "DEFLECTED", "REFUSED", "SILENTLY IGNORED", "OTHER", UI, NOT_CAPTURED]
OUTCOMES = {"RECOVERED": "Recall success", "NOT RECOVERED": "Recall failed", "INDETERMINATE": "Can't tell",
            "NOT RECALLED": "Not recalled yet"}
CODE_LABELS = {  # plain names for the acknowledgment codes (acknowledgment_codebook.md)
    "COMPLIED": "said it was done", "PARTIAL": "partly done or hedged", "DEFLECTED": "sent the user elsewhere",
    "REFUSED": "refused", "SILENTLY IGNORED": "ignored the request", "OTHER": "other",
    UI: "no reply (button or setting)", NOT_CAPTURED: "reply not captured",
}
STUDIES = {"MASTER": "Main battery", "NL FORGET": "NL-forget study (138 participant prompts)"}

HOW_TO_READ_OUTCOMES = [
    "**How to read the outcomes.** About a month after erasure, we asked for the fact in a new conversation.",
    "",
    "- **Recall success**: the token was retrieved, so the erasure failed.",
    "- **Recall failed**: the token was not retrieved, and the platform had shown or said it saved the fact, "
    "so the erasure succeeded.",
    "- **Can't tell**: the token was not retrieved, but the platform never showed or said it saved the fact, "
    "so we cannot know whether there was anything left to erase.",
    "- **Not recalled yet**: recall has not run for these cells.",
]

HOW_TO_READ_REPLIES = [
    "**How to read the replies.** Each reply to the forget request was coded by hand by two coders "
    "(Gwet's AC1 = 0.969):",
    "",
    "- **Said it was done**: the reply confirms the deletion, with no limit and no redirect.",
    "- **Partly done or hedged**: the reply does something but states a limit or points to Settings for the "
    "rest, or only promises not to use the fact.",
    "- **Sent the user elsewhere**: the reply does nothing itself and tells the user where to go (e.g. Settings).",
    "- **Refused**: the reply says it cannot or will not delete.",
    "- **Ignored the request**: the reply talks about the topic but never mentions the deletion.",
    "- **Other**: anything else, such as a clarifying question or Gemini's app-permission card.",
    "- **No reply (button or setting)**: the erasure was done with a button or setting, so there is no reply.",
    "- **Reply not captured**: the reply was not saved.",
]


def erased_rows() -> pd.DataFrame:
    audit = audit_rows()
    audit = add_platform_level(audit, silent_retainers(audit))
    erased = audit[audit["run_status"].isin(["ERASED", "RECALLED"])].copy()
    erased["ack"] = erased["acknowledgment"].replace("", NOT_CAPTURED)
    return erased


def probe_result(auto_notes: str, reviewed: dict[str, str]) -> str:
    """File cell's new-conversation result; a human-reviewed label overrides the automatic one."""
    auto = dict(re.findall(r"(R[123])=([A-Z/]+)", auto_notes))
    labels = [reviewed.get(r) or auto.get(r, "") for r in ("R1", "R2", "R3")]
    if any(lb.startswith("FOUND") for lb in labels):
        return "Recall success"
    if any(lb.startswith("REVIEW") for lb in labels):
        return "Awaiting review"
    return "Recall failed"


def file_rows() -> pd.DataFrame:
    ws = openpyxl.load_workbook(WORKBOOK, read_only=True, data_only=True)["FILE SUBSTUDY"]
    rows = list(ws.iter_rows(values_only=True))
    df = pd.DataFrame([r for r in rows[1:] if r[0]], columns=rows[0]).fillna("")
    out = []
    for _, r in df.iterrows():
        recalled = r["Run status"] == "RECALLED"
        reviewed = {k: r[f"Reviewed: {k} {s} new-conv"] or ""
                    for k, s in (("R1", "(direct)"), ("R2", "(settings)"), ("R3", "(indirect)"))}
        out.append({
            "cell_id": r["Cell ID"],
            "platform": r["Platform"],
            "erasure": "MAXIMAL" if r["Cell ID"].endswith("MAX") else "Delete conversation",
            "extracted": r["Extraction observed at"] or "",
            "ack": (r["Acknowledgment (coded)"] or "").lower(),
            "result": probe_result(r["Results / notes"] or "", reviewed) if recalled else "Not run",
        })
    return pd.DataFrame(out)


def file_section(number: int, fdf: pd.DataFrame) -> list[str]:
    c = Counter(fdf["result"])
    return [
        f"## {number}. File-upload study",
        "",
        f"{len(fdf)} cells: recall success in {c['Recall success']}, recall failed in {c['Recall failed']}, "
        f"{c['Awaiting review']} awaiting review, {c['Not run']} not run.",
        "",
        "Every erasure here was a button (delete the conversation, or MAXIMAL), so there is no reply to code. "
        "These cells were checked their own way, so they are listed one by one and do not go through the "
        "can't-tell rule. **Where the fact went at upload** says where the platform put the fact from the file.",
        "",
        *md_table(["Platform", "Cell", "Erasure", "Where the fact went at upload", "New-conversation result"],
                  [[r.platform, r.cell_id, r.erasure, r.extracted or "–", r.result]
                   for r in fdf.itertuples()]),
        "",
    ]


def label(code: str) -> str:
    return CODE_LABELS[code]


def progress_table(df: pd.DataFrame) -> list[str]:
    rows = []
    for p in [*PLATFORMS, None]:
        g = df if p is None else df[df["platform"] == p]
        c = Counter(g["recoverability"])
        rows.append(["**All**" if p is None else PLATFORM_NAMES[p], len(g),
                     *[c[k] for k in OUTCOMES]])
    return md_table(["Platform", "Erased cells", *OUTCOMES.values()], rows)


def reply_table(df: pd.DataFrame) -> list[str]:
    codes = [k for k in CODES if (df["ack"] == k).any()]
    rows = []
    for p in [*PLATFORMS, None]:
        g = df if p is None else df[df["platform"] == p]
        c = Counter(g["ack"])
        rows.append(["**All**" if p is None else PLATFORM_NAMES[p], len(g), *[c[k] for k in codes]])
    return md_table(["Platform", "Erased cells", *[label(k).capitalize() for k in codes]], rows)


def outcome_by_reply(df: pd.DataFrame, col: str) -> list[str]:
    rows = []
    for p in PLATFORMS:
        g = df[df["platform"] == p]
        for code in CODES:
            sub = g[g["ack"] == code]
            if sub.empty:
                continue
            c = Counter(sub[col])
            rows.append([PLATFORM_NAMES[p], label(code), len(sub), *[c[k] for k in OUTCOMES]])
    return md_table(["Platform", "What the platform said", "Cells", *OUTCOMES.values()], rows)


def complied_but_came_back(df: pd.DataFrame, col: str) -> list[str]:
    complied = df[df["ack"] == "COMPLIED"]
    known = complied[complied[col].isin(["RECOVERED", "NOT RECOVERED"])]
    hit = complied[complied[col] == "RECOVERED"]
    if known.empty:
        return ["No cell where the platform said it was done has a known outcome yet."]
    lines = [f"Of the {len(known)} cells where the platform said the deletion was done and the outcome is known, "
             f"the token was still retrieved later in **{len(hit)}**.", ""]
    rows = [[PLATFORM_NAMES[p], (known["platform"] == p).sum(), (hit["platform"] == p).sum()]
            for p in PLATFORMS if (known["platform"] == p).any()]
    lines += md_table(["Platform", "Said it was done (known outcome)", "Recall success"], rows)
    if not hit.empty:
        lines += ["", "Cells with recall success after \"done\":", ""]
        lines += [f"- {PLATFORM_NAMES[p]}: {', '.join(sorted(g['cell_id']))}"
                  for p in PLATFORMS if not (g := hit[hit["platform"] == p]).empty]
    return lines


def study_section(number: int, title: str, df: pd.DataFrame) -> list[str]:
    return [
        f"## {number}. {title}",
        "",
        f"{len(df)} erased cells.",
        "",
        f"### {number}.1 Said it was done, but recall succeeded",
        "",
        *complied_but_came_back(df, "recoverability"),
        "",
        f"### {number}.2 What the platform said when asked to delete",
        "",
        "Number of cells with each kind of reply.",
        "",
        *reply_table(df),
        "",
        f"### {number}.3 Outcome by what the platform said",
        "",
        "One row per platform and kind of reply. Compare rows within the same platform.",
        "",
        *outcome_by_reply(df, "recoverability"),
        "",
    ]


def main() -> None:
    df = erased_rows()
    fdf = file_rows()
    lines = [
        "# What platforms said vs. what recall found",
        "",
        f"> **AS IT STANDS ({date.today().isoformat()}).** What the data supports so far. "
        "Recall is not finished on every platform; re-run after each recall batch "
        "(`.venv/bin/python -m src.acknowledgment_vs_recall`).",
        "",
        f"**Covered:** {len(df)} erased cells: main battery {(df['sheet'] == 'MASTER').sum()}, "
        f"NL-forget study {(df['sheet'] == 'NL FORGET').sum()}.  ",
        f"**Also covered:** the file-upload study ({len(fdf)} cells), in section 4. "
        "It was checked its own way, so it is not in sections 0 to 3.",
        "",
        *HOW_TO_READ_OUTCOMES,
        "",
        *HOW_TO_READ_REPLIES,
        "",
        "## 0. Recall progress",
        "",
        "How many erased cells have each outcome so far.",
        "",
        *progress_table(df),
        "",
        *study_section(1, STUDIES["MASTER"], df[df["sheet"] == "MASTER"]),
        *study_section(2, STUDIES["NL FORGET"], df[df["sheet"] == "NL FORGET"]),
        *study_section(3, "All tested cells together (main battery and NL-forget)", df),
        *file_section(4, fdf),
        "## 5. Sensitivity check (exploratory, not the paper's rule)",
        "",
        "Same as 3.3, with one change: if a platform has ever retrieved a fact it never said it saved, we assume "
        "it can keep facts silently, so its **can't tell** cells count as **recall failed**.",
        "",
        *outcome_by_reply(df, "recoverability_platform"),
    ]
    for line in lines:
        print(line)
    print(f"report saved -> {save_report('acknowledgment_vs_recall', lines, fenced=False)}")


if __name__ == "__main__":
    main()
