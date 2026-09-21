# RTBF Survey Analysis

Analysis of a within-subject survey study on data-deletion methods for AI chatbots. Two scenario blocks (`Q4` = less sensitive data, `Q5` = more sensitive data) repeat the same question battery.

## Setup

Requires [`uv`](https://docs.astral.sh/uv/).

```bash
uv venv .venv --python 3.11
uv pip install -r requirements.txt --python .venv
```

## Running

Run scripts as modules from the repo root, via `uv run` (no need to activate the venv manually):

```bash
uv run python -m src.screen
```

This loads `data/raw/RTBF_survey_results.xlsx`, applies the `Q6.5` attention check, prints N retained / N dropped, and writes the screened frame to `data/processed/screened.csv`.

To run the equivalent notebook:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/00_screen.ipynb
# or open it normally: uv run jupyter notebook notebooks/00_screen.ipynb
```

## Repo structure

```
data/raw/         Raw Qualtrics export — read-only, never overwritten
data/processed/   Screened/cleaned output (written by src/screen.py)
src/config.py     Named constants: column groups, scenario mapping, attention-check spec
src/load.py       Parses the raw xlsx into a clean DataFrame + question-ID -> text map
src/screen.py     Applies the attention check; writes data/processed/screened.csv
notebooks/        One notebook per analysis step, thin wrappers around src/
outputs/tables/   Generated tables
outputs/figures/  Generated figures
```

## Data notes

- The raw export has **2 metadata header rows** (question ID, full question text), not the standard 3-row Qualtrics format — there's no ImportId-JSON row. Data starts at row 2 (0-indexed). See `src/config.py`.
- The scenario mapping (`Q4` = less sensitive, `Q5` = more sensitive) is **not encoded in the export** — it's hard-coded in `src/config.py` from the survey design.
- Analysis base is currently gated only on the `Q6.5` attention check (205 retained / 14 dropped as of the last raw export). A second gate — restricting to respondents who have deleted data before — is a `TODO` in `src/screen.py`, pending confirmation of the exact column (`Q3.2_1`..`Q3.2_9` / `Q3.2_13` is the current best candidate).





<!-- Not done — and this is the gap: paper.tex has zero mention of the coding comparison or AC1 anywhere (I grepped for kappa/AC1/Gwet/agreement/inter-rater — nothing). The Methodology section only covers the technical audit (injection/erasure/recall); the qualitative prompt-coding study (deletion_location/justification/what/mood/tone/verb/accompanying_request, 138 items, two coders) isn't written up at all yet, and Results §"Technical Audit" (line 549) is still a TODO stub. -->
