"""Backfills the platform's reply into NL-forget erase transcripts from their screenshots.

Until 2026-09-23 the erase step saved only the erasure method's name in
`json/02_erase.json`, so the reply to a typed NL-forget request survived only
as `screenshots/02_erase.png` (798 cells). The reply is what the paper's
Acknowledgment measurement is coded from, so it has to exist as text.

The screenshots are the only source on disk, so the text is read out of them
with macOS's built-in Vision OCR (`ocr_screenshot.swift`). Two things follow
from that, and both are recorded per cell instead of being hidden:

  * The screenshots are 1280x720 viewport captures, not whole pages. A long
    reply can run past the bottom edge, a toast can sit on top of it, Claude's
    upsell modal can blur it out entirely, and DeepSeek scrolls a long reply
    so far that the request is off the top. A partial reply saved as "the
    reply" could hide a redirect ("go to Settings") that changes how the reply
    is coded, so every cell gets a `reply_status`:

      complete           request and the end of the reply are both visible
      check              as complete, but OCR read a line with low confidence
      cut_off            reply runs into the input box or is under a toast
      start_not_visible  request is not on screen, so the reply's start is unverified
      covered            a modal hides the chat (Claude's upsell)
      no_reply_visible   nothing found below the request

    Only `complete` and `check` are the whole reply. The others are what was
    visible, and need the platform's own conversation (or the user) to finish.

  * OCR can misread a character. Language correction is off (see the Swift
    file) so unusual words are not "fixed" toward dictionary words; the raw
    OCR of every screenshot is kept next to it as `02_erase_ocr.json`.

The reply is written into `02_erase.json` under NEW keys (`reply_text`,
`reply_status`, `reply_flags`, `reply_source`, `reply_extracted_at`). The
`exchanges` key is left alone: it means "captured from the page", which this
is not. Nothing existing in the file is changed.

    python extract_erase_replies.py                 # OCR + report, no transcript changes
    python extract_erase_replies.py --write         # also fill the JSONs
    python extract_erase_replies.py --write --force # redo cells already filled
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import subprocess
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path

import openpyxl

import config

OCR_SOURCE = "screenshot OCR (macOS Vision, language correction off); not captured from the page"
OCR_SOURCE_RESCROLL = (
    "screenshot OCR (macOS Vision, language correction off); 1280x720 viewport capture from the "
    "reloaded conversation with the request scrolled to the top (recover_erase_replies.py), "
    "replacing the earlier viewport-cropped reply"
)
OCR_BINARY = config.TESTER_ROOT / "data" / "ocr_screenshot"
OCR_SOURCE_FILE = config.TESTER_ROOT / "ocr_screenshot.swift"
REPORT_PATH = config.TESTER_ROOT / "data" / "erase_reply_extraction.csv"
REPORT_PATH_RESCROLL = config.TESTER_ROOT / "data" / "erase_reply_extraction_rescroll.csv"

VIEW_W, VIEW_H = 1280, 720  # every screenshot is this viewport size; Copilot's at 4x
HEADER_BOTTOM = 50
INPUT_CLEARANCE = 12  # a reply whose last line is this close to the input box is cut off

# (right edge of the sidebar, right edge of the chat pane, top of the input box), in
# viewport pixels, measured from real screenshots of each platform.
PANE: dict[str, tuple[int, int, int]] = {
    "chatgpt": (262, VIEW_W, 640),
    "claude": (285, VIEW_W, 628),
    "gemini": (288, VIEW_W, 605),
    "deepseek": (262, 1225, 565),  # right edge cuts off the scroll-position marker
    "perplexity": (240, 930, 608),
    "copilot": (52, VIEW_W, 572),
}

# ChatGPT puts an ad card under the reply, after the row of action icons; Perplexity floats
# a cookie-consent card into the chat column once the reply ends. Both are told apart from
# a reply by the gap: a reply's own paragraphs are at most ~46px apart, the chrome below
# sits further off. Measured per-platform from live screenshots: ChatGPT's icon row puts
# the ad card 80px+ away; Perplexity's reply-to-cookie-card gap is ~50px.
AD_GAP: dict[str, int] = {"chatgpt": 60, "perplexity": 40}

# Floating overlays that sit inside the chat column after the reply and must be stripped
# whenever they appear -- not every rescroll screenshot catches them, but when it does the
# OCR picks them up as plain text in the pane range. The gap-based AD_GAP cut above
# normally catches them first; this is a belt-and-braces match on the opening line, used
# to truncate reply_lines in case the gap wasn't enough.
_OVERLAY_START = re.compile(r"^.{0,3}(cookie policy|we and our partners use cookies)", re.IGNORECASE)

# UI text that is on screen but is not part of the reply. "Edit in a page" (Copilot) is
# matched loosely because OCR reads it many ways ("Editin a page", "Eitina page").
_CHROME = re.compile(
    r"^(ask anything|ask gemini|ask a follow-?up|message deepseek|message copilot|write a message"
    r"|researched( \d+s)?|dictate|message is empty|flash|smart|model"
    r"|free preview of advanced search.*|learn more|read more|pro|ad|search|computer)\b"
    r"|can make mistakes|ai-generated, for reference only|ads do not influence"
    r"|^.{0,12}(edit|eit)\w*\s*(in\s*)?a?\s*page$",
    re.IGNORECASE,
)
# Status pills the chat UI draws before a reply ("Memory updated", "Read and updated memory ›",
# "Memory deleted ›"). Not the platform's words, but evidence of what the interface showed (a
# memory being read, changed or deleted), so they are kept apart in `reply_ui_notes` instead of
# dropped. They often share a line with the reply's first words, so they are stripped as a prefix.
_UI_PILL = re.compile(
    r"^.{0,3}\b(read and updated memory|memory (updated|saved|deleted)|updated memory( [\w.-]+\.md)?"
    r"|updating memory|reading memory|saved to memory)\b\s*[›>»]?\s*",
    re.IGNORECASE,
)
_MODAL = re.compile(r"use opus|upgrade to pro|higher usage limits|see all plans|not now", re.IGNORECASE)
_TOAST = re.compile(r"free preview of advanced search", re.IGNORECASE)
_LOW_CONFIDENCE = 0.35


@dataclass(frozen=True)
class OcrLine:
    text: str
    x: float  # all in viewport pixels, origin top-left
    y: float
    w: float
    h: float
    conf: float

    @property
    def bottom(self) -> float:
        return self.y + self.h


@dataclass
class Reply:
    text: str | None
    status: str
    flags: list[str] = field(default_factory=list)
    ui_notes: list[str] = field(default_factory=list)


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", text.lower().replace("’", "'"))


def _is_noise(line: OcrLine) -> bool:
    """Stray symbols OCR picks up from icons, close buttons and scrollbars ("X", "-", "=")."""
    return sum(ch.isalnum() for ch in line.text) < 3


def load_request_texts(xlsx_path: Path) -> dict[str, str]:
    """Cell id -> the erasure request that was typed, from MASTER and NL FORGET."""
    workbook = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    requests: dict[str, str] = {}
    for sheet in ("MASTER ", "NL FORGET"):
        rows = workbook[sheet].iter_rows(values_only=True)
        header = next(rows)
        column = next(i for i, name in enumerate(header) if name and str(name).startswith("Erasure request text"))
        for row in rows:
            if row[0] and row[column]:
                requests[str(row[0])] = str(row[column])
    return requests


def to_lines(ocr: dict, view_w: float = VIEW_W, view_h: float = VIEW_H) -> list[OcrLine]:
    """Vision's bounding boxes are 0..1 fractions of the image, so pixel
    coordinates come from the image's own dimensions. Viewport-mode defaults
    (1280x720) keep the original call sites working; full-page mode passes
    the real image width/height from the OCR result."""
    return [
        OcrLine(
            text=raw["text"], x=raw["x"] * view_w, y=raw["y"] * view_h,
            w=raw["w"] * view_w, h=raw["h"] * view_h, conf=raw["conf"],
        )
        for raw in ocr.get("lines", [])
    ]


def find_request_bottom(lines: list[OcrLine], request: str) -> float | None:
    """Bottom edge of the typed request on screen, or None if it is not visible.

    The request bubble is several wrapped lines, so lines are matched by word
    overlap with the request text and grouped while they stay close together.
    The last (lowest) group that covers most of the request's words wins,
    because Perplexity also shows the earlier disclosure turn above it. After
    the winning group is picked, its bottom is extended to include single-
    word continuation lines (e.g. a trailing "planning") that the >= 2-word
    filter below excluded -- without this, a request wrapping to a one-word
    tail leaves that tail misidentified as the first line of the reply, and
    AD_GAP then cuts off the real reply as "chrome below the reply"
    (confirmed on PE-NLF-I0005 and a handful of other Perplexity cells)."""
    request_words = set(_words(request))
    if not request_words:
        return None
    matching = [
        line for line in lines
        if len(_words(line.text)) >= 2
        and sum(w in request_words for w in _words(line.text)) / len(_words(line.text)) >= 0.75
    ]
    sorted_pane = sorted(lines, key=lambda ln: ln.y)
    matching_set = {id(line) for line in matching}
    groups: list[list[OcrLine]] = []
    for line in sorted(matching, key=lambda ln: ln.y):
        if not groups:
            groups.append([line])
            continue
        last_bottom = groups[-1][-1].bottom
        gap = line.y - last_bottom
        if gap < 45:
            groups[-1].append(line)
            continue
        # Larger gap -- extend the group only when no non-matching pane line
        # sits in that gap. The intended case is a long request bubble where
        # Vision OCR dropped a line or three; the counterexample is a short
        # request bubble immediately followed by the reply, where a reply
        # line (or a chrome pill like "Researched 1s") sits in the gap and
        # must break the group so the reply doesn't get swallowed into the
        # request's bottom. Confirmed on CH-NLF-I0302 (OCR missed 3 of 11
        # request lines, 98px gap, no intervening lines).
        intervening = [
            ln for ln in sorted_pane
            if last_bottom < ln.y < line.y and id(ln) not in matching_set
        ]
        if gap < 150 and not intervening:
            groups[-1].append(line)
        else:
            groups.append([line])
    for group in reversed(groups):
        covered = {w for ln in group for w in _words(ln.text)} & request_words
        if len(covered) / len(request_words) >= 0.6:
            bottom = max(ln.bottom for ln in group)
            while True:
                extended = False
                for ln in lines:
                    if bottom < ln.y < bottom + 30:
                        tail_words = _words(ln.text)
                        if tail_words and all(w in request_words for w in tail_words):
                            bottom = max(bottom, ln.bottom)
                            extended = True
                if not extended:
                    break
            return bottom
    return None


def _join_paragraphs(lines: list[OcrLine]) -> str:
    """Wrapped lines are joined with a space; a blank line's worth of gap starts a new paragraph.

    The gap is measured between one line's box and the next (not between line tops), so a
    tall line does not read as a paragraph break."""
    if not lines:
        return ""
    height = statistics.median(ln.h for ln in lines)
    paragraphs: list[list[str]] = [[lines[0].text]]
    for prev, line in zip(lines, lines[1:]):
        if line.y - prev.bottom > 0.9 * height:
            paragraphs.append([])
        paragraphs[-1].append(line.text)
    return "\n\n".join(" ".join(p) for p in paragraphs)


def extract_reply(platform: str, ocr: dict, request: str | None) -> Reply:
    # Rescroll captures hide the sidebar and grow the viewport to fit the
    # whole reply, so the image can be taller than the 1280x720 default.
    # Scale OCR's fractional y to the real image height so pixel geometry
    # (HEADER_BOTTOM, input_top) still applies -- and translate input_top
    # (viewport-mode distance from the top of a 720-tall viewport) into the
    # taller image by preserving its distance from the viewport bottom,
    # since the composer stays position:fixed to the bottom.
    sidebar_right, pane_right, input_top = PANE[platform]
    image_h = float(ocr.get("height") or VIEW_H)
    is_tall = image_h > VIEW_H * 1.1
    if is_tall:
        view_h = image_h
        input_top = view_h - (VIEW_H - input_top)
    else:
        view_h = VIEW_H
    lines = to_lines(ocr, view_h=view_h)

    if any(_MODAL.search(line.text) for line in lines):
        return Reply(None, "covered", ["a modal is over the chat"])

    pane = [
        ln for ln in lines
        if ln.x >= sidebar_right and ln.x < pane_right and ln.y >= HEADER_BOTTOM
    ]
    toast_ys = [ln.y for ln in pane if _TOAST.search(ln.text)]

    flags: list[str] = []
    request_bottom = find_request_bottom(pane, request) if request else None
    if request_bottom is None:
        flags.append("request not visible")
        request_bottom = HEADER_BOTTOM
    # Strip leading non-word prefixes before chrome-matching so Perplexity's
    # "= Researched" status pill (OCR'd with a stray leading "=") still gets
    # recognized as chrome. The `_CHROME` regex is anchored at `^` on purpose
    # (matches titles, not substrings), so a cheap lstrip reaches the same
    # anchor cases without broadening the regex.
    def _stripped_for_chrome(text: str) -> str:
        return text.lstrip("=•+·»><- ").strip()

    reply_lines = sorted(
        (
            ln for ln in pane
            if ln.y > request_bottom and ln.bottom <= input_top + INPUT_CLEARANCE
            and not _is_noise(ln) and not _CHROME.search(_stripped_for_chrome(ln.text))
        ),
        key=lambda ln: (round(ln.y), ln.x),
    )
    # Truncate at the first floating-overlay opener (cookie banner, etc.) in
    # case AD_GAP's gap-based cut wasn't enough -- useful when the reply
    # ended right next to the overlay with no visible gap.
    for i, ln in enumerate(reply_lines):
        if _OVERLAY_START.search(ln.text):
            reply_lines = reply_lines[:i]
            break
    ui_notes: list[str] = []
    while reply_lines and (pill := _UI_PILL.match(reply_lines[0].text)):
        ui_notes.append(pill.group(1))
        rest = reply_lines[0].text[pill.end():]
        reply_lines = ([replace(reply_lines[0], text=rest)] if any(c.isalnum() for c in rest) else []) + reply_lines[1:]

    ended_visibly = False  # something other than the reply follows it, so it is not cut off
    if ad_gap := AD_GAP.get(platform):
        for i, (prev, ln) in enumerate(zip(reply_lines, reply_lines[1:]), start=1):
            if ln.y - prev.bottom > ad_gap:
                reply_lines, ended_visibly = reply_lines[:i], True
                break
    if not reply_lines:
        return Reply(None, "no_reply_visible", flags, ui_notes)

    if not ended_visibly and reply_lines[-1].bottom >= input_top - INPUT_CLEARANCE:
        flags.append("reply reaches the input box")
    if toast_ys and any(reply_lines[0].y <= y <= reply_lines[-1].bottom + 40 for y in toast_ys):
        flags.append("a toast overlaps the reply")
    if any(ln.conf < _LOW_CONFIDENCE for ln in reply_lines):
        flags.append("low-confidence OCR line")

    text = _join_paragraphs(reply_lines)
    if "request not visible" in flags:
        status = "start_not_visible"
    elif "reply reaches the input box" in flags or "a toast overlaps the reply" in flags:
        status = "cut_off"
    elif "low-confidence OCR line" in flags:
        status = "check"
    else:
        status = "complete"
    return Reply(text, status, flags, ui_notes)


def ensure_ocr_binary(binary: Path = OCR_BINARY) -> Path:
    if not binary.exists() or binary.stat().st_mtime < OCR_SOURCE_FILE.stat().st_mtime:
        binary.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["swiftc", "-O", "-o", str(binary), str(OCR_SOURCE_FILE)], check=True)
    return binary


def run_ocr(images: list[Path], binary: Path, batch: int = 40) -> dict[str, dict]:
    results: dict[str, dict] = {}
    for start in range(0, len(images), batch):
        chunk = images[start:start + batch]
        out = subprocess.run(
            [str(binary), *map(str, chunk)], check=True, capture_output=True, text=True
        ).stdout
        for line in out.splitlines():
            record = json.loads(line)
            results[record["image"]] = record
        print(f"OCR {min(start + batch, len(images))}/{len(images)}", flush=True)
    return results


def find_targets(force: bool) -> list[tuple[str, str, Path]]:
    """(platform, cell id, erase json) for every NL-forget erase that has no captured reply."""
    targets = []
    for path in sorted(config.TRANSCRIPTS_DIR.glob("*/*/json/02_erase.json")):
        data = json.loads(path.read_text())
        if "exchanges" in data or not str(data.get("erasure_type_text", "")).startswith("NL forget"):
            continue
        if "reply_text" in data and not force:
            continue
        targets.append((path.parts[-4], path.parts[-3], path))
    return targets


def find_rescroll_targets(force: bool) -> list[tuple[str, str, Path]]:
    """(platform, cell id, erase json) for every NL-forget cell with a
    `02_erase_rescroll.png` captured by `recover_erase_replies.py` -- a
    re-reload where the request bubble was scrolled to the top of the
    viewport before the screenshot, so the reply fills the space below. The
    captures are still standard 1280x720 viewport images, so the same
    `extract_reply()` logic applies, just reading the new file. `--force`
    redoes cells whose `reply_source` already reflects the rescroll pass.
    Cells whose text came from a live re-erase (reerase_gemini_cells.py and
    similar) are always skipped -- the rescroll.png on disk reflects the
    pre-reerase thread and would overwrite the fresh reply with wrong-turn
    OCR."""
    targets = []
    for path in sorted(config.TRANSCRIPTS_DIR.glob("*/*/json/02_erase.json")):
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        if not str(data.get("erasure_type_text", "")).startswith("NL forget"):
            continue
        rescroll_image = path.parent.parent / "screenshots" / "02_erase_rescroll.png"
        if not rescroll_image.exists():
            continue
        source = data.get("reply_source", "")
        if source.startswith("live re-erase"):
            continue
        if source == OCR_SOURCE_RESCROLL and not force:
            continue
        targets.append((path.parts[-4], path.parts[-3], path))
    return targets


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--write", action="store_true", help="fill the reply into 02_erase.json")
    parser.add_argument("--force", action="store_true", help="also redo cells already filled")
    parser.add_argument("--reocr", action="store_true", help="OCR again even where a saved OCR json is newer than the screenshot")
    parser.add_argument("--limit", type=int, help="only the first N cells (for a trial)")
    parser.add_argument(
        "--rescroll", action="store_true",
        help="run against `02_erase_rescroll.png` captures from `recover_erase_replies.py` "
             "instead of the original viewport screenshots. Preserves the old reply_* fields "
             "as reply_*_prior on first overwrite so the audit trail stays visible.",
    )
    args = parser.parse_args()

    screenshot_name = "02_erase_rescroll.png" if args.rescroll else "02_erase.png"
    cache_name = "02_erase_rescroll_ocr.json" if args.rescroll else "02_erase_ocr.json"
    report_path = REPORT_PATH_RESCROLL if args.rescroll else REPORT_PATH
    reply_source = OCR_SOURCE_RESCROLL if args.rescroll else OCR_SOURCE
    targets = (find_rescroll_targets(args.force) if args.rescroll else find_targets(args.force))[: args.limit]
    requests = load_request_texts(config.MASTER_XLSX_PATH)
    images = [json_path.parent.parent / "screenshots" / screenshot_name for _, _, json_path in targets]
    cache = {image: image.parent.parent / "json" / cache_name for image in images}
    fresh = [
        image for image in images
        if args.reocr or not cache[image].exists() or cache[image].stat().st_mtime < image.stat().st_mtime
    ]
    ocr_by_image = run_ocr(fresh, ensure_ocr_binary()) if fresh else {}
    for image in images:
        if str(image) not in ocr_by_image:
            ocr_by_image[str(image)] = json.loads(cache[image].read_text())

    now = datetime.now(timezone.utc).isoformat()
    rows: list[dict] = []
    for (platform, cell_id, json_path), image in zip(targets, images):
        ocr = ocr_by_image[str(image)]
        (json_path.parent / cache_name).write_text(json.dumps(ocr, indent=2))
        reply = extract_reply(platform, ocr, requests.get(cell_id))
        rows.append({
            "cell_id": cell_id, "platform": platform, "status": reply.status,
            "flags": "; ".join(reply.flags), "chars": len(reply.text or ""),
            "request_known": cell_id in requests,
        })
        if args.write:
            data = json.loads(json_path.read_text())
            # Rescroll overwrites preserve the viewport-mode OCR fields as
            # reply_*_prior on first overwrite only; a second rescroll run
            # keeps that same prior intact (don't clobber the real original).
            if args.rescroll and "reply_text" in data and "reply_text_prior" not in data:
                for key in ("reply_text", "reply_status", "reply_flags", "reply_ui_notes", "reply_source", "reply_extracted_at"):
                    if key in data:
                        data[f"{key}_prior"] = data[key]
            data.update({
                "reply_text": reply.text, "reply_status": reply.status, "reply_flags": reply.flags,
                "reply_ui_notes": reply.ui_notes,
                "reply_source": reply_source, "reply_extracted_at": now,
            })
            json_path.write_text(json.dumps(data, indent=2))

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["cell_id"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"{len(rows)} cells; wrote transcripts: {args.write}; rescroll: {args.rescroll}; report: {report_path}")
    for platform in sorted({r["platform"] for r in rows}):
        counts: dict[str, int] = {}
        for r in rows:
            if r["platform"] == platform:
                counts[r["status"]] = counts.get(r["status"], 0) + 1
        print(f"  {platform:11s}", counts)


if __name__ == "__main__":
    main()
