# Bertram et al. Five Years of the Right to be Forgotten

ACM CCS 2019, 14 pages, DOI 10.1145/3319535.3354208. File: `2_audits/bertram-ccs19-five-years-rtbf.pdf` (Google Research copy). Read the abstract, introduction, Sections 2 and 3 (background, dataset, annotations, ethics), Sections 4 and 6 and the relevant parts of Section 5, related work and conclusion. I did not read every country and hostname table.

## Question
How do Europeans use the "right to be forgotten" ruling (delisting from search results) in practice, and what is delisted?

## Data and method
- All European delisting requests filed with Google Search from 30 May 2014 to 31 May 2019: 3,231,694 requested URLs from 502,648 requesters, 509,051 hostnames (Table 1, Section 3). The authors are Google employees; this is a retrospective analysis of the company's own records.
- Each URL has a verdict (delisted or rejected) and, from 22 January 2016, manual reviewer annotations: category of site (directory, news, social media, government, miscellaneous), content on the page, and type of requester (Tables 2 to 4). Google reviews each request by hand; "there is no automation in the decision making process" (Section 2.2).
- Ethics: the authors never discuss details that could identify requesters, so they cannot release sample URLs or the mapping to annotations, and they say this conflicts with reproducibility standards (Section 3.3).

## Findings
- Only 44.5% of requested URLs met the criteria for delisting; delisting rates ranged from 25% to 53% by country and from 3% to 100% by category of personal information (Introduction, Section 4.1).
- Two dominant intents: 29% of URLs related to social media and directory services containing personal information, and 21% to news and government sites, mostly the requester's legal history; 17% of removals relate to legal history (Abstract, Introduction).
- Concentration: France, Germany and the United Kingdom produced 50.1% of requested URLs; the top 1,000 requesters (0.2% of requesters) produced 16.3%, many of them law firms and reputation-management services (Section 4).
- Requests are mostly local (over 75% for country-code domains came from the same country) (Section 6).
- 84% of requested URLs came from private individuals; minors were 6% of requesters (Introduction).
- After requests peaked right after the ruling (about 282,000 URLs in the first two months), they fell to about 47,000 URLs a month from January 2015 (Section 4.1).
- Delisting happens on result pages for name queries in European search services and in other services when the search comes from the requester's country; the French regulator's demand for global delisting was pending at the court (Section 2.3).

## Limits the authors state
Cannot release URLs or exact content; results do not generalize to other countries' versions of the right (Russia, Turkey) (Section 2.4); pending requests omitted from the window (footnote 2); about half of URLs fall in "miscellaneous" categories.

## How it differs from ours
- It is about search-engine delisting, in which links are removed from results and the underlying page and data stay online. This is a different thing from deleting data a user gave to a service, and the paper says so (Section 2.1: "access to lawfully published, truthful information about a person may be restricted via search engines").
- It describes demand and the provider's decisions, not whether a deletion removed the data.

## Use in our paper
- Cite for scale and for the point that the right to be forgotten in its best-known form is delisting rather than erasure; also that a provider decides with manual review and no user-visible proof. It is the Google-side account that Shastri et al. cite.
- Careful wording: do not use these percentages as statistics on data deletion requests to services; they concern delisting only.
