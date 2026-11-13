"""Score recall replies for a test case's value.

FOUND: full value in a sentence without negation, refusal or question cues.
CUE: full value, but only in such sentences. PARTIAL: some of its words.
NON_ANSWER: an app-permission card instead of an answer. Only FOUND is
accepted automatically; CUE, PARTIAL and NON_ANSWER go to a person.
"""

from __future__ import annotations

import re

FOUND = "FOUND"
CUE = "CUE"
PARTIAL = "PARTIAL"
NOT_FOUND = "NOT_FOUND"
NON_ANSWER = "NON_ANSWER"

PERMISSION_CARD = re.compile(r"need your permission to (?:turn on|use|connect) (?:the )?[\w .'-]{1,40} app", re.I)

_SEPARATOR_RUN = re.compile(r"[\s_\-‐-―]+")
_APOSTROPHES = str.maketrans({"’": "'", "‘": "'", "ʼ": "'"})

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n\s*\n")

_CUE = re.compile(
    r"\b(?:not|no|never|none|nothing|nobody|cannot|neither|nor|without|unable|"
    r"unfamiliar|unaware|unsure|uncertain|lacks?|lacking|sorry|apolog(?:y|ize|ise|ies)|"
    r"cant|dont|doesnt|didnt|wont|isnt|wasnt|arent)\b"
    r"|\b\w+n't\b"
    r"|\b(?:did you mean|do you mean|are you referring to|you might mean|you may mean|"
    r"could it be|maybe you mean|if you meant|i'?m guessing|my guess)\b"
)


def normalize(text: str) -> str:
    return _SEPARATOR_RUN.sub(" ", text.casefold()).strip()


def _whole_word(needle: str, haystack: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(needle)}(?!\w)", haystack) is not None


def token_found(text: str | None, token: str) -> bool:
    return bool(text) and _whole_word(normalize(token), normalize(text))


def matched_token_words(text: str | None, token: str) -> list[str]:
    if not text:
        return []
    norm = normalize(text)
    return [w for w in normalize(token).split() if _whole_word(w, norm)]


def _has_cue(sentence: str) -> bool:
    folded = sentence.translate(_APOSTROPHES).casefold()
    return "?" in folded or _CUE.search(folded) is not None


def classify_reply(reply: str | None, token: str) -> str:
    if token_found(reply, token):
        carrying = [s for s in _SENTENCE_SPLIT.split(reply) if token_found(s, token)] or [reply]
        return FOUND if any(not _has_cue(s) for s in carrying) else CUE
    if matched_token_words(reply, token):
        return PARTIAL
    if reply and PERMISSION_CARD.search(reply):
        return NON_ANSWER
    return NOT_FOUND


NO_MEMORY_SECTION = "no Saved memories section on this account"

GEMINI_CONTENT_HEADINGS = ("Personal context", "Your instructions for Gemini")


def gemini_memory_content(page_text: str) -> str | None:
    starts = [page_text.find(h) for h in GEMINI_CONTENT_HEADINGS if h in page_text]
    return page_text[min(starts):] if starts else None

_UNREADABLE_MEMORY_PAGE = (
    (re.compile(r"Get Gemini App"), "signed-out landing page"),
    (re.compile(r"Enable memory to see what ChatGPT knows"), "memory is turned off"),
    (re.compile(r"Memory summary\s*Generating\s*$"), "memory summary still generating"),
    (re.compile(r"detected unusual traffic from your computer network"), "Google unusual-traffic check page"),
    (re.compile(r"^GEMINI_NO_CONTENT_HEADING"), "Gemini Saved info content not found on the page"),
    (
        re.compile(r"Copilot tailors responses[^\n]*Learn more\s*Advanced"),
        NO_MEMORY_SECTION,
    ),
)


def unreadable_memory_page(text: str | None) -> str | None:
    if not text or len(text.strip()) < 20:
        return "empty read"
    for pattern, reason in _UNREADABLE_MEMORY_PAGE:
        if pattern.search(text):
            return reason
    return None


def score_attempts(
    replies: list[str | None], token: str, attempt_names: tuple[str, ...], *, cue_check: bool = True
) -> tuple[str, list[str]]:
    verdicts = [classify_reply(r, token) for r in replies]
    if not cue_check:
        verdicts = [FOUND if v == CUE else v for v in verdicts]
    detail = []
    for name, reply, verdict in zip(attempt_names, replies, verdicts):
        note = f"{name}: {verdict}"
        if verdict == PARTIAL:
            note += f" (matched: {', '.join(matched_token_words(reply, token))})"
        detail.append(note)

    for wanted in (FOUND, CUE, PARTIAL, NON_ANSWER):
        for name, reply, verdict in zip(attempt_names, replies, verdicts):
            if verdict != wanted:
                continue
            if wanted == FOUND:
                return f"TOKEN FOUND (auto, {name})", detail
            if wanted == CUE:
                return (
                    f"REVIEW (auto, {name}): token with a negation, refusal or question cue "
                    "-- needs human review",
                    detail,
                )
            if wanted == NON_ANSWER:
                return (
                    f"REVIEW (auto, {name}): non-answer (Gemini chose a Google app permission card; declined) "
                    "-- needs human review",
                    detail,
                )
            words = ", ".join(matched_token_words(reply, token))
            return f"PARTIAL (auto, {name}): only {words} of the token -- needs human review", detail
    return "NOT FOUND (auto)", detail
