"""
fig7_cost_benefit -- replaces src/methods.py's plot_cost_benefit(). Same 3
scales (protection, effort, benefit_loss), but restructured per method: 3
bars per method -- overall (pooled), less-sensitive, more-sensitive -- instead
of 2 scenario subplots colored by scale. Purely descriptive (means, no
significance testing) -- reuses fig_crowning.scope_results() for the
mean/scope computation so numbers match crowning.md exactly, but draws no
stars here (that's fig_crowning_combined.png's job).
"""

import numpy as np
import matplotlib.pyplot as plt

from src.screen import get_bases
from src.methods import SHORT_METHOD

from .fig_crowning import scope_results, METHODS_ORDER, SCOPES, COLORS, SCALE_TITLE

# Bumped 2026-08-25 per advisor feedback: figure label/tick text was too
# small to read at paper column width.
plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 13,
    "legend.fontsize": 11,
})
TICK_FONTSIZE = 11
TITLE_FONTSIZE = 14


def plot_combined(all_results, path="outputs/figures/fig7_method_cost_benefit.png"):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5), sharey=True)
    x = np.arange(len(METHODS_ORDER))
    w = 0.26

    for ax, scale in zip(axes, ("protection", "effort", "benefit_loss")):
        results = all_results[scale]
        for i, scope in enumerate(SCOPES):
            vals = [results[scope]["means"].get(m, np.nan) for m in METHODS_ORDER]
            ax.bar(x + (i - 1) * w, vals, w, label=scope.capitalize(), color=COLORS[scope])
        ax.set_xticks(x)
        ax.set_xticklabels([SHORT_METHOD[m] for m in METHODS_ORDER], fontsize=TICK_FONTSIZE)
        ax.set_ylim(0, 5)
        ax.set_title(SCALE_TITLE[scale], fontsize=TITLE_FONTSIZE)

    axes[0].set_ylabel("Mean rating (1-5 Likert)")
    handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS[s]) for s in SCOPES]
    fig.legend(handles, [s.capitalize() for s in SCOPES], loc="lower center",
               ncol=3, bbox_to_anchor=(0.5, -0.04))
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    return path


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    results = scope_results(bases)
    saved = plot_combined(results)
    print(f"saved -> {saved}")
