# paper.tex consistency audit (2026-09-30)

Scope: `RTBF-Analysis/paper/paper.tex` read top to bottom (1377 lines). Every number was checked against the paper itself and, where a source exists, against the data: `RTBF-Analysis/outputs/results/*.md`, `outputs/tables/*.csv`, the raw Qualtrics export (recomputed in a scratch script), `RTBF-Prompt/data/RTBF Experiments.xlsx`, `tester/` (config, flows, transcripts, accounts.md) and `Compare/*/agreement_report.md`.

Nothing in the paper was edited. Line numbers refer to paper.tex as of this audit. "Decision" marks items that need your call, not just a fix.

---

## A. Contradictions (fix before adding results)

### A1. Fourth Pass agreement (n=138) is not in the paper; paper still says 50 items
- Paper 451 ("Each dimension was coded on 50 items"), 457-458, Table `tab:ac1` (469-492, n=50, pooled AC1 0.905) all match the **Third Pass** report.
- `Compare/Fourth Pass/agreement_report.md` (new, untracked) reports n=138 per dimension: deletion_location 0.890, justification 0.943, what 0.956, mood 0.959, tone 0.990, verb 0.947, accompanying_request 0.962, **pooled AC1 0.954** (923/966 = 95.5%).
- Every per-dimension value and the pooled value differ from Table `tab:ac1`. The 138 items are the same 138 that feed the audit, so the paper's "50 items" and the audit sample are now out of step.
- Decision: which pass is the paper's reported reliability? If Fourth Pass, rewrite 451-458, the table, its caption and the footnote at 491, and the statement at 460-467 that the deletion-location reliability is "reported on a sample coded under the final definition". If Third Pass stays, the Fourth Pass files should not be cited anywhere.

### A2. "A researcher-controlled account" per platform vs many accounts
- 509-510 ("Each platform is tested through a researcher-controlled account"), 843-844 ("All six accounts are provisioned on each platform's free, no-cost tier"), 1303-1304 ("all six accounts were free-tier accounts") read as one account per platform (six in total).
- The paper's own Contamination control paragraph (596-620) describes dedicated accounts per blanket cell and a separate NL-forget account per platform. `tester/accounts.md` lists a main account plus dedicated `maximal_i1`, `maximal_i2`, `maximal_i3`, `maximal_file` accounts; the workbook's battery rows use 12 distinct emails.
- Fix: say "accounts" (plural, number of accounts per platform) in all three places. Also decide whether to state the total account count in Methods. (You confirmed every account is on a free tier, so the free-tier claims at 844 and 1304 are correct; only "six accounts" and "a ... account" need fixing.)

### A3. Two different denominators in the same Results subsection (expectations vs verification) and Discussion
- Expectations text (1023): 59.0, 54.2, 49.2, 28.5, 27.7, 10.5%. I recomputed these from the raw data: they are over **all 354** participant-scenario observations (including Clear-all-memories, Privacy dashboard, Delete account, Other).
- Verification text (1025): 46.7, 20.5, 19.2, 15.8, 14.5, 11.4%. These equal the "All (317)" row of Table `tab:verification`, i.e. the **four qualifying methods only (317)**. On the 354 base the same items are 44.6, 20.6, 21.8, 16.1, 17.5, 10.2%; note the order of "same conversation" and "new conversation" flips, and "settings" (17.5) would overtake "interface" (16.1).
- Both paragraphs say "of observations" with no base, and the pooled tables (`tab:contingency`, `tab:verification`) are on 317.
- Knock-on: Discussion 1142 says 46.7% "did not know how to check" but Design implications (1178) says "about 45%". 45% is roughly the 354-base figure (44.6%); 46.7% is the 317 base. Same quantity, two bases.
- Fix: choose one base per claim and state it (n) in the sentence, or add an "All" row to `tab:contingency` so the expectations figures are traceable. Use one number in Discussion.

### A4. Pooled sample size: 352 vs 354 vs 317, and 176 vs 177 participants
- 319-321: "352 observations from the 176 participants who named a method in both scenarios". 956 (EFA): "354 participant-scenario observations". 952: "n=317 across the four methods".
- Data explains it: GEE filters "Other" (one person chose Other in each scenario, `pooled_gee.md`), so 352 from 176 participants; EFA and the expectation/verification percentages use all 354; the four-method tables use 317. The paper never reconciles these, and the user-facing sentence at 316-317 says paired n=177 "answered both" method items, and Table `tab:method-usage` sums to 177 in each scenario including "Other".
- Fix: one sentence in Methods listing the bases (354 all observations; 352 excluding "Other", used by the GEE; 317 for the four qualifying methods) and which analysis uses which. Decision: whether the EFA (354) and the descriptive percentages should stay on 354 while the GEEs are on 352.

### A5. Two-pipeline reliability claim points at a section that does not describe two pipelines
- 294-296: alpha "confirmed identically by both analysis pipelines described in §sample-knowledge". The User Study section (862-1071) describes no pipelines. Either describe them (there are two code paths: `RTBF-Analysis/src` and `RTBF-Analysis/scipy_analysis`) or drop the clause. Data check: alphas 0.870 to 0.923 (`reliability.md`), so ".87 to .92" is correct.

### A6. "Pre-registered" design
- 516 ("a pre-registered experiment design"), 691 (probe order "set in the pre-registered design"), and the TODO at 1104 ("a pre-registered interim cut").
- The paper itself says the recall design was changed mid-study (829-838 "replaces an earlier design"; forced-choice stage dropped; two-attempt rule added 2026-09-23). The workbook header still says "Expected outcome (pre-register…". I found no registry or timestamped registration in the repo.
- Your memory note says not to call expectations pre-registered or state when they were written; that rule applies here too. Decision: remove "pre-registered" (use "fixed experiment design", "the experiment design") unless there is an actual registration to cite.

### A7. Benefit-loss claim in Discussion rests on a non-significant result
- 1155-1157: "delete a specific saved memory" is "both the highest-effort and highest-benefit-loss method participants rated", presented as "this paper's own finding" and then given a mechanism.
- Results 995: benefit loss "did not differ significantly" (pooled Wald p_Holm = .15; within scenarios p > .15). Only effort differs (and only three of the six pairwise contrasts reported involve specific memory significantly; specific memory vs clear-all history was not significant, p_Holm = .24 in `pooled_gee_posthoc_effort.csv`).
- Fix: Discussion should say the effort difference is supported and the benefit-loss ordering is descriptive only, and the "highest effort" claim should be limited to "higher than single conversation and ask-to-forget".

### A8. Method-eligibility rule stated as universal, but tests include small methods
- 347-348: "Only methods chosen by at least 14 distinct participants enter inferential tests." 952 repeats it for the four-method rating tests.
- Table `tab:analysis-families` (385-403) lists McNemar tests across "7 methods" (method choice) and "8 methods" (ideal methods), and the Stuart-Maxwell omnibus over all categories. These include Delete account (5 observations), File a request (0) and Clear-all-memories/Privacy dashboard (15 each).
- Fix: scope the rule to "method-by-rating and method-by-expectation/verification tests" and say the between-scenario tests cover all listed methods.

### A9. Dunn post hoc result in the Effort subsection is incomplete (found 2026-09-30, scipy re-run)
- Paper (Effort subsection): "Within scenarios, only single-conversation versus specific-memory deletion in the less-sensitive scenario was significant ($p_{Holm}<.001$)."
- Both pipelines (`src` and `scipy_analysis`, identical) show, for the **more-sensitive** scenario (Kruskal-Wallis H = 16.98), two significant Dunn pairs: single conversation vs clear-all-history (p_Holm = .0098, r = .34) and single conversation vs specific memory (p_Holm = .0078, r = .43). The less-sensitive scenario has one (single vs specific, p_Holm = .0002).
- So "only ... in the less-sensitive scenario" is wrong; three pairwise results are significant within scenarios, not one.

---

## B. Numbers and wording that disagree with the data or with each other

| # | Where | Issue | Evidence |
|---|---|---|---|
| B1 | 1116 | "only 15-36% ... no longer used for training" | Table `tab:contingency` and `pooled_obs_expectation_pct.csv`: 16.4 to 35.9 for the four methods. Should be 16-36%. |
| B2 | 991 | Protection shift reported as "p<.001" although protection is in a Holm family of 3 scales (377-379) and the paper's rule (341-342) says Holm-adjusted values are reported as p_Holm | `scenario_shift.md`: protection p_holm = .0018. So "p_Holm = .002" is what the rule requires; "p < .001" is the raw value. Willingness (single unadjusted test) is fine. |
| B3 (resolved by data: Shapiro-Wilk rejects normality for all three scales, so Wilcoxon is used for every scale and the paired-t branch is never used) | 326-328 vs 378 | Methods says the Wilcoxon test "was used for these comparisons (chosen over a paired t-test per a per-scale Shapiro-Wilk)". Table says "Wilcoxon signed-rank, or paired t where the difference scores pass Shapiro-Wilk". | Results only ever report r (rank-biserial) and Wilcoxon. Say which scales used which test, or drop "or paired t". |
| B4 | 923 | "The smallest difference was for deleting a specific saved memory (31.1% to 41.8%...)" | That is the **largest** percentage-point change and the **smallest p** (.011). Reword to "the smallest p-value". |
| B5 | 956 | Protection "unrelated to ... benefit loss (rho = .13)" | With 354 observations rho = .13 is roughly p = .01 if treated as independent (my estimate; not in any output). Say "weakly related" or report p. |
| B6 | 956 | "the same pattern held within each scenario" after stating bounds (min loading .67, max cross-loading .15) | `user_study.md`: less-sensitive Benefit-loss item 3 loads .66; more-sensitive Benefit-loss item 3 cross-loads .18 on effort. Bounds hold only pooled. |
| B7 | 436-437 | "32 of 375 prompts altered: 20 organization, 12 location, and 3 person redactions" | Breakdown sums to 35 (`prompt_clean.md` agrees with both numbers: 32 prompts, 35 redactions). Write "35 redactions across 32 prompts". |
| B8 | 1029 | Post-deletion feedback 41.2 + 34.5 + 29.4 = 105.1% | The item is select-all (`user_study.md` Q7.1). Say "select all" so the total over 100% is not read as an error. 4.0% "have not attempted" and 2.3% "other" are omitted. |
| B9 | 498-499 vs 567-568 | "for use verbatim as the chat-typed erasure request" vs "typed verbatim ... with only its disclosed referent substituted in" | Keep one wording: verbatim except for the referent. |
| B10 | 499 | "The sample is a fixed item list, not regenerable under a different random seed." | `RTBF-Prompt/results/prompt_clean.md` logs "sampled 137 of 375 (floor=15/locus, seed=42)", i.e. the pipeline had a seed and gave 137. The final list (138, `nl_forget_prompts_138_final.csv`) differs by one. State how the 138th item was added, or the claim reads as inconsistent with the log. |
| B11 | 433-435 | Corpus "draws on all complete respondents who wrote a prompt" (209 participants; 218 complete) | `prompt_clean.md`: extraction ran on an export with 217 participant rows, not 218. Probably the earlier export. Confirm no participant is missing; otherwise state the export used. |
| B12 | 29 vs 27 | Title text "What Does 'Delete' Mean? ..." but `pdftitle` metadata is "Right to Be Forgotten in LLMs: An Empirical Audit of Data Deletion Methods Across Six Platforms" | PDF metadata should match the submitted title. |

---

## C. Cross-references, typos and text defects

- 140: "a partially overlapping set with the six audited here; see \S\ref{sec:intro}". The Introduction never lists Li et al.'s six platforms, so the pointer leads nowhere. Name the overlap here or drop the pointer.
- 78, 83: LaTeX quotes are malformed: `` `memories,'' `` and `` `forget'' `` (single opening tick, double closing). Use `` ``memories,'' ``.
- 1277: "was extracted form this too," is a typo and an unfinished sentence.
- 198-269 / 268: the pipeline figure has label `fig:testing-pipeline` but is never referenced in the text, so the diagram floats with no mention. Same for labels `sec:background`, `sec:methodology`, `sec:discussion` (unused; harmless).
- 921 vs 991-999: the order-confound caveat is given once (921, "every difference between scenarios reported in this section") but the Evaluation subsections (protection higher in more-sensitive; willingness in Discussion 1164) are presented with no caveat of their own, and 1164-1165 adds one only in passing. Consider a one-line caveat where the protection shift (991) is reported.
- 1174-1186 and 1111-1132 promise that "the technical audit (RQ2/RQ5) takes up directly" the expectation question; Results is still a stub, so these are forward references to nothing. Do not change until results exist, but re-check them then. (Related: your rule that Related Work never forward-references results is respected; Discussion forward-references are fine.)
- The anonymity block and several comments (59-66, 722-725, 826-828, 1075-1105, 1190-1237, 1245-1247, 1250-1259) are author TODOs; they must be removed or resolved before submission.

---

## D. Placeholders (not inconsistencies, listed so nothing is lost)

`\begin{abstract} TBWL`, Technical Audit Results (1106), Limitations (1238), Conclusion (1247). Two TODOs inside Methods are still open: (a) the spot check of automatically accepted FOUND replies and reviewer agreement (722-725), (b) whether incomplete OCR replies were later recovered (826-828). The Methods already state what Results will report ("Results report both attempts for every cell", 839-841; four measurements; counts of each commitment type), so those promises must be honoured when results are added.

---

## E. Checked and consistent (no action)

- Survey flow: 235 → 17 incomplete → 218 → 1 attention, 36 never deleted → 181 → 177 paired (`screen.md`); 37 of 218 in Ethics (1274) = 1 + 36; 16.5% = 36/218.
- Demographics table: age, gender, education counts sum to 177 and percentages match `sample_demographics.csv`; "73% under 45" and "62.1% bachelor's or higher" follow from the table; privacy knowledge 5.06; AI literacy 3.83; concern 3.80.
- Method-choice table: all counts and percentages; pooled n by method (164, 73, 41, 39 = 317); Stuart-Maxwell p = .393; all ideal-method percentages and the McNemar numbers (p = .011, p_Holm = .088).
- Willingness (3.98 → 4.37, +0.39, CI [+0.23, +0.55], r = .55), protection, effort and benefit-loss bootstrap CIs; all per-method means and SDs in `tab:method-scales`; every pooled Wald and post hoc value in the Effort, Protection and Benefit-loss subsections; Kruskal-Wallis H and p values; regression coefficients (AI literacy b = .28 / -.29; all benefit-loss p >= .10); EFA KMO, eigenvalues, variance explained (70.6%) and every loading in `tab:efa`.
- Expectation GEE Holm p >= .37, V <= .18; verification Holm p values (.001, .007, .007, .039, .046); Table `tab:contingency` and `tab:verification` rows.
- Corpus: 415 raw, 209 participants, 375 distinct prompts; AC1 table rows and pooled 318/350 = 90.9% / 0.905 (match the Third Pass).
- Audit design: 73 + 12 = 85 cells (MASTER 73 rows, FILE 12 rows); 138 × 6 = 828; 133 × 6 = 798 erased and 30 not run; 7 Gemini Keep cards, all NL-forget cells (7 of 133); 48-hour erasure and 31-day recall (`tracking.py`); stealth plugin used by exactly two platforms (Claude, Perplexity); the five commitment types match the workbook's values; Table `tab:consistency-rule` agrees with its text.
- All `\cite` keys exist in refs.bib and no bib entry is uncited; all `\ref` targets exist.

## F. Not verified

- The factual claims attributed to the cited papers (for example Bertram et al.'s 3.2 million URLs, Habib et al.'s 150 websites, Zhang et al.'s 18 interviewees, and Li et al.'s six platforms) were not re-checked here.
- Data side, for information: the NL FORGET sheet's Email column shows one address for all six platforms, including Gemini, while your memory notes say Gemini runs on a separate account; the paper's statement (one dedicated account per platform) is unaffected, but the sheet should match whichever is right before the accounts are described in Methods.
