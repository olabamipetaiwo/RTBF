# Bourtoule, Chandrasekaran, Choquette-Choo, Jia, Travers, Zhang, Lie, Papernot. Machine Unlearning

IEEE Symposium on Security and Privacy (S&P) 2021, DOI 10.1109/SP40001.2021.00019. File: `3_ai/bourtoule-sp21-machine-unlearning.pdf` (arXiv v3, December 2020; the header says it appeared in the 42nd IEEE S&P). Read the abstract, introduction, the definition, SISA training in outline, the headline results and the discussion section on verified unlearning. I did not read the analytical derivations of the speed-ups or the appendices.

## Question
Can a trained model "unlearn" a user's data efficiently, with a guarantee strong enough for the right to be forgotten, without retraining from scratch (Abstract, Section I)?

## Definition and method
- Definition: unlearning must give the same distribution of models as never training on the point at all. The authors say this is stricter than differential privacy, because differential privacy bounds a point's contribution but keeps it above zero, while forgetting needs zero contribution (Section I).
- SISA training (Sharded, Isolated, Sliced, Aggregated): split the training data into shards, train an isolated model on each, slice each shard's data and checkpoint the model between slices, and aggregate the shard models' outputs. An unlearning request retrains only the affected shard from the slice before the point was added.
- A refined variant uses prior knowledge of which users are likely to ask for deletion.

## Findings
- Speed-up over retraining from scratch (no assumption on request distribution): 4.63 times on the Purchase dataset, 2.45 times on SVHN, 1.36 times on ImageNet with a small accuracy loss of about 2 percentage points when combined with transfer learning (Abstract, Section I).
- Sharding gives speed-up only when the number of requests is below about three times the number of shards; for complex tasks more shards reduce accuracy; slicing always helps (Section I).
- The authors state their request counts are three orders of magnitude above earlier work, and argue the approach handles more requests than Google reported expecting for the right to be forgotten.

## Limits the authors state
- Verification: "We assume that the service provider performs unlearning in an honest manner." The guarantee holds if the data owner trusts the provider; a regulator could audit the code. "There is no way to measure the influence of a data point on the model parameters", and these models are often proprietary, so whether unlearning can be verified is left open (Verified Unlearning paragraph, Discussion).
- Designed for stateful training such as SGD on deep networks; the framework does not address unlearning used to mitigate poisoning (Section I).

## How it differs from ours
- It is an algorithm run by the model owner on the training set. Deployed chat agents train in the background on data we cannot see, and the deletion we test is a request through an interface; nothing in this paper says whether any provider uses SISA or any similar method.
- The point we can use: the authors say a user cannot verify unlearning from outside. Our recall check is one external signal, and it cannot test the model's parameters.

## Use in our paper
- Cite as the standard exact-unlearning reference and for the definition (a model with the data unlearned equals a model never trained on it). Pair with Xue et al. (CSUR 2026) on verification, and Chen et al. (CCS 2021), who show unlearning itself can leak information.
- The "honest provider" assumption appears in Garg et al. too; both say the verification problem is unresolved.
