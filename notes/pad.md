whci# RTBF Chatbot Deletion Study — Project Update

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

The data does support a story, with a clear order:
1. Motivation: people want to delete more when the data is sensitive (willingness M = 4.37 vs 3.98, p < .001).
2. Habit: they rely on the simplest interface actions, which they found themselves, with little guidance from the platform.
3. The gap: the method they rank as ideal, asking the chatbot to forget, is one they rarely use.
4. So what: the controls people trust and use are not the ones they would choose. The next question is whether those controls do what people expect, which is 4.3 and then the audit.

Proposal
- Reorder the four paragraphs in that order: Willingness, then Past use and Methods chosen (merged), then Ideal vs used.
- Replace my opening sentence with: "Users want to delete their data, more so when it is sensitive, but they rely on the few controls they found on their own, and the method they would prefer, asking the chatbot to forget, is one they rarely use."
- Add a closing sentence: "So the question is whether the controls people actually use do what they expect, which we turn to next."
- Cut the repeated "did not differ between scenarios" lines down to one clause, since they aren't part of the story.


---


Preseent all the results to Professors  today, we will choose the direction to go form there


---

Accounts
- CO-I1-E4 (granular facts editor): the default Copilot account, anchorexperiment@gmail.com, session sessions/copilot.json. It has no per-cell override in config.py or accounts.md.
- CO-I1-E6 (maximal): olataiwo839@gmail.com, session sessions/copilot__ui_migration_i1.json. It was moved off its original account on 2026-




----


1. Where deletion was asked (conversation, memory, backend database, whole account): no effect, ChatGPT came back at every level (from 41 of 53 unspecified to 10 of 10 memory) and Perplexity stayed low (1 of 10 to 14 of 53).
2. What was named (a specific fact, a general one, none): the only real effect, Perplexity gave the name in 16 of 109 specific requests against 10 of 17 with none named, while ChatGPT stayed high either way (87 of 107 against 15 of 17).
3. Mood (command, question, statement): no clear effect, Perplexity gave the name more for questions (6 of 14) than commands (19 of 105) but the group is small, and ChatGPT was high for all.
4. Tone (polite, neutral, friendly): no clear effect, ChatGPT 55 of 71 polite against 50 of 54 neutral, and the friendly group (6 requests) is too small to read.
5. Verb (technical, everyday): no effect, ChatGPT 100 of 122 technical against 6 of 7 everyday, Perplexity 26 of 124 against 3 of 7.
6. Giving a reason: no effect, ChatGPT 101 of 121 without against 7 of 10 with, Perplexity 28 of 122 against 3 of 11.
7. Asking for something else too (verify, get guidance, keep context): no effect, ChatGPT 97 of 118 with nothing extra against 6 of 7 asking to verify, and the extra-request groups are only 3 to 7 requests.


how

We had two people label each of the 138 requests by hand on the seven things, sent every request to all six chatbots, asked for the fact in a new chat about a month later, then counted per platform how often it came back for each label (no significance tests, so "no clear effect" means the counts look alike).


Yes, we counted separately for each platform, because the platforms behave so differently (ChatGPT almost always gave the fact back, Claude never did), and pooling them would have measured the platform instead of the wording.

It would tell us whether a gap between two groups (say polite against neutral) is bigger than chance would produce, but here it adds little: Claude is 0 everywhere, ChatGPT is high everywhere, and the groups are small, so a "not significant" result would show only that we couldn't tell, not that wording has no effect.



-----

rq in a fied list