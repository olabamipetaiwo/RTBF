# Prompt pipeline, Steps 1-4: what happened (traced 2026-09-30)

Every count below was re-derived by re-running the scripts on the recorded
input into a scratch folder (project results untouched). With the code as it
was, Steps 1 and 3 reproduce the saved `results/raw_prompts.csv` and
`results/step3_unique_phrasings.csv` byte for byte, so the pipeline is
deterministic.

## Input

`data/RTBF_Survey_Results.xlsx` (Qualtrics export, 2026-07-27; identical in
content to `RTBF_July+28,+2026_01.25.xlsx`): 220 sheet rows = 2 header rows
(short names, question text) + **218 data rows**, all `Finished == True`,
responses dated 2026-06-25 to 2026-07-21. Questions read: Q4.11 (less-sensitive
scenario) and Q5.11 (more-sensitive scenario), "what would your message be?",
with the participant's method (Q4.2/Q5.2) and rationale (Q4.12/Q5.12).

This is not the file the survey analysis reads
(`RTBF-Analysis/survey/RTBF_September+9,+2026_14.25.xlsx`, 235 submissions, 218
complete); both have the same 218 complete respondents, collected in the same
window.

## Step 1: extraction (`extract_prompt.py`)

One row per non-blank prompt per block, no filtering.

**Defect found.** The script sets `HEADER_ROWS = 3` (its docstring says row 2 is
an ImportId row), but this export has only 2 header rows. The first data row
(respondent `R_7fThEZ0Dj0u37Pj`, complete, 2026-06-25, who wrote both
prompts) is therefore skipped as a header.

| | As run | Header fixed |
|---|---|---|
| Participant rows read | 217 | 218 |
| Prompt instances | 415 | 417 |
| Participants contributing | 209 | 210 |
| Answered both blocks | 206 | 207 |
| Per block (Q4 / Q5) | 207 / 208 | 208 / 209 |

The 217-versus-218 mismatch noted in the paper audit (B11) is this defect.
The file itself holds 417 typed prompts (208 + 209 non-blank), 2 more than
were extracted.

## Step 2: unit of analysis (`unit.py`)

Reads Step 1's output; participant is the unit. As run: 206 participants wrote 2
prompts, 3 wrote 1; 14 of 206 (6.8%) wrote identical text in both blocks.

## Step 3: normalize and deduplicate (`normalize.py`)

Normalization (NFKC, curly quotes and dashes folded, lowercase, whitespace
collapsed) builds the comparison key; the original text is kept. Within a
participant only: exact repeats removed, then near repeats (cosine similarity at
least 0.90 over character 3-5-gram TF-IDF; longer text kept, ties to Q4).
Cross-participant duplicates are kept in the analysis pool and removed only for
the unique list.

| | As run | Header fixed |
|---|---|---|
| Input prompts | 415 | 417 |
| Within-participant exact repeats removed | 15 | 15 |
| Within-participant near repeats removed | 7 | 7 |
| Analysis pool (cross-participant duplicates kept) | 393 | 395 |
| Global exact duplicates removed | 18 | 18 |
| Unique phrasings | 375 | 377 |

The missing respondent's two prompts are both new phrasings, so each adds one
row to the pool and one to the unique list.

## Step 4: PII scrub (`scrub_pii.py`)

Regex for structured identifiers, spaCy entities for names and places, written
to a `prompt_scrubbed` display column (originals kept). Corrected on
2026-09-30: spaCy had tagged the verb "Delete" (19 times), "chatbot"/"AI" as
organizations, people or places; 25 of the 35 original redactions were false
positives. A word-list exclusion now applies; result 7 of 375 prompts altered,
10 location redactions, all read by hand.

## Not traced here

How the 138 audit prompts were selected from this corpus is not recorded in
Steps 1-4. Nothing in these steps reduces 375 to 138.
