# Malki, Polamarasetty, Warner, Costanza. "Hoovered up as a data point": Exploring Privacy Behaviours, Awareness, and Concerns Among UK Users of LLM-based Conversational Agents

PoPETs 2025(4), pp. 838-860 (from the PDF header). File: `4_users/malki-popets25-hoovered-up.pdf` (PoPETs copy). The first-page extraction scrambled the author affiliations, so check the author list against the proceedings before citing. Read the abstract, introduction and research questions, the method in outline, the behaviour and awareness results, the deletion-expectation results (Table 3), the discussion and the limitations. I skimmed the demographic regressions and the open-text coding.

## Question
How do UK users of LLM chat assistants protect their privacy, what do they know and fear, and what do they expect from deletion, retention and opt-out (Abstract, RQ1 to RQ4)?

## Method
- Online survey of 211 UK adult users of LLM-based conversational agents recruited on Prolific (221 completed after a screener of 375). Questions on eight privacy behaviours, awareness of features, self-disclosure boundaries, concern, and expectations of deletion and model-training opt-out shown through mockups of three features: opting out of model training, deleting all chats, deleting the account (Section 3). Pilot with 15 people. Free-text answers analysed qualitatively (151 usable).

## Findings
- Protective behaviour was low: the most common was deleting or clearing chat history (31.3%, n = 66), then removing sensitive information from prompts (27.0%, n = 57); only 15 participants (7.1%) had opted out of model training (Section 4).
- Awareness: 49.3% (n = 105) knew they could delete chat history; 28.9% (n = 61) knew they could opt out of training; of those aware of the opt-out, 41 of 61 had not used it.
- Expectations of deletion (Table 3, read from the rendered table, p. 846): almost all assumed they would immediately lose access to chats (90.0%) and accounts (87.7%) and that the data would be permanently deleted (chat history 76.4% immediately, 11.8% within days; account data 67.3% immediately, 16.6% within days). For "patterns that the model has learned from my data will be removed from the model", 31.8% expected it immediately and 11.4% within days after chat deletion (43.2% together), and 33.1% and 12.8% after account deletion (45.9% together); 47.4% (chat) and 46.0% (account) expected it never.
- The authors conclude that "many participants held inaccurate beliefs about the effects of deleting data and opting out of model training" and "believed that information could be retroactively unlearned from the model" (Abstract, Section 1).
- Participants also reported knowledge gaps about "whether data deletion was effective" and feelings of privacy cynicism.

## Limits the authors state
Prolific sample, mostly university-educated ChatGPT users; self-reports; the mockups cover three features, not every platform's implementation.

## How it differs from ours
- Malki et al. measure what users expect and believe. They did not test what the products do. This is the user-expectation half of the picture that our work sets against observed outcomes: a user who expects data to be gone within days and out of the model can be wrong in either direction.
- Reading note: the text extraction lost Table 3's column headings and I first misread 47.4% as an expectation of unlearning; the rendered table shows it is the share who expected it never. Quote "about 43% to 46% expected unlearning immediately or within days" or the exact cells, not "almost half expected unlearning" alone.

## Use in our paper
- Cite as the most direct prior survey of expectations for deletion in LLM chat assistants, and quote the concrete figures (7.1% opted out; about 43% to 46% expected the model to unlearn immediately or within days, while 46% to 47% expected it never). Combine with Zhang et al. (CHI 2024) and Chen et al. (CHI 2026) in the "users" paragraph. Our contribution is to compare such expectations with what deletion actually does.
