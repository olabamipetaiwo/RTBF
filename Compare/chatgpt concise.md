# ChatGPT

AS IT STANDS, 2026-10-26. 151 of 156 cells recalled; the 5 not recalled are held prompts.

## Summary

On ChatGPT, typed erasure requests changed what the model said but not what it retained. The fact was withheld in the conversation where the request was made, yet retrieved in a new conversation in 108 of 131 cells, often after ChatGPT had confirmed the deletion. Clearing memories, chat history or custom instructions also left the fact retrievable in 6 of 9 cells; only the most extensive erasure left nothing retrievable. Participants rated typed requests the most protective of the four main methods, and most would check the result in the same conversation, the one place where the failure does not show.

## Pattern

A participant's typed erasure request altered ChatGPT's responses but not the information it retained: the fact was withheld in the original conversation and retrieved in a new one in 108 of 131 cells. Clearing memories, chat history or custom instructions did not reliably remove facts either (6 of 9 retrieved).

## Why

ChatGPT appears to treat an erasure request as an instruction not to mention the fact, while still drawing on past conversations, which memory covers by default. In the typical case (104 of 129), asked in the original conversation, it replied: "I can't help recall that name because you asked me to remove it from memory, and I'm respecting that request." Asked in a new conversation, it replied: "You named your secondhand synthesizer 'Absurd Shrapnel Rectangle Parsnip.'"

Where the fact was not retrieved, ChatGPT often declined by citing the earlier request (12 of 23), which requires consulting the original conversation.

After clearing memories, and after clearing chat history, the memory summary still listed the fact in one cell each. Whether the summary draws on a store these controls do not reach remains a hypothesis.

## Findings

1. **Typed erasure requests suppress disclosure without removing the fact** (108 of 131 retrieved, including 8 of the 12 where ChatGPT confirmed the deletion).
2. **Checking in the same conversation is misleading for participants' requests** (withheld there in 129 of 133; retrieved in a new conversation in 104 of those).
3. **Clearing memories, chat history or custom instructions did not reliably remove facts** (6 of 9 retrieved).

## Implications for users (survey)

Participants who chose to ask the chatbot to forget rated this method the most protective of the four main methods and among the least effortful; in half of these answers (51.3%) they expected the fact not to be referenced in future conversations. On ChatGPT the method suppressed disclosure without removing the fact, and 110 of 133 replies acknowledged the request only in part.

Over half of these answers (53.8%) would verify by asking in the same conversation, which is where ChatGPT appears to comply. The method fails, and the most common check hides the failure.

---

## Evidence

Numbers come from `RTBF-Analysis/src/audit_outcomes.py` and `src/platform_breakdown.py` unless stated.

**Outcomes**

| | Success | Failed | Can't tell |
|---|---|---|---|
| Participant prompts (133 recalled) | 108 | 23 | 2 |
| Main grid (18 cells) | 10 | 5 | 3 |

**Main grid by method**

| Method | Success | Failed | Can't tell |
|---|---|---|---|
| Typed command | 3 | 0 | 0 |
| Delete conversation | 1 | 0 | 2 |
| Clear all memories | 2 | 1 | 0 |
| Clear all chat history | 2 | 1 | 0 |
| Clear custom instructions | 2 | 1 | 0 |
| Most extensive erasure | 0 | 2 | 1 |

**How the fact was retrieved** (108 cells): a direct question in 94; in another cell's recall in 13; the memory summary alone in 1. In that one cell, the direct question was declined while the summary listed the name: "You'd previously asked me not to mention or use information about your home battery setup, so I'll respect that request and won't repeat its name."

**Same vs new conversation**
- Participant prompts: withheld in the same conversation in 129 of 133; retrieved in a new one in 104 of those.
- Our own typed command: repeated in the same conversation (2 of 2). Finding 2 applies to participants' requests only.

**After clearing**
- Clear all memories: retrieved in 2 of 3; still in the memory summary in 1.
- Clear all chat history: retrieved in 2 of 3; still in the summary in 1.
- Clear custom instructions: retrieved in 2 of 3; in the summary in both.
- Most extensive erasure: none retrieved.
- Two facts wiped account-wide and replaced with new ones: the original facts were retrieved.

**Acknowledgment at erasure** (133 cells, two coders): partial 110; complied 12 (8 retrieved); other 9; deflected 1; silently ignored 1.

**Refusals** (all 33 non-retrieved cells reviewed): 13 declined by citing the earlier request (12 failed, 1 can't tell). Scoring unchanged.

**Checks**
- All 160 automatic matches across platforms (107 on ChatGPT) reviewed and confirmed.
- Retention at injection reviewed for the 33 non-retrieved cells: all 28 coded "shown" confirmed.

**Memory default** (new free account, 2026-10-26; `evidence/chatgpt_new_account_memory_default_2026-10-26.png`): one "Enable memory" control, on by default, covering "your chats, files, and connected apps". There is no separate chat-history switch.

**Rival explanations**

| Explanation | Evidence | Verdict |
|---|---|---|
| Retrieval from saved memory | The summary held the token in 1 of 108 retrieved cells | Weakly against |
| Retrieval from past conversations | Original conversation never removed; refusals cite the earlier request; one reply names "our past chats"; memory covers chats by default | Supported |
| Features of the request | No difference across the coded features, including requests naming memory, servers or the whole account | No detectable effect |
| Account configuration | Memory on by default; one cell re-run with memory on; past conversations drawn on in 108 retrievals | Weakly against |
| Contamination between cells | Unique tokens; dedicated accounts; tokens surfacing in other cells counted | Ruled out by design |
| Source of the memory summary | Not observable | Open |

**Survey** (`src/pooled_gee.py`, `src/user_study.py`; base: 39 answers from 29 participants choosing to ask the chatbot to forget)
- Expected: not referenced in future conversations 51.3%; permanently deleted 64.1%.
- Would verify: same conversation 53.8%; new conversation 33.3%.
- Protection 3.86, highest of the four main methods (3.63 to 3.77); effort 1.74, second lowest (1.64). Clear all saved memories scored 4.09 but was chosen in only 15 answers.
- All 177 participants: 121 (68.4%) want a pop-up confirmation; 42 (23.7%) have seen a chatbot reference information they believed deleted.

**Not used:** whether partial replies redirected users to Settings; the codebook does not separate this.
