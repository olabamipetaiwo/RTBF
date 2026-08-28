"""
Step 8: calibration & gaps (descriptive cross-tabs), both scenarios.

8a. Confidence vs verification.
    Q4.6/Q5.6 = confidence in the verification answer (5-pt ordinal).
    Q4.5/Q5.5 = did they verify (select-all; "verified" = any YES option 1-5
                ticked; options 6/7 are "did NOT know how" / "did NOT want to").
    Cross-tab exposes CONFIDENT-BUT-UNVERIFIED users (miscalibration).

8b. Used vs ideal method.
    Q4.2/Q5.2 = method actually used (single-select).
    Q4.13/Q5.13 = methods would choose from ALL options (select-all).
    Per method: %used vs %ideal -> under/over-adoption relative to preference.
    NOTE: Q4.13/Q5.13's option order does NOT match Q4.2/Q5.2's — verified
    against the raw question labels (src/screen.py's load_labels) for BOTH
    scenarios and mapped explicitly below (same order in both). Option 8
    ("File a request.") has no Q4.2/Q5.2 counterpart at all, so it's
    reported separately with no %used/gap.
"""

import pandas as pd
from src.screen import get_bases
from src.reporting import save_report

SCEN = {"less": ("Q4.6", "Q4.5", "Q4.2", "Q4.13"), "more": ("Q5.6", "Q5.5", "Q5.2", "Q5.13")}

CONF_ORDER = ["Not confident at all (I doubted it worked)", "Slightly confident",
              "Moderately confident", "Very confident",
              "Completely confident (I had no doubt)"]
CONF_SHORT = {CONF_ORDER[0]: "Not at all", CONF_ORDER[1]: "Slightly",
              CONF_ORDER[2]: "Moderately", CONF_ORDER[3]: "Very",
              CONF_ORDER[4]: "Completely"}
METHODS = {
    "Delete this single conversation.": "Delete single conv",
    "Clear all conversation history.": "Clear all history",
    "Delete a specific saved memory or fact.": "Delete specific mem",
    "Type a message asking the AI Chatbot to forget it.": "Ask to forget",
    "Clear all saved memories.": "Clear all memories",
    "Privacy dashboard or account-level data management page.": "Privacy dashboard",
    "Delete my account entirely.": "Delete account",
}
# Q4.13/Q5.13 option order verified against raw labels (both scenarios,
# identical order) — does NOT match Q4.2/Q5.2's order.
IDEAL_MAP = {
    1: "Type a message asking the AI Chatbot to forget it.",
    2: "Delete this single conversation.",
    3: "Clear all conversation history.",
    4: "Delete a specific saved memory or fact.",
    5: "Clear all saved memories.",
    6: "Delete my account entirely.",
    7: "Privacy dashboard or account-level data management page.",
}
NO_USED_EQUIVALENT = {8: "File a request."}   # not an option in Q4.2/Q5.2 at all


def confidence_vs_verification(df, conf_col, verify_prefix):
    verify_yes = [f"{verify_prefix}_{i}" for i in range(1, 6)]
    verified = df[verify_yes].notna().any(axis=1)
    conf = df[conf_col]
    tab = pd.crosstab(conf.map(CONF_SHORT), verified,
                      rownames=["confidence"], colnames=["verified"])
    tab = tab.reindex([CONF_SHORT[c] for c in CONF_ORDER]).fillna(0).astype(int)
    tab.columns = ["did NOT verify", "verified"]
    tab["% confident-but-unverified"] = (
        tab["did NOT verify"] / (tab["did NOT verify"] + tab["verified"]) * 100
    ).round(1)
    return tab


def used_vs_ideal(df, used_col, ideal_prefix):
    n = len(df)
    used = df[used_col].value_counts()
    rows = []
    for i, method in IDEAL_MAP.items():
        pct_used = 100 * int(used.get(method, 0)) / n
        pct_ideal = 100 * int(df[f"{ideal_prefix}_{i}"].notna().sum()) / n
        rows.append({"method": METHODS[method], "%used": round(pct_used, 1),
                     "%ideal": round(pct_ideal, 1),
                     "gap (ideal-used)": round(pct_ideal - pct_used, 1)})
    out = pd.DataFrame(rows).sort_values("gap (ideal-used)", ascending=False)

    extra = []
    for i, label in NO_USED_EQUIVALENT.items():
        pct_ideal = 100 * int(df[f"{ideal_prefix}_{i}"].notna().sum()) / n
        extra.append({"method": label, "%used": "n/a (not a Q4.2/Q5.2 option)",
                       "%ideal": round(pct_ideal, 1), "gap (ideal-used)": "n/a"})
    return out, pd.DataFrame(extra)


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    lines = []
    for scen, (conf_col, verify_prefix, used_col, ideal_prefix) in SCEN.items():
        df = bases[scen]
        lines.append("\n" + "=" * 60)
        lines.append(f"{scen.upper()} SENSITIVE — 8a. Confidence vs verification ({conf_col}/{verify_prefix})")
        lines.append("=" * 60)
        lines.append(confidence_vs_verification(df, conf_col, verify_prefix).to_string())

        lines.append(f"\n{scen.upper()} SENSITIVE — 8b. Used vs ideal method ({used_col}/{ideal_prefix})")
        lines.append("=" * 60)
        gap_tab, extra_tab = used_vs_ideal(df, used_col, ideal_prefix)
        lines.append(gap_tab.to_string(index=False))
        lines.append("\n-- options with no %used counterpart (not in Q4.2/Q5.2) --")
        lines.append(extra_tab.to_string(index=False))

    for line in lines:
        print(line)

    report_path = save_report("calibration", lines)
    print(f"\nreport saved -> {report_path}")
