"""Matched (paired) rank-biserial correlation for Wilcoxon signed-rank,
Kerby (2014) simple-difference formula -- same value pingouin.wilcoxon reports
as "RBC", computed here from scipy.stats.rankdata directly instead of pingouin.
"""

import numpy as np
from scipy.stats import rankdata


def matched_rank_biserial(d):
    d = np.asarray(d, dtype=float)
    d = d[d != 0]
    ranks = rankdata(np.abs(d))
    r_plus = ranks[d > 0].sum()
    r_minus = ranks[d < 0].sum()
    return (r_plus - r_minus) / (r_plus + r_minus)
