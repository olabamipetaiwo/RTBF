# Provisional results

Status: **Section 5 is written on the final base of 865 test cases (67 through UI actions, 798 through prompts).**
Of these, 804 have a real recall result and **61 are placeholders** (49 Copilot, 12 Gemini), listed below.
Every number in Section 5 that includes a placeholder is provisional.

## When recall has run

Every cell in the table below is replaced by its real result. Nothing in the paper keeps a placeholder.

1. Finish Copilot and Gemini recall and enter the results (and the three reviews) in `RTBF Experiments.xlsx`.
2. `cd RTBF-Analysis && .venv/bin/python -m src.audit_outcomes && .venv/bin/python -m src.provisional_fill`.
   A cell with a real result drops out of the fill. When `outputs/results/provisional_fill.md` reports 0 placeholders, the base is 865 real results.
3. Re-run the other saved Section 5 scripts (`src.expectation_gap`, `src.recall_refusals`, `src.outcome_by_prompt_features`, `src.gemini_permission_cards`) and re-count every Section 5 number against the real results.
4. Update each number listed under "Section 5 numbers that depend on placeholders" (below), and re-read each sentence whose claim could change (for example "at least", "never", "every", "only", "mostly").
5. Replace each row's "Real result" column, then delete this file's placeholders.

## How the placeholders were chosen

A missing test case takes the most common recall result among the completed test cases with the same agent, the same part (UI actions or prompts) and the same retention code at injection (`src/provisional_fill.py`). Every group used is unanimous except the 2 Copilot UI-action test cases (3 can't tell, 1 recall success).

| Agent | Part | Retention at injection | Placeholder | Test cases | Completed test cases in the group |
|---|---|---|---|---|---|
| Copilot | prompts | shown | recall failed | 22 | 35 recall failed |
| Copilot | prompts | no signal | can't tell | 25 | 51 can't tell |
| Gemini | prompts | acknowledged or no signal | can't tell | 12 | 115 and 6 can't tell |
| Copilot | UI actions | no signal | can't tell | 2 | 3 can't tell, 1 recall success |

No placeholder is a recall success. If any of these come back as recall success, the share of recall success rises above 18.7% and every "at least" claim about it changes in the same direction.

## Placeholder cells (61)

| Cell | Agent | Part | Placeholder | Retention | Real result |
|---|---|---|---|---|---|
| CO-I1-E4 | Copilot | through UI actions | can't tell | no_signal | |
| CO-I1-E6 | Copilot | through UI actions | can't tell | no_signal | |
| CO-NLF-I0000 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0002 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0010 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0023 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0024 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0026 | Copilot | through prompts | can't tell | no_signal | |
| GE-NLF-I0032 | Gemini | through prompts | can't tell | no_signal | |
| CO-NLF-I0036 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0041 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0043 | Copilot | through prompts | recall failed | shown | |
| GE-NLF-I0045 | Gemini | through prompts | can't tell | no_signal | |
| CO-NLF-I0045 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0047 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0053 | Copilot | through prompts | can't tell | no_signal | |
| GE-NLF-I0060 | Gemini | through prompts | can't tell | no_signal | |
| CO-NLF-I0060 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0067 | Copilot | through prompts | recall failed | shown | |
| GE-NLF-I0090 | Gemini | through prompts | can't tell | no_signal | |
| CO-NLF-I0096 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0099 | Copilot | through prompts | recall failed | shown | |
| CO-NLF-I0121 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0124 | Copilot | through prompts | recall failed | shown | |
| CO-NLF-I0133 | Copilot | through prompts | recall failed | shown | |
| CO-NLF-I0137 | Copilot | through prompts | recall failed | shown | |
| CO-NLF-I0140 | Copilot | through prompts | recall failed | shown | |
| GE-NLF-I0141 | Gemini | through prompts | can't tell | no_signal | |
| GE-NLF-I0146 | Gemini | through prompts | can't tell | acknowledged | |
| CO-NLF-I0146 | Copilot | through prompts | recall failed | shown | |
| CO-NLF-I0153 | Copilot | through prompts | recall failed | shown | |
| CO-NLF-I0165 | Copilot | through prompts | recall failed | shown | |
| CO-NLF-I0169 | Copilot | through prompts | recall failed | shown | |
| CO-NLF-I0177 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0181 | Copilot | through prompts | recall failed | shown | |
| GE-NLF-I0182 | Gemini | through prompts | can't tell | no_signal | |
| CO-NLF-I0195 | Copilot | through prompts | recall failed | shown | |
| CO-NLF-I0201 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0209 | Copilot | through prompts | recall failed | shown | |
| GE-NLF-I0230 | Gemini | through prompts | can't tell | no_signal | |
| CO-NLF-I0236 | Copilot | through prompts | recall failed | shown | |
| GE-NLF-I0237 | Gemini | through prompts | can't tell | no_signal | |
| CO-NLF-I0239 | Copilot | through prompts | recall failed | shown | |
| GE-NLF-I0241 | Gemini | through prompts | can't tell | no_signal | |
| CO-NLF-I0241 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0252 | Copilot | through prompts | recall failed | shown | |
| CO-NLF-I0264 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0279 | Copilot | through prompts | recall failed | shown | |
| CO-NLF-I0293 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0302 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0309 | Copilot | through prompts | recall failed | shown | |
| CO-NLF-I0319 | Copilot | through prompts | can't tell | no_signal | |
| GE-NLF-I0326 | Gemini | through prompts | can't tell | no_signal | |
| CO-NLF-I0339 | Copilot | through prompts | recall failed | shown | |
| CO-NLF-I0345 | Copilot | through prompts | can't tell | no_signal | |
| GE-NLF-I0350 | Gemini | through prompts | can't tell | no_signal | |
| CO-NLF-I0351 | Copilot | through prompts | recall failed | shown | |
| CO-NLF-I0364 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0365 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0367 | Copilot | through prompts | can't tell | no_signal | |
| CO-NLF-I0371 | Copilot | through prompts | recall failed | shown | |

Three of these (CO-NLF-I0096, GE-NLF-I0230, GE-NLF-I0350) were recalled and await review, so their real result is the reviewed one.

## Section 5 numbers that depend on placeholders

Each row: where it is, the number with its placeholders, and the number on real results only (804 base) for reference. After recall, replace each with the re-counted number.

### 5.1 Overall Behavior of Agents

| Sentence | In the paper (865 base) | On real results only |
|---|---|---|
| Headline base | 865 test cases | 804 |
| Recall success | 18.7% (162) | 20.1% (162) |
| Recall failed | 26.8% (232) | 26.1% (210) |
| Can't tell | 54.5% (471) | 53.7% (432) |
| "nearly one in five" and "at least 18.7%" | follow the recall success share | would read "at least one in five" (20.1%) |
| Deleting a specific saved memory | 2 of 7 | 2 of 6 |
| Sending a deletion-request prompt: recall success | 144 of 811 | 144 of 752 |
| Sending a deletion-request prompt: can't tell | 454 of 811 | 417 of 752 |
| Gemini can't tell | 138 of 145 | 126 of 133 |
| Copilot can't tell | 81 of 145 | 54 of 96 |

Placeholders behind these: Copilot 22 recall failed and 27 can't tell, Gemini 12 can't tell. If any come back as recall success, the recall success rows rise and the "nearly one in five" wording changes.

### 5.2 Cross-Agent Difference

| Sentence | In the paper (865 base) | On real results only |
|---|---|---|
| Copilot recall failed, typed requests | 57 of 133 (35 real + 22 placeholders) | 35 of 86 |
| Copilot can't tell, typed requests (not stated, implied by "the rest") | 76 of 133 (51 real + 25 placeholders) | 51 of 86 |
| Gemini can't tell, typed requests ("every test case was can't tell") | 133 of 133 (121 real + 12 placeholders) | 121 of 121 |
| "we found none [withheld] for the other four agents" | assumes none among the 59 typed-request placeholders (47 Copilot, 12 Gemini), which have no recall reply to read | none among the replies in the review sheets (`Compare/RefusalCheck/`, all marked 2026-11-02) |
| Copilot test cases consistent with the documentation, typed requests | 57 of 133 (35 real + 22 placeholders recall failed) | 35 of 86 |
| Base for "1 contradicted it" | 399 (352 real + 47 placeholders) | 352 |
| Consistent test cases where the fact came back | 107 of 318 (all ChatGPT, no placeholders involved); 211 recall failed | 107 of 296 |
| Wording: "On Claude and Copilot, recall success never occurred under any code" | Copilot: 57 known outcomes, of which 22 are placeholders (recall failed), so true by construction for those 22 | 35 known outcomes, none recall success |

After recall: rebuild the Copilot and Gemini review sheets for the new rows (the builder overwrites existing marks, so copy the marked rows across first), re-run `src.recall_refusals`, and re-check the sentence.

### 5.3 What Agents Say

The reply counts themselves (798 deletion requests typed in the chat: 299 complied, 267 partial, 168 deflected, 8 refused, 7 silently ignored, 42 other, 7 not captured) are real: every erase reply, including those for Copilot and Gemini placeholders, is coded. They do not change when recall finishes. Only the recall splits below depend on placeholders.

| Sentence | In the paper (865 base) | On real results only |
|---|---|---|
| Recall success after complied replies | 11 of 299 (43 test cases without a real recall result) | 11 of 256 |
| Recall success after partial replies | 101 of 267 (10 without a real recall result) | 101 of 257 |
| Can't tell after deflected replies | 144 of 168 (5 placeholders) | 139 of 163 |

### 5.4 User Expectation vs. Behavior

The same-conversation counts (ChatGPT 104 of 108, Claude 86 of 130) are on complete agents and do not depend on placeholders. The survey shares do not either.

| Sentence | In the paper (865 base) | On real results only |
|---|---|---|
| Interface showed the change | 49 test cases (47 real + 2 placeholders, CO-I1-E4 and CO-I1-E6) | 47 |
| Of those, can't tell | 16 (14 real + 2 placeholders) | 14 |



- Methods. It states 865 test cases and doesn't explain that 61 are placeholders. That is deliberate, since the final numbers will agree, but a reminder: the "at least 18.7%" wording in 5.1 is the one sentence whose wording, not just a number, changes if any placeholder becomes recall success.
- The three pending reviews (CO-NLF-I0096, GE-NLF-I0230, GE-NLF-I0350).
- The claim ledger, which we agreed is later.

