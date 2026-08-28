"""Perplexity flow (perplexity.ai). All 12 MASTER rows for this platform
started as `VERIFY` status (not `LOCKED` like every other platform's
starting point) with all 5 gating DECISIONS questions (Q7-Q11) unanswered
-- the least-confirmed platform in the project going in. Q7 and Q11 are
now confirmed live (2026-08-27); Q8/Q9/Q10 remain open, but they gate
memory-dependent surfaces (I1/I2/E4/E5) that are moot for this account
anyway (see Q7 below) until it's upgraded off Free.

**Q7 CONFIRMED (blocks everything memory-related)**: this test account
(Anchor Experiments, Free plan) is tier-gated out of Memory entirely --
Settings > Customize > Memory throws a generic "Internal Error" in the
UI, but the underlying network requests reveal the real cause: GET
.../rest/sse/computer/memory/digest-settings and GET
.../rest/computer/memory/dream-settings/enabled-flags both return 403
Forbidden. DECISION (2026-08-27, user): do not upgrade to Pro for this --
build only what Free tier supports (send_message/new_conversation, E2/E3
thread deletion). I1/I2/E4/E5/R2 (all memory-dependent) stay unbuilt and
`raise NotImplementedError` with this cited, not guessed at.

**Q11 CONFIRMED (blocks E2/E3)**: single-thread delete and all-threads
delete are genuinely separate actions, not two names for the same thing.
Both live at /library, which the product itself calls "Sessions" (not to
be confused with the sidebar's unrelated, and apparently unused,
"Sessions" panel that stayed empty throughout testing -- a different
feature). Verified live with real persistence checks: single delete via
a per-row "Session options" menu (10 -> 9 threads), bulk delete via a
"Session selection options" -> "All" -> toolbar "Delete" flow (9 -> 0,
"No sessions yet"). Each has its own distinct confirm dialog wording
("Delete session?" vs "Delete N sessions?").

**Session capture and a genuinely new Cloudflare wrinkle**: cookie-export
alone (import_exported_cookies.py) is sufficient to authenticate -- no
localStorage needed. But /library specifically (not the homepage, not
/search/<id> conversation pages) kept hitting Cloudflare's "Performing
security verification" challenge even with a fully valid, authenticated
session -- this is the same wall that forced an earlier work session to
pause and cool down (see PROJECT_STATUS.md's "Perplexity live selector
work" section for that history). Confirmed live 2026-08-27 that
`playwright-stealth` (see flows/claude.py and flows/base.py's
USE_STEALTH flag for the full backstory on that package) resolves it --
/library loads cleanly with USE_STEALTH = True here. Unlike Claude's
block, this one was route-specific (homepage was always fine) and had
partially self-resolved once already after a cooldown, so it may be a
hybrid of rate-based flagging and a fingerprint check rather than purely
one or the other -- stealth is the fix in practice either way.

Still open, not yet resolved:
- Q8 (blocks I1): does a single conversational mention persist, or is
  there a repetition gate requiring the disclosure to be sent more than
  once? Moot until the account has Memory access (Q7).
- Q9 (blocks I2): does an explicit "remember this" instruction reliably
  persist? Same Q7 dependency.
- Q10 (scope decision): Perplexity Spaces in or out? Default leans CUT
  (workspace feature, weak personal-memory claim) -- still needs explicit
  user sign-off, not silently decided.
- The possible 30-day retention log of *cleared* memories mentioned in
  early design docs was never checked -- moot until Q7 is revisited too.
"""

from __future__ import annotations

from .base import PlatformFlow


class PerplexityFlow(PlatformFlow):
    platform = "perplexity"

    # Trying this 2026-08-27 after /library specifically (not the homepage)
    # kept hitting Cloudflare's "Performing security verification" challenge
    # even with a valid session -- same wall hit before the earlier cooldown
    # pause. Prior diagnosis called this velocity/rate-based, distinct from
    # Claude's persistent per-navigation fingerprint check that stealth
    # fixed -- flip this back to False if /library still fails with stealth
    # on, since that would confirm it's really rate-based, not a fingerprint
    # check stealth can address.
    USE_STEALTH = True

    # Set once I2's real target is confirmed live -- default (empty) means
    # I2 routes to send_message() like Claude/ChatGPT/Copilot; add "I2"
    # here if it turns out to target a dedicated field instead, like
    # Gemini's does.
    MEMORY_FIELD_INJECTION_TYPES: set[str] = set()

    # Keys are the exact erasure_type_text values from CellPlan (MASTER
    # sheet's Erasure desc column). Don't trust these exist as described
    # until confirmed live -- Q11 specifically questions whether E2/E3 are
    # really separate actions.
    ERASURE_DISPATCH = {
        "NL forget prompt": "_send_nl_forget",  # chat message, not a UI click
        "Delete single thread": "_delete_single_thread",
        "Delete all threads": "_delete_all_threads",
        "Delete individual memory": "_delete_individual_memory",
        "Clear all memories": "_clear_all_memories",
        "MAXIMAL": "_erase_maximal",
    }

    def _dismiss_cookie_banner(self) -> None:
        """A cookie-consent banner ("Allow all" / "Only necessary") renders
        on top of the composer on a freshly loaded session -- confirmed
        live 2026-08-27 it can intercept clicks if not dismissed first.
        Defensive no-op if already dismissed (matches deepseek.py's
        pattern for the same kind of banner)."""
        btn = self.page.query_selector('button:has-text("Allow all")')
        if btn:
            btn.click(force=True)
            self.page.wait_for_timeout(500)

    def new_conversation(self) -> None:
        self.page.goto("https://www.perplexity.ai/")
        self.page.wait_for_timeout(1500)
        self._dismiss_cookie_banner()

    def send_message(self, text: str) -> str:
        """Composer is a contenteditable div (#ask-input, not a <textarea>),
        confirmed live via a full DOM dump -- aria-placeholder="Ask
        anything...". The Submit button doesn't exist in the DOM until
        the composer has content (aria-label="Submit" appears only after
        typing). Submitting navigates to a new /search/<id> URL and
        streams the answer into a `[class*="prose"]` element -- polling
        for that count to increase, then for its text to stabilize,
        mirrors the pattern already proven on claude.py/chatgpt.py."""
        self._dismiss_cookie_banner()
        before = len(self.page.query_selector_all('[class*="prose"]'))

        self.page.locator('#ask-input').click(force=True)
        self.page.keyboard.type(text)
        self.page.wait_for_timeout(500)
        self.page.locator('button[aria-label="Submit"]').click(force=True)

        def _last_reply_text() -> str:
            els = self.page.query_selector_all('[class*="prose"]')
            return els[-1].inner_text() if els else ""

        deadline_ms = 60000
        waited_ms = 0
        while waited_ms < deadline_ms:
            if len(self.page.query_selector_all('[class*="prose"]')) > before:
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
        """Only used if I2 turns out to target a field, not chat -- confirm
        live before implementing, see module docstring."""
        raise NotImplementedError

    def read_memory_settings(self) -> str:
        """R2: DECISIONS Q7 confirmed live 2026-08-27 that this test
        account (Free plan) is tier-gated out of Memory entirely --
        Settings > Customize > Memory throws a generic "Internal Error"
        while the underlying requests return 403 Forbidden. Standing
        decision: don't upgrade to Pro for this: I1/I2/E4/E5/R2 (all
        memory-dependent) stay unbuilt and documented as tier-gated until
        the account is upgraded, if ever."""
        raise NotImplementedError

    # --- ERASURE_DISPATCH targets ---

    def _send_nl_forget(self) -> None:
        """Not a UI click -- routes back through send_message() with the
        erasure_request_sentence() text once that's wired in
        (RTBF-Prompt/token_generator.py). Placeholder for now, same as
        every other platform's equivalent method."""
        raise NotImplementedError

    def _delete_single_thread(self) -> None:
        """E2: confirmed live 2026-08-27, genuinely distinct from
        _delete_all_threads() (Q11) -- see module docstring. Deletes the
        most recent thread ("Session" in the UI's own terminology) from
        /library via its per-row "Session options" menu -> Delete, then a
        real confirm dialog ("Delete session? ... Delete/Cancel").
        Verified with a persistence check (thread count decreased by
        exactly 1 across a reload)."""
        self.page.goto("https://www.perplexity.ai/library")
        self.page.wait_for_timeout(2000)
        opt_btns = self.page.query_selector_all('button[aria-label="Session options"]')
        if not opt_btns:
            raise RuntimeError("_delete_single_thread: no sessions found to delete")
        opt_btns[0].click(force=True)
        self.page.wait_for_timeout(500)
        self.page.get_by_role("menuitem", name="Delete", exact=True).click()
        self.page.wait_for_timeout(800)
        self.page.locator('[role="dialog"], [role="alertdialog"]').last.get_by_role(
            "button", name="Delete", exact=True
        ).click(force=True)
        self.page.wait_for_timeout(1000)

    def _delete_all_threads(self) -> None:
        """E3: confirmed live 2026-08-27, genuinely distinct from
        _delete_single_thread() (Q11) -- see module docstring. Selects
        every thread via /library's bulk "Session selection options" menu
        -> "All" (a select-mode toggle, not itself a delete action), then
        the resulting selection toolbar's "Delete" button, then a real
        confirm dialog ("Delete N sessions? ... Delete/Cancel"). Verified
        with a persistence check (all threads gone, "No sessions yet"
        after a reload)."""
        self.page.goto("https://www.perplexity.ai/library")
        self.page.wait_for_timeout(2000)
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

    def _delete_individual_memory(self) -> None:
        """E4: blocked, not just unimplemented -- DECISIONS Q7 confirmed
        live 2026-08-27 that this Free-plan test account can't reach
        Memory at all (403 Forbidden on the underlying settings requests).
        See read_memory_settings()."""
        raise NotImplementedError

    def _clear_all_memories(self) -> None:
        """E5: same Q7 tier-gate block as _delete_individual_memory() --
        see read_memory_settings()."""
        raise NotImplementedError

    def _erase_maximal(self) -> None:
        """E6: all singles combined in one setup (design rule). Will raise
        on both the Q7-tier-gated memory steps and _send_nl_forget() (pipeline
        wiring) until those are resolved -- E2/E3 (thread deletion) are the
        only pieces of this that currently work standalone."""
        raise NotImplementedError
