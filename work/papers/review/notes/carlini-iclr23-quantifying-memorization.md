# Carlini, Ippolito, Jagielski, Lee, Tramèr, Zhang. Quantifying Memorization Across Neural Language Models

ICLR 2023 ("Published as a conference paper at ICLR 2023" in the PDF header; arXiv v3, 6 March 2023). File: `3_ai/carlini-iclr23-quantifying-memorization.pdf`. Read the abstract, introduction, related work and the definition of extractability. I did not read the experiment sections on dataset subsets, the model-family comparison or the mitigation discussion in full.

## Question
How much of a language model's training data can be extracted, and what controls the amount (Abstract)?

## Method
- Definition 3.1: a string s is extractable with k tokens of context from model f if some training sequence is [prefix p of length k || s] and f, prompted with p under greedy decoding, outputs s. Example in the paper: given the prefix "My phone number is", the model outputs "555-6789".
- Experiments feed prefixes of sequences taken from each model's own training set and check whether the model completes them verbatim, across three model families (GPT-Neo is the main one) and their training sets (The Pile for GPT-Neo and GPT-J). Having the training set allows tighter bounds than earlier attacks (Section 1).

## Findings (three log-linear relationships, Abstract and Section 1)
- Model scale: larger models within a family memorize 2 to 5 times more than smaller ones.
- Duplication: examples repeated more often in training data are more likely to be extractable.
- Context: extraction is orders of magnitude easier with longer prompts.
- GPT-J (6 billion parameters) memorizes at least 1% of The Pile, against the earlier estimate of 600 sequences found in GPT-2 (Section 1).
- Across model families the picture is more complicated than the single trend.
- The authors conclude that memorization "is more prevalent than previously believed and will likely get worse as models continue to scale, at least without active mitigations".

## Limits the authors state
Measures only verbatim extractability under greedy decoding; requires access to the training data; results depend on the model family.

## How it differs from ours
- Same relation to our work as Carlini et al. (2021): it shows content can sit in weights and come out when prompted. Context length matters here, and in our recall tests we give the assistant a short cue about the planted fact, which may matter for whether it comes back.

## Use in our paper
- Cite with Carlini et al. 2019 and 2021 for the memorization line of work: extractable training data grows with scale, duplication and context. Do not read it as showing that chat inputs become training data.
