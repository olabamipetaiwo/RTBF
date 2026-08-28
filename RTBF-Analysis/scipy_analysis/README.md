# scipy_analysis

Scipy-only reimplementation of the `src/` statistical pipeline, built to cross-check
whether the results correlate with the original ("manual") pipeline. Reads the same
screened data via `src.screen.get_bases()` -- only the test/post-hoc/correction layer is
reimplemented here, replacing `statsmodels` (McNemar, Stuart-Maxwell, the ordinal trend
test, Holm/FDR correction), `pingouin` (Wilcoxon effect size, Cronbach's alpha), and
`scikit-posthocs` (Dunn's post-hoc) with hand-rolled `scipy.stats`/`numpy` equivalents.
`src/` and `outputs/` are untouched; this folder writes only to `scipy_analysis/outputs/`.

## Running

From the repo root, same convention as `src/`:

```bash
uv run python -m scipy_analysis.stats
uv run python -m scipy_analysis.verify
uv run python -m scipy_analysis.moderators
uv run python -m scipy_analysis.willingness
uv run python -m scipy_analysis.calibration_stats
uv run python -m scipy_analysis.reliability
uv run python -m scipy_analysis.mcnemar
uv run python -m scipy_analysis.global_correction
uv run python -m scipy_analysis.compare   # the comparison report
```

`compare.py` is the deliverable: it joins this pipeline's p-values against
`src.global_correction.collect_all_pvals`'s on `(family, label)` and reports Pearson r /
Spearman rho across all matched tests, plus any significance flips, in
`scipy_analysis/outputs/results/compare.md` and
`scipy_analysis/outputs/tables/compare_pvals.csv`.

## What to expect

Last run: **101 tests compared, Pearson r = 0.99997, Spearman rho = 0.99992, 0 significance
flips.** 73 rows match exactly; the other 28 differ by <0.02 for two understood reasons:

- **`verify.*` / `moderators.method_choice` rows**: scipy's own r x c `fisher_exact` is
  internally Monte-Carlo-randomized with no exposed seed, so these drift slightly even
  between two runs of the *same* code -- not a reimplementation discrepancy.
- **`stats.between_scenario_likert` / `willingness.scenario_shift` (Wilcoxon) rows**:
  `scipy.stats.wilcoxon`'s default continuity-correction setting differs slightly from
  pingouin's, producing a <0.002 p-value difference.

Kruskal-Wallis, Mann-Whitney, Shapiro-Wilk, and paired-t rows (already scipy in `src/`)
match exactly, as expected.

## Files

- `reporting.py` -- `save_report()`, same contract as `src/reporting.py` but writing to
  `scipy_analysis/outputs/results/`.
- `correction.py` -- Holm and BH-FDR correction (numpy).
- `dunn.py` -- Dunn's post-hoc test (`scipy.stats.rankdata` + `norm`).
- `mcnemar_scipy.py` -- exact/asymptotic McNemar (`scipy.stats.binomtest` / `chi2`).
- `effects.py` -- matched rank-biserial correlation for Wilcoxon.
- `stats.py`, `verify.py`, `moderators.py`, `willingness.py`, `calibration_stats.py`,
  `reliability.py`, `mcnemar.py`, `global_correction.py` -- one module per `src/`
  counterpart, same section numbering and `(family, label)` keys.
- `compare.py` -- the side-by-side comparison report.
