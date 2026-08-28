"""
fig10 -- explicit ranking of task 4's method-choice-shift table (mcnemar.py's
per_method_shift, already fully computed: less->more McNemar per method +
Holm across 7). The only genuinely new piece per tasks.md's own framing: the
existing table isn't sorted by shift magnitude, just the method list's fixed
order. This re-sorts by net shift (added - dropped, descending) and adds a
net-shift bar chart colored by sig/ns. No new statistics.

Honest headline (already established in mcnemar.md/stats.md): none of the 7
per-method shifts survive Holm correction -- closest is "Type a message
asking the AI Chatbot to forget it" (p_holm=.1345), which also happens to be
the single largest net decliner (net=-11). The chart will show every bar in
the same "ns" grey -- that's the correct, honest picture, not a bug.
"""

import matplotlib.pyplot as plt

from src.screen import get_bases

from .reporting import save_report
from .mcnemar import per_method_shift

# Bumped 2026-08-25 per advisor feedback: figure label/tick text was too
# small to read at paper column width.
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
})
TICK_FONTSIZE = 11

SIG_COLOR = "#B4436C"
NS_COLOR = "#999999"


def ranked_shift(paired):
    """per_method_shift(), resorted by net = added - dropped, descending."""
    out = per_method_shift(paired).copy()
    out["net"] = out["added"] - out["dropped"]
    return out.sort_values("net", ascending=False).reset_index(drop=True)


def plot_net_shift(ranked, path="outputs/figures/fig10_method_shift_ranking.png"):
    fig, ax = plt.subplots(figsize=(8, 5))
    y = range(len(ranked))
    colors = [SIG_COLOR if s == "*" else NS_COLOR for s in ranked["sig"]]
    ax.barh(y, ranked["net"], color=colors)
    ax.set_yticks(y); ax.set_yticklabels(ranked["method"], fontsize=TICK_FONTSIZE)
    ax.invert_yaxis()  # biggest gainer at top
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Net shift (added - dropped), less -> more sensitive")
    ax.set_title("Method choice shift ranking (McNemar + Holm; none survive correction)")
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight"); plt.close()
    return path


if __name__ == "__main__":
    paired = get_bases(verbose=False)["paired"]
    ranked = ranked_shift(paired)

    lines = [
        "=== Method choice shift, RANKED by net (added - dropped) ===",
        ranked.to_string(index=False),
        "\nnet = added - dropped (positive = net gain in popularity, negative = net loss)",
        "None survive Holm correction (sig column empty for all 7) -- ranking shows",
        "magnitude of raw shift, not statistical significance.",
    ]

    fig_path = plot_net_shift(ranked)
    lines.append(f"\nsaved -> {fig_path}")

    for line in lines:
        print(line)

    report_path = save_report("fig10_method_shift_ranking", lines)
    print(f"\nreport saved -> {report_path}")
