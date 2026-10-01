#!/usr/bin/env python3
"""
Step 1 - Extraction (RTBF prompt analysis)
==========================================
Reads the Qualtrics results export and emits ONE row per deletion-prompt
instance in tidy long format. No filtering, normalization, dedup, or labeling
happens here; those are later, separately reported steps.

Qualtrics export layout:

row 0 = short column header
row 1 = full question text
row 2 = ImportId JSON, only in some exports

The first response row is located by content (ResponseId starts with "R_"),
not by a fixed header count: see qualtrics_export.py.

Each participant passes through two blocks (Q4, Q5) and is asked the same
hypothetical in each: "If you were to type a message asking the AI Chatbot to
delete your location data, what would your message be?" We therefore carry:
  pid            - ResponseId (participant key; links back to survey for todo 2)
  block          - Q4 or Q5 (source block = a within-subject variable)
  method_context - the deletion method the participant selected in that block
                   (Q4.2 / Q5.2); lets us later test method -> phrasing
  prompt         - the free-text deletion message (Q4.11 / Q5.11)
  rationale      - "why phrase it this way" (Q4.12 / Q5.12); metadata for the
                   human-coding validation step, not a prompt itself
"""
import argparse
import pandas as pd

from qualtrics_export import load_export

# Attention checks, the same two items and the same rule as the survey
# analysis (RTBF-Analysis/src/screen.py): a respondent is excluded only if
# they ANSWERED a check with the wrong value. A blank answer is not a failure.
ATTENTION_CHECKS = {"Q6.5": "Sometimes", "Q9.3": "Agree"}

BLOCKS = {
    "Q4": {"prompt": "Q4.11", "rationale": "Q4.12", "method": "Q4.2"},
    "Q5": {"prompt": "Q5.11", "rationale": "Q5.12", "method": "Q5.2"},
}

def failed_attention(header, data):
    """Boolean Series: True where a check was answered with the wrong value."""
    wrong = pd.Series(False, index=data.index)
    for name, expected in ATTENTION_CHECKS.items():
        answer = data.iloc[:, header.index(name)]
        wrong |= answer.notna() & (answer != expected)
    return wrong


def extract(xlsx_path, screen_attention=False):
    header, _, data = load_export(xlsx_path)
    n_failed = 0
    if screen_attention:
        wrong = failed_attention(header, data)
        n_failed = int(wrong.sum())
        data = data[~wrong].reset_index(drop=True)

    def col(name):
        return data.iloc[:, header.index(name)]

    pid = col("ResponseId")
    rows = []
    for block, cmap in BLOCKS.items():
        prompt = col(cmap["prompt"])
        rationale = col(cmap["rationale"])
        method = col(cmap["method"])
        for i in range(len(data)):
            p = prompt.iloc[i]
            if pd.isna(p) or not str(p).strip():
                continue                      # no message written in this block
            rows.append({
                "pid": pid.iloc[i],
                "block": block,
                "method_context": ("" if pd.isna(method.iloc[i]) else str(method.iloc[i]).strip()),
                "prompt": str(p).strip(),
                "rationale": ("" if pd.isna(rationale.iloc[i]) else str(rationale.iloc[i]).strip()),
            })
    return pd.DataFrame(rows), len(data), n_failed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", required=True)
    ap.add_argument("--out", default="raw_prompts.csv")
    ap.add_argument("--screen-attention", action="store_true",
                    help="exclude respondents who answered an attention check wrongly")
    a = ap.parse_args()

    df, n_participants, n_failed = extract(a.xlsx, a.screen_attention)
    df.to_csv(a.out, index=False)

    n_prompts = len(df)
    n_contrib = df["pid"].nunique()
    per_block = df["block"].value_counts().sort_index()

    blocks_per_pid = df.groupby("pid")["block"].agg(set)
    both    = blocks_per_pid.apply(lambda s: s == {"Q4", "Q5"}).sum()
    q4_only = blocks_per_pid.apply(lambda s: s == {"Q4"}).sum()
    q5_only = blocks_per_pid.apply(lambda s: s == {"Q5"}).sum()

    if a.screen_attention:
        print(f"Failed attention (excluded): {n_failed}")
    print(f"Participant rows kept      : {n_participants}")
    print(f"Prompt instances extracted : {n_prompts}")
    print(f"Participants contributing  : {n_contrib}")
    print(f"  answered both blocks     : {both}")
    print(f"  Q4 only                  : {q4_only}")
    print(f"  Q5 only                  : {q5_only}")
    print(f"Per-block counts           : {per_block.to_dict()}")
    print(f"\nwrote {a.out}  (columns: {list(df.columns)})")

if __name__ == "__main__":
    main()