# replies_by_outcome

_Run at 2026-11-03T15:46:28_

Source: outputs/tables/audit_outcomes_provisional.csv (798 typed-request test cases, placeholders included).

## Reply type against outcome (all agents)

| Reply | Recall success | Recall failed | Can't tell | Test cases | Share of all |
|---|---|---|---|---|---|
| Complied | 11 | 142 | 146 | 299 | 37.5% |
| Partial | 101 | 39 | 127 | 267 | 33.5% |
| Deflected | 13 | 11 | 144 | 168 | 21.1% |
| Refused | 1 | 0 | 7 | 8 | 1.0% |
| Silently ignored | 3 | 1 | 3 | 7 | 0.9% |
| Other | 9 | 18 | 15 | 42 | 5.3% |
| Not captured | 1 | 0 | 6 | 7 | 0.9% |
| All replies | 139 | 211 | 448 | 798 | 100.0% |

## After a reply that complied

- Complied: 299 test cases; 153 with a known outcome (recall success or recall failed); recall success in 11 of those 153.

## By agent (rows within an agent are comparable)

| Agent | Reply | Recall success | Recall failed | Can't tell | Test cases |
|---|---|---|---|---|---|
| ChatGPT | Complied | 8 | 4 | 0 | 12 |
| ChatGPT | Partial | 91 | 17 | 2 | 110 |
| ChatGPT | Deflected | 1 | 0 | 0 | 1 |
| ChatGPT | Silently ignored | 1 | 0 | 0 | 1 |
| ChatGPT | Other | 7 | 2 | 0 | 9 |
| Claude | Complied | 0 | 93 | 2 | 95 |
| Claude | Partial | 0 | 13 | 0 | 13 |
| Claude | Deflected | 0 | 10 | 0 | 10 |
| Claude | Silently ignored | 0 | 1 | 0 | 1 |
| Claude | Other | 0 | 14 | 0 | 14 |
| Copilot | Complied | 0 | 45 | 52 | 97 |
| Copilot | Partial | 0 | 9 | 12 | 21 |
| Copilot | Deflected | 0 | 1 | 9 | 10 |
| Copilot | Other | 0 | 2 | 3 | 5 |
| DeepSeek | Complied | 0 | 0 | 20 | 20 |
| DeepSeek | Partial | 0 | 0 | 29 | 29 |
| DeepSeek | Deflected | 0 | 0 | 77 | 77 |
| DeepSeek | Refused | 0 | 0 | 3 | 3 |
| DeepSeek | Silently ignored | 0 | 0 | 2 | 2 |
| DeepSeek | Other | 0 | 0 | 2 | 2 |
| Gemini | Complied | 0 | 0 | 57 | 57 |
| Gemini | Partial | 0 | 0 | 15 | 15 |
| Gemini | Deflected | 0 | 0 | 48 | 48 |
| Gemini | Refused | 0 | 0 | 2 | 2 |
| Gemini | Silently ignored | 0 | 0 | 1 | 1 |
| Gemini | Other | 0 | 0 | 10 | 10 |
| Perplexity | Complied | 3 | 0 | 15 | 18 |
| Perplexity | Partial | 10 | 0 | 69 | 79 |
| Perplexity | Deflected | 12 | 0 | 10 | 22 |
| Perplexity | Refused | 1 | 0 | 2 | 3 |
| Perplexity | Silently ignored | 2 | 0 | 0 | 2 |
| Perplexity | Other | 2 | 0 | 0 | 2 |
| Perplexity | Not captured | 1 | 0 | 6 | 7 |
