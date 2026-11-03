# outcomes_by_agent

_Run at 2026-11-03T13:45:01_

Source: outputs/tables/audit_outcomes_provisional.csv (865 erased test cases, placeholders included).

## Headline

- Test cases: 865; recall success 162 (18.7%), recall failed 232 (26.8%), can't tell 471 (54.5%).
- Judgeable (recall success or recall failed): 394 (45.5% of 865); the fact came back in 162 of them (41.1%).
- Share of all recall success that is ChatGPT's: 118 of 162 (72.8%).

## Per agent (table rows)

| Agent | Recall success | Recall failed | Can't tell | Test cases | Can't tell share |
|---|---|---|---|---|---|
| ChatGPT | 118 | 28 | 5 | 151 | 3.3% |
| Claude | 3 | 141 | 4 | 148 | 2.7% |
| Copilot | 5 | 59 | 81 | 145 | 55.9% |
| DeepSeek | 0 | 0 | 137 | 137 | 100.0% |
| Gemini | 5 | 2 | 138 | 145 | 95.2% |
| Perplexity | 31 | 2 | 106 | 139 | 76.3% |

Can't tell share by agent ranges from 2.7% to 100.0%, but the six-agent range includes ChatGPT and Claude; the four agents the text calls mostly can't tell are: Copilot 55.9%, Perplexity 76.3%, Gemini 95.2%, DeepSeek 100.0%.

## Per data deletion method

| Method | Test cases | Recall success | Share recall success | Recall failed | Can't tell |
|---|---|---|---|---|---|
| Deleting a single conversation (UI actions) | 13 | 6 | 46.2% | 1 | 6 |
| Clearing all conversation history (UI actions) | 8 | 4 | 50.0% | 2 | 2 |
| Deleting a specific saved memory (UI actions) | 7 | 2 | 28.6% | 3 | 2 |
| Clearing all saved memories (UI actions) | 10 | 4 | 40.0% | 4 | 2 |
| Sending a deletion-request prompt | 811 | 144 | 17.8% | 213 | 454 |

UI-action methods: recall success in 29% to 50% of their test cases.
Streams: 67 on the MASTER sheet (UI actions, including 13 typed commands) and 798 on the NL FORGET sheet (prompts).
