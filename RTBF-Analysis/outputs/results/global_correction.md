# global_correction

_Run at 2026-08-03T03:40:50_

```text
=== Global correction across 101 primary/omnibus tests ===
raw p<.05        : 31 / 101
Holm-global p<.05: 14 / 101
BH-FDR q<.05     : 22 / 101

-- tests significant at raw p<.05 (sorted by p_raw) --
                       family                                         label    p_raw  p_holm_global  p_fdr_global  sig_holm_global  sig_fdr_global
    calibration.used_vs_ideal                          [less] Ask to forget 0.000000       0.000000      0.000000             True            True
    calibration.used_vs_ideal                     [more] Clear all memories 0.000000       0.000000      0.000000             True            True
    calibration.used_vs_ideal                    [less] Delete specific mem 0.000000       0.000000      0.000000             True            True
    calibration.used_vs_ideal                      [more] Clear all history 0.000000       0.000000      0.000000             True            True
    calibration.used_vs_ideal                      [less] Clear all history 0.000000       0.000000      0.000000             True            True
    calibration.used_vs_ideal                      [less] Privacy dashboard 0.000000       0.000000      0.000000             True            True
    calibration.used_vs_ideal                    [more] Delete specific mem 0.000000       0.000000      0.000000             True            True
    calibration.used_vs_ideal                          [more] Ask to forget 0.000000       0.000000      0.000000             True            True
   willingness.scenario_shift                  [scenario shift] willingness 0.000012       0.001127      0.000136             True            True
    calibration.used_vs_ideal                     [less] Delete single conv 0.000100       0.009200      0.000842             True            True
    calibration.used_vs_ideal                     [less] Clear all memories 0.000100       0.009200      0.000842             True            True
    calibration.used_vs_ideal                      [more] Privacy dashboard 0.000100       0.009200      0.000842             True            True
          verify.verification                       [less] asked same convo 0.000300       0.026700      0.002331             True            True
         stats.between_method                       [less|effort] method KW 0.000361       0.031740      0.002602             True            True
stats.between_scenario_likert                [protection] scenario Wilcoxon 0.000611       0.053163      0.004115            False            True
         stats.between_method                       [more|effort] method KW 0.000715       0.061470      0.004512            False            True
          verify.verification                        [less] asked new convo 0.000800       0.068000      0.004753            False            True
    calibration.used_vs_ideal                     [more] Delete single conv 0.001000       0.084000      0.005611            False            True
          verify.verification                       [less] did NOT know how 0.001100       0.091300      0.005847            False            True
          verify.verification                       [more] asked same convo 0.006000       0.492000      0.030300            False            True
          verify.verification                       [more] checked settings 0.006600       0.534600      0.031743            False            True
           verify.expectation                       [more] not ref. current 0.007700       0.616000      0.035350            False            True
 calibration.confidence_trend                                        [less] 0.012352       0.975797      0.054241            False           False
     moderators.method_choice                 [more] chatgpt_tenure->method 0.013500       1.000000      0.056813            False           False
     moderators.method_choice                      [less] age_group->method 0.016800       1.000000      0.067872            False           False
     mcnemar.per_method_shift            Type a message asking the AI Chatb 0.019200       1.000000      0.074585            False           False
    calibration.used_vs_ideal                         [more] Delete account 0.021500       1.000000      0.080426            False           False
 calibration.confidence_trend                                        [more] 0.025979       1.000000      0.093711            False           False
           verify.expectation                        [more] not ref. future 0.029500       1.000000      0.102741            False           False
stats.between_scenario_binary [scenario shift] expectation (Q4.4/Q5.4) opt1 0.031141       1.000000      0.104842            False           False
          verify.verification                       [more] did NOT know how 0.043700       1.000000      0.142377            False           False

-- of those, still significant under BH-FDR global correction --
                       family                          label    p_raw  p_fdr_global
    calibration.used_vs_ideal           [less] Ask to forget 0.000000      0.000000
    calibration.used_vs_ideal      [more] Clear all memories 0.000000      0.000000
    calibration.used_vs_ideal     [less] Delete specific mem 0.000000      0.000000
    calibration.used_vs_ideal       [more] Clear all history 0.000000      0.000000
    calibration.used_vs_ideal       [less] Clear all history 0.000000      0.000000
    calibration.used_vs_ideal       [less] Privacy dashboard 0.000000      0.000000
    calibration.used_vs_ideal     [more] Delete specific mem 0.000000      0.000000
    calibration.used_vs_ideal           [more] Ask to forget 0.000000      0.000000
   willingness.scenario_shift   [scenario shift] willingness 0.000012      0.000136
    calibration.used_vs_ideal      [less] Delete single conv 0.000100      0.000842
    calibration.used_vs_ideal      [less] Clear all memories 0.000100      0.000842
    calibration.used_vs_ideal       [more] Privacy dashboard 0.000100      0.000842
          verify.verification        [less] asked same convo 0.000300      0.002331
         stats.between_method        [less|effort] method KW 0.000361      0.002602
stats.between_scenario_likert [protection] scenario Wilcoxon 0.000611      0.004115
         stats.between_method        [more|effort] method KW 0.000715      0.004512
          verify.verification         [less] asked new convo 0.000800      0.004753
    calibration.used_vs_ideal      [more] Delete single conv 0.001000      0.005611
          verify.verification        [less] did NOT know how 0.001100      0.005847
          verify.verification        [more] asked same convo 0.006000      0.030300
          verify.verification        [more] checked settings 0.006600      0.031743
           verify.expectation        [more] not ref. current 0.007700      0.035350

-- of those, still significant under Holm global correction (strictest) --
                    family                        label    p_raw  p_holm_global
 calibration.used_vs_ideal         [less] Ask to forget 0.000000       0.000000
 calibration.used_vs_ideal    [more] Clear all memories 0.000000       0.000000
 calibration.used_vs_ideal   [less] Delete specific mem 0.000000       0.000000
 calibration.used_vs_ideal     [more] Clear all history 0.000000       0.000000
 calibration.used_vs_ideal     [less] Clear all history 0.000000       0.000000
 calibration.used_vs_ideal     [less] Privacy dashboard 0.000000       0.000000
 calibration.used_vs_ideal   [more] Delete specific mem 0.000000       0.000000
 calibration.used_vs_ideal         [more] Ask to forget 0.000000       0.000000
willingness.scenario_shift [scenario shift] willingness 0.000012       0.001127
 calibration.used_vs_ideal    [less] Delete single conv 0.000100       0.009200
 calibration.used_vs_ideal    [less] Clear all memories 0.000100       0.009200
 calibration.used_vs_ideal     [more] Privacy dashboard 0.000100       0.009200
       verify.verification      [less] asked same convo 0.000300       0.026700
      stats.between_method      [less|effort] method KW 0.000361       0.031740
```

## DON'T CLEAR THIS
## Interpretation

Global correction (global_correction.md) — the honesty check on the whole project

This is the strictest possible read of the entire analysis: what survives if all ~101 primary tests run across every script are treated as one family, instead of each script's own local Holm correction (which only ever compares a test against its own small sub-family of 2-8 related tests)? Answer: **roughly a third of "raw significant" results (31) shrink to 14 under global Holm, or 22 under the more standard BH-FDR.**

- **What survives even the strictest global Holm correction (14 tests) — the results you can defend without any caveat about multiple testing:**
  1. **8 `calibration.used_vs_ideal` tests** (p_raw effectively 0) — but remember these carry the select-all/single-select structural caveat from `calibration_stats.md`; statistically bulletproof, conceptually still needs that caveat attached.
  2. **Willingness scenario shift** (`willingness.md`, p=.000012) — the cleanest, least-caveated result in the entire project. No structural confound, large effect size, survives every correction tried.
  3. **3 more `used_vs_ideal` tests** (Delete single conv, Clear all memories, Privacy dashboard).
  4. **Verification differs by method, "asked same convo" option** (`verify.md`, p=.0003).
  5. **Effort differs by method, less-sensitive scenario** (`stats.md`, p=.00036).

- **What looked solid within its own script's correction but does NOT survive global correction — worth flagging down a notch when citing:**
  - **Protection scenario shift** (`stats.md` steps 3-4) — p_raw=.0006, survives its own within-family Holm (p_holm=.0018) and BH-FDR-global (q=.004), but narrowly **fails** global Holm (p_holm_global=.053). This was reported as one of the two headline "clean" findings earlier in this project — it's still very likely real (BH-FDR, the more standard choice for a battery this size, keeps it), but it's not quite as bulletproof as "effort by method" or "willingness by scenario."
  - **Effort by method, more-sensitive scenario** (p_raw=.0007) — same pattern, survives FDR not Holm-global.
  - Several `verify.py` method-association results (asked new convo, did NOT know how, checked settings, not ref. current) — real at the raw and FDR level, gone under strict Holm.
  - **Both `moderators.md` method-choice associations** (age in "less," tenure in "more") — neither survives FDR or Holm-global. Confirms the read already given in `moderators.md`: these are noise, not confirmed effects.
  - Confidence→verification trend tests, the per-method McNemar for "Ask to forget," and the aggregate McNemar "permanently deleted" shift all fall away entirely under any global correction — consistent with how they were already caveated as suggestive-not-confirmed in their own reports.

**Bottom line for anyone citing this project**: if you need one uncaveated headline claim, use **willingness rises significantly with scenario sensitivity** — it's the only major finding that's both large in effect size and survives literally every correction method tried, at any level of strictness. Everything else should carry at least a "significant within its own comparison family" qualifier rather than being presented as globally airtight.
