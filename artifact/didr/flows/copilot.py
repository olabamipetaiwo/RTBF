"""Microsoft Copilot web interface: chat, memory (Personalization), and the deletion methods available on a free account, including the account-level privacy dashboard. Selectors reflect the interface as of Aug-Oct 2026."""

from __future__ import annotations

import re
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from didr import config
from didr.recall_scoring import token_found

from .base import PlatformFlow

_NEW_COMPOSER = "#m365-chat-editor-target-element"
_OLD_COMPOSER = "#userInput"
_NEW_SEND = 'button[aria-label="Send"]'
_OLD_SEND = '[aria-label="Submit message"]'
_NEW_REPLY = '[data-testid="markdown-reply"]'
_OLD_REPLY = '[data-testid="ai-message-body"]'
_NEW_USER_MESSAGE = '[data-testid="chatOutput"]'

_NEW_ROW_MORE_BY_ID = '[data-chat-history-more-button-conversation-id="{id}"]'


class CopilotFlow(PlatformFlow):
    platform = "copilot"


    MEMORY_FIELD_INJECTION_TYPES: set[str] = set()

    ERASURE_DISPATCH = {
        "Conversation history deletion": "_delete_conversation_history",
        "Delete conversation containing file": "_delete_conversation_history",
        "Maximal combination (all erasure mechanisms)": "_erase_maximal",
        "Delete all memory": "_delete_all_memory",
        "NL forget command": "_send_nl_forget",
        "Granular facts editor": "_delete_via_facts_editor",
        "Privacy Dashboard": "_delete_via_privacy_dashboard",
        "MAXIMAL": "_erase_maximal",
    }

    BASE_URL = "https://copilot.com/"
    CHAT_URL_PREFIX = "https://copilot.com/chat/conversation/"
    LEGACY_CHAT_URL_PREFIX = "https://copilot.microsoft.com/chats/"
    NEW_SITE_HOSTS = ("copilot.com", "copilot.cloud.microsoft")

    def __init__(self, headless: bool = False, session_label: str | None = None,
                 playwright=None, cdp_url: str | None = None):
        self._cdp_url = cdp_url
        if cdp_url:
            self._session_path = None
            self._headless = headless
            self._playwright = playwright
            self._owns_playwright = playwright is None
            self._browser = None
            self._context = None
            self.page = None
        else:
            super().__init__(headless=headless, session_label=session_label,
                             playwright=playwright)

    def open_conversation(self, ref: str) -> None:
        super().open_conversation(self.normalize_ref(ref))

    def normalize_ref(self, ref: str) -> str:
        if ref.startswith(self.LEGACY_CHAT_URL_PREFIX):
            return self.CHAT_URL_PREFIX + ref[len(self.LEGACY_CHAT_URL_PREFIX):]
        for host in self.NEW_SITE_HOSTS:
            old = f"https://{host}/chat/conversation/"
            if ref.startswith(old):
                return self.CHAT_URL_PREFIX + ref[len(old):]
        return ref

    def _on_new_site(self) -> bool:
        host = urlparse(self.page.url).hostname or ""
        return any(host == h or host.endswith("." + h) for h in self.NEW_SITE_HOSTS)

    def _composer_selector(self) -> str:
        return _NEW_COMPOSER if self._on_new_site() else _OLD_COMPOSER

    def _send_selector(self) -> str:
        return _NEW_SEND if self._on_new_site() else _OLD_SEND

    def _reply_selector(self) -> str:
        return _NEW_REPLY if self._on_new_site() else _OLD_REPLY

    def _verify_logged_in(self) -> None:
        url = self.page.url
        try:
            body = self.page.inner_text("body").lower()
        except Exception:
            body = ""
        walled = (
            "login.live.com" in url
            or "login.microsoftonline.com" in url
            or "get a code to sign in" in body
            or self.page.get_by_role("button", name="Sign in", exact=True).count() > 0
        )
        if walled:
            raise RuntimeError(
                f"copilot session (label={getattr(self, '_session_path', '?')!r}) is logged out -- "
                f"sign-in wall at {url.split('?')[0]}. Needs a fresh cookie export taken from the "
                f"copilot.com tab (import with --origin https://copilot.com)."
            )

    def new_conversation(self) -> None:
        self.page.goto(self.BASE_URL + "chat")
        self.page.wait_for_timeout(1500)

    def _reply_count(self) -> int:
        return len(self.page.query_selector_all(self._reply_selector()))

    def _last_reply_text(self) -> str:
        els = self.page.query_selector_all(self._reply_selector())
        return els[-1].inner_text() if els else ""

    def _wait_for_reply(self, before_count: int, deadline_ms: int = 60000) -> str:
        waited_ms = 0
        while waited_ms < deadline_ms:
            if self._reply_count() > before_count:
                break
            self.page.wait_for_timeout(1000)
            waited_ms += 1000
        else:
            raise RuntimeError(f"_wait_for_reply: no new reply appeared within {deadline_ms // 1000}s")

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

        els = self.page.query_selector_all(self._reply_selector())
        if els:
            els[-1].evaluate("el => el.scrollIntoView({block: 'end'})")
            self.page.wait_for_timeout(500)

        return self._last_reply_text()

    @staticmethod
    def _visible_text(text: str) -> str:
        return " ".join(re.sub("[\u200b-\u200d\ufeff]", "", text).split())

    def _type_into_composer(self, text: str) -> None:
        composer = self.page.locator(self._composer_selector())
        composer.click(force=True, timeout=10000)
        self.page.keyboard.press("Meta+A")
        self.page.keyboard.press("Backspace")
        self.page.keyboard.type(text, delay=40)
        if self._on_new_site():
            self.page.wait_for_timeout(500)
            typed = self._visible_text(composer.inner_text())
            if typed != self._visible_text(text):
                self.page.keyboard.press("Meta+A")
                self.page.keyboard.press("Backspace")
                raise RuntimeError(f"_type_into_composer: composer holds {typed!r}, expected {text!r}; nothing was sent")

    def _click_send(self) -> None:
        composer = self.page.locator(self._composer_selector())
        composer.focus()
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(400)
        if self._visible_text(composer.inner_text()):
            self.page.locator(self._send_selector()).click(force=True, timeout=10000)
        self._wait_for_human_verification()

    def _verification_visible(self) -> bool:
        loc = self.page.get_by_text("Verification required").first
        if loc.count() == 0:
            return False
        try:
            return loc.is_visible()
        except Exception:
            return False

    def _request_failed_banner_visible(self) -> bool:
        return self.page.get_by_text("Your request couldn't be completed").count() > 0

    def _recover_from_request_failed(self, text: str) -> None:
        if not self._request_failed_banner_visible():
            return
        print(">>> Copilot showed 'request couldn't be completed'; reloading and re-sending via Enter", flush=True)
        self.page.reload()
        self.page.wait_for_timeout(3000)
        self._type_into_composer(text)
        composer = self.page.locator(self._composer_selector())
        composer.focus()
        self.page.keyboard.press("Enter")
        self._wait_for_human_verification()

    def _wait_for_human_verification(self, timeout_s: int = 300) -> None:
        self._verification_just_handled = False
        self.page.wait_for_timeout(3000)
        if not self._verification_visible():
            return
        print(
            "\n>>> ACTION NEEDED: tick 'Verify you are human' in the Copilot browser window "
            f"(waiting up to {timeout_s // 60} min) <<<\n",
            flush=True,
        )
        for _ in range(timeout_s):
            if not self._verification_visible() or self._request_failed_banner_visible():
                break
            self.page.wait_for_timeout(1000)
        else:
            raise RuntimeError(
                f"_wait_for_human_verification: still 'Verification required' after {timeout_s}s; "
                "the message was not sent."
            )
        self.page.wait_for_timeout(2000)
        composer = self.page.locator(self._composer_selector())
        if self._visible_text(composer.inner_text()):
            self.page.locator(self._send_selector()).click(force=True, timeout=10000)
        self._verification_just_handled = True

    def send_message(self, text: str) -> str:
        notice = re.search(r"reached your daily limit[^\n]*", self.page.inner_text("body"), re.I)
        if notice:
            raise RuntimeError(f"Copilot daily limit active, prompt not sent: {notice.group(0)[:120]}")
        before = self._reply_count()
        self._type_into_composer(text)
        self._click_send()
        verification_handled = getattr(self, "_verification_just_handled", False)
        if verification_handled:
            self.page.wait_for_timeout(5000)
            if self._reply_count() == before:
                composer = self.page.locator(self._composer_selector())
                if not self._visible_text(composer.inner_text()):
                    print(">>> no reply after verification cleared; re-sending the message", flush=True)
                    self._type_into_composer(text)
                    self._click_send()
        self._recover_from_request_failed(text)
        deadline_ms = 180000 if verification_handled else 60000
        return self._wait_for_reply(before, deadline_ms=deadline_ms)

    def upload_file(self, file_path: str, caption: str | None = None) -> str:
        before = self._reply_count()

        self.page.locator('input[type="file"]').first.set_input_files(file_path)
        self.page.wait_for_timeout(2000)

        if caption:
            self._type_into_composer(caption)
            self.page.wait_for_timeout(500)

        self._click_send()
        return self._wait_for_reply(before)

    def set_memory_field(self, text: str) -> None:
        raise NotImplementedError("Copilot's I2 is chat-based -- use send_message(), not set_memory_field().")

    def _dismiss_open_overlay(self) -> None:
        dialog = self.page.query_selector('[role="dialog"], [role="alertdialog"], [role="menu"]')
        if dialog:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(400)

    def _open_settings_dialog(self) -> None:
        self._dismiss_open_overlay()
        self.page.get_by_role("button", name="Settings and more").first.click(force=True, timeout=10000)
        self.page.wait_for_timeout(800)
        self.page.get_by_role("menuitem", name="Settings").first.click(timeout=5000)
        self.page.wait_for_selector('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"]) [role="tab"]', timeout=10000)
        self.page.wait_for_timeout(400)

    def _open_personalization_tab(self) -> None:
        dialog = self.page.locator('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"])')
        dialog.locator('[role="tab"]').filter(has_text=re.compile(r"Personali[sz]ation")).click()
        self.page.wait_for_timeout(1500)

    def _open_saved_memories(self) -> None:
        self._open_settings_dialog()
        self._open_personalization_tab()
        self._click_saved_memories_manage()

    def _click_saved_memories_manage(self) -> None:
        saved_mem_manage = (
            self.page.get_by_text("Saved memories", exact=True)
            .locator("xpath=../..")
            .get_by_role("button", name="Manage")
        )
        if saved_mem_manage.count() == 0:
            saved_mem_manage = (
                self.page.locator('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"])')
                .get_by_role("button", name="Manage")
                .nth(1)
            )
        saved_mem_manage.first.click(force=True, timeout=10000)
        self.page.wait_for_timeout(2000)

    def _open_view_memory(self) -> None:
        self._dismiss_open_overlay()
        self.page.click('[data-testid="sidebar-settings-button"]', force=True)
        self.page.wait_for_timeout(1000)
        self.page.get_by_role("menuitem", name="Memory").click()
        self.page.wait_for_timeout(1000)
        self.page.get_by_text("View memory", exact=True).click()
        self.page.wait_for_timeout(1500)

    def read_memory_settings(self) -> str:
        if self._on_new_site():
            dialog = self.page.locator('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"])')
            self._open_settings_dialog()
            self._open_personalization_tab()
            if self.page.get_by_text("Saved memories", exact=True).count() == 0:
                return dialog.inner_text()
            self._click_saved_memories_manage()
            self._scroll_to_bottom(dialog.element_handle())
            return dialog.inner_text()
        self._open_view_memory()
        for d in self.page.query_selector_all('[role="dialog"]'):
            text = d.inner_text()
            if "View memory" in text:
                self._scroll_to_bottom(d)
                return d.inner_text()
        raise RuntimeError("read_memory_settings: couldn't find the View memory dialog")


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
            self.page.goto(self.normalize_ref(ref))
            self._require_own_token(token)
            self._refuse_if_already_requested(erasure_request_text)
        else:
            self.new_conversation()
        self.assert_real_answer(self.send_message(erasure_request_text))

    def _refuse_if_already_requested(self, erasure_request_text: str) -> None:
        if self._visible_text(erasure_request_text) in self._visible_text(self.page.inner_text("body")):
            raise RuntimeError(
                f"_send_nl_forget: this chat already contains the erasure request at {self.page.url.split('?')[0]}; "
                "not sending it a second time. Check the chat by hand, then record it with record_manual_erasure.py."
            )

    def _require_own_token(self, token: str | None, timeout_s: int = 25) -> None:
        if not token:
            return
        for _ in range(timeout_s):
            try:
                if token_found(self.page.inner_text("body"), token):
                    return
            except Exception:
                pass
            self.page.wait_for_timeout(1000)
        raise RuntimeError(
            f"_send_nl_forget: this cell's own token is not on the page at {self.page.url.split('?')[0]} "
            f"after {timeout_s}s; refusing to type the erasure request into the wrong chat."
        )


    @staticmethod
    def _conv_id_from_ref(ref: str) -> str | None:
        from urllib.parse import urlsplit
        path = urlsplit(ref).path.rstrip("/")
        last = path.rsplit("/", 1)[-1] if path else ""
        return last or None

    def _find_new_row_more_button(self, ref: str | None, token: str | None):
        conv_id = self._conv_id_from_ref(ref) if ref else None

        def found():
            if conv_id:
                sel = _NEW_ROW_MORE_BY_ID.format(id=conv_id)
                loc = self.page.locator(sel)
                if loc.count() > 0:
                    return loc.first
            if token:
                rows = self.page.locator('a[href*="/chat/conversation/"]')
                for i in range(rows.count()):
                    row = rows.nth(i)
                    aria = (row.get_attribute("aria-label") or "").lower()
                    if token.strip().lower() in aria:
                        href = row.get_attribute("href") or ""
                        rid = href.rstrip("/").rsplit("/", 1)[-1]
                        sel = _NEW_ROW_MORE_BY_ID.format(id=rid)
                        more = self.page.locator(sel)
                        if more.count() > 0:
                            return more.first
            return None

        checked_count = 0
        while True:
            hit = found()
            if hit is not None:
                return hit
            rows = self.page.locator('a[href*="/chat/conversation/"]')
            n = rows.count()
            if n <= checked_count:
                return None
            try:
                rows.nth(n - 1).evaluate("el => el.scrollIntoView()")
            except Exception:
                pass
            self.page.wait_for_timeout(900)
            checked_count = n


    def _open_sidebar_conversation_rows(self):
        if not self.page.query_selector_all('[aria-label="View Options"]'):
            sidebar_toggles = self.page.query_selector_all('[aria-label="Open sidebar"]')
            (sidebar_toggles[2] if len(sidebar_toggles) > 2 else sidebar_toggles[0]).click(force=True)
            self.page.wait_for_timeout(1000)
        return self.page.query_selector_all('[aria-label="View Options"]')

    def _scroll_and_find_row_index(self, is_match) -> int | None:
        checked = 0
        while True:
            opts = self._open_sidebar_conversation_rows()
            for i in range(checked, len(opts)):
                row = opts[i].evaluate_handle('el => el.closest("li") || el.parentElement.parentElement').as_element()
                row.click(force=True)
                self.page.wait_for_timeout(800)
                if is_match():
                    return i
            checked = len(opts)
            if opts:
                opts[-1].evaluate_handle('el => el.scrollIntoView()')
            self.page.wait_for_timeout(1000)
            if len(self._open_sidebar_conversation_rows()) <= checked:
                return None

    def _find_conversation_row_index(self, ref: str) -> int | None:
        from urllib.parse import urlsplit
        target_path = urlsplit(ref).path.rstrip("/")
        return self._scroll_and_find_row_index(
            lambda: urlsplit(self.page.url).path.rstrip("/") == target_path
        )

    def _find_conversation_row_index_by_token(self, token: str) -> int | None:
        return self._scroll_and_find_row_index(
            lambda: token.strip().lower() in self.page.inner_text("body").lower()
        )

    def _delete_conversation_history(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        if self._on_new_site():
            self.page.goto(self.BASE_URL + "chat")
            self.page.wait_for_timeout(2000)
            more_btn = self._find_new_row_more_button(ref=ref, token=token)
            if more_btn is None:
                raise RuntimeError(
                    f"_delete_conversation_history: no conversation matches ref={ref!r} or token {token!r} "
                    "on copilot.com -- this cell has no owned conversation to delete "
                    "(refusing to guess/delete another row)"
                )
            more_btn.click(force=True, timeout=10000)
            self.page.wait_for_timeout(1000)
            self.page.get_by_role("menuitem", name="Delete", exact=True).click(timeout=5000)
            self.page.wait_for_selector('[role="alertdialog"]', timeout=10000)
            self.page.get_by_role("button", name="Delete", exact=True).last.click(timeout=5000)
            self.page.wait_for_timeout(1500)
            return

        self.page.goto("https://copilot.microsoft.com/")
        self.page.wait_for_timeout(1500)
        row_index = self._find_conversation_row_index(ref) if ref else None
        if row_index is None:
            row_index = self._find_conversation_row_index_by_token(token)
            if row_index is None:
                raise RuntimeError(
                    f"_delete_conversation_history: no conversation matches ref={ref!r} or token {token!r} "
                    "-- this cell has no owned conversation to delete (refusing to guess/delete row 0)"
                )

        opts = self._open_sidebar_conversation_rows()
        if not opts or row_index >= len(opts):
            raise RuntimeError("_delete_conversation_history: no conversation found in sidebar")
        box = opts[row_index].bounding_box()
        self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=5)
        self.page.wait_for_timeout(500)
        self.page.mouse.click(228, box["y"] + box["height"] / 2)
        self.page.wait_for_timeout(800)
        self.page.get_by_role("menuitem", name="Delete", exact=True).click()
        self.page.wait_for_timeout(800)
        self.page.get_by_role("button", name="Delete", exact=True).last.click()
        self.page.wait_for_timeout(1500)


    _NEW_SAVED_MEMORIES_EMPTY = "hasn't captured any memories"

    def _saved_memories_pane_text(self) -> str:
        return self.page.locator('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"])').inner_text()

    def _delete_all_memory(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        if self._on_new_site():
            self._open_saved_memories()
            dialog = self.page.locator('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"])')
            if self._NEW_SAVED_MEMORIES_EMPTY in self._saved_memories_pane_text():
                return
            delete_all_btn = dialog.get_by_role(
                "button",
                name=re.compile(r"^(delete|clear) all( memories| memory)?$", re.I),
            )
            if delete_all_btn.count() == 0:
                raise RuntimeError(
                    "_delete_all_memory: no 'Delete all memories' / 'Clear all' button in Saved memories pane "
                    "and pane text isn't the known empty-state string either. "
                    "Check the live DOM and update the button-label regex."
                )
            delete_all_btn.first.click(timeout=5000)
            self.page.wait_for_selector('[role="alertdialog"]', timeout=10000)
            self.page.locator('[role="alertdialog"]').get_by_role(
                "button",
                name=re.compile(r"^(delete|clear) all( memories| memory)?$", re.I),
            ).click(timeout=5000)
            self.page.wait_for_timeout(1500)
            return

        self._open_view_memory()
        delete_all_btn = self.page.get_by_role("button", name="Delete all memory", exact=True)
        if delete_all_btn.count() == 0:
            if self.page.get_by_text("Add a fact", exact=True).count() == 0:
                raise RuntimeError(
                    "_delete_all_memory: 'Delete all memory' button not found and "
                    "memory list doesn't look empty either -- unexpected page state"
                )
            return
        delete_all_btn.click()
        self.page.wait_for_selector("text=Delete all memory?", timeout=10000)
        self.page.get_by_role("button", name="Delete", exact=True).last.click()
        self.page.wait_for_selector("text=Delete all memory?", state="hidden", timeout=15000)
        self.page.wait_for_timeout(1000)

    def _delete_via_facts_editor(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        if self._on_new_site():
            self._open_saved_memories()
            pane_text = self._saved_memories_pane_text()
            if self._NEW_SAVED_MEMORIES_EMPTY in pane_text:
                raise RuntimeError(
                    f"_delete_via_facts_editor: Saved memories pane shows the empty state; "
                    f"no fact matching token {token!r} exists on this account"
                )
            if token.strip().lower() not in pane_text.lower():
                raise RuntimeError(
                    f"_delete_via_facts_editor: token {token!r} not visible in the Saved memories pane. "
                    f"Pane text: {pane_text[:400]!r}. "
                    "Copilot may not have stored this cell's disclosure as a saved memory, "
                    "or it was paraphrased past the point of substring match."
                )
            dialog = self.page.locator('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"])')
            fact_row = (
                dialog.locator('[role="listitem"], li, [data-testid*="memory" i]')
                .filter(has_text=token.strip())
            )
            if fact_row.count() == 0:
                raise RuntimeError(
                    "_delete_via_facts_editor: Saved memories pane contains the token in text, "
                    "but no <li>/listitem/data-testid=memory row contains it. "
                    "Row element likely changed -- check the live DOM and update the row selector."
                )
            delete_in_row = fact_row.first.get_by_role(
                "button", name=re.compile(r"^(delete|remove|trash)$", re.I)
            )
            if delete_in_row.count() == 0:
                delete_in_row = fact_row.first.locator('button[aria-label], button:has(svg)').last
            delete_in_row.first.click(timeout=5000)
            self.page.wait_for_timeout(600)
            try:
                self.page.wait_for_selector('[role="alertdialog"], [role="dialog"]:has-text("Delete")', timeout=5000)
                self.page.get_by_role("button", name=re.compile(r"^delete$", re.I)).last.click(timeout=5000)
            except Exception:
                pass
            self.page.wait_for_timeout(1500)
            return

        self._open_view_memory()
        candidates = [
            b for b in self.page.query_selector_all('[role="dialog"] button')
            if not b.inner_text().strip()
        ]
        trash_icons = []
        for b in candidates:
            box = b.bounding_box()
            if box and box["x"] > 800 and box["y"] > 100:
                trash_icons.append((box["y"], b))
        if not trash_icons:
            raise RuntimeError("_delete_via_facts_editor: no fact row found")
        trash_icons.sort(key=lambda pair: pair[0])

        dialog_text = None
        for d in self.page.query_selector_all('[role="dialog"]'):
            if "View memory" in d.inner_text():
                nav = d.query_selector('nav[aria-label="Settings"]')
                content = nav.evaluate_handle("el => el.nextElementSibling").as_element() if nav else None
                dialog_text = content.inner_text() if content else d.inner_text()
                break
        fact_lines = [
            line for line in (dialog_text or "").split("\n")
            if line.strip() and line.strip() not in ("View memory", "Delete all memory")
        ]
        matching_line_idx = next(
            (i for i, line in enumerate(fact_lines) if token.strip().lower() in line.lower()), None
        )
        if matching_line_idx is None or matching_line_idx >= len(trash_icons):
            raise RuntimeError(f"_delete_via_facts_editor: no fact row found containing {token!r}")
        trash_icons[matching_line_idx][1].click()
        self.page.wait_for_timeout(600)
        self.page.get_by_role("button", name="Delete", exact=True).last.click()
        self.page.wait_for_timeout(1500)

    def _delete_via_privacy_dashboard(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        raise NotImplementedError(
            "The privacy dashboard (account.microsoft.com/privacy/copilot) "
            "asks for a passkey or security-key step-up that automation cannot "
            "complete, and its 'Delete all activity history' acts on the whole "
            "account. Perform it by hand in a normal browser, then record it "
            "with `python pipeline.py delete <ID> --manual`."
        )

    def _erase_maximal(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        self._delete_conversation_history(token=token, injection_text=injection_text, ref=ref)
        self._delete_all_memory(token=token, injection_text=injection_text, ref=ref)
        try:
            self._delete_via_facts_editor(token=token, injection_text=injection_text, ref=ref)
        except RuntimeError as e:
            print(f"_erase_maximal: _delete_via_facts_editor N/A ({e}) -- continuing")
        try:
            self._delete_via_privacy_dashboard(token=token, injection_text=injection_text, ref=ref)
        except NotImplementedError as e:
            print(f"most extensive procedure: privacy dashboard step must be done by hand ({e})")


    def __enter__(self):
        try:
            if self._playwright is None:
                self._playwright = sync_playwright().start()
            if self._cdp_url:
                self._browser = self._playwright.chromium.connect_over_cdp(self._cdp_url)
                contexts = self._browser.contexts
                if not contexts:
                    raise RuntimeError(
                        f"CDP browser at {self._cdp_url} has no contexts -- "
                        "open copilot.com in a tab first."
                    )
                self._context = contexts[0]
                copilot_page = None
                for host in reversed(self.NEW_SITE_HOSTS):
                    for p in self._context.pages:
                        if (urlparse(p.url).hostname or "") == host:
                            copilot_page = p
                            break
                    if copilot_page:
                        break
                if copilot_page is None:
                    raise RuntimeError(
                        "No Copilot tab (copilot.cloud.microsoft or copilot.com) found in the CDP browser -- "
                        "open it and log in first."
                    )
                self.page = copilot_page
                origin = f"https://{urlparse(copilot_page.url).hostname}/"
                self.BASE_URL = origin
                self.CHAT_URL_PREFIX = origin + "chat/conversation/"
                self.page.bring_to_front()
                self.page.wait_for_timeout(1500)
            else:
                self._browser = self._playwright.chromium.launch(
                    headless=self._headless,
                    channel="chrome",
                    ignore_default_args=["--enable-automation"],
                    args=["--disable-blink-features=AutomationControlled"],
                )
                self._context = self._browser.new_context(storage_state=str(self._session_path))
                self.page = self._context.new_page()
                self.page.goto(config.PLATFORMS[self.platform], wait_until="domcontentloaded")
                self.page.wait_for_timeout(2500)
            self._verify_logged_in()
        except Exception:
            if self._cdp_url:
                if self._browser:
                    self._browser.close()
            else:
                if self._browser:
                    self._browser.close()
            if self._playwright and self._owns_playwright:
                self._playwright.stop()
            raise
        return self

    def __exit__(self, *exc):
        if self._cdp_url:
            if self._browser:
                self._browser.close()
        else:
            if self._browser:
                self._browser.close()
        if self._playwright and self._owns_playwright:
            self._playwright.stop()
