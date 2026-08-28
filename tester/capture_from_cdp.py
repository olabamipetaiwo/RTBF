"""Attach to an already-running, already-logged-in Chrome (launched with
--remote-debugging-port by the user themselves -- see login_setup.py's
module docstring for why launching that isn't done from here) and save its
storage_state for a platform. Read-only against the live session: doesn't
navigate through any login/OAuth flow, just asks the existing authenticated
context for its cookies + localStorage.

Usage:
    python capture_from_cdp.py chatgpt --cdp-url http://localhost:9222
"""

from __future__ import annotations

import argparse

from playwright.sync_api import sync_playwright

import config


def capture(platform: str, cdp_url: str) -> None:
    out_path = config.session_path(platform)
    config.SESSIONS_DIR.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(cdp_url)
        context = browser.contexts[0]
        pages = [pg for pg in context.pages if "chatgpt.com" in pg.url or "openai.com" in pg.url]
        page = pages[0] if pages else context.pages[0]

        shot_path = config.SESSIONS_DIR / f"_check_{platform}_cdp.png"
        page.screenshot(path=str(shot_path))
        print(f"Current page: {page.url}")
        print(f"Screenshot -> {shot_path}")

        context.storage_state(path=str(out_path))
        print(f"Session saved -> {out_path}")

        cookie_names = sorted(c["name"] for c in context.cookies() if "chatgpt" in c["domain"] or "openai" in c["domain"])
        print(f"Cookie names: {cookie_names}")

        browser.close()  # disconnects CDP only -- does not close the user's Chrome


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=list(config.PLATFORMS))
    parser.add_argument("--cdp-url", default="http://localhost:9222")
    args = parser.parse_args()
    capture(args.platform, args.cdp_url)
