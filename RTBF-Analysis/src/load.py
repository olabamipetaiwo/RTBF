"""Load the raw Qualtrics export into a clean, analysis-ready DataFrame."""

import warnings

import pandas as pd

from src import config

# This workbook's styles.xml has no default cell style, which makes openpyxl
# emit a harmless UserWarning on every load. Silence just that message.
warnings.filterwarnings(
    "ignore",
    message="Workbook contains no default style, apply openpyxl's default",
    category=UserWarning,
)


def load_survey_data(path: str = config.RAW_DATA_PATH) -> pd.DataFrame:
    """Read the raw xlsx export and return a DataFrame with question-ID column names."""
    raw = pd.read_excel(path, header=None)
    id_row = raw.iloc[config.QID_ROW_IDX]
    data = raw.iloc[config.DATA_START_ROW_IDX:].reset_index(drop=True)
    data.columns = id_row
    return data


def load_question_text_map(path: str = config.RAW_DATA_PATH) -> dict[str, str]:
    """Return a mapping of question ID -> full question text, for labeling outputs."""
    raw = pd.read_excel(path, header=None)
    id_row = raw.iloc[config.QID_ROW_IDX]
    text_row = raw.iloc[config.QTEXT_ROW_IDX]
    return dict(zip(id_row, text_row))
