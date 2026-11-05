# Nouwens, Liccardi, Veale, Karger, Kagal. Dark Patterns after the GDPR: Scraping Consent Pop-ups and Demonstrating their Influence

ACM CHI 2020 (Honolulu; PDF is arXiv v1, 8 January 2020; authors on the PDF show four names, and the full list should be checked against the proceedings entry for the manifest). File: `4_users/nouwens-chi20-dark-patterns-gdpr.pdf`. Read the abstract, introduction, research questions, the scraping study summary, the field-experiment results and the limitations. I did not read the legal requirements mapping or the experimental design details beyond the outline.

## Question
How do the most common consent management platform (CMP) designs affect people's consent choices, and how many comply with minimal GDPR requirements (Abstract)?

## Method
- Study 1: scraped the designs of the five most popular CMPs on the top 10,000 UK websites (n = 680 sites with them), and checked them against minimal requirements set from European law: no pre-ticked boxes, rejection as easy as acceptance, explicit consent.
- Study 2: a field experiment with 40 participants testing the eight most common designs (Section 4).

## Findings
- "Dark patterns and implied consent are ubiquitous": only 11.8% of the 680 sites met the minimal requirements; 56.2% pre-ticked optional vendors (Section 3).
- Notification style (banner or barrier) had no effect on consent; removing the opt-out button from the first page raised consent by 22 to 23 percentage points; offering granular controls on the first page lowered consent by 8 to 20 percentage points (Abstract).
- The authors suggest focusing regulation on the few central CMP vendors as an efficient route to compliance.

## Limits the authors state
The scraper could not guarantee freedom from false positives and negatives because consent pop-ups are rendered dynamically in JavaScript and may be customised; small participant sample (40) recruited through personal contacts (Limitations, Section 4).

## How it differs from ours
- Consent, not deletion. Its method is relevant as a measurement approach: scrape deployed interfaces at scale, then test their effect with users. It shows that interface design alone shifts choices by tens of points.

## Use in our paper
- Cite with Mathur et al. (dark patterns at scale) and Utz et al. for evidence that privacy controls are often designed in ways that steer users, and that the presence of a control does not mean it works as the user expects. Another candidate to trim if space is short.
