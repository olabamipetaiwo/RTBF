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

E5 (Privacy Dashboard) was originally left unautomated (2026-08-27) for the
same reason as Gemini's E3: cross-domain (account.microsoft.com/privacy/
copilot), sign-in wall with only copilot.microsoft.com's session captured.
Briefly resolved 2026-08-28 by merging a second cookie export taken from
account.microsoft.com/privacy/copilot into the session -- the initial
page GET then worked, and the full delete sequence completed live once
end-to-end against anchorexperiment@gmail.com.

**Reclassified SKIP 2026-10-05** -- two independent reasons, either of
which is sufficient on its own:

  (a) Attribution risk (project decision, overrides everything else):
      "Delete all activity history" is account-wide and clears all
      sibling cells' Copilot activity on that account, not just this
      cell's. Running it on any shared-account cell would corrupt the
      pending attribution for every other cell on that account. Even
      the ".first" (Copilot apps) scope is still account-wide for that
      product. Do not run this for any cell, by any means (not
      automated, not by hand), unless the project policy explicitly
      changes.

  (b) Microsoft step-up auth now blocks the destructive click anyway:
      live retry on migration_dev 2026-10-05 showed the initial GET
      still works (merged cookies authorise the view), but the
      destructive click now triggers Microsoft's FIDO2/passkey +
      email-code step-up:
      login.microsoft.com/<tenant>/bridge/fido?...oauth20_authorize.srf?...
      After the challenge, subsequent GETs also redirect to
      login.live.com's "Sign in another way" wall, so the session is
      wedged. Cookie exports cannot carry an elevated-auth state
      through this. Not clear whether Microsoft tightened the policy
      between 2026-08-28 and 2026-10-05 or whether migration_dev's
      defaults are stricter.

_delete_via_privacy_dashboard() now raises NotImplementedError with the
SKIP reason; _erase_maximal() wraps the call in try/except so MAXIMAL
continues with its other three sub-steps and the Privacy Dashboard
component is logged as SKIP, matching the pattern used for Gemini's
_delete_all_activity() (which is MANUAL, not SKIP -- the policy
rationale here is Copilot-specific).
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

import config
from recall_scoring import token_found

from .base import PlatformFlow

# --- copilot.com migration (2026-09-23 / 2026-10-02) ----------------------
# Microsoft moved Copilot from copilot.microsoft.com to copilot.com (a new
# origin with a different login: MSAL + OhpAuth/OhpToken cookies, no Auth0).
# Chats survived; only the URL changed:
#   https://copilot.microsoft.com/chats/<id>  ->  https://copilot.com/chat/conversation/<id>
#
# Migrated 2026-09-23 (needed for NL-forget erasure + its login check):
# new_conversation(), the reply/composer/send selectors shared by
# send_message()/upload_file(), _verify_logged_in(), _send_nl_forget().
#
# Migrated 2026-10-02 (this round, against the migration_dev throwaway
# account; see accounts.md): the Settings/Memory entry point moved from
# "sidebar-settings-button -> menuitem Memory -> View memory" to a Fluent-UI
# "Settings and more" button -> menuitem Settings -> dialog with
# tabs (General/Personalization/Data controls/...), where Memory now lives
# as "Saved memories" + "Manage" under Personalization. The sidebar row's
# per-conversation menu moved too: the hover kebab is no longer
# aria-label="View Options" + a magic-offset click, it has a stable
# per-id data attribute (data-chat-history-more-button-conversation-id) and
# its menu uses role="menuitem" items (Rename / Move to notebook / Delete),
# with an alertdialog confirm ("Delete chat?") instead of the old dialog.
# Rows now also have real a[href*="/chat/conversation/<id>"] -- the old
# docstring finding that "sidebar rows have no href" no longer holds.
# All of this verified live end-to-end against copilot.com on the
# migration_dev throwaway account (the throwaway chat was deleted via the
# new flow as the final e2e check).
#
# Verified live on migration_dev 2026-10-05 (seeded two memories, ran one
# facts-editor delete + one bulk delete end-to-end):
#   - _delete_via_facts_editor populated path: a per-memory row is a plain
#     <li> whose visible text contains the stored fact (Copilot paraphrases
#     the raw "Remember this: X" message when it saves -- e.g. "my
#     throwaway project name is Filing Lake Chop Nest" was saved as
#     "Throwaway project name is Filing Lake Chop Nest."). Token-substring
#     matched the sibling-left-alone row and deleted only that one.
#   - _delete_all_memory populated path: the trigger button is labeled
#     "Delete all memories" (plural, visible even with just one memory --
#     differs from the old UI's 2+ facts rule). Confirm alertdialog's title
#     is "Do you want to delete all Copilot memories?" with buttons
#     "Cancel" and "Delete all memories" (identical label to the trigger).
# Still LIVE-VERIFY: _delete_via_privacy_dashboard on migration_dev (that
# destination hasn't moved, but migration_dev has no
# account.microsoft.com cookie merge).
# The old selectors stay as fallbacks (gated on _on_new_site()==False) in
# case an account has not been migrated yet.
_NEW_COMPOSER = "#m365-chat-editor-target-element"  # contenteditable, aria-label "Message Copilot"
_OLD_COMPOSER = "#userInput"
_NEW_SEND = 'button[aria-label="Send"]'  # only appears once text has been typed
_OLD_SEND = '[aria-label="Submit message"]'
_NEW_REPLY = '[data-testid="markdown-reply"]'  # Copilot's reply text, without the "Copilot said:" prefix
_OLD_REPLY = '[data-testid="ai-message-body"]'
_NEW_USER_MESSAGE = '[data-testid="chatOutput"]'  # the user's own message text, without the "You said:" prefix

# New-UI sidebar row kebab: stable, per-conversation id attribute, no hover
# dance / magic offsets. Format with the conversation id (the UUID piece
# after /chat/conversation/).
_NEW_ROW_MORE_BY_ID = '[data-chat-history-more-button-conversation-id="{id}"]'


class CopilotFlow(PlatformFlow):
    platform = "copilot"

    # CDP mode: connect to a user-launched Chrome instead of launching one.
    # Chrome must already be running with --remote-debugging-port=9222 and
    # logged into copilot.com. This avoids Playwright launch fingerprints
    # that Cloudflare Turnstile detects even with stealth patches on.
    #   open -a "Google Chrome" --args --remote-debugging-port=9222
    # Then pass cdp_url="http://localhost:9222" to the constructor.

    # Confirmed live 2026-10-05 on the migration_dev session: without stealth,
    # every send triggered the Verify-you-are-human challenge AND, after the
    # user ticked it, Copilot's "Your request couldn't be completed. Refresh
    # to try again." error banner, in a loop that never let a message through.
    # Enabling playwright-stealth's patches resolves it; same remedy as
    # Claude/Perplexity (see base.py's USE_STEALTH docstring).
    USE_STEALTH = True

    # I2 is chat-based here (like Claude/ChatGPT), not field-based (like
    # Gemini) -- confirmed live, see module docstring finding 1.
    MEMORY_FIELD_INJECTION_TYPES: set[str] = set()

    # Keys are the exact erasure_type_text values from CellPlan (MASTER
    # sheet's Erasure desc column), matching MASTER's description text.
    ERASURE_DISPATCH = {
        "Conversation history deletion": "_delete_conversation_history",
        # FILE-substudy aliases -- see flows/claude.py's ERASURE_DISPATCH
        # for why these exist. MAXIMAL's alias hits the same
        # _erase_maximal() as the main battery's CO-*-E6 cells (now
        # including _delete_via_privacy_dashboard() -- see below).
        "Delete conversation containing file": "_delete_conversation_history",
        "Maximal combination (all erasure mechanisms)": "_erase_maximal",
        "Delete all memory": "_delete_all_memory",
        "NL forget command": "_send_nl_forget",  # chat message, not a UI click
        "Granular facts editor": "_delete_via_facts_editor",
        "Privacy Dashboard": "_delete_via_privacy_dashboard",  # cross-domain, SKIP as of 2026-10-05 (attribution risk + step-up auth) -- see module docstring
        "MAXIMAL": "_erase_maximal",
    }

    BASE_URL = "https://copilot.com/"
    CHAT_URL_PREFIX = "https://copilot.com/chat/conversation/"
    LEGACY_CHAT_URL_PREFIX = "https://copilot.microsoft.com/chats/"

    def __init__(self, headless: bool = False, session_label: str | None = None,
                 playwright=None, cdp_url: str | None = None):
        self._cdp_url = cdp_url
        if cdp_url:
            self._session_path = None
            self._headless = headless
            self._playwright = playwright
            self._owns_playwright = playwright is None
            self._browser = None
            self._context = None
            self.page = None
        else:
            super().__init__(headless=headless, session_label=session_label,
                             playwright=playwright)

    @classmethod
    def normalize_ref(cls, ref: str) -> str:
        """run_tracking.json's injection_ref was captured on the old domain;
        the same chat id opens at the new URL."""
        if ref.startswith(cls.LEGACY_CHAT_URL_PREFIX):
            return cls.CHAT_URL_PREFIX + ref[len(cls.LEGACY_CHAT_URL_PREFIX):]
        return ref

    def _on_new_site(self) -> bool:
        host = urlparse(self.page.url).hostname or ""
        return host == "copilot.com" or host.endswith(".copilot.com")

    def _composer_selector(self) -> str:
        return _NEW_COMPOSER if self._on_new_site() else _OLD_COMPOSER

    def _send_selector(self) -> str:
        return _NEW_SEND if self._on_new_site() else _OLD_SEND

    def _reply_selector(self) -> str:
        return _NEW_REPLY if self._on_new_site() else _OLD_REPLY

    def _verify_logged_in(self) -> None:
        """Copilot had no login check, so a dead session would have run as a
        signed-out user without failing (the failure that falsely marked 20
        Gemini cells erased on 2026-09-17, see base.py). A logged-out
        session either redirects to a Microsoft login page or shows a
        "Sign in" button."""
        url = self.page.url
        try:
            body = self.page.inner_text("body").lower()
        except Exception:
            body = ""
        walled = (
            "login.live.com" in url
            or "login.microsoftonline.com" in url
            or "get a code to sign in" in body
            or self.page.get_by_role("button", name="Sign in", exact=True).count() > 0
        )
        if walled:
            raise RuntimeError(
                f"copilot session (label={getattr(self, '_session_path', '?')!r}) is logged out -- "
                f"sign-in wall at {url.split('?')[0]}. Needs a fresh cookie export taken from the "
                f"copilot.com tab (import with --origin https://copilot.com)."
            )

    def new_conversation(self) -> None:
        self.page.goto(self.BASE_URL + "chat")
        self.page.wait_for_timeout(1500)

    def _reply_count(self) -> int:
        return len(self.page.query_selector_all(self._reply_selector()))

    def _last_reply_text(self) -> str:
        els = self.page.query_selector_all(self._reply_selector())
        return els[-1].inner_text() if els else ""

    def _wait_for_reply(self, before_count: int, deadline_ms: int = 60000) -> str:
        """Shared by send_message() and upload_file(). `deadline_ms` is bumped
        by send_message() to 180s on the first reply after a human-verification
        challenge, since Copilot is slow to generate the first post-challenge
        response."""
        waited_ms = 0
        while waited_ms < deadline_ms:
            if self._reply_count() > before_count:
                break
            self.page.wait_for_timeout(1000)
            waited_ms += 1000
        else:
            raise RuntimeError(f"_wait_for_reply: no new reply appeared within {deadline_ms // 1000}s")

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
        else:
            # Hole caught live 2026-10-05 on chatgpt (CH-I1-E5): the old
            # silent fall-through returned "" when the reply shell
            # appeared but never populated, so the next prompt fired on
            # top of the half-finished turn. Same fix applied here.
            raise RuntimeError("_wait_for_reply: reply never stabilised with non-empty text within 60s")

        # Scroll the last reply into full view before reading — triggers any
        # lazy-rendered content and ensures the screenshot captures everything.
        els = self.page.query_selector_all(self._reply_selector())
        if els:
            els[-1].evaluate("el => el.scrollIntoView({block: 'end'})")
            self.page.wait_for_timeout(500)

        return self._last_reply_text()

    @staticmethod
    def _visible_text(text: str) -> str:
        """Whitespace-normalised text without the zero-width characters the
        new composer appends (seen live 2026-09-23: U+200B U+200C)."""
        return " ".join(re.sub("[\u200b-\u200d\ufeff]", "", text).split())

    def _type_into_composer(self, text: str) -> None:
        """Types `text` with a 40 ms per-key delay so the sequence doesn't
        arrive as a 0 ms burst (seen live 2026-10-05: zero-delay typing kept
        Copilot's abuse score elevated on migration_dev, triggering
        verification + Refresh errors on every submit even with stealth on).
        On the new site, checks the composer holds exactly `text` before
        anything is sent (whitespace-insensitive): a dropped or reordered
        character in a contenteditable would otherwise go out as a slightly
        different erasure request."""
        composer = self.page.locator(self._composer_selector())
        composer.click(force=True, timeout=10000)
        self.page.keyboard.press("Meta+A")
        self.page.keyboard.press("Backspace")
        self.page.keyboard.type(text, delay=40)
        if self._on_new_site():
            self.page.wait_for_timeout(500)
            typed = self._visible_text(composer.inner_text())
            if typed != self._visible_text(text):
                self.page.keyboard.press("Meta+A")
                self.page.keyboard.press("Backspace")
                raise RuntimeError(f"_type_into_composer: composer holds {typed!r}, expected {text!r}; nothing was sent")

    def _click_send(self) -> None:
        """Submits by pressing Enter on the focused composer rather than
        forcing a click on the Send button (seen live 2026-10-05: the
        force=True click bypasses Playwright's actionability checks and
        shows up on Copilot's side without the hover/focus event sequence a
        real send has; combined with 0 ms typing it kept the migration_dev
        session's abuse score elevated). Falls back to the forced send-click
        if Enter didn't register (composer still visibly holds the text)."""
        composer = self.page.locator(self._composer_selector())
        composer.focus()
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(400)
        if self._visible_text(composer.inner_text()):
            # Enter didn't submit (composer still full) -- fall back.
            self.page.locator(self._send_selector()).click(force=True, timeout=10000)
        self._wait_for_human_verification()

    def _verification_visible(self) -> bool:
        # get_by_text(...).count() matches hidden DOM nodes too -- seen live
        # 2026-10-05: after the user ticks the challenge, Copilot leaves the
        # "Verification required" string in the DOM as a hidden element and
        # surfaces the Refresh-banner instead, so a bare count check never
        # noticed the clear and timed out. Require the first match to be
        # actually visible.
        loc = self.page.get_by_text("Verification required").first
        if loc.count() == 0:
            return False
        try:
            return loc.is_visible()
        except Exception:
            return False

    def _request_failed_banner_visible(self) -> bool:
        # Seen live 2026-10-05: after a human-verification challenge clears,
        # Copilot sometimes surfaces this red banner instead of actually
        # sending the message. The banner's own "Refresh" button reloads the
        # page; we do a page.reload() to the same effect.
        return self.page.get_by_text("Your request couldn't be completed").count() > 0

    def _recover_from_request_failed(self, text: str) -> None:
        """Reload the page, wait for the composer back, re-type, and submit
        via the Enter key instead of a forced Send click. The forced click is
        a strong automation signal that Copilot sometimes keeps flagging even
        after verification clears, which is what put us in this state; Enter
        on a focused composer looks much more like a human submission.
        No-op if the banner is not visible."""
        if not self._request_failed_banner_visible():
            return
        print(">>> Copilot showed 'request couldn't be completed'; reloading and re-sending via Enter", flush=True)
        self.page.reload()
        self.page.wait_for_timeout(3000)
        self._type_into_composer(text)
        composer = self.page.locator(self._composer_selector())
        composer.focus()
        self.page.keyboard.press("Enter")
        self._wait_for_human_verification()  # the refreshed page may re-prompt verification

    def _wait_for_human_verification(self, timeout_s: int = 300) -> None:
        """copilot.com shows a "Verification required / Verify you are human"
        box when a message is sent from this automated browser (seen live
        2026-09-23), and the message is NOT sent until it is completed. It is
        deliberately not bypassed: this prints a notice and waits for a
        PERSON to tick the box in the browser window, then makes sure the
        message actually went (re-clicking Send once if the composer still
        holds it). Raises if nobody completes it, leaving the cell
        untouched.

        Sets self._verification_just_handled = True when it actually waited
        for a human; send_message() reads this to (a) extend its reply
        timeout and (b) re-type the message if the composer went empty
        without the send actually registering."""
        self._verification_just_handled = False
        self.page.wait_for_timeout(3000)  # the box appears about a second after the click
        if not self._verification_visible():
            return
        print(
            "\n>>> ACTION NEEDED: tick 'Verify you are human' in the Copilot browser window "
            f"(waiting up to {timeout_s // 60} min) <<<\n",
            flush=True,
        )
        for _ in range(timeout_s):
            # Treat the request-failed banner as "verification is done": the
            # challenge was ticked, Copilot just surfaced an error on the
            # pending send. Fall through so _recover_from_request_failed()
            # can take over.
            if not self._verification_visible() or self._request_failed_banner_visible():
                break
            self.page.wait_for_timeout(1000)
        else:
            raise RuntimeError(
                f"_wait_for_human_verification: still 'Verification required' after {timeout_s}s; "
                "the message was not sent."
            )
        self.page.wait_for_timeout(2000)
        composer = self.page.locator(self._composer_selector())
        if self._visible_text(composer.inner_text()):  # verification done but the message is still unsent
            self.page.locator(self._send_selector()).click(force=True, timeout=10000)
        self._verification_just_handled = True

    def send_message(self, text: str) -> str:
        before = self._reply_count()
        self._type_into_composer(text)
        self._click_send()
        verification_handled = getattr(self, "_verification_just_handled", False)
        if verification_handled:
            # Verification is cleared, but the send sometimes doesn't register:
            # the composer either still holds the text (the existing re-click
            # inside _wait_for_human_verification covers that) or has gone
            # empty with the message silently dropped. Catch the second case
            # by waiting briefly for a reply, then re-typing+re-clicking if
            # none has come and the composer is empty.
            self.page.wait_for_timeout(5000)
            if self._reply_count() == before:
                composer = self.page.locator(self._composer_selector())
                if not self._visible_text(composer.inner_text()):
                    print(">>> no reply after verification cleared; re-sending the message", flush=True)
                    self._type_into_composer(text)
                    self._click_send()
        # Separately, Copilot sometimes replaces the pending send with a
        # "Your request couldn't be completed. Refresh to try again." banner,
        # most often right after a verification challenge. Reload+resend.
        self._recover_from_request_failed(text)
        deadline_ms = 180000 if verification_handled else 60000
        return self._wait_for_reply(before, deadline_ms=deadline_ms)

    def upload_file(self, file_path: str, caption: str | None = None) -> str:
        """FILE-substudy cells: attach a document via the real (hidden)
        <input type="file"> found live 2026-08-28 -- directly reachable
        via set_input_files(), no need to click "Attach files, connect
        apps, or make something with Copilot" first. .pdf is in its
        accept list. caption=None (default) sends the file with no
        accompanying message."""
        before = self._reply_count()

        self.page.locator('input[type="file"]').first.set_input_files(file_path)
        self.page.wait_for_timeout(2000)

        if caption:
            self._type_into_composer(caption)
            self.page.wait_for_timeout(500)

        self._click_send()
        return self._wait_for_reply(before)

    def set_memory_field(self, text: str) -> None:
        """Not used for Copilot -- I2 is chat-based, see module docstring."""
        raise NotImplementedError("Copilot's I2 is chat-based -- use send_message(), not set_memory_field().")

    def _dismiss_open_overlay(self) -> None:
        """Settings dialogs and menus persist across clicks in the same flow
        instance -- the "state carries over" issue originally documented on
        the old UI (and same class as Gemini's goto()-no-op). Escape clears
        any Settings dialog / menu / alertdialog on both old and new sites."""
        dialog = self.page.query_selector('[role="dialog"], [role="alertdialog"], [role="menu"]')
        if dialog:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(400)

    def _open_settings_dialog(self) -> None:
        """New site only: click "Settings and more" -> menuitem "Settings".
        Waits for the Settings dialog's tab list before returning so later
        clicks on Personalization/Data controls don't race the mount.

        Multiple elements match aria="Settings and more" (an overflow
        button at both top-right of the main area and bottom of the
        sidebar) -- `.first` is fine, either opens the same menu."""
        self._dismiss_open_overlay()
        self.page.get_by_role("button", name="Settings and more").first.click(force=True, timeout=10000)
        self.page.wait_for_timeout(800)
        self.page.get_by_role("menuitem", name="Settings").first.click(timeout=5000)
        self.page.wait_for_selector('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"]) [role="tab"]', timeout=10000)
        self.page.wait_for_timeout(400)

    def _open_personalization_tab(self) -> None:
        """Click the Personalization tab inside the already-open Settings
        dialog. Scoped to the dialog -- the Settings dialog is a modal
        with tabs General/Personalization/Data controls/Notifications/
        About/Sources; Personalization holds Saved memories + Customize
        Copilot."""
        dialog = self.page.locator('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"])')
        dialog.locator('[role="tab"]').filter(has_text="Personalization").click()
        self.page.wait_for_timeout(1500)

    def _open_saved_memories(self) -> None:
        """New-site equivalent of the old `_open_view_memory()`. The entry
        point moved from "sidebar settings button -> Memory menuitem ->
        View memory text" to "Settings and more -> Settings dialog ->
        Personalization tab -> Manage next to 'Saved memories'".
        The old "Memory" menuitem no longer exists.

        The Personalization pane has two "Manage" buttons (Customize
        Copilot and Saved memories, in that order) -- scope by the
        "Saved memories" text's parent to pick the right one; fallback
        to the second-by-index Manage inside the Settings dialog, which
        has been the stable position in the live DOM."""
        self._open_settings_dialog()
        self._open_personalization_tab()
        saved_mem_manage = (
            self.page.get_by_text("Saved memories", exact=True)
            .locator("xpath=../..")
            .get_by_role("button", name="Manage")
        )
        if saved_mem_manage.count() == 0:
            saved_mem_manage = (
                self.page.locator('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"])')
                .get_by_role("button", name="Manage")
                .nth(1)
            )
        saved_mem_manage.first.click(force=True, timeout=10000)
        self.page.wait_for_timeout(2000)

    def _open_view_memory(self) -> None:
        """Old-site (copilot.microsoft.com) entry: sidebar-settings-button
        -> Memory menuitem -> View memory. Kept for backward compatibility
        on any account not yet migrated to copilot.com. See
        _open_saved_memories() for the current-site equivalent."""
        self._dismiss_open_overlay()
        self.page.click('[data-testid="sidebar-settings-button"]', force=True)
        self.page.wait_for_timeout(1000)
        self.page.get_by_role("menuitem", name="Memory").click()
        self.page.wait_for_timeout(1000)
        self.page.get_by_text("View memory", exact=True).click()
        self.page.wait_for_timeout(1500)

    def read_memory_settings(self) -> str:
        """R2: the Saved memories pane on the new site, or the "View memory"
        dialog on the old site.

        New site: scope to the Settings dialog (aria-label="Settings").
        The pane renders *inside* the same dialog -- there is no second
        dialog like the old UI's "View memory" overlay; clicking Manage
        just swaps the right-hand pane. Dialog-scoped read picks up only
        the Saved memories content, not sidebar chat titles (same reason
        the old code scoped to the View memory dialog -- see the long
        rationale in the else branch).

        Old site: scoped to the dialog specifically, NOT page body --
        confirmed live 2026-08-27 this matters: "Delete all memory"
        explicitly does not delete conversation history (the confirm
        dialog says so), and conversations get auto-titled from their
        content (e.g. a "Remember this: my kayak is called X" message can
        produce a sidebar conversation titled around X). body-scoped text
        search picked up those lingering sidebar titles and produced a
        false "still present" reading even when the actual memory list was
        correctly empty -- this cost significant debugging time chasing a
        phantom deletion bug that didn't exist before this was found.

        [role="dialog"] alone isn't unique enough on the old site either
        -- the old page had ~9 elements with that role (mostly empty
        design-system portal placeholders, one even part of the chat
        message UI). Scope to specifically the one containing "View
        memory"."""
        if self._on_new_site():
            self._open_saved_memories()
            dialog = self.page.locator('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"])')
            self._scroll_to_bottom(dialog.element_handle())
            return dialog.inner_text()
        self._open_view_memory()
        for d in self.page.query_selector_all('[role="dialog"]'):
            text = d.inner_text()
            if "View memory" in text:
                self._scroll_to_bottom(d)
                return d.inner_text()
        raise RuntimeError("read_memory_settings: couldn't find the View memory dialog")

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
        this cell's injection was field/settings-based, which has no
        owned conversation -- falls back to a fresh conversation
        instead."""
        if not erasure_request_text:
            raise RuntimeError(
                "_send_nl_forget: no erasure_request_text provided -- "
                "this cell's prompt-set text isn't wired in"
            )
        if ref:
            self.page.goto(self.normalize_ref(ref))
            self._require_own_token(token)
            self._refuse_if_already_requested(erasure_request_text)
        else:
            self.new_conversation()
        self.assert_real_answer(self.send_message(erasure_request_text))

    def _refuse_if_already_requested(self, erasure_request_text: str) -> None:
        """A run interrupted after the request went out (a closed window, a
        timeout while waiting for the reply) leaves the cell "injected" while
        its chat already holds the erasure request; retrying blindly would
        send it a second time. Refuses instead, so a person can look."""
        if self._visible_text(erasure_request_text) in self._visible_text(self.page.inner_text("body")):
            raise RuntimeError(
                f"_send_nl_forget: this chat already contains the erasure request at {self.page.url.split('?')[0]}; "
                "not sending it a second time. Check the chat by hand, then record it with record_manual_erasure.py."
            )

    def _require_own_token(self, token: str | None, timeout_s: int = 25) -> None:
        """The chat that opened must show THIS cell's own token before an
        erasure request is typed into it. Without this, a redirect to a new
        chat (as happened when the old-domain URLs stopped resolving) would
        still get a real-looking reply and be logged as an erasure that
        touched nothing. Raises instead of falling back to any other chat,
        per the project-wide no-topmost-fallback rule."""
        if not token:
            return
        for _ in range(timeout_s):
            try:
                if token_found(self.page.inner_text("body"), token):
                    return
            except Exception:
                pass
            self.page.wait_for_timeout(1000)
        raise RuntimeError(
            f"_send_nl_forget: this cell's own token is not on the page at {self.page.url.split('?')[0]} "
            f"after {timeout_s}s; refusing to type the erasure request into the wrong chat."
        )

    # --- New-site sidebar helpers (copilot.com) ---------------------------

    @staticmethod
    def _conv_id_from_ref(ref: str) -> str | None:
        """Pull the conversation UUID out of either the old or new URL. The
        id itself survived the migration -- only the domain + path changed:
          https://copilot.microsoft.com/chats/<id>
          https://copilot.com/chat/conversation/<id>
        Both end in the same id. Returns None if `ref` doesn't look like
        either."""
        from urllib.parse import urlsplit
        path = urlsplit(ref).path.rstrip("/")
        # Last path segment is the id in both URL shapes.
        last = path.rsplit("/", 1)[-1] if path else ""
        return last or None

    def _find_new_row_more_button(self, ref: str | None, token: str | None):
        """New site: locate the sidebar row's "More" (3-dots) button for THIS
        cell. Rows now have real `a[href*="/chat/conversation/<id>"]` and
        each row's kebab is pinned by `data-chat-history-more-button-
        conversation-id="<id>"` -- no hover dance, no click-and-check,
        no magic offsets.

        Returns the Locator for the row's More button, or None if neither
        the ref id nor a token match is in the loaded sidebar. Scrolls
        the sidebar container to load more rows if the first pass doesn't
        find a match -- Copilot's sidebar still lazy-loads conversations
        (the bug fixed 2026-09-07 on the old UI); the new UI's row
        container is a div with data-testid or class `fai-CopilotNavDrawerBody`
        / `fai-CopilotNavItem` as its items (verified live 2026-10-02).
        Non-destructive: never clicks anything, only queries + scrolls."""
        conv_id = self._conv_id_from_ref(ref) if ref else None

        def found():
            if conv_id:
                sel = _NEW_ROW_MORE_BY_ID.format(id=conv_id)
                loc = self.page.locator(sel)
                if loc.count() > 0:
                    return loc.first
            if token:
                # Rows have aria-label equal to the chat title (which, for a
                # Remember-this seed, often includes the token verbatim) and
                # the a[href] carries the id. Match the aria-label first,
                # then the row's own innerText as a secondary signal.
                rows = self.page.locator('a[href*="/chat/conversation/"]')
                for i in range(rows.count()):
                    row = rows.nth(i)
                    aria = (row.get_attribute("aria-label") or "").lower()
                    if token.strip().lower() in aria:
                        href = row.get_attribute("href") or ""
                        rid = href.rstrip("/").rsplit("/", 1)[-1]
                        sel = _NEW_ROW_MORE_BY_ID.format(id=rid)
                        more = self.page.locator(sel)
                        if more.count() > 0:
                            return more.first
            return None

        checked_count = 0
        while True:
            hit = found()
            if hit is not None:
                return hit
            rows = self.page.locator('a[href*="/chat/conversation/"]')
            n = rows.count()
            if n <= checked_count:
                return None
            # Scroll the last loaded row into view to trigger lazy-load
            # (same mechanism as the old UI, just reached via the real
            # row element rather than the kebab).
            try:
                rows.nth(n - 1).evaluate("el => el.scrollIntoView()")
            except Exception:
                pass
            self.page.wait_for_timeout(900)
            checked_count = n

    # --- Old-site sidebar helpers (copilot.microsoft.com) -----------------

    def _open_sidebar_conversation_rows(self):
        """Old-site only (new site uses data-attribute selectors instead).

        Sidebar open/closed state persists across navigations (a client-
        side preference), so "Open sidebar" may or may not exist -- check
        for conversation rows first rather than assuming the toggle is
        there (confirmed live 2026-08-27: indexing sidebar_toggles[2]
        blindly threw IndexError once the sidebar was already open)."""
        if not self.page.query_selector_all('[aria-label="View Options"]'):
            sidebar_toggles = self.page.query_selector_all('[aria-label="Open sidebar"]')
            # Empirically the 3rd match is the real small icon button; the
            # 1st is an oversized wrapper that swallows clicks meant for
            # content underneath it (confirmed live 2026-08-27).
            (sidebar_toggles[2] if len(sidebar_toggles) > 2 else sidebar_toggles[0]).click(force=True)
            self.page.wait_for_timeout(1000)
        return self.page.query_selector_all('[aria-label="View Options"]')

    def _scroll_and_find_row_index(self, is_match) -> int | None:
        """Old-site only. Bug fixed 2026-09-07: Copilot's old-UI sidebar
        lazy-loads more conversations as you scroll -- confirmed live only
        20 rows render initially, growing to 63+ after repeated scrolling.
        CO-IF-E-MAX's own conversation was past that first 20, which is
        exactly why _delete_conversation_history() was reporting "not
        found" for an account that genuinely had the conversation
        (confirmed separately: it was there, just further down the lazy-
        loaded list). Clicks each row in turn (read-only/non-destructive,
        just switches which conversation is open), calling `is_match()`
        after each click; if nothing in the currently-loaded rows matches,
        scrolls to the last one to trigger loading more and keeps going --
        stops only once a scroll produces no new rows (the true end of
        the list)."""
        checked = 0
        while True:
            opts = self._open_sidebar_conversation_rows()
            for i in range(checked, len(opts)):
                row = opts[i].evaluate_handle('el => el.closest("li") || el.parentElement.parentElement').as_element()
                row.click(force=True)
                self.page.wait_for_timeout(800)
                if is_match():
                    return i
            checked = len(opts)
            if opts:
                opts[-1].evaluate_handle('el => el.scrollIntoView()')
            self.page.wait_for_timeout(1000)
            if len(self._open_sidebar_conversation_rows()) <= checked:
                return None

    def _find_conversation_row_index(self, ref: str) -> int | None:
        """Old-site only. Copilot's old sidebar rows had no href of their
        own (confirmed live 2026-08-31: `a[href]` in the sidebar only
        matched unrelated nav links like /discover) -- a conversation's
        real URL only appeared after navigating INTO it via a click. So
        identify THIS cell's own row by clicking each one in turn and
        checking whether the resulting URL matches `ref` (captured at
        injection time), rather than assuming index 0 is always the right
        conversation."""
        from urllib.parse import urlsplit
        target_path = urlsplit(ref).path.rstrip("/")
        return self._scroll_and_find_row_index(
            lambda: urlsplit(self.page.url).path.rstrip("/") == target_path
        )

    def _find_conversation_row_index_by_token(self, token: str) -> int | None:
        """Old-site only. Fallback for _delete_conversation_history() when
        `ref` is missing (legacy tracking data) -- clicks each sidebar row
        and checks its visible content for `token`. Same idea as base.py's
        _find_conversation_by_token() but via click-and-check because old-
        UI rows had no href."""
        return self._scroll_and_find_row_index(
            lambda: token.strip().lower() in self.page.inner_text("body").lower()
        )

    def _delete_conversation_history(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        """E1: deletes THIS cell's own conversation.

        New site (copilot.com): rows have real
        `a[href*="/chat/conversation/<id>"]` and each row's kebab is pinned
        by `data-chat-history-more-button-conversation-id="<id>"` -- the
        id survived the migration from copilot.microsoft.com/chats/<id>,
        so a ref captured on the old domain still identifies the right
        kebab here. Click the kebab -> menuitem "Delete" -> alertdialog
        "Delete chat?" -> button "Delete". No row-click dance, no
        bounding-box offset click, no mouse coordinate magic -- all three
        of those were old-UI workarounds. Verified end-to-end live
        2026-10-02 against migration_dev's throwaway chat.

        Old site (copilot.microsoft.com): preserves the pre-migration
        behavior -- click each row in turn to resolve its URL, then click
        the kebab at a known offset from its own bounding_box() (the old
        kebab element misreported its horizontal position, see finding 5
        in the module docstring).

        **No row-0 / topmost fallback, ever, as of 2026-09-09**: an
        earlier version fell back to row 0 whenever neither `ref` nor
        a content search found a match. Reverted per direct instruction
        -- a cell must only ever delete its own entry, never a sibling's.
        Both site paths raise when the cell's own row can't be found.
        Also falls back to a token search when `ref` IS given but doesn't
        match (a stale ref) -- confirmed live 2026-09-09 on Gemini's
        equivalent method that a stale ref can coexist with a real, still-
        present conversation."""
        if self._on_new_site():
            # Navigate to the sidebar listing. /chat is Copilot's "no
            # current chat" landing; the sidebar renders equally there.
            self.page.goto("https://copilot.com/chat")
            self.page.wait_for_timeout(2000)
            more_btn = self._find_new_row_more_button(ref=ref, token=token)
            if more_btn is None:
                raise RuntimeError(
                    f"_delete_conversation_history: no conversation matches ref={ref!r} or token {token!r} "
                    "on copilot.com -- this cell has no owned conversation to delete "
                    "(refusing to guess/delete another row)"
                )
            more_btn.click(force=True, timeout=10000)
            self.page.wait_for_timeout(1000)
            self.page.get_by_role("menuitem", name="Delete", exact=True).click(timeout=5000)
            # Confirm dialog is role="alertdialog" on the new site (was
            # role="dialog" on the old UI). Its "Delete" button has no
            # aria/testid -- scope by role=button + exact text, and take
            # .last to avoid matching the row's own Delete menuitem if the
            # menu is still in the DOM.
            self.page.wait_for_selector('[role="alertdialog"]', timeout=10000)
            self.page.get_by_role("button", name="Delete", exact=True).last.click(timeout=5000)
            self.page.wait_for_timeout(1500)
            return

        # --- Old-site path (unchanged) ---
        self.page.goto("https://copilot.microsoft.com/")
        self.page.wait_for_timeout(1500)
        row_index = self._find_conversation_row_index(ref) if ref else None
        if row_index is None:
            row_index = self._find_conversation_row_index_by_token(token)
            if row_index is None:
                raise RuntimeError(
                    f"_delete_conversation_history: no conversation matches ref={ref!r} or token {token!r} "
                    "-- this cell has no owned conversation to delete (refusing to guess/delete row 0)"
                )

        opts = self._open_sidebar_conversation_rows()
        if not opts or row_index >= len(opts):
            raise RuntimeError("_delete_conversation_history: no conversation found in sidebar")
        box = opts[row_index].bounding_box()
        self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=5)
        self.page.wait_for_timeout(500)
        self.page.mouse.click(228, box["y"] + box["height"] / 2)
        self.page.wait_for_timeout(800)
        self.page.get_by_role("menuitem", name="Delete", exact=True).click()
        self.page.wait_for_timeout(800)
        self.page.get_by_role("button", name="Delete", exact=True).last.click()
        self.page.wait_for_timeout(1500)

    # --- Memory erasures (E2, E4) -----------------------------------------

    # On the new site both methods share the Saved-memories pane as their
    # entry point (opened via _open_saved_memories()). The empty-state
    # marker ("hasn't captured any memories") was verified live 2026-10-02
    # on migration_dev (fresh account). The populated-pane shape was
    # verified live 2026-10-05 on migration_dev (two seeded memories):
    # per-fact rows are plain <li>s, the bulk-delete trigger is literally
    # "Delete all memories" (plural, visible even with one fact), and the
    # confirm alertdialog's confirm button carries the same label as the
    # trigger -- see the longer notes at the top of the module and inside
    # each method.

    _NEW_SAVED_MEMORIES_EMPTY = "hasn't captured any memories"

    def _saved_memories_pane_text(self) -> str:
        """Content of the Saved-memories pane -- the right-hand half of the
        Settings dialog after _open_saved_memories()."""
        return self.page.locator('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"])').inner_text()

    def _delete_all_memory(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        """Deliberately account-wide/blanket -- see [[project-destructive-actions-run-last]].
        `token`/`injection_text`/`ref` accepted for interface consistency
        but unused.

        New site: Settings -> Personalization -> Manage next to "Saved
        memories" -> pane with a "Delete all" control.

        Old site (preserved below): "Delete all memory" button on the
        View memory page. Only appears once there are 2+ facts (module
        docstring finding 2). The "Personalization and memory" toggle
        does NOT delete existing facts (finding 3).

        Treats an empty memory list as a legitimate no-op rather than an
        error -- confirmed live 2026-09-09 on CO-I1-E6 (and CO-I1-E4's
        equivalent facts-editor finding) that Copilot doesn't reliably
        infer memory-worthiness from a passive I1 disclosure, so "nothing
        to delete" is a real, recordable outcome here, not a bug. Same
        empty-state-as-no-op pattern as Gemini's _delete_all_saved_info
        and Perplexity's _delete_all_threads. The new-site empty-state
        text "Copilot hasn't captured any memories yet" was itself verified
        live 2026-10-02 on 
        
        """
        if self._on_new_site():
            self._open_saved_memories()
            dialog = self.page.locator('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"])')
            if self._NEW_SAVED_MEMORIES_EMPTY in self._saved_memories_pane_text():
                return
            # Trigger: "Delete all memories" (plural) -- verified live
            # 2026-10-05 on migration_dev; appears even with a single
            # memory present, unlike the old UI's 2+ facts rule. Regex
            # keeps "clear" / singular as safety fallbacks in case the
            # label drifts; raises loudly if nothing matches rather than
            # silently doing nothing.
            delete_all_btn = dialog.get_by_role(
                "button",
                name=re.compile(r"^(delete|clear) all( memories| memory)?$", re.I),
            )
            if delete_all_btn.count() == 0:
                raise RuntimeError(
                    "_delete_all_memory: no 'Delete all memories' / 'Clear all' button in Saved memories pane "
                    "and pane text isn't the known empty-state string either. "
                    "Check the live DOM and update the button-label regex."
                )
            delete_all_btn.first.click(timeout=5000)
            # Confirm alertdialog verified live 2026-10-05 on migration_dev:
            # title "Do you want to delete all Copilot memories?", two
            # buttons ("Cancel", "Delete all memories"). The confirm button
            # is labeled identically to the trigger, so match the same
            # regex but scope to the alertdialog -- a page-wide `.last`
            # worked here but would silently pick the trigger again if the
            # alertdialog ever failed to mount.
            self.page.wait_for_selector('[role="alertdialog"]', timeout=10000)
            self.page.locator('[role="alertdialog"]').get_by_role(
                "button",
                name=re.compile(r"^(delete|clear) all( memories| memory)?$", re.I),
            ).click(timeout=5000)
            self.page.wait_for_timeout(1500)
            return

        # --- Old-site path (unchanged) ---
        self._open_view_memory()
        delete_all_btn = self.page.get_by_role("button", name="Delete all memory", exact=True)
        if delete_all_btn.count() == 0:
            if self.page.get_by_text("Add a fact", exact=True).count() == 0:
                raise RuntimeError(
                    "_delete_all_memory: 'Delete all memory' button not found and "
                    "memory list doesn't look empty either -- unexpected page state"
                )
            return
        delete_all_btn.click()
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

    def _delete_via_facts_editor(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        """E4: deletes THIS cell's own fact, identified by matching `token`
        against each row's text.

        New site: inside the Saved-memories pane. Per-fact rows are plain
        <li>s whose visible text contains the saved fact; Copilot
        paraphrases the raw "Remember this: X" message when it saves
        (verified live 2026-10-05 on migration_dev: "my throwaway project
        name is Filing Lake Chop Nest" was stored as "Throwaway project
        name is Filing Lake Chop Nest."), so the token-substring match
        still holds but a longer injection sentence won't be reliable --
        match on the shortest distinctive piece.

        Old site: Live-verified 2026-08-31 that the View memory list
        shows facts verbatim (e.g. "Your pickling project is named
        'Filing Lake Chop Nest'") -- reliable substring match, unlike
        Claude's paraphrased Topics. The trash icon has no text/aria-
        label; working selector was x > 800 unlabeled buttons sorted by
        y, matched against the content pane's visible text split by line
        (both failure modes documented inline in the old-site branch
        below).

        No row-0 / first-row fallback here or on either site -- changed
        from always deleting the first row (which silently deleted a
        sibling cell's fact on a shared account) per the project-wide
        no-topmost-fallback rule."""
        if self._on_new_site():
            self._open_saved_memories()
            pane_text = self._saved_memories_pane_text()
            if self._NEW_SAVED_MEMORIES_EMPTY in pane_text:
                raise RuntimeError(
                    f"_delete_via_facts_editor: Saved memories pane shows the empty state; "
                    f"no fact matching token {token!r} exists on this account"
                )
            # Verified live 2026-10-05 on migration_dev: per-fact rows are
            # plain <li>s (not role="listitem", no data-testid), one row
            # per saved memory, each with its own delete control; the
            # fact's text sits in the row's innerText. The listitem/
            # data-testid selectors are kept here as forward-compatible
            # fallbacks in case Copilot swaps the row element later.
            if token.strip().lower() not in pane_text.lower():
                raise RuntimeError(
                    f"_delete_via_facts_editor: token {token!r} not visible in the Saved memories pane. "
                    f"Pane text: {pane_text[:400]!r}. "
                    "Copilot may not have stored this cell's disclosure as a saved memory, "
                    "or it was paraphrased past the point of substring match."
                )
            dialog = self.page.locator('[role="dialog"]:is([aria-label="Settings"], [aria-label="Chat settings"])')
            # Find a per-fact row/listitem that contains the token, then
            # click its own delete control.
            fact_row = (
                dialog.locator('[role="listitem"], li, [data-testid*="memory" i]')
                .filter(has_text=token.strip())
            )
            if fact_row.count() == 0:
                raise RuntimeError(
                    "_delete_via_facts_editor: Saved memories pane contains the token in text, "
                    "but no <li>/listitem/data-testid=memory row contains it. "
                    "Row element likely changed -- check the live DOM and update the row selector."
                )
            delete_in_row = fact_row.first.get_by_role(
                "button", name=re.compile(r"^(delete|remove|trash)$", re.I)
            )
            if delete_in_row.count() == 0:
                # Fallback: an icon-only button inside the row (no label).
                delete_in_row = fact_row.first.locator('button[aria-label], button:has(svg)').last
            delete_in_row.first.click(timeout=5000)
            self.page.wait_for_timeout(600)
            # Confirm dialog, same shape as the all-delete flow.
            try:
                self.page.wait_for_selector('[role="alertdialog"], [role="dialog"]:has-text("Delete")', timeout=5000)
                self.page.get_by_role("button", name=re.compile(r"^delete$", re.I)).last.click(timeout=5000)
            except Exception:
                # Some per-item deletes commit inline with no confirm --
                # that's not an error on this platform's past behavior.
                pass
            self.page.wait_for_timeout(1500)
            return

        # --- Old-site path (unchanged) ---
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

        # Scoped to the settings dialog's content pane (the sidebar <nav>'s
        # sibling <div>), not the whole dialog -- an unscoped dialog.inner_text()
        # also picks up the Settings sidebar's own tab labels (Preferences,
        # Shopping, Wallet, etc.), which silently shifted every fact's line
        # index relative to trash_icons and broke this on any account whose
        # settings sidebar has grown since 2026-08-27. Confirmed live
        # 2026-09-09 on CO-I2-E4 (1 real fact, but matching_line_idx landed
        # on index 9 -- the 9 sidebar labels -- instead of 0).
        dialog_text = None
        for d in self.page.query_selector_all('[role="dialog"]'):
            if "View memory" in d.inner_text():
                nav = d.query_selector('nav[aria-label="Settings"]')
                content = nav.evaluate_handle("el => el.nextElementSibling").as_element() if nav else None
                dialog_text = content.inner_text() if content else d.inner_text()
                break
        fact_lines = [
            line for line in (dialog_text or "").split("\n")
            if line.strip() and line.strip() not in ("View memory", "Delete all memory")
        ]
        matching_line_idx = next(
            (i for i, line in enumerate(fact_lines) if token.strip().lower() in line.lower()), None
        )
        if matching_line_idx is None or matching_line_idx >= len(trash_icons):
            raise RuntimeError(f"_delete_via_facts_editor: no fact row found containing {token!r}")
        trash_icons[matching_line_idx][1].click()
        self.page.wait_for_timeout(600)
        self.page.get_by_role("button", name="Delete", exact=True).last.click()
        self.page.wait_for_timeout(1500)

    def _delete_via_privacy_dashboard(self, token: str | None = None, injection_text: str = "", ref: str | None = None) -> None:
        """E5: cross-domain (account.microsoft.com/privacy/copilot). SKIP
        2026-10-05 -- see the SKIP block in the module docstring for the
        full story (two independent reasons: attribution risk + Microsoft
        step-up auth).

        Do NOT run this by hand either: "Delete all activity history" is
        account-wide for the Copilot apps product and would clear every
        sibling cell's activity on the same account, not just this
        cell's."""
        raise NotImplementedError(
            "E5: SKIP -- do not run (by any means). 'Delete all activity history' "
            "on account.microsoft.com/privacy/copilot is account-wide and would "
            "corrupt attribution for sibling cells sharing the account. The click "
            "also hits a Microsoft FIDO2/passkey step-up wall that cookie exports "
            "can't satisfy (2026-10-05 live retest). See the module docstring."
        )

    def _erase_maximal(self, token: str, injection_text: str = "", ref: str | None = None) -> None:
        """E6: all singles combined in one setup (design rule). Was calling
        _delete_via_privacy_dashboard() twice with no documented reason --
        removed 2026-08-31: every other platform's MAXIMAL runs each
        single mechanism exactly once, and a second call risks throwing
        (the "Clear" confirm button may not exist once history's already
        empty from the first call) rather than doing anything useful.

        Fixed 2026-09-13 (same pattern as claude.py's/gemini.py's
        _erase_maximal fixes, 2026-09-07/09): this used to run all four
        sub-steps with no error handling, so a step with nothing real to
        act on (confirmed live on CO-I1-E6: _delete_via_facts_editor
        raised "no fact row found", the same genuine I1-chat-memory-save
        non-determinism already documented on CO-I1-E4) aborted the whole
        sequence before ever reaching _delete_via_privacy_dashboard --
        the MAXIMAL cell's Privacy Dashboard component silently never ran
        at all. Now caught and logged as N/A instead of fatal, matching
        every other platform's MAXIMAL.

        2026-10-05: _delete_via_privacy_dashboard reclassified SKIP (do
        not run by any means -- attribution risk + Microsoft step-up
        auth; see its docstring and the module docstring). Wrapped in
        try/except here so a MAXIMAL cell's Privacy Dashboard sub-step
        logs as SKIP and the other three sub-steps still run; the raise
        itself is the "do not run" guard rail, not an error to recover
        from."""
        self._delete_conversation_history(token=token, injection_text=injection_text, ref=ref)
        self._delete_all_memory(token=token, injection_text=injection_text, ref=ref)
        try:
            self._delete_via_facts_editor(token=token, injection_text=injection_text, ref=ref)
        except RuntimeError as e:
            print(f"_erase_maximal: _delete_via_facts_editor N/A ({e}) -- continuing")
        try:
            self._delete_via_privacy_dashboard(token=token, injection_text=injection_text, ref=ref)
        except NotImplementedError as e:
            print(f"_erase_maximal: _delete_via_privacy_dashboard SKIP ({e}) -- continuing")


    def __enter__(self):
        try:
            if self._playwright is None:
                self._playwright = sync_playwright().start()
            if self._cdp_url:
                self._browser = self._playwright.chromium.connect_over_cdp(self._cdp_url)
                contexts = self._browser.contexts
                if not contexts:
                    raise RuntimeError(
                        f"CDP browser at {self._cdp_url} has no contexts -- "
                        "open copilot.com in a tab first."
                    )
                self._context = contexts[0]
                copilot_page = None
                for p in self._context.pages:
                    if "copilot.com" in p.url:
                        copilot_page = p
                        break
                if copilot_page is None:
                    raise RuntimeError(
                        "No copilot.com tab found in the CDP browser -- "
                        "open copilot.com and log in first."
                    )
                self.page = copilot_page
                self.page.bring_to_front()
                self.page.wait_for_timeout(1500)
            else:
                self._browser = self._playwright.chromium.launch(
                    headless=self._headless,
                    channel="chrome",
                    ignore_default_args=["--enable-automation"],
                    args=["--disable-blink-features=AutomationControlled"],
                )
                self._context = self._browser.new_context(storage_state=str(self._session_path))
                if self.USE_STEALTH:
                    Stealth().apply_stealth_sync(self._context)
                self.page = self._context.new_page()
                self.page.goto(config.PLATFORMS[self.platform], wait_until="domcontentloaded")
                self.page.wait_for_timeout(2500)
            self._verify_logged_in()
        except Exception:
            if self._cdp_url:
                if self._browser:
                    self._browser.close()
            else:
                if self._browser:
                    self._browser.close()
            if self._playwright and self._owns_playwright:
                self._playwright.stop()
            raise
        return self

    def __exit__(self, *exc):
        if self._cdp_url:
            if self._browser:
                self._browser.close()
        else:
            if self._browser:
                self._browser.close()
        if self._playwright and self._owns_playwright:
            self._playwright.stop()
