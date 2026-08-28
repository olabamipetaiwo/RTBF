"""Dunn's post-hoc test (pooled ranks across all kept groups), implemented
from scipy.stats.rankdata + scipy.stats.norm, replacing scikit_posthocs.posthoc_dunn.
Formula: Dunn (1964), z-test on pooled mean ranks with a tie correction; see
Dinno (2015) "Nonparametric Pairwise Multiple Comparisons" for the same form
scikit-posthocs implements.
"""

import itertools
import numpy as np
import pandas as pd
from scipy.stats import rankdata, norm

from .correction import holm


def dunn_test(data: pd.DataFrame, val_col: str, group_col: str) -> pd.DataFrame:
    groups = sorted(data[group_col].unique())
    x = data[val_col].to_numpy(dtype=float)
    g = data[group_col].to_numpy()
    N = len(x)

    ranks = rankdata(x)
    _, tie_counts = np.unique(x, return_counts=True)
    tie_sum = np.sum(tie_counts ** 3 - tie_counts)

    n = {grp: int((g == grp).sum()) for grp in groups}
    rbar = {grp: ranks[g == grp].mean() for grp in groups}

    pairs = list(itertools.combinations(groups, 2))
    pvals = []
    for g1, g2 in pairs:
        sigma = np.sqrt(
            ((N * (N + 1) / 12) - tie_sum / (12 * (N - 1))) * (1 / n[g1] + 1 / n[g2])
        )
        z = (rbar[g1] - rbar[g2]) / sigma
        pvals.append(2 * norm.sf(abs(z)))

    padj = holm(pvals)
    mat = pd.DataFrame(np.ones((len(groups), len(groups))), index=groups, columns=groups)
    for (g1, g2), pa in zip(pairs, padj):
        mat.loc[g1, g2] = pa
        mat.loc[g2, g1] = pa
    return mat
