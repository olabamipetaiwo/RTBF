"""Shared interface every platform flow implements. The session-loading
mechanics here are generic and don't depend on any platform's DOM, so
they're real and testable now. The per-platform subclasses (selectors,
button sequences) are not -- they need real investigation against each
live site and are stubbed with TODOs, not guessed at."""

from __future__ import annotations

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

import config


class PlatformFlow:
    platform: str = ""  # set by subclass, must match a key in config.PLATFORMS

    # R2 = N/A for DeepSeek (no memory settings UI exists at all, per
    # ENUMERATION). Subclasses without a memory-settings surface should set
    # this False instead of implementing read_memory_settings().
    HAS_MEMORY_UI: bool = True

    # cell_id / erasure_desc -> bound method, populated by subclasses.
    # Keyed on the exact erasure_desc string from CellPlan (run_cell.py),
    # e.g. "Delete conversation", "Clear all memories". Many cells share
    # the same erasure action, so this is dispatch-by-erasure-type, not
    # one branch per cell -- see the technical-audit plan for why.
    ERASURE_DISPATCH: dict[str, str] = {}  # erasure_desc -> method name

    # Which injection_type values route to set_memory_field() instead of
    # send_message(). Defaults to {"I3"} (Claude/ChatGPT: I3 is a settings
    # field, I1/I2 are both chat-based) -- Gemini overrides this to {"I2"}
    # since its I2 ("personal context injection") targets the Saved-info
    # field, not chat, confirmed live 2026-08-27. Don't assume the same
    # injection-type label means the same UI surface across platforms.
    MEMORY_FIELD_INJECTION_TYPES: set[str] = {"I3"}

    # Opt-in per platform. Claude's Cloudflare check rejected every
    # Playwright-driven browser regardless of engine (confirmed live
    # 2026-08-27: real Chrome AND Firefox both hit the identical challenge,
    # ruling out a CDP-specific signal -- this is a broader automation
    # fingerprint check, e.g. navigator.webdriver and similar). Applying
    # playwright-stealth's patches resolved it. The other 5 platforms
    # already work without this (cookie-export session capture was
    # sufficient there), so this defaults off -- only flip it on for a
    # platform that's actually been confirmed to need it, don't apply it
    # blanket "just in case."
    USE_STEALTH: bool = False

    def __init__(self, headless: bool = False, session_label: str | None = None):
        session = config.session_path(self.platform, session_label)
        if not session.exists():
            label_hint = f" --label {session_label}" if session_label else ""
            raise FileNotFoundError(
                f"No saved session for {self.platform!r}"
                f"{f' (label {session_label!r})' if session_label else ''} -- run "
                f"`python login_setup.py {self.platform}{label_hint}` first."
            )
        self._session_path = session
        self._headless = headless
        self._playwright = None
        self._browser = None
        self._context = None
        self.page = None

    def __enter__(self):
        try:
            self._playwright = sync_playwright().start()
            # headless=False + channel="chrome" (real Chrome, not bundled
            # Chromium) by default -- confirmed live 2026-08-27 on ChatGPT that
            # bundled headless Chromium gets stuck on Cloudflare's "verify you
            # are human" check even with valid session cookies, while real
            # Chrome headed passes straight through. Don't flip this to
            # headless=True without re-verifying per platform.
            self._browser = self._playwright.chromium.launch(headless=self._headless, channel="chrome")
            self._context = self._browser.new_context(storage_state=str(self._session_path))
            if self.USE_STEALTH:
                Stealth().apply_stealth_sync(self._context)
            self.page = self._context.new_page()
            self.page.goto(config.PLATFORMS[self.platform], wait_until="domcontentloaded")
            # The sidebar/layout has an opacity+width transition on load that
            # intercepts pointer events on anything underneath it even after
            # Playwright reports the target as visible/stable -- confirmed live
            # 2026-08-27 (both the account-menu button and the composer's send
            # button got hit by this). Let it finish before any subclass method
            # tries to click something.
            self.page.wait_for_timeout(2500)
            self._verify_logged_in()
        except Exception:
            # __exit__ is never called if __enter__ raises (context-manager
            # protocol), so anything already launched above (browser,
            # playwright driver) would otherwise leak for the rest of this
            # process's life. Confirmed live 2026-09-17: a leaked driver
            # from a _verify_logged_in() failure corrupted the very next
            # sync_playwright().start() call in the same process ("using
            # Playwright Sync API inside the asyncio loop"), crashing the
            # whole scheduler. Clean up whatever got created before
            # re-raising so the caller sees a normal failure, not a
            # process-wide corruption.
            if self._browser:
                self._browser.close()
            if self._playwright:
                self._playwright.stop()
            raise
        return self

    def _verify_logged_in(self) -> None:
        """No-op by default -- override per platform once its logged-out
        state's selector is confirmed live. Without this, a dead/expired
        session silently runs every action as an anonymous user: the page
        loads fine, the UI responds (sometimes even with a plausible-
        looking fabricated "success" reply), and nothing raises -- so the
        scheduler logs a false OK instead of a failure, and the real
        account is never touched. Confirmed live 2026-09-17 on Gemini:
        20 NL-forget erasure cells ran clean against a logged-out session
        before anyone noticed, each one scored as erased when none of them
        touched the real account at all. See `tester/accounts.md`'s
        nlforget section."""
        pass

    # Substrings that mean the platform never actually engaged with the
    # erasure request -- a rate limit, a paywall, or a generic service
    # hiccup, not a real answer (even a refusal like "I can't delete that"
    # is a real answer and must NOT match here -- see the docstring on
    # assert_real_answer()). Lowercased, checked as substrings. Confirmed
    # live 2026-09-17: Claude hit a hard session-limit paywall
    # ("Upgrade to keep chatting") on one NL-forget cell and Copilot
    # returned "I'm sorry, I'm having trouble responding to requests right
    # now" on several -- both got silently logged as a successful erasure
    # before this check existed, because send_message() only confirms
    # SOME reply text appeared and stabilized, never what it says.
    NON_ANSWER_SUBSTRINGS: tuple[str, ...] = (
        "having trouble responding",
        "try again in a bit",
        "try this again in a bit",
        "upgrade to keep chatting",
        "message limit",
        "session limit",
        "rate limit",
        "too many requests",
        "you've reached your limit",
        "hit your",
        "high demand",
        "over capacity",
        "at capacity",
        "something went wrong",
    )

    def assert_real_answer(self, reply: str) -> None:
        """Call this on every reply captured for an erasure action before
        treating it as a success. A REFUSAL ("I don't have the ability to
        delete stored data") is a real answer -- that's genuine data about
        how the platform handles the request, and must be counted as
        erased/attempted, not retried. Only a non-answer (rate limit,
        paywall, generic service error, or no text captured at all) fails
        this check, because there the platform never actually processed
        the request -- retry later, don't score it either way."""
        text = (reply or "").strip()
        if not text:
            raise RuntimeError("assert_real_answer: no reply text captured -- not a real answer")
        lower = text.lower()
        hit = next((s for s in self.NON_ANSWER_SUBSTRINGS if s in lower), None)
        if hit:
            raise RuntimeError(f"assert_real_answer: reply looks like a non-answer (matched {hit!r}), not a real answer: {text[:200]!r}")

    def __exit__(self, *exc):
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    # --- Interface every platform flow must implement ---
    # None of these have real selectors yet. Filling them in requires
    # actually driving a live, logged-in session per platform and is not
    # something to guess at from outside.

    def new_conversation(self) -> None:
        """Start a fresh chat/conversation in the current session (for
        cross-session recall probes)."""
        raise NotImplementedError

    def send_message(self, text: str) -> str:
        """Type `text` into the chat input, submit, and return the
        platform's response text. Used for injection (I1/I2), erasure (the
        13 NL-forget cells), and R1/R3 recall probes -- all the same
        mechanical action, different text."""
        raise NotImplementedError

    def set_memory_field(self, text: str) -> str | None:
        """I3 cells: fill the settings/custom-instructions field instead of
        the chat stream. Returns a durable ref identifying THIS cell's own
        entry for later targeted erasure (e.g. the exact new list-item
        label), or None when the surface is a single free-text field where
        the cell's own token is enough to find its line later (see
        ChatGPT's implementation) -- required wherever the visible entry
        doesn't literally contain the injected token (see Claude's
        implementation, whose Memory UI shows an AI-generated paraphrase,
        never the verbatim text)."""
        raise NotImplementedError

    def upload_file(self, file_path: str, caption: str | None = None) -> str:
        """FILE-substudy cells: attach a document instead of typing."""
        raise NotImplementedError

    def erase_via_ui(
        self,
        erasure_desc: str,
        token: str,
        injection_text: str,
        ref: str | None = None,
        erasure_request_text: str | None = None,
    ) -> None:
        """Dispatches to the matching method in ERASURE_DISPATCH by the
        exact erasure_desc string (e.g. "Delete conversation") -- shared
        base implementation, subclasses populate ERASURE_DISPATCH instead
        of overriding this. Many cells share the same erasure action, so
        this is one lookup, not one branch per cell_id.

        `token` (this cell's own anchor text) and `ref` (this cell's own
        conversation URL, captured at injection time -- None for a
        settings-field injection) are forwarded to every dispatched
        method so a "delete THIS cell's own conversation/entry" method can
        target precisely instead of grabbing whatever's topmost/first on
        a shared account. Confirmed live 2026-08-31 that grabbing
        "topmost in sidebar" silently deletes a sibling cell's data
        instead -- every narrow (non-account-wide) erasure method must
        accept and use these, even if a given platform's method doesn't
        need one of them. Broad/account-wide methods (Clear all memories,
        MAXIMAL, etc.) may ignore both -- they're deliberately blanket.

        `erasure_request_text` (added 2026-09-07, wiring in the
        NL-forget-prompt cells) is only non-None for the 13
        blocked_on_prompt_set cells' "NL forget prompt"/"NL forget
        command" erasure_desc -- precomputed by token_generator.py,
        forwarded only to _send_nl_forget(). Passed conditionally, not
        unconditionally like token/injection_text/ref, so every OTHER
        erasure method across all 6 platforms keeps its existing
        signature unchanged -- they'd never receive it anyway."""
        method_name = self.ERASURE_DISPATCH.get(erasure_desc)
        if method_name is None:
            raise NotImplementedError(
                f"{type(self).__name__} has no ERASURE_DISPATCH entry for "
                f"{erasure_desc!r}. Known: {list(self.ERASURE_DISPATCH)}"
            )
        kwargs = {"token": token, "injection_text": injection_text, "ref": ref}
        if erasure_request_text is not None:
            kwargs["erasure_request_text"] = erasure_request_text
        getattr(self, method_name)(**kwargs)

    def _find_conversation_by_token(self, token: str, base_url: str, link_selector: str) -> str | None:
        """Fallback for erasure methods when `ref` is missing (legacy
        tracking data from before injection-time ref capture existed,
        2026-08-31) -- searches every sidebar conversation's actual
        content for `token` instead of defaulting to "whatever's topmost"
        (confirmed live that guessing wrong silently deletes a sibling
        cell's conversation). Opens each conversation in turn and checks
        its visible text, since sidebar titles alone aren't reliably
        verbatim across platforms (Claude paraphrases; Copilot sometimes
        does, sometimes doesn't). Returns the first matching conversation's
        full URL, or None if none contain the token (e.g. a cross-
        mechanism cell with no owned conversation at all).

        As of 2026-09-09, EVERY caller must raise when this returns None,
        rather than falling back to "whatever's topmost" (the earlier
        guidance here endorsed exactly that fallback for a no-owned-
        conversation cell -- reverted per direct instruction after the
        same bug pattern surfaced live in gemini.py's _delete_conversation
        for GE-I2-E2, a cell with genuinely no owned conversation at all).
        A cell must only ever touch its own entry, never a sibling's as a
        fallback.

        Bug fixed 2026-09-07: used to hold live ElementHandle references
        across the loop's own page.goto() call -- Playwright invalidates
        those handles the instant the page navigates, so reading
        link.get_attribute("href") on any handle after the first
        navigation raised "Execution context was destroyed." Confirmed
        live on Claude (CL-I1-E1/CL-I3-E1/CL-IF-E-CONV, all legacy cells
        with no injection-time ref, all three hitting this exact fallback
        and failing identically). Fixed by extracting every href as a
        plain string up front, before any navigation happens -- plain
        strings can't be invalidated by a later page navigation the way a
        live DOM handle can."""
        links = self.page.query_selector_all(link_selector)
        hrefs = [link.get_attribute("href") for link in links]
        for href in hrefs:
            if not href:
                continue
            self.page.goto(f"{base_url}{href}" if href.startswith("/") else href)
            self.page.wait_for_timeout(1200)
            if token.strip().lower() in self.page.inner_text("body").lower():
                return self.page.url
        return None

    def read_memory_settings(self) -> str:
        """R2 probe: navigate to the memory/personalization settings page
        and return its visible text content for the caller to check
        against the referent/token. If HAS_MEMORY_UI is False (DeepSeek),
        returns "N/A" without attempting navigation -- subclasses without a
        memory-settings surface should NOT override this, just set the
        class attribute."""
        if not self.HAS_MEMORY_UI:
            return "N/A"
        raise NotImplementedError
