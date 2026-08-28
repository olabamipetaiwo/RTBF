"""
Step 3: Per-method scale scores, each scenario.
Mean/median/SD of protection, effort, benefit_loss by deletion method
(Q4.2 less-sensitive, Q5.2 more-sensitive). Reports per-method n and
flags methods below the reporting floor.

Scale scores = row-mean of the item set (validated in step 2, all alpha>=0.87).
Valence: protection high=good; effort high=more burden; benefit_loss high=more loss.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.screen import get_bases, LIKERT
from src.reporting import save_report

# Bumped 2026-08-25 per advisor feedback: figure label/tick text was too
# small to read at paper column width.
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
    "legend.fontsize": 11,
})
TICK_FONTSIZE = 11

SCALES = {"protection": (".7", 5), "effort": (".8", 4), "benefit_loss": (".9", 3)}
SCENARIOS = {"less": ("Q4", "Q4.2"), "more": ("Q5", "Q5.2")}
N_FLOOR = 14   # below this: descriptives shown but flagged, excluded from tests

SHORT_METHOD = {
    "Delete this single conversation.": "Delete single\nconversation",
    "Clear all conversation history.": "Clear all\nhistory",
    "Delete a specific saved memory or fact.": "Delete specific\nmemory",
    "Type a message asking the AI Chatbot to forget it.": "Ask chatbot\nto forget",
    "Clear all saved memories.": "Clear all\nmemories",
    "Privacy dashboard or account-level data management page.": "Privacy\ndashboard",
    "Delete my account entirely.": "Delete\naccount",
}


def scale_score(df, base, q, k):
    items = [f"{base}{q}_{i}" for i in range(1, k + 1)]
    return df[items].apply(lambda c: c.map(LIKERT)).mean(axis=1)


def per_method(scen):
    base, method_col = SCENARIOS[scen]
    df = get_bases(verbose=False)[scen].copy()
    df = df[df[method_col] != "Other (Please specify)"]   # drop free-text Other
    for name, (q, k) in SCALES.items():
        df[name] = scale_score(df, base, q, k)

    out = []
    for method, g in df.groupby(method_col):
        row = {"method": method, "n": len(g)}
        for name in SCALES:
            row[f"{name}_mean"] = round(g[name].mean(), 2)
            row[f"{name}_median"] = g[name].median()
            row[f"{name}_sd"] = round(g[name].std(), 2)
        row["flag"] = "" if len(g) >= N_FLOOR else f"n<{N_FLOOR}"
        out.append(row)
    return pd.DataFrame(out).sort_values("n", ascending=False).reset_index(drop=True)


def plot_cost_benefit(tables, path="outputs/figures/fig7_method_cost_benefit.png"):
    """Grouped bars of protection/effort/benefit_loss means by method (n>=N_FLOOR
    only), one subplot per scenario -- visualizes methods.md's own table, no new
    computation."""
    colors = {"protection_mean": "#4C9F70", "effort_mean": "#B4436C", "benefit_loss_mean": "#3b6fa0"}
    scale_label = {"protection_mean": "Protection", "effort_mean": "Effort", "benefit_loss_mean": "Benefit loss"}

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), sharey=True)
    for ax, scen in zip(axes, SCENARIOS):
        tbl = tables[scen]
        tbl = tbl[tbl["flag"] == ""].copy()
        tbl["method_short"] = tbl["method"].map(SHORT_METHOD)
        x = np.arange(len(tbl)); w = 0.26
        for i, col in enumerate(colors):
            ax.bar(x + (i - 1) * w, tbl[col], w, label=scale_label[col], color=colors[col])
        ax.set_xticks(x); ax.set_xticklabels(tbl["method_short"], fontsize=TICK_FONTSIZE)
        ax.set_ylim(0, 5)
        ax.set_title(f"{scen}-sensitive scenario (n>={N_FLOOR} methods only)")
    axes[0].set_ylabel("Mean rating (1-5 Likert)")
    axes[0].legend(loc="upper left", bbox_to_anchor=(0, -0.18), ncol=3)
    fig.suptitle("Cost-benefit ratings by deletion method")
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight"); plt.close()
    return path


if __name__ == "__main__":
    lines = []
    tables = {}
    for scen in SCENARIOS:
        tbl = per_method(scen)
        tables[scen] = tbl
        lines.append(f"\n===== {scen.upper()} SENSITIVE =====")
        lines.append(tbl.to_string(index=False))
        out_path = f"outputs/tables/per_method_{scen}.csv"
        tbl.to_csv(out_path, index=False)

    # ranked-by-scale views (mean), reportable methods only
    lines.append("\n\n===== RANKINGS (n>=15 only) =====")
    for scen in SCENARIOS:
        ok = tables[scen][tables[scen]["flag"] == ""]
        for name in SCALES:
            r = ok.sort_values(f"{name}_mean", ascending=False)[["method", "n", f"{name}_mean"]]
            lines.append(f"\n[{scen}] {name} (high to low):")
            lines.append(r.to_string(index=False))

    lines.append("\nsaved -> outputs/tables/per_method_less.csv, per_method_more.csv")

    fig_path = plot_cost_benefit(tables)
    lines.append(f"saved -> {fig_path}")

    for line in lines:
        print(line)

    report_path = save_report("methods", lines)
    print(f"report saved -> {report_path}")