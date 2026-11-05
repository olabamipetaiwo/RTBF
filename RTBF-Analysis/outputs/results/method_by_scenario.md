# method_by_scenario

_Run at 2026-11-04T03:33:09_

```text
=== Method x scenario interaction on protection, effort and benefit loss ===
317 responses from 165 participants; methods with >= 14 distinct participants: Delete this single conversation. (105); Clear all conversation history. (50); Delete a specific saved memory or fact. (30); Type a message asking the AI Chatbot to forget it. (29)
Model: scale ~ method * scenario, Gaussian GEE clustered on participant, independence working correlation, robust SEs. Joint Wald chi-square on the 3 interaction terms, Holm across the 3 scales.
Reference levels: first method listed above, scenario = less sensitive (LS).

----------------------------------------------------------------------
CHECK: paper's between-method test (no interaction) reproduces
----------------------------------------------------------------------
protection: method Wald chi2(3) = 3.71, p = 0.2949
effort: method Wald chi2(3) = 23.05, p = 0.0000
benefit_loss: method Wald chi2(3) = 6.94, p = 0.0738

======================================================================
PROTECTION
======================================================================
Means by method (LS, MS, Pooled) and responses per cell:
                                            method  Pooled     LS     MS  MS-LS  n_LS  n_MS  people
                  Delete this single conversation.  3.6293 3.5357 3.7275 0.1918    84    80     105
                   Clear all conversation history.  3.7726 3.7697 3.7750 0.0053    33    40      50
           Delete a specific saved memory or fact.  3.6488 3.5789 3.7091 0.1301    19    22      30
Type a message asking the AI Chatbot to forget it.  3.8564 3.8400 3.8857 0.0457    25    14      29

MS minus LS within each method (GEE contrasts from the interaction model, Holm across the 4 methods):
                                            method  diff_MS_minus_LS     se  p_raw  p_holm sig
                  Delete this single conversation.            0.1918 0.0733 0.0089  0.0357   *
                   Clear all conversation history.            0.0053 0.1228 0.9656  1.0000    
           Delete a specific saved memory or fact.            0.1301 0.2243 0.5618  1.0000    
Type a message asking the AI Chatbot to forget it.            0.0457 0.1926 0.8123  1.0000    

======================================================================
EFFORT
======================================================================
Means by method (LS, MS, Pooled) and responses per cell:
                                            method  Pooled     LS     MS   MS-LS  n_LS  n_MS  people
                  Delete this single conversation.  1.6433 1.6220 1.6656  0.0436    84    80     105
                   Clear all conversation history.  2.0925 1.9848 2.1812  0.1964    33    40      50
           Delete a specific saved memory or fact.  2.4939 2.6974 2.3182 -0.3792    19    22      30
Type a message asking the AI Chatbot to forget it.  1.7436 1.8600 1.5357 -0.3243    25    14      29

MS minus LS within each method (GEE contrasts from the interaction model, Holm across the 4 methods):
                                            method  diff_MS_minus_LS     se  p_raw  p_holm sig
                  Delete this single conversation.            0.0436 0.0795 0.5835  0.5835    
                   Clear all conversation history.            0.1964 0.1351 0.1460  0.2946    
           Delete a specific saved memory or fact.           -0.3792 0.2293 0.0982  0.2946    
Type a message asking the AI Chatbot to forget it.           -0.3243 0.1740 0.0624  0.2497    

======================================================================
BENEFIT_LOSS
======================================================================
Means by method (LS, MS, Pooled) and responses per cell:
                                            method  Pooled     LS     MS   MS-LS  n_LS  n_MS  people
                  Delete this single conversation.  2.9959 2.9683 3.0250  0.0567    84    80     105
                   Clear all conversation history.  3.1050 3.0606 3.1417  0.0811    33    40      50
           Delete a specific saved memory or fact.  3.4553 3.5439 3.3788 -0.1651    19    22      30
Type a message asking the AI Chatbot to forget it.  2.9060 2.9067 2.9048 -0.0019    25    14      29

MS minus LS within each method (GEE contrasts from the interaction model, Holm across the 4 methods):
                                            method  diff_MS_minus_LS     se  p_raw  p_holm sig
                  Delete this single conversation.            0.0567 0.1216 0.6407     1.0    
                   Clear all conversation history.            0.0811 0.1902 0.6699     1.0    
           Delete a specific saved memory or fact.           -0.1651 0.1850 0.3722     1.0    
Type a message asking the AI Chatbot to forget it.           -0.0019 0.2516 0.9940     1.0    

======================================================================
INTERACTION TESTS (joint Wald, df = 3), Holm across the 3 scales
======================================================================
       scale   chi2  df  p_raw  p_exch  p_art note  p_holm sig
  protection 1.3934   3 0.7071  0.7773 0.5168       1.0000    
      effort 8.1097   3 0.0438  0.0972 0.2312       0.1314    
benefit_loss 1.2163   3 0.7491  0.7271 0.8238       1.0000    

p_exch = exchangeable working correlation; p_art = aligned rank transform (GEE on ranks). Both are robustness checks and are not Holm-adjusted.

saved -> outputs/tables/method_by_scenario_*.csv
```
