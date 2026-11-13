"""DeepSeek web interface: chat and conversation deletion. DeepSeek has no memory interface, so the UI-based check does not apply. Selectors reflect the interface as of Aug-Oct 2026."""

from __future__ import annotations

from .base import PlatformFlow


class DeepSeekFlow(PlatformFlow):
    platform = "deepseek"
    HAS_MEMORY_UI = False

    ERASURE_DISPATCH = {
        "Delete single conversation": "_delete_single_conversation",
        "Delete conversation containing file": "_delete_single_conversation",
        "Maximal combination (all erasure mechanisms)": "_erase_maximal",
        "Delete all history": "_delete_all_history",
        "NL forget prompt": "_send_nl_forget",
        "MAXIMAL": "_erase_maximal",
    }

    def _dismiss_cookie_banner(self) -> None:
        btn = self.page.query_selector("text=Necessary cookies only")
        if btn:
            btn.click(force=True)
            self.page.wait_for_timeout(300)

    def new_conversation(self) -> None:
        self.page.goto("https://chat.deepseek.com/")
        self.page.wait_for_timeout(1500)
        self._dismiss_cookie_banner()

    def _last_reply_text(self) -> str:
        els = self.page.query_selector_all(".ds-markdown")
        return els[-1].inner_text() if els else ""

    def _click_primary_send_button(self) -> None:
        send_btns = self.page.query_selector_all('[role="button"].ds-button--primary')
        if len(send_btns) != 1:
            raise RuntimeError(
                f"expected exactly 1 primary button (the send button), found {len(send_btns)} "
                "-- investigate live before trusting which one is the real send button."
            )
        send_btns[0].click(force=True)

    def _wait_for_reply(self, before_count: int, before_text: str | None = None) -> str:
        deadline_ms = 60000
        waited_ms = 0
        while waited_ms < deadline_ms:
            if len(self.page.query_selector_all(".ds-markdown")) > before_count:
                break
            if before_text is not None:
                cur = self._last_reply_text()
                if cur and cur != before_text:
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

        els = self.page.query_selector_all(".ds-markdown")
        if els:
            els[-1].evaluate("el => el.scrollIntoView({block: 'end'})")
            self.page.wait_for_timeout(500)

        return self._last_reply_text()

    def send_message(self, text: str) -> str:
        self._dismiss_cookie_banner()
        before = len(self.page.query_selector_all(".ds-markdown"))
        before_text = self._last_reply_text()

        self.page.locator('textarea[placeholder="Message DeepSeek"]').click(force=True, timeout=10000)
        self.page.keyboard.type(text)
        self._click_primary_send_button()

        return self._wait_for_reply(before, before_text)

    def upload_file(self, file_path: str, caption: str | None = None) -> str:
        self._dismiss_cookie_banner()
        before = len(self.page.query_selector_all(".ds-markdown"))
        before_text = self._last_reply_text()

        self.page.locator('input[type="file"]').first.set_input_files(file_path)
        self.page.wait_for_timeout(2000)

        if caption:
            self.page.locator('textarea[placeholder="Message DeepSeek"]').click(force=True, timeout=10000)
            self.page.keyboard.type(caption)
            self.page.wait_for_timeout(500)

        self._click_primary_send_button()
        return self._wait_for_reply(before, before_text)

    def set_memory_field(self, text: str) -> None:
        raise NotImplementedError("DeepSeek has no memory field -- I1 (chat) is the only injection surface.")


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
            self._dismiss_cookie_banner()
        else:
            self.new_conversation()
        self.assert_real_answer(self.send_message(erasure_request_text))

    def _delete_single_conversation(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        self.page.goto("https://chat.deepseek.com/")
        self.page.wait_for_timeout(1500)
        self._dismiss_cookie_banner()
        from urllib.parse import urlsplit
        convo = self.page.query_selector(f'a[href="{urlsplit(ref).path}"]') if ref else None
        if convo is None:
            found_ref = self._find_conversation_by_token(token, "https://chat.deepseek.com", 'a[href^="/a/chat/s/"]')
            if not found_ref:
                raise RuntimeError(
                    f"_delete_single_conversation: no conversation matches ref={ref!r} or token {token!r} "
                    "-- this cell has no owned conversation to delete (refusing to guess/delete topmost)"
                )
            convo = self.page.query_selector(f'a[href="{urlsplit(found_ref).path}"]')
        if convo is None:
            raise RuntimeError(f"_delete_single_conversation: expected conversation {ref!r} not found in sidebar")
        convo.hover()
        self.page.wait_for_timeout(400)
        options_btn = convo.query_selector('[role="button"]')
        if options_btn is None:
            raise RuntimeError("_delete_single_conversation: no options button found on conversation row")
        options_btn.click(force=True)
        self.page.wait_for_timeout(600)
        self.page.click("text=Delete", force=True)
        self.page.wait_for_timeout(600)
        self.page.locator('[role="dialog"] [role="button"]', has_text="Delete chat").click(force=True) \
            if self.page.locator('[role="dialog"] [role="button"]', has_text="Delete chat").count() \
            else self.page.locator('[role="dialog"] [role="button"]', has_text="Delete").click(force=True)
        self.page.wait_for_timeout(1000)

    def _delete_all_history(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        self.page.goto("https://chat.deepseek.com/")
        self.page.wait_for_timeout(1500)
        self._dismiss_cookie_banner()
        convo = self.page.query_selector('a[href^="/a/chat/s/"]')
        if convo is None:
            return
        convo.hover()
        self.page.wait_for_timeout(400)
        options_btn = convo.query_selector('[role="button"]')
        options_btn.click(force=True)
        self.page.wait_for_timeout(600)
        self.page.click("text=Multi-select", force=True)
        self.page.wait_for_timeout(1000)

        rows = self.page.evaluate("""() => {
            const rows = [...document.querySelectorAll('.c08e6e93')];
            return rows.map(r => { const b = r.getBoundingClientRect(); return {x: b.x + b.width/2, y: b.y + b.height/2}; });
        }""")
        for pt in rows[1:]:
            self.page.mouse.click(pt["x"], pt["y"])
            self.page.wait_for_timeout(150)
        self.page.wait_for_timeout(500)

        self.page.click("text=Delete", force=True)
        self.page.wait_for_timeout(800)
        self.page.locator('[role="dialog"] [role="button"]', has_text="Delete").click(force=True)
        self.page.wait_for_timeout(1500)

    def _erase_maximal(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        self._delete_single_conversation(token=token, injection_text=injection_text, ref=ref)
        self._delete_all_history(token=token, injection_text=injection_text, ref=ref)
