"""
RTBF survey analysis pipeline (in-memory).

Single source of truth = the raw Qualtrics export. Every step is a function;
nothing is written to disk. Import and call `get_bases()` from later steps.

Qualtrics layout (verified against this workbook's raw XML): row0=question
IDs, row1=text, row2+=respondent data. This export has only 2 header rows,
not the standard Qualtrics 3-row format -- there is no importID JSON row,
so row 2 is already the first real respondent.

Scenario mapping is NOT in the export; fixed from survey design:
    Q4 block = LESS sensitive, Q5 block = MORE sensitive.
"""

import warnings

import pandas as pd

from src.reporting import save_report

RAW_FILE = "data/raw/RTBF_survey_results.xlsx"   # adjust path
SHEET = "Sheet0"

CHECKS = {"Q6.5": "Sometimes", "Q9.3": "Agree"}   # attention checks
NEVER_DELETED_COL = "Q3.2_13"    # "I have never deleted my data in AI Chatbots"
EVAL_LESS = "Q4.2"               # less-sensitive method selection
EVAL_MORE = "Q5.2"              # more-sensitive method selection

# Shared Likert mapping for the .7/.8/.9 scale items (protection/effort/
# benefit_loss), used by both src/reliability.py and src/methods.py. Kept
# here as the single source of truth so a raw-data typo variant only needs
# to be handled in one place.
LIKERT = {
    "Strongly Disagree": 1, "Stongly Disagree": 1,   # raw-data typo variant
    "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5,
}

# This workbook's styles.xml has no default cell style, which makes openpyxl
# emit a harmless UserWarning on every load. Silence just that message.
warnings.filterwarnings(
    "ignore",
    message="Workbook contains no default style, apply openpyxl's default",
    category=UserWarning,
)


def load_raw(path=RAW_FILE):
    """Respondent data with question-ID column names."""
    df = pd.read_excel(path, sheet_name=SHEET, header=None)
    data = df.iloc[2:].copy()
    data.columns = df.iloc[0].tolist()
    return data.reset_index(drop=True)


def load_labels(path=RAW_FILE):
    """question ID -> full question text, for labelling outputs."""
    df = pd.read_excel(path, sheet_name=SHEET, header=None)
    return dict(zip(df.iloc[0].tolist(), df.iloc[1].tolist()))


def screen_attention(data):
    """Drop only respondents who ANSWERED a check with the wrong value.
    Missing (incomplete) is not a failure. Returns (kept_df, n_dropped)."""
    wrong_any = pd.Series(False, index=data.index)
    for col, expected in CHECKS.items():
        wrong_any |= data[col].notna() & (data[col] != expected)
    return data[~wrong_any].reset_index(drop=True), int(wrong_any.sum())


def get_bases(path=RAW_FILE, verbose=True):
    """Full pipeline. Returns dict of base DataFrames:
        'less'   : answered Q4.2 (less-sensitive scenario)
        'more'   : answered Q5.2 (more-sensitive scenario)
        'paired' : answered both (for within-subject scenario tests)
    """
    data = load_raw(path)
    screened, n_drop = screen_attention(data)

    never = screened[NEVER_DELETED_COL].notna()
    eligible = screened[~never].copy()

    ans_less = eligible[EVAL_LESS].notna()
    ans_more = eligible[EVAL_MORE].notna()

    bases = {
        "less":   eligible[ans_less].reset_index(drop=True),
        "more":   eligible[ans_more].reset_index(drop=True),
        "paired": eligible[ans_less & ans_more].reset_index(drop=True),
    }

    lines = [
        "=== Analysis Base ===",
        f"  raw rows              : {len(data)}",
        f"  dropped (attention)   : {n_drop}",
        f"  picked never-deleted  : {int(never.sum())}",
        f"  eligible              : {len(eligible)}",
        f"  base less (Q4.2)      : {len(bases['less'])}",
        f"  base more (Q5.2)      : {len(bases['more'])}",
        f"  base paired (both)    : {len(bases['paired'])}",
    ]

    if verbose:
        for line in lines:
            print(line)

    report_path = save_report("screen", lines)
    if verbose:
        print(f"report saved -> {report_path}")

    return bases


if __name__ == "__main__":
    get_bases()