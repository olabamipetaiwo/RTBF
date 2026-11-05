# Carlini, Liu, Erlingsson, Kos, Song. The Secret Sharer: Evaluating and Testing Unintended Memorization in Neural Networks

USENIX Security 2019 (28th), pp. 267-284. File: `3_ai/carlini-sec19-secret-sharer.pdf` (USENIX proceedings copy; start page 267 and Smart Compose page 273 read from the PDF). Read the abstract, introduction, the definitions of canaries and exposure in outline, the Smart Compose study and the conclusions. I did not read the exposure derivation, the extraction algorithm's search details, or the differential-privacy comparison tables.

## Question
How can a practitioner measure the risk that a model unintentionally memorizes rare or unique training sequences, such as credit card numbers (Abstract)?

## Method
- Insert randomly generated "canary" sequences (a fixed format with random values, for example a number) into the training data, a chosen number of times, and train the model (Section 4). Canaries are named after the canary in a coal mine.
- Exposure metric: how much more likely (in perplexity rank) the model finds the inserted canary compared with other possible random values. High exposure means the inserted secret has been memorized.
- An extraction algorithm guided by exposure retrieves secret sequences, shown on a model trained on the Enron email data to extract credit card numbers.
- Applied at scale to Google's Smart Compose, trained on the emails of millions of users (Section 8).

## Findings
- Unintended memorization is "commonplace and hard to prevent": it begins early in training, appears across model types and strategies, and is not caused by overtraining; early stopping and dropout do not prevent it; only differentially private training removes it, at some cost in utility (Introduction).
- Smart Compose: canaries inserted from 1 to 10,000 times in training on over a billion sequences. For very rare canaries (one in a billion) the exposure was negligible; at 10,000 insertions the model produced the canary about 1,000 times more often than a random phrase (exposure 10), still not enough for the extraction attack to find it (Figure 4).
- The authors used the test to limit information drawn from any small set of users (Section 8).

## Limits the authors state
Exposure is a measure for planted sequences that cannot be applied after the fact to real secrets; measured exposure is lower for models trained with huge corpora seen for few epochs; the extraction results depend on model and training choices.

## How it differs from ours
- It plants random secrets in the training data and later checks whether the model has them. We plant synthetic facts in chat with deployed assistants and later check whether the assistant repeats them after a deletion request. The method is the same family: a random, unique, checkable string that cannot be there by chance.

## Use in our paper
- Cite as the origin of the canary approach to measuring memorization, to support our use of synthetic facts: a planted fact is the only way to know that what we find came from our own input.
- Accurate scope: this paper studies models trained on the data, not chat history or memory features.
