"""
Section 5.1 numbers, from one source: outcomes per agent, per data deletion method,
and the headline split.

Reads outputs/tables/audit_outcomes_provisional.csv (src.provisional_fill: real results
plus placeholders for cells not recalled yet) and keeps the 865 erased test cases
(NOT RECALLED rows are not test cases). Outcome mapping:

    RECOVERED      -> recall success
    NOT RECOVERED  -> recall failed
    INDETERMINATE  -> can't tell

Method groups are the survey-to-audit mapping in src.expectation_gap
(SURVEY_TO_ERASURES), so the groups here match the rest of Section 5. Typed requests
are every NL FORGET row plus the typed-command rows on the MASTER sheet.

Writes:
    outputs/tables/outcomes_by_agent.tex   (body rows for the Section 5.1 table)
    outputs/results/outcomes_by_agent.md   (every number quoted in Section 5.1)

AS IT STANDS: re-run after every recall batch:
    .venv/bin/python -m src.audit_outcomes && .venv/bin/python -m src.provisional_fill \
        && .venv/bin/python -m src.outcomes_by_agent
"""

from datetime import datetime
from pathlib import Path

import pandas as pd

from src.expectation_gap import PLATFORM_NAMES, PLATFORMS, SURVEY_TO_ERASURES, TYPED

IN_CSV = Path("outputs/tables/audit_outcomes_provisional.csv")
OUT_TEX = Path("outputs/tables/outcomes_by_agent.tex")
OUT_MD = Path("outputs/results/outcomes_by_agent.md")

OUTCOME = {"RECOVERED": "success", "NOT RECOVERED": "failed", "INDETERMINATE": "cant"}
UI_METHODS = {  # the four methods tested through UI actions, in report order
    "Deleting a single conversation": "Delete this single conversation.",
    "Clearing all conversation history": "Clear all conversation history.",
    "Deleting a specific saved memory": "Delete a specific saved memory or fact.",
    "Clearing all saved memories": "Clear all saved memories.",
}
ORDER = ["chatgpt", "claude", "copilot", "deepseek", "gemini", "perplexity"]
assert set(ORDER) == set(PLATFORMS)


def load() -> pd.DataFrame:
    df = pd.read_csv(IN_CSV, keep_default_na=False)
    df = df[df["recoverability"].isin(OUTCOME)].copy()  # drops NOT RECALLED
    df["outcome"] = df["recoverability"].map(OUTCOME)
    erasure_to_method = {e: m for m, es in SURVEY_TO_ERASURES.items() for e in es}
    df["method"] = [
        TYPED if sheet != "MASTER" else erasure_to_method.get(erasure, "other")
        for sheet, erasure in zip(df["sheet"], df["erasure"])
    ]
    return df


def counts(df: pd.DataFrame) -> pd.Series:
    c = df["outcome"].value_counts()
    return pd.Series({k: int(c.get(k, 0)) for k in ("success", "failed", "cant")})


def pct(part: int, whole: int) -> str:
    return f"{100 * part / whole:.1f}%"


def main() -> None:
    df = load()
    total = len(df)
    allc = counts(df)
    judged = allc["success"] + allc["failed"]

    by_agent = {p: counts(df[df["platform"] == p]) for p in ORDER}
    tex = [
        f"{PLATFORM_NAMES[p]} & {c['success']} & {c['failed']} & {c['cant']} & {c.sum()} \\\\"
        for p, c in by_agent.items()
    ]
    OUT_TEX.write_text("\n".join(tex) + "\n")

    lines = [
        "# outcomes_by_agent",
        "",
        f"_Run at {datetime.now().isoformat(timespec='seconds')}_",
        "",
        f"Source: {IN_CSV} ({total} erased test cases, placeholders included).",
        "",
        "## Headline",
        "",
        f"- Test cases: {total}; recall success {allc['success']} ({pct(allc['success'], total)}), "
        f"recall failed {allc['failed']} ({pct(allc['failed'], total)}), "
        f"can't tell {allc['cant']} ({pct(allc['cant'], total)}).",
        f"- Judgeable (recall success or recall failed): {judged} ({pct(judged, total)} of {total}); "
        f"the fact came back in {allc['success']} of them ({pct(allc['success'], judged)}).",
        f"- Share of all recall success that is ChatGPT's: {by_agent['chatgpt']['success']} of "
        f"{allc['success']} ({pct(by_agent['chatgpt']['success'], allc['success'])}).",
        "",
        "## Per agent (table rows)",
        "",
        "| Agent | Recall success | Recall failed | Can't tell | Test cases | Can't tell share |",
        "|---|---|---|---|---|---|",
        *[
            f"| {PLATFORM_NAMES[p]} | {c['success']} | {c['failed']} | {c['cant']} | {c.sum()} | "
            f"{pct(c['cant'], c.sum())} |"
            for p, c in by_agent.items()
        ],
        "",
        f"Can't tell share by agent ranges from "
        f"{min(100 * c['cant'] / c.sum() for c in by_agent.values()):.1f}% to "
        f"{max(100 * c['cant'] / c.sum() for c in by_agent.values()):.1f}%, but the six-agent range "
        "includes ChatGPT and Claude; the four agents the text calls mostly can't tell are: "
        + ", ".join(
            f"{PLATFORM_NAMES[p]} {pct(by_agent[p]['cant'], by_agent[p].sum())}"
            for p in ("copilot", "perplexity", "gemini", "deepseek")
        )
        + ".",
        "",
        "## Per data deletion method",
        "",
        "| Method | Test cases | Recall success | Share recall success | Recall failed | Can't tell |",
        "|---|---|---|---|---|---|",
    ]
    ui_shares = []
    for name, key in UI_METHODS.items():
        g = counts(df[df["method"] == key])
        ui_shares.append(100 * g["success"] / g.sum())
        lines.append(
            f"| {name} (UI actions) | {g.sum()} | {g['success']} | {pct(g['success'], g.sum())} | "
            f"{g['failed']} | {g['cant']} |"
        )
    t = counts(df[df["method"] == TYPED])
    lines += [
        f"| Sending a deletion-request prompt | {t.sum()} | {t['success']} | "
        f"{pct(t['success'], t.sum())} | {t['failed']} | {t['cant']} |",
        "",
        f"UI-action methods: recall success in {min(ui_shares):.0f}% to {max(ui_shares):.0f}% of "
        "their test cases.",
        f"Streams: {int((df['sheet'] == 'MASTER').sum())} on the MASTER sheet (UI actions, including "
        f"{int(((df['sheet'] == 'MASTER') & (df['method'] == TYPED)).sum())} typed commands) and "
        f"{int((df['sheet'] != 'MASTER').sum())} on the NL FORGET sheet (prompts).",
        "",
    ]
    OUT_MD.write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
