"""Generates the 828 NL-forget-prompt study cells (138 authoritative prompts
x 6 platforms) from nl_forget_prompts_138_final.csv -- disclosure sentence,
and recall-probe text (R1/R2/R3), reusing the exact same template
constants as token_generator.py / nl_forget_token_generator.py rather than
re-deriving any of it.

Injection is fixed I1-style chat disclosure for every cell (design decision,
2026-09-11): this study tests erasure-phrasing sensitivity, not injection-
type sensitivity, and NL-forget erasure is itself a chat message
(_send_nl_forget()), so I1 keeps injection and erasure on the same surface
(see PROJECT_STATUS.md / project memory for the full reasoning). Recall
probes stay the same multi-surface R1 (direct chat) / R2 (settings/memory
panel) / R3 (indirect chat) design used by every other cell in the 88-cell
battery, checking for residual leakage beyond just the injection surface --
not something specific to NL-forget cells.

No forced-choice distractors are built here: that recall stage was dropped
2026-09-23 (see R1_OPEN_TEMPLATES in token_generator.py), so R1 is the two
open attempts only.

Cell ID format: "<PLATFORM_PREFIX>-NLF-<item_id>", e.g. "CH-NLF-I0195".

Run: python nl_forget_cell_generator.py
Writes: data/nl_forget_cells.csv (828 rows, ready for the xlsx sheet writer)
        appends 828 rows to recall_probes.md (same table format as existing
        rows, so recall_probes_loader.py needs no changes)
"""

from __future__ import annotations

import csv
from pathlib import Path

import token_generator as tg

REPO_ROOT = Path(__file__).parent
PROMPTS_CSV = REPO_ROOT / "data" / "nl_forget_prompts_138_final.csv"
OUT_CELLS_CSV = REPO_ROOT / "data" / "nl_forget_cells.csv"
RECALL_PROBES_MD = tg.RECALL_PROBES_MD_PATH

PLATFORM_PREFIX = {
    "chatgpt": "CH", "claude": "CL", "gemini": "GE",
    "copilot": "CO", "perplexity": "PE", "deepseek": "DE",
}

NLFORGET_ACCOUNT_EMAIL = "astrataiwo@gmail.com"


def load_prompts() -> list[dict]:
    with PROMPTS_CSV.open() as f:
        return list(csv.DictReader(f))


def main() -> None:
    prompts = load_prompts()
    assert len(prompts) == 138, f"expected 138 prompts, got {len(prompts)}"

    cell_rows = []
    recall_probe_lines = []

    for i, p in enumerate(prompts):
        referent = p["referent"]
        token_str = p["token"]
        item_id = p["item_id"]
        erasure_request_text = p["final_erasure_text"]

        disclosure = tg.I1_TEMPLATES[i % len(tg.I1_TEMPLATES)].format(referent=referent, token=token_str)
        n_r1 = len(tg.R1_OPEN_TEMPLATES)
        r1_open = tg.R1_OPEN_TEMPLATES[i % n_r1].format(referent=referent)
        r1_open_followup = tg.R1_OPEN_TEMPLATES[(i + 1) % n_r1].format(referent=referent)
        r2 = tg.R2_PROCEDURE_TEMPLATE.format(referent=referent, token=token_str)
        n_r3 = len(tg.R3_INDIRECT_TEMPLATES)
        r3 = tg.R3_INDIRECT_TEMPLATES[i % n_r3].format(referent=referent)
        r3_followup = tg.R3_INDIRECT_TEMPLATES[(i + 1) % n_r3].format(referent=referent)

        for platform, prefix in PLATFORM_PREFIX.items():
            cell_id = f"{prefix}-NLF-{item_id}"
            cell_rows.append({
                "cell_id": cell_id,
                "platform": platform,
                "item_id": item_id,
                "referent": referent,
                "token": token_str,
                "disclosure_sentence": disclosure,
                "erasure_request_text": erasure_request_text,
                "email": NLFORGET_ACCOUNT_EMAIL,
                "deletion_locus": p["deletion_locus"],
                "syntactic_form": p["syntactic_form"],
                "politeness": p["politeness"],
                "verb_register": p["verb_register"],
                "justification": p["justification"],
                "swapped": p["swapped"],
                "note": p["note"],
            })
            recall_probe_lines.append(
                f"| {cell_id} | I1 | {token_str} | NL forget prompt | {r1_open} | "
                f"{r1_open_followup} | {r2} | {r3} | {r3_followup} |"
            )

    assert len(cell_rows) == 828, f"expected 828 cell rows, got {len(cell_rows)}"

    with OUT_CELLS_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cell_rows[0].keys()))
        w.writeheader()
        w.writerows(cell_rows)

    with RECALL_PROBES_MD.open("a") as f:
        f.write("\n## NL-forget-prompt study (138 authoritative prompts x 6 platforms, added 2026-09-11)\n\n")
        f.write("| Cell ID | Injection | Token | Erasure | R1 (open) | R1 (open follow-up) | R2 (settings) | R3 (indirect) | R3 (follow-up) |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")
        for line in recall_probe_lines:
            f.write(line + "\n")

    print(f"Wrote {len(cell_rows)} cell rows to {OUT_CELLS_CSV}")
    print(f"Appended {len(recall_probe_lines)} recall-probe rows to {RECALL_PROBES_MD}")


if __name__ == "__main__":
    main()
