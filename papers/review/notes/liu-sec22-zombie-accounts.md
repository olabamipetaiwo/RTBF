# Liu, Jia, Tan, Liu, Xing. How Are Your Zombie Accounts? Understanding Users' Practices and Expectations on Mobile App Account Deletion

USENIX Security 2022 (31st), pp. 863-880. File: `2_audits/liu-sec22-zombie-accounts.pdf` (USENIX proceedings copy). Read the abstract, introduction, background on the right to deletion, the pre-study (Section 4), the study design, recruitment, limitations, and the results for RQ2 and RQ3 in part. I skimmed the interview quotations and the open-text coding, and did not read the appendix questionnaire. The paper combines an app audit with a user survey, so it appears in group 2 and is also relevant to group 4.

## Question
Do users know about, use and understand mobile-app account deletion, and does the design of apps meet their expectations (Section 1, RQ1 to RQ3)?

## Method
- Pre-study (Section 4): 60 apps (30 from Chinese app stores, 30 from Google Play top free apps, October 2021), sampled across three popularity bands. For each app the authors registered a new account with a new phone, email and number, used it for at least half an hour, then walked through the deletion process, recording steps, conditions, notices and policy text. From this they derived a four-part model of account deletion: operation, condition, effect, time frame (Figure 2).
- Survey: 647 valid participants (279 US via Prolific, 368 China via Wenjuanxing; 688 recruited), November 2021 to January 2022, plus 20 on-site interviews (November 2021 to March 2022) (Section 5).

## Findings
- Pre-study: 8 of 60 apps had no self-service deletion and 3 required a website, 18% (11/60) in total; users needed on average 6.14 clicks, 4.01 of them to find the option; 65% (34/52) showed a notification step, 42% (22/52) authentication; only 65% (34/52) said which types of data would be deleted, and 58% (30/52) said anonymization would be used; 42% (22/52) stated a time frame, ranging from immediate to one year (14.75 days on average) (Section 4.2).
- Survey: 89% willing to protect personal data and 95% did not want unused apps to keep using their data, yet 75% likely kept accounts that should have been deleted (zombie accounts); 55% had deleted an account successfully (Section 1, RQ1 and RQ2).
- Understanding: more than half (57%) thought personal data would not be deleted after account deletion, and 61% thought deletion was reversible; 45% (125/279) of US participants wrongly believed that deactivation deletes data (Section 6.2). The authors read the first result as either misunderstanding or being "privacy resigned" and not believing the action takes effect.
- Experience: only 30% (105/355) of those who deleted found nothing inconvenient; 70% said the current design does not meet their expectations (Sections 1 and 6.3).

## Limits the authors state
Recruitment through online platforms; interviews on campus and reduced by COVID-19; the pre-study covers Android apps only; social desirability may inflate reported awareness (Section 5.4). The 60-app audit examines what each app shows and says, so it does not verify that data was removed.

## How it differs from ours
- It studies what users believe about deletion and how hard it is to start, not whether deletion works. The finding that many users doubt that deletion removes data is evidence for why verification matters, and suits our Section 6.2.
- Its four-part model (operation, condition, effect, time frame) is a useful vocabulary for what a platform tells users; our "documentation" category records the effect and time-frame parts for LLM agents.

## Use in our paper
- Cite for user doubt (57% think data is not deleted) and for the heterogeneity of deletion processes across apps.
- Care with one passage: Section 4.2 attributes "Businesses must respond to your request within 45 calendar days" to the GDPR, but that wording is from the California law; the GDPR's response period is one month (Art. 12(3), as Rupp et al. state). Do not repeat it.
