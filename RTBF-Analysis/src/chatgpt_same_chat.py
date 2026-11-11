"""
ChatGPT prompt-based recall successes that are consistent with documentation, and how many of them
the same-conversation check did not return (paper: Documentation consistency, "104 of the 107").

Base: outputs/tables/audit_outcomes_provisional.csv, NL FORGET sheet, platform chatgpt,
recall success (RECOVERED) with a CONSISTENT documentation verdict. The same-conversation check
was run in every one of these cases, so the original conversation survived in all of them.

    .venv/bin/python -m src.chatgpt_same_chat
"""

import pandas as pd

from src.reporting import save_report

TABLE = "outputs/tables/audit_outcomes_provisional.csv"


def main() -> None:
    d = pd.read_csv(TABLE)
    d = d[(d["sheet"].str.strip() == "NL FORGET") & (d["platform"] == "chatgpt")
          & (d["recoverability"] == "RECOVERED") & (d["policy_consistency"] == "CONSISTENT")]
    same = d["same_conversation_r1"].fillna("NOT RUN").value_counts().to_dict()
    lines = [
        f"Base: {len(d)} ChatGPT prompt-based recall successes consistent with documentation ({TABLE}).",
        f"Same-conversation check: {same}",
        f"Original conversation survived (check ran): {int(d['same_conversation_r1'].notna().sum())} of {len(d)}",
        f"Not returned in the original conversation: {same.get('NOT FOUND', 0)} of {len(d)}",
    ]
    print(save_report("chatgpt_same_chat", lines))


if __name__ == "__main__":
    main()
