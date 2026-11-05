# Carlini, Tramèr, Wallace, Jagielski, Herbert-Voss, Lee, Roberts, Brown, Song, Erlingsson, Oprea, Raffel. Extracting Training Data from Large Language Models

USENIX Security 2021 (30th), pp. 2633-2650 (start page 2633 read from the PDF; end page to confirm on usenix.org). File: `3_ai/carlini-sec21-extracting-training-data.pdf` (USENIX proceedings copy). Read the abstract, introduction, the definition of memorization, the headline results, the memorization-versus-model-size findings, and the lessons and conclusion. I did not read the attack's metric ablations or the categories table of extracted content line by line.

## Question
Can an attacker with only black-box query access recover individual training examples from a large language model, even though such models show little overfitting (Abstract, Section 1)?

## Method
- Target: GPT-2 (largest model 1.5 billion parameters), chosen because the model and its training data source are public, which limits harm (Section 1).
- Generate a large, diverse set of high-likelihood samples with three sampling strategies, then rank them with six membership metrics that compare the target model to a reference model or to a compression measure (zlib entropy). Manually check the top candidates against the training data, with the GPT-2 creators' help.
- Definition (Definition 2): a string is k-eidetic memorized if the model can produce it and it appears in at most k training examples (for GPT-2, one web page is one example).

## Findings
- 1,800 candidates (100 per each of 3 x 6 configurations); over 600 were verbatim training data; best configuration 67% precision. Content included names, phone and fax numbers, email addresses, IRC conversations, code and 128-bit UUIDs (Abstract, Section 1).
- Extraction worked for sequences that appeared in only one document; among 600,000 ordinary generated samples at least 604 (0.1%) contained memorized text, which the authors call a loose lower bound (Lessons).
- Larger models memorize more: the largest model memorized over 18 times as much as the 124-million-parameter model; for the largest model complete memorization occurred after as few as 33 insertions (Section 7).
- Memorization does not need overfitting: there is almost no train-test gap, yet some examples have anomalously low loss.
- The authors discuss mitigations (differentially private training, vetting data, limiting downstream impact, auditing for memorization) and say each is incomplete.

## Limits the authors state
Attack on one model family with a manual verification step; discovery depends on prompt prefixes; the 600,000-sample figure is a lower bound.

## How it differs from ours
- It shows that content can sit inside model weights and be recovered by prompting, which is a mechanism for post-deletion recall that no interface-level deletion would remove. We do not test training-data memorization: our synthetic facts enter through conversation, and our check is whether the assistant repeats them after deletion.

## Use in our paper
- Cite for the background claim that deployed language models can reproduce data they were trained on, so deletion from a user-facing store does not touch data inside weights. Pair with Carlini et al. (2019, 2023) and Lukas et al. (2023) on PII.
- Wording care: "training data" here means pre-training web text, not user chats. Whether providers train on user conversations is a different question that this paper does not address.
