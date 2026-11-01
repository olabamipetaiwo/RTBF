# cross_platform_assumptions

_Run at 2026-10-27T05:55:09_

Assumption checks for the cross-platform tests. Outcome: retrieved in a new conversation (1) or not (0); cells with no usable recall are excluded. Source of outcomes: `outputs/tables/audit_outcomes.csv`.

## 1. Design integrity

- Prompt ids per platform: ChatGPT 138, Claude 138, Gemini 138, Copilot 138, Perplexity 138, DeepSeek 138.
- Prompt ids present on all six platforms: 138 of 138.
- Prompt ids whose disclosed fact (token) differs between platforms: 0.

Outcome coverage per platform (138 prompts each):

| Platform | Retrieved | Not retrieved | No usable recall (excluded) | Retrieval rate on usable |
|---|---|---|---|---|
| ChatGPT | 108 | 25 | 5 | 0.81 |
| Claude | 0 | 133 | 5 | 0.00 |
| Gemini | 0 | 120 | 18 | 0.00 |
| Copilot | 0 | 67 | 71 | 0.00 |
| Perplexity | 31 | 102 | 5 | 0.23 |
| DeepSeek | 0 | 133 | 5 | 0.00 |

## 2. Complete cases

Cochran's Q uses only prompts with a usable recall on every platform in the comparison.

| Platforms compared | Prompts usable on all of them | Platforms with no variation in that set |
|---|---|---|
| all six platforms | 63 | Claude, Gemini, Copilot, DeepSeek |
| without Copilot | 120 | Claude, Gemini, DeepSeek |
| without Copilot and Gemini | 133 | Claude, DeepSeek |
| without Copilot, Gemini and DeepSeek | 133 | Claude |

## 3. Selection: do complete-case prompts differ from the dropped ones?

For each subset, a platform's retrieval rate among the kept prompts is compared with its rate among the prompts that were dropped (usable on that platform but missing on another). Fisher's exact test. A difference would mean the complete cases are not representative of the 138.

| Subset | Platform | Retrieved, kept prompts | Retrieved, dropped prompts | Fisher p |
|---|---|---|---|---|
| all six platforms | ChatGPT | 54 of 63 (86%) | 54 of 70 (77%) | 0.268 |
| all six platforms | Perplexity | 14 of 63 (22%) | 17 of 70 (24%) | 0.839 |
| without Copilot | ChatGPT | 100 of 120 (83%) | 8 of 13 (62%) | 0.069 |
| without Copilot | Perplexity | 29 of 120 (24%) | 2 of 13 (15%) | 0.732 |

Final human coding of the kept set (without Copilot, 120 of 138) against the dropped prompts. Pearson chi-square with a permutation p (10,000 shuffles, seed 2026).

| Feature | Kept / all, by level | Chi-square | Permutation p |
|---|---|---|---|
| deletion_location | account_all 2/6; backend_db 8/9; conversation 41/43; memory 10/11; prospective 13/13; unspecified 46/56 | 21.16 | 0.002 |
| what | general_pii 6/11; specific_pii 97/109; unspecified 17/18 | 11.48 | 0.006 |
| mood | imperative 94/108; other 3/3; question 12/16; statement 11/11 | 4.12 | 0.182 |
| tone | friendly 5/8; neutral 47/56; polite 68/74 | 6.26 | 0.039 |
| verb | lay 7/7; none 2/2; technical 111/129 | 1.44 | 0.690 |
| justification | FALSE 111/127; TRUE 9/11 | 0.28 | 0.632 |
| accompanying_request | guidance_for_self_deletion 3/3; none 109/125; preserve_context 3/3; verification 5/7 | 2.39 | 0.485 |

## 4. Independence of prompts

### 4a. Accounts

- Accounts used for the 138 typed requests: ChatGPT 1, Claude 1, Gemini 1, Copilot 1, Perplexity 1, DeepSeek 1.
- With one account per platform, every prompt on a platform shares that account's memory. Prompts on one platform are therefore not strictly independent. The sibling rule and the order check below measure how much this matters.

### 4b. Sibling rule

Cells scored RECOVERED because their token surfaced in another cell's recall (direct evidence of cross-prompt leakage).

| Platform | Sibling-rule cells | Retrieval rate, as scored | Retrieval rate, sibling cells removed |
|---|---|---|---|
| ChatGPT | 13 | 108 of 133 (81%) | 95 of 120 (79%) |
| Claude | 0 | 0 of 133 (0%) | 0 of 133 (0%) |
| Gemini | 0 | 0 of 120 (0%) | 0 of 120 (0%) |
| Copilot | 0 | 0 of 67 (0%) | 0 of 67 (0%) |
| Perplexity | 2 | 31 of 133 (23%) | 29 of 131 (22%) |
| DeepSeek | 0 | 0 of 133 (0%) | 0 of 133 (0%) |

### 4c. Injection order

Spearman correlation between a cell's position in its platform's injection sequence and whether it was retrieved. A correlation would mean earlier or later prompts behave differently, as accumulating memory would produce. Holm correction across the platforms tested.

| Platform | Cells with a timestamp | Spearman rho | p | Note |
|---|---|---|---|---|
| ChatGPT | 133 | -0.00 | 0.977 | Holm p = 0.977 |
| Claude | 133 | - | - | no variation or too few timestamps |
| Gemini | 120 | - | - | no variation or too few timestamps |
| Copilot | 67 | - | - | no variation or too few timestamps |
| Perplexity | 133 | -0.06 | 0.468 | Holm p = 0.936 |
| DeepSeek | 133 | - | - | no variation or too few timestamps |

### 4d. Near-duplicate prompts

- Prompts whose text repeats an earlier prompt exactly: 0.
- Pairs with text similarity of at least 0.90 (difflib ratio): 2.
- Repeated referents (the thing disclosed): 0.

  - I0032 / I0045 (0.94): "delete all location data" / "delete all my location data"
  - I0077 / I0165 (0.90): "please delete my location data for this conversation" / "please delete my location data from our conversation"

### 4e. Do the same prompts behave alike across platforms?

Phi coefficient (Pearson on 0/1) between platforms, on prompts usable on both. A value near 0 means the prompt has little to do with the outcome, and pairing adds little. A large value means the pairing is doing real work.

| Platform A | Platform B | Prompts | Phi |
|---|---|---|---|
| ChatGPT | Claude | 133 | no variation |
| ChatGPT | Gemini | 120 | no variation |
| ChatGPT | Copilot | 67 | no variation |
| ChatGPT | Perplexity | 133 | +0.04 |
| ChatGPT | DeepSeek | 133 | no variation |
| Claude | Gemini | 120 | no variation |
| Claude | Copilot | 67 | no variation |
| Claude | Perplexity | 133 | no variation |
| Claude | DeepSeek | 133 | no variation |
| Gemini | Copilot | 63 | no variation |
| Gemini | Perplexity | 120 | no variation |
| Gemini | DeepSeek | 120 | no variation |
| Copilot | Perplexity | 67 | no variation |
| Copilot | DeepSeek | 67 | no variation |
| Perplexity | DeepSeek | 133 | no variation |

## 5. Power for the pairwise McNemar tests

McNemar uses only discordant prompts (retrieved on one platform and not the other). With fewer than 10 discordant prompts the test has little power, and the exact version is required.

| A | B | Paired prompts | Both | A only | B only | Neither | Flag |
|---|---|---|---|---|---|---|---|
| ChatGPT | Claude | 133 | 0 | 108 | 0 | 25 |  |
| ChatGPT | Gemini | 120 | 0 | 100 | 0 | 20 |  |
| ChatGPT | Copilot | 67 | 0 | 57 | 0 | 10 |  |
| ChatGPT | Perplexity | 133 | 26 | 82 | 5 | 20 |  |
| ChatGPT | DeepSeek | 133 | 0 | 108 | 0 | 25 |  |
| Claude | Gemini | 120 | 0 | 0 | 0 | 120 | low power |
| Claude | Copilot | 67 | 0 | 0 | 0 | 67 | low power |
| Claude | Perplexity | 133 | 0 | 0 | 31 | 102 |  |
| Claude | DeepSeek | 133 | 0 | 0 | 0 | 133 | low power |
| Gemini | Copilot | 63 | 0 | 0 | 0 | 63 | low power |
| Gemini | Perplexity | 120 | 0 | 0 | 29 | 91 |  |
| Gemini | DeepSeek | 120 | 0 | 0 | 0 | 120 | low power |
| Copilot | Perplexity | 67 | 0 | 0 | 15 | 52 |  |
| Copilot | DeepSeek | 67 | 0 | 0 | 0 | 67 | low power |
| Perplexity | DeepSeek | 133 | 0 | 31 | 0 | 102 |  |

## 6. What "not retrieved" means

A zero can mean the platform erased or never used the fact, or that it never stored it. Retention at injection (coded when the fact was disclosed) separates the two: shown or claimed means the platform visibly kept it.

| Platform | Not retrieved | shown | claimed | acknowledged | denied | no_signal | uncoded |
|---|---|---|---|---|---|---|---|
| ChatGPT | 25 | 23 | 0 | 2 | 0 | 0 | 0 |
| Claude | 133 | 131 | 0 | 2 | 0 | 0 | 0 |
| Gemini | 120 | 0 | 0 | 115 | 0 | 5 | 0 |
| Copilot | 67 | 25 | 0 | 0 | 0 | 42 | 0 |
| Perplexity | 102 | 0 | 0 | 101 | 0 | 1 | 0 |
| DeepSeek | 133 | 0 | 0 | 133 | 0 | 0 | 0 |

## 7. Section 2 (erasure scope): is scope confounded?

Main-grid cells with a usable recall: 65. Commitment types present: DELETES 37, NO COMMITMENT 14, UNRELATED 8, DOES NOT DELETE 6.

- Left out of the two groups: 14 cells (NO COMMITMENT 14).

Cells per platform and group, with the number retrieved:

| Platform | Deletes: retrieved | Does not delete or unrelated: retrieved |
|---|---|---|
| ChatGPT | 3 of 8 | 3 of 6 |
| Claude | 0 of 12 | 3 of 3 |
| Gemini | 1 of 5 | 3 of 4 |
| Copilot | 3 of 5 | - |
| Perplexity | 0 of 4 | - |
| DeepSeek | 0 of 3 | 0 of 1 |

Cells per injection type and group (injection type changes how likely a fact is to be stored):

| Injection | deletes | does not delete or unrelated |
|---|---|---|
| I1 | 17 | 6 |
| I2 | 14 | 5 |
| I3 | 6 | 3 |

Crude (pooled over platforms) Fisher p = 0.0050; odds ratio = 0.13.

Platforms usable as strata (both groups present, both outcomes present): 3 of 6.
Cochran-Mantel-Haenszel across those platforms: pooled odds ratio = 0.16, p = 0.0107.
If the crude and stratified results agree in direction and size, platform is not driving the scope effect; if they diverge, the pooled Fisher test is confounded and cannot be used on its own.

