# global_correction

_Run at 2026-08-11T05:22:43_

```text
=== Global correction across 117 primary/omnibus tests ===
raw p<.05        : 39 / 117
Holm-global p<.05: 21 / 117
BH-FDR q<.05     : 31 / 117

-- tests significant at raw p<.05 (sorted by p_raw) --
                            family                                         label        p_raw  p_holm_global  p_fdr_global  sig_holm_global  sig_fdr_global
         calibration.used_vs_ideal                          [less] Ask to forget 0.000000e+00   0.000000e+00  0.000000e+00             True            True
         calibration.used_vs_ideal                    [more] Delete specific mem 0.000000e+00   0.000000e+00  0.000000e+00             True            True
         calibration.used_vs_ideal                      [more] Clear all history 0.000000e+00   0.000000e+00  0.000000e+00             True            True
         calibration.used_vs_ideal                     [more] Clear all memories 0.000000e+00   0.000000e+00  0.000000e+00             True            True
         calibration.used_vs_ideal                      [less] Clear all history 0.000000e+00   0.000000e+00  0.000000e+00             True            True
         calibration.used_vs_ideal                    [less] Delete specific mem 0.000000e+00   0.000000e+00  0.000000e+00             True            True
         calibration.used_vs_ideal                          [more] Ask to forget 0.000000e+00   0.000000e+00  0.000000e+00             True            True
         calibration.used_vs_ideal                      [less] Privacy dashboard 0.000000e+00   0.000000e+00  0.000000e+00             True            True
          expectation_rank.cochran                            [more] expectation 1.481900e-50   1.615271e-48  1.926470e-49             True            True
          expectation_rank.cochran                            [less] expectation 4.240788e-50   4.580051e-48  4.961722e-49             True            True
          expectation_rank.cochran                           [more] verification 1.715485e-28   1.835569e-26  1.824652e-27             True            True
          expectation_rank.cochran                           [less] verification 1.198078e-27   1.269962e-25  1.168126e-26             True            True
        willingness.scenario_shift                  [scenario shift] willingness 1.197947e-05   1.257844e-03  1.078152e-04             True            True
correlations.discriminant_validity                  [pooled] effort~benefit_loss 3.711786e-05   3.860258e-03  3.101993e-04             True            True
correlations.discriminant_validity                    [less] effort~benefit_loss 9.870114e-05   1.016622e-02  6.500000e-04             True            True
         calibration.used_vs_ideal                      [more] Privacy dashboard 1.000000e-04   1.020000e-02  6.500000e-04             True            True
         calibration.used_vs_ideal                     [less] Clear all memories 1.000000e-04   1.020000e-02  6.500000e-04             True            True
         calibration.used_vs_ideal                     [less] Delete single conv 1.000000e-04   1.020000e-02  6.500000e-04             True            True
                   crowning.pooled                               [pooled] effort 2.117372e-04   2.096198e-02  1.303855e-03             True            True
               verify.verification                       [less] asked same convo 3.000000e-04   2.940000e-02  1.755000e-03             True            True
              stats.between_method                       [less|effort] method KW 3.606854e-04   3.498648e-02  2.009533e-03             True            True
     stats.between_scenario_likert                [protection] scenario Wilcoxon 6.075186e-04   5.832178e-02  3.230894e-03            False            True
              stats.between_method                       [more|effort] method KW 7.147731e-04   6.790345e-02  3.636020e-03            False            True
               verify.verification                        [less] asked new convo 8.000000e-04   7.520000e-02  3.900000e-03            False            True
correlations.discriminant_validity                    [more] effort~benefit_loss 9.257597e-04   8.609565e-02  4.332555e-03            False            True
         calibration.used_vs_ideal                     [more] Delete single conv 1.000000e-03   9.200000e-02  4.500000e-03            False            True
               verify.verification                       [less] did NOT know how 1.100000e-03   1.001000e-01  4.766667e-03            False            True
               verify.verification                       [more] checked settings 5.100000e-03   4.590000e-01  2.131071e-02            False            True
               verify.verification                       [more] asked same convo 5.600000e-03   4.984000e-01  2.259310e-02            False            True
                verify.expectation                       [more] not ref. current 7.700000e-03   6.776000e-01  3.003000e-02            False            True
      calibration.confidence_trend                                        [less] 1.235187e-02   1.000000e+00  4.661833e-02            False            True
          moderators.method_choice                 [more] chatgpt_tenure->method 1.480000e-02   1.000000e+00  5.411250e-02            False           False
          moderators.method_choice                      [less] age_group->method 1.710000e-02   1.000000e+00  6.062727e-02            False           False
          mcnemar.per_method_shift            Type a message asking the AI Chatb 1.920000e-02   1.000000e+00  6.607059e-02            False           False
         calibration.used_vs_ideal                         [more] Delete account 2.150000e-02   1.000000e+00  7.187143e-02            False           False
      calibration.confidence_trend                                        [more] 2.597925e-02   1.000000e+00  8.443257e-02            False           False
                verify.expectation                        [more] not ref. future 2.950000e-02   1.000000e+00  9.328378e-02            False           False
     stats.between_scenario_binary [scenario shift] expectation (Q4.4/Q5.4) opt1 3.114121e-02   1.000000e+00  9.588215e-02            False           False
               verify.verification                       [more] did NOT know how 4.370000e-02   1.000000e+00  1.311000e-01            False           False

-- of those, still significant under BH-FDR global correction --
                            family                          label        p_raw  p_fdr_global
         calibration.used_vs_ideal           [less] Ask to forget 0.000000e+00  0.000000e+00
         calibration.used_vs_ideal     [more] Delete specific mem 0.000000e+00  0.000000e+00
         calibration.used_vs_ideal       [more] Clear all history 0.000000e+00  0.000000e+00
         calibration.used_vs_ideal      [more] Clear all memories 0.000000e+00  0.000000e+00
         calibration.used_vs_ideal       [less] Clear all history 0.000000e+00  0.000000e+00
         calibration.used_vs_ideal     [less] Delete specific mem 0.000000e+00  0.000000e+00
         calibration.used_vs_ideal           [more] Ask to forget 0.000000e+00  0.000000e+00
         calibration.used_vs_ideal       [less] Privacy dashboard 0.000000e+00  0.000000e+00
          expectation_rank.cochran             [more] expectation 1.481900e-50  1.926470e-49
          expectation_rank.cochran             [less] expectation 4.240788e-50  4.961722e-49
          expectation_rank.cochran            [more] verification 1.715485e-28  1.824652e-27
          expectation_rank.cochran            [less] verification 1.198078e-27  1.168126e-26
        willingness.scenario_shift   [scenario shift] willingness 1.197947e-05  1.078152e-04
correlations.discriminant_validity   [pooled] effort~benefit_loss 3.711786e-05  3.101993e-04
correlations.discriminant_validity     [less] effort~benefit_loss 9.870114e-05  6.500000e-04
         calibration.used_vs_ideal       [more] Privacy dashboard 1.000000e-04  6.500000e-04
         calibration.used_vs_ideal      [less] Clear all memories 1.000000e-04  6.500000e-04
         calibration.used_vs_ideal      [less] Delete single conv 1.000000e-04  6.500000e-04
                   crowning.pooled                [pooled] effort 2.117372e-04  1.303855e-03
               verify.verification        [less] asked same convo 3.000000e-04  1.755000e-03
              stats.between_method        [less|effort] method KW 3.606854e-04  2.009533e-03
     stats.between_scenario_likert [protection] scenario Wilcoxon 6.075186e-04  3.230894e-03
              stats.between_method        [more|effort] method KW 7.147731e-04  3.636020e-03
               verify.verification         [less] asked new convo 8.000000e-04  3.900000e-03
correlations.discriminant_validity     [more] effort~benefit_loss 9.257597e-04  4.332555e-03
         calibration.used_vs_ideal      [more] Delete single conv 1.000000e-03  4.500000e-03
               verify.verification        [less] did NOT know how 1.100000e-03  4.766667e-03
               verify.verification        [more] checked settings 5.100000e-03  2.131071e-02
               verify.verification        [more] asked same convo 5.600000e-03  2.259310e-02
                verify.expectation        [more] not ref. current 7.700000e-03  3.003000e-02
      calibration.confidence_trend                         [less] 1.235187e-02  4.661833e-02

-- of those, still significant under Holm global correction (strictest) --
                            family                        label        p_raw  p_holm_global
         calibration.used_vs_ideal         [less] Ask to forget 0.000000e+00   0.000000e+00
         calibration.used_vs_ideal   [more] Delete specific mem 0.000000e+00   0.000000e+00
         calibration.used_vs_ideal     [more] Clear all history 0.000000e+00   0.000000e+00
         calibration.used_vs_ideal    [more] Clear all memories 0.000000e+00   0.000000e+00
         calibration.used_vs_ideal     [less] Clear all history 0.000000e+00   0.000000e+00
         calibration.used_vs_ideal   [less] Delete specific mem 0.000000e+00   0.000000e+00
         calibration.used_vs_ideal         [more] Ask to forget 0.000000e+00   0.000000e+00
         calibration.used_vs_ideal     [less] Privacy dashboard 0.000000e+00   0.000000e+00
          expectation_rank.cochran           [more] expectation 1.481900e-50   1.615271e-48
          expectation_rank.cochran           [less] expectation 4.240788e-50   4.580051e-48
          expectation_rank.cochran          [more] verification 1.715485e-28   1.835569e-26
          expectation_rank.cochran          [less] verification 1.198078e-27   1.269962e-25
        willingness.scenario_shift [scenario shift] willingness 1.197947e-05   1.257844e-03
correlations.discriminant_validity [pooled] effort~benefit_loss 3.711786e-05   3.860258e-03
correlations.discriminant_validity   [less] effort~benefit_loss 9.870114e-05   1.016622e-02
         calibration.used_vs_ideal     [more] Privacy dashboard 1.000000e-04   1.020000e-02
         calibration.used_vs_ideal    [less] Clear all memories 1.000000e-04   1.020000e-02
         calibration.used_vs_ideal    [less] Delete single conv 1.000000e-04   1.020000e-02
                   crowning.pooled              [pooled] effort 2.117372e-04   2.096198e-02
               verify.verification      [less] asked same convo 3.000000e-04   2.940000e-02
              stats.between_method      [less|effort] method KW 3.606854e-04   3.498648e-02
```
