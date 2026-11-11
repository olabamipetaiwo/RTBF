# Group 5: Gaps (synthesis from the 46 notes read so far)

Synthesis only. No Related Work text is drafted and nothing is added to `refs.bib`. Each gap names the notes it rests on. All 50 papers are now read; Chen, Leon, Gray and Politou were added after this synthesis was first written.

## Gap 1: Deletion is audited in apps and websites, not in LLM assistants
- Audits of deployed services test whether deletion works, but the services are websites and mobile apps: Bertram et al. (CCS 2019), Rupp et al. (PoPETs 2022), Liu et al. (USENIX Security 2022), Yan et al. (USENIX Security 2025), Santhanam et al. (S&P 2022), the people-search study (PoPETs 2024).
- Their figures show deletion often fails or is incomplete: Rupp 24 of 90 non-compliant; Yan 12 of 176 submitted deletion requests failed; Santhanam 17 of 678 apps left data after deletion (preprint numbers).
- No note in groups 1 to 4 reports an audit of an LLM chat assistant's deletion. This must be stated as "none found in the papers we read", not "none exist".

## Gap 2: Deletion in AI is studied inside the model, not as a user-facing action
- Unlearning work (Bourtoule, Guo, Thudi, Shi MUSE, Li WMDP, Patil, Pawelczyk) tests removal from model weights under a researcher-controlled setup. The unit is a training example or a topic, and the trigger is an algorithm, not a user pressing delete.
- Our setting is the reverse: the trigger is the product's own deletion control, and the effect is observed only through the assistant's behavior.
- Chat memory is outside this literature. The memory papers (Park, Wang MEXTRA) study how memory is built and attacked, not whether deleting it works.

## Gap 3: Verification cannot certify deletion, only refute it
- Surveys (Xu 2023, Xue 2026) say behavioral verification is weak; Patil shows that rephrased prompts recover facts that a direct prompt no longer returns; Pawelczyk shows a prompt can imitate forgetting without changing the model.
- This is the basis for our asymmetry: recall failed is evidence that the data is gone from what the assistant can reach, while recall success or can't tell is not proof of retention or removal. No prior paper applies this asymmetry to product-level deletion.

## Gap 4: Users' expectations are measured, never compared with observed behavior of the same products
- Surveys: Malki 2025 (n = 211), Kwesi 2026 (n = 354), Zhang 2024 (19 interviews), Minaei 2022 (n = 191), Rao 2016 (n = 240, against stated policy).
- Rao compares expectations with policy text and states that actual handling "is difficult to assess in practice". Malki and Kwesi report belief and doubt, with no test of the products.
- Our study pairs the documentation, the deletion method and the observed outcome per assistant.
- Chen et al. (CHI 2026, 20 interviews) already report doubts that ChatGPT memory deletion works and one participant's account of a possible failure (P3). So user doubt about memory deletion is studied qualitatively; the gap is that nobody tests it. Say this, not "users' views of memory deletion are unstudied".

## Gap 5: Usability work asks whether a control can be found and used, not whether it works
- Habib 2020 and Habib and Cranor 2022 define usability through finding, understanding and using a choice. Li et al. (CHI 2026, co-authored by the supervisor) is the closest work, using a walkthrough of privacy controls. Their unit is the interface, not the effect.
- Chen CHI 2026 is now read (notes/chen-chi26-relational-gains-privacy-strains.md): 20 interviews on ChatGPT memory. It sits on the user side like Habib and Li, so Gap 5 stands.

## Gap 6: "Leave no trace" including derived data is a definition, with no measurement in products
- Group 1 (Garg, Sarkar Lethe, Geambasu Vanish) gives formal and systems definitions of deletion, including derived data. Park shows agents produce derived "reflections" from memory.
- No note measures whether derived content survives deletion of its source in a deployed assistant. This is also why our synthetic-fact design matters.

## Method precedents we can cite as ours
- Canary and synthetic secrets (Carlini 2019), extraction (Carlini 2021, 2023, Lukas 2023): a planted fact can be searched for later.
- Scraping plus manual checks at scale (Nouwens, Mathur) and walkthroughs (Li) as accepted ways to study deployed interfaces.

## What not to claim
- Not "first" without the sentence "to our knowledge, among the papers we reviewed"; the search covered about 50 papers, not the whole literature.
- Do not use arXiv-copy numbers (Patil, Thudi, Xue 2026, Bourtoule, Carlini 2021) until compared with the published versions.
- Do not repeat the Liu et al. "45 calendar days" GDPR attribution.
