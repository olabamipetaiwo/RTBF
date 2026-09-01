# Copilot (Microsoft) — policy excerpts

## Sources
- https://support.microsoft.com/en-us/microsoft-copilot/microsoft-copilot-privacy-controls — Microsoft Support, "Microsoft Copilot privacy controls" (fetched 2026-08-28)
- https://support.microsoft.com/en-us/privacy/manage-your-copilot-activity-history-in-the-privacy-dashboard — Microsoft Support, "Manage your Copilot activity history in the privacy dashboard" (fetched 2026-08-28)
- https://support.microsoft.com/en-us/privacy/microsoft-copilot/privacy-controls — Microsoft Support, "Microsoft Copilot for individuals: your privacy controls and choices" (retrieved via search snippet 2026-08-28)

## Conversation history (E1) vs. Memory (E2) — confirmed separate stores
> "To delete everything from memory in Copilot: Select your profile icon, then select **Memory** > **Delete all Memory**. **Your conversation history will not be deleted.**" — Microsoft Copilot privacy controls

> "You can delete individual items from your conversation history or delete your entire conversation history in Copilot at any time." — same source (no text found stating this reaches Memory in the other direction)

Same architectural pattern as Claude/ChatGPT: conversation history and Memory are explicitly separate deletion targets, and Microsoft states plainly that deleting Memory does **not** touch conversation history. No text found addressing the reverse (whether deleting conversation history removes Memory entries derived from it) — inferred null by the same architectural-separation logic used elsewhere (see `PROJECT_STATUS.md`'s prior live confirmation that Copilot's "Personalization and memory" toggle doesn't delete existing facts either — a related but distinct finding, not itself a deletion action).

## Retention window
> "Microsoft retains your conversation history for **18 months**" — Microsoft Copilot for individuals: privacy controls
> Files shared with Copilot are "stored securely for up to **30 days** and then automatically deleted."

No text found disclosing a specific backend-propagation delay after an explicit user-initiated deletion (distinct from the passive 18-month/30-day retention-then-auto-delete windows above) — this project's own R2/recall-delay design (31 days) is not directly corroborated or contradicted by anything found in Copilot's own documentation.

## Granular facts editor (E4) — confirmed same as "Delete all Memory," different UI entry point
This project's own live investigation (documented in `flows/copilot.py`) already confirmed the "View memory" / granular facts editor and the "Delete all Memory" action operate on the same underlying Memory store — this pass found no additional policy text beyond what's already cited above for E2.

## Privacy Dashboard (E5) — confirmed cross-domain, resolved 2026-08-28
> "If you select **Delete all activity history**, review the information in the 'Are you sure you want to clear your Copilot activity history?' dialog." — Manage your Copilot activity history in the privacy dashboard

Applies separately to "Copilot apps" (copilot.microsoft.com — this study's actual target) vs. "Copilot in Microsoft 365 apps" as two distinct sections on the same dashboard page — already confirmed live this session (see `PROJECT_STATUS.md`). No text found comparing this dashboard-level deletion's completeness/scope against the in-app "Conversation history deletion" (E1) or "Delete all Memory" (E2) actions — no citable basis to predict whether the Privacy Dashboard's action is broader, narrower, or equivalent to those; treat as its own independent erasure surface rather than assuming it's a superset.

## NL forget prompt (E3)
No policy text found addressing an in-chat natural-language "forget" request as a deletion trigger. Same gap as every other platform's equivalent cells.
