# Plan: cross-platform analysis

## Question

Do the patterns in `all.md` hold when the platforms are compared directly? In particular: does the platform decide whether the fact is retrieved; does a method aimed at a different store leave the fact retrievable; and do the checks a user can make track the outcome?

## Scope

- Built on the reviewed outcomes in `RTBF-Analysis/outputs/tables/audit_outcomes.csv`.
- Can't tell stays its own count (Dr Li). Where an analysis needs an outcome on every platform, it uses **retrieved in a new conversation, yes or no**, which is observable everywhere, and is labelled as retrieval, never as an erasure rate.
- Copilot joins when its recall is complete (open point).

## 1. Typed requests: the same prompt across platforms (main)

- Each of the 138 prompts ran on every platform, so each prompt is its own control (a paired design).
- Cells: prompts recalled on every included platform (about 120, limited by Gemini).
- Outcome: retrieved in a new conversation, yes or no.
- Test: Cochran's Q across platforms, then McNemar for each pair, corrected for multiple comparisons (Holm, open point). Each platform's rate with a Wilson 95% interval.
- Also: whether the prompts retrieved on one platform are the same ones retrieved on another.
- **Possible claim:** the platform, not the prompt, decides whether the fact is retrieved.

## 2. Erasure scope (main)

- Main grid only (about 70 cells).
- Groups from the commitment type coded from each help page: **deletes** (the method targets where the fact is kept) against **does not delete / unrelated** (it targets a different store).
- Outcome: retrieval rate in each group, overall and per platform.
- Test: Fisher's exact test overall; per platform descriptive only (groups too small).
- **Possible claim:** a method aimed at a different store leaves the fact retrievable, on every platform.

## 3. Do the user's checks track the outcome? (descriptive)

- **Same-conversation check:** per platform, same-conversation result against new-conversation retrieval (2×2), with how often the check gives the right answer and the direction in which it fails.
- **Settings-page check:** interface change against outcome (the 33 interface erasures showing a completed deletion with a known outcome), and memory page against retrieval.
- Counts and percentages with Wilson intervals; no tests (groups uneven, several empty).

## 4. Withholding and policy (descriptive)

- Refusals citing the request, per platform (reviewed: ChatGPT, Perplexity).
- Policy verdicts per platform: kept, broken, can't tell, and no commitment.
- Tables only; no tests.

## Not done

| Analysis | Reason |
|---|---|
| One model across platforms and methods | Too many empty groups: DeepSeek retrieved nothing, Claude erased everything. |
| Tests on the can't-tell share | A measurement limitation, not a platform comparison. |
| Tests on refusals or policy | Only two platforms refuse; most policy verdicts are no commitment. |

## Script

New `RTBF-Analysis/src/cross_platform.py`, reading only `audit_outcomes.csv` and the reviewed refusal sheets; output `outputs/results/cross_platform.md`. Re-run after every recall batch.

## Open points

1. Copilot: include only when its recall is complete, or now as partial?
2. Holm correction for the pairwise McNemar tests in analysis 1? whhhtis

## My question
- is this a statiscal test

Which parts are statistical

┌────────────────────────────────────────────┬─────────────┬────────────────────────────────────────────────────────────────────────────┐
│                  Section                   │    Type     │                                  Methods                                   │
├────────────────────────────────────────────┼─────────────┼────────────────────────────────────────────────────────────────────────────┤
│ 1. Same prompt across platforms            │ Inferential │ Cochran's Q, then pairwise McNemar, with Holm correction; Wilson intervals │
├────────────────────────────────────────────┼─────────────┼────────────────────────────────────────────────────────────────────────────┤
│ 2. Erasure scope                           │ Inferential │ Fisher's exact test                                                        │
├────────────────────────────────────────────┼─────────────┼────────────────────────────────────────────────────────────────────────────┤
│ 3. Do the user's checks track the outcome? │ Descriptive │ Counts, percentages, Wilson intervals                                      │
├────────────────────────────────────────────┼─────────────┼────────────────────────────────────────────────────────────────────────────┤
│ 4. Withholding and policy                  │ Descriptive │ Tables                                                                     │
└────────────────────────────────────────────┴─────────────┴────────────────────────────────────────────────────────────────────────────┘

Why these methods

- Cochran's Q (section 1): the same 138 prompts ran on every platform, so the data are paired. Each prompt gets a yes or no for "retrieved" on each platform. Cochran's Q is the extension of McNemar to more than two related binary samples. It asks whether the retrieval rate differs across platforms at all. A plain chi-square would be wrong, because it treats the platforms as independent groups and ignores that each prompt is its own control.
- McNemar for each pair: Q only says that some platform differs. McNemar says which pair differs. It uses only the discordant prompts, meaning retrieved on A but not on B, or the reverse.
- Holm correction: this is your "whhhtis" note. Six or more pairwise tests give a high chance of at least one false positive. Holm adjusts the p-values to control that. It is always at least as powerful as Bonferroni, so there is no reason to prefer Bonferroni. I'd answer open point 2 with yes.
- Wilson intervals: these are proportion intervals that behave well with small n and with rates near 0 or 1, which you have (DeepSeek retrieved nothing).
- Fisher's exact (section 2): it compares deletes against does-not-delete/unrelated, and the counts are small, so a chi-square approximation would be unreliable. The cells are different erasure attempts, so they are not paired, which makes Fisher the right test.
- No tests in sections 3 and 4: the plan says the groups are uneven or empty. Counts est report there.



- how will we run it, whay are we using the statistical metods
- how do we wite findings, what infliences discussin


How to write the findings

Follow the order your memory notes set: frame, report, interpret.

- Lead with observed counts, then the test. For example: "Of 120 prompts recalled on all platforms, X were retrieved on ChatGPT and Y on Claude (Q = …, p = …)."
- Name the base of every percentage.
- Say "retrieved in a new conversation", never "erasure rate".
- Report can't tell as its own count.
- Describe sections 3 and 4 in prose and tables, with no p-values.
- Keep the claims modest. "The platform, not the prompt, decides" is a possible claim only if Q is significant and the discordant pairs show the platform effect is large.

What shapes the discussion

- Ceiling and floor effects. DeepSeek retrieved nothing and Claude erased everything, so some platforms have no variance. That is why a single model across platforms was dropped.
- Gemini and Copilot coverage. Missing recall limits the complete-case set and the generalisability.
- Different commitment types. Platforms promise different things, so a retrieval difference may reflect the platform's design, not a policy failure.
- Multiple testing. Say that Holm was applied.
- Retrieval is not erasure. Not retrieving the fact does not prove it was deleted. Say that explicitly.
- Descriptive sections. They are suggestive, not confirmatory, and the discussion should say so.
