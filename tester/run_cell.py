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
from pathlib import Path

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

# FILE SUBSTUDY sheet column indices (1-indexed) -- a different layout
# than MASTER: no R1-R3 same/cross-session columns (Q16's verification
# is a one-time post-upload check, not a same/cross split), instead
# "Extraction observed at" (written at injection time) and
# "Results / notes" + "Observed outcome (coded)" (written at recall time).
FS_COL_RUN_STATUS = 9
FS_COL_EXTRACTION_OBSERVED_AT = 10
FS_COL_RESULTS_NOTES = 11
FS_COL_OBSERVED_OUTCOME = 12


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


def _update_file_substudy_row(cell_id: str, field_updates: dict[int, str]) -> None:
    """FILE SUBSTUDY's counterpart to _update_master_row() -- a separate
    sheet with a different column layout, so a separate small writer
    rather than trying to force one function to handle both shapes."""
    wb = openpyxl.load_workbook(config.MASTER_XLSX_PATH)
    ws = wb["FILE SUBSTUDY"]
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        if row[0].value == cell_id:
            for col, val in field_updates.items():
                ws.cell(row=row[0].row, column=col, value=val)
            wb.save(config.MASTER_XLSX_PATH)
            return
    raise ValueError(f"cell_id {cell_id!r} not found in FILE SUBSTUDY for writing")


def _cell_dir(platform: str, cell_id: str) -> tuple[Path, Path]:
    """Per-cell evidence folders: tester/transcripts/<platform>/<cell_id>/
    json/ and .../screenshots/ -- separate subfolders so a reviewer never
    has images and transcripts mixed together, organized per platform so
    each platform's evidence can be handed over independently."""
    base = config.TRANSCRIPTS_DIR / platform / cell_id
    json_dir, shots_dir = base / "json", base / "screenshots"
    json_dir.mkdir(parents=True, exist_ok=True)
    shots_dir.mkdir(parents=True, exist_ok=True)
    return json_dir, shots_dir


def _save_json(platform: str, cell_id: str, name: str, data) -> None:
    json_dir, _ = _cell_dir(platform, cell_id)
    (json_dir / f"{name}.json").write_text(json.dumps(data, indent=2))


def _save_screenshot(flow, platform: str, cell_id: str, name: str) -> None:
    _, shots_dir = _cell_dir(platform, cell_id)
    flow.page.screenshot(path=str(shots_dir / f"{name}.png"), full_page=True)


def _token_found(text: str | None, token: str) -> bool:
    return bool(text) and token.strip().lower() in text.lower()


def _quoted_options(text: str) -> list[str]:
    return re.findall(r'"([^"]+)"', text)


def _run_recall_probes(
    flow, probes: dict[str, str], token: str, platform: str, cell_id: str, session_label: str
) -> dict[str, str]:
    """Runs R1 (open, then forced-choice follow-up only if the open
    question didn't surface the token -- see recall_probes.md's own
    description of R1 as two-stage) / R2 / R3 against an already-open
    flow session. R1 and R3 each get their own fresh conversation (R3
    especially -- running it right after R1's direct probing would bias
    its leakage test); R1's forced-choice follow-up stays in R1's same
    conversation since it's a genuine follow-up, not a separate probe.
    `session_label` is "03_recall_same_session" or
    "04_recall_cross_session" -- used to name this sub-phase's saved
    transcript and per-probe screenshots. Returns just the scores; the
    transcript is saved directly rather than returned, since this is now
    the only place that needs it."""
    transcript: dict = {}

    flow.new_conversation()
    r1_open_reply = flow.send_message(probes["r1_open"])
    transcript["r1_open_sent"] = probes["r1_open"]
    transcript["r1_open_reply"] = r1_open_reply
    _save_screenshot(flow, platform, cell_id, f"{session_label}_r1_open")
    if _token_found(r1_open_reply, token):
        r1_score = "TOKEN FOUND (auto, open)"
    else:
        r1_choice_reply = flow.send_message(probes["r1_choice"])
        transcript["r1_choice_sent"] = probes["r1_choice"]
        transcript["r1_choice_reply"] = r1_choice_reply
        _save_screenshot(flow, platform, cell_id, f"{session_label}_r1_choice")
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
        _save_screenshot(flow, platform, cell_id, f"{session_label}_r2")
    else:
        transcript["r2_reply"] = None
        r2_score = "N/A"

    flow.new_conversation()
    r3_reply = flow.send_message(probes["r3"])
    transcript["r3_sent"] = probes["r3"]
    transcript["r3_reply"] = r3_reply
    r3_score = "TOKEN FOUND (auto)" if _token_found(r3_reply, token) else "NOT FOUND (auto)"
    _save_screenshot(flow, platform, cell_id, f"{session_label}_r3")

    _save_json(platform, cell_id, session_label, transcript)
    return {"r1": r1_score, "r2": r2_score, "r3": r3_score}


def _verify_file_injection(flow, upload_reply: str, token: str) -> tuple[str, dict]:
    """DECISIONS Q16 (revised): distinguishes in-conversation extraction
    from persistent-memory extraction as two separate passive checks,
    falling back to an explicit forced-read request only if neither
    finds the token. Confirmed live 2026-08-28 (Claude): sending the
    upload with no caption already produces a reply that spontaneously
    summarizes the document -- that reply itself IS the in-conversation
    passive check, no separate follow-up question needed. Returns
    (condition_label, transcript), where condition_label is one of:
    "extracted into conversation only" / "extracted into memory only" /
    "extracted into both" / "extracted only after forced read" /
    "never extracted"."""
    transcript: dict = {"upload_reply": upload_reply}
    conv_found = _token_found(upload_reply, token)

    if flow.HAS_MEMORY_UI:
        mem_reply = flow.read_memory_settings()
        transcript["memory_settings_reply"] = mem_reply
        mem_found = _token_found(mem_reply, token)
    else:
        transcript["memory_settings_reply"] = None
        mem_found = False

    if conv_found and mem_found:
        return "extracted into both", transcript
    if conv_found:
        return "extracted into conversation only", transcript
    if mem_found:
        return "extracted into memory only", transcript

    forced_reply = flow.send_message("Can you summarize the document I just shared?")
    transcript["forced_read_reply"] = forced_reply
    forced_conv_found = _token_found(forced_reply, token)

    forced_mem_found = False
    if flow.HAS_MEMORY_UI:
        mem_reply_after = flow.read_memory_settings()
        transcript["memory_settings_reply_after_forced"] = mem_reply_after
        forced_mem_found = _token_found(mem_reply_after, token)

    if forced_conv_found or forced_mem_found:
        return "extracted only after forced read", transcript
    return "never extracted", transcript


def inject_cell(cell_id: str) -> None:
    plan = load_cell(cell_id)
    print(f"Cell: {plan.cell_id}  Platform: {plan.platform}  Injection type: {plan.injection_type}")
    print(f"Token: {plan.token}")
    print(f"Injection text: {plan.injection_text!r}")

    flow_cls = FLOW_REGISTRY[plan.platform]

    if plan.injection_type == "FILE":
        pdf_path = config.TESTER_ROOT / "data" / "file_substudy_pdfs" / f"{cell_id}.pdf"
        if not pdf_path.exists():
            raise RuntimeError(
                f"{cell_id}: no PDF found at {pdf_path} -- run "
                f"generate_file_substudy_pdfs.py first"
            )
        with flow_cls() as flow:
            upload_reply = flow.upload_file(str(pdf_path))
            condition, verify_transcript = _verify_file_injection(flow, upload_reply, plan.token)
            _save_json(plan.platform, cell_id, "01_inject", verify_transcript)
            _save_screenshot(flow, plan.platform, cell_id, "01_inject")

        entry = tracking.mark_injected(cell_id)
        _update_file_substudy_row(
            cell_id,
            {FS_COL_RUN_STATUS: "INJECTED", FS_COL_EXTRACTION_OBSERVED_AT: condition},
        )
        print(f"Injected (file upload). Extraction observed: {condition}.")
        print(f"Erasure due at {entry['erasure_due_at']}.")
        return

    with flow_cls() as flow:
        if plan.injection_type in flow.MEMORY_FIELD_INJECTION_TYPES:
            flow.set_memory_field(plan.injection_text)
            inject_transcript = {"sent": plan.injection_text}
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
                reply = flow.send_message(plan.injection_text)
            inject_transcript = {"sent": plan.injection_text, "reply": reply}
        _save_json(plan.platform, cell_id, "01_inject", inject_transcript)
        _save_screenshot(flow, plan.platform, cell_id, "01_inject")

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
        _save_json(plan.platform, cell_id, "02_erase", {"erasure_type_text": plan.erasure_type_text})
        _save_screenshot(flow, plan.platform, cell_id, "02_erase")

    entry = tracking.mark_erased(cell_id)
    if plan.injection_type == "FILE":
        _update_file_substudy_row(cell_id, {FS_COL_RUN_STATUS: "ERASED"})
    else:
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
        same_scores = _run_recall_probes(
            flow, probes, token, plan.platform, cell_id, "03_recall_same_session"
        )

    with flow_cls() as flow:
        cross_scores = _run_recall_probes(
            flow, probes, token, plan.platform, cell_id, "04_recall_cross_session"
        )

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
    if plan.injection_type == "FILE":
        results_summary = (
            f"same-session: R1={same_scores['r1']}, R2={same_scores['r2']}, "
            f"R3={same_scores['r3']} | cross-session: R1={cross_scores['r1']}, "
            f"R2={cross_scores['r2']}, R3={cross_scores['r3']}"
        )
        _update_file_substudy_row(
            cell_id,
            {
                FS_COL_RUN_STATUS: "RECALLED",
                FS_COL_RESULTS_NOTES: results_summary,
                FS_COL_OBSERVED_OUTCOME: observed,
            },
        )
    else:
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

    print(f"Recalled. Observed outcome: {observed}")
    print(f"Transcripts/screenshots saved under "
          f"{config.TRANSCRIPTS_DIR / plan.platform / cell_id}")


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
