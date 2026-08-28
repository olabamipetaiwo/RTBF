"""
Objective knowledge & misconceptions (Q8.2-Q8.7). New for the paper's Results
section 1 ("What Users Know About Memory and Deletion") -- no prior script in
this repo touches these items.

Q8.2 = "right to be forgotten" definition (4-option best-answer)
Q8.3 = conversations may be used to train future models (True/False)
Q8.4 = "training data" definition (4-option best-answer)
Q8.5 = "memory" definition (4-option best-answer)
Q8.6 = "AI Chatbots access only public user data" (True/False; correct = False)
Q8.7 = "user data deleted after five years" (True/False; correct = False)

Correct answers matched by substring (not full text) so a transcription slip
in the long option text can't silently break scoring. Answer key confirmed
with the research team before running.

Paired base (n=177) used, consistent with every other reported N in this
analysis (sample.md, willingness.md, etc.) -- these items aren't scenario-
specific, so any of less/more/paired would give the same respondents; paired
keeps the denominator consistent with the rest of the paper.
"""

import pandas as pd
import matplotlib.pyplot as plt
from src.screen import get_bases
from src.reporting import save_report

# Bumped 2026-08-25 per advisor feedback: figure label/tick text was too
# small to read at paper column width.
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
})
ANNOTATION_FONTSIZE = 10

CORRECT_SUBSTR = {
    "Q8.2": "erase their personal data without undue delay",
    "Q8.3": "True",
    "Q8.4": "used to teach the AI model",
    "Q8.5": "retain information from past conversations",
    "Q8.6": "False",
    "Q8.7": "False",
}

ITEM_LABEL = {
    "Q8.2": "Right to be forgotten (definition)",
    "Q8.3": "Conversations may train future models",
    "Q8.4": "Training data (definition)",
    "Q8.5": "Memory (definition)",
    "Q8.6": "Chatbots access only public data (F)",
    "Q8.7": "User data deleted after 5 years (F)",
}

# Short label for the dominant wrong answer, used for figure annotation.
MISCONCEPTION_SHORT = {
    "Q8.2": {
        "The right of an individual to access and download a copy of all personal data an organisation holds about them": "confuses with right of access",
        "The right of an individual to prevent an organisation from collecting their personal data in the first place": "confuses with right to object/restrict",
        "The right of an individual to be notified within 72 hours if their personal data has been involved in a data breach": "confuses with breach notification",
    },
    "Q8.3": {"False": "believes chats aren't used for training"},
    "Q8.4": {
        "Instructions programmed by developers to control what topics the chatbot can discuss": "confuses with system prompts/rules",
        "Test conversations used to check whether the chatbot is working correctly before release": "confuses with QA/test data",
        "The personal profile an AI chatbot builds about each individual user over time": "confuses with user profile/memory",
    },
    "Q8.5": {
        "The storage space used to run the chatbot's software on a server": "confuses with server storage",
        "The chatbot's ability to search the internet for real-time information": "confuses with live web search",
        "The encryption system that protects user conversations from being accessed by third parties": "confuses with encryption",
    },
    "Q8.6": {"True": "believes chatbots see only public data"},
    "Q8.7": {"True": "believes a fixed 5-year deletion policy exists"},
}


def score_respondents(df):
    correct = pd.DataFrame({
        q: df[q].astype(str).str.contains(substr, regex=False)
        for q, substr in CORRECT_SUBSTR.items()
    })
    score = correct.sum(axis=1)
    return correct, score


def item_summary(df, correct):
    rows = []
    n = len(df)
    for q in CORRECT_SUBSTR:
        pct_correct = round(100 * correct[q].sum() / n, 1)
        wrong = df.loc[~correct[q], q]
        if len(wrong):
            top_wrong, top_n = wrong.value_counts().index[0], wrong.value_counts().iloc[0]
            misconception = MISCONCEPTION_SHORT[q].get(top_wrong, str(top_wrong)[:50])
            pct_misconception = round(100 * top_n / n, 1)
        else:
            misconception, pct_misconception = "-", 0.0
        rows.append({
            "item": q, "topic": ITEM_LABEL[q], "pct_correct": pct_correct,
            "dominant_misconception": misconception,
            "pct_holding_it": pct_misconception,
        })
    return pd.DataFrame(rows).sort_values("pct_correct").reset_index(drop=True)


def plot_accuracy(summary, path="outputs/figures/fig6_knowledge_accuracy.png"):
    # descending pct_correct -> barh plots last row at the top, so the
    # worst-understood item ends up most prominent (top of the chart)
    order = summary.sort_values("pct_correct", ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(order["topic"], order["pct_correct"], color="#3b6fa0", edgecolor="white")
    ax.bar_label(bars, fmt="%.0f%%", padding=4)
    ax.set_xlim(0, 100)
    ax.set_xlabel("% of respondents answering correctly (n=177)")
    ax.set_title("Objective knowledge: % correct per item\n(labels show the dominant misconception among wrong answers)")
    for bar, (_, row) in zip(bars, order.iterrows()):
        if row["pct_holding_it"] > 0:
            ax.text(2, bar.get_y() + bar.get_height() / 2,
                    f"{row['dominant_misconception']} ({row['pct_holding_it']:.0f}%)",
                    va="center", ha="left", fontsize=ANNOTATION_FONTSIZE, color="white")
    plt.tight_layout(); plt.savefig(path, dpi=200, bbox_inches="tight"); plt.close()
    return path


if __name__ == "__main__":
    paired = get_bases(verbose=False)["paired"]
    correct, score = score_respondents(paired)
    summary = item_summary(paired, correct)

    lines = [f"=== Objective knowledge (Q8.2-Q8.7), n={len(paired)} ===\n"]
    lines.append(summary.to_string(index=False))

    lines.append("\n=== Score distribution (0-6 correct) ===")
    dist = score.value_counts().reindex(range(7), fill_value=0)
    dist_pct = (100 * dist / len(paired)).round(1)
    dist_tbl = pd.DataFrame({"n": dist, "pct": dist_pct})
    lines.append(dist_tbl.to_string())
    lines.append(f"\nmean score : {score.mean():.2f} / 6")
    lines.append(f"median score: {score.median():.1f} / 6")

    out_path = "outputs/tables/knowledge_scores.csv"
    summary.to_csv(out_path, index=False)
    lines.append(f"\nsaved -> {out_path}")

    fig_path = plot_accuracy(summary)
    lines.append(f"saved -> {fig_path}")

    for line in lines:
        print(line)

    report_path = save_report("knowledge", lines)
    print(f"\nreport saved -> {report_path}")
