# Garg, Goldwasser, Vasudevan. Formalizing Data Deletion in the Context of the Right to be Forgotten

EUROCRYPT 2020 (Lecture Notes in Computer Science), DOI 10.1007/978-3-030-45724-2_13. File: `1_systems/garg-eurocrypt20-formalizing-deletion.pdf` (authors' copy, arXiv 2002.10635 v1, Feb 2020; page numbers of the published chapter not checked). Read the abstract, the introduction (Sections 1 to 1.3), the high-level definition and its lessons. I did not read the formal UC-framework definitions, the example constructions in Section 3, or the proofs in the appendix. Cryptographic proofs are beyond what this review needs.

## Question
How does an honest data collector know whether it complies with the right to be forgotten? The authors give a formal definition of what a deletion request must achieve (Abstract, Section 1).

## The definition (Section 1.1)
- "Leave no trace": after a deletion request is processed, the data collector and the rest of the system must be in a state equivalent, or very close, to the state they would have been in if the deleted data had never been provided.
- Formally, a real-world execution (the user shares data, then asks for deletion) and an ideal-world execution (the user never interacts) must give the same joint distribution of the collector's memory state and its communication with third parties, for any other users and any environment.
- Consequences they draw:
  - The data must not persist in the collector's memory, and stored information that depends on it must go too. They note this "diverge[s] from the GDPR... as it only requires deletion of data rather than what may have been derived from it via processing" (Section 1.1).
  - The collector cannot reveal collected data to external entities without a mechanism to forward deletion requests, since sharing "precludes it from honoring future deletion requests" (Section 1.1; Article 17's duty to inform other controllers is cited).
  - The collector must be "diligent": track where each user's data is stored, since a collector cannot delete what it cannot find.
  - Metadata matters: data structures must not preserve traces of deleted data (history independence). Even erasing a file can leave its size or the fact that a file existed (Section 1.1).
  - Authentication is needed so that other users cannot read data that is meant to be deleted or trigger deletions (Section 1.2).
- The GDPR statement that withdrawal "shall not affect the lawfulness of processing based on consent before its withdrawal" suggests derived results may be kept, yet processed versions "may encode all or most of the original data", and some machine learning models memorize their training data (Section 1, "Defining Deletion").

## Scope limits the authors state
- Honest collector only; no adversary. They do not try to let a collector prove to a user that data was deleted, and say this is "impossible in general, as a malicious data collector could always make additional secret copies" (Section 1; footnote 2 names settings where certification may be possible).
- The definition "cannot be viewed as expressing the statements of current laws"; it offers possible interpretations of what the law could expect (Abstract).
- Which deletion requests should be honored is out of scope (Section 1, "When is it okay to delete?").
- Relationship to machine unlearning: the closest prior definition is Ginart et al. on retracting training data from a model; the paper explains differences in scope and modelling in Section 2.2.

## How it differs from ours
- It is a theoretical definition for an honest collector; it contains no measurement. We test deployed services from outside, where we cannot see the collector's memory state. Their definition names the property we cannot observe (the full system state), and we observe only one consequence of it (whether a fact can be recalled).
- Their statement that a collector cannot prove deletion to users supports our Section 6.2: even in theory a user cannot verify, so verification must rely on indirect signals.

## Use in our paper
- Cite for a precise definition of deletion that includes derived data and metadata ("leave no trace"), and for the statement that proof of deletion is impossible in general. It frames what "deleted" should mean when we say a fact was or was not recalled.
- Note a mismatch to respect: our recall check examines whether a fact can be reproduced, not the whole system state, so it can show a failure of deletion but cannot show success; this matches our reporting of "can't tell" as its own count.
