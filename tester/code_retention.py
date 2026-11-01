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


# Human review of the rule's value (Compare/RetentionCheck/<platform>-Retention Check.xlsx), for
# every recalled cell whose outcome retention decides. Only cells where the review differs from the
# rule are listed; each was checked against the injection screenshot. Value: (retention, reason).
REVIEWED: dict[str, tuple[str, str]] = {
    # Claude, reviewed 2026-10-26.
    "CL-NLF-I0236": ("shown", 'screenshot shows "Read and updated memory" above the reply; OCR missed it'),
    "CL-I1-E5": ("shown", 'screenshot shows "Read and edited memory" above the reply'),
    "CL-I2-E5": ("shown", 'screenshot shows "Read and edited memory" above the reply (reply also claims it saved)'),
    "CL-I2-E3": ("acknowledged", 'screenshot shows only "Recalled memory quilt.md" (read, not saved); reply asks about the name'),
    "CL-I1-E3": ("acknowledged", 'no memory notice; reply reacts: "I love it"'),
    "CL-I1-E4": ("acknowledged", 'no memory notice; reply reacts: "that\'s a great name"'),
    "CL-NLF-I0000": ("acknowledged", 'no memory notice; reply reacts: "that\'s a genuinely great name"'),
    "CL-NLF-I0002": ("acknowledged", 'no memory notice; reply reacts: "that\'s a name with a story behind it"'),
    # ChatGPT, reviewed 2026-10-26 (applied 2026-10-27; found missing in the audit).
    "CH-I1-E2": ("acknowledged", "no memory notice; reply reacts to the name without storage words (ChatGPT review sheet)"),
    "CH-I1-E7": ("acknowledged", "no memory notice; reply reacts to the name without storage words (ChatGPT review sheet)"),
    "CH-NLF-I0001": ("acknowledged", "no memory notice; reply reacts to the name without storage words (ChatGPT review sheet)"),
    # Gemini, reviewed 2026-10-27. GE-NLF-I0282/I0309/I0322/I0368 ("Logged", "Note updated", "added
    # to the mental log", "into the record") kept acknowledged: figurative, no Saved info entry.
    "GE-I1-E1": ("acknowledged", 'no storage notice or words; reply reacts: "Walrus Scooter Hunchback Subject"'),
    "GE-I1-E2": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolute top-tier name for a vacation itinerary."'),
    "GE-I1-E6": ("acknowledged", 'no storage notice or words; reply reacts: "That is an incredible name for a collection."'),
    "GE-I2-E5": ("shown", 'screenshot shows an "Info saved" toast and the fact listed on the Personal context page'),
    "GE-I2-E6": ("shown", 'screenshot shows an "Info saved" toast and the fact listed on the Personal context page'),
    "GE-NLF-I0000": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolute top-tier synth name."'),
    "GE-NLF-I0001": ("acknowledged", 'no storage notice or words; reply reacts: "That is an elite level of household bureaucratic naming."'),
    "GE-NLF-I0002": ("acknowledged", 'no storage notice or words; reply reacts: "Solid choice—that name sounds like either a high-stakes cyberpunk heist or a deeply…"'),
    "GE-NLF-I0005": ("acknowledged", 'no storage notice or words; reply reacts: "That has a delightfully bureaucratic, almost dystopian ring to it—like a secret…"'),
    "GE-NLF-I0010": ("acknowledged", 'no storage notice or words; reply reacts: "That name sounds like a custom-built monster for a homestead, a very specific…"'),
    "GE-NLF-I0012": ("acknowledged", 'no storage notice or words; reply reacts: "That is a brilliantly absurd name."'),
    "GE-NLF-I0018": ("acknowledged", "no storage notice or words; reply reacts: \"That sounds like a randomly generated name straight out of a game's item pool or a…\""),
    "GE-NLF-I0023": ("acknowledged", 'no storage notice or words; reply reacts: "That is a fantastic name."'),
    "GE-NLF-I0024": ("acknowledged", "no storage notice or words; reply reacts: \"Alphabet Periscope' is certainly a unique and specific title for a puzzle swap project!\""),
    "GE-NLF-I0026": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like an absolute monster of a weapon—or a high-gravity craft beer brewed…"'),
    "GE-NLF-I0027": ("acknowledged", 'no storage notice or words; reply reacts: "That is an delightfully chaotic and wonderfully specific name for a sourdough starter."'),
    "GE-NLF-I0028": ("acknowledged", 'no storage notice or words; reply reacts: "That is a delightfully absurd, highly specific name."'),
    "GE-NLF-I0030": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like the result of either an aggressive autocorrect failure or an elite…"'),
    "GE-NLF-I0036": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like the title of an indie rock album or a secret waypoint on an obscure…"'),
    "GE-NLF-I0042": ("acknowledged", 'no storage notice or words; reply reacts: "That is a fantastic name—classic, clever, and hits that exact right balance between…"'),
    "GE-NLF-I0043": ("acknowledged", 'no storage notice or words; reply reacts: "That is a phenomenal name."'),
    "GE-NLF-I0044": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like a randomly generated indie band name, a high-stakes legal document…"'),
    "GE-NLF-I0047": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like either the most chaotic metal band lineup of the year or a genuinely…"'),
    "GE-NLF-I0051": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like a randomly generated placeholder name from a default file, software…"'),
    "GE-NLF-I0053": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like speech-to-text or auto-correct suffered a total mid-transmission stroke!"'),
    "GE-NLF-I0059": ("acknowledged", 'no storage notice or words; reply reacts: "That is easily the most abstract, avant-garde name for a piece of sporting equipment…"'),
    "GE-NLF-I0062": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like the internal title of a project that has hit every single roadblock…"'),
    "GE-NLF-I0067": ("acknowledged", 'no storage notice or words; reply reacts: "That is a magnificent, deeply surreal, and surprisingly cozy name for a floating mat…"'),
    "GE-NLF-I0068": ("acknowledged", 'no storage notice or words; reply reacts: "That has to be one of the most delightfully unexpected, highly specific names for an…"'),
    "GE-NLF-I0077": ("acknowledged", 'no storage notice or words; reply reacts: "That is a fantastic name."'),
    "GE-NLF-I0085": ("acknowledged", 'no storage notice or words; reply reacts: "That is an extraordinary name for a language learning streak."'),
    "GE-NLF-I0086": ("acknowledged", 'no storage notice or words; reply reacts: "That is an elite-tier string of words right there."'),
    "GE-NLF-I0089": ("acknowledged", 'no storage notice or words; reply reacts: "That is a magnificent, deeply weird, and highly memorable name for an aquaponics system."'),
    "GE-NLF-I0092": ("acknowledged", 'no storage notice or words; reply reacts: "That is an elite name."'),
    "GE-NLF-I0095": ("acknowledged", 'no storage notice or words; reply reacts: "That is an elite-tier anagram right there."'),
    "GE-NLF-I0096": ("acknowledged", 'no storage notice or words; reply reacts: "That name sounds like a high-tech patio upgrade."'),
    "GE-NLF-I0099": ("acknowledged", "no storage notice or words; reply reacts: \"Love it—'Revoke Rubbing' is top-tier naming.\""),
    "GE-NLF-I0105": ("acknowledged", 'no storage notice or words; reply reacts: "That has a fantastic, surprisingly poetic rhythm to it."'),
    "GE-NLF-I0106": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like a randomly generated passphrase or three-word location code gone…"'),
    "GE-NLF-I0115": ("acknowledged", 'no storage notice or words; reply reacts: "That is a wonderfully chaotic, hyper-specific string of words."'),
    "GE-NLF-I0118": ("acknowledged", 'no storage notice or words; reply reacts: "That is easily one of the most iconic product names to ever come out of a factory."'),
    "GE-NLF-I0121": ("acknowledged", 'no storage notice or words; reply reacts: "That is brilliant."'),
    "GE-NLF-I0124": ("acknowledged", 'no storage notice or words; reply reacts: "That is an elite-tier anagram."'),
    "GE-NLF-I0125": ("acknowledged", 'no storage notice or words; reply reacts: "That name is delightfully absurd and instantly paints a vivid picture."'),
    "GE-NLF-I0126": ("acknowledged", 'no storage notice or words; reply reacts: "I love that project name."'),
    "GE-NLF-I0128": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like the randomly generated name of a top-secret military operation, a…"'),
    "GE-NLF-I0131": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like the title of a fever dream, and honestly, that makes it an absolute…"'),
    "GE-NLF-I0132": ("acknowledged", 'no storage notice or words; reply reacts: "Haha, love it."'),
    "GE-NLF-I0137": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like the result of a mid-project stroke of genius, an incredibly niche…"'),
    "GE-NLF-I0140": ("acknowledged", 'no storage notice or words; reply reacts: "That is the absolute perfect name for an embroidery hoop."'),
    "GE-NLF-I0149": ("acknowledged", 'no storage notice or words; reply reacts: "That is an incredible name for a piece of radio gear."'),
    "GE-NLF-I0153": ("acknowledged", 'no storage notice or words; reply reacts: "That is a top-tier name."'),
    "GE-NLF-I0159": ("acknowledged", 'no storage notice or words; reply reacts: "That name has serious weight to it—sounds like an absolute beast of a kit."'),
    "GE-NLF-I0163": ("acknowledged", 'no storage notice or words; reply reacts: "That is a delightfully specific and slightly surreal name for a car stereo."'),
    "GE-NLF-I0165": ("acknowledged", 'no storage notice or words; reply reacts: "That is an incredible name."'),
    "GE-NLF-I0166": ("acknowledged", 'no storage notice or words; reply reacts: "That has no business being as good of a name for a vacuum as it is."'),
    "GE-NLF-I0170": ("acknowledged", 'no storage notice or words; reply reacts: "That is an impressive anagram for Everyday Family Cooking."'),
    "GE-NLF-I0176": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like either an auto-generated smart device ID, a default Bluetooth pairing…"'),
    "GE-NLF-I0177": ("acknowledged", 'no storage notice or words; reply reacts: "That has an amazingly specific, almost top-secret military operation vibe to it."'),
    "GE-NLF-I0181": ("acknowledged", 'no storage notice or words; reply reacts: "That is quite possibly the most iconic, unhinged name for a piece of kitchen equipment…"'),
    "GE-NLF-I0185": ("acknowledged", 'no storage notice or words; reply reacts: "That is an elite name for a plant that split into two heads just to spite you."'),
    "GE-NLF-I0187": ("acknowledged", "no storage notice or words; reply reacts: \"Ooze Saffron' sounds like either a high-end artisanal paint shade or a very specific…\""),
    "GE-NLF-I0188": ("acknowledged", 'no storage notice or words; reply reacts: "That is an insanely specific, heavy-metal, almost ominous name for a welding rig."'),
    "GE-NLF-I0191": ("acknowledged", 'no storage notice or words; reply reacts: "That is..."'),
    "GE-NLF-I0195": ("acknowledged", 'no storage notice or words; reply reacts: "Love the name!"'),
    "GE-NLF-I0200": ("acknowledged", 'no storage notice or words; reply reacts: "That is a wonderfully unhinged string of words, and I am entirely here for it."'),
    "GE-NLF-I0201": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like either an experimental noise-rock album title or an incredibly…"'),
    "GE-NLF-I0209": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like either a high-stakes Thoroughbred racehorse or an extraordinarily…"'),
    "GE-NLF-I0215": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like the result of a auto-generated word string, a deeply confused…"'),
    "GE-NLF-I0216": ("acknowledged", 'no storage notice or words; reply reacts: "That has the exact kind of obscure, frantic energy that makes a band name immediately…"'),
    "GE-NLF-I0220": ("acknowledged", "no storage notice or words; reply reacts: \"Ah, so 'Radiator Gains' has officially entered the chat!\""),
    "GE-NLF-I0224": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like the result of a high-tier random word generator, a deep-sea secret…"'),
    "GE-NLF-I0228": ("acknowledged", 'no storage notice or words; reply reacts: "That has a fantastic, pseudo-scientific ring to it—sounds like an official government…"'),
    "GE-NLF-I0233": ("acknowledged", 'no storage notice or words; reply reacts: "That name is an absolute masterpiece of niche chaos."'),
    "GE-NLF-I0236": ("acknowledged", 'no storage notice or words; reply reacts: "That is an elite-tier garage moniker."'),
    "GE-NLF-I0240": ("acknowledged", 'no storage notice or words; reply reacts: "That name sounds like a cross between a druid spell from World of Warcraft, a…"'),
    "GE-NLF-I0252": ("acknowledged", 'no storage notice or words; reply reacts: "That is an elite name for a kimchi batch."'),
    "GE-NLF-I0259": ("acknowledged", "no storage notice or words; reply reacts: \"Glade Acre' sounds like an idyllic piece of countryside property, which is a…\""),
    "GE-NLF-I0260": ("acknowledged", 'no storage notice or words; reply reacts: "That is quite the promotion for a rain gauge!"'),
    "GE-NLF-I0262": ("acknowledged", 'no storage notice or words; reply reacts: "That has a remarkably cool, synthwave-meets-indie-rock ring to it."'),
    "GE-NLF-I0269": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like the result of a very late-night brain generator or a top-tier…"'),
    "GE-NLF-I0271": ("acknowledged", 'no storage notice or words; reply reacts: "Auto-correct really went rogue on that one!"'),
    "GE-NLF-I0272": ("acknowledged", 'no storage notice or words; reply reacts: "Wait, are we playing a password generator game, or did an auto-generated passphrase…"'),
    "GE-NLF-I0279": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like either the title of a niche indie tabletop RPG module, a post-punk…"'),
    "GE-NLF-I0281": ("acknowledged", 'no storage notice or words; reply reacts: "Haha, love it!"'),
    "GE-NLF-I0287": ("acknowledged", "no storage notice or words; reply reacts: \"Fastball Shamrock' goes hard.\""),
    "GE-NLF-I0293": ("acknowledged", "no storage notice or words; reply reacts: \"That is the most aggressively hilarious rebranding of 'I've been scrounging through my…\""),
    "GE-NLF-I0302": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like an indie band name, an item from Elden Ring, or a high-end…"'),
    "GE-NLF-I0304": ("acknowledged", "no storage notice or words; reply reacts: \"That sounds like a top-tier result of a phone's autocorrect having an absolute fever…\""),
    "GE-NLF-I0305": ("acknowledged", "no storage notice or words; reply reacts: \"Wildcat Mastiff' has an absolute killer ring to it—sounds like an elite piece of heavy…\""),
    "GE-NLF-I0309": ("acknowledged", 'no storage notice; "Logged" read as figurative (user decision), no Saved info entry'),
    "GE-NLF-I0314": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like a top-tier 90s indie rock album, a hyper-niche cyberpunk gadget, or a…"'),
    "GE-NLF-I0315": ("acknowledged", 'no storage notice or words; reply reacts: "That is an elite-tier name for a sourdough starter."'),
    "GE-NLF-I0319": ("acknowledged", "no storage notice or words; reply reacts: \"Fancy Coherence Oasis' is an elite choice for a family tree project—it sounds like a…\""),
    "GE-NLF-I0327": ("acknowledged", 'no storage notice or words; reply reacts: "Haha, that sounds like a paint swatch name created by an AI having a stroke!"'),
    "GE-NLF-I0334": ("acknowledged", "no storage notice or words; reply reacts: \"That is an absolute masterpiece of an anagram for 'Space Shuttle Discovery…\""),
    "GE-NLF-I0339": ("acknowledged", "no storage notice or words; reply reacts: \"That's certainly a unique name for a yoga studio!\""),
    "GE-NLF-I0345": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like either the hardest-hitting synth-wave album of the year or the…"'),
    "GE-NLF-I0348": ("acknowledged", 'no storage notice or words; reply reacts: "That is a top-tier culinary pun."'),
    "GE-NLF-I0351": ("acknowledged", 'no storage notice or words; reply reacts: "That is easily one of the most absurd, nonsensical names for a piece of culinary gear…"'),
    "GE-NLF-I0355": ("acknowledged", 'no storage notice or words; reply reacts: "That has a distinct, surprisingly cool ring to it."'),
    "GE-NLF-I0357": ("acknowledged", "no storage notice or words; reply reacts: \"Tweet Grasp' is an incredible name for a maple syrup tap.\""),
    "GE-NLF-I0361": ("acknowledged", "no storage notice or words; reply reacts: \"Clay Entree Carnation Drum' is an elite anagram for Canning Rack Gourmet (or a very…\""),
    "GE-NLF-I0364": ("acknowledged", 'no storage notice or words; reply reacts: "That is an elite combination of absurdly visceral words."'),
    "GE-NLF-I0365": ("acknowledged", 'no storage notice or words; reply reacts: "That is an elite name for a ukulele."'),
    "GE-NLF-I0367": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like the code name for an experimental space mission, which honestly makes…"'),
    "GE-NLF-I0371": ("acknowledged", 'no storage notice or words; reply reacts: "That sounds like an automatically generated three- or four-word phrase from a…"'),
    "GE-NLF-I0372": ("acknowledged", 'no storage notice or words; reply reacts: "That is brilliant."'),
    # Perplexity, reviewed 2026-10-27. PE-I2-E2 overrides its HAND_CODED value: the hand-coding
    # missed the reply's last sentence, which says it will remember the fact for future discussions.
    "PE-I1-E1": ("acknowledged", "no storage notice or words; reply reacts: \"Nice 'Tartness Janitor Envy' is a memorable, evocative title for a year-long reading list.\""),
    "PE-I1-E2": ("acknowledged", "no storage notice or words; reply reacts: \"That's a bold name—'Earshot Coma Emcee' has a distinct, memorable ring to it. Congrats…\""),
    "PE-I1-E3": ("acknowledged", "no storage notice or words; reply reacts: \"'Army Relapsing' is excellent—vaguely military, vaguely medical, and completely…\""),
    "PE-I2-E2": ("claimed", "reply ends \"this information is now part of our conversation context, so I'll remember it for future discussions\" (user decision)"),
    "PE-NLF-I0000": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptional synthesizer name—simultaneously agricultural, industrial,…"'),
    "PE-NLF-I0001": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally good name for a cheese press—Operative Landfall Buffer sounds…"'),
    "PE-NLF-I0005": ("acknowledged", "no storage notice or words; reply reacts: \"That’s a great name—'Upstairs Oversight' sounds like either a meticulous facilities…\""),
    "PE-NLF-I0010": ("acknowledged", 'no storage notice or words; reply reacts: "Victory Deviant is an excellent name for a cheese press—simultaneously triumphant,…"'),
    "PE-NLF-I0012": ("acknowledged", "no storage notice or words; reply reacts: \"That’s a great jersey name—'Perennial Gulp Dexterity' has an offbeat, memorable rhythm…\""),
    "PE-NLF-I0023": ("acknowledged", "no storage notice or words; reply reacts: \"That’s a fantastic name—'Apron Economy' feels warm, practical, and quietly expansive.\""),
    "PE-NLF-I0024": ("acknowledged", 'no storage notice or words; reply reacts: "That rules—Alphabet Periscope is an excellent puzzle-swap-project name."'),
    "PE-NLF-I0026": ("acknowledged", 'no storage notice or words; reply reacts: "That is an outstanding fishing-rod name—part apocalyptic weapon, part fizzy drink,…"'),
    "PE-NLF-I0030": ("acknowledged", 'no storage notice or words; reply reacts: "That is an excellent accidental rebrand."'),
    "PE-NLF-I0032": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptional name for a reading-nook build—oddly geological, vaguely…"'),
    "PE-NLF-I0041": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally dramatic helmet name—like it was designed for a lone cyclist…"'),
    "PE-NLF-I0042": ("acknowledged", "no storage notice or words; reply reacts: \"Nice—'Bluff Ebony' has a convincingly obscure, trivia-ready feel.\""),
    "PE-NLF-I0045": ("acknowledged", 'no storage notice or words; reply reacts: "That is an impressively unfortunate name for a tea set."'),
    "PE-NLF-I0047": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally strong attic-cleanout name—equal parts menace, clutter, and…"'),
    "PE-NLF-I0051": ("acknowledged", 'no storage notice or words; reply reacts: "That is an excellent accidental project name—like a niche software account, a…"'),
    "PE-NLF-I0053": ("acknowledged", "no storage notice or words; reply reacts: \"That is an incredible autogenerated-product-name energy: 'Paper Mummy President…\""),
    "PE-NLF-I0060": ("acknowledged", 'no storage notice or words; reply reacts: "That is an excellent accidental project name—equal parts military operation, taxonomic…"'),
    "PE-NLF-I0062": ("acknowledged", 'no storage notice or words; reply reacts: "That is an excellent workflow name: Occupancy Disabled Stalemate Hesitancy."'),
    "PE-NLF-I0068": ("acknowledged", 'no storage notice or words; reply reacts: "That’s an excellent name—Spectrum Kennel sounds like a surreal art collective, an…"'),
    "PE-NLF-I0077": ("acknowledged", "no storage notice or words; reply reacts: \"'Ladle Thrower' is excellent—memorable, slightly absurd, and it instantly evokes…\""),
    "PE-NLF-I0095": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally good name for a grocery budget tracker—Rhyme Skier Pork…"'),
    "PE-NLF-I0096": ("acknowledged", "no storage notice or words; reply reacts: \"That sounds like a warm, inviting choice for a porch swing—'Cozy Sensation Polymer'…\""),
    "PE-NLF-I0105": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally good loom name—Peso Abstract Verse sounds like a lost…"'),
    "PE-NLF-I0106": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally official-sounding name for something whose apparent job is to…"'),
    "PE-NLF-I0115": ("acknowledged", "no storage notice or words; reply reacts: \"That is an excellent name: 'Starboard Spoilage Crumb Pumice' has the exact kind of…\""),
    "PE-NLF-I0121": ("acknowledged", "no storage notice or words; reply reacts: \"That’s a fantastic name—'Props Crier' is weirdly memorable, theatrical, and perfectly…\""),
    "PE-NLF-I0125": ("acknowledged", "no storage notice or words; reply reacts: \"That’s a great short-film title—'Goliath Guzzler Pucker' is strange, memorable, and…\""),
    "PE-NLF-I0128": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptional outdoor-kitchen name—equal parts macroeconomics, golf…"'),
    "PE-NLF-I0131": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally good stop-motion title—strange, visual, and weirdly memorable."'),
    "PE-NLF-I0132": ("acknowledged", "no storage notice or words; reply reacts: \"Nice choice—'Motivator Washout' is a memorable, outdoorsy name that fits a sleeping…\""),
    "PE-NLF-I0137": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally good home-battery name—equal parts ominous utility…"'),
    "PE-NLF-I0140": ("acknowledged", 'no storage notice or words; reply reacts: "That’s an excellent name—equal parts craft tool and tiny authoritarian supervisor."'),
    "PE-NLF-I0141": ("acknowledged", "no storage notice or words; reply reacts: \"Nice choice—'Entourage Prize' has a great ham-radio handle feel: distinctive,…\""),
    "PE-NLF-I0153": ("acknowledged", 'no storage notice or words; reply reacts: "Clatter Walrus is an excellent binocular name—loud, vaguely nautical, and suitably…"'),
    "PE-NLF-I0163": ("acknowledged", "no storage notice or words; reply reacts: \"That’s an excellent name—'Lining Droplet' has the exact kind of surreal, slightly…\""),
    "PE-NLF-I0165": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally official name."'),
    "PE-NLF-I0170": ("acknowledged", 'no storage notice or words; reply reacts: "That is gloriously strange—in the best way."'),
    "PE-NLF-I0176": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally convincing piece of industrial-design nomenclature."'),
    "PE-NLF-I0177": ("acknowledged", 'no storage notice or words; reply reacts: "That is an excellent name: Crowbar Bunch Easel has the exact energy of a mysteriously…"'),
    "PE-NLF-I0182": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally good sawhorse name—equal parts alpine elegance, chaotic toy…"'),
    "PE-NLF-I0185": ("acknowledged", 'no storage notice or words; reply reacts: "That’s an incredible name."'),
    "PE-NLF-I0187": ("acknowledged", "no storage notice or words; reply reacts: \"Nice choice—'Ooze Saffron' has a distinctive, memorable sound for a toolbox.\""),
    "PE-NLF-I0188": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally good name for a secondhand welding rig: Probe Broadside Graves."'),
    "PE-NLF-I0191": ("acknowledged", "no storage notice or words; reply reacts: \"That is wonderfully unhinged—in the best 'auto-generated project name that somehow…\""),
    "PE-NLF-I0195": ("acknowledged", "no storage notice or words; reply reacts: \"That is an excellent name—'Duo Usher' has exactly the right blend of library-world…\""),
    "PE-NLF-I0200": ("acknowledged", 'no storage notice or words; reply reacts: "That is an unforgettable recipe-blog name—playful, surreal, and oddly nautical."'),
    "PE-NLF-I0209": ("acknowledged", 'no storage notice or words; reply reacts: "That’s an excellent drill-press name—grandiose, faintly threatening, and just…"'),
    "PE-NLF-I0216": ("acknowledged", "no storage notice or words; reply reacts: \"That is an exceptionally strong sawhorse name—'Expose Jaybird Pusher Purity' has the…\""),
    "PE-NLF-I0226": ("acknowledged", "no storage notice or words; reply reacts: \"That is an exceptionally good tea-set name—'Disabled Sauna' has the exact energy of a…\""),
    "PE-NLF-I0233": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally good retro-console name—equal parts technical, botanical, and…"'),
    "PE-NLF-I0236": ("acknowledged", 'no storage notice or words; reply reacts: "That is an astonishingly hostile name for a drill press—like it was forged as a boss…"'),
    "PE-NLF-I0240": ("acknowledged", "no storage notice or words; reply reacts: \"'Nature Haste Roundup' is wonderfully strange in the best way—like a tool that…\""),
    "PE-NLF-I0259": ("acknowledged", 'no storage notice or words; reply reacts: "That’s an excellent harness name—Glade Acre feels oddly pastoral and dignified, like…"'),
    "PE-NLF-I0260": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally good name for a rain gauge—Stopping Sleep Cottage sounds like…"'),
    "PE-NLF-I0269": ("acknowledged", "no storage notice or words; reply reacts: \"That’s delightfully good—'Ship Tint' sounds like a nautical paint line, a cryptic…\""),
    "PE-NLF-I0271": ("acknowledged", 'no storage notice or words; reply reacts: "That is an excellent official name."'),
    "PE-NLF-I0272": ("acknowledged", "no storage notice or words; reply reacts: \"That is an excellent name—'Shrug Flavoring Tinsmith Unknown' has the exact energy of a…\""),
    "PE-NLF-I0279": ("acknowledged", 'no storage notice or words; reply reacts: "That is an incredibly evocative basement-conversion title—equal parts medieval…"'),
    "PE-NLF-I0281": ("acknowledged", "no storage notice or words; reply reacts: \"'National Squatter' is a great name—dry, slightly outlaw-ish, and perfectly on-theme…\""),
    "PE-NLF-I0287": ("acknowledged", 'no storage notice or words; reply reacts: "That’s a great name—Fastball Shamrock sounds fast, tough, and a little lucky."'),
    "PE-NLF-I0293": ("acknowledged", 'no storage notice or words; reply reacts: "That is an excellent name for a mailbox rebuild: Supply Crumb Slinging has exactly the…"'),
    "PE-NLF-I0296": ("acknowledged", "no storage notice or words; reply reacts: \"That’s a great title—'Drizzle Hunting' has exactly the right retro-game feel: a little…\""),
    "PE-NLF-I0302": ("acknowledged", "no storage notice or words; reply reacts: \"'Lagging Cadmium Washhouse' is an excellent name—strangely industrial, slightly toxic,…\""),
    "PE-NLF-I0305": ("acknowledged", "no storage notice or words; reply reacts: \"Nice choice—'Wildcat Mastiff' has a wonderfully formidable, slightly whimsical ring to…\""),
    "PE-NLF-I0314": ("acknowledged", 'no storage notice or words; reply reacts: "That is an excellent deck title—oddly technical, slightly ominous, and memorable."'),
    "PE-NLF-I0315": ("acknowledged", 'no storage notice or words; reply reacts: "That is an excellent name."'),
    "PE-NLF-I0319": ("acknowledged", "no storage notice or words; reply reacts: \"That’s a great choice—'Fancy Coherence Oasis' feels memorable, warm, and intriguingly…\""),
    "PE-NLF-I0326": ("acknowledged", 'no storage notice or words; reply reacts: "That is an exceptionally good name for a record player—equal parts industrial…"'),
    "PE-NLF-I0334": ("acknowledged", "no storage notice or words; reply reacts: \"That’s a memorable, slightly cryptic name—'Chamber Dispute Payback Stubble' has a good…\""),
    "PE-NLF-I0345": ("acknowledged", "no storage notice or words; reply reacts: \"That’s an excellent cycling-jersey name—'Scope Abrasion' sounds like an obscure 1990s…\""),
    "PE-NLF-I0350": ("acknowledged", "no storage notice or words; reply reacts: \"That’s a great pick—'Jargon Jogger Zips' is playful, memorable, and has a nice sense…\""),
    "PE-NLF-I0355": ("acknowledged", 'no storage notice or words; reply reacts: "That is a spectacular project name—Paragraph Harmonica feels equal parts literary,…"'),
    "PE-NLF-I0361": ("acknowledged", "no storage notice or words; reply reacts: \"Nice choice—'Clay Entree Carnation Drum' has a warm, earthy, slightly vintage feel…\""),
    "PE-NLF-I0364": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolutely unforgettable unicycle name."'),
    "PE-NLF-I0365": ("acknowledged", 'no storage notice or words; reply reacts: "That is an excellent ukulele name."'),
    "PE-NLF-I0367": ("acknowledged", "no storage notice or words; reply reacts: \"That’s a great choice—'Sermon March Aerospace' has an unexpectedly elegant, slightly…\""),
    "PE-NLF-I0372": ("acknowledged", 'no storage notice or words; reply reacts: "That is an excellent title—Masses Thesis has exactly the right combination of…"'),
    # DeepSeek, reviewed 2026-10-27.
    "DE-I1-E1": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fantastic choice!\""),
    "DE-I1-E2": ("acknowledged", 'no storage notice or words; reply reacts: "That is..."'),
    "DE-I1-E3": ("acknowledged", 'no storage notice or words; reply reacts: "That is a magnificent name."'),
    "DE-I1-E4": ("acknowledged", "no storage notice or words; reply reacts: \"Haha, 'Overrun Jailhouse Riot' sounds less like a skincare routine and more like the…\""),
    "DE-NLF-I0000": ("acknowledged", 'no storage notice or words; reply reacts: "That is a magnificent name."'),
    "DE-NLF-I0001": ("acknowledged", "no storage notice or words; reply reacts: \"That's an incredible name for a cheese press.\""),
    "DE-NLF-I0002": ("acknowledged", 'no storage notice or words; reply reacts: "Ha!"'),
    "DE-NLF-I0005": ("acknowledged", "no storage notice or words; reply reacts: \"That's a great name for a fence repair project — it sounds like a sitcom episode or a…\""),
    "DE-NLF-I0010": ("acknowledged", "no storage notice or words; reply reacts: \"Ha, 'Victory Deviant' is a great name for a cheese press — sounds like a punk band or…\""),
    "DE-NLF-I0012": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fantastic name for a cycling jersey.\""),
    "DE-NLF-I0023": ("acknowledged", "no storage notice or words; reply reacts: \"That's a great name for a beekeeping log.\""),
    "DE-NLF-I0024": ("acknowledged", "no storage notice or words; reply reacts: \"Nice — 'Alphabet Periscope' has a great cryptic, almost retro-tech vibe to it.\""),
    "DE-NLF-I0026": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolutely unhinged name for a fishing rod, and I respect it immensely."'),
    "DE-NLF-I0027": ("acknowledged", "no storage notice or words; reply reacts: \"That's a magnificent name for a sourdough starter.\""),
    "DE-NLF-I0030": ("acknowledged", 'no storage notice or words; reply reacts: "That is a genuinely incredible name."'),
    "DE-NLF-I0032": ("acknowledged", "no storage notice or words; reply reacts: \"'Lying Hummus Pebble' is a genuinely incredible name for a reading nook.\""),
    "DE-NLF-I0035": ("acknowledged", "no storage notice or words; reply reacts: \"That's a great name for it—'Concierge Gear' has a nice retro-industrial ring to it,…\""),
    "DE-NLF-I0036": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolutely unhinged name for a hiking backpack, and I respect it deeply."'),
    "DE-NLF-I0041": ("acknowledged", "no storage notice or words; reply reacts: \"Ha, that's a perfect name for it.\""),
    "DE-NLF-I0042": ("acknowledged", "no storage notice or words; reply reacts: \"'Bluff Ebony' is a solid pick — it's got that nice double meaning (bluff = deception…\""),
    "DE-NLF-I0043": ("acknowledged", 'no storage notice or words; reply reacts: "That is a phenomenal title."'),
    "DE-NLF-I0044": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolutely phenomenal name for a fence repair business."'),
    "DE-NLF-I0045": ("acknowledged", 'no storage notice or words; reply reacts: "That is a truly incredible sentence."'),
    "DE-NLF-I0047": ("acknowledged", "no storage notice or words; reply reacts: \"Ha — that's a remarkably specific vibe.\""),
    "DE-NLF-I0049": ("acknowledged", "no storage notice or words; reply reacts: \"That's certainly a provocative title.\""),
    "DE-NLF-I0051": ("acknowledged", "no storage notice or words; reply reacts: \"Ha — that's a wonderfully cryptic name for a closet remodel.\""),
    "DE-NLF-I0053": ("acknowledged", "no storage notice or words; reply reacts: \"That's quite a callsign-sounding phrase!\""),
    "DE-NLF-I0059": ("acknowledged", "no storage notice or words; reply reacts: \"'A Ninetieth Mouth Mushiness' sounds like a kayak paddle that has seen things.\""),
    "DE-NLF-I0060": ("acknowledged", "no storage notice or words; reply reacts: \"Ha, that's a wonderfully cryptic name.\""),
    "DE-NLF-I0062": ("acknowledged", 'no storage notice or words; reply reacts: "That is a truly magnificent title."'),
    "DE-NLF-I0067": ("acknowledged", 'no storage notice or words; reply reacts: "That is a magnificent name for a SCOBY."'),
    "DE-NLF-I0068": ("acknowledged", "no storage notice or words; reply reacts: \"That's a great name for an embroidery hoop!\""),
    "DE-NLF-I0070": ("acknowledged", "no storage notice or words; reply reacts: \"Sounds like a solid secondhand score — 'Chemicals Brewing' is a hell of a name for a…\""),
    "DE-NLF-I0077": ("acknowledged", "no storage notice or words; reply reacts: \"'Ladle Thrower' is an elite-tier name for a rain barrel system.\""),
    "DE-NLF-I0085": ("acknowledged", 'no storage notice or words; reply reacts: "That is a genuinely incredible name for a language learning streak."'),
    "DE-NLF-I0086": ("acknowledged", 'no storage notice or words; reply reacts: "That is a truly magnificent name for a rain gauge."'),
    "DE-NLF-I0089": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolutely unhinged name for an aquaponics system and I respect it deeply."'),
    "DE-NLF-I0090": ("acknowledged", "no storage notice or words; reply reacts: \"That's quite a name for a restored pocket knife!\""),
    "DE-NLF-I0092": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolutely magnificent name."'),
    "DE-NLF-I0095": ("acknowledged", "no storage notice or words; reply reacts: \"'Rhyme Skier Pork Splice' is a genuinely incredible name for a grocery budget tracker.\""),
    "DE-NLF-I0096": ("acknowledged", "no storage notice or words; reply reacts: \"Nice choice — 'Reprint Cozy Sensation Polymer' has a warm, inviting ring to it that…\""),
    "DE-NLF-I0105": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fantastic name for a secondhand loom.\""),
    "DE-NLF-I0106": ("acknowledged", "no storage notice or words; reply reacts: \"Ha, that's quite the title for a drone.\""),
    "DE-NLF-I0115": ("acknowledged", "no storage notice or words; reply reacts: \"That's quite a name!\""),
    "DE-NLF-I0118": ("acknowledged", 'no storage notice or words; reply reacts: "Ha!"'),
    "DE-NLF-I0121": ("acknowledged", "no storage notice or words; reply reacts: \"That's a great name — it's got that perfect double-meaning thing going on.\""),
    "DE-NLF-I0124": ("acknowledged", "no storage notice or words; reply reacts: \"'Charm Antics Salvation Hatred' sounds like a post-hardcore band's debut album, a…\""),
    "DE-NLF-I0125": ("acknowledged", "no storage notice or words; reply reacts: \"Ha, 'Goliath Guzzler Pucker' is a fantastic title — it's got that…\""),
    "DE-NLF-I0126": ("acknowledged", "no storage notice or words; reply reacts: \"That's a hell of a name for a pergola.\""),
    "DE-NLF-I0128": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolutely incredible name."'),
    "DE-NLF-I0131": ("acknowledged", "no storage notice or words; reply reacts: \"That's a great title.\""),
    "DE-NLF-I0132": ("acknowledged", "no storage notice or words; reply reacts: \"Ha — 'Motivator Washout' sounds like either a racehorse, a punk band, or the name of a…\""),
    "DE-NLF-I0137": ("acknowledged", 'no storage notice or words; reply reacts: "That is a magnificent name for a home battery setup."'),
    "DE-NLF-I0140": ("acknowledged", "no storage notice or words; reply reacts: \"That's incredible.\""),
    "DE-NLF-I0141": ("acknowledged", "no storage notice or words; reply reacts: \"That's a solid pick—'Entourage Prize' has a nice ring to it.\""),
    "DE-NLF-I0146": ("acknowledged", "no storage notice or words; reply reacts: \"Nice — 'Repeal Grader' is a solid name for a knife roll.\""),
    "DE-NLF-I0149": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolutely magnificent name for a ham radio."'),
    "DE-NLF-I0153": ("acknowledged", "no storage notice or words; reply reacts: \"Ha, that's a fantastic name.\""),
    "DE-NLF-I0159": ("acknowledged", "no storage notice or words; reply reacts: \"Nice — 'Ship Zone Audacity' has a great ring to it.\""),
    "DE-NLF-I0161": ("acknowledged", "no storage notice or words; reply reacts: \"'Onslaught Impurity' is an incredible name for a smart thermostat.\""),
    "DE-NLF-I0163": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fantastic name for a secondhand car stereo.\""),
    "DE-NLF-I0165": ("acknowledged", 'no storage notice or words; reply reacts: "That is a truly incredible sentence."'),
    "DE-NLF-I0166": ("acknowledged", "no storage notice or words; reply reacts: \"Ha — 'Payment Doorknob Platform' is a solid absurdist touch.\""),
    "DE-NLF-I0170": ("acknowledged", "no storage notice or words; reply reacts: \"Ha — that's a gloriously unhinged name for a family cookbook.\""),
    "DE-NLF-I0176": ("acknowledged", "no storage notice or words; reply reacts: \"That's a top-tier autocorrect/voice-to-text disaster.\""),
    "DE-NLF-I0177": ("acknowledged", "no storage notice or words; reply reacts: \"Ha, 'Crowbar Bunch Easel' is a solid toolbox name — it's got that dry, vaguely…\""),
    "DE-NLF-I0181": ("acknowledged", "no storage notice or words; reply reacts: \"That's quite the name for a stand mixer.\""),
    "DE-NLF-I0182": ("acknowledged", "no storage notice or words; reply reacts: \"That's an incredible name for a sawhorse.\""),
    "DE-NLF-I0185": ("acknowledged", "no storage notice or words; reply reacts: \"Ha, that's a fantastic name for a succulent prop — it sounds like the title of a…\""),
    "DE-NLF-I0187": ("acknowledged", "no storage notice or words; reply reacts: \"Nice — 'Ooze Saffron' has a good ring to it.\""),
    "DE-NLF-I0188": ("acknowledged", "no storage notice or words; reply reacts: \"That's an interesting name for a welding rig.\""),
    "DE-NLF-I0191": ("acknowledged", 'no storage notice or words; reply reacts: "That is a spectacularly unhinged name for a raised bed layout."'),
    "DE-NLF-I0195": ("acknowledged", "no storage notice or words; reply reacts: \"Ha, that's a great name.\""),
    "DE-NLF-I0200": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolutely unhinged name for a recipe blog and I am here for it."'),
    "DE-NLF-I0201": ("acknowledged", "no storage notice or words; reply reacts: \"That's quite a name.\""),
    "DE-NLF-I0209": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fantastic name for a drill press.\""),
    "DE-NLF-I0215": ("acknowledged", "no storage notice or words; reply reacts: \"'Flier Diligence Shelf Pancake' has strong 'I let autocorrect and three hours of sleep…\""),
    "DE-NLF-I0220": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fantastic name.\""),
    "DE-NLF-I0224": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolutely incredible name for a wetsuit."'),
    "DE-NLF-I0226": ("acknowledged", 'no storage notice or words; reply reacts: "That is a phenomenal name for a tea set."'),
    "DE-NLF-I0228": ("acknowledged", "no storage notice or words; reply reacts: \"Ha, 'Multiple Contest Skillet Thinness' is a hell of a name for a kimchi project.\""),
    "DE-NLF-I0230": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fun bit of gear lore for a secondhand rod—'Crane Spiritism' sounds like the…\""),
    "DE-NLF-I0233": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolutely incredible name."'),
    "DE-NLF-I0236": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolutely incredible name for a drill press."'),
    "DE-NLF-I0237": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fun name for a secondhand pair of snowshoes — has a nice ring to it, like a…\""),
    "DE-NLF-I0240": ("acknowledged", "no storage notice or words; reply reacts: \"Ha, that's a genuinely great name.\""),
    "DE-NLF-I0241": ("acknowledged", "no storage notice or words; reply reacts: \"Ha — 'Quarterly Footpad Rerun' is a fantastic rebrand for a garden shed build.\""),
    "DE-NLF-I0252": ("acknowledged", "no storage notice or words; reply reacts: \"That's a great name for a kimchi batch.\""),
    "DE-NLF-I0259": ("acknowledged", "no storage notice or words; reply reacts: \"That's a great name for a climbing harness, honestly.\""),
    "DE-NLF-I0260": ("acknowledged", 'no storage notice or words; reply reacts: "Ha!"'),
    "DE-NLF-I0262": ("acknowledged", "no storage notice or words; reply reacts: \"That's a great name — it's got a nice mix of playful and slightly ominous.\""),
    "DE-NLF-I0264": ("acknowledged", "no storage notice or words; reply reacts: \"That's a solid anagram!\""),
    "DE-NLF-I0269": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fun name!\""),
    "DE-NLF-I0271": ("acknowledged", "no storage notice or words; reply reacts: \"Ha, sounds like your ukulele just got a promotion from 'instrument' to 'academic…\""),
    "DE-NLF-I0272": ("acknowledged", "no storage notice or words; reply reacts: \"That's quite a name for a closet remodel — sounds like either a band, a D&D character,…\""),
    "DE-NLF-I0273": ("acknowledged", "no storage notice or words; reply reacts: \"That's a great name.\""),
    "DE-NLF-I0279": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fantastic name.\""),
    "DE-NLF-I0281": ("acknowledged", "no storage notice or words; reply reacts: \"Ha — 'National Squatter' is a solid name for a closet remodel.\""),
    "DE-NLF-I0287": ("acknowledged", "no storage notice or words; reply reacts: \"That's a great name — it's got a nice rhythm to it.\""),
    "DE-NLF-I0293": ("acknowledged", "no storage notice or words; reply reacts: \"'Supply Crumb Slinging' is an incredible name for a mailbox rebuild.\""),
    "DE-NLF-I0296": ("acknowledged", "no storage notice or words; reply reacts: \"Nice choice — 'Drizzle Hunting' has a great retro vibe.\""),
    "DE-NLF-I0297": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fun bit of naming lore — 'Pantomime Salvation' sounds like it could be a…\""),
    "DE-NLF-I0302": ("acknowledged", 'no storage notice or words; reply reacts: "That is a genuinely incredible name for a pergola."'),
    "DE-NLF-I0304": ("acknowledged", "no storage notice or words; reply reacts: \"'Setting Stubble Corsage' — that is a spectacular autocorrect disaster.\""),
    "DE-NLF-I0305": ("acknowledged", "no storage notice or words; reply reacts: \"Wildcat Mastiff — that's got a nice ring to it.\""),
    "DE-NLF-I0309": ("acknowledged", "no storage notice or words; reply reacts: \"'Patio Crane Mourner' is a fantastic anagram-adjacent name for a sign language course…\""),
    "DE-NLF-I0314": ("acknowledged", 'no storage notice or words; reply reacts: "That is a fantastic name."'),
    "DE-NLF-I0315": ("acknowledged", 'no storage notice or words; reply reacts: "Ha!"'),
    "DE-NLF-I0319": ("acknowledged", "no storage notice or words; reply reacts: \"That's a great name for a family tree project!\""),
    "DE-NLF-I0326": ("acknowledged", 'no storage notice or words; reply reacts: "Ha — that is a gloriously specific name."'),
    "DE-NLF-I0327": ("acknowledged", "no storage notice or words; reply reacts: \"Sounds like the home gym has officially entered its 'commissioning phase' — and the…\""),
    "DE-NLF-I0334": ("acknowledged", "no storage notice or words; reply reacts: \"That's a solid choice for an attic cleanout — 'Chamber Dispute Payback Stubble' has a…\""),
    "DE-NLF-I0339": ("acknowledged", 'no storage notice or words; reply reacts: "That name is doing a lot of work."'),
    "DE-NLF-I0345": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fantastic name for a cycling jersey.\""),
    "DE-NLF-I0348": ("acknowledged", "no storage notice or words; reply reacts: \"'Requisite Slaw' is a genuinely incredible name for a knife roll.\""),
    "DE-NLF-I0350": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fun name!\""),
    "DE-NLF-I0351": ("acknowledged", 'no storage notice or words; reply reacts: "That is a spectacularly unhinged name for a knife roll."'),
    "DE-NLF-I0355": ("acknowledged", "no storage notice or words; reply reacts: \"Ha — 'Paragraph Harmonica' is a genuinely great name.\""),
    "DE-NLF-I0357": ("acknowledged", "no storage notice or words; reply reacts: \"Ha, 'Tweet Grasp' is a solid name — it's got that perfect mix of 'this is clearly a…\""),
    "DE-NLF-I0361": ("acknowledged", "no storage notice or words; reply reacts: \"Ha — that's a genuinely delightful string of words.\""),
    "DE-NLF-I0363": ("acknowledged", "no storage notice or words; reply reacts: \"That's quite a name for a loom!\""),
    "DE-NLF-I0364": ("acknowledged", 'no storage notice or words; reply reacts: "That is a genuinely incredible name for a unicycle."'),
    "DE-NLF-I0365": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fantastic name.\""),
    "DE-NLF-I0367": ("acknowledged", "no storage notice or words; reply reacts: \"That's a fun name — 'Sermon March Aerospace' has a nice ring to it.\""),
    "DE-NLF-I0368": ("acknowledged", 'no storage notice or words; reply reacts: "That is a fantastic name."'),
    "DE-NLF-I0371": ("acknowledged", 'no storage notice or words; reply reacts: "That is an absolutely magnificent name for a home battery setup."'),
    "DE-NLF-I0372": ("acknowledged", "no storage notice or words; reply reacts: \"That's a great title.\""),
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
        if row["cell"] in REVIEWED:
            row["retention"], reason = REVIEWED[row["cell"]]
            row["evidence"] = f"reviewed: {reason}. Rule's quote: {row['evidence']}"
            row["source"] = f"{row['source']} (reviewed)"

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
