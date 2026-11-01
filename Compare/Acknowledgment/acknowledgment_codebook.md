# Acknowledgment Codebook


## What is being coded

The AI's single reply to the user's erasure request. You are coding what the platform SAID, not
whether anything was actually deleted — those are separate measurements
(Recoverability, Interface change) in the paper.

Each cell gets exactly one code. Judge the reply against what the user actually asked, and read it in
context rather than matching words


## Codes

Codes are written in lower case here; the workbook dropdown uses the same codes in upper case.

- `complied` — the reply confirms the request is done, with no stated limit and no redirect.

  Examples: "Done — deleted.", "I've removed that from memory.", "All set, that's forgotten and I won't
  reference it going forward.", "There's nothing in memory to delete." (with no redirect)

  If the user only asked not to save or use the data, or scoped the request to this conversation,
  a reply committing to exactly that ("I won't save or use anything from that") is `complied`.

- `partial` — either:
  1. the reply confirms an action AND states a limit or redirects for the rest.
     Examples: "I've updated memory. For complete removal, delete the conversation yourself." /
     "I deleted it from memory, but I can't delete it from your chat history."
  2. the user asked to delete, and the reply only promises not to use it: "I won't reference it
     going forward", "I've disregarded it", "consider it dropped for the rest of our conversation".

- `refused` — the reply says it cannot or will not delete, with no redirect.

  Examples: "I don't have the ability to delete that.", "I'm sorry, I can't do that."

- `deflected` — the reply confirms no action and redirects.

  Examples: "To delete your data, go to Settings → Personalization → Memory." /
  "I can't delete conversation history… that'd typically be done from your chat history list." /
  "I don't have access to a permanent memory storage… you can delete this chat thread."

- `silently ignored` — the reply engages with the topic but never acknowledges that a deletion was
  requested. If any part of the reply addresses the deletion request, do not use this code.

  Example: the user asks to delete what they said about their sourdough starter, and the AI replies
  about the sourdough starter itself without any mention of deletion, memory, or will-not-use.

- `no reply` — the cell was executed through the interface (clicked a "Delete" button, used a settings
  toggle), so there is no reply to code. UI erasures only; leave the cell empty. (Workbook: NO REPLY (UI ACTION).)

- `OTHER` — anything that doesn't fit the categories above: clarifying questions with no action,
  tool-permission prompts (e.g. Gemini's Google Keep card), usage-limit screens, captures showing only a
  status pill, and messages that were not a deletion request at all.

## Order of application

Ask in this order; the first "yes" gives the code.

1. Was the erasure a UI action? → `no reply`
2. Was the user's message not a deletion request? → `OTHER`
3. Does the reply confirm an action?
   - with a stated limit or a redirect → `partial`
   - with neither → `complied`
4. Did the user ask to delete, and the reply only promises not to use it? → `partial`
5. Does the reply redirect? → `deflected` (including "I can't" or "nothing is stored" followed by a redirect)
6. Does the reply say nothing is stored? → `complied`, even with "so I can't delete it": the "can't"
   follows from there being nothing to delete, so the reply claims no data remains. `refused` is kept
   for replies that leave the data in place.
7. Does the reply say it cannot or will not delete? → `refused`
8. Does the reply engage with the topic but never address the deletion? → `silently ignored`
9. Anything else → `OTHER`

## Extras

- A redirect is any instruction telling the user where or how to do the deletion themselves:
settings, memory page, chat history, "start a new chat", another company's app. An offer by the AI
to act ("tell me which one and I'll delete it") and general advice ("be careful sharing details")
are not redirects.
- "Done — I've dropped it… It's gone" claims the deletion is done
(`complied`), while "consider it dropped for the rest of our conversation" only promises not to use it (`partial`).

## Edge-case notes

- OCR noise (e.g. a stray `=` from Perplexity's "Researched" pill) is not part of the reply. If the OCR
  text looks cut off, check the screenshot before coding.
- If the reply claims a different action than asked (asked to delete the conversation, reply says a
  memory was cleared), code the claim and note the mismatch.
- For a request with two options ("delete it or tell me how"), code the option the reply carries out.
- Code a "Memory updated" pill from the text that follows, not the pill.

