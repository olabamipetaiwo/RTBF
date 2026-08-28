# Inter-Coder Comparison: Jihwan vs. Taiwo (50 shared prompts)



Where ->  Deletion Location -> Same construct (place data deleted from) — compared, 83.3% agreement 

Why -> Justification ->  Same construct (reason stated or not) — compared, 92% raw  kappa 0.468 

Jihwan - WHat - **24/50 *20 agree, 4 disagree** / Strategy
Taiwo  - Form / Tone / Verb 

What: 45/50 
Where: 18/50 
Why: 6/50
Strategy: 9/50

Only 2 of the 7 total dimensions across both schemes line up. 

Jihwan's own coding instructions explicitly said to set aside "how they phrased the request (e.g., tone or verb choice)" for now,

#### Testing all prompts on all platforms is not feasible

## 1. Location (Jihwan "Where" vs. Taiwo "Deletion Location")

memory → memory,
everywhere → account_all, 
history → conversation, 
database → backend_db,
account → account_all, 
messages → conversation, 
session → conversation. 





**Disagreements:**

| Item | Prompt | Jihwan | Taiwo |
|---|---|---|---|
| 3 | "delete all my personal information... for safety and security" | everywhere | unspecified |
| 8 | "remove... any address or location I mentioned... no longer connected to this conversation" (hedged: "memory * if records refer to the memory") | memory (hedged) | conversation |
| 12 | "Delete my location history" | conversation (history→conversation) | unspecified |
| 13 | "Please remove my location data entirely." | everywhere | unspecified |

Pattern in the disagreements: items 3 and 13 are both cases where the
prompt uses a broad/absolute word ("all", "entirely") and Jihwan read that
as a location claim ("everywhere"), while Taiwo's scheme treats an absolute
scope word as an **extent** signal, not a location one, and defaults
location to "unspecified" when no place is literally named -- a genuine
scheme-design difference, not a misread of the same text. Item 12 is a
narrower version of the same thing ("history" read as a place by Jihwan,
but not literally naming conversation/memory/database, so Taiwo's stricter
rule leaves it unspecified).

## 2. Reason Given (Jihwan "Why" non-empty vs. Taiwo "Justification" = TRUE)

The one binary, directly comparable dimension: did the prompt state a
reason for the deletion request at all?

|  | Taiwo: yes | Taiwo: no |
|---|---|---|
| **Jihwan: yes** | 2 (items 3, 28) | 4 (items 4, 23, 40, 48) |
| **Jihwan: no** | 0 | 44 |

- Percent agreement: **92.0%**
- Cohen's kappa: **0.468** (moderate -- raw agreement looks high mainly
  because "no reason" is the common case for both coders; kappa corrects
  for that base rate and is the more honest number here)
- All 4 disagreements are the same direction: Jihwan credited a reason,
  Taiwo didn't. Reading the 4 prompts (items 4, 23, 40, 48), each states a
  *forward-looking* concern ("I don't want this used to train/reference in
  future conversations") rather than a reason for deleting *per se* --
  plausible reading either way: Jihwan coded it as the "why" behind the
  request, Taiwo's scheme apparently doesn't count a forward-looking
  concern as a "justification." Worth a joint read before finalizing which
  reading goes in the paper.

## Not compared (different constructs, not different codings of the same thing)

- **Jihwan "What" vs. Taiwo "Extent"**: Jihwan's "what" names *which data*
  (17 highly specific free-text values, e.g. "the address I gave"); Taiwo's
  "extent" measures *how much* (item/category/all/unspecified). These
  aren't the same axis -- comparing them would mean comparing answers to
  two different questions.
- **Jihwan "Strategy" vs. Taiwo Form/Tone/Verb**: Jihwan's strategy (9/50
  filled: "all relevant information", "verification", "guidance for
  self-deletion", "replacement") has no counterpart in Taiwo's scheme at
  all, which instead captures grammatical mood, politeness, and verb
  choice -- entirely different phenomena.

## Bottom line for the meeting

 Location (83.3% on the 24 items ) splits
on whether an absolute-scope word ("all", "entirely") counts as a location
claim; 

Reason-given (92% raw / kappa 0.468) splits on whether a
forward-looking "don't use this later" concern counts as a justification.
