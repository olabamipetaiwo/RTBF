"""Build the refusal review sheet for one platform.

Why: src/recall_refusals.py flags new-conversation R1 replies that decline to
give the name by citing the user's earlier erasure request. That flag comes
from a pattern search, so before the count is reported we review every R1 reply
it could apply to: all recalled cells whose outcome is recall failed or can't
tell (the token did not come back). The search's own flag is shown so the
review also checks it.

Code:
  REFUSAL      a reply declines to give the name by citing an earlier request
               from the user to forget, delete or not use it
  NOT REFUSAL  anything else (e.g. "I couldn't find a previous conversation...")
  UNCLEAR      cannot tell
Either R1 attempt counts.

Run from RTBF-Analysis/:  .venv/bin/python ../Compare/RefusalCheck/make_sheet.py chatgpt
"""

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, ".")
from src.recall_refusals import is_refusal  # the pattern search being checked

AUDIT_TABLE = Path("outputs/tables/audit_outcomes.csv")
TRANSCRIPTS = Path("../tester/transcripts")
OUT = Path("../Compare/RefusalCheck")
OUTCOMES = {"NOT RECOVERED": "recall failed", "INDETERMINATE": "can't tell"}


def main(platform: str) -> None:
    cells = pd.read_csv(AUDIT_TABLE)
    cells = cells[(cells.platform == platform) & cells.recoverability.isin(OUTCOMES)]
    rows = []
    for _, c in cells.sort_values("cell_id").iterrows():
        path = TRANSCRIPTS / platform / c.cell_id / "json" / "03_recall_new_conversation.json"
        if not path.exists():
            continue
        t = json.loads(path.read_text())
        replies = [t.get("r1_open_reply") or "", t.get("r1_open_followup_reply") or ""]
        rows.append({
            "Cell ID": c.cell_id, "Study": c.sheet, "Current outcome": OUTCOMES[c.recoverability],
            "Question": t.get("r1_open_sent"), "R1 reply 1": replies[0], "R1 reply 2": replies[1],
            "Pattern search flag": "REFUSAL" if any(is_refusal(r) for r in replies) else "",
            "Reviewed (REFUSAL / NOT REFUSAL / UNCLEAR)": "", "Note": "",
        })
    out = OUT / f"{platform}-Refusal Check.xlsx"
    pd.DataFrame(rows).to_excel(out, index=False)
    print(f"{len(rows)} cells -> {out}")


if __name__ == "__main__":
    main(sys.argv[1].lower())
