"""
Section 5.4 numbers and figure, from one source: do the checks a user can make
(asking again in the same conversation; looking at the screen) match what recall found?

Reads outputs/tables/audit_outcomes_provisional.csv (src.provisional_fill: real results
plus placeholders for cells not recalled yet). Only test cases with a KNOWN outcome are
used (recall success or recall failed); can't tell is left out, because for an agent
whose test cases are all can't tell (Gemini, DeepSeek) a check cannot be right or wrong.

Same-conversation check (deletion requests typed in the chat; NL FORGET rows plus the
typed-command rows on the MASTER sheet): after the request, the user asks for the fact
in the same conversation. "Still there" = the agent repeated the fact (R1 same-conv
FOUND); "gone" = it did not (NOT FOUND). The check MATCHES when still there goes with
recall success, or gone goes with recall failed.
    - said gone, recall success   : the check reassured the user wrongly
    - said still there, recall failed : the check raised a false alarm

Interface check (deletions through UI actions, not typed in the chat): interface_change
CHANGED = the screen showed the item gone.

Writes:
    outputs/results/checks_vs_outcome.md       (every number quoted in Section 5.4)
    outputs/figures/fig_checks_vs_outcome.png  (copied to paper/figures/)

AS IT STANDS: re-run after every recall batch:
    .venv/bin/python -m src.audit_outcomes && .venv/bin/python -m src.provisional_fill \
        && .venv/bin/python -m src.checks_vs_outcome
"""

import shutil
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.expectation_gap import PLATFORM_NAMES

IN_CSV = Path("outputs/tables/audit_outcomes_provisional.csv")
OUT_MD = Path("outputs/results/checks_vs_outcome.md")
OUT_FIG = Path("outputs/figures/fig_checks_vs_outcome.png")
PAPER_FIG = Path("../paper/figures/fig_checks_vs_outcome.png")

TYPED_ERASURES = {"NL forget command", "NL forget prompt"}
AGENT_ORDER = ["chatgpt", "claude", "perplexity", "copilot"]  # agents with known outcomes
COLORS = {"match": "#2a78d6", "reassured": "#eb6834", "alarm": "#6250d6"}  # validated, light mode
INK, INK_2 = "#0b0b0b", "#52514e"


def load() -> pd.DataFrame:
    df = pd.read_csv(IN_CSV, keep_default_na=False)
    return df[df["recoverability"].isin({"RECOVERED", "NOT RECOVERED", "INDETERMINATE"})].copy()


def same_conversation(df: pd.DataFrame) -> pd.DataFrame:
    typed = df[(df["sheet"] != "MASTER") | df["erasure"].isin(TYPED_ERASURES)]
    known = typed[typed["recoverability"].isin({"RECOVERED", "NOT RECOVERED"})
                  & typed["same_conversation_r1"].isin({"FOUND", "NOT FOUND"})]
    rows = []
    for p in AGENT_ORDER:
        g = known[known["platform"] == p]
        success = g["recoverability"] == "RECOVERED"
        still = g["same_conversation_r1"] == "FOUND"
        match = int(((still & success) | (~still & ~success)).sum())
        reassured = int((~still & success).sum())
        alarm = int((still & ~success).sum())
        rows.append({"platform": p, "n": len(g), "match": match, "reassured": reassured, "alarm": alarm})
    return pd.DataFrame(rows)


def interface(df: pd.DataFrame) -> dict[str, int]:
    ui = df[(df["sheet"] == "MASTER") & ~df["erasure"].isin(TYPED_ERASURES)]
    changed = ui[ui["interface_change"] == "CHANGED"]
    known = changed[changed["recoverability"].isin({"RECOVERED", "NOT RECOVERED"})]
    return {
        "changed": len(changed),
        "known": len(known),
        "success": int((known["recoverability"] == "RECOVERED").sum()),
        "failed": int((known["recoverability"] == "NOT RECOVERED").sum()),
        "cant_tell": len(changed) - len(known),
        "unchanged": int((ui["interface_change"] == "UNCHANGED").sum()),
        "unchanged_success": int(((ui["interface_change"] == "UNCHANGED")
                                  & (ui["recoverability"] == "RECOVERED")).sum()),
    }


GREY = "#9a9a96"
ROW_ORDER = ["chatgpt", "claude", "copilot", "perplexity"]  # most to least wrong


def _rows(sc: pd.DataFrame, ui: dict[str, int]) -> list[dict]:
    """One row per check: agents (same-conversation check) then the screen check."""
    rows = []
    for p in ROW_ORDER:
        r = sc[sc["platform"] == p].iloc[0]
        rows.append({"label": f"{PLATFORM_NAMES[p]} (n={r['n']})", "n": r["n"],
                     "right": r["match"], "worked_but_back": r["reassured"], "failed_but_gone": r["alarm"]})
    rows.append({"label": f"Screen check, UI actions (n={ui['known']})", "n": ui["known"],
                 "right": ui["failed"], "worked_but_back": ui["success"], "failed_but_gone": 0})
    return rows


def _style(ax) -> None:
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(colors=INK_2)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of test cases with a known outcome (%)", color=INK_2)


def _save(fig, name: str) -> None:
    out = OUT_FIG.parent / name
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    if PAPER_FIG.parent.exists():
        shutil.copy(out, PAPER_FIG.parent / name)


def draw_wrong(rows: list[dict]) -> None:
    """Option A: one bar per check, the share of test cases where the check gave the wrong answer."""
    plt.rcParams.update({"font.size": 11, "font.family": "serif", "axes.edgecolor": INK_2})
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ys = [0, 1, 2, 3, 4.4]  # a gap before the screen check
    wrong = [100 * (r["worked_but_back"] + r["failed_but_gone"]) / r["n"] for r in rows]
    ax.barh(ys, wrong, color=COLORS["match"], height=0.6)
    for y, w in zip(ys, wrong):
        ax.text(w + 1.5, y, f"{w:.0f}%", va="center", color=INK, fontsize=10.5)
    ax.set_yticks(ys, [r["label"] for r in rows])
    ax.invert_yaxis()
    ax.set_title("How often the check disagreed with the outcome", loc="left", fontsize=11.5, color=INK)
    _style(ax)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of test cases where the check disagreed (%)", color=INK_2)
    _save(fig, "fig_checks_wrong.png")


def draw_direction(rows: list[dict]) -> None:
    """Option B: the same, with the two ways a check can be wrong shown separately."""
    plt.rcParams.update({"font.size": 11, "font.family": "serif", "axes.edgecolor": INK_2})
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    ys = [0, 1, 2, 3, 4.4]
    parts = [("right", GREY, "Check agreed with the outcome"),
             ("worked_but_back", COLORS["reassured"], "Check suggested deleted, outcome recall success"),
             ("failed_but_gone", COLORS["alarm"], "Check suggested not deleted, outcome recall failed")]
    left = [0.0] * len(rows)
    for key, color, _ in parts:
        share = [100 * r[key] / r["n"] for r in rows]
        ax.barh(ys, share, left=left, color=color, edgecolor="white", linewidth=1.5, height=0.6)
        for y, s, l in zip(ys, share, left):
            if s >= 9:
                ax.text(l + s / 2, y, f"{s:.0f}%", ha="center", va="center", color="white", fontsize=10)
        left = [l + s for l, s in zip(left, share)]
    ax.set_yticks(ys, [r["label"] for r in rows])
    ax.invert_yaxis()
    ax.set_title("What the check suggested, against what happened", loc="left", fontsize=11.5, color=INK)
    _style(ax)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, c, _ in parts]
    fig.legend(handles, [lab for _, _, lab in parts], loc="upper center", ncol=1, frameon=False,
               bbox_to_anchor=(0.5, 0.0), fontsize=10)
    _save(fig, "fig_checks_direction.png")


def draw(sc: pd.DataFrame, ui: dict[str, int]) -> None:
    rows = _rows(sc, ui)
    draw_wrong(rows)
    draw_direction(rows)


def main() -> None:
    df = load()
    sc, ui = same_conversation(df), interface(df)
    wrong = [100 * (r.reassured + r.alarm) / r.n for r in sc.itertuples()]
    lines = [
        "# checks_vs_outcome",
        "",
        f"_Run at {datetime.now().isoformat(timespec='seconds')}_",
        "",
        f"Source: {IN_CSV}. Known outcomes only (recall success or recall failed); can't tell is left out.",
        "",
        "## Same-conversation check (deletion requests typed in the chat)",
        "",
        "| Agent | Test cases | Matched | Said gone, recall success | Said still there, recall failed | Wrong share |",
        "|---|---|---|---|---|---|",
        *[
            f"| {PLATFORM_NAMES[r.platform]} | {r.n} | {r.match} | {r.reassured} | {r.alarm} | "
            f"{100 * (r.reassured + r.alarm) / r.n:.0f}% |"
            for r in sc.itertuples()
        ],
        "",
        f"Wrong share ranges from {min(wrong):.0f}% to {max(wrong):.0f}% across the four agents with "
        "known outcomes (Gemini and DeepSeek have none; Copilot has few).",
        "",
        "## Interface check (deletions through UI actions)",
        "",
        f"- Screen showed the item gone in {ui['changed']} test cases; {ui['known']} have a known outcome "
        f"(recall success {ui['success']}, recall failed {ui['failed']}); {ui['cant_tell']} are can't tell.",
        f"- Recall success after the screen showed it gone: {ui['success']} of {ui['known']} "
        f"({100 * ui['success'] / ui['known']:.0f}%).",
        f"- Screen unchanged: {ui['unchanged']} test cases, recall success in {ui['unchanged_success']}.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines))
    draw(sc, ui)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
