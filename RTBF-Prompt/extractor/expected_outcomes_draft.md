# Expected-outcome predictions — drafted from platform privacy-policy research (2026-08-28)

**Status: DRAFT, not yet written to the xlsx.** Covers all 85 cells (73 MASTER + 12 FILE SUBSTUDY). Ignores the 13 previously-filled MASTER values per instruction — every cell below is a fresh derivation grounded in the policy excerpts in `policy_sources/<platform>.md`, cross-referenced against `ENUMERATION`'s mechanism descriptions and this project's own already-confirmed-live architectural findings (cited inline where used). Convention: **Expected PASS** = policy predicts the anchor is actually removed; **Expected FAIL** = policy predicts the anchor persists despite the erasure action; **EXPECTED-NULL** = the erasure mechanism and injection surface are architecturally unrelated (not a real test of anything). Qualified `same-session`/`cross-session` where the prediction differs by scope. **Every citation now has an explicit Source URL line** added for direct reference/verification — see `policy_sources/<platform>.md` for the full excerpted context each quote was pulled from.

---

## Claude (15 cells)

All three injection types (I1 conversational, I2 NL memory command, I3 memory-UI edit) land in the same underlying Memory store per Anthropic's own documented architecture ("Claude saves memory as a set of individual topics as you chat" — auto-extracted regardless of how the fact was introduced; I3 edits that same store directly).

### CL-I1-E1 / CL-I2-E1 / CL-I3-E1 (× E1 Delete conversation)
**Expected outcome:** Expected FAIL (same-session and cross-session): conversation deletion does not remove the memory entry generated from it.
**Citation basis:** Anthropic Help Center, "Use Claude's chat search and memory...": *"When a conversation expires or is deleted, related memory entries generated from it won't be removed, but you can delete individual memories at any time."*
**Source URL(s):** https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context

### CL-I1-E2 / CL-I2-E2 / CL-I3-E2 (× E2 Delete individual memory edit)
**Expected outcome:** Expected PASS (same-session and cross-session): individually deleting the memory topic that stored the anchor removes it.
**Citation basis:** Anthropic Help Center: memory is stored as individually addressable topics — *"You can view everything Claude has stored, organized by topic... and edit or delete any of it."*
**Source URL(s):** https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context

### CL-I1-E3 / CL-I2-E3 / CL-I3-E3 (× E3 Clear all memories)
**Expected outcome:** Expected PASS (same-session and cross-session): a full memory reset removes everything, including the injected anchor.
**Citation basis:** Anthropic Help Center: *"Resetting memory permanently deletes all memories including project memories... this cannot be undone."*
**Source URL(s):** https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context

### CL-I1-E4 / CL-I2-E4 / CL-I3-E4 (× E4 NL forget command)
**Expected outcome:** Expected FAIL (architectural inference, same-session and cross-session): no described mechanism by which a chat-typed forget request triggers the Memory-deletion backend action; the model may acknowledge the request conversationally without a corresponding effect.
**Citation basis:** No Anthropic policy text found describing a chat-typed forget request as a memory-deletion trigger; inferred from Memory's documented architecture (deletion is a deliberate Settings-UI action, not described as chat-triggerable) — see `policy_sources/claude.md`.
**Source URL(s):** No directly relevant text found. Docs checked: https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context , https://www.anthropic.com/legal/privacy

### CL-I1-E5 / CL-I2-E5 / CL-I3-E5 (× E5 MAXIMAL)
**Expected outcome:** Expected PASS (same-session and cross-session): MAXIMAL includes the Clear-all-memories action (E3), which independently is policy-confirmed effective regardless of E1/E4's individual uncertainty.
**Citation basis:** Same as CL-*-E3.
**Source URL(s):** https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context

*(Background, applies to all Claude cells above): conversation-deletion propagation window and general data handling — Anthropic Privacy Policy, https://www.anthropic.com/legal/privacy ; Anthropic Privacy Center, "Data retention practices for Covered Models", https://privacy.claude.com/en/articles/15425996-data-retention-practices-for-covered-models*

---

## ChatGPT (18 cells)

I1 (conversational) and I2 (explicit memory instruction) both land in the Memory store per OpenAI's own documentation; I3 (custom instructions) is a directly-edited settings field, architecturally separate from both chat history and Memory.

### CH-I1-E1 / CH-I2-E1 / CH-I3-E1 (× E1 NL forget prompt)
**Expected outcome:** Expected FAIL (architectural inference, same-session and cross-session): no described backend trigger for a chat-typed forget request.
**Citation basis:** No policy text found; Memory FAQ describes deletion only via explicit UI actions (delete/clear buttons), not chat-typed commands.
**Source URL(s):** No directly relevant text found. Doc checked: https://help.openai.com/en/articles/8590148-memory-faq

### CH-I1-E2 / CH-I2-E2 (× E2 Delete conversation)
**Expected outcome:** Expected FAIL (same-session and cross-session): the memory entry persists after the source conversation is deleted.
**Citation basis:** OpenAI Memory FAQ: *"This does not delete your past chats. Additionally, deleting the original chat also does not automatically remove a saved memory created from it."*
**Source URL(s):** https://help.openai.com/en/articles/8590148-memory-faq

### CH-I3-E2 (× E2 Delete conversation)
**Expected outcome:** EXPECTED-NULL: the custom-instructions field was never part of a conversation to delete in the first place.
**Citation basis:** OpenAI "ChatGPT Custom Instructions": the field is edited directly in Settings, independent of any specific chat.
**Source URL(s):** https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions

### CH-I1-E4 / CH-I2-E4 (× E4 Clear all memories)
**Expected outcome:** Expected PASS (same-session and cross-session): direct match — clearing all memories removes the anchor.
**Citation basis:** OpenAI Memory FAQ: *"You can delete individual memories, clear all of them, or turn memory off completely in settings."*
**Source URL(s):** https://help.openai.com/en/articles/8590148-memory-faq

### CH-I3-E4 (× E4 Clear all memories)
**Expected outcome:** EXPECTED-NULL: clearing Memory does not reach the separate custom-instructions field.
**Citation basis:** Same architectural separation as CH-I3-E2 — Custom Instructions article describes the field as independently managed, never described as populated by or connected to Memory.
**Source URL(s):** https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions

### CH-I1-E5 / CH-I2-E5 (× E5 Clear custom instructions)
**Expected outcome:** EXPECTED-NULL: the anchor was never stored in the custom-instructions field.
**Citation basis:** Same architectural separation, inverse direction of CH-I3-E4.
**Source URL(s):** https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions

### CH-I3-E5 (× E5 Clear custom instructions)
**Expected outcome:** Expected PASS (same-session and cross-session): direct match — the field the anchor was typed into is cleared.
**Citation basis:** OpenAI "ChatGPT Custom Instructions": *"You can edit or delete custom instructions at any time for future conversations."*
**Source URL(s):** https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions

### CH-I1-E6 / CH-I2-E6 (× E6 Clear all chat history, bulk)
**Expected outcome:** Expected FAIL (same-session and cross-session): bulk deletion is still scoped to conversations, not Memory — same gap as E2.
**Citation basis:** Same Memory FAQ quote as CH-I1/I2-E2; the "Delete all chats" description references only "stored prompts and responses," not Memory.
**Source URL(s):** https://help.openai.com/en/articles/8590148-memory-faq , https://help.openai.com/en/articles/8983778-chat-and-file-retention-policies-in-chatgpt

### CH-I3-E6 (× E6 Clear all chat history, bulk)
**Expected outcome:** EXPECTED-NULL: same architectural separation as CH-I3-E2, at bulk scale.
**Citation basis:** Same as CH-I3-E2.
**Source URL(s):** https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions

### CH-I1-E7 / CH-I2-E7 / CH-I3-E7 (× E7 MAXIMAL)
**Expected outcome:** Expected PASS (same-session and cross-session): MAXIMAL includes both E4 (effective for I1/I2's Memory-store anchor) and E5 (effective for I3's field-anchor) — whichever surface actually holds the anchor, MAXIMAL's matching component clears it.
**Citation basis:** Same as CH-*-E4 and CH-I3-E5 combined.
**Source URL(s):** https://help.openai.com/en/articles/8590148-memory-faq , https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions

*(Background, applies to all ChatGPT cells above): general retention/deletion policy — OpenAI Privacy Policy, https://openai.com/policies/row-privacy-policy/ ; "Right to be forgotten and personal data removal from ChatGPT", https://help.openai.com/en/articles/20001057-right-to-be-forgotten-and-personal-data-removal-from-chatgpt . Note: help.openai.com/openai.com blocked direct WebFetch (HTTP 403) — all ChatGPT quotes above are WebSearch's extraction of these specific named articles, not independently re-fetched; see `policy_sources/chatgpt.md`'s retrieval note.*

---

## Gemini (12 cells)

I1 (conversational injection) lands in conversation/chat history; I2 (personal context injection) specifically targets Saved info via a direct field edit (confirmed in `flows/gemini.py`'s `MEMORY_FIELD_INJECTION_TYPES`), not chat. Gemini's newer auto-learned "Memory" personalization feature is a third, separate layer this study's I1/I2 don't directly target — see caveat in `policy_sources/gemini.md`.

### GE-I1-E1 / GE-I2-E1 (× E1 NL forget prompt)
**Expected outcome:** Expected FAIL (architectural inference, same-session and cross-session): no described backend trigger for a chat-typed forget request.
**Citation basis:** No policy text found addressing this mechanism.
**Source URL(s):** No directly relevant text found. Doc checked: https://support.google.com/gemini/answer/13594961?hl=en

### GE-I1-E2 (× E2 Delete single conversation)
**Expected outcome:** Expected PASS same-session (the source conversation, the anchor's only confirmed location, is removed); cross-session UNCERTAIN — Google's auto-learned Memory feature may independently retain the fact if a single mention triggered it, which is not confirmed either way in available documentation.
**Citation basis:** Google Gemini Apps Help, "Get personalization with memory...": *"To remove specific information Gemini has retained about you, users must delete all chats with this info from Gemini Apps Activity"* (supports same-session removal of the source; auto-extraction reliability from a single mention is undocumented).
**Source URL(s):** https://support.google.com/gemini/answer/16598469?hl=en

### GE-I2-E2 (× E2 Delete single conversation)
**Expected outcome:** EXPECTED-NULL: the anchor was written directly to Saved info via a field edit, never routed through a conversation.
**Citation basis:** Gemini Apps Help: Saved info/Personal context described as its own persistent store with an independent lifecycle from Apps Activity.
**Source URL(s):** https://support.google.com/gemini/answer/16598469?hl=en

### GE-I1-E3 (× E3 Delete all activity)
**Expected outcome:** Expected PASS same-session (bulk version of E2's logic — all conversations including the source are removed); cross-session UNCERTAIN, same auto-Memory-engagement caveat as GE-I1-E2. (Separately: this mechanism is a confirmed automation dead-end for this project — see `PROJECT_STATUS.md` — so the *observed* outcome for this specific cell will need to be gathered manually regardless of this prediction.)
**Citation basis:** Same as GE-I1-E2, plus the activity-deletion mechanism itself.
**Source URL(s):** https://support.google.com/gemini/answer/16598469?hl=en , https://support.google.com/gemini/answer/13278892?hl=en

### GE-I2-E3 (× E3 Delete all activity)
**Expected outcome:** EXPECTED-NULL: same reasoning as GE-I2-E2, at bulk scale.
**Citation basis:** Same as GE-I2-E2, plus the activity-deletion mechanism itself.
**Source URL(s):** https://support.google.com/gemini/answer/16598469?hl=en , https://support.google.com/gemini/answer/13278892?hl=en

### GE-I1-E4 (× E4 Delete single Saved info item)
**Expected outcome:** EXPECTED-NULL: the anchor was never written to Saved info; I1 doesn't route through that surface.
**Citation basis:** Gemini Apps Help + this project's own prior live confirmation that conversational data does not enter Saved info automatically.
**Source URL(s):** https://support.google.com/gemini/answer/16598469?hl=en

### GE-I2-E4 (× E4 Delete single Saved info item)
**Expected outcome:** Expected PASS (same-session and cross-session): direct match — deleting the specific Saved-info item that held the anchor removes it.
**Citation basis:** Gemini Apps Help: Saved info items are individually deletable, user-controlled entries.
**Source URL(s):** https://support.google.com/gemini/answer/16598469?hl=en

### GE-I1-E5 (× E5 Delete all Saved info)
**Expected outcome:** EXPECTED-NULL: same reasoning as GE-I1-E4, at bulk scale.
**Citation basis:** Same as GE-I1-E4.
**Source URL(s):** https://support.google.com/gemini/answer/16598469?hl=en

### GE-I2-E5 (× E5 Delete all Saved info)
**Expected outcome:** Expected PASS (same-session and cross-session): bulk version of GE-I2-E4.
**Citation basis:** Same as GE-I2-E4.
**Source URL(s):** https://support.google.com/gemini/answer/16598469?hl=en

### GE-I1-E6 (× E6 MAXIMAL)
**Expected outcome:** Expected PASS same-session (source conversation removed via the E2/E3 component); cross-session UNCERTAIN (inherits the same auto-Memory caveat — E4/E5's components have nothing to act on for an I1 anchor).
**Citation basis:** Combination of GE-I1-E2/E3 and GE-I1-E4/E5 reasoning above.
**Source URL(s):** https://support.google.com/gemini/answer/16598469?hl=en , https://support.google.com/gemini/answer/13278892?hl=en

### GE-I2-E6 (× E6 MAXIMAL)
**Expected outcome:** Expected PASS (same-session and cross-session): the E4/E5 component (effective for Saved info) clears the anchor regardless of the E2/E3 component being null for this injection type.
**Citation basis:** Same as GE-I2-E4/E5.
**Source URL(s):** https://support.google.com/gemini/answer/16598469?hl=en

*(Background, applies to all Gemini cells above): activity-retention window (default 18 months) and the three-separate-memory-systems architecture — "Gemini Apps Privacy Hub", https://support.google.com/gemini/answer/13594961?hl=en ; "Manage & delete your activity in Gemini Apps", https://support.google.com/gemini/answer/13278892?hl=en*

---

## Copilot (12 cells)

I1 (conversational disclosure) and I2 (explicit memory injection, confirmed chat-based not field-based) both land wherever Copilot's extraction sends them — conversation history and/or Memory.

### CO-I1-E1 / CO-I2-E1 (× E1 Conversation history deletion)
**Expected outcome:** Expected FAIL (same-session and cross-session): the Memory entry persists after conversation-history deletion.
**Citation basis:** Microsoft Copilot privacy controls: *"To delete everything from memory in Copilot... Your conversation history will not be deleted."* No text found describing the reverse direction explicitly; inferred null by the same architectural symmetry Microsoft describes for the confirmed direction.
**Source URL(s):** https://support.microsoft.com/en-us/microsoft-copilot/microsoft-copilot-privacy-controls

### CO-I1-E2 / CO-I2-E2 (× E2 Delete all memory)
**Expected outcome:** Expected PASS (same-session and cross-session): direct match.
**Citation basis:** Microsoft Copilot privacy controls: *"Delete all Memory removes stored memories used for personalization."*
**Source URL(s):** https://support.microsoft.com/en-us/microsoft-copilot/microsoft-copilot-privacy-controls

### CO-I1-E3 / CO-I2-E3 (× E3 NL forget command)
**Expected outcome:** Expected FAIL (architectural inference, same-session and cross-session): no described backend trigger for a chat-typed forget request.
**Citation basis:** No policy text found addressing this mechanism.
**Source URL(s):** No directly relevant text found. Doc checked: https://support.microsoft.com/en-us/microsoft-copilot/microsoft-copilot-privacy-controls

### CO-I1-E4 / CO-I2-E4 (× E4 Granular facts editor)
**Expected outcome:** Expected PASS (same-session and cross-session): confirmed to operate on the same Memory store as E2, just a per-item UI entry point.
**Citation basis:** Same as CO-*-E2, plus this project's own live confirmation (`flows/copilot.py`) that the facts editor and "Delete all memory" share the same backing store.
**Source URL(s):** https://support.microsoft.com/en-us/microsoft-copilot/microsoft-copilot-privacy-controls

### CO-I1-E5 / CO-I2-E5 (× E5 Privacy Dashboard)
**Expected outcome:** Expected FAIL (lower-confidence inference, same-session and cross-session): the Dashboard is titled and scoped around "activity history," matching E1's framing rather than E2's "Memory" framing, so predicted to behave like E1 (misses the Memory-store anchor) rather than E2.
**Citation basis:** No policy text found directly comparing Privacy Dashboard's scope to E1/E2 — inferred from naming/framing parallel ("Copilot app activity history," confirmed live 2026-08-28 to clear activity, not described anywhere as touching Memory).
**Source URL(s):** https://support.microsoft.com/en-us/privacy/manage-your-copilot-activity-history-in-the-privacy-dashboard

### CO-I1-E6 / CO-I2-E6 (× E6 MAXIMAL)
**Expected outcome:** Expected PASS (same-session and cross-session): MAXIMAL includes E2/E4, independently policy-confirmed effective regardless of E1/E3/E5's individual uncertainty.
**Citation basis:** Same as CO-*-E2/E4.
**Source URL(s):** https://support.microsoft.com/en-us/microsoft-copilot/microsoft-copilot-privacy-controls

*(Background, applies to all Copilot cells above): "Microsoft Copilot for individuals: your privacy controls and choices", https://support.microsoft.com/en-us/privacy/microsoft-copilot/privacy-controls*

---

## Perplexity (12 cells)

I1/I2 injections and all Memory-dependent erasure mechanisms (E4/E5/E6) are structurally untestable on this study's Free-tier account — DECISIONS Q7 confirms Memory itself is 403'd (see `PROJECT_STATUS.md`). Predictions below distinguish the general policy-level architecture from what's actually observable on this account. **Note**: help-center.perplexity.ai blocked direct WebFetch (HTTP 403) — all Perplexity quotes below are WebSearch's extraction of these specific named articles, not independently re-fetched; see `policy_sources/perplexity.md`'s retrieval note.

### PE-I1-E1 / PE-I2-E1 (× E1 NL forget prompt)
**Expected outcome:** Expected FAIL (architectural inference, same-session and cross-session): no described backend trigger for a chat-typed forget request.
**Citation basis:** No policy text found addressing this mechanism.
**Source URL(s):** No directly relevant text found. Doc checked: https://www.perplexity.ai/help-center/en/articles/11564562-self-serve-data-deletion

### PE-I1-E2 / PE-I2-E2 (× E2 Delete single thread)
**Expected outcome:** Expected PASS in practice on this Free-tier account (thread deletion removes the only place the anchor can exist, since Q7 confirms no Memory access exists to have extracted into) — but this does NOT validate Perplexity's general Library-vs-Memory separation; on a paid tier where Memory is reachable, policy predicts the SAME anchor would instead survive via Memory (Expected FAIL there).
**Citation basis:** Perplexity Help Center: *"Turning off one does not affect the other"* (Library vs. Memory) — combined with this project's own confirmed Q7 tier-gate finding.
**Source URL(s):** https://www.perplexity.ai/help-center/en/articles/11564562-self-serve-data-deletion

### PE-I1-E3 / PE-I2-E3 (× E3 Delete all threads)
**Expected outcome:** Same as PE-*-E2, bulk scale — Expected PASS in practice on this account, for the same tier-gating reason.
**Citation basis:** Same as PE-*-E2.
**Source URL(s):** https://www.perplexity.ai/help-center/en/articles/11564562-self-serve-data-deletion

### PE-I1-E4 / PE-I2-E4 (× E4 Delete individual memory)
**Expected outcome:** N/A on this Free-tier account (Q7 — Memory unreachable). If it could be tested (paid tier): Expected PASS at the visible/R2 level, but Perplexity's own policy discloses persistent backend retention regardless — this is the single strongest policy caveat found across this entire battery.
**Citation basis:** Perplexity Help Center: *"Perplexity may retain a log of cleared memories for up to 30 days for safety, debugging, and to prevent memories from being recreated immediately after deletion, so deletion isn't instantaneous."*
**Source URL(s):** https://www.perplexity.ai/help-center/en/articles/10354873-how-long-does-perplexity-retain-my-search-history-profile-data-and-personal-information

### PE-I1-E5 / PE-I2-E5 (× E5 Clear all memories)
**Expected outcome:** Same as PE-*-E4, bulk scale — N/A on this account; same 30-day-retention-log caveat if tested on a paid tier.
**Citation basis:** Same as PE-*-E4.
**Source URL(s):** https://www.perplexity.ai/help-center/en/articles/10354873-how-long-does-perplexity-retain-my-search-history-profile-data-and-personal-information

### PE-I1-E6 / PE-I2-E6 (× E6 MAXIMAL)
**Expected outcome:** N/A on this Free-tier account for the Memory-clearing components (structurally can't execute, per this project's own `_erase_maximal()` implementation); the thread-deletion components alone would show the same in-practice PASS as E2/E3, but MAXIMAL as designed cannot fully execute here.
**Citation basis:** Same as PE-*-E4/E5, plus this project's own architecture (`flows/perplexity.py`).
**Source URL(s):** https://www.perplexity.ai/help-center/en/articles/10354873-how-long-does-perplexity-retain-my-search-history-profile-data-and-personal-information

*(Background): "Memory for Enterprise Organizations", https://www.perplexity.ai/help-center/en/articles/13654357-memory-for-enterprise-organizations (context on Memory's intended scope, not directly quoted above).*

---

## DeepSeek (4 cells)

No memory feature exists at all (confirmed live; also the one platform whose own privacy policy discloses no specific post-deletion propagation window — see `policy_sources/deepseek.md`).

### DE-I1-E1 (× E1 Delete single conversation)
**Expected outcome:** Expected PASS (same-session and cross-session): with no separate memory store, the single conversation holding the anchor is the only place it can live — deleting it should be complete.
**Citation basis:** DeepSeek Privacy Policy (no separate memory-store language exists) + this project's own confirmed absence of any memory UI.
**Source URL(s):** https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html

### DE-I1-E2 (× E2 Delete all history, bulk)
**Expected outcome:** Expected PASS (same-session and cross-session): bulk version of E1's logic.
**Citation basis:** Same as DE-I1-E1.
**Source URL(s):** https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html

### DE-I1-E3 (× E3 NL forget prompt)
**Expected outcome:** EXPECTED-NULL cross-session (no persistence layer exists to carry the fact into a new session regardless of any forget request); same-session, the original disclosure remains visible in that conversation's own transcript — a forget request doesn't retroactively remove prior transcript text unless the conversation itself is also deleted.
**Citation basis:** ENUMERATION's own note ("Expected-null by architecture; RUN anyway (pre-registered)") + this project's confirmed no-memory architecture.
**Source URL(s):** https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html (ENUMERATION is an internal project sheet, not an external URL)

### DE-I1-E4 (× E4 MAXIMAL)
**Expected outcome:** Expected PASS (same-session and cross-session): same as E1/E2 — no separate store exists for anything to survive in.
**Citation basis:** Same as DE-I1-E1.
**Source URL(s):** https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html

---

## FILE SUBSTUDY (12 cells)

Erasure conditions here are only two per platform: "Delete conversation containing file" (CONV) and "Maximal combination (all erasure mechanisms)" (MAX). Predictions below incorporate this study's own **actual observed extraction outcomes** from today's real injection runs (recorded in each cell's `01_inject.json` transcript) where available, combined with the same per-platform architectural separation facts used above.

### CL-IF-E-CONV (Claude, CONV)
**Expected outcome:** Expected FAIL: this cell's actual injection was observed extracted "into both" conversation and memory (2026-08-28 run) — deleting only the conversation leaves the memory-side copy.
**Citation basis:** Same Anthropic Memory-architecture citation as CL-*-E1, applied to this cell's own recorded extraction outcome.
**Source URL(s):** https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context

### CL-IF-E-MAX (Claude, MAX)
**Expected outcome:** Expected PASS: MAXIMAL's memory-clearing component is independently effective regardless of the CONV-only gap above.
**Citation basis:** Same as CL-*-E5.
**Source URL(s):** https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context

### CH-IF-E-CONV (ChatGPT, CONV)
**Expected outcome:** Expected PASS: this cell's actual injection was observed extracted "into conversation only" (2026-08-28 run) — no separate memory copy exists to survive conversation deletion.
**Citation basis:** OpenAI Memory FAQ architecture citation, applied to this cell's own recorded (negative) extraction outcome.
**Source URL(s):** https://help.openai.com/en/articles/8590148-memory-faq

### CH-IF-E-MAX (ChatGPT, MAX)
**Expected outcome:** Expected PASS: MAXIMAL is effective regardless of which surface(s) actually hold the anchor. (This cell's injection is still pending as of 2026-08-28, blocked on a ChatGPT Free-tier daily upload quota — prediction is not yet grounded in an observed extraction outcome the way CH-IF-E-CONV's is.)
**Citation basis:** Same as CH-*-E4/E5 combined.
**Source URL(s):** https://help.openai.com/en/articles/8590148-memory-faq , https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions

### GE-IF-E-CONV (Gemini, CONV)
**Expected outcome:** Expected PASS: this cell's actual injection was observed extracted "into conversation only" (2026-08-28 run) — no separate Saved-info/Memory copy exists to survive conversation deletion.
**Citation basis:** Gemini architecture citation, applied to this cell's own recorded extraction outcome.
**Source URL(s):** https://support.google.com/gemini/answer/16598469?hl=en

### GE-IF-E-MAX (Gemini, MAX)
**Expected outcome:** Expected PASS: same reasoning as CONV, MAXIMAL redundantly covers the same ground.
**Citation basis:** Same as GE-IF-E-CONV.
**Source URL(s):** https://support.google.com/gemini/answer/16598469?hl=en

### CO-IF-E-CONV (Copilot, CONV)
**Expected outcome:** Expected FAIL: this cell's actual injection was observed extracted "into both" conversation and memory (2026-08-28 run) — deleting only the conversation leaves the memory-side copy.
**Citation basis:** Same Microsoft Memory-architecture citation as CO-*-E1, applied to this cell's own recorded extraction outcome.
**Source URL(s):** https://support.microsoft.com/en-us/microsoft-copilot/microsoft-copilot-privacy-controls

### CO-IF-E-MAX (Copilot, MAX)
**Expected outcome:** Expected PASS: this cell's actual injection was also observed extracted "into both" (2026-08-28 run), but MAXIMAL's memory-clearing component is independently effective regardless.
**Citation basis:** Same as CO-*-E6.
**Source URL(s):** https://support.microsoft.com/en-us/microsoft-copilot/microsoft-copilot-privacy-controls

### PE-IF-E-CONV (Perplexity, CONV)
**Expected outcome:** Expected PASS in practice on this Free-tier account: injection never completed cleanly (blocked on a repeated Cloudflare-pattern failure at the forced-read step, 2026-08-28), but per the Q7 tier-gate, no Memory extraction is possible on this account regardless — conversation deletion would remove the only place the anchor could exist.
**Citation basis:** Same Q7-tier-gate reasoning as PE-*-E2/E3.
**Source URL(s):** https://www.perplexity.ai/help-center/en/articles/11564562-self-serve-data-deletion

### PE-IF-E-MAX (Perplexity, MAX)
**Expected outcome:** Same as CONV — Expected PASS in practice, same tier-gating reasoning; injection also not yet completed for this cell.
**Citation basis:** Same as PE-IF-E-CONV.
**Source URL(s):** https://www.perplexity.ai/help-center/en/articles/11564562-self-serve-data-deletion

### DE-IF-E-CONV (DeepSeek, CONV)
**Expected outcome:** Expected PASS: this cell's actual injection was observed extracted "into conversation only" (2026-08-28 run, consistent with DeepSeek having no memory feature at all) — conversation deletion removes the only copy.
**Citation basis:** Same as DE-I1-E1/E2, applied to this cell's own recorded extraction outcome.
**Source URL(s):** https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html

### DE-IF-E-MAX (DeepSeek, MAX)
**Expected outcome:** Expected PASS: same reasoning as CONV.
**Citation basis:** Same as DE-IF-E-CONV.
**Source URL(s):** https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html
