# Professor comment revisions (2026-11-05)

Comment: (1) do not highlight inconclusive / can't tell cases, since this is the limitation of recall-based analysis; (2) do not highlight how data sensitivity changes user choices, since it is a valid but more subordinate question; (3) Figure 3 fonts: no all-bold, align sizes with main text, module names slightly larger than submodules.

This file records the ORIGINAL wording so any edit can be restored if he objects.

## Sensitivity (applied)

### RQ1, intro.tex line 34
Original:
> What deletion methods do users use, and how do their choices vary with data sensitivity?

Changed to:
> What deletion methods do users use and prefer, and how do they discover deletion controls?

Finding 1 (user_study.tex) supports this: methods used (76.8% single conversation), methods preferred (47-50% request prompt, 61-66% single conversation), discovery (most explored settings or guessed; 6 of 177 learned from the agent).

### Other sensitivity edits (all applied; approach is keep it but subordinate, not remove it)

- intro.tex line 49. Original: "...using scenarios with different levels of data sensitivity to investigate how deletion choices and expectations vary."
  Now: "...using scenarios with different levels of data sensitivity."
- intro.tex line 69. Original: "Regarding deletion practices, participants' willingness to delete increased with data sensitivity, while their deletion-method choices remained largely unchanged (RQ1)."
  Now: "Regarding deletion practices, participants primarily used conversation-level deletion methods and often discovered deletion controls on their own, and although they were more willing to delete in the more sensitive scenario, their method choices did not change significantly (RQ1)."
- user_study.tex sensitivity paragraph (~259-267). Original ended with an extra sentence, now removed: "Thus, although participants expressed greater willingness to delete information in the more sensitive scenario, we found no corresponding evidence of a change in their selected deletion methods." Paragraph position, order and numbers unchanged.
- user_study.tex Finding 1 box. Original order: use/discover sentence, then "The more sensitive scenario increased willingness to delete but did not significantly change deletion-method choices.", then the preferred-prompts sentence. Now the sensitivity sentence is last.

## Can't tell (all applied)

1. intro.tex line 73. Original:
> Observed outcomes varied more across agents than across deletion methods or request wording, while 54.5\% of test cases were classified as \emph{can't tell} because initial storage could not be established.

2. tech_analysis.tex RQ3 opening. Original:
> Post-deletion recall outcomes were often uncertain, and previously disclosed information remained retrievable in a substantial number of test cases.
> Of the 865 test cases, 394 (45.5\%) had determinable recall outcomes, including 162 (41.1\% of determinable cases) classified as \textit{recall success}.
> The remaining 471 test cases (54.5\%) were classified as \textit{can't tell} because we could not establish that the injected facts had initially been saved in the tested locations.
> Thus, recall success was observed in 18.7\% of all test cases, while more than half could not support a definitive recall outcome.

3. tech_analysis.tex deletion-request prompts sentence. Original:
> For deletion-request prompts, the most extensively tested method, 144 of 811 test cases resulted in recall success, while 454 were classified as \textit{can't tell}.

4. tech_analysis.tex Finding 3 box. Original:
> Previously disclosed information remained retrievable after deletion in a substantial number of test cases. However, 54.5\% of outcomes were inconclusive because initial storage could not be verified, highlighting the difficulty of determining deletion outcomes through external testing.

5. discussion.tex, "Observability of deletion outcomes": ADDED the sentence "In our data, 471 of 865 test cases (54.5\%) fell into this category, and for DeepSeek, Gemini, and Perplexity most cases could not be classified as recall success or recall failed." (nothing removed)

6a. tech_analysis.tex agent comparison. Original ending:
> ...were classified as \textit{can't tell}, limiting conclusions about their deletion effectiveness.

6b. tech_analysis.tex expectations vs outcomes. Original:
> Deletion-request prompts exhibited similar discrepancies, although uncertainty was substantial. ... Thus, observable recall contradicted the expectation that deletion would prevent subsequent retrieval in some cases, while more than half of these outcomes could not be determined.

7. conclusion.tex line 11. Original ending:
> ...further complicated by the limited reliability of user-facing verification signals and the uncertainty of many post-deletion outcomes.

## Figure 3
Not started. Original: figures/DIDR.png (raster, all text bold, about five font sizes). Keep a copy before replacing.
