# stats

_Run at 2026-08-07T14:18:50_

```text
paired base n = 177

======================================================================
STEPS 1-2  BETWEEN-METHOD (Kruskal-Wallis -> Dunn's + Holm)
======================================================================

[less | protection] KW  H=5.18  p=0.1593  eps2=0.014  -> ns

[less | effort] KW  H=18.42  p=0.0004  eps2=0.098  -> SIG
    * Delete this single conversat vs Delete a specific saved memo p_holm=0.0002  r=0.597

[less | benefit_loss] KW  H=5.29  p=0.1515  eps2=0.015  -> ns

[more | protection] KW  H=0.54  p=0.9106  eps2=-0.016  -> ns

[more | effort] KW  H=16.98  p=0.0007  eps2=0.092  -> SIG
    * Delete this single conversat vs Clear all conversation histo p_holm=0.0098  r=0.342
    * Delete this single conversat vs Delete a specific saved memo p_holm=0.0078  r=0.426

[more | benefit_loss] KW  H=2.89  p=0.4088  eps2=-0.001  -> ns

======================================================================
STEPS 3-4  BETWEEN-SCENARIO Likert (Shapiro -> t/Wilcoxon, Holm x3)
======================================================================

[protection] shapiro_normal=False  Wilcoxon  stat=1752.0  r=0.382  mean_diff=+0.133 (more>less)
    p_raw=0.0006  p_holm=0.0018  -> SIG

[effort] shapiro_normal=False  Wilcoxon  stat=1750.5  r=0.085  mean_diff=+0.032 (more>less)
    p_raw=0.4867  p_holm=0.5952  -> ns

[benefit_loss] shapiro_normal=False  Wilcoxon  stat=1999.5  r=0.123  mean_diff=+0.043 (more>less)
    p_raw=0.2976  p_holm=0.5952  -> ns

======================================================================
STEP 5  BETWEEN-SCENARIO binary: McNemar per option
======================================================================

-- expectation (Q4.4/Q5.4) --
    opt1: less-only=  9 more-only= 22 (more>less)  p_holm=0.2180  ns
    opt2: less-only= 12 more-only= 21 (more>less)  p_holm=0.9284  ns
    opt3: less-only= 25 more-only= 15 (less>more)  p_holm=0.9284  ns
    opt4: less-only= 18 more-only= 18 (less>more)  p_holm=1.0000  ns
    opt5: less-only= 12 more-only= 16 (more>less)  p_holm=1.0000  ns
    opt6: less-only=  6 more-only=  9 (more>less)  p_holm=1.0000  ns
    opt7: less-only=  1 more-only=  0 (less>more)  p_holm=1.0000  ns

-- verification (Q4.5/Q5.5) --
    opt1: less-only= 16 more-only= 13 (less>more)  p_holm=1.0000  ns
    opt2: less-only= 10 more-only= 17 (more>less)  p_holm=1.0000  ns
    opt3: less-only= 12 more-only= 10 (less>more)  p_holm=1.0000  ns
    opt4: less-only= 15 more-only= 10 (less>more)  p_holm=1.0000  ns
    opt5: less-only=  5 more-only=  5 (less>more)  p_holm=1.0000  ns
    opt6: less-only= 13 more-only= 13 (less>more)  p_holm=1.0000  ns
    opt7: less-only=  7 more-only=  5 (less>more)  p_holm=1.0000  ns
    opt8: less-only=  0 more-only=  1 (more>less)  p_holm=1.0000  ns

======================================================================
STEP 6  METHOD SWITCHING (Q4.2->Q5.2): Stuart-Maxwell + transitions
======================================================================

stayed on same method: 113/176 (64%)  switched: 63 (36%)
Stuart-Maxwell marginal homogeneity: stat=6.276  df=6  p=0.3930  -> ns

transition matrix (rows=less, cols=more), short labels:
Q5.2     Clear…  Clear…  Delete…  Delete…  Delete…  Privac…  Type…
Q4.2                                                              
Clear…       23       2        0        1        6        1      0
Clear…        1       4        0        0        1        1      0
Delete…       1       0       11        0        5        1      1
Delete…       0       0        0        2        0        0      0
Delete…      13       1        7        0       59        1      3
Privac…       1       0        0        0        1        4      0
Type…         1       1        4        0        8        1     10
```

## DON'T CLEAR THIS
## Interpretation

Statistical tests (stats.md) — what's actually significant

This is the formal test of everything `methods.md` described only descriptively. Short version: **effort** is where the real, tested signal lives; protection and benefit_loss differences across methods don't hold up.

- **Method differences (steps 1-2, Kruskal-Wallis)**: only **effort** differs significantly across methods, in both scenarios (less: H=18.42, p=0.0004; more: H=16.98, p=0.0007). Protection and benefit_loss are all `ns`. 

The protection spread (3.54-3.94) and benefit_loss spread (2.91-3.54) that looked suggestive in the descriptives are not distinguishable from sampling variation at these group sizes, this is a failure to detect a difference, not proof the methods are identical.

Effort does: "Delete this single conversation" is significantly lower-effort than "Delete a specific saved memory or fact" in both scenarios (r=0.60 less, r=0.43 more), and also significantly lower than "Clear all conversation history" in the more-sensitive scenario (r=0.34). That's the one method comparison you can actually stand behind and it makes intuitive sense: hunting down a specific saved memory is felt as more work than deleting one conversation.

- **Scenario effect (steps 3-4, paired)**: raising data sensitivity (less→more) significantly increases perceived **protection** (Wilcoxon, p_holm=0.0018, r=0.38, +0.133 on a 5-pt scale) but has no significant effect on effort or benefit_loss (both ns after Holm). 

Read this as a framing effect: the same deletion action is *felt* as more protective when the underlying data feels more sensitive, even though how burdensome it feels and how much you feel you lose don't move. This is a small-to-medium effect (r≈0.38), not a large one.

  ⚠️ **Protection specifically gets a different answer on each axis — don't conflate them:**
  | question | test | result |
  |---|---|---|
  | Does *which method* someone uses predict their protection rating? | Kruskal-Wallis, steps 1-2 | **ns** (less: p=0.159; more: p=0.911) |
  | Does *scenario sensitivity* (less→more) predict protection rating? | Paired Wilcoxon, steps 3-4 | **SIG** (p_holm=0.0018) |

  So "protection is ns" is only true for the method comparison. 
  
  The correct combined statement is: **method choice doesn't move protection, but scenario sensitivity does.** benefit_loss is the only scale that's ns on *both* axes — it's the one dead end here.


- **Expectation & verification (step 5, McNemar)**: McNemar option 1 (expected "permanently deleted"): 9 people dropped this belief going less→more sensitive, 22 picked it up. Tested alone, that's p=.031 (significant). But it's 1 of 7 options tested together, so Holm correction raises the bar → p_holm=.218 (ns).

Bottom line: the raw signal is real-looking, but correcting for testing 7 options at once means you can't rule out chance. Not "no effect" — just not provable at this sample size.

1. No defensible claim that scenario sensitivity changes what people expect happens to their data, or whether they verify it — none of the 7+8 options survive correction. So you can't say "sensitivity shifts expectations" in the write-up.

2. One lead worth flagging for future work: the "permanently deleted" belief (option 1) had the strongest raw signal (p=.031, 22 people gained this expectation vs. 9 who lost it) — suggestive that more sensitive data makes people assume stronger deletion happens, but underpowered to confirm here. Worth a targeted follow-up study rather than a claim now.

- **Method switching (step 6)**: 64% of respondents pick the *same* method in both scenarios; 36% switch. But the switch isn't a systematic escalation toward heavier methods — Stuart-Maxwell marginal homogeneity is ns (p=0.393), meaning the aggregate distribution of method choice doesn't shift. The transition matrix shows switching in both directions: 13 people moved from "Delete this single conversation" up to "Clear all conversation history" when sensitivity rose (the single largest off-diagonal cell), but 6 moved the opposite way (heavier→lighter), and similar two-way churn shows up elsewhere in the matrix. So there's real individual-level churn (over a third of respondents), just no clean population-level "people escalate under sensitivity" story.

**Bottom line for write-up**: the one clean, tested claim from this whole battery is 

- "deletion method significantly affects perceived effort, and scenario sensitivity significantly affects perceived protection" 

— everything else (protection/benefit_loss by method, effort/benefit_loss by scenario, expectation/verification shifts, systematic method escalation) is not statistically supported at this sample size (bases: less=177, more=178, paired=177 — and considerably smaller once split by method group or discordant pairs), even though some of it looked suggestive in the raw descriptives.


It's not that 177 is small in absolute terms — for a paired test (protection/effort/benefit_loss by scenario) that's a decent sample. The real bottleneck is that several of these tests don't actually use the full 177:

- Method-level tests (Kruskal-Wallis): 177 gets split across 4-7 method groups — some as small as n=2-19. Small groups = low power, regardless of the healthy top-line n.
- McNemar (expectation/verification): only discordant respondents (people who switched their answer) count — for option 1 that was 31 people out of 177, not 177.
- Stuart-Maxwell (switching): a 7×7 table with several near-empty cells (e.g. "Delete my account entirely" n=2) — most of the 177 sits on the diagonal (unchanged) and contributes nothing to the test.

So "not statistically supported at this sample size" really means: the effective sample feeding each specific test is often much smaller than the headline 177, and it's that smaller number — not the survey's overall size — that limits power for those particular claims.
