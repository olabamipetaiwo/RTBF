# RTBF Prompt Analysis — Artifact

This repository accompanies our paper on right-to-be-forgotten (RTBF) deletion
prompts. It contains the raw survey export and the analysis scripts used to
produce the results reported in the paper, starting with Step 1 (extraction).

## Contents

- `data/RTBF.qsf` — Qualtrics survey definition (for reference; not needed to run the scripts)
- `data/RTBF_Survey_Results.xlsx` — raw Qualtrics results export (input data)
- `extract_prompt.py` — Step 1: extracts one row per deletion-prompt instance into tidy long format
- `unit.py` — Step 2: reports the analytic unit (participant) and within-participant non-independence (exact-duplicate phrasing across blocks)
- `normalize.py` — Step 3: normalizes text and collapses within-participant exact/near-duplicate prompts
- `scrub_pii.py` — Step 4: redacts structured PII (regex) and named entities (spaCy) into a new `prompt_scrubbed` column
- `feature_extraction.py` — Step 5: deterministic rule-based labeling (deletion locus, data granularity, syntactic form, politeness, verb register, justification)
- `build_sheet.py` — Step 6a: samples items from Step 5's labels and builds blind coder sheets, a hidden rule key, and a codebook, for human-coding validation of the Step 5 labels
- `score_sheet.py` — Step 6b: run after two humans fill in the coder sheets independently; scores inter-coder agreement and rule-vs-human accuracy
- `csv_to_excel.py` — packages the Step 6a coder sheets + codebook into one Excel workbook for handing to coders
- `chart.py` — descriptive survey charts (chatbot usage/tenure, deletion method by scenario), run independently of the Step 1-6 pipeline, directly on the raw Qualtrics export
- `results/` — script outputs (e.g. `raw_prompts.csv`, `step3_analysis_pool.csv`, `step3_unique_phrasings.csv`, `step4_scrubbed.csv`, `step5_labeled.csv`)
- `results/codebook/` — Step 6 outputs (coding sheets, rule key, codebook, packaged Excel workbook)
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.11+
- pip

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running Step 1: Extraction

```bash
python extract_prompt.py --xlsx data/RTBF_Survey_Results.xlsx --out results/raw_prompts.csv
```

Always pass `--out` explicitly and point it somewhere other than
`data/RTBF_Survey_Results.xlsx` — the script overwrites whatever path you give
it, and the input file must not be clobbered.

This reads the raw export and writes the output CSV with one row per
deletion-prompt instance, columns:

- `pid` — participant ResponseId
- `block` — `Q4` or `Q5` (within-subject source block)
- `method_context` — the deletion method the participant selected in that block
- `prompt` — the free-text deletion message
- `rationale` — the participant's stated rationale for phrasing (coding-validation metadata, not a prompt itself)

Expected console summary on the current data:

```
Participant rows in export : 217
Prompt instances extracted : 415
Participants contributing  : 209
  answered both blocks     : 206
  Q4 only                  : 1
  Q5 only                  : 2
Per-block counts           : {'Q4': 207, 'Q5': 208}
```

If your numbers differ, the export file has changed since this artifact was
prepared.

## Running Step 2: Unit-of-analysis check

```bash
python unit.py
```

Takes no arguments; reads `results/raw_prompts.csv` directly (run Step 1
first). Reports the analytic unit (participant, not prompt instance), how many
prompts each participant contributes, and — among participants who wrote a
prompt in both blocks — how often the Q4 and Q5 phrasing is exactly identical
(non-independence evidence used to justify later analytic choices).

Expected console summary on the current data:

```
analytic unit           : participant
participants (unit n)   : 209
prompt instances        : 415
prompts per participant : {2: 206, 1: 3}
participants w/ 2 prompts: 206
  identical in both blocks: 14 (6.8%)
```

## Running Step 3: Normalize and dedup

```bash
python normalize.py --in results/raw_prompts.csv \
  --pool_out results/step3_analysis_pool.csv \
  --unique_out results/step3_unique_phrasings.csv
```

Takes Step 1's output and produces two files:

- `step3_analysis_pool.csv` — normalized; each participant's exact and near
  (cosine ≥ 0.90 over char 3–5 n-gram TF-IDF) repeats collapsed to one row
  (longer text kept, ties → Q4). Cross-participant duplicates are **preserved**
  — this is the prevalence-safe pool.
- `step3_unique_phrasings.csv` — the analysis pool with global exact
  duplicates also removed; input to clustering / test-set selection.

Normalization (`prompt_norm`) applies Unicode NFKC, folds curly quotes/dashes
to ASCII, lowercases, and collapses whitespace; the original text is kept in
`prompt`. Dedup and near-dup collapse only ever compare a participant against
their own other prompt — never across participants.

Expected console summary on the current data:

```
input prompt instances                     : 415
within-participant EXACT repeats removed    : 15
within-participant NEAR repeats removed     : 7  (cos >= 0.9, char(3, 5))
analysis pool (cross-participant dups kept) : 393   -> results/step3_analysis_pool.csv
  participants represented                 : 209
global exact duplicates removed for cluster : 18
unique phrasings (clustering input)         : 375   -> results/step3_unique_phrasings.csv
```

## Running Step 4: PII scrub

`spacy`'s CLI imports `click`, which is not reliably pulled in as a transitive
dependency (an installed `typer` version may not declare it) — install it
explicitly, then fetch the spaCy model, both one-time setup steps:

```bash
pip install click
python -m spacy download en_core_web_sm
```

Then run:

```bash
python scrub_pii.py --in results/step3_unique_phrasings.csv --out results/step4_scrubbed.csv
```

Takes Step 3's unique-phrasings output and adds a `prompt_scrubbed` column:
regex redaction first (email, URL, SSN, card number, phone, ZIP, @-handle),
then spaCy named-entity redaction (PERSON, GPE/LOC/FAC → `[LOCATION]`, ORG,
NORP). The original `prompt` column is left untouched; `prompt_scrubbed` is
the display column for the paper. Prints how many prompts were altered and a
count of redactions by placeholder type.

Expected console summary on the current data:

```
rows                 : 375
prompts altered      : 32 (8.5%)
redactions by type   : {'[LOCATION]': 12, '[ORG]': 20, '[PERSON]': 3}
```

## Running Step 5: Feature extraction (labeling)

```bash
python feature_extraction.py --in results/step3_unique_phrasings.csv \
  --col prompt --out results/step5_labeled.csv
```

Deterministic, rule-based (regex) labeling — runs on the original `prompt`
text, not the scrubbed version, and needs no additional dependencies. Adds
per-row columns:

- `deletion_locus` / `deletion_locus_multilabel` — WHERE the prompt asks the
  data to be removed from (`memory`, `conversation`, `account_all`,
  `backend_db`, `prospective`, or `unspecified`); first match wins for
  `deletion_locus`, all matches kept, pipe-joined, in
  `deletion_locus_multilabel` (precedence = pattern list order in the script)
- `data_granularity` — WHAT unit of data is targeted, independent of locus:
  `specific_item` (one named piece of data) / `category` (an unnamed class)
  / `all` (explicit totality) / `unspecified`. Split out from the old
  `scope`'s `item` value, which conflated WHAT with WHERE.
- `syntactic_form` — grammatical mood only: `question` / `statement` /
  `imperative` / `other`
- `politeness` — `polite` / `bare`, independent of `syntactic_form`
- `politeness_n` — count of politeness markers (please, kindly, thanks, …)
- `verb_register` — `technical` (delete/erase/purge/…) vs. `lay` (forget/get
  rid of/…) vs. `mixed` vs. `none`
- `justification` — whether a reason/motivation was given (because, GDPR, …)
- `word_count`

`deletion_locus` and `data_granularity` used to be one conflated `scope`
column; `syntactic_form` and `politeness` used to be one conflated `form`
column. Split per advisor feedback so each dimension varies independently
(mirrors the WHERE/WHAT split common in privacy-taxonomy work, and the
mood/politeness-strategy split standard in speech-act and computational
politeness literature, e.g. Danescu-Niculescu-Mizil et al. 2013).

Expected console summary on the current data:

```
rows labeled : 375  (col='prompt')

DELETION_LOCUS:
deletion_locus
unspecified     40.0
memory          19.5
conversation    19.2
account_all     14.7
prospective      3.7
backend_db       2.9

DATA_GRANULARITY:
data_granularity
specific_item    72.5
unspecified      18.7
all               5.1
category          3.7

SYNTACTIC_FORM:
syntactic_form
imperative    67.2
other         20.8
question       8.3
statement      3.7

politeness: {'polite': 219, 'bare': 156}
verb_register: {'technical': 316, 'none': 25, 'lay': 23, 'mixed': 11}
justification: 13 (3.5%)
multi-locus prompts: 61
```

Note: `deletion_locus` unspecified jumped to 40% relative to the old
`scope`'s 12% — this is expected, not a regression: most prompts in this
survey name a specific piece of data (location) via `data_granularity`
without saying where it should be removed from, and that's now correctly
split into two separate facts instead of being hidden inside one `item`
scope value.

## Running Step 6: Blind human-coding validation

Step 6 checks whether Step 5's deterministic (regex) labels can be trusted,
by having two humans label a sample independently, blind to the automated
labels, and comparing.

### Step 6a: build the coder sheets

```bash
mkdir -p results/codebook
cd results/codebook
python ../../build_sheet.py --in ../step5_labeled.csv
cd ../..
```

Takes Step 5's output and writes four files into `results/codebook/`:

- `step6_coding_sheet_coder1.csv`, `step6_coding_sheet_coder2.csv` — identical
  blank sheets, one per coder: `item_id` and `prompt` only, plus empty
  `deletion_locus_all`, `deletion_locus_primary`, `data_granularity`,
  `syntactic_form`, `politeness`, `verb_register`, `justification`, `notes`
  columns for the coder to fill in. Both coders get the same sampled items so
  agreement between them can be measured. No automated labels are included,
  so coding is blind.
- `step6_rule_key.csv` — the hidden automated labels for those same items
  (`deletion_locus`, `deletion_locus_multilabel`, `data_granularity`,
  `syntactic_form`, `politeness`, `verb_register`, `justification`), plus
  `rationale` (the participant's own "why did you phrase it this way?"
  answer, carried through from Step 1) for your reference when adjudicating
  disagreements afterward. Not shown to coders.
- `step6_codebook.md` — the coding manual: for every column in the coder
  sheet, what it means, the allowed values, and what each value means.

The sample is stratified by Step 5's `deletion_locus` label with a floor of
15 items per locus, so rare loci aren't left out. Because the floor can push
small loci above their proportional share, the sampled total can exceed
`--target`.

Expected console summary on the current data:

```
sampled 137 of 375 (floor=15/locus, seed=42)
per-locus: {'unspecified': 48, 'memory': 23, 'conversation': 23, 'account_all': 18, 'prospective': 14, 'backend_db': 11}
```

Optionally, package the two blank sheets and the codebook into a single
workbook to hand to coders:

```bash
python csv_to_excel.py
```

Writes `results/codebook/step6_coding_sheets.xlsx` with three sheets:
`instructions` (the codebook), `coder1`, `coder2`.

### Step 6b: score the filled-in sheets

Run only after both coders have filled in their sheets independently:

```bash
python score_sheet.py \
  --coderA results/codebook/step6_coding_sheet_coder1.csv \
  --coderB results/codebook/step6_coding_sheet_coder2.csv \
  --key results/codebook/step6_rule_key.csv
```

Reports, in order:

- inter-coder agreement (% agreement, Cohen's kappa, Krippendorff's alpha)
  for `deletion_locus_primary`, `data_granularity`, `syntactic_form`,
  `politeness`, `verb_register`, `justification`, plus mean Jaccard and
  per-locus kappa for the multi-label `deletion_locus_all`
- counts of disagreements per column, to adjudicate
- rule-vs-human accuracy: for items where both coders agree (the human gold
  label), how often the Step 5 automated label matches, plus a confusion
  matrix of human `deletion_locus_primary` vs. the automated `deletion_locus`

`krippendorff` is an optional dependency — if it isn't installed, alpha is
reported as `nan` and everything else still runs.

## Running the survey charts

```bash
python chart.py --xlsx data/RTBF_Survey_Results.xlsx --outdir results
```

Independent of the Step 1-6 pipeline above - reads the raw Qualtrics export
directly, not any of the `results/step*.csv` files. Restricts to
attention-check passers (`Q6.5 == "Sometimes"` and `Q9.3 == "Agree"`), a
filter not applied anywhere else in this repo, so these charts describe a
smaller population than the deletion-prompt analysis. Writes two PNGs to
`--outdir`:

- `chart_ai_usage_tenure.png` — stacked bar of which AI chatbots
  respondents use and for how long
- `chart_method_by_scenario.png` — ranked horizontal bars of the deletion
  method selected in each scenario (Q4 and Q5)

Expected console summary on the current data:

```
respondents: 217 total -> 201 attention-check passers

users per bot (attention-pass):
                   Less than 6 months  6 to 12 months  1 to 2 years  2+ years  total
ChatGPT                            33              26            64        76    199
Gemini                             46              50            58        28    182
Microsoft Copilot                  51              32            31        18    132
Claude                             49              41            27        12    129
Perplexity                         37              19            15         8     79
Deepseek                           26              19            17         3     65
```

## Notes on the input format

The Qualtrics export has three header rows before response data begins:
row 0 (short column header), row 1 (full question text), row 2 (ImportId
JSON). `extract_prompt.py` accounts for this automatically (`HEADER_ROWS = 3`).

This step performs no filtering, normalization, deduplication, or labeling —
those happen in later, separately reported steps.
