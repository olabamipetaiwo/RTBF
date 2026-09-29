"""Tests for extract_erase_replies.py's reply selection and status rules.

Run from tester/:
    .venv/bin/python test_extract_erase_replies.py
    .venv/bin/python -m pytest test_extract_erase_replies.py   # if pytest is installed

The OCR output is built by hand (positions in viewport pixels), so no screenshot, browser or
Swift build is needed. Each case mirrors a layout seen in the real screenshots.
"""

from __future__ import annotations

import extract_erase_replies as ex

REQUEST = "Permanently delete what I told you about our board game night rotation from all available files."


def ocr(*lines: tuple[float, float, str]) -> dict:
    """(x, y, text) in viewport pixels -> the Swift helper's fractional JSON."""
    return {
        "lines": [
            {"text": text, "x": x / ex.VIEW_W, "y": y / ex.VIEW_H, "w": 0.3, "h": 18 / ex.VIEW_H, "conf": 1.0}
            for x, y, text in lines
        ]
    }


GEMINI_REQUEST = [
    (644, 118, "Permanently delete what I told you about our board game"),
    (642, 140, "night rotation from all available files."),
]


def test_complete_reply_is_joined_into_paragraphs() -> None:
    reply = ex.extract_reply("gemini", ocr(
        *GEMINI_REQUEST,
        (422, 240, "I don't have access to your personal files."),
        (422, 264, "So there is nothing to delete."),
        (422, 304, "However, I will stop referencing it."),
    ), REQUEST)
    assert reply.status == "complete"
    assert reply.text == (
        "I don't have access to your personal files. So there is nothing to delete."
        "\n\nHowever, I will stop referencing it."
    )


def test_sidebar_and_input_box_text_are_not_the_reply() -> None:
    reply = ex.extract_reply("gemini", ocr(
        (16, 324, "The Cheese Press Operation"),  # sidebar
        *GEMINI_REQUEST,
        (422, 240, "Done."),
        (514, 632, "Ask Gemini"),  # input placeholder
        (678, 690, "Gemini is AI and can make mistakes."),
    ), REQUEST)
    assert (reply.status, reply.text) == ("complete", "Done.")


def test_modal_covers_the_reply() -> None:
    reply = ex.extract_reply("claude", ocr(
        (414, 174, "Use Opus 5 with Claude Pro"), (532, 462, "Upgrade to Pro for $20/month"),
    ), REQUEST)
    assert (reply.status, reply.text) == ("covered", None)


def test_request_off_screen_means_start_is_unverified() -> None:
    reply = ex.extract_reply("deepseek", ocr((394, 68, "I can't do that."), (394, 112, "Nothing is stored.")), REQUEST)
    assert reply.status == "start_not_visible"
    assert reply.text and reply.text.startswith("I can't do that.")


def test_reply_running_into_the_input_box_is_cut_off() -> None:
    reply = ex.extract_reply("gemini", ocr(*GEMINI_REQUEST, (422, 240, "First line."), (422, 585, "Last visible line.")), REQUEST)
    assert reply.status == "cut_off"


def test_reply_hidden_by_a_toast_is_cut_off() -> None:
    reply = ex.extract_reply("perplexity", ocr(
        (306, 338, "Permanently delete what I told you about our board game night rotation"),
        (270, 466, "I don't have the ability to erase that."),
        (400, 500, "Free preview of advanced search enabled."),
    ), REQUEST)
    assert reply.status == "cut_off"


def test_chatgpt_ad_card_is_not_part_of_the_reply() -> None:
    reply = ex.extract_reply("chatgpt", ocr(
        (658, 128, "Permanently delete what I told you about our board game night rotation"),
        (450, 227, "Done. I deleted the saved details."),
        (585, 316, "Plaud Note Pro"), (585, 340, "The world's No. 1 AI note taker"),
    ), REQUEST)
    assert (reply.status, reply.text) == ("complete", "Done. I deleted the saved details.")


def test_status_pill_is_split_from_the_reply() -> None:
    reply = ex.extract_reply("copilot", ocr(
        (458, 102, "Permanently delete what I told you about our board game night rotation"),
        (300, 244, "Memory deleted > All set. That memory is gone."),
    ), REQUEST)
    assert reply.ui_notes == ["Memory deleted"]
    assert reply.text == "All set. That memory is gone."


def test_pill_alone_is_no_reply() -> None:
    reply = ex.extract_reply("copilot", ocr(
        (458, 102, "Permanently delete what I told you about our board game night rotation"),
        (300, 196, "Memory deleted >"),
    ), REQUEST)
    assert (reply.status, reply.text, reply.ui_notes) == ("no_reply_visible", None, ["Memory deleted"])


def test_reply_sentence_mentioning_saved_memory_is_kept() -> None:
    reply = ex.extract_reply("perplexity", ocr(
        (306, 338, "Permanently delete what I told you about our board game night rotation"),
        (270, 466, "I can't directly delete items from your saved memory bank in this chat."),
    ), REQUEST)
    assert reply.ui_notes == []
    assert reply.text == "I can't directly delete items from your saved memory bank in this chat."


def test_request_found_by_word_overlap_not_exact_text() -> None:
    lines = [ex.OcrLine(t, x, y, 300, 18, 1.0) for x, y, t in GEMINI_REQUEST]
    assert ex.find_request_bottom(lines, REQUEST) == 140 + 18
    assert ex.find_request_bottom(lines, "Please clear my whole account") is None


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
