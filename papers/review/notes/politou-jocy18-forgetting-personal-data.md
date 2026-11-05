# Politou, Alepis, Patsakis. Forgetting personal data and revoking consent under the GDPR: Challenges and proposed solutions

Journal of Cybersecurity 4 (1), 2018, pp. 1-20, DOI 10.1093/cybsec/tyy001 (review article, open access). File: `1_systems/politou-jocy18-forgetting-personal-data.pdf`. Read the abstract, introduction, the sections on the right to be forgotten and on implementation challenges, and the conclusions. I skimmed the long background on privacy theory and the consent-revocation section (not our topic) without reading every proposed consent framework.

## Question
What are the controversies around consent withdrawal and the right to be forgotten (RtbF) under the GDPR, and can existing methods and technologies implement them in current computing infrastructures (Abstract)?

## Argument
- Article 17 covers more than erasure: erasure is the controller deleting data, while "to be forgotten" implies deletion "from all possible sources" in which the data reside (RtbF section).
- Article 17(2) requires "reasonable steps, including technical measures" to tell other controllers to erase links, copies or replications. The authors conclude that controllers need technical means "to allow the tracking of personal information and to prove its efficient removal", and that "the burden to prove that the erasure has been implemented successfully from all available sources is still technologically questionable" (RtbF section).
- The regulation does not say how to enforce deletion when data has reached third parties or been anonymized or pseudonymized, so some doubt enforceability; Article 19 exempts notifying recipients when this "proves impossible or involves a disproportionate effort" (RtbF section).
- The CJEU ruling removes links, not the information itself, so it "cannot be considered as an actual forgetting" (RtbF section).
- Some scholars argue that forgetting comes in "grades" and could rely on the level of encoding or retrieval, not on plain erasure (RtbF section).
- Implementation obstacles (Implementation challenges, Challenges and conclusions):
  - Hadoop-style immutable storage never physically deletes files; old versions are only flagged inactive, which blocks compliance with assured deletion.
  - Backups: the GDPR deletion duty applies to backups too, but backups exist for integrity and disaster recovery, and in financial institutions records may have to be kept.
  - A dashboard that lets users delete their data (for example Google's activity controls) gives relief, but "there is not any evidence of permanently erasure of these data from company's servers", and one can never know if data were replicated elsewhere.
- Conclusion: enforcement is feasible if implementation guidelines and low-level specifications are put in place "in a clear and cross-platform manner in order to cater for all possible exceptions and complexities".

## Limits
A review article: no new measurement. Written before the GDPR applied (accepted February 2018), so it predates enforcement experience and LLMs.

## How it differs from ours
- It is legal and architectural analysis of whether deletion can be made to work; we test whether it did work in deployed agents.
- It shows the tension our results illustrate: the law asks for deletion from all sources and for proof, yet the technical means to prove it are missing.

## Use in our paper
- Cite for the legal basis (Article 17(1)(b), 17(2), 19) and for the point that proving deletion is the unresolved part. Supports Section 6.2 (users cannot verify) from the controller side: even controllers lack means to prove removal.
- The backups point links to our survey question on expectation of permanent deletion from the database and backups (Politou's separate Computer Law and Security Review paper on backups has no PDF yet).
- The PDF header carries a download stamp from academic.oup.com for a University of Central Florida user, dated 4 November 2026. This is only a download watermark; the paper is open access.
