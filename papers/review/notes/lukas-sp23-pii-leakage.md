# Lukas, Salem, Sim, Tople, Wutschitz, Zanella-Béguelin. Analyzing Leakage of Personally Identifiable Information in Language Models

IEEE Symposium on Security and Privacy (S&P) 2023 (cited in the PDF as "the full publication in IEEE S&P 2023"). File: `3_ai/lukas-sp23-pii-leakage.pdf` (arXiv v4, 23 April 2023). Read the abstract, introduction and the figure that defines the three attacks. I did not read the game-based definitions in detail or the per-dataset results tables. Check numbers against the S&P version before quoting; the page range is in the manifest from Crossref.

## Question
Does scrubbing personally identifiable information (PII) from training data, or training with differential privacy, stop a language model from leaking PII (Abstract)?

## Method
- Three game-based definitions of PII leakage with only API access to the model: extraction (generate text and pull out PII), reconstruction (given a sentence with the PII masked, rank candidate fillers), and inference (decide which of a candidate set of PII items appeared in the training data) (Figure 1).
- GPT-2 models fine-tuned in three domains (case law, health care, emails), with and without scrubbing and with sentence-level differential privacy.

## Findings
- New attacks extract up to 10 times more PII sequences than existing attacks (Abstract).
- Scrubbing "reduce[s] but do[es] not prevent" leakage, because scrubbing is imperfect and trades off against data utility.
- Sentence-level differential privacy reduces PII disclosure but still leaks about 3% of PII sequences (Abstract).
- The authors report a connection between record-level membership inference and PII reconstruction.
- Context from the introduction: attackers with black-box API access can extract at least 1% of the training data of some models (citing Carlini et al.).

## Limits the authors state
GPT-2-scale models fine-tuned on three datasets; leakage is measured against the PII the training set contains and the scrubber's definition of PII.

## How it differs from ours
- It looks at leakage of personal data from fine-tuned models through black-box queries, which is the same access an end user has to a hosted assistant. Our probe is simpler (ask for a fact the user supplied) and is aimed at a deletion event.

## Use in our paper
- Cite, with Carlini et al., for the claim that language models can leak personal data through the API and that removing PII from the data before training is not a full defence. Do not extend its figures to commercial assistants.
