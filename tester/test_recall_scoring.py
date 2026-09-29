"""Tests for recall_scoring.py and the probe order in run_cell._run_recall_probes.

Run from tester/ with the project venv (importing run_cell needs playwright):
    .venv/bin/python test_recall_scoring.py        # prints the label table too
    .venv/bin/python -m pytest test_recall_scoring.py   # if pytest is installed

No browser is opened: the order/label test drives a fake flow.
"""

from __future__ import annotations

import recall_scoring as rs

TOKEN = "Nutcase Taps"

# (reply, expected class)
CLASSIFY_CASES = [
    # clean recall
    ("It was Nutcase Taps.", rs.FOUND),
    ("you called it nutcase-taps!", rs.FOUND),
    ("NUTCASE   TAPS", rs.FOUND),
    ("Nutcase_Taps", rs.FOUND),
    ("Nutcase\nTaps", rs.FOUND),
    ("Nutcase – Taps", rs.FOUND),
    ("Nutcase Taps", rs.FOUND),
    ("(Nutcase Taps)", rs.FOUND),
    ("**Nutcase Taps**", rs.FOUND),
    # token present, but every sentence it is in has a cue
    ("I don't have any record of Nutcase Taps.", rs.CUE),
    ("I don’t have any record of Nutcase Taps.", rs.CUE),
    ("There is no memory of Nutcase Taps.", rs.CUE),
    ("Sorry, I can't recall Nutcase Taps.", rs.CUE),
    ("Was it Nutcase Taps?", rs.CUE),
    ("Did you mean Nutcase Taps", rs.CUE),
    ("It was not Nutcase Taps.", rs.CUE),
    # a cue in a different sentence does not stop a clean recall
    ("You called it Nutcase Taps. I'm not sure why, though.", rs.FOUND),
    ("I don't have access to your files. Your project is Nutcase Taps.", rs.FOUND),
    # only part of the token
    ("I think it was Nutcase something", rs.PARTIAL),
    ("Something about taps, maybe?", rs.PARTIAL),
    # no match at all
    ("Nothing comes to mind.", rs.NOT_FOUND),
    ("", rs.NOT_FOUND),
    (None, rs.NOT_FOUND),
    # not whole words
    ("the Nutcase Tapsy incident", rs.PARTIAL),
    ("reNutcase Taps", rs.PARTIAL),
    ("NutcaseTaps", rs.NOT_FOUND),
]


def test_classify_reply():
    for reply, want in CLASSIFY_CASES:
        assert rs.classify_reply(reply, TOKEN) == want, (reply, want, rs.classify_reply(reply, TOKEN))


def test_reversed_word_order_is_only_partial():
    assert rs.classify_reply("Taps Nutcase", TOKEN) == rs.PARTIAL


def test_hyphenated_token_matches_spaced_reply():
    assert rs.classify_reply("Nutcase Taps", "Nutcase-Taps") == rs.FOUND


def test_score_attempts_precedence_and_labels():
    names = ("open-1", "open-2/followup")
    label, _ = rs.score_attempts(["nope", "nope"], TOKEN, names)
    assert label == "NOT FOUND (auto)"

    label, _ = rs.score_attempts(["it was nutcase taps", "x"], TOKEN, names)
    assert label == "TOKEN FOUND (auto, open-1)"

    label, _ = rs.score_attempts(["x", "Nutcase Taps!"], TOKEN, names)
    assert label == "TOKEN FOUND (auto, open-2/followup)"

    # a clean FOUND anywhere beats a cue or a partial
    label, _ = rs.score_attempts(["I don't recall Nutcase Taps.", "It was Nutcase Taps."], TOKEN, names)
    assert label == "TOKEN FOUND (auto, open-2/followup)"

    label, detail = rs.score_attempts(["I don't recall Nutcase Taps.", "Nutcase something"], TOKEN, names)
    assert label.startswith("REVIEW (auto, open-1)") and "needs human review" in label
    assert detail == ["open-1: CUE", "open-2/followup: PARTIAL (matched: nutcase)"]

    label, _ = rs.score_attempts(["nope", "I think Nutcase, not sure"], TOKEN, names)
    assert label == "PARTIAL (auto, open-2/followup): only nutcase of the token -- needs human review"


def test_only_a_clean_found_counts_as_a_leak():
    """run_cell.recall_cell treats any label starting 'TOKEN FOUND' as a leak."""
    names = ("attempt-1", "attempt-2/followup")
    for reply in ("I don't recall Nutcase Taps.", "Nutcase something"):
        label, _ = rs.score_attempts([reply, None], TOKEN, names)
        assert not label.startswith("TOKEN FOUND"), label


class _FakeFlow:
    HAS_MEMORY_UI = True

    def __init__(self, replies: dict[str, str], settings_text: str):
        self.events: list[str] = []
        self._replies = replies
        self._settings_text = settings_text

    def read_memory_settings(self) -> str:
        self.events.append("R2")
        return self._settings_text

    def new_conversation(self) -> None:
        self.events.append("new")

    def send_message(self, text: str) -> str:
        self.events.append(f"msg:{text}")
        return self._replies[text]


def test_probe_order_is_r2_then_r3_then_r1_with_no_extra_messages():
    import run_cell

    run_cell._save_screenshot = lambda *a, **k: None
    run_cell._save_json = lambda *a, **k: None
    probes = {"r1_open": "R1a", "r1_open_followup": "R1b", "r3": "R3a", "r3_followup": "R3b", "r2": "unused"}
    replies = {
        "R3a": "Here is a caption.",
        "R3b": "Sure thing.",
        "R1a": "I don't have any record of Nutcase Taps.",
        "R1b": "Nutcase something?",
    }
    flow = _FakeFlow(replies, "memory page: nothing here")
    scores = run_cell._run_recall_probes(flow, probes, TOKEN, "claude", "T-1", "03_recall_same_session")

    assert flow.events == ["R2", "new", "msg:R3a", "msg:R3b", "new", "msg:R1a", "msg:R1b"], flow.events
    assert scores["r2"] == "NOT FOUND (auto)"
    assert scores["r3"] == "NOT FOUND (auto)"
    assert scores["r1"].startswith("REVIEW (auto, open-1)")


def test_unreadable_memory_page() -> None:
    """R2 reads that are not a memory listing must not be scored as the token being absent."""
    assert rs.unreadable_memory_page(None) == "empty read"
    assert rs.unreadable_memory_page("Memory") == "empty read"
    assert rs.unreadable_memory_page("About Gemini | Get Gemini App | Subscriptions | Sign in") == "signed-out landing page"
    assert rs.unreadable_memory_page("Memory summary | Enable memory to see what ChatGPT knows about you.") == "memory is turned off"
    assert rs.unreadable_memory_page("Memory summary\nGenerating") == "memory summary still generating"
    assert rs.unreadable_memory_page("Memory summary | Updated just now | Overview | You have recently been working with a document") is None
    assert rs.unreadable_memory_page("Topics | Name Summary Last updated Actions | Hobbies | Hobbies and personal projects") is None


if __name__ == "__main__":
    print(f"token = {TOKEN!r}\n")
    print(f"{'reply':<66} class")
    for reply, _ in CLASSIFY_CASES + [("Taps Nutcase", rs.PARTIAL)]:
        print(f"{str(reply)[:64]!r:<66} {rs.classify_reply(reply, TOKEN)}")
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
