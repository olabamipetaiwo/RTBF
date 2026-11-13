# Workbook

`data/DIDR Test Cases.xlsx`, sheet `TEST CASES`, one row per test case. Create with `python pipeline.py init [--design file.csv]`. Transcripts and screenshots go to `results/<agent>/<ID>/`.

## You fill

| Column | Values |
|---|---|
| Test case ID | Unique, e.g. `CH-01` |
| Agent | `chatgpt`, `claude`, `gemini`, `copilot`, `perplexity`, `deepseek` |
| Injection method | `prompt`, `memory-request prompt`, `UI action` |
| Deletion method | `deletion-request prompt`, `delete a single conversation`, `clear all conversation history`, `delete a specific saved memory`, `clear all saved memories`, `use a privacy dashboard`, `clear custom instructions`, `most extensive procedure` (availability per agent: `didr/methods.py`) |
| Account | Blank = `sessions/<agent>.json`; a label = `sessions/<agent>__<label>.json` |

## Pipeline fills

| Stage | Column | Content |
|---|---|---|
| | Status | `generated`, `injected`, `deleted`, `recalled`, `classified` |
| 1 | Entity, Value, Disclosure sentence, recall prompts | Synthetic fact and its prompts |
| 2 | Injected at, Conversation reference | Time (UTC) and conversation URL |
| 2 | Storage evidence | Written as `review`; replace with `yes (...)` or `no` |
| 3 | Deletion request text | Deletion-request prompts only |
| 3 | Deleted at, Agent response | |
| 3 | Response code | You code it (`docs/response_codebook.md`) |
| 4 | Recalled at, UI-based check / Indirect / Direct recall result | `TOKEN FOUND`, `NOT FOUND`, `N/A`, or `REVIEW`/`PARTIAL` |
| 4 | Same-conversation result | Reported separately; not counted |
| 5 | Recall outcome | `recall success`, `recall failed`, `can't tell`, `needs review` |

Storage evidence is `yes` only after an explicit memory notification or an explicit agent confirmation, or when the fact was typed into a saved-memory page. Before classifying, set every Storage evidence and overwrite every `REVIEW`/`PARTIAL` cell with `TOKEN FOUND (reviewed)` or `NOT FOUND (reviewed)`.
