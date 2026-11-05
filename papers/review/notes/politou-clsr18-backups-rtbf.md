# Politou, Michota, Alepis, Pocs, Patsakis. Backups and the right to be forgotten in the GDPR: An uneasy relationship

Computer Law & Security Review 34 (2018), pp. 1247-1257, DOI 10.1016/j.clsr.2018.08.006 (page header and DOI line in the PDF). File: `1_systems/politou-clsr18-backups-rtbf.pdf` (Elsevier PDF, downloaded by the user through the UCF library). Read the abstract, introduction, the legal discussion of erasure and backups, the part on timescales and backup media, and the conclusions. I did not read the sections on ERP systems, search services and security standards in detail.

## Question
What does the GDPR's right to erasure (Article 17) imply for backups and archives, and what organizational, business and technical problems follow (Abstract)?

## Method
- Legal and technical analysis, not an empirical study. The authors read Articles 12, 17 and 89 and recitals against common backup standards, retention policies and backup media.

## Findings
- It is reasonable to argue that the right to erasure applies to backups as well; the UK ICO's guidance says deletion should also apply to backups, while recognising that deletion is not always straightforward and that it is sometimes preferable to put information "beyond use" with safeguards (Section 3).
- Article 12(3) requires the controller to act on an erasure request "without undue delay and in any event within one month of receipt", extendable by two further months for complex or numerous requests. This one-month limit is about responding to the request, and is not a deadline for physical removal from every copy.
- Technical obstacle: for tape backups deleting a single record "is impossible" without restoring the whole database, because tapes store data in sequential blocks, so deletion carries cost and complexity (Section 4).
- The GDPR does not prescribe technical methods. The authors say it is deliberately technology-agnostic, which leaves the practical meaning of "erased" to organizations (Conclusions).

## Limits the authors state
It is a discussion paper that identifies challenges. It does not measure what organizations do, and it states no remedy that fits every backup system.

## How it differs from ours
- It concerns the legal duty and the engineering difficulty of deleting from backups. We check what happens after deletion in deployed assistants. It gives the reason deletion may legitimately take time or leave copies, which affects how we interpret a recall success shortly after deletion.

## Use in our paper
- Cite for (a) erasure applies to backups, but "beyond use" is accepted by the ICO as a safeguard, so deletion in law need not mean physical removal, and (b) the one-month limit in Article 12(3). This also corrects the Liu et al. "45 calendar days" attribution noted earlier: the GDPR period is one month.
- Use in the legal paragraph with Politou's other paper (JoCy 2018), already read.
