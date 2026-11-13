"""Cross-process file lock and atomic writes for the workbook and run state."""

from __future__ import annotations

import fcntl
import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from didr import config

LOCK_PATH = config.STATE_DIR / ".shared_files.lock"


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
