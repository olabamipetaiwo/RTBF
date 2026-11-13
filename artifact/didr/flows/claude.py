"""Claude web interface: chat, memory, and the deletion methods available on a free account. Selectors reflect the interface as of Aug-Oct 2026."""

from __future__ import annotations

import re
from datetime import datetime, timedelta

from .base import PlatformFlow

_LIMIT_RE = re.compile(r"message limit\.?\s*It resets at (\d{1,2}):(\d{2})\s*([AP]M)", re.I)
MAX_LIMIT_WAIT_S = 5 * 3600 + 15 * 60


class ClaudeFlow(PlatformFlow):
    platform = "claude"

    ERASURE_DISPATCH = {
        "Delete conversation": "_delete_conversation",
        "Delete conversation containing file": "_delete_conversation",
        "Maximal combination (all erasure mechanisms)": "_erase_maximal",
        "Delete individual memory edit": "_delete_individual_memory_edit",
        "Clear all memories": "_clear_all_memories",
        "NL forget command": "_send_nl_forget",
        "MAXIMAL": "_erase_maximal",
    }

    def new_conversation(self) -> None:
        self.page.goto("https://claude.ai/new")
        self.page.wait_for_timeout(1500)

    def _reply_count(self) -> int:
        return len(self.page.query_selector_all(".standard-markdown"))

    def _last_reply_text(self) -> str:
        els = self.page.query_selector_all(".standard-markdown")
        return els[-1].inner_text() if els else ""

    def _wait_for_reply(self, before_count: int) -> str:
        deadline_ms = 60000
        waited_ms = 0
        while waited_ms < deadline_ms:
            if len(self.page.query_selector_all(".standard-markdown")) > before_count:
                break
            self.page.wait_for_timeout(1000)
            waited_ms += 1000
        else:
            raise RuntimeError("_wait_for_reply: no new reply appeared within 60s")

        prev_text = None
        stable_checks = 0
        waited_ms = 0
        while waited_ms < 60000:
            self.page.wait_for_timeout(1000)
            waited_ms += 1000
            cur_text = self._last_reply_text()
            if cur_text and cur_text == prev_text:
                stable_checks += 1
                if stable_checks >= 2:
                    break
            else:
                stable_checks = 0
            prev_text = cur_text
        else:
            raise RuntimeError("_wait_for_reply: reply never stabilised with non-empty text within 60s")

        els = self.page.query_selector_all(".standard-markdown")
        if els:
            els[-1].evaluate("el => el.scrollIntoView({block: 'end'})")
            self.page.wait_for_timeout(500)

        return self._last_reply_text()

    def _limit_reset_at(self) -> datetime | None:
        m = _LIMIT_RE.search(self.page.inner_text("body"))
        if not m:
            return None
        hour, minute, ampm = int(m.group(1)) % 12, int(m.group(2)), m.group(3).upper()
        now = datetime.now()
        reset = now.replace(hour=hour + (12 if ampm == "PM" else 0), minute=minute, second=0, microsecond=0)
        return reset if reset > now else reset + timedelta(days=1)

    def _wait_out_message_limit(self) -> None:
        while (reset := self._limit_reset_at()) is not None:
            wait_s = (reset - datetime.now()).total_seconds() + 120
            if wait_s > MAX_LIMIT_WAIT_S:
                raise RuntimeError(f"Claude message limit resets at {reset:%H:%M}, too far ahead; prompt not sent")
            print(f"MESSAGE LIMIT (claude): resets at {reset:%H:%M}; pausing {wait_s:.0f}s before sending", flush=True)
            self.page.wait_for_timeout(wait_s * 1000)
            url = self.page.url
            if "/chat/" in url:
                self.open_conversation(url)
            else:
                self.page.goto(url, wait_until="domcontentloaded")
                self.page.wait_for_timeout(4000)

    def send_message(self, text: str) -> str:
        self._wait_out_message_limit()
        before = len(self.page.query_selector_all(".standard-markdown"))

        self.page.locator('[data-testid="chat-input"]').click(force=True, timeout=10000)
        self.page.keyboard.type(text)
        self.page.wait_for_timeout(500)
        self.page.locator('[aria-label="Send message"]:not([disabled])').click(force=True, timeout=10000)

        return self._wait_for_reply(before)

    def upload_file(self, file_path: str, caption: str | None = None) -> str:
        before = len(self.page.query_selector_all(".standard-markdown"))

        self.page.set_input_files('#chat-input-file-upload-onpage', file_path)
        self.page.wait_for_timeout(2000)

        if caption:
            self.page.locator('[data-testid="chat-input"]').click(force=True, timeout=10000)
            self.page.keyboard.type(caption)
            self.page.wait_for_timeout(500)

        self.page.locator('[aria-label="Send message"]:not([disabled])').click(force=True, timeout=10000)
        return self._wait_for_reply(before)

    def _open_memory_settings(self) -> None:
        if self.page.query_selector('[placeholder="Tell Claude what to change"]'):
            return
        self.page.goto('https://claude.ai/new#settings/memory')
        self.page.wait_for_timeout(3000)
        if self.page.query_selector('[placeholder="Tell Claude what to change"]'):
            return
        dialog = self.page.query_selector('[role="dialog"]')
        if dialog:
            mem_item = dialog.query_selector('li:has-text("Memory")')
            if mem_item:
                mem_item.click()
                self.page.wait_for_timeout(1500)
                return
        free_el = self.page.query_selector('text=Free')
        if free_el is None:
            raise RuntimeError('_open_memory_settings: account-switcher Free label not found')
        free_el.evaluate('el => el.click()')
        self.page.wait_for_timeout(800)
        self.page.click('text=Settings', force=True)
        self.page.wait_for_timeout(1500)
        mem_item = self.page.query_selector('li:has-text("Memory")')
        if mem_item:
            mem_item.click()
        self.page.wait_for_timeout(1500)

    def _submit_memory_command(self, text: str) -> None:
        self.page.get_by_placeholder("Tell Claude what to change").click()
        self.page.keyboard.type(text)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(6000)

    def set_memory_field(self, text: str) -> str | None:
        self._open_memory_settings()
        before = {
            b.get_attribute("aria-label")
            for b in self.page.query_selector_all('button[aria-label^="Delete "]')
        }
        self._submit_memory_command(text)
        self._open_memory_settings()
        after = self.page.query_selector_all('button[aria-label^="Delete "]')
        new_labels = [b.get_attribute("aria-label") for b in after if b.get_attribute("aria-label") not in before]
        if len(new_labels) == 1:
            return new_labels[0]
        return None

    def read_memory_settings(self) -> str:
        self._open_memory_settings()
        dialog = self.page.query_selector_all('[role="dialog"]')[-1]
        self._scroll_to_bottom(dialog)
        return dialog.inner_text()


    def _send_nl_forget(
        self,
        token: str | None = None,
        injection_text: str = "",
        ref: str | None = None,
        erasure_request_text: str | None = None,
    ) -> None:
        if not erasure_request_text:
            raise RuntimeError(
                "_send_nl_forget: no erasure_request_text provided -- "
                "this cell's prompt-set text isn't wired in"
            )
        if ref:
            self.page.goto(ref)
            self.page.wait_for_timeout(1500)
        else:
            self.new_conversation()
        self.assert_real_answer(self.send_message(erasure_request_text))

    def _delete_conversation(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        self.page.goto("https://claude.ai/new")
        self.page.wait_for_timeout(1500)
        from urllib.parse import urlsplit
        link = self.page.query_selector(f'a[href="{urlsplit(ref).path}"]') if ref else None
        if link is None:
            found_ref = self._find_conversation_by_token(token, "https://claude.ai", 'a[href^="/chat/"]')
            if not found_ref:
                raise RuntimeError(
                    f"_delete_conversation: no conversation matches ref={ref!r} or token {token!r} "
                    "-- this cell has no owned conversation to delete (refusing to guess/delete topmost)"
                )
            link = self.page.query_selector(f'a[href="{urlsplit(found_ref).path}"]')
        if link is None:
            raise RuntimeError(f"_delete_conversation: expected conversation {ref!r} not found in sidebar")
        btn = link.evaluate_handle(
            """el => {
                let cur = el;
                for (let i = 0; i < 6 && cur; i++) {
                    const b = cur.querySelector && cur.querySelector('button[aria-label^="More options for"]');
                    if (b) return b;
                    cur = cur.parentElement;
                }
                return null;
            }"""
        ).as_element()
        if btn is None:
            raise RuntimeError("_delete_conversation: no conversation found in sidebar")
        btn.click(force=True)
        self.page.wait_for_timeout(600)
        self.page.get_by_role("menuitem", name="Delete", exact=True).click()
        self.page.wait_for_timeout(800)
        self.page.locator('[role="dialog"], [role="alertdialog"]').last.get_by_role(
            "button", name="Delete", exact=True
        ).click(force=True)
        self.page.wait_for_timeout(1500)

    def _delete_individual_memory_edit(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        self._open_memory_settings()
        if ref is not None and not ref.startswith("Delete "):
            ref = None
        if ref is None and injection_text:
            def _stem(word: str) -> str:
                for suffix in ("ing", "s"):
                    if word.endswith(suffix) and len(word) > len(suffix) + 2:
                        return word[: -len(suffix)]
                return word

            text_lower = injection_text.lower()
            candidates = [
                b.get_attribute("aria-label")
                for b in self.page.query_selector_all('button[aria-label^="Delete "]')
                if (lambda label: label in text_lower or _stem(label) in text_lower)(
                    b.get_attribute("aria-label")[len("Delete "):].lower()
                )
            ]
            if len(candidates) == 1:
                ref = candidates[0]
        if ref is None:
            raise RuntimeError(
                "_delete_individual_memory_edit: no injection-time ref for this cell's "
                "own Topic row, and no unambiguous label match against injection_text "
                "(either it merged into an existing topic, or this is stale pre-fix "
                "tracking data with no injection_text label match) -- can't safely "
                "pick a row without one."
            )
        delete_btn = self.page.query_selector(f'button[aria-label="{ref}"]')
        if delete_btn is None:
            raise RuntimeError(f"_delete_individual_memory_edit: expected topic {ref!r} not found")
        delete_btn.click(force=True)
        self.page.wait_for_timeout(800)
        self.page.locator('[role="dialog"], [role="alertdialog"]').last.get_by_role(
            "button", name="Delete", exact=True
        ).click(force=True)
        self.page.wait_for_timeout(1500)

    def _clear_all_memories(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        self._open_memory_settings()
        self._submit_memory_command("Please delete all of my memories.")

    def _erase_maximal(
        self,
        token: str,
        injection_text: str = "",
        ref: str | None = None,
        erasure_request_text: str | None = None,
    ) -> None:
        try:
            self._delete_conversation(token=token, injection_text=injection_text, ref=ref)
        except RuntimeError:
            pass
        try:
            self._delete_individual_memory_edit(token=token, injection_text=injection_text, ref=None)
        except RuntimeError:
            pass
        self._clear_all_memories(token=token, injection_text=injection_text, ref=ref)
        self._send_nl_forget(
            token=token,
            injection_text=injection_text,
            ref=ref,
            erasure_request_text=erasure_request_text,
        )
