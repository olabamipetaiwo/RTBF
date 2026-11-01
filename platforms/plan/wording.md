# Plan: outcomes against the coded prompts, all platforms

## Question

Did any coded feature of a typed erasure request change the outcome on any platform? For example, did asking for deletion from memory rather than from the conversation, or writing politely rather than neutrally, change whether the fact was retrieved?

## Scope

- **Typed-request study only.** The 138 participant prompts are the only coded requests. Each ran on all six platforms.
- **Main battery as a reference.** Its typed request is one fixed command, so nothing varies. It only shows whether our own command led to the same outcome as the participants' prompts (casual-mention cell only, since every participant prompt followed a casual mention). It goes in the "What the user asked for, and how" row of each rival-explanations table, not in Findings: one cell per platform cannot carry a finding.
- **Seven dimensions, each analysed on its own:**

| Group | Dimension | Levels |
|---|---|---|
| What is asked | Deletion location | unspecified, conversation, no future use, memory, backend database, whole account |
| | What | specific, general, unspecified |
| How it is phrased | Mood | imperative, question, statement, other |
| | Tone | polite, neutral, friendly |
| | Verb | technical, lay, none |
| What accompanies it | Justification | given, not given |
| | Accompanying request | none, verification, guidance, preserve context |

## Where each platform stands

| Platform | Success | Failed | Can't tell | Not recalled |
|---|---|---|---|---|
| ChatGPT | 108 | 23 | 2 | 5 |
| Claude | 0 | 131 | 2 | 5 |
| Copilot | 0 | 18 | 39 | 81 (in progress) |
| Perplexity | 31 | 0 | 102 | 5 |
| Gemini | 0 | 0 | 120 | 18 |
| DeepSeek | 0 | 0 | 133 | 5 |

- Within each platform the outcome barely varies, so there is little for the prompt to explain.
- Can't tell is reported as can't tell, as its own count, never folded into success or failure (Dr Li).
- **Gemini and DeepSeek are left out:** every cell is can't tell, so there is no difference between prompts to explain. Each platform file says so in one line.
- **Perplexity is included with its own outcome:** gave the name or withheld it, over all 133 recalled cells (31 gave it; 97 of the other 102 withheld it citing the request, reviewed). Its tables are labelled as giving versus withholding the name, not as an erasure rate.

## Not done

| Analysis | Reason |
|---|---|
| Features against acknowledgment | The acknowledgment code is judged against what was asked, so the result would partly repeat the coding rule. |
| Combinations of features | Too few prompts per combination. |
| Every feature against every measure | Too many tests on too little variation; some would be significant by chance. |
| One model across platforms | The platform decides almost everything, so the model would measure the platform. |

## A. Outcome at each level of each dimension (main)

- For every platform and dimension: success / known outcome at each level, with a 95% interval.
- The range is taken over levels with at least 6 prompts, as in Rupp et al.; each rate is printed with its interval, so a small level (e.g. friendly tone, 3 of 6, about 19% to 81%) is not read as a difference. Smaller levels are reported with their counts only.
- Named cases on every platform: requests for deletion from memory, from the backend database, and of the whole account.
- **Possible claim:** no coded feature changed the outcome. On ChatGPT, the fact was retrieved in most cells at every level; on Claude, erasure held at every level.
- **Why ranges, not tests:** with little variation, a non-significant test shows little; rates with intervals are the recommended alternative (Altman and Bland 1995; Hoenig and Heisey 2001).
- **Precedent:** Rupp et al. (PoPETs 2022) reported erasure compliance by subgroup without tests, taking the range over subgroups with at least 6 services; we use the same minimum.
- **Goes to:** the "What the user asked for, and how" row of each platform's rival-explanations table.

## B. The same prompt across platforms

Moved to `cross-platform.md` (analysis 1), which covers it with a test across all platforms rather than one pair.

## C. Refusals against what is asked (Evidence only)

- Split each platform's cells into: retrieved; declined, citing the request; not retrieved.
- Report by deletion location and what. No tests.
- Reviewed refusals only: ChatGPT (13) and Perplexity (97), both reviewed.

## Script

Extend `RTBF-Analysis/src/outcome_by_prompt_features.py` with A and C. Re-run after every recall batch.

## Questions

- What does A and C ansers, whuch questions
- 
