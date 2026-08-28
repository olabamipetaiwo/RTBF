#!/usr/bin/env python3
"""Step 6b - score coder sheets. Run AFTER two humans fill them independently."""

import argparse
import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score

try:
    import krippendorff

    HAVE_K = True
except Exception:
    HAVE_K = False

LOCI = [
    "conversation",
    "memory",
    "account_all",
    "prospective",
    "backend_db",
    "unspecified",
]
SINGLE = [
    "deletion_locus_primary",
    "data_granularity",
    "syntactic_form",
    "politeness",
    "verb_register",
    "justification",
]
RULE_KEY_COL = {"deletion_locus_primary": "deletion_locus"}


def load(p):
    d = pd.read_csv(p, dtype=str).fillna("")
    for c in d.columns:
        d[c] = d[c].str.strip()
    return d.set_index("item_id")


def alpha(a, b):
    if not HAVE_K:
        return float("nan")
    cats = sorted(set(a) | set(b))
    m = {v: i for i, v in enumerate(cats)}
    rel = np.array([[m[v] for v in a], [m[v] for v in b]], dtype=float)
    return krippendorff.alpha(rel, level_of_measurement="nominal")


def to_set(x):
    return set(t for t in str(x).split("|") if t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--coderA", required=True)
    ap.add_argument("--coderB", required=True)
    ap.add_argument("--key", default="step6_rule_key.csv")
    a = ap.parse_args()
    A, B, K = load(a.coderA), load(a.coderB), load(a.key)
    ids = [i for i in A.index if i in B.index and i in K.index]
    A, B, K = A.loc[ids], B.loc[ids], K.loc[ids]
    print(f"items double-coded: {len(ids)}\n--- INTER-CODER AGREEMENT ---")
    for c in SINGLE:
        pa = (A[c] == B[c]).mean()
        kp = cohen_kappa_score(A[c], B[c])
        print(
            f"{c:14s} %agree={pa:.2f}  kappa={kp:.3f}  alpha={alpha(list(A[c]),list(B[c])):.3f}"
        )
    aset, bset = [to_set(x) for x in A["deletion_locus_all"]], [
        to_set(x) for x in B["deletion_locus_all"]
    ]
    jac = np.mean(
        [len(x & y) / len(x | y) if (x | y) else 1.0 for x, y in zip(aset, bset)]
    )
    per = {
        s: round(
            cohen_kappa_score([int(s in x) for x in aset], [int(s in y) for y in bset]),
            2,
        )
        for s in LOCI
        if sum(int(s in x) for x in aset) + sum(int(s in y) for y in bset) > 0
    }
    print(f"deletion_locus_all  meanJaccard={jac:.2f}  per-locus kappa={per}")
    print(
        "\ndisagreements to adjudicate:", {c: int((A[c] != B[c]).sum()) for c in SINGLE}
    )
    print("\n--- RULE vs HUMAN GOLD (coder-agreed items only) ---")
    for c in SINGLE:
        idx = [i for i in ids if A.at[i, c] == B.at[i, c]]
        rule = (
            K.loc[idx, RULE_KEY_COL.get(c, c)].astype(str).str.lower()
        )
        gold = A.loc[idx, c].astype(str).str.lower()
        print(
            f"{c:22s} n={len(idx):3d}  rule_accuracy={(rule.values==gold.values).mean():.2f}  kappa={cohen_kappa_score(rule,gold):.3f}"
        )
    idx = [i for i in ids if A.at[i, "deletion_locus_primary"] == B.at[i, "deletion_locus_primary"]]
    print("\ndeletion_locus confusion (rows=human gold, cols=rule):")
    print(
        pd.crosstab(
            A.loc[idx, "deletion_locus_primary"].str.lower(),
            K.loc[idx, "deletion_locus"].str.lower(),
        ).to_string()
    )


if __name__ == "__main__":
    main()
