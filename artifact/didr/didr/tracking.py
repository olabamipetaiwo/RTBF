"""Stage timestamps and due times: deletion >= 48 h after injection, recall >= 30 days after deletion."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from didr import config
from didr.shared_files import atomic_write_text, write_lock

STATE_PATH = config.STATE_DIR / "run_state.json"
DELETION_DELAY = timedelta(hours=48)
RECALL_DELAY = timedelta(days=30)


def now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def load() -> dict[str, dict]:
    return json.loads(STATE_PATH.read_text()) if STATE_PATH.exists() else {}


def get(test_case_id: str) -> dict | None:
    return load().get(test_case_id)


def _update(test_case_id: str, **fields) -> dict:
    with write_lock():
        data = load()
        entry = data.setdefault(test_case_id, {})
        entry.update(fields)
        atomic_write_text(STATE_PATH, json.dumps(data, indent=2, sort_keys=True) + "\n")
    return entry


def mark_injected(test_case_id: str, ref: str | None) -> dict:
    t = now()
    return _update(test_case_id, status="injected", injected_at=_iso(t),
                   deletion_due_at=_iso(t + DELETION_DELAY), injection_ref=ref)


def mark_deleted(test_case_id: str) -> dict:
    t = now()
    return _update(test_case_id, status="deleted", deleted_at=_iso(t), recall_due_at=_iso(t + RECALL_DELAY))


def mark_recalled(test_case_id: str) -> dict:
    return _update(test_case_id, status="recalled", recalled_at=_iso(now()))


def require(test_case_id: str, status: str, due_field: str, force: bool) -> dict:
    entry = get(test_case_id)
    current = entry.get("status") if entry else "not injected"
    if current != status:
        raise RuntimeError(f"{test_case_id}: expected status {status!r}, found {current!r}")
    if now() < datetime.fromisoformat(entry[due_field]) and not force:
        raise RuntimeError(f"{test_case_id}: not due until {entry[due_field]}; use --force to override")
    return entry


def due(status: str, due_field: str) -> list[str]:
    t = now()
    return sorted(
        tc for tc, e in load().items()
        if e.get("status") == status and t >= datetime.fromisoformat(e[due_field])
    )
