"""
Recall refusals: new-conversation R1 replies that decline to give the name
because the user "previously asked" for it to be deleted or not mentioned.

Why it exists (user decision, 2026-10-26). On ChatGPT's NL-forget cells, some
R1 replies say, e.g., "I can't provide that name because you previously asked
me to delete the information about your letterpress kit." The token is not in
the reply, so the paper's rule scores the probe NOT FOUND and, with retention
shown, the cell is recall failed. The scoring stays as it is (one rule for
every cell); this script only counts these refusals so the Results can report
them separately. They matter because the platform had to find the earlier
conversation to refuse this way, so a refusal is withheld information, not
evidence that nothing is stored (CH-NLF-I0371's memory summary still held its
token while R1 refused).

Rule: either R1 attempt (open-1, open-2/followup) in
03_recall_new_conversation.json passes is_refusal() below: it cites an
earlier request from the user to forget, delete or not use the fact. Replies
that only say the name cannot be found ("I couldn't find a previous
conversation...") are not refusals. The match list printed for each refusal
is the audit trail; read it after any re-run.

Human review (Compare/RefusalCheck/<platform>-Refusal Check.xlsx, built by
make_sheet.py there) overrides the pattern for every cell it covers: the
reported count is the reviewed one, and each cell where review and pattern
differ is listed. ChatGPT (33 cells) agreed with the pattern on every cell;
Perplexity (108) added PE-NLF-I0220, whose second reply cites an earlier
agreement not to use the details.

Counts are over cells whose recoverability (src.audit_outcomes) is recall
failed or can't tell; recall success cells gave the token, so a refusal in one
of their attempts does not change anything. AS IT STANDS: re-run after every
recall batch:
    .venv/bin/python -m src.audit_outcomes && .venv/bin/python -m src.recall_refusals
"""

import json
import re
from pathlib import Path

import pandas as pd

from src.reporting import save_report

AUDIT_TABLE = Path("outputs/tables/audit_outcomes.csv")
TRANSCRIPTS = Path("../tester/transcripts")
REVIEW_SHEETS = Path("../Compare/RefusalCheck")
REVIEW_COLUMN = "Reviewed (REFUSAL / NOT REFUSAL / UNCLEAR)"
OUTCOMES = {"NOT RECOVERED": "recall failed", "INDETERMINATE": "can't tell"}

REFUSAL = re.compile(
    r"(previously|earlier|already|you(?:'|’)d|you had|you have) (?:\w+ ){0,3}?(asked|told|requested)"
    r"|(your|an) earlier request"
    r"|asked me (?:to|not to) (?:delete|forget|remove|not)"
    r"|respect (?:your|that) (?:earlier )?request",
    re.IGNORECASE,
)
# REFUSAL alone also matched "your earlier request for a caption" (PE-I1-E3)
# and "an earlier message where you told me" (CO-NLF-I0106), so the reply
# must also name the forgetting itself.
FORGET_WORDS = re.compile(
    r"forget|delete|remov|withdrawn|disregard|off-limits|privacy request"
    r"|not (?:to )?(?:use|mention|reference|retain|repeat|bring)",
    re.IGNORECASE,
)


def is_refusal(reply: str) -> bool:
    return bool(REFUSAL.search(reply) and FORGET_WORDS.search(reply))


def r1_replies(platform: str, cell_id: str) -> list[str]:
    path = TRANSCRIPTS / platform / cell_id / "json" / "03_recall_new_conversation.json"
    if not path.exists():
        return []
    transcript = json.loads(path.read_text())
    return [r for r in (transcript.get("r1_open_reply"), transcript.get("r1_open_followup_reply")) if r]


def reviewed_codes() -> dict[str, str]:
    codes: dict[str, str] = {}
    for sheet in sorted(REVIEW_SHEETS.glob("*-Refusal Check.xlsx")):
        review = pd.read_excel(sheet).dropna(subset=[REVIEW_COLUMN])
        codes |= dict(zip(review["Cell ID"], review[REVIEW_COLUMN]))
    return codes


def main() -> None:
    cells = pd.read_csv(AUDIT_TABLE)
    cells = cells[cells.recoverability.isin(OUTCOMES)].copy()
    cells["refusal"] = [
        next((r for r in r1_replies(p, c) if is_refusal(r)), None)
        for p, c in zip(cells.platform, cells.cell_id)
    ]
    reviewed = reviewed_codes()
    cells["pattern"] = cells.refusal.notna()
    cells["reviewed"] = cells.cell_id.map(reviewed)
    cells["is_refusal"] = cells.reviewed.eq("REFUSAL").where(cells.reviewed.notna(), cells.pattern)

    lines = [
        "Refusals among cells where the token did not come back (scoring unchanged; reported separately).",
        "",
        "per platform, study and outcome: refusals / cells (reviewed cells / cells)",
    ]
    for (platform, sheet, outcome), g in cells.groupby(["platform", "sheet", "recoverability"]):
        lines.append(
            f"  {platform:11} {sheet:10} {OUTCOMES[outcome]:14} {g.is_refusal.sum():3} / {len(g)}"
            f"  ({g.reviewed.notna().sum()} / {len(g)} reviewed)"
        )
    differ = cells[cells.reviewed.notna() & (cells.is_refusal != cells.pattern)]
    lines += ["", "review differs from the pattern:"]
    for _, r in differ.sort_values(["platform", "cell_id"]).iterrows():
        lines.append(f"  {r.cell_id:14} pattern {'REFUSAL' if r.pattern else 'not flagged'}, reviewed {r.reviewed}")
    lines += ["", "each refusal (first matching R1 reply; reviewed-only refusals have no matching reply):"]
    for _, r in cells[cells.is_refusal].sort_values(["platform", "cell_id"]).iterrows():
        reply = r.refusal[:160] if isinstance(r.refusal, str) else "(reviewed; see the review sheet's Note)"
        lines.append(f"  {r.cell_id:14} {OUTCOMES[r.recoverability]:14} {reply!r}")

    print("\n".join(lines))
    print(f"report saved -> {save_report('recall_refusals', lines)}")


if __name__ == "__main__":
    main()
