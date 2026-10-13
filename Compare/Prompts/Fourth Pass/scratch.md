The main ways to use the coded categories in Results:

1. Frequency table — distribution of prompt types across the 138 prompts (what kinds of deletion language did users actually write?)
2. Cross-tab: prompt type × platform response — did certain prompt types get compliance vs. refusal vs. partial responses?
3. Cross-tab: prompt type × actual erasure outcome — did the type of prompt the user wrote predict whether data was actually removed at recall?

The most interesting finding would be if prompt wording doesn't matter — platforms respond the same regardless of how users phrase the request — or if it does (e.g., explicit "delete my data" gets compliance but vague "forget this" gets ignored).



------



Descriptive frequencies — what the 138 prompts look like as a corpus:
- Where users think their data lives (deletion_location: conversation vs. memory vs. backend vs. unspecified)
- What they ask to delete (what: specific PII vs. general PII vs. unspecified)
- How they ask (mood, tone, verb: imperative vs. polite vs. technical vs. lay)
- Whether they give a reason (justification) or make additional requests (accompanying_request)

Cross-tabs against platform outcomes — the interesting analysis:
- Does deletion_location predict erasure success? (e.g., users who say "from this conversation" vs. "from your memory" — does the match/mismatch with where data actually lives affect whether it gets deleted?)
- Does verb type (technical vs. lay vs. mixed) affect compliance rates?
- Do prompts with justification get better compliance than those without?

The core finding you're testing is whether how users phrase their deletion request matters for what actually happens — or whether platform behavior is independent of prompt characteristics.

Want me to sketch out the specific tables once the master sheet is ready?