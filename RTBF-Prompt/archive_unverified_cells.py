"""Moves cells off MASTER (or FILE SUBSTUDY) into an "ARCHIVED CELLS" sheet
instead of deleting them outright -- for cells whose designed method turns
out not to exist on the live platform (confirmed via ../tester's live
selector investigation, not guessed). Keeps the exact row so it can be
pasted straight back into MASTER if a platform later reintroduces the
surface, or if the finding turns out to be wrong.

Archive sheet layout: one section per platform (platform name as a bold
header row, then MASTER's own column headers, then the archived rows),
with 5 blank rows between platform sections so more can be appended later
as other platforms get live-tested. Idempotent-ish: re-running with the
same cell_ids appends another dated entry rather than deduplicating --
intentional, since a re-verification finding is worth keeping too.

Usage (edit CELLS_TO_ARCHIVE below, then run):
    python archive_unverified_cells.py
"""

from __future__ import annotations

import datetime

import openpyxl
from openpyxl.styles import Font

XLSX_PATH = "data/RTBF Experiments.xlsx"
ARCHIVE_SHEET = "ARCHIVED CELLS"
BLANK_ROWS_BETWEEN_PLATFORMS = 5

# platform -> [(cell_id, reason), ...]. Reasons should cite what was
# actually confirmed live, not just "doesn't work".
CELLS_TO_ARCHIVE: dict[str, list[tuple[str, str]]] = {
    "ChatGPT": [
        ("CH-I1-E3", "Confirmed live 2026-08-27: ChatGPT's memory UI no longer "
                      "has per-item memory deletion. \"Manage\" opens a single "
                      "AI-generated \"Memory summary\" card (Overview + "
                      "\"Ask or update\" free-text box), not a list of "
                      "individually deletable entries. Only whole-memory clear "
                      "exists now (\"Delete and turn off memory\", see E4). "
                      "Product redesign, not a selector/automation gap -- see "
                      "tester/flows/chatgpt.py's module docstring."),
        ("CH-I2-E3", "Same finding as CH-I1-E3 -- see that row's reason."),
        ("CH-I3-E3", "Same finding as CH-I1-E3 -- see that row's reason."),
    ],
}


def _find_row(ws, cell_id: str) -> int:
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        if row[0].value == cell_id:
            return row[0].row
    raise ValueError(f"{cell_id!r} not found in {ws.title!r}")


def archive_cells() -> None:
    wb = openpyxl.load_workbook(XLSX_PATH)
    master = wb["MASTER "]
    headers = [c.value for c in master[1]]

    if ARCHIVE_SHEET in wb.sheetnames:
        archive = wb[ARCHIVE_SHEET]
    else:
        archive = wb.create_sheet(ARCHIVE_SHEET)

    today = datetime.date.today().isoformat()

    for platform, entries in CELLS_TO_ARCHIVE.items():
        # Find/append this platform's section: search for an existing
        # "platform" header cell in column A; if absent, start a new
        # section after the current last used row (+ blank-row gap).
        section_row = None
        for row in archive.iter_rows(min_col=1, max_col=1):
            if row[0].value == platform:
                section_row = row[0].row
                break

        if section_row is None:
            start = archive.max_row + (BLANK_ROWS_BETWEEN_PLATFORMS if archive.max_row > 1 else 0) + 1
            if archive.max_row <= 1 and archive.max_row == 1 and archive.cell(1, 1).value is None:
                start = 1  # sheet is genuinely empty
            archive.cell(start, 1, platform).font = Font(bold=True, size=13)
            header_row = start + 1
            for col_idx, h in enumerate(headers + ["Reason archived", "Date archived"], start=1):
                archive.cell(header_row, col_idx, h).font = Font(bold=True)
            data_start = header_row + 1
        else:
            # Existing section: find its header row (next row) and the
            # first fully-blank row after its existing data to append to.
            header_row = section_row + 1
            data_start = header_row + 1
            while archive.cell(data_start, 1).value is not None:
                data_start += 1

        row_to_archive = data_start
        master_rows_to_delete = []
        for cell_id, reason in entries:
            src_row_idx = _find_row(master, cell_id)
            master_rows_to_delete.append(src_row_idx)
            values = [master.cell(src_row_idx, c + 1).value for c in range(len(headers))]
            for col_idx, val in enumerate(values, start=1):
                archive.cell(row_to_archive, col_idx, val)
            archive.cell(row_to_archive, len(headers) + 1, reason)
            archive.cell(row_to_archive, len(headers) + 2, today)
            row_to_archive += 1

        # Delete from MASTER in reverse row order so earlier indices don't shift.
        for r in sorted(master_rows_to_delete, reverse=True):
            master.delete_rows(r, 1)

        print(f"{platform}: archived {len(entries)} cell(s) -> {ARCHIVE_SHEET!r}, removed from MASTER")

    wb.save(XLSX_PATH)
    print(f"Saved -> {XLSX_PATH}")


if __name__ == "__main__":
    archive_cells()
