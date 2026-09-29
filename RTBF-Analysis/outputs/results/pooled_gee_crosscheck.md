# pooled_gee_crosscheck

_Run at 2026-09-23T10:29:06_

```text
=== Cross-checks for the pooled GEE (src/pooled_gee.py) ===
352 observations, 176 participants; methods: ['Delete this single conversation.', 'Clear all conversation history.', 'Delete a specific saved memory or fact.', 'Type a message asking the AI Chatbot to forget it.']

----------------------------------------------------------------------
1. Random-intercept mixed model, likelihood-ratio test for method
   (compare with the GEE Wald test in pooled_gee.md; agreement on which
   scales show an effect is the check, not equality of p-values)
----------------------------------------------------------------------
  protection    LR chi2(3)=  3.607  p=0.3071
  effort        LR chi2(3)= 21.666  p=0.0001
  benefit_loss  LR chi2(3)=  3.802  p=0.2836

----------------------------------------------------------------------
2. Effort: participant-cluster bootstrap (5,000 draws, seed 42) vs GEE contrasts
   diff = reference (single conversation) minus method; GEE contrast is adjusted for scenario
----------------------------------------------------------------------
                                      method  gee_diff  ci_low  ci_high  boot_diff  boot_ci_low  boot_ci_high
             Clear all conversation history.    -0.450  -0.762   -0.138     -0.447       -0.771        -0.139
     Delete a specific saved memory or fact.    -0.852  -1.248   -0.455     -0.849       -1.253        -0.455
Type a message asking the AI Chatbot to forg    -0.098  -0.387    0.191     -0.100       -0.397         0.186
```
