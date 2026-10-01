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


# Words that spaCy's small English model mislabels as entities in short
# imperative deletion requests, found by listing every entity it flagged
# across the 375 prompts (2026-09-30): sentence-initial "Delete" tagged ORG
# (19 of 35 flagged entities, e.g. "Delete all personal data" became
# "[ORG] all personal data"), "chatbot"/"AI Chatbot" tagged PERSON, "AI"
# tagged GPE, and the typo "hte" tagged ORG. None is identifying text, and
# redacting them removed the verb from the prompt. An entity is kept as
# non-PII only when EVERY one of its words is in this set, so a real name or
# place that merely contains one of these words is still redacted.
NOT_PII_WORDS = {
    "delete", "forget", "remove", "erase", "clear", "the", "hte", "location",
    "ai", "chatbot", "bot", "assistant",
}


def is_deletion_vocabulary(ent_text):
    words = re.findall(r"[a-z]+", ent_text.lower())
    return bool(words) and all(w in NOT_PII_WORDS for w in words)


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
        if tag and not ent.text.startswith("[") and not is_deletion_vocabulary(ent.text):
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
