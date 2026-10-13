"""One-off: re-run the NL-forget erase step on the 2 Gemini cells whose
original 2026-09-13 erase landed on an expired session (sent nothing but the
scheduler marked them erased). Detected by auditing reloaded threads for the
erase request text -- GE-NLF-I0044 and GE-NLF-I0240 show only the injection
turn, no erase bubble.

For each cell this script navigates to the injection_ref, verifies the token
is visible and the erase request is NOT already there (safeguard against
re-sending if the audit was wrong), types the erase request through
`GeminiFlow.send_message`, and writes the resulting reply back to
`transcripts/gemini/<cell>/json/02_erase.json` along with a fresh screenshot.

    python reerase_gemini_cells.py
    python reerase_gemini_cells.py --cell GE-NLF-I0044   # just one
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

import config
import tracking
from flows.gemini import GeminiFlow
from run_cell import load_cell

RE_ERASE_SOURCE = (
    "live re-erase on 2026-10-02 (reerase_gemini_cells.py): original erase step on "
    "2026-09-13 landed on an expired Gemini nlforget session and sent nothing"
)
TARGET_CELLS = ["GE-NLF-I0044", "GE-NLF-I0240"]


def reerase_cell(flow, cell_id: str) -> dict:
    plan = load_cell(cell_id)
    entry = tracking.get(cell_id)
    if entry is None or not entry.get("injection_ref"):
        return {"ok": False, "reason": "no injection_ref in tracking.json"}
    ref = entry["injection_ref"]

    page = flow.page
    flow._goto_fresh(ref)
    page.wait_for_timeout(2500)

    body = page.locator("body").inner_text()
    if plan.token.strip().lower() not in body.lower():
        return {"ok": False, "reason": f"token not visible on reload ({page.url!r})"}
    # Safeguard: if the erase request IS already present, don't re-send.
    snippet = (plan.erasure_request_text or "").strip()[:50].lower()
    if snippet and snippet in body.lower():
        return {"ok": False, "reason": "erase request already present in thread -- refusing to double-send"}

    reply = flow.send_message(plan.erasure_request_text)
    flow.assert_real_answer(reply)

    # Save the fresh capture alongside the original (don't overwrite the
    # 2026-09-13 screenshot even though it was useless -- audit trail).
    screenshots_dir = config.TRANSCRIPTS_DIR / "gemini" / cell_id / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(screenshots_dir / "02_erase_reerase.png"))

    json_path = config.TRANSCRIPTS_DIR / "gemini" / cell_id / "json" / "02_erase.json"
    data = json.loads(json_path.read_text()) if json_path.exists() else {}
    # Preserve the original (empty / wrong-turn) OCR fields as _prior for the
    # audit trail -- same pattern as the viewport-to-rescroll transition.
    if "reply_text" in data and "reply_text_prior" not in data:
        for key in ("reply_text", "reply_status", "reply_flags", "reply_ui_notes", "reply_source", "reply_extracted_at"):
            if key in data:
                data[f"{key}_prior"] = data[key]
    now = datetime.now(timezone.utc).isoformat()
    data.update({
        "reply_text": reply,
        "reply_status": "complete",
        "reply_flags": [],
        "reply_ui_notes": [],
        "reply_source": RE_ERASE_SOURCE,
        "reply_extracted_at": now,
    })
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(data, indent=2))
    return {"ok": True, "reply_chars": len(reply)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cell", help="One cell id (defaults to running both targets).")
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    cells = [args.cell] if args.cell else TARGET_CELLS

    with sync_playwright() as pw:
        with GeminiFlow(headless=args.headless, session_label="nlforget", playwright=pw) as flow:
            for cell in cells:
                print(f"\n[gemini] re-erasing {cell}")
                try:
                    result = reerase_cell(flow, cell)
                except Exception as exc:
                    print(f"  FAILED: {exc}")
                    continue
                if result["ok"]:
                    print(f"  OK -- reply {result['reply_chars']} chars")
                else:
                    print(f"  skipped: {result['reason']}")


if __name__ == "__main__":
    main()
