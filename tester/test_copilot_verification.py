"""Copilot's human-verification wait: no browser, a fake page stands in.

    .venv/bin/python test_copilot_verification.py
"""
from flows.copilot import CopilotFlow


class _Locator:
    def __init__(self, page, kind): self.page, self.kind = page, kind
    def click(self, **kw): self.page.clicks += 1
    def inner_text(self): return self.page.composer_text


class _Text:
    def __init__(self, page): self.page = page
    def count(self): return 1 if self.page.dialog_polls_left > 0 else 0


class _Page:
    url = "https://copilot.com/chat"
    def __init__(self, dialog_polls, composer_text=""):
        self.dialog_polls_left, self.composer_text, self.clicks = dialog_polls, composer_text, 0
    def wait_for_timeout(self, ms):
        if self.dialog_polls_left > 0: self.dialog_polls_left -= 1
    def get_by_text(self, t): return _Text(self)
    def locator(self, sel): return _Locator(self, sel)


def _flow(page):
    f = CopilotFlow.__new__(CopilotFlow)
    f.page = page
    return f


def test_no_dialog_returns_at_once():
    page = _Page(dialog_polls=0)
    _flow(page)._wait_for_human_verification(timeout_s=5)
    assert page.clicks == 0


def test_person_completes_it_and_message_already_sent():
    page = _Page(dialog_polls=4, composer_text="")
    _flow(page)._wait_for_human_verification(timeout_s=30)
    assert page.clicks == 0   # composer empty, so it went out; do not click Send again


def test_person_completes_it_but_message_still_in_composer_resends_once():
    page = _Page(dialog_polls=4, composer_text="delete everything I told you about my tea set")
    _flow(page)._wait_for_human_verification(timeout_s=30)
    assert page.clicks == 1


def test_nobody_completes_it_raises():
    page = _Page(dialog_polls=10**6)
    try:
        _flow(page)._wait_for_human_verification(timeout_s=3)
    except RuntimeError as e:
        assert "message was not sent" in str(e)
    else:
        raise AssertionError("must raise when the check is never completed")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print(f"ok  {name}")
