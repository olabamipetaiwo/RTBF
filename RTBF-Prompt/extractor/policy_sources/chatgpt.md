# ChatGPT (OpenAI) — policy excerpts

## Sources
- https://help.openai.com/en/articles/8983778-chat-and-file-retention-policies-in-chatgpt — OpenAI Help Center, "Chat and File Retention Policies in ChatGPT" (retrieved via search snippet 2026-08-28; direct WebFetch returned HTTP 403 on help.openai.com)
- https://help.openai.com/en/articles/8590148-memory-faq — OpenAI Help Center, "Memory FAQ" (retrieved via search snippet 2026-08-28; direct WebFetch 403)
- https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions — OpenAI Help Center, "ChatGPT Custom Instructions" (retrieved via search snippet 2026-08-28)
- https://help.openai.com/en/articles/20001057-right-to-be-forgotten-and-personal-data-removal-from-chatgpt — OpenAI Help Center, "Right to be forgotten and personal data removal from ChatGPT" (retrieved via search snippet 2026-08-28)
- https://openai.com/policies/row-privacy-policy/ — OpenAI Privacy Policy (direct WebFetch 403, not independently re-verified against primary text this pass)

**Note on retrieval**: help.openai.com and openai.com both returned HTTP 403 to direct WebFetch (bot protection). The quotes below come from WebSearch's own extraction of these specific, named Help Center articles — still a checkable, specific citation (exact article title + URL), just not independently re-fetched and re-quoted directly in this pass.

## Conversation deletion (E2) and bulk deletion (E6)
> "When you delete a chat or your account, the chat is removed from your account immediately and scheduled for permanent deletion from OpenAI systems within 30 days, unless the chat has already been de-identified and disassociated from you, or OpenAI must retain it longer for security or legal obligations." — Chat and File Retention Policies

> "You can select 'Delete all chats' in Settings and Data Controls to confirm the action. Deleting conversations ensures that stored prompts and responses are scheduled for removal from the platform's systems." — (bulk delete)

Same 30-day backend propagation window as Claude's, and no indication bulk-delete behaves differently from single-delete in terms of the retention window (both are "scheduled for removal").

## Memory architecture (I1/I2 injection surface; E4 erasure surface)
> "Saved memories are details you've directly told ChatGPT to remember... You can delete individual memories, clear all of them, or turn memory off completely in settings." — Memory FAQ

> **"It's important to note that this does not delete your past chats. Additionally, deleting the original chat also does not automatically remove a saved memory created from it."** — Memory FAQ

Same architectural pattern as Claude and (per this project's own prior live findings) Gemini/Copilot: **conversation deletion does not reach the separate memory store, and vice versa** — memory deletion (E4) doesn't delete the conversation that originally produced the memory.

## Custom instructions (I3 injection surface; E5 erasure surface)
> "You can edit or delete custom instructions at any time for future conversations. Updates to your instructions are reflected only in future conversations. To remove custom instructions from previous conversations, you can clear those conversations from your chat history." — ChatGPT Custom Instructions

Custom instructions are a config field separate from both chat history and the Memory store — clearing this field (E5) only affects future conversations' system context, and per this same text does not retroactively touch any past conversation. This confirms E5 acting on I3 injections should be a clean field-clear (the injected anchor was typed directly into this field), while E5 acting on an I1/I2 injection (conversational disclosure, which never touched this field) is architecturally a scope mismatch.

> "When you delete your OpenAI account, custom instructions that are tied to your account will also be deleted within 30 days as part of that process." — (account deletion context, not directly relevant to per-field clearing, included for completeness)

## NL forget prompt (E1)
No primary policy text found addressing whether an in-chat natural-language "please forget X" request triggers any actual backend deletion action (vs. a conversational acknowledgment only) — same gap as Claude's E4. No citable source for this mechanism specifically.

## Out-of-scope but worth noting: the formal "Right to be forgotten" process
OpenAI has a **separate, formal, case-by-case legal request mechanism** (submitted via the Privacy Portal, not an in-product UI button) for removing personal information from ChatGPT's responses under GDPR-style rights: *"erasure", "right to be forgotten" or "objection" rights are not absolute and OpenAI may decline a request if they have a lawful reason for doing so."* This is explicitly **not** what this study's E1-E7 cells test (those are self-service in-product UI actions) — worth distinguishing in the paper's framing so readers don't conflate "the button in Settings didn't fully erase it" with "OpenAI's formal RTBF process failed," which are different claims.
