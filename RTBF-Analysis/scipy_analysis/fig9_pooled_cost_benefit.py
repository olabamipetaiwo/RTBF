"""
fig9 -- grouped bar chart of protection/effort/benefit_loss means by method,
POOLED (both scenarios combined, task 2's dedup logic via
scipy_analysis.pooling.pooled_method_scores). Matches src/methods.py's
fig7_method_cost_benefit.png exactly in style (colors, bar width, y-axis,
short labels) -- same "3-chart set" (fig7's less/more subplots + this
"overall" view), just sourced from the pooled dataset instead of re-scoring
raw per-scenario items. No new statistics -- pure visualization.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.screen import get_bases
from src.stats import N_FLOOR
from src.methods import SHORT_METHOD

from .reporting import save_report
from .pooling import pooled_method_scores

# Bumped 2026-08-25 per advisor feedback: figure label/tick text was too
# small to read at paper column width.
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
    "legend.fontsize": 11,
})
TICK_FONTSIZE = 11

COLORS = {"protection_mean": "#4C9F70", "effort_mean": "#B4436C", "benefit_loss_mean": "#3b6fa0"}
SCALE_LABEL = {"protection_mean": "Protection", "effort_mean": "Effort", "benefit_loss_mean": "Benefit loss"}


def pooled_table(bases, n_floor=N_FLOOR):
    """Same shape as src.methods.per_method(): method, n, {scale}_mean/_median/_sd, flag."""
    pooled = pooled_method_scores(bases)
    out = []
    for method, g in pooled.groupby("method"):
        row = {"method": method, "n": len(g)}
        for name in ("protection", "effort", "benefit_loss"):
            row[f"{name}_mean"] = round(g[name].mean(), 2)
            row[f"{name}_median"] = g[name].median()
            row[f"{name}_sd"] = round(g[name].std(), 2)
        row["flag"] = "" if len(g) >= n_floor else f"n<{n_floor}"
        out.append(row)
    return pd.DataFrame(out).sort_values("n", ascending=False).reset_index(drop=True)


def plot_pooled_cost_benefit(tbl, path="outputs/figures/fig9_pooled_cost_benefit.png"):
    tbl = tbl[tbl["flag"] == ""].copy()
    tbl["method_short"] = tbl["method"].map(SHORT_METHOD)
    fig, ax = plt.subplots(figsize=(8, 5.5))
    x = np.arange(len(tbl)); w = 0.26
    for i, col in enumerate(COLORS):
        ax.bar(x + (i - 1) * w, tbl[col], w, label=SCALE_LABEL[col], color=COLORS[col])
    ax.set_xticks(x); ax.set_xticklabels(tbl["method_short"], fontsize=TICK_FONTSIZE)
    ax.set_ylim(0, 5)
    ax.set_ylabel("Mean rating (1-5 Likert)")
    ax.set_title(f"Overall (pooled, both scenarios; n>={N_FLOOR} methods only)")
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.14), ncol=3)
    fig.suptitle("Cost-benefit ratings by deletion method -- pooled")
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight"); plt.close()
    return path


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    tbl = pooled_table(bases)

    lines = ["\n===== POOLED (both scenarios) =====", tbl.to_string(index=False)]
    table_path = "scipy_analysis/outputs/tables/pooled_method_table.csv"
    tbl.to_csv(table_path, index=False)
    lines.append(f"\nsaved -> {table_path}")

    lines.append("\n\n===== RANKINGS (n>=14 only) =====")
    ok = tbl[tbl["flag"] == ""]
    for name in ("protection", "effort", "benefit_loss"):
        r = ok.sort_values(f"{name}_mean", ascending=False)[["method", "n", f"{name}_mean"]]
        lines.append(f"\n[pooled] {name} (high to low):")
        lines.append(r.to_string(index=False))

    fig_path = plot_pooled_cost_benefit(tbl)
    lines.append(f"\nsaved -> {fig_path}")

    for line in lines:
        print(line)

    report_path = save_report("fig9_pooled_cost_benefit", lines)
    print(f"\nreport saved -> {report_path}")
