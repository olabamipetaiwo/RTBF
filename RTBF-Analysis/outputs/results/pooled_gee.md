# pooled_gee

_Run at 2026-11-11T01:44:02_

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

======================================================================
FULL COEFFICIENTS of every primary GEE (reference: first method listed above, scenario = less); robust SEs; OR = exp(beta) for logit models
======================================================================
                        outcome    model                                                            term    beta  se_robust       z  p_raw  ci_low  ci_high  odds_ratio  or_ci_low  or_ci_high  omnibus_chi2  omnibus_df  omnibus_p  n_obs  n_clusters  converged
            permanently deleted    logit                                                       Intercept  0.2193     0.2060  1.0644 0.2872 -0.1845   0.6231      1.2452     0.8315      1.8647        1.9391           3     0.5851    317         165       True
            permanently deleted    logit                    C(method)[T.Clear all conversation history.] -0.2794     0.3425 -0.8158 0.4146 -0.9506   0.3918      0.7562     0.3865      1.4797        1.9391           3     0.5851    317         165       True
            permanently deleted    logit            C(method)[T.Delete a specific saved memory or fact.]  0.3004     0.4383  0.6855 0.4930 -0.5586   1.1594      1.3505     0.5720      3.1881        1.9391           3     0.5851    317         165       True
            permanently deleted    logit C(method)[T.Type a message asking the AI Chatbot to forget it.]  0.2693     0.4147  0.6495 0.5160 -0.5434   1.0821      1.3091     0.5807      2.9509        1.9391           3     0.5851    317         165       True
            permanently deleted    logit                                             C(scenario)[T.more]  0.2604     0.1394  1.8673 0.0619 -0.0129   0.5337      1.2974     0.9872      1.7051        1.9391           3     0.5851    317         165       True
        made invisible / hidden    logit                                                       Intercept -0.9402     0.2185 -4.3027 0.0000 -1.3685  -0.5119      0.3906     0.2545      0.5993        6.2631           3     0.0995    317         165       True
        made invisible / hidden    logit                    C(method)[T.Clear all conversation history.]  0.2510     0.3500  0.7170 0.4734 -0.4351   0.9370      1.2853     0.6472      2.5523        6.2631           3     0.0995    317         165       True
        made invisible / hidden    logit            C(method)[T.Delete a specific saved memory or fact.] -1.1309     0.6058 -1.8667 0.0619 -2.3182   0.0565      0.3228     0.0985      1.0581        6.2631           3     0.0995    317         165       True
        made invisible / hidden    logit C(method)[T.Type a message asking the AI Chatbot to forget it.] -0.6449     0.5424 -1.1890 0.2344 -1.7079   0.4181      0.5247     0.1813      1.5191        6.2631           3     0.0995    317         165       True
        made invisible / hidden    logit                                             C(scenario)[T.more]  0.1753     0.1801  0.9736 0.3303 -0.1777   0.5284      1.1917     0.8372      1.6962        6.2631           3     0.0995    317         165       True
not referenced in current convo    logit                                                       Intercept -0.0394     0.2024 -0.1948 0.8456 -0.4362   0.3574      0.9613     0.6465      1.4295        7.6797           3     0.0531    317         165       True
not referenced in current convo    logit                    C(method)[T.Clear all conversation history.] -0.1755     0.3348 -0.5241 0.6002 -0.8317   0.4807      0.8391     0.4353      1.6172        7.6797           3     0.0531    317         165       True
not referenced in current convo    logit            C(method)[T.Delete a specific saved memory or fact.]  1.0144     0.4148  2.4454 0.0145  0.2014   1.8274      2.7576     1.2231      6.2175        7.6797           3     0.0531    317         165       True
not referenced in current convo    logit C(method)[T.Type a message asking the AI Chatbot to forget it.]  0.3292     0.3975  0.8281 0.4076 -0.4499   1.1082      1.3898     0.6377      3.0290        7.6797           3     0.0531    317         165       True
not referenced in current convo    logit                                             C(scenario)[T.more] -0.3750     0.1630 -2.3002 0.0214 -0.6945  -0.0555      0.6873     0.4993      0.9460        7.6797           3     0.0531    317         165       True
 not referenced in future convo    logit                                                       Intercept  0.2101     0.2077  1.0117 0.3117 -0.1970   0.6172      1.2339     0.8212      1.8538        3.6958           3     0.2962    317         165       True
 not referenced in future convo    logit                    C(method)[T.Clear all conversation history.] -0.4702     0.3418 -1.3757 0.1689 -1.1401   0.1997      0.6249     0.3198      1.2210        3.6958           3     0.2962    317         165       True
 not referenced in future convo    logit            C(method)[T.Delete a specific saved memory or fact.]  0.3829     0.4302  0.8901 0.3734 -0.4603   1.2262      1.4666     0.6311      3.4081        3.6958           3     0.2962    317         165       True
 not referenced in future convo    logit C(method)[T.Type a message asking the AI Chatbot to forget it.] -0.1302     0.4272 -0.3048 0.7605 -0.9674   0.7071      0.8779     0.3801      2.0280        3.6958           3     0.2962    317         165       True
 not referenced in future convo    logit                                             C(scenario)[T.more] -0.0798     0.1557 -0.5124 0.6084 -0.3850   0.2254      0.9233     0.6804      1.2529        3.6958           3     0.2962    317         165       True
    no longer used for training    logit                                                       Intercept -1.0343     0.2364 -4.3747 0.0000 -1.4976  -0.5709      0.3555     0.2237      0.5650        5.2719           3     0.1529    317         165       True
    no longer used for training    logit                    C(method)[T.Clear all conversation history.] -0.6960     0.4005 -1.7378 0.0822 -1.4810   0.0890      0.4986     0.2274      1.0930        5.2719           3     0.1529    317         165       True
    no longer used for training    logit            C(method)[T.Delete a specific saved memory or fact.] -0.4848     0.4609 -1.0519 0.2929 -1.3881   0.4185      0.6158     0.2496      1.5197        5.2719           3     0.1529    317         165       True
    no longer used for training    logit C(method)[T.Type a message asking the AI Chatbot to forget it.]  0.3869     0.4595  0.8420 0.3998 -0.5137   1.2874      1.4724     0.5983      3.6235        5.2719           3     0.1529    317         165       True
    no longer used for training    logit                                             C(scenario)[T.more]  0.1852     0.1702  1.0878 0.2767 -0.1485   0.5188      1.2034     0.8620      1.6801        5.2719           3     0.1529    317         165       True
          not sure what happens    logit                                                       Intercept -1.9587     0.3347 -5.8518 0.0000 -2.6148  -1.3027      0.1410     0.0732      0.2718        2.0646           3     0.5591    317         165       True
          not sure what happens    logit                    C(method)[T.Clear all conversation history.] -0.3304     0.5715 -0.5781 0.5632 -1.4505   0.7898      0.7187     0.2344      2.2029        2.0646           3     0.5591    317         165       True
          not sure what happens    logit            C(method)[T.Delete a specific saved memory or fact.] -0.6247     0.8113 -0.7700 0.4413 -2.2149   0.9655      0.5354     0.1092      2.6261        2.0646           3     0.5591    317         165       True
          not sure what happens    logit C(method)[T.Type a message asking the AI Chatbot to forget it.] -0.9890     0.7787 -1.2701 0.2040 -2.5152   0.5372      0.3719     0.0808      1.7112        2.0646           3     0.5591    317         165       True
          not sure what happens    logit                                             C(scenario)[T.more]  0.0815     0.2460  0.3314 0.7403 -0.4007   0.5638      1.0850     0.6699      1.7573        2.0646           3     0.5591    317         165       True
                     protection gaussian                                                       Intercept  3.5688     0.0899 39.7146 0.0000  3.3927   3.7450         NaN        NaN         NaN        3.7066           3     0.2949    317         165       True
                     protection gaussian                    C(method)[T.Clear all conversation history.]  0.1359     0.1524  0.8916 0.3726 -0.1628   0.4346         NaN        NaN         NaN        3.7066           3     0.2949    317         165       True
                     protection gaussian            C(method)[T.Delete a specific saved memory or fact.]  0.0135     0.1584  0.0850 0.9323 -0.2971   0.3240         NaN        NaN         NaN        3.7066           3     0.2949    317         165       True
                     protection gaussian C(method)[T.Type a message asking the AI Chatbot to forget it.]  0.2431     0.1429  1.7011 0.0889 -0.0370   0.5232         NaN        NaN         NaN        3.7066           3     0.2949    317         165       True
                     protection gaussian                                             C(scenario)[T.more]  0.1239     0.0463  2.6783 0.0074  0.0332   0.2146         NaN        NaN         NaN        3.7066           3     0.2949    317         165       True
                         effort gaussian                                                       Intercept  1.6523     0.0748 22.0975 0.0000  1.5057   1.7988         NaN        NaN         NaN       23.0522           3     0.0000    317         165       True
                         effort gaussian                    C(method)[T.Clear all conversation history.]  0.4503     0.1592  2.8279 0.0047  0.1382   0.7624         NaN        NaN         NaN       23.0522           3     0.0000    317         165       True
                         effort gaussian            C(method)[T.Delete a specific saved memory or fact.]  0.8515     0.2022  4.2119 0.0000  0.4553   1.2477         NaN        NaN         NaN       23.0522           3     0.0000    317         165       True
                         effort gaussian C(method)[T.Type a message asking the AI Chatbot to forget it.]  0.0979     0.1474  0.6644 0.5064 -0.1910   0.3868         NaN        NaN         NaN       23.0522           3     0.0000    317         165       True
                         effort gaussian                                             C(scenario)[T.more] -0.0184     0.0491 -0.3743 0.7082 -0.1146   0.0779         NaN        NaN         NaN       23.0522           3     0.0000    317         165       True
                   benefit_loss gaussian                                                       Intercept  2.9829     0.1018 29.2989 0.0000  2.7834   3.1824         NaN        NaN         NaN        6.9397           3     0.0738    317         165       True
                   benefit_loss gaussian                    C(method)[T.Clear all conversation history.]  0.1075     0.1713  0.6274 0.5304 -0.2283   0.4433         NaN        NaN         NaN        6.9397           3     0.0738    317         165       True
                   benefit_loss gaussian            C(method)[T.Delete a specific saved memory or fact.]  0.4580     0.1910  2.3976 0.0165  0.0836   0.8325         NaN        NaN         NaN        6.9397           3     0.0738    317         165       True
                   benefit_loss gaussian C(method)[T.Type a message asking the AI Chatbot to forget it.] -0.0865     0.1925 -0.4494 0.6532 -0.4638   0.2908         NaN        NaN         NaN        6.9397           3     0.0738    317         165       True
                   benefit_loss gaussian                                             C(scenario)[T.more]  0.0267     0.0677  0.3946 0.6931 -0.1060   0.1595         NaN        NaN         NaN        6.9397           3     0.0738    317         165       True

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
