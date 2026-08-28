# calibration

_Run at 2026-08-03T03:34:51_

```text

============================================================
LESS SENSITIVE — 8a. Confidence vs verification (Q4.6/Q4.5)
============================================================
            did NOT verify  verified  % confident-but-unverified
confidence                                                      
Not at all               9         2                        81.8
Slightly                20        14                        58.8
Moderately              36        25                        59.0
Very                    21        30                        41.2
Completely               9        11                        45.0

LESS SENSITIVE — 8b. Used vs ideal method (Q4.2/Q4.13)
============================================================
             method  %used  %ideal  gap (ideal-used)
      Ask to forget   14.1    46.9              32.8
Delete specific mem   10.7    31.1              20.3
 Delete single conv   47.5    66.1              18.6
  Clear all history   18.6    35.6              16.9
 Clear all memories    4.0    16.9              13.0
  Privacy dashboard    3.4    15.3              11.9
     Delete account    1.1     4.5               3.4

-- options with no %used counterpart (not in Q4.2/Q5.2) --
         method                        %used  %ideal gap (ideal-used)
File a request. n/a (not a Q4.2/Q5.2 option)     2.3              n/a

============================================================
MORE SENSITIVE — 8a. Confidence vs verification (Q5.6/Q5.5)
============================================================
            did NOT verify  verified  % confident-but-unverified
confidence                                                      
Not at all               8         1                        88.9
Slightly                24        14                        63.2
Moderately              27        27                        50.0
Very                    25        28                        47.2
Completely              11        12                        47.8

MORE SENSITIVE — 8b. Used vs ideal method (Q5.2/Q5.13)
============================================================
             method  %used  %ideal  gap (ideal-used)
      Ask to forget    7.9    50.0              42.1
Delete specific mem   12.4    41.6              29.2
 Clear all memories    4.5    24.2              19.7
  Clear all history   22.5    40.4              18.0
 Delete single conv   45.5    60.1              14.6
  Privacy dashboard    5.1    17.4              12.4
     Delete account    1.7     6.2               4.5

-- options with no %used counterpart (not in Q4.2/Q5.2) --
         method                        %used  %ideal gap (ideal-used)
File a request. n/a (not a Q4.2/Q5.2 option)     5.1              n/a
```

## DON'T CLEAR THIS
## Interpretation

Calibration (calibration.md) — descriptive, now covering BOTH scenarios (fixed a gap where "more" was never actually run despite the docstring claiming it was)

- **Confidence-verification miscalibration doesn't improve when stakes rise — if anything it's slightly worse.** Compare the "Not at all confident" row: 81.8% never verified in the less-sensitive scenario vs. **88.9%** in the more-sensitive one. Every confidence band shows flat-to-worse verification in the more-sensitive scenario except "Moderately confident" (59.0%→50.0%, an improvement). The natural expectation — that people check more carefully when the data matters more — isn't what the raw numbers show.

- **Used-vs-ideal gaps widen in the more-sensitive scenario for most methods**, not narrow: "Ask to forget" 32.8→**42.1** points, "Delete specific mem" 20.3→**29.2**, "Clear all memories" 13.0→**19.7**. People's *preferences* shift toward these methods faster than their *actual behavior* does when data is more sensitive — the disconnect between what people want and what they do gets bigger exactly when the stakes are highest.

- **Desire for a "File a request" option (which doesn't exist in the actual method list) roughly doubles**: 2.3%→5.1%. Small in absolute terms, but a consistent signal that some users want a more formal/accountable deletion mechanism than anything currently offered, and want it more as sensitivity rises.

See `calibration_stats.md` for which of these patterns are statistically confirmed.
no