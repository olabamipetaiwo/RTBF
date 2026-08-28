# fig10_method_shift_ranking

_Run at 2026-08-25T23:45:07_

```text
=== Method choice shift, RANKED by net (added - dropped) ===
                            method  dropped  added  discordant  dir  p_raw  p_holm sig  net
    Clear all conversation history       10     17          27 gain 0.2482  1.0000        7
Delete a specific saved memory or         8     11          19 gain 0.6476  1.0000        3
Privacy dashboard or account-level        2      5           7 gain 0.4531  1.0000        3
          Clear all saved memories        3      4           7 gain 1.0000  1.0000        1
        Delete my account entirely        0      1           1 gain 1.0000  1.0000        1
   Delete this single conversation       25     21          46 drop 0.6583  1.0000       -4
Type a message asking the AI Chatb       15      4          19 drop 0.0192  0.1345      -11

net = added - dropped (positive = net gain in popularity, negative = net loss)
None survive Holm correction (sig column empty for all 7) -- ranking shows
magnitude of raw shift, not statistical significance.

saved -> outputs/figures/fig10_method_shift_ranking.png
```
