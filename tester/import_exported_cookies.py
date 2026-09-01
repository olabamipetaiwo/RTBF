"""Converts a cookie-export-extension JSON dump (e.g. from the "Cookie-Editor"
Chrome extension's Export button) into the storage_state.json shape
Playwright expects, so `flows/<platform>.py` can load it like any other
captured session.

Why this exists: every route that had Playwright itself perform or inherit
a login (OAuth, native email/password, Chrome-profile copy, CDP-attach) got
blocked by a deliberate anti-automation defense somewhere in the chain --
confirmed live 2026-08-27 across ChatGPT specifically (Google OAuth reject,
Cloudflare "verifying you are human" hang on native login, Chrome refusing
its own remote-debugging port on the default profile, Chrome silently
dropping __Secure-/__Host- cookies from a copied profile). A cookie-export
browser extension sidesteps all of it: it's not CDP, not remote debugging,
not a copied profile -- just a normal extension reading its own browser's
current cookies via the standard chrome.cookies API, which is what
"Cookie-Editor" and similar extensions do.

Usage:
    1. In your normal, everyday Chrome (already logged into the target
       platform), install "Cookie-Editor" from the Chrome Web Store.
    2. On the platform's tab (e.g. chatgpt.com), open the extension, use its
       Export button (exports the current tab's cookies as JSON).
    3. Save that JSON to sessions/_manual_export_<platform>.json (don't
       paste it into chat -- it contains live auth tokens).
    4. python import_exported_cookies.py chatgpt

For a platform whose erasure action is cross-domain (Gemini's "Delete all
activity" opens myactivity.google.com, not gemini.google.com; Copilot's
"Privacy Dashboard" opens account.microsoft.com, not copilot.microsoft.com)
-- see flows/gemini.py's and flows/copilot.py's module docstrings -- a
single-domain session hits a sign-in wall on that second domain. Use
`merge` instead of overwriting the whole session:
    5. On the SECOND domain's tab (e.g. myactivity.google.com, already
       logged in via the same Google account), export cookies the same way,
       save to sessions/_manual_export_<platform>_<label>.json (`<label>` is
       any short tag for the domain, e.g. "myactivity" or "privacy").
    6. python import_exported_cookies.py gemini --merge myactivity
       Merges those cookies into the existing sessions/gemini.json rather
       than replacing it, so one Playwright context carries both domains'
       auth at once. Re-running with the same label re-merges (new cookies
       for a given name+domain+path win over old ones from that label).
"""

from __future__ import annotations

import argparse
import json

import config

_SAMESITE_MAP = {
    "no_restriction": "None", "unspecified": "None", "none": "None",
    "lax": "Lax", "strict": "Strict",
}


def _load_cookies(export_path) -> list[dict]:
    raw = json.loads(export_path.read_text())
    if isinstance(raw, dict) and "cookies" in raw:
        raw = raw["cookies"]  # some export formats wrap in {"cookies": [...], "url": ...}

    cookies = []
    for c in raw:
        expires = c.get("expirationDate", -1)
        if c.get("session"):
            expires = -1
        cookies.append({
            "name": c["name"],
            "value": c["value"],
            "domain": c["domain"],
            "path": c.get("path", "/"),
            "expires": expires if expires is not None else -1,
            "httpOnly": bool(c.get("httpOnly", False)),
            "secure": bool(c.get("secure", False)),
            "sameSite": _SAMESITE_MAP.get(str(c.get("sameSite", "lax")).lower(), "Lax"),
        })
    return cookies


def _report(cookies: list[dict], out_path) -> None:
    names = sorted(c["name"] for c in cookies)
    print(f"-> {out_path} now has {len(cookies)} cookies")
    print(f"Cookie names: {names}")
    auth_markers = [n for n in names if "session" in n.lower() or "auth" in n.lower()]
    if auth_markers:
        print(f"Looks like real auth cookies are present: {auth_markers}")
    else:
        print("WARNING: no cookie name looks like a session/auth token -- verify before trusting this.")


def convert(platform: str, origin: str | None = None, account_label: str | None = None) -> None:
    """origin: if a localStorage dump exists at
    sessions/_manual_localstorage_<platform>.json (see module docstring),
    it gets attached to storage_state's "origins" for this URL -- needed
    for platforms whose session lives partly/wholly in localStorage, not
    just cookies (confirmed live 2026-08-27 on Copilot: Auth0's SPA SDK
    keeps the real session tokens in localStorage under an
    "@@auth0spajs@@..." key, cookies alone weren't enough to load an
    authenticated session). Defaults to config.PLATFORMS[platform]. Fully
    replaces the existing session file -- use `merge()` instead when adding
    a second domain's cookies to an already-working session.

    `account_label` saves to a SEPARATE dedicated account's session file
    (sessions/<platform>__<account_label>.json, via config.session_path)
    instead of the main sessions/<platform>.json -- added 2026-08-31 for
    MAXIMAL cells that must not share an account with a sibling MAXIMAL
    cell (see config.py's MAXIMAL_ACCOUNT_LABEL). NOT the same thing as
    `merge()`'s `label` -- that's a second DOMAIN of the SAME account
    (e.g. myactivity.google.com), this is a wholly separate account.
    Reads from a differently-named export file
    (sessions/_manual_export_<platform>__<account_label>.json) so
    exporting a new account's cookies never overwrites the main account's
    already-saved export -- export the NEW account's cookies (logged into
    it in your everyday Chrome, same Cookie-Editor flow as usual) to that
    path first."""
    suffix = f"__{account_label}" if account_label else ""
    export_path = config.SESSIONS_DIR / f"_manual_export_{platform}{suffix}.json"
    if not export_path.exists():
        raise FileNotFoundError(
            f"Expected the extension's exported JSON at {export_path} -- save it there first."
        )

    cookies = _load_cookies(export_path)

    origins = []
    ls_path = config.SESSIONS_DIR / f"_manual_localstorage_{platform}{suffix}.json"
    if ls_path.exists():
        ls_raw = json.loads(ls_path.read_text())
        # Accept either {"key": "value", ...} or [["key", "value"], ...]
        # (both are what `JSON.stringify(localStorage)` /
        # `JSON.stringify(Object.entries(localStorage))` produce).
        items = ls_raw.items() if isinstance(ls_raw, dict) else ls_raw
        origins.append({
            "origin": origin or config.PLATFORMS[platform],
            "localStorage": [{"name": k, "value": v} for k, v in items],
        })
        print(f"Attached {len(origins[0]['localStorage'])} localStorage entries from {ls_path}")

    out_path = config.session_path(platform, account_label)
    config.SESSIONS_DIR.mkdir(exist_ok=True)
    out_path.write_text(json.dumps({"cookies": cookies, "origins": origins}, indent=2))
    print(f"Converted {len(cookies)} cookies")
    _report(cookies, out_path)


def merge(platform: str, label: str, origin: str | None = None, account_label: str | None = None) -> None:
    """Adds a second domain's cookies (and optionally localStorage) into
    the EXISTING sessions/<platform>.json (or a dedicated account's
    session, see `account_label` below), for platforms whose erasure
    action is cross-domain (see module docstring). Reads
    sessions/_manual_export_<platform>_<label>.json and
    sessions/_manual_localstorage_<platform>_<label>.json (same shape as
    convert()'s inputs, just domain-scoped and labeled). Cookies are keyed
    by (name, domain, path) -- a cookie already in the session with the
    same key gets replaced by the new export's version, everything else
    from the existing session is kept as-is.

    `account_label` merges into a SEPARATE dedicated account's session
    (sessions/<platform>__<account_label>.json) instead of the main one --
    needed for MAXIMAL cells on a dedicated account whose own erasure also
    needs a cross-domain surface (e.g. Gemini's GE-I2-E6/GE-IF-E-MAX still
    need myactivity.google.com merged in even though they're not on the
    main gemini.json). Distinct from `label`, which names the DOMAIN being
    merged, not the account."""
    export_path = config.SESSIONS_DIR / f"_manual_export_{platform}_{label}.json"
    if not export_path.exists():
        raise FileNotFoundError(
            f"Expected the extension's exported JSON at {export_path} -- save it there first."
        )
    out_path = config.session_path(platform, account_label)
    if not out_path.exists():
        raise FileNotFoundError(
            f"{out_path} doesn't exist yet -- run `convert` for {platform} "
            f"{f'(--account {account_label}) ' if account_label else ''}first, "
            f"merge only adds to an existing session."
        )

    state = json.loads(out_path.read_text())
    existing_cookies = {(c["name"], c["domain"], c["path"]): c for c in state.get("cookies", [])}
    new_cookies = _load_cookies(export_path)
    for c in new_cookies:
        existing_cookies[(c["name"], c["domain"], c["path"])] = c
    state["cookies"] = list(existing_cookies.values())

    ls_path = config.SESSIONS_DIR / f"_manual_localstorage_{platform}_{label}.json"
    if ls_path.exists():
        ls_raw = json.loads(ls_path.read_text())
        items = ls_raw.items() if isinstance(ls_raw, dict) else ls_raw
        state.setdefault("origins", []).append({
            "origin": origin or f"https://{label}",
            "localStorage": [{"name": k, "value": v} for k, v in items],
        })
        print(f"Attached {len(items) if isinstance(items, dict) else len(list(items))} localStorage entries from {ls_path}")

    out_path.write_text(json.dumps(state, indent=2))
    print(f"Merged {len(new_cookies)} cookies from label {label!r}")
    _report(state["cookies"], out_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=list(config.PLATFORMS))
    parser.add_argument("--merge", metavar="LABEL", help="merge a second domain's export into the existing session instead of replacing it")
    parser.add_argument(
        "--account", metavar="LABEL",
        help="save/merge into a SEPARATE dedicated account (e.g. --account maximal_i2) instead of "
             "the main session -- see config.py's MAXIMAL_ACCOUNT_LABEL for which cells need one.",
    )
    args = parser.parse_args()
    if args.merge:
        merge(args.platform, args.merge, account_label=args.account)
    else:
        convert(args.platform, account_label=args.account)
