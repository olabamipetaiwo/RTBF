"""Regenerates token.md/data/token_assignment.csv/recall_probes.md from the
live xlsx (data/RTBF Experiments.xlsx), the actual source of truth (see
tester/CLAUDE.md and run_cell.py, which read tokens/disclosure text
straight from it, never from these docs).

Why this exists: multiple re-injections since the original
token_generator.py run (2026-08-26) -- MAXIMAL account moves, structural-
conflict isolation, data-loss recovery, the Claude memory-migration
re-injection, this session's Gemini-instability migration -- updated the
xlsx live but never wrote the change back into token.md/
token_assignment.csv/recall_probes.md. Found 2026-09-09: 34 of 85 live
cells had a stale token in token.md. Direct instruction from the user
(2026-09-09): there should be no doc drift anywhere, full sync now.

Cannot just re-run token_generator.py's own write_token_md()/
write_recall_probes_md() -- those call disclosure_sentence()/
recall_probes(), which derive each cell's referent from
REFERENTS[sorted(load_cell_ids(xlsx)).index(cell_id)]. That index has
drifted from original-generation time (3 ChatGPT cells were archived,
shifting every later cell's sorted position), so recomputing now would
silently reassign DIFFERENT referents than what's already been disclosed
live to each platform -- a much worse drift than the one being fixed.

Instead: the live disclosure sentence in the xlsx is authoritative and
already contains the real referent. This script reverse-parses the
referent out of it (try each template in the cell's injection-type
family against the known token; exactly one should match) rather than
trusting any index-based lookup. R1-open/R3-indirect phrasing variant
choice is free to pick fresh here (deterministic by cell_id) since recall
hasn't run for ANY cell yet (confirmed via tester/data/run_tracking.json,
0 of 78 recalled as of 2026-09-09) -- nothing has been probed with the
old phrasing that would need to stay fixed.

Distractors are regenerated for every live cell (not just the 34
drifted), continuing token_generator.py's own seeded draw sequence in
sorted-cell-id order, excluding the full 250-entry token pool (both live
and reserve) throughout so global uniqueness is preserved. Safe for the
same reason -- no recall has used the old distractor sets yet.

Run: python sync_docs_from_xlsx.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

import token_generator as tg

WORDLIST_PATH = tg.WORDLIST_PATH
XLSX_PATH = tg.XLSX_PATH
MAPPING_CSV_PATH = tg.MAPPING_CSV_PATH
TOKEN_MD_PATH = tg.TOKEN_MD_PATH
RECALL_PROBES_MD_PATH = tg.RECALL_PROBES_MD_PATH


def load_live_disclosures(xlsx_path: Path) -> dict[str, str]:
    """cell_id -> live disclosure sentence, straight from the xlsx."""
    import openpyxl

    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    out: dict[str, str] = {}
    for sheetname in ("MASTER ", "FILE SUBSTUDY"):
        ws = wb[sheetname]
        header = [c.value for c in ws[1]]
        col_idx = {h: i + 1 for i, h in enumerate(header) if h}
        cellid_col = col_idx["Cell ID"]
        disc_col = next(col_idx[h] for h in header if h and "Disclosure" in h)
        for row in ws.iter_rows(min_row=2):
            cid = row[cellid_col - 1].value
            if cid:
                out[cid] = row[disc_col - 1].value
    return out


def load_live_tokens(xlsx_path: Path) -> dict[str, str]:
    """cell_id -> live token string, straight from the xlsx."""
    import openpyxl

    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    out: dict[str, str] = {}
    for sheetname in ("MASTER ", "FILE SUBSTUDY"):
        ws = wb[sheetname]
        header = [c.value for c in ws[1]]
        col_idx = {h: i + 1 for i, h in enumerate(header) if h}
        cellid_col = col_idx["Cell ID"]
        anchor_col = next(col_idx[h] for h in header if h and "Anchor" in h)
        for row in ws.iter_rows(min_row=2):
            cid = row[cellid_col - 1].value
            if cid:
                out[cid] = row[anchor_col - 1].value
    return out


def recover_referent(disclosure: str, token_str: str, injection_type: str) -> str:
    """Reverse-parses the referent out of an already-live disclosure
    sentence by trying each candidate template for this injection type
    against the known token, rather than trusting any index-based
    REFERENTS[] lookup (see module docstring for why that's unsafe now).
    Builds a regex from each template (literal parts escaped, {referent}
    -> capture group, {token} -> the known literal token) and matches the
    whole disclosure string against it."""
    import re

    if injection_type == "I1":
        templates = tg.I1_TEMPLATES
    elif injection_type == "I2":
        templates = tg.I2_TEMPLATES
    elif injection_type == "I3":
        templates = [tg.I3_TEMPLATE]
    elif injection_type == "FILE":
        templates = [tg.FILE_CONTENT_TEMPLATE]
    else:
        raise ValueError(f"unknown injection type: {injection_type!r}")

    for template in templates:
        placeholder = "\x00REFERENT\x00"
        filled = template.replace("{referent}", placeholder).format(token=token_str)
        pattern = "^" + re.escape(filled).replace(re.escape(placeholder), "(.+)") + "$"
        m = re.match(pattern, disclosure)
        if m:
            return m.group(1)
    raise RuntimeError(
        f"recover_referent: no {injection_type} template matches disclosure "
        f"{disclosure!r} with token {token_str!r}"
    )


def main() -> None:
    raw_words = tg.load_wordlist(WORDLIST_PATH)
    nouns = tg.filter_to_nouns(raw_words)
    categorized = tg.filter_excluded_categories(nouns)
    words = tg.filter_denylist(categorized)

    injection_types = tg.load_injection_types(XLSX_PATH)
    erasure_desc = tg.load_erasure_desc(XLSX_PATH)
    live_tokens = load_live_tokens(XLSX_PATH)
    live_disclosures = load_live_disclosures(XLSX_PATH)
    cell_ids = sorted(live_tokens)

    token_pool = tg.build_token_pool(words, tg.SEED, tg.N_TOKENS)
    pool_by_str = {tg.token(tup): tup for tup in token_pool}

    assigned: list[tuple[str, tuple[str, ...]]] = []
    referents: dict[str, str] = {}
    unmatched = []
    for cid in cell_ids:
        live_tok = live_tokens[cid]
        tup = pool_by_str.get(live_tok)
        if tup is None:
            unmatched.append(cid)
            continue
        assigned.append((cid, tup))
        referents[cid] = recover_referent(live_disclosures[cid], live_tok, injection_types[cid])

    if unmatched:
        raise RuntimeError(
            f"{len(unmatched)} live cell(s) have a token not found in the "
            f"deterministic {tg.N_TOKENS}-entry pool (SEED={tg.SEED}) -- "
            f"can't safely sync, investigate before proceeding: {unmatched}"
        )

    live_tuples = {tup for _, tup in assigned}
    reserve = [tup for tup in token_pool if tup not in live_tuples]

    # Regenerate distractors for every live cell, continuing the same
    # seeded stream token_generator.py uses, excluding the FULL pool
    # (live + reserve) throughout to preserve global uniqueness for any
    # future reserve draw too.
    rng = random.Random(tg.SEED)
    tg._sample_distinct_tuples(rng, words, len(token_pool), exclude=set(), length_choices=tg.LENGTH_CHOICES)
    exclude = set(token_pool)
    distractors_by_cell: dict[str, list[tuple[str, ...]]] = {}
    for cid, tup in assigned:
        d = tg._sample_distinct_tuples_fixed_length(rng, words, tg.DISTRACTORS_PER_TOKEN, exclude, len(tup))
        exclude.update(d)
        distractors_by_cell[cid] = d

    # --- write token_assignment.csv ---
    with MAPPING_CSV_PATH.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "cell_id", "injection_type", "token", "token_length",
            "disclosure_sentence", "distractor_1", "distractor_2", "distractor_3",
        ])
        for cid, tup in assigned:
            writer.writerow([
                cid, injection_types[cid], tg.token(tup), len(tup),
                live_disclosures[cid],
                *[tg.token(d) for d in distractors_by_cell[cid]],
            ])

    # --- write token.md ---
    lines = []
    lines.append("# RTBF Technical Audit -- Injected Anchor Tokens")
    lines.append("")
    lines.append(
        f"Synced from the live xlsx by `sync_docs_from_xlsx.py`, "
        f"{len(assigned)} live cells, {len(reserve)} held in reserve "
        f"(same deterministic {tg.N_TOKENS}-token pool as the original "
        f"`token_generator.py` run, seed `{tg.SEED}`). Tokens and "
        f"disclosure text here are read directly from the xlsx (the "
        f"authoritative source, see tester/CLAUDE.md) -- this file is a "
        f"synced view, not independently generated. Re-run this script "
        f"after any re-injection so it never drifts again."
    )
    lines.append("")
    lines.append("## Assigned (live cells)")
    lines.append("")
    lines.append("| Cell ID | Injection type | Anchor token | Disclosure/injection text | Distractors |")
    lines.append("|---|---|---|---|---|")
    for cid, tup in assigned:
        cw = tg.token(tup)
        distractors = ", ".join(tg.token(d) for d in distractors_by_cell[cid])
        lines.append(f"| {cid} | {injection_types[cid]} | {cw} | {live_disclosures[cid]} | {distractors} |")
    lines.append("")
    lines.append(f"## Reserve pool ({len(reserve)} unassigned)")
    lines.append("")
    lines.append(
        "For reruns of a deviating cell or new cells added later. Draw in "
        "order. Disclosure text isn't pre-computed here -- build it from "
        "the cell's own injection-type template once known (see "
        "token_generator.py's I1/I2/I3/FILE_CONTENT templates), same as "
        "any other re-injection."
    )
    lines.append("")
    lines.append("| # | Anchor token | Length |")
    lines.append("|---|---|---|")
    for j, tup in enumerate(reserve):
        lines.append(f"| {j + 1} | {tg.token(tup)} | {len(tup)} |")
    TOKEN_MD_PATH.write_text("\n".join(lines) + "\n")

    # --- write recall_probes.md ---
    lines = []
    lines.append("# RTBF Technical Audit -- Recall Probe Runbook")
    lines.append("")
    lines.append(
        "Synced from the live xlsx by `sync_docs_from_xlsx.py`. See "
        "token.md's header for the token/pool provenance. R1-open/"
        "R3-indirect phrasing variant is chosen fresh per cell here "
        "(deterministic by cell_id) since no cell has been recalled yet "
        "(tester/data/run_tracking.json) -- nothing already probed that "
        "needs to stay fixed."
    )
    lines.append("")
    lines.append(
        "- **R1 (direct)**: two-stage. Ask the open question first -- "
        "unprompted production of the exact token is the strongest "
        "signal. Only if that's wrong, refused, or ambiguous, follow up "
        "with the forced-choice question (true token vs. 3 length-matched "
        "distractors, Staufer 2025/WikiMem-style)."
    )
    lines.append(
        "- **R2 (settings)**: not a chat probe -- a fixed inspection "
        "procedure against the platform's memory/personalization UI."
    )
    lines.append(
        "- **R3 (indirect)**: the token never appears in the probe text "
        "itself."
    )
    lines.append("")
    lines.append(
        "Erasure column is informational, straight from the MASTER/FILE "
        "SUBSTUDY sheets. For the 13 cells flagged \"Blocked on prompt "
        "set?\" = YES, the erasure request text itself comes from the "
        "qualitative-coding pipeline, not this script."
    )
    lines.append("")
    lines.append(
        '"Answer" is the correct token for that cell -- the ground truth '
        "to score R1/R3 responses against directly in this table."
    )
    lines.append("")
    lines.append("| Cell ID | Type | Answer (token) | Erasure (FYI, from sheet) | R1 open | R1 forced-choice | R2 procedure | R3 indirect |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for i, (cid, tup) in enumerate(assigned):
        cw = tg.token(tup)
        referent = referents[cid]
        d1, d2, d3 = [tg.token(d) for d in distractors_by_cell[cid]]
        r1_open = tg.R1_OPEN_TEMPLATES[i % len(tg.R1_OPEN_TEMPLATES)].format(referent=referent)
        r1_choice = tg.R1_CHOICE_TEMPLATE.format(token=cw, d1=d1, d2=d2, d3=d3)
        r2 = tg.R2_PROCEDURE_TEMPLATE.format(referent=referent, token=cw)
        r3 = tg.R3_INDIRECT_TEMPLATES[i % len(tg.R3_INDIRECT_TEMPLATES)].format(referent=referent)
        erasure = erasure_desc.get(cid, "")
        lines.append(
            f"| {cid} | {injection_types[cid]} | {cw} | {erasure} | {r1_open} | "
            f"{r1_choice} | {r2} | {r3} |"
        )
    RECALL_PROBES_MD_PATH.write_text("\n".join(lines) + "\n")

    print(f"Synced {len(assigned)} live cells, {len(reserve)} reserve, {len(unmatched)} unmatched.")
    print(f"Wrote {MAPPING_CSV_PATH}, {TOKEN_MD_PATH}, {RECALL_PROBES_MD_PATH}")


if __name__ == "__main__":
    main()
