"""Count Gemini replies to participants' own deletion requests that were an app-permission card.

Gemini sometimes answers a deletion request with "First, I'll need your permission to turn on
the <app> app" and a No thanks / Continue pair, instead of a reply. Nothing is deleted in those
cases, and the audit declined every card. This counts them in the saved deletion replies
(`02_erase.json`) of the NL-forget cells (`GE-NLF-*`), by app, so the paper's number comes from
a script.

Run from the RTBF-Analysis folder: `.venv/bin/python -m src.gemini_permission_cards`.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from src.reporting import save_report

TRANSCRIPTS = Path("../tester/transcripts/gemini")
CARD = re.compile(r"need your permission to turn on the (?P<app>[\w ]+?) app", re.IGNORECASE)


def card_app(reply: str) -> str | None:
    """The app a permission card asks for, or None if the reply is not a card."""
    match = CARD.search(reply)
    return match["app"] if match else None


def main() -> None:
    replies = {
        path.parts[-3]: json.loads(path.read_text())["reply_text"]
        for path in sorted(TRANSCRIPTS.glob("GE-NLF-*/json/02_erase.json"))
    }
    cards = {cell: app for cell, reply in replies.items() if (app := card_app(reply))}
    by_app = Counter(cards.values())

    lines = [
        "Gemini replies to participants' own deletion requests that were an app-permission card",
        "(nothing deleted; every card was declined with No thanks).",
        "",
        f"deletion requests with a saved reply: {len(replies)}",
        f"permission cards: {len(cards)} ({len(cards) / len(replies):.1%} of {len(replies)})",
        *(f"  {app}: {n}" for app, n in by_app.most_common()),
        "",
        "cells: " + ", ".join(sorted(cards)),
    ]
    print("\n".join(lines))
    print(f"report saved -> {save_report('gemini_permission_cards', lines)}")


if __name__ == "__main__":
    main()
