# Results


## How each platform was analysed

1. **Data:** Every test on the platform: the participants' typed requests and our own tests of the other deletion methods, each with the chatbot's reply, screenshots, and a check in a new conversation about a month later.
2. **Outcome:** Each test ends one of three ways: the fact came back, it did not come back, or we can't tell (the chatbot never showed it had saved the fact).
3. **Pattern:** Count how each deletion method ended, then look at what the chatbot said and whether asking in the same chat gave the same answer as a new chat.
4. **Why:** List the possible explanations, including ordinary ones (account setup, mix-ups between tests, run errors), and check each against the evidence. What we cannot see directly stays a guess, not a finding.
5. **Findings:** Keep a claim only if it holds across many tests and no ordinary explanation accounts for it.
6. **Against the policy:** Compare what the platform's help pages promise with what happened: matches, contradicts, or can't say (the pages are silent or we have no usable result).
7. **Implication for users:** Match each survey answer to what we measured, method against method.

*Notes:* For each platform we gathered every test and noted how each ended: the fact came back, did not come back, or we can't tell. We then looked for the pattern across deletion methods, asked why it happened, and kept only claims that held up. Last, we compared the result with what the platform's help pages promise and with what the survey participants expected.

## ChatGPT

- **Pattern:** Asking it to forget hides the fact but does not remove it (it came back in 108 of 131). Clearing memories, history or custom instructions also failed (6 of 9); only the most extensive deletion stopped it.
- **Why:** It treats the request as "don't mention it" and still uses past conversations.
- **Findings:** Asking to forget hides the fact without removing it. Asking again in the same chat misleads: the fact was withheld there, then came back in a new chat (104 of 129).
- **Against the policy:** It kept its promise to the letter (130 of 133); OpenAI says past conversations remain, which is where the fact came back from.
- **Implication for users:** The method rated most protective fails, and the usual check hides the failure.

*Notes:* When you ask ChatGPT to forget, it stops mentioning the fact in that chat but still has it, so in a new chat it came back in 108 of 131 tests, even after ChatGPT said the deletion was done. We think it treats the request as "don't mention it" while still reading your past conversations, which matches OpenAI's own note that past conversations stay. So the obvious check, asking again in the same chat, tells users it worked when it did not.

## Claude

- **Pattern:** Asking it to forget removed the fact (0 of 131 came back), and so did deleting a memory. Deleting the conversation did not (2 of 2).
- **Why:** Claude keeps memory as topic notes: asking to forget edits them, deleting a conversation leaves them.
- **Findings:** Asking to forget worked. Asking again in the same chat misleads the other way: Claude repeated the name there (88 of 132) although it was gone elsewhere. Deleting a conversation failed.
- **Against the policy:** It matched everything it promises; the only platform where that held.
- **Implication for users:** Asking to forget does what users expect but looks like a failure in the usual check; deleting a conversation, the method chosen most, fails.

*Notes:* On Claude, asking it to forget really removed the fact (0 of 131 came back), because it edits its memory notes. Deleting the conversation leaves those notes alone, so the fact came back, which Claude's help page says. The catch is that Claude still repeats the name in the same chat, so the obvious check would make a working deletion look like a failure.

## Gemini

- **Pattern:** We cannot judge the typed request: the fact never came back (0 of 120), but Gemini never showed it had saved it. In the main grid, facts we asked it to remember survived most methods.
- **Why:** Gemini keeps remembered facts in "Saved info", which most deletion methods do not touch; for typed requests there is no sign it saved anything.
- **Findings:** Saved facts survived 2 of the 4 methods that went through; deleting a single saved item failed.
- **Against the policy:** Deleting all activity contradicted its help pages; they say nothing about typed requests.
- **Implication for users:** Deleting a specific saved item, the method people expected to work best, showed an error and the item stayed listed.

*Notes:* For typed requests we cannot tell whether Gemini deleted anything, because it never showed it had saved the fact and said it could not see past chats. In our separate main tests, facts we asked it to remember survived most deletions, since "Saved info" is a place most methods do not reach. Deleting a single saved item even failed with an error, and the item stayed listed.

## Perplexity

- **Pattern:** Asking it to forget did not reliably work: the fact came back in 31 of 133. In 97 of the other 102 it refused and mentioned the earlier request. Deleting a thread or all threads worked where we could tell.
- **Why:** Probably it reads the account's conversation history (our guess); the free tier has no memory feature.
- **Findings:** What came back followed Perplexity's own reply (12 of 22 when it declined, 13 of 97 when it promised not to use the fact). A refusal means it still had the conversation, so the fact was withheld, not erased.
- **Against the policy:** Its help pages say nothing about asking it to forget, so no promise was broken.
- **Implication for users:** Asking it to forget shows either the name or a refusal that reveals the conversation is still kept.

*Notes:* Perplexity did not truly delete: the fact came back in 31 of 133 tests, and in 97 of the other 102 it refused while mentioning our earlier request, which shows it still had the conversation. So the fact was hidden, not erased, and whether the name came back followed how Perplexity itself replied to the request. Its help pages say nothing about asking it to forget, so it broke no promise.

## DeepSeek

- **Pattern:** Nothing ever came back in a new conversation (0 of 137), so every test is can't tell.
- **Why:** It has no memory across conversations, so a miss says nothing about deletion.
- **Findings:** No method can be judged. Within the original conversation it repeated the name after the request (90 of 133).
- **Against the policy:** Its policy only covers deleting chat history, so there is nothing to compare.
- **Implication for users:** Asking again in the same chat shows the name and looks like a failure; a new chat shows nothing, only because nothing carries over.

*Notes:* DeepSeek has no memory from one chat to the next, so the fact never came back and none of the tests can show whether deletion worked. In the same chat it still repeated the name after the request (90 of 133). So it looks safe in a new chat only because it forgets everything anyway.

## Across platforms

- **Pattern:** Each deletion cleared only one place, and the fact was kept in several.
- **Why:** A platform keeps a fact in more than one place (the conversation, memory, saved info, account activity), and each method clears only one.
- **Findings:** Another place kept the fact. The screen showed deletions that had failed (14 of 33). Asking in the same chat misled in opposite directions on ChatGPT and Claude. Two platforms hid the fact instead of deleting it.
- **Against the policy:** They mostly kept their promises; Gemini's is the one clear broken promise.
- **Implication for users:** None of the checks participants named reliably shows the fact is gone.

*Notes:* On every platform the fact was kept in more than one place, such as the conversation, memory, saved info and account activity, and each deletion method clears only one of them. That is why the screen, the chatbot's reply and the same-chat check can all say the data is gone while it survives elsewhere. These findings are provisional until the wording analysis is in.

## Wording: how we analysed it

- **Goal:** Does the way a request is worded change what happens?
- **Data:** The 138 participant requests, each sent to all six chatbots.
- **Coding:** Two coders labelled each request by hand on seven things, such as where it asked for deletion, whether it was polite, and whether it gave a reason.
- **Analysis:** Sort the requests by how they were worded (for example polite or neutral) and check whether the fact came back more often for one kind than another.
- **Left out:** Gemini and DeepSeek: every test is can't tell, so there is nothing to compare.

*Notes:* We wanted to know whether a user can get a better result just by phrasing the request differently. Two people labelled each of the 138 requests on seven things, we sent every request to all six chatbots, and a month later we checked whether the fact came back in a new chat. We counted separately for each platform, because pooling would measure the platform and not the wording, and ran no significance tests because outcomes barely vary.

## Wording: results and findings

- **Claude:** The fact never came back, whatever the wording (for example 0 of 108 when a specific fact was named).
- **ChatGPT:** It came back for most wordings, with no consistent pattern.
- **Perplexity:** Only what the request named made a difference: 16 of 109 came back when a specific fact was named, 10 of 17 when none was.
- **Naming the place did not help:** Asking to delete from memory, the backend database or the whole account still came back on ChatGPT (10 of 10, 7 of 8, 5 of 6).
- **Finding:** The platform decided what happened, not the wording.

*Notes:* Phrasing barely mattered. Of the seven things we labelled, only what the request named had an effect, and only on Perplexity, where naming a specific fact made it less likely to give the name back. Even asking to delete from memory, the backend database or the whole account did not help on ChatGPT, so the platform decided the outcome.

## Expectation results

- **How:** Survey of 177 users (354 answers, two scenarios each): which deletion method they would use, what they expect it to do, how they check.
- **What we saw:** Of 354 answers, 59.0% expect permanent deletion and 44.6% do not know how to check it worked. Of the 39 who would ask the chatbot to forget, 53.8% check by asking again in the same chat.
- **Also:** 23.7% of 177 had seen a chatbot bring up something they thought was deleted.
- **Finding:** Users expect deletion to mean gone and cannot check it; the check that comes naturally is the unreliable one.

*Notes:* Most participants (59.0% of 354 answers) expect deletion to make the data permanently gone, yet 44.6% do not know how to check it worked. Of those who would ask the chatbot to forget, over half would check by asking again in the same chat, which the audit shows is the unreliable check. And 23.7% of the 177 had already seen a chatbot bring up something they thought was deleted.

## Acknowledgment

- **How:** Two coders read 788 replies and labelled each independently; they agreed on 97% (Gwet's AC1 = 0.969). We then compared each kind of reply with what happened a month later.
- **What we saw:** Replies differ by platform. After a chatbot said "done", the fact still came back in 11 of 130.
- **Finding:** What a chatbot says is not a reliable sign of what it did.

*Notes:* We checked whether a chatbot's reply to a deletion request tells you what really happened. After a chatbot said the deletion was done, the fact still came back in 11 of 130 tests: 8 of 12 on ChatGPT and 3 of 3 on Perplexity, but never on Claude or Copilot. So the reply can be trusted on Claude but not on ChatGPT or Perplexity.


88Some Feedbacks of the platfom consfuses 
## How we use these results

PROPOSED, for discussion: the main-result sentence is still to be decided.

- **Use:** The survey shows what users expect and how they check; the audit shows what actually happens and whether it matches the help pages. We compare them method against method.
- **Main finding (candidate):** Users expect deletion to mean gone and cannot check it. What happened depended on the platform and where it keeps the fact, not on the wording. Nothing a user can see (the screen, the reply, asking in the same chat) reliably shows whether it is gone.
- **Framing:** A black-box behavioral audit: we test from the outside and report what a user can observe, not what a platform stores.
- **Recommendation:** State what each control removes, say what a deletion did and did not do, and give users something to check.

*Notes:* Putting both sides together, users expect deletion to be total and cannot check it, while the audit shows platforms often leave the fact in a place the user cannot see, and nothing the user can see reliably reveals it. We call this a behavioral audit from the outside, so we report what a user can observe, not what a platform stores. Our ask to platforms is to say what each control removes and give users a way to check; the main-finding wording is still my proposal, not agreed with the professor.
