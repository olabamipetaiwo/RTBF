# Rao, Schaub, Sadeh, Acquisti, Kang. Expecting the Unexpected: Understanding Mismatched Privacy Expectations Online

SOUPS 2016 (Twelfth Symposium on Usable Privacy and Security), Denver, June 22-24, 2016, USENIX. Page range as in the manifest (not rechecked here). File: `4_users/rao-soups16-mismatched-expectations.pdf` (USENIX proceedings copy). Read the abstract, introduction, the method in outline, the results on deletion expectations and the discussion with limitations. I did not read the regression models for collection and sharing in detail.

## Question
Where do users' expectations about a website's data practices (collection, sharing, deletion) differ from the practices the site states in its privacy policy (Abstract)?

## Method
- Between-subjects online study: 240 participants recruited on Amazon Mechanical Turk (US only), each assigned to one of 16 websites chosen across finance, health and dictionary categories (with and without offline presence). Participants looked at the site, then gave "best guess" answers on whether the site collects, shares or deletes specific data, in the sense of expected likelihood rather than desire (Section 3).
- Expectations were compared with data practices annotated by the authors from each website's privacy policy (deletion annotated as full, partial or none).

## Findings
- Deletion: 32% of participants expected websites to allow full deletion, while only 19% of the analysed sites did; 48% expected partial deletion against 12% of sites; about 20% thought no deletion would be allowed against 19% of sites (Discussion). The authors conclude that participants "expect websites to allow deletion more than websites actually do".
- Participants expected all website types to permit deletion; website type did not affect deletion expectations. Age and trust in the website changed expectations (older participants were about 1.8 times more likely per unit to expect no deletion).
- More generally, mismatches between expectations and stated practices are substantial and vary with website type and user traits.

## Limits the authors state
Practices are those disclosed in privacy policies, and "how a website actually handles personal information... could potentially be different, but this is difficult to assess in practice"; MTurk, US-only participants; online rather than in-lab (Limitations).

## How it differs from ours
- Expectations against stated practices, not against observed behavior. The authors name the gap we address as the part that is hard to assess.

## Use in our paper
- Cite for the finding that users expect more deletion than sites provide, from 2016, to show the expectation gap predates LLM assistants. Pair with Malki et al. (2025) for the LLM case. Use it to state the limitation we lift: comparing expectations with what happens, not with what a policy says.
