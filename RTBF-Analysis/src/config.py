"""Named constants for the RTBF survey analysis. No logic lives here."""

# --- Paths -------------------------------------------------------------

RAW_DATA_PATH = "data/raw/RTBF_survey_results.xlsx"
PROCESSED_DATA_DIR = "data/processed"
SCREENED_DATA_PATH = "data/processed/screened.csv"

# --- Header structure of the raw Qualtrics export -----------------------
# This export has only 2 metadata header rows (no Qualtrics ImportId-JSON
# row, which some exports include as a 3rd header row): row 0 is the
# question ID (e.g. "Q4.7_1"), row 1 is the full question text. Data
# starts at row 2 (0-indexed).

QID_ROW_IDX = 0
QTEXT_ROW_IDX = 1
DATA_START_ROW_IDX = 2

# --- Scenario mapping ----------------------------------------------------
# NOT present anywhere in the raw export -- Qualtrics does not encode which
# question block corresponds to which scenario. This is a within-subject
# design where the same question battery (Q4.x / Q5.x) is repeated for two
# scenarios; the mapping below is hard-coded from the survey design.

SCENARIO_MAP = {
    "Q4": "less_sensitive",
    "Q5": "more_sensitive",
}

# --- Column groups (repeated per scenario) --------------------------------

PROTECTION_COLS = {
    "less_sensitive": ["Q4.7_1", "Q4.7_2", "Q4.7_3", "Q4.7_4", "Q4.7_5"],
    "more_sensitive": ["Q5.7_1", "Q5.7_2", "Q5.7_3", "Q5.7_4", "Q5.7_5"],
}

EFFORT_COLS = {
    "less_sensitive": ["Q4.8_1", "Q4.8_2", "Q4.8_3", "Q4.8_4"],
    "more_sensitive": ["Q5.8_1", "Q5.8_2", "Q5.8_3", "Q5.8_4"],
}

BENEFIT_LOSS_COLS = {
    "less_sensitive": ["Q4.9_1", "Q4.9_2", "Q4.9_3"],
    "more_sensitive": ["Q5.9_1", "Q5.9_2", "Q5.9_3"],
}

# --- Attention check -------------------------------------------------------

ATTENTION_CHECK_COL = "Q6.5"
ATTENTION_CHECK_EXPECTED = "Sometimes"
