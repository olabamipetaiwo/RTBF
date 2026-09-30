# Tasks: resolve paper.tex inconsistencies -  ""
 
**Working rules (agreed 2026-09-30):** one item at a time; first explain the problem and the data behind it, then propose the fix, apply only after your OK. Paper is a scientific paper, not a project report (no process history). Every percentage must name a consistent base: 177 participants / 354 observations / 317 four-method observations. Survey tests: SciPy (`scipy_analysis`) where covered, `src` (statsmodels) for GEEs, factor analysis, regressions.

**Status at handoff (2026-09-30):** section A done (A1-A9), B1 done. Next: B2, then B3-B12, C, D, E. Yao's meeting feedback (she) is still to be handled after B; only her scale-to-factor edit is applied so far (`RTBF-Analysis/paper/paper-yao-edit.tex` is her copy, made before today's changes; do not merge it wholesale).

Source: `notes/inconsistencies.md` (line numbers refer to paper.tex as audited 2026-09-30). One item at a time; tick when fixed in the paper and the source note agrees. "Decision" = needs your call first.    

## B. Numbers and wording
- [ ] **B7** 436-437: "35 redactions across 32 prompts".
- [ ] **B8** 1029: mark the post-deletion feedback item as select-all; mention omitted 4.0% / 2.3%.
- [ ] **B9** 498-499 vs 567-568: one wording, "verbatim except the referent".
- [ ] **B10** 499: reconcile "not regenerable" with the logged seed=42 / 137-item draw; say how the 138th item came about.
- [ ] **B11** 433-435: confirm the prompt extraction export (217 rows) vs 218 complete respondents; state the export or fix.
- [ ] **B12** Title (29) vs `pdftitle` (27): make the PDF metadata match.

## C. Text defects

- [ ] **C1** 140: remove or fix the "see \S\ref{sec:intro}" pointer to Li et al.'s platforms.
- [ ] **C2** 78, 83: fix LaTeX quote marks.
- [ ] **C3** 1277: fix "extracted form this too," (typo, unfinished sentence).
- [ ] **C4** Reference the pipeline figure (`fig:testing-pipeline`) in the text.
- [ ] **C5** Add an order-confound caveat where the protection shift (991) is reported.
- [ ] **C6** Re-check Discussion forward references (1111-1132, 1174-1186) once Results exist.
- [ ] **C7** Before submission: remove author TODO comments and resolve the Ethics placeholders.

## D. Open placeholders (after the above)

- [ ] **D1** Abstract, Technical Audit Results, Limitations, Conclusion (all `TBWL`).
- [ ] **D2** Methods TODOs: FOUND-reply spot check and reviewer agreement (722-725); recovery of incomplete OCR replies (826-828).
- [ ] **D3** Sheet check: NL FORGET Email column vs Gemini's separate account, before accounts are described in Methods.

## E. Possible additions (not in the paper now)

- [ ] **E1** Moderator analysis (`src/moderators.py`, age group / ChatGPT tenure vs ratings, willingness and method choice): not reported in the paper. Ratings and willingness show no effect; age group vs method choice in the less-sensitive scenario is nominally significant (Fisher p = .016 raw) and would need multiple-comparison handling if added. Decision deferred; paper stays as is for now.
