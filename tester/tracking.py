"""Local scheduling state for the inject/erase/recall split -- tracks when
each cell was injected/erased and when its next phase is due. This is
tester's own run-tracking metadata (see tester/CLAUDE.md's `data/`
description), separate from the shared RTBF Experiments.xlsx: MASTER gets
the human-relevant results (Run status, R1-R3 outcomes, a Notes
breadcrumb), this file gets the scheduling mechanics (exact timestamps,
due-date math) that only tester itself needs to compute.

Study design (confirmed with the user 2026-08-28): erasure runs 48 hours
after injection; recall runs 31 days after erasure (not after injection).
Same-session and cross-session recall both happen at that single 31-day
mark -- see run_cell.py's recall_cell() -- they are not staggered across
two different calendar times.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import config

TRACKING_PATH = config.TESTER_ROOT / "data" / "run_tracking.json"

ERASURE_DELAY = timedelta(hours=48)
RECALL_DELAY = timedelta(days=31)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


def _parse(s: str | None) -> datetime | None:
    return datetime.fromisoformat(s) if s else None


def load() -> dict[str, dict]:
    if not TRACKING_PATH.exists():
        return {}
    return json.loads(TRACKING_PATH.read_text())


def save(data: dict[str, dict]) -> None:
    TRACKING_PATH.parent.mkdir(parents=True, exist_ok=True)
    TRACKING_PATH.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def get(cell_id: str) -> dict | None:
    return load().get(cell_id)


def mark_injected(cell_id: str, ts: datetime | None = None, ref: str | None = None) -> dict:
    """`ref` is the cell's own durable target identifier -- the exact
    conversation URL for a chat-based injection, or None for a settings-
    field injection (those are targeted by token/text match at erasure
    time instead, see each flow's erasure methods). Without this, erasure
    has no way to distinguish this cell's own conversation/entry from a
    sibling cell's sharing the same account -- confirmed live 2026-08-31
    that grabbing "whatever's topmost in the sidebar" silently deletes
    the wrong cell's data when multiple cells share an account."""
    ts = ts or _now()
    data = load()
    data[cell_id] = {
        "status": "injected",
        "injected_at": _iso(ts),
        "erasure_due_at": _iso(ts + ERASURE_DELAY),
        "erased_at": None,
        "recall_due_at": None,
        "recalled_at": None,
        "injection_ref": ref,
    }
    save(data)
    return data[cell_id]


def mark_erased(cell_id: str, ts: datetime | None = None) -> dict:
    ts = ts or _now()
    data = load()
    entry = data.setdefault(cell_id, {})
    entry["status"] = "erased"
    entry["erased_at"] = _iso(ts)
    entry["recall_due_at"] = _iso(ts + RECALL_DELAY)
    save(data)
    return entry


def mark_recalled(cell_id: str, ts: datetime | None = None) -> dict:
    ts = ts or _now()
    data = load()
    entry = data.setdefault(cell_id, {})
    entry["status"] = "recalled"
    entry["recalled_at"] = _iso(ts)
    save(data)
    return entry


def due_for_erasure(now: datetime | None = None) -> list[str]:
    now = now or _now()
    data = load()
    return [
        cid for cid, e in data.items()
        if e.get("status") == "injected" and _parse(e.get("erasure_due_at")) and now >= _parse(e["erasure_due_at"])
    ]


def due_for_recall(now: datetime | None = None) -> list[str]:
    now = now or _now()
    data = load()
    return [
        cid for cid, e in data.items()
        if e.get("status") == "erased" and _parse(e.get("recall_due_at")) and now >= _parse(e["recall_due_at"])
    ]
