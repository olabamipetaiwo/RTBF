#!/usr/bin/env python3
"""
Survey charts:
  1) AI chatbots used and for how long  -> stacked bar (tenure stacked per bot)
  2) Deletion method selected per scenario -> ranked bars (Q4.2 and Q5.2)
Attention-check passers only (Q6.5 == 'Sometimes' AND Q9.3 == 'Agree').
"""

import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HEADER_ROWS = 3
BOT_COLS = [f"Q3.1_{i}" for i in range(1, 7)]
TENURE_ORDER = [
    "Less than 6 months",
    "6 to 12 months",
    "1 to 2 years",
    "2+ years",
]  # short->long
NOT_USED = {"never used", ""}

METHOD_SHORT = {
    "Delete this single conversation.": "Delete this conversation",
    "Clear all conversation history.": "Clear all history",
    "Type a message asking the AI Chatbot to forget it.": "Ask chatbot to forget",
    "Delete a specific saved memory or fact.": "Delete a saved memory",
    "Clear all saved memories.": "Clear all memories",
    "Privacy dashboard or account-level data management page.": "Privacy dashboard",
    "Delete my account entirely.": "Delete account",
    "Other (Please specify)": "Other",
}


def load(xlsx):
    raw = pd.read_excel(xlsx, header=None, dtype=str)
    header, qtext = raw.iloc[0].tolist(), raw.iloc[1].tolist()
    data = raw.iloc[HEADER_ROWS:].reset_index(drop=True)
    return header, qtext, data


def attention_pass(header, data):
    def c(n):
        return data.iloc[:, header.index(n)].astype(str).str.strip().str.lower()

    mask = (c("Q6.5") == "sometimes") & (c("Q9.3") == "agree")
    return data[mask].reset_index(drop=True)


def bot_label(qtext_i):  # text ends with ' - <Bot>'
    return qtext_i.split(" - ")[-1].strip()


def chart_tenure(header, qtext, data, outdir):
    labels = {h: bot_label(qtext[header.index(h)]) for h in BOT_COLS}
    # count matrix: bot x tenure
    counts = {}
    for h in BOT_COLS:
        col = data.iloc[:, header.index(h)].fillna("").str.strip()
        vc = col[~col.str.lower().isin(NOT_USED)].value_counts()
        counts[labels[h]] = {t: int(vc.get(t, 0)) for t in TENURE_ORDER}
    df = pd.DataFrame(counts).T  # rows=bots, cols=tenure
    df["__total"] = df.sum(axis=1)
    df = df.sort_values("__total", ascending=False).drop(columns="__total")

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bottom = [0] * len(df)
    cmap = plt.get_cmap("YlGnBu")
    colors = [cmap(x) for x in (0.30, 0.50, 0.70, 0.90)]
    for tenure, color in zip(TENURE_ORDER, colors):
        vals = df[tenure].tolist()
        ax.bar(
            df.index, vals, bottom=bottom, label=tenure, color=color, edgecolor="white"
        )
        bottom = [b + v for b, v in zip(bottom, vals)]
    for i, tot in enumerate(bottom):
        ax.text(i, tot + 1, str(int(tot)), ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("Number of users")
    ax.set_title("AI chatbots used, by length of use")
    ax.legend(title="Length of use", frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    fig.savefig(outdir / "chart_ai_usage_tenure.png", dpi=200)
    plt.close(fig)
    return df


def chart_methods(header, data, outdir):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), sharex=False)
    for ax, (qcol, title) in zip(
        axes, [("Q4.2", "Scenario 1 (Q4)"), ("Q5.2", "Scenario 2 (Q5)")]
    ):
        col = data.iloc[:, header.index(qcol)].dropna().str.strip()
        vc = col.value_counts()
        vc.index = [METHOD_SHORT.get(x, x) for x in vc.index]
        vc = vc.sort_values(ascending=False)  # descending so largest is leftmost
        ax.bar(vc.index, vc.values, color="#3b6ea5", edgecolor="white")
        for i, v in enumerate(vc.values):
            ax.text(i, v + 0.5, str(int(v)), ha="center", va="bottom", fontsize=9)
        ax.set_title(f"Deletion method selected - {title}")
        ax.set_ylabel("Number of respondents")
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(axis="x", rotation=30)
        for label in ax.get_xticklabels():
            label.set_ha("right")
    plt.tight_layout()
    fig.savefig(outdir / "chart_method_by_scenario.png", dpi=200)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", default="data/RTBF_Survey_Results.xlsx")
    ap.add_argument("--outdir", default="results")
    a = ap.parse_args()
    outdir = Path(a.outdir)
    outdir.mkdir(exist_ok=True)

    header, qtext, data = load(a.xlsx)
    n_all = len(data)
    data = attention_pass(header, data)
    print(f"respondents: {n_all} total -> {len(data)} attention-check passers")

    tdf = chart_tenure(header, qtext, data, outdir)
    print("\nusers per bot (attention-pass):")
    print(tdf.assign(total=tdf.sum(axis=1)).to_string())
    chart_methods(header, data, outdir)
    print(
        f"\nwrote {outdir}/chart_ai_usage_tenure.png and {outdir}/chart_method_by_scenario.png"
    )


if __name__ == "__main__":
    main()
