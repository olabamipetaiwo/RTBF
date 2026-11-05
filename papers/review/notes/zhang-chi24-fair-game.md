# Zhang, Jia, Lee, Yao, Das, Lerner, Wang, Li. "It's a Fair Game", or Is It? Examining How Users Navigate Disclosure Risks and Benefits When Using LLM-Based Conversational Agents

ACM CHI 2024 (Honolulu, May 11-16, 2024). File: `4_users/zhang-chi24-fair-game.pdf` (arXiv v2, 2 April 2024). Read the abstract, introduction, the research questions, the method for both studies, the summary of findings and the dataset limitations. I did not read the typology tables, the full quotations or the design guidelines. Check the final published wording before quoting.

## Question
What sensitive information do people disclose in real ChatGPT conversations, why, and how aware and equipped are they to protect their privacy (RQ1 to RQ3, Section 1)?

## Method
- Study 1: qualitative analysis of 200 sessions (10,380 messages) from the ShareGPT52K dataset, 50,496 ChatGPT histories shared by users of a Chrome extension between December 2022 and March 2023; PII removed and no verbatim quotes (Section 3).
- Study 2: semi-structured interviews with 19 users of LLM-based conversational agents (18 ChatGPT users and one other), recruited from Prolific and the authors' networks, July to August 2023, interviewed until saturation (Section 4).

## Findings
- Users disclosed many kinds of PII, including other people's data, and some conversations gradually elicited more sensitive information at the assistant's request (Study 1).
- Users face constant trade-offs between privacy, utility and convenience; many held the pessimistic view "You can't have it both ways" (P9, P19); almost every participant used ad-hoc protective measures (Study 2).
- Erroneous mental models of how responses are generated and how services improve limited users' ability to reason about risk; most participants did not know they could opt out of having ChatGPT use their data for training; ChatGPT's opt-out interface included dark patterns that tie privacy to loss of utility (Section 1).
- Human-like interaction encouraged more disclosure. The authors conclude the "fair game" some participants described "is far from fair".

## Limits the authors state
Shared conversations may not be representative (users who chose to share them); limited context for each disclosure; small interview sample; findings reflect ChatGPT in 2023 (Sections 3.1.4 and 4).

## How it differs from ours
- Studies what users disclose and believe, before any deletion. It documents the mental-model problem that would also affect deletion expectations. It does not test deletion.

## Use in our paper
- Cite for real-world disclosure to chat assistants and for users' incorrect mental models and limited awareness of controls, which sets up why deletion expectations matter. Pair with Malki et al. (2025), which measures awareness and expectations on a larger sample.
