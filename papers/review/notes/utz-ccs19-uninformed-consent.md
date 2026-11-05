# Utz, Degeling, Fahl, Schaub, Holz. (Un)informed Consent: Studying GDPR Consent Notices in the Field

ACM CCS 2019, 18 pages, DOI 10.1145/3319535.3354212 (from the PDF's reference block). File: `4_users/utz-ccs19-uninformed-consent.pdf` (arXiv v2, 22 October 2019). Read the abstract, introduction, research questions, the summary of results and the limitations. I did not read the classification of 1,000 notices, the statistical models or the survey coding in detail.

## Question
Do the position, number of choices, nudging and wording of cookie consent notices change what visitors consent to (Abstract)?

## Method
- Systematized the design properties of a sample of 1,000 consent notices collected from live websites (Section 3).
- Three field experiments on a German-language e-commerce site with more than 80,000 unique visitors: position of the notice (Experiment 1, n = 14,135), number of choices and nudging by emphasis or pre-selection (Experiment 2, n = 36,530), privacy-policy link and technical versus non-technical wording (Experiment 3, n = 32,225). A follow-up survey of more than 100 visitors asked about their motivations and expectations.

## Findings
- Visitors were most likely to interact with notices at the bottom (left) of the screen; bars at the top had the lowest interaction rates.
- Interaction was higher with notices offering at most two options than with notices that let users choose per category or company, and the more choices a notice offered, the more likely visitors were to decline cookies.
- Nudging has "a large effect on the choices users make": small implementation decisions can substantially change whether and how people interact with the notice (Abstract).
- More than 60% of popular European websites showed such notices after the GDPR took effect (May 2018).

## Limits the authors state
All experiments ran on one German-language e-commerce site whose visitors may not be representative; the survey was voluntary and small (Section 7).

## How it differs from ours
- It is about consent at the moment of collection, not deletion. Its use for us is the principle: how a control is presented changes what users do, and the presence of a control does not make it informed. It also shows field experiments at scale, which we cannot run.

## Use in our paper
- Cite once, if the Related Work paragraph on privacy controls needs a consent example, for "design details of a control change user behavior". It is the least central of the group 4 papers and can be dropped if the list needs trimming.
