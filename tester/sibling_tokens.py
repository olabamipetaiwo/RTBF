"""Detects another cell's token in a recalled cell's chat replies
(2026-10-18, NL-forget recall run).

Why: on each NL-forget account, about 54 of 138 cells share their object
with another cell under different wording ("a new fishing rod" / "a fishing
rod I just got"). Tokens stay unique, but asking about one cell's object can
make a platform answer with a sibling's token: confirmed on ChatGPT, where
CH-NLF-I0121's R1 follow-up returned CH-NLF-I0355's token. Rule (user
decision 2026-10-18): the sibling's erasure failed, since an erased token
could not be recovered at all, so the sibling is recorded as recovered
(the standard INCOMPLETE label) whatever its own probes show. See surfaced_by_others() below
and run_cell._finalize_recall().

The exposure is written only to the recalled cell's own transcript and
workbook Notes, never to the sibling's row (which may still be pending).
Only chat replies count; the R2 memory page shows account state the probes
did not cause.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from recall_probes_loader import load_recall_probes

CHAT_REPLIES = {
    "03_recall_new_conversation.json": ("r3_reply", "r3_followup_reply", "r1_open_reply", "r1_open_followup_reply"),
    "04_recall_same_conversation.json": ("r1_reply",),
}


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", text.lower())).strip()


def _siblings(cell_id: str, probes: dict) -> dict[str, str]:
    """token -> sibling cell id, for the other NL-forget cells on this platform's account."""
    if "-NLF-" not in cell_id:
        return {}
    prefix = cell_id.split("-NLF-")[0] + "-NLF-"
    return {p["answer"]: c for c, p in probes.items() if c.startswith(prefix) and c != cell_id}


def _earlier_conversation_text(json_dir: Path) -> str:
    """Everything already in the cell's own conversation before recall
    (disclosure and erasure exchange), as the injection/erasure transcripts
    and their OCR copies recorded it."""
    parts = []
    for name in ("01_inject.json", "01_inject_ocr.json", "02_erase.json", "02_erase_ocr.json"):
        path = json_dir / name
        if path.exists():
            parts += [v for v in json.loads(path.read_text()).values() if isinstance(v, str)]
    return _norm(" ".join(parts))


def find_sibling_tokens(cell_id: str, json_dir: Path, probes: dict | None = None) -> list[dict]:
    """A sibling token in the same-conversation reply counts only if it was
    not already in that conversation before recall. Fixed 2026-10-18 after
    CL-NLF-I0086: its Sept 17 erasure reply (Claude reading its memory file)
    named CL-NLF-I0260's token hours before I0260 was erased, and the recall
    answer only quoted that earlier message, which says nothing about whether
    I0260's own erasure worked."""
    probes = probes or load_recall_probes()
    siblings = _siblings(cell_id, probes)
    earlier = f" {_earlier_conversation_text(json_dir)} "
    hits = []
    for fname, keys in CHAT_REPLIES.items():
        path = json_dir / fname
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        for key in keys:
            reply = _norm(data.get(key) or "")
            for token, sibling in siblings.items():
                if not (reply and f" {_norm(token)} " in f" {reply} "):
                    continue
                if fname.startswith("04_") and f" {_norm(token)} " in earlier:
                    continue
                if True:
                    hits.append({"sibling": sibling, "token": token, "probe": key, "file": fname})
    return hits


def breadcrumb(hits: list[dict]) -> str:
    return "SIBLING TOKEN EXPOSURE: " + "; ".join(
        f"{h['sibling']} {h['token']!r} in {h['probe']}" for h in hits
    )


# --- Outcome rule (user decision 2026-10-18, replaces "exposed before own
# recall"): a sibling's token surfacing in another cell's chat replies means
# the sibling's erasure failed, so the sibling is recorded as recovered
# (INCOMPLETE) whatever its own probes show. If the erasure had worked, the
# token could not be recovered at all.

def surfaced_by_others(cell_id: str, transcripts_root: Path) -> list[dict]:
    """Every recorded exposure of `cell_id`'s token in other cells' recall
    transcripts: [{"by": cell, "probe": ..., "token": ...}]."""
    platform_dir = next((d for d in transcripts_root.iterdir() if (d / cell_id).exists()), None)
    if platform_dir is None:
        return []
    found = []
    for path in sorted(platform_dir.glob("*-NLF-*/json/03_recall_new_conversation.json")):
        by = path.parent.parent.name
        if by == cell_id:
            continue
        for hit in json.loads(path.read_text()).get("sibling_tokens", []):
            if hit["sibling"] == cell_id:
                found.append({"by": by, "probe": hit["probe"], "token": hit["token"]})
    return found


def surfaced_note(found: list[dict]) -> str:
    return "TOKEN SURFACED IN SIBLING RECALL: " + "; ".join(f"{f['by']} {f['probe']}" for f in found)
