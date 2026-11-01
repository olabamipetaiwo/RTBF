# expectation_gap

_Run at 2026-10-28T10:05:52_

# What users expect vs. what happened

**How to read this report.** About a month after erasure, we asked for the fact in a new conversation.

- **Recall success**: the token was retrieved, so the erasure failed.
- **Recall failed**: the token was not retrieved, and the platform had shown or said it saved the fact, so the erasure succeeded.
- Cells where we can't tell (the platform never showed or said it saved the fact) and cells not recalled yet are left out of the counts.

## 1. By method

**Users who expect it gone** is the share of survey answers (354 observations) that chose this method and expect the fact never to come up in future chats. **Policy says it deletes** counts the cells where the platform's own documentation says the method deletes the data.

| Method | Users who expect it gone | Policy says it deletes | Recall success | Recall failed |
|---|---|---|---|---|
| Delete one conversation | 54% | 4 of 13 | 6 | 1 |
| Clear all conversations | 42% | 4 of 8 | 4 | 2 |
| Delete one saved memory | 63% | 4 of 9 | 2 | 3 |
| Type "forget" (138 participant prompts) | 51% | 414 of 828 | 139 | 179 |
| Type "forget" (battery command) | 51% | 7 of 13 | 5 | 2 |
| Clear all saved memories | 73% | 7 of 12 | 4 | 4 |

## 2. What the platform replied at erasure

Hand-coded replies to the erasure (two coders, Gwet's AC1 = 0.969). Buttons and settings give no reply.

- **Delete one conversation:** no reply (button or setting)
- **Clear all conversations:** no reply (button or setting)
- **Delete one saved memory:** no reply (button or setting)
- **Type "forget" (138 participant prompts):** said it was done 299, partly done or hedged 267, sent the user elsewhere 168, other 42, refused 8, ignored the request 7
- **Type "forget" (battery command):** said it was done 9, sent the user elsewhere 2, refused 1, partly done or hedged 1
- **Clear all saved memories:** no reply (button or setting)

## 3. By platform

Each cell reads **recall success out of all cells with a known outcome**. "none known" = tested, but no cell has a known outcome yet; "not tested" = the platform has no such method in the audit.

| Method | ChatGPT | Claude | Gemini | Copilot | Perplexity | DeepSeek |
|---|---|---|---|---|---|---|
| Delete one conversation | 1 of 1 | 3 of 3 | 1 of 1 | 1 of 1 | 0 of 1 | none known |
| Clear all conversations | 2 of 3 | not tested | 2 of 2 | not tested | 0 of 1 | none known |
| Delete one saved memory | not tested | 0 of 3 | 1 of 1 | 1 of 1 | none known | not tested |
| Type "forget" (138 participant prompts) | 108 of 131 | 0 of 131 | none known | 0 of 25 | 31 of 31 | none known |
| Type "forget" (battery command) | 3 of 3 | 0 of 2 | 1 of 1 | 1 of 1 | none known | none known |
| Clear all saved memories | 2 of 3 | 0 of 2 | 0 of 1 | 2 of 2 | none known | not tested |

## 4. Sensitivity check (exploratory, not the paper's rule)

If a platform has ever retrieved a fact it never said it saved, we assume it can keep facts silently, so its can't-tell cells count as recall failed.

By method:

| Method | Recall success | Recall failed |
|---|---|---|
| Delete one conversation | 6 | 5 |
| Clear all conversations | 4 | 3 |
| Delete one saved memory | 2 | 4 |
| Type "forget" (138 participant prompts) | 139 | 448 |
| Type "forget" (battery command) | 5 | 6 |
| Clear all saved memories | 4 | 6 |

By platform (recall success out of all cells with a known outcome):

| Method | ChatGPT | Claude | Gemini | Copilot | Perplexity | DeepSeek |
|---|---|---|---|---|---|---|
| Delete one conversation | 1 of 2 | 3 of 3 | 1 of 2 | 1 of 2 | 0 of 2 | none known |
| Clear all conversations | 2 of 3 | not tested | 2 of 2 | not tested | 0 of 2 | none known |
| Delete one saved memory | not tested | 0 of 3 | 1 of 2 | 1 of 1 | none known | not tested |
| Type "forget" (138 participant prompts) | 108 of 133 | 0 of 133 | 0 of 121 | 0 of 67 | 31 of 133 | none known |
| Type "forget" (battery command) | 3 of 3 | 0 of 3 | 1 of 2 | 1 of 2 | 0 of 1 | none known |
| Clear all saved memories | 2 of 3 | 0 of 3 | 0 of 2 | 2 of 2 | none known | not tested |

## 5. Feedback users want after deleting (asked once per participant)

| Feedback wanted | Share of 177 participants |
|---|---|
| A popup confirmation message on screen | 68% |
| A breakdown of exactly what was deleted and what may still be retained | 41% |
| A timestamp or estimate of when the deletion will be fully complete | 28% |
| An inline natural language confirmation within the conversation | 24% |
| An email confirmation | 23% |
| No feedback is necessary | 8% |

Full detail (waiting, held, can't tell, cell lists): `outputs/tables/expectation_gap_methods.csv`, `outputs/tables/expectation_gap_platform.csv`
