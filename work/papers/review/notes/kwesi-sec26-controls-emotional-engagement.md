# Kwesi, Cao, Cunningham, Emami-Naeini. The Impact of Security and Privacy Controls on Users' Emotional Engagement with Generative AI Chatbots

USENIX Security 2026 (35th Symposium, Baltimore, August 12-14, 2026). Pages 1647-1666, read from the printed numbers on the first and last pages of the PDF. File: `4_users/kwesi-sec26-controls-emotional-engagement.pdf` (USENIX proceedings copy). Read the abstract, introduction, the method outline, the results on skepticism and deletion, the discussion summary and the limitations. I did not read the full statistical models or the coding of each rationale.

## Question
How do the security and privacy controls of chat assistants (deletion, memory toggles, training opt-outs, local-only processing, login) change users' willingness to disclose emotional matters, their sense of protection, and their view of the chatbot's usefulness (Abstract)?

## Method
- Mixed-methods vignette study with 354 US participants recruited on Prolific, all using a GenAI chatbot for emotional or social support at least monthly. Nine S&P controls were drawn from consumer apps as of August to September 2025, among them Delete Conversation, Delete Account & Data, Memory Toggle and a model-training opt-out. Participants rated each vignette on three 7-point questions and gave a free-text rationale (Section 3).

## Findings
- Controls enabling deletion of disclosures had the largest positive effect on willingness to engage, outperforming technically sophisticated controls such as local-only processing and training opt-outs, which participants found hard to understand (Abstract).
- Trust is fragile: 121 participants (34.2%) expressed explicit skepticism that privacy controls would function as promised. On deletion, "I would still wonder if it's actually deleted" (P197). Forty participants both wanted to disclose more and doubted the controls would protect them (Section 4).
- The authors describe the gap as "between interface promise and system behavior that users cannot bridge through inspection" (Discussion): users understood the deletion claim but questioned whether the backend would honor it.

## Limits the authors state
Hypothetical vignettes, which may differ from real decisions under distress; control definitions reflect apps in August to September 2025; US Prolific sample skewing younger, more educated and 65.5% White; excludes non-users and active avoiders (Limitations).

## How it differs from ours
- It measures belief about deletion controls, with no test of the controls. Our study tests the thing these users doubt. Their phrase for what users cannot do ("bridge through inspection") is the gap between what the interface shows and what the backend does.

## Use in our paper
- Cite as the most recent evidence that users doubt chat-assistant deletion controls (34.2%) and value them most. Together with Malki et al. it gives two surveys of LLM users on deletion; ours is the behavioral test. Attribution: this paper is a vignette study of hypothetical controls.
