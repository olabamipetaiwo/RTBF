"""
Per-platform breakdown behind the platform analysis files (platforms/<platform>.md).

The outcome counts themselves come from src.audit_outcomes; this script adds the
cuts that platforms/how.md step 1 asks for, so every number quoted in a
platform file has a saved source (one-source rule):

  1. Which probe retrieved the token, for recall-success cells (R1, R2, R3, or
     the sibling rule).
  2. Same conversation against new conversation, for typed-erasure cells: the
     same-conversation R1 (never part of the outcome) crossed with the
     new-conversation outcome.
  3. Main-grid cells one by one: erasure method, probe results and outcome.
  4. Original tokens retrieved after replacement: main-grid cells that were
     re-injected with a new token after an account-wide erasure wiped them. The
     original tokens are read from the first committed token table (git commit
     ORIGINAL_TOKENS_COMMIT, RTBF-Prompt/token.md); a cell is listed when its new-
     conversation recall replies contain its original token instead of, or as
     well as, its current one.

Run after src.audit_outcomes, and again after every recall batch:
    .venv/bin/python -m src.audit_outcomes && .venv/bin/python -m src.platform_breakdown [platform ...]
With no platform names, every platform is reported.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

from src.reporting import save_report

AUDIT_TABLE = Path("outputs/tables/audit_outcomes.csv")
TRANSCRIPTS = Path("../tester/transcripts")
ORIGINAL_TOKENS_COMMIT = "34e3bc9"  # 2026-08-28, first committed token table
OUTCOME_WORDS = {"RECOVERED": "recall success", "NOT RECOVERED": "recall failed",
                 "INDETERMINATE": "can't tell", "NOT RECALLED": "not recalled", "PENDING REVIEW": "pending review"}
RECALL_REPLY_KEYS = ("r1_open_reply", "r1_open_followup_reply", "r3_reply", "r3_followup_reply", "r2_reply")


def original_tokens() -> dict[str, str]:
    table = subprocess.run(
        ["git", "show", f"{ORIGINAL_TOKENS_COMMIT}:RTBF-Prompt/token.md"],
        capture_output=True, text=True, check=True, cwd="..",
    ).stdout
    rows = (line.split("|") for line in table.splitlines() if line.startswith("| ") and "-I" in line)
    return {r[1].strip(): r[3].strip() for r in rows if len(r) > 3}


def recall_text(platform: str, cell_id: str) -> str:
    path = TRANSCRIPTS / platform / cell_id / "json" / "03_recall_new_conversation.json"
    if not path.exists():
        return ""
    transcript = json.loads(path.read_text())
    return " ".join(transcript.get(k) or "" for k in RECALL_REPLY_KEYS)


def platform_lines(cells: pd.DataFrame, originals: dict[str, str], current: dict[str, str]) -> list[str]:
    lines: list[str] = []
    for sheet, g in cells.groupby("sheet"):
        lines += [f"-- {sheet} --", "outcomes:"]
        for outcome, n in g.recoverability.value_counts().items():
            lines.append(f"  {OUTCOME_WORDS.get(outcome, outcome):15} {n}")

        success = g[g.recoverability == "RECOVERED"]
        lines.append(f"probe that retrieved the token ({len(success)} recall-success cells):")
        for reason, n in success.recoverability_reason.value_counts().items():
            lines.append(f"  {reason:60} {n}")
        lines.append(f"  R3 involved in {success.r3.eq('FOUND').sum()} of {len(success)}")

        typed = g[g.same_conversation_r1.isin(["FOUND", "NOT FOUND"])]
        if len(typed):
            lines.append(f"same conversation (rows) against new-conversation outcome (columns), {len(typed)} typed-erasure cells:")
            table = pd.crosstab(typed.same_conversation_r1, typed.recoverability.map(OUTCOME_WORDS))
            lines += ["  " + l for l in table.to_string().splitlines()]

        if sheet == "MASTER":
            lines.append("main-grid cells:")
            for _, r in g.sort_values(["erasure", "cell_id"]).iterrows():
                lines.append(
                    f"  {r.cell_id:12} {str(r.erasure)[:30]:30} R1={r.r1} R2={r.r2} R3={r.r3} "
                    f"-> {OUTCOME_WORDS.get(r.recoverability, r.recoverability)}"
                )
            replaced = [
                (r.cell_id, originals[r.cell_id])
                for _, r in g.iterrows()
                if r.cell_id in originals and originals[r.cell_id] != current.get(r.cell_id)
                and originals[r.cell_id].lower() in recall_text(r.platform, r.cell_id).lower()
            ]
            lines.append(f"original token retrieved after replacement: {len(replaced)}")
            lines += [f"  {c}: original token '{t}' in the new-conversation recall replies" for c, t in replaced]
        lines.append("")
    return lines


def main() -> None:
    cells = pd.read_csv(AUDIT_TABLE)
    wanted = [p.lower() for p in sys.argv[1:]] or sorted(cells.platform.unique())
    originals = original_tokens()
    sys.path.insert(0, "../tester")
    from recall_probes_loader import load_recall_probes  # tester's parser of recall_probes.md
    current = {c: p["answer"] for c, p in load_recall_probes().items()}

    lines = ["Per-platform breakdown (see platforms/how.md, step 1).", ""]
    for platform in wanted:
        lines += [f"===== {platform} =====", *platform_lines(cells[cells.platform == platform], originals, current)]
    print("\n".join(lines))
    name = "platform_breakdown" if not sys.argv[1:] else "platform_breakdown_" + "_".join(wanted)
    print(f"report saved -> {save_report(name, lines)}")


if __name__ == "__main__":
    main()
