# mcnemar

_Run at 2026-08-07T14:22:23_

```text
=== Per-method choice shift (less -> more): McNemar + Holm ===
                            method  dropped  added  discordant  dir  p_raw  p_holm sig
   Delete this single conversation       25     21          46 drop 0.6583  1.0000    
    Clear all conversation history       10     17          27 gain 0.2482  1.0000    
Delete a specific saved memory or         8     11          19 gain 0.6476  1.0000    
Type a message asking the AI Chatb       15      4          19 drop 0.0192  0.1345    
          Clear all saved memories        3      4           7 gain 1.0000  1.0000    
Privacy dashboard or account-level        2      5           7 gain 0.4531  1.0000    
        Delete my account entirely        0      1           1 gain 1.0000  1.0000    

dropped = picked in less-sensitive only (abandoned when sensitive)
added   = picked in more-sensitive only (adopted when sensitive)
Holm across 7 methods. Stuart-Maxwell omnibus was ns (p=0.393).
```
