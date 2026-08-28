# willingness

_Run at 2026-08-07T14:20:47_

```text
=== Willingness to delete: less vs more sensitive (paired Wilcoxon) ===
n pairs        : 177
mean willing (less): 3.977   (more): 4.367
mean_diff      : +0.390  (more>less)
W              : 754.5
p-value        : 0.0000   RBC r=+0.546
verdict        : SIG

willingness distribution (count):
                    less  more
Definitely not         3     0
Probably not          22    10
Might or might not    27    17
Probably yes          49    48
Definitely yes        76   102

============================================================
WILLINGNESS BY METHOD (Kruskal-Wallis -> Dunn's + Holm)
============================================================

[less] KW  H=3.22  p=0.3586  eps2=0.001  -> ns

[more] KW  H=5.12  p=0.1631  eps2=0.014  -> ns
```

## DON'T CLEAR THIS
## Interpretation

Willingness to delete (willingness.md) — the strongest scenario effect in the whole battery, and a clean null for method

- **Scenario effect is large and unambiguous**: willingness rises from 3.98 to 4.37 (less→more sensitive), p<.0001, RBC r=+0.546 — the biggest effect size of any test in this project. "Definitely yes" alone grows from 76→102 respondents; "Definitely not" drops to zero. Unlike the protection-rating shift (r=0.38, a framing effect), this is a large, decisive behavioral-intent shift. Per `global_correction.md`, this is one of only 14 results that survive the strictest possible correction across the *entire* ~100-test battery — the single most bulletproof finding in this analysis.

- **Willingness does NOT differ by which method someone used**, in either scenario (less: p=.359; more: p=.163, both ns). This is a clean, sensible null: willingness is a property of the *person's disposition* toward deleting at all, not a property of which specific method happens to be available or chosen — unlike effort, which is inherently method-specific (how much work does *this* action take). Good discriminant validity check: the scale is measuring something conceptually distinct from the per-method ratings in `stats.md`.

**Bottom line**: "people become significantly more willing to delete as data sensitivity rises, regardless of method" is the single strongest, most defensible claim in this entire analysis.
