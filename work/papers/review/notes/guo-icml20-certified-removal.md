# Guo, Goldstein, Hannun, van der Maaten. Certified Data Removal from Machine Learning Models

ICML 2020, PMLR 119, pp. 3832-3842 (from the manifest; checked against the PMLR page earlier). File: `3_ai/guo-icml20-certified-removal.pdf`. Read the abstract, introduction, the definition of certified removal (Section 2), the outline of the linear mechanism (Section 3.1) and the discussion of non-linear models (Section 3.3). I did not read the proofs, the batch-removal analysis or the experiments in detail.

## Question
Can data be removed from a trained model without retraining so that the result cannot be told apart from a model that never saw the data (Abstract)?

## Definition and method
- Certified removal: a removal mechanism M is epsilon-certified if, for every set of models T, every dataset and every removed point, the probability that the modified model lies in T is within a factor e^(-epsilon) to e^(epsilon) of the probability for a model trained without that point (Equation 1). The definition is inspired by differential privacy and bounds the max-divergence between the two models.
- Mechanism for L2-regularized linear models with differentiable convex loss (for example logistic regression): a Newton step on the parameters largely removes the point's influence; the leftover error shrinks quadratically with training set size; the residual is masked by randomly perturbing the training loss (Section 3.1).
- Non-linear models: certified removal applies only to a linear layer on top of features from a public pretrained extractor or a differentially private extractor. For example, language models pretrained on public text can be used as extractors (Section 3.3).

## Findings
- The mechanism is practical in some settings, with removal cost on the order of d^3 at removal time (inverting a d-by-d matrix) (Section 3.1).
- The authors emphasize that certified removal is "a very strong notion of removal; in practical applications, less constraining notions may equally fulfill the data owner's expectation of removal".
- It guarantees that membership-inference attacks (Yeom et al., Carlini et al.) fail on removed data.

## Limits the authors state
Guarantees cover convex linear models and extractors that never saw the removed data; deep networks need the extractor to be public or private; many removals accumulate error and require retraining after some point.

## How it differs from ours
- A provable guarantee on small models, not an audit of deployed ones. The paper marks the distance between what can be proved (linear, public features) and what products do (large fine-tuned, closed models).

## Use in our paper
- Cite, with Bourtoule et al., as one of the two foundational definitions (exact via SISA, certified via a differential-privacy-style bound). The remark that weaker notions may satisfy owners is relevant to why users judge deletion by what they can see.
