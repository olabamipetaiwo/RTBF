"""
Step 1: Sample description on the analysis base (n=177, answered Q4.2).
  - Demographics table (Q2.x), plus an age-distribution pie chart.
  - Chatbot usage x tenure (Q3.1): absolute stacked bar, a 100%-stacked
    version (tenure composition, comparable across bots), an adoption-share
    pie (relative popularity), and an adoption-rate bar (% of sample).
    "Never used" excluded throughout.
"""

import pandas as pd
import matplotlib.pyplot as plt
from src.screen import get_bases, load_labels
from src.reporting import save_report

# Bumped 2026-08-25, revised twice same day. First attempt scaled font size
# purely by the LaTeX column-shrink factor (see prior comment history) to
# target literal body-text parity -- this overlapped titles/labels/ticks
# badly, because the shrink-factor math only accounts for point size, not
# whether the layout (rotation, padding, tick count) has room for text that
# much bigger. Settled on a smaller, layout-safe bump instead (~1.6x the
# original sizes) plus fixing the rotation/padding that was masking these
# collisions at the old, tiny font size.
plt.rcParams.update({
    "font.size": 15,
    "axes.titlesize": 17,
    "axes.labelsize": 15,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "legend.fontsize": 13,
    "legend.title_fontsize": 14,
})

TENURE_ORDER = ["Less than 6 months", "6 to 12 months", "1 to 2 years", "2+ years"]
CHATBOTS = {"Q3.1_1": "ChatGPT", "Q3.1_2": "Claude", "Q3.1_3": "Gemini",
            "Q3.1_4": "Copilot", "Q3.1_5": "Perplexity", "Q3.1_6": "Deepseek"}
DEMO = {"Q2.1": "Age", "Q2.2": "Lives in US", "Q2.3": "Ever used a chatbot"}


def demographics_table(df, labels):
    rows = []
    for col, label in DEMO.items():
        for val, n in df[col].value_counts(dropna=False).items():
            rows.append({"variable": label, "question_text": labels.get(col, ""),
                         "response": val, "n": int(n),
                         "pct": round(100 * n / len(df), 1)})
    return pd.DataFrame(rows)


def tenure_matrix(df):
    mat = {name: [int(df[col].value_counts().get(b, 0)) for b in TENURE_ORDER]
           for col, name in CHATBOTS.items()}
    m = pd.DataFrame(mat, index=TENURE_ORDER).T
    m["total_users"] = m.sum(axis=1)
    return m.sort_values("total_users", ascending=False)


TENURE_SHADES = plt.cm.Greens([0.4, 0.6, 0.8, 1.0])


def plot_tenure(mat, path="outputs/figures/fig1_ai_tenure.png"):
    ax = mat[TENURE_ORDER].plot(kind="bar", stacked=True, figsize=(9, 5.5),
                                color=TENURE_SHADES, edgecolor="white", linewidth=0.4)
    ax.set_ylabel("Number of participants (users only)")
    ax.set_xlabel("")
    ax.set_title("AI chatbot usage and tenure", pad=14)
    ax.legend(title="Tenure", bbox_to_anchor=(1.01, 1), loc="upper left")
    # Bare bot names no longer fit horizontally at the larger tick font --
    # rotate instead of the old rotation=0.
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight"); plt.close()
    return path


def plot_age_pie(demo, path="outputs/figures/fig2_age_distribution.png"):
    age = demo[demo["variable"] == "Age"].set_index("response")["n"]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(age, labels=age.index, autopct="%1.1f%%", colors=plt.cm.viridis(
        [i / len(age) for i in range(len(age))]), wedgeprops={"edgecolor": "white"})
    ax.set_title("Age distribution")
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight"); plt.close()
    return path


def plot_adoption_share_pie(mat, path="outputs/figures/fig3_chatbot_adoption_share.png"):
    share = mat["total_users"]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(share, labels=share.index, autopct="%1.1f%%", colors=plt.cm.viridis(
        [i / len(share) for i in range(len(share))]), wedgeprops={"edgecolor": "white"})
    ax.set_title("Chatbot adoption share\n(share of total usage instances, participants may use multiple)")
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight"); plt.close()
    return path


def tenure_pct_matrix(mat):
    return mat[TENURE_ORDER].div(mat["total_users"], axis=0) * 100


def plot_tenure_pct(mat_pct, path="outputs/figures/fig4_tenure_pct_stacked.png"):
    ax = mat_pct.plot(kind="bar", stacked=True, figsize=(9, 5),
                       colormap="viridis", edgecolor="white", linewidth=0.4)
    ax.set_ylabel("% of that chatbot's users")
    ax.set_xlabel("")
    ax.set_ylim(0, 100)
    ax.set_title("AI chatbot tenure composition (100% stacked)")
    ax.legend(title="Tenure", bbox_to_anchor=(1.01, 1), loc="upper left")
    plt.xticks(rotation=0); plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight"); plt.close()
    return path


def adoption_rate(mat, n):
    return (mat["total_users"] / n * 100).sort_values(ascending=False)


def plot_adoption_rate_bar(rates, path="outputs/figures/fig5_adoption_rate.png"):
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(rates.index[::-1], rates.values[::-1], color="#3b6fa0",
                    edgecolor="white")
    ax.bar_label(bars, fmt="%.1f%%", padding=4)
    ax.set_xlabel("% of sample (n = participants) who have used the chatbot")
    ax.set_xlim(0, 100)
    ax.set_title("Chatbot adoption rate")
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight"); plt.close()
    return path


if __name__ == "__main__":
    df = get_bases(verbose=False)["less"]   # analysis base, n=177
    labels = load_labels()

    lines = [f"sample: n = {len(df)}", ""]

    demo = demographics_table(df, labels)
    lines.append("=== demographics ===")
    lines.append(demo.drop(columns="question_text").to_string(index=False))
    mat = tenure_matrix(df)
    lines.append("\n=== usage x tenure (users only) ===")
    lines.append(mat.to_string())

    demo.to_csv("outputs/tables/sample_demographics.csv", index=False)
    mat.to_csv("outputs/tables/ai_tenure_matrix.csv")
    lines.append(f"\nsaved -> {plot_tenure(mat)}")
    lines.append(f"saved -> {plot_age_pie(demo)}")
    lines.append(f"saved -> {plot_adoption_share_pie(mat)}")

    mat_pct = tenure_pct_matrix(mat)
    mat_pct.to_csv("outputs/tables/ai_tenure_pct_matrix.csv")
    lines.append(f"saved -> {plot_tenure_pct(mat_pct)}")

    rates = adoption_rate(mat, len(df))
    rates.rename("adoption_rate_pct").to_csv("outputs/tables/chatbot_adoption_rate.csv")
    lines.append(f"saved -> {plot_adoption_rate_bar(rates)}")

    for line in lines:
        print(line)

    report_path = save_report("sample", lines)
    print(f"report saved -> {report_path}")