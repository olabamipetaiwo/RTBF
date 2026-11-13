"""Stage 3: apply the deletion method, at least 48 hours after injection."""

from __future__ import annotations

from didr import methods, tracking, workbook
from didr.runner import open_flow, record_exchanges, save_json, save_screenshot


def delete(test_case_id: str, force: bool = False, manual: bool = False) -> None:
    tc = workbook.get(test_case_id)
    entry = tracking.require(tc.id, "injected", "deletion_due_at", force)
    method = tc["Deletion method"]
    key = methods.dispatch_key(method, tc.agent)
    request_text = tc["Deletion request text"]
    if method in methods.PROMPT_DELETION_METHODS and not request_text:
        raise RuntimeError(f"{tc.id}: no deletion request text")

    if manual:
        save_json(tc.agent, tc.id, "02_delete", {"method": method, "performed": "by hand"})
        response = "(performed by hand)"
    else:
        if (tc.agent, method) in methods.MANUAL_STEPS:
            raise RuntimeError(f"{tc.id}: {method!r} on {tc.agent} must be done by hand; then use --manual")
        with open_flow(tc.agent, tc.account) as flow:
            exchanges = record_exchanges(flow)
            flow.erase_via_ui(
                key,
                token=tc["Value"],
                injection_text=tc["Disclosure sentence"],
                ref=entry.get("injection_ref"),
                erasure_request_text=request_text,
            )
            save_json(tc.agent, tc.id, "02_delete", {"method": method, "exchanges": exchanges})
            save_screenshot(flow, tc.agent, tc.id, "02_delete")
        response = "\n\n".join(e["reply"] for e in exchanges if e.get("reply")) or None

    entry = tracking.mark_deleted(tc.id)
    workbook.update_one(tc.id, {"Status": "deleted", "Deleted at": entry["deleted_at"], "Agent response": response})
    print(f"{tc.id}: deleted; recall due {entry['recall_due_at']}")
