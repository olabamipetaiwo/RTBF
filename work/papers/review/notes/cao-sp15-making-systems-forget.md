# Cao and Yang. Towards Making Systems Forget with Machine Unlearning

IEEE S&P 2015, pp. 463-480, DOI 10.1109/SP.2015.35. File: `1_systems/cao-sp15-making-systems-forget.pdf` (S&P archive copy). Read the abstract, introduction, background, overview, approach, evaluation summary, discussion, related work and conclusion. I did not work through the four case-study sections (VI to IX) line by line; I took their results from Table I and the introduction.

## Question
How can a system make a learning component forget a user's data, and everything derived from it (the data's "lineage"), completely and quickly (Abstract, Section I)?

## Argument and method
- Defines "forgetting systems" with two goals: completeness (the unlearned system behaves as one retrained without the data) and timeliness (faster than retraining) (Section III-A).
- Reasons users want forgetting: privacy (users deleted accounts after a Facebook policy change; Google removed 171,183 links by October 2014 under the right to be forgotten), security (polluted training data), usability (a recommendation keeps showing a TV show after the search record was deleted) (Section I-A).
- Approach: rewrite a learning algorithm in "summation form" (statistical query learning) so that forgetting a sample means subtracting it from a few stored sums and recomputing the model (Section IV). Covers feature selection and model training.
- Evaluated on four systems: LensKit (recommender), a re-implementation of Zozzle (JavaScript malware detector), an online social network spam filter, PJScan (PDF malware detector), with real workloads such as more than 100K malware samples from Huawei (Sections I-C, V).

## Findings
- Completeness: for LensKit, ten repeated runs gave identical recommendations after unlearning and after retraining, and the largest similarity difference was below 1.0 x 10^-6 (floating point). A published inference attack gained nothing after unlearning (Section VI-C).
- Timeliness: Zozzle retraining takes over a day on the Huawei data, while unlearning takes less than a second (Section I-B). LensKit unlearning took 45 s against 4 min 56 s for retraining, a 6.57 times speedup in Table I.
- Ease of use: 20 to 300 lines of code changed per system, under 1% of each system (Section I-C); LensKit needed 302 lines (0.3%).

## Limits the authors state
- Forgetting does not protect the data that remains, and identifying which samples to forget is a separate problem (Section X).
- Unlearning does not replace retraining; it is better when the data to forget is small relative to the training set (Section III-A).

## How it differs from ours
- It is about classical machine learning models, not LLM agents. It treats forgetting as a property that can be checked against a retrained model. Our agents are black boxes, so we cannot retrain; we test from outside.
- Its motivation matches our setting: users want data forgotten for privacy, and "lineage" (derived data in memory, summaries) is the same concern as memory snippets derived from conversations.

## Use in our paper
- Origin of the term unlearning and of the completeness idea: deleting from a store is not the same as removing the data's effects on derived state. Fits Related Work, group "Data deletion in computer systems", as the root of the unlearning line.
- Quote candidate for the lineage point: the data "creeps into many places and appearing in many forms" (Section I-A).
