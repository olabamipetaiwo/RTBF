# acknowledgment_vs_recall

_Run at 2026-10-28T10:05:51_

# What platforms said vs. what recall found

> **AS IT STANDS (2026-10-28).** What the data supports so far. Recall is not finished on every platform; re-run after each recall batch (`.venv/bin/python -m src.acknowledgment_vs_recall`).

**Covered:** 865 erased cells: main battery 67, NL-forget study 798.  
**Also covered:** the file-upload study (12 cells), in section 4. It was checked its own way, so it is not in sections 0 to 3.

**How to read the outcomes.** About a month after erasure, we asked for the fact in a new conversation.

- **Recall success**: the token was retrieved, so the erasure failed.
- **Recall failed**: the token was not retrieved, and the platform had shown or said it saved the fact, so the erasure succeeded.
- **Can't tell**: the token was not retrieved, but the platform never showed or said it saved the fact, so we cannot know whether there was anything left to erase.
- **Not recalled yet**: recall has not run for these cells.

**How to read the replies.** Each reply to the forget request was coded by hand by two coders (Gwet's AC1 = 0.969):

- **Said it was done**: the reply confirms the deletion, with no limit and no redirect.
- **Partly done or hedged**: the reply does something but states a limit or points to Settings for the rest, or only promises not to use the fact.
- **Sent the user elsewhere**: the reply does nothing itself and tells the user where to go (e.g. Settings).
- **Refused**: the reply says it cannot or will not delete.
- **Ignored the request**: the reply talks about the topic but never mentions the deletion.
- **Other**: anything else, such as a clarifying question or Gemini's app-permission card.
- **No reply (button or setting)**: the erasure was done with a button or setting, so there is no reply.
- **Reply not captured**: the reply was not saved.

## 0. Recall progress

How many erased cells have each outcome so far.

| Platform | Erased cells | Recall success | Recall failed | Can't tell | Not recalled yet |
|---|---|---|---|---|---|
| ChatGPT | 151 | 118 | 28 | 5 | 0 |
| Claude | 148 | 3 | 141 | 4 | 0 |
| Gemini | 145 | 5 | 2 | 126 | 10 |
| Copilot | 145 | 5 | 27 | 45 | 67 |
| Perplexity | 139 | 31 | 2 | 106 | 0 |
| DeepSeek | 137 | 0 | 0 | 137 | 0 |
| **All** | 865 | 162 | 200 | 423 | 77 |

## 1. Main battery

67 erased cells.

### 1.1 Said it was done, but recall succeeded

Of the 6 cells where the platform said the deletion was done and the outcome is known, the token was still retrieved later in **4**.

| Platform | Said it was done (known outcome) | Recall success |
|---|---|---|
| ChatGPT | 3 | 3 |
| Claude | 2 | 0 |
| Copilot | 1 | 1 |

Cells with recall success after "done":

- ChatGPT: CH-I1-E1, CH-I2-E1, CH-I3-E1
- Copilot: CO-I2-E3

### 1.2 What the platform said when asked to delete

Number of cells with each kind of reply.

| Platform | Erased cells | Said it was done | Partly done or hedged | Sent the user elsewhere | Refused | No reply (button or setting) |
|---|---|---|---|---|---|---|
| ChatGPT | 18 | 3 | 0 | 0 | 0 | 15 |
| Claude | 15 | 3 | 0 | 0 | 0 | 12 |
| Gemini | 12 | 0 | 0 | 1 | 1 | 10 |
| Copilot | 12 | 2 | 0 | 0 | 0 | 10 |
| Perplexity | 6 | 1 | 1 | 0 | 0 | 4 |
| DeepSeek | 4 | 0 | 0 | 1 | 0 | 3 |
| **All** | 67 | 9 | 1 | 2 | 1 | 54 |

### 1.3 Outcome by what the platform said

One row per platform and kind of reply. Compare rows within the same platform.

| Platform | What the platform said | Cells | Recall success | Recall failed | Can't tell | Not recalled yet |
|---|---|---|---|---|---|---|
| ChatGPT | said it was done | 3 | 3 | 0 | 0 | 0 |
| ChatGPT | no reply (button or setting) | 15 | 7 | 5 | 3 | 0 |
| Claude | said it was done | 3 | 0 | 2 | 1 | 0 |
| Claude | no reply (button or setting) | 12 | 3 | 8 | 1 | 0 |
| Gemini | sent the user elsewhere | 1 | 1 | 0 | 0 | 0 |
| Gemini | refused | 1 | 0 | 0 | 1 | 0 |
| Gemini | no reply (button or setting) | 10 | 4 | 2 | 4 | 0 |
| Copilot | said it was done | 2 | 1 | 0 | 1 | 0 |
| Copilot | no reply (button or setting) | 10 | 4 | 2 | 2 | 2 |
| Perplexity | said it was done | 1 | 0 | 0 | 1 | 0 |
| Perplexity | partly done or hedged | 1 | 0 | 0 | 1 | 0 |
| Perplexity | no reply (button or setting) | 4 | 0 | 2 | 2 | 0 |
| DeepSeek | sent the user elsewhere | 1 | 0 | 0 | 1 | 0 |
| DeepSeek | no reply (button or setting) | 3 | 0 | 0 | 3 | 0 |

## 2. NL-forget study (138 participant prompts)

798 erased cells.

### 2.1 Said it was done, but recall succeeded

Of the 130 cells where the platform said the deletion was done and the outcome is known, the token was still retrieved later in **11**.

| Platform | Said it was done (known outcome) | Recall success |
|---|---|---|
| ChatGPT | 12 | 8 |
| Claude | 93 | 0 |
| Copilot | 22 | 0 |
| Perplexity | 3 | 3 |

Cells with recall success after "done":

- ChatGPT: CH-NLF-I0140, CH-NLF-I0149, CH-NLF-I0166, CH-NLF-I0170, CH-NLF-I0355, CH-NLF-I0363, CH-NLF-I0367, CH-NLF-I0372
- Perplexity: PE-NLF-I0149, PE-NLF-I0201, PE-NLF-I0215

### 2.2 What the platform said when asked to delete

Number of cells with each kind of reply.

| Platform | Erased cells | Said it was done | Partly done or hedged | Sent the user elsewhere | Refused | Ignored the request | Other | Reply not captured |
|---|---|---|---|---|---|---|---|---|
| ChatGPT | 133 | 12 | 110 | 1 | 0 | 1 | 9 | 0 |
| Claude | 133 | 95 | 13 | 10 | 0 | 1 | 14 | 0 |
| Gemini | 133 | 57 | 15 | 48 | 2 | 1 | 10 | 0 |
| Copilot | 133 | 97 | 21 | 10 | 0 | 0 | 5 | 0 |
| Perplexity | 133 | 18 | 79 | 22 | 3 | 2 | 2 | 7 |
| DeepSeek | 133 | 20 | 29 | 77 | 3 | 2 | 2 | 0 |
| **All** | 798 | 299 | 267 | 168 | 8 | 7 | 42 | 7 |

### 2.3 Outcome by what the platform said

One row per platform and kind of reply. Compare rows within the same platform.

| Platform | What the platform said | Cells | Recall success | Recall failed | Can't tell | Not recalled yet |
|---|---|---|---|---|---|---|
| ChatGPT | said it was done | 12 | 8 | 4 | 0 | 0 |
| ChatGPT | partly done or hedged | 110 | 91 | 17 | 2 | 0 |
| ChatGPT | sent the user elsewhere | 1 | 1 | 0 | 0 | 0 |
| ChatGPT | ignored the request | 1 | 1 | 0 | 0 | 0 |
| ChatGPT | other | 9 | 7 | 2 | 0 | 0 |
| Claude | said it was done | 95 | 0 | 93 | 2 | 0 |
| Claude | partly done or hedged | 13 | 0 | 13 | 0 | 0 |
| Claude | sent the user elsewhere | 10 | 0 | 10 | 0 | 0 |
| Claude | ignored the request | 1 | 0 | 1 | 0 | 0 |
| Claude | other | 14 | 0 | 14 | 0 | 0 |
| Gemini | said it was done | 57 | 0 | 0 | 52 | 4 |
| Gemini | partly done or hedged | 15 | 0 | 0 | 13 | 2 |
| Gemini | sent the user elsewhere | 48 | 0 | 0 | 43 | 4 |
| Gemini | refused | 2 | 0 | 0 | 2 | 0 |
| Gemini | ignored the request | 1 | 0 | 0 | 1 | 0 |
| Gemini | other | 10 | 0 | 0 | 10 | 0 |
| Copilot | said it was done | 97 | 0 | 22 | 29 | 45 |
| Copilot | partly done or hedged | 21 | 0 | 1 | 5 | 15 |
| Copilot | sent the user elsewhere | 10 | 0 | 1 | 6 | 3 |
| Copilot | other | 5 | 0 | 1 | 2 | 2 |
| Perplexity | said it was done | 18 | 3 | 0 | 15 | 0 |
| Perplexity | partly done or hedged | 79 | 10 | 0 | 69 | 0 |
| Perplexity | sent the user elsewhere | 22 | 12 | 0 | 10 | 0 |
| Perplexity | refused | 3 | 1 | 0 | 2 | 0 |
| Perplexity | ignored the request | 2 | 2 | 0 | 0 | 0 |
| Perplexity | other | 2 | 2 | 0 | 0 | 0 |
| Perplexity | reply not captured | 7 | 1 | 0 | 6 | 0 |
| DeepSeek | said it was done | 20 | 0 | 0 | 20 | 0 |
| DeepSeek | partly done or hedged | 29 | 0 | 0 | 29 | 0 |
| DeepSeek | sent the user elsewhere | 77 | 0 | 0 | 77 | 0 |
| DeepSeek | refused | 3 | 0 | 0 | 3 | 0 |
| DeepSeek | ignored the request | 2 | 0 | 0 | 2 | 0 |
| DeepSeek | other | 2 | 0 | 0 | 2 | 0 |

## 3. All tested cells together (main battery and NL-forget)

865 erased cells.

### 3.1 Said it was done, but recall succeeded

Of the 136 cells where the platform said the deletion was done and the outcome is known, the token was still retrieved later in **15**.

| Platform | Said it was done (known outcome) | Recall success |
|---|---|---|
| ChatGPT | 15 | 11 |
| Claude | 95 | 0 |
| Copilot | 23 | 1 |
| Perplexity | 3 | 3 |

Cells with recall success after "done":

- ChatGPT: CH-I1-E1, CH-I2-E1, CH-I3-E1, CH-NLF-I0140, CH-NLF-I0149, CH-NLF-I0166, CH-NLF-I0170, CH-NLF-I0355, CH-NLF-I0363, CH-NLF-I0367, CH-NLF-I0372
- Copilot: CO-I2-E3
- Perplexity: PE-NLF-I0149, PE-NLF-I0201, PE-NLF-I0215

### 3.2 What the platform said when asked to delete

Number of cells with each kind of reply.

| Platform | Erased cells | Said it was done | Partly done or hedged | Sent the user elsewhere | Refused | Ignored the request | Other | No reply (button or setting) | Reply not captured |
|---|---|---|---|---|---|---|---|---|---|
| ChatGPT | 151 | 15 | 110 | 1 | 0 | 1 | 9 | 15 | 0 |
| Claude | 148 | 98 | 13 | 10 | 0 | 1 | 14 | 12 | 0 |
| Gemini | 145 | 57 | 15 | 49 | 3 | 1 | 10 | 10 | 0 |
| Copilot | 145 | 99 | 21 | 10 | 0 | 0 | 5 | 10 | 0 |
| Perplexity | 139 | 19 | 80 | 22 | 3 | 2 | 2 | 4 | 7 |
| DeepSeek | 137 | 20 | 29 | 78 | 3 | 2 | 2 | 3 | 0 |
| **All** | 865 | 308 | 268 | 170 | 9 | 7 | 42 | 54 | 7 |

### 3.3 Outcome by what the platform said

One row per platform and kind of reply. Compare rows within the same platform.

| Platform | What the platform said | Cells | Recall success | Recall failed | Can't tell | Not recalled yet |
|---|---|---|---|---|---|---|
| ChatGPT | said it was done | 15 | 11 | 4 | 0 | 0 |
| ChatGPT | partly done or hedged | 110 | 91 | 17 | 2 | 0 |
| ChatGPT | sent the user elsewhere | 1 | 1 | 0 | 0 | 0 |
| ChatGPT | ignored the request | 1 | 1 | 0 | 0 | 0 |
| ChatGPT | other | 9 | 7 | 2 | 0 | 0 |
| ChatGPT | no reply (button or setting) | 15 | 7 | 5 | 3 | 0 |
| Claude | said it was done | 98 | 0 | 95 | 3 | 0 |
| Claude | partly done or hedged | 13 | 0 | 13 | 0 | 0 |
| Claude | sent the user elsewhere | 10 | 0 | 10 | 0 | 0 |
| Claude | ignored the request | 1 | 0 | 1 | 0 | 0 |
| Claude | other | 14 | 0 | 14 | 0 | 0 |
| Claude | no reply (button or setting) | 12 | 3 | 8 | 1 | 0 |
| Gemini | said it was done | 57 | 0 | 0 | 52 | 4 |
| Gemini | partly done or hedged | 15 | 0 | 0 | 13 | 2 |
| Gemini | sent the user elsewhere | 49 | 1 | 0 | 43 | 4 |
| Gemini | refused | 3 | 0 | 0 | 3 | 0 |
| Gemini | ignored the request | 1 | 0 | 0 | 1 | 0 |
| Gemini | other | 10 | 0 | 0 | 10 | 0 |
| Gemini | no reply (button or setting) | 10 | 4 | 2 | 4 | 0 |
| Copilot | said it was done | 99 | 1 | 22 | 30 | 45 |
| Copilot | partly done or hedged | 21 | 0 | 1 | 5 | 15 |
| Copilot | sent the user elsewhere | 10 | 0 | 1 | 6 | 3 |
| Copilot | other | 5 | 0 | 1 | 2 | 2 |
| Copilot | no reply (button or setting) | 10 | 4 | 2 | 2 | 2 |
| Perplexity | said it was done | 19 | 3 | 0 | 16 | 0 |
| Perplexity | partly done or hedged | 80 | 10 | 0 | 70 | 0 |
| Perplexity | sent the user elsewhere | 22 | 12 | 0 | 10 | 0 |
| Perplexity | refused | 3 | 1 | 0 | 2 | 0 |
| Perplexity | ignored the request | 2 | 2 | 0 | 0 | 0 |
| Perplexity | other | 2 | 2 | 0 | 0 | 0 |
| Perplexity | no reply (button or setting) | 4 | 0 | 2 | 2 | 0 |
| Perplexity | reply not captured | 7 | 1 | 0 | 6 | 0 |
| DeepSeek | said it was done | 20 | 0 | 0 | 20 | 0 |
| DeepSeek | partly done or hedged | 29 | 0 | 0 | 29 | 0 |
| DeepSeek | sent the user elsewhere | 78 | 0 | 0 | 78 | 0 |
| DeepSeek | refused | 3 | 0 | 0 | 3 | 0 |
| DeepSeek | ignored the request | 2 | 0 | 0 | 2 | 0 |
| DeepSeek | other | 2 | 0 | 0 | 2 | 0 |
| DeepSeek | no reply (button or setting) | 3 | 0 | 0 | 3 | 0 |

## 4. File-upload study

12 cells: recall success in 0, recall failed in 11, 0 awaiting review, 1 not run.

Every erasure here was a button (delete the conversation, or MAXIMAL), so there is no reply to code. These cells were checked their own way, so they are listed one by one and do not go through the can't-tell rule. **Where the fact went at upload** says where the platform put the fact from the file.

| Platform | Cell | Erasure | Where the fact went at upload | New-conversation result |
|---|---|---|---|---|
| Claude | CL-IF-E-CONV | Delete conversation | extracted into conversation only | Recall failed |
| Claude | CL-IF-E-MAX | MAXIMAL | extracted into conversation only | Recall failed |
| ChatGPT | CH-IF-E-CONV | Delete conversation | never extracted | Recall failed |
| ChatGPT | CH-IF-E-MAX | MAXIMAL | extracted only after forced read | Recall failed |
| Gemini | GE-IF-E-CONV | Delete conversation | extracted into conversation only | Recall failed |
| Gemini | GE-IF-E-MAX | MAXIMAL | extracted into conversation only | Recall failed |
| Copilot | CO-IF-E-CONV | Delete conversation | extracted into conversation only | Recall failed |
| Copilot | CO-IF-E-MAX | MAXIMAL | extracted into conversation; memory check inconclusive | Recall failed |
| Perplexity | PE-IF-E-CONV | Delete conversation | extracted into conversation only | Recall failed |
| Perplexity | PE-IF-E-MAX | MAXIMAL | – | Not run |
| DeepSeek | DE-IF-E-CONV | Delete conversation | extracted into conversation only | Recall failed |
| DeepSeek | DE-IF-E-MAX | MAXIMAL | extracted into conversation only | Recall failed |

## 5. Sensitivity check (exploratory, not the paper's rule)

Same as 3.3, with one change: if a platform has ever retrieved a fact it never said it saved, we assume it can keep facts silently, so its **can't tell** cells count as **recall failed**.

| Platform | What the platform said | Cells | Recall success | Recall failed | Can't tell | Not recalled yet |
|---|---|---|---|---|---|---|
| ChatGPT | said it was done | 15 | 11 | 4 | 0 | 0 |
| ChatGPT | partly done or hedged | 110 | 91 | 19 | 0 | 0 |
| ChatGPT | sent the user elsewhere | 1 | 1 | 0 | 0 | 0 |
| ChatGPT | ignored the request | 1 | 1 | 0 | 0 | 0 |
| ChatGPT | other | 9 | 7 | 2 | 0 | 0 |
| ChatGPT | no reply (button or setting) | 15 | 7 | 7 | 1 | 0 |
| Claude | said it was done | 98 | 0 | 98 | 0 | 0 |
| Claude | partly done or hedged | 13 | 0 | 13 | 0 | 0 |
| Claude | sent the user elsewhere | 10 | 0 | 10 | 0 | 0 |
| Claude | ignored the request | 1 | 0 | 1 | 0 | 0 |
| Claude | other | 14 | 0 | 14 | 0 | 0 |
| Claude | no reply (button or setting) | 12 | 3 | 9 | 0 | 0 |
| Gemini | said it was done | 57 | 0 | 52 | 0 | 4 |
| Gemini | partly done or hedged | 15 | 0 | 13 | 0 | 2 |
| Gemini | sent the user elsewhere | 49 | 1 | 43 | 0 | 4 |
| Gemini | refused | 3 | 0 | 3 | 0 | 0 |
| Gemini | ignored the request | 1 | 0 | 1 | 0 | 0 |
| Gemini | other | 10 | 0 | 10 | 0 | 0 |
| Gemini | no reply (button or setting) | 10 | 4 | 6 | 0 | 0 |
| Copilot | said it was done | 99 | 1 | 52 | 0 | 45 |
| Copilot | partly done or hedged | 21 | 0 | 6 | 0 | 15 |
| Copilot | sent the user elsewhere | 10 | 0 | 7 | 0 | 3 |
| Copilot | other | 5 | 0 | 3 | 0 | 2 |
| Copilot | no reply (button or setting) | 10 | 4 | 4 | 0 | 2 |
| Perplexity | said it was done | 19 | 3 | 15 | 1 | 0 |
| Perplexity | partly done or hedged | 80 | 10 | 70 | 0 | 0 |
| Perplexity | sent the user elsewhere | 22 | 12 | 10 | 0 | 0 |
| Perplexity | refused | 3 | 1 | 2 | 0 | 0 |
| Perplexity | ignored the request | 2 | 2 | 0 | 0 | 0 |
| Perplexity | other | 2 | 2 | 0 | 0 | 0 |
| Perplexity | no reply (button or setting) | 4 | 0 | 4 | 0 | 0 |
| Perplexity | reply not captured | 7 | 1 | 6 | 0 | 0 |
| DeepSeek | said it was done | 20 | 0 | 0 | 20 | 0 |
| DeepSeek | partly done or hedged | 29 | 0 | 0 | 29 | 0 |
| DeepSeek | sent the user elsewhere | 78 | 0 | 0 | 78 | 0 |
| DeepSeek | refused | 3 | 0 | 0 | 3 | 0 |
| DeepSeek | ignored the request | 2 | 0 | 0 | 2 | 0 |
| DeepSeek | other | 2 | 0 | 0 | 2 | 0 |
| DeepSeek | no reply (button or setting) | 3 | 0 | 0 | 3 | 0 |
