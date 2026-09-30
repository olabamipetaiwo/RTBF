"""
Spearman correlations between the three rating scales (protection, effort,
benefit loss), the source for the paper's sentence on how strongly the
scales are related (Results, measurement model).

Base: the paired analysis sample from src/screen.py (n=177 participants,
each rating both scenarios). Scale scores use src/stats.py's scale_score and
SCALES, the same scoring as every other scale result in the paper.

Two views are reported:
  * pooled: the 177 participants' two scenario ratings stacked into 354
    participant-scenario observations, matching the factor analysis base.
    Its p-values treat the 354 rows as independent although each participant
    contributes two, so they overstate the evidence and are shown for
    reference only.
  * per scenario (n=177 each): one row per participant, so the p-values are
    valid. These are the ones to cite for significance.

Spearman rather than Pearson because the scale scores are bounded,
discrete means of Likert items and not normally distributed
(src/stats.py's Shapiro-Wilk checks).
"""

from itertools import combinations

import pandas as pd
from scipy import stats

from src.reporting import save_report
from src.screen import get_bases
from src.stats import SCALES, scale_score

SCENARIOS = {"less-sensitive": "Q4", "more-sensitive": "Q5"}


def scenario_scores(paired: pd.DataFrame, base: str) -> pd.DataFrame:
    """One row per participant, one column per scale, for a scenario."""
    return pd.DataFrame(
        {name: scale_score(paired, base, q, k) for name, (q, k) in SCALES.items()}
    )


def correlation_rows(scores: pd.DataFrame, label: str) -> list[str]:
    n = len(scores)
    lines = [f"\n{label} (n={n})"]
    for a, b in combinations(SCALES, 2):
        rho, p = stats.spearmanr(scores[a], scores[b])
        lines.append(f"  {a} x {b}: rho={rho:+.3f}  p={p:.4f}")
    return lines


def main() -> None:
    paired = get_bases(verbose=False)["paired"]
    per_scenario = {s: scenario_scores(paired, base) for s, base in SCENARIOS.items()}
    pooled = pd.concat(per_scenario.values(), ignore_index=True)

    lines = [
        f"paired base n = {len(paired)}; pooled observations = {len(pooled)}",
        "Spearman rank correlations between scale scores",
        "(pooled p-values treat two rows per participant as independent: reference only)",
    ]
    lines += correlation_rows(pooled, "POOLED")
    for scenario, scores in per_scenario.items():
        lines += correlation_rows(scores, scenario.upper())

    for line in lines:
        print(line)
    print(f"report saved -> {save_report('scale_correlations', lines)}")


if __name__ == "__main__":
    main()
