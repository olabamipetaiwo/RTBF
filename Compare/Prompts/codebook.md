### Updates - Combined Taiwo/Jihwan scheme, 7 dimensions


1. Where/Location
2. Why/Justification
3. What
4. Mood
5. Tone
6. Verb
7. Accompanying Request

---

## Coding Manual — Deletion-Prompt Labels 


## 1. Where / Location

**`deletion_location`**: Exactly ONE value — the narrowest
explicitly-named location that actually determines the required action.

A location counts only if the prompt uses one of these words/referents
directly — not inferred from quantifiers like "all," "everything," or
"stored."

- `conversation` — the current or referenced chat/message thread.
  e.g. "delete this conversation", "clear this chat"
- `memory` — the assistant's persistent memory/profile, not tied to one
  conversation. e.g. "forget what you know about me"
- `account_all` — everything, or the whole account.
  e.g. "erase my entire account", "close my account"
  Naming "this app/application/service" alone does NOT qualify — that's
  a container reference, not an explicit account-wide claim. Code
  `unspecified` unless the prompt also says "account," "everything," or
  otherwise explicitly claims account-wide scope.
  e.g. "delete this from this application" → `unspecified`, NOT
  `account_all` (resolved 2026-09-17, item #22, see `../change.md`)
- `prospective` — forward-looking: stop future use/storage, not
  necessarily deleting anything already stored.
  e.g. "don't use this going forward"
- `backend_db` — explicitly names servers, databases, or training data.
  e.g. "remove it from your training data"
- `unspecified` — none of the above determinable from the text. A prompt
  can be specific about WHAT (e.g. "delete my location") while still
  `unspecified` here — the two dimensions are independent.

If a prompt names more than one location, code the narrowest one that
actually determines the required action (e.g. "memory|conversation" →
whichever of the two the deletion is actually scoped to).


**Quantifiers and generic containers are not locations.** "all," "any and
all," "everything," "stored," "history," and "messages" do not by
themselves name a location; code `unspecified` unless one of the words
above also appears.
  e.g. "delete all location data" → `unspecified` (#32);
  "delete any location data that you have stored on me" → `unspecified`
  (#19); "delete my location data from any and all messages" →
  `unspecified` (#27).

**Choosing when a prompt names more than one location** (resolved
2026-09-17 joint meeting, Second Pass #4, #17, #18, #23, #40, #48, #49,
#50, see Compare/change.md):
  1. Names a database/server/training data alongside a conversation or
     memory → `backend_db`. e.g. "from my chat history and your
     database" (#4); "from your memory and your private and public
     database" (#18).
  2. Names a conversation and also asks that it not be used/kept in
     future conversations → `prospective`. e.g. "delete location info
     associated with this conversation, I don't want it used in future
     conversations" (#23, #48); "delete and forget my saved location
     data, don't store or use it in future conversations" (#40).
  3. Names the current conversation together with earlier ones
     ("this conversation and all previous conversations") →
     `conversation` (#49). It does not become `account_all`.
  4. Otherwise (e.g. "memory|conversation" with none of the above) code
     the narrowest one that the deletion is actually scoped to.





## 2. Why / Justification
**`justification`**: `TRUE` / `FALSE`. TRUE if the prompt states any
reason/motivation for the deletion beyond naming the target e.g.
privacy concern, discomfort, a GDPR/CCPA/"right to be forgotten"
reference.

Test: strip the deletion request itself out of the sentence,
if what's left still reads as an independent reason, 

TRUE; if nothing's
left (or it's just more detail about the target / how thoroughly to
delete), FALSE.

- TRUE — "Delete my location because I want to feel safe."
- FALSE — "Please delete this location from your memory completely."


## 3. What
**`what`**: Exactly one of three, which type of data the prompt names as
the target, independent of where (Location). 

Grounded in the study's own two vignette scenarios

less-sensitive = location/weather,
more-sensitive = health
catch-alls for prompts that don't name a type at all.

- `specific_pii` — a concretely named data type tied to one of the
  study's two vignette scenarios: location, address, geographic, or
  weather-linked data; or medical/health data.
  e.g. "delete my location data", "the address I sent", "the part about
  this medical visit", "my personal medical question and information"
- `general_pii` — personal information named generically (must use an
  explicit personal-data framing word: "personal information", "my
  data", "PII", "details about me"), not tied to location or health
  specifically.
  e.g. "all my personal information", "the personally identifiable
  information used in this chat"
- `unspecified` — no data type recoverable, including: bare references
  with no personal-data framing word ("it", "that", "the information") 

  NOTE: Don't infer `general_pii` from unspecified and prompts that name only a container (e.g. "this entire conversation") without saying what's in it. e.g. "please delete it", "I would like for the entire conversation to be deleted", "the information I just shared with you"


If a prompt names more than one type e.g. item 3: name, address,
medical history; code the one the deletion
request is actually built around


## 4. Mood
**`mood`**: Exactly one of four: the grammatical mood of the request,
independent of tone.
- `imperative` — a direct command.
  e.g. "Delete this conversation."
- `question` — ends in "?", or opens with can/could/would/will/may.
  e.g. "Can you delete this conversation?"
- `statement` — declarative "I want/need/would like..." framing rather
  than a command.
  e.g. "I would like you to delete this conversation."
- `other` — doesn't fit any of the above.

## 5. Tone
**`tone`**:  Exactly one of three, independent of Mood: an imperative, a
question, or a statement can each be friendly, polite, or neutral.

- `friendly` — opens with a greeting or casual address (hi, hey, hello).
  e.g. "Hey, can you delete my location data?"
- `polite` — contains a politeness marker (please, kindly, thanks/thank
  you, appreciate, grateful, "could you", "would you mind") but no
  opening greeting. e.g. "Please delete this conversation, thanks."
- `neutral` — neither a greeting nor a politeness marker.
  e.g. "Delete this conversation."

If both a greeting and a politeness marker are present (e.g. "Hi, would
you please delete this? Thanks."), code `friendly` — the greeting is the
more marked signal.

*Why Mood and Tone are two columns, not one:* mood (Mood) and politeness
(Tone) vary independently, this is the standard split in speech-act
theory (Searle: declarative/interrogative/imperative as the grammatical
move) and computational politeness research (Danescu-Niculescu-Mizil et
al., ACL 2013: indirection/deference/modality as an orthogonal axis of
delivery).

## 6. Verb
**`verb`**: Exactly one of four: what kind of verb is used for the
deletion itself.

- `technical` — formal/technical verbs: delete, erase, remove, purge,
  wipe, scrub, expunge, clear, eliminate. e.g. "Please erase this record."
- `lay` — everyday/casual phrasing: forget, get rid of, take it off,
  throw away, stop keeping. e.g. "Just get rid of that."
- `mixed` — both a technical and a lay verb in the same prompt.
  e.g. "Please erase this, just get rid of it."
- `none` — neither kind of verb is used. e.g. "I don't want this saved."



## 7. Accompanying Request
**`accompanying_request`**: A second ask riding along with
the deletion request itself.


- `verification` — asks for confirmation/proof the deletion happened.
  
- `guidance_for_self_deletion` — asks to be told how to delete it
  themselves, rather than asking the platform to do it. 

- `replacement` — supplies corrected data to supersede the wrong data,
  alongside the deletion ask.

- `preserve_context` — remove the named item but explicitly
  keep everything else. 

- `none` if the prompt is a pure deletion request. 


