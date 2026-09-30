# compare

_Run at 2026-09-30T15:10:39_

```text
=== scipy_analysis vs src (manual) pipeline: 101 tests compared ===
Pearson  r   = 1.000000  (p=0.00e+00)
Spearman rho = 1.000000  (p=0.00e+00)

exact match (diff < 1e-9)      : 97 / 101
near match  (1e-9 <= diff < .02): 4 / 101
drifted     (diff >= .02)       : 0 / 101
significance flips (p<.05 disagreement): 0 / 101

-- 16 label(s) present in only one pipeline (fix before trusting the totals) --
                            family                            label     _merge
correlations.discriminant_validity       [less] effort~benefit_loss right_only
correlations.discriminant_validity   [less] protection~benefit_loss right_only
correlations.discriminant_validity         [less] protection~effort right_only
correlations.discriminant_validity       [more] effort~benefit_loss right_only
correlations.discriminant_validity   [more] protection~benefit_loss right_only
correlations.discriminant_validity         [more] protection~effort right_only
correlations.discriminant_validity     [pooled] effort~benefit_loss right_only
correlations.discriminant_validity [pooled] protection~benefit_loss right_only
correlations.discriminant_validity       [pooled] protection~effort right_only
                   crowning.pooled            [pooled] benefit_loss right_only
                   crowning.pooled                  [pooled] effort right_only
                   crowning.pooled              [pooled] protection right_only
          expectation_rank.cochran               [less] expectation right_only
          expectation_rank.cochran              [less] verification right_only
          expectation_rank.cochran               [more] expectation right_only
          expectation_rank.cochran              [more] verification right_only

-- no significance flips --
```
