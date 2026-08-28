"""
Step 5: Method selection per scenario (Q4.2 vs Q5.2).
Fig 2: grouped bars, ONE shared method order across both scenarios
(sorted by combined frequency) so the less->more shift is readable.

Single-select, so counts sum to each scenario's n. "Other" dropped.
Paired base (n=177) used so both bars describe the same respondents.
"""

import textwrap

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.screen import get_bases
from src.reporting import save_report

# Bumped 2026-08-25, revised twice same day -- first attempt scaled purely
# by the LaTeX column-shrink factor and overlapped everything (7 full-length
# verbatim survey options at 32pt has nowhere to go in a 13in-wide figure).
# Settled on a smaller, layout-safe bump (~1.5x original) plus taller
# figsize and fixed legend/title placement so the extra text height and
# larger font actually fit.
plt.rcParams.update({
    "font.size": 15,
    "axes.titlesize": 17,
    "axes.labelsize": 15,
    "legend.fontsize": 12,
})
TICK_FONTSIZE = 12
VALUE_LABEL_FONTSIZE = 11

# Verbatim survey option text (Q4.2/Q5.2), wrapped for axis display -- not
# paraphrased/abbreviated, per feedback that figures must use the exact
# term used in the survey.
METHODS = [
    "Delete this single conversation.",
    "Clear all conversation history.",
    "Delete a specific saved memory or fact.",
    "Type a message asking the AI Chatbot to forget it.",
    "Clear all saved memories.",
    "Privacy dashboard or account-level data management page.",
    "Delete my account entirely.",
]


def _wrap(label, width=18):
    return "\n".join(textwrap.wrap(label, width=width))


def selection_counts(paired):
    less = paired["Q4.2"].value_counts()
    more = paired["Q5.2"].value_counts()
    methods = [m for m in METHODS if m in less.index or m in more.index]
    df = pd.DataFrame({
        "less": [int(less.get(m, 0)) for m in methods],
        "more": [int(more.get(m, 0)) for m in methods],
    }, index=[_wrap(m) for m in methods])
    return df.assign(total=lambda d: d["less"] + d["more"]) \
             .sort_values("total", ascending=False)


def plot(df, path="outputs/figures/fig2_method_selection.png"):
    order = df.drop(columns="total")
    x = np.arange(len(order)); w = 0.4
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.bar(x - w/2, order["less"], w, label="Less sensitive", color="#4C9F70")
    ax.bar(x + w/2, order["more"], w, label="More sensitive", color="#B4436C")
    ax.set_xticks(x); ax.set_xticklabels(order.index, fontsize=TICK_FONTSIZE)
    ax.set_ylabel("Participants selecting method")
    ax.set_title("Deletion method selection by scenario", pad=14)
    ax.set_ylim(top=max(order["less"].max(), order["more"].max()) * 1.15)
    ax.legend(loc="upper right")
    for i, (l, m) in enumerate(zip(order["less"], order["more"])):
        ax.text(i - w/2, l + 0.5, str(l), ha="center", fontsize=VALUE_LABEL_FONTSIZE)
        ax.text(i + w/2, m + 0.5, str(m), ha="center", fontsize=VALUE_LABEL_FONTSIZE)
    plt.tight_layout(); plt.savefig(path, dpi=200, bbox_inches="tight"); plt.close()
    return path


if __name__ == "__main__":
    paired = get_bases(verbose=False)["paired"]
    df = selection_counts(paired)

    lines = ["=== method selection counts (paired base) ===", df.to_string()]
    fig_path = plot(df)
    lines.append(f"\nsaved -> {fig_path}")

    for line in lines:
        print(line)

    report_path = save_report("method_selection", lines)
    print(f"\nreport saved -> {report_path}")
