"""
fig_crowning -- for each scale (protection, effort, benefit_loss), a grouped
bar chart with one group per qualifying method (n>=N_FLOOR in every scope)
and 3 bars per group: pooled / less / more (crowning.py's scope A / scope B).

Pooled scope (revised 2026-09-23, paper review item N4): medians are now
computed over participant-scenario observations (one row per participant per
scenario, 352 rows, no stayer averaging), the same unit of analysis as the
pooled GEE tests in src/pooled_gee.py. The earlier version took medians from
pooling.pooled_method_scores, which averaged stayers' two responses into one
half-step value and put switchers in two groups; see src/pooled_gee.py for why
that pooling was replaced.

Significance: only effort has a pairwise post-hoc result that the figure
annotates -- "Delete this single conversation" significantly lower-effort
than "Delete a specific saved memory", in the pooled scope (participant-
clustered GEE contrast, p_holm=.0002; see pooled_gee.md) and the less scope
(Dunn, p_holm=.0002); NOT significant in the more scope. The pooled GEE also
finds single-conversation lower-effort than "Clear all history" (p_holm=.019),
which is reported in the paper text, not drawn here. Protection and
benefit_loss have no significant omnibus test in any scope and get no stars.
"""

import numpy as np
import matplotlib.pyplot as plt

from src.methods import SHORT_METHOD
from src.pooled_gee import SURVEY_XLSX, build_observation_frame, qualifying_methods
from src.screen import get_bases
from src.stats import SCEN

from .crowning import crown_scale, _scored, DIRECTION

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
    obs = build_observation_frame(bases["paired"])
    pooled = obs[obs["method"].isin(qualifying_methods(obs))]
    for scale in DIRECTION:
        # Only "medians" is read by _plot_ax; no KW here (the pooled test is the GEE).
        out[scale]["pooled"] = {"medians": pooled.groupby("method")[scale].median().to_dict()}

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
        # Stagger the two annotations vertically: adjacent bars are narrower
        # than a "***" run, and once pooled and less share the same median
        # (both 1.5 with observation-level pooling) same-height stars merge
        # into an unreadable "*****".
        for row, scope in enumerate(("pooled", "less")):  # more scope: ns, no star
            i = SCOPES.index(scope)
            xpos = x[i_single] + (i - 1) * w
            ypos = results[scope]["medians"][METHODS_ORDER[i_single]]
            ax.annotate("***", (xpos, ypos), textcoords="offset points",
                        xytext=(0, 6 + 24 * row), ha="center", fontsize=ANNOTATION_FONTSIZE, fontweight="bold")

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
    bases = get_bases(path=SURVEY_XLSX, verbose=False)
    results = scope_results(bases)
    saved = plot_combined(results)
    print(f"saved -> {saved}")
