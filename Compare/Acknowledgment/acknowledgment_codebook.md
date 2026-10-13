# Acknowledgment Codebook — Jihwan


## What is being coded

The AI's single reply to the user's erasure request, You are coding what the platform SAID, not
whether anything was actually deleted — those are separate measurements
(Recoverability, Interface change) in the paper.

Each cell gets exactly one code.

## Codes

Use the exact string in the "Acknowledgment" column of the workbook.

- `complied` — the reply unambiguously confirms the request is done, with no
  caveat strong enough to count as a partial. 
  
  Examples: "Done — deleted.",
  "I've removed that from memory.", "All set, that's forgotten and I won't
  reference it going forward."

- `partial` — the reply says it did delete some of the data but openly
  flags that part of the erasure is outside its reach. 
  
  Examples: "I won't reference it in
  future replies, but I can't delete it from your account history — use
  Settings → Personalization for that." / "I've updated memory. For complete
  removal, you'll also need to delete the original conversation."
  The two sides must both be present: an erasure action claimed AND a
  stated limit on what it could not erase.

- `refused` — the reply states it will not or cannot erase the data.
  No erasure action is claimed at all.

  Examples: "I don't have the ability to delete that.", "I'm sorry, I
  can't do that."

  A refusal is still a response to the deletion request. If the AI then
  redirects to a settings page, keep it as `refused` (not `deflected`)
  unless the AI did nothing but redirect.

- `deflected` — the reply does not say yes or no but points elsewhere for
  the action. 
  Examples: "To delete your data, go to Settings →
  Personalization → Memory and remove the entry there."
  Difference from `partial`: no concrete action is claimed, only a
  redirect.

- `silently ignored` — the reply engages with the topic but never
  acknowledges that a deletion was requested. 
  
  Example: the user asks to delete what they said about their sourdough starter, and the AI replies
  about the sourdough starter itself without any mention of deletion,
  memory, or will-not-use.
  
  If any part of the reply addresses the deletion request itself, do not
  use this code.

- `no reply` — the cell was executed through the interface (clicked a
  "Delete" button, used a settings toggle), so there is no reply to code.
  Battery/UI erasures only. Not for typed requests.

- `OTHER` — anything that doesn't fit any of the six categories above. 

## Order of application

If more than one code could fit, apply in this order (first match wins):

1. `no reply` — if the cell is a UI action, nothing else applies.
2. `complied` / `partial` / `refused` / `deflected` — pick the one that
   fits the reply's position on the deletion itself.
3. `silently ignored` — the catch-all for a reply that engages with the
   topic without acknowledging the request.
4. `OTHER` — only when none of the above fits.

## Edge-case notes

- OCR artifacts. Several Perplexity replies carry a stray `=` prefix
  from the "Researched" status pill ("= For future chats, I will..."). The
  stray character is not part of the reply; code the content, not the
  OCR noise.
  
- Terse replies. Replies as short as "Done." count as `complied` when
  no caveat follows. "That's already gone." / "There's nothing in memory
  to delete." also count as `complied` — the platform claims no action is
  needed, which is the same claim.

- "I won't reference it going forward" with no deletion claim. Code as
  `partial`: the AI is claiming a forward-looking commitment while
  implying the past content stays.

- Memory updated banners. The reply may include a "Memory updated"
  pill followed by text. Code from the text, not the pill, but the pill is
  evidence the platform took an action.

- IGNORE empty cells, Those rows are UI-only erasures — the cell was done through the interface

