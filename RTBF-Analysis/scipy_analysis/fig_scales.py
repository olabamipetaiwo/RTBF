"""
fig_scales -- mean protection, effort, and benefit-loss ratings for the four
most chosen data deletion methods (paper Section 4.2, Figure "fig:scales").

Replaces fig_crowning.py's output for the rebuilt paper (2026-11-01):
  * bars show MEANS, not medians, because the paper text quotes means
    (user_study.md "PER-METHOD MEANS"; the scales are 3-5 item averages, so a
    median hides most of the variation);
  * no significance stars -- the text reports the tests;
  * method labels use the paper's own term ("deletion-request prompt"), not
    the survey wording "ask chatbot to forget" (terms.txt);
  * three panels side by side for a full-width float (figure*), not stacked
    for a single column.

Same unit as the pooled GEE (src/pooled_gee.py): one row per participant per
scenario, methods restricted to qualifying_methods(), "Other" dropped.
"""

import matplotlib.pyplot as plt
import numpy as np

from src.pooled_gee import SURVEY_XLSX, build_observation_frame, qualifying_methods
from src.screen import get_bases

from .crowning import DIRECTION

METHODS = [
    ("Delete this single conversation.", "Single\nconver-\nsation"),
    ("Clear all conversation history.", "All\nhistory"),
    ("Delete a specific saved memory or fact.", "Saved\nmemory"),
    ("Type a message asking the AI Chatbot to forget it.", "Deletion-\nrequest\nprompt"),
]
SCALE_TITLE = {"protection": "Protection", "effort": "Effort", "benefit_loss": "Benefit loss"}
COLORS = {"all": "#F2C230", "less": "#4C9F70", "more": "#B4436C"}
LEGEND = {"all": "Both scenarios", "less": "Less sensitive", "more": "More sensitive"}


def method_means(obs, scale):
    """{scope: {method: mean}} for both scenarios pooled and for each scenario."""
    sub = obs[obs["method"].isin(qualifying_methods(obs))]
    scopes = {"all": sub}
    for scen in ("less", "more"):
        scopes[scen] = sub[sub["scenario"] == scen]
    return {k: v.groupby("method")[scale].mean().to_dict() for k, v in scopes.items()}


def plot(obs, path):
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.9), sharey=True)
    x = np.arange(len(METHODS))
    w = 0.26
    for ax, scale in zip(axes, DIRECTION):
        means = method_means(obs, scale)
        for i, scope in enumerate(("all", "less", "more")):
            vals = [means[scope].get(m, np.nan) for m, _ in METHODS]
            ax.bar(x + (i - 1) * w, vals, w, color=COLORS[scope], label=LEGEND[scope])
        ax.set_xticks(x)
        ax.set_xticklabels([lab for _, lab in METHODS], fontsize=9)
        ax.set_title(SCALE_TITLE[scale], fontsize=13, loc="left")
        ax.set_ylim(1, 5)
    axes[0].set_ylabel("Mean rating (1 to 5)", fontsize=11)
    handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS[s]) for s in COLORS]
    fig.legend(handles, [LEGEND[s] for s in COLORS], loc="lower center", ncol=3,
               fontsize=11, bbox_to_anchor=(0.5, -0.14))
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


if __name__ == "__main__":
    bases = get_bases(path=SURVEY_XLSX, verbose=False)
    obs = build_observation_frame(bases["paired"])
    means = {s: method_means(obs, s) for s in DIRECTION}
    for scale, by_scope in means.items():
        print(scale, {m[:12]: round(v, 2) for m, v in by_scope["all"].items()})
    kept = obs[obs["method"].isin(qualifying_methods(obs))]
    print("choices:", len(kept), "participants per method:",
          kept.groupby("method")["pid"].nunique().to_dict())
    print("saved ->", plot(obs, "../paper/figures/fig_scales.png"))
