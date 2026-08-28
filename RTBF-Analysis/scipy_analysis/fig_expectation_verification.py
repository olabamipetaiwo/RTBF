"""
fig_expectation_verification -- for expectation (Q4.4/Q5.4, 7 options) and
verification (Q4.5/Q5.5, 8 options), a grouped bar chart with one group per
option and 3 bars per group: overall / less / more.

"Overall" is recomputed directly from pooled raw responses -- the less- and
more-scenario binary selection matrices (expectation_rank.option_matrix) are
concatenated row-wise (n=177+178=355 scenario-instances) and the selection
rate is taken over that combined set, NOT an average of the two scenario
rates. Unlike crowning/pooling.py's method-pooling, no dedup is needed here:
each respondent's less- and more-scenario answers are legitimately about two
different contexts (their expectation/verification behavior under lower vs.
higher data sensitivity), not the same target counted twice.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.screen import get_bases

from .expectation_rank import SCEN, FAMILIES, option_matrix
from .fig_crowning import COLORS

# Bumped 2026-08-25, revised four times. Rounds 1-3 kept the figure at
# figsize width=13in (matching the other multi-panel figures) and tried to
# compensate via font size and a taller canvas -- this is the wrong lever:
# a 13in-wide source shrunk to a ~3.375in column is a ~0.26x reduction no
# matter what, and blowing up mpl font size to compensate needs unwieldy
# 30-40pt values that either overlap (round 1) or, if kept moderate,
# actually go too small on the printed page while the canvas grows
# needlessly tall (round 3, flagged 2026-08-26 -- verified against an
# actual compiled-paper screenshot, not just an on-screen PNG preview,
# which doesn't reflect physical print shrink at all). Round 4: shrink the
# SOURCE figure width toward the actual print target instead of fighting
# the ratio with font size. At width=9in the shrink factor is ~0.375x
# (matches src/sample.py's fig1, which reads fine at print scale), so
# ordinary matplotlib font sizes (18-29pt here) land in the readable range
# without needing extreme values or an oversized canvas.
plt.rcParams.update({
    "font.size": 18,
    "axes.labelsize": 24,
    "legend.fontsize": 21,
})
TICK_FONTSIZE = 21
TITLE_FONTSIZE = 29

SCOPES = ["overall", "less", "more"]
FAMILY_TITLE = {"expectation": "Expectation", "verification": "Verification"}


def family_rates(bases, family):
    q_suffix, opts = FAMILIES[family]
    mats = {scen: option_matrix(bases[scen], f"{SCEN[scen]}{q_suffix}", opts) for scen in SCEN}
    pooled = pd.concat(mats.values(), axis=0, ignore_index=True)

    rates = {
        "less": (mats["less"].sum(axis=0) / len(mats["less"]) * 100),
        "more": (mats["more"].sum(axis=0) / len(mats["more"]) * 100),
        "overall": (pooled.sum(axis=0) / len(pooled) * 100),
    }
    order = rates["overall"].sort_values(ascending=False).index
    return {scope: rates[scope].loc[order] for scope in SCOPES}


def plot_family(ax, family, rates):
    labels = rates["overall"].index.tolist()
    x = np.arange(len(labels))
    w = 0.26
    for i, scope in enumerate(SCOPES):
        color = COLORS["pooled"] if scope == "overall" else COLORS[scope]
        ax.bar(x + (i - 1) * w, rates[scope].values, w, label=scope.capitalize(), color=color)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=TICK_FONTSIZE, rotation=65, ha="right")
    ax.set_ylim(0, 100)
    ax.set_title(FAMILY_TITLE[family], fontsize=TITLE_FONTSIZE, pad=10)


def plot_combined(all_rates, path="outputs/figures/fig_expectation_verification.png"):
    fig, axes = plt.subplots(1, 2, figsize=(9, 10), gridspec_kw={"wspace": 0.2})
    for ax, family in zip(axes, ("expectation", "verification")):
        plot_family(ax, family, all_rates[family])
    axes[0].set_ylabel("% of scenario-instances selecting option")

    handles = [plt.Rectangle((0, 0), 1, 1, color=(COLORS["pooled"] if s == "overall" else COLORS[s]))
               for s in SCOPES]
    fig.legend(handles, [s.capitalize() for s in SCOPES], loc="lower center",
               ncol=3, bbox_to_anchor=(0.5, -0.3), fontsize=TICK_FONTSIZE + 2)
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    return path


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    all_rates = {family: family_rates(bases, family) for family in FAMILIES}
    saved = plot_combined(all_rates)
    print(f"saved -> {saved}")
