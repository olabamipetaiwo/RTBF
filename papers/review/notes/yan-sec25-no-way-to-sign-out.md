# Yan, Liao, Ma, Aldeen, Kumar, Cheng. No Way to Sign Out? Unpacking Non-Compliance with Google Play's App Account Deletion Requirements

USENIX Security 2025 (34th), pp. 3277-3296 (both ends read from the printed page numbers in the PDF). File: `2_audits/yan-sec25-no-way-to-sign-out.pdf` (USENIX proceedings copy). Read the abstract, introduction, background on Google Play's requirement, the pilot study, DeleteTracker's design (all four modules, especially the Verifier), results for availability, compliance and functionality, the evaluation summary and limitations. I did not read the prompt-engineering details of the link classifier or the appendix.

## Question
Do apps on Google Play provide account deletion links, do these links meet Google Play's requirement of both an in-app path and a web method, and can users really delete their accounts by following them (RQ1 to RQ3, Section 1)?

## Method
- Pilot study of the top 50 apps, analysed by two PhD-level students by hand, to define three issue types: link, content and functionality issues (Section 3).
- DeleteTracker, with four modules (Section 1, Section 4): a crawler for deletion links in the Google Play app and website, a link analyzer (missing, inaccessible, similar, cross-platform-inconsistent links), a method classifier (language-model prompting to label a page as in-app path, web-based, alternative such as email, or missing), and a verifier.
- Verifier (Section 4.4), done by hand because apps differ too much to automate: two annotators with fixed virtual-user profiles register, log in, request deletion, and then test the result. For apps with a deletion delay (7, 14 or 30 days) they verified one month after the request. Deletion counts as failed if re-login still works, or re-registration with the same email says it is already registered; for Google sign-in accounts, if previously created usage traces (for example a stored weight and age, or a liked song) are still there after re-login.
- Scale: 863 apps analysed from 1,000 popular apps (AndroZoo-based list) (Section 5, Limitations).

## Findings
- 291 of the 863 apps gave no account deletion link and 25 gave inaccessible links; of 494 apps with a link, 13.8% offered only an in-app path, 50.8% only a web method, and only 8.5% both, as required (Introduction, Section 5). 64.6% offered one method.
- Functionality (Section 5, RQ3): the verifier registered accounts for 182 apps (others needed a phone number, card, subscription or region) and submitted 176 deletion requests. 12 apps failed to delete the account as promised: 2 had a delete button that returned an error; 5 let the tester log in again with the old credentials and the usage traces were still there; 5 refused re-registration with the same email ("Email already taken") after the stated retention period (for example one app stated 27 days). Two of the 12 apps have over 500 million downloads and 7 over 100 million.
- The authors reported the findings to Google through the vulnerability process; Google acknowledged them and assigned Medium (S2) severity (Abstract).

## Limits the authors state
Only 1,000 popular apps considered; recall estimated from 100 sampled apps; the crawler was slow and missed some apps; the functionality check is manual with two annotators and so covers 176 requests; apps requiring sensitive data to register were not testable (Section 7).

## How it differs from ours
- Its functionality test is the same idea as ours, an external behavioural check after a deletion request (can I log in again; do my traces remain), carried out on fewer than 200 apps by hand. For agents the equivalent of "re-login and look for traces" is recall of a synthetic fact, and our traces are text the agent can repeat, not account state.
- It waited a month before checking, to allow for deletion delays. We should say how much time passed between deletion and recall in our design, and treat that as a limit if it was short.

## Use in our paper
- Cite for a recent (2025) peer-reviewed audit that goes past interface checks to test whether deletion worked: 12 of 176 requests failed (about 7%). Compute and state the base (12 of the 176 submitted requests), not 12 of 863.
- Support for the usage-trace method: plant a marker, request deletion, test for the marker afterwards.
- A scope note: the paper says it differs from an earlier 2022 work that checked functionality through code analysis; I did not identify which reference it is, so do not rely on that comparison.
