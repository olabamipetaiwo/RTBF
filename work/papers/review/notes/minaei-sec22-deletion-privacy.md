# Minaei, Mondal, Kate. Empirical Understanding of Deletion Privacy: Experiences, Expectations, and Measures

USENIX Security 2022 (31st). Pages 3415-3432, read from the printed numbers on the first and last pages of the PDF. File: `4_users/minaei-sec22-deletion-privacy.pdf` (USENIX proceedings copy). Read the abstract, introduction, the limitations and the statement of findings. I did not read the contextual-integrity analysis of scenarios or the design-guideline section in detail.

## Question
What are users' experiences with deleting social-media posts, what do they expect about the privacy of the act of deleting, and how effective do they find current deletion mechanisms (Abstract)?

## Method
- Online survey of 191 participants from Europe and the US recruited on Prolific, using the contextual integrity framework to describe scenarios (who might notice a deletion, in what context). Videos and scenarios in English (Limitations).

## Findings
- More than 80% had deleted at least one social-media post; on average about 35% of deletions happened more than a week after posting (Abstract).
- The main reason for deleting was irrelevance over time; most participants nevertheless believed that a deletion signals that the deleted content contained something damaging to its owner.
- Participants were significantly more concerned about large-scale data collectors (third-party data companies, the government) noticing a deletion than about people in their social circle.
- Participants judged popular deletion mechanisms as very useful for removing content in several scenarios but "not very effective in protecting the privacy of those deletions" (Abstract); design guidelines follow.

## Limits the authors state
Prolific sample, probably younger and more tech-savvy; English-only; self-reported experiences and scenario judgments (Limitations).

## How it differs from ours
- The deletion in question is of posts on social platforms, and the privacy issue is that the act of deleting is itself a signal. It supports the point that a deletion event is information, which Chen et al. (CCS 2021) show for models, and shows the user side of it. It is not about whether data is removed.

## Use in our paper
- Cite for user experience of deletion and the finding that users judge current deletion tools as not effective at protecting privacy, in the "users" paragraph. Keep claims to social-media posts.
