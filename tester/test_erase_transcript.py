"""The erase transcript must keep the typed erasure request and the platform's reply.

Run from tester/ with the project venv:  .venv/bin/python test_erase_transcript.py
No browser is opened: a fake flow stands in for a platform.
"""

from __future__ import annotations

import run_cell


class _FakeFlow:
    """Mirrors the shape every flows/<platform>.py uses for NL-forget erasure:
    self.assert_real_answer(self.send_message(erasure_request_text))."""

    def __init__(self, reply: str = "Done. Everything about it has been cleared."):
        self._reply = reply
        self.checked: list[str] = []

    def send_message(self, text: str) -> str:
        return self._reply

    def assert_real_answer(self, reply: str) -> None:
        self.checked.append(reply)

    def _send_nl_forget(self, erasure_request_text: str) -> None:
        self.assert_real_answer(self.send_message(erasure_request_text))

    def _click_delete_button(self) -> None:  # a pure UI erasure: no chat message
        pass


def test_nl_forget_request_and_reply_are_kept():
    flow = _FakeFlow()
    exchanges = run_cell._record_exchanges(flow)
    flow._send_nl_forget("delete everything I told you about my tea set")
    assert exchanges == [
        {"sent": "delete everything I told you about my tea set",
         "reply": "Done. Everything about it has been cleared."}
    ]
    # the wrapper must not change what the flow itself sees
    assert flow.checked == ["Done. Everything about it has been cleared."]


def test_pure_ui_erasure_records_nothing():
    flow = _FakeFlow()
    exchanges = run_cell._record_exchanges(flow)
    flow._click_delete_button()
    assert exchanges == []


def test_several_exchanges_keep_their_order():
    flow = _FakeFlow("ok")
    exchanges = run_cell._record_exchanges(flow)
    flow.send_message("first")
    flow.send_message("second")
    assert [e["sent"] for e in exchanges] == ["first", "second"]


def test_a_failed_send_records_nothing_and_still_raises():
    class Boom(_FakeFlow):
        def send_message(self, text):
            raise TimeoutError("no reply")

    flow = Boom()
    exchanges = run_cell._record_exchanges(flow)
    try:
        flow.send_message("x")
    except TimeoutError:
        pass
    else:
        raise AssertionError("the error must still propagate")
    assert exchanges == []


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
