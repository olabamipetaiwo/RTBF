#!/usr/bin/env python3
"""Step 4 - PII scrub. Redacts structured PII (regex) + named entities (spaCy).
Adds `prompt_scrubbed`; originals preserved. Display column for the paper."""

import argparse, re
import pandas as pd
import spacy

REGEX = [
    ("[EMAIL]", r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    ("[URL]", r"https?://\S+|www\.\S+"),
    ("[SSN]", r"\b\d{3}-\d{2}-\d{4}\b"),
    ("[CARD]", r"\b(?:\d[ -]?){13,16}\b"),
    ("[PHONE]", r"\b\+?\d[\d\-\s().]{7,}\d\b"),
    ("[ZIP]", r"\b\d{5}(?:-\d{4})?\b"),
    ("[HANDLE]", r"(?<!\w)@\w+"),
]
# spaCy entity label -> placeholder
ENT_MAP = {
    "PERSON": "[PERSON]",
    "GPE": "[LOCATION]",
    "LOC": "[LOCATION]",
    "FAC": "[LOCATION]",
    "ORG": "[ORG]",
    "NORP": "[GROUP]",
}


def scrub(text, nlp, counts):
    t = str(text)
    for tag, pat in REGEX:
        t, n = re.subn(pat, tag, t)
        if n:
            counts[tag] = counts.get(tag, 0) + n
    doc = nlp(t)
    # replace entity spans right-to-left so offsets stay valid
    for ent in sorted(doc.ents, key=lambda e: e.start_char, reverse=True):
        tag = ENT_MAP.get(ent.label_)
        if tag and not ent.text.startswith("["):
            t = t[: ent.start_char] + tag + t[ent.end_char :]
            counts[tag] = counts.get(tag, 0) + 1
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="results/step3_unique_phrasings.csv")
    ap.add_argument("--out", default="results/step4_scrubbed.csv")
    ap.add_argument("--col", default="prompt")
    a = ap.parse_args()

    df = pd.read_csv(a.inp)
    nlp = spacy.load("en_core_web_sm")
    counts = {}
    df["prompt_scrubbed"] = df[a.col].map(lambda x: scrub(x, nlp, counts))
    n_changed = (df["prompt_scrubbed"] != df[a.col].astype(str)).sum()
    df.to_csv(a.out, index=False)

    print(f"rows                 : {len(df)}")
    print(f"prompts altered      : {n_changed} ({n_changed/len(df)*100:.1f}%)")
    print(f"redactions by type   : {dict(sorted(counts.items()))}")
    print(f"wrote {a.out}  (new column: prompt_scrubbed)")


if __name__ == "__main__":
    main()
