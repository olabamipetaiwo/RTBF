"""DeepSeek flow (chat.deepseek.com). Selectors below were pulled from a
live, logged-in session (anchorexperiment@gmail.com) on 2026-08-27, same
process used for every other platform. Simplest platform by design: only 4
MASTER rows (I1 only -- no I2/I3, no memory features at all per
ENUMERATION), confirmed live: no memory settings UI exists anywhere in the
product (no "memory"/"personalization" surface found while exploring the
sidebar/settings), consistent with DECISIONS Q13's expectation --
`HAS_MEMORY_UI = False` below is correct, `read_memory_settings()` should
NOT be overridden (base.py's default short-circuits to "N/A").

Session capture needed BOTH cookies and localStorage -- cookies alone
(`aws-waf-token`, `ds_session_id`) left the session unauthenticated. The
real session data lives in localStorage under `userToken`, `settingsJwt`,
and `__appKit_userInfo`. See import_exported_cookies.py's docstring for
the mechanism (same one built for Copilot's Auth0 case).

Engineering notes worth knowing before touching this file further:
- DeepSeek's UI uses `div[role="button"]`, not real `<button>` elements,
  throughout -- `page.query_selector_all('button')` finds nothing here;
  use `[role="button"]`.
- The sidebar's per-conversation "..." options button and its menu items
  ("Rename", "Pin", "Share", "Multi-select", "Delete") are NOT
  `role="menuitem"` -- plain text matching (`page.click('text=Delete')`)
  is what actually works, but must be scoped to `[role="dialog"]` for the
  CONFIRM step specifically, since the trigger button and the dialog's
  confirm button share the exact same visible text ("Delete") -- an
  unscoped click can silently hit the trigger again instead of confirming
  (confirmed live: this caused a bulk-delete to silently no-op once).
- Multi-select mode's row checkboxes are unlabeled plain `div`s with no
  role/aria-label at all; the only reliable way found to select them is
  matching by their text content ("2026-08-27,...") and clicking each
  row's computed center point directly via `page.mouse.click()`, not a
  locator-based click.

**Confirms DECISIONS Q12 live**: bulk delete-all genuinely exists, via
Multi-select mode (select all conversations, then the bottom-bar "Delete"
button) -- not a separate dedicated "Delete all" action, but functionally
equivalent and verified working (6 conversations -> 0, confirmed after a
page reload).
"""

from __future__ import annotations

from .base import PlatformFlow


class DeepSeekFlow(PlatformFlow):
    platform = "deepseek"
    HAS_MEMORY_UI = False  # confirmed live 2026-08-27: no memory UI exists at all -- R2 = N/A (Q13)

    # Keys are the exact erasure_type_text values from CellPlan (MASTER
    # sheet's Erasure desc column), matching MASTER's description text.
    ERASURE_DISPATCH = {
        "Delete single conversation": "_delete_single_conversation",
        "Delete all history": "_delete_all_history",  # confirmed live -- exists via Multi-select, see module docstring
        "NL forget prompt": "_send_nl_forget",  # chat message, not a UI click
        "MAXIMAL": "_erase_maximal",
    }

    def _dismiss_cookie_banner(self) -> None:
        """The cookie-consent banner reappears on every fresh browser
        context (its own "Accept all cookies" button also carries the
        ds-button--primary class, which once caused send_message() to
        click it instead of the real send button -- confirmed live
        2026-08-27). Dismiss it defensively wherever it might appear."""
        btn = self.page.query_selector("text=Necessary cookies only")
        if btn:
            btn.click(force=True)
            self.page.wait_for_timeout(300)

    def new_conversation(self) -> None:
        self.page.goto("https://chat.deepseek.com/")
        self.page.wait_for_timeout(1500)
        self._dismiss_cookie_banner()

    def send_message(self, text: str) -> str:
        self._dismiss_cookie_banner()
        before = len(self.page.query_selector_all(".ds-markdown"))

        self.page.locator('textarea[placeholder="Message DeepSeek"]').click(force=True, timeout=10000)
        self.page.keyboard.type(text)
        # With the cookie banner dismissed above, this should be the only
        # match -- if a second ds-button--primary shows up again for some
        # other reason, that's worth investigating live, not silently
        # picking one.
        send_btns = self.page.query_selector_all('[role="button"].ds-button--primary')
        if len(send_btns) != 1:
            raise RuntimeError(
                f"send_message: expected exactly 1 primary button (the send button), found {len(send_btns)} "
                "-- investigate live before trusting which one is the real send button."
            )
        send_btns[0].click(force=True)

        def _last_reply_text() -> str:
            els = self.page.query_selector_all(".ds-markdown")
            return els[-1].inner_text() if els else ""

        deadline_ms = 60000
        waited_ms = 0
        while waited_ms < deadline_ms:
            if len(self.page.query_selector_all(".ds-markdown")) > before:
                break
            self.page.wait_for_timeout(1000)
            waited_ms += 1000
        else:
            raise RuntimeError("send_message: no new reply appeared within 60s")

        prev_text = None
        stable_checks = 0
        waited_ms = 0
        while waited_ms < 60000:
            self.page.wait_for_timeout(1000)
            waited_ms += 1000
            cur_text = _last_reply_text()
            if cur_text and cur_text == prev_text:
                stable_checks += 1
                if stable_checks >= 2:
                    break
            else:
                stable_checks = 0
            prev_text = cur_text

        return _last_reply_text()

    def set_memory_field(self, text: str) -> None:
        """Not applicable -- DeepSeek has no I2/I3 injection surface, no
        memory field exists. Should never be called for this platform."""
        raise NotImplementedError("DeepSeek has no memory field -- I1 (chat) is the only injection surface.")

    # --- ERASURE_DISPATCH targets ---

    def _send_nl_forget(self) -> None:
        """Not a UI click -- routes back through send_message() with the
        erasure_request_sentence() text once that's wired in
        (RTBF-Prompt/token_generator.py). Expected-null by architecture:
        DeepSeek is claimed to have no persistence layer, so this cell is
        pre-registered to fail -- run it anyway, don't skip it."""
        raise NotImplementedError

    def _delete_single_conversation(self) -> None:
        """E1: deletes the most recently opened/first conversation from
        the sidebar."""
        self.page.goto("https://chat.deepseek.com/")
        self.page.wait_for_timeout(1500)
        convo = self.page.query_selector('a[href^="/a/chat/s/"]')
        if convo is None:
            raise RuntimeError("_delete_single_conversation: no conversation found in sidebar")
        convo.hover()
        self.page.wait_for_timeout(400)
        options_btn = convo.query_selector('[role="button"]')
        if options_btn is None:
            raise RuntimeError("_delete_single_conversation: no options button found on conversation row")
        options_btn.click(force=True)
        self.page.wait_for_timeout(600)
        self.page.click("text=Delete", force=True)
        self.page.wait_for_timeout(600)
        # Scoped to the dialog specifically -- the trigger and confirm
        # buttons share the literal text "Delete" (this row's menuitem
        # says "Delete", the confirm dialog's button also says "Delete"),
        # an unscoped click can hit the wrong one. See module docstring.
        self.page.locator('[role="dialog"] [role="button"]', has_text="Delete chat").click(force=True) \
            if self.page.locator('[role="dialog"] [role="button"]', has_text="Delete chat").count() \
            else self.page.locator('[role="dialog"] [role="button"]', has_text="Delete").click(force=True)
        self.page.wait_for_timeout(1000)

    def _delete_all_history(self) -> None:
        """E2: confirmed live via Multi-select mode -- select every
        conversation row, then the bottom-bar "Delete" button, then
        confirm. See module docstring for why row-selection needs
        coordinate clicks rather than a locator-based click."""
        self.page.goto("https://chat.deepseek.com/")
        self.page.wait_for_timeout(1500)
        convo = self.page.query_selector('a[href^="/a/chat/s/"]')
        if convo is None:
            return  # nothing to delete
        convo.hover()
        self.page.wait_for_timeout(400)
        options_btn = convo.query_selector('[role="button"]')
        options_btn.click(force=True)
        self.page.wait_for_timeout(600)
        self.page.click("text=Multi-select", force=True)
        self.page.wait_for_timeout(1000)

        # Structural selector (the row-title div's own class), NOT a text-
        # content pattern -- confirmed live 2026-08-27 that conversation
        # titles vary wildly (auto-generated summaries, sometimes a raw
        # ISO timestamp, sometimes just the message text) and an earlier
        # version of this method that regex-matched a date-like title
        # silently found 0 rows once titles didn't happen to look like
        # that. `a[href^="/a/chat/s/"]` (used elsewhere in this file)
        # isn't present in multi-select mode, hence this fallback class.
        rows = self.page.evaluate("""() => {
            const rows = [...document.querySelectorAll('.c08e6e93')];
            return rows.map(r => { const b = r.getBoundingClientRect(); return {x: b.x + b.width/2, y: b.y + b.height/2}; });
        }""")
        # First row is already selected (carried over from the options
        # menu selection state) -- only click the rest.
        for pt in rows[1:]:
            self.page.mouse.click(pt["x"], pt["y"])
            self.page.wait_for_timeout(150)
        self.page.wait_for_timeout(500)

        self.page.click("text=Delete", force=True)
        self.page.wait_for_timeout(800)
        self.page.locator('[role="dialog"] [role="button"]', has_text="Delete").click(force=True)
        self.page.wait_for_timeout(1500)

    def _erase_maximal(self) -> None:
        """E4: singles combined in one setup (design rule)."""
        self._delete_single_conversation()
        self._delete_all_history()
