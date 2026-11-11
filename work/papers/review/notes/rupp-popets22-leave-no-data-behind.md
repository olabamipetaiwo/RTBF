# Rupp, Syrmoudis, Grossklags. Leave No Data Behind: Empirical Insights into Data Erasure from Online Services

Proceedings on Privacy Enhancing Technologies (PoPETs) 2022(3), pp. 437-455, DOI 10.56553/popets-2022-0080. File: `2_audits/rupp-popets22-leave-no-data-behind.pdf` (open-access PoPETs copy). Read the abstract, introduction, background, methodology (all six steps and ethics), Sections 4 and 5 in part (results, analysis, further insights), discussion and conclusion. I skimmed the per-service tables and the DPO questionnaire detail (Section 5) and did not read the appendices.

## Question
How do online services handle erasure requests in practice, and what data remains afterwards (Section 1, five questions)?

## Method (Section 3)
- 90 services chosen from the SimilarWeb ranking (top 50 worldwide and top 50 in Germany, with exclusions for no accounts, no EU operation, languages other than English or German, adult sites, and duplicate services of one company, plus extra services so every category is covered). Accounts created December 2019 under one fictional person, with five email accounts.
- Data feeding: fill in profile fields, create public posts and private messages (using a second account), and use each site for six weeks (about 60 minutes of active use each) so that the account looked real.
- Manual deletion of individual data within the account, re-entering any data deleted so the later request starts from a full account (Section 3.3).
- Complete deletion in March 2020: the in-account button where one existed, otherwise a formal Art. 17 request by email or form. Outcome per item classed as deleted, anonymized or not deleted (Section 3.4).
- More than six months later (November 2020), an Art. 15 right-of-access request to every service to see what data remained (Section 3.5). Follow-up emails to services that still held data, and a nine-question questionnaire to all 90 Data Protection Officers (Section 3.6).
- Ethics: the study followed earlier GDPR request studies; 29 services required real names, so terms of service were violated without harm; the authors state they used a "minor deception" by not disclosing the reason for requests (Section 3.7).

## Findings
- In-account deletion: 76 of the 83 services where data could be entered (92%) let users delete at least one category; private messages could rarely be deleted (11%), public posts or comments in 54% of cases (Section 4.1, Table 1).
- 62 services (69%) offered a deletion button; the other 28 were contacted by email or form; mean response time to email requests 4.4 days, median 3 days; 3 did not respond at all, and 2 of those deleted silently; 3 responded but did not process the request; 37 services (41%) required an additional step such as an email confirmation (Section 4.2).
- 24 of 90 services (27%) did not complete erasure so that all personal data was deleted or anonymized ("non-compliant") (Section 4.5, Abstract).
- Compliance by method: 82% of email requests were completed compliantly against 69% of button requests; 19 of 62 button requests left data, while only 3 of the 20 services that state a button counts as an Art. 17 request were non-compliant (Sections 4.5 and 5).
- Services gave almost no information on the scope of erasure, or on whether requests are forwarded to third parties (Section 6.1). Newsletter data was often treated as separate from account data.
- The authors state the observability problem: the higher compliance rate "might also stem from the nature of data erasure, i.e., the unobservability of the actual erasure, as a user cannot verify that data really has been deleted from the internal systems of a service" (Section 6.1).

## Limits the authors state
56 of 90 services are German and 63 rank better than 3000 in SimilarWeb, so results should not be generalized; each service received one request, by button or by formal route, so the comparison of the two routes may be biased; third-party data is out of scope (Section 7). Public-visibility and access-request checks can only show remaining data, not prove its absence.

## How it differs from ours
- Closest method to ours on the web side: create accounts with known data, ask for deletion, then look for what remains. We replace the right-of-access request with recall prompts to the agent, since an agent has no equivalent public profile to check.
- It tests one deletion route per service, which led them to flag the button-versus-formal difference; our design varies the deletion route (data deletion methods) within each agent, so can compare them directly.
- It has a six-week data-feeding step for realism and a delay of more than six months before checking; our recall checks happen soon after deletion. If we reuse their argument for waiting, note that we did not wait months.

## Use in our paper
- Cite as the main published audit of whether services delete after a request, with the 27% figure and the button-versus-formal gap, and for the argument that a user cannot verify erasure from the outside.
- Their account-creation-with-fictional-person design supports our use of synthetic facts and dedicated accounts.
