"""Build a Playwright storage_state.json directly from your real Chrome
profile's cookies -- no Chrome relaunch involved at all.

Why this exists (superseded the profile-copy approach in login_setup.py's
--from-chrome-profile mode): copying Chrome's profile directory and
relaunching real Chrome against the copy kept silently losing the
`__Secure-`/`__Host-` prefixed session cookies ChatGPT's auth depends on --
confirmed live 2026-08-27 across four attempts. Chrome's own cookie-store
validation on load/shutdown appears to strip these prefixed cookies when
the profile isn't the exact original one it thinks it owns, regardless of
Local State/profile-directory-name fixes. Decrypting the cookies straight
from the SQLite file and handing Playwright a storage_state built from
the plaintext values sidesteps that entirely -- Chrome itself is never
involved after this point.

macOS only. Read-only against your real Chrome profile's Cookies file --
never modifies it, never touches a live/running Chrome.

How Chrome encrypts cookies on macOS: the actual encryption key is a
password stored in macOS Keychain under "Chrome Safe Storage" (shared by
every Chrome profile on this machine, not per-profile). Each
`encrypted_value` blob is `b"v10" + AES-128-CBC(...)` using a key derived
from that password via PBKDF2-HMAC-SHA1 (salt=b"saltysalt", 1003
iterations, 16-byte key), a fixed all-space IV, PKCS7 padding, and (recent
Chrome versions) a leading integrity byte on the decrypted plaintext.

Usage:
    python extract_chrome_cookies.py chatgpt --profile "Profile 7"
"""

from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

import config

REAL_CHROME_DIR = Path.home() / "Library/Application Support/Google/Chrome"

# Platform -> the cookie host suffixes worth pulling. Broader than just the
# login domain since auth/session validation often spans subdomains (e.g.
# ChatGPT's auth.openai.com, ws.chatgpt.com).
COOKIE_DOMAINS = {
    "chatgpt": ["chatgpt.com", "openai.com"],
    "claude": ["claude.ai", "anthropic.com"],
    "gemini": ["google.com", "gemini.google.com"],
    "copilot": ["microsoft.com", "bing.com", "copilot.microsoft.com"],
    "perplexity": ["perplexity.ai"],
    "deepseek": ["deepseek.com"],
}

# playwright storage_state sameSite values
_SAMESITE_MAP = {-1: "None", 0: "None", 1: "Lax", 2: "Strict"}


def _get_safe_storage_password() -> bytes:
    out = subprocess.run(
        ["security", "find-generic-password", "-w", "-s", "Chrome Safe Storage"],
        capture_output=True, text=True, timeout=30,
    )
    if out.returncode != 0:
        raise RuntimeError(
            f"Couldn't read 'Chrome Safe Storage' from Keychain (exit {out.returncode}): "
            f"{out.stderr.strip()}. If macOS popped a permission dialog, approve it and re-run."
        )
    return out.stdout.strip().encode("utf-8")


def _derive_key(password: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA1(), length=16, salt=b"saltysalt", iterations=1003
    )
    return kdf.derive(password)


def _decrypt_cookie_value(encrypted_value: bytes, key: bytes) -> str | None:
    if not encrypted_value:
        return ""
    if not encrypted_value.startswith(b"v10") and not encrypted_value.startswith(b"v11"):
        # Unencrypted/legacy -- shouldn't normally happen on a modern macOS Chrome.
        return None
    ciphertext = encrypted_value[3:]
    iv = b" " * 16
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()
    pad_len = padded[-1]
    if not (1 <= pad_len <= 16):
        return None
    plaintext = padded[:-pad_len]
    # Recent Chrome versions prefix decrypted cookie plaintext with a
    # 32-byte SHA256 "integrity" hash before the real value on some
    # platforms -- strip it if present (real value is UTF-8 printable,
    # the hash prefix isn't).
    try:
        return plaintext.decode("utf-8")
    except UnicodeDecodeError:
        if len(plaintext) > 32:
            try:
                return plaintext[32:].decode("utf-8")
            except UnicodeDecodeError:
                return None
        return None


def _copy_cookies_db_readonly(source_profile: str) -> Path:
    src = REAL_CHROME_DIR / source_profile / "Cookies"
    if not src.exists():
        raise FileNotFoundError(f"No Cookies file at {src}")
    tmp_dir = Path(tempfile.mkdtemp(prefix="chrome_cookies_"))
    dst = tmp_dir / "Cookies"
    shutil.copy2(src, dst)
    return dst


def extract_cookies(platform: str, source_profile: str) -> list[dict]:
    domains = COOKIE_DOMAINS[platform]
    key = _derive_key(_get_safe_storage_password())

    db_copy = _copy_cookies_db_readonly(source_profile)
    conn = sqlite3.connect(str(db_copy))
    conn.row_factory = sqlite3.Row
    where = " OR ".join("host_key LIKE ?" for _ in domains)
    params = [f"%{d}%" for d in domains]
    rows = conn.execute(
        f"SELECT host_key, name, value, encrypted_value, path, expires_utc, "
        f"is_secure, is_httponly, samesite, has_expires FROM cookies WHERE {where}",
        params,
    ).fetchall()
    conn.close()
    shutil.rmtree(db_copy.parent, ignore_errors=True)

    cookies = []
    skipped = []
    for row in rows:
        value = row["value"] or _decrypt_cookie_value(row["encrypted_value"], key)
        if value is None:
            skipped.append(f"{row['host_key']}{row['name']}")
            continue
        # Chrome epoch (microseconds since 1601-01-01) -> Unix seconds.
        if row["has_expires"] and row["expires_utc"]:
            expires = row["expires_utc"] / 1_000_000 - 11644473600
        else:
            expires = -1
        cookies.append({
            "name": row["name"],
            "value": value,
            "domain": row["host_key"],
            "path": row["path"],
            "expires": expires,
            "httpOnly": bool(row["is_httponly"]),
            "secure": bool(row["is_secure"]),
            "sameSite": _SAMESITE_MAP.get(row["samesite"], "Lax"),
        })

    if skipped:
        print(f"Warning: couldn't decrypt {len(skipped)} cookie(s): {skipped}")
    return cookies


def build_storage_state(platform: str, source_profile: str) -> None:
    cookies = extract_cookies(platform, source_profile)
    out_path = config.session_path(platform)
    config.SESSIONS_DIR.mkdir(exist_ok=True)

    state = {"cookies": cookies, "origins": []}
    out_path.write_text(json.dumps(state, indent=2))

    names = sorted(c["name"] for c in cookies)
    print(f"Extracted {len(cookies)} cookies -> {out_path}")
    print(f"Cookie names: {names}")

    auth_markers = [n for n in names if "session" in n.lower() or "auth" in n.lower()]
    if auth_markers:
        print(f"Looks like real auth cookies are present: {auth_markers}")
    else:
        print("WARNING: no cookie name looks like a session/auth token -- "
              "this may not actually be a logged-in session. Verify before trusting it.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=list(COOKIE_DOMAINS))
    parser.add_argument("--profile", default="Profile 7", help="Chrome profile folder name (default: 'Profile 7')")
    args = parser.parse_args()
    build_storage_state(args.platform, args.profile)
