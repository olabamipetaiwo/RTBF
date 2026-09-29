"""
Independent cross-checks for src/pooled_gee.py's pooled between-method tests.

The project's other statistical results are cross-validated by a second,
scipy-only pipeline (scipy_analysis/). The pooled GEE has no scipy
counterpart (scipy has no GEE), so this module checks it with two methods
that share none of its machinery:

  1. Random-intercept linear mixed model (participant as the random effect),
     fitted by maximum likelihood, with a likelihood-ratio test for the method
     terms (full model vs. scenario-only model). This handles the same
     within-participant dependence through a different model class. It is more
     efficient than the GEE when its assumptions hold, so its p-values are
     expected to be smaller; agreement on WHICH scales show a method effect is
     what is being checked, not equality of p-values.
  2. Participant-cluster bootstrap of the raw effort mean differences: resample
     whole participants (both of their observations together) with replacement,
     recompute each method's mean effort, and take percentile intervals of the
     differences. No model at all, so it checks the GEE's point estimates and
     intervals directly. Because the GEE's independence-working-correlation
     estimates equal the observed group means (adjusted for scenario), the
     bootstrap differences should match the GEE contrasts closely.

Both run on the same 352-observation frame and the same four qualifying
methods as pooled_gee.py.
"""

import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

from src.pooled_gee import (
    SURVEY_XLSX, _model_frame, build_observation_frame, fit_gee, pairwise_contrasts,
    qualifying_methods,
)
from src.reporting import save_report
from src.screen import get_bases
from src.stats import SCALES

N_BOOT = 5_000
SEED = 42


def mixed_model_lrt(data: pd.DataFrame, scale: str) -> tuple[float, int, float]:
    """LR test for the method terms in a random-intercept model (ML fits)."""
    df = data["method"].nunique() - 1
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        full = smf.mixedlm(f"{scale} ~ C(method) + C(scenario)", data, groups="pid").fit(reml=False)
        reduced = smf.mixedlm(f"{scale} ~ C(scenario)", data, groups="pid").fit(reml=False)
    lr = 2 * (full.llf - reduced.llf)
    return lr, df, float(stats.chi2.sf(lr, df))


def cluster_bootstrap_diffs(data: pd.DataFrame, methods: list[str], scale: str,
                            n_boot: int = N_BOOT, seed: int = SEED) -> pd.DataFrame:
    """Percentile CIs for (reference method mean) minus (each other method's
    mean) of `scale`, resampling participants with all their observations."""
    pids = data["pid"].unique()
    sums = np.zeros((len(pids), len(methods)))
    counts = np.zeros_like(sums)
    row_of = {pid: i for i, pid in enumerate(pids)}
    for row in data.itertuples():
        i, j = row_of[row.pid], methods.index(row.method)
        sums[i, j] += getattr(row, scale)
        counts[i, j] += 1

    rng = np.random.default_rng(seed)
    draw = rng.integers(0, len(pids), size=(n_boot, len(pids)))
    with np.errstate(invalid="ignore", divide="ignore"):
        means = sums[draw].sum(axis=1) / counts[draw].sum(axis=1)     # (n_boot, n_methods)
    diffs = means[:, [0]] - means[:, 1:]
    rows = []
    for k, method in enumerate(methods[1:]):
        col = diffs[:, k]
        rows.append({"a": methods[0], "b": method, "boot_diff": np.nanmean(col),
                     "boot_ci_low": np.nanpercentile(col, 2.5), "boot_ci_high": np.nanpercentile(col, 97.5)})
    return pd.DataFrame(rows)


def main() -> None:
    bases = get_bases(path=SURVEY_XLSX, verbose=False)
    obs = build_observation_frame(bases["paired"])
    methods = qualifying_methods(obs)
    data = _model_frame(obs, methods)

    lines = ["=== Cross-checks for the pooled GEE (src/pooled_gee.py) ===",
             f"{len(obs)} observations, {obs['pid'].nunique()} participants; methods: {methods}",
             "", "-" * 70,
             "1. Random-intercept mixed model, likelihood-ratio test for method",
             "   (compare with the GEE Wald test in pooled_gee.md; agreement on which",
             "   scales show an effect is the check, not equality of p-values)", "-" * 70]
    for scale in SCALES:
        lr, df, p = mixed_model_lrt(data, scale)
        lines.append(f"  {scale:13} LR chi2({df})={lr:7.3f}  p={p:.4f}")

    lines += ["", "-" * 70,
              f"2. Effort: participant-cluster bootstrap ({N_BOOT:,} draws, seed {SEED}) vs GEE contrasts",
              "   diff = reference (single conversation) minus method; GEE contrast is adjusted for scenario",
              "-" * 70]
    gee, _, _ = fit_gee(data, "effort", sm.families.Gaussian())
    contrasts = pairwise_contrasts(gee, methods)
    contrasts = contrasts[contrasts["a"] == methods[0]].rename(columns={"diff": "gee_diff"})
    boot = cluster_bootstrap_diffs(data, methods, "effort")
    merged = boot.merge(contrasts[["a", "b", "gee_diff", "ci_low", "ci_high"]], on=["a", "b"])
    merged["method"] = merged["b"].str.slice(0, 44)
    lines.append(merged[["method", "gee_diff", "ci_low", "ci_high", "boot_diff",
                         "boot_ci_low", "boot_ci_high"]].round(3).to_string(index=False))

    print("\n".join(lines))
    print(f"\nreport saved -> {save_report('pooled_gee_crosscheck', lines)}")


if __name__ == "__main__":
    main()
