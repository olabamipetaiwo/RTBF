# expectation

_Run at 2026-08-03T02:44:06_

```text

======================================================================
LESS SENSITIVE — EXPECTATIONS (Q4.4, % per option)
======================================================================
                                                  method  n  permanently deleted (DB+backups)  made invisible / hidden  not referenced in current convo  not referenced in future convo  no longer used for training  not sure what happens  other flag
                        Delete this single conversation. 84                              56.0                     27.4                             46.4                            53.6                         26.2                   14.3    0.0     
                         Clear all conversation history. 33                              48.5                     36.4                             54.5                            51.5                         15.2                    6.1    3.0     
      Type a message asking the AI Chatbot to forget it. 25                              60.0                     12.0                             60.0                            56.0                         36.0                    4.0    0.0     
                 Delete a specific saved memory or fact. 19                              63.2                     15.8                             63.2                            52.6                         15.8                    5.3    0.0     
                               Clear all saved memories.  7                              28.6                     14.3                             42.9                            57.1                         42.9                    0.0    0.0 n<14
Privacy dashboard or account-level data management page.  6                              66.7                     33.3                             66.7                            83.3                         50.0                   16.7   16.7 n<14
                             Delete my account entirely.  2                              50.0                    100.0                             50.0                             0.0                        100.0                    0.0    0.0 n<14

======================================================================
LESS SENSITIVE — VERIFICATIONS (Q4.5, % per option)
======================================================================
                                                  method  n  asked in same conversation  asked in new conversation  checked memory/data settings  checked UI visibility  submitted privacy-portal request  did NOT know how to check  did NOT want to check  other flag
                        Delete this single conversation. 84                        10.7                        8.3                          11.9                   17.9                               3.6                       59.5                   14.3    1.2     
                         Clear all conversation history. 33                        27.3                       18.2                          12.1                   21.2                               6.1                       42.4                    9.1    0.0     
      Type a message asking the AI Chatbot to forget it. 25                        52.0                       40.0                          16.0                    8.0                               0.0                       24.0                    4.0    0.0     
                 Delete a specific saved memory or fact. 19                        26.3                       31.6                          36.8                   15.8                               5.3                       21.1                   15.8    5.3     
                               Clear all saved memories.  7                        14.3                       42.9                          28.6                   28.6                              14.3                       28.6                    0.0    0.0 n<14
Privacy dashboard or account-level data management page.  6                         0.0                       50.0                          50.0                    0.0                              16.7                       33.3                    0.0    0.0 n<14
                             Delete my account entirely.  2                        50.0                        0.0                         100.0                  100.0                              50.0                        0.0                    0.0    0.0 n<14

======================================================================
MORE SENSITIVE — EXPECTATIONS (Q5.4, % per option)
======================================================================
                                                  method  n  permanently deleted (DB+backups)  made invisible / hidden  not referenced in current convo  not referenced in future convo  no longer used for training  not sure what happens  other flag
                        Delete this single conversation. 81                              60.5                     32.1                             42.0                            54.3                         29.6                   11.1    0.0     
                         Clear all conversation history. 40                              55.0                     35.0                             27.5                            35.0                         17.5                   12.5    2.5     
                 Delete a specific saved memory or fact. 22                              68.2                      9.1                             72.7                            72.7                         22.7                    9.1    0.0     
      Type a message asking the AI Chatbot to forget it. 14                              71.4                     28.6                             42.9                            42.9                         35.7                    7.1    0.0     
Privacy dashboard or account-level data management page.  9                              66.7                     33.3                             77.8                            77.8                         55.6                   22.2    0.0 n<14
                               Clear all saved memories.  8                              62.5                     50.0                             87.5                            87.5                         37.5                   12.5    0.0 n<14
                             Delete my account entirely.  3                             100.0                     66.7                             33.3                            33.3                         66.7                    0.0    0.0 n<14

======================================================================
MORE SENSITIVE — VERIFICATIONS (Q5.5, % per option)
======================================================================
                                                  method  n  asked in same conversation  asked in new conversation  checked memory/data settings  checked UI visibility  submitted privacy-portal request  did NOT know how to check  did NOT want to check  other flag
                        Delete this single conversation. 81                        14.8                       17.3                           8.6                   11.1                               1.2                       56.8                    9.9    2.5     
                         Clear all conversation history. 40                        12.5                       17.5                          15.0                   25.0                               7.5                       42.5                   12.5    0.0     
                 Delete a specific saved memory or fact. 22                        18.2                       36.4                          36.4                    9.1                               0.0                       36.4                    9.1    4.5     
      Type a message asking the AI Chatbot to forget it. 14                        57.1                       21.4                           0.0                   14.3                               0.0                       21.4                   14.3    0.0     
Privacy dashboard or account-level data management page.  9                        22.2                       44.4                          66.7                   22.2                              33.3                       22.2                    0.0    0.0 n<14
                               Clear all saved memories.  8                        37.5                       62.5                          37.5                   12.5                              12.5                       12.5                    0.0    0.0 n<14
                             Delete my account entirely.  3                        33.3                       33.3                           0.0                    0.0                              33.3                       33.3                    0.0    0.0 n<14

saved -> outputs/tables/expectations_{less,more}.csv, verifications_{less,more}.csv
```

## DON'T CLEAR THIS
## Interpretation

Expectations & verifications by method (expectation.md) — descriptive only, not tested

This is a per-method breakdown of the same expectation/verification questions `stats.py` step 5 tested in aggregate (and found `ns` after correction). This script doesn't run any significance tests itself — read these as suggestive patterns to investigate, not confirmed findings. Cell sizes are small once split by method × option (e.g. "Type a message" more-sensitive is n=14), so a swing of 2-3 respondents moves the percentage by 15-20 points.

- **Training-data blind spot, across every method**: "no longer used for training" is the lowest- or near-lowest-endorsed expectation for every reportable method in both scenarios (15-37%, vs. 42-77% for other options). Regardless of which deletion method someone uses, roughly 65-85% of users do **not** expect it to stop their data from being used to train the model. That's a consistent gap across the whole method set, not specific to any one action — worth flagging as a trust/communication gap independent of which button someone clicks.

- **Verification effort tracks invocation effort**: the two methods `stats.py` already found to be lowest-effort ("Delete this single conversation", "Clear all conversation history") also have by far the highest "did NOT know how to check" rates (59.5%/42.4% less-sensitive, 56.8%/42.5% more-sensitive) and the lowest active-verification rates. "Type a message asking the AI Chatbot to forget it" is the opposite: verification is nearly built into the action (52.0%/57.1% "asked in same conversation" — i.e. the natural next step after typing a request is seeing if the bot still remembers). So the easiest methods to invoke are also the ones users are least equipped to verify — the effort tradeoff `methods.md`/`stats.md` found for *using* a method extends to *checking that it worked*.

- **Directional (untested) shift toward "permanently deleted" for the two biggest methods**: for "Delete this single conversation" (56.0%→60.5%) and "Clear all conversation history" (48.5%→55.0%), belief in permanent deletion rises modestly from less- to more-sensitive scenario — consistent in direction with the aggregate McNemar signal in `stats.md` (raw p=.031, ns after Holm). Since this script runs no test, this is circumstantial support at best, not independent confirmation.

**Caveat**: none of this is statistically tested at the per-method level — treat it the same way early `methods.md` treated its untested descriptives: real candidates for follow-up (e.g. a per-method McNemar or chi-square on "did NOT know how to check"), not claims to publish as-is.
