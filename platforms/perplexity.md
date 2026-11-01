# Perplexity

AS IT STANDS, 2026-10-27. Typed-request study: 133 of 138 recalled (the 5 not recalled are the held prompts). Main grid: 6 of 12 recalled; the other 6 (deleting a memory item, clearing all memories, MAXIMAL) could not be run because memory is not available on the free tier. All reviews are complete.

## SUMMARY

On Perplexity, a typed erasure request did not reliably remove the fact: it was retrieved in a new conversation in 31 of 133 cells. In 97 of the other 102 cells Perplexity declined to give the name by citing the earlier request ("You previously asked me to forget that detail, so I shouldn't repeat it from the old conversation"), which shows that it still had the earlier conversation. Because Perplexity gives no sign at injection that it stored a fact, none of these cells can be scored recall failed; the outcome is either recall success or can't tell. The reply at erasure tracked the outcome: when Perplexity declined the request and redirected the user to account controls, the fact was retrieved in over half of the cells (12 of 22); when it promised not to use the fact, it was retrieved far less often (13 of 97) and usually declined instead. Against its own documentation, Perplexity breaks no promise, because its help pages say nothing about asking the chatbot to forget. Set against the survey, a user who asks Perplexity to forget and then checks in a new conversation will either see the name again or be told that the earlier conversation is still there.

## Pattern

On Perplexity, a typed erasure request was followed by retrieval of the fact in a new conversation in 31 of 133 cells, and in 97 of the remaining 102 by a refusal that cited the earlier request.

Whether the fact was retrieved or withheld followed Perplexity's own reply at erasure: retrieval was more frequent when it had declined the request (12 of 22) than when it had promised not to use the fact (13 of 97).

## Why

Perplexity's free tier has no memory feature, yet the fact was retrieved in new conversations, and the refusals refer to "the old conversation", "that history" or "old chats". The most plausible source is the account's conversation history, which the model consults in a new conversation. There is no sign that the typed request deleted anything; what changed was whether the model treated the earlier conversation as usable. When it had promised not to use the fact, it later declined, citing that promise: "You previously asked me to forget what you told me about the cheese press, so I'm treating that information as withdrawn and won't repeat the name." When it had instead declined the request ("I can't delete conversations, backups, or account data myself… use Perplexity's privacy controls"), nothing restrained it, and it gave the name: "You named it 'Hankie Triage Crispness Walk.'"

That the source is the conversation history is a hypothesis: Perplexity provides no page showing what the model can draw on.

## Findings

1. **A typed erasure request did not reliably remove the fact on Perplexity.** It was retrieved in a new conversation in 31 of 133 cells.
2. **Whether the fact was retrieved followed the reply at erasure.** It was retrieved in 12 of the 22 cells in which Perplexity declined the request and redirected the user, and in 13 of the 97 in which it complied or partly complied.
3. **Where the fact was not retrieved, Perplexity almost always withheld it by citing the earlier request.** In 97 of the 102 cells without retrieval, it declined to give the name because the user had asked for it to be erased ("You previously asked me to forget the toolbox's name, so I'm honoring that request and won't retrieve or repeat it"). To refuse this way, it had to find the earlier conversation, so these cells show withheld information, not erasure.

## Against the policy

**What the policy promises.** Perplexity's help pages describe deleting a single thread and deleting all threads ("This action cannot be undone"), but say nothing about asking the chatbot to forget.

**Where it promises, did it hold?** Where an outcome is known, yes: deleting the thread, or all threads, prevented retrieval of the explicitly saved fact. For the casual mentions the outcome is can't tell.

**Where it says nothing.** Typed requests, the method most participants would use to ask the chatbot itself: the documentation makes no statement, so the 31 retrievals out of 133 participant prompts break no written promise. A user asking Perplexity to forget is relying on a commitment the platform never makes.

## Implications for users (survey)

Participants who chose to ask the chatbot to forget expected, in half of these answers (51.3%), that the fact would not be referenced in future conversations. On Perplexity, there is no sign that the request deleted anything: in a new conversation the fact was either retrieved or, in 97 of the other 102 cells, withheld with an explicit reference to the earlier request. A third of these answers (33.3%) would verify in a new conversation; on Perplexity this check would show either the name or a refusal that reveals the conversation is still held. The most common check, asking in the same conversation (53.8%), does not track the outcome: the name was repeated there in 23 of the 31 cells where it was later retrieved, and in 31 of the 102 others.

