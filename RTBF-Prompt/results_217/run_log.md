# Steps 1-4 on data/RTBF_Survey_Results.xlsx with the attention screen (wrong answers only), 2026-09-30

## Step 1
Failed attention (excluded): 1
Participant rows kept      : 217
Prompt instances extracted : 415
Participants contributing  : 209
  answered both blocks     : 206
  Q4 only                  : 1
  Q5 only                  : 2
Per-block counts           : {'Q4': 207, 'Q5': 208}

wrote results_217/raw_prompts.csv  (columns: ['pid', 'block', 'method_context', 'prompt', 'rationale'])

## Step 2
analytic unit           : participant
participants (unit n)   : 209
prompt instances        : 415
prompts per participant : {2: 206, 1: 3}
participants w/ 2 prompts: 206
  identical in both blocks: 14 (6.8%)

## Step 3
input prompt instances                     : 415
within-participant EXACT repeats removed    : 15
within-participant NEAR repeats removed     : 7  (cos >= 0.9, char(3, 5))
analysis pool (cross-participant dups kept) : 393   -> results_217/step3_analysis_pool.csv
  participants represented                 : 209
global exact duplicates removed for cluster : 18
unique phrasings (clustering input)         : 375   -> results_217/step3_unique_phrasings.csv

## Step 4
rows                 : 375
prompts altered      : 7 (1.9%)
redactions by type   : {'[LOCATION]': 10}
wrote results_217/step4_scrubbed.csv  (new column: prompt_scrubbed)
