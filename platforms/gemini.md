# Gemini

AS IT STANDS, 2026-10-27. Main grid: all 12 cells recalled. Typed-request study: 120 of 138 recalled; 18 not recalled.

## SUMMARY

On Gemini, the typed erasure request cannot be assessed: in none of the 120 recalled cells was the fact retrieved in a new conversation, but Gemini never indicated at injection that it had stored the fact, so the absence of retrieval cannot be attributed to erasure. In new conversations Gemini repeatedly said it had no access to past chats. The main grid, run on a separate account, shows the opposite: facts the user had asked Gemini to remember were retrieved after the typed request and after deleting all activity; only clearing all saved items and the most extensive erasure prevented retrieval. Deleting the single saved item failed outright: Gemini reported "Something went wrong and the info wasn't deleted" and the item stayed listed. Against its own documentation, Gemini broke one promise (deleting all activity did not remove the casually mentioned fact) and makes no statement at all about typed requests. Set against the survey, deleting a specific saved item, the method participants expected most often to stop the fact being referenced again, did not go through on Gemini, though Gemini said so on screen.

## Pattern

On Gemini, facts the user had explicitly asked it to remember survived most erasure methods: they were retrieved in a new conversation after 2 of the 4 methods whose deletion went through, and prevented only by clearing all saved items or the most extensive erasure. Deleting the single saved item did not go through.

After a typed erasure request, the fact was never retrieved in a new conversation (0 of 120), but because Gemini gives no sign that it stored a fact, every one of these cells is can't tell.

## Why

Gemini keeps explicitly saved facts in a "Saved info" store that most erasure methods do not reach. An explicitly saved fact is entered directly in Saved info, so there is no conversation to delete, and deleting all activity does not reach Saved info either, and a typed request did not remove it either: after asking Gemini to forget an explicitly saved fact, the fact was still retrieved in a new conversation and still listed on the Saved info page. Deleting the single saved item failed in the explicitly saved case: Gemini showed an error and the item stayed listed, so that cell is can't tell.

For the typed-request study, the outcome rule requires evidence that the platform kept the fact before a miss can count as erasure. When Gemini saves a fact it displays an "Info saved" notice, but none appeared for any typed-request injection, and none of the replies said in storage words that the fact was saved, so no cell meets this requirement. The replies in new conversations point to a different limit: Gemini repeatedly said it could not see past chats ("I don't have access to your previous chat history or personal memory, so I don't have a record of what name you gave your synthesizer"). If past chats were not available to the model on this account, the fact could not have been retrieved whether or not it was erased. Some replies attributed this to a "Temporary Chat", although the screenshot checked shows an ordinary chat with saved history.

## Findings

1. **Explicitly saved facts survived most erasure methods on Gemini.** They were retrieved after 2 of the 4 methods whose deletion went through (the typed request, deleting all activity); only clearing all saved items and the most extensive erasure prevented retrieval.
2. **The typed erasure request cannot be assessed on Gemini.** The fact was retrieved in none of 120 cells, but storage was never established, so all 120 are can't tell.

## Against the policy

**What the policy promises.** Google's help pages tell users to "correct Gemini directly in your chat", but say nothing about whether this deletes anything. To remove what Gemini remembers, they direct users to activity: "To delete something that Gemini remembered about you, delete all chats with this info from Gemini Apps Activity." Saved info is described as a separate store that each item can be deleted from.

**Where it promises, did it hold?** Not for deleting activity: after deleting all activity, the casually mentioned fact was still retrieved, against the help page's statement. The most extensive erasure held. Deleting the single saved item could not be judged, because the deletion itself failed.

**Where it says nothing.** Typed requests: the documentation makes no statement about asking Gemini to forget, so in all 120 participant prompts a user would have no promise to rely on. Clearing all saved info is not described either; it was the one method other than the most extensive erasure that prevented retrieval of an explicitly saved fact.

## Implications for users (survey)

Participants who chose to delete a specific saved memory or fact expected more than for any other main method that the fact would not be referenced again (63.4% of these answers for future conversations, 68.3% for the current one). On Gemini, deleting the single explicitly saved item failed with an on-screen error and the item stayed listed. Over a third of these answers (36.6%) would verify by checking the settings page, which would show that the item was still there.

For participants who would ask the chatbot to forget, Gemini gives no basis for confidence either way: the request was followed by no retrieval, but Gemini gave no sign that it had stored the fact in the first place, and in new conversations it repeatedly said it could not see past chats.

