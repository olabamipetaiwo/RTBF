"""
Figure-only script for the paper's "sensitivity effect" section: a dumbbell
chart of less -> more sensitive scenario means for protection, effort,
benefit_loss, and willingness. No new statistics -- reuses the same scale
scoring src/stats.py and src/willingness.py already use, and the significance
calls already established there (stats.md steps 3-4, willingness.md):

  protection   SIG  (Wilcoxon, p_holm=.0018, r=0.38)
  effort       ns
  benefit_loss ns
  willingness  SIG  (Wilcoxon, p<.0001, r=+0.55 -- largest effect in the study)
"""

import matplotlib.pyplot as plt
from src.screen import get_bases
from src.stats import scale_score, SCALES
from src.willingness import WILLING
from src.reporting import save_report

# Bumped 2026-08-25 per advisor feedback: figure label/tick text was too
# small to read at paper column width.
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
})
ANNOTATION_FONTSIZE = 11

SIG = {
    "protection": ("SIG", "p_holm=.0018, r=0.38"),
    "effort": ("ns", ""),
    "benefit_loss": ("ns", ""),
    "willingness": ("SIG", "p<.0001, r=+0.55"),
}
ROW_ORDER = ["willingness", "protection", "effort", "benefit_loss"]
ROW_LABEL = {"willingness": "Willingness", "protection": "Protection",
             "effort": "Effort", "benefit_loss": "Benefit loss"}


def scenario_means(paired):
    out = {}
    for name, (q, k) in SCALES.items():
        less = scale_score(paired, "Q4", q, k)
        more = scale_score(paired, "Q5", q, k)
        out[name] = (less.mean(), more.mean())
    less_w = paired["Q4.10"].map(WILLING)
    more_w = paired["Q5.10"].map(WILLING)
    out["willingness"] = (less_w.mean(), more_w.mean())
    return out


def plot(means, path="outputs/figures/fig8_scenario_shift.png"):
    fig, ax = plt.subplots(figsize=(8, 5))
    for i, name in enumerate(ROW_ORDER):
        lo, hi = means[name]
        sig, stat = SIG[name]
        color = "#B4436C" if sig == "SIG" else "#999999"
        ax.plot([lo, hi], [i, i], color=color, linewidth=2, zorder=1)
        ax.scatter([lo], [i], color="#4C9F70", s=90, zorder=2, label="Less sensitive" if i == 0 else None)
        ax.scatter([hi], [i], color="#B4436C", s=90, zorder=2, label="More sensitive" if i == 0 else None)
        tag = f"{sig}" + (f" ({stat})" if stat else "")
        ax.text(max(lo, hi) + 0.08, i, tag, va="center", fontsize=ANNOTATION_FONTSIZE,
                color=("black" if sig == "SIG" else "#777777"))

    ax.set_yticks(range(len(ROW_ORDER)))
    ax.set_yticklabels([ROW_LABEL[n] for n in ROW_ORDER])
    ax.set_xlim(1, 5.6)
    ax.set_xlabel("Mean rating (1-5 Likert)")
    ax.set_title("Scenario sensitivity effect: less -> more sensitive (paired, n=177)")
    ax.set_ylim(-0.6, len(ROW_ORDER) - 0.4)
    ax.legend(loc="upper left", bbox_to_anchor=(0, 1.18), ncol=2, frameon=False)
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight"); plt.close()
    return path


if __name__ == "__main__":
    paired = get_bases(verbose=False)["paired"]
    means = scenario_means(paired)

    lines = ["=== Scenario means, less vs more sensitive (paired, n=%d) ===" % len(paired)]
    for name in ROW_ORDER:
        lo, hi = means[name]
        sig, stat = SIG[name]
        lines.append(f"{ROW_LABEL[name]:12s} less={lo:.3f}  more={hi:.3f}  diff={hi-lo:+.3f}  {sig} {stat}")

    fig_path = plot(means)
    lines.append(f"\nsaved -> {fig_path}")

    for line in lines:
        print(line)

    report_path = save_report("scenario_shift", lines)
    print(f"\nreport saved -> {report_path}")
