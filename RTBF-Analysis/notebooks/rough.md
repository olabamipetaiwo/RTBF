# Results (rough draft)

All figures below are in `outputs/figures/`. All statistics are pulled directly from
`outputs/results/*.md` — file names are cited inline so every number can be traced back to
its source script. Sample: paired base, n = 177 (US-only, prior AI-chatbot users; see
`sample.md`). Significance threshold α = .05; where a family of tests was Holm-corrected,
the corrected p (`p_holm`) is what's reported as SIG/ns, not the raw p.

---

## 1) What Users Know About Memory and Deletion

Objective knowledge was assessed with six best-answer/true-false items covering the "right
to be forgotten," AI training data, chatbot memory, data access scope, and retention policy
(`knowledge.md`). Respondents averaged **5.06 / 6 correct (84%; median 5/6)**; scores were
concentrated at the high end (46% answered all six correctly, 28% got five), but a
non-trivial 9% answered three or fewer correctly.

Accuracy varied considerably by topic (Figure 6):

| Item | % correct | Dominant misconception |
|---|---|---|
| Conversations may train future models | 94% | 6% believe chats aren't used for training |
| Memory (definition) | 87% | 11% confuse "memory" with server storage |
| Right to be forgotten (definition) | 86% | 6% confuse it with the right of access |
| Training data (definition) | 84% | 6% confuse it with developer-set system prompts |
| User data deleted after 5 years (False) | 84% | 16% believe a fixed 5-year deletion policy exists |
| **Chatbots access only public data (False)** | **70%** | **30% believe chatbots see only public data** |

The standout gap is the belief that chatbots only process publicly available data: nearly
1 in 3 respondents hold this misconception, making it the single weakest-understood concept
in the battery — well below the ~85-94% accuracy on the other five items. The second-largest
gap is the fixed 5-year retention myth (16%), suggesting users default to inventing a
concrete retention timeline when none is actually communicated to them.

*(Figure 6: `fig6_knowledge_accuracy.png`)*

---

## 2) Deletion Expectations and the Sensitivity Effect

### Scenario expectations and the within-subject comparison

The within-subject comparison (same 177 respondents, less-sensitive vs. more-sensitive data
scenario) produced the study's clearest and largest effect: **willingness to delete rises
significantly with data sensitivity** (paired Wilcoxon, mean 3.98 → 4.37, p < .0001, matched
rank-biserial r = +0.55 — the largest effect size anywhere in this analysis; `willingness.md`).
"Definitely yes" responses grew from 76 to 102 respondents, and "Definitely not" dropped to
zero. This result is one of only 14 (of ~101) tests in the whole battery that survives the
strictest possible global multiple-comparison correction (`global_correction.md`).

**Perceived protection** also rises significantly with sensitivity (Wilcoxon, p_holm = .0018,
r = 0.38, +0.133 on the 5-point scale; `stats.md` steps 3-4) — a smaller, framing-type effect:
the same deletion action *feels* more protective when the underlying data feels more
sensitive, even though **effort and benefit-loss ratings do not move** (both ns after Holm
correction). Note this is a different question from "does method choice affect protection"
(Kruskal-Wallis, ns in both scenarios) — method choice does not move protection, but scenario
sensitivity does (Figure 8).

Expectation and verification beliefs (what users think deletion actually does, and whether
they check) show no result that survives correction: the largest raw signal — a shift toward
expecting "permanently deleted" (9 respondents lost this belief, 22 gained it going
less→more) — is significant alone (raw p = .031) but does not survive Holm correction across
the 7 expectation options tested together (p_holm = .218, ns; `stats.md` step 5). This should
be reported as "not confirmed at this sample size," not as evidence sensitivity has no effect
on expectations.

Method switching is real but not systematic: 36% of respondents chose a different deletion
method in the more-sensitive scenario, but the aggregate distribution of method choice does
not shift (Stuart-Maxwell marginal homogeneity, p = .393, ns; `stats.md` step 6) — switching
runs in both directions (e.g., 13 respondents moved to a heavier method, 6 moved to a lighter
one), so this is individual-level churn, not population-level escalation toward heavier
methods under higher sensitivity.

*(Figure 8: `fig8_scenario_shift.png` — paired means, less vs. more sensitive, for
willingness/protection/effort/benefit-loss)*

### Prior-verification behavior

Confidence in one's belief about what deletion did predicts whether the respondent actually
verified it, in both scenarios — but the relationship does not strengthen when the data is
more sensitive (ordinal trend test: less-sensitive z = 2.50, p = .012; more-sensitive
z = 2.23, p = .026 — still significant, but weaker; `calibration_stats.md`). Descriptively,
miscalibration is flat-to-worse under higher sensitivity: among respondents who were "not at
all confident," 81.8% never verified in the less-sensitive scenario vs. **88.9%** in the
more-sensitive one (`calibration.md`).

The gap between which method people **actually use** and which they consider **ideal**
widens as sensitivity rises for most methods — e.g., "ask the chatbot to forget"
(32.8 → 42.1 percentage points), "delete a specific saved memory" (20.3 → 29.2 points),
"clear all saved memories" (13.0 → 19.7 points; `calibration.md`). These gaps are
statistically significant for 6 of 7 methods in the less-sensitive scenario and all 7 of 7
in the more-sensitive scenario (paired McNemar + Holm; `calibration_stats.md`), and 8 of
these used-vs-ideal tests survive even the strictest global correction across the entire
~101-test battery — among the most statistically robust results in this analysis. (Caveat:
"used" is single-select and "ideal" is select-all, so `ideal_only > used_only` is close to
mechanically likely for any popular method — the ranking and widening of gaps across
scenarios is the meaningful part, not the raw significance.)

### Cost-benefit ratings by method

Of the three per-method rating scales, **only effort significantly differentiates deletion
methods** (Kruskal-Wallis: less-sensitive H = 18.42, p = .0004; more-sensitive H = 16.98,
p = .0007; `stats.md` steps 1-2) — protection and benefit-loss do not differ significantly
by method in either scenario. Post-hoc comparisons (Dunn's, Holm-corrected) show "delete
this single conversation" is significantly lower-effort than "delete a specific saved memory
or fact" in both scenarios (r = 0.60 less-sensitive, r = 0.43 more-sensitive), and also
significantly lower-effort than "clear all conversation history" in the more-sensitive
scenario (r = 0.34).

Descriptively (`methods.md`), this produces a clear cost/benefit tradeoff structure that
holds in both scenarios (Figure 7): **"delete this single conversation"** is the
cheapest method (lowest effort: 1.62/1.67 less/more) but also the least protective
(3.54/3.73); **"delete a specific saved memory or fact"** is the opposite extreme — highest
effort (2.70/2.32) *and* highest felt benefit-loss (3.54/3.38), without being the most
protective option. Willingness to delete does not depend on which method someone uses, in
either scenario (Kruskal-Wallis, ns; `willingness.md`) — willingness is a property of a
person's disposition toward deleting at all, distinct from the method-specific cost ratings
described here.

*(Figure 7: `fig7_method_cost_benefit.png`)*




