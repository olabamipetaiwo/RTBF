# Shi, Lee, Huang, Malladi, Zhao, Holtzman, Liu, Zettlemoyer, Smith, Zhang. MUSE: Machine Unlearning Six-Way Evaluation for Language Models

ICLR 2025 (venue confirmed earlier on the iclr.cc poster page). File: `3_ai/shi-iclr25-muse.pdf`. **This PDF is arXiv v2 (14 July 2024, marked "Preprint. Under review"), not the ICLR 2025 camera-ready.** Numbers below come from the abstract and introduction and must be checked in the ICLR version before quoting. Read the abstract, introduction, the six criteria and metric definitions (Section 3), and the summary of results. I did not read the per-algorithm tables or appendices.

## Question
Do approximate unlearning algorithms for language models meet what both data owners and model deployers expect, measured on six properties (Abstract)?

## Method
- Six criteria: (1) no verbatim memorization, (2) no knowledge memorization, (3) no privacy leakage, (4) utility preservation on data not meant to be removed, (5) scalability with the size of the removal request, (6) sustainability over sequential requests (Figure 1).
- Reference: a model retrained without the forget set. A good unlearned model should match the retrained model on each measure. Privacy leakage (PrivLeak) is the relative gap in membership-inference AUC between the unlearned and the retrained model on forget and holdout data; the ideal is close to zero (Section 3).
- Data: Harry Potter books and BBC news articles collected after August 2023 (Section 3.2). Models: LLaMA-2 7B for news and ICLM-7B for books, fine-tuned to create a target model (with the forget set) and a retrained model (without). Eight approximate unlearning algorithms, including negative preference optimization (NPO) and task vectors.

## Findings
- Most algorithms reduce verbatim and knowledge memorization to varying degrees, but only one avoids severe privacy leakage (Abstract). NPO and task vectors are the best at removing memorization, but NPO often permits privacy leakage, and both sharply reduce utility and struggle with large forget sets and with successive requests (Section 1).
- The authors conclude that unlearning algorithms "generally fail to meet data owner expectations in preventing privacy leakage, which is one of the primary motivations for unlearning" (Section 1).

## Limits the authors state
The benchmark covers two corpora and 7B models with fine-tuned targets, not production-scale pretraining (Section 3.2); the leakage test is a membership-inference test, which depends on the attack used.

## How it differs from ours
- It evaluates unlearning algorithms inside open models, with access to weights and to the retrained reference. We evaluate whole products from outside with no reference model.
- Its split of what a data owner wants (no verbatim text, no knowledge, no sign that the data was ever used) is useful: our recall check tests the second one (does the assistant still know the fact) at the behavior level.

## Use in our paper
- Cite for the current state of LLM unlearning and for the claim that approximate unlearning often fails privacy-leakage or utility goals. Use the published version's numbers, not these.
- Distinguish: MUSE concerns removing training data from weights, while the deletion requests we test act on products' conversation history and memory.

## Version check
Checked against the published ICLR 2025 PDF (saved as `3_ai/shi-iclr25-muse-published.pdf`): the abstract and Section 1 statements quoted here appear in the published text.
