# Perplexity — policy excerpts

## Sources
- https://www.perplexity.ai/help-center/en/articles/10354873-how-long-does-perplexity-retain-my-search-history-profile-data-and-personal-information — Perplexity Help Center, "How long does Perplexity retain my search history, profile data, and personal information?" (retrieved via search snippet 2026-08-28; direct WebFetch returned HTTP 403)
- https://www.perplexity.ai/help-center/en/articles/11564562-self-serve-data-deletion — Perplexity Help Center, "Self-Serve Data Deletion" (retrieved via search snippet 2026-08-28; direct WebFetch 403)
- https://www.perplexity.ai/help-center/en/articles/13654357-memory-for-enterprise-organizations — Perplexity Help Center, "Memory for Enterprise Organizations" (search snippet)

**Note on retrieval**: help-center.perplexity.ai returned 403 to direct WebFetch. Quotes below come from WebSearch's own extraction of these specific, named Help Center articles.

## The 30-day retention log of cleared memories — the fact ENUMERATION already flagged as needing citation
> "Perplexity **may retain a log of cleared memories for up to 30 days** for safety, debugging, and to prevent memories from being recreated immediately after deletion, so deletion isn't instantaneous." — Perplexity Help Center

This is the single most important citable fact for this platform: **Perplexity explicitly discloses that clearing a memory doesn't mean immediate, complete erasure** — a 30-day retention log persists behind the scenes even after the user-facing "cleared" state. Directly relevant to E4/E5's Expected-outcome predictions: a passing R2 check (memory panel shows nothing) does not by itself establish full backend erasure per Perplexity's own stated policy — same caveat this project already flagged for the one MASTER row (`PE-I1-E4`) that referenced this before this pass.

## Library (conversation/thread history) vs. Memory — confirmed separate stores
> "Perplexity's conversation history (your Library) stores the full text of search and answer threads, while Memory stores compact personalization facts about you — preferences, background, recurring topics. **Turning off one does not affect the other.**" — Perplexity Help Center / product documentation

Same architectural separation pattern as every other platform researched this pass: thread/Library deletion (E2/E3) does not reach Memory (E4/E5), and vice versa.

## Account-level / general retention
> "Your account and personal information are retained as long as your account is active, and if you delete your account, Perplexity removes your data from its servers within 30 days."
> Uploaded files/images: auto-deleted after 30 days (consumer), 7 days (enterprise).

## Thread deletion mechanics (E2/E3) — already confirmed live this project
This project's own live investigation (`flows/perplexity.py`, confirmed 2026-08-27) already established single-thread vs. all-threads deletion are genuinely separate actions with separate confirm dialogs. No additional policy-level nuance found in this pass beyond the general 30-day account-deletion window above (no specific per-thread deletion propagation window disclosed distinct from that).

## NL forget prompt (E1)
No policy text found addressing an in-chat natural-language "forget" request as a deletion trigger. Same gap as every other platform's equivalent cells.

## Tier-gating caveat (already confirmed live this project, restated for completeness)
This study's Free-tier test account is 403'd out of the Memory feature entirely (DECISIONS Q7, confirmed live 2026-08-27) — every Memory-dependent cell (E4/E5/E6, and I1/I2's own Q8/Q9 calibration questions) is structurally untestable on this account regardless of what the policy says should happen. Not a new finding from this pass, but directly relevant context for how to phrase Expected-outcome text for those cells (predictions can be policy-grounded in principle, but "Observed outcome" for these cells will read N/A/blocked-by-tier, not a genuine pass/fail).
