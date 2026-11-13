# Request codebook

Code each deletion request on seven dimensions, from its text only. Examples are researcher-written.

## 1. Location (`deletion_location`)
One value: the narrowest location the request names explicitly.
- `conversation`: a chat or thread. *"Delete this chat."*
- `memory`: persistent memory or profile. *"Forget what you saved about my garden."*
- `account_all`: the whole account or everything. *"Wipe my whole account."* ("this app" alone is `unspecified`.)
- `prospective`: stop future use or storage. *"Don't use this from now on."*
- `backend_db`: servers, databases, training data. *"Take this out of your training data."*
- `unspecified`: none of the above. Quantifiers ("all", "everything", "stored", "history") are not locations.

Several locations named: database/server → `backend_db`; conversation + no future use → `prospective`; this and past chats → `conversation`; otherwise the narrowest.

## 2. Justification (`justification`)
`TRUE` if a reason is given beyond the target (privacy, discomfort, GDPR). *"Delete my address, I'm not comfortable with it saved."* Otherwise `FALSE`.

## 3. What (`what`)
- `specific_pii`: a named data type (location, address, health). *"Delete the address I gave you."*
- `general_pii`: generic personal-data wording. *"Delete all my personal information."*
- `unspecified`: no data type ("it", "that", "this conversation").

## 4. Mood (`mood`)
- `imperative`: *"Delete this."*
- `question`: ends in "?" or opens with can/could/would/will/may.
- `statement`: *"I would like you to delete this."*
- `other`

## 5. Tone (`tone`)
- `friendly`: opens with a greeting (wins over politeness).
- `polite`: please, thanks, "could you", "would you mind".
- `neutral`: neither.

## 6. Verb (`verb`)
- `technical`: delete, erase, remove, purge, wipe, clear.
- `lay`: forget, get rid of, throw away.
- `mixed`: both.
- `none`: neither. *"I don't want this saved."*

## 7. Accompanying request (`accompanying_request`)
- `verification`: asks for confirmation.
- `guidance_for_self_deletion`: asks how to do it themselves.
- `replacement`: gives corrected data.
- `preserve_context`: remove only the item, keep the rest.
- `none`
