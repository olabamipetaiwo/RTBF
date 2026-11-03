"""
Section 5.3 numbers, from one source: what the agent said in reply to a typed
deletion request, against the recall outcome.

Reads outputs/tables/audit_outcomes_provisional.csv (src.provisional_fill) and keeps the
typed-request test cases that are in the 865 base (the NL FORGET sheet, 798 test cases).
Reply type is the hand-coded acknowledgment (Gwet's AC1 = 0.969), named with the agent reply types in paper/terms.txt. Outcome mapping:

    RECOVERED      -> recall success
    NOT RECOVERED  -> recall failed
    INDETERMINATE  -> can't tell

Writes:
    outputs/tables/replies_by_outcome.tex   (body rows for the Section 5.3 table)
    outputs/results/replies_by_outcome.md   (every number quoted in Section 5.3)

AS IT STANDS: re-run after every recall batch:
    .venv/bin/python -m src.audit_outcomes && .venv/bin/python -m src.provisional_fill \
        && .venv/bin/python -m src.replies_by_outcome
"""

from datetime import datetime
from pathlib import Path

import pandas as pd

from src.expectation_gap import PLATFORM_NAMES

IN_CSV = Path("outputs/tables/audit_outcomes_provisional.csv")
OUT_TEX = Path("outputs/tables/replies_by_outcome.tex")
OUT_MD = Path("outputs/results/replies_by_outcome.md")

OUTCOME = {"RECOVERED": "success", "NOT RECOVERED": "failed", "INDETERMINATE": "cant"}
REPLY_ORDER = [  # coded acknowledgment -> row label
    ("COMPLIED", "Complied"),
    ("PARTIAL", "Partial"),
    ("DEFLECTED", "Deflected"),
    ("REFUSED", "Refused"),
    ("SILENTLY IGNORED", "Silently ignored"),
    ("OTHER", "Other"),
    ("", "Not captured"),
]


def load() -> pd.DataFrame:
    df = pd.read_csv(IN_CSV, keep_default_na=False)
    df = df[(df["sheet"] == "NL FORGET") & df["recoverability"].isin(OUTCOME)].copy()
    df["outcome"] = df["recoverability"].map(OUTCOME)
    return df


def counts(g: pd.DataFrame) -> dict[str, int]:
    c = g["outcome"].value_counts()
    return {k: int(c.get(k, 0)) for k in ("success", "failed", "cant")}


def pct(part: int, whole: int) -> str:
    return f"{100 * part / whole:.1f}%"


def main() -> None:
    df = load()
    total = len(df)
    unknown = sorted(set(df["acknowledgment"]) - {code for code, _ in REPLY_ORDER})
    assert not unknown, f"unmapped acknowledgment codes: {unknown}"

    rows, md_rows = [], []
    for code, label in REPLY_ORDER:
        g = df[df["acknowledgment"] == code]
        if g.empty:
            continue
        c = counts(g)
        rows.append(f"{label} & {c['success']} & {c['failed']} & {c['cant']} & {len(g)} \\\\")
        md_rows.append(
            f"| {label} | {c['success']} | {c['failed']} | {c['cant']} | {len(g)} | "
            f"{pct(len(g), total)} |"
        )
    allc = counts(df)
    rows.append(f"All replies & {allc['success']} & {allc['failed']} & {allc['cant']} & {total} \\\\")
    md_rows.append(
        f"| All replies | {allc['success']} | {allc['failed']} | {allc['cant']} | {total} | 100.0% |"
    )
    OUT_TEX.write_text("\n".join(rows) + "\n")

    done = df[df["acknowledgment"] == "COMPLIED"]
    done_known = done[done["outcome"] != "cant"]
    lines = [
        "# replies_by_outcome",
        "",
        f"_Run at {datetime.now().isoformat(timespec='seconds')}_",
        "",
        f"Source: {IN_CSV} ({total} typed-request test cases, placeholders included).",
        "",
        "## Reply type against outcome (all agents)",
        "",
        "| Reply | Recall success | Recall failed | Can't tell | Test cases | Share of all |",
        "|---|---|---|---|---|---|",
        *md_rows,
        "",
        "## After a reply that complied",
        "",
        f"- Complied: {len(done)} test cases; {len(done_known)} with a known outcome "
        f"(recall success or recall failed); recall success in {int((done_known['outcome'] == 'success').sum())} "
        f"of those {len(done_known)}.",
        "",
        "## By agent (rows within an agent are comparable)",
        "",
        "| Agent | Reply | Recall success | Recall failed | Can't tell | Test cases |",
        "|---|---|---|---|---|---|",
    ]
    for p in ("chatgpt", "claude", "copilot", "deepseek", "gemini", "perplexity"):
        for code, label in REPLY_ORDER:
            g = df[(df["platform"] == p) & (df["acknowledgment"] == code)]
            if g.empty:
                continue
            c = counts(g)
            lines.append(
                f"| {PLATFORM_NAMES[p]} | {label} | {c['success']} | {c['failed']} | {c['cant']} | {len(g)} |"
            )
    lines.append("")
    OUT_MD.write_text("\n".join(lines))
    print("\n".join(lines[:30]))


if __name__ == "__main__":
    main()
