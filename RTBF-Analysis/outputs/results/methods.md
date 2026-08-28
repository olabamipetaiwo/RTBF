# methods

_Run at 2026-08-25T23:45:14_

```text

===== LESS SENSITIVE =====
                                                  method  n  protection_mean  protection_median  protection_sd  effort_mean  effort_median  effort_sd  benefit_loss_mean  benefit_loss_median  benefit_loss_sd flag
                        Delete this single conversation. 84             3.54                3.6           0.85         1.62          1.500       0.71               2.97             3.000000             1.05     
                         Clear all conversation history. 33             3.77                4.0           0.93         1.98          2.000       0.94               3.06             3.333333             1.11     
      Type a message asking the AI Chatbot to forget it. 25             3.84                4.0           0.61         1.86          2.000       0.90               2.91             3.000000             0.98     
                 Delete a specific saved memory or fact. 19             3.58                3.8           0.89         2.70          2.500       1.09               3.54             3.666667             0.86     
                               Clear all saved memories.  7             3.94                4.0           0.30         2.21          2.000       1.10               3.90             4.000000             0.71 n<14
Privacy dashboard or account-level data management page.  6             3.90                4.2           1.04         2.33          2.375       1.14               3.06             3.000000             1.39 n<14
                             Delete my account entirely.  2             3.80                3.8           0.57         3.25          3.250       0.71               3.17             3.166667             0.24 n<14

===== MORE SENSITIVE =====
                                                  method  n  protection_mean  protection_median  protection_sd  effort_mean  effort_median  effort_sd  benefit_loss_mean  benefit_loss_median  benefit_loss_sd flag
                        Delete this single conversation. 81             3.73                3.8           0.91         1.67          1.500       0.81               3.02             3.000000             1.01     
                         Clear all conversation history. 40             3.78                4.0           0.82         2.18          2.000       1.00               3.14             3.333333             1.10     
                 Delete a specific saved memory or fact. 22             3.71                4.0           0.69         2.32          2.250       0.97               3.38             3.500000             0.92     
      Type a message asking the AI Chatbot to forget it. 14             3.89                4.0           0.73         1.54          1.375       0.50               2.90             2.833333             0.95     
Privacy dashboard or account-level data management page.  9             3.93                4.0           0.84         2.50          3.000       1.49               3.37             3.666667             1.09 n<14
                               Clear all saved memories.  8             4.22                4.1           0.69         1.88          1.500       1.14               3.12             3.333333             1.27 n<14
                             Delete my account entirely.  3             4.33                4.4           0.70         3.50          3.250       0.66               4.00             4.333333             0.58 n<14


===== RANKINGS (n>=15 only) =====

[less] protection (high to low):
                                            method  n  protection_mean
Type a message asking the AI Chatbot to forget it. 25             3.84
                   Clear all conversation history. 33             3.77
           Delete a specific saved memory or fact. 19             3.58
                  Delete this single conversation. 84             3.54

[less] effort (high to low):
                                            method  n  effort_mean
           Delete a specific saved memory or fact. 19         2.70
                   Clear all conversation history. 33         1.98
Type a message asking the AI Chatbot to forget it. 25         1.86
                  Delete this single conversation. 84         1.62

[less] benefit_loss (high to low):
                                            method  n  benefit_loss_mean
           Delete a specific saved memory or fact. 19               3.54
                   Clear all conversation history. 33               3.06
                  Delete this single conversation. 84               2.97
Type a message asking the AI Chatbot to forget it. 25               2.91

[more] protection (high to low):
                                            method  n  protection_mean
Type a message asking the AI Chatbot to forget it. 14             3.89
                   Clear all conversation history. 40             3.78
                  Delete this single conversation. 81             3.73
           Delete a specific saved memory or fact. 22             3.71

[more] effort (high to low):
                                            method  n  effort_mean
           Delete a specific saved memory or fact. 22         2.32
                   Clear all conversation history. 40         2.18
                  Delete this single conversation. 81         1.67
Type a message asking the AI Chatbot to forget it. 14         1.54

[more] benefit_loss (high to low):
                                            method  n  benefit_loss_mean
           Delete a specific saved memory or fact. 22               3.38
                   Clear all conversation history. 40               3.14
                  Delete this single conversation. 81               3.02
Type a message asking the AI Chatbot to forget it. 14               2.90

saved -> outputs/tables/per_method_less.csv, per_method_more.csv
saved -> outputs/figures/fig7_method_cost_benefit.png
```
