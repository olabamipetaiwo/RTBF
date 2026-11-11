# Li, Pan, Gopal, Yue, Berrios, Gatti, Li, Dombrowski, Goel, Mukobi, and others (including Hendrycks). The WMDP Benchmark: Measuring and Reducing Malicious Use With Unlearning

ICML 2024, PMLR 235 (pages from the manifest, checked earlier). File: `3_ai/li-icml24-wmdp.pdf`. Read the abstract, introduction, the RMU summary, the experimental setup in outline and the stated limitations (Appendix D.1). I did not read the question-construction process, the full result tables or the robustness analyses. This paper is about unlearning dangerous knowledge, not personal data, so I kept it to the points that bear on unlearning evaluation.

## Question
Can hazardous knowledge (biosecurity, cybersecurity, chemical security) be measured with a public benchmark and removed from a language model by unlearning, with general capabilities kept (Abstract)?

## Method
- WMDP: 3,668 multiple-choice questions, developed by academics and consultants at a reported cost of more than $200K, as a proxy for hazardous knowledge (Section 3).
- RMU (Representation Misdirection for Unlearning): fine-tune the model so activations on hazardous text are perturbed in a random direction while activations on benign text are preserved; the loss is computed on one layer and gradients updated on the layers before it to save memory (Section 4).
- Unlearning experiments on Zephyr-7B-beta, Yi-34B-Chat and Mixtral-8x7B-Instruct, with MMLU and MT-Bench as measures of general capability (Section 5.1).

## Findings
- RMU significantly reduces WMDP accuracy while mostly keeping MMLU and MT-Bench performance (Section 1); the authors report that the unlearned knowledge could not be recovered by linear probes or adversarial attacks (Sections 5.2 and 5.3).
- The authors say RMU "markedly improves upon existing baselines, but future work is necessary to improve the precision of unlearning while fully maintaining general capabilities" (Section 5).

## Limits the authors state (Appendix D.1)
- Multiple-choice tests of retained knowledge do not test whether a model would reveal the information helpfully during an attack, and memorized facts can inflate scores.
- The benchmark is static, so "benchmarking on only WMDP may yield a false sense of model safety after unlearning".
- It addresses API-access models only; for models with downloadable weights "unlearned information can be trivially re-introduced by malicious actors" (citing Lynch et al., 2024).

## How it differs from ours
- It unlearns topics from open-weight models and measures answers to multiple-choice questions; ours deletes user-supplied facts in deployed products and measures recall.
- The quoted limit applies to us too: a measure of retained knowledge can understate or overstate removal, which is why we report can't tell separately.

## Use in our paper
- Cite once as a recent example of LLM unlearning evaluated on question accuracy, and for the authors' own warning that a score after unlearning can give "a false sense" of removal. If the final list needs trimming, this is a candidate to drop: its topic (hazardous knowledge) is far from personal data deletion.
