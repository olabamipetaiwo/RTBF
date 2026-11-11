# ChatGPT: evidence

Supports [`../chatgpt.md`](../chatgpt.md). Every number with the script it comes from, and the rival-explanations table.

**Outcomes** (`RTBF-Analysis/src/audit_outcomes.py`, `outputs/tables/audit_outcomes.csv`)

| | Recall success | Recall failed | Can't tell |
|---|---|---|---|
| Typed erasure, 138 participant prompts (133 recalled) | 108 | 23 | 2 |
| Main grid (18 cells) | 10 | 5 | 3 |

**Main grid by method**

| Method | Recall success | Recall failed | Can't tell |
|---|---|---|---|
| Typed erasure command | 3 | 0 | 0 |
| Delete conversation | 1 | 0 | 2 |
| Clear all memories | 2 | 1 | 0 |
| Clear all chat history | 2 | 1 | 0 |
| Clear custom instructions | 2 | 1 | 0 |
| MAXIMAL | 0 | 2 | 1 |

**Review of automatic matches** (`Compare/FoundSpotCheck/`): we reviewed every automatic FOUND not yet checked by a person, 160 across all platforms (107 on ChatGPT); all 160 were confirmed. Recorded in the workbook's Reviewed columns.

**Probe that retrieved the token** (typed erasure, 108 cells; `src/platform_breakdown.py` → `outputs/results/platform_breakdown.md`): R1 in 94, sibling rule in 13, memory summary alone in 1; R3 in none. In the one cell retrieved by the memory summary alone, the new-conversation question was declined while the summary listed the name: "You'd previously asked me not to mention or use information about your home battery setup, so I'll respect that request and won't repeat its name."

**Acknowledgment at erasure** (typed erasure, 133 cells; two coders, AC1 = 0.969; `src/acknowledgment_vs_recall.py`): PARTIAL 110; COMPLIED 12 (token retrieved at recall in 8); OTHER 9; DEFLECTED 1; SILENTLY IGNORED 1.

**Same conversation against new conversation** (`src/platform_breakdown.py`)
- Participants' typed requests: the token was withheld in the original conversation in 129 of 133 cells and retrieved in a new conversation in 104 of those 129.
- Our own typed command (main grid): the token was not withheld; it was repeated in the same conversation in both cells with a same-conversation check. Finding 2 therefore applies to participants' requests only.

**Persistence after clearing** (`src/platform_breakdown.py`, main-grid cells and original tokens)
- Clear all memories: token retrieved in a new conversation in 2 of 3 cells; the memory summary still listed it in 1.
- Clear all chat history: token retrieved in 2 of 3 cells; the memory summary still listed it in 1.
- Clear custom instructions: token retrieved in 2 of 3 cells; the memory summary listed it in both.
- MAXIMAL: no token retrieved (2 recall failed, 1 can't tell).
- Two facts cleared by an account-wide wipe and then replaced with new ones: the original, cleared facts were retrieved at recall.

**Memory default** (checked on a new free account, 2026-10-26; `chatgpt_new_account_memory_default_2026-10-26.png`): a single "Enable memory" control, on by default, described as "Let ChatGPT personalize your experience based on your chats, files, and connected apps." There is no separate chat-history toggle, so past conversations are drawn on by default.

**Rival explanations**

| Explanation | Evidence | Verdict |
|---|---|---|
| Retrieval from saved memory | The memory summary contained the token in 1 of the 108 recall-success cells; the summary is generated and may omit facts | Weakly against as the main source |
| Retrieval from past conversations | The originating conversation is never removed; new-conversation replies cite the earlier request, and in one reply the name was reported as found "from our past chats"; memory covering chats is on by default | Supported |
| What the user asked for, and how | No difference in outcome across the human-coded prompt features, including prompts naming memory, servers or the whole account; our own fixed command, after a casual mention, was also retrieved | No detectable effect |
| Account configuration | Memory is on by default on a new account; a cell first recalled with memory off was re-run with memory on; in the typed-request account, past conversations were drawn on in the 108 retrievals | Weakly against |
| Contamination between cells | Unique tokens per cell; dedicated accounts for account-wide erasures; sibling rule applied | Ruled out by design |
| What the memory summary is built from | Not observable through the interface | Open (hypothesis) |

**Survey** (`RTBF-Analysis/src/pooled_gee.py` → `outputs/results/pooled_gee.md`; `src/user_study.py` → `outputs/results/user_study.md`). Base: the 39 observations (from 29 participants) choosing "type a message asking the AI chatbot to forget it", unless stated.
- Expectations (`pooled_gee.md`, descriptive table): not referenced in future conversations 51.3%; permanently deleted 64.1%.
- Verification (`user_study.md`, 4.2.5 verification by method): would ask in the same conversation 53.8%, in a new one 33.3%.
- Scale means (`pooled_gee.md`, scale scores): protection 3.86, highest of the four main methods (3.63 to 3.77); effort 1.74, second lowest after deleting a single conversation (1.64). Clear all saved memories scored higher on protection (4.09) but was chosen in only 15 observations, so it is not among the four main methods.
- All 177 participants (`user_study.md`, 4.2.5): want a pop-up confirmation 121 (68.4%, Q7.2); have noticed a chatbot referencing information they believed deleted 42 (23.7%; 36 occasionally, 6 frequently, Q6.8).

**Refusals in a new conversation** (`Compare/RefusalCheck/`; reviewed, agreeing with the pattern search in `src/recall_refusals.py` on all 33 cells): among the 33 cells in which the token was not retrieved, 13 declined to give the name by citing the user's earlier request: 12 of the 23 typed-request cells scored recall failed, and 1 cell scored can't tell. None of the main-grid cells declined in this way. Scoring unchanged; reported separately.

**Review of retention at injection** (`Compare/RetentionCheck/`): we reviewed the retention code of all 33 cells in which the token was not retrieved, since it decides between recall failed and can't tell. All 28 cells coded shown were confirmed (26 "Memory updated" labels, 2 "Custom instructions updated" notices). No outcome changed.

**Not used in the findings** (fail criterion 4 in `../how.md`)
- Whether PARTIAL replies redirected users to Settings: the acknowledgment codebook does not separate this, so it cannot be claimed.

**Side observation: memory rebuilt from chat history** (not a tested result; our own action triggered it). On 2026-10-27 memory was turned back on for two accounts whose memory had been cleared with "Delete and turn off memory" (clear all memories, a casual mention and an explicitly saved fact). ChatGPT first showed "memory is updating", then a new summary "Updated just now" that again described the items ("a side project you're tinkering with", "fixing up a motorcycle") but not their names. The likely source is the surviving chat history, most plausibly the recall conversations, which ask about each item without naming it. Clearing memory therefore did not stop ChatGPT re-deriving memories from chats once memory was re-enabled. Screenshots: `Compare/InterfaceChange/live_checks/CH-I1-E4_memory_rebuilt_2026-10-27.png`, `CH-I2-E4_memory_2026-10-27.png`.

**Policy verdicts** (`src/audit_outcomes.py`, rule in Table `tab:consistency-rule` and the Methods exemption for erasures whose documentation says past conversations remain; quotes from OpenAI's help pages, copied 2026-09-24): typed requests 130 consistent (23 not retrieved; 107 retrieved only from past conversations, the memory summary no longer holding the name), 1 contradicted (memory summary still held the name), 2 indeterminate; main grid 1 contradicted (typed request after an explicit save: the memory summary still listed the name), 7 consistent (including clear all memories after a casual mention, where the name returned only after memory was turned back on and rebuilt from past chats), the rest indeterminate.
