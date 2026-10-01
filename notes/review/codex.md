# Developmental review of `paper.tex`

**Paper:** What Does ‘Delete’ Mean? User Expectations and Observable Data Persistence Across Six LLM Chatbots  
**Reviewed:** `RTBF-Analysis/paper/paper.tex`, September 30, 2026  
**Perspective:** Simulated senior usable security and privacy reviewer for IEEE S&P; not an actual Stanford affiliation or conference review.  
**Stage:** Work in progress. Missing audit results, abstract, and conclusion are treated as unfinished work, not negative findings about the project.

## Overall assessment

This is a worthwhile research question with a plausible S&P contribution. The strongest potential contribution is a carefully scoped account of how deletion interfaces, conversational assurances, observable persistence, and user expectations disagree. The survey provides useful evidence about expectations and perceived effort, and the participant-derived request corpus could make the audit substantially more realistic than a researcher-written prompt benchmark.

My current assessment is **promising, but requiring substantive methodological revision before submission**. I would not assign a final accept/reject score while the principal audit findings are unavailable. Even assuming those results are completed, however, several current inference rules would prevent me from trusting the central conclusions. These are not problems that filling in the TBWL sections will automatically solve. The most urgent work is to correct the retention and policy-verdict logic, resolve the remaining repeated-measures analysis problem, and establish what the survey–audit comparison can actually identify.

Confidence is high in the manuscript-level concerns below, but limited regarding implementation and numerical correctness: I read the manuscript and bibliography, but did not rerun the analyses, inspect all audit transcripts, or verify every citation. Source line numbers below refer to this version of `paper.tex`.

**Venue-year clarification:** The request names S&P 2026, while the source comments target 2027 and describe work conducted after the 2026 submission deadlines. S&P 2026's last paper deadline was November 13, 2025, and its symposium took place in May 2026. I use the requested venue as a research-quality benchmark; the actual submission year needs correction. [Official S&P 2026 CFP](https://sp2026.ieee-security.org/cfpapers.html).

## What is already strong

- **Relevant privacy problem.** A deletion action can affect chat history, persistent memory, and future personalization differently. Understanding that distinction matters to users' ability to control disclosures.
- **Potentially complementary methods.** Survey responses can establish what people expect; a behavioral audit can establish what is observable after specific actions. The natural-language request corpus offers a concrete connection between the two.
- **Several good inferential safeguards.** The draft distinguishes a generated acknowledgment from a policy statement, recognizes that non-recovery does not prove backend erasure, treats method choice as self-selected, avoids interpreting nonsignificance as equivalence, and does not infer a training misconception from an unselected checkbox.
- **Useful transparency about the evolving protocol.** Account contamination, platform changes, missing acknowledgment captures, and earlier outcome-dependent repetition are acknowledged. This transparency will help if the final paper also establishes which observations followed which protocol.
- **Potentially actionable survey findings.** The effort difference between specific-memory deletion and conversation deletion, uncertainty about verification, and preferences for deletion feedback are more useful than a generic claim that users misunderstand privacy.

## Major concerns requiring changes

### 1. The retention criterion contradicts the paper's otherwise careful measurement scope

**Location:** Technical Audit, especially lines 715–737 and 749–779.

The measurement-scope paragraph correctly says that a missing token does not establish erasure. Later, however, the manuscript says a missing token can count as evidence of deletion if retention was established, and accepts both a memory notice and a generated statement such as “I will remember” as establishing that the fact was kept. A chatbot's assurance is not evidence that the particular token was durably stored on the surface being tested. Even a generic “Memory updated” notice does not establish what was stored. Conversely, a generated denial does not establish that storage did not occur.

Even independently verified pre-erasure storage would not turn a failed recall probe into proof of deletion: retrieval failure, feature changes, or ordinary forgetting remain alternatives. This matters most for platforms where the audit lacks a directly inspectable memory surface.

**Required revision:** Separate (a) claimed retention, (b) interface notification, (c) token or fact visibly present on an identified surface, and (d) demonstrated retrieval. Preserve “not recovered under these probes” as the negative outcome. Do not promote an assurance into observed storage or non-recovery into confirmed erasure. Add a feasible calibration subset of injected-but-not-deleted controls and never-injected controls across relevant platform/injection conditions. These need not double every experimental cell. Their purpose is to characterize probe sensitivity and false positives, not to certify backend deletion.

If additional control runs are infeasible, a narrower descriptive study of observed recoverability is still possible; a claim about deletion effectiveness would remain unsupported.

### 2. The policy-consistency rule does not sufficiently identify the surface or time to which a promise applies

**Location:** Policy commitments, lines 527–550; temporal design, lines 626–634; Table “How policy consistency is derived,” lines 781–800.

The current rule labels a `DELETES` cell contradicted if the token is recovered or the interface is unchanged. Recovery from a surviving conversation is not necessarily a contradiction of a promise to delete a saved memory. The draft recognizes this for one natural-language case, but the problem applies more generally to any independently retained copy. Likewise, an unchanged screenshot immediately after an asynchronous action does not establish failure to meet a later completion deadline. An interface can also continue displaying a cached view.

The rule labels non-recovery plus an interface that is not unchanged as “consistent,” even when the interface is not observable. Readers may mistake that label for verified fulfillment.

**Required revision:** Represent each policy claim as an action, target surface, preconditions, completion interval, and relevant exceptions. Record exactly what was observed, where, and when. Use verdicts such as “observed contradiction of the scoped commitment,” “no contradiction observed,” and “not assessable.” Recovery whose source cannot be attributed should establish account-level recoverability, not automatically a surface-specific policy violation. Apply this principle throughout the matrix, not just as one exception.

Provide dated policy snapshots and a platform/action-specific justification for the 31-day endpoint. A common observation day can be useful, but cannot by itself establish that every distinct commitment has expired.

### 3. Unique tokens establish attribution, not experimental independence

**Location:** NL-forget extension and contamination controls, lines 552–624; recall protocol, lines 678–709.

Unique referents and tokens help determine which disclosure produced a response. They do not eliminate interactions among 133 prompts on one account: accumulated memories, capacity limits, history-based retrieval, earlier deletions, and evolving personalization can affect later trials. A request naming one referent is not guaranteed to affect only that referent. The existing discussion of an actual broad-erasure incident reinforces the importance of this distinction.

The statement that phrasing is the “only varying factor” is therefore too strong. Referents, tokens, execution times, and account state also vary. Without appropriate balancing or replication, this is a test of diverse requests under specified conditions, not an identified causal estimate of phrasing effects.

The cross-session safeguards are thoughtful, but “independent” remains too strong when the first visit failed to emit the complete token: a partial token, a paraphrase, or the probe conversation itself can still change account state. Within a visit, the second attempt can also echo the first response.

**Required revision:** Report distinct accounts, ordering, batching, resets, and replication explicitly. Use isolated accounts or fresh-state replications for a targeted subset of headline findings where feasible. Report first attempts separately from any-attempt recovery. Describe cross-session observations as follow-up measurements with no detected full-token reinsertion when that is all the evidence establishes. Do not treat the 798 extension cells as 798 independent platform trials or two prompts as independent replications of deletion.

### 4. The central user–system “gap” is not yet operationalized

**Location:** Introduction RQ5; Related Work positioning; audit-results TODO.

The TODO correctly recognizes that using the same six platform names does not make the studies matched. This is a central design issue, not simply a future discussion-writing task. A participant choosing “delete a conversation” for a generic chatbot cannot automatically be classified as mistaken using an audit cell from a specific platform, feature configuration, and date. Expectations about database backups or training are particularly difficult because this audit cannot verify them.

**Required revision:** Build a joint display with one row per expectation: exact survey wording, participant reference context, applicable platform/control/surface, relevant audit observation, and permissible inference. Distinguish an expectation conflicting with documented scope, an expectation contradicted by observed behavior, and an expectation the audit cannot assess. These are different findings.

If the survey did not capture platform-specific expectations, present a conceptual comparison with explicit assumptions; do not estimate the percentage of users whose platform failed them. Narrow “who bears that gap” unless a defensible subgroup comparison exists. Never infer inequity across demographic groups from this question alone.

### 5. One survey analysis still violates the repeated-measures structure

**Location:** Analysis-family table, lines 407–409; protection, benefit-loss, and effort results, lines 979–988.

The manuscript uses Mann–Whitney tests to compare ratings across scenarios within each chosen method. Many participants appear in both scenario-specific groups; others switch methods and appear only once in that particular comparison. These are partially overlapping groups, not independent samples. The clustered pooled GEE is a useful improvement elsewhere, but it does not repair these separate tests.

**Required revision:** Remove these tests if they are not essential. Otherwise define the estimand and use an analysis that retains participant dependence, such as an appropriately specified participant-clustered model with method-by-scenario terms. A paired analysis restricted to people choosing the same method in both scenarios answers a different, narrower question and should be labeled accordingly. Small groups may make descriptive estimates preferable to additional interaction testing.

Also resolve the following reporting issues:

- The claim that independence working correlation keeps GEE point estimates equal to observed group means is not generally true with scenario also included as a predictor. Separate raw cell means from adjusted estimates and state how reported contrasts were obtained.
- The pooled factor analysis has 354 rows but 177 independent participants. The reported within-scenario replication is reassuring; foreground it and avoid interpreting conventional pooled adequacy tests as if all rows were independent. Explain whether parallel analysis respects clustering, or use scenario-specific results as the primary measurement check.
- Define the reported Wilcoxon effect size `r`, treatment of ties/zero differences, and its denominator. Distinguish the signed-rank test's target from the bootstrap mean difference; reporting both is acceptable, but they are not the same estimand.
- Report the promised GEE sensitivity results and full regression estimates with uncertainty. The exploratory AI-literacy associations should not become selective headline findings on the basis of unadjusted p-values alone.

### 6. The vignette comparison does not isolate data sensitivity

**Location:** RQ4; survey scenarios; willingness/protection results; Discussion.

The scenarios change city to exact home address, weather to STI treatment, and the surrounding task and possible consequences. Randomized order helps with order effects; it does not separate these simultaneous manipulations. Higher willingness to delete in the health/address vignette is a defensible finding. A causal claim that sensitivity itself produced that change is not.

The instruction already says the participant wants to delete data “to protect your privacy.” That framing may prime deletion and protection ratings; willingness here is elicited within a deletion-oriented hypothetical task.

**Required revision:** Frame the existing result as a contrast between two bundled scenarios and make the confounding explicit. Report the order check if the randomization record is available. A manipulation check could help establish perceived sensitivity, but would not remove the other differences. A new factorial study is optional if claims are narrowed; it becomes necessary only if isolating sensitivity is central to the contribution.

### 7. Survey provenance and construct wording need reconciliation

**Location:** Survey methodology, prompt corpus, lines 1021–1023 approximately, and Appendix.

All analyzed respondents reportedly had deleted chatbot data before, yet 2.8% later say they never attempted deletion and 4.0% say they had not attempted it on the feedback item. Different question scopes might explain this; the manuscript does not currently show whether they do. These are not grounds to discard respondents automatically, but they matter to the claim that the sample consists entirely of experienced deleters.

The paper also calls verification a recollection of past behavior while administering it in each hypothetical scenario. Without the exact wording and branching, it is unclear whether responses describe past practice, intended checking, or scenario-specific recollection. Pooling these responses cannot resolve that ambiguity.

**Required revision:** Include the full instrument, response options, branching, scale sources/adaptations, and timing of items. Explain contradictory eligibility responses and, if warranted, give a transparent sensitivity analysis. Provide a flow diagram for both the 235-to-177 analysis sample and the 209-participant prompt corpus. Report missing-item handling and the scenario-specific analysis bases explicitly. Do not characterize self-reported privacy knowledge or AI literacy as validated competence without showing the measures.

### 8. The natural-language corpus needs a clearer analytic purpose

**Location:** Prompt corpus, lines 420–484; NL-forget extension, lines 552–568.

The seven coding dimensions and their agreement statistics occupy meaningful space, but their role in answering a research question is not yet clear. The selection labels were revised after sampling, and five broadly scoped prompts are excluded precisely because they request a consequential kind of deletion. Deduplication and stratified sampling also mean the tested prompt proportions are not population frequencies.

**Required revision:** State whether the corpus is for coverage, descriptive failure analysis, or estimating associations with phrasing. Report the original sampling strata, counts, inclusion probabilities or selection rule, label revision, and final codebook. Show how referent substitution preserves request scope with representative examples. Report broad-request exclusions as a boundary of the corpus audit, not as evidence about the reliability of all natural-language deletion requests. If coding supports comparisons, account for shared prompt authors and shared accounts where relevant; if not, move most reliability detail to the appendix.

The statement that kappa “understates true agreement” should be softened. Raw agreement is directly observed; chance-corrected coefficients embody different assumptions. Justify AC1 without asserting that it reveals a uniquely true reliability value. Per-dimension agreement is more interpretable than pooling heterogeneous dimensions into one coefficient.

## Contribution, interpretation, and presentation

The closest cited walkthrough already studies how platforms define and expose controls, including ambiguity in natural-language control. The proposed advance should therefore rest on longitudinal behavioral evidence and a defensible comparison with user expectations, not simply “six platforms” or “users have incomplete mental models.” A short comparison table can clarify the distinction. I checked the closest paper's public primary-source description, but did not conduct an exhaustive novelty search. [Li et al., Privacy Control in Conversational LLM Platforms](https://arxiv.org/abs/2602.10684).

The title's “observable data persistence” is appropriately scoped. Bring the Introduction into alignment: “actually handle deletion” and “removes the data” are broader than what the audit can establish. State the privacy property and affected actor explicitly: for example, continued account-level availability or future personalization after a scoped deletion request. This need not be an adversarial attack paper, but recoverability should be connected to a concrete privacy consequence rather than automatically called a leak to another party.

The Discussion sometimes outruns the evidence. The claim that verification uncertainty is a property of deletion controls generally needs more support than one selected sample. A memory mental-model explanation for higher effort is plausible, but unmeasured. The audit does not independently validate participants' recollections of checking behavior. Keep these as hypotheses or interpretations, and make the design implications traceable to actual findings.

“Participatory survey” also deserves explanation: if participants supplied responses and example requests but did not participate in design or interpretation, “survey with participant-authored deletion requests” is more precise.

## Ethics and reproducibility

The ethics section has useful concrete disclosures, including consent, compensation, and the scope of IRB review. It would be stronger with median completion time/effective hourly pay and clarification of whether research-analysis exclusions affected compensation. Explain how potential identifiers in free-text responses and linkage metadata were handled; reconcile “no identifying information collected” with the later redaction of prompt text.

Replace “no path to harm” with a bounded account of assessed risks and mitigations. Standard account access and free-tier availability alone do not establish permission for every automation technique. Describe the bot-detection circumvention factually, the study volume/rate controls, and relevant permission or terms considerations without assuming either ethical clearance or wrongdoing. If the completed audit finds consequential privacy failures, explain the disclosure approach and status.

The manuscript says every phase saves a transcript, but also says chat-based erasure replies were not saved and had to be recovered by OCR. Specify the actual evidence retained by phase, OCR validation, and missingness. An audit artifact should permit tracing each headline result to its injection, erasure action, policy snapshot, timing, probe transcript, and coding decision. Redact account credentials and participant identifiers before any release.

## Completion work, distinct from the methodological concerns

I do not penalize these placeholders at this development stage. Before submission, however, the paper needs:

- Audit results with planned, executed, pending, failed, excluded, and assessable denominators by platform and test arm. In-progress cells must not enter negative-result counts.
- A frozen analysis cutoff and protocol-version accounting, especially for re-injected cells and changes to repetition rules. Explain whether older observations are eligible for the final analysis.
- Platform, feature, account-tier, and observation-date context; no unqualified rankings across unequal sets of controls.
- Separate presentation of acknowledgment, interface state, recovery, and policy verdicts, including missing captures and inconclusive observations.
- A completed RQ5 comparison supported by the available survey context, followed by audit limitations, an abstract, and a conclusion that reflect actual findings.
- A compiled-PDF check for table readability, figure legibility, references, anonymity, and the correct submission-year requirements. I have not assessed rendered layout in this review.

## Recommended order of work

1. **Before committing further audit effort:** fix the retention/policy decision rules, define the RQ5 mapping, and determine whether a targeted control/replication subset is feasible.
2. **Using existing survey data:** replace or remove the overlapping-group Mann–Whitney tests, reconcile question wording and eligibility inconsistencies, and narrow the vignette claims.
3. **Before final audit analysis:** freeze the cutoff, protocol eligibility rules, coding procedure, and denominators; validate a sample of automatic and human-coded outcomes.
4. **After those decisions:** write the audit findings and integrated discussion, then shorten the methods narrative and finish the abstract and conclusion.

The acceptance case should be that this study establishes a specific, consequential disconnect between deletion promises, user expectations, and observable behavior under a credible protocol. The survey alone does not yet establish that case, and a large audit cell count cannot substitute for measurement validity. The project has a plausible route to it, provided the central claims stay within what the completed evidence can support.
