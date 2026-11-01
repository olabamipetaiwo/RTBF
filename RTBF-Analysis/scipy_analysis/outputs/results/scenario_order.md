# scenario_order

_Run at 2026-10-20T01:29:19_

```text
=== Scenario order check (LS = weather, MS = health) ===

1. Split (n=177 of 177 paired; order missing for 0)
   LS first: 83   MS first: 94
   binomial test vs 50/50: p=0.4524  -> even

2. Scenario shift (MS - LS) by order: Mann-Whitney U, Holm x4
   [willingness] mean shift LS-first=+0.349 (n=83)  MS-first=+0.426 (n=94)
       U=3967.5  r=-0.017  p_raw=0.8317  p_holm=1.0000  -> ns
   [protection] mean shift LS-first=+0.159 (n=83)  MS-first=+0.111 (n=94)
       U=4110.0  r=-0.054  p_raw=0.5259  p_holm=1.0000  -> ns
   [effort] mean shift LS-first=+0.030 (n=83)  MS-first=+0.035 (n=94)
       U=3566.5  r=0.086  p_raw=0.2915  p_holm=1.0000  -> ns
   [benefit_loss] mean shift LS-first=+0.068 (n=83)  MS-first=+0.021 (n=94)
       U=3844.5  r=0.014  p_raw=0.8622  p_holm=1.0000  -> ns

3. Changed method between scenarios, by order: Fisher's exact
   LS first: switched 33/83 (39.8%)
   MS first: switched 30/94 (31.9%)
   odds ratio=0.710  p=0.3454  -> ns

As reported in the paper (Methods, Missingness and aggregation):
   83 LS first, 94 MS first; binomial p=.45
   shift by order: all p_Holm=1.00 (lowest 1.00)
   changed method by order: Fisher's exact p=.35
```
