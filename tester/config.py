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


def session_path(platform: str) -> Path:
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform: {platform!r}, expected one of {list(PLATFORMS)}")
    return SESSIONS_DIR / f"{platform}.json"
