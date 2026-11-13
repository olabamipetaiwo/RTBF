"""The test-case workbook: stages read test cases from it and write results back."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

from didr import config
from didr.shared_files import atomic_save_workbook, write_lock

SHEET = "TEST CASES"

LAYOUT: list[tuple[str, str]] = [
    ("Test case", "Test case ID"),
    ("Test case", "Agent"),
    ("Test case", "Injection method"),
    ("Test case", "Deletion method"),
    ("Test case", "Account"),
    ("Test case", "Status"),
    ("1 Fact generation", "Entity"),
    ("1 Fact generation", "Value"),
    ("1 Fact generation", "Disclosure sentence"),
    ("1 Fact generation", "Direct recall prompt"),
    ("1 Fact generation", "Direct recall follow-up"),
    ("1 Fact generation", "Indirect recall prompt"),
    ("1 Fact generation", "Indirect recall follow-up"),
    ("2 Injection", "Injected at"),
    ("2 Injection", "Conversation reference"),
    ("2 Injection", "Storage evidence"),
    ("3 Deletion", "Deletion request text"),
    ("3 Deletion", "Deleted at"),
    ("3 Deletion", "Agent response"),
    ("3 Deletion", "Response code"),
    ("4 Recall", "Recalled at"),
    ("4 Recall", "Direct recall result"),
    ("4 Recall", "Indirect recall result"),
    ("4 Recall", "UI-based check result"),
    ("4 Recall", "Same-conversation result"),
    ("5 Classification", "Recall outcome"),
]
COLUMNS: dict[str, int] = {header: i + 1 for i, (_, header) in enumerate(LAYOUT)}

USER_COLUMNS = ("Test case ID", "Agent", "Injection method", "Deletion method", "Account")

_STAGE_FILL = {
    "Test case": "D9D9D9",
    "1 Fact generation": "DDEBF7",
    "2 Injection": "E2EFDA",
    "3 Deletion": "FCE4D6",
    "4 Recall": "FFF2CC",
    "5 Classification": "EDEDED",
}


@dataclass
class TestCase:
    row: int
    values: dict[str, object] = field(default_factory=dict)

    def __getitem__(self, header: str):
        value = self.values.get(header)
        return value.strip() if isinstance(value, str) else value

    @property
    def id(self) -> str:
        return self["Test case ID"]

    @property
    def agent(self) -> str:
        return (self["Agent"] or "").lower()

    @property
    def account(self) -> str | None:
        return self["Account"] or None


def create(path: Path | None = None, overwrite: bool = False) -> Path:
    path = path or config.WORKBOOK_PATH
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} already exists; pass overwrite=True to replace it")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = SHEET
    for stage, header in LAYOUT:
        cell = ws.cell(row=1, column=COLUMNS[header], value=header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor=_STAGE_FILL[stage])
        ws.column_dimensions[get_column_letter(COLUMNS[header])].width = max(14, len(header) + 2)
    ws.freeze_panes = "B2"
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    return path


def _open(path: Path, read_only: bool = False):
    if not path.exists():
        raise FileNotFoundError(f"{path} not found; create it with `python pipeline.py init`")
    wb = openpyxl.load_workbook(path, read_only=read_only, data_only=True)
    if SHEET not in wb.sheetnames:
        raise ValueError(f"{path} has no {SHEET!r} sheet")
    ws = wb[SHEET]
    headers = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
    expected = [h for _, h in LAYOUT]
    if headers[: len(expected)] != expected:
        raise ValueError(f"{path}: header row does not match the DIDR layout; recreate it with `python pipeline.py init`")
    return wb, ws


def test_cases(path: Path | None = None) -> Iterator[TestCase]:
    path = path or config.WORKBOOK_PATH
    _, ws = _open(path, read_only=True)
    for r, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if not row or not row[0]:
            continue
        yield TestCase(row=r, values={h: row[i - 1] if i - 1 < len(row) else None for h, i in COLUMNS.items()})


def get(test_case_id: str, path: Path | None = None) -> TestCase:
    for tc in test_cases(path):
        if tc.id == test_case_id:
            return tc
    raise KeyError(f"test case {test_case_id!r} not found in the workbook")


def update(updates: dict[str, dict[str, object]], path: Path | None = None) -> None:
    """`updates` maps test case ID -> {header: value}; written in one save."""
    path = path or config.WORKBOOK_PATH
    with write_lock():
        wb, ws = _open(path)
        found = set()
        for r in range(2, ws.max_row + 1):
            tc_id = ws.cell(row=r, column=1).value
            if tc_id in updates:
                for header, value in updates[tc_id].items():
                    ws.cell(row=r, column=COLUMNS[header], value=value)
                found.add(tc_id)
        missing = set(updates) - found
        if missing:
            raise KeyError(f"test cases not found in the workbook: {sorted(missing)}")
        atomic_save_workbook(wb, path)


def update_one(test_case_id: str, fields: dict[str, object], path: Path | None = None) -> None:
    update({test_case_id: fields}, path)
