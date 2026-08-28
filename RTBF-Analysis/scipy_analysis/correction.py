"""Holm step-down and Benjamini-Hochberg FDR correction, implemented by hand
with numpy so scipy_analysis never has to import statsmodels.stats.multitest.
Both match statsmodels.stats.multitest.multipletests(method="holm"/"fdr_bh").
"""

import numpy as np


def holm(pvals):
    p = np.asarray(pvals, dtype=float)
    m = len(p)
    order = np.argsort(p)
    sorted_p = p[order]
    adj = np.empty(m)
    running_max = 0.0
    for i in range(m):
        val = min((m - i) * sorted_p[i], 1.0)
        running_max = max(running_max, val)
        adj[i] = running_max
    out = np.empty(m)
    out[order] = adj
    return out


def bh_fdr(pvals):
    p = np.asarray(pvals, dtype=float)
    m = len(p)
    order = np.argsort(p)
    sorted_p = p[order]
    ranks = np.arange(1, m + 1)
    adj = sorted_p * m / ranks
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    adj = np.clip(adj, 0, 1)
    out = np.empty(m)
    out[order] = adj
    return out
