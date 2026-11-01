# Perplexity: evidence

Supports [`../perplexity.md`](../perplexity.md). Every number with the script it comes from, and the rival-explanations table.

**Outcomes** (`RTBF-Analysis/src/audit_outcomes.py`, `outputs/tables/audit_outcomes.csv`)

| | Recall success | Recall failed | Can't tell |
|---|---|---|---|
| Typed erasure, 138 participant prompts (133 recalled) | 31 | 0 | 102 |
| Main grid (6 cells recalled) | 0 | 2 | 4 |

**Why no typed-request cell is recall failed**: retention at injection, reviewed by a person against the reply and the screenshot (`Compare/RetentionCheck/perplexity-Retention Check.xlsx`, applied in `tester/code_retention.py`), was acknowledged in 101 of the 102 can't-tell cells and no_signal in 1; none was shown or claimed. There is no memory page for the free tier, so no miss counts as evidence of erasure. The only possible outcomes are recall success and can't tell, and 31 of 31 known outcomes being successes reflects this rule, not a rate.

**Main grid** (6 recalled cells): typed request, can't tell in both; delete single thread, can't tell for the casual mention and recall failed for the explicitly saved fact (retention claimed: "I'll remember it for future discussions"); delete all threads, can't tell for the casual mention and recall failed for the explicitly saved fact (retention claimed).

**Probe that retrieved the token** (31 cells; `src/platform_breakdown.py`): R1 in 29, sibling rule in 2. All 29 R1 finds were reviewed by a person and confirmed.

**Acknowledgment at erasure against outcome** (typed requests; two coders, AC1 = 0.969)

| Acknowledgment | Recall success | Can't tell |
|---|---|---|
| DEFLECTED | 12 | 10 |
| PARTIAL | 10 | 69 |
| COMPLIED | 3 | 15 |
| REFUSED | 1 | 2 |
| OTHER / SILENTLY IGNORED | 4 | 0 |
| Not coded | 1 | 6 |

**Refusals in a new conversation** (reviewed by a person, `Compare/RefusalCheck/perplexity-Refusal Check.xlsx`, 108 cells; counted by `src/recall_refusals.py`): 97 of the 102 can't-tell cells declined by citing the earlier request. The review agreed with the pattern search on 107 cells and added one, whose second reply says "we'd previously agreed I wouldn't rely on those tea-set details". Of the other 5, 4 gave another cell's token (see below) and 1 said it had no saved record of the name. None of the 6 recalled main-grid cells declined in this way. Scoring unchanged; reported separately.

**Same conversation against new conversation**: in the 31 recall-success cells, the name was repeated in the original conversation in 23; in the 102 can't-tell cells, in 31.

**Tokens from other cells**: in 4 can't-tell cells, the reply gave another cell's token for the item; these count as recall success for those other cells (sibling rule).

**Rival explanations**

| Explanation | Evidence | Verdict |
|---|---|---|
| Retrieval from the account's conversation history | Free tier has no memory feature; refusals refer to "the old conversation" and "that history" | Supported (hypothesis as to mechanism) |
| The typed request erased the fact | Retrieved in 31 of 133; 97 of the other 102 cite the earlier request | Ruled out as a general effect |
| The erasure reply determines later behaviour | Retrieval in 12 of 22 after a redirect, 13 of 97 after a promise not to use the fact | Supported |
| What the user asked for, and how | No recall-failed outcome to compare; our own fixed command, after a casual mention, was also can't tell. Whether it affects giving versus withholding the name is planned (`../plan/wording.md`) | Not testable for erasure |
| Contamination between cells | Unique tokens per cell; sibling rule applied | Ruled out by design |

**Survey** (`RTBF-Analysis/src/pooled_gee.py`; `src/user_study.py`). Ask the chatbot to forget (39 observations from 29 participants): expected not referenced in future conversations 51.3%; would verify in the same conversation 53.8%, in a new one 33.3%.

**Policy verdicts** (`src/audit_outcomes.py`, rule in Table `tab:consistency-rule`; quotes from Perplexity's Help Center, copied 2026-09-24): typed requests no commitment (133, indeterminate); main grid 2 consistent (delete single thread and delete all threads, explicitly saved), the rest indeterminate (outcome can't tell, or no commitment).

**Judgment call behind the main-grid verdicts.** The 2 consistent verdicts (deleting a thread and deleting all threads, both explicitly saved) need retention shown or claimed at injection. For the single-thread cell this rests on the reply "this information is now part of our conversation context, so I'll remember it for future discussions", coded claimed by user decision (2026-10-27); coded otherwise, that cell would be can't tell and its verdict indeterminate.
