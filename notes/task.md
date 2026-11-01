# TASKS

**How we work:** one item at a time. For each item I explain the problem and show the data, propose a fix, and change the paper only after you say OK. When an item is done, move it to the "Completed" section at the end of this file. Every number in the paper must come from a saved script, and every percentage must say what it is a percentage of (177 participants, 354 observations, or 317 observations).

**Writing rule for the whole paper (guide the reader):**
- Every section opens with a one-sentence roadmap and its takeaway.
- Every paragraph opens with its claim, in a plain sentence. Bold lead-ins that only name a topic ("Sample scope.", "Design.") are removed.
- A bold lead-in is allowed only when it is itself a claim, with at most about 5 per section. Parallel detail goes in a table.
- Each part closes with a "so" sentence that tells the reader what to take away and leads into the next part.
- No heading for a part under about 100 words.

**Order:** items near the top can be done now. Items further down wait on something. Each item says what it waits on.



---1. 

## Running in the background

**E1. Finish the recall runs for Gemini and Copilot.** After each batch, re-run these five scripts in this order (from the `RTBF-Analysis` folder) and tell me which numbers changed: `src.audit_outcomes`, `src.cross_platform_assumptions`, `src.cross_platform`, `src.outcome_by_prompt_features`, `src.expectation_gap`.

---

## A. Can be done now

**11. Decide the main result of the paper and the order of the sections.** (PR2.) The professor and the peer review both say the point of the paper is vague and that results should come first. We need one sentence that states the main result. The sections below depend on it.
- This is for you and the professor to decide. I will not ask you to choose during a session.
- Reports with the evidence: `expectation_gap`, `method_selection`, `verify`, `user_study`, `cross_platform` and `outcome_by_prompt_features` (in `RTBF-Analysis/outputs/results`).
- A possible framing to show the professor: what users expect (survey), what happens (behavioral audit), and whether the checks users rely on show it.
- Best decided after items 1 to 10 and after the recall runs end.
- Marked as tentative with `TBWL` in `paper.tex` until this is decided: the Results roadmap sentence, the Introduction roadmap sentence, the Discussion opening (What the Results Mean), and, once drafted, the Abstract and Conclusion. Item 12 (Methods) also waits on this.

**12. Reorganise the Methods section.** (PR8.) Waits on item 11. The professor says it mixes methods with results, has no overview, and uses jargon. Peer review says it has too many subtitles and asks to reorganise sections 3.1 and 3.3. Each part should go: goal, then the design and why, then what we did. Items 6 to 10 supply the content.
- The peer review also says there are too many subheadings. Rule to apply across the paper: no heading for a part under about 100 words. In User Study, Protection, Benefit Loss and Effort are already merged into one subsection. Methods (17 bold lead-ins under 3 subsections) and Background (6 lead-ins) still need it.

**27. Decide whether to present the 12 file-upload test cases.** Decision for later: present them or leave them out of the results slides and the paper's results.
- What exists: 12 test cases (delete the conversation, or the most extensive deletion, on each of six platforms). Results are in `RTBF-Analysis/outputs/results/acknowledgment_vs_recall.md`, section 4. In 11 the fact did not come back (recall failed) and 1 was not run (Perplexity, most extensive deletion).
- Checked their own way, listed one by one: they do not go through the can't-tell rule. Every deletion was a button, so there is no reply to code.
- The meeting slides mention them only in the Scope line, as analysed separately.
- If we present them, the analysis still has to be written: where the fact went at upload (conversation only, never extracted, or extracted after a forced read) against the new-conversation result.









## D. Last

**25. Final submission checks.** (C7.)
- Run `python3 make_submission.py --number <HotCRP number>` in `RTBF-Analysis/paper`. Its only failure should be the three `TBWL` placeholders from item 24.
- LaTeX is not installed on this machine, so the paper has not been compiled since many edits. Compile `paper_submission.tex` on Overleaf and check that the two appendix tables fit the page.
- Leave the Ethics Considerations section as it is, apart from the "technical audit" wording; the professor wrote "this part looks good".
- Upload only `paper_submission.tex`.
- Check that the Ethics text matches the HotCRP Ethics field.
- Check that the account records (`config.py`, `accounts.md`, the Email column of the workbook) match the account-isolation sentence in Methods.
- Check that the quotes from the OpenAI and Perplexity help pages still match the live pages (appendix `sec:policy-sources`).
- Re-run `python -m src.number_sources` after any number changes and confirm its exceptions table is empty.

**26. Read the whole paper as Dr Wang will.** (PR19, note 3.) Before the paper goes back to Dr Wang for review, read it start to finish and check that it is clear to someone who has not followed our work: no unexplained words, each part says why before what, and every finding is stated plainly.

---

## E. Professor's comments already handled

- **"This part looks good"** (Ethics Considerations). Nothing to change. The only edit there was the "behavioral audit" wording.
- **"This is a user-oriented analysis, not a full technical analysis"** (start of the audit section). The paper no longer calls it a "technical audit". It now says "behavioral audit" everywhere except inside the professor's own comments.

---
- **"When ChatGPT does not delete data on deleting a conversation, e.g. an API that archives with archive=true"** (start of the audit results). Not added to the paper. See item 4 under Completed.

---
- **"What are the key takeaways of each section here?"** (start of the User Study section). Each part now opens with one plain takeaway sentence.

---
- **"It is not explicit what is the design of survey questions, and what are the major types of survey questions asked here"** (start of the survey Methods). The survey Methods now list the seven kinds of questions.

---

## Completed

**1. Fix the wording.** (PR3.) Done in `paper.tex`. Terms now used everywhere:
- "behavioral audit" (not "technical audit").
- "recall success", "recall failed" and "inconclusive" for the outcome of a recall check.
- "test case" (not "cell"), with the sentence that defines it.
- "topic" and "token", defined where the test setup is first described, with one sentence on how we made them.
- "disclosure", used only in the audit and defined at first use. The survey says "mentioned" or "shared".
- "recall check" (not "probe").
- "deletion" (not "erasure") for requests, methods, actions and controls. "Erasure" stays only in the GDPR sentences. "Participants' own deletion requests" replaces "NL-forget-prompt".
- "battery" and "condition test" are gone. "Negative / positive controls" is explained in plain words.
- "memory feature" and "saved memory" are defined once in the Introduction.
- Not done: the scripts and reports still use their own outcome words. We set them aside because reviewers read only the paper.

**2. Check the survey numbers in `notes/findings.md`.** (D9.) Done.
- 23.7% (42 of 177 participants noticed a chatbot bring up deleted information) is correct. `src/user_study.py` now prints the combined figure, and the output is saved in `outputs/results/user_study.md`.
- 53.8% was wrongly described as "survey answers". It is the share of the 39 observations where participants chose ask-to-forget. Across all 354 observations, 20.6% would check in the same chat and 21.8% in a new chat. `findings.md` is corrected in three places. The paper's table row was already right.

**3. Give me your wording for five unclear notes in `review.md`.** (PR19.) Done. Your answers:
- "The effective way to communicate with the users" means how our paper communicates its findings to readers. This is now part of items 5 and 23.
- "Section 3.3" labels the notes about the audit methods section. Items 8 and 12 already cover them.
- "The draft need to be clear for Dr Wang to review again" is now item 26.
- "Battery" is closed. It is already replaced in the paper.
- "In the research: goal, then design (justification and consideration), then what we did" is already covered by item 12.

**4. Check one claim in the transcripts.** (PR16a.) Closed without a check, and no paper text is added.
- The professor suggested that ChatGPT's "delete conversation" may only archive the conversation.
- About six months ago, before our experiments, ChatGPT hid a deleted chat with a request that set a flag. By the time we ran the audit it used a real delete request. So the saved transcripts say nothing about the flag behavior.
- We cannot prove how ChatGPT handles a deleted chat on its servers, so the archive point stays out of the paper. The Methods already say that our observations cannot show what happens in backend storage.

**5. User Study results: say the main takeaway of each part.** (PR15.) Done in `paper.tex`.
- Each part of the User Study section (usage, measurement model, protection, benefit loss, effort, expectations) now opens with one plain takeaway sentence. Every percentage in the new sentences names its base (354 observations or 177 participants).
- To keep the parts short I cut sentences that only repeated a takeaway: the "data sensitivity did not change the method" clause, the "similar trade-off" closing sentence, and the claim that method matters less to protection than data sensitivity (the data do not support it).
- Still open: the Expectations part is the longest. Shortening its five paragraphs is part of the Results rewrite (items 11 and 12).

**6. Explain the survey design.** (PR9.) Done in `paper.tex`.
- The survey Methods now open with why we ran the survey, then the seven kinds of questions (screening and consent, background, the two scenarios, deletion experience, privacy knowledge, attitudes and AI ability, demographics), then what we did.
- The verification question asks what participants have done ("Have you ever verified…"), so the paper and `findings.md` now say participants "had checked", not "would check".
- Still open: the professor's "why before what" comment applies to the other Methods parts too (items 7 to 10 and 12).

**7. Explain why we chose these six chatbots.** (PR13.) Done in `paper.tex`.
- The Behavioral Audit Methods now open with one paragraph: the six are the major general-purpose consumer chatbots available in the United States, our survey participants used each one (36.2% to 99.4% of 177), and they differ in where they keep a fact, their deletion controls and their developers. It says the results describe these designs and not every chatbot.
- No outside usage figures or citations are used. Statcounter and Pew are not citable, and Pew shows Meta AI and Grok ahead of Claude, so we do not claim the six are "the most used".
- Li et al. (CHI 2026, already cited) studied a different six (Character.ai, ChatGPT, Claude, Gemini, Meta AI, Pi) and required US-based developers, so DeepSeek would not fit their rule. We do not use their set as a precedent.

**8. Justify our other choices.** (PR12.) Done in `paper.tex`. Two new paragraphs open the audit's Design part, with the reasons before the method:
- The injection and deletion methods match how people use and delete chatbot data. We walked through each platform's interface and listed every control (similar to the walkthrough in Li et al.). The three ways of giving information each reach a different place a platform may keep it. The deletion methods match those our survey participants know, and each platform also gets one maximal combination of all its controls.
- Left out: settings that only switch a feature off, account deletion (nothing left to test), and requests filed with the company (handled outside the chatbot).
- File uploads are a separate group of 12 test cases because a platform can read a document, save it, do both or neither.
- Still open: the recall checks (item 9). The professor's comment on justifying injection, deletion and recall methods is only fully handled when item 9 is done.

**9. Justify the three recall checks, especially R2.** (PR11.) Done in `paper.tex`. A paragraph before the recall-check details gives each check's reason: R1 asks directly, R3 never names the topic and looks for leaks in ordinary tasks, R2 reads the memory page and does not depend on the chatbot's answer. It names the platforms where R2 does not apply (DeepSeek, Perplexity, Copilot). Checked in `tester/`: all three are really carried out, in the stated order. Counts are in `src/recall_check_value.py`: R1 found the token in all 23 main-grid recall successes and in 123 of 139 in the forget group, and R2 settled one case alone. No published study justifies the checks (only preprints), so the paper argues from what each check can see. Also added Chen et al. (CHI 2026) to Background in the LLM memory paragraph, as evidence that users doubt deletion works and cannot check.

**10. Explain how we coded the deletion requests and analysed them.** (PR14.) Done in `paper.tex`. The coding was already described (two coders, practice round, shared codebook, seven dimensions, agreement in Table 2). What was missing was the analysis, so an "Audit analysis" paragraph now closes the Behavioral Audit section: each test case reduced to "did the fact come back in a new conversation", reported as retrieval and not a deletion rate; then the three analyses (platform comparison with each request as its own control, deletion scope against documented commitment, and request wording described only). The paragraph matches the three scripts (Holm correction, Wilson intervals, no tests on wording). The method text stays fixed after the recall runs end; only numbers change.

**13. Say what the behavioral audit is and is not.** (PR10.) Done in `paper.tex`. Three changes in the Behavioral Audit subsection:
- A goal paragraph first: the audit shows what a user can observe after asking a chatbot to delete something, and whether that matches the platform's documentation. It is a user-side test, not a technical analysis, so it cannot show whether data was removed from backend storage.
- The name stays "behavioral audit" (the professor gave no other term); the goal paragraph defines it.
- A shorter Playwright sentence, plus what automation gave us: identical test cases, scheduled 48-hour and 31-day steps, a saved reply and screenshot at every step, manual logins with saved sessions, and pacing within free-tier limits.
- Decision: we do not claim the automation as a technical contribution (the paper's contribution is the design and findings).
- Still open elsewhere: the professor's comment on a term for "all outcomes are externally observable" sits in Limitations (item 22) and Discussion (item 21).

**14. Say which deletion methods users have.** (PR7.) Done in `paper.tex`. Placed in Background, after the "Auditing LLM platform controls" paragraph. One paragraph names the five main ways to delete (ask the chatbot to forget, delete one conversation, clear all history, delete one saved memory, clear all saved memories), the platform-specific extras (ChatGPT custom instructions, Copilot privacy dashboard), and account deletion and filing a request. It says the list covers what a user can do from a consumer account, not what a company does internally. Table `tab:methods` shows which platforms have each method; built from the audit's test cases and the project's records. Your answers: Copilot's conversation control deletes one conversation (so no clear-all), and Perplexity's memory controls show a dash because they need a paid plan. If item 12 moves where this knowledge belongs, the paragraph and table can move with it.

**15. Rewrite Background and Related Work.** (PR6.) Done in `paper.tex`, with one part left open. It is now two sections with no subsections. Background has the right to erasure, the deletion methods (item 14) and a new paragraph introducing how we report outcomes (acknowledgment, recall outcome, policy consistency). Related Work has three points, each opening with its claim: deletion rights are hard to exercise and check; users hold incomplete models of deletion (including Chen et al.); platform-control work describes the controls but does not test them, and unlearning work shows a control may establish less than it appears to. The old bold lead-ins and "Positioning" paragraph are gone. Open: the professor's "missing literature review" is not extended; no published study justifying the recall checks was found (see item 9), so no new references were added.
- Extended 2026-10-28: Related Work now cites Rupp et al. (PoPETs 2022, closest audit precedent), Liu et al. (USENIX Security 2022) and Kwesi et al. (USENIX Security 2026), read from the PDFs, and states the gap; Background adds the California right to delete and a paragraph on where a fact can live in a chatbot. New bib keys: `rupp2022leave`, `liu2022zombie`, `kwesi2026impact`, `ccpa2018`. Open: the CCPA sentence was written from Liu et al.'s citation of §1798.105, not checked against the statute.

**16. Make an overview figure.** (PR4.) Done. Figure 1 is `figures/overview.png`, placed before Methodology with the caption "Study overview: a survey of what users expect and an audit of what six chatbots do after a deletion request, compared in the last step." It shows the survey, the audit (disclose a topic, delete it 48 hours later, recall check 31 days later) and the comparison, with arrows from the survey, the audit and the platform documentation into the comparison. The professor's comment stays in the caption.

**17. Add the wording and Gemini results to the Results.** (D6.) Draft placed in `paper.tex` under Behavioral Audit Results (two paragraphs, before the `TBWL`); the section is restructured under items 11 and 20.
- Gemini permission cards: 8 of 133 deletion requests (6.0%), 7 for Google Keep and 1 for Gmail, nothing deleted. The earlier "7 of 133" counted Keep only. New script `src/gemini_permission_cards.py`.
- Wording: ChatGPT shows no wording pattern, Claude 0 of 131, Perplexity differs only on what is asked (specific 16 of 109, unspecified 10 of 17). Gemini and DeepSeek left out (all can't tell).
- Open: add Copilot's count to the wording paragraph once its recall finishes (rides on E1). Survey versus audit and the same-chat check go in with items 18 and 19.

**18. Build the two comparison tables.** (D8.) Draft placed in `paper.tex` under Behavioral Audit Results as `tab:gap-method` (Table A) and `tab:gap-platform` (Table B), generated by `src/expectation_gap.py` into `outputs/tables/expectation_gap_method.tex` and `expectation_gap_platform.tex`. Your decisions: two survey columns (never mentioned again, permanently deleted) with `tab:contingency` linked for the rest; the two ask-to-forget sets are one row; build now, refresh later.
- Feedback users want (68% popup, 41% breakdown, 8% none) was asked once per participant, so it is not a column; say it in the text beside the platform-reply column.
- Open: after recall ends, re-run `src.expectation_gap` and paste the two `.tex` files over the table bodies; the captions say "as it stands" and must lose that wording.

**19. Compare the survey with the behavioral audit.** (D7.) Draft placed in `paper.tex` under Behavioral Audit Results after `tab:gap-platform` (four short paragraphs). Only expectation and verification are compared with the audit; protection, effort and benefit loss are left out with a one-sentence reason (they record feeling, which the audit cannot observe). Prose points to the tables and does not repeat their counts; the only audit counts in it are ChatGPT's same-chat check (129 said gone, 104 came back, of 135, from `src/cross_platform.py`).
- Open: reconcile `findings.md`'s "91 of 272 (33%)" same-chat figure with `cross_platform` (274 of 672) before it is used anywhere. Refresh the wording after recall ends (Perplexity has many can't-tell cases).

**20. Write the Behavioral Audit Results.** (PR16.) Drafted in `paper.tex` as a roadmap sentence and four subsections: What Chatbots Said and Did (`tab:gap-method`), Platforms Differ and Wording Hardly Matters (`tab:retrieval`, `tab:gap-platform`), Documentation Against Behavior (`tab:policy-verdicts`), Survey Against Audit. Prose carries no counts that a table holds; platform comparisons use the retrieval rule. Tables come from `src/expectation_gap.py` and `src/cross_platform.py` (`outputs/tables/*.tex`).
- Also done 2026-10-28: 15 Copilot replies coded (13 partial, 2 other) and written to the workbook; AC1 not recomputed. 7 Perplexity replies are still uncoded.
- Open: the professor's two questions on the placeholder are still in the paper (`\xw`, keep verbatim); the `TBWL` after the section and the old TODO comment block are still there, to remove once you accept the section. After recall ends: re-run `src.expectation_gap` and `src.cross_platform`, paste the `.tex` bodies, drop "as it stands" from the captions, refresh Copilot's figures.

**21. Rewrite the Discussion.** (PR17.) Drafted in `paper.tex` as three subsections: What the Results Mean, What We Recommend, What a Technical Audit Would Add. The two outdated forward pointers are gone; the professor's `\xw` comments stay (two of them sit in Limitations). Wording of the last part is to be reviewed later (user, 2026-10-28).
- Open: the main-result sentence from item 11 is a `TBWL` at the top of What the Results Mean; refresh "almost always matched" after Copilot recall ends; decide whether "it found what a look at stored data would not" should be softened.

**22. Rewrite the Limitations.** (PR18.) Done in `paper.tex`: two paragraphs, no headings. The first opens with the value of the study and then states who the survey describes; the second names the audit a "black-box behavioral audit" (your decision, the term the introduction already uses) and says it reports what a user can observe, not what a platform stores. It answers the professor's account-reuse question with the saved checks (`cross_platform_assumptions`: requests sharing an account's memory barely changed the retrieval rates and showed no order effect). The professor's `\xw` comments are untouched. The 7 uncoded Perplexity replies are not mentioned (your decision).
- Open: re-check the account-reuse sentence after the recall runs end (the sibling-rule and order checks re-run with `src.cross_platform_assumptions`).

**23. Rewrite the Introduction.** (PR5.) Drafted in `paper.tex` (as it stands): a hook from our own survey (23.7% of 177 noticed a chatbot bring up information they believed deleted), the GDPR and prior-work paragraphs trimmed, a short "what we did" paragraph that cites Figure 1 (`fig:testing-pipeline`), (the Key findings box was removed 2026-10-28: the user does not want findings in the Introduction; Rupp et al. do the same, Kwesi et al. and Liu et al. summarise findings in prose, none uses a box), the five RQs in one sentence, and a roadmap. The professor's two `\xw` comments at the top stay.
- Open: the professor's review note asked for results up front, so it may return; the professor's comment on Figure 1's caption ("cannot serve as an overview") is still open and now matters more because the Introduction cites it.

**24. Fill in the Abstract and Conclusion.** (D1.) Both drafted and placed in `paper.tex` on 2026-10-28, each with a bold `{TBWL}` where item 11's main-result sentence goes. The Abstract carries the findings (the Introduction has no findings box): 59.0% of 354 observations expected permanent deletion, 44.6% did not know how to verify, the platform pattern, and Gemini's app-permission requests (6.0% of 133 requests; 7 Google Keep, 1 Gmail). The Conclusion has two paragraphs and no statistics.
- Open: both wait on item 11; "three of the six platforms" and "half the platforms" depend on Copilot's recall finishing.
