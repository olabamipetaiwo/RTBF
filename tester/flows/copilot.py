"""Copilot flow (copilot.microsoft.com). Selectors below were pulled from a
live, logged-in session (anchorexperiment@gmail.com, signed in via "Sign in
with Google" -- Copilot supports Microsoft/Apple/Google login, not just
Microsoft-native) on 2026-08-27, same process used for ChatGPT and Gemini.

Session capture needed BOTH cookies and localStorage this time -- Copilot's
login is Auth0-based (SPA SDK), and the actual session tokens live in
localStorage under "@@auth0spajs@@..." and "msal.2|...accesstoken/
refreshtoken/idtoken..." keys, not in cookies (the cookies are just a
lightweight "is authenticated" flag). Cookie-only export (which sufficed for
ChatGPT and Gemini) left the session unauthenticated here. See
import_exported_cookies.py's docstring -- it now accepts an optional
sessions/_manual_localstorage_<platform>.json (grabbed via one DevTools
Console command: copy(JSON.stringify(Object.fromEntries(Object.entries(
localStorage))))) and attaches it to storage_state's origins.

Findings that shaped the design below:

1. I2 ("explicit memory injection") IS chat-based, like Claude/ChatGPT --
   NOT field-based like Gemini's Saved-info. The Settings > Memory > "Add a
   fact" button doesn't open a dedicated field; it just navigates to the
   normal chat composer pre-filled with "Remember this:". The underlying
   action is a regular chat message either way, so
   MEMORY_FIELD_INJECTION_TYPES stays empty (send_message() handles I2).

2. E4 "Granular facts editor" is a genuine per-item list (Settings > Memory
   > View memory), same shape as Gemini's Saved-info -- add/delete-one/
   delete-all all work. "Delete all memory" only appears as a button once
   there are 2+ facts (not visible with 0 or 1) -- don't assume it's always
   present.

3. The "Personalization and memory" toggle on the Memory settings page does
   NOT delete existing facts -- confirmed live by toggling off then back on
   and finding a previously-saved fact still present. It's a feature
   on/off switch, not an erasure action. Don't use it for _delete_all_memory().

4. E1 ("Conversation history deletion") and E5 ("Privacy Dashboard") were
   two separate MASTER rows, but Settings > Privacy > "Export or delete
   history" turned out to route to the SAME cross-domain destination as E5
   (account.microsoft.com/privacy) -- so that particular UI path isn't E1's
   real target. The actual E1 mechanism is the same-domain per-conversation
   delete from the sidebar (like ChatGPT/Gemini's conversation delete),
   confirmed live and implemented below.

5. The sidebar's per-conversation "..." (View Options) button is
   deceptive: its own reported bounding_box() sits at the right vertical
   position but the wrong horizontal one -- clicking there force-clicks
   through to the row's navigate-into-conversation handler instead.
   Clicking the real visible icon position (empirically ~28px further
   right than the button element's own box) works. If this ever breaks,
   re-derive the offset live rather than reusing the magic number blindly.

E5 (Privacy Dashboard) is deliberately left unautomated -- same standing
decision as Gemini's E3 (Delete all activity): confirmed live it's cross-
domain (account.microsoft.com/privacy) and hits a sign-in wall with only
copilot.microsoft.com's session captured. Not worth a second cross-domain
cookie+localStorage export for one erasure surface. Run E5/E6 cells
manually instead of through run_cell.py.
"""

from __future__ import annotations

from .base import PlatformFlow


class CopilotFlow(PlatformFlow):
    platform = "copilot"

    # I2 is chat-based here (like Claude/ChatGPT), not field-based (like
    # Gemini) -- confirmed live, see module docstring finding 1.
    MEMORY_FIELD_INJECTION_TYPES: set[str] = set()

    # Keys are the exact erasure_type_text values from CellPlan (MASTER
    # sheet's Erasure desc column), matching MASTER's description text.
    ERASURE_DISPATCH = {
        "Conversation history deletion": "_delete_conversation_history",
        # FILE-substudy aliases -- see flows/claude.py's ERASURE_DISPATCH
        # for why these exist. MAXIMAL's alias still hits the same
        # cross-domain _delete_via_privacy_dashboard() block as the main
        # battery's CO-*-E6 cells -- not resolved by this alias.
        "Delete conversation containing file": "_delete_conversation_history",
        "Maximal combination (all erasure mechanisms)": "_erase_maximal",
        "Delete all memory": "_delete_all_memory",
        "NL forget command": "_send_nl_forget",  # chat message, not a UI click
        "Granular facts editor": "_delete_via_facts_editor",
        "Privacy Dashboard": "_delete_via_privacy_dashboard",  # deliberately manual, see module docstring
        "MAXIMAL": "_erase_maximal",
    }

    def new_conversation(self) -> None:
        self.page.goto("https://copilot.microsoft.com/")
        self.page.wait_for_timeout(1500)

    def _last_reply_text(self) -> str:
        els = self.page.query_selector_all('[data-testid="ai-message-body"]')
        return els[-1].inner_text() if els else ""

    def _wait_for_reply(self, before_count: int) -> str:
        """Shared by send_message() and upload_file()."""
        deadline_ms = 60000
        waited_ms = 0
        while waited_ms < deadline_ms:
            if len(self.page.query_selector_all('[data-testid="ai-message-body"]')) > before_count:
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

        return self._last_reply_text()

    def send_message(self, text: str) -> str:
        before = len(self.page.query_selector_all('[data-testid="ai-message-body"]'))

        self.page.locator("#userInput").click(force=True, timeout=10000)
        self.page.keyboard.type(text)
        self.page.locator('[aria-label="Submit message"]').click(force=True, timeout=10000)

        return self._wait_for_reply(before)

    def upload_file(self, file_path: str, caption: str | None = None) -> str:
        """FILE-substudy cells: attach a document via the real (hidden)
        <input type="file"> found live 2026-08-28 -- directly reachable
        via set_input_files(), no need to click "Attach files, connect
        apps, or make something with Copilot" first. .pdf is in its
        accept list. caption=None (default) sends the file with no
        accompanying message."""
        before = len(self.page.query_selector_all('[data-testid="ai-message-body"]'))

        self.page.locator('input[type="file"]').first.set_input_files(file_path)
        self.page.wait_for_timeout(2000)

        if caption:
            self.page.locator("#userInput").click(force=True, timeout=10000)
            self.page.keyboard.type(caption)
            self.page.wait_for_timeout(500)

        self.page.locator('[aria-label="Submit message"]').click(force=True, timeout=10000)
        return self._wait_for_reply(before)

    def set_memory_field(self, text: str) -> None:
        """Not used for Copilot -- I2 is chat-based, see module docstring."""
        raise NotImplementedError("Copilot's I2 is chat-based -- use send_message(), not set_memory_field().")

    def _open_view_memory(self) -> None:
        # If a Settings dialog is already open (e.g. this is a second call
        # in the same flow instance), clicking the account button again
        # doesn't reliably reopen the "Memory" shortcut menuitem -- close
        # first for a clean state. Confirmed live 2026-08-27: same class of
        # "state carries over between calls" issue as Gemini's goto()-no-op.
        dialog = self.page.query_selector('[role="dialog"], [role="alertdialog"]')
        if dialog:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(500)

        self.page.click('[data-testid="sidebar-settings-button"]', force=True)
        self.page.wait_for_timeout(1000)
        self.page.get_by_role("menuitem", name="Memory").click()
        self.page.wait_for_timeout(1000)
        self.page.get_by_text("View memory", exact=True).click()
        self.page.wait_for_timeout(1500)

    def read_memory_settings(self) -> str:
        """R2: the Granular facts editor ("View memory") page.

        Scoped to the dialog specifically, NOT page body -- confirmed live
        2026-08-27 this matters: "Delete all memory" explicitly does not
        delete conversation history (the confirm dialog says so), and
        conversations get auto-titled from their content (e.g. a
        "Remember this: my kayak is called X" message can produce a
        sidebar conversation titled around X). body-scoped text search
        picked up those lingering sidebar titles and produced a false
        "still present" reading even when the actual memory list was
        correctly empty -- this cost significant debugging time chasing a
        phantom deletion bug that didn't exist before this was found.

        [role="dialog"] alone isn't unique enough either -- this page has
        ~9 elements with that role (mostly empty design-system portal
        placeholders, one is even part of the chat message UI). Scope to
        specifically the one containing "View memory"."""
        self._open_view_memory()
        for d in self.page.query_selector_all('[role="dialog"]'):
            text = d.inner_text()
            if "View memory" in text:
                return text
        raise RuntimeError("read_memory_settings: couldn't find the View memory dialog")

    # --- ERASURE_DISPATCH targets ---

    def _send_nl_forget(self) -> None:
        """Not a UI click -- routes back through send_message() with the
        erasure_request_sentence() text once that's wired in
        (RTBF-Prompt/token_generator.py). Placeholder for now, same as
        every other platform's equivalent method."""
        raise NotImplementedError

    def _delete_conversation_history(self) -> None:
        """E1: deletes the most recently opened conversation from the
        sidebar. See module docstring finding 5 for why the click position
        is offset from the button's own bounding_box()."""
        self.page.goto("https://copilot.microsoft.com/")
        self.page.wait_for_timeout(1500)
        # Sidebar open/closed state persists across navigations (a client-
        # side preference), so "Open sidebar" may or may not exist -- check
        # for conversation rows first rather than assuming the toggle is
        # there (confirmed live 2026-08-27: indexing sidebar_toggles[2]
        # blindly threw IndexError once the sidebar was already open).
        if not self.page.query_selector_all('[aria-label="View Options"]'):
            sidebar_toggles = self.page.query_selector_all('[aria-label="Open sidebar"]')
            # Empirically the 3rd match is the real small icon button; the
            # 1st is an oversized wrapper that swallows clicks meant for
            # content underneath it (confirmed live 2026-08-27).
            (sidebar_toggles[2] if len(sidebar_toggles) > 2 else sidebar_toggles[0]).click(force=True)
            self.page.wait_for_timeout(1000)

        opts = self.page.query_selector_all('[aria-label="View Options"]')
        if not opts:
            raise RuntimeError("_delete_conversation_history: no conversation found in sidebar")
        box = opts[0].bounding_box()
        self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=5)
        self.page.wait_for_timeout(500)
        self.page.mouse.click(228, box["y"] + box["height"] / 2)
        self.page.wait_for_timeout(800)
        self.page.get_by_role("menuitem", name="Delete", exact=True).click()
        self.page.wait_for_timeout(800)
        self.page.get_by_role("button", name="Delete", exact=True).last.click()
        self.page.wait_for_timeout(1500)

    def _delete_all_memory(self) -> None:
        """E2: "Delete all memory" button on the View memory page. Only
        appears once there are 2+ facts -- see module docstring finding 2.
        Do NOT use the "Personalization and memory" toggle for this --
        confirmed live it doesn't delete existing facts (finding 3)."""
        self._open_view_memory()
        self.page.get_by_role("button", name="Delete all memory", exact=True).click()
        # Wait for the "Delete all memory?" confirm dialog to actually
        # appear before clicking its Delete button -- confirmed live
        # 2026-08-27 this is flaky with a fixed short wait: sometimes the
        # confirm click lands before the dialog has fully mounted and
        # silently does nothing, leaving all facts intact with no error.
        self.page.wait_for_selector("text=Delete all memory?", timeout=10000)
        self.page.get_by_role("button", name="Delete", exact=True).last.click()
        # Then wait for that dialog to close (delete committed) before
        # returning, not just a fixed short wait.
        self.page.wait_for_selector("text=Delete all memory?", state="hidden", timeout=15000)
        self.page.wait_for_timeout(1000)

    def _delete_via_facts_editor(self) -> None:
        """E4: deletes the first fact via its trash icon in the View
        memory list. Confirmed live to be a genuine per-item list, same
        shape as Gemini's Saved-info -- see module docstring finding 2.

        The trash icon has no text/aria-label, and a text-content-based
        search is unreliable here: fact text can be split across child
        nodes (fails a children.length===0 leaf check), and an unscoped
        search matches the settings dialog's own "Preferences" tab button
        before ever reaching a real fact row (confirmed live 2026-08-27,
        both tried and both failed). What actually works: the dialog has
        exactly 3 unlabeled buttons -- the dialog's own close X (top
        right, y roughly 90), the "View memory" back arrow (top left,
        x roughly 500), and each fact's trash icon (right-aligned, x >
        800, y increasing per row). Filtering to x > 800 and sorting by y
        reliably picks the first fact's trash icon."""
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
        trash_icons[0][1].click()
        self.page.wait_for_timeout(600)
        self.page.get_by_role("button", name="Delete", exact=True).last.click()
        self.page.wait_for_timeout(1500)

    def _delete_via_privacy_dashboard(self) -> None:
        """E5: deliberately left manual (2026-08-27 decision, same as
        Gemini's E3) -- confirmed live it's cross-domain
        (account.microsoft.com/privacy) and hits a sign-in wall with only
        copilot.microsoft.com's session captured. Run these cells by hand."""
        raise NotImplementedError(
            "E5 (Privacy Dashboard) is deliberately manual -- run this cell "
            "by hand rather than through run_cell.py, per the standing "
            "decision on cross-domain erasure surfaces (see Gemini's E3)."
        )

    def _erase_maximal(self) -> None:
        """E6: all singles combined in one setup (design rule). Will raise
        on _delete_via_privacy_dashboard() until/unless that decision
        changes."""
        self._delete_conversation_history()
        self._delete_all_memory()
        self._delete_via_facts_editor()
        self._delete_via_privacy_dashboard()
