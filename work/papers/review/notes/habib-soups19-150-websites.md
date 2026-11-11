# Habib, Zou, Jannu, Sridhar, Swoopes, Acquisti, Cranor, Sadeh, Schaub. An Empirical Analysis of Data Deletion and Opt-Out Choices on 150 Websites

SOUPS 2019 (Fifteenth Symposium on Usable Privacy and Security), USENIX, pp. 387-406. File: `2_audits/habib-soups19-150-websites.pdf` (USENIX proceedings copy). Read the abstract, introduction, regulatory background, related work on deletion evaluations, method, the results on data deletion, the discussion and conclusion. I skimmed the email and advertising opt-out results and did not read the appendix codebook in detail.

## Question
What email, targeted-advertising and data deletion choices do websites offer, and how do they present them (Section 1, two research questions)?

## Method
- Manual content analysis and heuristic evaluation of 150 English-language websites sampled from Alexa's global top 10,000 (as of 22 March 2018): 50 ranked 1 to 200, 50 ranked 201 to 5,000, 50 ranked above 5,000. Pornographic sites and sites needing SSN, card or non-email verification to create an account were excluded (Section 4.1).
- Analysed April to October 2018; websites analysed before the GDPR date of 25 May 2018 were reviewed again in October (Section 4).
- Two researchers coded 75 websites (50%) independently; agreement was Cohen's kappa 0.82; all disagreements were reconciled (Section 4).
- It is a review of what the pages offer. They did not submit deletion requests to find out whether data was deleted.

## Findings on data deletion
- 111 of 150 sites (74%) offered a data deletion mechanism, against 51% in the earlier GPEN sample (Section 5.1, Table 2).
- Of the sites offering deletion, 75 offered it only in the privacy policy, 3 only in account settings, 33 in several places. Only 27 policies linked directly to a deletion tool or form; 81 gave instructions to email a request (Section 5.1).
- Types (108 policies): 80 let visitors choose types of information to remove; 41 offered permanent account deletion; 13 allowed deactivation (Section 5.3).
- Timing was unclear: 90 of 108 gave no time frame for permanent deletion; only 4 said "immediately", 3 said 30 days, 2 said up to a year (Section 5.3). Overall, only 19% of sites with deletion choices stated a time frame (Section 6).
- Effort: choices needed on average three to five user actions before the final button; one deletion form needed 38 actions (Sections 5.4 and 6).
- The GDPR contributed: 37 sites updated their privacy policy around its effective date (Section 5.1).
- Conclusion: "presence of choices is not the same as enabling visitors to execute the choice" (Section 7).

## Limits the authors state
Only English-language sites from the top 10,000; US-based consumer perspective; exclusions of financial sites needing sensitive data; the analysis concerns usability, not legal compliance (Sections 3.1 and 4.4).

## How it differs from ours
- It audits the presentation of choices (documentation and interface), not whether a request had an effect. It is the website-era counterpart of the interface-level walkthrough of Li et al. (CHI 2026): both stop at what the user can see.
- Its finding that most sites say nothing about when deletion completes is the same gap we meet on AI agents, where documentation rarely says what a deletion covers.

## Use in our paper
- Cite for the base rates of how websites document deletion (74% offer it, 19% state timing, 27 of 111 link a tool) and for "presence of a choice is not the same as it working".
- Our own "documentation" category (help and privacy pages) parallels their policy analysis; we can say we extend the same kind of reading to LLM agents and add the test of whether the deletion worked.
