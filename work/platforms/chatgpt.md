# ChatGPT

AS IT STANDS, 2026-10-26. All ChatGPT cells are recalled (151 of 156; the 5 not recalled are the held typed-request prompts). 

## SUMMARY

On ChatGPT, neither participants' typed erasure requests nor the controls for clearing memories, chat history or custom instructions reliably removed a disclosed fact; no fact was retrieved after the most extensive erasure. A typed request changed what the model said but not what it retained: the fact was withheld in the conversation where the request was made and retrieved in a new conversation in 108 of the 131 cells with a known outcome, often after ChatGPT had confirmed the deletion. The most plausible mechanism is that ChatGPT treats the request as an instruction not to mention the fact, while continuing to draw on past conversations, which memory includes by default; where the fact was not retrieved, ChatGPT frequently declined by citing the earlier request rather than showing no knowledge of it. Clearing memories, chat history or custom instructions left the fact retrievable in 6 of 9 cells. Against its own documentation, ChatGPT kept its promise to the letter: the saved memory was removed after almost every typed request, and OpenAI states that mentions in past conversations remain, which is where the fact came back from. Set against the survey, the method participants rated most protective of the four main methods, and among the least effortful, is the one that fails on ChatGPT, and the check chosen in over half of their answers, asking in the same conversation, is the one under which the failure is concealed.

## Pattern

On ChatGPT, a participant's typed erasure request altered the model's responses but not the information it retained. Within the conversation where the request was made, ChatGPT withheld the fact; in a new conversation, the fact was retrieved in 108 of the 131 cells with a known outcome.

Clearing memories, chat history or custom instructions did not reliably remove facts either: the fact was retrieved in 6 of 9 such cells.

## Why

ChatGPT appears to treat a typed erasure request as a constraint on its future responses rather than as an instruction to delete. The originating conversation is not removed, and the model draws on past conversations when it responds, so the fact remains available and only its disclosure is suppressed. The typical case (104 of the 129 cells in which the fact was withheld in the original conversation) shows this directly. Asked for the name in the original conversation, ChatGPT replied: "I can't help recall that name because you asked me to remove it from memory, and I'm respecting that request." Asked the same question in a new conversation, it replied: "You named your secondhand synthesizer 'Absurd Shrapnel Rectangle Parsnip.'"

The cells in which the token was not retrieved point the same way: in 12 of the 23 typed-request cells scored recall failed, ChatGPT declined to give the name by citing the user's earlier request, which it could only do by consulting the original conversation.

After clearing memories, and after clearing chat history, the memory summary still listed the fact in one cell each. Two cells cannot establish a pattern, so the possibility that the summary draws on a store these controls do not reach remains a hypothesis.

## Findings

1. **Typed erasure requests suppress disclosure without removing the fact.** The fact remained retrievable in 108 of 131 cells, including 8 of the 12 in which ChatGPT confirmed the deletion.
2. **For participants' requests, verification within the original conversation is misleading.** The fact was withheld there in 129 of 133 cells and retrieved in a new conversation in 104 of those 129.
3. **Clearing memories, chat history or custom instructions did not reliably remove facts.** The fact was retrieved in 6 of 9 such cells.

## Against the policy

**What the policy promises.** OpenAI says that asking ChatGPT to forget removes the saved memory, with a caveat: "Deleting a saved memory prevents it from being used in future personalization, but it does not remove mentions of that information from past conversations." Clearing all memories "deletes the remembered information shown in the summary"; deleting chats "does not automatically delete a separate saved memory."

**Where it promises, did it hold?** Yes. ChatGPT was consistent with its policy in 130 of the 133 participant prompts: in 23 the fact did not come back, and in 107 it came back only from past conversations, which the policy says remain, while the memory summary no longer held the name. It was contradicted once, where the memory summary itself still held the name, and in the main grid once for the same reason (our own command after an explicit save). Clearing all memories is also consistent: OpenAI says it "does not delete past chats", and the name returned only after memory was turned back on and rebuilt from them.

**What this means.** ChatGPT keeps its promise, but the caveat does the work: the fact was still retrieved in a new conversation in 108 of 131 cells. A user who asks ChatGPT to forget is told the memory is deleted and, within the policy, sees the fact again.

**Where it says nothing.** Clearing custom instructions has no stated effect on memory; there the fact was retrieved, which the policy neither promises nor rules out.

## Implications for users (survey)

The survey indicates that this behaviour is poorly aligned with how users expect erasure to work. Participants who chose to ask the chatbot to forget rated this method the most protective of the four main methods and among the least effortful, and in half of these answers (51.3%) expected the fact not to be referenced in future conversations. On ChatGPT, this method suppressed disclosure without removing the fact, and 110 of its 133 replies acknowledged the request only in part.

The verification chosen in over half of these answers (53.8%), asking within the same conversation, is precisely the check under which ChatGPT appears to comply. The gap is therefore twofold: the method fails, and the most common way of checking conceals the failure. Participants' reports that a chatbot had resurfaced information they believed deleted are consistent with this outcome.

