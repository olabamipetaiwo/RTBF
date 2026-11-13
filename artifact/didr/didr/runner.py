"""Browser sessions and evidence (transcripts, screenshots) for the live stages."""

from __future__ import annotations

import json
from pathlib import Path

from didr import config
from flows.chatgpt import ChatGPTFlow
from flows.claude import ClaudeFlow
from flows.copilot import CopilotFlow
from flows.deepseek import DeepSeekFlow
from flows.gemini import GeminiFlow
from flows.perplexity import PerplexityFlow

FLOWS: dict[str, type] = {
    "chatgpt": ChatGPTFlow,
    "claude": ClaudeFlow,
    "gemini": GeminiFlow,
    "copilot": CopilotFlow,
    "perplexity": PerplexityFlow,
    "deepseek": DeepSeekFlow,
}


class FlowNotStarted(RuntimeError):
    pass


def open_flow(agent: str, account: str | None):
    try:
        return FLOWS[agent](session_label=account)
    except FileNotFoundError as exc:
        raise FlowNotStarted(str(exc)) from exc


def evidence_dirs(agent: str, test_case_id: str) -> tuple[Path, Path]:
    base = config.RESULTS_DIR / agent / test_case_id
    json_dir, shots_dir = base / "json", base / "screenshots"
    json_dir.mkdir(parents=True, exist_ok=True)
    shots_dir.mkdir(parents=True, exist_ok=True)
    return json_dir, shots_dir


def save_json(agent: str, test_case_id: str, name: str, data) -> None:
    json_dir, _ = evidence_dirs(agent, test_case_id)
    (json_dir / f"{name}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))


def save_screenshot(flow, agent: str, test_case_id: str, name: str) -> None:
    """Scrolls inner chat panels to the bottom first so the latest reply is captured."""
    _, shots_dir = evidence_dirs(agent, test_case_id)
    flow.page.evaluate("""() => {
        for (const el of document.querySelectorAll('*')) {
            if (el.scrollHeight > el.clientHeight + 20 &&
                ['auto', 'scroll'].includes(getComputedStyle(el).overflowY)) {
                el.scrollTop = el.scrollHeight;
            }
        }
        window.scrollTo(0, document.body.scrollHeight);
    }""")
    flow.page.wait_for_timeout(800)
    flow.page.screenshot(path=str(shots_dir / f"{name}.png"), full_page=True)


def record_exchanges(flow) -> list[dict]:
    exchanges: list[dict] = []
    send_message = flow.send_message

    def recording_send_message(text, *args, **kwargs):
        reply = send_message(text, *args, **kwargs)
        exchanges.append({"sent": text, "reply": reply})
        return reply

    flow.send_message = recording_send_message
    return exchanges


def send_fresh(flow, text: str) -> str:
    """Send, and fail if the reply is just the previous message read again."""
    last_reply = getattr(flow, "_last_reply_text", None)
    reply_count = getattr(flow, "_reply_count", None)
    before = last_reply() if last_reply else None
    before_count = reply_count() if reply_count else None
    reply = flow.send_message(text)
    if before and reply and reply.strip() == before.strip():
        if before_count is None or reply_count() <= before_count:
            raise RuntimeError(f"stale read: reply to {text!r} is identical to the reply already on the page")
    return reply
