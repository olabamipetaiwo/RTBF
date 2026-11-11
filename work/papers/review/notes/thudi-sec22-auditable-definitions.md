# Thudi, Jia, Shumailov, Papernot. On the Necessity of Auditable Algorithmic Definitions for Machine Unlearning

USENIX Security 2022 (31st), venue confirmed earlier on usenix.org (this is the paper I first mistook for "Unrolling SGD"). File: `3_ai/thudi-sec22-auditable-definitions.pdf` (arXiv v2, 19 February 2022, header "In 31st USENIX Security Symposium"). Read the abstract, introduction and the statement of the main claims. I did not read the formal definition of forgeability, the proofs, or the experiments in detail. Check page numbers and the final wording against the USENIX version before quoting.

## Question
Can unlearning be defined and proven by looking at the resulting model's parameters, and how can anyone verify that exact unlearning was actually carried out (Abstract)?

## Argument and method
- Approximate unlearning defines success as the unlearned model being close in parameter space to a model retrained without the data. The authors show this is wrong: nearly identical parameters can come from non-overlapping datasets, because training value comes from the trajectory of gradient steps, and different minibatches can give the same average gradient (Section 1).
- Forgeability: two datasets are forgeable if points of one can replace points of the other while keeping the model updates the same up to a small error. If the dataset with the points removed is forgeable with the original, "unlearning can be achieved at no cost", since the model does not change at all. They show this is possible for standard models and datasets (Section 1).
- Even for exact unlearning, one cannot formally prove from a training trajectory that certain points were absent.

## Findings and conclusion
- "Unlearning is only well-defined at the algorithmic level": the only auditable claim a model owner can make is that it ran a particular algorithm designed for external scrutiny (Abstract).
- Approximate approaches can justify unlearning only by the process, not by the final model; the authors propose verifiable computation as a direction (Section 1). This parallels Dwork et al.'s point that privacy guarantees belong to algorithms, not datasets.

## Limits
Supervised classification setting, not language models; it argues that proof from outputs is impossible, not that unlearning algorithms fail.

## How it differs from ours
- It is a theory-and-experiment argument about verification of unlearning claims. We test behavior, which this paper would count as insufficient to prove absence. That agrees with our reporting: recall failed shows deletion failed, but recall success does not prove deletion, so "can't tell" stays a separate count.

## Use in our paper
- Cite for the claim that outputs or parameters alone cannot prove a model forgot, so an outside check of behavior can refute a deletion but not certify it. It supports the asymmetry in our design. Together with Garg et al. (impossible in general for a user to prove deletion) and Xue et al. (CSUR 2026, verification survey).

## Version check
Checked against the USENIX PDF (saved as `3_ai/thudi-sec22-auditable-definitions-published.pdf`): pages 4007-4022 from the printed numbers, and the quoted conclusions appear in the published text.
