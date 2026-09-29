# pooled_gee

_Run at 2026-09-23T10:29:04_

```text
=== Pooled between-method tests: participant-clustered GEE ===
352 participant-scenario observations from 176 participants (paired base n=177; 'Other' filtered per scenario).
Qualifying methods (>= 14 distinct participants): Delete this single conversation. (ref); Clear all conversation history.; Delete a specific saved memory or fact.; Type a message asking the AI Chatbot to forget it.
Model: outcome ~ method + scenario, clustered on participant, independence working correlation with robust SEs (primary; see module docstring). Wald chi-square on the method coefficients.
p_exch = sensitivity check under an exchangeable working correlation; p_lpm = sensitivity check with a linear-probability (Gaussian) GEE; rho = within-person correlation of the outcome (exchangeable fit).
p_naive = same comparison ignoring clustering (chi-square / Kruskal-Wallis on the observations); shown only to expose the size of the correction.

----------------------------------------------------------------------
DESCRIPTIVE: % of each method's observations selecting each expectation
----------------------------------------------------------------------
                                                  method  n_obs  n_people       flag  permanently deleted  made invisible / hidden  not referenced in current convo  not referenced in future convo  no longer used for training  not sure what happens  other
                        Delete this single conversation.    164       105                            58.5                     29.9                             44.5                            54.3                         28.0                   12.8    0.0
                         Clear all conversation history.     73        50                            52.1                     35.6                             39.7                            42.5                         16.4                    9.6    2.7
                 Delete a specific saved memory or fact.     41        30                            65.9                     12.2                             68.3                            63.4                         19.5                    7.3    0.0
      Type a message asking the AI Chatbot to forget it.     39        29                            64.1                     17.9                             53.8                            51.3                         35.9                    5.1    0.0
                               Clear all saved memories.     15        11 <14 people                 46.7                     33.3                             66.7                            73.3                         40.0                    6.7    0.0
Privacy dashboard or account-level data management page.     15        11 <14 people                 66.7                     33.3                             73.3                            80.0                         53.3                   20.0    6.7
                             Delete my account entirely.      5         3 <14 people                 80.0                     80.0                             40.0                            20.0                         80.0                    0.0    0.0

----------------------------------------------------------------------
DESCRIPTIVE: scale scores per method (observation level)
----------------------------------------------------------------------
                                                  method  n_obs  n_people       flag  protection_mean  protection_median  protection_sd  effort_mean  effort_median  effort_sd  benefit_loss_mean  benefit_loss_median  benefit_loss_sd
                        Delete this single conversation.    164       105                        3.63                3.8           0.88         1.64           1.50       0.76               3.00                 3.00             1.03
                         Clear all conversation history.     73        50                        3.77                4.0           0.87         2.09           2.00       0.97               3.11                 3.33             1.10
                 Delete a specific saved memory or fact.     41        30                        3.65                3.8           0.79         2.49           2.25       1.03               3.46                 3.67             0.88
      Type a message asking the AI Chatbot to forget it.     39        29                        3.86                4.0           0.65         1.74           1.50       0.79               2.91                 3.00             0.95
                               Clear all saved memories.     15        11 <14 people             4.09                4.0           0.54         2.03           1.75       1.10               3.49                 3.67             1.09
Privacy dashboard or account-level data management page.     15        11 <14 people             3.92                4.0           0.89         2.43           3.00       1.32               3.24                 3.33             1.18
                             Delete my account entirely.      5         3 <14 people             4.12                4.2           0.64         3.40           3.25       0.60               3.67                 3.33             0.62

======================================================================
EXPECTATIONS by method, logit GEE, Holm across 7 options (inestimable options enter the family at p=1)
======================================================================
                         option  n_selected   chi2  df  p_raw  p_exch  p_lpm  p_naive  cramers_v    rho                                                   note  p_holm sig
            permanently deleted         186 1.9391 3.0 0.5851  0.3722 0.5754   0.4460      0.092 0.6944                                                         1.0000    
        made invisible / hidden          87 6.2631 3.0 0.0995  0.1694 0.0264   0.0234      0.173 0.5822                                                         0.5969    
not referenced in current convo         151 7.6797 3.0 0.0531  0.1615 0.0290   0.0178      0.178 0.5725                                                         0.3718    
 not referenced in future convo         166 3.6958 3.0 0.2962  0.7317 0.2722   0.1624      0.127 0.6142                                                         1.0000    
    no longer used for training          80 5.2719 3.0 0.1529  0.3940 0.1249   0.0805      0.146 0.6250                                                         0.7647    
          not sure what happens          33 2.0646 3.0 0.5591  0.4513 0.4544   0.4491      0.091 0.5955                                                         1.0000    
                          other           2    NaN NaN    NaN     NaN 0.7930   0.0811      0.146 1.0607 logit not estimable (a method has 0 or all selections)  1.0000    

======================================================================
SCALES by method, Gaussian GEE, Holm across 3 scales
======================================================================
       scale    chi2  df  p_raw  p_exch  p_naive    rho note  p_holm sig
  protection  3.7066   3 0.2949  0.2471   0.2496 0.8574       0.2949    
      effort 23.0522   3 0.0000  0.0046   0.0000 0.8176       0.0001   *
benefit_loss  6.9397   3 0.0738  0.2801   0.0503 0.7245       0.1477    

Pairwise contrasts for effort (lower = less effort); diff = a minus b, adjusted for scenario, Holm within the 6 pairs:
                                      a                                                  b    diff  ci_low  ci_high  p_raw  p_holm
       Delete this single conversation.                    Clear all conversation history. -0.4503 -0.7624  -0.1382 0.0047  0.0187
       Delete this single conversation.            Delete a specific saved memory or fact. -0.8515 -1.2477  -0.4553 0.0000  0.0002
       Delete this single conversation. Type a message asking the AI Chatbot to forget it. -0.0979 -0.3868   0.1910 0.5064  0.5064
        Clear all conversation history.            Delete a specific saved memory or fact. -0.4012 -0.8729   0.0705 0.0955  0.2385
        Clear all conversation history. Type a message asking the AI Chatbot to forget it.  0.3524 -0.0414   0.7461 0.0795  0.2385
Delete a specific saved memory or fact. Type a message asking the AI Chatbot to forget it.  0.7536  0.2871   1.2201 0.0015  0.0077

saved -> outputs/tables/pooled_obs_*.csv, pooled_gee_*.csv
```

## DON'T CLEAR THIS
## Interpretation

Pooled between-method analyses (`pooled_gee.md`), added 2026-09-23 for paper review item N4
(reviewer: "pooled expectation analysis is not statistically defensible"). Replaces the pooled
Kruskal-Wallis / Dunn / Fisher analyses in `scipy_analysis/pooling.py`, `crowning.py` (scope A) and
`contingency_table.py`. The paper's pooled numbers now come from this file.

**Why the old pooling was replaced.** Stayers (same method in both scenarios) were averaged into
one 0/0.5/1 (or half-step Likert) value; switchers sat un-averaged in two method groups. So (1) the
method groups shared participants, which KW and Fisher both assume they do not, and Holm cannot fix
that; (2) averaged and un-averaged values were mixed in one column; (3) 0.5-weighted sums were
rounded to integers to feed Fisher's exact test. Fix: 352 participant-scenario observations
(176 participants x 2), participant-clustered GEE, robust SEs. Everything pooled (percentages,
means, medians, the figure's pooled bars) uses the same 352 observations.

**Decisions (and why):**

- **Independence working correlation is primary; exchangeable is a sensitivity check.** Method
  varies within a participant (switchers), so it is a time-varying covariate, and a non-independence
  working correlation is consistent only under the "full covariate conditional mean" assumption
  (Pepe & Anderson 1994), which is implausible here. Found empirically, not just in theory: with
  the within-person correlation near 0.8 for effort (rho=0.82), an exchangeable fit shrank the
  effort contrasts to about half the raw group differences (single vs clear history -0.25 vs -0.45),
  i.e. it estimated a within-person blend, not the between-group comparison the paper reports.
  The independence fit's contrasts match the raw group means and the participant-cluster bootstrap
  (`pooled_gee_crosscheck.md`: -0.450 vs -0.447, -0.852 vs -0.849, -0.098 vs -0.100). This choice
  was made after seeing the exchangeable estimates disagree with the bootstrap, on estimand
  grounds, not to move a p-value: the exchangeable omnibus results reach the same conclusions
  (effort p=.0046, protection .25, benefit loss .28, no expectation option significant).
- **N_FLOOR=14 counts distinct participants, not observations.** Counting observations lets
  "Clear all saved memories" and "Privacy dashboard" (15 obs, 11 people each) through, because
  stayers count twice. Distinct participants reproduces the paper's four qualifying methods.
- **"Other" (expectation option 7) is not estimable.** Selected twice in total, both times under
  one method, so the logit has a zero cell. It enters the Holm family at p=1, the same convention as
  `verify.py`'s "skip(0 sel)". Reported descriptively only.
- **Scenario is a covariate.** Scenario shifts several outcomes and is confounded with order
  (paper Limitations), so the method test is not driven by the scenario shift.
- **p_naive is shown but is not a valid test.** It ignores clustering (chi-square / KW over 352
  observations) and exists to show the size of the correction: it would have put "made invisible"
  and "not referenced (current)" at p=.023 and .018; the clustered tests give .10 and .053.

**What changed in the results (legacy pooled analysis -> participant-clustered GEE):**

| quantity | legacy | now |
|---|---|---|
| effort, omnibus | KW H=19.54, p=.0002 | Wald chi2(3)=23.05, p_holm=.0001 |
| protection, omnibus | KW H=2.41, p=.49 | chi2(3)=3.71, p_holm=.29 |
| benefit loss, omnibus | KW H=4.49, p=.21 | chi2(3)=6.94, p=.074, p_holm=.15 |
| single vs specific memory (effort) | Dunn p_holm=.0002 | -0.85 [-1.25,-0.46], p_holm=.0002 |
| single vs clear history (effort) | Dunn p_holm=.0509, ns | -0.45 [-0.76,-0.14], p_holm=.019 |
| specific memory vs forget (effort) | not reported | +0.75 [+0.29,+1.22], p_holm=.008 |
| expectations by method | closest p=.049 (p_holm=.344) | closest p=.053 (p_holm=.37); none significant |
| means: effort single / specific | 1.68 / 2.45 | 1.64 / 2.49 |

**The one conclusion that moved:** single conversation vs clear history on effort. It was "not
distinguishable" (p_holm=.051, borderline) and is now significant (p_holm=.019, borderline the
other way). It is NOT significant within either scenario alone (Dunn, less and more), so it rests on
the pooled analysis only; the paper says so. Different tests (mean-based Wald vs rank-based Dunn) can
land on either side of .05 for a borderline effect; the CI [-0.76,-0.14] is the better summary.

**Independent check.** The scipy-only pipeline has no GEE, so `pooled_gee_crosscheck.md` checks it
with a random-intercept mixed model (agrees: protection ns, effort p=.0001, benefit loss ns) and a
participant-cluster bootstrap (matches the contrasts to within 0.01).

**Not done / caveats.** Legacy `scipy_analysis/` pooled modules are kept (with notes) but their
outputs are stale; `scipy_analysis/global_correction.py` still registers the legacy pooled KW
p-values under "crowning.pooled". GEE robust SEs with 176 clusters are fine for these sizes; the
smallest qualifying method has 29 participants, so method-specific contrasts involving it are wider.
