 Abstract — one-paragraph summary of study + top findings
 Introduction — motivation, gap, research questions (RQs)
 Methodology — survey design, screening/sample (global.md §0), scale
liability, two-pipeline validation approach (statsmodels/pingouin/
ikit-posthocs vs. scipy-only cross-check)



Results — Sample & Knowledge — demographics, chatbot experience,
jective knowledge check (§0) - Done 

Results — Method Usage & Cost/Benefit Ratings — selection counts,
otection/effort/benefit_loss means per method (§A1/§B3-B4) - Done 

Results — Is Any Method Statistically Best? — Kruskal-Wallis + Dunn's
owning analysis, pooled and per-scenario (§A2/§B5). - Done

Results — Discriminant Validity — protection/effort/benefit_loss as
 separate constructs (§B2). Reported as a lower-triangular correlation
 matrix (rows/cols = protection, effort, benefit_loss; diagonal and upper
 triangle blank; cell = Spearman ρ with significance stars, e.g. .305***),                                                                          matching the format the user provided as a reference screenshot — not the
 plain results table currently in global.md §B2. Scope: pooled only
 (ρ: protection~effort=-0.057, protection~benefit_loss=0.129,
 effort~benefit_loss=0.305, p_holm=.0003 → ***), one table, per user
 confirmation. - Done



 8. Results — Scenario Sensitivity Effects — willingness/protection rise,
 effort/benefit_loss don't (§A2/§A4) - Done

 9. Results — Method Switching Behavior — Stuart-Maxwell, per-method
 McNemar, ranked shift (§A2 step 6/§B9) - Done


 10. Results — Expectations & Verification — within-scenario ranking,
 between-method differences, training-data blind spot (§A3/§B7/§B8) - Done

 11. Results — Calibration — confidence vs. verification, used-vs-ideal
 method gaps (§A7) - Done

 12. Results — Moderators — age, chatbot tenure effects (§A5) - Done


 13. Discussion — synthesis across findings, implications for chatbot/AI
 product design
 14. Limitations — sample skew, underpowered subgroups, McNemar power caveats
 15. Conclusion
 16. Cross-validation note (methods appendix or footnote) — the two-pipeline
 agreement (§ Cross-validation), likely folded into Methodology (#3) rather
 than standalone


 15. Conclusion
 16. Cross-validation note (methods appendix or footnote) — the two-pipeline
 agreement (§ Cross-validation), likely folded into Methodology (#3) rather
 than standalone



 <!-- end of session - whcih oth the figures have we not touched -->