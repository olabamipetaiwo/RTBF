# cross_platform

_Run at 2026-10-28T10:12:50_

Cross-platform analysis. Outcome: the fact came back in a new conversation (retrieval, not erasure). Cells with no usable recall are excluded. Source: `outputs/tables/audit_outcomes.csv`. Assumption checks: `outputs/results/cross_platform_assumptions.md`.

## 1. Typed requests: the same 138 prompts on every platform

Outcome: the fact came back in a new conversation. Retrieval, not erasure.

| Platform | Fact came back (usable prompts) | Prompts without a usable recall |
|---|---|---|
| ChatGPT | 108 of 133 (81%, 95% CI 73.7 to 86.9) | 5 |
| Claude | 0 of 133 (0%, 95% CI 0.0 to 2.8) | 5 |
| Gemini | 0 of 121 (0%, 95% CI 0.0 to 3.1) | 17 |
| Copilot | 0 of 67 (0%, 95% CI 0.0 to 5.4) | 71 |
| Perplexity | 31 of 133 (23%, 95% CI 16.9 to 31.2) | 5 |
| DeepSeek | 0 of 133 (0%, 95% CI 0.0 to 2.8) | 5 |

Cochran's Q asks whether the platforms differ at all. Platforms with no variation still count in the totals.

| Platforms compared | Prompts usable on all | Q | df | p |
|---|---|---|---|---|
| without Copilot (Gemini included, so its 13 account-wide prompts are out) | 121 | 327.4 | 4 | 1.30e-69 |
| without Copilot and Gemini | 133 | 256.3 | 3 | 2.89e-55 |

Exact McNemar test for every pair of platforms, on the prompts usable on both. Holm correction over all 15 pairs.

| A | B | Prompts | Both | A only | B only | Neither | p | Holm p | Note |
|---|---|---|---|---|---|---|---|---|---|
| ChatGPT | Claude | 133 | 0 | 108 | 0 | 25 | 6.16e-33 | 9.24e-32 |  |
| ChatGPT | Gemini | 121 | 0 | 101 | 0 | 20 | 7.89e-31 | 1.03e-29 |  |
| ChatGPT | Copilot | 67 | 0 | 57 | 0 | 10 | 1.39e-17 | 1.53e-16 |  |
| ChatGPT | Perplexity | 133 | 26 | 82 | 5 | 20 | 5.08e-19 | 6.09e-18 |  |
| ChatGPT | DeepSeek | 133 | 0 | 108 | 0 | 25 | 6.16e-33 | 9.24e-32 |  |
| Claude | Gemini | 121 | 0 | 0 | 0 | 121 | 1.00e+00 | 1.00e+00 | identical outcomes, no test |
| Claude | Copilot | 67 | 0 | 0 | 0 | 67 | 1.00e+00 | 1.00e+00 | identical outcomes, no test |
| Claude | Perplexity | 133 | 0 | 0 | 31 | 102 | 9.31e-10 | 9.31e-09 |  |
| Claude | DeepSeek | 133 | 0 | 0 | 0 | 133 | 1.00e+00 | 1.00e+00 | identical outcomes, no test |
| Gemini | Copilot | 64 | 0 | 0 | 0 | 64 | 1.00e+00 | 1.00e+00 | identical outcomes, no test |
| Gemini | Perplexity | 121 | 0 | 0 | 29 | 92 | 3.73e-09 | 2.98e-08 |  |
| Gemini | DeepSeek | 121 | 0 | 0 | 0 | 121 | 1.00e+00 | 1.00e+00 | identical outcomes, no test |
| Copilot | Perplexity | 67 | 0 | 0 | 15 | 52 | 6.10e-05 | 4.27e-04 |  |
| Copilot | DeepSeek | 67 | 0 | 0 | 0 | 67 | 1.00e+00 | 1.00e+00 | identical outcomes, no test |
| Perplexity | DeepSeek | 133 | 0 | 31 | 0 | 102 | 9.31e-10 | 9.31e-09 |  |

ChatGPT and Perplexity are the only two platforms where the fact came back for some prompts and not others. On the 133 prompts usable on both: both 26, ChatGPT only 82, Perplexity only 5, neither 20. Phi = +0.04, Fisher's exact p = 0.796: a prompt that came back on one platform is no more likely to come back on the other.

## 2. Erasure scope (main grid)

Cells with a usable recall: 65. Groups follow the commitment coded from each help page.

| Group | Fact came back |
|---|---|
| deletes | 7 of 37 (19%, 95% CI 9.5 to 34.2) |
| does not delete or unrelated | 9 of 14 (64%, 95% CI 38.8 to 83.7) |
| no commitment (not in the test) | 7 of 14 (50%, 95% CI 26.8 to 73.2) |

Fisher's exact test, deletes against the rest: odds ratio 0.13, p = 0.0050.

Platform-adjusted check (Mantel-Haenszel over the 3 platforms that have both groups and both outcomes): pooled odds ratio 0.16, p = 0.0107.

Per platform (descriptive only, groups too small to test):

| Platform | Deletes | Does not delete or unrelated |
|---|---|---|
| ChatGPT | 3 of 8 | 3 of 6 |
| Claude | 0 of 12 | 3 of 3 |
| Gemini | 1 of 5 | 3 of 4 |
| Copilot | 3 of 5 | - |
| Perplexity | 0 of 4 | - |
| DeepSeek | 0 of 3 | 0 of 1 |

## 3. Do the checks a user can make track the outcome? (descriptive)

Same-conversation check: after the forget request, the user asks about the fact in the same chat (typed requests only). "Check says yes" means the chat still produced the fact. "Check says no, fact came back" is the dangerous direction: the user is told it is gone and it is not.

| Platform | Cells | Check says yes, fact came back | Check says yes, did not come back | Check says no, fact came back | Check says no, did not come back | Check right |
|---|---|---|---|---|---|---|
| ChatGPT | 135 | 6 | 0 | 104 | 25 | 31 of 135 (23%, 95% CI 16.7 to 30.7) |
| Claude | 134 | 0 | 89 | 0 | 45 | 45 of 134 (34%, 95% CI 26.1 to 41.9) |
| Gemini | 120 | 0 | 69 | 0 | 51 | 51 of 120 (42%, 95% CI 34.0 to 51.4) |
| Copilot | 15 | 0 | 8 | 0 | 7 | 7 of 15 (47%, 95% CI 24.8 to 69.9) |
| Perplexity | 135 | 23 | 31 | 8 | 73 | 96 of 135 (71%, 95% CI 63.0 to 78.1) |
| DeepSeek | 134 | 0 | 90 | 0 | 44 | 44 of 134 (33%, 95% CI 25.5 to 41.2) |

Interface check (cells erased through the interface), known outcomes only: "changed" means the screen showed the item gone. Cells where the screen showed it gone and the outcome is can't tell are not counted here (14).

| Platform | Cells | Changed, fact came back | Changed, did not come back | Unchanged, fact came back | Unchanged, did not come back |
|---|---|---|---|---|---|
| ChatGPT | 12 | 5 | 5 | 2 | 0 |
| Claude | 11 | 2 | 8 | 1 | 0 |
| Copilot | 6 | 4 | 2 | 0 | 0 |
| Gemini | 6 | 3 | 2 | 1 | 0 |
| Perplexity | 2 | 0 | 2 | 0 | 0 |

Memory-page check (R2): the fact appears on the memory page, against whether the new-conversation questions (R1 and R3 only) found it.

| Platform | Cells | On page, fact came back | On page, did not come back | Not on page, fact came back | Not on page, did not come back |
|---|---|---|---|---|---|
| ChatGPT | 147 | 5 | 1 | 99 | 42 |
| Claude | 148 | 0 | 0 | 3 | 145 |
| Copilot | 42 | 0 | 0 | 5 | 37 |
| Gemini | 101 | 4 | 0 | 3 | 94 |

## 4. Withholding and policy (descriptive)

Refusals that cite the user's earlier request are counted by `src.recall_refusals` (one source); see its report.

Policy verdicts per platform. Can't tell includes every cell whose commitment is no commitment or unrelated.

| Platform | Cells recalled | Kept | Broken | Can't tell | of which no commitment |
|---|---|---|---|---|---|
| ChatGPT | 151 | 137 | 2 | 12 | 4 |
| Claude | 148 | 143 | 0 | 5 | 0 |
| Gemini | 135 | 1 | 1 | 133 | 126 |
| Copilot | 78 | 28 | 1 | 49 | 5 |
| Perplexity | 139 | 2 | 0 | 137 | 135 |
| DeepSeek | 137 | 0 | 0 | 137 | 0 |

