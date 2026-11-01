"""Gemini over CDP: drives a Chrome the user started and signed into by hand,
instead of a fresh automated browser loaded with exported cookies.

Why (2026-10-18): the cookie-based flows (gemini.py, gemini_selenium.py) were
cut off three times in one day on the NL-forget account. First came Google's
unusual-traffic page, then the exported session was logged out, then (from
~19:05) the composer silently ignored all automated input. Copilot had the
same kind of trouble until it moved to the user's own Chrome over CDP, and
since then it hasn't been blocked. This flow does the same for Gemini.

Setup (separate from Copilot's Chrome on 9222 so the two never share a profile):
  open -na "Google Chrome" --args --remote-debugging-port=9223 \\
      --user-data-dir="$HOME/gemini-cdp-profile"   (outside /tmp, so the sign-in survives a reboot)
then sign in to gemini.google.com in that window and leave one Gemini tab open.

Switching: the cookie flow stays the default (run_cell.FLOW_REGISTRY). This one
is used only when a CDP URL is passed for Gemini (run_cell.recall_cell(...,
cdp_url=...), or nlf_recall_scheduler.py --gemini-method cdp).

Selectors, memory-page reading and erasure methods come from GeminiFlow
(Playwright). Pacing, overload handling and the block check use the same
settings as GeminiSeleniumFlow, so both methods behave the same.
"""

from __future__ import annotations

import random
import time

from playwright.sync_api import sync_playwright

from .gemini import GeminiFlow
from .gemini_selenium import GeminiSeleniumFlow
from recall_scoring import PERMISSION_CARD

GEMINI_CDP_URL = "http://localhost:9223"
COMPOSER = '[aria-label="Enter a prompt for Gemini"]'
SEND_BUTTON = 'button[aria-label="Send message"]'
REPLY = ".model-response-text"
SUBMIT_WAIT_SECONDS = 60
RESPONSE_WAIT_SECONDS = 120


class GeminiCDPFlow(GeminiFlow):
    # Shared with the Selenium flow (see its comments for where each came from).
    PROMPT_GAP_SECONDS = GeminiSeleniumFlow.PROMPT_GAP_SECONDS
    PROMPT_LONG_GAP_SECONDS = GeminiSeleniumFlow.PROMPT_LONG_GAP_SECONDS
    PROMPT_LONG_GAP_CHANCE = GeminiSeleniumFlow.PROMPT_LONG_GAP_CHANCE
    OVERLOAD_BACKOFF_SECONDS = GeminiSeleniumFlow.OVERLOAD_BACKOFF_SECONDS
    OVERLOAD_PHRASES = GeminiSeleniumFlow.OVERLOAD_PHRASES
    SETTLE_SECONDS = 180

    def __init__(self, cdp_url: str = GEMINI_CDP_URL, expected_account: str | None = "Olaoluwa Boluwatife",
                 playwright=None, **_kwargs):
        # No session file: the signed-in Chrome is the session. session_label
        # and headless are accepted (and ignored) so callers can treat both
        # Gemini flows alike.
        self._cdp_url = cdp_url
        self._expected_account = expected_account
        self._session_path = f"CDP {cdp_url}"
        self._playwright = playwright
        self._owns_playwright = playwright is None
        self._browser = None
        self._context = None
        self.page = None
        self.send_log: list[dict] = []

    def __enter__(self):
        try:
            if self._playwright is None:
                self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.connect_over_cdp(self._cdp_url)
            if not self._browser.contexts:
                raise RuntimeError(f"CDP browser at {self._cdp_url} has no contexts -- open gemini.google.com in it first.")
            self._context = self._browser.contexts[0]
            pages = [p for p in self._context.pages if "gemini.google.com" in p.url]
            if not pages:
                raise RuntimeError(f"No gemini.google.com tab in the CDP browser at {self._cdp_url} -- open one and sign in.")
            self.page = pages[0]
            self.page.bring_to_front()
            # Reload before checking who is signed in: a stale tab once showed
            # the previous account after a switch (Copilot, 2026-10-18).
            self.page.goto("https://gemini.google.com/app", wait_until="domcontentloaded")
            self.page.wait_for_timeout(4000)
            self._check_not_blocked()
            self._verify_logged_in()
            if self._expected_account:
                body = self.page.inner_text("body")
                if self._expected_account.lower() not in body.lower():
                    raise RuntimeError(
                        f"Gemini CDP tab is not signed in as {self._expected_account!r} -- stopping, nothing sent"
                    )
        except Exception:
            self._disconnect()
            raise
        return self

    def __exit__(self, *exc):
        self._disconnect()

    def _disconnect(self) -> None:
        # For a CDP connection, close() only disconnects; the user's Chrome
        # and its tabs stay open (same as CopilotFlow's CDP mode).
        if self._browser:
            self._browser.close()
            self._browser = None
        if self._playwright and self._owns_playwright:
            self._playwright.stop()
            self._playwright = None

    # --- names the shared recall code expects (see run_cell._send_fresh) ---

    def _last_reply_text(self) -> str:
        return self._last_response_text()

    def _reply_count(self) -> int:
        return len(self.page.query_selector_all(REPLY))

    def _check_not_blocked(self) -> None:
        if "google.com/sorry" in self.page.url:
            raise RuntimeError("Google unusual-traffic check page is showing; stop Gemini, prompt not sent")

    def _is_overload(self, reply: str) -> bool:
        low = (reply or "").lower()
        return len(low) < 300 and any(p in low for p in self.OVERLOAD_PHRASES)

    def read_memory_settings(self) -> str:
        text = super().read_memory_settings()
        self._check_not_blocked()
        return text

    # --- sending ---

    def send_message(self, text: str) -> str:
        """Same contract as GeminiSeleniumFlow.send_message: a human pause
        first, and an overload reply is never returned as an answer (pause,
        one re-ask in the same chat, logged; then raise)."""
        self._check_not_blocked()
        long_gap = random.random() < self.PROMPT_LONG_GAP_CHANCE
        time.sleep(random.uniform(*(self.PROMPT_LONG_GAP_SECONDS if long_gap else self.PROMPT_GAP_SECONDS)))
        reply = self._send_once(text)
        if self._is_overload(reply):
            pause = random.uniform(*self.OVERLOAD_BACKOFF_SECONDS)
            self.send_log.append({"prompt": text, "overload_reply": reply, "paused_s": round(pause)})
            print(f"GEMINI OVERLOAD: {reply[:80]!r}; pausing {pause:.0f}s, then re-asking once", flush=True)
            time.sleep(pause)
            self._check_not_blocked()
            reply = self._send_once(text)
            if self._is_overload(reply):
                raise RuntimeError(f"Gemini still overloaded after one re-ask: {reply[:120]!r}")
            self.send_log[-1]["reask_reply"] = reply
        if PERMISSION_CARD.search(reply or ""):
            # Gemini answered with a Google app-permission card (Tasks for
            # "I'm working on..." prompts, Keep for notes). User decision
            # 2026-10-18: the card is Gemini choosing a path from the prompt,
            # so it is recorded as that probe's answer (a non-answer, reported
            # as a finding) and the question is NOT re-asked. It is declined
            # ("No thanks") so the account stays unchanged; "Continue" would
            # connect the app and corrupt the study.
            # Screenshot of the card as Gemini showed it (with its "No thanks"
            # / "Continue" buttons), taken before declining; run_cell sets
            # card_shot_dir to the cell's screenshot folder.
            shot = None
            if getattr(self, "card_shot_dir", None):
                path = self.card_shot_dir / f"permission_card_{len(self.send_log) + 1:02d}_before_decline.png"
                self.page.screenshot(path=str(path), full_page=True)
                shot = path.name
            self._decline_permission_card()
            self.send_log.append({"prompt": text, "permission_card_reply": reply, "declined": True,
                                  "screenshot_before_decline": shot})
            print(f"GEMINI PERMISSION CARD: {reply[:80]!r}; declined, recorded as non-answer", flush=True)
        return reply

    def _decline_permission_card(self) -> None:
        button = self.page.get_by_role("button", name="No thanks", exact=True)
        if button.count():
            button.last.click(timeout=10000)
            self.page.wait_for_timeout(1500)

    def _send_once(self, text: str) -> str:
        """Types like a person, checks the box holds exactly the prompt,
        clicks Send, and checks the prompt appeared in the chat. Nothing is
        sent if the text did not land (the failure the cookie flow hit on
        2026-10-18, when typed keys never reached the composer)."""
        before = self._reply_count()
        composer = self.page.locator(COMPOSER).first
        # Typing can lose focus partway (GE-NLF-I0089, 2026-10-18: only
        # "what did we decide to call an aquaponic" landed). Nothing has been
        # sent at that point, so the box is cleared and the prompt retyped
        # once before giving up.
        for attempt in (1, 2):
            composer.click(timeout=10000)
            self.page.wait_for_timeout(random.randint(300, 900))
            if attempt == 2:
                self.page.keyboard.press("Meta+A")
                self.page.keyboard.press("Backspace")
                self.page.wait_for_timeout(500)
            for ch in text:
                self.page.keyboard.type(ch)
                time.sleep(random.uniform(0.03, 0.12))
            self.page.wait_for_timeout(random.randint(400, 1000))
            typed = composer.inner_text()
            if " ".join(typed.split()) == " ".join(text.split()):
                break
            print(f"GEMINI TYPING: attempt {attempt} landed {typed[:60]!r}; "
                  + ("clearing and retyping" if attempt == 1 else "giving up, nothing sent"), flush=True)
        else:
            raise RuntimeError(f"prompt text did not land in the composer, not sent: {typed[:80]!r}")

        queries_before = self.page.locator("user-query").count()
        self.page.locator(SEND_BUTTON).first.click(timeout=10000)
        # 60 s, not 15: on slow WiFi (2026-10-19, GE-NLF-I0153/I0128) the
        # question reached Gemini but showed on the page after 15 s, which
        # stopped the run mid-cell with the question already sent.
        for _ in range(SUBMIT_WAIT_SECONDS):
            self.page.wait_for_timeout(1000)
            if self.page.locator("user-query").count() > queries_before:
                break
        else:
            raise RuntimeError(f"prompt not submitted: no new user message in the chat {SUBMIT_WAIT_SECONDS}s after Send")
        return self._wait_for_reply(before)

    def _wait_for_reply(self, before_count: int) -> str:
        """GeminiFlow's wait with the longer settle time (180 s, see
        GeminiSeleniumFlow._wait_for_reply for why)."""
        # 120 s, not 60: on slow WiFi (2026-10-19, GE-NLF-I0269) a reply
        # started after 60 s and the run stopped with the answer on its way.
        for _ in range(RESPONSE_WAIT_SECONDS):
            if self._reply_count() > before_count:
                break
            self.page.wait_for_timeout(1000)
        else:
            raise RuntimeError(f"_wait_for_reply: no new response appeared within {RESPONSE_WAIT_SECONDS}s")
        prev, stable = None, 0
        for _ in range(self.SETTLE_SECONDS):
            self.page.wait_for_timeout(1000)
            cur = self._last_response_text()
            stable = stable + 1 if cur and cur == prev else 0
            if stable >= 2:
                break
            prev = cur
        else:
            raise RuntimeError(f"_wait_for_reply: reply never stabilised within {self.SETTLE_SECONDS}s")
        els = self.page.query_selector_all(REPLY)
        if els:
            els[-1].evaluate("el => el.scrollIntoView({block: 'end'})")
            self.page.wait_for_timeout(500)
        return self._last_response_text()
