"""
fig_crowning -- for each scale (protection, effort, benefit_loss), a grouped
bar chart with one group per qualifying method (n>=N_FLOOR in every scope)
and 3 bars per group: pooled / less / more (crowning.py's scope A / scope B).

Significance: only effort has ANY confirmed pairwise post-hoc result per
crowning.md -- "Delete this single conversation" significantly lower-effort
than "Delete a specific saved memory", in the pooled and less scopes only
(p_holm=.0002 both; NOT significant in the more scope, p_holm=.0781). That is
the only annotation drawn. Protection and benefit_loss are ns in every scope
(6/6 tests null) and get no stars, per crowning.md's own verdict.
"""

import numpy as np
import matplotlib.pyplot as plt

from src.screen import get_bases
from src.methods import SHORT_METHOD
from src.stats import SCEN

from .crowning import crown_scale, _scored, DIRECTION
from .pooling import pooled_method_scores

# Bumped 2026-08-25, revised four times, checked against an actual
# print-scale simulation each round (2026-08-26), not just an on-screen PNG
# preview (which doesn't reflect physical print shrink and gave false
# "looks fine" readings twice). Rounds 1-3 kept 3 panels side by side --
# with 4 groups of full verbatim 2-line method names, that layout never
# fits in a ~3.375in paper column at a font size that's simultaneously
# non-overlapping and readable, no matter the font/rotation tuning. Round 4
# stacks the 3 panels vertically instead (see plot_combined) so each one
# gets the full column width; figsize width dropped from 13in to 6in
# (~0.5625x shrink), letting ordinary font sizes work directly.
plt.rcParams.update({
    "font.size": 16,
    "legend.fontsize": 16,
})
TICK_FONTSIZE = 12
TITLE_FONTSIZE = 20
ANNOTATION_FONTSIZE = 18

# Consistent with src/method_selection.py's scenario colors (fig2): less
# sensitive = green, more sensitive = pink. Pooled gets a neutral third color.
COLORS = {"pooled": "#F2C230", "less": "#4C9F70", "more": "#B4436C"}
SCALE_TITLE = {"protection": "Protection", "effort": "Effort", "benefit_loss": "Benefit Loss"}
SCOPES = ["pooled", "less", "more"]

METHODS_ORDER = [
    "Delete this single conversation.",
    "Clear all conversation history.",
    "Delete a specific saved memory or fact.",
    "Type a message asking the AI Chatbot to forget it.",
]


def scope_results(bases):
    """{scale: {scope: crown_scale result}} for pooled/less/more."""
    out = {scale: {} for scale in DIRECTION}
    pooled = pooled_method_scores(bases)
    for scale, direction in DIRECTION.items():
        out[scale]["pooled"] = crown_scale(pooled, "method", scale, direction)

    for scen, (base, mcol) in SCEN.items():
        df = bases[scen]
        df = df[df[mcol] != "Other (Please specify)"]
        for scale, direction in DIRECTION.items():
            scored = _scored(df, base, scale)
            out[scale][scen] = crown_scale(scored, mcol, "_s", direction)
    return out


def _plot_ax(ax, scale, results):
    x = np.arange(len(METHODS_ORDER))
    w = 0.26

    for i, scope in enumerate(SCOPES):
        r = results[scope]
        vals = [r["medians"].get(m, np.nan) for m in METHODS_ORDER]
        bars = ax.bar(x + (i - 1) * w, vals, w, label=scope.capitalize(), color=COLORS[scope])

    if scale == "effort":
        i_single = METHODS_ORDER.index("Delete this single conversation.")
        for scope in ("pooled", "less"):  # more scope: ns, no star
            i = SCOPES.index(scope)
            xpos = x[i_single] + (i - 1) * w
            ypos = results[scope]["medians"][METHODS_ORDER[i_single]]
            ax.annotate("***", (xpos, ypos), textcoords="offset points",
                        xytext=(0, 6), ha="center", fontsize=ANNOTATION_FONTSIZE, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels([SHORT_METHOD[m] for m in METHODS_ORDER], fontsize=TICK_FONTSIZE,
                        rotation=0, ha="center")
    ax.set_ylim(0, 5.6)
    ax.set_ylabel("Median rating (1-5 Likert)", fontsize=TICK_FONTSIZE + 2)
    ax.set_title(SCALE_TITLE[scale], fontsize=TITLE_FONTSIZE, pad=8, loc="left")
    return bars


def plot_combined(all_results, path="outputs/figures/fig_crowning_combined.png"):
    # Stacked vertically (3 rows, 1 col), not side by side -- with 4 groups
    # of full verbatim 2-line method names, 3 panels sharing a single
    # column's width (~3.375in in the paper) never fit at a font size that
    # is both non-overlapping and actually readable (checked against a
    # print-scale simulation, not just an on-screen preview, 2026-08-26).
    # Stacking gives each panel the FULL column width instead of a third of
    # it -- pure matplotlib layout change, no LaTeX involved.
    fig, axes = plt.subplots(3, 1, figsize=(6, 13), gridspec_kw={"hspace": 0.55})
    scales = ("protection", "effort", "benefit_loss")
    for ax, scale in zip(axes, scales):
        _plot_ax(ax, scale, all_results[scale])

    handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS[s]) for s in SCOPES]
    fig.legend(handles, [s.capitalize() for s in SCOPES], loc="lower center",
               ncol=3, bbox_to_anchor=(0.5, -0.02), fontsize=TICK_FONTSIZE + 2)
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    return path


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    results = scope_results(bases)
    saved = plot_combined(results)
    print(f"saved -> {saved}")
