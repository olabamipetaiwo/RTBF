# Xue, Magno, Cunha, Almeida, Ross. The Right to be Forgotten in the Media: A Data-Driven Study

PoPETs 2016(4), pp. 389-402, DOI 10.1515/popets-2016-0046. File: `2_audits/xue-popets16-rtbf-media.pdf` (open-access PoPETs copy). Read the abstract, introduction, the dataset and content analysis in outline, Section 5 (attacks), the Streisand-effect results, the demographic section in outline, and the conclusion with recommendations. I did not read the LDA topic tables or the Twitter and Google Trends metric definitions in detail.

## Question
What kind of content is delisted under the "right to be forgotten" for UK media pages, can a third party discover delisted links and their requesters, and do requesters suffer a "Streisand effect" (Section 1)?

## Method
- Dataset: 283 delisted media pages that UK outlets republished themselves, analysed by manual classification and Latent Dirichlet Allocation topic modelling (Section 4).
- Attack (Section 5): to identify the requester of a known delisted article, search the engine for each name in the article together with the title; if the delisted URL is missing for that name, the name is the requester. Second attack: rediscover delisted links by searching in the same way. Proof of concept found two previously unknown delisted URLs and requesters.
- Streisand effect (Section 6): visibility gain measured with Google Trends and Twitter data before and after republication.

## Findings
- Strongest topics: violent crime, road accidents, drugs, murder, prostitution, financial misconduct, sexual assault; 221 of 283 pages concerned criminal events and 62 miscellaneous (cited by Bertram et al.).
- The requester-finding attack identified 80 requesters for 103 of the 283 articles; it failed for the other 180, probably because the requester is not named in the article (Section 5.1). Verification: in every case where the link was missing on google.uk, it still appeared on google.com (this holds because the ruling applied only to European Google sites at the time).
- Streisand effect: fewer than half of the requesters had a positive visibility gain, so it is not general, though some requesters did show large gains (Section 6).
- The authors' view is that the right "has been largely working", but that their attacks put its efficacy in question for online media content, estimating an attacker with enough resources could rediscover 30 to 40% of delisted URLs (Section 9.1).

## Limits the authors state
Moderate sample (283 articles); UK media only, so conclusions may not generalize (Section 7); the rediscovery attack was tried as a proof of concept at small scale and would need to get around rate limits.

## How it differs from ours
- Search delisting only; the page stays online and the "forgetting" is removal from results for a name query. The attack works because the delisting leaves an observable difference in behavior (a result missing for one query form but present for another).
- Its method is the same kind of move as ours: use the system's behavior under different queries to find out what a removal did. This turns a deletion into an inference problem and shows that an outside party can learn from the pattern of what disappears.

## Use in our paper
- Cite alongside Bertram et al. for the best-known right-to-be-forgotten mechanism (delisting), and for the point that removal can be probed from outside by differential querying. Keep it in the "audits of deployed services" group as work on delisting, not erasure.
- Do not describe it as a study of data deletion by services.
