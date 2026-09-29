"""Parses RTBF-Prompt/notes/recall_probes.md's per-cell probe table(s) -- the real,
already-generated R1/R2/R3 probe text for all 88 main-battery cells plus
(added 2026-09-11) the 828 NL-forget-prompt-study cells, each in their own
table under their own heading -- rather than regenerating it here.
Regenerating would mean reconstructing token_generator.py's exact
`assigned`/`distractors_by_token` ordering (or nl_forget_cell_generator.py's
equivalent); parsing the file it already writes is simpler and can't drift
from the canonical source. Reads every table in the file, not just the
first -- see the in_table reset below.

The file is a clean pipe-delimited markdown table (confirmed live
2026-08-28: no embedded `|` characters in cell content), so a plain
line-based split is sufficient -- no markdown-table library needed.
"""

from __future__ import annotations

import config

RECALL_PROBES_MD_PATH = config.PROMPT_REPO / "notes" / "recall_probes.md"

_HEADER_PREFIX = "| Cell ID "
_SEPARATOR_PREFIX = "|---"

_cache: dict[str, dict[str, str]] | None = None


def _parse_row(line: str) -> list[str]:
    # Drop the leading/trailing "|" then split on "|", stripping each cell.
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [cell.strip() for cell in inner.split("|")]


def load_recall_probes() -> dict[str, dict[str, str]]:
    """cell_id -> {"answer", "r1_open", "r1_open_followup", "r2", "r3",
    "r3_followup"}. r1_open_followup/r3_followup are the fixed, always-run
    second attempts added 2026-09-23 (see review.md item 3a) to remove the
    outcome-dependent-repetition asymmetry the paper review flagged -- every
    cell gets both, not just cells whose first attempt was surprising.

    Raises if a table header still has the forced-choice column dropped
    2026-09-23: the columns are read by position, so a stale table would
    silently shift every probe into the wrong field."""
    global _cache
    if _cache is not None:
        return _cache

    result: dict[str, dict[str, str]] = {}
    lines = RECALL_PROBES_MD_PATH.read_text().splitlines()

    in_table = False
    for line in lines:
        if line.startswith(_HEADER_PREFIX):
            if "choice" in line.lower():
                raise ValueError(
                    f"{RECALL_PROBES_MD_PATH} still has an R1 forced-choice column "
                    "(dropped 2026-09-23); regenerate or strip it before running recall."
                )
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith(_SEPARATOR_PREFIX):
            continue
        if not line.startswith("|"):
            # table ended -- don't stop scanning the whole file: a later
            # section (e.g. the NL-forget-prompt study's own table, added
            # 2026-09-11) can start a fresh table with its own
            # _HEADER_PREFIX line further down.
            in_table = False
            continue
        cols = _parse_row(line)
        if len(cols) < 9:
            continue
        (cell_id, _type, answer, _erasure, r1_open, r1_open_followup,
         r2, r3, r3_followup) = cols[:9]
        result[cell_id] = {
            "answer": answer,
            "r1_open": r1_open,
            "r1_open_followup": r1_open_followup,
            "r2": r2,
            "r3": r3,
            "r3_followup": r3_followup,
        }

    _cache = result
    return result
