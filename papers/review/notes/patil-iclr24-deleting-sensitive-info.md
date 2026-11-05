# Patil, Hase, Bansal. Can Sensitive Information Be Deleted From LLMs? Objectives for Defending Against Extraction Attacks

ICLR 2024 (venue confirmed earlier on the iclr.cc page). File: `3_ai/patil-iclr24-deleting-sensitive-info.pdf`. **This PDF is arXiv v1 (29 September 2023), not the ICLR 2024 version.** The figures below (38%, 29%, 2.4%) come from v1; check them against the ICLR version before quoting. Read the abstract, introduction and the summary of attacks, defenses and findings. I did not read the threat-model details, the experiment tables, or the defense objectives' derivations.

## Question
Can specific sensitive facts be deleted directly from a language model's weights so that extraction attacks cannot recover them (Abstract)?

## Method
- Threat model: an attack succeeds if the answer to a sensitive question appears among B generated candidates (B = 20 in the headline numbers), reflecting settings where information is insecure if it is among B candidates (Section 3).
- Model editing (ROME and related methods) applied to GPT-J to delete chosen facts.
- Whitebox attack: read candidate answers out of the model's intermediate hidden states using interpretability tools.
- Blackbox attack: automatic input rephrasing; sample outputs for many paraphrases of the question, which exploits the editing method's non-zero error rate on rephrasings.
- Defenses: new objectives that also remove the answer from intermediate representations.

## Findings
- Even state-of-the-art editing "struggle[s] to truly delete factual information": the whitebox attack recovered the deleted answer 38% of the time and the blackbox rephrasing attack 29% of the time at B = 20 (Abstract, Section 1).
- Two observations behind the attacks: traces of deleted information remain in intermediate hidden states, and an edit for one phrasing of a question may not carry over to rephrased versions (Abstract).
- A new defense lowers whitebox success from 38% to 2.4%, but it does worse against attacks it was not designed for, including the paraphrasing attack; the authors "do not find a single universally effective defense method".
- They argue even low success rates matter when individuals have ownership of their personal data (Abstract).
- RLHF-style suppression is the usual approach to removing sensitive information from outputs, but it only hides it (introduction).

## Limits
Factual question answering on GPT-J-scale models; edits applied to single facts; the threat model assumes the attacker knows the question.

## How it differs from ours
- Deletion by weight editing on an open model with access to its states. We cannot see inside deployed products. The blackbox attack is the nearest match: asking for the same fact in rephrased ways after a deletion, which is also how we word several recall probes.
- Their finding that deletion can hold for one phrasing and fail for another suggests that one probe that fails to recall a fact is weak evidence of deletion. That bears on our "can't tell" count and on using several probe forms per fact.

## Use in our paper
- Cite as direct evidence from LLM research that a deleted fact can resurface under a different question or via internal states, and as support for using multiple recall prompts per fact. Use the ICLR version's numbers.

## Version check
Checked against the published ICLR 2024 PDF (saved as `3_ai/patil-iclr24-deleting-sensitive-info-published.pdf`): the 38%, 29%, 2.4% and B = 20 figures are the same there, so they can be quoted from the published paper.
