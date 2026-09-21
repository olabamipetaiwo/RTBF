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

    def _verify_logged_in(self) -> None:
        """Logged-out Gemini renders a full, plausible-looking chat UI --
        it even answers messages (sometimes with a fabricated "I've
        cleared that" reply) -- with the only tell being a "Sign in"
        button in the top-right nav (confirmed live 2026-09-17, see
        base.py's docstring for the incident this fixes). Checked with a
        short timeout since this runs on every session start and a
        logged-in session never shows this button at all."""
        if self.page.get_by_role("button", name="Sign in", exact=True).count() > 0:
            raise RuntimeError(
                f"gemini session (label={getattr(self, '_session_path', '?')!r}) is logged out -- "
                f"'Sign in' button present. Needs a fresh cookie export before this account can run."
            )

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

    def _send_nl_forget(
        self,
        token: str | None = None,
        injection_text: str = "",
        ref: str | None = None,
        erasure_request_text: str | None = None,
    ) -> None:
        """Not a UI click -- routes back through send_message() with the
        erasure_request_sentence() text (RTBF-Prompt/token_generator.py),
        wired in 2026-09-07. `erasure_request_text` is precomputed per
        cell (only the 13 blocked_on_prompt_set cells get one, written to
        MASTER by token_generator.py) and forwarded here by base.py's
        erase_via_ui(). Navigates to this cell's own conversation via
        `ref` (captured at injection time) so the erasure request lands
        in the same conversation as the disclosure. If `ref` is missing,
        this cell's injection was field-routed (I2 targets a dedicated
        field on this platform, see MEMORY_FIELD_INJECTION_TYPES), which
        has no owned conversation -- falls back to a fresh conversation
        instead, same rationale as _delete_conversation's no-ref fallback
        above."""
        if not erasure_request_text:
            raise RuntimeError(
                "_send_nl_forget: no erasure_request_text provided -- "
                "this cell's prompt-set text isn't wired in"
            )
        if ref:
            self._goto_fresh(ref)  # plain goto() can no-op on this Angular SPA, see _goto_fresh
        else:
            self.new_conversation()
        self.assert_real_answer(self.send_message(erasure_request_text))

    def _delete_conversation(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        """Deletes THIS cell's own conversation, identified by `ref` (the
        exact conversation URL captured at injection time) -- same fix as
        ChatGPT/Claude/DeepSeek. NOTE: unverified live against this
        platform specifically -- Gemini's session was logged out when this
        was written (see PROJECT_STATUS/memory), re-verify once
        re-authenticated, before trusting this on a real cell.

        **No topmost fallback, ever, as of 2026-09-09**: an earlier
        version fell back to topmost whenever `ref` was missing and the
        token search found nothing -- real risk surfaced live for
        `GE-I2-E2` (I2 injects into the Saved-info field, not chat, so it
        has NO owned conversation at all; this method would have silently
        deleted whatever conversation was topmost on the shared account,
        e.g. a sibling I1 cell's real conversation). Reverted per direct
        instruction -- a cell must only ever delete its own entry, never a
        sibling's as a fallback. If nothing matches, raise instead of
        guessing (which correctly surfaces "this cell has no conversation
        to delete" as an error, not a silent wrong deletion)."""
        self._goto_fresh("https://gemini.google.com/app")
        from urllib.parse import urlsplit
        convo = self.page.query_selector(f'a[href="{urlsplit(ref).path}"]') if ref else None
        if convo is None:
            # Either no ref was given, or the given ref is stale (confirmed
            # live 2026-09-09 on GE-I1-E6: a 2026-09-01 ref no longer
            # matched anything, even though the conversation genuinely
            # still existed in the sidebar, auto-titled from its token) --
            # both cases get the same token-content search before giving
            # up, never a topmost guess.
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
        # Scoped to the row container, not page-wide -- an unscoped click
        # always grabs the topmost row's options button regardless of which
        # row was hovered. Same bug found and fixed on chatgpt.py's
        # equivalent method 2026-09-09. Note: the options button is a
        # SIBLING of the <a> (both children of <gem-nav-list-item>), not a
        # descendant of it -- confirmed live 2026-09-09 that convo.query_selector
        # itself always returns None here, unlike chatgpt.py's DOM shape.
        # No force=True here -- confirmed live 2026-09-09 that a forced
        # click on this specific button opens nothing (Angular Material's
        # menu-trigger overlay needs a real actionability-checked click;
        # force skips that and the event falls through to the sidebar link
        # underneath, navigating into the conversation instead of opening
        # the options menu).
        row = convo.evaluate_handle('el => el.closest("gem-nav-list-item")').as_element()
        row.query_selector('button[aria-label*="More options for"]').click()
        self.page.wait_for_timeout(600)
        self.page.get_by_role("menuitem", name="Delete", exact=True).click()
        self.page.wait_for_timeout(600)
        self.page.get_by_role("button", name="Delete", exact=True).click()
        self.page.wait_for_timeout(1000)

    def _delete_all_activity(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
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

    def _delete_saved_info_item(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        """Deletes THIS cell's own Saved-info item, identified by finding
        the context-menu button whose enclosing row contains `token` --
        confirmed live 2026-08-27 (module docstring finding 1) that Saved-
        info items store the literal injected sentence verbatim, unlike
        Claude's paraphrased Topics, so a substring match against the
        cell's own token is reliable here (no diff-capture needed).
        Changed 2026-08-31 from grabbing the first item unconditionally --
        that silently deleted a sibling cell's saved fact on a shared
        account. NOTE: unverified live against this platform specifically
        -- Gemini's session was logged out when this was written, re-
        verify once re-authenticated before trusting this on a real cell.

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
        # Clicking the menuitem only opens a second confirmation dialog
        # ("Delete instructions?") -- missed this the first time and the
        # method silently no-op'd (no error, item just stayed). Same
        # two-step confirm pattern as _delete_all_saved_info() below.
        self.page.wait_for_timeout(600)
        dialog = self.page.locator('[role="dialog"], [role="alertdialog"]').first
        dialog.get_by_role("button", name="Delete", exact=True).click()
        self.page.wait_for_timeout(1000)

    def _delete_all_saved_info(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        """Deliberately account-wide/blanket -- see [[project-destructive-actions-run-last]].
        `token`/`injection_text`/`ref` accepted for interface consistency
        but unused.

        Fixed 2026-09-09: an empty Saved-info list (e.g. an I1 MAXIMAL
        cell, which never wrote anything into Saved-info in the first
        place -- injection went into chat, not this field) has no
        "Delete all" button at all, and the old code just timed out
        waiting for one, indistinguishable from a real failure. Checks
        for the empty-state message first and treats it as a legitimate
        no-op (nothing to delete is a valid, correct outcome here), not
        an error."""
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
        """E6: E1+E2+E3+E4+E5 combined in one setup (design rule).

        Fixed 2026-09-09 (same pattern as claude.py's _erase_maximal fix
        2026-09-07): used to run all three sub-steps with no error
        handling, so a step with nothing real to act on aborted the whole
        sequence before ever reaching _delete_all_saved_info -- the one
        component that actually matters for this cell. Two sub-steps are
        expected to legitimately have nothing to act on / no automatable
        surface, and are now caught and logged as N/A instead of fatal:

        1. _delete_conversation(): for an I2 MAXIMAL cell (injection goes
           into the Saved-info field, not chat -- see
           MEMORY_FIELD_INJECTION_TYPES), there is no owned conversation
           at all, so this correctly raises "no owned conversation to
           delete" under the 2026-09-09 no-topmost-fallback policy. That's
           the right outcome for this cell, not a bug.
        2. _delete_all_activity(): confirmed permanent dead end (5
           independent live attempts 2026-08-28, see its own docstring)
           -- myactivity.google.com rejects any CDP-driven browser
           regardless of cookie freshness. Always raises
           NotImplementedError. Run this component by hand if full
           MAXIMAL coverage matters for a given cell; this method can't
           do it."""
        try:
            self._delete_conversation(token=token, injection_text=injection_text, ref=ref)
        except RuntimeError as e:
            print(f"_erase_maximal: _delete_conversation N/A ({e}) -- continuing")
        try:
            self._delete_all_activity(token=token, injection_text=injection_text, ref=ref)
        except NotImplementedError as e:
            print(f"_erase_maximal: _delete_all_activity N/A ({e}) -- continuing")
        self._delete_all_saved_info(token=token, injection_text=injection_text, ref=ref)
