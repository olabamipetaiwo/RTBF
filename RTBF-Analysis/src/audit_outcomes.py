"""
Derived audit outcomes: recoverability and policy consistency, per cell.

The paper (Methods, "Outcome recording and repetition" and Table
tab:consistency-rule) records four measurements per cell. Two are coded by
hand into the workbook (acknowledgment, interface change). Recoverability and
policy consistency are NOT stored: they are derived here, at analysis time,
from the recall columns, the retention value coded at injection and the
commitment type, so there is one place that defines them.

Final recall design (2026-10-01, see RTBF-Prompt/notes/recall_probe_standardization.md):
one new-conversation recall per cell (R1, R2, R3) decides recoverability. The
single same-conversation R1 request for typed erasures is reported separately
and never enters either derivation.

Recoverability (new-conversation probes only):
  RECOVERED       any probe found the token (after human review where it was
                  held for review). A find counts whatever layer the injection
                  reached.
  PENDING REVIEW  nothing found, but a probe is still awaiting or stuck in
                  human review (unresolved, UNCLEAR).
  NOT RECOVERED   nothing found and at least one probe's miss counts as
                  evidence of absence (see miss_counts).
  INDETERMINATE   nothing found and no miss counts, so a missing token is never
                  read as evidence of deletion.
  NOT RECALLED    recall has not been recorded for the cell.

A miss counts as evidence of absence only for a layer the injection reached.
R1 and R3 (fresh-chat questions): only when the platform showed or claimed a
save at injection (retention "shown" or "claimed"). R2 (the memory/settings
page): also when the injection itself targeted that layer (I2 explicit
"remember", I3 direct entry) unless the platform said it could not store it
("denied").

Policy consistency (Table tab:consistency-rule), computed only after recall:
  DELETES          CONTRADICTED if recovered or interface UNCHANGED; CONSISTENT
                   if NOT RECOVERED and interface not UNCHANGED (changed or not
                   observable); otherwise INDETERMINATE.
  DOES NOT DELETE  never contradicted; CONSISTENT if recovered, else INDETERMINATE.
  NO COMMITMENT, UNRELATED, NOT TESTABLE: never contradicted, never consistent
                   (INDETERMINATE): reported descriptively.

Interface change for a typed request (NL forget prompt/command) is NOT
OBSERVABLE by definition: a request typed into the chat leaves nothing on the
interface to inspect. FILE cells use a separate verification taxonomy and are
skipped.

Documentation (inputs, rules, prerequisites for a real run, caveats): docs/audit_outcomes.md

Run from RTBF-Analysis/:  python -m src.audit_outcomes
Reads (read-only): the master workbook and tester/data/retention_coding.csv.
Writes outputs/results/audit_outcomes.md and outputs/tables/audit_outcomes.csv.
"""

from __future__ import annotations

import csv
import warnings
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import openpyxl

from src.reporting import save_report

# Paths are relative to RTBF-Analysis/, like the other src modules.
WORKBOOK = Path("../RTBF-Prompt/data/RTBF Experiments.xlsx")
RETENTION_CSV = Path("../tester/data/retention_coding.csv")
OUT_TABLE = Path("outputs/tables/audit_outcomes.csv")

# Per-probe statuses.
FOUND, NOT_FOUND, PENDING, NA, NOT_RECALLED = "FOUND", "NOT FOUND", "PENDING", "N/A", "NOT RECALLED"
# Recoverability values.
RECOVERED, NOT_RECOVERED, INDETERMINATE = "RECOVERED", "NOT RECOVERED", "INDETERMINATE"
PENDING_REVIEW, FILE_TAXONOMY = "PENDING REVIEW", "FILE (classified separately)"
# Policy consistency values.
CONTRADICTED, CONSISTENT = "CONTRADICTED", "CONSISTENT"
# Commitment types and interface-change values, as in the workbook dropdowns.
DELETES, DOES_NOT_DELETE = "DELETES", "DOES NOT DELETE"
CHANGED, UNCHANGED, NOT_OBSERVABLE = "CHANGED", "UNCHANGED", "NOT OBSERVABLE"

RETAINED = ("shown", "claimed")  # the only values that establish the platform kept the fact
TYPED_ERASURES = ("NL forget prompt", "NL forget command")
PROBES = ("r1", "r2", "r3")

# Erasures whose own documentation says past conversations remain (paper, Methods; widened to
# every such deletion 2026-10-27, user decision). A recovery that can only have come from those
# conversations is consistent with the documentation. Value: whether the memory summary (R2) must
# not hold the token for that to be shown. It must for a typed request, which leaves memory on, so
# a token still in the summary means the saved memory survived. It need not after "Delete and turn
# off memory": memory was emptied and switched off, so any later summary was rebuilt from chats.
PAST_CONVERSATIONS_REMAIN: dict[tuple[str, str], bool] = {
    ("chatgpt", "NL forget prompt"): True,     # "does not remove mentions ... from past conversations"
    ("chatgpt", "Clear all memories"): False,  # "It does not delete past chats."
    ("copilot", "Delete all memory"): True,    # "Your conversation history will not be deleted."
}

# Cells whose erasure action itself visibly failed: nothing was deleted, so the recall says
# nothing about erasure and the cell is can't tell whatever the probes found (user decision
# 2026-10-27, from the interface-change review). Value: the reason, quoted from the screen.
FAILED_ERASURES: dict[str, str] = {
    "GE-I2-E4": "Gemini reported \"Something went wrong and the info wasn't deleted\"; the item stayed listed",
    "GE-I1-E5": "the delete click failed on all 3 attempts; the empty list was observed later, not caused by the action",
}


def probe_status(auto: str | None, reviewed: str | None = None) -> str:
    """One probe's status from its automatic label and, if present, the human review.

    A review overrides the automatic label. UNCLEAR stays PENDING (it goes to a
    second reviewer). R2 review values are VERBATIM / PARAPHRASED / ABSENT.
    NON-ANSWER (a Gemini app-permission card instead of a reply) and N/A (no
    surface for the probe to read: a MAXIMAL erasure turned ChatGPT memory off,
    or memory was never on for the account) take the probe out, so the cell
    rests on its other probes (user decisions 2026-10-19).
    """
    review = (reviewed or "").strip().upper()
    if review:
        if review in ("FOUND", "VERBATIM", "PARAPHRASED"):
            return FOUND
        if review in ("NOT FOUND", "ABSENT"):
            return NOT_FOUND
        if review in ("NON-ANSWER", "N/A"):
            return NA
        return PENDING  # UNCLEAR or anything unexpected: never guess
    label = (auto or "").strip().upper()
    if not label:
        return NOT_RECALLED
    if label.startswith("TOKEN FOUND"):
        return FOUND
    if label.startswith("NOT FOUND"):
        return NOT_FOUND
    if label.startswith("N/A"):
        return NA
    return PENDING  # REVIEW (...), PARTIAL (...)


SIBLING_NOTE = "TOKEN SURFACED IN SIBLING RECALL"  # written by tester/sibling_tokens.surfaced_note()


def sibling_exposed(notes: str) -> bool:
    """Whether the Notes record a sibling exposure that still stands.

    Notes are " | "-separated entries in time order. A later CORRECTION entry that names the
    sibling note and calls it withdrawn cancels it (e.g. CL-NLF-I0260, withdrawn 2026-10-18
    because the sibling only quoted its own earlier erasure reply).
    """
    exposed = False
    for entry in notes.split(" | "):
        if entry.startswith(SIBLING_NOTE):
            exposed = True
        elif entry.startswith("CORRECTION") and SIBLING_NOTE in entry and "withdrawn" in entry:
            exposed = False
    return exposed


def miss_counts(probe: str, injection_type: str, retention: str | None) -> bool:
    """Whether a miss on `probe` is evidence of absence (the layer was reached)."""
    kept = retention in RETAINED
    if probe == "r2":
        return kept or (injection_type in ("I2", "I3") and retention != "denied")
    return kept


def recoverability(
    statuses: dict[str, str], injection_type: str, retention: str | None, sibling_exposed: bool = False,
) -> tuple[str, str]:
    """(value, reason) for the new-conversation recall of one cell.

    sibling_exposed: another NL-forget cell's recall returned this cell's token
    (workbook Notes "TOKEN SURFACED IN SIBLING RECALL"). Sibling rule, user
    decision 2026-10-18: the erasure failed, so the cell is RECOVERED whatever
    its own probes show (tester/sibling_tokens.py).
    """
    if injection_type == "FILE":
        return FILE_TAXONOMY, "file cells use a separate verification taxonomy"
    if any(statuses.get(p, NOT_RECALLED) == NOT_RECALLED for p in ("r1", "r3")):
        return NOT_RECALLED, "no recall recorded"
    found = [p for p in PROBES if statuses.get(p) == FOUND]
    if found:
        return RECOVERED, f"found by {', '.join(p.upper() for p in found)}"
    if sibling_exposed:
        return RECOVERED, "token surfaced in a sibling cell's recall (sibling rule)"
    pending = [p for p in PROBES if statuses.get(p) == PENDING]
    if pending:
        return PENDING_REVIEW, f"{', '.join(p.upper() for p in pending)} awaiting human review"
    counting = [p for p in PROBES if statuses.get(p) == NOT_FOUND and miss_counts(p, injection_type, retention)]
    if counting:
        return NOT_RECOVERED, f"miss counts for {', '.join(p.upper() for p in counting)} (retention: {retention})"
    return INDETERMINATE, f"no miss counts as evidence of absence (retention: {retention})"


def policy_consistency(commitment: str | None, interface_change: str | None, recov: str) -> tuple[str, str]:
    """(value, reason) from the commitment type, interface change and recoverability."""
    if recov in (NOT_RECALLED, FILE_TAXONOMY):
        return recov, "no verdict before recall" if recov == NOT_RECALLED else "classified separately"
    if not commitment:
        return INDETERMINATE, "commitment type missing"
    if commitment == DELETES:
        if recov == RECOVERED:
            return CONTRADICTED, "content recovered"
        if interface_change == UNCHANGED:
            return CONTRADICTED, "interface unchanged"
        if recov == NOT_RECOVERED:
            if interface_change in (CHANGED, NOT_OBSERVABLE):
                return CONSISTENT, "not recovered and interface not unchanged"
            return INDETERMINATE, "interface change not coded"
        return INDETERMINATE, f"recoverability {recov.lower()}"
    if commitment == DOES_NOT_DELETE:
        if recov == RECOVERED:
            return CONSISTENT, "content recovered, as the documentation says it would remain"
        return INDETERMINATE, "documentation states scope only; a miss shows nothing"
    return INDETERMINATE, f"{commitment.lower()}: reported descriptively"


def effective_interface_change(erasure: str | None, coded: str | None) -> str | None:
    """A typed request leaves nothing on the interface to inspect."""
    return NOT_OBSERVABLE if (erasure or "").strip() in TYPED_ERASURES else (coded or None)


@dataclass
class CellInputs:
    cell_id: str
    sheet: str
    platform: str
    injection_type: str
    erasure: str
    run_status: str
    commitment: str | None
    acknowledgment: str | None
    interface_coded: str | None
    retention: str | None
    statuses: dict[str, str]
    sibling_exposed: bool
    same_conversation: str  # reported separately, never enters a derivation


def _headers(ws) -> dict[str, int]:
    """Header text (stripped) -> 0-based column index."""
    return {str(c.value).strip(): i for i, c in enumerate(ws[1]) if c.value}


def _cell(row: tuple, idx: dict[str, int], name: str):
    i = idx.get(name)
    value = row[i] if i is not None and i < len(row) else None
    return None if value in ("", None) else str(value).strip()


def load_retention() -> dict[str, str]:
    with RETENTION_CSV.open() as f:
        return {r["cell"]: r["retention"] for r in csv.DictReader(f)}


def load_cells() -> list[CellInputs]:
    """Every non-FILE cell of MASTER and NL FORGET with its derivation inputs."""
    warnings.filterwarnings("ignore", category=UserWarning)
    retention = load_retention()
    wb = openpyxl.load_workbook(WORKBOOK, read_only=False, data_only=True)
    cells: list[CellInputs] = []
    for sheet, erasure_col in (("MASTER ", "Erasure desc"), ("NL FORGET", "Erasure")):
        ws = wb[sheet]
        idx = _headers(ws)
        for row in ws.iter_rows(min_row=2, values_only=True):
            cell_id = _cell(row, idx, "Cell ID")
            if not cell_id:
                continue
            statuses = {}
            for probe, auto_name in (
                ("r1", "R1 (direct) new-conv"),
                ("r2", "R2 (settings) new-conv"),
                ("r3", "R3 (indirect) new-conv"),
            ):
                statuses[probe] = probe_status(
                    _cell(row, idx, auto_name), _cell(row, idx, f"Reviewed: {auto_name}")
                )
            same_name = "R1 (direct) same-conv (typed erasure only)"
            same_conversation = probe_status(_cell(row, idx, same_name), _cell(row, idx, f"Reviewed: {same_name}"))
            injection = _cell(row, idx, "Injection") or ""
            cells.append(CellInputs(
                cell_id=cell_id, sheet=sheet.strip(), platform=(_cell(row, idx, "Platform") or "").lower(),
                injection_type=injection, erasure=_cell(row, idx, erasure_col) or "",
                run_status=_cell(row, idx, "Run status") or "",
                commitment=_cell(row, idx, "Commitment type"),
                acknowledgment=_cell(row, idx, "Acknowledgment (coded)"),
                interface_coded=_cell(row, idx, "Interface change (coded)"),
                retention=retention.get(cell_id), statuses=statuses,
                sibling_exposed=sibling_exposed(_cell(row, idx, "Notes") or ""),
                same_conversation=same_conversation,
            ))
    return cells


def derive(c: CellInputs) -> dict[str, str]:
    recov, recov_reason = recoverability(c.statuses, c.injection_type, c.retention, c.sibling_exposed)
    if c.cell_id in FAILED_ERASURES:
        recov, recov_reason = INDETERMINATE, f"erasure action failed: {FAILED_ERASURES[c.cell_id]}"
    interface = effective_interface_change(c.erasure, c.interface_coded)
    policy, policy_reason = policy_consistency(c.commitment, interface, recov)
    summary_must_be_clear = PAST_CONVERSATIONS_REMAIN.get((c.platform, (c.erasure or "").strip()))
    if policy == CONTRADICTED and recov == RECOVERED and summary_must_be_clear is not None:
        if not summary_must_be_clear or c.statuses["r2"] == NOT_FOUND:
            policy, policy_reason = CONSISTENT, "recovered from past conversations, which the documentation says remain"
        elif c.statuses["r2"] != FOUND:
            policy, policy_reason = INDETERMINATE, "recovered, but the memory summary was not read"
    return {
        "cell_id": c.cell_id, "sheet": c.sheet, "platform": c.platform, "injection": c.injection_type,
        "erasure": c.erasure, "run_status": c.run_status, "commitment": c.commitment or "",
        "retention": c.retention or "", "interface_change": interface or "",
        "acknowledgment": c.acknowledgment or "",
        "r1": c.statuses["r1"], "r2": c.statuses["r2"], "r3": c.statuses["r3"],
        "same_conversation_r1": c.same_conversation,
        "recoverability": recov, "recoverability_reason": recov_reason,
        "policy_consistency": policy, "policy_reason": policy_reason,
    }


def missing_inputs(c: CellInputs) -> list[str]:
    """Inputs that block a verdict for an erased cell, so gaps are visible, never guessed."""
    if c.injection_type == "FILE" or c.run_status not in ("ERASED", "RECALLED"):
        return []
    gaps = []
    if not c.commitment:
        gaps.append("commitment type")
    if not c.acknowledgment:
        gaps.append("acknowledgment")
    if not c.retention:
        gaps.append("retention at injection")
    if c.erasure not in TYPED_ERASURES and not c.interface_coded:
        gaps.append("interface change")
    return gaps


def main() -> None:
    cells = load_cells()
    rows = [derive(c) for c in cells]
    OUT_TABLE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_TABLE.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    lines = [f"cells read: {len(cells)} (MASTER and NL FORGET; FILE cells are classified separately)", ""]
    lines.append("recoverability (new-conversation recall):")
    for k, v in Counter(r["recoverability"] for r in rows).most_common():
        lines.append(f"  {k:30} {v}")
    lines.append("\npolicy consistency:")
    for k, v in Counter(r["policy_consistency"] for r in rows).most_common():
        lines.append(f"  {k:30} {v}")
    gaps = Counter()
    for c in cells:
        for g in missing_inputs(c):
            gaps[g] += 1
    erased = sum(1 for c in cells if c.run_status in ("ERASED", "RECALLED") and c.injection_type != "FILE")
    lines.append(f"\nmissing inputs among {erased} erased cells (each blocks or weakens a verdict):")
    for k, v in gaps.most_common():
        lines.append(f"  {k:30} {v}")
    if not gaps:
        lines.append("  none")
    lines.append(f"\nper-cell table: {OUT_TABLE}")
    for line in lines:
        print(line)
    print(f"report saved -> {save_report('audit_outcomes', lines)}")


if __name__ == "__main__":
    main()
