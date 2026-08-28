## Task 1 — Discriminant validity: protection vs effort vs benefit_loss

 Context

 tasks.md task 1 asks whether protection, effort, and benefit_loss are statistically
 distinguishable constructs, or whether some pair is so tightly coupled that treating them                                                                
 as separate scales isn't defensible. The tool for this is a discriminant-validity check:
 pairwise Spearman correlation (scales are non-normal per the existing Shapiro results
ready run in stats.py), with the standard rule of thumb that |ρ| ≥ 0.8 on a pair means
 the two scales can't really be claimed as separate. The threshold applies to |ρ| (not ρ)
 because protection and benefit_loss could plausibly correlate negatively.

 Two scopes were specified: (A) within each scenario, (B) pooled across both — 3 pairs ×
 3 scopes = up to 9 correlations. 
 
 

 Per project convention ("Strictly Scipy" — confirmed and saved to memory), this goes in
 scipy_analysis/ using only scipy/numpy, following the existing pattern where
 scipy_analysis/*.py modules reuse data-prep helpers from src/*.py but implement the
 actual statistical test themselves without statsmodels/pingouin/scikit-posthocs.

 Two design questions were resolved with the user during planning:
 - Scope A (within scenario): use bases["less"] (n=177) and bases["more"] (n=178)
 directly and independently — not the paired base — matching how src/stats.py's
 existing between_method() (steps 1-2) already treats each scenario's base as its own
 independent sample.
 - Scope B (pooled): use bases["paired"] (n=177), averaging each respondent's
 less-scena




 1. python -m scipy_analysis.correlations — confirm 9 rows print (6 [less]/[more],
 3 [pooled]); rho in [-1, 1]; n at/near 177 for [less]/[pooled] rows and near
8 for [more] rows; p_holm >= p_raw for every row; verdict is COUPLED only when
 |rho| >= 0.8. Confirm scipy_analysis/outputs/results/correlations.md is written.
 2. python -m scipy_analysis.global_correction — confirm header reads                                                                                       === Global correction across 110 primary/omnibus tests === (101 + 9); confirm                                                                              scipy_analysis/outputs/tables/global_correction_all_tests.csv grows to 111 lines                                                                        (110 rows + header); grep "correlations.discriminant_validity" on that CSV returns                                                                exactly 9 rows whose p_raw matches step 1's output exactly (same underlying
 spearmanr call, not re-derived); confirm the pre-existing 101 rows' p_raw values are
 unchanged (their p_holm_global/p_fdr_global may shift slightly since the family size
 grew from 101 to 110).




## Task 2a

 Task 2 — Pooling a method's respondents across both scenarios

 Context

 tasks.md (lines 15-23) sets up a data-prep step needed before the next task can run
 Kruskal-Wallis on a "pooled" (both-scenarios-combined) sample per method. Naively
 concatenating bases["less"] and bases["more"] would double-count any respondent who
 used the same method in both scenarios — breaking Kruskal-Wallis's independence-of-
 observations assumption. The task spec (already resolved by the user, "refined version of
 solution") gives the exact algorithm:

 - If a respondent used the same method in both scenarios (a "stayer"): average their
 less-scenario and more-scenario scale scores into one observation in that method's
 group.
 - If a respondent switched methods between scenarios: their less-scenario rating and
 more-scenario rating are genuinely about two different methods, so each becomes its own
 independent observation in its own method's group — nothing gets double-counted within
 a group.
 - Residual caveat (documented, not solved): a switcher still contributes to two different
 groups. Milder than double-counting within one group; unavoidable for pooled within-
 subject data. Worth a caveat sentence in the output, not a blocker.

 Exploration confirmed: no pooling code exists anywhere yet (src/ or scipy_analysis/).
 tasks.md:21's "the table above already reflects" reference does not resolve to anything
 in the repo — checked notebooks/*.md, rough.md, slides.md — it's a dangling
 reference to a table shown in an earlier chat, not a file. Nothing to recover from there;
 this plan builds the table fresh. The "delete a specific saved memory" 19/22 → 30 pooled
 example in tasks.md:33 traces back to real per-scenario n's in
 outputs/tables/per_method_less.csv/per_method_more.csv (from src/methods.py), but no
 existing file sums/dedupes them — that 30 is illustrative, not yet verified; this task's
tput will produce the real number.

 Per project convention ("Strictly Scipy"), this goes in scipy_analysis/, reusing
 src.stats.SCALES, src.stats.scale_score, src.stats.SCEN, src.stats.N_FLOOR, and
 src.screen.get_bases — same reuse precedent as scipy_analysis/correlations.py
 (task 1). scipy_analysis/mcnemar.py's METHODS/SHORT list is the canonical 7-method
 naming to reuse for consistency.

 Key structural finding from exploration: between_method() (scipy_analysis/stats.py)
 cannot consume this pooled output unmodified — it computes scale_score() itself from raw
 per-item Likert columns, but the pooled dataset will already contain final averaged/
 dedup'd numeric scores (no raw item columns to re-score). So this task produces a clean
 long-format DataFrame; the next task (Kruskal-Wallis on pooled groups) will reuse only
 the grouping pattern (pooled.loc[pooled["method"]==m, scale].dropna().values), not
 between_method() itself. That KW step is explicitly out of scope here — this task is
 data-prep + a caveat-documenting summary only.

 Filtering choice: match how between_method() and method_switching() already filter
 "Other (Please specify)" — but per-scenario-independently rather than requiring both
 scenario answers to be non-"Other". A respondent who answered "Other" in less but a real
 method in more should still contribute their more-scenario observation to that method's
 group (this mirrors how between_method() filters "Other" separately within each of
 bases["less"]/bases["more"], not jointly).

 Implementation

 New file: scipy_analysis/pooling.py

 """
 Task 2 -- pool each method's respondents across both scenarios into one
 long-format dataset, for the next task's pooled (both-scenarios) Kruskal-
 Wallis. Naive concatenation of less+more would double-count any respondent
 who used the SAME method in both scenarios (breaks KW's independent-
 observations assumption). Per-respondent rule (paired base, n=177):

   - same method in both scenarios (a "stayer"): average their less- and
     more-scenario scale scores into ONE observation in that method's group.
   - different method per scenario (a "switcher"): less-scenario rating and
     more-scenario rating are genuinely about two different methods, so each
     becomes its own independent observation in its own method's group --
     nothing double-counted within a group.
   - "Other (Please specify)" is filtered per scenario independently (same
     convention as stats.between_method / stats.method_switching), so a
     respondent who answered "Other" in one scenario but a real method in
     the other still contributes that scenario's observation.

 Residual caveat (documented, not solved): a switcher still contributes to
 TWO different groups. Milder than double-counting within one group, and an
 unavoidable feature of pooling within-subject data -- reported alongside
 the pooled n's below, not silently absorbed.
 

 Notes:
 - pooled_method_scores(bases) is the reusable artifact — the next task (pooled
 Kruskal-Wallis) and the task-3 "overall" grouped bar chart both consume this directly
 (pooled.loc[pooled["method"]==m, scale].dropna().values), no recomputation needed.
 Saved to scipy_analysis/outputs/tables/pooled_method_scores.csv for reuse without
 re-running Python, matching the existing convention (expectation.py etc. save to
 outputs/tables/).
 - pooled_n_summary() is the caveat-documenting deliverable task 2 itself asks for —
 makes the stayed/switched/solo composition of each method's pooled n auditable, and
 will directly confirm or correct the illustrative "19/22 → 30 pooled" example from
 tasks.md:33.
 - No N_FLOOR filtering applied here — kept methods are decided by the next task
 (Kruskal-Wallis), matching how between_method() applies the floor after building full
 counts, not during data prep.
 - SHORT/METHODS imported from scipy_analysis/mcnemar.py for label consistency
 with the rest of the study's reporting.

 Verification

 1. python -m scipy_analysis.pooling — confirm summary table prints for all 7 methods;
 n_pooled = n_stayed + n_switched + n_solo for every row (internal consistency check);
 n_stayed + n_switched (people who answered both scenarios, non-Other) should be ≤
 min(n_less, n_more) roughly, and n_pooled should sit below n_less + n_more for any
 method with stayers (since stayers count once, not twice) — spot-check
 "Delete a specific saved memory or fact." against the tasks.md illustrative 19/22→30.
 2. Confirm scipy_analysis/outputs/tables/pooled_method_scores.csv and
 scipy_analysis/outputs/results/pooling.md are written.
 3. Sanity check total row count: len(pooled) should be ≤ 2 * 177 (max if everyone
 switched and both scenarios were non-Other) and ≥ 177 (min if everyone stayed) —
 confirm it falls in that range.


## Task 2 — statistically identify the best method (protection/effort/benefit_loss)

 Context

 tasks.md (lines 27-33, currently numbered "2.") asks for a statistical (not
 descriptive) answer to which deletion method is most protective, least effort, and
 lowest benefit_loss — for (a) the pooled sample (both scenarios combined, using task 2's
 dedup logic) and (b) each scenario separately.

 The method is specified exactly: per scale, Kruskal-Wallis across methods with n≥14,
 and if significant, Dunn's post-hoc + Holm for all pairs. The crowning rule is the part
 that needs real implementation — nothing like it exists in the codebase yet (confirmed by
 grep):

 ▎ A method only gets crowned "most protective"/"least effort"/"lowest benefit loss" if it
 ▎ (1) has the best point estimate and (2) significantly beats every other method it's
 ▎ compared against in the post-hoc — not just some. If it beats some but isn't
 ▎ distinguishable from others, that's the honest finding ("X is significantly lower-effort
 ▎ than Y and Z, but not distinguishable from W") rather than a forced single-winner claim.
 ▎ If the omnibus itself is ns, the answer is "no method is statistically distinguishable" —
 ▎ not "they're all equal."

 Exploration confirmed three conventions to match:
 - Point estimate = mean, not median — src/methods.py's ranking narrative sorts by
 f"{name}_mean" (line 98), the established convention for "which method looks best."
 - scipy_analysis/dunn.py's dunn_test(data, val_col, group_col) takes a long-format
 df and returns a square DataFrame indexed/columned by method name, already
 Holm-corrected internally across whatever pairs are in that one call — no second Holm
 pass needed, but each scale needs its own separate call (don't batch scales together).
 - Effect size: rank_biserial_indep(a, b) from src.stats (Mann-Whitney U based),
 already imported this way by scipy_analysis/stats.py — reuse directly, don't
implement.
e-confirmation exercise, exactly as
 flagged. Scope (a) pooled is the only genuinely new computation, using the higher pooled
 n's from task 2 (e.g. Delete specific memory: 19/22 → 30) that could plausibly tip
 protection/benefit_loss from ns into detectable.

 Implementation

 New file: scipy_analysis/crowning.py

 """
 Statistically identify the most protective / least-effort / lowest-
 benefit-loss deletion method. Kruskal-Wallis (n>=14 floor) per scale -> if
 significant, Dunn's post-hoc + Holm (dunn_test, already Holm-corrected
 internally) -> crowning synthesis per tasks.md's rule: a method is CROWNED
 only if it (1) has the best point estimate (mean, matching src.methods.py's
 convention) AND (2) significantly beats EVERY other kept method in the
 post-hoc. Partial wins are reported honestly, never forced into a single
 winner. ns omnibus -> "no method is statistically distinguishable."

 Two scopes:
   (a) pooled -- scipy_analysis.pooling.pooled_method_scores(bases) (task 2's
       dedup logic, n=239). NEW omnibus tests -- these 3 feed the global
       p-value registry.
   (b) per-scenario -- less, more. DUPLICATES stats.between_method's KW+Dunn
       computation (deterministic, must match stats.md exactly) because
       between_method doesn't expose the full pairwise matrix or point
       estimates externally. NOT re-registered globally -- already present
       under "stats.between_method".
 """


 # import block:
 from .crowning import pooled_crowning

 # inside collect_all_pvals, after the correlations line:
 all_pvals += [("crowning.pooled", lbl, p) for lbl, p in pooled_crowning(bases, [])]

 Adds 3 new tests (protection/effort/benefit_loss, pooled scope only) — battery goes from
 110 (after task 1) to 113. Per-scenario crowning is deliberately excluded from this list
 (see Context — avoids double-counting stats.between_method's existing 6 entries for
 these same scenario/scale combinations).

 Verification

 1. python -m scipy_analysis.crowning — confirm 4 kept methods for every (scale, scope)
 combination (Delete single conv, Clear history, Delete specific memory, Type message —
 the same 4 that clear n≥14 in every scope per task 2's summary table).
 2. Cross-check scope (b) against stats.md exactly: less-scenario effort H=18.42,
 p=0.0004; more-scenario effort H=16.98, p=0.0007; protection/benefit_loss omnibus ns in
 both scenarios (stats.md steps 1-2). Any mismatch means the recomputation has a bug.
 3. Confirm scope (b) effort verdicts are both PARTIAL (not CROWNED) — less-scenario:
 "Delete this single conversation" beats exactly 1 of 3 others; more-scenario: beats 2 of
 3 — matching the pre-verified expectation above.
 4. python -m scipy_analysis.global_correction — confirm battery header reads 113 tests
 (110 + 3); confirm the 3 new crowning.pooled rows appear in
 global_correction_all_tests.csv with p_raw matching step 1's pooled output exactly;
 confirm none of the existing stats.between_method rows changed (no double-counting
 introduced).

 Files touched

scipy_analysis/crowning.py — new
 - scipy_analysis/global_correction.py — one import line + one all_pvals += line




 ## Task 3 — Grouped bar chart, pooled/overall scope (fig9)

 Context

 tasks.md (lines 36-38) asks for a grouped bar chart documenting protection/effort/
 benefit_loss by method, matching what fig7_method_cost_benefit.png already does for
 each scenario separately — but for the pooled/overall scope (task 2's dedup logic),
 giving a consistent "overall + per-scenario" 3-chart set.

 Read src/methods.py in full (111 lines) to get the exact source of truth: per_method()
 computes {name}_mean/_median/_sd + n + an n<14 flag per method from raw per-scenario
 data, and plot_cost_benefit() renders it as 1×2 subplots (less/more), grouped bars
 (w=0.26, offsets (i-1)*w), fixed y-axis 0-5, colors
 {"protection": "#4C9F70", "effort": "#B4436C", "benefit_loss": "#3b6fa0"} (confirmed
 reused across src/methods.py, src/scenario_shift.py, src/method_selection.py,
 src/knowledge.py — the established palette), x-tick labels from a module-level
 SHORT_METHOD dict (multi-line short names, e.g. "Delete this single conversation.": "Delete single\nconversation"), single shared legend below the left axis, dpi=200, bbox_inches="tight". This task's new chart matches that style exactly, sourced from
 scipy_analysis/pooling.py's pooled_method_scores(bases) (already built — long-format,
 columns method, protection, effort, benefit_loss, source, n=239, 4 methods clear n≥14)
 instead of re-scoring raw items per scenario.


 Output split: the PNG goes to the shared outputs/figures/fig9_pooled_cost_benefit.png
 (joining fig1-fig8, since the task explicitly wants this to read as part of the same
 3-chart visual set — that's a property of where the image file sits, not which package
 computed it). The CSV summary table and text report stay inside the scipy_analysis/
 package tree (scipy_analysis/outputs/tables/, scipy_analysis/outputs/results/),
 matching every other scipy_analysis module's own convention.

 No new statistics here — pure visualization of already-computed pooled means, same as
 fig7/fig8 are documented as visualizing existing results, not computing new ones.


 Verification

 1. python -m scipy_analysis.fig9_pooled_cost_benefit — confirm the printed pooled table
 shows the same 4 methods as crowning.py/pooling.py (Delete single conv, Clear
 history, Delete specific memory, Type message) with n matching task 2's
 n_pooled column exactly (105, 50, 30, 29).
 2. Cross-check means: effort_mean for "Delete this single conversation" should read
 1.68 (matches crowning.md's [pooled | effort] Delete this single c=1.679 rounded).
 Spot-check one more (e.g. benefit_loss for "Delete a specific saved memory" = 3.43,
 matching crowning.md's Delete a specific sa=3.433).
 3. Confirm outputs/figures/fig9_pooled_cost_benefit.png is created (joining fig1-8 in
 the shared figures directory) and visually resembles fig7's panels (same colors,
 same y-range 0-5, same short method labels) — open/view the PNG to confirm.
 4. Confirm scipy_analysis/outputs/tables/pooled_method_table.csv and
ipy_analysis/outputs/results/fig9_pooled_cost_benefit.md are written.

 Files touched

 - scipy_analysis/fig9_pooled_cost_benefit.py — new
 - outputs/figures/fig9_pooled_cost_benefit.png — new (generated, shared figures dir)
 - scipy_analysis/outputs/tables/pooled_method_table.csv — new (generated)



## Task 4 — Method choice shift: explicit ranking + net-shift chart (fig10)

 Context

 tasks.md (lines 40-51) covers Q4.2→Q5.2 method choice shift. Two pieces already exist
 and need no new computation:
 - Transition matrix + Stuart-Maxwell omnibus (stats.md step 6, ns, p=.393).
 - Per-method McNemar + Holm (scipy_analysis/mcnemar.py's per_method_shift(),
 already computed and already registered in the global p-value battery under
 "mcnemar.per_method_shift" — confirmed present, 7 rows, in
 global_correction_all_tests.csv).

 Read scipy_analysis/mcnemar.py and its current output (mcnemar.md) in full to confirm
 exact state: the table exists but is printed in the fixed METHODS list order, not sorted
 by shift magnitude. The task's own text identifies this as "the only genuinely new piece"
 — a resort by net shift, plus an optional net-shift bar chart colored by sig/ns. Going                                                                                                                                                                                                                        with that default (not the alternative it floats — combining with cost/benefit ratings —
 which is a bigger, separate design decision left for later if wanted).

 Confirmed via the numbers: sorting by net = added − dropped (descending) puts "Clear all
 conversation history" (net=+7) at the top and "Type a message asking the AI Chatbot to
rget it" (net=−11) at the bottom — matching the existing narrative that this method is
 "the only one with even a suggestive (non-significant) decline." None of the 7 methods
 survive Holm correction (mcnemar.md: all sig column blank) — the chart will
 correctly show every bar in the same "not significant" color; that's the honest picture,
 not a bug to fix.

 No new statistics — this is presentational only, same category as fig9 (task 3). No
 global_correction.py changes needed since no new p-values are produced (re-sorting
 existing output, not re-testing).



 Notes:
 - ranked_shift() calls per_method_shift() directly (no recomputation) and only adds a
 net column + resort — matches the task's own "trivial change" framing exactly.
 - Color convention reuses the existing sig/ns palette (#B4436C / #999999) already
 established in src/scenario_shift.py (fig8), for visual consistency across the figure
 set rather than inventing a new scheme.
 - File placed in scipy_analysis/ (alongside mcnemar.py, which it imports from),
 matching the location precedent set for fig9 in task 3 — figures that visualize an
 existing scipy_analysis test module's output live next to that module.
 - PNG saved to the shared outputs/figures/ directory (joining fig1-fig9), same
 reasoning as fig9's output split: the figure set is a shared visual asset regardless of
 which package computed the underlying numbers.

 Verification

 1. python -m scipy_analysis.fig10_method_shift_ranking — confirm 7 rows print, sorted
 with "Clear all conversation history" (net=+7) first and "Type a message asking the AI
 Chatbot to forget it" (net=-11) last.
 2. Confirm every row's sig column is blank (matches mcnemar.md — none survive Holm),
 and confirm the chart renders all 7 bars in NS_COLOR (grey), none in SIG_COLOR.
 3. Confirm outputs/figures/fig10_method_shift_ranking.png is created; view it to confirm
 bars are sorted top-to-bottom by net shift, diverging left/right from zero.
 4. Confirm scipy_analysis/outputs/results/fig10_method_shift_ranking.md is written.
 5. No global_correction.py changes — confirm battery stays at 113 tests (unchanged from
 task 3) since this task produces no new p-values.

 Files touched

 - scipy_analysis/fig10_method_shift_ranking.py — new
 - outputs/figures/fig10_method_shift_ranking.png — new (generated, shared figures dir)