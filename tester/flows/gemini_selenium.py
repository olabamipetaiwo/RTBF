"""Selenium-based Gemini flow using undetected-chromedriver.

Playwright's CDP connection is detected by Google's server-side bot
detection — even with webdriver patches, blink-feature disabling, and
Enter-key submission, certain prompt types trigger "I encountered an error"
responses while the same prompts work in a manual browser.

undetected-chromedriver patches the chromedriver binary itself (removes
cdc_ markers, modifies window.navigator properties at a lower level than
JS init scripts can), which makes it invisible to Google's detection.

This flow implements the same interface as GeminiFlow (PlatformFlow) so
run_cell.py can use it as a drop-in replacement via FLOW_REGISTRY.
"""

from __future__ import annotations

import json
import random
import time
from pathlib import Path

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config
from recall_scoring import gemini_memory_content, PERMISSION_CARD


class GeminiSeleniumFlow:
    platform = "gemini"
    HAS_MEMORY_UI = True
    MEMORY_FIELD_INJECTION_TYPES = {"I2"}

    ERASURE_DISPATCH = {
        "NL forget prompt": "_send_nl_forget",
        "Delete single conversation": "_delete_conversation",
        "Delete conversation containing file": "_delete_conversation",
        "Maximal combination (all erasure mechanisms)": "_erase_maximal",
        "Delete all activity": "_delete_all_activity",
        "Delete single Saved info item": "_delete_saved_info_item",
        "Delete all Saved info": "_delete_all_saved_info",
        "MAXIMAL": "_erase_maximal",
    }

    NON_ANSWER_SUBSTRINGS = (
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

    def __init__(self, headless: bool = False, session_label: str | None = None, **_kwargs):
        self.send_log: list[dict] = []
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
        self._driver: uc.Chrome | None = None
        self.page = None

    def __enter__(self):
        options = uc.ChromeOptions()
        if self._headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self._driver = uc.Chrome(options=options, use_subprocess=True)
        self._driver.maximize_window()

        self._load_cookies()

        self._driver.get("https://gemini.google.com/")
        time.sleep(3)

        self._verify_logged_in()

        self.page = _PageShim(self._driver)
        return self

    def _load_cookies(self) -> None:
        session_data = json.loads(self._session_path.read_text())
        cookies = session_data.get("cookies", [])

        self._driver.get("https://gemini.google.com/")
        time.sleep(1)

        for cookie in cookies:
            c = {
                "name": cookie["name"],
                "value": cookie["value"],
                "domain": cookie.get("domain", ""),
                "path": cookie.get("path", "/"),
            }
            if cookie.get("expires"):
                c["expiry"] = int(cookie["expires"])
            if cookie.get("secure"):
                c["secure"] = True
            if cookie.get("httpOnly"):
                c["httpOnly"] = True
            if cookie.get("sameSite") in ("Strict", "Lax", "None"):
                c["sameSite"] = cookie["sameSite"]
            try:
                self._driver.add_cookie(c)
            except Exception as e:
                print(f"  cookie {cookie['name']}: {e}")
        print(f"Loaded {len(cookies)} cookies")

    def _verify_logged_in(self) -> None:
        try:
            sign_in_buttons = self._driver.find_elements(By.XPATH, "//button[normalize-space()='Sign in']")
            if sign_in_buttons:
                raise RuntimeError(
                    f"gemini session (label={self._session_path!r}) is logged out -- "
                    "'Sign in' button present. Needs a fresh cookie export."
                )
        except RuntimeError:
            raise
        except Exception:
            pass

    def __exit__(self, *exc):
        if self._driver:
            try:
                self._driver.quit()
            except Exception:
                pass

    def _goto_fresh(self, url: str) -> None:
        current = self._driver.current_url.rstrip("/")
        target = url.rstrip("/")
        if current == target:
            self._driver.refresh()
        else:
            self._driver.get(url)
        time.sleep(2)

    def new_conversation(self) -> None:
        self._goto_fresh("https://gemini.google.com/app")

    def _get_response_elements(self):
        return self._driver.find_elements(By.CSS_SELECTOR, ".model-response-text")

    def _last_response_text(self) -> str:
        els = self._get_response_elements()
        return els[-1].text if els else ""

    # Names the shared recall code expects (run_cell._send_fresh's stale-read
    # guard, open_conversation's load wait), matching the Playwright flows.
    def _last_reply_text(self) -> str:
        return self._last_response_text()

    def _reply_count(self) -> int:
        return len(self._get_response_elements())

    def open_conversation(self, ref: str) -> None:
        """Reopen a past chat and wait until its earlier replies have
        rendered (same reason as flows/base.py's open_conversation: counting
        replies before they load makes an old reply look new)."""
        self._driver.get(ref)
        prev, stable = None, 0
        for _ in range(30):
            time.sleep(1)
            cur = self._last_reply_text()
            stable = stable + 1 if cur and cur == prev else 0
            if stable >= 2:
                return
            prev = cur
        raise RuntimeError(f"open_conversation: earlier replies never finished loading at {ref}")

    def _wait_for_reply(self, before_count: int) -> str:
        deadline = 60
        waited = 0
        while waited < deadline:
            if len(self._get_response_elements()) > before_count:
                break
            time.sleep(1)
            waited += 1
        else:
            raise RuntimeError("_wait_for_reply: no new response appeared within 60s")

        # Settle wait raised 60 -> 180 s (2026-10-18): GE-NLF-I0279's
        # same-conversation reply and GE-NLF-I0012's R3 follow-up were still
        # changing after 60 s (long replies, and Gemini sometimes swaps in a
        # second draft while writing; see GE-NLF-I0357's re-ask).
        prev_text = None
        stable_checks = 0
        waited = 0
        while waited < 180:
            time.sleep(1)
            waited += 1
            cur_text = self._last_response_text()
            if cur_text and cur_text == prev_text:
                stable_checks += 1
                if stable_checks >= 2:
                    break
            else:
                stable_checks = 0
            prev_text = cur_text
        else:
            raise RuntimeError("_wait_for_reply: reply never stabilised within 180s")

        els = self._get_response_elements()
        if els:
            self._driver.execute_script("arguments[0].scrollIntoView({block: 'end'})", els[-1])
            time.sleep(0.5)

        return self._last_response_text()

    def _human_type(self, element, text: str) -> None:
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.03, 0.08))

    # Human-like pacing and overload handling (user direction 2026-10-18,
    # after the pilot: rushed prompts got "I'm having a hard time fulfilling
    # your request" from Gemini, and quick page loads triggered Google's
    # unusual-traffic check). A random pause precedes every prompt; an
    # overload reply is never returned as an answer: the flow waits, re-asks
    # the same prompt once in the same chat (logged in send_log), and raises
    # if Gemini is still overloaded.
    # Gap before each prompt (revised 2026-10-18, user: a flat uniform wait
    # looks robotic): mostly a short pause, sometimes a long one, like a
    # person who reads the reply, or looks away, before typing again.
    PROMPT_GAP_SECONDS = (5, 25)
    PROMPT_LONG_GAP_SECONDS = (40, 90)
    PROMPT_LONG_GAP_CHANCE = 0.15
    OVERLOAD_BACKOFF_SECONDS = (180, 300)
    OVERLOAD_PHRASES = ("having a hard time", "having trouble responding", "try again in a bit",
                        "try this again in a bit", "something went wrong", "high demand", "at capacity")

    def _check_not_blocked(self) -> None:
        if "google.com/sorry" in self._driver.current_url:
            raise RuntimeError("Google unusual-traffic check page is showing; stop Gemini, prompt not sent")

    def _is_overload(self, reply: str) -> bool:
        low = (reply or "").lower()
        return len(low) < 300 and any(p in low for p in self.OVERLOAD_PHRASES)

    def send_message(self, text: str) -> str:
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
                self._driver.save_screenshot(str(path))
                shot = path.name
            self._decline_permission_card()
            self.send_log.append({"prompt": text, "permission_card_reply": reply, "declined": True,
                                  "screenshot_before_decline": shot})
            print(f"GEMINI PERMISSION CARD: {reply[:80]!r}; declined, recorded as non-answer", flush=True)
        return reply

    def _decline_permission_card(self) -> None:
        buttons = self._driver.find_elements(By.XPATH, "//button[normalize-space()='No thanks']")
        if buttons:
            buttons[-1].click()
            time.sleep(1.5)

    def _send_once(self, text: str) -> str:
        before = len(self._get_response_elements())

        composer = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Enter a prompt for Gemini"]'))
        )
        composer.click()
        time.sleep(0.5)

        # Since ~19:05 on 2026-10-18 the composer ignores Selenium key events
        # entirely (send_keys, ActionChains and Enter all left it empty, so
        # GE-NLF-I0012's prompts were never submitted), while editor input
        # events still work. So the prompt goes in word by word as input
        # events, the box is checked to hold exactly the prompt, and the Send
        # button is clicked; nothing is sent if the text did not land.
        for i, word in enumerate(text.split(" ")):
            self._driver.execute_script(
                "arguments[0].focus(); document.execCommand('insertText', false, arguments[1])",
                composer, (" " if i else "") + word,
            )
            time.sleep(random.uniform(0.15, 0.45))
        time.sleep(0.5)
        if " ".join(composer.text.split()) != " ".join(text.split()):
            raise RuntimeError(f"prompt text did not land in the composer, not sent: {composer.text[:80]!r}")

        queries_before = len(self._driver.find_elements(By.CSS_SELECTOR, "user-query"))
        WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Send message"]'))
        ).click()
        for _ in range(15):
            time.sleep(1)
            if len(self._driver.find_elements(By.CSS_SELECTOR, "user-query")) > queries_before:
                break
        else:
            raise RuntimeError("prompt not submitted: no new user message in the chat 15s after Send")

        return self._wait_for_reply(before)

    def read_memory_settings(self) -> str:
        self._goto_fresh("https://gemini.google.com/saved-info")
        self._check_not_blocked()
        self._scroll_to_bottom()
        content = gemini_memory_content(self._driver.find_element(By.TAG_NAME, "body").text)
        return content if content is not None else "GEMINI_NO_CONTENT_HEADING (page had no Saved info heading)"

    def _scroll_to_bottom(self, element=None) -> None:
        if element:
            self._driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", element)
        else:
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1.5)

    def set_memory_field(self, text: str) -> None:
        self._goto_fresh("https://gemini.google.com/saved-info")
        add_btn = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']"))
        )
        add_btn.click()
        time.sleep(0.8)
        field = self._driver.find_element(By.CSS_SELECTOR, '[aria-label="Enter new memory"]')
        field.send_keys(text)
        submit = self._driver.find_element(By.XPATH, "//button[normalize-space()='Submit']")
        submit.click()
        waited = 0
        while waited < 15:
            rejection = self._driver.find_elements(By.XPATH, "//*[contains(text(),\"Gemini can't save this info\")]")
            if rejection:
                raise RuntimeError(f"Gemini rejected the saved-info text: {text!r}")
            dialogs = self._driver.find_elements(By.CSS_SELECTOR, '[role="dialog"], [role="alertdialog"]')
            if not dialogs:
                break
            time.sleep(0.5)
            waited += 0.5
        else:
            raise RuntimeError("set_memory_field: dialog never closed within 15s")

    def assert_real_answer(self, reply: str) -> None:
        text = (reply or "").strip()
        if not text:
            raise RuntimeError("assert_real_answer: no reply text captured")
        lower = text.lower()
        hit = next((s for s in self.NON_ANSWER_SUBSTRINGS if s in lower), None)
        if hit:
            raise RuntimeError(f"assert_real_answer: non-answer (matched {hit!r}): {text[:200]!r}")

    def erase_via_ui(self, erasure_desc, token, injection_text, ref=None, erasure_request_text=None):
        method_name = self.ERASURE_DISPATCH.get(erasure_desc)
        if method_name is None:
            raise NotImplementedError(f"No ERASURE_DISPATCH for {erasure_desc!r}")
        kwargs = {"token": token, "injection_text": injection_text, "ref": ref}
        if erasure_request_text is not None:
            kwargs["erasure_request_text"] = erasure_request_text
        getattr(self, method_name)(**kwargs)

    def _send_nl_forget(self, token=None, injection_text="", ref=None, erasure_request_text=None):
        if not erasure_request_text:
            raise RuntimeError("_send_nl_forget: no erasure_request_text")
        if ref:
            self._goto_fresh(ref)
        else:
            self.new_conversation()
        self.assert_real_answer(self.send_message(erasure_request_text))

    def _delete_conversation(self, token, injection_text="", ref=None):
        self._goto_fresh("https://gemini.google.com/app")
        from urllib.parse import urlsplit
        convo = None
        if ref:
            path = urlsplit(ref).path
            try:
                convo = self._driver.find_element(By.CSS_SELECTOR, f'a[href="{path}"]')
            except Exception:
                convo = None

        if convo is None:
            found_ref = self._find_conversation_by_token(token)
            if not found_ref:
                raise RuntimeError(
                    f"_delete_conversation: no conversation matches ref={ref!r} or token {token!r}"
                )
            path = urlsplit(found_ref).path
            convo = self._driver.find_element(By.CSS_SELECTOR, f'a[href="{path}"]')

        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self._driver).move_to_element(convo).perform()
        time.sleep(0.4)

        row = self._driver.execute_script(
            "return arguments[0].closest('gem-nav-list-item')", convo
        )
        options_btn = row.find_element(By.CSS_SELECTOR, 'button[aria-label*="More options for"]')
        options_btn.click()
        time.sleep(0.6)
        delete_item = WebDriverWait(self._driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@role='menuitem' and normalize-space()='Delete']"))
        )
        delete_item.click()
        time.sleep(0.6)
        confirm = self._driver.find_element(By.XPATH, "//button[normalize-space()='Delete']")
        confirm.click()
        time.sleep(1)

    def _find_conversation_by_token(self, token: str) -> str | None:
        links = self._driver.find_elements(By.CSS_SELECTOR, 'a[href^="/app/"]')
        hrefs = [link.get_attribute("href") for link in links]
        for href in hrefs:
            if not href:
                continue
            self._driver.get(href if href.startswith("http") else f"https://gemini.google.com{href}")
            time.sleep(1.2)
            body_text = self._driver.find_element(By.TAG_NAME, "body").text
            if token.strip().lower() in body_text.lower():
                return self._driver.current_url
        return None

    def _delete_all_activity(self, token=None, injection_text="", ref=None):
        raise NotImplementedError("E3: myactivity.google.com rejects CDP browsers — run by hand.")

    def _delete_saved_info_item(self, token, injection_text="", ref=None):
        self._goto_fresh("https://gemini.google.com/saved-info")
        menu_btns = self._driver.find_elements(
            By.CSS_SELECTOR, 'button[aria-label*="Opens a context menu for the info"]'
        )
        target_btn = None
        for btn in menu_btns:
            row_text = self._driver.execute_script("""
                let cur = arguments[0];
                for (let i = 0; i < 6 && cur; i++) {
                    if (cur.innerText && cur.innerText.trim().length > 10) return cur.innerText;
                    cur = cur.parentElement;
                }
                return "";
            """, btn)
            if token.strip().lower() in row_text.lower():
                target_btn = btn
                break
        if target_btn is None:
            raise RuntimeError(f"_delete_saved_info_item: no item containing {token!r}")
        target_btn.click()
        time.sleep(0.6)
        menu_items = self._driver.find_elements(By.CSS_SELECTOR, '[role="menuitem"]')
        delete_item = next((el for el in menu_items if el.text.strip() == "Delete"), None)
        if delete_item is None:
            raise RuntimeError("_delete_saved_info_item: no 'Delete' menuitem found")
        delete_item.click()
        time.sleep(0.6)
        dialog = self._driver.find_element(By.CSS_SELECTOR, '[role="dialog"], [role="alertdialog"]')
        confirm = dialog.find_element(By.XPATH, ".//button[normalize-space()='Delete']")
        confirm.click()
        time.sleep(1)

    def _delete_all_saved_info(self, token=None, injection_text="", ref=None):
        self._goto_fresh("https://gemini.google.com/saved-info")
        empty = self._driver.find_elements(
            By.XPATH, "//*[contains(text(),\"You haven't asked Gemini to save anything about you yet\")]"
        )
        if empty:
            print("_delete_all_saved_info: already empty")
            return
        delete_all = WebDriverWait(self._driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Delete all']"))
        )
        delete_all.click()
        time.sleep(0.8)
        dialog = self._driver.find_element(By.CSS_SELECTOR, '[role="dialog"], [role="alertdialog"]')
        confirm = dialog.find_element(By.XPATH, ".//button[normalize-space()='Delete all']")
        confirm.click()
        time.sleep(1)

    def _erase_maximal(self, token, injection_text="", ref=None):
        try:
            self._delete_conversation(token=token, injection_text=injection_text, ref=ref)
        except RuntimeError as e:
            print(f"_erase_maximal: _delete_conversation N/A ({e}) -- continuing")
        try:
            self._delete_all_activity(token=token, injection_text=injection_text, ref=ref)
        except NotImplementedError as e:
            print(f"_erase_maximal: _delete_all_activity N/A ({e}) -- continuing")
        self._delete_all_saved_info(token=token, injection_text=injection_text, ref=ref)

    def upload_file(self, file_path: str, caption: str | None = None) -> str:
        before = len(self._get_response_elements())
        upload_btn = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Upload & tools"]'))
        )
        upload_btn.click()
        time.sleep(0.8)
        file_input = self._driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        file_input.send_keys(str(Path(file_path).resolve()))
        time.sleep(2)
        if caption:
            composer = self._driver.find_element(
                By.CSS_SELECTOR, '[aria-label="Enter a prompt for Gemini"]'
            )
            composer.click()
            self._human_type(composer, caption)
            time.sleep(0.5)
        send_btn = self._driver.find_element(By.CSS_SELECTOR, '[aria-label="Send message"]')
        send_btn.click()
        return self._wait_for_reply(before)


class _PageShim:
    """Minimal shim so run_cell.py's _save_screenshot(flow.page.screenshot(...))
    and flow.page.goto(...) work with a Selenium driver."""

    def __init__(self, driver: uc.Chrome):
        self._driver = driver

    def screenshot(self, *, path: str, full_page: bool = False) -> None:
        self._driver.save_screenshot(path)

    def goto(self, url: str, **_kwargs) -> None:
        self._driver.get(url)
        time.sleep(1.5)

    def wait_for_timeout(self, ms: int) -> None:
        time.sleep(ms / 1000)

    def evaluate(self, js: str, arg=None):
        """Playwright-style evaluate for an arrow-function string, e.g. the
        scroll-before-screenshot script in run_cell._save_screenshot."""
        return self._driver.execute_script(f"return ({js})(arguments[0]);", arg)

    def inner_text(self, selector: str) -> str:
        el = self._driver.find_element(By.CSS_SELECTOR, selector)
        return el.text

    def locator(self, selector: str):
        return _LocatorShim(self._driver, selector)

    @property
    def url(self) -> str:
        return self._driver.current_url


class _LocatorShim:
    """Minimal shim for Playwright locator calls used by run_cell.py."""

    def __init__(self, driver, selector):
        self._driver = driver
        self._selector = selector

    def inner_text(self) -> str:
        el = self._driver.find_element(By.CSS_SELECTOR, self._selector)
        return el.text
