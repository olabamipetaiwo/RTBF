"""ChatGPT flow (chatgpt.com).

Selectors below were pulled from a live, logged-in session on 2026-08-27
(not guessed). One real product-design finding from that session that
changes an ENUMERATION assumption: ChatGPT's memory UI has been redesigned
since ENUMERATION was written. It's no longer a list of individually
deletable memory bullets -- "Manage" now opens a single AI-generated
"Memory summary" card (Overview prose + a "Dive Deeper" link) with an
"Ask or update" free-text box for corrections, plus a "..." menu with only
"About memory" / "Refresh summary" / "Delete and turn off memory". There is
no per-item delete control anymore. This directly resolves DECISIONS Q4/Q6
territory: "Delete individual memory entry" as ENUMERATION described it
(pick one bullet, delete it) does not exist in the current product --
individual correction now happens by typing a natural-language correction
into the summary's "Ask or update" box, which is functionally closer to I2
(explicit memory instruction) than a UI-click erasure. Flagged in
_delete_individual_memory_entry() below; needs a DECISIONS update, not a
selector fix.

Both of the originally VERIFY/PROVISIONAL erasure rows are now resolved:
Q6 (E5 field-clear vs. toggle) is moot per the above (there's no toggle,
just a text field). Q5 (E6, bulk chat history delete) confirmed live
2026-08-28: it genuinely exists, under Settings > Data controls > "Delete
all" ("Delete all chats") -- see _clear_all_chat_history_bulk().
"""

from __future__ import annotations

from .base import PlatformFlow


class ChatGPTFlow(PlatformFlow):
    platform = "chatgpt"

    # Keys are the exact erasure_type_text values from CellPlan (MASTER
    # sheet's Erasure desc column), matching ENUMERATION's description text.
    ERASURE_DISPATCH = {
        "NL forget prompt": "_send_nl_forget",  # chat message, not a UI click
        "Delete conversation": "_delete_conversation",
        # FILE-substudy aliases -- see flows/claude.py's ERASURE_DISPATCH
        # for why these exist (same methods, different sheet phrasing).
        "Delete conversation containing file": "_delete_conversation",
        "Maximal combination (all erasure mechanisms)": "_erase_maximal",
        "Delete individual memory entry": "_delete_individual_memory_entry",
        "Clear all memories": "_clear_all_memories",
        "Clear custom instructions": "_clear_custom_instructions",  # VERIFY, Q6 -- field-clear vs. toggle, see method docstring
        "Clear all chat history (bulk)": "_clear_all_chat_history_bulk",  # confirmed live 2026-08-28, Q5
        "MAXIMAL": "_erase_maximal",
    }

    def new_conversation(self) -> None:
        # .first: "create-new-chat-button" testid matches two elements (a
        # sidebar link and a header icon) -- either works, first is stable.
        # force=True: the sidebar's opacity/width transition briefly
        # intercepts pointer events right after page load even though the
        # element reports visible/stable -- confirmed live 2026-08-27.
        self.page.wait_for_timeout(1000)
        self.page.locator('[data-testid="create-new-chat-button"]').first.click(force=True, timeout=10000)
        self.page.wait_for_timeout(1500)

    def _last_assistant_text(self) -> str:
        turns = self.page.query_selector_all('[data-message-author-role="assistant"]')
        return turns[-1].inner_text() if turns else ""

    def _wait_for_reply(self, before_count: int) -> str:
        """Shared by send_message() and upload_file(). Waits for a NEW
        assistant turn to appear (turn count increases), not just for the
        send-button selector to exist -- it exists before, during, and
        after sending, so it's not a useful signal by itself. Then waits
        for streaming to finish by polling until the response text stops
        changing between checks -- the send-button testid doesn't
        reliably flip back to a stable "done" state to wait on (confirmed
        live 2026-08-27). Re-queries fresh each poll rather than reusing
        one ElementHandle -- React replaces (not mutates) the streaming
        turn's DOM node, so a handle captured early goes stale and reads
        back empty forever (confirmed live 2026-08-27)."""
        deadline_ms = 60000
        waited_ms = 0
        while waited_ms < deadline_ms:
            turns = self.page.query_selector_all('[data-message-author-role="assistant"]')
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

        return self._last_assistant_text()

    def send_message(self, text: str) -> str:
        before = len(self.page.query_selector_all('[data-message-author-role="assistant"]'))

        self.page.locator("#prompt-textarea").click(force=True, timeout=10000)
        self.page.keyboard.type(text)
        self.page.locator('[data-testid="send-button"]').click(force=True, timeout=10000)

        return self._wait_for_reply(before)

    def upload_file(self, file_path: str, caption: str | None = None) -> str:
        """FILE-substudy cells: attach a document via the real (hidden)
        <input type="file" id="upload-files"> found live 2026-08-28 --
        the only one of 3 file inputs present (upload-files/upload-photos/
        upload-camera) without an image-only accept restriction. Directly
        reachable via set_input_files(), no need to click "Add files and
        more" first. caption=None (default) sends the file with no
        accompanying message."""
        before = len(self.page.query_selector_all('[data-message-author-role="assistant"]'))

        self.page.set_input_files('#upload-files', file_path)
        self.page.wait_for_timeout(2000)
        # Confirmed live 2026-08-28 (CH-IF-E-MAX, 3 consecutive attempts):
        # set_input_files() occasionally doesn't register at all -- no
        # attachment chip, no send-button, no error, nothing -- while an
        # identical call for a different cell/file succeeds immediately.
        # No selector/timing cause found (file itself was verified intact);
        # reads as the same class of real nondeterminism already documented
        # for Copilot's chat-based memory save. One retry, same as that
        # fix, rather than chasing a root cause further.
        if self.page.locator('[data-testid="send-button"]').count() == 0:
            self.page.set_input_files('#upload-files', file_path)
            self.page.wait_for_timeout(3000)

        if caption:
            self.page.locator("#prompt-textarea").click(force=True, timeout=10000)
            self.page.keyboard.type(caption)
            self.page.wait_for_timeout(500)

        # Widened from a flat 10s after two real-batch failures 2026-08-28
        # (CH-IF-E-CONV, CH-IF-E-MAX) both timed out waiting for
        # send-button here -- same selector/flow that passed cleanly in
        # isolated verification earlier, so this reads as real-world file-
        # upload-processing variance (PDF size/network/server load), not a
        # selector regression. 25s gives ChatGPT's client-side upload
        # processing more headroom before giving up.
        self.page.locator('[data-testid="send-button"]').click(force=True, timeout=25000)
        return self._wait_for_reply(before)

    def _open_settings_personalization(self) -> None:
        self.page.goto("https://chatgpt.com/#settings/Personalization")
        self.page.wait_for_selector('[data-testid="personalization-tab"]', timeout=15000)
        self.page.wait_for_timeout(500)

    def _fill_custom_instructions(self, text: str) -> None:
        """Shared by set_memory_field() and _clear_custom_instructions() --
        same field, save mechanism, just different target text. Confirmed
        live 2026-08-27: this field does NOT autosave on blur/Tab -- it
        silently discards on reload unless the explicit "Save" button
        (role=button, name="Save") is clicked. Also confirmed .fill()
        alone reaches the field's value fine (React picks it up), so the
        earlier autosave assumption, not the fill mechanism, was the bug.

        `text` is the FULL new value to save, not a delta -- callers
        (set_memory_field's append, _clear_custom_instructions's own-line
        removal) compute the complete resulting text themselves before
        calling this. Confirmed live: if the resulting value equals the
        field's current value (nothing changed), ChatGPT never enables the
        Save button, so this waits for it to be visible+enabled with a
        short timeout instead of assuming it's always clickable -- a
        no-op call is treated as success, not a hang."""
        field = self.page.get_by_placeholder("Additional behavior, style, and tone preferences")
        field.click()
        field.fill(text)
        save_btn = self.page.get_by_role("button", name="Save", exact=True)
        try:
            save_btn.click(timeout=5000)
            self.page.wait_for_timeout(1500)
        except Exception:
            pass  # no-op edit (resulting text == current text) -- nothing to save

    def set_memory_field(self, text: str) -> None:
        """I3: ChatGPT's Custom Instructions settings field (Settings ->
        Personalization -> "Custom instructions" text box). APPENDS `text`
        as its own new line instead of overwriting the field -- confirmed
        live 2026-08-31 (CH-I3-E4/E5/E6/E7) that the field is a genuine
        multi-line textarea, not a single-value slot: overwriting silently
        destroyed every sibling I3 cell's anchor except whichever was
        injected last, since they all share one ChatGPT account. Each
        cell's line must stay independently identifiable (by its own
        token) so _clear_custom_instructions() can later remove only this
        cell's line without touching siblings'."""
        self._open_settings_personalization()
        field = self.page.get_by_placeholder("Additional behavior, style, and tone preferences")
        current = field.input_value()
        new_value = f"{current}\n{text}" if current.strip() else text
        self._fill_custom_instructions(new_value)

    def read_memory_settings(self) -> str:
        """R2 probe: opens the "Memory summary" panel and returns its
        Overview text -- this is now an AI-generated summary, not a raw
        list of stored facts, so exact-string matching against the
        referent/token may need to tolerate paraphrase. See module
        docstring.

        Closes both the Memory dialog and the Settings overlay (2
        Escape presses) before returning -- confirmed live 2026-08-28
        this is genuinely needed: leaving them open breaks a subsequent
        new_conversation() call (the composer/send-button never render
        while the Settings hash-route overlay is still active), which
        surfaced as a real send_message() timeout in
        _run_recall_probes()'s R3 step the first time this method was
        exercised as part of a real recall run. Same shape of bug as
        Claude's _open_memory_settings() (see that module's docstring)."""
        self._open_settings_personalization()
        self.page.get_by_role("button", name="Manage", exact=True).first.click()
        self.page.wait_for_timeout(1500)
        dialog = self.page.query_selector_all('[role="dialog"]')[-1]
        text = dialog.inner_text()
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(800)
        return text

    # --- ERASURE_DISPATCH targets ---

    def _send_nl_forget(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        """Not a UI click -- routes back through send_message() with the
        erasure_request_sentence() text once that's wired in
        (RTBF-Prompt/token_generator.py). Placeholder for now."""
        raise NotImplementedError

    def _delete_conversation(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        """Deletes THIS cell's own conversation, identified by `ref` (the
        exact conversation URL captured at injection time). Confirmed live
        2026-08-31 that grabbing "whatever's topmost in the sidebar"
        (the old behavior) silently deletes a completely unrelated cell's
        conversation whenever this account has been used for other cells
        more recently -- always true once cells share an account. Falls
        back to topmost only when `ref` is None (e.g. an I3 cell whose own
        injection lives in a settings field, not a conversation, so
        "Delete conversation" is deliberately testing an arbitrary/most-
        recent conversation as a cross-mechanism probe)."""
        if ref:
            from urllib.parse import urlsplit
            convo = self.page.query_selector(f'a[href="{urlsplit(ref).path}"]')
            if convo is None:
                raise RuntimeError(f"_delete_conversation: expected conversation {ref!r} not found in sidebar")
        else:
            convo = self.page.query_selector('a[href^="/c/"]')
        if convo is None:
            raise RuntimeError("_delete_conversation: no conversation found in sidebar")
        convo.hover()
        self.page.wait_for_timeout(300)
        self.page.click('[aria-label^="Open conversation options for"]')
        self.page.wait_for_timeout(500)
        self.page.click('[data-testid="delete-chat-menu-item"]')
        self.page.wait_for_timeout(500)
        self.page.click('[data-testid="delete-conversation-confirm-button"]')
        self.page.wait_for_timeout(1000)

    def _delete_individual_memory_entry(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        """No longer exists as ENUMERATION described it -- see module
        docstring. The current UI has no per-item delete; the closest
        analogue is typing a correction into the Memory summary's
        "Ask or update" box, which is a memory-instruction action, not a
        UI-click erasure. Needs a DECISIONS update before this cell can run
        as originally designed -- not a selector bug, don't just patch."""
        raise NotImplementedError(
            "ChatGPT's memory UI redesign removed per-item memory deletion "
            "(confirmed live 2026-08-27) -- needs a DECISIONS-sheet call on "
            "how/whether to adapt this cell before implementing further."
        )

    def _clear_all_memories(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        """Deliberately account-wide/blanket -- see [[project-destructive-actions-run-last]].
        `token`/`ref` accepted for interface consistency but unused: this
        mechanism has no narrower real-product equivalent to target with.
        Settings -> Personalization -> Manage (saved memories) -> "..."
        (aria-label "About You menu") -> "Delete and turn off memory".
        Note the real UI combines clear + disable in one action -- there is
        no clear-without-disabling variant, worth noting as a caveat on
        this cell's outcome coding. Confirmed live 2026-08-28: a real
        confirm dialog follows ("Delete and turn off memory? ... Delete
        and turn off memory / Cancel"), needs its own click -- the earlier
        caveat about this being unverified is resolved. Also confirmed:
        this genuinely disables the "Enable memory" toggle in
        Personalization settings, not just this dialog's own framing --
        re-enable it manually (Personalization -> "Enable memory" switch)
        before running any further memory-dependent cells on this
        account."""
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
        """Removes only THIS cell's own line (the one containing `token`)
        from the custom-instructions field, leaving any sibling cells'
        lines intact -- matches what a real user would actually do
        (selectively edit out one note), and mirrors set_memory_field()'s
        append-not-overwrite fix. Changed from a full-field blank
        2026-08-31 after confirming live that the old blanket-clear
        destroyed sibling I3 cells' anchors (e.g. CH-I3-E7's) days before
        their own scheduled erasure. Confirmed live 2026-08-27 this field
        is a genuine text field, not a toggle -- Q6 is resolved, no
        toggle-vs-field ambiguity exists."""
        self._open_settings_personalization()
        field = self.page.get_by_placeholder("Additional behavior, style, and tone preferences")
        current = field.input_value()
        remaining = "\n".join(
            line for line in current.split("\n") if token.strip().lower() not in line.lower()
        )
        self._fill_custom_instructions(remaining)

    def _clear_all_chat_history_bulk(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        """Deliberately account-wide/blanket -- see [[project-destructive-actions-run-last]].
        `token`/`ref` accepted for interface consistency but unused.
        E6: confirmed live 2026-08-28 (DECISIONS Q5) -- genuinely
        exists as a real "Delete all chats" action, under Settings > Data
        controls (not Personalization, and not the Archive-all button
        right above it -- easy to mix up, "Archive all" is a different
        control on the same panel). Path: profile menu -> Settings ->
        Data controls tab -> "Delete all" button
        (aria-label="Delete all Delete all chats") -> a real confirm
        dialog ("Clear your chat history - are you sure? This will
        delete all chats, including chats in Projects.") -> "Confirm
        deletion". Verified with a real persistence check (4 conversations
        -> 0 after reload). The confirm dialog's own text notes memory is
        a separate system ("To clear any memories from your chats, visit
        your settings") -- confirms this doesn't overlap with
        _clear_all_memories()."""
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
        """E7: all singles combined in one setup (design rule)."""
        self._delete_conversation(token=token, ref=ref)
        self._clear_all_memories(token=token, ref=ref)
        self._clear_custom_instructions(token=token, ref=ref)
