Run it again after each recall batch:
cd RTBF-Analysis && .venv/bin/python -m src.expectation_gap
The script is src/expectation_gap.py. Output goes to outputs/results/expectation_gap.md, plus two CSVs in outputs/tables/. It reuses audit_outcomes.py for the recall verdicts and get_bases() for the survey, so it follows the one-source rule.

How it reads. Each cell is "recovered / decided". Decided means recovered plus not recovered, and recovered means the erasure failed. Each kind of empty cell gets its own code:
- ind: indeterminate
- wai: waiting for recall
- hel: held by design
- gat: free-tier gate
- .: the platform has no such method

Table B so far (typed "forget", 138 participant prompts):

┌───────────────────┬─────────┬────────┬─────────────┬───────────────────┬────────────────┬─────────────┐
│                   │ ChatGPT │ Claude │   Gemini    │      Copilot      │   Perplexity   │  DeepSeek   │
├───────────────────┼─────────┼────────┼─────────────┼───────────────────┼────────────────┼─────────────┤
│ recovered/decided │ 92/118  │ 0/117  │ – (all ind) │ 0/9 (109 waiting) │ 27/27 (93 ind) │ – (all ind) │
└───────────────────┴─────────┴────────┴─────────────┴───────────────────┴────────────────┴─────────────┘

Single-conversation delete: Claude 3/3 recovered. The other platforms have mostly 1/1 or indeterminate cells.

What I found while building it:
1. Expected feedback wasn't asked per method. Q7.1 asked what feedback people currently get, and Q7.2 what they want, once per participant (177). So that column is a separate block under Table A, not one value per row. The headline from Q7.2: 68% want a popup confirmation, and 41% want a breakdown of what was deleted versus kept.
2. The acknowledgment column is empty. None of the 865 erased cells has acknowledgment coded yet, so it shows "(not coded)" until that's done.
3. The workbook and my notes disagree on two Copilot cells. Copilot E5 (Privacy Dashboard) is marked RECALLED in the workbook, and CO-I1-E6 is marked ERASED. My notes say both were skipped and never run. One of those records is wrong, so please check which.
4. Some methods match on only one side. MAXIMAL and ChatGPT's "Clear custom instructions" have no survey counterpart, so they're listed as audit-only rows. "Delete my account" is survey-only.
5. The typed "forget" row is split in two: the fixed battery command and the 138 participant prompts. They share the same survey numbers.