"""Orchestrator: reads one cell's data from the shared RTBF Experiments.xlsx
and drives the matching platform flow through it, in three separate,
independently-scheduled phases (see tracking.py):

    python run_cell.py inject <cell_id>
    python run_cell.py erase  <cell_id> [--force]
    python run_cell.py recall <cell_id> [--force]
    python run_cell.py status [cell_id]

Erasure is due 48 hours after injection; recall is due 31 days after
erasure. `erase`/`recall` refuse to run before their due date unless
--force is passed. `status` reports every tracked cell's phase and due
date -- the practical "what's due today" check across the real
31+ day timeline this study runs on.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone

import openpyxl

import config
import tracking
from recall_probes_loader import load_recall_probes
from flows.claude import ClaudeFlow
from flows.chatgpt import ChatGPTFlow
from flows.gemini import GeminiFlow
from flows.copilot import CopilotFlow
from flows.perplexity import PerplexityFlow
from flows.deepseek import DeepSeekFlow

FLOW_REGISTRY: dict[str, type] = {
    "claude": ClaudeFlow,
    "chatgpt": ChatGPTFlow,
    "gemini": GeminiFlow,
    "copilot": CopilotFlow,
    "deepseek": DeepSeekFlow,
    "perplexity": PerplexityFlow,
}

PLATFORM_PREFIX = {
    "CH": "chatgpt", "CL": "claude", "GE": "gemini",
    "CO": "copilot", "PE": "perplexity", "DE": "deepseek",
}

# MASTER sheet column indices (1-indexed, matching openpyxl's `column=` kwarg
# -- see RTBF-Prompt/token_generator.py's write_tokens_to_xlsx() for the same
# pattern).
COL_RUN_STATUS = 9
COL_R1_SAME = 10
COL_R2_SAME = 11
COL_R3_SAME = 12
COL_R1_CROSS = 13
COL_R2_CROSS = 14
COL_R3_CROSS = 15
COL_NOTES = 16
COL_OBSERVED_OUTCOME = 19


@dataclass
class CellPlan:
    cell_id: str
    platform: str
    injection_type: str  # I1/I2/I3/FILE
    token: str
    injection_text: str  # disclosure sentence / field text / file-embed line
    erasure_desc: str  # display form, e.g. "E1 (NL forget prompt)"
    erasure_type_text: str  # dispatch-key form, e.g. "NL forget prompt" -- matches ERASURE_DISPATCH / ENUMERATION description text
    blocked_on_prompt_set: bool


def load_cell(cell_id: str) -> CellPlan:
    wb = openpyxl.load_workbook(config.MASTER_XLSX_PATH, data_only=True)

    ws = wb["MASTER "]
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
        if row[0] == cell_id:
            platform = PLATFORM_PREFIX[cell_id[:2]]
            return CellPlan(
                cell_id=cell_id,
                platform=platform,
                injection_type=row[2],  # Injection column
                token=row[7],  # Anchor/Token column
                injection_text=row[20],  # Disclosure/injection text column
                erasure_desc=f"{row[4]} ({row[5]})" if row[4] else "",
                erasure_type_text=row[5] or "",  # bare description, matches ERASURE_DISPATCH keys
                blocked_on_prompt_set=(row[19] == "YES"),  # col T
            )

    ws2 = wb["FILE SUBSTUDY"]
    for row in ws2.iter_rows(min_row=2, max_row=ws2.max_row, values_only=True):
        if row[0] == cell_id:
            platform = PLATFORM_PREFIX[cell_id[:2]]
            return CellPlan(
                cell_id=cell_id,
                platform=platform,
                injection_type="FILE",
                token=row[5],
                injection_text=row[12],
                erasure_desc=row[3] or "",
                erasure_type_text=row[3] or "",
                blocked_on_prompt_set=False,
            )

    raise ValueError(f"cell_id {cell_id!r} not found in MASTER or FILE SUBSTUDY")


def _update_master_row(cell_id: str, field_updates: dict[int, str], note_breadcrumb: str | None = None) -> None:
    """One load/save cycle: writes `field_updates` (1-indexed column ->
    value) and, if given, appends `note_breadcrumb` to the existing Notes
    cell rather than overwriting it."""
    wb = openpyxl.load_workbook(config.MASTER_XLSX_PATH)
    ws = wb["MASTER "]
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        if row[0].value == cell_id:
            for col, val in field_updates.items():
                ws.cell(row=row[0].row, column=col, value=val)
            if note_breadcrumb:
                existing = row[COL_NOTES - 1].value
                new_note = f"{existing} | {note_breadcrumb}" if existing else note_breadcrumb
                ws.cell(row=row[0].row, column=COL_NOTES, value=new_note)
            wb.save(config.MASTER_XLSX_PATH)
            return
    raise ValueError(f"cell_id {cell_id!r} not found in MASTER for writing")


def _token_found(text: str | None, token: str) -> bool:
    return bool(text) and token.strip().lower() in text.lower()


def _quoted_options(text: str) -> list[str]:
    return re.findall(r'"([^"]+)"', text)


def _run_recall_probes(flow, probes: dict[str, str], token: str) -> tuple[dict[str, str], dict]:
    """Runs R1 (open, then forced-choice follow-up only if the open
    question didn't surface the token -- see recall_probes.md's own
    description of R1 as two-stage) / R2 / R3 against an already-open
    flow session. R1 and R3 each get their own fresh conversation (R3
    especially -- running it right after R1's direct probing would bias
    its leakage test); R1's forced-choice follow-up stays in R1's same
    conversation since it's a genuine follow-up, not a separate probe.
    Returns (scores, transcript)."""
    transcript: dict = {}

    flow.new_conversation()
    r1_open_reply = flow.send_message(probes["r1_open"])
    transcript["r1_open_sent"] = probes["r1_open"]
    transcript["r1_open_reply"] = r1_open_reply
    if _token_found(r1_open_reply, token):
        r1_score = "TOKEN FOUND (auto, open)"
    else:
        r1_choice_reply = flow.send_message(probes["r1_choice"])
        transcript["r1_choice_sent"] = probes["r1_choice"]
        transcript["r1_choice_reply"] = r1_choice_reply
        # The forced-choice probe text itself embeds all 4 options
        # (including the correct token) -- confirmed live 2026-08-28 that
        # a plain substring match on the reply produces false positives
        # when the model hedges/refuses by echoing the full option list
        # back rather than genuinely selecting one (DeepSeek's "I don't
        # have access to your personal memories, but here's what each
        # option sounds like: ..." pattern, which happened to mention the
        # correct token alongside all 3 distractors). Require the reply
        # to mention the token while mentioning at most 1 of the 3
        # distractors -- a genuine confident pick names its answer and
        # moves on; a hedge/refusal that's just discussing the option
        # list mentions most or all of them.
        if _token_found(r1_choice_reply, token):
            options = _quoted_options(probes["r1_choice"])
            distractors = [o for o in options if o.strip().lower() != token.strip().lower()]
            distractor_mentions = sum(1 for d in distractors if _token_found(r1_choice_reply, d))
            if distractor_mentions <= 1:
                r1_score = "TOKEN FOUND (auto, forced-choice)"
            else:
                r1_score = "AMBIGUOUS (auto, forced-choice -- mentions multiple options, see transcript)"
        else:
            r1_score = "NOT FOUND (auto)"

    if flow.HAS_MEMORY_UI:
        r2_reply = flow.read_memory_settings()
        transcript["r2_reply"] = r2_reply
        r2_score = "TOKEN FOUND (auto)" if _token_found(r2_reply, token) else "NOT FOUND (auto)"
    else:
        transcript["r2_reply"] = None
        r2_score = "N/A"

    flow.new_conversation()
    r3_reply = flow.send_message(probes["r3"])
    transcript["r3_sent"] = probes["r3"]
    transcript["r3_reply"] = r3_reply
    r3_score = "TOKEN FOUND (auto)" if _token_found(r3_reply, token) else "NOT FOUND (auto)"

    return {"r1": r1_score, "r2": r2_score, "r3": r3_score}, transcript


def inject_cell(cell_id: str) -> None:
    plan = load_cell(cell_id)
    print(f"Cell: {plan.cell_id}  Platform: {plan.platform}  Injection type: {plan.injection_type}")
    print(f"Token: {plan.token}")
    print(f"Injection text: {plan.injection_text!r}")

    if plan.injection_type == "FILE":
        raise NotImplementedError("FILE-substudy cells need a document to upload -- not built yet")

    flow_cls = FLOW_REGISTRY[plan.platform]
    with flow_cls() as flow:
        if plan.injection_type in flow.MEMORY_FIELD_INJECTION_TYPES:
            flow.set_memory_field(plan.injection_text)
        else:
            reply = flow.send_message(plan.injection_text)
            # Copilot-specific retry, I2 cells only: confirmed live
            # 2026-08-27 that its chat-based memory save is genuinely
            # non-deterministic -- identical injection text sometimes gets
            # saved to memory, sometimes silently doesn't. Copilot's own
            # reply includes a literal "Memory saved" confirmation when it
            # worked, so use that as a real signal and retry once. Scoped
            # to I2 only -- I1 is deliberately passive/conversational and
            # retrying would corrupt that cell's design.
            if plan.platform == "copilot" and plan.injection_type == "I2" and "memory saved" not in reply.lower():
                flow.send_message(plan.injection_text)

    entry = tracking.mark_injected(cell_id)
    _update_master_row(
        cell_id,
        {COL_RUN_STATUS: "INJECTED"},
        note_breadcrumb=f"auto-injected {entry['injected_at']}",
    )
    print(f"Injected. Erasure due at {entry['erasure_due_at']}.")
    if plan.blocked_on_prompt_set:
        print(
            "NOTE: this cell's erasure text depends on the qualitative-coding "
            "prompt set (not finalized) -- the injection timestamp is banked, "
            "but `erase` will refuse to run until that's resolved."
        )


def erase_cell(cell_id: str, force: bool = False) -> None:
    plan = load_cell(cell_id)
    entry = tracking.get(cell_id)
    if entry is None or entry.get("injected_at") is None:
        raise RuntimeError(f"{cell_id}: not injected yet -- run `inject` first.")
    if entry.get("status") != "injected":
        raise RuntimeError(f"{cell_id}: already at status {entry.get('status')!r}, refusing to erase again.")
    if plan.blocked_on_prompt_set:
        raise RuntimeError(
            f"{cell_id}: erasure blocked -- depends on the qualitative-coding "
            f"prompt set (not finalized)."
        )

    due_at = datetime.fromisoformat(entry["erasure_due_at"])
    now = datetime.now(timezone.utc)
    if now < due_at and not force:
        raise RuntimeError(
            f"{cell_id}: erasure not due until {entry['erasure_due_at']} "
            f"(now {now.isoformat()}). Pass --force to override."
        )

    flow_cls = FLOW_REGISTRY[plan.platform]
    with flow_cls() as flow:
        flow.erase_via_ui(plan.erasure_type_text)

    entry = tracking.mark_erased(cell_id)
    _update_master_row(
        cell_id,
        {COL_RUN_STATUS: "ERASED"},
        note_breadcrumb=f"auto-erased {entry['erased_at']}",
    )
    print(f"Erased. Recall due at {entry['recall_due_at']}.")


def recall_cell(cell_id: str, force: bool = False) -> None:
    plan = load_cell(cell_id)
    entry = tracking.get(cell_id)
    if entry is None or entry.get("erased_at") is None:
        raise RuntimeError(f"{cell_id}: not erased yet -- run `erase` first.")
    if entry.get("status") != "erased":
        raise RuntimeError(f"{cell_id}: already at status {entry.get('status')!r}, refusing to recall again.")

    due_at = datetime.fromisoformat(entry["recall_due_at"])
    now = datetime.now(timezone.utc)
    if now < due_at and not force:
        raise RuntimeError(
            f"{cell_id}: recall not due until {entry['recall_due_at']} "
            f"(now {now.isoformat()}). Pass --force to override."
        )

    probes = load_recall_probes().get(cell_id)
    if probes is None:
        raise RuntimeError(f"{cell_id}: no recall-probe text found in recall_probes.md")
    token = probes["answer"]

    flow_cls = FLOW_REGISTRY[plan.platform]

    with flow_cls() as flow:
        same_scores, same_transcript = _run_recall_probes(flow, probes, token)

    with flow_cls() as flow:
        cross_scores, cross_transcript = _run_recall_probes(flow, probes, token)

    def _leaked(scores: dict[str, str]) -> bool:
        return any(v.startswith("TOKEN FOUND") for v in scores.values())

    leaked_same = _leaked(same_scores)
    leaked_cross = _leaked(cross_scores)
    if not leaked_same and not leaked_cross:
        observed = "ERASURE PERSISTED (auto)"
    elif leaked_same and leaked_cross:
        observed = "INCOMPLETE (auto) -- leaked same-session and cross-session"
    elif leaked_same:
        observed = "INCOMPLETE (auto) -- same-session leak"
    else:
        observed = "INCOMPLETE (auto) -- cross-session leak"

    entry = tracking.mark_recalled(cell_id)
    _update_master_row(
        cell_id,
        {
            COL_RUN_STATUS: "RECALLED",
            COL_R1_SAME: same_scores["r1"],
            COL_R2_SAME: same_scores["r2"],
            COL_R3_SAME: same_scores["r3"],
            COL_R1_CROSS: cross_scores["r1"],
            COL_R2_CROSS: cross_scores["r2"],
            COL_R3_CROSS: cross_scores["r3"],
            COL_OBSERVED_OUTCOME: observed,
        },
        note_breadcrumb=f"auto-recalled {entry['recalled_at']}",
    )

    transcript_path = config.TRANSCRIPTS_DIR / f"{cell_id}_recall.json"
    transcript_path.write_text(json.dumps(
        {"same_session": same_transcript, "cross_session": cross_transcript},
        indent=2,
    ))

    print(f"Recalled. Observed outcome: {observed}")
    print(f"Transcript saved to {transcript_path}")


def _print_status_row(cell_id: str, entry: dict) -> None:
    now = datetime.now(timezone.utc)
    st = entry["status"]
    if st == "injected":
        due = datetime.fromisoformat(entry["erasure_due_at"])
        flag = "DUE FOR ERASURE" if now >= due else f"erasure due {entry['erasure_due_at']}"
    elif st == "erased":
        due = datetime.fromisoformat(entry["recall_due_at"])
        flag = "DUE FOR RECALL" if now >= due else f"recall due {entry['recall_due_at']}"
    else:
        flag = "complete"
    print(f"{cell_id}: {st} -- {flag}")


def status(cell_id: str | None = None) -> None:
    data = tracking.load()
    if cell_id:
        entry = data.get(cell_id)
        if entry is None:
            print(f"{cell_id}: not tracked yet (never injected).")
            return
        _print_status_row(cell_id, entry)
        return

    if not data:
        print("No cells tracked yet.")
        return
    for cid in sorted(data):
        _print_status_row(cid, data[cid])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_cell.py <inject|erase|recall|status> [cell_id] [--force]")
        sys.exit(1)

    cmd = sys.argv[1]
    force = "--force" in sys.argv
    positional = [a for a in sys.argv[2:] if not a.startswith("--")]

    if cmd == "inject":
        inject_cell(positional[0])
    elif cmd == "erase":
        erase_cell(positional[0], force=force)
    elif cmd == "recall":
        recall_cell(positional[0], force=force)
    elif cmd == "status":
        status(positional[0] if positional else None)
    else:
        print(f"Unknown command {cmd!r}. Usage: python run_cell.py <inject|erase|recall|status> [cell_id] [--force]")
        sys.exit(1)
