# Claude: evidence

Supports [`../claude-platform.md`](../claude-platform.md). Every number with the script it comes from, and the rival-explanations table.

**Outcomes** (`RTBF-Analysis/src/audit_outcomes.py`, `outputs/tables/audit_outcomes.csv`)

| | Recall success | Recall failed | Can't tell |
|---|---|---|---|
| Typed erasure, 138 participant prompts (133 recalled) | 0 | 131 | 2 |
| Main grid (15 cells) | 3 | 10 | 2 |

**Main grid by method**

| Method | Recall success | Recall failed | Can't tell |
|---|---|---|---|
| Delete conversation | 3 (1 had no conversation to delete) | 0 | 0 |
| Delete individual memory edit | 0 | 3 | 0 |
| Clear all memories (typed request on the Memory page) | 0 | 2 | 1 |
| Typed erasure command | 0 | 2 | 1 |
| MAXIMAL | 0 | 3 | 0 |

**Probe that retrieved the token** (main grid, 3 cells; `src/platform_breakdown.py` → `outputs/results/platform_breakdown.md`): R1 and R3 in all 3; the memory summary in none.

**Memory page after deleting a conversation**: topic names and summaries only (for example "Garden: Facts about the user's garden/vegetable patch"; "Pottery: User's pottery projects and piece names"), without the names they contain. The memory summary therefore cannot show whether a token is held.

**Acknowledgment at erasure** (typed erasure, 133 cells; two coders, AC1 = 0.969): COMPLIED 95; OTHER 14; PARTIAL 13; DEFLECTED 10; SILENTLY IGNORED 1. None of the 95 COMPLIED cells was retrieved.

**Same conversation against new conversation** (`src/platform_breakdown.py`)
- Participants' typed requests: the name was repeated in the original conversation in 88 of 132 cells (86 recall failed, 2 can't tell) and withheld in 44 (all recall failed).
- Our own typed command (main grid): repeated in 1 of 2 cells with a same-conversation check.

**Replies in a new conversation** (all 133 typed-request cells read): every reply reported having no name for the item, for example "I don't have a name on file for it" or "I can't find a name we settled on". None declined by citing the earlier request (consistent with `src/recall_refusals.py`: 0 of 131).

**Review of automatic matches** (`Compare/FoundSpotCheck/`): the 3 main-grid recall successes were among the 160 automatic FOUNDs reviewed across platforms; all were confirmed.

**Review of retention at injection** (`Compare/RetentionCheck/claude-Retention Check.xlsx`; applied in `tester/code_retention.py`, REVIEWED): we reviewed the retention code of all 145 cells scored recall failed or can't tell. The review agreed with the rule in 137. Of the 8 changes, two moved a cell from can't tell to recall failed, where the screenshot showed a memory notice the rule had missed ("Read and updated memory"; "Read and edited memory"); the other six did not change an outcome.

**Scoring correction** (2026-10-26): one typed-request cell had been scored recall success under the sibling rule although that exposure was withdrawn on 2026-10-18 (the other cell had only quoted its own earlier erasure reply). `src/audit_outcomes.py` now honours the withdrawal; the cell is recall failed.

**Rival explanations**

| Explanation | Evidence | Verdict |
|---|---|---|
| The fact was never stored | In all 131 recall-failed typed-request cells, the interface showed a memory notice at injection; reviewed against the screenshots | Ruled out |
| Claude withholds rather than forgets | No reply in a new conversation declined or cited the request; all reported having no name | Ruled out |
| Memory switched off | Memory notices at injection in 131 cells show that memory was in use | Ruled out |
| What the user asked for, and how | No typed request was retrieved, at any level of any coded feature; our own fixed command, after a casual mention, was not retrieved either (can't tell: no storage signal) | No detectable effect |
| Contamination between cells | Unique tokens per cell; dedicated accounts for account-wide erasures; sibling rule applied, one withdrawn exposure corrected | Ruled out by design |
| Memory held apart from the conversation | Deleting the conversation left the fact retrievable in 2 of 2 cells (a third, entered in the memory settings, had no conversation to delete); the memory topics remained listed | Supported |
| Where in memory the name was held | The memory page shows topic summaries only | Open (hypothesis) |

**Survey** (`RTBF-Analysis/src/pooled_gee.py` → `outputs/results/pooled_gee.md`; `src/user_study.py` → `outputs/results/user_study.md`)
- Ask the chatbot to forget (39 observations from 29 participants): expected not referenced in future conversations 51.3%; would verify in the same conversation 53.8%, in a new one 33.3%.
- Delete a single conversation (164 observations from 105 participants): expected not referenced in future conversations 54.3%, permanently deleted 58.5%; effort 1.64, lowest of the four main methods; protection 3.63; did not know how to verify 58.5%.

**Policy verdicts** (`src/audit_outcomes.py`, rule in Table `tab:consistency-rule`; quotes from Anthropic's help page, fetched 2026-09-23/24): typed requests 131 consistent, 2 indeterminate; main grid 12 consistent (including the 2 conversation deletions, where the policy says memory remains), 3 indeterminate (2 outcome can't tell; 1 unrelated, the settings-entered fact with no conversation to delete); no contradictions.
