# Xue, Hu, Lu, Shen, Li, Guo, Zhou, Li, Zhang, Zhang. Towards Reliable Forgetting: A Survey on Machine Unlearning Verification

ACM Computing Surveys 2026 (venue from Crossref today per the manifest; confirm volume and article number). File: `3_ai/xue-csur26-unlearning-verification-survey.pdf` (arXiv v3, 7 April 2026, template still with placeholders). Read the abstract, introduction and contributions, the verification-method taxonomy (behavioral versus parametric), the evaluation dimensions, and Section 6.3 on threats to behavioral verification. I did not read the per-method descriptions in Sections 3 and 4 in full. Check against the journal version before quoting.

## Question
How can anyone verify that unlearning really happened, and how reliable are the existing verification methods (Abstract)?

## Content
- Verification methods are split by evidence into behavioral (the model's responses to inputs: fingerprints and backdoors, privacy attacks such as membership inference, and performance-based tests) and parametric (examining parameters or derivatives, with theoretical guarantees; includes proof-of-unlearning logs) (Section 1).
- Seven evaluation dimensions: theoretical guarantees, access requirements, sample-level verification, verification accuracy, reliance on pre-injected data, efficiency and scalability, and method specificity.
- The central question stated: "how can model providers convincingly demonstrate that the targeted data has been thoroughly and irreversibly removed?" (Introduction). Most machine learning services are "opaque, server-side systems".
- A user-side idea in the survey: a user injects unique backdoor triggers into their own data and checks later whether the model's response to them changes (cited study); this gives black-box verification, but requires the data to have been planted before training. A related approach covers language models in black-box settings (WaterDrum, a watermark-based method).

## Findings the survey states
- No standard framework: a model can count as "successfully unlearned" under one criterion and fail another (Jeon et al., cited in the introduction).
- Providers could "selectively present verification outcomes to give a false impression of compliance", and existing verification mechanisms have exploitable weaknesses (Introduction, Section 6).
- Behavioral verification "inherently lacks robustness and exposes a broad and weakly protected attack surface": a model can be made to look forgotten by suppressing fingerprints, obfuscating privacy-leakage signals (for example with differential privacy or clipped outputs), or spoofing performance (Section 6.3). The root problem named is "the decoupling between observable behavior and true" removal.

## Limits
A survey with no experiments; coverage is mostly of research verification schemes that need the provider's cooperation or access to the model.

## How it differs from ours
- Every verification scheme in it assumes the auditor can access the model, or can plant a signal before training. We have neither: we audit products as an ordinary user, and our synthetic facts are planted through chat.
- Section 6.3 is the closest statement to our limit: observed behavior can differ from true removal in either direction. So our design reports recall failed as evidence that deletion failed, and treats recall success and can't tell as non-evidence of deletion.

## Use in our paper
- Cite for the claim that verification of unlearning is unresolved and that behavioral checks are weaker than parametric ones. It also supports describing our method as a behavioral check performed from outside.
- The survey's statement that a provider might hide non-compliance is an argument to keep our design (outside, repeated, with a control fact), not to rely on the provider's own answer.
