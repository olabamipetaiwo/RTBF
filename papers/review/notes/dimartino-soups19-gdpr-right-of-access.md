# Di Martino, Robyns, Weyts, Quax, Lamotte, Andries. Personal Information Leakage by Abusing the GDPR "Right of Access"

SOUPS 2019 (Fifteenth Symposium on Usable Privacy and Security), USENIX, pp. 371-386 (last printed page 386 confirmed from the PDF, which settles the 385 versus 386 question). File: `2_audits/dimartino-soups19-gdpr-right-of-access.pdf` (USENIX proceedings copy). Read the abstract, introduction, method (Sections 3.1 to 3.3), the main results and the limitations. I skimmed the individual case descriptions in the appendix and the authentication techniques.

## Question
How do organizations verify the identity of someone who asks for their data under the right of access (Art. 15), and can an impostor with forged or public information obtain another person's data (Section 1)?

## Method
- Two co-authors served as the targeted individuals, giving written consent. The other authors acted as the adversary, sending 55 access requests to organizations (finance, entertainment, retail, transport, news and others) that held the targets' data. About half are in the Belgian Alexa top 50 (Section 3.1).
- Adversary information came only from forged or public sources (social media, altered ID cards). Organizations are pseudonymised by category (Section 3.2).
- Ethics: approved by the university ethics committee; unrelated people's data that arrived by mistake was deleted at once (Section 3.3).

## Findings
- For 15 of the 55 organizations the adversary obtained full access to the target's personal data, including financial transactions, website visits and physical location history (Abstract). The table covers the 37 organizations that responded (Table 3).
- Only 12 of 41 organizations that said they would do so enforced a stated verification policy, and only 2 of 55 called the subject on a known phone number (Section 3.5, as printed).
- 8 of the 15 vulnerable organizations would not have been vulnerable without an altered ID card (Section 3.6).
- Policies and practice "vary significantly" and can be manipulated by social engineering. The paper proposes improvements such as calling the subject at a known number (Section 4).

## Limits the authors state
Only two targeted individuals; 55 organizations across industries; success depends on the personality of the staff member handling the request, and the required credentials cannot be defined exactly (Section 6).

## How it differs from ours
- It concerns access, not deletion, and it studies an attack (impersonation), not whether data was removed.
- Relevance to deletion: the same weakness would let an impostor trigger a deletion. Rupp et al. (PoPETs 2022) make this point and report that only 41% of services required an extra authentication step before erasing. For our agents, authentication is the logged-in session; we do not test impersonation.

## Use in our paper
- Cite once, if at all, for the claim that rights-request handling varies widely and is often weakly authenticated, as a reason that "deletion requests are honored" is not something a user can take for granted.
- Because it is off the deletion topic, this paper is a candidate to drop from the final list of about 50 if space is short; keep it only if the Related Work paragraph needs the authentication point.
