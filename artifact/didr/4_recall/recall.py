"""Stage 4: recall checks, at least 30 days after deletion.

Order: UI-based check, indirect prompt (twice), direct prompt (twice), each
prompt pair in its own new conversation; for deletion-request prompts, one
more direct prompt in the original conversation, reported separately.
"""

from __future__ import annotations

from didr import methods, tracking, workbook
from didr.recall_scoring import NO_MEMORY_SECTION, score_attempts, token_found, unreadable_memory_page
from didr.runner import evidence_dirs, open_flow, save_json, save_screenshot, send_fresh


def recall(test_case_id: str, force: bool = False) -> None:
    tc = workbook.get(test_case_id)
    entry = tracking.require(tc.id, "deleted", "recall_due_at", force)
    value = tc["Value"]

    with open_flow(tc.agent, tc.account) as flow:
        ui_result, ui_page = _ui_check(flow, tc.agent, tc.id, value)
        indirect = _ask_twice(flow, tc, "Indirect recall prompt", "Indirect recall follow-up", "indirect")
        direct = _ask_twice(flow, tc, "Direct recall prompt", "Direct recall follow-up", "direct")
        indirect_result, indirect_detail = score_attempts([r for _, r in indirect], value, ("indirect-1", "indirect-2"))
        direct_result, direct_detail = score_attempts([r for _, r in direct], value, ("direct-1", "direct-2"))
        save_json(tc.agent, tc.id, "03_recall", {
            "ui_page": ui_page,
            "indirect": [{"sent": s, "reply": r} for s, r in indirect],
            "direct": [{"sent": s, "reply": r} for s, r in direct],
            "scoring": {"ui": ui_result, "indirect": indirect_detail, "direct": direct_detail},
        })
        same_result = _same_conversation(flow, tc, entry.get("injection_ref"))

    entry = tracking.mark_recalled(tc.id)
    workbook.update_one(tc.id, {
        "Status": "recalled",
        "Recalled at": entry["recalled_at"],
        "UI-based check result": ui_result,
        "Indirect recall result": indirect_result,
        "Direct recall result": direct_result,
        "Same-conversation result": same_result,
    })
    print(f"{tc.id}: UI {ui_result} | indirect {indirect_result} | direct {direct_result} | same conversation {same_result}")


def _ui_check(flow, agent: str, test_case_id: str, value: str) -> tuple[str, str | None]:
    if not flow.HAS_MEMORY_UI:
        return "N/A (no memory interface)", None
    flow.memory_shot_path = evidence_dirs(agent, test_case_id)[1] / "03_recall_ui_panel.png"
    page = flow.read_memory_settings()
    flow.memory_shot_path = None
    save_screenshot(flow, agent, test_case_id, "03_recall_ui")
    if token_found(page, value):
        return "TOKEN FOUND (auto)", page
    problem = unreadable_memory_page(page)
    if problem == NO_MEMORY_SECTION:
        return f"N/A ({problem})", page
    if problem:
        return f"REVIEW (auto): memory page not readable ({problem})", page
    return "NOT FOUND (auto)", page


def _ask_twice(flow, tc, first: str, second: str, name: str) -> list[tuple[str, str]]:
    flow.new_conversation()
    exchanges = []
    for i, column in enumerate((first, second), start=1):
        reply = send_fresh(flow, tc[column])
        save_screenshot(flow, tc.agent, tc.id, f"03_recall_{name}_{i}")
        exchanges.append((tc[column], reply))
    return exchanges


def _same_conversation(flow, tc, ref: str | None) -> str:
    if tc["Deletion method"] not in methods.PROMPT_DELETION_METHODS or not ref:
        return "N/A"
    try:
        flow.open_conversation(ref)
        reply = send_fresh(flow, tc["Direct recall prompt"])
        save_screenshot(flow, tc.agent, tc.id, "04_recall_same_conversation")
        result, detail = score_attempts([reply], tc["Value"], ("same-conversation",), cue_check=False)
        save_json(tc.agent, tc.id, "04_recall_same_conversation", {"ref": ref, "reply": reply, "scoring": detail})
        return result
    except Exception as exc:  # the main result is already saved; keep it
        return f"ERROR ({type(exc).__name__}: {exc})"
