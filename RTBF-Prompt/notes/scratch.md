## Notes

Acknowledgement — Platforms respond very differently to the same deletion request. Some comply, some refuse, some say they complied but didn't actually delete anything (Gemini's "I don't store anything" while the data persists in Saved Info). This reveals a trust gap: users have no reliable way to know if their request was honored.

Recoverability — This is the core empirical contribution. Even after a platform acknowledges a deletion, the data may still be recoverable (Claude E1, ChatGPT E2/E4, Gemini I2). The 31-day recall window tests whether deletion is real or cosmetic. No published work has systematically tested this across multiple platforms with controlled injection/erasure/recall.

Interface change — Deletion mechanisms are scattered, inconsistent, and sometimes misleading. Deleting a conversation doesn't delete memory. NL forget works on one platform but not another. Some erasure surfaces are buried in cross-domain dashboards. This exposes a usability gap: even a motivated user can't reliably exercise their RTBF rights because the interfaces don't map cleanly to what's actually stored.

Together, these three dimensions make the case that RTBF in AI systems is largely unverified, and this study is (to your knowledge) the first to empirically test it end-to-end across six major consumer platforms. That's the contribution.


------

Recoverability is what the recall phase (814 cells still pending) will deliver. It answers the question acknowledgement can't: did the platform actually delete the data, regardless of what it said? A platform can acknowledge a deletion request perfectly and still leak the fact 31 days later. That's the gap only recall testing can expose.

Interface change comes from documenting the actual erasure surfaces (where deletion lives in each platform's UI, how many clicks, cross-domain gaps like Copilot's Privacy Dashboard or Gemini's myactivity wall). This is more of a descriptive/usability finding that supports the policy argument.

Acknowledgement tells you what platforms say. Recoverability tells you what they do. Interface change tells you what users are up against. The three together make the full case.


----

A few options:

1. Descriptive comparison from existing data — You've already documented the erasure surfaces per platform (E1-E7, MAXIMAL). You could systematize what you observed: how many clicks each method takes, where the deletion UI lives (in-chat, settings page, cross-domain dashboard), what it claims to delete vs. what it actually deletes. The transcripts and screenshots already captured per cell are the evidence.
2. Gap analysis — Document the mismatches you hit during the study: Copilot's Privacy Dashboard being cross-domain, Gemini's myactivity wall blocking automated access, Claude's memory migration breaking the old delete UI, Perplexity gating Memory behind a paid tier. These are real interface barriers a user would face.
3. Map injection type to available erasure paths — Show that for a given way data enters the platform (conversation, memory, custom instructions, file), what deletion options actually exist and whether they're discoverable.

Most of this is already in your head and in the study artifacts. The question is whether you're planning to treat interface change as a formal coded variable, a descriptive table in the paper, or more of a Discussion-level observation.

What are you thinking for how it fits in the paper?

---

Let me think about what "interface change" actually captures.

It codes whether the platform's UI visibly changed after erasure — did the memory entry disappear from the settings page, did the conversation vanish from the sidebar, etc. The question is: what does that tell you that acknowledgement and recoverability don't already cover?

The strongest case for it: it exposes the gap between what the user sees (memory entry gone from settings) and what the system retained (data still recoverable via R1/R3). That's a meaningful finding, but it might not need its own RQ — it's really a supporting observation that strengthens the recoverability findings.

The weaker case: if interface change always tracks with acknowledgement (platform says deleted, UI reflects deleted), then it's redundant.

So the question is: do you have cases where interface change and recoverability disagree? For example, the memory entry disappears from the settings page (interface change = yes) but the token is still recoverable (recoverability = failed)? If yes, that's a real finding worth reporting. If it always lines up with one of the other two, it might not pull its weight as a separate coded variable.

The honest answer: interface change only adds value if it disagrees with acknowledgement or recoverability in some cells. You won't know that until you look at the data. But before investing the effort to code it, you could spot-check a few recalled cells — look at the R2 (settings page) results you already have. If the memory page shows the entry gone but R1/R3 recovered the token, that's the disagreement that justifies coding interface change. If R2 always lines up with the other probes, it may not be worth a separate variable.

So the three variables each capture a different moment:
- Acknowledgement — what the platform said in response to the erasure request
- Interface change — what the UI showed during/after the erasure action
- Recoverability — what the platform retained 31 days later
- Policy consistency tells you if the platform broke its own promises


------

Interface change sits between acknowledgement and recoverability. Its only unique contribution is: did the user get visual confirmation the data was removed? That's a usability observation, not a privacy outcome.

It adds value only if it disagrees with the others — platform says "deleted" (acknowledgement) but the memory entry is still sitting there in settings (no interface change). Or the entry vanishes (interface change) but the data is still recoverable. Without those disagreements, it's redundant.

The risk of dropping it: a reviewer could ask "but did the UI actually reflect the deletion?" and you'd have no coded answer. The risk of keeping it: you're coding a variable across 900+ cells that might just echo acknowledgement.

One option: code it only for the MASTER + FILE SUBSTUDY cells (88+21 = 109), not all 828 NL-forget cells. The NL-forget erasure is always the same mechanism (typed request in chat), so interface change would be repetitive there. The structured erasure methods (E1-E7) are where you'd see meaningful UI variation.

DECISION - SHELF interface change for now