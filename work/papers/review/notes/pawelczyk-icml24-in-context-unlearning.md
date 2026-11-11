# Pawelczyk, Neel, Lakkaraju. In-Context Unlearning: Language Models as Few-Shot Unlearners

ICML 2024 (PMLR; pages from the manifest, checked earlier). File: `3_ai/pawelczyk-icml24-in-context-unlearning.pdf`. Read the abstract, introduction and contributions, the description of the method (Section 4) in outline, and the evaluation framework (LiRA-Forget, Section 3.2) in outline. I did not read the experiment tables or ablations. Check against the published version before quoting.

## Question
Can an LLM that is accessible only by query be made to behave as if it had unlearned some training points, without updating its parameters (Abstract)?

## Method
- In-Context UnLearning (ICUL): at inference time, add the points to be forgotten to the prompt with labels that differ from the ground truth, plus correctly labelled examples, so that the model's output on those points mimics a model retrained without them (Figure 2).
- Evaluation framework LiRA-Forget: adapts the LiRA membership inference attack to unlearning, comparing a model's behavior on the forgotten points with that of retrained models (Section 3.2).
- Tasks and models: text classification (SST-2, Amazon polarity, AG-News) and question answering, with Bloom (560M to 7.1B) and Llama-2 7B (Figures 3 and 4).

## Findings
- ICUL performs on par with, or in some cases better than, state-of-the-art unlearning methods that need parameter access, while preserving test accuracy (Abstract).
- It can run on a single V100 GPU for a 7B model (Section 1).
- The authors position it as a patch for black-box models "until the model can be updated or a retrained version can be deployed" (Contributions), complementary to white-box methods.

## Limits
Experiments on classification and small question-answering tasks; the deletion happens only for the length of the prompt context, because the underlying model is unchanged; the evaluation reflects membership inference as the measure.

## How it differs from ours
- It makes "unlearning" a matter of what the model is told at inference time. This is close to how many deployed assistants honor a "forget" instruction: they respond as if forgotten while the stored or trained content persists. Our natural-language forget prompts test whether telling an assistant to forget produces that behavior; this paper shows that such behavior can be engineered without any change to the model.
- It does not test deployed products or user-issued instructions.

## Use in our paper
- Cite as the research counterpart of the natural-language forget request: a prompt can mimic unlearning while the weights stay the same, so apparent forgetting from a prompt should not be read as removal. State that the paper is about classification tasks and a controlled setting.
