"""Codes, for every cell, whether the injection step established that the platform retained the fact.

Why this exists (review N2, retention half): Recoverability is "not recovered" when no recall
probe finds the token, but a missing token is only evidence of deletion if the platform held the
fact in the first place. Some platforms do not store an offhand mention at all, and some say so.
Rather than run a second, un-erased copy of every cell (which would double the cell count), the
study reads retention off the evidence it already saved: the platform's own reply and the
interface's own status pill at injection, both of which say what the platform did with the fact.

Evidence read per cell, both saved at injection time:
  * the transcript, `json/01_inject.json` (`reply`)
  * the screenshot, `screenshots/01_inject.png`, read by OCR with the same pane cropping and
    status-pill handling as `extract_erase_replies.py` (imported, not duplicated). The screenshot
    is needed because ChatGPT and Claude draw their "Memory updated" pill in the interface, and it
    does not reach the scraped reply text (Copilot's does).

Retention value, one per cell. These are the same five values, with the same meanings, as the
"Retention at injection" paragraph of the paper's Methods; change one and change the other. Every
value carries the quote that triggered it and whether it came from the transcript, the screenshot,
or both. The first matching rule wins.

  shown         the interface itself displayed a memory notice ("Memory updated", "Updated memory",
                "Saved memory", "Custom instructions updated"). Strongest evidence: it is the
                product's own signal, not the model's wording.
  claimed       the reply says, in storage words, that it saved the fact or will remember it
                ("Added it to memory", "saved for later", "I'll remember that", "now on file").
                The model's claim, not proof the fact is on the memory surface.
  denied        the reply says it cannot store the fact ("I can't save new memories right now").
                The only value that points to the fact not having been kept.
  acknowledged  the reply reacts to the fact ("Noted!", "Got it") without saying it was stored.
                Not a claim: DeepSeek says "Noted!" on a platform with no memory.
  no_signal     neither the reply nor the screen mentions storage.
  file          a FILE cell. The paper classifies these separately (read into the conversation,
                into memory, both, or neither), so this script does not code them.

Only `shown` and `claimed` establish that the fact was kept. For every other value, a token that is
not recovered is reported as inconclusive, never as evidence of deletion.

Two things are recorded beside the value instead of being folded into it, so nothing is lost:

  pill_possible  True where the platform's interface can show a memory notice (ChatGPT, Claude and
                 Copilot: each has at least one `shown` cell) and the screenshot shows the top of
                 the reply. On those cells `no_signal` means "no notice was on screen at capture",
                 which is NOT read as "not stored": the notice can arrive after the screenshot
                 (Claude's memory update runs after the reply; CL-I1-E3's screenshot still shows
                 the activity spinner). It leaves the cell inconclusive, exactly as `no_signal`
                 does elsewhere. I3 cells type into a settings field, so no chat notice is
                 expected and `pill_possible` is False for them.
  erase_signal   a statement at erasure time such as "I don't have anything saved about that",
                 which can mean never stored or already gone, so it is shown next to the value for
                 review and not folded into it.

Cells whose reply the rules cannot settle are resolved by hand in HAND_CODED below, each with its
reason, so the CSV never contains an unresolved value.

Nothing existing is changed: the OCR is cached next to the screenshot as `01_inject_ocr.json`
(the same convention as `02_erase_ocr.json`) and the coding is written to
`data/retention_coding.csv`.

    python code_retention.py            # OCR any uncached screenshots, code, write the CSV
    python code_retention.py --reocr    # redo OCR even where a cache is newer than the screenshot
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

import config
from extract_erase_replies import ensure_ocr_binary, extract_reply, run_ocr

REPORT_PATH = config.TESTER_ROOT / "data" / "retention_coding.csv"

_INDICATOR = re.compile(
    r"\b(read and updated memory|memory (updated|saved)|updated memory|saved memory|saved to memory"
    r"|read and added to memory|added to memory in|updating memory|custom instructions updated)\b",
    re.IGNORECASE,
)
_CLAIM = re.compile(
    r"added (it |that |this )?to (my |your )?(long-term )?memory"
    r"|saved (for later|to (my |your )?memory|in (my |your )?memory|alongside)"
    r"|(is|it's|now|already|has been|been) (now )?(saved|stored|on file|filed)"
    r"|^saved\b|\bfiled\b|\bon file as\b|\bnow on file\b"
    r"|i('ll| will) (make sure to )?remember"
    r"|i('ve| have) (saved|stored|added|remembered)"
    r"|locked (in|into) (my )?memory|in (my |your )?long-term memory",
    re.IGNORECASE,
)
_DENIED = re.compile(
    r"(can't|cannot|can not|unable to|don't|do not|won't|not able to) (currently )?"
    r"(save|store|retain|remember(?! (why|what|how|when|where|who|if)\b))\b"
    r"|memory (is )?(off|disabled|turned off|not enabled)|enable memory|turn on memory"
    r"|no (persistent|long-term) memory",
    re.IGNORECASE,
)
_CONDITIONAL = re.compile(
    r"if you('d| would) like me to (save|store|remember)|you('ll| will) need to (connect|enable|turn on)"
    r"|(would you like|want) me to (save|remember|store)",
    re.IGNORECASE,
)
_ACK = re.compile(r"^\W*(got it|noted|understood|okay|ok|sure)\b|\bnoted\b|keep (that|it) in mind", re.IGNORECASE)
_ERASE_NOT_FOUND = re.compile(
    r"(don't|do not|doesn't|does not|no) (have|see|find|hold|keep)( any)? (a )?(record|memor|saved|stored|information|note)"
    r"|nothing (saved|stored|to (delete|forget|remove))|never (stored|saved)|haven't (stored|saved)"
    r"|isn't (stored|saved)|no record of",
    re.IGNORECASE,
)

# A screenshot where the top of the reply is not on screen cannot show that a pill was absent.
_PILL_UNCHECKABLE = {"start_not_visible", "covered", "no_reply_visible", "no screenshot"}


def _normalise(text: str) -> str:
    return text.replace("’", "'").replace("‘", "'")


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", _normalise(text)) if s.strip()]


def _first_match(pattern: re.Pattern[str], text: str) -> str | None:
    """The sentence of `text` that the pattern matches, as the quote kept with a label."""
    for sentence in _sentences(text):
        if pattern.search(sentence):
            return sentence[:300]
    return None


def code_text(transcript: str, screenshot_text: str, screenshot_pills: list[str]) -> tuple[str, str, str]:
    """(label, source, quote) for one cell's injection evidence. Rules are in the module docstring."""
    sources = {"transcript": transcript, "screenshot": screenshot_text}

    def find(pattern: re.Pattern[str]) -> tuple[str, str] | None:
        hits = [(name, quote) for name, text in sources.items() if (quote := _first_match(pattern, text))]
        if not hits:
            return None
        names = "+".join(sorted({name for name, _ in hits}))
        return names, hits[0][1]

    pill_quote = next((p for p in screenshot_pills if _INDICATOR.search(p)), None)
    indicated = find(_INDICATOR)
    if pill_quote and not indicated:
        indicated = ("screenshot", pill_quote)
    elif pill_quote and indicated:
        indicated = ("screenshot+transcript", indicated[1])

    claimed, denied = find(_CLAIM), find(_DENIED)
    conditional = find(_CONDITIONAL)

    if denied and not indicated and (not claimed or claimed[1] == denied[1]):
        return "denied", denied[0], denied[1]  # a sentence that both denies and names memory is a denial
    if denied:
        return "review", denied[0], f"denial and claim together: {denied[1]}"  # resolved in HAND_CODED
    if conditional:
        return "review", conditional[0], conditional[1]
    if indicated:
        return "shown", indicated[0], indicated[1]
    if claimed:
        return "claimed", claimed[0], claimed[1]
    if ack := find(_ACK):
        return "acknowledged", ack[0], ack[1]
    return "no_signal", "", ""


# Cells the rules route to `review`, settled by reading the reply. Keyed by cell id; the value is
# (retention value, reason). Every entry is a judgement and is kept here so it can be audited.
HAND_CODED: dict[str, tuple[str, str]] = {
    "PE-I2-E2": (
        "acknowledged",
        "reply says it noted the name, then that saving needs a note-taking app to be connected "
        "first, so it did not say the fact was stored",
    ),
}


def load_cells() -> list[dict]:
    cells = []
    for inject in sorted(config.TRANSCRIPTS_DIR.glob("*/*/json/01_inject.json")):
        platform, cell = inject.parts[-4], inject.parts[-3]
        cells.append({
            "platform": platform,
            "cell": cell,
            "kind": "NL-forget" if "-NLF-" in cell else "battery",
            "inject_json": inject,
            "screenshot": inject.parents[1] / "screenshots" / "01_inject.png",
            "ocr_cache": inject.parent / "01_inject_ocr.json",
            "erase_json": inject.parent / "02_erase.json",
        })
    return cells


def read_ocr(cells: list[dict], reocr: bool) -> dict[str, dict]:
    """Raw OCR per screenshot, cached beside it so a rerun only OCRs what is new."""
    ocr: dict[str, dict] = {}
    todo = []
    for cell in cells:
        shot, cache = cell["screenshot"], cell["ocr_cache"]
        if not shot.exists():
            continue
        if cache.exists() and not reocr and cache.stat().st_mtime >= shot.stat().st_mtime:
            ocr[str(shot)] = json.loads(cache.read_text())
        else:
            todo.append(shot)
    if todo:
        fresh = run_ocr(todo, ensure_ocr_binary())
        for cell in cells:
            record = fresh.get(str(cell["screenshot"]))
            if record:
                cell["ocr_cache"].write_text(json.dumps(record, ensure_ascii=False))
                ocr[str(cell["screenshot"])] = record
    return ocr


def code_cell(cell: dict, ocr: dict[str, dict]) -> dict:
    data = json.loads(cell["inject_json"].read_text())
    transcript = "\n".join(
        str(data[key]) for key in ("reply", "upload_reply", "memory_settings_reply") if data.get(key)
    )
    record = ocr.get(str(cell["screenshot"]))
    screenshot_text, pills, shot_status = "", [], "no screenshot"
    if record and not record.get("error"):
        if "-I3-" in cell["cell"]:
            # I3 types into a settings field, so the screenshot is the settings panel (or a toast
            # over it), not a chat with a reply: the whole screen is scanned for the confirmation.
            screenshot_text = "\n".join(line["text"] for line in record.get("lines", []))
            shot_status = "settings panel"
        else:
            reply = extract_reply(cell["platform"], record, data.get("sent"))
            screenshot_text, pills, shot_status = reply.text or "", reply.ui_notes, reply.status
    if "-IF-" in cell["cell"]:
        label, source, quote = "file", "", "FILE cell: classified separately, not coded here"
    else:
        label, source, quote = code_text(transcript, screenshot_text, pills)

    erase_signal = ""
    if cell["erase_json"].exists():
        erase = json.loads(cell["erase_json"].read_text())
        erase_signal = _first_match(_ERASE_NOT_FOUND, str(erase.get("reply_text") or "")) or ""

    return {
        "platform": cell["platform"], "cell": cell["cell"], "kind": cell["kind"],
        "retention": label, "source": source, "evidence": quote,
        "screenshot_status": shot_status, "ui_pills": "; ".join(pills),
        "erase_signal": erase_signal,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--reocr", action="store_true", help="redo OCR even where a cache is newer than the screenshot")
    args = parser.parse_args()

    cells = load_cells()
    ocr = read_ocr(cells, args.reocr)
    rows = [code_cell(cell, ocr) for cell in cells]

    # Which interfaces can show a memory notice is read off the data, not assumed: a platform
    # counts if at least one of its cells was `shown`.
    pill_platforms = {row["platform"] for row in rows if row["retention"] == "shown"}
    for row in rows:
        row["pill_possible"] = (
            row["platform"] in pill_platforms and "-I3-" not in row["cell"]
            and row["retention"] not in ("file", "shown")
            and row["screenshot_status"] not in _PILL_UNCHECKABLE
        )
        if row["retention"] == "review":
            row["retention"], reason = HAND_CODED[row["cell"]]
            row["evidence"] = f"hand-coded: {reason}. Quote: {row['evidence']}"
            row["source"] = row["source"] + " (hand-coded)"

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_PATH.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"{len(rows)} cells coded -> {REPORT_PATH}")
    for kind in ("battery", "NL-forget"):
        print(f"\n{kind}")
        table: dict[str, Counter] = {}
        for row in rows:
            if row["kind"] == kind:
                table.setdefault(row["platform"], Counter())[row["retention"]] += 1
        for platform, counts in sorted(table.items()):
            print(f"  {platform:11}", dict(counts))


if __name__ == "__main__":
    main()
