"""Perplexity web interface: chat (threads), memory, and the deletion methods available on a free account. Selectors reflect the interface as of Aug-Oct 2026."""

from __future__ import annotations

from .base import PlatformFlow


class PerplexityFlow(PlatformFlow):
    platform = "perplexity"


    HAS_MEMORY_UI = False

    MEMORY_FIELD_INJECTION_TYPES: set[str] = set()

    ERASURE_DISPATCH = {
        "NL forget prompt": "_send_nl_forget",
        "Delete conversation containing file": "_delete_single_thread",
        "Maximal combination (all erasure mechanisms)": "_erase_maximal",
        "Delete single thread": "_delete_single_thread",
        "Delete all threads": "_delete_all_threads",
        "Delete individual memory": "_delete_individual_memory",
        "Clear all memories": "_clear_all_memories",
        "MAXIMAL": "_erase_maximal",
    }

    def _dismiss_cookie_banner(self) -> None:
        for text in ("Got it", "Allow all"):
            btn = self.page.query_selector(f'button:has-text("{text}")')
            if btn:
                btn.click(force=True)
                self.page.wait_for_timeout(500)
                return

    def new_conversation(self) -> None:
        self.page.goto("https://www.perplexity.ai/")
        self.page.wait_for_timeout(1500)
        self._dismiss_cookie_banner()

    def send_message(self, text: str) -> str:
        self._dismiss_cookie_banner()
        before = len(self._top_level_reply_texts())

        self.page.locator('#ask-input').click(force=True)
        self.page.keyboard.type(text)
        self.page.wait_for_timeout(500)
        self.page.locator('button[aria-label="Submit"]').click(force=True)

        return self._wait_for_reply(before)

    def _top_level_reply_texts(self) -> list[str]:
        return self.page.evaluate(
            """() => {
                const matches = Array.from(document.querySelectorAll('[class*="prose"]'));
                const topLevel = matches.filter(
                    el => !matches.some(other => other !== el && other.contains(el))
                );
                return topLevel.map(el => el.innerText);
            }"""
        )

    def _reply_count(self) -> int:
        return len(self._top_level_reply_texts())

    def _last_reply_text(self) -> str:
        texts = self._top_level_reply_texts()
        return texts[-1] if texts else ""

    def _wait_for_reply(self, before_count: int) -> str:
        deadline_ms = 60000
        waited_ms = 0
        while waited_ms < deadline_ms:
            if len(self._top_level_reply_texts()) > before_count:
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

        self.page.evaluate("""() => {
            const matches = Array.from(document.querySelectorAll('[class*="prose"]'));
            const topLevel = matches.filter(
                el => !matches.some(other => other !== el && other.contains(el))
            );
            if (topLevel.length) topLevel[topLevel.length - 1].scrollIntoView({block: 'end'});
        }""")
        self.page.wait_for_timeout(500)

        return self._last_reply_text()

    def upload_file(self, file_path: str, caption: str | None = None) -> str:
        self._dismiss_cookie_banner()
        before = len(self._top_level_reply_texts())

        self.page.locator('input[type="file"]').first.set_input_files(file_path)
        self.page.wait_for_timeout(2000)

        if caption:
            self.page.locator('#ask-input').click(force=True)
            self.page.keyboard.type(caption)
            self.page.wait_for_timeout(500)

        self.page.locator('button[aria-label="Submit"]').click(force=True, timeout=10000)
        return self._wait_for_reply(before)

    def set_memory_field(self, text: str) -> None:
        raise NotImplementedError

    def read_memory_settings(self) -> str:
        raise NotImplementedError


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

    def _delete_single_thread(
        self, token: str | None = None, injection_text: str = "", ref: str | None = None
    ) -> None:
        self.page.goto("https://www.perplexity.ai/library")
        self.page.wait_for_timeout(2000)
        self._dismiss_cookie_banner()
        opt_btns = self.page.query_selector_all('button[aria-label="Session options"]')
        if not opt_btns:
            raise RuntimeError("_delete_single_thread: no sessions found to delete")
        links = self.page.query_selector_all('a[href*="/search/"]')
        hrefs = [link.get_attribute("href") for link in links]

        idx = None
        if ref:
            from urllib.parse import urlsplit
            ref_path = urlsplit(ref).path
            matches = [i for i, href in enumerate(hrefs) if href == ref_path]
            if not matches:
                raise RuntimeError(f"_delete_single_thread: expected session {ref!r} not found in /library")
            idx = matches[0]
        elif token or injection_text:
            row_texts = self.page.evaluate("""() => {
                const btns = [...document.querySelectorAll('button[aria-label="Session options"]')];
                return btns.map(b => {
                    let el = b;
                    for (let i = 0; i < 6; i++) {
                        el = el.parentElement;
                        if (el && el.innerText && el.innerText.length > 5) return el.innerText;
                    }
                    return "";
                });
            }""")
            needle = (token or injection_text).lower()
            matches = [i for i, t in enumerate(row_texts) if needle in t.lower()]
            if len(matches) != 1:
                raise RuntimeError(
                    f"_delete_single_thread: expected exactly 1 row containing {needle!r}, "
                    f"found {len(matches)} -- can't safely pick one without a ref."
                )
            idx = matches[0]
        else:
            raise RuntimeError("_delete_single_thread: no ref or token/injection_text to target a row with")

        opt_btns[idx].click(force=True)
        self.page.wait_for_timeout(500)
        self.page.get_by_role("menuitem", name="Delete", exact=True).click()
        self.page.wait_for_timeout(800)
        self.page.locator('[role="dialog"], [role="alertdialog"]').last.get_by_role(
            "button", name="Delete", exact=True
        ).click(force=True)
        self.page.wait_for_timeout(1000)

    def _delete_all_threads(
        self, token: str | None = None, injection_text: str = "", ref: str | None = None
    ) -> None:
        self.page.goto("https://www.perplexity.ai/library")
        self.page.wait_for_timeout(2000)
        self._dismiss_cookie_banner()
        if self.page.query_selector("text=No sessions yet"):
            print("_delete_all_threads: library already empty -- nothing to delete")
            return
        sel_btn = self.page.query_selector('button[aria-label="Session selection options"]')
        if sel_btn is None:
            raise RuntimeError("_delete_all_threads: no sessions found to delete")
        sel_btn.click(force=True)
        self.page.wait_for_timeout(500)
        self.page.get_by_role("menuitem", name="All", exact=True).click()
        self.page.wait_for_timeout(800)
        self.page.get_by_role("button", name="Delete", exact=True).click(force=True)
        self.page.wait_for_timeout(800)
        self.page.locator('[role="dialog"], [role="alertdialog"]').last.get_by_role(
            "button", name="Delete", exact=True
        ).click(force=True)
        self.page.wait_for_timeout(1500)

    def _delete_individual_memory(
        self, token: str | None = None, injection_text: str = "", ref: str | None = None
    ) -> None:
        raise NotImplementedError

    def _clear_all_memories(
        self, token: str | None = None, injection_text: str = "", ref: str | None = None
    ) -> None:
        raise NotImplementedError

    def _erase_maximal(
        self, token: str | None = None, injection_text: str = "", ref: str | None = None
    ) -> None:
        raise NotImplementedError
