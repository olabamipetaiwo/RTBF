"""
Step 5: Method selection per scenario (Q4.2 vs Q5.2).
Fig 2: grouped bars, ONE shared method order across both scenarios
(sorted by combined frequency) so the less->more shift is readable.

Single-select, so counts sum to each scenario's n. "Other" dropped.
Paired base (n=177) used so both bars describe the same respondents.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pipeline import get_bases

SHORT = {
    "Delete this single conversation.": "Delete single\nconversation",
    "Clear all conversation history.": "Clear all\nhistory",
    "Delete a specific saved memory or fact.": "Delete specific\nmemory",
    "Type a message asking the AI Chatbot to forget it.": "Ask chatbot\nto forget",
    "Clear all saved memories.": "Clear all\nmemories",
    "Privacy dashboard or account-level data management page.": "Privacy\ndashboard",
    "Delete my account entirely.": "Delete\naccount",
}


def selection_counts(paired):
    less = paired["Q4.2"].value_counts()
    more = paired["Q5.2"].value_counts()
    methods = [m for m in SHORT if m in less.index or m in more.index]
    df = pd.DataFrame({
        "less": [int(less.get(m, 0)) for m in methods],
        "more": [int(more.get(m, 0)) for m in methods],
    }, index=[SHORT[m] for m in methods])
    return df.assign(total=lambda d: d["less"] + d["more"]) \
             .sort_values("total", ascending=False)


def plot(df, path="outputs/figures/fig2_method_selection.png"):
    order = df.drop(columns="total")
    x = np.arange(len(order)); w = 0.4
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - w/2, order["less"], w, label="Less sensitive", color="#4C9F70")
    ax.bar(x + w/2, order["more"], w, label="More sensitive", color="#B4436C")
    ax.set_xticks(x); ax.set_xticklabels(order.index, fontsize=9)
    ax.set_ylabel("Respondents selecting method")
    ax.set_title("Deletion method selection by scenario (shared order)")
    ax.legend()
    for i, (l, m) in enumerate(zip(order["less"], order["more"])):
        ax.text(i - w/2, l + 0.5, str(l), ha="center", fontsize=8)
        ax.text(i + w/2, m + 0.5, str(m), ha="center", fontsize=8)
    plt.tight_layout(); plt.savefig(path, dpi=200, bbox_inches="tight"); plt.close()
    return path


if __name__ == "__main__":
    paired = get_bases(verbose=False)["paired"]
    df = selection_counts(paired)
    print("=== method selection counts (paired base) ===")
    print(df.to_string())
    print(f"\nsaved -> {plot(df)}")



#     ┌────────────────────────────┬──────┬──────┬───────┐
# │           method           │ less │ more │ total │
# ├────────────────────────────┼──────┼──────┼───────┤
# │ Delete single conversation │ 84   │ 80   │ 164   │
# ├────────────────────────────┼──────┼──────┼───────┤
# │ Clear all history          │ 33   │ 40   │ 73    │
# ├────────────────────────────┼──────┼──────┼───────┤
# │ Delete specific memory     │ 19   │ 22   │ 41    │
# ├────────────────────────────┼──────┼──────┼───────┤
# │ Ask chatbot to forget      │ 25   │ 14   │ 39    │
# ├────────────────────────────┼──────┼──────┼───────┤
# │ Clear all memories         │ 7    │ 8    │ 15    │
# ├────────────────────────────┼──────┼──────┼───────┤
# │ Privacy dashboard          │ 6    │ 9    │ 15    │
# ├────────────────────────────┼──────┼──────┼───────┤
# │ Delete account             │ 2    │ 3    │ 5     │
# └────────────────────────────┴──────┴──────┴───────┘



# - "Delete single conversation" dominates regardless of sensitivity — ~48% (84/176) in less-sensitive, ~45% (80/176) in more-sensitive. It's the default choice by a wide margin in both scenarios, consistent with the effort finding from stats.py (it's the significantly lowest-effort method).
# - Biggest raw shift: "Ask chatbot to forget" drops nearly in half (25→14, -44%) as sensitivity rises, while "Clear all history" rises the most (33→40, +21%) and "Privacy dashboard" nearly doubles proportionally (6→9, +50%, though tiny n). Directionally, that reads like: when data feels more sensitive, fewer people trust a conversational request ("hey, forget this") and more lean toward a systemic/bulk action.

# Caveat — don't overclaim this: this directional pattern is exactly what stats.py step 6 (Stuart-Maxwell) already tested formally, on this same paired distribution, and it came back ns (p=.393). So while "ask chatbot to forget" losing 11 of its 25 people is a striking-looking raw number, the aggregate test says the overall 7-category distribution shift isn't statistically distinguishable from chance reshuffling at n=176. Treat these counts as the descriptive backdrop for that already-tested null, not a new finding — the formal answer here is still "no confirmed systematic shift in method choice with sensitivity."