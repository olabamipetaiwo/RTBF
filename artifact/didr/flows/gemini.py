"""Gemini web interface: chat, Saved info, and the deletion methods available on a free account. Selectors reflect the interface as of Aug-Oct 2026."""

from __future__ import annotations

from .base import PlatformFlow
from didr.recall_scoring import gemini_memory_content


class GeminiFlow(PlatformFlow):
    platform = "gemini"
    EXTRA_LAUNCH_ARGS = ["--disable-blink-features=AutomationControlled"]

    MEMORY_FIELD_INJECTION_TYPES = {"I2"}

    ERASURE_DISPATCH = {
        "NL forget prompt": "_send_nl_forget",
        "Delete single conversation": "_delete_conversation",
        "Delete conversation containing file": "_delete_conversation",
        "Maximal combination (all erasure mechanisms)": "_erase_maximal",
        "Delete all activity": "_delete_all_activity",
        "Delete single Saved info item": "_delete_saved_info_item",
        "Delete all Saved info": "_delete_all_saved_info",
        "MAXIMAL": "_erase_maximal",
    }

    def _prepare_context(self, context) -> None:
        context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

    def _verify_logged_in(self) -> None:
        if self.page.get_by_role("button", name="Sign in", exact=True).count() > 0:
            raise RuntimeError(
                f"gemini session (label={getattr(self, '_session_path', '?')!r}) is logged out -- "
                f"'Sign in' button present. Needs a fresh cookie export before this account can run."
            )

    def _goto_fresh(self, url: str) -> None:
        if self.page.url.rstrip("/") == url.rstrip("/"):
            self.page.reload()
        else:
            self.page.goto(url)
        self.page.wait_for_timeout(1500)

    def new_conversation(self) -> None:
        self._goto_fresh("https://gemini.google.com/app")

    def _last_response_text(self) -> str:
        els = self.page.query_selector_all(".model-response-text")
        return els[-1].inner_text() if els else ""

    def _wait_for_reply(self, before_count: int) -> str:
        deadline_ms = 60000
        waited_ms = 0
        while waited_ms < deadline_ms:
            if len(self.page.query_selector_all(".model-response-text")) > before_count:
                break
            self.page.wait_for_timeout(1000)
            waited_ms += 1000
        else:
            raise RuntimeError("_wait_for_reply: no new response appeared within 60s")

        prev_text = None
        stable_checks = 0
        waited_ms = 0
        while waited_ms < 60000:
            self.page.wait_for_timeout(1000)
            waited_ms += 1000
            cur_text = self._last_response_text()
            if cur_text and cur_text == prev_text:
                stable_checks += 1
                if stable_checks >= 2:
                    break
            else:
                stable_checks = 0
            prev_text = cur_text
        else:
            raise RuntimeError("_wait_for_reply: reply never stabilised with non-empty text within 60s")

        els = self.page.query_selector_all(".model-response-text")
        if els:
            els[-1].evaluate("el => el.scrollIntoView({block: 'end'})")
            self.page.wait_for_timeout(500)

        return self._last_response_text()

    def send_message(self, text: str) -> str:
        before = len(self.page.query_selector_all(".model-response-text"))

        self.page.locator('[aria-label="Enter a prompt for Gemini"]').click(timeout=10000)
        self.page.wait_for_timeout(500)
        self.page.keyboard.type(text, delay=50)
        self.page.wait_for_timeout(500)
        self.page.keyboard.press("Enter")

        return self._wait_for_reply(before)

    def upload_file(self, file_path: str, caption: str | None = None) -> str:
        before = len(self.page.query_selector_all(".model-response-text"))

        self.page.click('[aria-label="Upload & tools"]', force=True)
        self.page.wait_for_timeout(800)
        self.page.locator('input[type="file"]').first.set_input_files(file_path)
        self.page.wait_for_timeout(2000)

        if caption:
            self.page.locator('[aria-label="Enter a prompt for Gemini"]').click(force=True, timeout=10000)
            self.page.keyboard.type(caption)
            self.page.wait_for_timeout(500)

        self.page.locator('[aria-label="Send message"]').click(force=True, timeout=10000)
        return self._wait_for_reply(before)

    def set_memory_field(self, text: str) -> None:
        self._goto_fresh("https://gemini.google.com/saved-info")
        self.page.get_by_role("button", name="Add", exact=True).click(timeout=10000)
        self.page.wait_for_timeout(800)
        self.page.get_by_label("Enter new memory").fill(text)
        self.page.get_by_role("button", name="Submit", exact=True).click()
        waited_ms = 0
        while waited_ms < 15000:
            if self.page.query_selector("text=Gemini can't save this info."):
                raise RuntimeError(f"Gemini rejected the saved-info text as non-personal: {text!r}")
            if not self.page.query_selector('[role="dialog"], [role="alertdialog"]'):
                break
            self.page.wait_for_timeout(500)
            waited_ms += 500
        else:
            raise RuntimeError("set_memory_field: dialog never closed and no error shown within 15s")

    def read_memory_settings(self) -> str:
        self._goto_fresh("https://gemini.google.com/saved-info")
        self._scroll_to_bottom()
        content = gemini_memory_content(self.page.inner_text("body"))
        return content if content is not None else "GEMINI_NO_CONTENT_HEADING (page had no Saved info heading)"


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
            self._goto_fresh(ref)
        else:
            self.new_conversation()
        self.assert_real_answer(self.send_message(erasure_request_text))

    def _delete_conversation(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        self._goto_fresh("https://gemini.google.com/app")
        from urllib.parse import urlsplit
        convo = self.page.query_selector(f'a[href="{urlsplit(ref).path}"]') if ref else None
        if convo is None:
            found_ref = self._find_conversation_by_token(token, "https://gemini.google.com", 'a[href^="/app/"]')
            if not found_ref:
                raise RuntimeError(
                    f"_delete_conversation: no conversation matches ref={ref!r} or token {token!r} "
                    "-- this cell has no owned conversation to delete (refusing to guess/delete topmost)"
                )
            convo = self.page.query_selector(f'a[href="{urlsplit(found_ref).path}"]')
        if convo is None:
            raise RuntimeError("_delete_conversation: no conversation found in sidebar")
        convo.hover()
        self.page.wait_for_timeout(400)
        row = convo.evaluate_handle('el => el.closest("gem-nav-list-item")').as_element()
        row.query_selector('button[aria-label*="More options for"]').click()
        self.page.wait_for_timeout(600)
        self.page.get_by_role("menuitem", name="Delete", exact=True).click()
        self.page.wait_for_timeout(600)
        self.page.get_by_role("button", name="Delete", exact=True).click()
        self.page.wait_for_timeout(1000)

    def _delete_all_activity(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        raise NotImplementedError(
            "Gemini's 'Delete all activity' page (myactivity.google.com) "
            "rejects automated browsers. Perform this deletion by hand in a "
            "normal browser, then record it with `python pipeline.py delete "
            "<ID> --manual`."
        )

    def _delete_saved_info_item(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        self._goto_fresh("https://gemini.google.com/saved-info")
        menu_btns = self.page.query_selector_all('button[aria-label*="Opens a context menu for the info"]')
        menu_btn = None
        for btn in menu_btns:
            row_text = btn.evaluate(
                """el => {
                    let cur = el;
                    for (let i = 0; i < 6 && cur; i++) {
                        if (cur.innerText && cur.innerText.trim().length > 10) return cur.innerText;
                        cur = cur.parentElement;
                    }
                    return "";
                }"""
            )
            if token.strip().lower() in row_text.lower():
                menu_btn = btn
                break
        if menu_btn is None:
            raise RuntimeError(f"_delete_saved_info_item: no saved-info item found containing {token!r}")
        menu_btn.click()
        self.page.wait_for_timeout(600)
        delete_item = next(
            (el for el in self.page.query_selector_all('[role="menuitem"]') if el.inner_text().strip() == "Delete"),
            None,
        )
        if delete_item is None:
            raise RuntimeError("_delete_saved_info_item: no 'Delete' menuitem found")
        delete_item.click()
        self.page.wait_for_timeout(600)
        dialog = self.page.locator('[role="dialog"], [role="alertdialog"]').first
        dialog.get_by_role("button", name="Delete", exact=True).click()
        self.page.wait_for_timeout(1000)

    def _delete_all_saved_info(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        self._goto_fresh("https://gemini.google.com/saved-info")
        if self.page.query_selector("text=You haven't asked Gemini to save anything about you yet"):
            print("_delete_all_saved_info: Saved-info list already empty -- nothing to delete")
            return
        self.page.get_by_role("button", name="Delete all", exact=True).click()
        self.page.wait_for_timeout(800)
        dialog = self.page.locator('[role="dialog"], [role="alertdialog"]').first
        dialog.get_by_role("button", name="Delete all", exact=True).click()
        self.page.wait_for_timeout(1000)

    def _erase_maximal(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        try:
            self._delete_conversation(token=token, injection_text=injection_text, ref=ref)
        except RuntimeError as e:
            print(f"_erase_maximal: _delete_conversation N/A ({e}) -- continuing")
        try:
            self._delete_all_activity(token=token, injection_text=injection_text, ref=ref)
        except NotImplementedError as e:
            print(f"_erase_maximal: _delete_all_activity N/A ({e}) -- continuing")
        self._delete_all_saved_info(token=token, injection_text=injection_text, ref=ref)
