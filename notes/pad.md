# RTBF Chatbot Deletion Study — Project Update

Taiwo Olabamipe · University of Central Florida

---

## The Data

- 219 raw responses → 177 in the final analysis base
- Screened for attention checks and prior deletion experience
- Within-subject design: same participants rated a **less-sensitive**
  and a **more-sensitive** data-deletion scenario
- Sample: skews young (73% under 45), 62% bachelor's+, strong baseline
  privacy knowledge (5.06/6 correct on average)

---

## Analysis Rigor

- Every statistical test run through **two independent pipelines**
  (original `statsmodels`/`pingouin` stack vs. a from-scratch `scipy`-only
  reimplementation)
- 101 tests compared: **Pearson r = 0.9999**, **0 significance flips**
- Gives confidence the reported numbers aren't implementation artifacts

---

## Finding 1 — No Deletion Method Wins Outright

- Tested whether any method is statistically best on protection,
  effort, or perceived loss
- **Protection and loss:** no method separates from the others, at all
- **Effort:** the only scale with real separation — but even the
  best method ("delete this single conversation") only beats *one*
  rival, not all of them

---

## Finding 2 — Sensitivity Changes Feelings, Not Method Choice

- Willingness to delete rises significantly (+0.39) when data is
  more sensitive
- Perceived protection also rises significantly (+0.13)
- Effort and felt loss **don't move at all**
- Notably: *which method* you use never predicts protection — only
  *how sensitive the data feels* does

---

## Finding 3 — The Training-Data Blind Spot

- "This won't be used to train the model" is the **least-believed**
  outcome of deletion, for every method, in both scenarios
- 65–85% of participants don't expect deletion to stop their data
  from training the AI
- Consistent across the whole method set — not specific to any one
  deletion button

---

## Finding 4 — People Don't Verify, and the Gap Is Growing

- "I didn't know how to check" is the single most common response
  to "how did you verify deletion worked?" (~45% of the time)
- Participants consistently say they'd *ideally* use a heavier-duty
  method than the one they actually use
- That gap **widens**, not narrows, as sensitivity rises — the
  disconnect is biggest exactly when it matters most


---


----

The deletion-location definition was refined after piloting, and the
reliability reported here comes from coding under the final definition. A
location counts only when the prompt names it with an explicit referent
(conversation or chat, memory, account, or a database, server, or
training data); quantifiers such as ``all'' and generic containers such
as ``history'' or ``messages'' do not qualify. When a prompt names
several locations, a named database governs over a conversation or
memory, and a forward-looking clause governs over a named conversation.

-----

Honestly? It's a borderline fit — real strengths, real risks. The scope (GDPR Article 17 compliance in LLMs, 6 platforms, 828 cells, independent human coding with AC1, 177-person user study, recall audit) is squarely in S&P's privacy/measurement wheelhouse, and "do LLM providers actually honor erasure" is exactly the kind of empirical privacy question S&P reviewers care about right now.

The risk is that S&P reviewers often want a sharper technical contribution — an attack, a system, or a formal result — beyond "we measured compliance." Pure measurement + user study papers do get in, but they usually have to make a strong case that the finding is systemic, non-obvious, and actionable (not just "platforms are inconsistent, here's a table"). Your strongest angles for that framing are probably: (1) the cross-mechanism findings (NL-forget vs. UI-driven), (2) the recoverability + policy-consistency audit module, and (3) the gap between user mental models (survey) and actual platform behavior — the last one is the kind of hybrid technical+human-factors story S&P does occasionally reward.

If you want the honest ranking of venues for this specific paper as it stands:
1. USENIX Security — same tier, historically more welcoming to rigorous measurement work. Probably your best shot at a top-tier accept.
2. PETs (PoPETs) — natural home, high-quality, less brutal review variance, rolling submissions.
3. IEEE S&P — reach, but not crazy. Would want the technical-contribution framing tightened.
4. SOUPS — strong fit for the user-study half, lower tier than the above three.
5. CCS — similar bar to S&P, similar risk profile.

My call: submit to USENIX Security first, S&P second if that misses. Don't lead with S&P unless you're prepared to reframe the contribution around a specific systemic finding rather than the audit as a whole.



----

Right — concretely, S&P reviewers tend to grade "contribution" on one of these axes, so you'd want to pick which one(s) you're claiming and make it unmissable in the abstract and intro:

1. A system/methodology, not just a study. Frame the audit pipeline (injection → erasure → recall with layer-aware interpretation, PII scrub, dedup, AC1-validated coding, contamination-isolated accounts) as a reusable auditing framework for erasure claims on commercial LLMs — something future researchers or regulators could re-run against new platforms or new policy regimes. Right now the paper probably reads as "we ran a study"; the S&P framing is "we built an audit instrument and here's what it found on round one." Open-sourcing the pipeline reinforces this.
2. A threat model with a quantified attack surface. Define the adversary explicitly (curious third party, re-identification researcher, subpoena, future model trainer) and show that failed erasures expose a measurable amount of residual information — i.e., the recall phase isn't just "did they comply," it's "what fraction of erased facts remain extractable, and under what access pattern (same conversation / new chat / direct memory page)." That reframes the recall study as a leakage measurement, which S&P understands.
3. A taxonomy of erasure failure modes with mechanism-level explanations. Not "platforms are inconsistent," but "we identify N distinct failure modes (e.g., surface-layer deletion with retained embeddings, cross-conversation bleed via memory clustering, NL-forget acknowledgment without state change, confabulation-based re-emission like htiw etaicosseven), each attributable to a specific architectural choice." That turns the measurement into a structural finding reviewers can cite.
4. The user-study→platform-behavior gap as a security claim. Users form a mental model of "deleted means deleted"; your 177-person survey quantifies that expectation, and your audit quantifies the actual delta. Framed as "users operate under a privacy model the platforms don't honor, and here's the measured gap," this becomes a policy-security contribution rather than a UX observation.
5. Confabulation as a novel side channel. The CH-I1-E5 reversed-token result (htiw etaicosseven) is a genuinely interesting finding — if you can show it's reproducible and not a one-off, it's a small but novel leakage phenomenon worth a dedicated subsection. S&P likes "we found a new thing."

The cheapest tightening is #1 + #2 — reframe existing material, no new experiments. #3 and #5 are the most novel-feeling claims and would hit hardest with reviewers if your data already supports them. I'd avoid leading with #4 alone; it's stronger as a supporting beam than a load-bearing one at S&P (SOUPS/CHI would weight it higher).


-----

i am just curious, the best place to determine this is after the recall

Agreed — that's the right instinct. The recall results are the pivot point: they decide whether the paper's spine is "compliance audit" (fine, measurement-paper venues) or "measurable leakage with a threat model" (S&P/USENIX territory). Until you see the recoverability rates and the shape of the failure modes, picking a venue is premature — you'd be reverse-engineering a framing to fit a target instead of letting the finding pick the venue.

A few things worth watching for as recall comes in, since they'll decide the framing more than anything else:

- Magnitude. If recoverability is high (say >30% of erased facts recoverable via R1/R2/R3), the leakage framing writes itself. If it's low and scattered, the taxonomy/mechanism framing (#3 from earlier) becomes the stronger spine.
- Asymmetry across platforms or mechanisms. A clean split (e.g., NL-forget consistently leaks, UI-driven consistently doesn't; or memory-layer survives but conversation-layer doesn't) is a structural finding — S&P-shaped. Uniform mush across platforms is a policy finding — PETs/SOUPS-shaped.
- Any new side channels. If the htiw etaicosseven-style confabulation reproduces under R3's pressure variants on other cells, that alone can carry a subsection and sharpen the technical claim.
- The same-conversation R1 for typed erasures. That's the one most likely to show "erasure acknowledged but state unchanged" cleanly — which is the headline failure mode reviewers will remember.

First recall was due 2026-10-01 and the CH-I1-E5 run on 2026-10-05 is the first live one in the memory — so you're right at the start of the signal. I'd hold the venue decision until you have, at minimum, one full platform's recall completed; the shape will be obvious by then.


------

Recall due counts (875 pending; 1 already recalled, 30 with no due date — the 30 directive-frozen NL-forget/structural cells per memory):

┌────────────┬───────┐
│    Date    │ Count │
├────────────┼───────┤
│ 2026-10-08 │ 23    │
├────────────┼───────┤
│ 2026-10-09 │ 3     │
├────────────┼───────┤
│ 2026-10-10 │ 10    │
├────────────┼───────┤
│ 2026-10-11 │ 20    │
├────────────┼───────┤
│ 2026-10-12 │ 5     │
├────────────┼───────┤
│ 2026-10-13 │ 1     │
├────────────┼───────┤
│ 2026-10-14 │ 13    │
├────────────┼───────┤
│ 2026-10-18 │ 456   │
├────────────┼───────┤
│ 2026-10-19 │ 264   │
├────────────┼───────┤
│ 2026-10-24 │ 78    │
├────────────┼───────┤
│ 2026-10-30 │ 2     │
└────────────┴───────┘

-----

No — a low FOUND count doesn't hurt the paper. The audit's claim isn't "platforms leak lots of tokens"; it's "we systematically probed what their UIs claim to erase." All-NOT_FOUND is a valid, publishable result ("UI-promised erasure held in X% of cells, except these specific failures").

What carries the paper is the variation — across the 6 platforms, 3 injection loci (I1/I2/I3), erasure types, R1/R2/R3 layers, and UI-erasure vs NL-forget. Even a handful of FOUNDs become the interesting cells for Discussion; the rest become the baseline compliance rate.

Also, the paper already has load-bearing results independent of FOUND counts: 138-prompt coding (AC1=0.954), user study (n=177), deletion-location policy mapping, NL-forget refusal typology.

Where it would hurt: if every cell on every platform gave identical outcomes with zero platform/mechanism contrast. The layered design makes that unlikely.
