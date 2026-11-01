"""Build the retention review sheet for one platform.

Why: retention at injection is set by rule (tester/code_retention.py), from the
injection reply and an OCR read of the injection screenshot. It decides whether a
cell with no retrieved token is recall failed (retention shown or claimed: the
platform kept the fact, so the miss is evidence of erasure) or can't tell. No
person has checked it, so we review it where it matters: every recalled cell
whose outcome is recall failed or can't tell. (For recall-success cells,
retention does not affect the outcome.)

Codes are code_retention.py's own values, unchanged:
  shown         the interface displayed a memory notice ("Memory updated", ...)
  claimed       the reply says, in storage words, that it saved or will remember it
  denied        the reply says it cannot store the fact
  acknowledged  the reply reacts ("Noted!", "Got it") without saying it was stored
  no_signal     neither the reply nor the screen mentions storage

Run from RTBF-Analysis/:  .venv/bin/python ../Compare/RetentionCheck/make_sheet.py chatgpt
"""

import json
import sys
from pathlib import Path

import pandas as pd

AUDIT_TABLE = Path("outputs/tables/audit_outcomes.csv")
RETENTION = Path("../tester/data/retention_coding.csv")
TRANSCRIPTS = Path("../tester/transcripts")
OUT = Path("../Compare/RetentionCheck")
OUTCOMES = {"NOT RECOVERED": "recall failed", "INDETERMINATE": "can't tell"}


def main(platform: str) -> None:
    cells = pd.read_csv(AUDIT_TABLE)
    cells = cells[(cells.platform == platform) & cells.recoverability.isin(OUTCOMES)]
    coding = pd.read_csv(RETENTION).set_index("cell")
    rows = []
    for _, c in cells.sort_values("cell_id").iterrows():
        inject = TRANSCRIPTS / platform / c.cell_id / "json" / "01_inject.json"
        t = json.loads(inject.read_text()) if inject.exists() else {}
        r = coding.loc[c.cell_id] if c.cell_id in coding.index else {}
        rows.append({
            "Cell ID": c.cell_id, "Study": c.sheet, "Injection": c.injection,
            "Current outcome": OUTCOMES[c.recoverability],
            "Injection text sent": t.get("sent"), "Injection reply": t.get("reply"),
            "Screenshot": str((TRANSCRIPTS / platform / c.cell_id / "screenshots" / "01_inject.png").resolve()),
            "Rule's retention": r.get("retention"), "Rule's evidence": r.get("evidence"),
            "Evidence source": r.get("source"),
            "Reviewed retention (shown / claimed / denied / acknowledged / no_signal)": "", "Note": "",
        })
    out = OUT / f"{platform}-Retention Check.xlsx"
    pd.DataFrame(rows).to_excel(out, index=False)
    print(f"{len(rows)} cells -> {out}")


if __name__ == "__main__":
    main(sys.argv[1].lower())
