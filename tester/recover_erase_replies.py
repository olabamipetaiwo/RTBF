"""Reloads an incomplete NL-forget erase conversation and captures a full-page
screenshot, so `extract_erase_replies.py --fullpage` can re-OCR a reply the
original 1280x720 viewport grab cut off.

The original erase step only saved the method's name in `02_erase.json`, so the
reply itself survived only as `screenshots/02_erase.png` -- a 1280x720 viewport
capture. For 194 of the 785 NL-forget cells the viewport cropped the reply (103
cut off at the input box, 75 with the request scrolled past the top, 15 captured
before the reply arrived, 2 covered by a modal). D2b (`notes/task.md`) asked
whether to recover these by reloading the stored conversations or report them
uncaptured -- the user picked "recover all 194 cells, full-page screenshot".

What this script does, per cell:

  1. Look up the conversation URL for `cell_id` in `data/run_tracking.json`
     (`injection_ref`, captured and verified at injection time) and the token
     text from the shared xlsx via `run_cell.load_cell()`.
  2. Open the NL-forget session for `platform` (`sessions/<platform>__nlforget
     .json`) via the existing `PlatformFlow`, navigate to that URL.
  3. Confirm the token is still in the body -- the same session/erasure
     guarantee the original injection check used (`run_cell.py` ~L540). A
     logged-out session, a deleted conversation, or a reset history all trip
     this and the cell is skipped rather than silently captured against a
     login screen.
  4. Set the viewport tall enough to show the whole thread (`document.body
     .scrollHeight + buffer`), scroll any virtualized inner panes to the
     bottom to force lazy content, and screenshot to `screenshots/02_erase
     _fullpage.png`. The original `02_erase.png` is kept untouched.

What this script does NOT do: write back into `02_erase.json`. That's
`extract_erase_replies.py --fullpage`'s job, so the OCR pipeline stays the
single writer of `reply_text`/`reply_status` across all 785 cells.

Order and rate limits: the 2026-09-11 batch-injection finding (ChatGPT soft
rate limit after ~44 back-to-back requests, per
`feedback-batch-injections-to-avoid-rate-limits` memory) applies to any heavy
loop against these platforms. This script batches 40 cells per platform with a
10-min cooldown between batches, which is the policy the live NL-forget
injection run converged on.

    python recover_erase_replies.py                                # all platforms, default settings
    python recover_erase_replies.py --only perplexity,deepseek     # just the first wave with live sessions
    python recover_erase_replies.py --only perplexity --limit 1    # one-cell smoke test
    python recover_erase_replies.py --force                        # redo cells that already have a 02_erase_rescroll.png
    python recover_erase_replies.py --dry-run                      # print the plan, don't open a browser
"""

from __future__ import annotations

import argparse
import json
import time
from collections import deque
from pathlib import Path

from playwright.sync_api import sync_playwright

import config
import tracking
from flows.chatgpt import ChatGPTFlow
from flows.claude import ClaudeFlow
from flows.copilot import CopilotFlow
from flows.deepseek import DeepSeekFlow
from flows.gemini import GeminiFlow
from flows.perplexity import PerplexityFlow
from run_cell import load_cell

FLOW_REGISTRY = {
    "chatgpt": ChatGPTFlow,
    "claude": ClaudeFlow,
    "copilot": CopilotFlow,
    "deepseek": DeepSeekFlow,
    "gemini": GeminiFlow,
    "perplexity": PerplexityFlow,
}

# Perplexity 83 and DeepSeek 72 are the dominant piles (cut_off and
# start_not_visible respectively), so recovery sessions are driven in that
# order to catch the hardest cases first. ChatGPT and Claude are quick after.
# Copilot and Gemini NL-forget sessions were logged out as of 2026-09-23 and
# wait on a fresh cookie export (see `notes/task.md` D2b).
PLATFORM_ORDER = ["perplexity", "deepseek", "chatgpt", "claude", "copilot", "gemini"]

# `extract_erase_replies.extract_reply`'s own status vocabulary. Everything
# other than `complete`/`check` means the viewport cropped the reply, which is
# exactly what this script is here to recover.
INCOMPLETE_STATUSES = {"cut_off", "start_not_visible", "no_reply_visible", "covered"}

BATCH_SIZE = 40
COOLDOWN_SECONDS = 600
# Instead of resizing the viewport to the thread's "full" height -- which blows
# up on sidebar-dominated pages (Perplexity's past-conversations list etc.
# makes document.body.scrollHeight ~30000 px, which Vision OCR then downsamples
# into garbage) -- the recovery keeps the normal 1280x720 viewport and scrolls
# the request bubble to the top of it, so the erase reply fills the visible
# area below. Taken 2026-10-02 after a tall-viewport batch produced mostly
# `no_reply_visible` and low-confidence OCR.
SETTLE_MS = 2500
POST_RESIZE_MS = 600
RESCROLL_SCREENSHOT = "02_erase_rescroll.png"
# Hard ceiling on the resized viewport height so a stray un-hidden
# scroll container (sidebar variant we missed) can't blow up the
# image size and trigger Vision OCR's long-image downsampling. 3500 px
# covers ~90-line replies at chat-UI density, which is far longer than
# any erase reply observed in the study.
VIEWPORT_CEILING_PX = 3500
EARLY_ABORT_FAILS = 5  # bail only after this many consecutive failures with zero successes -- old MASTER cells sometimes fail individually, so a hair-trigger of 2 was dropping a healthy platform


def find_incomplete_cells(only_incomplete: bool = True) -> list[tuple[str, str, Path]]:
    """(platform, cell_id, 02_erase.json path) for every NLFORGET-sheet cell
    (cell_id contains `-NLF-`) whose captured reply status is incomplete. The
    13 MASTER-sheet NL-forget cells (e.g. PE-I1-E1, DE-I1-E3) share the same
    "NL forget prompt" erasure type and would otherwise match, but they ran
    on different accounts than this script's `nlforget` session; they're
    recorded as uncaptured in Limitations instead of chased separately.

    When `only_incomplete` is False, every NLFORGET cell is returned
    regardless of status -- used by `--cell` so a smoke-test can re-run a
    cell that was already partially recovered."""
    targets = []
    for path in sorted(config.TRANSCRIPTS_DIR.glob("*/*/json/02_erase.json")):
        cell_id = path.parts[-3]
        if "-NLF-" not in cell_id:
            continue
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        if not str(data.get("erasure_type_text", "")).startswith("NL forget"):
            continue
        if only_incomplete and data.get("reply_status") not in INCOMPLETE_STATUSES:
            continue
        targets.append((path.parts[-4], cell_id, path))
    return targets


_SCROLL_REQUEST_TO_TOP = r"""
    (snippet) => {
        const target = snippet.toLowerCase();
        const panes = Array.from(document.querySelectorAll('*')).filter(el => {
            try { return el.scrollHeight > el.clientHeight + 1 && el.clientHeight > 100; }
            catch (e) { return false; }
        });
        panes.forEach(el => { try { el.scrollTop = 0; } catch(e){} });
        // Prefer the FIRST text node that contains the snippet. On DeepSeek
        // some cells show the erase request sent twice (a retry pattern in
        // the live run); the first copy's reply is complete above the
        // viewport fold, the second copy's reply gets cropped. Last-match
        // would always lose the complete first reply. Last-match was tried
        // for Gemini (GE-NLF-I0044/I0240) but those cells don't contain the
        // erase request in the DOM at all -- a separate problem.
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        while (node = walker.nextNode()) {
            if (node.textContent && node.textContent.toLowerCase().includes(target)) {
                const el = node.parentElement;
                if (!el) continue;
                try { el.scrollIntoView({block: 'start', inline: 'nearest'}); return true; }
                catch (e) { return false; }
            }
        }
        return false;
    }
"""


def _recover_single_screenshot(page, screenshot_path: Path) -> None:
    screenshot_path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(screenshot_path))


_HIDE_SIDEBAR = """
    () => {
        // Chat UIs put a sidebar / past-conversation list / nav column
        // alongside the chat column. Hiding them before measuring page
        // height stops Perplexity/DeepSeek-style infinite-scroll sidebars
        // from pushing document.body.scrollHeight to tens of thousands of
        // pixels (confirmed live 2026-10-02 on an earlier run where the
        // sidebar scroll pushed viewport to 1280x28000+ and Vision OCR
        // downsampled the chat content into garbage).
        const selectors = ['nav', 'aside', '[role="navigation"]', '[role="complementary"]'];
        const hidden = [];
        for (const sel of selectors) {
            document.querySelectorAll(sel).forEach(el => {
                hidden.push([el, el.style.display]);
                el.style.display = 'none';
            });
        }
        return hidden.length;
    }
"""


def recover_cell(flow, cell_id: str, injection_ref: str, token: str, request_text: str, screenshot_path: Path) -> dict:
    page = flow.page
    page.set_viewport_size({"width": 1280, "height": 720})
    page.goto(injection_ref, wait_until="domcontentloaded")
    page.wait_for_timeout(SETTLE_MS)

    body = page.locator("body").inner_text()
    if token and token.strip().lower() not in body.lower():
        final_url = page.url
        login_markers = ("login", "sign-in", "sign_in", "signin", "auth")
        looks_logged_out = any(m in final_url.lower() for m in login_markers)
        looks_logged_out = looks_logged_out or any(
            m in body.lower() for m in ("log in", "sign in to continue", "please sign in")
        )
        reason = "login redirect / logged out" if looks_logged_out else "conversation gone / token missing"
        return {
            "ok": False,
            "reason": f"{reason} (landed on {final_url[:80]!r}, body {len(body)} chars)",
            "logged_out": looks_logged_out,
        }

    # The viewport screenshot taken at erase time cropped the reply because
    # the chat UI's auto-scroll left the composer and the end of the reply
    # at the bottom, with the request (and often the start of the reply)
    # scrolled off the top. Fix it on reload by positioning the request
    # bubble at the top of the viewport ourselves -- a text-content lookup
    # that works across platforms without per-platform selectors. The
    # request's first ~60 characters are enough to disambiguate (every
    # erase request text in the NL-forget sheet is unique).
    snippet = (request_text or "").strip()[:60]
    scrolled = False
    if snippet:
        try:
            scrolled = bool(page.evaluate(_SCROLL_REQUEST_TO_TOP, snippet))
        except Exception:
            scrolled = False
    if not scrolled:
        page.evaluate("() => { window.scrollTo(0, document.body.scrollHeight); }")
    page.wait_for_timeout(POST_RESIZE_MS)

    # Hide the sidebar before measuring page height, then grow the viewport
    # just enough to fit the chat column so the whole reply is in one
    # screenshot. The measure-resize cycle runs until scrollHeight stops
    # growing (chat UIs lazy-render content below the fold on resize), with
    # a hard ceiling as a safety net. If the content fits in 720 (the
    # normal viewport), the resize is a no-op.
    try:
        page.evaluate(_HIDE_SIDEBAR)
    except Exception:
        pass

    def _measure() -> int:
        try:
            return int(page.evaluate(
                "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
            ) or 720)
        except Exception:
            return 720

    target_h = 720
    for _ in range(4):
        scroll_h = _measure()
        new_target = min(max(720, scroll_h + 300), VIEWPORT_CEILING_PX)
        if new_target <= target_h:
            break
        target_h = new_target
        page.set_viewport_size({"width": 1280, "height": target_h})
        page.wait_for_timeout(POST_RESIZE_MS)

    if target_h > 720 and snippet and scrolled:
        try:
            page.evaluate(_SCROLL_REQUEST_TO_TOP, snippet)
            page.wait_for_timeout(POST_RESIZE_MS)
        except Exception:
            pass

    _recover_single_screenshot(page, screenshot_path)
    return {"ok": True, "scrolled_to_request": scrolled, "viewport_h": target_h}


def _parse_platforms(raw: str | None) -> list[str]:
    if not raw:
        return PLATFORM_ORDER
    requested = [p.strip() for p in raw.split(",") if p.strip()]
    unknown = [p for p in requested if p not in FLOW_REGISTRY]
    if unknown:
        raise SystemExit(f"unknown platform(s): {unknown}; expected a subset of {list(FLOW_REGISTRY)}")
    return requested


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", help="Comma-separated platform list; default is all six in PLATFORM_ORDER.")
    parser.add_argument("--cell", help="Run only this one cell id (bypasses --only/--limit). Useful for a smoke test.")
    parser.add_argument("--limit", type=int, help="Only the first N cells per platform (trial runs).")
    parser.add_argument("--force", action="store_true", help="Re-capture cells that already have a 02_erase_rescroll.png.")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan and exit; do not open a browser.")
    parser.add_argument("--headless", action="store_true", help="Run the browser headless. Not recommended (Cloudflare on Claude/Perplexity).")
    args = parser.parse_args()

    requested = _parse_platforms(args.only)
    all_targets = find_incomplete_cells(only_incomplete=not args.cell)
    if args.cell:
        all_targets = [t for t in all_targets if t[1] == args.cell]
        if not all_targets:
            raise SystemExit(f"--cell {args.cell!r}: no 02_erase.json found for this NL-forget cell")
        requested = [all_targets[0][0]]
    by_platform: dict[str, list[tuple[str, Path]]] = {}
    for platform, cell_id, path in all_targets:
        by_platform.setdefault(platform, []).append((cell_id, path))
    for cells in by_platform.values():
        cells.sort(key=lambda cp: cp[0])

    for platform in requested:
        cells = by_platform.get(platform, [])
        if args.limit is not None:
            cells = cells[: args.limit]
        if not cells:
            print(f"[{platform}] nothing incomplete")
            continue

        pending: list[tuple[str, Path, Path]] = []
        for cell_id, erase_json in cells:
            fullpage = erase_json.parent.parent / "screenshots" / "02_erase_rescroll.png"
            if fullpage.exists() and not args.force:
                continue
            pending.append((cell_id, erase_json, fullpage))

        if not pending:
            print(f"[{platform}] {len(cells)} incomplete, all already captured; pass --force to redo")
            continue

        print(f"[{platform}] {len(pending)} to recover (of {len(cells)} incomplete)")
        if args.dry_run:
            for cell_id, _, _ in pending[:5]:
                print(f"  would recover {cell_id}")
            if len(pending) > 5:
                print(f"  ... and {len(pending) - 5} more")
            continue

    # Build per-platform work queues up front so the scheduler below can
    # treat them uniformly. Platforms with nothing to do are dropped.
    platform_queues: dict[str, deque] = {}
    for platform in requested:
        cells = by_platform.get(platform, [])
        if args.limit is not None:
            cells = cells[: args.limit]
        if not cells:
            print(f"[{platform}] nothing incomplete")
            continue
        pending = [
            (cid, ej, ej.parent.parent / "screenshots" / "02_erase_rescroll.png")
            for cid, ej in cells
            if args.force or not (ej.parent.parent / "screenshots" / "02_erase_rescroll.png").exists()
        ]
        if not pending:
            print(f"[{platform}] {len(cells)} incomplete, all already captured; pass --force to redo")
            continue
        print(f"[{platform}] {len(pending)} to recover (of {len(cells)} incomplete)")
        platform_queues[platform] = deque(pending)

    if args.dry_run:
        for platform, pending in platform_queues.items():
            for cid, _, _ in list(pending)[:5]:
                print(f"  would recover {cid}")
            if len(pending) > 5:
                print(f"  ... and {len(pending) - 5} more on {platform}")
        return

    if not platform_queues:
        return

    # Open every platform's session up front and rotate through them one cell
    # at a time (round-robin). This interleaves the work: when Perplexity hits
    # its 40-cell batch boundary and goes into its per-platform cooldown, the
    # scheduler keeps serving DeepSeek/ChatGPT/Claude instead of sleeping.
    # The per-platform `cooldown_until` wall-clock means a slow platform
    # can't block a fast one.
    flow_contexts: dict[str, object] = {}
    flows: dict[str, object] = {}
    stats = {p: {"done": 0, "skipped": 0, "errors": 0} for p in platform_queues}
    cooldown_until = {p: 0.0 for p in platform_queues}
    cells_since_cooldown = {p: 0 for p in platform_queues}

    # One Playwright driver shared across every platform's PlatformFlow,
    # because sync_playwright() cannot be started twice in the same thread
    # ("using Playwright Sync API inside the asyncio loop"). Each platform
    # still gets its own Chrome launch + browser context + page -- the share
    # is only at the driver level. The explicit start/stop pair wraps the
    # whole scheduler so the driver is torn down even if a cell raises.
    shared_pw = sync_playwright().start()
    try:
        for platform in list(platform_queues):
            Flow = FLOW_REGISTRY[platform]
            try:
                ctx = Flow(headless=args.headless, session_label="nlforget", playwright=shared_pw)
                flows[platform] = ctx.__enter__()
                flow_contexts[platform] = ctx
                print(f"[{platform}] session opened")
            except FileNotFoundError as exc:
                print(f"[{platform}] session not found: {exc}; skipping this platform")
                del platform_queues[platform]
            except Exception as exc:
                print(f"[{platform}] platform session failed to open: {exc}; skipping this platform")
                del platform_queues[platform]

        rotation = deque(p for p in requested if p in platform_queues)

        while rotation:
            now = time.monotonic()
            # Pick the next platform at the front of the rotation whose
            # cooldown has elapsed. If every platform is cooling, sleep until
            # the earliest finishes -- but with 4 platforms rotating this is
            # rare, since cycling through the others typically absorbs the
            # 10-minute wait.
            picked = None
            for _ in range(len(rotation)):
                p = rotation[0]
                if cooldown_until[p] <= now:
                    picked = p
                    break
                rotation.rotate(-1)
            if picked is None:
                earliest = min(cooldown_until[p] for p in rotation)
                wait = max(1, int(earliest - now) + 1)
                print(f"[scheduler] all {len(rotation)} platforms cooling, sleeping {wait}s")
                time.sleep(wait)
                continue

            cell_id, _erase_json, fullpage_path = platform_queues[picked].popleft()
            cells_since_cooldown[picked] += 1
            flow = flows[picked]
            handled = False

            try:
                plan = load_cell(cell_id)
            except Exception as exc:
                print(f"[{picked}] {cell_id} load_cell failed: {exc}")
                stats[picked]["skipped"] += 1
                handled = True

            if not handled:
                entry = tracking.get(cell_id)
                injection_ref = (entry or {}).get("injection_ref")
                if not injection_ref:
                    print(f"[{picked}] {cell_id} no injection_ref in tracking.json")
                    stats[picked]["skipped"] += 1
                    handled = True

            if not handled:
                try:
                    result = recover_cell(flow, cell_id, injection_ref, plan.token, plan.erasure_request_text or "", fullpage_path)
                except Exception as exc:
                    print(f"[{picked}] {cell_id} FAILED: {exc}")
                    stats[picked]["errors"] += 1
                else:
                    if result["ok"]:
                        stats[picked]["done"] += 1
                        remaining = len(platform_queues[picked])
                        print(f"[{picked}] {cell_id} captured  (done={stats[picked]['done']}, left={remaining})")
                    else:
                        print(f"[{picked}] {cell_id} skipped: {result['reason']}")
                        stats[picked]["skipped"] += 1

            # Early-abort guard: if the platform has produced zero successes
            # and two failures or skips in a row, treat the session as dead
            # and drop the rest of its queue. Prevents a logged-out session
            # from hammering through its whole backlog as noise.
            if stats[picked]["done"] == 0 and (stats[picked]["errors"] + stats[picked]["skipped"]) >= EARLY_ABORT_FAILS:
                print(f"[{picked}] {EARLY_ABORT_FAILS} early failures with no successes -- likely a dead session, dropping this platform's remaining {len(platform_queues[picked])} cells")
                platform_queues[picked].clear()

            # Per-platform batch boundary. Only arm the cooldown if there's
            # more work waiting; a drained queue needs no further rest.
            if cells_since_cooldown[picked] >= BATCH_SIZE and platform_queues[picked]:
                cooldown_until[picked] = time.monotonic() + COOLDOWN_SECONDS
                cells_since_cooldown[picked] = 0
                print(f"[{picked}] batch of {BATCH_SIZE} done, cooldown {COOLDOWN_SECONDS}s armed; other platforms continue")

            if platform_queues[picked]:
                rotation.rotate(-1)
            else:
                rotation.remove(picked)
                print(f"[{picked}] platform complete: {stats[picked]}")
    finally:
        for platform, ctx in flow_contexts.items():
            try:
                ctx.__exit__(None, None, None)
            except Exception:
                pass
        try:
            shared_pw.stop()
        except Exception:
            pass

    print("\n=== summary ===")
    for p, s in stats.items():
        print(f"  {p:12s} done={s['done']:4d}  skipped={s['skipped']:3d}  errors={s['errors']:3d}")


if __name__ == "__main__":
    main()
