# fig9_pooled_cost_benefit

_Run at 2026-08-25T23:45:10_

```text

===== POOLED (both scenarios) =====
                                                  method   n  protection_mean  protection_median  protection_sd  effort_mean  effort_median  effort_sd  benefit_loss_mean  benefit_loss_median  benefit_loss_sd flag
                        Delete this single conversation. 105             3.66                3.8           0.85         1.68          1.625       0.78               3.01             3.000000             0.97     
                         Clear all conversation history.  50             3.80                4.0           0.84         2.04          2.000       0.92               3.11             3.333333             1.12     
                 Delete a specific saved memory or fact.  30             3.65                3.8           0.66         2.45          2.250       1.01               3.43             3.666667             0.86     
      Type a message asking the AI Chatbot to forget it.  29             3.79                4.0           0.64         1.79          1.750       0.83               2.99             3.000000             0.99     
                               Clear all saved memories.  11             4.05                4.0           0.48         2.14          2.000       1.08               3.32             3.666667             1.13 n<14
Privacy dashboard or account-level data management page.  11             3.97                4.0           0.76         2.62          3.000       1.38               3.35             3.666667             1.07 n<14
                             Delete my account entirely.   3             4.17                4.4           0.59         3.33          3.500       0.29               3.78             3.666667             0.51 n<14

saved -> scipy_analysis/outputs/tables/pooled_method_table.csv


===== RANKINGS (n>=14 only) =====

[pooled] protection (high to low):
                                            method   n  protection_mean
                   Clear all conversation history.  50             3.80
Type a message asking the AI Chatbot to forget it.  29             3.79
                  Delete this single conversation. 105             3.66
           Delete a specific saved memory or fact.  30             3.65

[pooled] effort (high to low):
                                            method   n  effort_mean
           Delete a specific saved memory or fact.  30         2.45
                   Clear all conversation history.  50         2.04
Type a message asking the AI Chatbot to forget it.  29         1.79
                  Delete this single conversation. 105         1.68

[pooled] benefit_loss (high to low):
                                            method   n  benefit_loss_mean
           Delete a specific saved memory or fact.  30               3.43
                   Clear all conversation history.  50               3.11
                  Delete this single conversation. 105               3.01
Type a message asking the AI Chatbot to forget it.  29               2.99

saved -> outputs/figures/fig9_pooled_cost_benefit.png
```
