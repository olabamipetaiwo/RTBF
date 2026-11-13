The decision being applied: two outcomes only. Recall success means the fact was retrieved; recall failed means it was not. All 471 can't-tell cases, including the 41 with no usable recall result or a failed deletion, count as recall failed on the 865 base.

Target numbers

┌────────────┬────────────────┬───────────────┬────────────┐
│   Agent    │ Recall success │ Recall failed │ Test cases │
├────────────┼────────────────┼───────────────┼────────────┤
│ ChatGPT    │ 118            │ 33            │ 151        │
├────────────┼────────────────┼───────────────┼────────────┤
│ Claude     │ 3              │ 145           │ 148        │
├────────────┼────────────────┼───────────────┼────────────┤
│ Copilot    │ 5              │ 140           │ 145        │
├────────────┼────────────────┼───────────────┼────────────┤
│ DeepSeek   │ 0              │ 137           │ 137        │
├────────────┼────────────────┼───────────────┼────────────┤
│ Gemini     │ 5              │ 140           │ 145        │
├────────────┼────────────────┼───────────────┼────────────┤
│ Perplexity │ 31             │ 108           │ 139        │
├────────────┼────────────────┼───────────────┼────────────┤
│ Total      │ 162            │ 703           │ 865        │
└────────────┴────────────────┴───────────────┴────────────┘

Step 1: Change the rule in one place
- Edit the classification in RTBF-Analysis/src/audit_outcomes.py so a case with no retrieval is recall failed, with no storage condition.
- Update docs/audit_outcomes.md to state the new rule and the date and reason for the change.

Step 2: Regenerate and verify
- Re-run the outcomes module and the roughly 15 scripts that read its output (outcomes by agent, prompt features, responses by outcome, expectation gap, same-conversation, consistency with documentation).
- Check that the totals match the table above and that recall success is unchanged everywhere.
- Re-run src/number_sources.py so every paper number still traces to a script.

Step 3: Recompute the documentation-consistency verdicts
- These depend on the recall outcome, so the counts of cases consistent with or contradicting each agent's documentation will move. I will report the old and new counts before any wording changes.

Step 4: Paper edits, one section at a time, wording shown to you first
- Methods (tech_analysis.tex, recall outcome classification): two-outcome definition. The storage-evidence paragraph no longer defines an outcome, so it is removed or reduced.
- Results (tech_analysis.tex, about 22 places): the per-agent table, the response table, the expectation-versus-outcome table, the prompt-wording results, the same-conversation paragraph, and Findings 3 and 8. Every "determinable cases" phrase goes.
- Introduction (intro.tex:76): the sentence saying we separated cases where storage could not be established no longer holds.
- Limitations (discussion.tex:98-100): replace the can't-tell paragraph with a statement that recall failed means not retrieved, and that we did not confirm storage before deletion.
- Abstract: it is locked, so I will only check it against the new numbers and tell you if anything conflicts.

Step 5: Close-out
- Terms lint and paper/terms.txt (retire "can't tell" and "determinable").
- Consistency check across sections, then the academic-writing pass on each edited section.
- Update provisional.md for every number that changed.

Two things I need from you before starting
- A snapshot of the current state. The working tree has uncommitted paper changes. I recommend committing before Step 1 so the can't-tell version is recoverable; say if you want me to do it.
- The Limitations wording is the sentence a reviewer will test. With DeepSeek at 137 of 137 recall failed, the paper has to say plainly that recall failed does not show the fact was ever stored. I will draft it in Step 4, but it is the one piece that should go past Dr. Xue.

Order of work is Steps 1 to 3 first (code and numbers, no paper text), then Step 4 section by section.