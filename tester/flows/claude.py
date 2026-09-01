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
        # FILE-substudy aliases -- same underlying methods, just the
        # FILE SUBSTUDY sheet's "Erasure condition" column phrases these
        # differently than MASTER's "Erasure desc" column does.
        "Delete conversation containing file": "_delete_conversation",
        "Maximal combination (all erasure mechanisms)": "_erase_maximal",
        "Delete individual memory edit": "_delete_individual_memory_edit",
        "Clear all memories": "_clear_all_memories",
        "NL forget command": "_send_nl_forget",  # chat message, not a UI click
        "MAXIMAL": "_erase_maximal",
    }

    def new_conversation(self) -> None:
        self.page.goto("https://claude.ai/new")
        self.page.wait_for_timeout(1500)

    def _last_reply_text(self) -> str:
        els = self.page.query_selector_all(".standard-markdown")
        return els[-1].inner_text() if els else ""

    def _wait_for_reply(self, before_count: int) -> str:
        """Shared by send_message() and upload_file() -- waits for a new
        .standard-markdown reply to appear, then for its text to settle
        (stop changing across 2 consecutive 1s checks) before returning
        it, since Claude streams replies in incrementally."""
        deadline_ms = 60000
        waited_ms = 0
        while waited_ms < deadline_ms:
            if len(self.page.query_selector_all(".standard-markdown")) > before_count:
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
        self.page.locator('[aria-label="Send message"]:not([disabled])').click(force=True, timeout=10000)

        return self._wait_for_reply(before)

    def upload_file(self, file_path: str, caption: str | None = None) -> str:
        """FILE-substudy cells: attach a document via the real (hidden)
        <input type="file"> found live 2026-08-28 --
        #chat-input-file-upload-onpage, directly reachable via
        set_input_files() without needing to click the "Add files"
        button first or intercept a native file-chooser dialog. Confirmed
        live: attaching produces a real visible PDF thumbnail chip in the
        composer before sending. caption=None (the default) sends the
        file with no accompanying message -- a silent upload, closest to
        "here's a doc for reference" rather than an explicit instruction
        about it."""
        before = len(self.page.query_selector_all(".standard-markdown"))

        self.page.set_input_files('#chat-input-file-upload-onpage', file_path)
        self.page.wait_for_timeout(2000)

        if caption:
            self.page.locator('[data-testid="chat-input"]').click(force=True, timeout=10000)
            self.page.keyboard.type(caption)
            self.page.wait_for_timeout(500)

        self.page.locator('[aria-label="Send message"]:not([disabled])').click(force=True, timeout=10000)
        return self._wait_for_reply(before)

    def _open_memory_settings(self) -> None:
        """Idempotent by design -- confirmed live 2026-08-27 that calling
        the naive account-switcher->Settings->Memory click sequence a
        second time (e.g. two set_memory_field() calls in a row) breaks:
        the Settings modal is left open on the Memory tab after a submit,
        so the next force=True click on the account switcher lands on the
        modal's backdrop instead (since the modal now covers the sidebar)
        and closes it, leaving nothing for the following "text=Settings"
        click to find. Check current state first and only do the
        navigation that's actually needed from here.

        The account-switcher click used to be hardcoded to "text=anchor"
        -- that's the MAIN account's own org/display name, not present on
        any dedicated MAXIMAL account (each has its own name, e.g.
        "T,Ola", "Tee"). Confirmed live 2026-09-01 this silently times out
        on every account except main. "text=Free" is the actually stable,
        portable label across every account's plan badge -- use that
        instead. It can match 2+ elements and land slightly outside the
        viewport depending on window size, so click via JS (bypasses
        Playwright's viewport-visibility check) rather than a normal
        click()."""
        if self.page.query_selector('[placeholder="Tell Claude what to change or remove"]'):
            return  # already on the Memory panel
        dialog = self.page.query_selector('[role="dialog"]')
        if dialog and "Settings" in dialog.inner_text():
            # Settings modal open, just not on the Memory tab yet.
            self.page.get_by_role("button", name="Memory", exact=True).click()
            self.page.wait_for_timeout(1500)
            return

        # Direct deep-link first -- confirmed live 2026-09-01 that the
        # click-through path (account-switcher -> Settings -> Memory tab)
        # intermittently crashes the whole page ("This page ran into a
        # problem") on at least one dedicated MAXIMAL account, while
        # goto()'ing the route directly loads cleanly every time on that
        # same account. Falls back to the click-through path only if the
        # direct nav doesn't land on the panel (e.g. an account/session
        # state where the deep link redirects elsewhere).
        self.page.goto("https://claude.ai/new#settings/memory")
        self.page.wait_for_timeout(2000)
        if self.page.query_selector('[placeholder="Tell Claude what to change or remove"]'):
            return

        free_el = self.page.query_selector("text=Free")
        if free_el is None:
            raise RuntimeError("_open_memory_settings: account-switcher 'Free' label not found")
        free_el.evaluate("el => el.click()")
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

    def set_memory_field(self, text: str) -> str | None:
        """I3: Settings > Memory's command box. Confirmed live it accepts
        genuinely new facts, not just edits/removals of existing ones --
        see module docstring (Q3).

        Returns the newly-created Topic row's exact aria-label suffix
        (e.g. "Jigsaw Puzzle"), captured by diffing the Delete-button list
        before/after submitting -- needed because Claude's Topic rows show
        an AI-generated paraphrase ("The user's jigsaw puzzle... and its
        name"), never the literal injected token (confirmed live
        2026-08-31), so later erasure can't find this cell's own row by
        substring-matching the token the way ChatGPT's custom-instructions
        field allows. Returns None if the fact merged into an EXISTING
        topic instead of creating a new one (module docstring's "Hobbies"
        merge finding) -- that case has no clean single-row target and
        must be surfaced, not guessed at."""
        self._open_memory_settings()
        before = {
            b.get_attribute("aria-label")
            for b in self.page.query_selector_all('button[aria-label^="Delete "]')
        }
        self._submit_memory_command(text)
        self._open_memory_settings()
        after = self.page.query_selector_all('button[aria-label^="Delete "]')
        new_labels = [b.get_attribute("aria-label") for b in after if b.get_attribute("aria-label") not in before]
        if len(new_labels) == 1:
            return new_labels[0]
        return None  # no new topic row (likely merged into an existing one) -- erasure must be told explicitly

    def read_memory_settings(self) -> str:
        """R2: the Memory settings panel. Note Claude clusters facts into
        thematic "Topics" rather than one entry per injected fact -- see
        module docstring caveat before scoring against a specific token."""
        self._open_memory_settings()
        return self.page.inner_text("body")

    # --- ERASURE_DISPATCH targets ---

    def _send_nl_forget(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        """Not a UI click -- routes back through send_message() with the
        erasure_request_sentence() text once that's wired in
        (RTBF-Prompt/token_generator.py). Placeholder here for now since
        that's still explicitly not wired into the pipeline."""
        raise NotImplementedError

    def _delete_conversation(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        """Deletes THIS cell's own conversation, identified by `ref` (the
        exact conversation URL captured at injection time). Confirmed live
        2026-08-31 that grabbing "whatever's topmost in the sidebar" (the
        old behavior) deletes a sibling cell's conversation instead,
        whenever this account has been used more recently for another
        cell -- always true once cells share an account. The sidebar's
        "More options for <title>" button has no href of its own, so it's
        found by walking up from the matching conversation link to its row
        container (verified live: 2 levels up from the `<a>`) and querying
        within that specific row, not page-wide. When `ref` is missing
        (legacy tracking data from before ref capture existed), searches
        every conversation's content for `token` instead of guessing --
        see _find_conversation_by_token(). Falls back to topmost only if
        that search also finds nothing (a cell with no owned conversation
        at all, e.g. an I3 cell using a conversation-delete as a cross-
        mechanism probe)."""
        self.page.goto("https://claude.ai/new")
        self.page.wait_for_timeout(1500)
        if not ref:
            ref = self._find_conversation_by_token(token, "https://claude.ai", 'a[href^="/chat/"]')
        if ref:
            from urllib.parse import urlsplit
            link = self.page.query_selector(f'a[href="{urlsplit(ref).path}"]')
            if link is None:
                raise RuntimeError(f"_delete_conversation: expected conversation {ref!r} not found in sidebar")
            btn = link.evaluate_handle(
                """el => {
                    let cur = el;
                    for (let i = 0; i < 6 && cur; i++) {
                        const b = cur.querySelector && cur.querySelector('button[aria-label^="More options for"]');
                        if (b) return b;
                        cur = cur.parentElement;
                    }
                    return null;
                }"""
            ).as_element()
        else:
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

    def _delete_individual_memory_edit(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        """E2: deletes THIS cell's own Topic/Area row, identified by `ref`
        (the exact "Delete <Topic Name>" aria-label captured at injection
        time by set_memory_field()'s before/after diff). Confirmed live
        2026-08-31 that grabbing "the first Topic row" (the old behavior)
        can just as easily delete an unrelated sibling cell's topic --
        Claude's Topic rows never show the literal injected token (an
        AI-generated paraphrase instead, e.g. "The user's jigsaw puzzle...
        and its name"), so there's no safe way to guess the right row
        without the diff-captured ref. Raises if `ref` is None (the fact
        merged into an existing topic at injection time, or this is
        stale pre-fix tracking data) rather than guessing.

        Confirmed live as a genuine per-item action (Q4) -- see module
        docstring. Correction from an earlier, wrong assumption: there is
        no separate "detail view" to click into. Each row in the
        Topics/Areas table has its own inline icon buttons in an Actions
        column, with real accessible names -- `aria-label="Delete <Topic
        Name>"` and `aria-label="Edit memory <Topic Name>"` -- discovered
        live 2026-08-27 via a full button/role dump after the previous
        JS-row-click approach silently did nothing (it was clicking on a
        table row that isn't itself interactive). Clicking that inline
        Delete button opens a genuine second confirm dialog ("Delete this
        memory? ... Cancel / Delete"), same two-step shape the earlier code
        already expected -- only the first click target was wrong."""
        self._open_memory_settings()
        if ref is None and injection_text:
            # Fallback for legacy tracking data (pre-dates ref capture):
            # Claude's Topic label (e.g. "Jigsaw Puzzle") is never the
            # literal token, but is reliably a substring of this cell's
            # own injection_text (e.g. "a jigsaw puzzle on the coffee
            # table is called ..." -- confirmed live 2026-08-31 across
            # every I3 cell checked). Match on that instead of guessing.
            candidates = [
                b.get_attribute("aria-label")
                for b in self.page.query_selector_all('button[aria-label^="Delete "]')
                if b.get_attribute("aria-label")[len("Delete "):].lower() in injection_text.lower()
            ]
            if len(candidates) == 1:
                ref = candidates[0]
        if ref is None:
            raise RuntimeError(
                "_delete_individual_memory_edit: no injection-time ref for this cell's "
                "own Topic row, and no unambiguous label match against injection_text "
                "(either it merged into an existing topic, or this is stale pre-fix "
                "tracking data with no injection_text label match) -- can't safely "
                "pick a row without one."
            )
        delete_btn = self.page.query_selector(f'button[aria-label="{ref}"]')
        if delete_btn is None:
            raise RuntimeError(f"_delete_individual_memory_edit: expected topic {ref!r} not found")
        delete_btn.click(force=True)
        self.page.wait_for_timeout(800)
        self.page.locator('[role="dialog"], [role="alertdialog"]').last.get_by_role(
            "button", name="Delete", exact=True
        ).click(force=True)
        self.page.wait_for_timeout(1500)

    def _clear_all_memories(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        """Deliberately account-wide/blanket -- see [[project-destructive-actions-run-last]].
        `token`/`injection_text`/`ref` accepted for interface consistency
        but unused: this mechanism has no narrower real-product equivalent.
        E3: no dedicated bulk-delete button exists even with a
        populated list (checked live) -- works through the same
        natural-language command box as set_memory_field(). See module
        docstring."""
        self._open_memory_settings()
        self._submit_memory_command("Please delete all of my memories.")

    def _erase_maximal(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        """E5: E1+E2+E3+E4 combined in one setup (design rule: diligent-user
        ceiling) -- calls the other four in sequence. Will raise on
        _send_nl_forget() until that's wired in."""
        self._delete_conversation(token=token, injection_text=injection_text, ref=ref)
        self._delete_individual_memory_edit(token=token, injection_text=injection_text, ref=ref)
        self._clear_all_memories(token=token, injection_text=injection_text, ref=ref)
        self._send_nl_forget()
