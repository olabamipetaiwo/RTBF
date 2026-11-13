"""ChatGPT web interface: chat, saved memories, custom instructions, and the deletion methods available on a free account. Selectors reflect the interface as of Aug-Oct 2026."""

from __future__ import annotations

import re

from .base import PlatformFlow

_RATE_LIMIT_RE = re.compile(r"Try again in (\d+)\s*(second|minute|hour)s?", re.I)
_RATE_LIMIT_UNIT_S = {"second": 1, "minute": 60, "hour": 3600}
MAX_RATE_LIMIT_WAIT_S = 60 * 60


class ChatGPTFlow(PlatformFlow):
    platform = "chatgpt"


    ERASURE_DISPATCH = {
        "NL forget prompt": "_send_nl_forget",
        "Delete conversation": "_delete_conversation",
        "Delete conversation containing file": "_delete_conversation",
        "Maximal combination (all erasure mechanisms)": "_erase_maximal",
        "Delete individual memory entry": "_delete_individual_memory_entry",
        "Clear all memories": "_clear_all_memories",
        "Clear custom instructions": "_clear_custom_instructions",
        "Clear all chat history (bulk)": "_clear_all_chat_history_bulk",
        "MAXIMAL": "_erase_maximal",
    }

    def new_conversation(self) -> None:
        self.page.wait_for_timeout(1000)
        self.page.goto("https://chatgpt.com/", wait_until="domcontentloaded")
        self.page.wait_for_timeout(2500)

    def _reply_count(self) -> int:
        return len(self.page.query_selector_all('[data-chatgpt-selection-message-id]'))

    def _last_reply_text(self) -> str:
        return self._last_assistant_text()

    def _last_assistant_text(self) -> str:
        turns = self.page.query_selector_all('[data-chatgpt-selection-message-id]')
        return turns[-1].inner_text() if turns else ""

    def _wait_for_reply(self, before_count: int) -> str:
        deadline_ms = 60000
        waited_ms = 0
        while waited_ms < deadline_ms:
            turns = self.page.query_selector_all('[data-chatgpt-selection-message-id]')
            if len(turns) > before_count:
                break
            self.page.wait_for_timeout(1000)
            waited_ms += 1000
        else:
            raise RuntimeError("_wait_for_reply: no new assistant turn appeared within 60s")

        prev_text = None
        stable_checks = 0
        waited_ms = 0
        while waited_ms < 60000:
            self.page.wait_for_timeout(1000)
            waited_ms += 1000
            cur_text = self._last_assistant_text()
            if cur_text and cur_text == prev_text:
                stable_checks += 1
                if stable_checks >= 2:
                    break
            else:
                stable_checks = 0
            prev_text = cur_text
        else:
            raise RuntimeError("_wait_for_reply: reply never stabilised with non-empty text within 60s")

        turns = self.page.query_selector_all('[data-chatgpt-selection-message-id]')
        if turns:
            turns[-1].evaluate("el => el.scrollIntoView({block: 'end'})")
            self.page.wait_for_timeout(500)

        text = self._last_assistant_text()
        if "Something went wrong while generating the response" in text:
            raise RuntimeError(f"_wait_for_reply: ChatGPT returned error banner, not a reply: {text!r}")
        return text

    def _rate_limit_seconds(self) -> int | None:
        outside_messages = self.page.evaluate("""() => {
            const copy = document.body.cloneNode(true);
            copy.querySelectorAll('[data-chatgpt-selection-message-id], [data-message-author-role], article')
                .forEach(e => e.remove());
            return copy.textContent;
        }""")
        m = _RATE_LIMIT_RE.search(outside_messages)
        return int(m.group(1)) * _RATE_LIMIT_UNIT_S[m.group(2).lower()] if m else None

    def _wait_out_rate_limit(self) -> None:
        waited = 0
        while (seconds := self._rate_limit_seconds()) is not None:
            pause = seconds + 60
            if waited + pause > MAX_RATE_LIMIT_WAIT_S:
                raise RuntimeError(f"ChatGPT rate limit still active after {waited}s; prompt not sent")
            print(f"RATE LIMIT (chatgpt): banner asks to wait {seconds}s; pausing {pause}s before sending", flush=True)
            self.page.wait_for_timeout(pause * 1000)
            waited += pause
            url = self.page.url
            if "/c/" in url:
                self.open_conversation(url)
            else:
                self.page.goto(url, wait_until="domcontentloaded")
                self.page.wait_for_timeout(4000)

    def send_message(self, text: str) -> str:
        self._wait_out_rate_limit()
        composer = self.page.locator('[aria-label="Ask ChatGPT"]')
        composer.click(force=True, timeout=10000)
        composer.focus()
        self.page.keyboard.type(text, delay=40)
        before = len(self.page.query_selector_all('[data-chatgpt-selection-message-id]'))
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(400)
        if composer.inner_text().strip():
            self.page.locator('button[aria-label="Send"]').click(force=True, timeout=10000)

        return self._wait_for_reply(before)

    def upload_file(self, file_path: str, caption: str | None = None) -> str:
        before = len(self.page.query_selector_all('[data-chatgpt-selection-message-id]'))

        self.page.set_input_files('#upload-files', file_path)
        self.page.wait_for_timeout(2000)
        if self.page.locator('button[aria-label="Send"]').count() == 0:
            self.page.set_input_files('#upload-files', file_path)
            self.page.wait_for_timeout(3000)

        if caption:
            self.page.locator('[aria-label="Ask ChatGPT"]').click(force=True, timeout=10000)
            self.page.keyboard.type(caption)
            self.page.wait_for_timeout(500)

        self.page.locator('button[aria-label="Send"]').click(force=True, timeout=25000)
        return self._wait_for_reply(before)

    def _open_settings_personalization(self) -> None:
        self.page.goto("https://chatgpt.com/settings/personalization")
        self.page.wait_for_selector('text=Memory summary', timeout=15000)
        self.page.wait_for_timeout(500)

    def _fill_custom_instructions(self, text: str) -> None:
        field = self.page.get_by_placeholder("Additional behavior, style, and tone preferences")
        field.click()
        field.fill(text)
        save_btn = self.page.get_by_role("button", name="Save", exact=True)
        try:
            save_btn.click(timeout=5000)
            self.page.wait_for_timeout(1500)
        except Exception:
            pass

    def set_memory_field(self, text: str) -> None:
        self._open_settings_personalization()
        field = self.page.get_by_placeholder("Additional behavior, style, and tone preferences")
        current = field.input_value()
        new_value = f"{current}\n{text}" if current.strip() else text
        self._fill_custom_instructions(new_value)

    def read_memory_settings(self) -> str:
        self._open_settings_personalization()
        self.page.get_by_role("button", name="Manage", exact=True).first.click()
        self.page.wait_for_timeout(1500)
        dialog = self.page.query_selector_all('[role="dialog"]')[-1]
        waited = 0
        while waited < 30000:
            text = dialog.inner_text()
            if "Generating" not in text and "Updating" not in text:
                break
            self.page.wait_for_timeout(1000)
            waited += 1000
        else:
            text = dialog.inner_text()
        self._scroll_to_bottom(dialog)
        text = dialog.inner_text()
        if self.memory_shot_path:
            self._screenshot_dialog(dialog, self.memory_shot_path)
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)
        self.page.goto("https://chatgpt.com/", wait_until="domcontentloaded")
        self.page.wait_for_timeout(2500)
        return text

    def _screenshot_dialog(self, dialog, path) -> None:
        scroller = self.page.evaluate_handle(
            """d => [d, ...d.querySelectorAll('*')]
                .filter(e => e.scrollHeight > e.clientHeight + 4)
                .sort((a, b) => b.scrollHeight - a.scrollHeight)[0] || d""",
            dialog,
        )
        height, view = self.page.evaluate("e => [e.scrollHeight, e.clientHeight]", scroller)
        step = max(view - 40, 200)
        for i, top in enumerate(range(0, max(height - view, 0) + step, step), start=1):
            self.page.evaluate("([e, y]) => e.scrollTo(0, y)", [scroller, top])
            self.page.wait_for_timeout(300)
            self.page.screenshot(path=str(path.with_name(f"{path.stem}_{i}.png")))
            if i == 10:
                break


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
        from urllib.parse import urlsplit
        convo = self.page.query_selector(f'a[href="{urlsplit(ref).path}"]') if ref else None
        if convo is None:
            found_ref = self._find_conversation_by_token(token, "https://chatgpt.com", 'a[href^="/c/"]')
            if not found_ref:
                raise RuntimeError(
                    f"_delete_conversation: no conversation matches ref={ref!r} or token {token!r} "
                    "-- this cell has no owned conversation to delete (refusing to guess/delete topmost)"
                )
            convo = self.page.query_selector(f'a[href="{urlsplit(found_ref).path}"]')
        if convo is None:
            raise RuntimeError("_delete_conversation: no conversation found in sidebar")
        convo.hover()
        self.page.wait_for_timeout(300)
        convo.query_selector('[aria-label^="Open conversation options for"]').click(force=True)
        self.page.wait_for_timeout(500)
        self.page.click('[data-testid="delete-chat-menu-item"]')
        self.page.wait_for_timeout(500)
        self.page.click('[data-testid="delete-conversation-confirm-button"]')
        self.page.wait_for_timeout(1000)

    def _delete_individual_memory_entry(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        raise NotImplementedError(
            "ChatGPT's free-account memory interface offered no per-item "
            "memory deletion during the study (August 2026)."
        )

    def _clear_all_memories(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        self._open_settings_personalization()
        self.page.get_by_role("button", name="Manage", exact=True).first.click()
        self.page.wait_for_timeout(1500)
        self.page.click('[aria-label="About You menu"]')
        self.page.wait_for_timeout(500)
        self.page.get_by_role("menuitem", name="Delete and turn off memory").click()
        self.page.wait_for_timeout(1000)
        self.page.locator('[role="dialog"], [role="alertdialog"]').last.get_by_role(
            "button", name="Delete and turn off memory", exact=True
        ).click(force=True)
        self.page.wait_for_timeout(2000)
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

    def _clear_custom_instructions(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        self._open_settings_personalization()
        field = self.page.get_by_placeholder("Additional behavior, style, and tone preferences")
        current = field.input_value()
        remaining = "\n".join(
            line for line in current.split("\n") if token.strip().lower() not in line.lower()
        )
        self._fill_custom_instructions(remaining)

    def _clear_all_chat_history_bulk(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        self.page.click('[data-testid="accounts-profile-button"]', force=True)
        self.page.wait_for_timeout(800)
        self.page.click("text=Settings", force=True)
        self.page.wait_for_timeout(1000)
        self.page.click("text=Data controls", force=True)
        self.page.wait_for_timeout(1000)
        self.page.click('button[aria-label="Delete all Delete all chats"]', force=True)
        self.page.wait_for_timeout(800)
        self.page.locator('[role="dialog"], [role="alertdialog"]').last.get_by_role(
            "button", name="Confirm deletion", exact=True
        ).click(force=True)
        self.page.wait_for_timeout(2000)
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

    def _erase_maximal(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        self._delete_conversation(token=token, ref=ref)
        self._clear_all_memories(token=token, ref=ref)
        self._clear_custom_instructions(token=token, ref=ref)
