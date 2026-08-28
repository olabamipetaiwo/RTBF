#!/usr/bin/env python3
"""Step 6a - build blind coder sheets + hidden rule key + codebook."""

import argparse
import numpy as np
import pandas as pd

CODEBOOK = """# Coding manual - deletion-prompt labels

Each row is one free-text deletion request a participant wrote. Label each
prompt independently, using only the text in the `prompt` column. Do NOT
consult the automated labels or the rule key while coding - they exist to
be compared against your judgments afterward, not to guide them.

Below, each section is one column in the sheet: what it is, the values
you're allowed to put in it, and what each value means.

## prompt
Allowed values: pre-filled. Do not edit.
Meaning: the participant's original free-text deletion request - this is
the text every other column is labeling.

## Deletion Location - all
Allowed values: any combination of the six values below, pipe-joined,
e.g. `memory|conversation`. List every value that plausibly applies to
WHERE the prompt is asking the data to be removed from; order doesn't
matter. This dimension is about location in the system only - NOT about
what specific piece of data is targeted (that's Extent, below).
- `conversation` - the current or a referenced chat/message thread.
  e.g. "delete this conversation", "forget what I just sent", "clear this chat"
- `memory` - the assistant's persistent memory/profile of the user, not
  tied to one conversation.
  e.g. "forget what you know about me", "delete your saved info about me"
- `account_all` - everything, or the whole account.
  e.g. "delete all my data", "erase my entire account", "close my account"
- `prospective` - forward-looking: stop future use/storage, not
  necessarily deleting anything already stored.
  e.g. "don't use this going forward", "stop saving what I tell you"
- `backend_db` - explicitly names servers, databases, or training data,
  rather than "your memory".
  e.g. "erase this from your database", "remove it from your training data"
- `unspecified` - a deletion request where none of the above can be
  determined from the text. Note: a prompt naming a specific piece of
  data (e.g. "delete my location") without saying where it should come
  from is `unspecified` here even though it's very concrete under
  Extent - the two dimensions are independent, and it's expected/common
  for a prompt to be specific about WHAT but silent on WHERE.
  e.g. "please delete it", "delete my location", "get rid of that"

## Deletion Location - primary
Allowed values: exactly ONE value from the same six used in Deletion
Location - all, and it must be one of the values you selected there.
Meaning: if Deletion Location - all has more than one tag, this is the
single location that most determines what the system would actually have
to go do. Rule of thumb: prefer the narrowest location that is still
explicitly named over a vaguer one implied alongside it. Example: "delete
this conversation and don't use it in future" -> Deletion Location - all
= `conversation|prospective`, but Deletion Location - primary =
`conversation`, because deleting the conversation is the concrete action;
"don't use it in future" is a secondary condition on that same action,
not a separate deletion target. If Deletion Location - all has only one
value, Deletion Location - primary is that same value.

## Extent
Allowed values: exactly ONE of the four below - WHAT unit of data is
targeted, independent of where it should be removed from.
- `item` - one concrete, named piece or type of data (a location, an
  address, a phone number, a specific fact/message), even if quantified
  ("all my location data" is still `item` - the referent is one named
  data type, "all" just quantifies instances of it).
  e.g. "delete my location", "the address I gave you", "that phone number"
- `category` - an unnamed class of information, broader than one item but
  not framed as literal totality.
  e.g. "delete my personal information", "delete my data"
- `all` - explicit totality: everything, or the whole account/data,
  with no specific item or bounded category named.
  e.g. "delete everything", "erase my entire account", "close my account"
- `unspecified` - can't tell what unit of data is targeted from the text.
  e.g. "please delete it", "get rid of that" with no recoverable referent

## Form
Allowed values: exactly ONE of the four below - the grammatical mood of
the request, independent of tone (that's Tone, below).
- `imperative` - a direct command.
  e.g. "Delete this conversation.", "Please delete this conversation, thanks."
- `question` - phrased as a question: ends in "?", or opens with
  can/could/would/will/may.
  e.g. "Can you delete this conversation?"
- `statement` - a declarative "I want/need/would like ..." framing rather
  than a command.
  e.g. "I would like you to delete this conversation."
- `other` - doesn't fit any of the above.

## Tone
Allowed values: exactly ONE of the three below - independent of Form
(grammatical mood): an imperative, a question, or a statement can each
be friendly, polite, or neutral.
- `friendly` - opens with a greeting or casual address (hi, hey, hello).
  e.g. "Hey, can you delete my location data?"
- `polite` - contains a politeness marker (please, kindly, thanks/thank
  you, appreciate, grateful, "could you", "would you mind") but no
  opening greeting.
  e.g. "Please delete this conversation, thanks."
- `neutral` - neither a greeting nor a politeness marker.
  e.g. "Delete this conversation."
If a prompt has both a greeting and a politeness marker (e.g. "Hi, would
you please delete this? Thanks."), code it `friendly` - the greeting is
the more marked signal.

## Verb
Allowed values: exactly ONE of the four below - what kind of verb is used
for the deletion itself.
- `technical` - formal/technical verbs: delete, erase, remove, purge,
  wipe, scrub, expunge, clear, eliminate.
  e.g. "Please erase this record."
- `lay` - everyday/casual phrasing: forget, get rid of, take it off,
  throw away, stop keeping.
  e.g. "Just get rid of that."
- `mixed` - the prompt uses both a technical verb and a lay verb.
  e.g. "Please erase this, just get rid of it."
- `none` - neither kind of verb is used at all.
  e.g. "I don't want this saved."

## justification
Allowed values: `TRUE` or `FALSE`.
Meaning: `TRUE` if the participant gives any reason or motivation for the
deletion, beyond stating what to delete - e.g. "because I don't want it
public", "for privacy reasons", "I'm not comfortable with this", a
reference to GDPR/CCPA/"right to be forgotten". `FALSE` if the prompt only
states the request with no stated reason. Test: strip out the deletion
request itself - if what's left still reads as an independent reason,
code TRUE; if nothing's left (or it's just more detail about the target
or how thoroughly to delete it), code FALSE.
  TRUE  - "Delete my location because I want to feel safe."
  FALSE - "Please delete this location from your memory completely."

## notes
Allowed values: free text, optional - leave blank if nothing to flag.
Meaning: use it to note anything ambiguous, borderline, or where you
went back and forth, so it can be discussed during adjudication.
"""


def stratified(df, target, floor, seed):
    parts = []
    for locus, g in df.groupby("deletion_locus"):
        n = len(g)
        k = n if n <= floor else max(floor, round(target * n / len(df)))
        parts.append(g.sample(min(k, n), random_state=seed))
    return pd.concat(parts).sample(frac=1, random_state=seed).reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="results/step5_labeled.csv")
    ap.add_argument("--target", type=int, default=120)
    ap.add_argument("--floor", type=int, default=15)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--coders", type=int, default=2)
    a = ap.parse_args()
    df = pd.read_csv(a.inp).reset_index(drop=True)
    df["item_id"] = ["I%04d" % i for i in range(len(df))]
    samp = stratified(df, a.target, a.floor, a.seed)
    blank = samp[["item_id", "prompt"]].copy()
    for c in [
        "deletion_locus_all",
        "deletion_locus_primary",
        "data_granularity",
        "syntactic_form",
        "politeness",
        "verb_register",
        "justification",
        "notes",
    ]:
        blank[c] = ""
    for i in range(1, a.coders + 1):
        blank.to_csv(f"step6_coding_sheet_coder{i}.csv", index=False)
    samp[
        [
            "item_id",
            "prompt",
            "rationale",
            "deletion_locus",
            "deletion_locus_multilabel",
            "data_granularity",
            "syntactic_form",
            "politeness",
            "verb_register",
            "justification",
        ]
    ].to_csv("step6_rule_key.csv", index=False)
    open("step6_codebook.md", "w").write(CODEBOOK)
    print(f"sampled {len(samp)} of {len(df)} (floor={a.floor}/locus, seed={a.seed})")
    print("per-locus:", samp["deletion_locus"].value_counts().to_dict())


if __name__ == "__main__":
    main()
