"""
Confidence intervals for the paper's headline scenario-shift effect sizes
(willingness, protection, effort, benefit_loss: less-sensitive vs
more-sensitive, paired n=177), added in response to paper review item 5
("confidence intervals" was one of the reviewer's specifically named gaps
alongside aggregation rules/missingness/multiplicity, which were already
covered elsewhere).

Wilcoxon signed-rank (used for all four scales per stats.py/willingness.py's
own Shapiro-Wilk normality check on the difference scores) has no simple
closed-form CI for the mean paired difference the paper actually reports
(the Δ values in Results), so this uses a percentile bootstrap over
participants: resample the n=177 paired differences with replacement,
recompute the mean, repeat 10,000 times, take the 2.5th/97.5th percentiles.
Seeded (np.random.default_rng(42)) for reproducibility -- rerunning this
script reproduces the exact same interval bounds.

This does not replace src/stats.py's between_scenario_likert or
willingness.py's scenario_shift; it reuses their exact same difference
series (same base, same scale_score/WILLING mapping) and adds only the
interval estimate those didn't compute.
"""

import numpy as np

from src.screen import get_bases
from src.reporting import save_report
from src.stats import scale_score, SCALES
from src.willingness import WILLING

N_BOOT = 10_000
SEED = 42
ALPHA = 0.05


def bootstrap_ci_mean(diffs: np.ndarray, n_boot: int = N_BOOT, seed: int = SEED, alpha: float = ALPHA):
    """Percentile bootstrap CI for the mean of paired differences."""
    rng = np.random.default_rng(seed)
    diffs = np.asarray(diffs, dtype=float)
    n = len(diffs)
    boot_means = np.empty(n_boot)
    for i in range(n_boot):
        boot_means[i] = rng.choice(diffs, size=n, replace=True).mean()
    lo, hi = np.percentile(boot_means, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(lo), float(hi)


def willingness_diffs(paired):
    less = paired["Q4.10"].map(WILLING)
    more = paired["Q5.10"].map(WILLING)
    m = pd_concat_dropna(less, more)
    return (m["more"] - m["less"]).values


def pd_concat_dropna(less, more):
    import pandas as pd
    m = pd.concat([less, more], axis=1)
    m.columns = ["less", "more"]
    return m.dropna()


def scale_diffs(paired, q, k):
    less = scale_score(paired, "Q4", q, k)
    more = scale_score(paired, "Q5", q, k)
    d = (more - less).dropna()
    return d.values


SURVEY_XLSX = "survey/RTBF_September+9,+2026_14.25.xlsx"


def main():
    bases = get_bases(path=SURVEY_XLSX, verbose=False)
    paired = bases["paired"]

    lines = ["=== Bootstrap 95% CIs for headline scenario-shift mean differences ===",
             f"(percentile bootstrap, n_boot={N_BOOT}, seed={SEED}, paired n={len(paired)})", ""]

    w = willingness_diffs(paired)
    lo, hi = bootstrap_ci_mean(w)
    lines.append(f"willingness    : mean_diff={w.mean():+.3f}  95% CI [{lo:+.3f}, {hi:+.3f}]  n={len(w)}")

    for scale, (q, k) in SCALES.items():
        d = scale_diffs(paired, q, k)
        lo, hi = bootstrap_ci_mean(d)
        lines.append(f"{scale:14} : mean_diff={d.mean():+.3f}  95% CI [{lo:+.3f}, {hi:+.3f}]  n={len(d)}")

    for line in lines:
        print(line)

    report_path = save_report("effect_cis", lines)
    print(f"\nreport saved -> {report_path}")


if __name__ == "__main__":
    main()
