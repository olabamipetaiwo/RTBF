# Gemini (Google) — policy excerpts

## Sources
- https://support.google.com/gemini/answer/13594961?hl=en — Gemini Apps Help, "Gemini Apps Privacy Hub" (fetched 2026-08-28)
- https://support.google.com/gemini/answer/16598469?hl=en — Gemini Apps Help, "Get personalization with memory of your past Gemini chats" (fetched 2026-08-28)
- https://support.google.com/gemini/answer/13278892?hl=en — Gemini Apps Help, "Manage & delete your activity in Gemini Apps" (retrieved via search snippet 2026-08-28)

## Important architectural note: Gemini has THREE separate memory-adjacent systems, not one
Per Google's own documentation, "Gemini's memory is not one feature — it splits across three separate systems with overlapping names": **Apps Activity** (conversation/chat history, this study's E2/E3 target), **Saved info / Personal context** (the older, explicit per-item list — confirmed live earlier this project as this study's actual I2 target, still called "Instructions for Gemini" in the current UI), and a newer **auto-learned "Memory" personalization feature** ("Personal Intelligence > Memory" toggle) that learns automatically from past chats.

**This matters for prediction direction**: for the newer auto-learned Memory feature, Google's own docs say the way to remove something it learned is to **delete the source chats from Apps Activity** — i.e. conversation deletion DOES reach that specific memory layer, the inverse of the Claude/ChatGPT pattern. But this study's I2 injections specifically target **Saved info**, not this newer auto-learned layer (confirmed via `tester/flows/gemini.py`'s `MEMORY_FIELD_INJECTION_TYPES = {"I2"}`), so this inversion doesn't apply to I2/E4/E5 cells — it's most relevant to whether E3 (Delete all activity) might incidentally also scrub anything the auto-learn feature picked up from an I1 conversational disclosure, which is a genuinely different, less certain prediction than Claude/ChatGPT's clean "conversation deletion never reaches memory."

## Activity/conversation retention & deletion (E2/E3)
> Default auto-delete: **18 months**, changeable to 3 months, 36 months, or indefinite (Gemini Apps Privacy Hub)
> "Chats reviewed by human reviewers (and related data like your language, device type, location info, or feedback) are **not deleted** when you delete your activity" — retained separately for up to 3 years
> "If you delete a chat, there might be a short delay before Gemini stops using it to personalize your responses." — disclosed short propagation delay (no specific number of days given)

## Saved info / Personal context (I2 injection surface; E4/E5 erasure surface)
> "Saved instructions remain 'saved until you choose to delete it' in distinct settings" — confirms Saved info is its own persistent store, independent lifecycle from Apps Activity.
> Deleting Gemini Apps activity specifically doesn't affect Saved info (implied by the same source treating them as separate settings sections; no text found stating activity-deletion reaches Saved info).

This confirms the EXPECTED-NULL pattern already used in one of the 13 pre-filled MASTER rows (`GE-I1-E4`) — conversational activity deletion does not reach Saved info, and (by the same separation) Saved info deletion does not remove the originating conversation.

## Auto-learned Memory feature (relevant to E3's scope, not a separate injection surface in this study)
> "To remove specific information Gemini has retained about you, users must delete all chats with this info from Gemini Apps Activity." — confirms conversation/activity deletion IS the disclosed mechanism for this specific layer.
> "If you only delete the chats, Gemini might still find the info in the connected app" (for Connected-Apps-sourced personalization specifically — not relevant to this study's disclosure-based injections, which aren't Connected-Apps data).

## NL forget prompt (E1)
No policy text found addressing an in-chat natural-language "forget" request as a deletion trigger. Same gap as Claude/ChatGPT's equivalent cells.

## Cross-domain note (already confirmed live this project, not new from this pass)
E3 (Delete all activity) opens a separate domain (myactivity.google.com) from gemini.google.com — already extensively investigated live this session (see `PROJECT_STATUS.md`'s "Gemini/Copilot cross-domain gap revisited" section); this is an automation-feasibility finding, not a policy citation, so not restated in full here.
