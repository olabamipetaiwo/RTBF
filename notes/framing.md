Where the paper sits right now: It's a measurement study with two parts — a survey (what users expect) and a technical audit (what platforms actually do). The gap between the two is the finding. There's no tool, no defense, no attack. The Discussion has "design implications" but they're observations, not contributions.

What S&P wants: The PINFINDER meta-review spells it out — they accepted it because it (1) introduced a framework (PINFINDER) as a tool, (2) used context-aware analysis instead of just pattern matching, (3) tested at scale (4,683 apps). The three scientific contributions they credited: independent confirmation, new tool, step forward.

The problem for this paper at S&P: Measurement-only papers do get accepted there, but they need either a very large scale, a novel methodology, or a solution component. This paper has 6 platforms and 177 survey respondents — that's thorough but not massive. The methodology (automated browser-based testing) is solid but not novel in the web-measurement sense. And there's no solution.

Three ways to think about framing it:

1. Compliance verification tool — Reframe the tester infrastructure as a reusable tool. "We built an automated framework that injects, erases, and recalls data across LLM platforms to test RTBF compliance." That gives you a tool contribution like PINFINDER. The threat model is: platforms claim compliance, users rely on it, the tool shows it's broken. The weakness: the tester is tied to 6 specific platforms, not generalizable in the way PINFINDER's SDK analysis is.
2. Threat model: the expectation gap as a privacy threat — The survey shows users expect permanent deletion (59%), the audit shows platforms don't deliver it. Frame this as: users make downstream privacy decisions (what to share, whether to reuse the platform) based on a false belief that deletion works. The threat is informed consent is undermined. The "solution" becomes a transparency/verification standard — what a platform would need to do to make deletion verifiable. This is more of a policy paper, which S&P does accept but is harder to land.
3. Measurement + disclosure — Treat the audit findings as vulnerability disclosures. "We tested 6 platforms' deletion controls and found X% fail to remove data as documented." This is the web-measurement tradition at S&P (like the Habib et al. dark patterns paper, or the GDPR compliance audits). The scale concern is real — 6 platforms is comprehensive for LLMs but small compared to web-scale measurement papers that test thousands of sites.

The real question: Does the paper need a solution component, or can it land as pure measurement? If it needs a solution, what is it? The tester is the most natural candidate, but it would need to be packaged as something other researchers can run (open-source, extensible, not just "our scripts"). If it's pure measurement, the framing needs to emphasize that this is the first systematic test of LLM deletion compliance, which it is.

What's your read — is Yao Li pushing toward building a solution, or toward framing what you already have differently?




-----

The problems the paper actually proves:

1. Undefined deletion semantics — "Delete" means different things across platforms and even across mechanisms on the same platform. Deleting a conversation ≠ deleting a memory ≠ asking to forget. Users don't know which surfaces are covered.
2. No verification — 44.6% of users don't know how to check if deletion worked. Platforms provide no feedback mechanism. 29.4% receive nothing at all after deleting.
3. Cross-surface persistence — Data lives on multiple surfaces (conversation, memory, training). Deleting from one doesn't propagate to others. The audit catches this directly: you erase via one mechanism, recall finds the data on a different surface.
4. NL-forget is untrustworthy — Platforms respond inconsistently. Some refuse, some claim compliance but do nothing (Gemini's "I don't store anything"), some partially comply. Users can't distinguish real compliance from lip service.
5. The expectation-behavior mismatch is systematic — 59% expect permanent deletion, the audit shows most mechanisms don't deliver it. This isn't a one-off bug; it's a structural gap between what the UI implies and what the backend does.

---

Now, solution space — what could actually fix each:

Solution A: Canary-based verification protocol (the paper's methodology, generalized)

The paper already built this: inject a unique semantic fact, delete it through the platform's controls, probe whether the platform still knows it across multiple recall channels (new conversation, same conversation, settings page). That's a black-box deletion verification method. Nternal database inspection. It works on any platform a user can interact with.

This is different from prior canary work (Carlini et al. tested random-string memorizhis uses semantically meaningful facts that mimic real user data and tests the fulldeletion lifecycle, not just training-data extraction.

The contribution: a practical, repeatable protocol that regulators, researchers, or e run to test whether deletion controls actually work. The paper's 85-cell × 3-probedataset proves it produces actionable results at scale.

Solution B: Deletion scope declaration (a transparency standard)

The audit produces a matrix: platform × mechanism × surface → does deletion cover it? That matrix is currently unknown to users. The solution: require platforms to declare what each deletion control
covers. "Deleting this conversation removes it from your conversation history. It doemory entries, and it does NOT affect training data."

The paper's data provides the empirical basis: here's what each mechanism actually does vs. what users assume, here's the gap, here's what a truthful declaration would say.

Solution C: Deletion receipt / feedback specification

41.2% of users want a breakdown of what was deleted and what may remain. The solution: after any deletion action, the platform returns a structured report — what surfaces were affected, what was
removed, what persists and why. The paper's survey data provides user demand evidencedes the content such a receipt would need to convey.

Solution D: The testing framework as an open-source tool

Package the automated inject → erase → recall pipeline as a reusable compliance testi can extend it to new platforms. Regulators can run it. This is the PINFINDER analog —"we built a tool that enables future science."

---

My read on which combination is strongest for S&P:                                                                                                                                                   
The canary verification protocol (A) is the most novel technical contribution. It's a new method, it works on black boxes, and the paper proves it produces results. Combined with the testing       framework (D) as the implementation, that gives you both a methodology and a tool. Th) and deletion receipt (C) are the "what platforms should do differently"recommendations that flow naturally from the findings.                                                                                                                                               
The threat model writes itself: users trust deletion controls, platforms don't deliver, and there's currently no way to verify. The canary protocol is the verification mechanism that doesn't exist today.

The weakest part is scale — 6 platforms. But the counterargument is that these 6 plat major LLM chatbot market, and the methodology is extensible. PINFINDER tested 4,683apps but the SDK ecosystem has millions; this paper tests 6 platforms but the LLM chatbot ecosystem currently has ~6 major ones.

What's your reaction — does the canary protocol as the central contribution feel right, or is Yao Li thinking about something else entirely?


--

hether it's achievable in the submission timeline is nto a bottleneck, we will achivev e it


The question is a concenerete additional solution work (packaging the tester as a reusable tool, formalizing the canary protocol, writing the threat model) is worth the delta in venue rank.

----

Strongest fit in current form: SOUPS. The paper is structurally a SOUPS paper. User study measuring deletion expectations + technical audit measuring platform behavior + the gap between them. Both Habib et al. (2019) and Ramokapane et al. (2017), which you already cite, were published at SOUPS. It's co-located with USENIX Security, well-respected in usable privacy, and wouldn't require restructuring the paper. The methodology is strong (CFA-validated scales, AC1 inter-rater reliability, canary-based audit) and the sample size (177 within-subjects, 6 platforms) is appropriate for the venue.

Also strong: CHI. Yao Li's own paper (Li et al. 2026) is at CHI. The mental model angle (users think "delete" means permanent removal, platforms disagree) is classic HCI. CHI would want you to lean harder into the design implications, which the Discussion already has. The technical audit becomes supporting evidence rather than the core contribution.

Good fit: FAccT. The paper is fundamentally about platform accountability: platforms promise deletion, users rely on that promise, the audit shows it's broken. FAccT takes mixed-methods (survey + technical measurement) and doesn't require a tool.

Possible: PETS. Privacy measurement methodology. The canary approach as a technique for measuring deletion compliance on black-box systems is novel enough for PETS.

What S&P / CCS / USENIX Security would say in its current form: "Interesting measurement, insufficient technical contribution." These venues want either a new attack, a new defense, a new tool, or measurement at a scale that reveals something structurally new. 6 platforms is comprehensive for the LLM space but it's not 4,683 apps. The methodology is sound but browser-based testing isn't methodologically novel. Without a solution component (the canary verification protocol, the testing framework as a reusable tool, or a transparency standard with teeth), the paper would likely get desk-rejected or get R3/R4 reviews at a top-4 security venue.

The real tradeoff: SOUPS or CHI accepts the paper roughly as-is and gets it published. S&P requires building out the solution component, which is more work but higher prestige. The question for you and Yao Li is whether the additional solution work (packaging the tester as a reusable tool, formalizing the canary protocol, writing the threat model) is worth the delta in venue rank, and whether it's achievable in the submission timeline.