# Thudi, Deza, Chandrasekaran, Papernot. Unrolling SGD: Understanding Factors Influencing Machine Unlearning

IEEE European Symposium on Security and Privacy (EuroS&P) 2022, DOI via Crossref (checked earlier). File: `3_ai/thudi-eurosp22-unrolling-sgd.pdf` (arXiv v2, 2 March 2022). Read the abstract, introduction, the taxonomy of approximate-unlearning criteria in outline, the definition of verification error, the statement of the unlearning error and the conclusion. I did not read the Taylor-series derivations or the experiments in detail. Check page numbers and wording against the EuroS&P version before quoting.

## Question
Approximate unlearning papers use many different criteria for "forgot". Which single measure covers most of them, and which factors in SGD training make approximate unlearning easier (Abstract)?

## Method
- Taxonomy of approximate-unlearning approaches (logits, weights, and so on) and of the criteria they use: poor performance on the point, membership-inference scores, similar weights to a retrained model.
- Verification error: the L2 difference between the weights of the approximately unlearned model and a naively retrained one. They argue this implies a large class of other metrics.
- Because verification error needs the retrained model (which defeats the purpose), they derive an easy-to-compute proxy, the "unlearning error", from a Taylor expansion of SGD, and a training penalty that limits the total change in weights so that later approximate unlearning has lower error. Experiments on CIFAR-10, CIFAR-100 and IMDB sentiment analysis.

## Findings
- Different unlearning papers measure different things, and these claims cannot be compared directly (Section 1).
- Membership inference is imprecise as a criterion: a method can lower the membership score without having unlearned, and the test can give false positives (Section 3).
- The training penalty reduces unlearning error and hence verification error in their experiments (Section 10).

## Limits the authors state
The strongest limitation of verification error is its cost, since it needs the retrained model; results rest on assumptions about the model, loss and algorithm; image and sentiment classifiers only.

## How it differs from ours
- A theory and method paper on how to make approximate unlearning close to retraining. Its companion paper (Thudi et al., USENIX Security 2022, in this list) later argued that closeness in weights is not a valid proof, so the two should be cited together, with the later paper's correction stated.
- Its remark that a behavioral score such as membership inference can look unlearned without being so is the same limit that applies to our recall test.

## Use in our paper
- Cite, at most briefly, as part of the evidence that there is no agreed measure of "forgot" in machine unlearning. It may be dropped from the final list if space is short, since the companion paper makes the stronger point.
