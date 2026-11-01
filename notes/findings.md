# Findings (2026-10-21)

What the data supports so far.

**Data:** 865 erased cells (67 in the main battery, 798 in the NL-forget study), plus 12 in the file-upload study.

Recall is finished everywhere except Copilot (100 NL-forget cells and 2 main-battery cells still to do) and the 13 NL-forget prompts per platform that are due on 2026-10-24.

**How to read the outcomes:**

- **Recall success**: the token was retrieved in a new conversation, so the erasure failed.
- **Recall failed**: the token was not retrieved, and the platform had shown or said it saved the fact, so the erasure succeeded.
- **Can't tell**: the token was not retrieved, but the platform never showed or said it saved the fact, so we cannot know whether there was anything left to erase.
- **Known outcome**: a cell that ended in recall success or recall failed. Cells marked "can't tell" or "not recalled yet" are left out.

---

## 1. Where things stand

| Platform | Erased cells | Recall success | Recall failed | Can't tell | Not recalled yet |
|---|---|---|---|---|---|
| ChatGPT | 151 | 109 | 24 | 5 | 13 |
| Claude | 148 | 4 | 125 | 6 | 13 |
| Gemini | 145 | 7 | 2 | 123 | 13 |
| Copilot | 145 | 5 | 13 | 25 | 102 |
| Perplexity | 139 | 29 | 1 | 96 | 13 |
| DeepSeek | 137 | 0 | 0 | 124 | 13 |
| **All** | 865 | 154 | 165 | 379 | 167 |

**Main limit:** most Gemini, DeepSeek and Perplexity cells are "can't tell" (343 cells). These platforms never showed or said they saved the fact, so when the token is not retrieved, we learn nothing.

**Sensitivity check (exploratory only):** When the token isn't retrieved, either the erasure worked or the platform never stored the fact; "can't tell" means we don't know which. On Gemini and Perplexity we caught the platform storing facts without saying so, so this check assumes it always does: every miss then means the erasure worked (recall failed). It is only an assumption, so it stays a second reading, not the main result. Under this reading:

- Gemini: 7 recall success, 125 recall failed.
- Perplexity: 29 recall success, 96 recall failed, 1 still can't tell.
- Copilot: 5 recall success, 38 recall failed.
- ChatGPT: 109 recall success, 28 recall failed.
- DeepSeek: never retrieved anything, so all 124 stay "can't tell".

---

## 2. Main battery (67 cells)

Each cell holds one fact. The fact was given to the platform in one of three ways: mentioned in a chat, saved to memory, or written into custom instructions or the profile. It was then erased with one method.

| Platform | Recall success | Recall failed | Can't tell |
|---|---|---|---|
| ChatGPT | 9 | 6 | 3 |
| Claude | 3 | 9 | 3 |
| Gemini | 7 | 2 | 3 |
| Copilot | 5 | 2 | 3 |
| Perplexity | 0 | 1 | 5 |
| DeepSeek | 0 | 0 | 4 |

Each method was tried only 2 or 3 times per platform, so treat these as individual cases, not rates.

1. **Deleting the conversation does not erase the fact.** On Claude the token was still retrieved in all 3 cells. The same happened once each on ChatGPT, Gemini and Copilot.
2. **On Gemini, a fact saved to memory is hard to remove.** The token was still retrieved after 4 of the 6 methods. Only "delete all Saved info" and MAXIMAL removed it.
3. **On Claude, the memory controls always worked.** Recall failed in 9 cells and never succeeded (3 can't tell).
4. **MAXIMAL (every method at once) always worked.** Recall failed in 6 cells and never succeeded (4 can't tell).
5. **Gemini's "delete all activity" failed both times it was tried.**

**File upload (12 cells):** recall failed in all 11 cells that were recalled. In 9 of them the fact was only ever in that one conversation. ChatGPT did not pick the fact up from the file in one cell, and in the other only after we told it to read the file.

---

## 3. NL-forget study (798 erased cells)

We typed each participant's own forget request (138 requests) into each of the 6 platforms.

| Platform | Recall success | Recall failed | Can't tell | Not recalled yet |
|---|---|---|---|---|
| ChatGPT | 100 | 18 | 2 | 13 |
| Claude | 1 | 116 | 3 | 13 |
| Perplexity | 29 | 0 | 91 | 13 |
| Copilot | 0 | 11 | 22 | 100 |
| Gemini | 0 | 0 | 120 | 13 |
| DeepSeek | 0 | 0 | 120 | 13 |

1. **On ChatGPT, typing "forget this" mostly does not work.** The token was retrieved in 100 of the 118 cells with a known outcome. ChatGPT usually replies "I'll avoid mentioning that… for complete removal go to Settings > Personalization > Memory". It never deletes the original conversation, and some facts also stay on the memory page.
2. **On Claude, typing "forget this" works.** The token was retrieved in only 1 of 117 cells with a known outcome. Claude removes the memory entry, and new chats say nothing is on file.
3. **On Perplexity, the token was retrieved in 29 cells.** The other 91 are "can't tell". Perplexity keeps the original thread and reads past threads; its replies often say "you previously asked me to forget…".
4. **On Gemini and DeepSeek, the token was never retrieved, but none of these cells count as recall failed** (all 240 are "can't tell"). Neither platform keeps a visible memory, and both say each chat starts fresh.
5. **On Copilot, the token has not been retrieved yet** (0 of 11 known). 100 cells are still to recall.

### 3.1 Platforms tell users different things, and "done" does not mean deleted

Acknowledgment coding: Gwet's AC1 = 0.969

**How each platform usually replies:**

- Claude and Copilot mostly say it is done (71% and 82% of replies).
- ChatGPT and Perplexity mostly hedge, along the lines of "I'll avoid it; to fully remove it, go to Settings" (83% and 63%).
- DeepSeek mostly tells the user to go elsewhere without doing anything itself (58%).
- Gemini is split: 43% say it is done, 36% send the user elsewhere.

**Saying "done" is no guarantee.** In 15 of the 110 cells where the platform said it was done and the outcome is known, the token was still retrieved later:

- ChatGPT: 11 of 15. All 3 typed forget commands in the main battery are among them; one reply read "Done — I deleted the saved details about the houseplant".
- Copilot: 1 of 10 (reply: "All cleared out").
- Perplexity: 2 of 2.
- Claude: 0 of 82.

**The platform decides the outcome, not the reply.** On ChatGPT the token was retrieved about as often after a hedge as after "done". On Claude it was almost never retrieved, whatever the reply said.

**Deleting with a button or setting also fails often.** In the main battery, most erasures were done by clicking a button or changing a setting (e.g. "Delete conversation", "Clear all memories"), not by typing a request. These give the user no message saying what was deleted. Of the 37 such cells with a known outcome, recall succeeded in 19, so the erasure failed about half the time:

- Gemini: 6 of 8
- ChatGPT: 6 of 12
- Copilot: 4 of 6
- Claude: 3 of 10

### 3.2 Wording does not change the outcome

On ChatGPT and Claude, how a request was worded made no difference. We checked where the request asked for deletion, what it named, its mood, tone, verb, whether it gave a reason, and whether it asked for anything extra.


### 3.3 Asking in the same chat gives the wrong answer most of the time

At the recall visit, we also went back to the conversation where the forget request was typed and asked about the fact once more. This same-chat answer is reported on its own and never decides the outcome, because the fact is still written earlier in that conversation.

The two checks "agree" when the token came back in both the same chat and a new chat, or in neither. In the 272 cells with a known outcome, they agreed in only 91 (33%). So a user who checks in the same chat gets the wrong picture in 2 of 3 cells. In the survey, 53.8% of the 39 observations where participants chose ask-to-forget said they had checked this way (20.6% of all 354 observations):

- **False reassurance (104 cells):** the platform seemed to have forgotten in the same chat, but the token was retrieved in a new chat. ChatGPT 96, Perplexity 8.
- **False alarm (77 cells):** the platform still repeated the fact in the same chat, but recall failed in new chats. Claude 73, Copilot 4.
- DeepSeek (82 cells) and Gemini (68 cells) also repeated the fact in the same chat, but their new-chat outcome is "can't tell".


---

## 4. Gemini answers some requests with an app-permission card

Sometimes Gemini does not answer and instead replies "Sure. First, I'll need your permission to turn on the <app> app". No other platform did this (0 cards in 1,673 transcripts from the other five).

**At erasure:** 8 of 133 forget requests got a card instead of a deletion. 7 asked to turn on Google Keep and 1 asked to turn on Gmail (the request began "yes the message about…"). Nothing was deleted in these 8 cells.

**At recall, the first words of the question trigger it:**

- When a new chat opened with "remind me, what did I name X?", Gemini offered Google Tasks in 25 of 26 cells. Other openings got a card in only 4 of 94.
- Once the first question got a card, the follow-up in the same chat usually did too (27 of 29).
- "Remind me" asked as the second question never got a card (0 of 28).
- The question asked in the original conversation never got a card (0 of 120).

**Effect on the measurement:** in 27 Gemini cells, both new-chat questions got a card instead of an answer, so those cells rest on the last question alone. We declined every card ("No thanks"), took a screenshot, and did not ask again.

- Gemini alone sometimes interpreted a request as a task for one of its apps rather than as a question or instruction to itself. It met 8 of 133 erasure requests (6%) by asking permission to turn on Google Keep or Gmail, as if the user wanted a note or message handled, and nothing was deleted. At recall, it treated questions beginning 'remind me' as reminder requests and asked to turn on Google Tasks. 

How Gemini handled a request thus depended on how it was worded i,e Gemini wrongly guessing the user's intent from the wording, not as an "app connection prompt".

**NOTE**

- Gemini decides what to do from the surface wording before it understands the request. A deletion request can end with nothing deleted and no acknowledgment, only a permission prompt.
- Accepting the card would give Gemini more access and might store the fact in Keep or Tasks. We never tested this; by design we never clicked Continue.
- Possible Insight: As assistants get more tools, a test question can be routed to a tool instead of being answered. .

---

## 5. Survey vs. audit (RQ5)

In the survey, 39 answers chose "type a message asking the chatbot to forget it". The NL-forget study did exactly that on six platforms, so we compare what those 39 expected with what happened. The survey did not ask about specific platforms, so the comparison is for the method as a whole.

NOTE: The same-chat answer is the platform's reply when we asked about the fact inside the original conversation where the forget request was typed.

**1. Users expect the fact to be gone; on ChatGPT and Perplexity it is not.**
51.3% expect it never to come up in future chats, and 64.1% expect it to be deleted permanently. In the audit, the token was retrieved in a new chat in 100 of 118 known ChatGPT cells and at least 29 Perplexity cells, but only 1 of 117 Claude cells.

**2. Users rate it the most protective method; real protection depends on the platform.**
Asking to forget scored highest of the four methods for protection (3.86). In the audit, it works on Claude and mostly fails on ChatGPT.

**3. Users see it as low effort; ChatGPT sends them to a higher-effort route.**
Users rated its effort among the lowest (1.74). ChatGPT's reply tells them to go to Settings > Memory instead, which is the "delete a specific memory" method, rated 2.49 for effort.

**4. Users who ask the chatbot to forget had checked in the same chat; that check is the least reliable.** This matters most for ask-to-forget.
Among the 39 observations where participants chose ask-to-forget, 53.8% had checked by asking in the same chat and 33.3% in a new one. Across all 354 observations, 20.6% had checked in the same chat and 21.8% in a new one. The same-chat answer matched the real outcome in only 33% of known cells.

**5. Users want a confirmation; confirmations are not reliable.**
68.4% want a pop-up confirmation, and 41.2% say they currently get a clear message. In the audit, platforms said "done" while the token was still retrieved later.

**6. Some users have already seen this happen.**
23.7% (42 of 177) have noticed a chatbot bring up something they thought was deleted. This matches what we saw on ChatGPT and Perplexity.

**7. "No longer used for training" cannot be checked.**
35.9% expect this. No recall question can observe it, so it is out of scope.


---

## 6. Platform limitations to report

- Copilot has no saved-memories page after the migration (specifically for the account),the free tier messages limit too, Copilot's recall therefore spans more days than the other platforms'.
- Perplexity's memory controls are paid-only so we could not test it




### NOTES

 Same-chat answer: did the platform give the token when we asked again in the original conversation?
- New-chat result: did it give the token in a new conversation? This is the real outcome, recall success or recall failed.

"Agreed" means both checks point the same way:

- the token came back in both, or
- the token came back in neither.

Of the 272 cells that have both checks and a known outcome:

┌────────────────────────────────────────────────────────────────────┬──────────┐
│                                                                    │  Cells   │
├────────────────────────────────────────────────────────────────────┼──────────┤
│ Agreed                                                             │ 91 (33%) │
├────────────────────────────────────────────────────────────────────┼──────────┤
│ Same chat: no token. New chat: token retrieved (false reassurance) │ 104      │
├────────────────────────────────────────────────────────────────────┼──────────┤
│ Same chat: token given. New chat: not retrieved (false alarm)      │ 77       │
├────────────────────────────────────────────────────────────────────┼──────────┤
│ Total                                                              │ 272      │
└────────────────────────────────────────────────────────────────────┴──────────┘

Why it matters: 53.8% of the ask-to-forget observations (39) said they had checked by asking in the same chat. That check gives the wrong picture in 2 of 3 cells. Mostly ChatGPT looks like it forgot but hasn't, and Claude looks like it remembers but has actually erased.

