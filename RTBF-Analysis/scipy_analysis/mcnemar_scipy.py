"""McNemar test implemented on scipy primitives only, mirroring
statsmodels.stats.contingency_tables.mcnemar's two branches:
  exact  -> two-sided exact binomial test on the discordant pairs
  approx -> chi-square with continuity correction, 1 df
"""

from scipy.stats import binomtest, chi2


def mcnemar_p(table, exact=None):
    """table = [[a, b], [c, d]]; b, c are the discordant cells."""
    b, c = table[0][1], table[1][0]
    discordant = b + c
    if exact is None:
        exact = discordant < 25

    if discordant == 0:
        return 0.0, 1.0

    if exact:
        stat = min(b, c)
        p = binomtest(stat, discordant, 0.5, alternative="two-sided").pvalue
    else:
        stat = (abs(b - c) - 1) ** 2 / discordant
        p = chi2.sf(stat, 1)
    return stat, p
