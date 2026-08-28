"""Run once per platform to capture a logged-in session for reuse.

Two modes:

1. `python login_setup.py <platform>` -- opens a real (headed) browser
   (real installed Chrome via channel="chrome", not Playwright's bundled
   Chromium) to the platform's login page and you log in manually inside
   it. Works fine for platforms without Google-OAuth-specific detection.

2. `python login_setup.py <platform> --from-chrome-profile` -- for
   platforms where Google rejects ANY Playwright-driven browser during
   sign-in ("This browser or app may not be secure"), confirmed live
   2026-08-26 on ChatGPT's "Continue with Google" -- happens because
   Playwright attaches via the Chrome DevTools Protocol (CDP), which
   Google's OAuth risk check detects independent of which browser binary
   is running; switching to real Chrome alone does NOT fix this.

   Instead: you log into the platform in your own everyday Chrome first
   (no automation involved at all, so Google never sees anything to
   reject), fully quit Chrome, then this copies only the small
   session-relevant pieces of your profile (Cookies, Local Storage, Local
   State, Preferences -- not your whole multi-GB profile, and NEVER your
   live profile directory) into sessions/_chrome_profile_copy/, launches
   Playwright against that COPY, and verifies it inherited your logged-in
   session before saving it as this project's storage_state.

Every other script in this project loads the saved sessions/<platform>.json
instead of logging in again, so this is the only step that needs a human.

Gemini and Copilot involve a second origin for some erasure surfaces
(Google's Activity controls, Microsoft's Privacy Dashboard -- see the
technical-audit plan). SECONDARY_DOMAINS below gets visited once during
session capture so its cookies are captured into the same storage_state
file too, instead of needing a separate login capture per domain.

Usage:
    python login_setup.py claude
    python login_setup.py chatgpt --from-chrome-profile
    ...
"""

import shutil
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

import config

# Platform -> URL to also click through during login, so its cookies land in
# the same storage_state file. Not yet confirmed live whether visiting these
# actually requires a separate auth step or rides on the same Google/
# Microsoft account session.
SECONDARY_DOMAINS = {
    "gemini": "https://myactivity.google.com/",
    "copilot": "https://account.microsoft.com/privacy",
}

# macOS only, for now -- other platforms would need different source paths.
REAL_CHROME_DIR = Path.home() / "Library/Application Support/Google/Chrome"
PROFILE_COPY_DIR = config.SESSIONS_DIR / "_chrome_profile_copy"

# Only these small, session-relevant pieces get copied -- never the whole
# (multi-GB, cache-heavy) profile, and never in place / never the live
# directory itself.
PROFILE_FILES_TO_COPY = [
    "Local State",                     # top-level, profile metadata
]
PROFILE_SUBDIR_FILES_TO_COPY = [       # relative to Default/
    "Cookies",
    "Cookies-journal",
    "Preferences",
]
PROFILE_SUBDIRS_TO_COPY = [            # relative to Default/, copied whole
    "Local Storage",
]


def _prepare_chrome_profile_copy(source_profile: str = "Default") -> Path:
    src_default = REAL_CHROME_DIR / source_profile
    if not src_default.exists():
        raise FileNotFoundError(
            f"No Chrome profile at {src_default} -- pass a different "
            f"source_profile if you use a non-default one (e.g. 'Profile 7')."
        )

    if PROFILE_COPY_DIR.exists():
        shutil.rmtree(PROFILE_COPY_DIR)
    # Destination folder name MUST match source_profile exactly. Local
    # State (copied below) records last_used/last_active_profiles by this
    # folder name -- if it doesn't match, Chrome can't find the profile it
    # expects, silently creates a brand-new EMPTY one with that name, and
    # never touches our copied cookies at all. (Confirmed live 2026-08-27:
    # this is why the first two capture attempts landed on a logged-out
    # page despite valid cookies sitting right there in "Default".)
    dst_default = PROFILE_COPY_DIR / source_profile
    dst_default.mkdir(parents=True)

    for name in PROFILE_FILES_TO_COPY:
        src = REAL_CHROME_DIR / name
        if src.exists():
            shutil.copy2(src, PROFILE_COPY_DIR / name)

    for name in PROFILE_SUBDIR_FILES_TO_COPY:
        src = src_default / name
        if src.exists():
            shutil.copy2(src, dst_default / name)

    for name in PROFILE_SUBDIRS_TO_COPY:
        src = src_default / name
        if src.exists():
            shutil.copytree(src, dst_default / name)

    return PROFILE_COPY_DIR


def capture_session_from_chrome_profile(
    platform: str, source_profile: str = "Profile 7", auto: bool = False
) -> None:
    """auto=True skips the input() prompts (for driving this from a tool that
    can't relay a live terminal) -- instead it waits for the page to settle,
    takes a screenshot to sessions/_check_<platform>.png for visual
    verification, and saves storage_state unconditionally. Check the
    screenshot before trusting the saved session."""
    if not auto:
        print(
            "This copies only Cookies/Local Storage/Preferences from your real "
            "Chrome profile -- never the live profile itself. Make sure Chrome "
            "is FULLY QUIT (Cmd+Q, not just closed) before continuing, so the "
            "files aren't being written to mid-copy."
        )
        input("Chrome fully quit? Press Enter to continue... ")

    profile_dir = _prepare_chrome_profile_copy(source_profile)
    print(f"Profile pieces copied -> {profile_dir}")

    url = config.PLATFORMS[platform]
    out_path = config.session_path(platform)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir), headless=False, channel="chrome"
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(url)

        if auto:
            page.wait_for_load_state("networkidle", timeout=15000)
            page.wait_for_timeout(2000)
            shot_path = config.SESSIONS_DIR / f"_check_{platform}.png"
            page.screenshot(path=str(shot_path))
            print(f"\nOpened {url} using your copied profile. Screenshot -> {shot_path}")
        else:
            print(f"\nOpened {url} using your copied profile.")
            input(
                "Check the browser window -- if you're already logged in, great. "
                "If not, log in manually here. Once you see the chat UI, press "
                "Enter to continue... "
            )

        secondary = SECONDARY_DOMAINS.get(platform)
        if secondary:
            page.goto(secondary)
            if auto:
                page.wait_for_load_state("networkidle", timeout=15000)
                page.wait_for_timeout(2000)
                shot_path2 = config.SESSIONS_DIR / f"_check_{platform}_secondary.png"
                page.screenshot(path=str(shot_path2))
                print(f"Also opened {secondary}. Screenshot -> {shot_path2}")
            else:
                print(f"\nAlso opened {secondary} (needed for this platform's cross-domain erasure surface).")
                input("Confirm you're logged in there too (same account), then press Enter to save the session... ")

        context.storage_state(path=str(out_path))
        print(f"Session saved -> {out_path}")
        context.close()


def _wait_for_signal(signal_path: Path, timeout_s: int = 900) -> bool:
    """Poll for signal_path to appear (touched by a separate process once the
    human is done), instead of blocking on input() -- input() doesn't work
    when this script is launched from a tool that isn't attached to a real
    TTY, which is how this gets run in practice. Returns False on timeout."""
    waited = 0
    while not signal_path.exists():
        if waited >= timeout_s:
            return False
        time.sleep(2)
        waited += 2
    signal_path.unlink()
    return True


def capture_session(platform: str, wait_for_signal: bool = False) -> None:
    url = config.PLATFORMS[platform]
    out_path = config.session_path(platform)
    config.SESSIONS_DIR.mkdir(exist_ok=True)
    signal_path = config.SESSIONS_DIR / f".continue_{platform}"
    signal_path.unlink(missing_ok=True)

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False, channel="chrome")
        except Exception as e:
            print(f"Couldn't launch real Chrome ({e}). Falling back to bundled Chromium --")
            print("Google sign-in may block this with 'This browser or app may not be secure.'")
            browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        print(f"\nOpened {url}")
        print("Log in manually (handle CAPTCHA/verification/2FA as needed).")
        print("If Google rejects sign-in ('browser or app may not be secure'),")
        print(f"stop and re-run with: python login_setup.py {platform} --from-chrome-profile")

        if wait_for_signal:
            print(f"Waiting for signal file {signal_path} (touched once you're logged in)...")
            if not _wait_for_signal(signal_path):
                print("Timed out waiting for login. Session NOT saved.")
                browser.close()
                return
        else:
            input("Once you're fully logged in and see the chat UI, press Enter here to continue... ")

        secondary = SECONDARY_DOMAINS.get(platform)
        if secondary:
            page.goto(secondary)
            print(f"\nAlso opened {secondary} (needed for this platform's cross-domain erasure surface).")
            if wait_for_signal:
                secondary_signal = config.SESSIONS_DIR / f".continue_{platform}_secondary"
                secondary_signal.unlink(missing_ok=True)
                print(f"Waiting for signal file {secondary_signal}...")
                _wait_for_signal(secondary_signal)
            else:
                input("Confirm you're logged in there too (same account), then press Enter to save the session... ")

        context.storage_state(path=str(out_path))
        print(f"Session saved -> {out_path}")
        browser.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    from_profile = "--from-chrome-profile" in args
    auto = "--auto" in args
    args = [a for a in args if a not in ("--from-chrome-profile", "--auto")]

    if len(args) != 1 or args[0] not in config.PLATFORMS:
        print(f"Usage: python login_setup.py <platform> [--from-chrome-profile] [--auto]")
        print(f"Platforms: {list(config.PLATFORMS)}")
        sys.exit(1)

    config.SESSIONS_DIR.mkdir(exist_ok=True)
    if from_profile:
        capture_session_from_chrome_profile(args[0], auto=auto)
    else:
        capture_session(args[0], wait_for_signal=auto)
