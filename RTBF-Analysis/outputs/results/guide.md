Looking at the actual numbers in stats.md:

Steps 1-2 (Kruskal-Wallis, differencesach scenario):
[less | protection]     H=5.18  p=0.1593  -> ns
[less | benefit_loss]   H=5.29  p=0.1515  -> ns
[more | protection]     H=0.54  p=0.9106  -> ns                                                        [more | benefit_loss]   H=2.89  p=0.40

Yes — all four are ns. That's what "Protection and benefit_loss are all ns" refers to: which deletion  method someone used doesn't significanon or benefit_loss rating, in eitherscenario.                                
                                                              
Steps 3-4 (paired test, differences between scenarios less→more, regardless of method):
[protection]     p_holm=0.0018  -> SIG                                                                 [benefit_loss]   p_holm=0.5952  -> ns
Here protection is significant — going from less-sensitive to more-sensitive data significantly raises perceived protection.

So the two "protection" results aren't contradictory, they're answering different questions:           - Does method choice move protection?
- Does scenario sensitivity move protection? → Yes (SIG).                                              
benefit_loss is the only scale that's ns on both axes — method doesn't move it, and scenario doesn't   move it either.

The interpretation section in stats.md states this correctly but the two facts are in separate bullets,which makes it easy to misread at a gl section to make themethod-vs-scenario distinction more explicit for protection specifically?
                                                                                                         Brewed for 16s

❯ what is ns?                                                                                            
"ns" = not significant — shorthand for "the p-value did not fall below the significance threshold (0.05)," so the test failed to detect a statistically reliable difference/effect at that sample size.  
It's not a null score or "zero effect" — it just means the data don't clear the bar needed to confidently rule out chance. That distinction matters here specifically: the script's own docstring in stats.py flags it explicitly — "Nulls fference.'" Several of your groups aresmall (n=14–33 for some methods), so an ns result could mean "genuinely no effect" or "too little data to tell," and this analysis can't distinguish between those two.


- **Scenario effect (steps 3- sensitivity (less→more) signifi
cantly increases perceived **protection** (Wilcoxon, p_holm=0.0018, r=0.38, +0.133 on a
 5-pt scale) but has no significant effect on effort or benefit_loss (both ns after Hol
m). Read this as a framing eftion is *felt* as more protectiv
e when the underlying data feels more sensitive, even though how burdensome it feels an
d how much you feel you lose don't move. This is a small-to-medium effect (r≈0.38), not
 a large one.

  ⚠️ **Protection specifically gets a different answer on each axis — don't conflate th
em:**
  | question | test | result |
  |---|---|---|
  | Does *which method* someoection rating? | Kruskal-Wallis,
 steps 1-2 | **ns** (less: p=0.159; more: p=0.911) |
  | Does *scenario sensitivity* (less→more) predict protection rating? | Paired Wilcoxo
n, steps 3-4 | **SIG** (p_hol

  So "protection is ns" is only true for the method comparison. The correct combined st
atement is: **method choice doesn't move protection, but scenario sensitivity does.** b
enefit_loss is the only scale that's ns on *both* axes — it's the one dead end here.

- **Expectation & verification (step 5, McNemar)**: nothing survives Holm correction ac
ross either the 7 expectation options or the 8 verification options — all `ns`. The lar
gest raw discordance (expecting "permanently deleted," option 1: 9 less-only vs. 22 mor
e-only) looks suggestive on its face but doesn't clear multiple-comparison correction.
Per the script's own caveat, treat these as **underpowered nulls, not evidence of no ef
fect** — don't report "sensitivity doesn't change expectations," report "we can't confi
rm it does at this sample size."

- **Method switching (step 6)**: 64% of respondents pick the *same* method in both scen
arios; 36% switch. But the switch isn't a systematic escalation toward heavier methods
— Stuart-Maxwell marginal homogeneity is ns (p=0.393), meaning the aggregate distributi
on of method choice doesn't shift. The transition matrix shows switching in both direct
ions: 13 people moved from "Delete this single conversation" up to "Clear all conversat
ion history" when sensitivity rose (the single largest off-diagonal cell), but 6 moved         the opposite way (heavier→lig churn shows up elsewhere in the
 matrix. So there's real individual-level churn (over a third of respondents), just no
clean population-level "people escalate under sensitivity" story.                             
Added a comparison table right after the scenario-effect bullet that puts the two protection results side by side, plus a one-line takeaway distinguishing method-level (ns) from scenario-level (SIG). Also clarified that benefit_loss is the onlaxes — the actual dead end in thisdataset.
                                                                                                    Worked for 18s

❯ what is the criteria we are using to detwrmine ns or SIG?

The threshold is α = 0.05 everywhere (p < 0.05 = SIG, p ≥ 0.05 = ns) — but which p-value gets compared to that threshold differs by step, because some families of tests are multiple-comparison corrected and some aren't. From src/stats.py:

┌───────────┬────────────────────────────────┬─────────────────────────────────────────────────────┐
│   Step    │              Test              │               What's compared to 0.05               │
├───────────┼────────────────────────────────┼────────────────────────────────────────────────────│ 1-2       │ Kruskal-Wallis (method   0.05 (line ~72), no correction    │
│ omnibus   │ differences)                   │ across the 6 omnibus tests (3 scales × 2 scenarios) │
├───────────┼────────────────────────────────┼────────────────────────────────────────────────────│ 1-2       │ Dunn's pairwise (which m but only run if the omnibus above │
│ post-hoc  │  differ)                       │  was already SIG                                    │
├───────────┼────────────────────────────────┼────────────────────────────────────────────────────│           │ Paired t-test / Wilcoxonacross the 3 scales                │
│ 3-4       │ (scenario effect)              │ (protection/effort/benefit_loss) via                │
│           │                                │ multipletests(..., method="holm")                  ├───────────┼────────────────────────────────────────────────────────────┤
│ 5         │ McNemar                        │ Holm-corrected p, separately within the 7           │
│           │ (expectation/verification)     │ expectation options and the 8 verification options ├───────────┼────────────────────────────────────────────────────────────┤
│ 6         │ Stuart-Maxwell (method         │ raw p — single omnibus test, nothing to correct for │
│           │ switching)                     │                                                    └───────────┴────────────────────────────────────────────────────────────┘
                                                                                                  Worth flagging: steps 1-2's omnibus Kr p, uncorrected across the 6 of them,while steps 3-4 correct across their 3. That's an inconsistency in how conservative the two families are — if you ran all 6 KW tests through the same Holm correction, some of the currently-SIG effortresults (p=0.0004, p=0.0007) would alme they're well under 0.05/6≈0.0083, but it's not guaranteed and isn't currently being applied. Want me to make that correction explicit (either add Holm across the 6 omnibus tests, or add a comment explaining why it's intentionally leuncorrected)?

✻ Worked for 22s                                                                                    
※ recap: We're running statistical tests on your RTBF deletion-method survey and just finished writing up the findings in stats.md. Next: decide whether to Holm-correct the six Kruskal-Wallis             method-comparison tests, which currents.

❯ raw p?                                                                                            
"Raw p" = the p-value straight out of the statistical test itself, with no adjustment for running multiple tests — as opposed to "p_holm that same p-value inflated upward bythe Holm procedure to compensate for testing multiple hypotheses at once.                              
Why it matters: every time you run more than one test, your chance of at least one false positive (a "significant" result that's actually just noise) climbs. Correction procedures like Holm raise the bar  each additional test has to clear, so  rate across the whole family of testsstays near 5%, not 5%-per-test.

Concretely, in your stats.md:
- Steps 3-4 report both: p_raw=0.0006 p_holm=0.0018 for protection — the raw p is what the Wilcoxon     test itself produced; p_holm is that vupward to account for testing 3 scales. The SIG/ns call is made on p_holm, not p_raw.                                                           - Steps 1-2's omnibus Kruskal-Wallis lg. p=0.0004 for effort) — that's theraw, uncorrected p, and it's what's directly compared to 0.05. There's no p_holm column for those       because, as noted, that family isn't cs.

So "raw p < 0.05" in the steps-1-2 table means literally that single test's own p-value, untouched —    not adjusted for the fact that 6 such

✻ Cogitated for 11s

❯ what is p?                                                                                             
p (p-value) is the probability of seeing a result as extreme as the one you got — or more extreme — if  there were actually no real effect/dif hypothesis were true).

- Small p (e.g., p=0.0004 for effort by method) → "if method truly made no difference, a gap this large between groups would only show up 4 tihance alone." That's unlikely enoughthat you conclude the difference is probably real, not noise.
- Large p (e.g., p=0.91 for protection by method, "more" scenario) → "if method truly made no difference, seeing exactly this pattern (or a bigger gap) would happen 91% of the time by pure chance." Way too common to conclude anything — you can't distinguish it from noise.

It is not:
- The probability the null hypothesis
- The probability your finding is "real."
- The size or importance of the effect— the r=, dz=, eps2= values in yourreport — is for). A tiny, meaningless effect can still hit p<0.05 with a big enough sample, and a leffect can fail to reach significance  is exactly the caveat baked into your stats.py docstring: "Kept methods are n~14-83: tests detect only LARGE effects").
                                                                                                   Where it comes from in each test you'r
- Kruskal-Wallis / Mann-Whitney: derived from how extreme the rank-sum differences between groups are.
- Paired t-test: derived from how far the mean of the paired differences is from zero, relative to their spread.
- Wilcoxon signed-rank: like the paired t-test but based on ranks of differences, not raw values — here because Shapiro-Wilk found the di.
- McNemar: derived from the imbalance between the two "discordant" cells (switched one way vs. the other) in a 2×2 table.

The 0.05 cutoff itself is just a convention — not a law of nature — for deciding "unlikely enough toact on."



H is the Kruskal-Wallis test statistic — the number the p-value for your steps 1-2 (between-method) tests is derived from. It's the non-parametric analog of the F-statistic in ANOVA.

How it's built: Kruskal-Wallis ranks all the observations across every method group together (ignoring which group they came from), then checks whether the average rank in each group is close to what you'd expect if group membership didn't matter. H measures how far the groups' average ranks deviate from that "no difference" expectation — weighted by group size.

- H ≈ 0 → the groups' average ranks are basically identical → methods aren't separating the data at all.
- Large H → at least one group's ranks are systematically higher or lower than the others → methods are producing different distributions of scores.

H is then compared against a chi-squared distribution with k − 1 degrees of freedom (k = number of groups) to get the p-value. That's why your eps2 (epsilon-squared) effect size formula in stats.py — (H − k + 1) / (n − k) — subtracts off k − 1: it's rescaling H by its expected value under the null so you get a 0–1 effect-size measure instead of a raw, sample-size-dependent statistic.

Concretely from your report: [less | effort] KW H=18.42 p=0.0004 — ranking all ~186 protection-effort scores together across the 4 qualifying methods, the actual rank-spread between method groups was far larger (H=18.42) than the ~3 (=k−1, roughly the expected value under the null for 4 groups) you'd expect if effort really didn't depend on method — hence the very small p-value.

It's called the Kruskal-Wallis H statistic (or just "the H-statistic" / "test statistic H").

For write-ups, the standard (APA-style) way to report it is:

▎ H(df, N) = value, p = value

e.g. for your [less | effort] result:

▎ H(3, N=161) = 18.42, p < .001

where df = k − 1 (k = number of method groups compared, so 4 groups − 1 = 3), and N is the total n across the groups actually tested (not your full paired base of 177 — just the sum of the kept-method group sizes for that scale).

The interpretation direction is always the same regardless of which threshold you pick:
- p ≤ threshold → reject the null → SIG → "unlikely enough to be chance; treat this as a real effect."
- p > threshold → fail to reject the null → ns → "too likely to be chance; can't distinguish this from noise."
