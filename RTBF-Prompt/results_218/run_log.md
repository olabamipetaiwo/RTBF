# Steps 1-4 re-run 2026-09-30 on data/RTBF_Survey_Results.xlsx (218 complete respondents), header offset fixed

## Step 1
Participant rows in export : 218
Prompt instances extracted : 417
Participants contributing  : 210
  answered both blocks     : 207
  Q4 only                  : 1
  Q5 only                  : 2
Per-block counts           : {'Q4': 208, 'Q5': 209}

wrote results_218/raw_prompts.csv  (columns: ['pid', 'block', 'method_context', 'prompt', 'rationale'])

## Step 2
analytic unit           : participant
participants (unit n)   : 210
prompt instances        : 417
prompts per participant : {2: 207, 1: 3}
participants w/ 2 prompts: 207
  identical in both blocks: 14 (6.8%)

## Step 3
input prompt instances                     : 417
within-participant EXACT repeats removed    : 15
within-participant NEAR repeats removed     : 7  (cos >= 0.9, char(3, 5))
analysis pool (cross-participant dups kept) : 395   -> results_218/step3_analysis_pool.csv
  participants represented                 : 210
global exact duplicates removed for cluster : 18
unique phrasings (clustering input)         : 377   -> results_218/step3_unique_phrasings.csv

## Step 4
rows                 : 377
prompts altered      : 7 (1.9%)
redactions by type   : {'[LOCATION]': 10}
wrote results_218/step4_scrubbed.csv  (new column: prompt_scrubbed)
