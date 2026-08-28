# compare

_Run at 2026-08-07T14:24:19_

```text
=== scipy_analysis vs src (manual) pipeline: 101 tests compared ===
Pearson  r   = 0.999961  (p=3.57e-205)
Spearman rho = 0.999828  (p=2.84e-173)

exact match (diff < 1e-9)      : 73 / 101
near match  (1e-9 <= diff < .02): 28 / 101
drifted     (diff >= .02)       : 0 / 101
significance flips (p<.05 disagreement): 0 / 101

-- no significance flips --
```
