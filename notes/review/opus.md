# IEEE S&P 2026 Review

**Paper:** What Does 'Delete' Mean? User Expectations and Observable Data Persistence Across Six LLM Chatbots

**Reviewer:** (simulated faculty review, usable security and privacy)

**Disclaimer:** This review is based on an incomplete draft. The Abstract, Technical Audit Results (Section 5), most of the Discussion, a substantial portion of the Limitations, and the Conclusion are all marked TBWL. My assessment is necessarily provisional; a final verdict would depend heavily on those missing sections, particularly the audit results, which carry the paper's most novel empirical contribution.

---

## Summary

The paper proposes a two-pronged study of data deletion in commercial LLM chatbots: (1) a participatory survey (n=177 paired) measuring user expectations, method choices, perceived protection/effort/benefit-loss, and verification behavior across a less-sensitive and more-sensitive vignette, and (2) a technical audit of six platforms' deletion controls (85 cells + 798 NL-forget-prompt cells), testing whether invoking a control actually removes the data it claims to. Five research questions span system behavior (RQ1), policy gaps (RQ2), user expectations and verification (RQ3), data sensitivity effects (RQ4), and the divergence between user expectation and platform behavior (RQ5).

---

## Strengths

**S1. Important, timely question.** Hundreds of millions of people use LLM chatbots and share sensitive data with them. Whether the deletion controls these platforms expose actually work is a first-order usable-privacy question that, remarkably, has not been tested empirically on live accounts. The paper fills a genuine gap between Li et al.'s interface walkthrough (CHI 2026) and the user-side mental-model literature. This is the right question at the right time for S&P.

**S2. Methodological rigor of the technical audit design.** The audit methodology is unusually well thought through for a black-box behavioral study. The canary-token attribution design (unique referent + unique token per cell, with quantifiable guess probability), the contamination-control regime (dedicated accounts for broad-action cells, scheduling narrowest-first), the three-probe recall design (R2/R3/R1 in fixed order to limit inter-probe contamination), and the explicit separation of four measurements (acknowledgment, interface change, recoverability, policy consistency) with a deterministic derivation rule (Table 2) are all strong design choices. The paper is also admirably transparent about what it does not measure (backend storage, training-data removal), and the "Measurement scope" paragraph is a model of intellectual honesty about observational limits.

**S3. The NL-forget-prompt extension is a genuine contribution.** Using 133 participant-written erasure prompts verbatim (after PII scrubbing) as the erasure requests, rather than researcher-authored phrasings, is a meaningful methodological advance. It directly tests whether the way real users phrase deletion requests affects whether the platform complies, which is a question prior work has not asked. The coding and reliability (AC1 = 0.954 pooled, seven dimensions, two independent coders on all 138) are solid.

**S4. Clean measurement model.** The EFA is textbook: adequate sampling (KMO = .81), parallel analysis retaining exactly the three intended factors, every item loading >= .67 on its intended factor with cross-loadings <= .15, and high reliability (alpha = .87-.92). The three scales are well separated (rho <= .27). This is a cleaner factor structure than most survey papers at top venues report.

**S5. Careful statistical practice.** The paper uses Holm correction with explicit families, reports Holm-adjusted and unadjusted p-values without mixing them, treats all survey analyses as exploratory, uses bootstrapped CIs for the paired mean differences (because the Wilcoxon test has no closed-form interval for the mean), chooses GEEs with independence working correlation for a defensible reason (method varies within participant), and explicitly states that method comparisons are associations with the chosen method, not causal effects. This level of care is above the S&P baseline.

**S6. Transparent account of design limitations.** The paper is forthcoming about the lack of positive/negative controls, the non-independence of cross-session recall, the outcome-dependent repetition asymmetry (now fixed), and the acknowledged-but-not-verified retention status. Many papers hide these; this one structures them into the design description.

---

## Weaknesses

**W1. (Major) The audit results are missing.** The entire empirical contribution of RQ1, RQ2, and the system side of RQ5 is TBWL. This is the half of the paper that would make it an S&P paper rather than a SOUPS paper. Without it, I cannot evaluate whether the audit design, however well specified, actually produced interesting findings: whether deletion controls fail, how often, on which platforms, in which ways. The Discussion currently makes forward references to audit results that do not exist ("the technical audit (RQ2/RQ5) takes up directly"), which means the Discussion itself is incomplete and its claims are ungrounded. **The paper is not reviewable in its current state for the system-side contribution.**

**W2. (Major) RQ5 is entirely unaddressed.** RQ5 (divergence between user expectation and audited platform behavior) is the paper's integrative research question, the one that justifies combining a survey and an audit in a single paper rather than publishing them separately. With no audit results, there is nothing to compare user expectations against. Even the Discussion section, which is partially drafted, does not attempt any RQ5 analysis: it discusses what users expect and what prior work found, but never maps a user expectation (e.g., "59% expect permanent deletion") to a specific platform's observed behavior (e.g., "Platform X's conversation deletion left the token recoverable in Y% of cells"). Until this mapping exists, the two halves of the paper are two separate studies stapled together, not an integrated contribution.

**W3. (Major) The survey findings, standing alone, are modest.** The survey results that are reported, taken on their own, are incremental over existing usable-privacy work on deletion mental models (Ramokapane et al., Habib et al., Kang et al., Zhang et al.). The main findings are: (a) single-conversation deletion is most popular, (b) willingness to delete is higher for sensitive data (not surprising), (c) effort differs across methods but protection and benefit-loss do not, (d) ~45% don't know how to verify deletion, and (e) expectations don't significantly differ across methods (but the study is underpowered to detect this). These are useful descriptive contributions, but for S&P, I would expect either a larger effect, a more surprising finding, or the integrative RQ5 analysis that ties them to observed platform behavior. The paper's own Discussion acknowledges that the verification finding mirrors what Ramokapane et al. and Habib et al. already showed, and that the effort finding is consistent with Zhang et al.'s interview results. The paper needs the audit results to elevate the survey findings from "confirms prior work in a new context" to "reveals a measurable, consequential gap between what users think and what platforms do."

**W4. (Moderate) No power analysis, and several analyses are underpowered.** The paper candidly states "we set no formal sample-size target or power calculation and aimed for roughly 200 respondents," and the smallest method groups have 14 participants. For the expectation-by-method analysis, the paper itself notes "observed rates differed by up to 29 percentage points for some options" but no association was detected, and calls this "a failure to detect an association at these group sizes, not evidence that methods elicit the same expectations." This is honest, but it also means a meaningful portion of the survey analysis is inconclusive. At S&P, I would want either a larger sample or a more focused design that concentrates power on the comparisons that matter most. The paper's own framing as exploratory mitigates this somewhat, but "exploratory" is not a license for underpowered analyses; it is a license for not pre-registering, which is a different thing.

**W5. (Moderate) The two scenarios both concern location data.** The Limitations section acknowledges this, but it is a real constraint on the sensitivity manipulation. Both scenarios disclose location information; the more-sensitive one adds a health context (STI treatment) and a home address. This means the sensitivity difference is confounded with (a) health vs. weather context, (b) home address vs. city name, and (c) STI stigma. A reviewer could reasonably ask: is the effect driven by data sensitivity per se, or by health stigma specifically? The paper cannot answer this, and the claim is scoped to "these two scenarios," but the RQ framing ("Does data sensitivity change...") is broader than the evidence supports.

**W6. (Moderate) Self-selection in method choice.** The paper correctly notes that method choice was self-selected, so differences between methods are associations, not effects. But the paper does not discuss the selection mechanism. People who choose "ask the chatbot to forget" may be systematically different from people who choose "delete a single conversation" in ways that explain the effort and verification differences (e.g., comfort with natural language, familiarity with settings interfaces). Without controlling for these, the method comparisons are descriptive at best. The GEE includes method and scenario as predictors but not participant characteristics as covariates (the regression is separate and uses only participant characteristics, not method). A model that includes both would be more informative.

**W7. (Minor-Moderate) The 138-prompt sampling is not fully reproducible.** The paper states: "We selected 138 of the 375 prompts for the technical audit by stratified sampling on an automated deletion-location label, with a floor so that small categories were retained. The label definition was revised after the draw." This means the stratification variable changed after the sample was drawn, so re-running the stated procedure on the current labels would not reproduce the same 138 prompts. This is acknowledged, but it weakens the claim that the sample is principled. The paper should state what the pre-revision labels were, or simply describe the achieved allocation (how many prompts per final category) and present the list as fixed.

**W8. (Minor-Moderate) Ethics of circumventing bot detection.** The paper uses playwright-stealth to bypass Cloudflare bot detection on two platforms. The ethics section argues this "defeats a bot-detection heuristic aimed at traffic patterns, not an access-control mechanism." This is a distinction without a clear difference: bot detection is a security control, and circumventing it, even on your own account, violates most platforms' terms of service. The paper should engage more directly with this: did the authors consider notifying the platforms? Does the IRB exemption cover the audit methodology, or only the survey? (The paper says "the IRB review covered the survey only," which means the audit, including the bot-detection circumvention, was not reviewed.) For S&P specifically, this is a venue where ethical research conduct is taken seriously, and a more thorough discussion is warranted.

**W9. (Minor) Discussion is partially drafted but already over-hedged.** The existing Discussion paragraphs are cautious to the point of saying very little. Every claim is followed by two or three caveats. For example, the training-data paragraph concludes with "we therefore report the selection pattern without inferring a misconception," which is good practice but leaves the reader with no takeaway. The design-implications paragraph says "if the patterns hold" and "whether either change alters what users understand or do would need to be tested directly," which, while accurate, makes the section feel like a literature review of the paper's own findings rather than an interpretation of them. The Discussion should make bolder, more specific claims where the data support them, and save the hedging for the Limitations.

**W10. (Minor) Missing figures and tables for the audit.** The pipeline figure (Figure 1) is schematic and does not convey the scale or complexity of the 85+798-cell design. A platform-by-method grid showing cell counts, or a diagram of the injection/erasure/recall timeline, would help readers grasp the audit's structure. The audit results section will presumably have its own tables, but the methodology section could benefit from a design-matrix table.

**W11. (Minor) Presentation.** The Methodology section is very long (~4 pages of dense text) and reads more like a technical report than a conference paper. Key design choices are buried in paragraph-length explanations. The contamination-control description alone is nearly a page. This level of detail is admirable for reproducibility but will lose readers at S&P, where reviewers evaluate 6+ papers per round. Consider moving some of the finer-grained details (e.g., the full scheduling safeguard story, the OCR pipeline, the retention-at-injection taxonomy) to an appendix and keeping the main text to the design decisions that affect interpretation.

---

## Questions for the Authors

1. **What are the audit results?** Even a summary (e.g., "X% of cells with a DELETES commitment still had the token recoverable at 31 days") would let me evaluate whether the paper's core contribution delivers.

2. **How will RQ5 be operationalized?** Which specific survey expectations will be mapped to which specific audit findings, and at what level of granularity (per-platform, per-method, per-mechanism)?

3. **Why not include the 36 never-deleted respondents in a separate analysis?** They are potentially the most interesting group (people who have never found or used a deletion control). Even a descriptive comparison of their demographics and chatbot usage against the 181 eligible respondents would add value.

4. **What is the distribution of commitment types across the 85 cells?** How many are DELETES, DOES NOT DELETE, NO COMMITMENT, UNRELATED, and NOT TESTABLE? This matters for knowing how many cells can even produce a policy-consistency verdict.

5. **For the NL-forget extension, what distribution of outcomes do you expect?** If most platforms simply comply with any natural-language deletion request (or refuse all of them), the 798 cells may produce a very skewed distribution that limits what can be learned from the prompt-phrasing variation.

---

## Minor Issues

- Line 1: The comment says "IEEE S&P 2027 submission format" but the review is for 2026. Clarify the target venue year.
- The Abstract is TBWL. Even a placeholder structured abstract would help reviewers.
- Table 1 (AC1): "Pooled (966 ratings)" = 138 prompts x 7 dimensions = 966. This is fine but should be stated explicitly so a reader does not have to compute it.
- The paper uses "participant-scenario observations" and "observations" interchangeably. Pick one and define it once.
- Table 4 (contingency): The column headers are truncated. "Not ref. (current)" and "Not ref. (future)" should be spelled out or given full labels in the caption.
- The "Platform changes" paragraph about Copilot and Gemini should be in Limitations or Results, not Methodology. It describes events that happened during the study, not design choices.
- The attention-check exclusion (1 of 218) is mentioned in both the survey methodology and the prompt-corpus section. The prompt-corpus section should simply cross-reference the survey section rather than re-describing it.
- The paper cites Roediger & Karpicke (2006) and Graf & Schacter (1985) for the recall-probe ordering rationale. These are human memory citations used as analogies for chatbot behavior, which the paper acknowledges ("not as evidence about these platforms"). This is fine, but a reviewer might question whether the analogy has any empirical basis for LLM chat history. Consider softening or dropping the analogy if it does not add explanatory value.

---

## Overall Assessment

**Provisional: Weak Accept (conditional on the audit results)**

The paper asks an excellent question, has a well-designed audit methodology, and reports a clean survey with careful statistical practice. The Related Work positioning is precise and the paper is intellectually honest about its limits. However, in its current state, the paper is approximately half-written: the entire system-side empirical contribution (RQ1, RQ2, RQ5) is missing, and without it, the survey findings alone are a solid SOUPS contribution but do not clear the bar for S&P. The verdict depends almost entirely on what the audit finds.

If the audit results show substantial, systematic gaps between what platforms claim and what they do, and the RQ5 analysis maps those gaps to the user expectations measured in the survey, this could be a strong S&P paper. If the audit results are mostly "platforms do what they say," the paper's contribution shrinks to "we checked and it was fine," which is less compelling regardless of how well the checking was done.

**Recommendation:** Complete the audit, write the results and RQ5 analysis, and resubmit. The foundation is strong enough that the final paper could range anywhere from a clear reject (if the audit is inconclusive) to a strong accept (if it reveals meaningful, actionable gaps). I cannot assign a final score until the empirical core of the paper exists.

---

*Review written 2026-09-30. Reviewed as an incomplete draft per the authors' note.*
