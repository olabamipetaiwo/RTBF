# reliability

_Run at 2026-08-07T14:22:07_

```text
=== Cronbach's alpha (>=0.70 = acceptable) ===
scenario        scale  items  n_complete  alpha         ci95  unmapped_values verdict
    less   protection      5         177  0.893 [0.86, 0.92]                0      OK
    less       effort      4         177  0.921 [0.90, 0.94]                0      OK
    less benefit_loss      3         177  0.870 [0.83, 0.90]                0      OK
    more   protection      5         177  0.900 [0.88, 0.92]                0      OK
    more       effort      4         177  0.923 [0.90, 0.94]                0      OK
    more benefit_loss      3         177  0.872 [0.84, 0.90]                0      OK

saved -> outputs/tables/scale_reliability.csv
```

## DON'T CLEAR THIS
## Interpretation

Reliability (reliability.md) — can the scale scores be trusted

- All 6 scales (protection/effort/benefit_loss × less/more) have α between 0.87–0.92, all "OK," 0 unmapped values, n_complete=177 throughout.
- Read: this is strong internal consistency — well above the conventional 0.70 bar, actually into "very good" territory (some methodologists would even flag >0.90 as mild redundancy among items, but not concerning at 3-5 items). This licenses everything downstream: it's statistically defensible to average each item set into a single scale score per respondent, which is exactly what methods.py then does. If these had come back <0.70, the per-method means in step 3 wouldn't mean much.
