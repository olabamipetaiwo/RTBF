# correlations

_Run at 2026-08-11T03:01:22_

# Method

1. Rank both variables, compute the ordinary (Pearson) correlation on the ranks — that gives ρ.
2. Convert ρ to a t-statistic: t = ρ × √((n-2) / (1-ρ²)). For [less] effort~benefit_loss: ρ=0.288, n=177 → t ≈ 3.978.
3. Look up that t-statistic in a t-distribution with n-2 degrees of freedom (175 here) — the p-value is the probability of getting a t this extreme (either direction) if the true correlation were 0.

```text


p(rho):  the Spearman correlation coefficient itself
p_raw :  p-value

======================================================================
TASK 1  DISCRIMINANT VALIDITY (Spearman, |rho|>=0.8 = coupled, Holm x9)
======================================================================

label                                 n  p(rho)    p_raw   p_holm  verdict
[less] protection~effort            177  -0.002   0.9779   1.0000  DISTINCT
[less] protection~benefit_loss      177   0.126   0.0956   0.5278  DISTINCT
[less] effort~benefit_loss          177   0.288   0.0001   0.0008  DISTINCT

[more] protection~effort            177  -0.068   0.3705   1.0000  DISTINCT
[more] protection~benefit_loss      177   0.128   0.0889   0.5278  DISTINCT
[more] effort~benefit_loss          177   0.247   0.0009   0.0065  DISTINCT


[pooled] protection~effort          177  -0.057   0.4485   1.0000  DISTINCT
[pooled] protection~benefit_loss    177   0.129   0.0880   0.5278  DISTINCT
[pooled] effort~benefit_loss        177   0.305   0.0000   0.0003  DISTINCT
```

TASK -  Make it into a table(check Slack) and add to overleaf


The p-value answers: If effort and benefit_loss were truly unrelated in the real population (true ρ=0),
how likely is it that a random sample of 177 people would still show a correlation as strong as 0.288 (or stronger) just by chance?

p_raw=0.0001 means: about a 1-in-10,000 chance of seeing this by luck alone if there were really no relationship. 

That's low enough to say the correlation is probably real, not noise — hence "significant."


## Interpretation

**Bottom line**: all 9 pairs are `DISTINCT` — max |ρ| = 0.305, nowhere near the 0.8
coupling threshold. Protection, effort, and benefit_loss hold up as statistically
separate constructs(statistically distinguishable constructs) in every scope (less, more, pooled). Task 1's aim is supported.

- **protection ⊥ effort**: ρ ranges -0.002 to -0.068 across all three scopes, all ns.
  How protective a method feels carries no relationship to how much work it feels
  like — genuinely independent axes, not just "distinguishable."

- **effort ~ benefit_loss is the one real relationship here**: ρ ≈ 0.25-0.31, and it's
  the only pair that's actually statistically significant — in the less-scenario and
  pooled scopes it survives even the strictest whole-study correction (Holm across all
  110 tests in the global battery: p_holm_global=.0099 and .0037 respectively); the
  more-scenario version is significant raw and under FDR but narrowly misses the
  strictest global Holm (p_holm_global=.085).

  Still only ρ≈0.3 — a small-to-moderate effect, not remotely close to redundant.

  in Summary - People who feel a deletion method takes more effort also tend to feel it costs them more (lost benefit), Not strong enough that effort and benefit_loss are the same thing, just a mild "more work, more loss" tendency. 
  
  Makes sense: the fiddlier methods (like hunting down one specific memory) feel like both more work and like you're giving up more, compared to a one-click action.

- **protection ~ benefit_loss**: small positive trend (ρ≈0.13) in all three scopes,
  consistently `ns`. Worth flagging: task 1's own pre-analysis hypothesis expected this
  pair *could* run negative ("more protection felt ↔ less loss felt"). The data show
  the opposite sign, but it's not distinguishable from zero at n=177 — no directional
  claim should be made, just note the a priori guess didn't pan out even in direction.

---

Rules

 - ρ (rho): Spearman's rank correlation coefficient — measures how strongly two variables move together, ranging from -1 (perfectly opposite ranking) to +1 (perfectly same ranking), 0 = no relationship. Used instead of Pearson's r because it works on ranks, not raw values, which is appropriate here since the Likert scales aren't normally distributed.
- |ρ|: absolute value of ρ — strips the sign so you're just measuring strength of association regardless of direction. Used for the 0.8 discriminant-validity threshold because a strong negative relationship (e.g. -0.85) would be just as much a "these aren't separate constructs" problem as a strong positive one (+0.85).
- p_raw: the raw p-value from the Spearman test — probability of seeing a correlation this strong (or stronger) if the true correlation were actually 0. Below .05 conventionally counts as "statistically significant," but this is before accounting for running multiple tests.
- p_holm: the p-value after Holm correction — adjusted upward to control for the fact that testing many pairs at once inflates the chance that at least one looks significant by luck. 

--- 

Why Holms

The problem it solves: every statistical test has a false-positive rate — at p<.05, there's a 5% chance of calling a real-zero relationship "significant" just from sampling noise. That's fine for one test. But run 9 tests (like this module does), and the chance that at least one comes back "significant" by pure luck climbs toward 1-(0.95)^9 ≈ 37%. Run all 110 across the whole study and it's over 99%. Without correction, you'd expect to find "significant" results even if literally nothing in the data were real.

Why Holm specifically: it's a step-down procedure — sort p-values smallest to largest, and each one has to clear a progressively looser bar than the smallest one did. It controls the same guarantee as Bonferroni (chance of any false positive across the whole family stays ≤5%) but is strictly more powerful — it never rejects fewer tests than Bonferroni would, sometimes more. That's why this codebase uses Holm everywhere instead of a flat Bonferroni divide.

Concretely in this data: [more] effort~benefit_loss has p_raw=.0009 — looks solid on its own. But it's 1 of 9 correlations tested here, and 1 of 110 in the whole study. Locally-corrected it's still fine (p_holm=.0065), but once folded into the full 110-test battery, the bar gets high enough that it just misses (p_holm_global=.085) — meaning across the entire study's worth of testing, you can't fully rule out that this particular result is a lucky draw. That's the exact reason stats.md's "permanently deleted" finding was flagged as ns despite raw p=.031 — same mechanism.

----

Spearman, |rho|>=0.8 = coupled, Holm x9

- Spearman — the test used: Spearman's rank correlation, not the more common Pearson correlation. Chosen because these Likert scales aren't normally distributed (confirmed earlier in stats.py's Shapiro tests), and Spearman doesn't assume normality — it works on ranks instead of raw values.
- |rho|>=0.8 = coupled — the pass/fail rule this whole task hinges on: if the strength of correlation between a pair of scales (protection/effort/benefit_loss) hits 0.8 or higher (regardless of sign, hence the absolute value bars), those two scales are considered too tightly coupled to defend as separate constructs — you couldn't claim "protection" is really measuring something different from "effort" if they moved together that closely. Below 0.8 = DISTINCT, at or above = COUPLED. None of the 9 pairs hit this (max was 0.305), so all 9 are DISTINCT.
- Holm x9 — the multiple-comparison correction applied: Holm's step-down correction, run across a family of 9 tests (the 9 rows in the table — 3 scale pairs × 3 scopes). This is what produces the p_holm column, distinct from the raw p_raw column, and adjusts for the fact that 9 tests were run at once rather than just one.


- p(rho) column (mislabeled — should just say rho): the Spearman correlation coefficient itself. Computed by ranking both variables and correlating the ranks (explained a couple messages back). Range: -1 to +1. This is the effect size — how strong the relationship is.
- p_raw column: the actual p-value, derived from that ρ via the t-distribution conversion I walked through last message (t = ρ√((n-2)/(1-ρ²)), then read off the t-distribution). Range: 0 to 1. This is the significance test — how surprising that ρ would be if the true relationship were zero.

- p_holm is p_raw, adjusted upward by the Holm correction to account for testing all 9 pairs at once

1. Sort all 9 p_raw values smallest → largest.
2. Multiply each by its "remaining count" — the smallest (rank 1) gets ×9, rank 2 gets ×8, rank 3 gets ×7, … down to the largest (rank 9) which gets ×1 (unchanged). This is Holm's core idea: the test that looked most impressive has to survive the harshest penalty, since it had the most "chances" to look impressive by luck.
3. Enforce monotonicity — each p_holm must be at least as large as the one before it in sorted order (running_max in the table above). This stops a correction artifact where a later, less-significant-looking test could end up with a smaller adjusted p-value than an earlier one — nonsensical, since it was less impressive to start with.
4. Cap at 1.0.

---

The verdict column is the simplest one — it doesn't touch p_raw or p_holm at all. It's a direct threshold check on rho alone:

r["verdict"] = "DISTINCT" if abs(r["rho"]) < THRESHOLD else "COUPLED"

where THRESHOLD = 0.8. That's it — no statistical test, no correction, just: is the correlation strength under 0.8 or not.

In this context, "distinct" and "coupled" describe whether two of the three rated qualities (protection, effort, benefit_loss) are actually measuring the same underlying thing in respondents' minds, or genuinely different things.

- DISTINCT: the two scales move together weakly enough (|ρ| < 0.8) that you can defend calling them separate constructs. Practically: when someone rates a deletion method as, say, high-effort, that rating doesn't strongly predict how they'll rate its protection or benefit-loss — the three questions are capturing different aspects of the person's experience, not the same underlying feeling asked three ways.
- COUPLED: the two scales move together so tightly (|ρ| ≥ 0.8) that they're effectively redundant — if you know someone's score on one, you can predict their score on the other almost perfectly. In that case, treating them as two separate measured constructs in the study would be misleading — you'd really just be measuring one thing twice under two different names, and any claim like "protection and effort are independently affected by X" would be suspect since they're not independent to begin with.

Why this matters for the study: the whole point of having three separate rating scales (protection, effort, benefit_loss) is to argue they capture three different dimensions of how people experience a deletion method. If any pair had come back COUPLED, that would undercut treating them as three separate findings throughout the rest of the analysis — you'd effectively have two scales, not three, wearing different labels. Since all 9 pairs came back DISTINCT (max ρ=0.305, well under 0.8), that concern doesn't apply here — the three scales hold up as measuring genuinely different things.

----

why dow we need to coupute p_raw and p_holm when we are using  rho as the guard fr  istunct/coupled

Because they're answering a different question than the threshold check, and dropping them would lose real information. Two separate things are true at once about a correlation: how strong is it (that's what the 0.8 threshold judges) and can you trust it's not just noise (that's what p_raw/p_holm judge). A number can be weak-but-real, or weak-and-meaningless, and |ρ| alone can't tell you which.

Concretely from your own table:

- effort~benefit_loss: rho=0.288 (weak), p_holm=0.0008 (statistically solid). This is a weak, real relationship — you can confidently say these two scales do move together somewhat, even though not enough to be redundant.
- protection~benefit_loss: rho≈0.13 (also weak), p_raw≈0.09-0.10, ns. This is weak, unconfirmed — you cannot say these move together at all; the observed 0.13 could just be sampling noise around a true value of zero.

If you only looked at rho vs. 0.8, both of these would print identically as "DISTINCT, small number" — but they support very different claims in the write-up. The first lets you say "effort and benefit_loss are genuinely related, just not so tightly that they're the same construct" (a positive finding). The second only lets you say "we found no evidence these are related" (an absence of finding) — that's exactly the caveat I wrote into the interpretation about protection~benefit_loss's flipped sign not being trustworthy.

deep

1. Protection is its own island. ρ with effort ranges -0.002 to -0.068 across less/more/pooled; ρ with benefit_loss ranges 0.126 to 0.129. Both essentially zero and never statistically significant in any scope. Whatever drives how protective a method feels to someone, it doesn't track with how much work they think it takes or how much they feel they lose. Of the three scales, protection is the most independent.
2. Effort and benefit_loss have the one real relationship in the set. ρ ≈ 0.25–0.31 (less=0.288, more=0.247, pooled=0.305) — positive, small-to-moderate, and the only pair that's actually statistically significant: in the less-scenario and pooled scopes it survives even the strictest whole-study correction (Holm across all 110 tests in the global battery, p_holm_global=.0099 and .0037); the more-scenario version is significant raw and under FDR but narrowly misses the strictest global Holm (p_holm_global=.085). Still only ρ≈0.3 — real, but nowhere near redundant. In plain terms: people who feel a deletion method takes more effort also tend to feel it costs them more — a mild "more work, more loss" tendency, not the same thing. Makes intuitive sense: fiddlier methods (hunting down one specific memory) feel like both more work and more of a loss, compared to a one-click action.
3. The correlation structure is stable across scenarios. Comparing less vs. more sensitive, none of the three pairs flip from present to absent or reverse sign (protection~effort: -0.002→-0.068; protection~benefit_loss: 0.126→0.128; effort~benefit_loss: 0.288→0.247). Notable because other measures in this study do shift with scenario sensitivity — protection's absolute level rises significantly less→more (stats.md steps 3-4, p_holm=.0018) — so while how protective people feel changes with sensitivity, how the three scales relate to each other doesn't.
4. protection~benefit_loss ran the "wrong" direction, though not confirmed. Weak positive trend (ρ≈0.13) in every scope, consistently ns. Task 1's own pre-analysis hypothesis expected this pair could run negative ("more protection felt ↔ less loss felt"). The data show the opposite sign — but since it's not statistically distinguishable from zero at n=177, no directional claim should actually be made; just worth flagging that the a priori guess didn't pan out even in direction.