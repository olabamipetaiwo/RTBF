#!/usr/bin/env python3
"""
Step 5 - Feature extraction (labeling)
Deterministic rule-based labels. Runs on ORIGINAL prompt text, case-insensitive.

`deletion_locus` = WHERE the data should be removed from (system-side location).
`data_granularity` = WHAT unit of data is targeted, independent of locus.
These used to be conflated in one `scope` column (with `item` standing in for
granularity); split per advisor feedback so locus and granularity are scored
as separate dimensions. Likewise `syntactic_form` (grammatical mood) and
`politeness` (tone) used to be conflated in one `form` column; split so mood
and politeness strategy - independently varying per speech-act/politeness
theory - are separate dimensions instead of one column with a cross-product
of values (e.g. `polite_imperative`).

Precedence = list order within each pattern list; for `deletion_locus`, all
matches are kept in deletion_locus_multilabel. For `data_granularity`,
first match wins, preferring the narrowest concrete referent (a specific-item
noun) over vaguer category/totality language mentioned alongside it - same
narrowest-wins principle as deletion_locus_primary.
"""
import argparse, re
import pandas as pd

LOCUS_PATTERNS = [
    ("backend_db",   r"\b(database|data ?base|server|backend|back-end|"
                     r"training (data|set)|all available files|all files|"
                     r"private and public|wherever .*stored|everywhere|"
                     r"third[- ]part|from (your|the) system)\b"),
    ("account_all",  r"\b(all (my|the)? ?(personal )?(data|information|info)|"
                     r"everything (you|about)|all data about me|my account|"
                     r"entire account|delete .*account|close .*account|"
                     r"all (my )?location|all the data|any (and all|data)|all personal)\b"),
    ("memory",       r"\b(memory|remember|memoris?ed|memoriz?ed|saved|stored?|"
                     r"what you know about me|you'?ve stored|retain|keep on file|"
                     r"you have (for|on|about) me|collected about me|have (for|about) me)\b"),
    ("prospective",  r"\b(don'?t (use|store|keep|save)|do not (use|store|keep|save|reference)|"
                     r"going forward|in future|future conversation|"
                     r"stop (storing|keeping|using)|no longer)\b"),
    ("conversation", r"\b((this|that|our|the|previous|current|prior) (chat|conversation|thread|session)|"
                     r"conversation (we|i) (just )?had|conversation (on|about)|chat history|"
                     r"(conversation |chat )?history|what i (just )?(sent|said|typed|shared|submitted|mentioned)|"
                     r"this message|from (this |the )?(chat|history|conversation)|from here)\b"),
]

GRANULARITY_PATTERNS = [
    ("specific_item", r"\b((this|the|my|current|that) location|location data|location or metadata|"
                     r"location (i|that i) (mentioned|shared|gave|submitted)|"
                     r"address|phone ?number|e-?mail|zip ?code|city|state information|"
                     r"medical history|social security|date of birth|birthday|credit card|"
                     r"data (about|regarding) (me|my|[a-z]+)|"
                     r"said information|that information|the info i|the text that|this message)\b"),
    ("all",          r"\b(everything|entire account|whole account|close (my|the) account|"
                     r"all of it|entirely|wipe (me|everything) out|"
                     r"all (of )?(my |the )?(personal )?(data|information|info))\b"),
    ("category",     r"\b(personal (data|information|info)|my (data|information|info)|"
                     r"the (data|information|info)|any (data|information|info)|"
                     r"information about me|info about me|data about me|details about me)\b"),
]

QUESTION_STARTERS    = r"^\s*(can|could|would|will|may|please can|could you please)\b"
STATEMENT_STARTERS   = r"^\s*(i\s+(want|would like|'?d like|need|request|wish|would prefer)|i'?d (want|like|prefer))\b"
IMPERATIVE_STARTERS  = r"^\s*(please\s+)?(delete|erase|remove|forget|clear|wipe|purge|scrub|expunge|eliminate|get rid|stop|do not|don'?t|drop)\b"
POLITENESS_MARKERS   = [r"\bplease\b", r"\bkindly\b", r"\bthank(s| you)?\b", r"\bappreciate\b",
                        r"\bgrateful\b", r"would you mind", r"could you", r"if (you could|possible)"]
TECH_VERBS = r"\b(delete|erase|remove|purge|wipe|scrub|expunge|eliminate|clear)\b"
LAY_VERBS  = r"\b(forget|get rid of|take (it |them )?off|throw (away|out)|stop keeping)\b"
JUSTIFICATION = (r"(because|since|so that|i don'?t want|for .{0,20}(reason|privacy|security)|"
                 r"worried|uncomfortable|concern|gdpr|ccpa|right to be forgotten|no longer want)")

def _has(pat, t): return re.search(pat, t, flags=re.I) is not None

def locus_labels(t):
    matches = [name for name, pat in LOCUS_PATTERNS if _has(pat, t)]
    return (matches[0] if matches else "unspecified"), ("|".join(matches) if matches else "unspecified")

def data_granularity(t):
    for name, pat in GRANULARITY_PATTERNS:
        if _has(pat, t): return name
    return "unspecified"

def syntactic_form(t):
    if t.strip().endswith("?") or _has(QUESTION_STARTERS, t): return "question"
    if _has(STATEMENT_STARTERS, t):                           return "statement"
    if _has(IMPERATIVE_STARTERS, t):                          return "imperative"
    return "other"

def politeness_n(t): return sum(_has(m, t) for m in POLITENESS_MARKERS)

def politeness(t): return "polite" if politeness_n(t) > 0 else "bare"

def verb_register(t):
    tech, lay = _has(TECH_VERBS, t), _has(LAY_VERBS, t)
    if tech and lay: return "mixed"
    if tech:         return "technical"
    if lay:          return "lay"
    return "none"

def featurize(prompt):
    t = str(prompt).strip()
    locus, multi = locus_labels(t)
    return {"deletion_locus": locus, "deletion_locus_multilabel": multi,
            "data_granularity": data_granularity(t),
            "syntactic_form": syntactic_form(t), "politeness": politeness(t),
            "politeness_n": politeness_n(t),
            "verb_register": verb_register(t), "justification": _has(JUSTIFICATION, t),
            "word_count": len(t.split())}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="results/step3_unique_phrasings.csv")
    ap.add_argument("--col", default="prompt")
    ap.add_argument("--out", default="results/step5_labeled.csv")
    a = ap.parse_args()
    df = pd.read_csv(a.inp)
    feats = pd.DataFrame([featurize(p) for p in df[a.col]])
    out = pd.concat([df, feats], axis=1)
    out.to_csv(a.out, index=False)
    print(f"rows labeled : {len(out)}  (col='{a.col}')")
    print("\nDELETION_LOCUS:\n" + (out["deletion_locus"].value_counts(normalize=True)*100).round(1).to_string())
    print("\nDATA_GRANULARITY:\n" + (out["data_granularity"].value_counts(normalize=True)*100).round(1).to_string())
    print("\nSYNTACTIC_FORM:\n" + (out["syntactic_form"].value_counts(normalize=True)*100).round(1).to_string())
    print("\npoliteness:", out["politeness"].value_counts().to_dict())
    print("verb_register:", out["verb_register"].value_counts().to_dict())
    print("justification:", int(out["justification"].sum()), f"({out['justification'].mean()*100:.1f}%)")
    print("multi-locus prompts:", int(out["deletion_locus_multilabel"].str.contains(r"\|").sum()))

if __name__ == "__main__":
    main()