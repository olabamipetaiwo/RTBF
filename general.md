Part One

-----
I’ve finished reviewing the paper and left comments in colored text (I didn’t go through the abstract, findings, or discussion).

I’m still learning as a PhD student, just like you, so I could be wrong. Please discuss my comments with the professors before applying any of them. That said, here are my thoughts on the paper.

I noticed a few problems.

First, the paper lacks a main focus. For example, you raise several points in the introduction and background:


“Can users effectively delete information they have shared with LLM agents?”
“Understanding what users expect from data deletion with how deployed LLM agents behave afterward is important because users may rely on deletion controls and confirmations without knowing whether their information remains retrievable.”
“Understanding whether and how data deletion works in these systems becomes critical to protecting users’ privacy rights.“But are these the core problems we want to explore?


I thought the main point of the paper was to understand what users expect from data deletion in LLM agents and how they act to delete their data (more or less, but the focus is on the user side). So I think you need a clear idea of the motivation and novelty of this work. Based on my understanding, the technical audit is not the main motivation or novelty here.

Second, there is a structural problem. Currently, Sections 3 and 4 each combine a method with its findings: Section 3 explains the user study procedure and its findings, and Section 4 explains the technical analysis methodology and its findings. If you look at this paper from our lab (https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11573461), you’ll see that it follows this structure: (3) User Study Methodology, (4) User Study Findings, and (5) PRODEGENs. I suggest discussing with the professors whether to restructure the paper in a similar way. Separating the findings from the methods helps reviewers quickly locate and read the findings.

Also, you could consider combining the background and related work sections. In user study papers, it is common to discuss prior work in the background because it helps define the research gap the paper addresses.

However, you should discuss this with Dr. Wang and Dr. Li first, since I’m not completely sure.

Third, the findings read as somewhat vague. I didn’t read the findings section closely so I may be wrong, but my overall impression is that there are a lot of numbers, figures, and details, but their connection to the main focus (which, as I mentioned, the motivation and novelty of this paper) is weak.

A word of advice is that the findings are the most important part of the paper, yet they are the part where co-authors can help the least. You need to come up with clear findings that connect to the main point of the paper across the introduction, background, and discussion. This means every sentence should be precise.

For example, the last sentence of Section 3.2.2 says: “These findings highlight a gap between users’ expectations of deletion and their ability to establish its outcome, motivating our subsequent post-deletion analysis (Section 4).” What exactly is the “gap” you’re mentioning in users’ expectations of deletion? What does “their ability to establish its outcome” means? And “how” did this motivate the post-deletion analysis?

In addition, if Section 4 only tests LLM responses, why did we code participants’ deletion requests (Table 4)? I thought they were supposed to be used to examine users’ expectations of deletion. In other words, I can’t clearly understand the purpose of the “Deletion-request wording” subsection.

I’m also worried about the “Deletion-request responses” subsection. First, categorizing LLM responses (complied, partial, deflected, refused, silently ignored, and other) seems somewhat arbitrary, especially since I believe we both used AI to code them. Second, I don’t understand why the tone of an LLM’s response matters when checking whether the data was actually deleted.

But again, I will read the findings section thoroughly later. For now, I’ve only skimmed it, so I may have misunderstood some parts.

Please feel free to reach out if you’d like to discuss anything. I hope this feedback is helpful.


---

2. Why "Deletion-request wording" is there (tech_analysis.tex:288).
3. Why the agent's responses matter (tech_analysis.tex:209).
4. The vague closing sentence of 3.2.2 (user_study.tex:336).
5. One central question in the Introduction: state that the novelty is the pairing of user expectations with tests of what agents actually do, using participants' own deletion requests.


----


Part 2

Taiwo SP is a top conference and reviewers today are very harsh. More than half of the submissions will be rejected in the first round. So you want the paper to be more than perfect in order to get to the second round. Not just overall or generally good, every detail has to be perfect.
[11:35 AM]If the paper is rejected, the next time we can submit it is at least half year later. You don’t want to waste the time
[11:36 AM]I will read it again today

-----

Recommendation: Major Revision. The question is timely and the writing is unusually careful about what it can claim, but the evidence does not yet support the headline.

Desk checks

- Page limit: the body runs to page 15. S&P has recently capped body text at 13 pages, so check this against the current CFP, because it is a desk-reject risk.
- Appendix B (Survey Questions) is empty. The instrument can't be reviewed.
- No vendor disclosure. The ethics appendix says no provider permission was obtained, and it mentions neither disclosure of the four cases that contradict documentation nor terms-of-service implications of Playwright automation.
- No artifact or data availability statement.



7. Measurement fit is weak. RMSEA is .099 pooled and up to .108 per scenario, and the method comparisons rest on groups of 29 and 30.



------


Yao li hot comment comment



### Thread A: started by Yao Li, 2026-11-10 11:28 PM (11 replies)

**Yao Li (11:28 PM):** @olabamipe taiwo why did you delete the test statistics? I remember the old tables have those
[image: 3.1.4 Data Analysis paragraph]

**olabamipe taiwo:** No, I didn't delete it

**Yao Li:** This table now only has mean. It has Scenario differences, method differences earlier
[image: TABLE 2, previously used / scenario-based / desired deletion methods, counts only]

**Yao Li:** in earlier conversation, I discussed with you adding the test statistics
[image: Slack, Wednesday Oct 21; Yao Li's sketch table: rows Single / Clear all / Specific / Ask to forget; columns Protection Pooled, LS, MS (3.63, 3.54, 3.73), "?scenario diff"; row "avg of LS / avg of MS / ?scenario diff"; bottom row "Statistical Difference": "between methods X2=..." and "between scenario X2=..."]

**olabamipe taiwo:** Yes, i will check my history

**olabamipe taiwo (12:34, edited):** I am 100% sure I made this table over the weekend

**Yao Li:** a lot of different tests are described in the methods. But in the findings the test results are missing.

**olabamipe taiwo:** I will go over the section again now and fill in the missing values

**Yao Li (also sent to the channel; repeated at 12:41 AM):** for these tests, you need to report test statistics (a number) and p
[image: 3.1.4 Data Analysis, with red circles around (1) "We used Wilcoxon signed-rank tests for willingness to delete, perceived privacy protection, effort, and benefit loss; the Stuart-Maxwell test for overall deletion-method choices; and McNemar tests for individual deletion methods, expected deletion outcomes, and verification strategies. We assessed scenario-order effects using binomial, Mann-Whitney, and Fisher's exact tests." and (2) "We used GEE contrasts for pairwise effort differences and chi-square or Fisher's exact tests for verification strategies within each scenario."]

**Yao Li:** either like this or put in the table
[image: "The more sensitive scenario increased willingness to delete but did not significantly change method choices. In LS and MS, respectively, 125 and 150 of 177 would probably or definitely delete the information (Wilcoxon signed-rank, p < .001, r = .55). Method-choice distributions did not differ significantly (Stuart-Maxwell, χ²(6) = 6.28, p = .39)."]

**Yao Li:** right now only wilcoxon and stuart-maxwell can be found

**Yao Li:** data analysis methods and findings need to be aligned, like "I did this test" in Method section, and then "This test shows ..." in Finding section.

### Channel message: Yao Li, 2026-11-10 11:30 PM

**Yao Li:** McNemar, Mann Whitney U, binomial, Fisher's exact test results are not reported anywhere in the paper,

### Thread B: started by Yao Li, 2026-11-10 11:33 PM (10 replies)

**Yao Li (11:33 PM):** I told you several times that you need to report the test statistics. If you think my comments are not important, then do whatever you want to do. I am not going to read your paper again.

**olabamipe taiwo:** I didn't remove the test statistics, infact i used the sample table you gave me last week to guide what I did. It must be an editorial error @Yao Li

**Yao Li:** i saw this table which is great. But it only shows GEE results. The results of other tests are missing.
[image: TABLE 10, Full GEE results (omnibus χ²(3), Holm p, odds ratios, β)]

**olabamipe taiwo:** It's likely an editorial error that occurre[d]...

**olabamipe taiwo (12:35, edited):** This is the guideline I followed when i was creating the table over the weekend @Yao Li
[image: Yao Li, Friday 3:51 PM: "just to explain why need these. For test like Wilcoxon, Stuart-Maxwell, it is a standard to report test statistics and p value to report significance, as well as the mean or median in each group/condition so that if signicant, readers know in which way it is significantly different. / For test like GEE, regresions, you need to report at least betas and p value, X^2. In this case expected outcomes are categorical so odds ratios instead of betas. protection, efforts, loss are numerical, so beta is good enough / my table includes almost everything reviewers normally need, so you can follow it" ; olabamipe taiwo, Friday 4:47 PM: "I will factor in everything you said and put the tables in the appendix"]

**Yao Li:** Table 10 only addresses
[quote: "For test like GEE, regresions, you need to report at least betas and p value, X^2. In this case expected outcomes are categorical so odds ratios instead of betas. protection, efforts, loss are numerical, so beta is good enough"]

**Yao Li:** you need a table or some other thing to address
[quote: "just to explain why need these. For test like Wilcoxon, Stuart-Maxwell, it is a standard to report test statistics and p value to report significance, as well as the mean or median in each group/condition so that if signicant, readers know in which way it is significantly different."]

**olabamipe taiwo:** Okay

**Yao Li:** see if you can retrieve the older version of Table 2

**olabamipe taiwo:** On it already

### Earlier thread: scale sources

**Yao Li:** I left a comment asking you to explain each of them and cite the source, did you address that?
[image: "For RQ2, participants rated their chosen method on five-point agreement scales for: perceived privacy protection (five items), effort (four items), and potential loss of personalized benefits (three items)." with the three scale names highlighted]


------

## Yao Li test-statistics fix: unit tasks (2026-11-11)

One edit per task, taken in order. Every number from a saved script; re-check against the paper's bases before use.

**0. Re-run the saved test scripts.** stats.md, mcnemar.md, verify.md, willingness.md are dated 2026-10-20. Re-run and confirm they match the paper's bases (177 / 176 / 317) before any number goes in.

**RQ1: practices**
1. Willingness: add W and the LS/MS means (3.98 -> 4.37) to the existing Wilcoxon sentence (her "mean or median in each group" rule).
2. Method choice, each method (McNemar): one sentence that no individual method shifted significantly between scenarios, with the statistic and p_Holm.
3. Desired methods LS vs MS: McNemar p values exist in user_study.md, but Methods does not name this test. Decide: report it and name it in Methods, or leave it out.

**RQ2: evaluations**
4. Restore old Table 2 (Yao Li's Oct 21 sketch): rows = four methods; columns = Pooled / LS / MS means for protection, effort, benefit loss; plus a "method difference" row (GEE chi2, p_Holm) and a "scenario difference" row (Wilcoxon W, p_Holm). Decide: next to fig_scales or replacing it.
5. Scenario difference in scales: one sentence; protection rose LS -> MS (p_Holm = .002); effort and benefit loss did not.
6. Method difference in scales: add chi2(3) to the existing effort/protection sentence, and report benefit loss (currently missing).
7. Effort pairwise contrasts (GEE): one sentence on which pairs differed.

**RQ2: expectations and verification**
8. Expectations across methods (GEE): add chi2(3) values next to the existing p_Holm.
9. Expectations LS vs MS (McNemar): one sentence, none significant.
10. Verification LS vs MS (McNemar): one sentence, none significant.
11. Verification across methods (chi-square / Fisher): one sentence on the significant options, tied to the existing 53.8% figure.

**Robustness**
12. Scenario order: one sentence with the binomial, Mann-Whitney U, and Fisher's exact results.

**Close-out**
13. Alignment pass: every test named in Methods has a "this test shows ..." result in Findings, and nothing extra in either.
14. tab:analysis-families: decide whether it gets a Result column or stays as the index once results are in the text.

Done: scale sources explained and cited (user_study.tex, appendix tab:scale-items, refs.bib xu2011personalization / xu2011information).



---


Methods without reporting it in Findings would break Yao Li's alignment rule.

1. Table caption: add at the end of the tab:method-scales caption
Here's the wording for each piece. I've also added a fourth, a Findings sentence: naming the test in Methods without reporting it in Findings would break Yao Li's alignment rule.

1. Table caption: add at the end of the tab:method-scales caption

▎ The $p_{\mathrm{Holm}}$ column compares LS and MS ratings within each method (Mann-Whitney, Holm-corrected across the four methods; $U$ values in Table~\ref{tab:analysis-families}); participants who chose the same method in both scenarios appear in both groups, which this test does not account for.

2. Methods: the "We used GEE contrasts…" sentence

Current:

▎ We used GEE contrasts for pairwise effort differences and chi-square or Fisher's exact tests for verification strategies within each scenario.

Proposed:

▎ We used GEE contrasts for pairwise effort differences, chi-square or Fisher's exact tests for verification strategies within each scenario, and Mann-Whitney tests~\cite{mann1947test} comparing LS and MS ratings within each method.

3. Findings: add after the "Across scenarios, perceived protection was higher in MS…" sentence

▎ Within each method, LS and MS ratings did not differ significantly on any scale (Mann-Whitney, all $p_{\mathrm{Holm}}\geq.54$; Table~\ref{tab:method-scales}).

4. Appendix tab:analysis-families: new row under "Scenario comparisons"

Analysis: Protection, effort, and benefit loss (within each method)
Test: Mann-Whitney
Sample: Responses choosing each of the four methods in LS and MS