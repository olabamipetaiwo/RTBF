#!/usr/bin/env python3
"""
Step 3 - Normalize and dedup (RTBF prompt analysis)
===================================================
Input : step1_prompts_long.csv  (415 prompt instances, one row each)
Output:
  step3_analysis_pool.csv    - normalized; each participant's exact + near
                               repeats collapsed; CROSS-participant duplicates
                               PRESERVED (this is the prevalence-safe pool)
  step3_unique_phrasings.csv - analysis pool with global exact-duplicates
                               removed (input to clustering / test-set selection)

Reportable choices
------------------
* Normalization: Unicode NFKC; curly quotes/dashes folded to ASCII; lowercased
  and whitespace-collapsed to form the comparison key `prompt_norm`. The
  original text is preserved in `prompt`.
* Exact dedup: WITHIN participant only. A participant who wrote byte-identical
  text in both blocks contributes that phrasing once.
* Near-dup collapse: WITHIN participant only. Similarity = cosine over
  character n-gram (3-5) TF-IDF, a LEXICAL measure chosen because a near-dup is
  a minor surface rewording, not a semantic paraphrase. Threshold = 0.90
  (stated, tunable). When two of a participant's prompts exceed threshold, the
  LONGER text is kept (ties -> Q4).
* Cross-participant duplicates are NOT collapsed here; identical text from two
  different people is genuine agreement in phrasing and is prevalence signal.
"""

import argparse, unicodedata, re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

NEAR_DUP_THRESHOLD = 0.90
NGRAM = (3, 5)


def normalize(text):
    t = unicodedata.normalize("NFKC", str(text))
    t = (
        t.replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2013", "-")
        .replace("\u2014", "-")
    )
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t


def collapse_within_participant(df, vectorizer):
    """Return kept-row indices after within-participant exact+near collapse."""
    X = vectorizer.transform(df["prompt_norm"])
    keep, dropped_exact, dropped_near = [], 0, 0
    for pid, g in df.groupby("pid"):
        idx = g.index.tolist()
        # exact within participant
        seen, exact_kept = {}, []
        for i in idx:
            key = df.at[i, "prompt_norm"]
            if key in seen:
                dropped_exact += 1
            else:
                seen[key] = i
                exact_kept.append(i)
        # near within participant (pairwise among survivors)
        survivors = []
        for i in exact_kept:
            merged = False
            for j in survivors:
                sim = cosine_similarity(X[i], X[j])[0, 0]
                if sim >= NEAR_DUP_THRESHOLD:
                    # keep longer; if current longer, swap it in for j
                    if len(df.at[i, "prompt"]) > len(df.at[j, "prompt"]):
                        survivors[survivors.index(j)] = i
                    dropped_near += 1
                    merged = True
                    break
            if not merged:
                survivors.append(i)
        keep.extend(survivors)
    return sorted(keep), dropped_exact, dropped_near


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="results/raw_prompts.csv")
    ap.add_argument("--pool_out", default="results/step3_analysis_pool.csv")
    ap.add_argument("--unique_out", default="results/step3_unique_phrasings.csv")
    a = ap.parse_args()

    df = pd.read_csv(a.inp)
    n_in = len(df)
    df["prompt_norm"] = df["prompt"].map(normalize)

    # one shared char-ngram space so within-person cosines are comparable
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=NGRAM, min_df=1)
    vec.fit(df["prompt_norm"])

    keep_idx, d_exact, d_near = collapse_within_participant(df, vec)
    pool = df.loc[keep_idx].reset_index(drop=True)

    # prevalence-safe pool keeps cross-participant duplicates
    pool.to_csv(a.pool_out, index=False)

    # globally-unique phrasings for clustering / test-set selection
    unique = pool.drop_duplicates("prompt_norm").reset_index(drop=True)
    unique.to_csv(a.unique_out, index=False)

    print(f"input prompt instances                     : {n_in}")
    print(f"within-participant EXACT repeats removed    : {d_exact}")
    print(
        f"within-participant NEAR repeats removed     : {d_near}  (cos >= {NEAR_DUP_THRESHOLD}, char{NGRAM})"
    )
    print(
        f"analysis pool (cross-participant dups kept) : {len(pool)}   -> {a.pool_out}"
    )
    print(f"  participants represented                 : {pool['pid'].nunique()}")
    print(f"global exact duplicates removed for cluster : {len(pool) - len(unique)}")
    print(
        f"unique phrasings (clustering input)         : {len(unique)}   -> {a.unique_out}"
    )


if __name__ == "__main__":
    main()
