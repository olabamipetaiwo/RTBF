# calibration_stats

_Run at 2026-08-07T14:24:13_

```text

============================================================
LESS SENSITIVE — 8a. Confidence -> verification: ordinal trend test
============================================================
col_0                                       did NOT verify  verified
Q4.6                                                                
Not confident at all (I doubted it worked)               9         2
Slightly confident                                      20        14
Moderately confident                                    36        25
Very confident                                          21        30
Completely confident (I had no doubt)                    9        11

trend statistic=280.000  z=2.502  p=0.0124  -> SIG (verification rises with confidence)

LESS SENSITIVE — 8b. Used vs ideal, per method: paired McNemar + Holm
============================================================
             method  used_only  ideal_only  discordant        dir  p_raw  p_holm sig
      Ask to forget          6          64          70 ideal>used 0.0000  0.0000   *
 Delete single conv         17          50          67 ideal>used 0.0001  0.0003   *
Delete specific mem          6          42          48 ideal>used 0.0000  0.0000   *
  Clear all history          5          35          40 ideal>used 0.0000  0.0000   *
 Clear all memories          5          28          33 ideal>used 0.0001  0.0003   *
  Privacy dashboard          1          22          23 ideal>used 0.0000  0.0000   *
     Delete account          1           7           8 ideal>used 0.0703  0.0703    

============================================================
MORE SENSITIVE — 8a. Confidence -> verification: ordinal trend test
============================================================
col_0                                       did NOT verify  verified
Q5.6                                                                
Not confident at all (I doubted it worked)               8         1
Slightly confident                                      24        14
Moderately confident                                    27        27
Very confident                                          25        28
Completely confident (I had no doubt)                   11        12

trend statistic=282.000  z=2.227  p=0.0260  -> SIG (verification rises with confidence)

MORE SENSITIVE — 8b. Used vs ideal, per method: paired McNemar + Holm
============================================================
             method  used_only  ideal_only  discordant        dir  p_raw  p_holm sig
      Ask to forget          2          77          79 ideal>used 0.0000  0.0000   *
Delete specific mem          5          57          62 ideal>used 0.0000  0.0000   *
 Delete single conv         16          42          58 ideal>used 0.0010  0.0021   *
  Clear all history          9          41          50 ideal>used 0.0000  0.0000   *
 Clear all memories          3          38          41 ideal>used 0.0000  0.0000   *
  Privacy dashboard          3          25          28 ideal>used 0.0001  0.0002   *
     Delete account          1           9          10 ideal>used 0.0215  0.0215   *

used_only  = used it but did NOT mark it ideal
ideal_only = marked it ideal but did NOT use it  (this is the gap direction)
Holm across 7 methods, within each scenario. 'File a request.' excluded: no Q4.2/Q5.2 counterpart.
```
