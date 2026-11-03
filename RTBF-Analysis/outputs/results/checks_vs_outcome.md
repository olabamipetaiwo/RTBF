# checks_vs_outcome

_Run at 2026-11-03T16:04:49_

Source: outputs/tables/audit_outcomes_provisional.csv. Known outcomes only (recall success or recall failed); can't tell is left out.

## Same-conversation check (deletion requests typed in the chat)

| Agent | Test cases | Matched | Said gone, recall success | Said still there, recall failed | Wrong share |
|---|---|---|---|---|---|
| ChatGPT | 133 | 29 | 104 | 0 | 78% |
| Claude | 131 | 45 | 0 | 86 | 66% |
| Perplexity | 31 | 23 | 8 | 0 | 26% |
| Copilot | 8 | 4 | 0 | 4 | 50% |

Wrong share ranges from 26% to 78% across the four agents with known outcomes (Gemini and DeepSeek have none; Copilot has few).

## Interface check (deletions through UI actions)

- Screen showed the item gone in 49 test cases; 33 have a known outcome (recall success 14, recall failed 19); 16 are can't tell.
- Recall success after the screen showed it gone: 14 of 33 (42%).
- Screen unchanged: 4 test cases, recall success in 4.
