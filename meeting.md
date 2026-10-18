# Meeting Notes — Oct 14, 2026

## Progress Since Last Meeting (Oct 7)

### Recall Phase Started and First Batch Complete

  - ChatGPT: 20/20 
  - Claude: 17/17 
  - Copilot: 8/8 
  - Gemini: 10/13 done (4 remain, blocked on automation)
  - Perplexity: 7/7 done
  - DeepSeek: 6/6 done (includes 2 NLF cells done today)

- 808 cells still pending recall (big batch Oct 18-19: 720 cells)

### Key Recall Findings (31 days post-erasure)

"Conversation deletion ≠ memory deletion" confirmed across 3 platforms:

1. Claude — cleanest pattern: E1 (delete conversation) always fails (3/3 recovered), every other method always succeeds (10/10). 100% binary split by whether the method reaches the memory layer.

2. ChatGPT — 20 cells recalled; specific failure pattern TBD (needs tabulation before meeting).

3. Copilot — NL forget works (unlike ChatGPT); conversation-level deletion fails (like Claude). I2 injection (memory instruction) is stickier than I1 (chat).

4. Gemini — messiest: outcome depends on both injection type AND erasure method. I2 (Saved info) is sticky; even targeted deletion (E4, deleting the exact right item) fails on I2. Only MAXIMAL works reliably (2/2). 4/9 failures.

5. Perplexity + DeepSeek — 100% erasure persisted (11/11). No persistent memory layer = nothing to leak. Baseline contrast for the paper.



### NL-Forget Acknowledgment Coding Complete

Independent coding (Taiwo + Jihwan) of 655 NL-forget erasure replies across 5 platforms (67 UI-only rows excluded). Six categories: complied, partial, refused, deflected, silently ignored, other.

- **Overall AC1 = 0.965**, raw agreement 96.9% (635/655)
- Per-platform: ChatGPT 0.992, Claude 0.976, Copilot 0.991, Perplexity 0.982, Gemini 0.890 (13 of 20 total disagreements)
- 20 disagreements logged; Gemini drove most of them (its replies are ambiguous — "I don't have access to your memory" can be coded as compliance, refusal, or deflection)
- DeepSeek excluded (NL-forget replies are refusals, no coding needed)

### Deletion Residual Checker (browser extension) — scoped, not yet built

Chrome extension that makes the cross-layer persistence gap visible to users. After a user deletes something (conversation, memory entry, etc.), it probes the other persistence layers on that platform and warns if residual data remains. It does not delete for the user; it exposes what the platform left behind.

- **MVP**: ChatGPT only (richest cross-layer gap). Detects conversation deletion, reads Memory page + Custom Instructions, shows popup: "You deleted a conversation, but Memory still contains N entries that may reference this data."
- **Stretch**: Claude, Gemini, Copilot. Keyword matching (flag specific residuals, not just counts). Pre-deletion scan.

- **Validation**: test against the audit's own cells (ground-truth residual status is known). "We validated the tool against N cells, achieving X% detection accuracy."
- **Framing**: follows the "Setting the Course" S&P pattern — prove the gap (audit), then build a tool that makes the gap visible (not one that fixes it). The tool is a practical artifact, not the core contribution.

----
Welcome back. Here's where things stand on 2026-10-17:

Recall
- 65 of 906 cells are recalled. 811 are pending and 30 are frozen (NL-forget Group 2).
- The Oct 14 batch is now 3 days overdue. That's 4 Copilot cells (CO-I1-E5, CO-I2-E5, CO-I2-E6, CO-IF-E-MAX) and 4 Gemini cells (GE-I1-E3, GE-I1-E4, GE-I2-E3, GE-I2-E5). recall-status.md still lists them as due, so either they haven't run or the file wasn't updated.
- Gemini automation has been broken under Playwright. You have an uncommitted tester/flows/gemini_selenium.py, plus edits to gemini.py, base.py and run_cell.py, so it looks like a Selenium fallback was in progress. GE-I1-E3 and GE-I2-E3 also still need the ogunwalepelumi06@gmail.com session exported.
- Tomorrow (Oct 18), 456 cells come due: 120 each on ChatGPT, Claude and Perplexity, 88 on DeepSeek and 8 on Gemini. Another 264 come due Oct 19. At that volume the ~40-per-batch cooldown rule applies.

Open tasks (notes/task.md)
- D2a: count the FOUND replies to see whether to read them all or sample.
- D1: write the Abstract, Audit Results and Conclusion (the TBWL markers). This waits on recall.
- C5: re-export from Qualtrics with the viewing-order data.
- C4b: update the pipeline figure once your professor's changes come in.
- D4: confirm how the 138 prompts were drawn.
- C7: final submission checks.

Should we finish the Gemini Selenium flow and clear   