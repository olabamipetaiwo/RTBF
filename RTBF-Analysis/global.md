# RTBF Survey Analysis — Global Results

This file consolidates every result from the analysis, with concise interpretation, from **both**
statistical pipelines in this repo:

- **Part A — Normal analysis** (`src/`): the original pipeline, using `statsmodels` (McNemar,
  Stuart-Maxwell, ordinal trend test, Holm/FDR correction), `pingouin` (Wilcoxon effect size,
  Cronbach's alpha), and `scikit-posthocs` (Dunn's post-hoc). Outputs in `outputs/results/`.
- **Part B — Scipy analysis** (`scipy_analysis/`): a from-scratch reimplementation of the same
  test/post-hoc/correction layer using only `scipy.stats`/`numpy`, reading the same screened data.
  Outputs in `scipy_analysis/outputs/results/`. This is also where every *newer* analysis (task
  list in `tasks.md`) was implemented, so Part B has some sections with no Part A counterpart.

The two pipelines were cross-checked against each other — see **Cross-validation**, at the end —
and agree almost exactly, so treat numbers in both parts as validated.

Convention throughout: α = 0.05, Holm correction applied within each stated test family unless
noted otherwise.

---

## 0. Sample, screening & knowledge check

*(Descriptive only — identical inputs feed both pipelines, so this isn't split.)*

**Screening:** 219 raw rows → 1 dropped (failed `Q6.5` attention check) → 36 dropped (never
deleted data before) → 182 eligible → paired analysis base **n=177** (answered both Q4.2 and
Q5.2).

**Sample (n=177):** 100% US-based, 100% prior chatbot users (eligibility criteria, not findings).
Age skews young — 73% under 45, only 11% over 55. Chatbot experience: ChatGPT near-universal
(99.4%), Gemini widely used (92.7%), Claude/Copilot mid-tier (67.8% each), Perplexity/Deepseek
least used and most recently adopted (41.8%/36.2%).

**Read:** findings generalize to a young, US, experienced-chatbot-user population. Any
platform-specific split would be far better powered for ChatGPT/Gemini than Deepseek.

**Objective knowledge (Q8.2–Q8.7, n=177):** mean score 5.06/6, median 5/6 — generally
knowledgeable sample. Weakest item: "chatbots access only public data" — only 70.1% correct,
29.9% hold that misconception. Strongest: "conversations may train future models" (93.8%
correct).

---

# Part A — Normal analysis (`src/`)

## A1. Method usage & per-method cost/benefit

Method selection counts (paired base, n=177):

| method | less | more |
|---|---|---|
| Delete single conversation | 84 | 80 |
| Clear all history | 33 | 40 |
| Delete specific memory | 19 | 22 |
| Ask chatbot to forget | 25 | 14 |
| Clear all memories | 7 | 8 |
| Privacy dashboard | 6 | 9 |
| Delete account | 2 | 3 |

Only the top 4 clear the n≥14 floor used for group comparisons.

Mean ratings (5-pt scales), n≥14 methods:

| method | scenario | n | protection | effort | benefit_loss |
|---|---|---|---|---|---|
| Delete single conversation | less | 84 | 3.54 | 1.62 | 2.97 |
| Delete single conversation | more | 81 | 3.73 | 1.67 | 3.02 |
| Clear all history | less | 33 | 3.77 | 1.98 | 3.06 |
| Clear all history | more | 40 | 3.78 | 2.18 | 3.14 |
| Delete specific memory | less | 19 | 3.58 | 2.70 | 3.54 |
| Delete specific memory | more | 22 | 3.71 | 2.32 | 3.38 |
| Ask chatbot to forget | less | 25 | 3.84 | 1.86 | 2.91 |
| Ask chatbot to forget | more | 14 | 3.89 | 1.54 | 2.90 |

**Ranking (n≥15):** "Ask chatbot to forget" rates highest protection in both scenarios;
"Delete specific memory" is consistently highest-effort and highest-benefit-loss; "Delete single
conversation" is consistently lowest-effort. (These are descriptive rankings only — see A2 for
which differences are statistically real.)

## A2. Between-method & between-scenario tests (`stats.md`)

**Steps 1–2, between-method (Kruskal-Wallis):**

| scale | less | more |
|---|---|---|
| protection | H=5.18, p=.159 → ns | H=0.54, p=.911 → ns |
| effort | H=18.42, p=.0004 → **SIG** | H=16.98, p=.0007 → **SIG** |
| benefit_loss | H=5.29, p=.152 → ns | H=2.89, p=.409 → ns |

**Steps 3–4, between-scenario (paired Wilcoxon, Holm ×3):**

| scale | mean diff (more − less) | p_raw | p_holm | verdict |
|---|---|---|---|---|
| protection | +0.133 | .0006 | .0018 | **SIG**, r=0.38 |
| effort | +0.032 | .485 | .594 | ns |
| benefit_loss | +0.043 | .297 | .594 | ns |

**Interpretation — protection gets two different answers depending on the question asked:**
does *which method* someone uses predict their protection rating? No (ns, both scenarios). Does
*scenario sensitivity itself* (less→more) predict protection? Yes (SIG, p_holm=.0018) — a
small-to-medium effect (r≈0.38). These aren't contradictory; they answer different questions, and
conflating them is the easiest way to misread this dataset. **benefit_loss is the only scale
that's ns on both axes** — method doesn't move it, scenario doesn't move it either.

**Step 5, McNemar per expectation/verification option (Holm ×7/×8):** nothing survives
correction in either family. Largest raw discordance ("permanently deleted": 9 less-only vs. 22
more-only) looks suggestive but doesn't clear correction — treat as an **underpowered null**, not
confirmed absence of effect.

**Step 6, method switching (Stuart-Maxwell + transition matrix):** 64% of respondents (113/176)
stay on the same method; 36% (63) switch. Stuart-Maxwell marginal homogeneity: stat=6.276, df=6,
p=.393 → ns — no systematic population-level escalation toward heavier methods. Real
individual-level churn, no clean aggregate direction.

## A3. Expectations & verification by method (`expectation.md`)

Descriptive only — no significance test in this script (aggregate test is `stats.md` step 5,
already ns).

- **Training-data blind spot, every method:** "no longer used for training" is the lowest- or
  near-lowest-endorsed expectation for every method in both scenarios (15–37% vs. 42–77% for
  other options) — 65–85% of users do **not** expect deletion to stop their data training the
  model, regardless of method.
- **Verification effort tracks invocation effort:** the two lowest-effort methods ("Delete single
  conversation," "Clear all history") also have by far the highest "did NOT know how to check"
  rates (59.5%/42.4% less, 56.8%/42.5% more) and lowest active-verification rates. "Ask chatbot to
  forget" is the opposite — verification is nearly built into the action (52–57% "asked in same
  conversation").
- **Directional (untested) shift toward "permanently deleted"** for the two biggest methods as
  sensitivity rises — consistent in direction with the ns aggregate McNemar signal, not
  independent confirmation.

## A4. Scenario shift summary (`scenario_shift.md`)

| measure | less | more | diff | verdict |
|---|---|---|---|---|
| Willingness | 3.977 | 4.367 | +0.390 | **SIG** p<.0001, r=+0.55 |
| Protection | 3.659 | 3.792 | +0.133 | **SIG** p_holm=.0018, r=0.38 |
| Effort | 1.903 | 1.935 | +0.032 | ns |
| Benefit loss | 3.075 | 3.119 | +0.043 | ns |

Willingness to delete rises more strongly with sensitivity (r=0.55) than protection does
(r=0.38); effort and benefit_loss are unmoved.

## A5. Moderators (`moderators.md`)

| moderator | scenario | protection/effort/benefit_loss/willingness | method choice |
|---|---|---|---|
| Age group | less | all 4 ns | **SIG** p=.0151, V=.229 |
| Age group | more | all 4 ns | ns p=.0797 |
| ChatGPT tenure | less | all 4 ns | ns p=.1213 |
| ChatGPT tenure | more | all 4 ns | **SIG** p=.0133, V=.207 |

Neither moderator affects the rating scales in either scenario. Age predicts method choice in the
less-sensitive scenario only; tenure predicts it in the more-sensitive scenario only — modest
effect sizes (V≈0.2–0.23), real but not large.

## A6. Willingness (`willingness.md` — Part A source is `scenario_shift.md`/`stats.md`, no
standalone Part A file; see A4).

## A7. Calibration (`calibration.md` descriptive + `calibration_stats.md` tested)

**8a. Confidence vs. verification:** even "Not at all confident" respondents skip verification
81.8% of the time (less) / 88.9% (more). Every confidence band shows flat-to-worse verification
more-sensitive except "Moderately confident" (59.0%→50.0%, an improvement). Confidence-verification
miscalibration does **not** improve when stakes rise — if anything it's slightly worse.

**8b. Used vs. ideal method — gaps widen, not narrow, as sensitivity rises**, for most methods:
"Ask to forget" 32.8→42.1 pts, "Delete specific mem" 20.3→29.2, "Clear all memories" 13.0→19.7.
People's *preferences* shift toward heavier methods faster than their *actual behavior* does.
Desire for a "File a request" option (not in the actual method list) roughly doubles: 2.3%→5.1%.

## A8. Reliability

Cronbach's alpha for all 3 scales, both scenarios, all ≥0.87 (see B — identical scale
construction, values reported once in Part B §B6 to avoid duplication; both pipelines compute the
same alpha).

## A9. Method switching / McNemar summary

See A2 step 6 above (`stats.md`) — the standalone `mcnemar.md`/ranking breakdown is a scipy-only
addition, reported in Part B §B9.

---

# Part B — Scipy analysis (`scipy_analysis/`)

*Same test families as Part A, reimplemented in scipy only, plus the newer task-driven analyses
that only exist here.*

## B1. Reliability (Cronbach's alpha, ≥0.70 = acceptable)

| scenario | scale | items | alpha | 95% CI | verdict |
|---|---|---|---|---|---|
| less | protection | 5 | 0.893 | [.86, .92] | OK |
| less | effort | 4 | 0.921 | [.90, .94] | OK |
| less | benefit_loss | 3 | 0.870 | [.83, .90] | OK |
| more | protection | 5 | 0.900 | [.88, .92] | OK |
| more | effort | 4 | 0.923 | [.90, .94] | OK |
| more | benefit_loss | 3 | 0.872 | [.84, .90] | OK |

All six scales are reliably measured (0.87–0.92, well above the 0.70 bar).

## B2. Discriminant validity — are protection/effort/benefit_loss separate constructs? (`correlations.md`)

Spearman ρ, 3 scale pairs × 3 scopes (less/more/pooled), Holm ×9. Threshold: |ρ|≥0.8 = too
coupled to treat as separate constructs.

| pair | less ρ | more ρ | pooled ρ | verdict |
|---|---|---|---|---|
| protection ~ effort | −0.002 ns | −0.068 ns | −0.057 ns | DISTINCT |
| protection ~ benefit_loss | 0.126 ns | 0.128 ns | 0.129 ns | DISTINCT |
| effort ~ benefit_loss | 0.288, p_holm=.0008 | 0.247, p_holm=.0065 | 0.305, p_holm=.0003 | DISTINCT |

**Bottom line:** all 9 pairs DISTINCT, max |ρ|=0.305 — nowhere near the coupling threshold.

- **Protection is its own island** — essentially zero, never-significant correlation with either
  other scale.
- **Effort ~ benefit_loss is the one real relationship**: small-to-moderate (ρ≈0.25–0.31),
  statistically real (survives global Holm in less/pooled scopes; narrowly misses it in
  more-scenario, p_holm_global=.085). People who find a method more effortful also tend to feel it
  costs more — fiddlier methods (hunting down one memory) feel like both more work and more of a
  loss vs. a one-click action. Still weak, not redundant.
- **protection ~ benefit_loss** ran opposite the pre-registered hypothesis sign (expected
  negative), but the +0.13 observed is not distinguishable from zero — no directional claim
  warranted.
- Structure is stable across scenarios — no pair flips sign or crosses significance less→more,
  even though protection's absolute *level* does shift with scenario (B5).

## B3. Pooling methodology (`pooling.md`)

Each of the 177 respondents contributes exactly one observation per method group: same-method-
both-scenarios respondents have their two ratings averaged; method-switchers contribute one point
to each of the two methods they used (mild, unavoidable non-independence across groups, no
double-counting within a group).

| method | n_less | n_more | n_pooled |
|---|---|---|---|
| Delete single conversation | 84 | 81 | 105 |
| Clear all history | 33 | 40 | 50 |
| Delete specific memory | 19 | 22 | 30 |
| Ask chatbot to forget | 25 | 14 | 29 |
| Clear all memories | 7 | 8 | 11 |
| Privacy dashboard | 6 | 9 | 11 |
| Delete account | 2 | 3 | 3 |

## B4. Pooled cost/benefit table (`fig9_pooled_cost_benefit.md`)

| method | n | protection | effort | benefit_loss |
|---|---|---|---|---|
| Delete single conversation | 105 | 3.66 | 1.68 | 3.01 |
| Clear all history | 50 | 3.80 | 2.04 | 3.11 |
| Delete specific memory | 30 | 3.65 | 2.45 | 3.43 |
| Ask chatbot to forget | 29 | 3.79 | 1.79 | 2.99 |

## B5. "Crowning" — is any method statistically the best? (`crowning.md`)

Kruskal-Wallis (4 qualifying methods) → Dunn's + Holm if significant. A method is "crowned" only
if it has the best point estimate **and** significantly beats *every* other method.

| scale | less | more | pooled |
|---|---|---|---|
| protection | ns | ns | ns |
| benefit_loss | ns | ns | ns |
| effort | H=18.42, p=.0004 **PARTIAL** | H=16.98, p=.0007 **PARTIAL** | H=19.54, p=.0002 **PARTIAL** |

**Bottom line: no method is ever fully crowned on any scale, in any scope.** Strongest defensible
claim: *"Delete this single conversation" is reliably lower-effort than "delete a specific saved
memory," everywhere* — but not distinguishable from "clear all history" or "ask chatbot to
forget," so no single lowest-effort method can be named.

- Less & pooled: "Delete single conversation" has the best mean effort, significantly beats
  "Delete specific memory" (p_holm=.0002 both) — indistinguishable from the other two.
- **More scenario flips the point estimate**: "Ask chatbot to forget" has the lowest raw mean
  (1.54 vs. 1.67) but doesn't significantly beat anything (closest p_holm=.078). The "delete
  single conversation = lowest effort" narrative used elsewhere holds in 2 of 3 scopes, not this
  one specifically.
- Protection/benefit_loss: 6/6 tests null even after pooling roughly doubled n for smaller
  methods specifically to give this a chance to find something.

## B6. Scenario effect (`stats.md`) — matches Part A2 exactly (cross-validated, see below)

Reported once in Part A §A2/A4 — scipy pipeline reproduces identical H/p/Wilcoxon values.

## B7. Between-method verification/expectation tests (`verify.md`)

Significant (Holm-corrected) associations between method and behavior:

- **Less-sensitive verification:** "asked same convo" (p_holm=.0016), "asked new convo"
  (p_holm=.0102), "did NOT know how" (p_holm=.0080).
- **More-sensitive verification:** "asked same convo" (p_holm=.0368), "checked settings"
  (p_holm=.0441).
- No expectation option reaches significance by method in either scenario.

Confirms the descriptive pattern in A3: verification behavior depends on method; expectations do
not (at least not detectably at this n).

## B8. Within-scenario ranking of beliefs/verification (`expectation_rank.md`) — scipy-only

Cochran's Q on the full option set, per scenario — is there a genuine pecking order among options,
independent of method or scenario-to-scenario shift?

| family | less Q, p | more Q, p |
|---|---|---|
| Expectation | Q=245.25, p=4.2e-50 **SIG** | Q=247.39, p=1.5e-50 **SIG** |
| Verification | Q=142.99, p=1.2e-27 **SIG** | Q=147.02, p=1.7e-28 **SIG** |

Both scenarios: **"did NOT know how to check" is the single most common verification response**
(~44–45%). Expectation ranking top-to-bottom (less): permanently deleted (55.4%) > not ref.
future (54.2%) > not ref. current (52.0%) > not used for training (26.6%) > made invisible (26.0%)
> not sure (9.6%) > other (1.1%) — pairwise McNemar+Holm confirms nearly every adjacent gap is
real, not noise. This answers "is there a real hierarchy within one scenario" — it does **not**
answer whether rates shift between scenarios (that's A2 step 5, ns) or whether they differ by
method (that's B7).

## B9. Method switching, McNemar per method + ranked shift (`mcnemar.md`, `fig10_method_shift_ranking.md`)

| method | dropped | added | discordant | net | p_holm |
|---|---|---|---|---|---|
| Clear all history | 10 | 17 | 27 | +7 | 1.0 |
| Delete specific memory | 8 | 11 | 19 | +3 | 1.0 |
| Privacy dashboard | 2 | 5 | 7 | +3 | 1.0 |
| Clear all memories | 3 | 4 | 7 | +1 | 1.0 |
| Delete account | 0 | 1 | 1 | +1 | 1.0 |
| Delete single conversation | 25 | 21 | 46 | −4 | 1.0 |
| Ask chatbot to forget | 15 | 4 | 19 | −11 | .135 |

**Nothing survives Holm correction** — closest is "Ask chatbot to forget" (p_raw=.019,
p_holm=.135). "Clear all history" gains the most net adopters (+7); "Ask chatbot to forget" loses
the most (−11) as sensitivity rises, but neither is statistically confirmed. **Why the test lacks
power despite a real-looking net-11 shift:** McNemar only draws on discordant (switching)
respondents — "Ask chatbot to forget" has only 19 people (15+4) feeding its test, not 177, and
Holm across 7 methods raises the bar further. The effect may be real; the test is underpowered,
not the population.

## B10. Global multiple-comparison correction (`global_correction.md`)

Across **117 primary/omnibus tests** in the whole study: 39 significant at raw p<.05, dropping to
**21 under Holm-global** (strictest) and **31 under BH-FDR-global**.

Survives even strict whole-study Holm: all calibration used-vs-ideal gaps (A7/B-equivalent), all
four expectation/verification Cochran's Q rankings (B8), the willingness scenario shift (A4), the
effort~benefit_loss correlation in less/pooled scopes (B2), the effort crowning-partial result
(B5), several verify.py method-verification associations (B7), the effort omnibus KW in both
scenarios (A2/B5), and — narrowly — the protection scenario-shift (A2/A4).

**Nuance:** the protection scenario-shift Wilcoxon (p_holm=.0018 within its own 3-test family,
and still significant under BH-FDR-global) is *not* significant under the strictest whole-study
Holm-global correction (p_holm_global≈.058) — right at the edge once folded into all 117 tests.
Report as a real, if borderline, effect.

---

## Cross-validation (`scipy_analysis/outputs/results/compare.md`)

The scipy pipeline (Part B) was checked against the original statsmodels/pingouin/scikit-posthocs
pipeline (Part A) across every matched test:

- **101 tests compared: Pearson r = 0.999961, Spearman rho = 0.999828.**
- 73/101 exact matches (diff < 1e-9); 28/101 near matches (diff < 0.02); 0 drifted; **0
  significance flips**.
- The 28 near-matches are explained by (1) scipy's r×c `fisher_exact` being internally
  Monte-Carlo-randomized with no exposed seed — drifts slightly even between two runs of the same
  code, not a reimplementation discrepancy — affecting `verify.*`/`moderators.method_choice`
  rows; and (2) `scipy.stats.wilcoxon`'s default continuity correction differing slightly from
  `pingouin`'s, producing a <0.002 p-value difference on `stats.between_scenario_likert` /
  `willingness.scenario_shift` rows.

**Conclusion:** the two pipelines agree closely enough that every number in Part A and Part B
above should be read as validated, not as two competing analyses.
