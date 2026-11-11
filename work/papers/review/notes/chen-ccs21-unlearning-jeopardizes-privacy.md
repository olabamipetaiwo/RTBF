# Chen, Zhang, Wang, Backes, Humbert, Zhang. When Machine Unlearning Jeopardizes Privacy

ACM CCS 2021, pp. 896-911 (pages from the manifest, checked against Crossref earlier). File: `3_ai/chen-ccs21-unlearning-jeopardizes-privacy.pdf` (arXiv v2, 14 September 2021, "To appear in CCS 2021"). Read the abstract, introduction and contributions, the threat setting and datasets in outline, and the main results summary. I did not read the full attack feature-construction ablations or the multi-sample and online-learning sections line by line.

## Question
Does unlearning leave a trace of the deleted sample, so that the act of unlearning creates a new privacy risk for it (Abstract, Section 1)?

## Method
- Black-box setting: the attacker can query both the original model and the unlearned model (the model after the target sample was removed, for example by retraining without it).
- A membership inference attack that uses both models' output vectors, combined by concatenation (better for overfitted models) or by difference (better for well-generalised models), to decide whether the target sample was in the original training set but not in the unlearned one.
- Two new metrics: Degradation Count (share of cases where confidence is higher with the new attack than with classical membership inference) and Degradation Rate (average confidence increase).
- Models from logistic regression and decision trees to convolutional networks (ResNet50, DenseNet), on categorical datasets (for example Adult) and images (MNIST, CIFAR10).

## Findings
- The attack often beats classical membership inference on the original model, so unlearning "can have counterproductive effects on privacy" (Abstract).
- The effect is largest for well-generalised models, where classical inference is near chance: on a decision-tree classifier the classical AUC is about 0.5, against 0.89 for the new attack, with Degradation Count 0.85 and Degradation Rate 0.28 (Section 1).
- It also works with several intermediate unlearned models, with group deletion, and in online learning where samples are added and deleted together.
- Mitigations: releasing only the predicted label, temperature scaling, and differential privacy work; publishing top-k confidence values, even top-1, does not stop it (Section 1).

## Limits the authors state
Classification models only, not generative language models; assumes the attacker can query both versions of the model. A related study they cite (Brockschmidt et al.) shows similar leakage for language models and data deletion.

## How it differs from ours
- It is an attack on classifiers built by the researchers; ours is a test of deployed assistants through their chat interface.
- Its message for us is conceptual: a deletion event itself produces an observable difference, and comparison before and after deletion can reveal what was deleted. Our design compares recall before and after a deletion request, with the benign aim of checking whether the data went.

## Use in our paper
- Cite as evidence that unlearning is not privacy-neutral: "forgetting" can leave an imprint that a before-and-after comparison exposes. Careful wording: this is shown for classifiers, so do not say it holds for language-model assistants.
