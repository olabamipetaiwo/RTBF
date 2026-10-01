"""Shared reader for the Qualtrics results export used by the prompt pipeline.

A Qualtrics xlsx export has a short-name header row (row 0), a question-text
row (row 1), and, depending on the export settings, an ImportId row (row 2)
before the first response. Earlier code hard-coded three header rows; the
export actually used here has only two, so the first respondent was read as
a header row and silently dropped (217 of 218 complete respondents; found
2026-09-30). The first data row is therefore located by content: the first
row below the question text whose ResponseId starts with "R_".
"""

import warnings

import pandas as pd

warnings.filterwarnings(
    "ignore", message="Workbook contains no default style", category=UserWarning
)

RESPONSE_ID_COL = "ResponseId"
RESPONSE_ID_PREFIX = "R_"
QUESTION_TEXT_ROW = 1


def load_export(xlsx_path):
    """Return (header, question_text, data) for a Qualtrics xlsx export.

    header: list of column short names; question_text: list of full question
    texts; data: DataFrame of responses only, all columns as strings.
    """
    raw = pd.read_excel(xlsx_path, header=None, dtype=str)
    header = raw.iloc[0].tolist()
    ids = raw.iloc[:, header.index(RESPONSE_ID_COL)].fillna("")
    is_response = ids.str.startswith(RESPONSE_ID_PREFIX)
    candidates = is_response[is_response].index
    start = int(candidates[0])
    if start <= QUESTION_TEXT_ROW:
        raise ValueError(f"{xlsx_path}: first response found above the header rows")
    if not is_response.iloc[start:].all():
        raise ValueError(f"{xlsx_path}: non-response rows below the first response")
    data = raw.iloc[start:].reset_index(drop=True)
    return header, raw.iloc[QUESTION_TEXT_ROW].tolist(), data
