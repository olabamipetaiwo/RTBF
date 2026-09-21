"""Parses RTBF-Prompt/recall_probes.md's per-cell probe table(s) -- the real,
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

RECALL_PROBES_MD_PATH = config.PROMPT_REPO / "recall_probes.md"

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
    """cell_id -> {"answer", "r1_open", "r1_choice", "r2", "r3"}."""
    global _cache
    if _cache is not None:
        return _cache

    result: dict[str, dict[str, str]] = {}
    lines = RECALL_PROBES_MD_PATH.read_text().splitlines()

    in_table = False
    for line in lines:
        if line.startswith(_HEADER_PREFIX):
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
        if len(cols) < 8:
            continue
        cell_id, _type, answer, _erasure, r1_open, r1_choice, r2, r3 = cols[:8]
        result[cell_id] = {
            "answer": answer,
            "r1_open": r1_open,
            "r1_choice": r1_choice,
            "r2": r2,
            "r3": r3,
        }

    _cache = result
    return result
