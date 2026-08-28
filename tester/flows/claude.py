"""Claude flow (claude.ai). Sixth platform built (2026-08-27), most cells
(15 setups: 3 injection types x 5 erasure types, all `LOCKED` in MASTER,
though Q3/Q4 gated I3 and E2 specifically until confirmed live below --
LOCKED means the design was considered settled when written, not
live-confirmed, same caveat as every other platform).

Session capture needed something new: cookie-export alone (sufficient for
the other 5 platforms) authenticated fine, but claude.ai's Cloudflare
check rejected the resulting Playwright session outright -- and unlike
every earlier block in this project, it wasn't CDP-specific. Confirmed
live 2026-08-27 that switching to Firefox (a completely different
automation protocol) hit the exact same challenge, ruling out a
CDP-only signal. What resolved it: the `playwright-stealth` package,
which patches the standard automation fingerprints (`navigator.webdriver`
and similar) that Cloudflare's check was keying on. See `flows/base.py`'s
`USE_STEALTH` flag -- set True here, False everywhere else (the other
platforms don't need it and it's not applied blanket "just in case").

**Q3 confirmed live**: memory edits ARE genuinely user-addable, not just
deletable. Settings > Memory has a natural-language command box ("Tell
Claude what to change or remove") that, despite its change/remove framing,
accepted a brand-new fact never mentioned in chat and added it (confirmed
via the inline "Adding X to memory" progress indicator and a persisted,
reloadable entry afterward).

**Q4 confirmed live**: per-item deletion of AI-generated memory genuinely
exists -- NOT via a detail view (an earlier pass wrongly assumed that;
corrected 2026-08-27 after a full button/aria-label DOM dump showed each
Topic/Area row has its own inline `aria-label="Delete <Topic Name>"`
icon button in an Actions column, with no detail view to click into at
all). Clicking it opens a real confirm dialog ("Delete this memory? ...
Cancel / Delete"), verified working with a persistence check (two
distinct topics injected, one deleted, the other survived a reload
untouched). See `_delete_individual_memory_edit()`.

**Real product-design finding, not in either DECISIONS question**:
Claude's memory is NOT a flat one-item-per-fact list like Gemini's Saved-
info or Copilot's Granular facts editor. It's organized into thematic
"Topics" (and a separate "Areas" grouping seen live for a different kind
of theme) -- injecting two unrelated facts (a kayak name, a sourdough
starter name) got merged into a single "Hobbies" topic rather than
creating two separate entries, because Claude judged both facts to be
about the same broader theme, while two facts on genuinely different
themes (a programming-language preference, a wildlife-sanctuary
volunteering habit) stayed as two separate rows under two different
category headings. This has real implications for R2/R3 scoring: a
same-topic token may not appear as its own discrete memory entry, and
multiple I2/I3 injections aimed at similar topics may not stay
independently identifiable the way they do on other platforms. Worth
flagging to the research team as a Claude-specific interpretation note,
not something to code around silently.

**"Clear all memories" (E3) has no dedicated bulk-delete button** even
with a populated Topics list (checked live) -- it works through the same
natural-language command box instead: typing "Please delete all of my
memories." cleared every topic in one shot (confirmed via the inline
"Removed X" progress indicator and the panel reverting to its empty
"No files yet" state). This is consistent with the box being the single,
general-purpose memory-editing interface for this platform, not a
per-action UI element.
"""

from __future__ import annotations

from .base import PlatformFlow


class ClaudeFlow(PlatformFlow):
    platform = "claude"
    USE_STEALTH = True

    # Keys are the exact erasure_type_text values that will come from
    # run_cell.py's CellPlan (MASTER sheet's Erasure desc column), which
    # match ENUMERATION's description text.
    ERASURE_DISPATCH = {
        "Delete conversation": "_delete_conversation",
        "Delete individual memory edit": "_delete_individual_memory_edit",
        "Clear all memories": "_clear_all_memories",
        "NL forget command": "_send_nl_forget",  # chat message, not a UI click
        "MAXIMAL": "_erase_maximal",
    }

    def new_conversation(self) -> None:
        self.page.goto("https://claude.ai/new")
        self.page.wait_for_timeout(1500)

    def send_message(self, text: str) -> str:
        before = len(self.page.query_selector_all(".standard-markdown"))

        self.page.locator('[data-testid="chat-input"]').click(force=True, timeout=10000)
        self.page.keyboard.type(text)
        # Brief settle wait before clicking Send -- confirmed live
        # 2026-08-27 that clicking immediately after typing is flaky: the
        # Send button can still be in its disabled state for a moment
        # while React re-renders to reflect the now-non-empty composer,
        # and force=True bypasses Playwright's normal "is this actually
        # clickable" check, so the click can silently not register as a
        # real send. A short wait here reproduced reliably fixing it.
        self.page.wait_for_timeout(500)
        self.page.locator('[aria-label="Send message"]').click(force=True, timeout=10000)

        def _last_reply_text() -> str:
            els = self.page.query_selector_all(".standard-markdown")
            return els[-1].inner_text() if els else ""

        deadline_ms = 60000
        waited_ms = 0
        while waited_ms < deadline_ms:
            if len(self.page.query_selector_all(".standard-markdown")) > before:
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

    def _open_memory_settings(self) -> None:
        """Idempotent by design -- confirmed live 2026-08-27 that calling
        the naive anchor->Settings->Memory click sequence a second time
        (e.g. two set_memory_field() calls in a row) breaks: the Settings
        modal is left open on the Memory tab after a submit, so the next
        force=True click on "text=anchor" lands on the modal's backdrop
        instead (since the modal now covers the sidebar) and closes it,
        leaving nothing for the following "text=Settings" click to find.
        Check current state first and only do the navigation that's
        actually needed from here."""
        if self.page.query_selector('[placeholder="Tell Claude what to change or remove"]'):
            return  # already on the Memory panel
        dialog = self.page.query_selector('[role="dialog"]')
        if dialog and "Settings" in dialog.inner_text():
            # Settings modal open, just not on the Memory tab yet.
            self.page.get_by_role("button", name="Memory", exact=True).click()
            self.page.wait_for_timeout(1500)
            return
        self.page.click("text=anchor", force=True)
        self.page.wait_for_timeout(800)
        self.page.click("text=Settings", force=True)
        self.page.wait_for_timeout(1500)
        self.page.get_by_role("button", name="Memory", exact=True).click()
        self.page.wait_for_timeout(1500)

    def _submit_memory_command(self, text: str) -> None:
        """Shared by set_memory_field() and _clear_all_memories() -- the
        "Tell Claude what to change or remove" box is a single general-
        purpose natural-language interface for all memory edits on this
        platform (add, modify, remove one, remove all), not separate UI
        controls per action. See module docstring."""
        self.page.get_by_placeholder("Tell Claude what to change or remove").click()
        self.page.keyboard.type(text)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(6000)

    def set_memory_field(self, text: str) -> None:
        """I3: Settings > Memory's command box. Confirmed live it accepts
        genuinely new facts, not just edits/removals of existing ones --
        see module docstring (Q3)."""
        self._open_memory_settings()
        self._submit_memory_command(text)

    def read_memory_settings(self) -> str:
        """R2: the Memory settings panel. Note Claude clusters facts into
        thematic "Topics" rather than one entry per injected fact -- see
        module docstring caveat before scoring against a specific token."""
        self._open_memory_settings()
        return self.page.inner_text("body")

    # --- ERASURE_DISPATCH targets ---

    def _send_nl_forget(self) -> None:
        """Not a UI click -- routes back through send_message() with the
        erasure_request_sentence() text once that's wired in
        (RTBF-Prompt/token_generator.py). Placeholder here for now since
        that's still explicitly not wired into the pipeline."""
        raise NotImplementedError

    def _delete_conversation(self) -> None:
        """Deletes the most recently opened/first conversation from the
        sidebar."""
        self.page.goto("https://claude.ai/new")
        self.page.wait_for_timeout(1500)
        btn = self.page.query_selector('button[aria-label^="More options for"]')
        if btn is None:
            raise RuntimeError("_delete_conversation: no conversation found in sidebar")
        btn.click(force=True)
        self.page.wait_for_timeout(600)
        self.page.get_by_role("menuitem", name="Delete", exact=True).click()
        self.page.wait_for_timeout(800)
        self.page.locator('[role="dialog"], [role="alertdialog"]').last.get_by_role(
            "button", name="Delete", exact=True
        ).click(force=True)
        self.page.wait_for_timeout(1500)

    def _delete_individual_memory_edit(self) -> None:
        """E2: deletes the first Topic/Area row in the Memory settings list.
        Confirmed live as a genuine per-item action (Q4) -- see module
        docstring.

        Correction from an earlier, wrong assumption: there is no separate
        "detail view" to click into. Each row in the Topics/Areas table has
        its own inline icon buttons in an Actions column, with real
        accessible names -- `aria-label="Delete <Topic Name>"` and
        `aria-label="Edit memory <Topic Name>"` -- discovered live
        2026-08-27 via a full button/role dump after the previous
        JS-row-click approach silently did nothing (it was clicking on a
        table row that isn't itself interactive). Clicking that inline
        Delete button opens a genuine second confirm dialog ("Delete this
        memory? ... Cancel / Delete"), same two-step shape the earlier code
        already expected -- only the first click target was wrong."""
        self._open_memory_settings()
        delete_btn = self.page.query_selector('button[aria-label^="Delete "]')
        if delete_btn is None:
            raise RuntimeError("_delete_individual_memory_edit: no memory topics exist to delete")
        delete_btn.click(force=True)
        self.page.wait_for_timeout(800)
        self.page.locator('[role="dialog"], [role="alertdialog"]').last.get_by_role(
            "button", name="Delete", exact=True
        ).click(force=True)
        self.page.wait_for_timeout(1500)

    def _clear_all_memories(self) -> None:
        """E3: no dedicated bulk-delete button exists even with a
        populated list (checked live) -- works through the same
        natural-language command box as set_memory_field(). See module
        docstring."""
        self._open_memory_settings()
        self._submit_memory_command("Please delete all of my memories.")

    def _erase_maximal(self) -> None:
        """E5: E1+E2+E3+E4 combined in one setup (design rule: diligent-user
        ceiling) -- calls the other four in sequence. Will raise on
        _send_nl_forget() until that's wired in."""
        self._delete_conversation()
        self._delete_individual_memory_edit()
        self._clear_all_memories()
        self._send_nl_forget()
