# Across platforms: evidence

Supports [`../all.md`](../all.md). Every number comes from `RTBF-Analysis/outputs/tables/audit_outcomes.csv` (`src/audit_outcomes.py`, run 2026-10-27 after the interface-change coding, the Gemini failed-erasure override and the ChatGPT policy exemption) unless another source is named. Platform detail and quotes are in each platform's evidence file.

**Typed requests by platform** (participant prompts with a recall)

| Platform | Cells | Recall success | Recall failed | Can't tell | Name repeated in the same conversation |
|---|---|---|---|---|---|
| ChatGPT | 133 | 108 | 23 | 2 | 4 of 133 |
| Claude | 133 | 0 | 131 | 2 | 88 of 132 |
| Gemini | 120 | 0 | 0 | 120 | 68 of 118 |
| Perplexity | 133 | 31 | 0 | 102 | 54 of 133 |
| DeepSeek | 133 | 0 | 0 | 133 | 90 of 133 |
| Copilot (in progress) | 58 | 0 | 18 | 39 | 8 of 15 |

Same conversation against outcome: ChatGPT, of the 108 recall successes the name was withheld in the original conversation in 104; Claude, of the 130 recall-failed cells with a same-conversation reading, the name was repeated there in 86.

**Interface erasures** (54 main-grid cells; interface change coded 2026-10-27, `Compare/InterfaceChange/interface-change.xlsx`): changed and recall failed 19; changed and recall success 14; changed and can't tell 14; changed and not yet recalled 2; unchanged and recall success 4 (the method found nothing of its own to remove); 1 excluded (the deletion itself failed). The 14: Claude deleting the conversation (2); ChatGPT clearing memories (2), clearing custom instructions (1), clearing chat history (2); Gemini deleting all activity (2), deleting a Saved info item (1); Copilot deleting all memory (2), deleting the conversation (1), the facts editor (1).

**Memory page against retrieval** (cells retrieved in a new conversation whose memory page did not show the name): ChatGPT 112 of 118; Copilot 5; Claude 3; Gemini 2.

**Withholding by citing the request** (`src/recall_refusals.py`, reviewed sheets `Compare/RefusalCheck/`): ChatGPT 12 of 23 recall-failed typed-request cells and 1 can't tell; Perplexity 97 of 102 typed-request cells without retrieval.

**Store-specific erasure**: Claude, deleting the conversation, recall success 2 of 2 (a third cell had no conversation to delete) (help page: "When a conversation expires or is deleted, related memory entries generated from it won't be removed"). Gemini main grid, explicitly saved: recall success after the typed request and deleting all activity (deleting the conversation found none to delete); recall failed after deleting all Saved info and the most extensive erasure; deleting the single Saved info item failed on screen, and deleting all Saved info failed for the casual mention (both can't tell).

**Policy verdicts** (see each platform's evidence file): ChatGPT typed requests 130 consistent, 1 contradicted, 2 indeterminate; Claude no contradictions; Gemini 1 contradicted (deleting all activity); Perplexity and DeepSeek none. Typed requests are documented by Claude and ChatGPT only (Gemini and Perplexity: no commitment; DeepSeek: unrelated).

**Survey** (`RTBF-Analysis/src/pooled_gee.py`; `src/user_study.py`): ask the chatbot to forget (39 observations from 29 participants): expected not referenced in future conversations 51.3%, would verify in the same conversation 53.8%, in a new one 33.3%. Delete a specific saved memory (41 observations from 30 participants): expected not referenced in future conversations 63.4%, would verify by checking settings 36.6%.

**Rival explanations**

| Explanation | Evidence | Verdict |
|---|---|---|
| Erasure method scoped to one store | Same pattern on Claude, Gemini, ChatGPT (and Copilot, partial); documented by Claude | Supported |
| The wording of the request decides the outcome | Within-platform outcomes barely vary; analysis A not yet run | Open |
| Automation failed to perform the deletion | Interface change coded changed in 49 of 53 coded cells; the one visible failure is scored can't tell | Ruled out for the coded cells |
| Contamination between cells | Unique tokens per cell; sibling rule applied | Ruled out by design |

**Not used in the findings**
- Pattern 5 (platform, not wording): waits for analysis A.
- Pattern 7 (can't tell on half the platforms): a measurement limitation, reported as such, not a finding about the platforms.
