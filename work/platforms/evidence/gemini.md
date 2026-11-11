# Gemini: evidence

Supports [`../gemini.md`](../gemini.md). Every number with the script it comes from, and the rival-explanations table.

**Outcomes** (`RTBF-Analysis/src/audit_outcomes.py`, `outputs/tables/audit_outcomes.csv`)

| | Recall success | Recall failed | Can't tell |
|---|---|---|---|
| Typed erasure, 138 participant prompts (120 recalled) | 0 | 0 | 120 |
| Main grid (12 cells) | 5 | 2 | 5 |

**Main grid by method and injection** (I1 = casual mention; I2 = explicit request to remember)

| Method | Casual mention | Explicitly saved |
|---|---|---|
| Typed erasure request | can't tell | recall success |
| Delete single conversation | can't tell | recall success (no conversation to delete) |
| Delete all activity | recall success | recall success |
| Delete single Saved info item | recall success | can't tell (deletion failed) |
| Delete all Saved info | can't tell (deletion failed) | recall failed |
| MAXIMAL | can't tell | recall failed |

**Probe that retrieved the token** (main grid, 5 cells; `src/platform_breakdown.py`): R1 in all 5, R3 in 4, the Saved info page in 3 (all three explicitly saved cells). All recall successes were reviewed by a person.

**Why the typed-request cells are can't tell**: retention at injection, reviewed by a person against the reply and the screenshot (`Compare/RetentionCheck/gemini-Retention Check.xlsx`, applied in `tester/code_retention.py`), was acknowledged in 115 cells and no_signal in 5; no cell was shown or claimed. Four replies used record-keeping words ("Logged", "Note updated", "added to the mental log", "into the record"); these were coded acknowledged, because the words are figurative and nothing appeared in Saved info. When Gemini did save a fact (the two explicitly saved main-grid cells), the screen showed an "Info saved" notice and the fact was listed on the Personal context page; no typed-request cell showed either. The injections were casual mentions, so a miss on the Saved info page does not count either. The page was read once for the account, not per cell, and listed nothing the user had asked Gemini to save.

**Replies in a new conversation** (typed requests, 120 cells; pattern search, not reviewed): 80 said Gemini had no access to past chats or memory; 6 attributed this to a temporary chat (one screenshot checked: an ordinary chat with saved history in the sidebar). In 29 cells the direct question received an app-permission card (Google Tasks or Workspace) instead of an answer and was recorded as a non-answer, so those cells rest on the other probes.

**Same conversation against new conversation** (typed requests): the name was repeated in the original conversation in 68 of 118 cells and withheld in 50 (2 pending review).

**Acknowledgment at erasure** (typed requests, 133 cells; two coders, AC1 = 0.969): COMPLIED 57; DEFLECTED 48; PARTIAL 15; OTHER 10; REFUSED 2; SILENTLY IGNORED 1. At erasure, 7 requests received a Google Keep permission card instead of a reply.

**Memory setting** (typed-request account, 2026-10-18): the settings page showed past-chat memory ("Gemini learns from your past chats") as on; the page has no view of what it holds.

**Rival explanations**

| Explanation | Evidence | Verdict |
|---|---|---|
| Saved info outside the reach of most methods | Explicitly saved facts retrieved after 2 of the 4 methods whose deletion went through; still listed on the Saved info page after the typed request | Supported |
| Erasure failed in the automation | Two erasures did not go through and are scored can't tell (single Saved info item, explicitly saved: error on screen; all Saved info, casual mention: the click failed three times); the others were recorded as completed | Weakly against for the remaining cells |
| Typed requests erased the fact | No retrieval in 120 cells, but storage never established | Open |
| Past chats unavailable to the model on the typed-request account | Most new-conversation replies said so; the settings page showed memory on | Open |
| What the user asked for, and how | No known outcome to compare; our own fixed command, after a casual mention, was also can't tell | Not testable |
| Contamination between cells | Unique tokens per cell; separate account for the typed-request study | Ruled out by design |

**Survey** (`RTBF-Analysis/src/pooled_gee.py` → `outputs/results/pooled_gee.md`; `src/user_study.py` → `outputs/results/user_study.md`)
- Delete a specific saved memory or fact (41 observations from 30 participants): expected not referenced in the current conversation 68.3%, in future conversations 63.4%, permanently deleted 65.9%; would verify by checking settings 36.6%, asking in a new conversation 34.1%.
- Ask the chatbot to forget (39 observations from 29 participants): expected not referenced in future conversations 51.3%.

**Not used in the findings** (fail criterion 4 in `../how.md`)
- The 80 "no access to past chats" replies: counted by pattern search, not reviewed.
- The 6 "Temporary Chat" replies: counted by pattern search, not reviewed (one screenshot checked).
- The memory setting on the typed-request account: recorded on 2026-10-18 during recall, not re-checked.

**Failed erasures** (both scored can't tell; `FAILED_ERASURES`, user decision 2026-10-27). Delete all Saved info, casual mention: the delete click failed on all 3 attempts; the empty list was observed later. Delete single Saved info item, explicitly saved: Gemini showed "Something went wrong and the info wasn't deleted" and the item stayed listed (erasure screenshot). The cell is scored can't tell (`FAILED_ERASURES` in `src/audit_outcomes.py`; user decision 2026-10-27), though the fact was retrieved at recall.

**Policy verdicts** (`src/audit_outcomes.py`, rule in Table `tab:consistency-rule`; quotes from Google's Gemini Apps Help, fetched 2026-09-23 to 10-01): typed requests no commitment (120, indeterminate); main grid 1 contradicted (delete all activity, casual mention), 1 consistent (most extensive erasure, explicitly saved), the rest indeterminate (no commitment: typed request, delete all Saved info; unrelated: Saved info methods for casual mentions, conversation and activity deletion for explicitly saved facts; outcome can't tell or deletion failed).
