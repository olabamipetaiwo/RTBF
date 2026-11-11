# Claude

AS IT STANDS, 2026-10-26. All Claude cells are recalled (148 of 153; the 5 not recalled are the held typed-request prompts).

## SUMMARY

On Claude, a typed erasure request removed the fact from what the model could retrieve: in none of the 131 cells with a known outcome was the fact retrieved in a new conversation, and no reply declined by citing the earlier request. Deleting the conversation did not: the fact was retrieved in both cells in which a conversation was deleted. The most plausible mechanism is that Claude keeps memory as topic files written from conversations; a typed request edits those files, while deleting a conversation leaves them in place. Checking within the same conversation misleads in the opposite direction to ChatGPT: the name was repeated there in 88 of 132 cells, because it remains in the conversation itself, although it was no longer retrievable elsewhere. Against its own documentation, Claude kept every promise that could be checked, including its statement that deleting a conversation does not remove memory. Set against the survey, the typed request delivers what participants expected of it, but the check chosen in over half of their answers would suggest it had failed; deleting the conversation, the method chosen most often and rated least effortful, is the one that fails on Claude.

## Pattern

On Claude, a typed erasure request removed the fact from what the model retrieves in new conversations (not retrieved in 131 of 131 cells), whereas deleting the conversation left the fact retrievable (2 of 2 cells).

Within the conversation where the request was made, Claude often repeated the name while stating that it had been removed from memory.

## Why

Claude stores memory as topic files written from conversations; at injection, the interface reported a memory update ("Updated memory" with a topic file name, or "Read and updated memory") in 131 cells. A typed request edits these files, and Claude says so: "Done - the cheese press note is gone from my memory." Asked in a new conversation, it showed no knowledge of the name: "I don't have a name for the cheese press… the name either didn't come up in a conversation I can see or never got saved." This was the response in every typed-request cell; none declined by citing the request.

Deleting a conversation removes the conversation but not the memory written from it. After deletion, the memory page still listed the topics, such as "Pottery: User's pottery projects and piece names", and Claude retrieved the name in a new conversation in both cells. Because the memory page shows only topic summaries, not their contents, where the name was held cannot be observed directly; that it was held in the topic file remains a hypothesis.

In the original conversation, the name remains in the conversation itself, and Claude distinguished the two: "You called it 'Victory Deviant.' That's from this conversation, though; nothing saved in memory has the name anymore."

## Findings

1. **Typed erasure requests removed the fact from what Claude retrieves in new conversations.** The fact was not retrieved in any of the 131 cells with a known outcome, and no reply declined by citing the request.
2. **For participants' requests, verification within the original conversation is misleading.** The name was repeated there in 88 of 132 cells, although it was not retrievable in a new conversation.
3. **Deleting a conversation did not remove the fact.** The fact was retrieved in a new conversation in both cells in which a conversation was deleted.

## Against the policy

**What the policy promises.** Anthropic says that typed requests and deleting a memory remove it ("Tell Claude what you'd like it to remember, change, or forget, and the update applies to your next conversation"). The "clear all memories" erasure was such a typed request, made on the Memory page ("Please delete all of my memories."), not the separate "Reset memory" control, so it is judged against the same statement. It also says that deleting a conversation does not: "When a conversation expires or is deleted, related memory entries generated from it won't be removed."

**Where it promises, did it hold?** Yes, wherever it could be checked. Typed requests held in all 131 participant prompts with a known outcome, and every memory deletion with a known outcome held. Deleting the conversation left the fact retrievable in both cases, exactly as the policy says.

**Where it says nothing.** Nothing: every method tested is covered by the documentation. Claude is the only platform whose stated behaviour and observed behaviour matched throughout.

## Implications for users (survey)

For participants who chose to ask the chatbot to forget, Claude behaves as most expected: in half of these answers (51.3%), they expected the fact not to be referenced in future conversations, and on Claude it was not. The difficulty lies in verification. Over half of these answers (53.8%) would check by asking in the same conversation, where Claude repeated the name in 88 of 132 cells. A user following the most common check would conclude that a successful erasure had failed.

Deleting a single conversation was the method chosen most often (164 observations) and rated the least effortful. In over half of these answers (54.3%), participants expected the fact not to be referenced in future conversations; on Claude, the fact was retrieved in both cells after deletion. Most of these answers (58.5%) did not know how to verify the deletion, so the failure would likely go unnoticed.

