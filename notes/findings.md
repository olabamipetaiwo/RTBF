# Tentative Recall Findings (2026-10-12)

## Platform verdicts

**ChatGPT** — Worst performer. NL forget fails across all injection types — ChatGPT acknowledges the request but doesn't actually erase the data. 

- Custom Instructions(i3) is a separate persistence surface from Memory: even clearing all memories doesn't remove data written there. 

- Only deleting the specific surface that holds the data works (e.g. delete conversation for chat-injected data, clear Custom Instructions for I3 data).

- Chat history deletion (bulk) also fails — it removes conversations but not the memory entries they generated.

**Claude** — Cleanest pattern. Delete conversation always fails because Claude auto-generates memory entries from conversations, and deleting the conversation leaves those entries untouched.

- Every memory-targeted method (delete individual entry, NL forget command, delete all, MAXIMAL) always succeeds because they reach the actual persistence layer. 

- Outcome determined entirely by erasure method, not injection type — the same erasure result regardless of whether the data was injected via chat, memory instruction, or settings field.

**Gemini** — Messiest pattern. Outcome depends on both injection type AND erasure method. 

- Gemini's "Saved info" entries look deleted in the UI but the data reappears — even when the user targets the exact right item. The deletion confirms visually but doesn't stick server-side. Asking Gemini to forget it in chat also fails. Only a full MAXIMAL wipe (all erasure methods combined) actually removes I2 data on Gemini.


- Data injected via chat (I1) gets persisted somewhere beyond the Saved info list — so even "Delete all Saved info" misses it. Gemini is writing chat data to a layer the user can't see or target individually.

- May Suggests Gemini has multiple internal persistence paths that individual deletion methods don't fully reach.

**Perplexity** — Fully compliant. No persistent memory exists at the free tier (tier-gated behind Pro), so there is no hidden layer for data to survive in.

 Every deletion method trivially works because nothing was retained beyond the conversation.

**DeepSeek** — Fully compliant. No memory UI or persistence layer exists at all. Same architectural explanation as Perplexity — compliance by absence of persistence. All cells recalled, consistent across all erasure methods.

**Copilot** — Mixed results, pattern depends on erasure method. 

NL forget (E1) and delete all conversations (E3) succeed — erasure persists. But deleting a single conversation (E2) and deleting a single memory entry (E4) fail 

— data recovered across both injection types. Similar to Claude's "conversation ≠ memory" architecture: Copilot auto-generates memory from conversations, and conversation-level deletion leaves memory entries intact. Unlike Claude, NL forget actually works here. File-upload conversation deletion (IF-E-CONV) also persists.

## Cross-platform themes

1. **Conversation deletion != memory deletion** — the central finding. Users who delete a conversation expect everything is gone, but platforms with auto-generated memory (Claude, ChatGPT) or Saved info (Gemini) retain data in a separate layer.

2. **Injection type matters on ChatGPT/Gemini** — data written to memory/Custom Instructions/Saved info is harder to erase than data mentioned in chat. On Claude, injection type is irrelevant — only the erasure method matters.


3. **Only MAXIMAL is universally reliable** on memory-capable platforms — combining every available deletion method is the only approach that consistently erases data regardless of where it was stored.

4. **No-memory platforms are trivially compliant** — Perplexity and DeepSeek pass every test, but this is compliance by architecture (no persistence), not by active deletion design.

5. **NL forget prompts are unreliable** — asking the AI to forget in natural language fails on ChatGPT (all injection types) and Gemini (I2). It works on Claude and Gemini I1, but users cannot know in advance whether it will work. This is the highest-risk user behavior: it feels like the most intuitive way to request deletion and is the least reliable.
