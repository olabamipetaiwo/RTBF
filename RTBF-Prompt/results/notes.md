Extract prompt result

Participant rows in export : 217
Prompt instances extracted : 415
Participants contributing  : 209
  answered both blocks     : 206
  Q4 only                  : 1
  Q5 only                  : 2
Per-block counts           : {'Q4': 207, 'Q5': 208}


Unit Reults

analytic unit           : participant
participants (unit n)   : 209
prompt instances        : 415
<!-- 206 participants contributed 2 prompts each, and 3 participants contributed 1 prompt each. -->
prompts per participant : {2: 206, 1: 3}
participants w/ 2 prompts: 206
  identical in both blocks: 14 (6.8%)

Normalize Results

input prompt instances                     : 415
within-participant EXACT repeats removed    : 15
within-participant NEAR repeats removed     : 7  (cos >= 0.9, char(3, 5))
analysis pool (cross-participant dups kept) : 393   -> results/step3_analysis_pool.csv
  participants represented                 : 209
global exact duplicates removed for cluster : 18
unique phrasings (clustering input)         : 375   -> results/step3_unique_phrasings.csv


Scrub results

rows                 : 375
prompts altered      : 32 (8.5%)
redactions by type   : {'[LOCATION]': 12, '[ORG]': 20, '[PERSON]': 3}


Features Extraction

Rows labeled : 375  (col='prompt')

SCOPE:
scope
item            28.0
memory          19.5
conversation    19.2
account_all     14.7
unspecified     12.0
prospective      3.7
backend_db       2.9

FORM:
form
polite_imperative    44.3
bare_imperative      22.9
other                12.5
question              8.3
polite_other          8.3
statement             3.7

verb_register: {'technical': 316, 'none': 25, 'lay': 23, 'mixed': 11}
justification: 13 (3.5%)
multi-scope prompts: 182


Features Extraction v2 (2026-08-24) — advisor feedback: split scope into
deletion_locus (WHERE) + data_granularity (WHAT), split form into
syntactic_form (mood) + politeness (tone). item removed from locus.

Rows labeled : 375  (col='prompt')

DELETION_LOCUS:
deletion_locus
unspecified     40.0
memory          19.5
conversation    19.2
account_all     14.7
prospective      3.7
backend_db       2.9

DATA_GRANULARITY:
data_granularity
specific_item    72.5
unspecified      18.7
all               5.1
category          3.7

SYNTACTIC_FORM:
syntactic_form
imperative    67.2
other         20.8
question       8.3
statement      3.7

politeness: {'polite': 219, 'bare': 156}
verb_register: {'technical': 316, 'none': 25, 'lay': 23, 'mixed': 11}
justification: 13 (3.5%)
multi-locus prompts: 61

Step 6a resampled: 137 of 375 (floor=15/locus, seed=42)
per-locus: {'unspecified': 48, 'memory': 23, 'conversation': 23, 'account_all': 18, 'prospective': 14, 'backend_db': 11}

Sample reconciliation (2026-08-24): the 137-item resample above was a fresh
draw, different from the 138-item sample already sent to Jihwan (coding/RTBF
Taiwo Coding Sheet .xlsx) and already hand-coded by Taiwo in that same file.
Decision: the 138-item list in coding/ is authoritative (it's what was
already distributed). step6_rule_key.csv, step6_coding_sheet_coder1.csv, and
step6_coding_sheet_coder2.csv were regenerated against that exact 138-item
list (item_id derived by exact-text match against step5_labeled.csv) instead
of the fresh 137-item draw. Only 108/138 of these overlap the discarded
137-item draw; the other 30 are prompts the old scope-based (pre-revision)
sampling had included that the new locus-based sampling didn't.
CAVEAT: build_sheet.py's stratified() sampler was NOT modified - if it's
rerun, it will draw a new random 137-item sample again and silently diverge
from this reconciled 138-item list. Do not rerun build_sheet.py without
re-doing this reconciliation, or pin/hardcode the 138-item list first.




## CODING DIMENSION


1. Split scope → deletion_locus (item removed) + new data_granularity

Privacy/data-taxonomy work treats "where the data lives in the system" and "what unit of data" as separate axes — one multi-dimensional GDPR taxonomy paper explicitly separates data categories from data qualifiers, and describes granularity as its own hierarchy (dataset → table → attribute level). That maps cleanly onto your professor's point: item was smuggling a granularity judgment into what should be a pure locus dimension.

- deletion_locus (was scope_all/scope_primary, minus item): conversation, memory, account_all, prospective, backend_db, unspecified — unchanged definitions, just item removed.
- data_granularity (new): what unit of data is targeted, independent of where —
  - specific_item — one named fact ("my address", "that phone number")
  - category — an unnamed class ("my personal information", "my data")
  - all — totality/everything, no specific referent
  - unspecified — can't tell

2. Split form → syntactic_form + politeness

This is exactly the separation Searle's speech-act mood taxonomy (declarative/interrogative/imperative as the grammatical move) and Danescu-Niculescu-Mizil's politeness classifier (indirection, deference, impersonalization, modality as an orthogonal axis of how the same mood is delivered) argue for — mood and politeness strategy are independently varying.

- syntactic_form: imperative, question, statement, other — pure grammatical mood, no politeness folded in.
- politeness: polite / bare (or reuse the existing politeness_n marker-count feature from Step 5 as a continuous companion instead of/alongside a binary label — your call).

3. Grounding in NLP norms — the two papers that most directly back this: A Computational Approach to Politeness with Application to Social Factors (Danescu-Niculescu-Mizil et al., ACL 2013 — the standard politeness-classification reference, Stanford Politeness Corpus) and Searle's directive speech-act taxonomy as operationalizifiers (mood ≠ politeness strategy). Worth citing both in your methods section as precedent for why these are separate dimensions rather than one conflated form column.


## Setup Experimtns

1. Isolation (the core "no interference" requirement)
- Fresh, unauthenticated or freshly-provisioned account/session per trial — no shared conversation history, memory, or personalization state carried between prompt conditions or platforms.
- Separate browser profile / sandboxed environment per platform per trial (cookies, local storage, and any cross-session memory features reset between runs).
- One prompt-condition per session — never test two different prompt variants in the same conversation, since the model's response to the second is then confounded by the first.

2. Standardized protocol (identical across all 6 platforms)
A fixed sequence per trial: (1) seed the session with a controlled piece of test PII, (2) issue the deletion request using one of your coded prompt variants verbatim, (3) apply a tiered verification probe (below), (4) log the raw transcript + classified outcome.

3. Tiered verification for "was it actually deleted" — black-box means you can only observe behavior, so use escalating probes rather than trusting the model's own claim:
- Same-session recall (weak signal — could be conversational suppression, not real deletion)
- New-session recall, same account (tests persistent memory/profile deletion)
- Delayed recall after 24–48h (tests whether deletion is immediate vs. batch-processed on the backend)

4. Trial design for statistical validity
- Multiple independent trials per (platform × prompt-dimension) cell — LLM outputs are stochastic, so single-shot results aren't defensible.
- Randomize trial order across platforms and prompt conditions to control for time-based drift (model updates mid-study are a real confound with these platforms).
- Record and pin the model version/date for each platform at time of test — reproducibility requirement.

5. Documentation for IEEE S&P submission
- Explicit threat/capability model: "black-box" = no privileged API access, no cooperation from the platform, observation-only.
- Pre-registered protocol and outcome taxonomy (complied / partial / refused / deflected / silently ignored) before running trials, to avoid post-hoc categorization bias.
- ToS note: automated/scripted testing of consumer chat UIs may violate platform ToS — worth a line in limitations/ethics.



<!-- Resolve -->

Isolation

- One fresh, unauthenticated account per (I,E) cell, not per platform. Since dry runs are done but the full battery hasn't started, this is fully actionable now, before any real data collection begins.
- Separate browser profile per account (cookies, local storage, cache cleared between cells) so no session-level state survives across cells even within the same platform.
- One prompt-condition per session, never mixed, per the original point 1: this is already implicit in the fixed per-cell order but should be stated as an explicit rule so it survives contact with whoever actually runs the trials.
- Practical note: this multiplies account-provisioning overhead across however many (I,E) cells exist per platform times 6 platforms. Worth a short, scripted account-setup checklist (disposable email alias, standard signup steps) so this isn't a bottleneck, but that's an implementation detail for whenever you're ready to build it.

Standardized protocol

Keep the locked fixed per-cell order in §3 exactly as written (inject, verify, erase, post-erasure R2, cross-session leg, same-session leg, resurrection R2). Add one explicit requirement: every reading in that sequence gets a raw transcript plus a classified outcome logged at the time it's taken, not reconstructed after the fact.

Verification timing

Standardize the resurrection check to 48 hours for all six platforms, not just Claude's synthesis-driven case. 48h clears Claude's stated ~24h synthesis window and gives a consistent, defensible interval to cite for every platform, rather than justifying a different delay per platform.

Trial design

Single-shot (n=1) per cell, as designed. This goes into the paper's limitations section explicitly: LLM output stochasticity means a single reading per cell can't distinguish a one-off anomaly from systematic behavior, and that's an acknowledged constraint, not an oversight.

One thing I'd still flag: dry runs already ran in a fixed order (Claude first), but the full battery hasn't started, so there's a real opportunity to randomize or at least document a principled order for the actual data-collection runs, rather than defaulting to the same fixed order used for piloting. Worth a quick decision, but not blocking, since Perplexity-last and DeepSeek's placement already have stated methodological reasons (web-search contamination control) that a pure randomization would undermine.

Outcome coding

Pre-register a basic outcome taxonomy before any fullied / partial / refused / deflected / silently ignored. This is locked before data collection starts. Deeper failure-mode themes (what previously lived in the dropped FM-1..FM-5 schemill emerge inductively from the data afterward, pers just adds a bias-resistant floor under the headlinecompliance numbers.                                                                                                            
Documentation                                                                                                                  
- Explicit black-box capability statement: no API/backend access, no platform cooperation, observation-only through the consumeinterface.
- ToS limitation note: automated/scripted testing of consumer chat UIs may violate platform ToS, worth one sentence in         ethics/limitations.
- Record model version and test date per platform per cell (not currently in §3), since these six products update on their own schedules during the run window.

## Anchor

Relevant published work:
- Carlini, Liu, Erlingsson, Kos, Song, "The Secret Sharer: Evaluating and Testing Unintended Memorization in Neural Networks," USENIX Security 2019 (arXiv:1802.08232) — the foundational canary methodology: an injected probe must have quantifiably plow a priori guess-probability so later recall can't be attributed to chance.
- Meeus, Wutschitz, Zanella-Béguelin, Tople, Shokri, "The Canary's Echo: Auditing Privacy Risks of LLM-Generated Synthetic Text," ICML 2025 (arXiv:2502.14921) — canaries need an in-distribution/naturalistic carrier, or filters strip them and they read as gibberish rather than genuine disclosure.
- Maini, Feng, Schwarzschild, Lipton, Kolter, "TOFU: A Task of Fictitious Unlearning for LLMs," arXiv:2401.06121 (COLM 2024) — precedent for using wholly fictitious, non-sensitive synthetic content as the forget-target, avoiding both IRB exposure and confounds from real-world facts the model already knew.
- Staufer, "What Should LLMs Forget? Quantifying Personal Data in LLMs for Right-to-Be-Forgotten Requests" (WikiMem), XKDD 2025 @ ECML PKDD (arXiv:2507.11128) — scores recall against plausible false alternatives, not just presence/absence, to rule out generic guessing.

Proposed scheme (satisfies DECISIONS Q17's "naturalistic project codenames, non-sensitive, unique per cell"): a two-word fictitious project codename (e.g. "Project Amber Falcon"), drawn deterministically (seeded RNG, reproducible) without replacement from two disjoint word lists, one pair assigned per cell across all 88 cells (76 MASTER + 12 FILE SUBSTUDY — matches the SETUP sheet's 88 total). Word-list size kept well above 88 to keep per-cell guess-probability low (Carlini), no appended digits/codes so it stays conversationally natural (Meeus), filtered to exclude real trademarks/places/PII-like terms (TOFU), plus a small set of false-alternative distractors per anchor for scoring recall probes later (Staufer)