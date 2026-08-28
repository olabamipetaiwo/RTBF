# contingency_table

_Run at 2026-08-24T13:22:59_

```text
(* = method n < 14; see verify.md for the significance test on this pairing)


======================================================================
POOLED (deduped per respondent, same mechanism as pooling.py) — method x expectation
======================================================================
                     expectation  Delete this single conversation. (n=105)  Clear all conversation history. (n=50)  Delete a specific saved memory or fact. (n=30)  Type a message asking the AI Chatbot to forget it. (n=29)  Clear all saved memories.* (n=11)  Privacy dashboard or account-level data management page.* (n=11)  Delete my account entirely.* (n=3)  Total
permanently deleted (DB+backups)                                      62.0                                    27.0                                            19.5                                                       16.5                                5.0                                                               7.5                                 2.5  140.0
         made invisible / hidden                                      31.0                                    18.0                                             4.0                                                        4.0                                4.5                                                               3.0                                 2.5   67.0
 not referenced in current convo                                      46.0                                    20.5                                            19.0                                                       16.5                                7.5                                                               8.5                                 1.5  119.5
  not referenced in future convo                                      53.5                                    22.5                                            17.5                                                       15.5                                8.5                                                               8.5                                 1.0  127.0
     no longer used for training                                      29.0                                    10.5                                             5.0                                                        9.5                                4.5                                                               6.0                                 2.5   67.0
           not sure what happens                                      11.0                                     4.5                                             1.5                                                        1.5                                0.5                                                               1.5                                 0.0   20.5
                           other                                       0.0                                     1.0                                             0.0                                                        0.0                                0.0                                                               0.5                                 0.0    1.5

saved -> scipy_analysis/outputs/tables/contingency_pooled.csv

----------------------------------------------------------------------
POOLED, % of each method's own n (comparable across methods; raw
counts above scale with method popularity and are not)
----------------------------------------------------------------------
                                                  method   n  permanently deleted (DB+backups)  made invisible / hidden  not referenced in current convo  not referenced in future convo  no longer used for training  not sure what happens  other
                        Delete this single conversation. 105                              59.0                     29.5                             43.8                            51.0                         27.6                   10.5    0.0
                         Clear all conversation history.  50                              54.0                     36.0                             41.0                            45.0                         21.0                    9.0    2.0
                 Delete a specific saved memory or fact.  30                              65.0                     13.3                             63.3                            58.3                         16.7                    5.0    0.0
      Type a message asking the AI Chatbot to forget it.  29                              56.9                     13.8                             56.9                            53.4                         32.8                    5.2    0.0
                               Clear all saved memories.  11                              45.5                     40.9                             68.2                            77.3                         40.9                    4.5    0.0
Privacy dashboard or account-level data management page.  11                              68.2                     27.3                             77.3                            77.3                         54.5                   13.6    4.5
                             Delete my account entirely.   3                              83.3                     83.3                             50.0                            33.3                         83.3                    0.0    0.0

saved -> scipy_analysis/outputs/tables/contingency_pooled_pct.csv

----------------------------------------------------------------------
READING (descriptive)
----------------------------------------------------------------------
No strong tendency overall: 'permanently deleted', 'not referenced in
current convo', and 'not referenced in future convo' are the top 3
expectations for every method, and 'not sure'/'other' stay rare for
every method -- a flat ranking across methods, consistent with
verify.md's finding that no expectation option survives Holm
correction against method in either scenario (less or more).

One pattern flagged above: the heavier-touch methods (Clear all
saved memories, Privacy dashboard, both n=11) run ~25-30pt higher on
'not referenced in future convo' (77% both) than the lighter methods
(single-conversation delete 51%, clear history 45%). Both are below
N_FLOOR=14 and dropped from the significance test below -- see that
test for the 4 methods it can actually speak to.

======================================================================
POOLED significance test (method x expectation, per option)
Same test_family() logic as verify.py (chi2 if all expected>=5 else
Fisher, Holm-corrected within family). Pooled cells rounded to the
nearest int for Fisher's integer requirement. Methods with n<14
dropped first (same floor as everywhere else in this repo):
kept = ['Delete this single conversation.', 'Clear all conversation history.', 'Delete a specific saved memory or fact.', 'Type a message asking the AI Chatbot to forget it.']
======================================================================
                          option   test  p_raw  p_holm  cramers_v sig
permanently deleted (DB+backups)   chi2 0.7091  1.0000      0.080    
         made invisible / hidden   chi2 0.0491  0.3435      0.192    
 not referenced in current convo   chi2 0.1449  0.8695      0.159    
  not referenced in future convo   chi2 0.5420  1.0000      0.100    
     no longer used for training   chi2 0.3176  1.0000      0.128    
           not sure what happens fisher 0.9200  1.0000      0.057    
                           other fisher 0.5051  1.0000      0.124    

saved -> scipy_analysis/outputs/tables/contingency_pooled_sig.csv
```
## finding

No significant association between deletion method and expectation, on the pooled data.

For all 7 expectation options (tested against the 4 methods with n≥14: single-conversation delete, clear all history, delete specific memory, type "forget" message), after Holm correction across the family:

┌─────────────────────────────┬────────┬───────┬────────┬────────────┬─────┐
│           option            │  test  │ p_raw │ p_holm │ Cramér's V │ sig │
├─────────────────────────────┼────────┼───────┼────────┼────────────┼─────┤
│ permanently deleted         │ chi2   │ .709  │ 1.000  │ .080       │     │
├─────────────────────────────┼────────┼───────┼────────┼────────────┼─────┤
│ made invisible / hidden     │ chi2   │ .049  │ .344   │ .192       │     │
├─────────────────────────────┼────────┼───────┼────────┼────────────┼─────┤
│ not ref. current convo      │ chi2   │ .145  │ .870   │ .159       │     │
├─────────────────────────────┼────────┼───────┼────────┼────────────┼─────┤
│ not ref. future convo       │ chi2   │ .542  │ 1.000  │ .100       │     │
├─────────────────────────────┼────────┼───────┼────────┼────────────┼─────┤
│ no longer used for training │ chi2   │ .318  │ 1.000  │ .128       │     │
├─────────────────────────────┼────────┼───────┼────────┼────────────┼─────┤
│ not sure what happens       │ fisher │ .920  │ 1.000  │ .057       │     │
├─────────────────────────────┼────────┼───────┼────────┼────────────┼─────┤
│ other                       │ fisher │ .505  │ 1.000  │ .124       │     │
└─────────────────────────────┴────────┴───────┴────────┴────────────┴─────┘

None survive Holm correction — closest is "made invisible / hidden" (raw p=.049, but Holm p=.344, ns). Effect sizes are all small (Cramér's V ≤ .19).

Bottom line: which deletion method someone picks tells you nothing statistically about what they expect it to do. This matches verify.md's separate less/more-scenario tests, so the finding holds whether you look at each scenario individually or pool them together.