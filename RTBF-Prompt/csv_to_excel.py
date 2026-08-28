#!/usr/bin/env python3
"""Step 6a helper - convert the blind coder sheets to a single Excel workbook."""

import argparse

import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--coder1", default="results/codebook/step6_coding_sheet_coder1.csv")
    ap.add_argument("--coder2", default="results/codebook/step6_coding_sheet_coder2.csv")
    ap.add_argument("--codebook", default="results/codebook/step6_codebook.md")
    ap.add_argument("--out", default="results/codebook/step6_coding_sheets.xlsx")
    a = ap.parse_args()

    with pd.ExcelWriter(a.out, engine="openpyxl") as writer:
        codebook_lines = open(a.codebook).read().splitlines()
        pd.DataFrame({"instructions": codebook_lines}).to_excel(
            writer, sheet_name="instructions", index=False
        )
        pd.read_csv(a.coder1, dtype=str).fillna("").to_excel(
            writer, sheet_name="coder1", index=False
        )
        pd.read_csv(a.coder2, dtype=str).fillna("").to_excel(
            writer, sheet_name="coder2", index=False
        )

        writer.sheets["instructions"].column_dimensions["A"].width = 100

    print(f"wrote {a.out} (sheets: instructions, coder1, coder2)")


if __name__ == "__main__":
    main()
