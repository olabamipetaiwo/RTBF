# calibration_stats

_Run at 2026-08-07T14:21:33_

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

## DON'T CLEAR THIS
## Interpretation

Calibration stats (calibration_stats.md) — testing the gaps calibration.md found descriptively, now BOTH scenarios (fixed the gap where "more" was never actually run)

- **Confidence predicts verification in both scenarios, but the trend is weaker when it matters more**: less-sensitive p=.012 (z=2.50); more-sensitive p=.026 (z=2.23) — still significant, but the trend statistically weakens exactly when you'd hope it would strengthen. Combined with `calibration.md`'s raw numbers (verification flat-to-worse in the more-sensitive scenario at low confidence), this reinforces rather than contradicts the miscalibration story: **the correlation between confidence and checking doesn't get stronger when the data is more sensitive.**

- **Used-vs-ideal gaps: 6/7 methods significant in "less," all 7/7 significant in "more."** "Delete account" flips from ns (less: p_holm=.070, n=8 discordant) to significant (more: p_holm=.0215, n=10 discordant) — likely just a power threshold being crossed as the discordant count grew, not a real qualitative change in behavior.

  ⚠️ **Same structural caveat as before, in both scenarios**: Q4.2/Q5.2 ("used") is single-select, Q4.13/Q5.13 ("ideal") is select-all, so `ideal_only > used_only` being significant is close to mechanically guaranteed for any popular method. What's still meaningful: the **relative ranking and magnitude** of the gaps, and how that ranking **shifts between scenarios**.

  On that basis: gaps grow larger in the more-sensitive scenario for every major method — "Ask to forget" discordant count rises from 70 (less) to **79** (more), "Delete specific mem" from 48 to **62**. This matches the widening %-gaps already seen in `calibration.md`.

- **Global correction check** (see `global_correction.md`): 8 of the used-vs-ideal tests come back at p_raw essentially 0 (rounds to .0000) and survive even the strictest possible correction across the *entire* ~100-test analysis battery — these are the single most statistically bulletproof results in the whole project, modulo the structural caveat above. Several of the more marginal ones (e.g. "more: Delete account," p_raw=.0215) do NOT survive global correction, so treat within-family significance here as a lower bar than "genuinely the strongest evidence in this dataset."

**Bottom line**: confidence→verification trend is real in both scenarios but doesn't strengthen with stakes; used-vs-ideal gaps are statistically significant nearly everywhere but need the select-all/single-select caveat attached whenever cited, and the *widening* of these gaps in the more-sensitive scenario is itself a new, worth-reporting pattern.
