"""Final acknowledgment codes: agreed codes plus adjudicated disagreements.

Sources (read-only): ./Taiwo-Acknowledgment Coding.xlsx, ./Jihwan-Acknowledgment Coding.xlsx
(sheet "Acknowledgment", code in column E) and ./disagreements.csv (column
adjudicated_value, settled by both coders on 2026-10-20).

Writes:
  ./Final-Acknowledgment Coding.xlsx  one row per coded cell, both coders' codes,
                                      the final code and where it came from.
  ../../RTBF-Prompt/data/RTBF Experiments.xlsx
                                      the final code, upper-cased to match the
                                      dropdown, in column "Acknowledgment (coded)"
                                      of the MASTER and NL FORGET sheets.

Rows the coders left empty have no reply to code. In MASTER they are UI-only
erasures, written as "NO REPLY (UI ACTION)"; in NL FORGET the typed request's
reply was never captured, and the cell is left empty. A row with reply text but no
code from either coder is "not yet coded" and left out of the workbook (the
DeepSeek rows appended 2026-10-20 start that way). The codebook's OTHER code is
not in the workbook dropdown, so it is added there.

Usage: python3 build_final_acknowledgment.py
"""

import csv
from pathlib import Path

import openpyxl
from openpyxl.styles import Font

HERE = Path(__file__).parent
TAIWO_FILE = HERE / "Taiwo-Acknowledgment Coding.xlsx"
JIHWAN_FILE = HERE / "Jihwan-Acknowledgment Coding.xlsx"
DISAGREEMENTS = HERE / "disagreements.csv"
FINAL_FILE = HERE / "Final-Acknowledgment Coding.xlsx"
WORKBOOK = HERE.parent.parent / "RTBF-Prompt" / "data" / "RTBF Experiments.xlsx"

SHEET = "Acknowledgment"
CODE_COL = 5  # column E in both coding workbooks
TARGET_COLUMN = "Acknowledgment (coded)"
TARGET_SHEETS = {"MASTER ": "NO REPLY (UI ACTION)", "NL FORGET": None}
NEW_DROPDOWN_VALUE = "OTHER"


def normalize(value: object) -> str:
    return str(value).strip().lower() if value is not None else ""


def load_coder(path: Path) -> dict[str, dict]:
    ws = openpyxl.load_workbook(path, data_only=True)[SHEET]
    rows = {}
    for r in range(2, ws.max_row + 1):
        cell_id = ws.cell(r, 1).value
        if cell_id:
            rows[str(cell_id).strip()] = {
                "platform": normalize(ws.cell(r, 2).value),
                "request": ws.cell(r, 3).value or "",
                "reply": ws.cell(r, 4).value or "",
                "code": normalize(ws.cell(r, CODE_COL).value),
            }
    return rows


def load_adjudicated() -> dict[str, tuple[str, str]]:
    with DISAGREEMENTS.open(newline="") as f:
        rows = {r["cell_id"]: (r["adjudicated_value"].strip(), r["adjudication_notes"]) for r in csv.DictReader(f)}
    unresolved = [cell for cell, (value, _) in rows.items() if not value]
    if unresolved:
        raise SystemExit(f"unadjudicated disagreements: {unresolved}")
    return rows


def final_codes() -> list[dict]:
    taiwo, jihwan = load_coder(TAIWO_FILE), load_coder(JIHWAN_FILE)
    if taiwo.keys() != jihwan.keys():
        raise SystemExit("the two coding workbooks list different cells")
    adjudicated = load_adjudicated()
    out = []
    for cell_id, t in taiwo.items():
        j_code = jihwan[cell_id]["code"]
        if not t["code"] and not j_code and t["reply"]:
            final, source, note = "", "not yet coded", ""
        elif not t["code"] and not j_code:
            final, source, note = "", "no reply to code", ""
        elif t["code"] == j_code:
            final, source, note = t["code"], "agreed", ""
        elif cell_id in adjudicated:
            final, note = adjudicated[cell_id]
            source = "adjudicated"
        else:
            raise SystemExit(f"{cell_id}: coders disagree and no adjudicated value exists")
        out.append({"cell_id": cell_id, **t, "taiwo": t["code"], "jihwan": j_code,
                    "final": final, "source": source, "note": note})
    return out


def write_final_file(rows: list[dict]) -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = SHEET
    headers = ["Cell ID", "Platform", "Erasure request text", "Reply text",
               "Taiwo", "Jihwan", "Final", "Source", "Adjudication note"]
    ws.append(headers)
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in rows:
        ws.append([r["cell_id"], r["platform"], r["request"], r["reply"],
                   r["taiwo"], r["jihwan"], r["final"], r["source"], r["note"]])
    ws.freeze_panes = "A2"
    wb.save(FINAL_FILE)


def write_workbook(rows: list[dict]) -> dict[str, int]:
    final = {r["cell_id"]: r["final"] for r in rows if r["source"] != "not yet coded"}
    wb = openpyxl.load_workbook(WORKBOOK)
    written = {}
    for sheet, empty_value in TARGET_SHEETS.items():
        ws = wb[sheet]
        headers = [c.value for c in ws[1]]
        id_col = headers.index("Cell ID") + 1
        code_col = headers.index(TARGET_COLUMN) + 1
        n = 0
        for r in range(2, ws.max_row + 1):
            cell_id = ws.cell(r, id_col).value
            if cell_id in final:
                ws.cell(r, code_col).value = final[cell_id].upper() or empty_value
                n += 1
        for dv in ws.data_validations.dataValidation:
            if "COMPLIED" in (dv.formula1 or "") and NEW_DROPDOWN_VALUE not in dv.formula1:
                dv.formula1 = dv.formula1.rstrip('"') + f',{NEW_DROPDOWN_VALUE}"'
        written[sheet.strip()] = n
    wb.save(WORKBOOK)
    return written


def main() -> None:
    rows = final_codes()
    write_final_file(rows)
    written = write_workbook(rows)
    sources = {s: sum(r["source"] == s for r in rows)
               for s in ("agreed", "adjudicated", "no reply to code", "not yet coded")}
    print(f"{FINAL_FILE.name}: {len(rows)} cells {sources}")
    print(f"{WORKBOOK.name}: written {written}")


if __name__ == "__main__":
    main()
