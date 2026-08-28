"""
Per-method paired test of choice shift with sensitivity (less -> more),
FULL FAMILY with Holm correction.

Follow-up to the ns Stuart-Maxwell omnibus (step 6). For each method, reduce
each of the 177 paired respondents to binary (picked it in less? in more?),
run McNemar on the paired 2x2, then Holm-correct across all methods so the
"one method that moved" claim is stress-tested against having 7 chances.

Reports every method's discordant cells (dropped vs added) so the raw
asymmetry is visible, not just the p-value.
"""

import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests
from src.screen import get_bases
from src.reporting import save_report

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
        p = mcnemar(table, exact=(dropped + added) < 25).pvalue
        rows.append((SHORT[m], dropped, added, dropped + added, p)); pvals.append(p)

    padj = multipletests(pvals, method="holm")[1]
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
        "Holm across 7 methods. Stuart-Maxwell omnibus was ns (p=0.393).",
    ]

    for line in lines:
        print(line)

    report_path = save_report("mcnemar", lines)
    print(f"\nreport saved -> {report_path}")
