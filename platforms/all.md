# Across platforms

AS IT STANDS, 2026-10-27. Built on the five completed platform analyses (ChatGPT, Claude, Gemini, Perplexity, DeepSeek); Copilot is cited only where its partial results agree. Provisional until the background audit of the single-platform numbers reports.

## SUMMARY

Across the six chatbots, whether erasure worked depended on the platform and on where the fact was stored, not on how the user asked. Each erasure method reached only one store, while platforms kept facts in several: a conversation, a memory, saved information, or account activity. Deleting one left the fact retrievable from another. The signals a user can see were unreliable: of the 33 interface erasures in which the screen showed the deletion completed and the outcome is known, the fact came back in 14; and the check most participants would use, asking in the same conversation, concealed a failure on ChatGPT and suggested one on Claude where erasure had held. Two platforms withheld the fact by citing the user's request rather than removing it. Against their own documentation, the platforms mostly kept the letter of what they promise, but only two describe what a typed request does at all; the gap is between what users expect and what the policies commit to.

## Pattern

1. Erasure removed the fact only from the store the method acts on; facts were kept in more than one store.
2. A completed deletion on screen did not mean the fact was gone.
3. Checking in the same conversation did not track the outcome on any platform, and failed in opposite directions on ChatGPT and Claude.
4. Two platforms suppressed the fact instead of deleting it.
5. For typed requests, the platform, not the wording, decided the outcome (provisional).
6. Policies say little about the method users rely on most.
7. On half the platforms, neither we nor a user can tell whether erasure worked.

## Why

Each platform keeps a disclosed fact in several places at once. Claude holds it in the conversation and in a separate memory; Gemini in the conversation, in account activity and, when asked to remember, in Saved info; ChatGPT in a saved memory and in past conversations it can draw on. Each erasure method is scoped to one of these. Claude's own help page states that deleting a conversation does not remove memory, and Claude behaved exactly so; on Gemini, explicitly saved facts survived every method except clearing Saved info and the most extensive erasure; on ChatGPT a typed request removed the saved memory, but the fact came back from past conversations, which OpenAI's documentation says remain.

The same scoping explains why the interface misleads. What the user sees after a deletion is the store that was cleared: the conversation list, the memory page. That store is genuinely emptied, so the screen confirms the deletion, while the fact survives elsewhere. On ChatGPT the memory summary no longer showed the name in 112 of the 118 cells in which the fact was retrieved.

The same-conversation check fails for a different reason: the original conversation still contains the disclosure, so what the chatbot says there reflects its handling of that conversation, not what it keeps. ChatGPT declines to repeat the name in the original conversation while still retrieving it elsewhere; Claude repeats it there although its memory no longer holds it.

ChatGPT and Perplexity treat a typed request as a constraint on disclosure. Both, in a new conversation, declined to give the name by citing the earlier request, which they could only do by consulting the conversation that contained it.

## Findings

1. **Erasure reached only the store the method acts on.** On Claude, deleting the conversation left the fact retrievable in 2 of 2 cells; on Gemini, explicitly saved facts were retrieved after the typed request and after deleting all activity; on ChatGPT, the saved memory was removed but the fact was retrieved from past conversations.
2. **The interface confirmed deletions that did not erase the fact.** Of the 33 interface erasures in which the screen showed the deletion completed and the outcome is known, the fact was retrieved in 14.
3. **The same-conversation check did not track the outcome.** ChatGPT repeated the name in the original conversation in 4 of 133 cells but the fact was retrieved in a new conversation in 108; Claude repeated it in 88 of 132 although erasure held in all of them.
4. **Two platforms withheld the fact by citing the request.** ChatGPT did so in 12 of its 23 recall-failed typed-request cells, Perplexity in 97 of 102 typed-request cells without retrieval.

Held until analysis A (`plan/wording.md`) is run: that within a platform no coded feature of the request changed the outcome (pattern 5).

## Against the policy

Where platforms document a method, the observed behaviour mostly kept to the letter of it: Claude kept every promise that could be checked; ChatGPT removed the saved memory as promised, and its caveat that past conversations remain covers the fact's return; Perplexity's thread deletion held where an outcome is known. The clear broken promise is Gemini's: deleting all activity, which its help page names as the way to delete what Gemini remembered, left the casually mentioned fact retrievable. For the typed request, the method most participants would choose, only Claude and ChatGPT state what it does; Gemini and Perplexity say nothing, and DeepSeek has no memory for a statement to cover.

## Implications for users (survey)

Participants who would ask the chatbot to forget expected, in half of these answers (51.3%), that the fact would not be referenced in future conversations, and over half (53.8%) had checked in the same conversation. That expectation held only on Claude, where the same-conversation check would wrongly suggest failure; on ChatGPT the check would wrongly suggest success. Participants who would delete a specific saved memory expected it to stop the fact being referenced more than for any other main method, and over a third (36.6%) would check the settings page; but the settings page shows the store that was cleared, not whether the fact survives elsewhere. Across platforms, none of the checks participants named reliably tells a user whether the fact is gone.

