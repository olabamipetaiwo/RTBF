"""Orchestrator: reads one cell's data from the shared RTBF Experiments.xlsx
and drives the matching platform flow through it.

Right now the xlsx-reading half is fully functional (no platform-specific
knowledge needed). The execution half is gated behind an actual PlatformFlow
subclass existing for that platform -- none do yet (selectors need real
investigation against each live, logged-in site). Until then this runs in
dry-run mode: it prints exactly what would be sent/clicked, without a flow
class attempting to guess at real page elements.

Usage:
    python run_cell.py CH-I1-E1
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

import openpyxl

import config
from flows.claude import ClaudeFlow
from flows.chatgpt import ChatGPTFlow
from flows.gemini import GeminiFlow
from flows.copilot import CopilotFlow
from flows.perplexity import PerplexityFlow
from flows.deepseek import DeepSeekFlow

# Populate as real per-platform flow classes are built (see flows/base.py).
# Registered platforms still raise NotImplementedError once they reach a
# method that needs real selectors -- registering here just turns off the
# dry-run print and lets execution actually start.
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


def run(cell_id: str) -> None:
    plan = load_cell(cell_id)
    print(f"Cell: {plan.cell_id}  Platform: {plan.platform}  Injection type: {plan.injection_type}")
    print(f"Token: {plan.token}")
    print(f"Injection text: {plan.injection_text!r}")
    print(f"Erasure (from sheet): {plan.erasure_desc}")
    if plan.blocked_on_prompt_set:
        print("BLOCKED: this cell's erasure step depends on the qualitative-coding prompt set (not finalized).")
        return

    flow_cls = FLOW_REGISTRY.get(plan.platform)
    if flow_cls is None:
        print(f"\n[DRY RUN] No PlatformFlow implemented yet for {plan.platform!r} -- would:")
        print(f"  1. Load session for {plan.platform}")
        print(f"  2. Inject ({plan.injection_type}): {plan.injection_text!r}")
        print(f"  3. Verify injection landed")
        print(f"  4. Erase: {plan.erasure_desc}")
        print(f"  5. Run R1/R2/R3 probes, same-session and cross-session")
        return

    with flow_cls() as flow:
        if plan.injection_type == "FILE":
            raise NotImplementedError("FILE-substudy cells need a document to upload -- not built yet")
        elif plan.injection_type in flow.MEMORY_FIELD_INJECTION_TYPES:
            flow.set_memory_field(plan.injection_text)
        else:
            reply = flow.send_message(plan.injection_text)
            # Copilot-specific retry, I2 cells only: confirmed live
            # 2026-08-27 that its chat-based memory save is genuinely
            # non-deterministic -- identical injection text sometimes gets
            # saved to memory, sometimes silently doesn't (verified both
            # outcomes against the SAME token/text across separate runs,
            # not a selector or timing artifact). Copilot's own reply
            # includes a literal "Memory saved" confirmation when it
            # worked, so use that as a real signal and retry once rather
            # than proceeding blind into an erasure step that would find
            # nothing to act on. Scoped to I2 only -- I1 is a deliberately
            # passive/conversational disclosure that's methodologically
            # NOT supposed to reliably trigger a save (it's testing
            # whether the platform infers memory-worthiness on its own);
            # retrying on I1 would turn it into a repeated, more I2-like
            # signal and corrupt that cell's design.
            if plan.platform == "copilot" and plan.injection_type == "I2" and "memory saved" not in reply.lower():
                flow.send_message(plan.injection_text)
        # TODO once a real flow exists: verify injection landed for every
        # platform, not just this one Copilot-specific signal, then:
        flow.erase_via_ui(plan.erasure_type_text)
        # TODO: R1/R2/R3 probes, same-session and cross-session


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_cell.py <cell_id>")
        sys.exit(1)
    run(sys.argv[1])
