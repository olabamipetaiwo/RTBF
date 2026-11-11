# Xu, Zhu, Zhang, Zhou, Yu. Machine Unlearning: A Survey

ACM Computing Surveys 2023, DOI from Crossref (checked earlier). File: `3_ai/xu-csur23-machine-unlearning-survey.pdf` (arXiv v1, 6 June 2023; the template still shows "J. ACM ... 2018" placeholders, so this is a different typeset version from the journal). Read the abstract, introduction, the taxonomy and definitions of verifiability, the verification-methods section and Table 5. I skimmed the sections on individual unlearning methods and did not read the application and open-problems sections in full. Compare with the journal version before quoting page numbers or sentences.

## Question
What are the main approaches to machine unlearning, how are they verified, and what problems remain (Abstract)?

## Content
- Defines machine unlearning (also called selective forgetting, data deletion, scrubbing) as removing samples and their influence from a training set and a trained model, motivated by privacy, usability and the right to be forgotten (laws named: GDPR, CCPA, Japan's APPI, Canada's proposed CPPA) (Section 1).
- Taxonomy of unlearning strategies: exact unlearning by retraining or partitioning, and approximate unlearning that manipulates the model's weights; plus a taxonomy of verification mechanisms (Figure 4).
- Verification mechanisms (Section 3.2, Table 5): retraining-based; attack-based (membership inference or model inversion); relearn-time-based (how fast the model regains performance on the removed samples); accuracy-based; theory-based (similarity to a retrained model); information-bound-based (upper bound on residual information). The survey marks retraining-based verification as applicable only to special schemes, attack-, relearn- and accuracy-based as having "inadequate verification capability", and the theory-based ones as comprehensive but hard to implement.

## Statements to use
- "Model providers may claim externally that they remove those influences from their models, but, in reality, this is not the case" (Verification Mechanisms; cites an earlier work). For data providers, proving that the provider completed unlearning "may also be tricky, especially for complex deep models with huge training datasets" (same passage).
- Removing a small portion of samples barely changes a model, and even if removed, the model may still predict correctly because other users provided similar samples; so a reasonable verification mechanism "is a topic worthy of further research".

## Limits
A survey, mostly about classification models; the language-model material is thin, so it does not cover recent LLM unlearning.

## How it differs from ours
- It covers methods that act on trained models. Our work does not test any of these methods; it tests products whose internals are unknown.

## Use in our paper
- Cite as the broad survey for definitions and for the point that verification of unlearning is an open problem with no accepted method. For LLM-specific unlearning verification, rely on Xue et al. (CSUR 2026) and MUSE.
