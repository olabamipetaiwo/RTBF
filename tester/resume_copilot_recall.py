"""Completes a Copilot NL-forget recall that stopped between probes
(2026-11-01: CO-NLF-I0188's first R3 prompt hit the free-tier daily limit and got no
answer, so the run stopped with R3 unanswered and nothing else sent).

resume_recall.py cannot do this: it finds a cell's chats through ChatGPT/Claude's
conversation-list APIs, and Copilot has none. Here the cell's R3 chat is named
by URL instead, on the command line.

    python resume_copilot_recall.py CO-NLF-I0188 <R3 chat URL>            (read-only plan)
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


def _check_chat(flow: CopilotFlow, cell_id: str, probes: dict, url: str) -> tuple[int, int]:
    """Opens the R3 chat; returns (user prompts in it, replies in it). Raises on anything unexpected."""
    flow.open_conversation(url)
    flow.page.wait_for_timeout(4000)
    body = _norm(flow.page.inner_text("body"))
    if _norm(probes["r3"]) not in body:
        raise RuntimeError(f"{cell_id}: the chat at {url} does not contain this cell's R3 probe; nothing sent")
    prompts = 1 + (_norm(probes["r3_followup"]) in body)
    return prompts, flow._reply_count()


def _retry_unanswered(flow: CopilotFlow, cell_id: str) -> str:
    if (notice := LIMIT_NOTICE.search(flow.page.inner_text("body"))):
        raise RuntimeError(f"{cell_id}: daily limit still active ({notice.group(0)[:100]}); nothing sent")
    before = flow._reply_count()
    flow.page.get_by_role("button", name="Try again").click(timeout=RETRY_TIMEOUT_MS)
    return flow._wait_for_reply(before)


def resume(cell_id: str, url: str, apply: bool) -> None:
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
        titles = _sidebar_titles(flow)
        for key in ("r3_followup", "r1_open", "r1_open_followup"):
            if key != "r3_followup" and _prompt_in_sidebar(titles, probes[key]):
                raise RuntimeError(f"{cell_id}: a chat starting with the {key} prompt already exists; refusing to guess")
        prompts, replies = _check_chat(flow, cell_id, probes, url)
        todo = []
        if replies < 1:
            todo.append("r3_retry")
        if prompts == 1:
            todo.append("r3_followup")
        todo += ["r1_open", "r1_open_followup"]
        print(f"{cell_id}: R3 chat has {prompts} prompt(s) and {replies} repl(ies)")
        print(f"{cell_id}: will do {todo}; same-conversation R1 stays deferred")
        if not apply:
            print("DRY RUN -- nothing sent or written")
            return

        r3_replies = []
        if "r3_retry" in todo:
            r3_replies.append(_retry_unanswered(flow, cell_id))
        else:
            r3_replies.append(flow._last_reply_text())
        rc._save_screenshot(flow, plan.platform, cell_id, f"{SESSION}_r3")
        if "r3_followup" in todo:
            r3_replies.append(rc._send_fresh(flow, probes["r3_followup"]))
        else:
            r3_replies.append(flow._last_reply_text())
        rc._save_screenshot(flow, plan.platform, cell_id, f"{SESSION}_r3_followup")

        flow.new_conversation()
        r1_replies = [rc._send_fresh(flow, probes["r1_open"])]
        rc._save_screenshot(flow, plan.platform, cell_id, f"{SESSION}_r1_open")
        r1_replies.append(rc._send_fresh(flow, probes["r1_open_followup"]))
        rc._save_screenshot(flow, plan.platform, cell_id, f"{SESSION}_r1_open_followup")

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
                "r3_chat": url,
                "note": "R3 prompt 1 was sent before the daily limit stopped the run and got no answer; "
                        "it was answered through the chat's Try again button, not re-typed. "
                        "R2 re-read at resume (the original run's read is kept only as "
                        "03_recall_new_conversation_r2.png).",
            },
        })

    rc._finalize_recall(plan, cell_id, {"r1": r1_score, "r2": r2_score, "r3": r3_score},
                        rc.DEFERRED_SAME_CONVERSATION,
                        f"resumed-recall (interrupted by Copilot's daily limit; did at resume: {todo})")


if __name__ == "__main__":
    resume(sys.argv[1], sys.argv[2], apply="--apply" in sys.argv)
