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

    # DECISIONS Q7 confirmed live: this Free-tier test account is 403'd
    # out of Memory entirely -- read_memory_settings() was never
    # implemented (correctly) since there's nothing reachable to read.
    # Without this override, base.py's default HAS_MEMORY_UI = True would
    # make any caller that checks it (e.g. the FILE substudy's
    # _verify_file_injection() in run_cell.py) call
    # read_memory_settings() and hit its NotImplementedError instead of
    # skipping it cleanly -- same pattern as deepseek.py's own (genuinely
    # memory-feature-less) HAS_MEMORY_UI = False.
    HAS_MEMORY_UI = False

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
        # FILE-substudy aliases -- see flows/claude.py's ERASURE_DISPATCH
        # for why these exist. MAXIMAL's alias hits the same Q7 tier-gate
        # block as the main battery's PE-*-E6 cells (calls memory-clear
        # methods that are NotImplementedError on this Free-tier account).
        "Delete conversation containing file": "_delete_single_thread",
        "Maximal combination (all erasure mechanisms)": "_erase_maximal",
        "Delete single thread": "_delete_single_thread",
        "Delete all threads": "_delete_all_threads",
        "Delete individual memory": "_delete_individual_memory",
        "Clear all memories": "_clear_all_memories",
        "MAXIMAL": "_erase_maximal",
    }

    def _dismiss_cookie_banner(self) -> None:
        """A cookie-consent banner renders on top of the composer on a
        freshly loaded session -- confirmed live 2026-08-27 it can
        intercept clicks if not dismissed first. Defensive no-op if
        already dismissed (matches deepseek.py's pattern for the same
        kind of banner).

        Fixed 2026-09-09: Perplexity changed the banner's wording since
        2026-08-27 -- confirmed live it now reads "Decline optional" /
        "Got it", not "Allow all". The old selector matched nothing, so
        this silently no-op'd, leaving the banner up -- confirmed live
        this caused `_send_nl_forget()`/`send_message()`'s `force=True`
        Submit click to land on the banner instead of the real button
        (same collision class as DeepSeek's cookie-banner/send-button
        bug): the erasure message never actually sent, and
        `_wait_for_reply()` correctly timed out waiting for a reply that
        was never going to come. Matches on "Got it" now; kept "Allow
        all" too in case the wording reverts or A/B-tests back."""
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
        """Composer is a contenteditable div (#ask-input, not a <textarea>),
        confirmed live via a full DOM dump -- aria-placeholder="Ask
        anything...". The Submit button doesn't exist in the DOM until
        the composer has content (aria-label="Submit" appears only after
        typing). Submitting navigates to a new /search/<id> URL and
        streams the answer into a `[class*="prose"]` element -- polling
        for that count to increase, then for its text to stabilize,
        mirrors the pattern already proven on claude.py/chatgpt.py."""
        self._dismiss_cookie_banner()
        before = len(self._top_level_reply_texts())

        self.page.locator('#ask-input').click(force=True)
        self.page.keyboard.type(text)
        self.page.wait_for_timeout(500)
        self.page.locator('button[aria-label="Submit"]').click(force=True)

        return self._wait_for_reply(before)

    # Bug found live 2026-09-07: `[class*="prose"]` matches nested elements
    # too, not just the top-level answer container -- a single multi-item
    # answer (e.g. a bulleted list read back from an uploaded file) renders
    # as ONE outer match plus one match per list item, all sharing a class
    # containing "prose". The old `els[-1]` picked the LAST of that flat
    # list, which for a multi-item answer is just the tail list item, not
    # the full answer -- silently truncating captured replies whenever an
    # answer has more than one paragraph/list item. Caught on `PE-IF-E-CONV`:
    # the real answer contained the injected token, but `_last_reply_text()`
    # returned only "Look into new phone case options." (the last list
    # item), producing a false-negative token-not-found and triggering an
    # unnecessary (and separately broken) forced-read fallback. Fixed by
    # filtering to only elements not contained within another match, then
    # taking the last of those -- the actual top-level answer container.
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

    def _last_reply_text(self) -> str:
        texts = self._top_level_reply_texts()
        return texts[-1] if texts else ""

    def _wait_for_reply(self, before_count: int) -> str:
        """Shared by send_message() and upload_file()."""
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

        return self._last_reply_text()

    def upload_file(self, file_path: str, caption: str | None = None) -> str:
        """FILE-substudy cells: attach a document via the real (hidden)
        <input type="file"> found live 2026-08-28 -- directly reachable
        via set_input_files(), no need to click "Add files or tools"
        first. .pdf is in its accept list. Unlike Claude/ChatGPT/Copilot/
        Gemini, send_message()'s own docstring notes the Submit button
        doesn't exist in the DOM until the composer has TEXT content --
        confirm live whether attaching a file alone is enough before
        trusting caption=None works the same way here."""
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
        in the same conversation as the disclosure. Not blocked by Q7's
        tier gate -- this is a plain chat message, no memory-API call."""
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
        """E2: confirmed live 2026-08-27, genuinely distinct from
        _delete_all_threads() (Q11) -- see module docstring. Deletes THIS
        cell's own thread ("Session" in the UI's own terminology) from
        /library via its per-row "Session options" menu -> Delete, then a
        real confirm dialog ("Delete session? ... Delete/Cancel").

        Fixed 2026-09-08 (was topmost-only, opt_btns[0], since 2026-08-27
        -- flagged but not fixed at the time since no erasure had run yet
        on this now-shared account; see PROJECT_STATUS.md/memory for the
        "genuinely deletes whatever's topmost" writeup). Same ref-then-
        token pattern as claude.py/chatgpt.py's _delete_conversation:
        `ref` (the exact /search/<uuid> URL captured at injection) is
        matched against each row's own link href first -- confirmed live
        2026-09-08 this is NECESSARY, not just tidier, for the FILE
        substudy cell specifically: /library shows several identically-
        titled "PE-IF-E-CONV.pdf" rows (stray conversations from earlier
        upload retries), so title-text matching alone can't disambiguate
        them, only the ref URL can. Falls back to a token/injection_text
        substring match against each row's own visible title text (shown
        verbatim in /library, confirmed live -- unlike Claude's
        paraphrased Topics) only when `ref` is None (legacy tracking
        data), same as every other platform's equivalent method."""
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
        """E3: confirmed live 2026-08-27, genuinely distinct from
        _delete_single_thread() (Q11) -- see module docstring. Selects
        every thread via /library's bulk "Session selection options" menu
        -> "All" (a select-mode toggle, not itself a delete action), then
        the resulting selection toolbar's "Delete" button, then a real
        confirm dialog ("Delete N sessions? ... Delete/Cancel"). Verified
        with a persistence check (all threads gone, "No sessions yet"
        after a reload).

        Fixed 2026-09-09: PE-I1-E3/PE-I2-E3 share this identical blanket
        action on the same account, so running it once for real (via
        PE-I1-E3) genuinely satisfies both -- confirmed live, "No sessions
        yet" afterward. Running it a second time for PE-I2-E3 hit an
        already-empty account with no "Session selection options" button
        to click, indistinguishable from a real failure until now. Checks
        for the empty-state message first and treats it as a legitimate
        no-op (nothing to delete IS the correct outcome here, same as
        Gemini's _delete_all_saved_info fix), not an error."""
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
        """E4: blocked, not just unimplemented -- DECISIONS Q7 confirmed
        live 2026-08-27 that this Free-plan test account can't reach
        Memory at all (403 Forbidden on the underlying settings requests).
        See read_memory_settings(). Permanently out of scope, confirmed
        2026-09-07 -- no plan to upgrade off free tier."""
        raise NotImplementedError

    def _clear_all_memories(
        self, token: str | None = None, injection_text: str = "", ref: str | None = None
    ) -> None:
        """E5: same Q7 tier-gate block as _delete_individual_memory() --
        see read_memory_settings(). Permanently out of scope, confirmed
        2026-09-07."""
        raise NotImplementedError

    def _erase_maximal(
        self, token: str | None = None, injection_text: str = "", ref: str | None = None
    ) -> None:
        """E6: all singles combined in one setup (design rule). Will raise
        on the Q7-tier-gated memory steps (E4/E5, permanently out of
        scope) -- E2/E3 (thread deletion) and E1 (_send_nl_forget, now
        wired) are the pieces of this that work standalone; the whole
        combination still can't complete while E4/E5 are blocked."""
        raise NotImplementedError
