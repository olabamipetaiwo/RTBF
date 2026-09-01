"""Shared paths and platform config -- this project reads the experiment
design and injection/erasure/recall text from RTBF-Prompt rather than
duplicating any of it."""

from pathlib import Path

TESTER_ROOT = Path(__file__).parent
RTBF_ROOT = TESTER_ROOT.parent
PROMPT_REPO = RTBF_ROOT / "RTBF-Prompt"

MASTER_XLSX_PATH = PROMPT_REPO / "data" / "RTBF Experiments.xlsx"
SESSIONS_DIR = TESTER_ROOT / "sessions"
TRANSCRIPTS_DIR = TESTER_ROOT / "transcripts"

# Login URLs only -- account creation is handled manually (see
# login_setup.py), not by this project. Verify/update these against the
# live sites; not yet confirmed against real DOM.
PLATFORMS = {
    "claude": "https://claude.ai/login",
    "chatgpt": "https://chatgpt.com/auth/login",
    "gemini": "https://gemini.google.com/",
    "copilot": "https://copilot.microsoft.com/",
    "perplexity": "https://www.perplexity.ai/",
    "deepseek": "https://chat.deepseek.com/sign_in",
}


def session_path(platform: str, label: str | None = None) -> Path:
    """`label` selects a secondary, independently-logged-in account for
    this platform (e.g. "maximal_i2") instead of the main
    sessions/<platform>.json -- added 2026-08-31 because MAXIMAL cells
    are deliberately account-wide/blanket erasures, and multiple MAXIMAL
    cells sharing one account would wipe each other's anchors before
    their own turn (confirmed: every platform has 2-4 MAXIMAL cells on
    what was previously a single shared account). One MAXIMAL cell per
    platform stays on the main account (schedulable last, as usual); the
    rest each need their own dedicated account via this label."""
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform: {platform!r}, expected one of {list(PLATFORMS)}")
    if label:
        return SESSIONS_DIR / f"{platform}__{label}.json"
    return SESSIONS_DIR / f"{platform}.json"


# Main-account email per platform, used by any cell NOT in
# MAXIMAL_ACCOUNT_LABEL below -- see accounts.md for how each was
# confirmed (live, via Settings/Account page or account dropdown, not
# guessed from a display name).
MAIN_ACCOUNT_EMAIL: dict[str, str] = {
    "chatgpt": "olacoderpad@gmail.com",
    "claude": "anchorexperiment@gmail.com",
    "gemini": "anchorexperiment@gmail.com",
    "copilot": "anchorexperiment@gmail.com",
    "perplexity": "anchorexperiment@gmail.com",
    "deepseek": "anchorexperiment@gmail.com",
}

# Dedicated MAXIMAL account email per (platform, label) -- see accounts.md
# for the full per-cell breakdown and how each was confirmed.
MAXIMAL_ACCOUNT_EMAIL: dict[tuple[str, str], str] = {
    ("chatgpt", "maximal_i1"): "olabamipet@gmail.com",
    ("chatgpt", "maximal_i2"): "experimentanchor@gmail.com",
    ("chatgpt", "maximal_i3"): "anchorexperiment+001@gmail.com",
    ("chatgpt", "maximal_file"): "participantone@rtbfexperiment.com.ng",
    ("claude", "maximal_i1"): "olabamipet@gmail.com",
    ("claude", "maximal_i2"): "experimentanchor@gmail.com",
    ("claude", "maximal_i3"): "olacoderpad@gmail.com",
    ("claude", "maximal_file"): "participantone@rtbfexperiment.com.ng",
    ("gemini", "maximal_i1"): "olabamipet@gmail.com",
    ("gemini", "maximal_i2"): "olacoderpad@gmail.com",
    ("gemini", "maximal_file"): "teeola48@gmail.com",
    ("copilot", "maximal_i1"): "olabamipet@gmail.com",
    ("copilot", "maximal_i2"): "experimentanchor@gmail.com",
    ("copilot", "maximal_file"): "teeola48@gmail.com",
    ("deepseek", "maximal_i1"): "olabamipet@gmail.com",
    ("deepseek", "maximal_file"): "experimentanchor@gmail.com",
}


def account_email(cell_id: str, platform: str) -> str:
    """Single source of truth for "which email ran this cell" -- used both
    to backfill the xlsx's Email column and to write it going forward on
    every injection. Mirrors accounts.md; keep both in sync if an account
    ever needs to change."""
    label = MAXIMAL_ACCOUNT_LABEL.get(cell_id)
    if label:
        return MAXIMAL_ACCOUNT_EMAIL.get((platform, label), "")
    return MAIN_ACCOUNT_EMAIL.get(platform, "")


# Cell -> dedicated-account label, for every MAXIMAL cell. Every MAXIMAL
# cell gets its own account -- none of them, including the platform's
# "first" one, share an account with any other cell (narrow or MAXIMAL)
# -- see session_path()'s docstring. Simplified 2026-08-31 from an
# earlier "one stays on main" design: keeping the main account entirely
# free of MAXIMAL erasures removes it from the destructive-actions-run-
# last scheduling question altogether, not just for sibling MAXIMAL cells.
MAXIMAL_ACCOUNT_LABEL: dict[str, str] = {
    "CL-I1-E5": "maximal_i1",
    "CL-I2-E5": "maximal_i2",
    "CL-I3-E5": "maximal_i3",
    "CL-IF-E-MAX": "maximal_file",
    "CH-I1-E7": "maximal_i1",
    "CH-I2-E7": "maximal_i2",
    "CH-I3-E7": "maximal_i3",
    "CH-IF-E-MAX": "maximal_file",
    "GE-I1-E6": "maximal_i1",
    "GE-I2-E6": "maximal_i2",
    "GE-IF-E-MAX": "maximal_file",
    "CO-I1-E6": "maximal_i1",
    "CO-I2-E6": "maximal_i2",
    "CO-IF-E-MAX": "maximal_file",
    "PE-I1-E6": "maximal_i1",
    "PE-I2-E6": "maximal_i2",
    "PE-IF-E-MAX": "maximal_file",
    "DE-I1-E4": "maximal_i1",
    "DE-IF-E-MAX": "maximal_file",
}
