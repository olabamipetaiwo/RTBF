## TASK

**Working rules:** one item at a time; explain the problem and the data, propose the fix, apply after the OK. The paper is a scientific paper, not a project report. Name the base of every percentage (177 participants / 354 observations / 317 four-method observations). Every number needs a saved source: `scipy_analysis` first, then `src`. Delete an item once it is done.

# EXPERIMENTS

- [ ] **X8** Two hand-coded measurements for the outcomes module (`python -m src.audit_outcomes`): **Acknowledgment** — Taiwo's 655 cells coded, Jihwan's coding pending, then compute Gwet's AC1 agreement. **Interface change** for the 54 battery cells erased through the interface (typed requests are "not observable" and need no coding).
- [ ] **D2a** Count the auto-accepted FOUND replies across all recalled cells. A few dozen: a person reads all. Hundreds: draw a random sample. Second-reviewer agreement (Gwet's AC1) is a separate decision.
- [ ] ChatGPT human review: 4 cells pending (CH-I1-E5, CH-I1-E7, CH-I2-E7, CH-I3-E7) + CH-IF-E-MAX. Read transcripts and confirm verdicts.

# WRITE

- [ ] **D1** After recall: the Abstract, Technical Audit Results and Conclusion (the `TBWL` markers). Include the Gemini Keep observation (7 of 133 chat-based erasure requests, nothing deleted), re-check the Discussion's three audit forward references ("takes up directly", "check independently", "the mismatch RQ5 measures"), and add to the audit Limitations: incomplete OCR replies only if some stay uncaptured (D2b), the order result (C5).
- [ ] **C5** Scenario order was randomized but is not in the current export. You re-export the responses from Qualtrics with "viewing order data for randomized surveys" (check 235 rows, 218 complete). Then compute each respondent's order, test whether the scenario shift differs by order, check the split is roughly even, and report it in the paper and in Limitations.
- [ ] **C4b** After your professor's changes to the pipeline figure (`fig:testing-pipeline`): re-check the caption, the sentence citing it (Technical Audit opening) and where the figure sits; update the recall stages in `testing_pipeline_overview.svg` and `.png` (one new-conversation recall plus one same-conversation request).

# REVIEW

- [ ] **D4** Confirm with whoever produced the 138-prompt list how it was drawn. It is recorded as stratified on the automated deletion-location label (before its revision) with a floor (`RTBF-Prompt/results/prompt_clean.md`); you remember no dimension being involved. If not confirmed, rewrite the paragraph at `paper.tex` line ~482.
- [ ] **C7** Before submission, last. Status 2026-10-01: `cd RTBF-Analysis/paper && python3 make_submission.py --number <HotCRP number>` runs; its only failure is the 3 `TBWL` placeholders (Abstract line 30, Audit Results ~1047, Conclusion ~1179 of the output), i.e. D1. LaTeX is not installed on this machine, so the paper has not been compiled since the policy-source appendix and the 40-odd edits were added: compile `paper_submission.tex` on Overleaf or elsewhere and check the two new appendix tables fit the page. Then: upload only `paper_submission.tex`; check the Ethics text matches the HotCRP Ethics field; check the account records (`config.py`, `accounts.md`, workbook Email column) match the isolation sentence in Methods; check the OpenAI and Perplexity help-page quotes (Appendix `sec:policy-sources`) still match the live pages; re-run `python -m src.number_sources` (in `RTBF-Analysis`) after any number changes and confirm its exceptions table is empty.
