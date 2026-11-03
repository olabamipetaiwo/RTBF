"""Completes a Copilot NL-forget recall that stopped between probes
(2026-11-01: CO-NLF-I0188's first R3 prompt hit the free-tier daily limit and got no
answer, so the run stopped with R3 unanswered and nothing else sent).

resume_recall.py cannot do this: it finds a cell's chats through ChatGPT/Claude's
conversation-list APIs, and Copilot has none. Here the cell's R3 chat is named
by URL instead, on the command line.

    python resume_copilot_recall.py CO-NLF-I0169 <R3 chat URL> [<R1 chat URL>]            (read-only plan)
    python resume_copilot_recall.py CO-NLF-I0188 <R3 chat URL> --apply    (send what is missing, record)

It refuses to send anything unless: the tab is signed in as the study account, no
daily-limit notice is showing, the chat's first user message is this cell's R3
probe, the R3 follow-up and both R1 prompts are not already in the account's
chat list, and the chat holds at most the R3 prompt, its reply and the follow-up.
An unanswered R3 prompt is answered through the chat's own "Try again" button, so
the prompt is not typed (and not sent) twice.

R2 is re-read at resume time, since the interrupted run's score was never saved.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timezone

import nlf_recall_scheduler as sched
import run_cell as rc
import tracking
from flows.copilot import CopilotFlow
from recall_probes_loader import load_recall_probes
from recall_scoring import NO_MEMORY_SECTION, score_attempts, token_found, unreadable_memory_page

SESSION = "03_recall_new_conversation"
LIMIT_NOTICE = re.compile(r"reached your daily limit[^\n]*", re.I)
RETRY_TIMEOUT_MS = 10_000


def _norm(text: str) -> str:
    return " ".join(text.split())


def _sidebar_titles(flow: CopilotFlow) -> list[str]:
    """Chat-list titles are cut at about 50 characters, so compare prefixes."""
    return [_norm(t) for t in flow.page.locator("nav a, aside a").all_inner_texts()]


def _prompt_in_sidebar(titles: list[str], prompt: str) -> bool:
    prefix = _norm(prompt)[:40]
    return any(t.startswith(prefix) for t in titles)


def _read_chat(flow: CopilotFlow, cell_id: str, url: str, first: str, second: str) -> tuple[int, list[str]]:
    """Opens a recall chat; returns (this cell's prompts in it, its reply texts). Raises on anything unexpected."""
    # Not flow.open_conversation(): it waits for earlier replies, and this chat may hold none.
    flow.page.goto(flow.normalize_ref(url))
    flow.page.wait_for_timeout(5000)
    body = _norm(flow.page.inner_text("main"))
    if _norm(first) not in body:
        raise RuntimeError(f"{cell_id}: the chat at {url} does not start with {first!r}; nothing sent")
    prompts = 1 + (_norm(second) in body)
    replies = [el.inner_text() for el in flow.page.query_selector_all(flow._reply_selector())]
    if len(replies) > prompts:
        raise RuntimeError(f"{cell_id}: {url} holds {len(replies)} replies for {prompts} prompts; nothing sent")
    return prompts, replies


def _retry_unanswered(flow: CopilotFlow, cell_id: str, r3_prompt: str) -> str:
    # No daily-limit pre-check here: the unanswered turn stores its own "reached your daily
    # limit" notice, so the text stays after the reset. Try again only replays the same
    # prompt; if the limit is still on, no reply appears and _wait_for_reply raises.
    before = flow._reply_count()
    seen = _norm(flow.page.inner_text("body")).count(_norm(r3_prompt))
    flow.page.get_by_role("button", name="Try again").click(timeout=RETRY_TIMEOUT_MS)
    reply = flow._wait_for_reply(before)
    if _norm(flow.page.inner_text("body")).count(_norm(r3_prompt)) > seen:
        raise RuntimeError(f"{cell_id}: Try again duplicated the R3 prompt in the chat; stopping before anything else is sent")
    return reply


def _finish_chat(flow: CopilotFlow, cell_id: str, url: str, first: str, second: str, replies: list[str],
                 prompts: int) -> tuple[list[str], list[str]]:
    """Answers whatever is missing in one two-prompt chat; returns (its two replies, what was done)."""
    done = []
    if len(replies) < prompts:  # only the last prompt can be unanswered
        replies.append(_retry_unanswered(flow, cell_id, first if prompts == 1 else second))
        done.append("retry")
    if prompts == 1:
        replies.append(rc._send_fresh(flow, second))
        done.append("followup")
    return replies, done


def resume(cell_id: str, r3_url: str, r1_url: str | None, apply: bool) -> None:
    plan = rc.load_cell(cell_id)
    entry = tracking.get(cell_id)
    if plan.platform != "copilot" or plan.sheet != "NLFORGET":
        raise RuntimeError(f"{cell_id}: resume_copilot_recall.py handles Copilot NL-forget cells only")
    if entry.get("status") != "erased":
        raise RuntimeError(f"{cell_id}: status {entry.get('status')!r}, nothing to resume")
    probes = load_recall_probes()[cell_id]
    token = probes["answer"]

    if not sched._account_ok("copilot"):
        raise RuntimeError(f"{cell_id}: tab is not signed in as the study account; nothing sent")

    with CopilotFlow(cdp_url=sched.CDP_URL) as flow:
        flow.page.goto(flow.BASE_URL)
        flow.page.wait_for_timeout(3000)
        if r1_url is None:
            titles = _sidebar_titles(flow)
            if _prompt_in_sidebar(titles, probes["r1_open"]):
                raise RuntimeError(f"{cell_id}: a chat starting with the R1 prompt already exists; pass its URL")
        r3_prompts, r3_replies = _read_chat(flow, cell_id, r3_url, probes["r3"], probes["r3_followup"])
        r1_prompts, r1_replies = (0, [])
        if r1_url:
            r1_prompts, r1_replies = _read_chat(flow, cell_id, r1_url, probes["r1_open"], probes["r1_open_followup"])
        print(f"{cell_id}: R3 chat {r3_prompts} prompt(s), {len(r3_replies)} repl(ies); "
              f"R1 chat {'none' if not r1_url else f'{r1_prompts} prompt(s), {len(r1_replies)} repl(ies)'}")
        print(f"{cell_id}: same-conversation R1 stays deferred")
        if not apply:
            print("DRY RUN -- nothing sent or written")
            return

        did: dict[str, list[str]] = {}
        flow.page.goto(flow.normalize_ref(r3_url))
        flow.page.wait_for_timeout(4000)
        r3_replies, did["r3"] = _finish_chat(flow, cell_id, r3_url, probes["r3"], probes["r3_followup"],
                                             r3_replies, r3_prompts)
        rc._save_screenshot(flow, plan.platform, cell_id, f"{SESSION}_r3_followup")

        if r1_url:
            flow.page.goto(flow.normalize_ref(r1_url))
            flow.page.wait_for_timeout(4000)
            r1_replies, did["r1"] = _finish_chat(flow, cell_id, r1_url, probes["r1_open"],
                                                 probes["r1_open_followup"], r1_replies, r1_prompts)
        else:
            flow.new_conversation()
            r1_replies = [rc._send_fresh(flow, probes["r1_open"]), rc._send_fresh(flow, probes["r1_open_followup"])]
            did["r1"] = ["open", "followup"]
        rc._save_screenshot(flow, plan.platform, cell_id, f"{SESSION}_r1_open_followup")
        todo = did

        r2_reply = flow.read_memory_settings()
        if token_found(r2_reply, token):
            r2_score = "TOKEN FOUND (auto)"
        elif (problem := unreadable_memory_page(r2_reply)) == NO_MEMORY_SECTION:
            r2_score = f"N/A ({NO_MEMORY_SECTION})"
        elif problem:
            r2_score = f"REVIEW (auto, r2): memory page not readable ({problem}) -- needs human review"
        else:
            r2_score = "NOT FOUND (auto)"
        rc._save_screenshot(flow, plan.platform, cell_id, f"{SESSION}_r2_reread")

        r3_score, r3_detail = score_attempts(r3_replies, token, rc._R3_ATTEMPTS)
        r1_score, r1_detail = score_attempts(r1_replies, token, rc._R1_ATTEMPTS)
        rc._save_json(plan.platform, cell_id, SESSION, {
            "r2_reply": r2_reply,
            "r3_sent": probes["r3"], "r3_reply": r3_replies[0],
            "r3_followup_sent": probes["r3_followup"], "r3_followup_reply": r3_replies[1],
            "r1_open_sent": probes["r1_open"], "r1_open_reply": r1_replies[0],
            "r1_open_followup_sent": probes["r1_open_followup"], "r1_open_followup_reply": r1_replies[1],
            "scoring": {"r3": r3_detail, "r1": r1_detail},
            "resumed": {
                "at": datetime.now(timezone.utc).isoformat(),
                "did": todo,
                "r3_chat": r3_url, "r1_chat": r1_url,
                "note": "the run was stopped by Copilot's daily limit; replies already in the chats were read from the "
                        "page, an unanswered prompt was answered through the chat's Try again button "
                        "(not re-typed), and only prompts not yet in a chat were sent. "
                        "R2 re-read at resume (the original run's read is kept only as "
                        "03_recall_new_conversation_r2.png).",
            },
        })

    rc._finalize_recall(plan, cell_id, {"r1": r1_score, "r2": r2_score, "r3": r3_score},
                        rc.DEFERRED_SAME_CONVERSATION,
                        f"resumed-recall (interrupted by Copilot's daily limit; did at resume: {todo})")


if __name__ == "__main__":
    urls = [a for a in sys.argv[2:] if a.startswith("http")]
    resume(sys.argv[1], urls[0], urls[1] if len(urls) > 1 else None, apply="--apply" in sys.argv)
