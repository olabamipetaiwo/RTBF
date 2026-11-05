# Method x scenario interaction: plan to add it to the paper

Status (2026-11-04): analysis run and saved; nothing added to the paper. The user is still deciding and will ask in a later session.

## What was run

- Script: `RTBF-Analysis/src/method_by_scenario.py`
- Report: `RTBF-Analysis/outputs/results/method_by_scenario.md`
- Tables: `RTBF-Analysis/outputs/tables/method_by_scenario_tests.csv`, `method_by_scenario_shift_{protection,effort,benefit_loss}.csv`
- Model: scale ~ method * scenario, Gaussian GEE clustered on participant, independence working correlation, robust SEs; 317 responses, four methods with at least 14 participants (105, 50, 30, 29). Reproduces the paper's between-method test (effort chi2(3) = 23.05, benefit loss 6.94, protection p = .29).
- Reason: Yao Li's table (2026-10-07 screenshot) asks for per-method LS / MS / Pooled means, a per-method scenario difference, and a between-methods and between-scenarios test, via GEE with a method x scenario interaction or ART ANOVA. The paper's between-method GEE uses scenario only as a covariate, so it assumes the LS to MS shift is equal for all methods.

## Results

Joint Wald test of the interaction (df = 3), Holm across the 3 scales:

| Scale | chi2 | p raw | p Holm | p exchangeable | p ART check |
|---|---|---|---|---|---|
| Protection | 1.39 | .71 | 1.00 | .78 | .52 |
| Effort | 8.11 | .044 | .13 | .097 | .23 |
| Benefit loss | 1.22 | .75 | 1.00 | .73 | .82 |

MS minus LS within each method (scale points; Holm across the 4 methods within each scale):

| Method | Protection | Effort | Benefit loss |
|---|---|---|---|
| Single conversation | +0.19 (p Holm .036) | +0.04 | +0.06 |
| Clear all history | +0.01 | +0.20 | +0.08 |
| Specific saved memory | +0.13 | -0.38 | -0.17 |
| Ask to forget | +0.05 | -0.32 | 0.00 |

Reading: no detected difference in the scenario shift across methods; only one within-method change is significant (protection, single conversation, the largest group). A significant change in one method beside nonsignificant changes in others does not show the methods differ. The ART check is a manual aligned-rank-transform with the clustered GEE on the ranks, not ARTool output. No confidence intervals (Yao Li decision, 2026-10-07); standard errors are shown instead.

## Plan if added to the paper (user wants the table and the findings in the main text)

1. Section 4.2: add a full-width table `tab:scale-by-scenario` in Yao Li's layout (row per method; for each scale Pooled, LS, MS, MS minus LS; asterisk on the one significant change; last row with the Holm-adjusted interaction test). Caption: "Mean ratings of protection, effort, and benefit loss by data deletion method, pooled and in the less (LS) and more (MS) sensitive scenarios, with the change from LS to MS (317 responses from 105, 50, 30, and 29 participants). Ratings use five-point agreement scales. An asterisk marks a change with $p_{\mathrm{Holm}}<.05$ across the four methods. The last row gives the Holm-adjusted test of the method-by-scenario interaction."
   Text after the existing effort/protection sentence: "The change from LS to MS did not differ detectably between the four methods (method-by-scenario interaction: protection $p_{\mathrm{Holm}}=1.0$, effort $p_{\mathrm{Holm}}=.13$, benefit loss $p_{\mathrm{Holm}}=1.0$; Table~\ref{tab:scale-by-scenario}). Within methods, only protection for deleting a single conversation changed, rising by 0.19 points in MS ($p_{\mathrm{Holm}}=.036$), and a change in one method beside no detected change in the others does not show that the methods differ."
2. Design (Section 3), statistics paragraph: one sentence saying we also tested whether the change from LS to MS differed between methods, with a method-by-scenario interaction in the same models.
3. Appendix `tab:analysis-families`: two new rows. (a) Protection, effort, benefit loss, method x scenario; Gaussian GEE with interaction, clustered by participant (joint Wald, 3 df); 317 responses, 4 methods; Holm family: the 3 scales. (b) Protection, effort, benefit loss, less vs more within each method; GEE contrasts from the interaction model; 317 responses, 4 methods; Holm family: the 4 methods, within each scale.
4. Supporting work: add the new numbers to `src/number_sources.py` (exceptions list must stay empty); add a test for `src/method_by_scenario.py` under `RTBF-Analysis/tests/`; add the two families to `src/global_correction.py` (pools about 100 tests) and rerun it, checking whether the paper cites its totals.
5. After every edit: run `python3 -I terms_lint.py` from `paper/`; check every number against the saved outputs; show wording first and apply one task at a time. No change needed to Limitations (they already say a nonsignificant result means no detected difference).

## Open decision

Figure 3 (`fig:scales`) shows the same means (pooled, LS, MS per method). Replace it with the table (recommended: saves space, and Figure 3 is the figure that kept floating to the end of the paper) or keep both (takes more room; page count could not be checked). Alternative layouts considered: table in the appendix with one pointer sentence in 4.2, and mentioning the single-conversation result only in the appendix.
