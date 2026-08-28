# stats

_Run at 2026-08-07T14:24:08_

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
    p_raw=0.4854  p_holm=0.5935  -> ns

[benefit_loss] shapiro_normal=False  Wilcoxon  stat=1999.5  r=0.123  mean_diff=+0.043 (more>less)
    p_raw=0.2968  p_holm=0.5935  -> ns

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
