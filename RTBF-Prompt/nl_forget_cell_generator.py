"""Generates the 828 NL-forget-prompt study cells (138 authoritative prompts
x 6 platforms) from nl_forget_prompts_138_final.csv -- disclosure sentence,
recall-probe text (R1/R2/R3), and distractors, reusing the exact same
template constants and collision-free seeded draw as token_generator.py /
nl_forget_token_generator.py rather than re-deriving any of it.

Injection is fixed I1-style chat disclosure for every cell (design decision,
2026-09-11): this study tests erasure-phrasing sensitivity, not injection-
type sensitivity, and NL-forget erasure is itself a chat message
(_send_nl_forget()), so I1 keeps injection and erasure on the same surface
(see PROJECT_STATUS.md / project memory for the full reasoning). Recall
probes stay the same multi-surface R1 (direct chat) / R2 (settings/memory
panel) / R3 (indirect chat) design used by every other cell in the 88-cell
battery, checking for residual leakage beyond just the injection surface --
not something specific to NL-forget cells.

Distractors: continues the EXACT SAME seeded draw as the rest of the
project (token_generator.SEED, via draw_distractors() over the full
520-token pool = 250 existing + 270 nl_forget), so distractors are
collision-free against every token in use anywhere, by construction.

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
RECALL_PROBES_MD = REPO_ROOT / "recall_probes.md"

PLATFORM_PREFIX = {
    "chatgpt": "CH", "claude": "CL", "gemini": "GE",
    "copilot": "CO", "perplexity": "PE", "deepseek": "DE",
}

NLFORGET_ACCOUNT_EMAIL = "astrataiwo@gmail.com"


def load_prompts() -> list[dict]:
    with PROMPTS_CSV.open() as f:
        return list(csv.DictReader(f))


def build_distractors_for_138() -> list[tuple]:
    """Same collision-free seeded draw as the rest of the project --
    continues to a 520-token pool (250 existing + 270 nl_forget), draws 3
    length-matched distractors per token for all 520, then takes the first
    138 (pool_index 1-138, the ones actually in use here)."""
    words = tg.filter_denylist(tg.filter_excluded_categories(tg.filter_to_nouns(tg.load_wordlist(tg.WORDLIST_PATH))))
    full_pool = tg.build_token_pool(words, tg.SEED, 520)
    distractors_520 = tg.draw_distractors(words, tg.SEED, full_pool, n_assigned=520, n_distractors=3)
    return distractors_520[250:250 + 138]  # nl_forget pool starts at index 250


def main() -> None:
    prompts = load_prompts()
    assert len(prompts) == 138, f"expected 138 prompts, got {len(prompts)}"
    distractors_138 = build_distractors_for_138()

    cell_rows = []
    recall_probe_lines = []

    for i, p in enumerate(prompts):
        referent = p["referent"]
        token_str = p["token"]
        item_id = p["item_id"]
        erasure_request_text = p["final_erasure_text"]

        disclosure = tg.I1_TEMPLATES[i % len(tg.I1_TEMPLATES)].format(referent=referent, token=token_str)
        r1_open = tg.R1_OPEN_TEMPLATES[i % len(tg.R1_OPEN_TEMPLATES)].format(referent=referent)
        d1, d2, d3 = [tg.token(d) for d in distractors_138[i]]
        r1_choice = tg.R1_CHOICE_TEMPLATE.format(token=token_str, d1=d1, d2=d2, d3=d3)
        r2 = tg.R2_PROCEDURE_TEMPLATE.format(referent=referent, token=token_str)
        r3 = tg.R3_INDIRECT_TEMPLATES[i % len(tg.R3_INDIRECT_TEMPLATES)].format(referent=referent)

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
                f"| {cell_id} | I1 | {token_str} | NL forget prompt | {r1_open} | {r1_choice} | {r2} | {r3} |"
            )

    assert len(cell_rows) == 828, f"expected 828 cell rows, got {len(cell_rows)}"

    with OUT_CELLS_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cell_rows[0].keys()))
        w.writeheader()
        w.writerows(cell_rows)

    with RECALL_PROBES_MD.open("a") as f:
        f.write("\n## NL-forget-prompt study (138 authoritative prompts x 6 platforms, added 2026-09-11)\n\n")
        f.write("| Cell ID | Injection | Token | Erasure | R1 (open) | R1 (choice) | R2 (settings) | R3 (indirect) |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for line in recall_probe_lines:
            f.write(line + "\n")

    print(f"Wrote {len(cell_rows)} cell rows to {OUT_CELLS_CSV}")
    print(f"Appended {len(recall_probe_lines)} recall-probe rows to {RECALL_PROBES_MD}")


if __name__ == "__main__":
    main()
