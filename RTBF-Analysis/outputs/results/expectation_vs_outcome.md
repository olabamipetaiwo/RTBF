# expectation_vs_outcome

_Run at 2026-11-03T17:28:47_

Sources: outputs/tables/pooled_obs_expectation_pct.csv (Pooled responses) and the provisional audit table (placeholders included).

| Method | Responses | Expect not in future conversations | Expect permanent deletion | Test cases | Recall success | Recall failed | Can't tell |
|---|---|---|---|---|---|---|---|
| Delete a single conversation | 164 | 54.3% | 58.5% | 13 | 6 | 1 | 6 |
| Clear all conversation history | 73 | 42.5% | 52.1% | 8 | 4 | 2 | 2 |
| Delete a specific saved memory | 41 | 63.4% | 65.9% | 7 | 2 | 3 | 2 |
| Send a deletion-request prompt | 39 | 51.3% | 64.1% | 811 | 144 | 213 | 454 |

Expect not in future conversations: 42.5% to 63.4% across the four methods.
Expect permanent deletion: 52.1% to 65.9%.
