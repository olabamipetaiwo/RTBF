# Artifact plan (rough)

Working draft. Nothing here has been applied to the repository or the paper.

## 1. Purpose

Release what lets a reader (a) check that every number in the paper comes from the data, and (b) rerun the Post-Deletion Behavioral Analysis on the same or other agents. The IEEE S&P CFP strongly encourages an anonymized artifact repository, and says it must not be updated after the paper deadline (Nov 17, 2026). So the repository has to be final before then.

## 2. What the artifact claims, and what it does not

Two levels of reproduction, stated plainly in the README:

- **Level A, recompute the paper's numbers.** Run the analysis scripts on the released processed data and get the paper's counts and tables (177 participants, 865 test cases, 394 judgeable, 162 recall success, AC1 values, and so on). This is fully reproducible.
- **Level B, rerun the study.** Run the automation against live agents with the reader's own accounts. This is not expected to give the same results, because agents change (the paper says so in Limitations). It is a method release, not a result reproduction.

## 3. Proposed contents

| Part | Source in this repo | Purpose |
|---|---|---|
| Survey analysis | `RTBF-Analysis/src`, `RTBF-Analysis/scipy_analysis`, `RTBF-Analysis/tests` | Section 4 numbers, tables, figures |
| Number check | `RTBF-Analysis/src/number_sources.py` | Maps each number in the paper to the script that produces it; exceptions list must stay empty |
| Post-deletion analysis outputs | `RTBF-Analysis/src/audit_outcomes.py` and the other outcome scripts | Section 5 numbers and tables |
| DIDR automation | `tester/` (Playwright flows, schedulers, recall scoring, run tracking) | Injection, deletion, and recall check on the six agents |
| Request corpus pipeline | `RTBF-Prompt/` (extraction, PII scrub, dedup, sampling) | How participant-written requests became the tested requests |
| Test-case table | master workbook / `tester/data/run_tracking.json` (de-identified) | The 865 test cases with outcome per cell |
| Coding sheets | `RTBF-Analysis/step6_coding_sheets.xlsx` and related | Reply coding, the basis for the AC1 values |
| Documentation | new top-level README, `docs/` | Setup, data dictionary, how to reproduce each table |

## 4. What must not be released

- `tester/sessions/`, cookies, any exported browser state (already git-ignored; confirm none is committed in history).
- `tester/transcripts/` raw conversations and screenshots (may contain account-identifying detail; already git-ignored).
- `tester/accounts.md` and anything with account emails or usernames. Release a version with the cell-to-account mapping but no identifiers, or only the account count per agent.
- Raw Qualtrics export (`data/raw/`), Prolific IDs, IP or location fields, free-text answers that were not scrubbed.
- `CLAUDE.md` files, `notes/`, `status.md`, review files, and the professor's `\xw` comments (not part of the repository anyway).
- Author names, institution names, local absolute paths (`/Users/...`), git author metadata, and comments that identify either. Also grep for the IRB number and funding.

## 5. Anonymization (required for submission)

- Host on Anonymous GitHub or GitFront, as the CFP suggests; use a neutral account and repository name.
- Create the repository from a fresh export, not from this git history, so commit authors (`olabamipetaiwo`) and messages do not leak.
- Strip author information from file headers, docstrings, notebook metadata, and `pyproject`/`requirements` metadata.
- After acceptance, replace the anonymous link with the real repository.

## 6. Repository layout (proposed)

```
README.md              what it is, the two levels, quick start
LICENSE                decision needed (see section 10)
analysis/              survey + outcome scripts (from RTBF-Analysis)
automation/            DIDR Playwright code (from tester)
requests/              request corpus pipeline (from RTBF-Prompt)
data/processed/        de-identified inputs needed for Level A
docs/                  data dictionary, number map, outcome rules, run protocol
```

## 7. Work needed before release

1. Sync README and results folders to the paper's corpus (the deferred item D5 in `notes/task.md`): README commands and expected outputs, `results_217` as the corpus, rerun Steps 5 and 6 on it.
2. Replace `tester/README.md`, which still says "Scaffolding only" and uses the retired term "technical audit".
3. Write the top-level README with a table that maps each paper table and figure to the command that makes it.
4. Remove the dead or duplicated files from the release copy (for example `method_slection.py`, `*_copy.png`, `.out` and `.log` run files, `$SCR`).
5. Confirm `src/number_sources.py` has an empty exceptions list on the release copy. It does not cover the demographic percentages, so either add them or list them as known.
6. Make sure the Level A path runs from a clean environment with only the released data (fresh venv, one command per table).
7. Write the data dictionary for the test-case table: cell id, agent, method, request, outcome, evidence fields.
8. Document the run protocol: account setup per agent, free tier only, dedicated accounts only for the most extensive deletion cells, the wait of at least 30 days, run window.
9. Run a leak scan on the release copy: emails, tokens, cookies, local paths, author names, institution, URLs of private repositories.

## 8. Paper changes (after the artifact exists, not before)

- A short artifact statement with the anonymous link (end of Introduction or Section 3, wherever the venue's norm and the page budget allow). Page limit is 13 pages of text plus 5 of references and appendix.
- Ethics Considerations: one sentence on intended use of the automation (research on one's own accounts, no access beyond the authenticated user) and that credentials and raw transcripts are excluded. The ethics section already says the study used only researcher-controlled accounts and that two agents needed a browser-stealth extension for automated sessions. The release should repeat that and state that the extension is not included, or is included with the same caveat (decision needed).
- Check that no wording in the paper still points to something the artifact leaves out.

## 9. Timeline

- Abstract registration: Nov 10, 2026.
- Paper deadline: Nov 17, 2026. The repository is frozen at this point. Aim to have the release copy and leak scan done a few days earlier so the link can go into the paper.

## 10. Open decisions for you

1. **Data scope.** Release the de-identified survey data, or only the aggregate outputs and scripts? The consent form permits future use of de-identified data in research and publication (Ethics section). Whether the IRB approval covers public release should be confirmed.
2. **Participant-written requests.** The tested requests came from participants. They were scrubbed for identifying information, but a public list of them is a separate step from using them in the analysis. Release as is, release a sample, or keep them out?
3. **Reply text and transcripts.** The agents' replies are part of the evidence. Release the extracted reply text only, or the coded categories only?
4. **Stealth extension.** Include it, document it, or leave it out?
5. **License.** For example MIT for code and CC BY for data. Pick one before release.
6. **Artifact evaluation.** Whether to submit for artifact evaluation if the venue offers it after acceptance. Decide later; it does not change the plan above.
