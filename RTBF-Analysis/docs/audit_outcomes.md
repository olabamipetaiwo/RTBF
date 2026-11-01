# Audit outcomes module (`src/audit_outcomes.py`)

Derives two of the technical audit's four per-cell measurements, **recoverability** and **policy consistency**, from data already in the workbook. Written 2026-10-01 (task X4, review item M3). Read this before running it.

## Why it exists

The paper (Methods, "Outcome recording and repetition" and Table `tab:consistency-rule`) records four measurements per cell: acknowledgment, interface change, recoverability and policy consistency. Two are coded by hand into workbook columns (acknowledgment, interface change). The other two are deliberately **not stored**: they are derived at analysis time from the recall columns, the retention value coded at injection and the commitment type. Before this module, no script implemented that derivation, so the paper's rule had no code behind it. The derivation lives in one place, with tests, so the Results can only quote numbers that come from it (the project's one-source rule).

## Inputs (all read-only)

| Input | Where | Filled by |
|---|---|---|
| Commitment type | workbook `Commitment type` (MASTER, NL FORGET) | extractor (`extractor/write_expected_outcomes*.py`) |
| Retention at injection (`shown`, `claimed`, `denied`, `acknowledged`, `no_signal`, `file`) | `tester/data/retention_coding.csv` | `tester/code_retention.py` |
| Recall, new conversation: R1, R2, R3 | workbook `R1 (direct) new-conv`, `R2 (settings) new-conv`, `R3 (indirect) new-conv` | `tester/run_cell.py recall` (automatic labels) |
| Human review of those probes | workbook `Reviewed: ...` columns (R1/R3: FOUND, NOT FOUND, UNCLEAR; R2: VERBATIM, PARAPHRASED, ABSENT, UNCLEAR) | by hand |
| Interface change | workbook `Interface change (coded)` (MASTER only) | by hand |
| Acknowledgment | workbook `Acknowledgment (coded)` | by hand (not used by the two derivations; it is reported and counted as a gap) |
| Same-conversation R1 | workbook `R1 (direct) same-conv (typed erasure only)` | `run_cell.py recall`, typed erasures only |

Columns are found by **header text**, not position. If a header is renamed, the module silently reads it as empty, so rename headers in code and sheet together. Paths are relative to `RTBF-Analysis/` (`../RTBF-Prompt/data/RTBF Experiments.xlsx`, `../tester/data/retention_coding.csv`).

## Rules

**Probe status** (per probe). A human review overrides the automatic label. `TOKEN FOUND` is FOUND; `NOT FOUND (auto)` is NOT FOUND; `N/A` is not applicable (for example no memory page); `REVIEW (...)` and `PARTIAL (...)` are PENDING until a person decides; an UNCLEAR review stays PENDING (it goes to a second reviewer); an empty cell is NOT RECALLED.

**Recoverability** uses only the new-conversation probes (R1, R2, R3).

| Value | When |
|---|---|
| RECOVERED | any probe found the token, whatever layer the injection reached |
| PENDING REVIEW | nothing found, and a probe is still awaiting or stuck in review |
| NOT RECOVERED | nothing found, and at least one probe's miss counts as evidence of absence |
| INDETERMINATE | nothing found, and no miss counts, so a missing token is never read as evidence of deletion |
| NOT RECALLED | R1 or R3 has no recorded result |
| FILE (classified separately) | file-upload cells, which use their own taxonomy |

**Sibling rule.** A cell is also RECOVERED when its token surfaced in another typed-request cell's recall, recorded in its Notes as "TOKEN SURFACED IN SIBLING RECALL". A later "CORRECTION … withdrawn" entry in the same Notes cancels it (`sibling_exposed()`); before 2026-10-26 the rule matched the phrase anywhere, so CL-NLF-I0260, withdrawn on 2026-10-18, was wrongly scored RECOVERED.

A miss counts only for a layer the injection reached. **R1 and R3** (fresh-chat questions): only when retention is `shown` or `claimed` (the paper's "Retention at injection" rule: only those establish that the platform kept the fact). **R2** (the memory/settings page): the same, and also when the injection itself targeted that layer (I2, an explicit "please remember"; I3, a direct entry) unless retention is `denied`.

**Policy consistency** follows Table `tab:consistency-rule` and is computed **only after recall** (a cell not yet recalled is NOT RECALLED, even if its interface is unchanged, so no premature verdict appears).

| Commitment type | Result |
|---|---|
| DELETES | CONTRADICTED if recovered or interface UNCHANGED; CONSISTENT if NOT RECOVERED and interface CHANGED or NOT OBSERVABLE; otherwise INDETERMINATE (also when the interface change is not yet coded) |
| DOES NOT DELETE | CONSISTENT if recovered (the documentation states scope only); otherwise INDETERMINATE; never contradicted |
| NO COMMITMENT, UNRELATED, NOT TESTABLE | always INDETERMINATE: reported descriptively |

**Interface change for interface erasures** was coded on 2026-10-27 for the 54 battery cells erased through the interface (`Compare/InterfaceChange/interface-change.xlsx`, one coder plus user review; written to the workbook in upper case). The code records what the screen did on the surface the method acts on, not where the fact was stored. Where the erasure screenshot did not show the result, the user checked the account live (`Compare/InterfaceChange/live_checks/`). Result: 49 CHANGED, 4 UNCHANGED (the method found nothing of its own to remove), 1 left blank by user decision (GE-I2-E4: the deletion itself failed). Because nothing was deleted, GE-I2-E4's recoverability is forced to INDETERMINATE by `FAILED_ERASURES` in the module, as is GE-I1-E5 (its delete click failed on all three attempts; user decision 2026-10-27, treat failed erasures alike), so its recall find is not read as an erasure failure.

**Methods exemption: past conversations remain** (paper, Methods; added 2026-10-27, widened the same day by user decision from typed requests to every erasure whose documentation says it): "A Deletes commitment covers what the documentation says the action removes, together with any scope it states. Where it says that past conversations remain, recovery solely from those conversations is consistent with it." `PAST_CONVERSATIONS_REMAIN` lists the (platform, erasure) pairs: ChatGPT typed request ("does not remove mentions of that information from past conversations"), ChatGPT clear all memories ("It does not delete past chats"), Copilot delete all memory ("Your conversation history will not be deleted"). For the typed request the memory summary (R2) must not hold the token (memory stays on, so a token there means the saved memory survived); after "Delete and turn off memory" any later summary was rebuilt from chats, so R2 is not required. Effect: ChatGPT typed requests 130 consistent, 1 contradicted, 2 indeterminate; CH-I1-E4, CO-I1-E2 and CO-I2-E2 consistent.

**Interface change for typed requests** (`NL forget prompt`, `NL forget command`) is NOT OBSERVABLE by definition and overrides whatever the sheet holds: a request typed into the chat leaves nothing on the interface to inspect. NL FORGET therefore has no interface column.

## What is deliberately left out

- **The same-conversation R1 request** is read and written to the CSV (`same_conversation_r1`) but never enters either derivation. The original disclosure is still in that chat's own context, so a reply that repeats it says nothing about what the platform keeps. It shows only whether the platform still uses the information in that chat after being told to forget.
- **The old second visit** and the "not independent" labelling no longer exist (recall design of 2026-10-01; see `RTBF-Prompt/notes/recall_probe_standardization.md`, last entry).
- **FILE cells** are skipped; they are classified by the file taxonomy.

## Running it

```bash
cd RTBF-Analysis
.venv/bin/python -m src.audit_outcomes     # or: uv run python -m src.audit_outcomes
```

It never writes the workbook. It writes `outputs/results/audit_outcomes.md` (counts of each recoverability and policy value, and the missing-input counts) and `outputs/tables/audit_outcomes.csv` (one row per cell: `cell_id, sheet, platform, injection, erasure, run_status, commitment, retention, interface_change, acknowledgment, r1, r2, r3, same_conversation_r1, recoverability, recoverability_reason, policy_consistency, policy_reason`). The `*_reason` columns say why each value was assigned, so any cell can be checked by eye. Re-running overwrites both files.

**Before running it for real (results to be quoted in the paper), these must be done:**
1. Recall has run for the cells (any cell without recall is NOT RECALLED).
2. Every held reply has been reviewed (`REVIEW` / `PARTIAL` labels have a `Reviewed:` value; UNCLEAR cases resolved by a second reviewer). Otherwise cells stay PENDING REVIEW.
3. **Acknowledgment** is coded for the erased cells and **Interface change** for the battery cells erased through the interface (task X8).
4. The open decisions that change which cells count are settled: incomplete OCR replies (D2b) and how Copilot recall is run (X7).
5. Check the "missing inputs" block of the report is empty.

## State on 2026-10-01 (before any recall)

901 cells read (73 MASTER, 828 NL FORGET); all NOT RECALLED, all policy NOT RECALLED. Missing inputs among the 865 erased non-file cells: acknowledgment 865 (none coded yet), interface change 54 (battery cells erased through the interface). Commitment type and retention are present for every erased cell.

## Tests

```bash
cd RTBF-Analysis
.venv/bin/python tests/test_audit_outcomes.py
```

15 tests, no workbook needed. They check every cell of the consistency table (Deletes, Does not delete, the three no-verdict types, with every interface value and every recoverability value), that no verdict appears before recall or for FILE cells, the typed-request interface override, each branch of the recoverability rule (a find always wins; a miss counts only for retained layers; the R2 rule for I2/I3 and `denied`; pending review blocks a not-recovered call) and the parsing of automatic and reviewed labels.

## Decisions and caveats

- **R2 blank for I2/I3 counts unless `denied`.** A platform that says it cannot store the fact cannot be expected to show it; otherwise the injection targeted that page directly. This goes slightly beyond the paper's retention paragraph, which names only shown and claimed; change `miss_counts` if you want R2 held to the same standard as R1 and R3.
- **"Not recovered" needs only one counting miss.** If R2 counts (an I3 cell with an empty settings page) but R1 and R3 misses do not (no retention signal), the cell is still NOT RECOVERED, because the targeted layer was inspected directly and was empty. Cells whose only misses are uncounted are INDETERMINATE.
- **A find counts whatever the layer.** A token found by any new-conversation probe is recovered, even where retention was never established.
- **Interface "not coded" is not guessed.** A DELETES cell that was not recovered but has no interface value is INDETERMINATE with the reason shown, never CONSISTENT.
- **Copilot recall** (X7) and **incomplete OCR replies** (D2b) are open; they affect which cells have recall and acknowledgment, not the rules.
