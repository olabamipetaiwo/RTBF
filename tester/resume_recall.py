"""Completes a ChatGPT or Claude NL-forget recall that was interrupted between probes
(2026-10-18: CH-NLF-I0371 was cut off by a pkill after R3, CH-NLF-I0293 by
ChatGPT's rate limit before its second R1 prompt). Re-running such a cell
from the start would send its probes twice, so this finds the cell's own
recall conversations, checks exactly which probes already reached them,
sends only the missing ones, and then records the cell through the same
run_cell._finalize_recall() as a normal recall.

    python resume_recall.py CH-NLF-I0293            (read-only: find, check, print the plan)
    python resume_recall.py CH-NLF-I0293 --apply    (send the missing probes and record)

Finding the conversations: ChatGPT titles chats with generated summaries,
so they are found by their first user message instead, through the web
app's own conversation list (/backend-api/conversations, read with the
logged-in session), limited to chats created while the cell was running
(from its recall screenshots' times). The tool refuses to send anything if
a probe appears twice, a chat holds anything other than this cell's
probes in order, or a sent probe has no reply.

R2 (memory page) is re-read at resume time, since the interrupted run kept
only its screenshot; the transcript says so.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone

import config
import run_cell as rc
import tracking
from flows.chatgpt import ChatGPTFlow
from flows.claude import ClaudeFlow
from recall_probes_loader import load_recall_probes
from recall_scoring import NO_MEMORY_SECTION, score_attempts, unreadable_memory_page
from recall_scoring import token_found

SESSION = "03_recall_new_conversation"

_CLAUDE_LIST_JS = """async () => {
  const org = document.cookie.split('; ').find(c => c.startsWith('lastActiveOrg='))?.split('=')[1];
  const r = await fetch(`/api/organizations/${org}/chat_conversations?limit=100`);
  let body = null; try { body = await r.json(); } catch (e) {}
  const items = Array.isArray(body) ? body.map(c => ({id: c.uuid, create_time: c.created_at})) : null;
  return {status: r.status, items, detail: Array.isArray(body) ? null : JSON.stringify(body).slice(0, 200)};
}"""

_CLAUDE_CONV_JS = """async (id) => {
  const org = document.cookie.split('; ').find(c => c.startsWith('lastActiveOrg='))?.split('=')[1];
  const c = await (await fetch(`/api/organizations/${org}/chat_conversations/${id}?tree=False&rendering_mode=messages`)).json();
  return (c.chat_messages || []).map(m => ({
    role: m.sender === 'human' ? 'user' : 'assistant',
    text: (Array.isArray(m.content) ? m.content.filter(x => x.type === 'text').map(x => x.text).join('\\n') : (m.text || '')).trim(),
  })).filter(m => m.text);
}"""
WINDOW_MARGIN = timedelta(minutes=5)

_LIST_JS = """async () => {
  const s = await (await fetch('/api/auth/session')).json();
  const h = {Authorization: 'Bearer ' + s.accessToken};
  const r = await fetch('/backend-api/conversations?offset=0&limit=100&order=updated', {headers: h});
  let body = null; try { body = await r.json(); } catch (e) {}
  return {status: r.status, items: body && body.items, detail: body && body.detail};
}"""

_CONV_JS = """async (id) => {
  const s = await (await fetch('/api/auth/session')).json();
  const h = {Authorization: 'Bearer ' + s.accessToken};
  const c = await (await fetch('/backend-api/conversation/' + id, {headers: h})).json();
  const out = []; let node = c.current_node;
  while (node) {
    const m = c.mapping[node].message;
    if (m && ['user', 'assistant'].includes(m.author.role) && m.content && m.content.parts) {
      const text = m.content.parts.filter(p => typeof p === 'string').join('\\n').trim();
      if (text) out.unshift({role: m.author.role, text});
    }
    node = c.mapping[node].parent;
  }
  return out;
}"""


PLATFORMS = {
    "chatgpt": {"flow": ChatGPTFlow, "list_js": _LIST_JS, "conv_js": _CONV_JS, "url": "https://chatgpt.com/c/{}"},
    "claude": {"flow": ClaudeFlow, "list_js": _CLAUDE_LIST_JS, "conv_js": _CLAUDE_CONV_JS, "url": "https://claude.ai/chat/{}"},
}


def _window(platform: str, cell_id: str) -> tuple[datetime, datetime]:
    _, shots = rc._cell_dir(platform, cell_id)
    times = [datetime.fromtimestamp(p.stat().st_mtime, timezone.utc) for p in shots.glob(f"{SESSION}_*.png")]
    if not times:
        raise RuntimeError(f"{cell_id}: no recall screenshots, nothing to resume")
    return min(times) - WINDOW_MARGIN, max(times) + WINDOW_MARGIN


def _ts(value) -> datetime:
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, timezone.utc)
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def discover(flow, platform: str, cell_id: str, probes: dict) -> dict:
    """Returns {"r3": conv|None, "r1": conv|None}; conv = {id, messages}. Raises on anything unexpected."""
    adapter = PLATFORMS[platform]
    start, end = _window(platform, cell_id)
    for attempt in range(4):
        listing = flow.page.evaluate(adapter["list_js"])
        if listing["items"] is not None:
            items = listing["items"]
            break
        print(f"{cell_id}: conversation list unavailable (HTTP {listing['status']}: {listing['detail']}); "
              f"retrying in 60s", flush=True)
        flow.page.wait_for_timeout(60_000)
    else:
        raise RuntimeError(f"{cell_id}: conversation list unavailable after 4 tries; nothing sent")
    found: dict[str, list] = {"r3": [], "r1": []}
    for it in items:
        if not (start <= _ts(it["create_time"]) <= end):
            continue
        msgs = flow.page.evaluate(adapter["conv_js"], it["id"])
        users = [m["text"] for m in msgs if m["role"] == "user"]
        for kind, first, second in (("r3", probes["r3"], probes["r3_followup"]),
                                    ("r1", probes["r1_open"], probes["r1_open_followup"])):
            if users and users[0] == first:
                if users not in ([first], [first, second]):
                    raise RuntimeError(f"{cell_id}: {kind} chat {it['id']} holds unexpected messages: {users}")
                found[kind].append({"id": it["id"], "messages": msgs})
    result = {}
    for kind, convs in found.items():
        if len(convs) > 1:
            raise RuntimeError(f"{cell_id}: {len(convs)} chats start with the {kind} probe; refusing to guess")
        conv = convs[0] if convs else None
        if conv:
            roles = [m["role"] for m in conv["messages"]]
            if roles != ["user", "assistant"] * (len(roles) // 2) or len(roles) % 2:
                raise RuntimeError(f"{cell_id}: {kind} chat {conv['id']} has a probe without a reply: {roles}")
        result[kind] = conv
    return result


def _plan(convs: dict) -> list[str]:
    todo = []
    r3_users = [m for m in (convs["r3"] or {}).get("messages", []) if m["role"] == "user"]
    r1_users = [m for m in (convs["r1"] or {}).get("messages", []) if m["role"] == "user"]
    if not r3_users:
        raise RuntimeError("no R3 chat found; this cell did not get far enough to resume (re-run it normally)")
    if len(r3_users) == 1:
        todo.append("r3_followup")
    if len(r1_users) == 0:
        todo += ["r1_open", "r1_open_followup"]
    elif len(r1_users) == 1:
        todo.append("r1_open_followup")
    return todo


def _replies(conv: dict | None) -> list[str]:
    return [m["text"] for m in (conv or {}).get("messages", []) if m["role"] == "assistant"]


def resume(cell_id: str, apply: bool) -> None:
    plan = rc.load_cell(cell_id)
    entry = tracking.get(cell_id)
    platform = plan.platform
    if platform not in PLATFORMS or plan.sheet != "NLFORGET":
        raise RuntimeError(f"{cell_id}: resume_recall.py handles ChatGPT/Claude NL-forget cells only")
    adapter = PLATFORMS[platform]
    if entry.get("status") != "erased":
        raise RuntimeError(f"{cell_id}: status {entry.get('status')!r}, nothing to resume")
    probes = load_recall_probes()[cell_id]
    token = probes["answer"]

    with adapter["flow"](session_label="nlforget") as flow:
        convs = discover(flow, platform, cell_id, probes)
        todo = _plan(convs)
        print(f"{cell_id}: R3 chat {convs['r3']['id']} has {len(_replies(convs['r3']))} answered probe(s); "
              f"R1 chat {convs['r1']['id'] if convs['r1'] else 'none'} has {len(_replies(convs['r1']))}")
        print(f"{cell_id}: will send {todo or 'nothing'}"
              f"{' + the same-conversation R1' if rc._same_conversation_eligible(plan, entry) else ''}")
        if not apply:
            print("DRY RUN -- nothing sent or written")
            return

        transcript: dict = {}
        r2_reply = flow.read_memory_settings()
        transcript["r2_reply"] = r2_reply
        rc._save_screenshot(flow, platform, cell_id, f"{SESSION}_r2_reread")
        if token_found(r2_reply, token):
            r2_score = "TOKEN FOUND (auto)"
        elif (problem := unreadable_memory_page(r2_reply)) == NO_MEMORY_SECTION:
            r2_score = f"N/A ({NO_MEMORY_SECTION})"
        elif problem:
            r2_score = f"REVIEW (auto, r2): memory page not readable ({problem}) -- needs human review"
        else:
            r2_score = "NOT FOUND (auto)"

        r3_replies = _replies(convs["r3"])
        if "r3_followup" in todo:
            flow.open_conversation(adapter["url"].format(convs["r3"]["id"]))
            r3_replies.append(rc._send_fresh(flow, probes["r3_followup"]))
            rc._save_screenshot(flow, platform, cell_id, f"{SESSION}_r3_followup")

        r1_replies = _replies(convs["r1"])
        if "r1_open" in todo:
            flow.new_conversation()
            r1_replies.append(rc._send_fresh(flow, probes["r1_open"]))
            rc._save_screenshot(flow, platform, cell_id, f"{SESSION}_r1_open")
        elif "r1_open_followup" in todo:
            flow.open_conversation(adapter["url"].format(convs["r1"]["id"]))
        if "r1_open_followup" in todo:
            r1_replies.append(rc._send_fresh(flow, probes["r1_open_followup"]))
            rc._save_screenshot(flow, platform, cell_id, f"{SESSION}_r1_open_followup")

        transcript.update({
            "r3_sent": probes["r3"], "r3_reply": r3_replies[0],
            "r3_followup_sent": probes["r3_followup"], "r3_followup_reply": r3_replies[1],
            "r1_open_sent": probes["r1_open"], "r1_open_reply": r1_replies[0],
            "r1_open_followup_sent": probes["r1_open_followup"], "r1_open_followup_reply": r1_replies[1],
        })
        r3_score, r3_detail = score_attempts(r3_replies, token, rc._R3_ATTEMPTS)
        r1_score, r1_detail = score_attempts(r1_replies, token, rc._R1_ATTEMPTS)
        transcript["scoring"] = {"r3": r3_detail, "r1": r1_detail}
        transcript["resumed"] = {
            "at": datetime.now(timezone.utc).isoformat(),
            "sent_at_resume": todo,
            "already_answered_before_interruption": {
                "r3_chat": convs["r3"]["id"], "r3_answers": len(_replies(convs["r3"])),
                "r1_chat": convs["r1"]["id"] if convs["r1"] else None, "r1_answers": len(_replies(convs["r1"])),
            },
            "note": "replies already in the chats were read from the platform's conversation data, not re-sent; "
                    "R2 re-read at resume (original read kept only as 03_recall_new_conversation_r2.png)",
        }
        rc._save_json(platform, cell_id, SESSION, transcript)

        same_conv_label = "N/A (not applicable)"
        if rc._same_conversation_eligible(plan, entry):
            try:
                same_conv_label = rc._run_same_conversation_probe(
                    flow, probes, token, platform, cell_id, entry["injection_ref"], "04_recall_same_conversation")
            except Exception as exc:
                same_conv_label = f"ERROR (same-conversation probe failed: {type(exc).__name__}: {exc})"
                print(f"WARNING {cell_id}: {same_conv_label}")

    rc._finalize_recall(plan, cell_id, {"r1": r1_score, "r2": r2_score, "r3": r3_score},
                        same_conv_label, f"resumed-recall (interrupted between probes; sent at resume: {todo})")


if __name__ == "__main__":
    resume(sys.argv[1], apply="--apply" in sys.argv)
