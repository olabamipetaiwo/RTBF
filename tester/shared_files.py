"""Cross-process lock + atomic writes for the two files every run_cell.py
process shares: data/run_tracking.json and the RTBF Experiments.xlsx.

Why (2026-10-18): both are written as whole-file load -> modify -> save.
That was safe while only one run_cell.py process ran at a time (the
injection scheduler ran platforms strictly in sequence for exactly this
reason). The NL-forget recall scheduler runs one process per platform in
parallel, so two platforms finishing a cell within the same few seconds
would each load the old file and the second save would silently drop the
first cell's result. Every load -> save cycle now runs under one exclusive
flock on data/.shared_files.lock, and saves go to a temp file that is
then renamed over the original, so a crash mid-save can't leave a
truncated workbook or JSON behind.

The lock is not re-entrant: never call one locked function from inside
another's `with write_lock():` block.
"""

from __future__ import annotations

import fcntl
import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import config

LOCK_PATH = config.TESTER_ROOT / "data" / ".shared_files.lock"


@contextmanager
def write_lock() -> Iterator[None]:
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOCK_PATH.open("w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def _tmp_path(path: Path) -> Path:
    # Same directory (so the rename is atomic) and same suffix (openpyxl
    # checks the extension when saving).
    return path.with_name(f".{path.stem}.tmp-{os.getpid()}{path.suffix}")


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = _tmp_path(path)
    tmp.write_text(text)
    os.replace(tmp, path)


def atomic_save_workbook(wb, path: Path) -> None:
    tmp = _tmp_path(path)
    wb.save(tmp)
    os.replace(tmp, path)
