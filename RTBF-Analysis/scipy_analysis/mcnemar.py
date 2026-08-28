"""
Scipy-only reimplementation of src/mcnemar.py (per-method choice shift,
less -> more). Uses mcnemar_scipy.mcnemar_p (was statsmodels) and
scipy_analysis.correction.holm (was statsmodels.multitest).
"""

import pandas as pd

from src.screen import get_bases

from .reporting import save_report
from .correction import holm
from .mcnemar_scipy import mcnemar_p

METHODS = [
    "Delete this single conversation.",
    "Clear all conversation history.",
    "Delete a specific saved memory or fact.",
    "Type a message asking the AI Chatbot to forget it.",
    "Clear all saved memories.",
    "Privacy dashboard or account-level data management page.",
    "Delete my account entirely.",
]
SHORT = {m: m.split(".")[0][:34] for m in METHODS}


def per_method_shift(paired):
    rows, pvals = [], []
    for m in METHODS:
        less = paired["Q4.2"] == m
        more = paired["Q5.2"] == m
        both = int((less & more).sum()); neither = int((~less & ~more).sum())
        dropped = int((less & ~more).sum()); added = int((~less & more).sum())
        table = [[neither, added], [dropped, both]]
        _, p = mcnemar_p(table)
        rows.append((SHORT[m], dropped, added, dropped + added, p)); pvals.append(p)

    padj = holm(pvals)
    return pd.DataFrame(
        [(name, d, a, disc,
          "drop" if d > a else ("gain" if a > d else "-"),
          round(p, 4), round(pa, 4), "*" if pa < 0.05 else "")
         for (name, d, a, disc, p), pa in zip(rows, padj)],
        columns=["method", "dropped", "added", "discordant", "dir", "p_raw", "p_holm", "sig"],
    )


if __name__ == "__main__":
    paired = get_bases(verbose=False)["paired"]
    out = per_method_shift(paired)

    lines = [
        "=== Per-method choice shift (less -> more): McNemar + Holm ===",
        out.to_string(index=False),
        "\ndropped = picked in less-sensitive only (abandoned when sensitive)",
        "added   = picked in more-sensitive only (adopted when sensitive)",
        "Holm across 7 methods.",
    ]

    for line in lines:
        print(line)

    report_path = save_report("mcnemar", lines)
    print(f"\nreport saved -> {report_path}")
