# Mathur, Acar, Friedman, Lucherini, Mayer, Chetty, Narayanan. Dark Patterns at Scale: Findings from a Crawl of 11K Shopping Websites

Proc. ACM Hum.-Comput. Interact. 3, CSCW, Article 81 (November 2019), 32 pages, DOI 10.1145/3359183 (from the PDF's reference block). File: `4_users/mathur-cscw19-dark-patterns-at-scale.pdf` (arXiv v2, 20 September 2019). Read the abstract, the contributions, the crawler and clustering method in outline, the prevalence summary and the lower-bound statements. I did not read the per-type descriptions, the taxonomy of attributes or the third-party analysis in detail.

## Question
How common are dark patterns on shopping websites, of what types, and which third parties supply them (Abstract)?

## Method
- Built a crawler that visits product, cart and checkout pages, divides each page into visible segments (about 13 million segments), clusters the text of segments with hierarchical clustering, and gives clusters to an expert analyst to label, instead of reading every page manually (Sections 3 and 4).
- Crawled about 53,000 product pages from about 11,000 shopping websites drawn from a list of 19,455 English-language shopping sites found by classifying a larger set of sites (Section 4).

## Findings
- 1,818 dark pattern instances of 15 types in 7 broader categories, found on 1,254 of about 11,000 sites (about 11.1%) (Section 5).
- 183 websites used deceptive practices; 22 third-party entities offered dark patterns as a turnkey solution (Abstract).
- A taxonomy of dark-pattern attributes (for example, asymmetric, covert, deceptive, hides information, restrictive).

## Limits the authors state
Only text-based interface elements on product, cart and checkout pages of English-language shopping sites were analysed, so the numbers are "a lower bound" on dark patterns in use (Sections 1 and 3).

## How it differs from ours
- Shopping, not data deletion, and a text-based crawl at scale. Its relevance to us is the method idea: automated discovery with expert judgment on top, and the explicit statement of a lower bound. It also shows the kind of design that can make controls hard to use.

## Use in our paper
- Cite once, with Nouwens et al. and Utz et al., for "interface design steers users", only if the paragraph on privacy controls needs a general dark-pattern source. It is peripheral to deletion and can be dropped first if the list is trimmed. Always report 11.1% as a lower bound on shopping sites.
