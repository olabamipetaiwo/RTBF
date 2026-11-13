"""Paths and agent URLs. Optional overrides come from `.env` (see `.env.example`)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

WORKBOOK_PATH = Path(os.getenv("DIDR_WORKBOOK", ROOT / "data" / "DIDR Test Cases.xlsx"))
SESSIONS_DIR = Path(os.getenv("DIDR_SESSIONS_DIR", ROOT / "sessions"))
RESULTS_DIR = Path(os.getenv("DIDR_RESULTS_DIR", ROOT / "results"))
STATE_DIR = ROOT / "data" / "state"
HEADLESS = os.getenv("DIDR_HEADLESS", "0") == "1"

PLATFORMS = {
    "chatgpt": "https://chatgpt.com/auth/login",
    "claude": "https://claude.ai/login",
    "gemini": "https://gemini.google.com/",
    "copilot": "https://copilot.com/",
    "perplexity": "https://www.perplexity.ai/",
    "deepseek": "https://chat.deepseek.com/sign_in",
}


def session_path(platform: str, label: str | None = None) -> Path:
    if platform not in PLATFORMS:
        raise ValueError(f"unknown agent {platform!r}; expected one of {list(PLATFORMS)}")
    return SESSIONS_DIR / (f"{platform}__{label}.json" if label else f"{platform}.json")
