# DIDR: Data Injection–Deletion–Recall pipeline

Artifact for *"I Thought It Was Gone"* (IEEE S&P 2027 submission). DIDR injects a synthetic fact into an LLM agent, applies a deletion method, and checks 30 days later whether the fact can still be recalled. It drives each agent's web interface with Playwright.

> The flows in `flows/` reflect the agents' interfaces as of August–October 2026 and may need updating. The offline stages and tests do not depend on the agents.

**Not included:** our accounts, sessions, transcripts, results, survey responses, or participant-written deletion requests.

## Components

| DIDR stage | Code | Command |
|---|---|---|
| Synthetic fact generation | `1_fact_generation/` | `generate` |
| Injection (prompt / UI action) | `2_injection/` | `inject` |
| Deletion-request sampling | `3_deletion/sample_requests.py` | `sample-requests` |
| Deletion (prompt / UI action), ≥48 h after injection | `3_deletion/delete.py` | `delete` |
| Recall (UI check, indirect, direct), ≥30 days after deletion | `4_recall/` | `recall` |
| Outcome classification | `5_classification/` | `classify` |
| Agent automation | `flows/` | |

Test cases are rows in one workbook, `data/DIDR Test Cases.xlsx` (see `docs/workbook.md`).

## Setup

Python 3.11+ and Google Chrome.
```
pip install -r requirements.txt
python -c "import nltk; nltk.download('wordnet')"
```

## Quickstart (offline)

```
python -m pytest tests/
python pipeline.py init --design examples/design.csv
python pipeline.py generate
python pipeline.py sample-requests --requests examples/example_requests.csv --target 10 --floor 2
python pipeline.py status
```

## Live agents (your own accounts)

1. `python login_setup.py <agent> [--label NAME]`: log in by hand; the session is saved to `sessions/`. If Google sign-in rejects the browser, use `--from-chrome-profile`.
2. `python pipeline.py inject <ID> ...`
3. `python pipeline.py delete [<ID> ...]`. Gemini "Delete all activity" and the Copilot privacy dashboard must be done by hand; then run `delete <ID> --manual`.
4. `python pipeline.py recall [<ID> ...]`
5. Fill Storage evidence and resolve `REVIEW`/`PARTIAL` results from the saved transcripts, then `python pipeline.py classify`.

`--force` skips the waits (for testing only). Account-wide deletion methods erase every fact on the account, so give them a dedicated account.

## Claims supported

| Paper (Section 5) | Code | Test |
|---|---|---|
| Unique synthetic values, filtered word list | `1_fact_generation/generate_facts.py` | `test_generate_is_deterministic_and_unique` |
| Stratified sampling of deletion requests | `3_deletion/sample_requests.py` | `test_sample_requests_fills_prompt_cases` |
| 48 h / 30 day timeline | `didr/tracking.py` | `test_schedule_enforces_waits` |
| Recall check order; same-conversation check reported separately | `4_recall/recall.py` | `test_recall_order_and_scoring` |
| Recall success / recall failed / can't tell | `5_classification/classify.py` | `test_classification_rules`, `test_same_conversation_never_counts` |
| Reply scoring | `didr/recall_scoring.py` | `tests/test_recall_scoring.py` |

The paper's counts are not reproducible from this artifact: they come from live agents at a point in time.

## Ethics

Facts are synthetic and non-sensitive. Use only accounts you own and respect each agent's terms of service. Sessions and results are git-ignored.

## License

MIT (`LICENSE`). EFF word list: CC BY 3.0 US.
