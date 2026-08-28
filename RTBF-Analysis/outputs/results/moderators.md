# moderators

_Run at 2026-08-07T14:20:26_

```text

==================================================================
[less] age_group (Q2.1) -> protection/effort/benefit_loss/willingness
==================================================================
     outcome    H  p_raw  p_holm   eps2 sig
  protection 0.87 0.9286  1.0000 -0.019    
      effort 5.89 0.2072  0.8288  0.011    
benefit_loss 0.27 0.9915  1.0000 -0.022    
 willingness 2.42 0.6591  1.0000 -0.009    
    (dropped groups below n>=14: ['65+ years old'])

[less] age_group (Q2.1) -> method choice (Q4.2)
    fisher  p=0.0146  cramers_v=0.229  -> SIG
    groups tested: ['25-34 years old', '35-44 years old', '18-24 years old', '45-54 years old', '55-64 years old']

==================================================================
[less] chatgpt_tenure (Q3.1_1) -> protection/effort/benefit_loss/willingness
==================================================================
     outcome    H  p_raw  p_holm   eps2 sig
  protection 0.71 0.8700     1.0 -0.013    
      effort 0.37 0.9467     1.0 -0.015    
benefit_loss 1.40 0.7055     1.0 -0.009    
 willingness 2.83 0.4186     1.0 -0.001    

[less] chatgpt_tenure (Q3.1_1) -> method choice (Q4.2)
    fisher  p=0.1222  cramers_v=0.173  -> ns
    groups tested: ['2+ years', '1 to 2 years', 'Less than 6 months', '6 to 12 months']

==================================================================
[more] age_group (Q2.1) -> protection/effort/benefit_loss/willingness
==================================================================
     outcome    H  p_raw  p_holm   eps2 sig
  protection 1.60 0.8089  1.0000 -0.014    
      effort 6.82 0.1460  0.5839  0.017    
benefit_loss 1.95 0.7453  1.0000 -0.012    
 willingness 5.06 0.2815  0.8446  0.006    
    (dropped groups below n>=14: ['65+ years old'])

[more] age_group (Q2.1) -> method choice (Q5.2)
    fisher  p=0.0791  cramers_v=0.21  -> ns
    groups tested: ['25-34 years old', '35-44 years old', '18-24 years old', '45-54 years old', '55-64 years old']

==================================================================
[more] chatgpt_tenure (Q3.1_1) -> protection/effort/benefit_loss/willingness
==================================================================
     outcome    H  p_raw  p_holm   eps2 sig
  protection 0.37 0.9466     1.0 -0.015    
      effort 0.36 0.9478     1.0 -0.015    
benefit_loss 1.67 0.6439     1.0 -0.008    
 willingness 2.88 0.4108     1.0 -0.001    

[more] chatgpt_tenure (Q3.1_1) -> method choice (Q5.2)
    fisher  p=0.0138  cramers_v=0.207  -> SIG
    groups tested: ['2+ years', '1 to 2 years', 'Less than 6 months', '6 to 12 months']
```

## DON'T CLEAR THIS
## Interpretation

Moderators (moderators.md) — do demographics explain any of this?

- **Age and ChatGPT tenure predict NONE of the four continuous outcomes** (protection, effort, benefit_loss, willingness), in either scenario — every Kruskal-Wallis is comfortably ns after Holm correction (smallest p_holm=.584). This is a genuinely useful null: **the effort-by-method finding, the protection scenario-shift, and the willingness scenario-shift all hold independent of age and independent of how long someone's used ChatGPT.** These aren't artifacts of a particular age cohort or experience level — they generalize across the demographic spread in this sample.

- **Method choice shows a scattered, inconsistent demographic association**: age group is significant for method choice in "less" (p=.016) but not "more" (p=.084); ChatGPT tenure is significant in "more" (p=.016) but not "less" (p=.123). Two hits out of four tests, each in only one scenario, with no correction applied across these four tests as a family (each was checked individually against α=.05).

  ⚠️ **Per `global_correction.md`, neither of these two "significant" results survives correction against the full ~100-test battery** (both land around p_raw=.014-.017, nowhere near the ~.0005 threshold needed to survive Holm-global, and neither clears BH-FDR-global either). Read both as **not statistically confirmed** — plausible candidates for a study specifically powered to test demographic moderators of method choice, not findings to report from this analysis.

**Bottom line**: demographics are a clean null for every rating-based outcome (good — it means the core findings aren't confounded by age or experience), and the two scattered method-choice associations don't survive scrutiny once tested against the rest of the battery.
