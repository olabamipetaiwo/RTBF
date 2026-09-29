"""Records an erasure that was done BY HAND, so it lands in the same places an automated erasure does.

Used when the automation session cannot log in as the account holding the injected chats (Copilot's NL-forget
cells, 2026-09-23; Copilot's battery cells CO-I1-E4 and CO-I1-E6, 2026-09-29). For one cell it:
  1. copies the screenshots to transcripts/<platform>/<cell>/screenshots/02_erase.png (then 02_erase_2.png, ...),
  2. writes json/02_erase.json with a "source" field saying it was manual, so it is never mistaken for an
     automated capture. An NL-forget cell gets the typed request and the reply (transcribed from the
     screenshot); a battery (MASTER) cell has no typed request, so it gets --outcome, a plain statement of
     what was done and what was found,
  3. marks the cell erased in data/run_tracking.json at the given time (this starts the 31-day recall clock),
  4. sets the cell's sheet row (NL FORGET or MASTER) to ERASED and appends a "manually erased" note.

FILE SUBSTUDY cells are not supported yet.

The erasure time should be the time on the screenshot itself (a macOS screenshot's filename carries it).

    .venv/bin/python record_manual_erasure.py CO-NLF-I0032 /path/to/shot.png \\
        --erased-at "2026-09-23 19:52" --reply-file reply.txt [--dry-run]
    .venv/bin/python record_manual_erasure.py CO-I1-E4 memory.png chat.png \\
        --erased-at "2026-09-29 16:17" --outcome "Saved memories list empty; nothing to delete"

If what happened was not one clean request (a send that was stopped and retyped, a changed wording), record
the real sequence: --exchanges-file holds a JSON list of {"sent", "reply"} in order, and --deviation states
in words what differs from the protocol. Both are written into 02_erase.json and the sheet's Notes.

Never overwrites an existing 02_erase.png or 02_erase.json, and refuses a cell that is not still "injected".
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

import config
import run_cell
import tracking

SOURCE_NOTE = "manual: typed by hand in the cell's own chat; reply transcribed from the screenshot"
BATTERY_SOURCE_NOTE = "manual: erasure done by hand in the platform's UI; outcome stated by the person who did it"


def _parse_local(text: str) -> datetime:
    """A wall-clock time as typed ("2026-09-23 19:52" or with seconds), in this machine's local zone."""
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
        try:
            return datetime.strptime(text, fmt).astimezone()
        except ValueError:
            continue
    raise SystemExit(f"--erased-at {text!r}: expected e.g. '2026-09-23 19:52'")


def record(
    cell_id: str, screenshots: list[Path], reply: str | None, erased_at: datetime, dry_run: bool = False,
    exchanges: list[dict] | None = None, deviation: str | None = None, outcome: str | None = None,
) -> dict:
    plan = run_cell.load_cell(cell_id)
    if plan.sheet not in ("NLFORGET", "MASTER"):
        raise SystemExit(f"{cell_id}: on the {plan.sheet} sheet, this recorder only handles NL FORGET and MASTER cells.")
    entry = tracking.get(cell_id)
    if not entry or entry.get("status") != "injected":
        raise SystemExit(f"{cell_id}: status is {entry.get('status') if entry else 'not tracked'!r}, expected 'injected'.")
    if plan.sheet == "NLFORGET":
        if not plan.erasure_request_text:
            raise SystemExit(f"{cell_id}: no erasure request text on the sheet.")
        if reply is None:
            raise SystemExit(f"{cell_id}: an NL-forget cell needs --reply, --reply-file or --exchanges-file.")
    elif not outcome:
        raise SystemExit(f"{cell_id}: a battery cell has no typed request, so --outcome is required.")
    for screenshot in screenshots:
        if not screenshot.is_file():
            raise SystemExit(f"screenshot not found: {screenshot}")

    # Paths only: run_cell._cell_dir() also creates the folders, which a dry run must not do.
    base = config.TRANSCRIPTS_DIR / plan.platform / cell_id
    png_dests = [
        base / "screenshots" / ("02_erase.png" if i == 0 else f"02_erase_{i + 1}.png") for i in range(len(screenshots))
    ]
    json_dest = base / "json" / "02_erase.json"
    for dest in (*png_dests, json_dest):
        if dest.exists():
            raise SystemExit(f"{dest} already exists, not overwriting.")

    transcript = {"erasure_type_text": plan.erasure_type_text}
    if plan.sheet == "NLFORGET":
        transcript["exchanges"] = exchanges or [{"sent": plan.erasure_request_text, "reply": reply}]
        transcript["source"] = SOURCE_NOTE
    else:
        transcript["outcome"] = outcome
        transcript["source"] = BATTERY_SOURCE_NOTE
    transcript["erased_at"] = erased_at.isoformat()
    transcript["screenshot_original_names"] = [screenshot.name for screenshot in screenshots]
    detail = "reply transcribed from screenshot" if plan.sheet == "NLFORGET" else outcome
    breadcrumb = f"manually erased {erased_at.isoformat()} (by hand; {detail})"
    if deviation:
        transcript["deviation"] = deviation
        breadcrumb += f" | DEVIATION: {deviation}"

    if dry_run:
        for screenshot, png_dest in zip(screenshots, png_dests):
            print(f"[dry run] {cell_id}: would copy {screenshot.name} -> {png_dest}")
        print(f"[dry run] would write {json_dest}: {transcript}")
        print(f"[dry run] would mark erased at {erased_at.isoformat()} and set the sheet's Run status to ERASED ({breadcrumb})")
        return transcript

    png_dests[0].parent.mkdir(parents=True, exist_ok=True)
    json_dest.parent.mkdir(parents=True, exist_ok=True)
    for screenshot, png_dest in zip(screenshots, png_dests):
        shutil.copy2(screenshot, png_dest)
    json_dest.write_text(json.dumps(transcript, indent=2))
    marked = tracking.mark_erased(cell_id, erased_at)
    if plan.sheet == "NLFORGET":
        run_cell._update_nlforget_row(cell_id, {run_cell.NLF_COL_RUN_STATUS: "ERASED"}, note_breadcrumb=breadcrumb)
    else:
        run_cell._update_master_row(cell_id, {run_cell.COL_RUN_STATUS: "ERASED"}, note_breadcrumb=breadcrumb)
    print(f"{cell_id}: recorded. erased_at={marked['erased_at']} recall_due_at={marked['recall_due_at']}")
    return transcript


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("cell_id")
    parser.add_argument("screenshots", type=Path, nargs="+", help="the first is saved as 02_erase.png, the rest as 02_erase_2.png, ...")
    parser.add_argument("--erased-at", required=True, help="local time on the screenshot, e.g. '2026-09-23 19:52'")
    reply = parser.add_mutually_exclusive_group()
    reply.add_argument("--reply", help="the platform's reply, transcribed")
    reply.add_argument("--reply-file", type=Path, help="file holding the transcribed reply")
    reply.add_argument("--exchanges-file", type=Path, help="JSON list of {sent, reply}: the real sequence, when it was not one clean request")
    parser.add_argument("--deviation", help="what differs from the protocol, in words (required with --exchanges-file)")
    parser.add_argument("--outcome", help="battery (MASTER) cells: what was done and found, in words")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    exchanges = None
    if args.exchanges_file:
        if not args.deviation:
            raise SystemExit("--exchanges-file needs --deviation saying what differs from one clean request.")
        exchanges = json.loads(args.exchanges_file.read_text())
        text = exchanges[-1]["reply"]
    else:
        text = args.reply if args.reply is not None else (args.reply_file.read_text().strip() if args.reply_file else None)
    record(args.cell_id, args.screenshots, text, _parse_local(args.erased_at), args.dry_run, exchanges, args.deviation, args.outcome)


if __name__ == "__main__":
    main()
