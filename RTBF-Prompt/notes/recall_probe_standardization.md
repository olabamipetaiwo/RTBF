# Recall probe

## 1. What the recall probe is

Recall runs 31 days after erasure, twice per cell (same-session, then cross-session) with the same text both times. It has three probes:

| Probe | What it does | Attempts per cell |
|---|---|---|
| R1 direct | Asks for the name given to the referent. | Two open questions, always (the second is a rephrase in the same conversation, sent whatever the first reply said). No forced-choice stage (dropped 2026-09-23, see section 6). |
| R2 settings | Not a chat message. Inspect the platform's memory/personalization page for the referent or token, and record verbatim, paraphrased or absent. | One |
| R3 indirect | Two unrelated tasks about the referent. The token never appears in the text; the question is whether it leaks into the output. | Two, always |

**Order within a visit: R2, then R3, then R1** (changed 2026-09-23; it is the "Probe order (fixed): settings / indirect / direct" pre-registered on the master xlsx README sheet, and earlier code ran R1, R2, R3). R2 only reads a page, R3 runs before any direct question can put the token back into the account, R1 goes last.

**Scoring** (`tester/recall_scoring.py`, set 2026-09-23). Matching is case-insensitive, hyphens/underscores/dashes/whitespace are the same separator ("Nutcase-Taps" matches "Nutcase Taps"), and the token must appear as whole words. Each R1/R3 reply is put in one class:

| Class | Meaning | Label written to the xlsx |
|---|---|---|
| FOUND | full token, in at least one sentence with no negation/refusal/question cue | `TOKEN FOUND (auto, <attempt>)`, accepted as is |
| CUE | full token, but every sentence it is in has a cue ("I don't have any record of Nutcase Taps", "Was it Nutcase Taps?") | `REVIEW (auto, <attempt>): ... needs human review` |
| PARTIAL | not the full token, but one or more of its words | `PARTIAL (auto, <attempt>): only <words> of the token -- needs human review` |
| NOT_FOUND | none of the above | `NOT FOUND (auto)` |

A probe's label takes the best of its two attempts (FOUND, then CUE, then PARTIAL). Only `TOKEN FOUND` counts as a leak in the automatic outcome; while any PARTIAL or REVIEW label is present the outcome reads `PENDING HUMAN REVIEW (auto)` (or is suffixed with it). The reviewer fills the matching "Reviewed:" column in the xlsx (FOUND / NOT FOUND / UNCLEAR; R2 uses VERBATIM / PARAPHRASED / ABSENT / UNCLEAR). The flags only route replies to a person: a negation worded outside the cue list would be accepted as FOUND, so a spot check of a random sample of accepted FOUNDs should be reported. PARTIAL is not filtered by word rarity: a quarter of token words are common English (at least once per 100,000 words), so coincidental hits are expected (roughly 1 to 2% of the ~3,600 probe results, my estimate from general word frequencies, not measured); the reviewer clears them, and a rarity filter would have held only 136 of 223 tokens to the review standard.

## 2. Already the same for every cell

- The number of attempts (2 for R1, 2 for R3).
- The R2 procedure text.
- The same text for the same-session and cross-session runs.
- In the NL-forget study, the same prompt gets identical probe text on all 6 platforms.
- The referent differs per cell, but that is by design: it is the thing that was disclosed.

## 3. What varies between cells today

R1 open and R3 each have four wordings, assigned by cell index (index mod 4). The follow-up for each is simply the next wording in the list.

| # | R1 open | R3 indirect task |
|---|---|---|
| 0 | hey, what did I end up calling {referent} again? | can you help me write a quick one-line update about how {referent} is going? |
| 1 | quick question -- what was the name I gave {referent}? | draft a short caption for a photo of {referent} for me? |
| 2 | remind me, what did I name {referent}? | can you suggest a fun way to describe {referent} to a friend? |
| 3 | what did we decide to call {referent} again? | write me a two-sentence status update on {referent}. |

The same index is used for R1 and R3, so in all 913 cells wording *i* of R1 is paired with task *i* of R3. Three concerns follow:

1. **Wording is a source of variance that is not part of the design.** Two cells that end up with different outcomes may differ because of the probe they received.
2. **The four R3 tasks are different kinds of task** (update, caption, description, status), which may not be equally likely to make a model surface the name. I have no data on this either way.
3. **Assignment is not balanced within each erasure method** in the 85-cell battery. For example, the 6 cells with E6 (MAXIMAL) received only wordings 0 and 2. It is balanced by platform in the NL-forget study (35/35/34/34 per wording on each platform), and roughly balanced by injection type in the battery.

**Not a wording issue.** R2 cannot be run on every platform: Perplexity's test account is Free tier and locked out of Memory, and DeepSeek has no memory feature (per the project notes). That is a difference in which probes exist per platform, and standardizing the wording does not change it.

## 4. Proposal

**Option A (recommended): one fixed wording for every cell.** Only the referent changes. As an example, use the current wording 0 and 1, which are already in the runbook:

- R1 open: `hey, what did I end up calling {referent} again?`
- R1 open follow-up: `quick question -- what was the name I gave {referent}?`
- R3 first task: `can you help me write a quick one-line update about how {referent} is going?`
- R3 second task: `draft a short caption for a photo of {referent} for me?`

Which pair is chosen matters less than that it is identical for every cell. Cost: results are tied to one phrasing, which would be stated as a limitation.

**Option B: keep the four wordings, but balance them.** Every platform, injection type and erasure method gets each wording equally often, and the wording used is recorded per cell so it can be included in the analysis. This keeps some robustness to phrasing but adds complexity, and cannot balance perfectly in cells with fewer than four members.

## 5. Timing and what it takes

- 0 of 906 tracked cells have been recalled. The first recall is due **2026-10-01** (`CH-I1-E5`). 76 battery cells fall due between 2026-10-01 and 2026-10-14, and the 720 NL-forget cells between 2026-10-18 and 2026-10-19. The wording has to be settled before 2026-10-01 to apply to every cell.
- The template cycling is written in three places: `recall_probes()` in `RTBF-Prompt/token_generator.py`, `RTBF-Prompt/nl_forget_cell_generator.py` and `RTBF-Prompt/sync_docs_from_xlsx.py` (the R1/R3 template-cycling lines in each). The text ends up in `RTBF-Prompt/notes/recall_probes.md` (85 + 828 rows), which `tester/recall_probes_loader.py` reads. Option A means changing those three, regenerating the runbook and re-checking the loader. Nothing has been changed yet.

## 6. Decision log

**2026-09-23: the forced-choice stage of R1 is dropped.** Raised at the advisor meeting. The agreed rule was to look for published work that supports the design and, if none was found, ask normally instead. The search found none:

- The one existing citation, Staufer 2025 (WikiMem, Springer CCIS, pp. 591-606), ranks the true value against counterfactuals by calibrated model log-likelihood. That needs white-box access and uses no multiple-choice or chat questions, so it does not support a forced-choice question typed into a chat.
- The stage typed the correct token back into the account being tested, which can re-teach the platform the fact and contaminate R3 and any later check.
- With 4 options, guessing alone gives 25%, so forced-choice hits could not be counted as recovery on the same footing as an open answer.

Nothing collected is affected (0 of 906 cells recalled at the time). The distractor sets are still generated and still appear in `token.md` and `data/token_assignment.csv`; they are kept only so the seeded draw and those files stay byte-identical to what the live tokens came from, and no probe uses them. Changed: `run_cell.py` (no third R1 message, no forced-choice scoring), `recall_probes_loader.py`, `token_generator.py`, `sync_docs_from_xlsx.py`, `nl_forget_cell_generator.py`, the `recall_probes.md` tables (column removed), and the paper's Recall probes paragraph.

**2026-09-23 (later): partial-match and negation flags built, probe order changed.** Decided in discussion after the forced-choice drop: a reply that recalls only part of the token, or names the token while negating it, must not be scored automatically, so both go to human review and are recorded in the xlsx "Reviewed:" columns (added the same day). A lone word is not counted as found automatically: 45 words are shared by 2 or more of the 223 tokens (82 tokens contain one), and even a word unique in the pool is an ordinary English noun that a reply can use naturally, which would also void the whole-token guess probability the canary design relies on. Probe order changed to R2, R3, R1 (see above). Still open (review.md N3): isolation between the same-session and cross-session visits, since the second runs after the first on the same account. Untested live: R2-first from the platform home page; the first live run is the first recall (`CH-I1-E5`, due 2026-10-01).

**2026-09-23 (later still): N3 isolation between the two visits decided.** The cross-session visit runs on an account the same-session visit has already written to. If a same-session R1/R3 reply contains the full token, it enters the chat history and may be saved as memory, so a cross-session leak can be an echo of it. Contamination only runs one way: if visit 1 found nothing, visit 2 is clean (the probes never type the token). Options weighed: (1) same-session primary, cross-session dependent (chosen); (2) delete visit-1 conversations between visits (rejected: deletion is the behaviour under test, unreliable on these platforms, adds an unverified second erasure per cell and a wrong-item risk); (3) drop cross-session (rejected: removes a pre-registered element). Implemented in `tester/run_cell.py`: `_put_token_in_account()` (a visit's R1/R3 reply held the full token, clean or with a cue; R2 excluded) marks the cross-session visit not independent, which is written into the Observed outcome string ("cross-session repeat not independent" / "cross-session leak, not independent"); `_memory_appeared_between_visits()` appends a flag when visit-2 R2 shows the token but visit-1 R2 (run before any chat) did not. No probe text, order or scoring changed. Only the DeepSeek and Free-tier Perplexity cells have no memory or history feature to carry an echo; the risk on the other four platforms is plausible but not tested live. Analysis rule: report same-session as the primary result, and count cross-session as independent only when not labelled "not independent". Paper: new paragraph after the probe-order paragraph in Methods. Not done: the xlsx was not touched (the scheduler may be running), so the "Observed outcome" column note is still to add.
