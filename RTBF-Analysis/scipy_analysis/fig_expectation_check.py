"""
fig_expectation_check -- expectation (Q4.4/Q5.4) and verification (Q4.5/Q5.5)
option shares for the rebuilt paper (Section 4.2, Figure "fig:expectation").

Same numbers as fig_expectation_verification.py (it reuses its family_rates:
overall = both scenarios pooled, one row per participant-scenario response,
n=354); what changes for the paper (2026-11-01):
  * option labels in plain words with the paper's terms ("agent", not
    "chatbot"), instead of the short analysis codes ("did NOT know how");
  * y-axis and legend say "responses" and "Both scenarios / Less sensitive /
    More sensitive";
  * two panels stacked (expectation above, verification below), vertical
    bars, drawn at the real width of one paper column (3.4 in, figure float).
"""

import textwrap

import matplotlib.pyplot as plt
import numpy as np

from src.screen import get_bases

from .expectation_rank import FAMILIES, SCEN, option_matrix
from .fig_crowning import COLORS
from .fig_expectation_verification import family_rates

LABELS = {
    "permanently deleted": "Permanently deleted from\ndatabase and backups",
    "not ref. future": "Not referenced in\nfuture conversations",
    "not ref. current": "Not referenced in\nthis conversation",
    "made invisible": "Made invisible\nto users",
    "not used for training": "No longer used\nfor training",
    "not sure": "Not sure what\nhappens",
    "other": "Other",
    "did NOT know how": "Did not know\nhow to check",
    "asked new convo": "Asked the agent in\na new conversation",
    "asked same convo": "Asked the agent in\nthe same conversation",
    "checked settings": "Checked memory or\nsaved-data settings",
    "checked UI": "Checked whether it\nwas still visible",
    "did NOT want to": "Did not want\nto check",
    "privacy-portal request": "Submitted a data\naccess request",
}
SCOPES = ["overall", "less", "more"]
SCOPE_COLOR = {"overall": COLORS["pooled"], "less": COLORS["less"], "more": COLORS["more"]}
SCOPE_LABEL = {"overall": "Both scenarios", "less": "Less sensitive", "more": "More sensitive"}
TITLE = {"expectation": "Expectation", "verification": "Verification"}


def plot(all_rates, path):
    # drawn at the real size of one paper column (3.4 in) so fonts print at 7 pt
    fig, axes = plt.subplots(2, 1, figsize=(3.4, 4.1))
    for ax, family in zip(axes, ("expectation", "verification")):
        rates = all_rates[family]
        labels = rates["overall"].index.tolist()
        x = np.arange(len(labels))
        w = 0.27
        for i, scope in enumerate(SCOPES):
            ax.bar(x + (i - 1) * w, rates[scope].values, w, color=SCOPE_COLOR[scope])
        ax.set_xticks(x)
        ax.set_xticklabels([LABELS[lab] for lab in labels],
                           fontsize=6, rotation=45, ha="right", rotation_mode="anchor", linespacing=0.95)
        ax.set_ylim(0, 70)
        ax.tick_params(axis="y", labelsize=7)
        ax.set_title(TITLE[family], fontsize=8, loc="left")
        ax.set_ylabel("% of responses", fontsize=7)
    handles = [plt.Rectangle((0, 0), 1, 1, color=SCOPE_COLOR[s]) for s in SCOPES]
    fig.legend(handles, [SCOPE_LABEL[s] for s in SCOPES], loc="lower center", ncol=3,
               fontsize=6.5, bbox_to_anchor=(0.5, 0.0), columnspacing=1.0, handlelength=1.2)
    fig.tight_layout(rect=(0, 0.03, 1, 1), h_pad=0.3)
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    all_rates = {fam: family_rates(bases, fam) for fam in FAMILIES}
    n_rows = sum(len(option_matrix(bases[s], f"{SCEN[s]}{FAMILIES['expectation'][0]}",
                                   FAMILIES["expectation"][1])) for s in SCEN)
    print("responses:", n_rows)
    for fam, rates in all_rates.items():
        print(fam, rates["overall"].round(1).to_dict())
    print("saved ->", plot(all_rates, "../paper/figures/fig_expectation.png"))
