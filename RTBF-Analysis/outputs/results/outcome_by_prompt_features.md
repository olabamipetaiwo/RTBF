# outcome_by_prompt_features

_Run at 2026-10-27T05:53:06_

# Does the wording of a forget request change the outcome?

> **AS IT STANDS (2026-10-27).** NL-forget study, 798 erased cells (318 with a known outcome). Re-run after each recall batch (`.venv/bin/python -m src.outcome_by_prompt_features`).

## A. Outcome at each level of each coded feature

Wording features are the final human coding of the 138 prompts. Each cell reads **came back of known** (the fact came back in a new conversation, out of cells with a known outcome) with a Wilson 95% interval. Levels with fewer than 6 cells show counts only and are left out of the range. "–" means no known outcome. Can't tell is not folded into either result. No tests: with so little variation a non-significant test shows little. Gemini and DeepSeek are left out because every cell is can't tell. Copilot's recall is still in progress, so its levels hold few cells. Perplexity's outcome is gave versus withheld the name, over all its recalled cells.

### Deletion location

| Platform | unspecified (53 prompts) | conversation (42 prompts) | prospective (13 prompts) | memory (10 prompts) | backend_db (9 prompts) | account_all (6 prompts) | Range over levels with 6+ cells |
|---|---|---|---|---|---|---|---|
| ChatGPT | 41 of 53 (64 to 87%) | 36 of 42 (72 to 93%) | 9 of 12 (47 to 91%) | 10 of 10 (72 to 100%) | 7 of 8 (53 to 98%) | 5 of 6 (44 to 97%) | 75% to 100% |
| Claude | 0 of 52 (0 to 7%) | 0 of 42 (0 to 8%) | 0 of 13 (0 to 23%) | 0 of 9 (0 to 30%) | 0 of 9 (0 to 30%) | 0 of 6 (0 to 39%) | 0% to 0% |
| Copilot | 0 of 9 (0 to 30%) | 0 of 8 (0 to 32%) | 0 of 4 | 0 of 3 | 0 of 1 | – | 0% to 0% |
| Perplexity (gave the name) | 14 of 53 (16 to 40%) | 12 of 42 (17 to 44%) | 1 of 13 (1 to 33%) | 1 of 10 (2 to 40%) | 2 of 9 (6 to 55%) | 1 of 6 (3 to 56%) | 8% to 29% |

Named cases (deletion from memory, from the backend database, of the whole account):

| Platform | memory | backend_db | account_all |
|---|---|---|---|
| ChatGPT | 10 of 10 (72 to 100%) | 7 of 8 (53 to 98%) | 5 of 6 (44 to 97%) |
| Claude | 0 of 9 (0 to 30%) | 0 of 9 (0 to 30%) | 0 of 6 (0 to 39%) |
| Copilot | 0 of 3 | 0 of 1 | – |
| Perplexity (gave the name) | 1 of 10 (2 to 40%) | 2 of 9 (6 to 55%) | 1 of 6 (3 to 56%) |

### What

| Platform | specific_pii (109 prompts) | unspecified (17 prompts) | general_pii (7 prompts) | Range over levels with 6+ cells |
|---|---|---|---|---|
| ChatGPT | 87 of 107 (73 to 88%) | 15 of 17 (66 to 97%) | 6 of 7 (49 to 97%) | 81% to 88% |
| Claude | 0 of 108 (0 to 3%) | 0 of 16 (0 to 19%) | 0 of 7 (0 to 35%) | 0% to 0% |
| Copilot | 0 of 23 (0 to 14%) | 0 of 1 | 0 of 1 | 0% to 0% |
| Perplexity (gave the name) | 16 of 109 (9 to 23%) | 10 of 17 (36 to 78%) | 5 of 7 (36 to 92%) | 15% to 71% |

### Mood

| Platform | imperative (105 prompts) | question (14 prompts) | statement (11 prompts) | other (3 prompts) | Range over levels with 6+ cells |
|---|---|---|---|---|---|
| ChatGPT | 84 of 103 (73 to 88%) | 12 of 14 (60 to 96%) | 10 of 11 (62 to 98%) | 2 of 3 | 82% to 91% |
| Claude | 0 of 103 (0 to 4%) | 0 of 14 (0 to 22%) | 0 of 11 (0 to 26%) | 0 of 3 | 0% to 0% |
| Copilot | 0 of 22 (0 to 15%) | 0 of 2 | 0 of 1 | – | 0% to 0% |
| Perplexity (gave the name) | 19 of 105 (12 to 27%) | 6 of 14 (21 to 67%) | 4 of 11 (15 to 65%) | 2 of 3 | 18% to 43% |

### Tone

| Platform | polite (73 prompts) | neutral (54 prompts) | friendly (6 prompts) | Range over levels with 6+ cells |
|---|---|---|---|---|
| ChatGPT | 55 of 71 (66 to 86%) | 50 of 54 (82 to 97%) | 3 of 6 (19 to 81%) | 50% to 93% |
| Claude | 0 of 73 (0 to 5%) | 0 of 52 (0 to 7%) | 0 of 6 (0 to 39%) | 0% to 0% |
| Copilot | 0 of 17 (0 to 18%) | 0 of 7 (0 to 35%) | 0 of 1 | 0% to 0% |
| Perplexity (gave the name) | 12 of 73 (10 to 27%) | 17 of 54 (21 to 45%) | 2 of 6 (10 to 70%) | 16% to 33% |

### Verb

| Platform | technical (124 prompts) | lay (7 prompts) | none (2 prompts) | Range over levels with 6+ cells |
|---|---|---|---|---|
| ChatGPT | 100 of 122 (74 to 88%) | 6 of 7 (49 to 97%) | 2 of 2 | 82% to 86% |
| Claude | 0 of 122 (0 to 3%) | 0 of 7 (0 to 35%) | 0 of 2 | 0% to 0% |
| Copilot | 0 of 23 (0 to 14%) | 0 of 2 | – | 0% to 0% |
| Perplexity (gave the name) | 26 of 124 (15 to 29%) | 3 of 7 (16 to 75%) | 2 of 2 | 21% to 43% |

### Justification

| Platform | FALSE (122 prompts) | TRUE (11 prompts) | Range over levels with 6+ cells |
|---|---|---|---|
| ChatGPT | 101 of 121 (76 to 89%) | 7 of 10 (40 to 89%) | 70% to 83% |
| Claude | 0 of 120 (0 to 3%) | 0 of 11 (0 to 26%) | 0% to 0% |
| Copilot | 0 of 21 (0 to 15%) | 0 of 4 | 0% to 0% |
| Perplexity (gave the name) | 28 of 122 (16 to 31%) | 3 of 11 (10 to 57%) | 23% to 27% |

### Accompanying request

| Platform | none (120 prompts) | verification (7 prompts) | guidance_for_self_deletion (3 prompts) | preserve_context (3 prompts) | Range over levels with 6+ cells |
|---|---|---|---|---|---|
| ChatGPT | 97 of 118 (74 to 88%) | 6 of 7 (49 to 97%) | 2 of 3 | 3 of 3 | 82% to 86% |
| Claude | 0 of 118 (0 to 3%) | 0 of 7 (0 to 35%) | 0 of 3 | 0 of 3 | 0% to 0% |
| Copilot | 0 of 22 (0 to 15%) | 0 of 1 | 0 of 1 | 0 of 1 | 0% to 0% |
| Perplexity (gave the name) | 24 of 120 (14 to 28%) | 2 of 7 (8 to 64%) | 3 of 3 | 2 of 3 | 20% to 29% |

## C. Refusals against what is asked

Each cell is retrieved, declined citing the request (human-reviewed refusals only), or not retrieved. Counts only, no tests.

**ChatGPT**: 133 cells with a recall, 13 reviewed refusals, 0 not-retrieved cells without a review (counted as not retrieved).

| Deletion location | Retrieved | Declined citing the request | Not retrieved |
|---|---|---|---|
| account_all | 5 | 1 | 0 |
| backend_db | 7 | 1 | 1 |
| conversation | 36 | 2 | 4 |
| memory | 10 | 0 | 0 |
| prospective | 9 | 4 | 0 |
| unspecified | 41 | 5 | 7 |

| What | Retrieved | Declined citing the request | Not retrieved |
|---|---|---|---|
| general_pii | 6 | 0 | 1 |
| specific_pii | 87 | 13 | 9 |
| unspecified | 15 | 0 | 2 |

**Perplexity**: 133 cells with a recall, 97 reviewed refusals, 0 not-retrieved cells without a review (counted as not retrieved).

| Deletion location | Retrieved | Declined citing the request | Not retrieved |
|---|---|---|---|
| account_all | 1 | 5 | 0 |
| backend_db | 2 | 7 | 0 |
| conversation | 12 | 28 | 2 |
| memory | 1 | 9 | 0 |
| prospective | 1 | 12 | 0 |
| unspecified | 14 | 36 | 3 |

| What | Retrieved | Declined citing the request | Not retrieved |
|---|---|---|---|
| general_pii | 5 | 2 | 0 |
| specific_pii | 16 | 89 | 4 |
| unspecified | 10 | 6 | 1 |

