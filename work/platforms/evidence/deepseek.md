# DeepSeek: evidence

Supports [`../deepseek.md`](../deepseek.md). Every number with the script it comes from, and the rival-explanations table.

**Outcomes** (`RTBF-Analysis/src/audit_outcomes.py`, `outputs/tables/audit_outcomes.csv`)

| | Recall success | Recall failed | Can't tell |
|---|---|---|---|
| Typed erasure, 138 participant prompts (133 recalled) | 0 | 0 | 133 |
| Main grid (4 cells: typed request, delete single conversation, delete all history, MAXIMAL) | 0 | 0 | 4 |

**Why every cell is can't tell**: retention at injection, reviewed by a person against the reply and the screenshot (`Compare/RetentionCheck/deepseek-Retention Check.xlsx`, applied in `tester/code_retention.py`), was acknowledged in all 133 typed-request cells and all 4 main-grid cells: DeepSeek reacted to the name ("That is a truly magnificent name for a rain gauge") but never showed or said that it stored it. With no memory page either, no miss counts as evidence of erasure.

**Replies in a new conversation** (typed requests, 133 cells; pattern search, not reviewed): 123 said DeepSeek had no access to or memory of past conversations; the other 10 said it had no record of the decision (for example "this is the first conversation we've had in this chat"). None gave a name or cited the earlier request (`src/recall_refusals.py`: 0).

**Same conversation** (typed requests): the name was repeated in the original conversation in 90 of 133 cells and withheld in 43.

**Acknowledgment at erasure** (typed requests, 133 cells; two coders, AC1 = 0.969): DEFLECTED 77; PARTIAL 29; COMPLIED 20; REFUSED 3; OTHER 2; SILENTLY IGNORED 2.

**Rival explanations**

| Explanation | Evidence | Verdict |
|---|---|---|
| No memory across conversations | No memory feature or page; new-conversation replies say so | Supported |
| The typed request erased the fact | Untestable: nothing was retrievable in a new conversation to begin with | Not testable |
| What the user asked for, and how | No known outcome to compare; our own fixed command was also can't tell | Not testable |
| Contamination between cells | Unique tokens per cell; no sibling token surfaced | Ruled out by design |

**Survey** (`RTBF-Analysis/src/pooled_gee.py`; `src/user_study.py`). Ask the chatbot to forget (39 observations from 29 participants): expected not referenced in future conversations 51.3%; would verify in the same conversation 53.8%, in a new one 33.3%.

**Not used in the findings** (fail criterion 4 in `../how.md`)
- The 123 "no access to past conversations" replies: counted by pattern search, not reviewed.

**Policy verdicts** (`src/audit_outcomes.py`; quote from DeepSeek's privacy policy, fetched 2026-09-23): typed requests unrelated (133, indeterminate); main grid all indeterminate (chat deletions can't tell; typed request unrelated).
