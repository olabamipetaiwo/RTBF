# crowning

_Run at 2026-08-11T04:14:42_

```text

======================================================================
SCOPE A -- POOLED (both scenarios, task 2 dedup)
======================================================================

[pooled | protection] (higher=better)  KW H=2.41 p=0.4923 eps2=-0.003  n_methods=4
    Clear all conversati=3.798
    Type a message askin=3.786
    Delete this single c=3.659
    Delete a specific sa=3.650
    -> ns: no method is statistically distinguishable from the others

[pooled | effort] (lower=better)  KW H=19.54 p=0.0002 eps2=0.079  n_methods=4
    Delete this single c=1.679
    Type a message askin=1.793
    Clear all conversati=2.042
    Delete a specific sa=2.446
    -> PARTIAL: 'Delete this single conversation' has the best point estimate but doesn't beat everyone -- not a clean winner
       * significantly beats Delete a specific saved memory p_holm=0.0002 r=0.483
       * NOT distinguishable from Clear all conversation history p_holm=0.0509 r=0.254
       * NOT distinguishable from Type a message asking the AI C p_holm=0.6272 r=0.107

[pooled | benefit_loss] (lower=better)  KW H=4.49 p=0.2136 eps2=0.007  n_methods=4
    Type a message askin=2.994
    Delete this single c=3.011
    Clear all conversati=3.107
    Delete a specific sa=3.433
    -> ns: no method is statistically distinguishable from the others

======================================================================
SCOPE B -- LESS SCENARIO (recomputed for crowning synthesis; omnibus p already in stats.md, not re-registered)
======================================================================

[less | protection] (higher=better)  KW H=5.18 p=0.1593 eps2=0.014  n_methods=4
    Type a message askin=3.840
    Clear all conversati=3.770
    Delete a specific sa=3.579
    Delete this single c=3.536
    -> ns: no method is statistically distinguishable from the others

[less | effort] (lower=better)  KW H=18.42 p=0.0004 eps2=0.098  n_methods=4
    Delete this single c=1.622
    Type a message askin=1.860
    Clear all conversati=1.985
    Delete a specific sa=2.697
    -> PARTIAL: 'Delete this single conversation' has the best point estimate but doesn't beat everyone -- not a clean winner
       * significantly beats Delete a specific saved memory p_holm=0.0002 r=0.597
       * NOT distinguishable from Clear all conversation history p_holm=0.1922 r=0.219
       * NOT distinguishable from Type a message asking the AI C p_holm=0.4070 r=0.163

[less | benefit_loss] (lower=better)  KW H=5.29 p=0.1515 eps2=0.015  n_methods=4
    Type a message askin=2.907
    Delete this single c=2.968
    Clear all conversati=3.061
    Delete a specific sa=3.544
    -> ns: no method is statistically distinguishable from the others

======================================================================
SCOPE B -- MORE SCENARIO (recomputed for crowning synthesis; omnibus p already in stats.md, not re-registered)
======================================================================

[more | protection] (higher=better)  KW H=0.54 p=0.9106 eps2=-0.016  n_methods=4
    Type a message askin=3.886
    Clear all conversati=3.775
    Delete this single c=3.728
    Delete a specific sa=3.709
    -> ns: no method is statistically distinguishable from the others

[more | effort] (lower=better)  KW H=16.98 p=0.0007 eps2=0.092  n_methods=4
    Type a message askin=1.536
    Delete this single c=1.666
    Clear all conversati=2.181
    Delete a specific sa=2.318
    -> PARTIAL: 'Type a message asking the AI Chatbot' has the best point estimate but doesn't beat everyone -- not a clean winner
       * NOT distinguishable from Delete this single conversation p_holm=1.0000 r=-0.006
       * NOT distinguishable from Clear all conversation history p_holm=0.1334 r=0.379
       * NOT distinguishable from Delete a specific saved memory p_holm=0.0781 r=0.484

[more | benefit_loss] (lower=better)  KW H=2.89 p=0.4088 eps2=-0.001  n_methods=4
    Type a message askin=2.905
    Delete this single c=3.025
    Clear all conversati=3.142
    Delete a specific sa=3.379
    -> ns: no method is statistically distinguishable from the others
```

TASk - we dont want to report number, create a chart for pooled
## DON'T CLEAR THIS
## Interpretation

ns = not significant -> It means the Kruskal-Wallis omnibus test's p-value came back ≥ .05 

**Bottom line**: no method is ever fully crowned on any scale, in any scope. The
strongest statement this data supports: **"delete this single conversation" is reliably
lower-effort than "delete a specific saved memory," everywhere — but no method is the
single best at anything.**

- **Protection and benefit_loss: `ns` everywhere** (pooled, less, more — 6/6 tests null).
  Pooling roughly doubled n for the smaller methods (task 2), which could plausibly have
  tipped these into significance — it didn't. No method differs from any other on how
  protective it feels or how much it feels like giving something up.

- **Effort is the only scale with a real signal, but it caps out at `PARTIAL`, never
  `CROWNED`.** "Delete this single conversation" has the best (lowest) mean effort in
  pooled and less-scenario, and clears only one hurdle each time — significantly beating
  "delete a specific saved memory" (p_holm=.0002 both places) — while staying
  statistically indistinguishable from "clear all conversation history" and "type a
  message." Pooled comes closest to a second win (vs. clear-history, p_holm=.051) without
  crossing .05.

- **More-scenario effort flips the point estimate**, and it matters: "type a message
  asking the AI Chatbot to forget it" has the lowest raw mean (1.536, vs. 1.666 for
  "delete this single conversation") — but it doesn't significantly beat any of the other
  3 methods (closest: vs. delete-specific-memory, p_holm=.078). The existing narrative
  elsewhere in this study only ever discusses "delete this single conversation" as the
  effort leader; that's true in 2 of 3 scopes but not the more-sensitive one specifically.

- **Takeaway for the write-up**: report effort as "delete this single conversation is
  significantly lower-effort than delete-a-specific-memory, holds in every scope tested —
  but is not distinguishable from clear-all-history or type-a-message, so it can't be
  called the single lowest-effort method." Protection and benefit_loss get no method-level
  claim at all.


  The survey has 7 deletion methods total, but only methods with n ≥ 14 respondents get included in these tests (N_FLOOR = 14, used consistently throughout this whole study) — too few responses and a group comparison isn't trustworthy.

Of the 7, only 4 clear that bar in every scope:

┌──────────────────────────────────────┬────────┬────────┬──────────┐
│                method                │ n_less │ n_more │ n_pooled │
├──────────────────────────────────────┼────────┼────────┼──────────┤
│ Delete this single conversation      │ 84     │ 81     │ 105      │
├──────────────────────────────────────┼────────┼────────┼──────────┤
│ Clear all conversation history       │ 33     │ 40     │ 50       │
├──────────────────────────────────────┼────────┼────────┼──────────┤
│ Delete a specific saved memory       │ 19     │ 22     │ 30       │
├──────────────────────────────────────┼────────┼────────┼──────────┤
│ Type a message asking the AI Chatbot │ 25     │ 14     │ 29       │
└──────────────────────────────────────┴────────┴────────┴──────────┘

The other 3 never reach 14 in any scope, so they're excluded everywhere:

┌──────────────────────────────────┬────────┬────────┬──────────┐
│              method              │ n_less │ n_more │ n_pooled │
├──────────────────────────────────┼────────┼────────┼──────────┤
│ Clear all saved memories         │ 7      │ 8      │ 11       │
├──────────────────────────────────┼────────┼────────┼──────────┤
│ Privacy dashboard / account page │ 6      │ 9      │ 11       │
├──────────────────────────────────┼────────┼────────┼──────────┤
│ Delete my account entirely       │ 2      │ 3      │ 3        │
└──────────────────────────────────┴────────┴────────┴──────────┘

How did we pool it -> Per respondent: same method both scenarios → average the two ratings into one observation; different method per scenario → keep both ratings separately, one point in each method's group.

Say three respondents rated "effort" (1-5 scale) in both scenarios:

- Person A: used "Delete this single conversation" in both scenarios. Rated effort 1 in the less-sensitive one, 2 in the more-sensitive one.
- Person B: used "Delete this single conversation" in less-sensitive, but switched to "Clear all conversation history" in more-sensitive.
- Person C: used "Clear all conversation history" in both scenarios. Rated it 3 both times.

Why we can't just dump all 6 ratings into their methods' groups: Person A would show up twice in "Delete this single conversation"'s group (1 and 2) — that's really just one person's opinion counted as if it were two people. Person C the same for "Clear history" (3 and 3). That inflates the group sizes with duplicated opinions, which breaks the statistical test's assumption that every data point is an independent person.

What we actually did:
- Person A (same method twice) → average their two ratings: (1+2)/2 = 1.5. One number, one person, goes into "Delete this single conversation"'s group.
- Person B (switched methods) → their less-sensitive rating is genuinely about "Delete this single conversation," their more-sensitive rating is genuinely about "Clear all conversation history" — two different things being rated, so both stay, one point each, in the correct method's group. Nothing's duplicated because each rating is describing a different method.
- Person C (same method twice) → averaged like Person A: (3+3)/2 = 3. One point in "Clear history"'s group.

End result: "Delete this single conversation" gets [1.5 (from A), 1 (from B's less-scenario)] = 2 points. "Clear all conversation history" gets [2 (from B's more-scenario), 3 (from C)] = 2 points. Every person contributes exactly one point to any single method's group — no one's opinion got counted twice for the same method.


Paraemeters 

- KW — the test name (Kruskal-Wallis): compares 4+ groups to check if any differ.
- H — how different the groups look from each other (bigger = more different).
- p — how likely that difference is just chance (small = probably real).
- eps2 — how big the difference actually is, not just whether it's real.


- KW — Kruskal-Wallis test. The non-parametric equivalent of one-way ANOVA — compares 3+ independent groups (here, the 4 methods) to see if their distributions differ. Non-parametric (rank-based) because these Likert scales aren't normally distributed, same reason Spearman was used over Pearson earlier.
- H = 2.41 — the test statistic. Computed by ranking all protection scores together (regardless of method), then checking whether the ranks are unevenly distributed across the 4 method groups. If all methods were identical, you'd expect ranks spread evenly; H measures how far from that "evenly spread" expectation the data actually is. Bigger H = groups look more different from each other.
- p = 0.4923 — the p-value for that H, using a chi-square distribution. Answers: "if the 4 methods truly had identical protection ratings, how likely is it you'd see groups looking this different (or more) by chance?" 49% — very likely by chance alone. That's why it's ns.
- eps2 = -0.003 (epsilon-squared) — the effect size, Kruskal-Wallis's analogue to R². Roughly: what fraction of the variation in ranks is "explained" by which method someone used. Ranges 0 to 1 in theory; slightly negative here just because H (2.41) landed below what you'd expect at random with this many groups/observations — essentially confirms the same thing as the p-value: there's nothing here. For comparison, effort's pooled test (line 18) has eps2=0.079, meaningfully positive, matching its actual significant result.