"""Gemini flow (gemini.google.com). Selectors below were pulled from a
live, logged-in session (anchorexperiment@gmail.com) on 2026-08-27, same
process used for ChatGPT: ad hoc exploration scripts against the real page,
selector confirmed by an actual DOM query result, then written here, then
verified end-to-end with a persistence check (reload/recount) for anything
that claims to save or delete.

Two real product-design findings from that session, both worth knowing
before touching this file further:

1. Gemini's old "Saved info" feature is still a genuine per-item list (add/
   edit/delete-one/delete-all all work as ENUMERATION assumed) -- it's just
   been renamed "Instructions for Gemini" in the UI, though the route is
   still /saved-info internally. Unlike ChatGPT's memory redesign, nothing
   was actually cut here. One real behavior worth knowing: the add endpoint
   validates content and will reject strings that don't read as a genuine
   personal fact/preference ("Gemini can't save this info") -- confirmed
   live that an arbitrary placeholder string gets rejected but a normal
   disclosure-style sentence ("I have been calling the sourdough starter I
   just began ... in my notes.") is accepted. The real token_generator.py
   disclosure text should be fine since it's written to read naturally, but
   this is worth keeping in mind if a cell fails here unexpectedly.

2. E3 ("Delete all activity") is confirmed genuinely cross-domain: Settings
   -> Activity opens a NEW TAB to myactivity.google.com/product/gemini, not
   an in-page navigation. That tab hit a Google sign-in wall using the
   cookie-export session captured from gemini.google.com alone. **Retried
   2026-08-28** with a second cookie export taken directly from
   myactivity.google.com, merged into sessions/gemini.json -- still hit
   the same sign-in wall (confirmed two ways, see _delete_all_activity()'s
   own docstring). Unlike Copilot's equivalent gap (resolved the same day,
   same technique), this one looks like a genuine session-binding defense
   on Google's account-activity surface, not just a missing cookie. E3/E6
   cells stay manual -- see DECISIONS Q20.
"""

from __future__ import annotations

from .base import PlatformFlow


class GeminiFlow(PlatformFlow):
    platform = "gemini"

    # I2 ("personal context injection") targets Saved-info, not chat --
    # unlike Claude/ChatGPT where I2 is chat-based. See base.py's
    # MEMORY_FIELD_INJECTION_TYPES docstring.
    MEMORY_FIELD_INJECTION_TYPES = {"I2"}

    # Keys are the exact erasure_type_text values from CellPlan (MASTER
    # sheet's Erasure desc column), matching ENUMERATION's description text.
    ERASURE_DISPATCH = {
        "NL forget prompt": "_send_nl_forget",  # chat message, not a UI click
        "Delete single conversation": "_delete_conversation",
        # FILE-substudy aliases -- see flows/claude.py's ERASURE_DISPATCH
        # for why these exist. MAXIMAL's alias still hits the same
        # cross-domain _delete_all_activity() block as the main battery's
        # GE-*-E6 cells -- not resolved by this alias, just correctly
        # mapped to the same (currently blocked) method.
        "Delete conversation containing file": "_delete_conversation",
        "Maximal combination (all erasure mechanisms)": "_erase_maximal",
        "Delete all activity": "_delete_all_activity",  # cross-domain, blocked on session capture -- see module docstring
        "Delete single Saved info item": "_delete_saved_info_item",
        "Delete all Saved info": "_delete_all_saved_info",
        "MAXIMAL": "_erase_maximal",
    }

    def _goto_fresh(self, url: str) -> None:
        """goto() to a URL you're already on can no-op in this Angular
        SPA -- the router sees no URL change and skips re-rendering,
        leaving stale element references behind (confirmed live 2026-08-27:
        _delete_saved_info_item() intermittently failed to find its own
        just-opened menu only when called right after another method had
        already navigated to the same /saved-info URL). Force a real
        reload when we're already there instead of relying on goto()."""
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
        """Shared by send_message() and upload_file(). Poll for a new
        response block, then for its text to stabilize -- re-query fresh
        each time rather than holding one stale ElementHandle, since the
        framework replaces (not mutates) the streaming node."""
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

        return self._last_response_text()

    def send_message(self, text: str) -> str:
        before = len(self.page.query_selector_all(".model-response-text"))

        self.page.locator('[aria-label="Enter a prompt for Gemini"]').click(force=True, timeout=10000)
        self.page.keyboard.type(text)
        self.page.locator('[aria-label="Send message"]').click(force=True, timeout=10000)

        return self._wait_for_reply(before)

    def upload_file(self, file_path: str, caption: str | None = None) -> str:
        """FILE-substudy cells: attach a document via one of the two
        hidden <input type="file"> elements found live 2026-08-28 after
        clicking "Upload & tools" (no unique id/selector distinguishes
        them from each other, but both accept .pdf among many other
        extensions -- .first works fine). Directly reachable via
        set_input_files() once the "Upload & tools" menu has been opened
        once (the inputs don't exist in the DOM before that). Confirmed
        live: produces a real "File uploaded <filename>.pdf" confirmation
        chip before sending. caption=None (default) sends the file with
        no accompanying message."""
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
        """I2 for Gemini: "Saved info" (UI label "Instructions for
        Gemini"), NOT the chat stream -- confirmed live, see module
        docstring. Content is validated server-side; a non-personal-fact-
        looking string gets rejected with "Gemini can't save this info"."""
        self._goto_fresh("https://gemini.google.com/saved-info")
        self.page.get_by_role("button", name="Add", exact=True).click(timeout=10000)
        self.page.wait_for_timeout(800)
        self.page.get_by_label("Enter new memory").fill(text)
        self.page.get_by_role("button", name="Submit", exact=True).click()
        # Poll for either outcome rather than a fixed short delay --
        # confirmed live 2026-08-27 that 2s isn't reliably enough for the
        # dialog to close: a fresh read_memory_settings() reload right
        # after can race ahead of the write and show the item missing even
        # though it saves correctly a moment later. A rejection keeps the
        # dialog open with an inline error instead of closing it.
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
        """R2: the Saved info / "Instructions for Gemini" page."""
        self._goto_fresh("https://gemini.google.com/saved-info")
        return self.page.inner_text("body")

    # --- ERASURE_DISPATCH targets ---

    def _send_nl_forget(self) -> None:
        """Not a UI click -- routes back through send_message() with the
        erasure_request_sentence() text once that's wired in
        (RTBF-Prompt/token_generator.py). Placeholder for now, same as
        Claude/ChatGPT's equivalent method."""
        raise NotImplementedError

    def _delete_conversation(self) -> None:
        """Deletes the most recently opened conversation from the sidebar."""
        self._goto_fresh("https://gemini.google.com/app")
        convo = self.page.query_selector('a[href^="/app/"]')
        if convo is None:
            raise RuntimeError("_delete_conversation: no conversation found in sidebar")
        convo.hover()
        self.page.wait_for_timeout(400)
        self.page.click('button[aria-label*="More options for"]')
        self.page.wait_for_timeout(600)
        self.page.get_by_role("menuitem", name="Delete", exact=True).click()
        self.page.wait_for_timeout(600)
        self.page.get_by_role("button", name="Delete", exact=True).click()
        self.page.wait_for_timeout(1000)

    def _delete_all_activity(self) -> None:
        """E3: confirmed cross-domain (opens a new tab to
        myactivity.google.com/product/gemini). Exhaustively retried
        2026-08-28 -- five independent attempts, all failed identically
        (full logged-out "Sign In" page):
          1. Cold goto() with a merged myactivity.google.com cookie export.
          2. The genuine in-app Settings -> Activity click-through (rules
             out a missing URL-embedded auth-handoff param).
          3. playwright-stealth applied to the whole context (rules out a
             bot-fingerprint/navigator.webdriver-style check -- Claude and
             Perplexity's Cloudflare checks were exactly this kind of
             thing and stealth fixed those; it does nothing here).
          4. An alternate in-product path (Settings -> Personal
             Intelligence -> Memory -> "Manage and delete") -- turned out
             to just link to a Google support article, not an in-page
             action; dead end, not an automatable alternative route.
          5. A second cookie export taken and merged within ~1 minute of
             testing, to rule out Google's known short-lived/rotating
             SIDTS-family cookies going stale between export and use --
             still failed identically.
        gemini.google.com's own session was spot-checked as unaffected
        throughout. This matches the pattern already documented elsewhere
        in this project (see ChatGPT's Google-OAuth investigation in
        PROJECT_STATUS.md: "Google's OAuth rejects any Playwright/CDP-
        driven browser during 'Continue with Google' regardless of browser
        binary") -- current best read is that myactivity.google.com
        enforces the same kind of rejection on ANY CDP-driven browser
        (which Playwright always is, real Chrome channel or not),
        independent of cookie validity. Treated as a confirmed dead end
        for this project's available techniques, not an unbuilt feature --
        don't retry the same approaches again without a genuinely new
        idea (e.g. a non-Playwright automation layer)."""
        raise NotImplementedError(
            "E3: myactivity.google.com rejects any CDP-driven browser "
            "regardless of cookie freshness/validity or stealth patching "
            "-- 5 independent live attempts 2026-08-28, all failed "
            "identically. Confirmed dead end, not a missing-cookie gap. "
            "Run this cell by hand. See DECISIONS Q20."
        )

    def _delete_saved_info_item(self) -> None:
        """Deletes the first Saved-info item via its per-item context menu
        ("Opens a context menu for the info." -> "Delete").

        Uses a raw [role="menuitem"] query + manual text match instead of
        get_by_role() here specifically -- confirmed live 2026-08-27 that
        get_by_role("menuitem", name="Delete") times out finding this
        particular menu's items even though a plain query_selector_all
        finds them immediately and reports them visible. Something about
        how this Angular Material overlay portal renders isn't showing up
        correctly in Playwright's accessibility-tree snapshot; the raw DOM
        query doesn't have that problem. (_delete_conversation()'s menu
        doesn't hit this -- get_by_role works fine there -- so this is
        scoped to this one menu, not a project-wide rule.)"""
        self._goto_fresh("https://gemini.google.com/saved-info")
        menu_btn = self.page.query_selector('button[aria-label*="Opens a context menu for the info"]')
        if menu_btn is None:
            raise RuntimeError("_delete_saved_info_item: no saved-info item found")
        menu_btn.click()
        self.page.wait_for_timeout(600)
        delete_item = next(
            (el for el in self.page.query_selector_all('[role="menuitem"]') if el.inner_text().strip() == "Delete"),
            None,
        )
        if delete_item is None:
            raise RuntimeError("_delete_saved_info_item: no 'Delete' menuitem found")
        delete_item.click()
        # Clicking the menuitem only opens a second confirmation dialog
        # ("Delete instructions?") -- missed this the first time and the
        # method silently no-op'd (no error, item just stayed). Same
        # two-step confirm pattern as _delete_all_saved_info() below.
        self.page.wait_for_timeout(600)
        dialog = self.page.locator('[role="dialog"], [role="alertdialog"]').first
        dialog.get_by_role("button", name="Delete", exact=True).click()
        self.page.wait_for_timeout(1000)

    def _delete_all_saved_info(self) -> None:
        self._goto_fresh("https://gemini.google.com/saved-info")
        self.page.get_by_role("button", name="Delete all", exact=True).click()
        self.page.wait_for_timeout(800)
        dialog = self.page.locator('[role="dialog"], [role="alertdialog"]').first
        dialog.get_by_role("button", name="Delete all", exact=True).click()
        self.page.wait_for_timeout(1000)

    def _erase_maximal(self) -> None:
        """E6: E1+E2+E3+E4+E5 combined in one setup (design rule). E3 will
        raise until its session-capture gap is resolved -- see
        _delete_all_activity()."""
        self._delete_conversation()
        self._delete_all_activity()
        self._delete_all_saved_info()
