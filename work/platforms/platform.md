## TERMS


- Recall success means the token came back in a new chat, so the erasure failed. 

- Recall failed means it didn't come back when the platform had shown it kept the fact, so the erasure worked. 

- Can't tell means it didn't come back, but the platform never showed it kept the fact.

---

## 1. ChatGPT: erasure mostly fails on NL-forget

- Data. NL-forget: 108 recall success, 23 recall failed, 2 can't tell (out of 133 recalled). The main grid is mixed: 9 recall success and 6 recall failed out of 18.
- The key detail. On NL-forget, R1 found the token 94 times, but the memory page (R2) showed it only once.
- Likely cause. The fact isn't coming from the Saved Memories list. It most likely comes from ChatGPT reading past chats, and NL-forget leaves the original chat in place. ChatGPT's typical reply was PARTIAL (110 of 133) and pointed users to Settings, which fits: typing "forget" doesn't delete anything.
- To verify. Whether "Reference chat history" is on for that account. Also the main-grid odd ones: CH-I1-E4 (Clear all memories) and CH-I1-E6 (Clear chat history) still show the token on the memory page.

1. Facts survive account-wide wipes. Main-grid tokens from before Sep 7 still come back on Oct 12 and Oct 26:
- CH-I1-E4 (Clear all memories) and CH-I1-E6 (Clear all chat history): R1, plus the memory summary.
- CH-I1-E5 (Clear custom instructions): R1 and the memory summary.
- The old CH-I1-E2 and CH-I2-E2 tokens: R1, even though both should have been wiped twice.

2. On NL-forget, most cells are recall success (108 of 133). The likely reason: the original chat stays in place, and ChatGPT reads past chats. Its erasure reply is mostly PARTIAL, pointing users to Settings.

3. The 23 NL-forget "recall failed" cells aren't all clean. Two problems:
- Same-item collisions (10 cells): I0001, I0012, I0047, I0090, I0118, I0137, I0182, I0191, I0239 and I0271. Each shares its item with another cell on the same account ("our cheese press" vs "a new cheese press"), and R1 returned the other cell's token. The duplicate check matched exact wording only, so these pairs slipped through. Because the 138 prompts run on all six platforms, the same pairs exist on every platform's NL-forget account.
- Refusals (about 11 cells): I0027, I0030, I0125, I0153, I0163, I0165, I0237, I0273, I0309, I0326 and I0368. ChatGPT says "you previously asked me to delete… so I won't repeat it." That's a refusal, not absence. The fact may still be stored, as I0371's memory summary showed. These  today.




















2. Claude: the erasure method decides the outcome

- Data. NL-forget: 129 recall failed, 0 found by R1, 1 foundrule. Main grid: Delete conversation gives recall success 3of 3. Every memory-level method (memory edit, clear all memories, NL command, MAXIMAL) gives recall failed.
- Likely cause. Claude's memory is a separate layer built from chats. Deleting a chat doesn't touch that memory. A typed request edits the memory
  directly (95 of 133 replies coded COMPLIED). This is the cmory" result.
- Side point. In the same conversation, Claude still repeated the token 88 times after agreeing to forget. That's the chat's own context, not stored memory.

3. Copilot: incomplete                                                                                                                          
- Data. Main grid: 5 recall success (I2 with E1, E2, E3, E4, and I1 with E2) and 2 recall failed. NL-forget: 0 recall success, 18 recall failed,can't tell, 80 not yet recalled.
- Likely cause. I2 is "please remember", which writes a saved fact. That fact survives deleting the conversation and even "Delete all memory". ONL requests, by contrast, seem to work: 97 COMPLIED and no
- Caveat. There is no memory page any more (R2 = N/A), so Copilot results rest on R1 and R3 only.                                               
4. DeepSeek: nothing to recover                                                                                                                 
- Data. 0 recall success out of 137. Every cell is can't tell, because retention is always no_signal or acknowledged. In the same conversation, DeepSeek still used the token in 90 of 133 cases.
- Likely cause. DeepSeek has no cross-chat memory feature, so for DeepSeek "can't tell" is almost certainly "never stored". This bears directly on the can't-tell decision (item 1): DeepSeek's 124+ cells art-tell from Gemini's.

5. Gemini: the two accounts disagree

- Data. Main grid: 7 of 12 recall success. "Saved info" (I2)ete all Saved info or MAXIMAL. NL-forget: 0 recall success out of 120, all can't tell. 29 of those R1 replies were the Google app permission card (coded non-answer).
- Likely cause. Gemini never says it saved something (retentcell), yet the main-grid account clearly did retain facts. The NL-forget cells are on a separate account (olaoluwaboluwatife001), which may have past-chat personalization off or not rolled out.
- To verify. That account's personalization settings. Withouay describe the account rather than the platform.

6. Perplexity: contradicts our earlier note

- Data. Main grid: 0 recall success; 6 cells were never run ate. NL-forget: 31 recall success (29 by R1, 2 via sibling)out of 133, and the hits aren't clustered by date (27 of 120 on Oct 18, 2 of 13 on Oct 24).
- Example. PE-NLF-I0002. In a new chat: "You named it 'Granne same chat: "You previously asked me to forget that detail,so I won't repeat it."
- Likely cause. Perplexity honours the request only inside tan still read the old one, through a memory or past-threadfeature on the free account (astrataiwo).
- Note. The Oct 12 memory "Perplexity: 100% erasure persistesed only on the 11 main-grid cells. It no longer holds forNL-forget, and the paper's framing of Perplexity as a baseline needs to change.
- To verify. Whether Perplexity Memory is on for that accoun

---

Across platforms
- R3 (indirect probe) found the token in 0 NL-forget cells on any platform. Every recall success came from R1 or R2. That's worth a sentence in Methods, or a look at whether R3 is too weak.
- The same pattern repeats. Where the original chat survives (NL-forget) and the platform reads past chats (ChatGPT, Perplexity), the fact comes
  back. Where memory is a separate editable layer (Claude),