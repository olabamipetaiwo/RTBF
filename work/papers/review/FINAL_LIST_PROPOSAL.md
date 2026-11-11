# Final list for Related Work

STATUS: APPROVED by the user on 2026-11-04 as proposed (41 kept, 9 cut). The four dark-pattern papers stay cut; Mathur may be added back if a result needs it. Nothing is in refs.bib yet and no Related Work text is drafted.

Rule in force: papers read only as a preprint or arXiv copy are cited for their general idea only. Figures may be quoted only from papers read in published form. "idea" below marks the papers where that rule applies.

Row numbers are the MANIFEST row numbers. KEEP 41, CUT 9.

## Group 1: Data deletion in computer systems (KEEP 8)
| # | Paper | Role in our paper | Cite as |
|---|---|---|---|
| 16 | Reardon et al., SoK: Secure Data Deletion (S&P 2013) | Defines what deleting data means and how it is checked | published |
| 18 | Geambasu et al., Vanish (USENIX Security 2009) | Deletion by making data unreadable; pages unconfirmed | published, no pages yet |
| 17 | Sarkar et al., Lethe (SIGMOD 2020) | A delete in a database is logical until compaction | published |
| 15 | Shastri et al., GDPR and database systems (PVLDB 2020) | Systems struggle to meet GDPR erasure | published |
| 14 | Garg et al., Formalizing Data Deletion (Eurocrypt 2020) | Formal definition of deletion including derived data | idea |
| 1 | Cao and Yang, Making Systems Forget (S&P 2015) | Origin of "unlearning": forget data and everything derived | published |
| 48 | Politou et al., Forgetting personal data (J. Cybersecurity 2018) | Legal and technical view of erasure | published |
| 49 | Politou et al., Backups and the RtbF (CLSR 2018) | One-month limit, "beyond use", backups | published |

## Group 2: Audits of deployed services (KEEP 8, CUT 1)
| # | Paper | Role | Cite as |
|---|---|---|---|
| 2 | Bertram et al., Five Years of the Right to be Forgotten (CCS 2019) | Search engines and delisting | published |
| 24 | Xue et al., RtBF in the media (PoPETs 2016) | Data-driven study of delisting | published |
| 3 | Habib et al., 150 websites (SOUPS 2019) | Deletion and opt-out choices on websites | published |
| 4 | Rupp et al., Leave No Data Behind (PoPETs 2022) | Deletion requests to websites; compliance | published |
| 5 | Liu et al., Zombie accounts (USENIX Security 2022) | Accounts left active after deletion | published |
| 6 | Yan et al., No Way to Sign Out? (USENIX Security 2025) | Deletion in Google Play apps | published |
| 19 | Santhanam et al., Sticky Leftovers (S&P 2022) | Data left on servers after account deletion | idea |
| 25 | Take, Gallagher et al., people-search sites (PoPETs 2024) | Opt-out and deletion at data brokers | published |
| 26 | Di Martino et al., GDPR right of access (SOUPS 2019) | CUT: about abuse of access requests, not deletion | |

## Group 3: Deletion in AI (KEEP 15, CUT 2)
| # | Paper | Role | Cite as |
|---|---|---|---|
| 7 | Bourtoule et al., Machine Unlearning (S&P 2021) | The standard retraining-based unlearning | idea |
| 33 | Guo et al., Certified Data Removal (ICML 2020) | Provable removal for simple models | published |
| 8 | Chen et al., Unlearning Jeopardizes Privacy (CCS 2021) | Deletion itself leaks information | idea |
| 31 | Xu et al., Machine Unlearning: A Survey (CSUR 2023) | Overview of unlearning | idea |
| 32 | Xue et al., Unlearning verification survey (CSUR 2026) | Verification is the open problem | idea |
| 28 | Thudi et al., Auditable definitions (USENIX Security 2022) | Unlearning cannot be proved from outputs | published |
| 10 | Shi et al., MUSE (ICLR 2025) | Six-way evaluation; privacy leakage after unlearning | published |
| 37 | Patil et al., Can sensitive information be deleted? (ICLR 2024) | Rephrased prompts recover "deleted" facts | published |
| 34 | Pawelczyk et al., In-context unlearning (ICML 2024) | Prompting can mimic forgetting | published |
| 27 | Carlini et al., The Secret Sharer (USENIX Security 2019) | Canary method for planted secrets | published |
| 9 | Carlini et al., Extracting training data (USENIX Security 2021) | LLMs reproduce training data | published |
| 36 | Carlini et al., Quantifying memorization (ICLR 2023) | Memorization grows with model size | published |
| 30 | Lukas et al., PII leakage in language models (S&P 2023) | PII extraction from LMs | idea |
| 46 | Wang et al., MEXTRA agent memory (ACL 2025) | Agent memory can be extracted | published |
| 47 | Park et al., Generative Agents (UIST 2023) | Agent memory with derived reflections | idea |
| 29 | Thudi et al., Unrolling SGD (EuroS&P 2022) | CUT: factors of unlearning, not about deletion or verification | |
| 35 | Li et al., WMDP (ICML 2024) | CUT: about hazardous knowledge, not user data | |

## Group 4: Users (KEEP 10, CUT 6)
| # | Paper | Role | Cite as |
|---|---|---|---|
| 50 | Li et al., Privacy Control in Conversational LLM Platforms (CHI 2026) | Closest prior work (walkthrough; supervisor is co-author) | idea |
| 43 | Chen et al., Relational Gains, Privacy Strains (CHI 2026) | Users doubt ChatGPT memory deletion | published |
| 20 | Malki et al., "Hoovered up" (PoPETs 2025) | Users' expectations of deletion and unlearning | published |
| 23 | Kwesi et al., S&P controls and emotional engagement (USENIX Security 2026) | Users value and doubt deletion controls | published |
| 38 | Zhang et al., "It's a Fair Game" (CHI 2024) | Mental models and disclosure | idea |
| 21 | Minaei et al., Deletion privacy (USENIX Security 2022) | Users judge deletion tools ineffective | published |
| 22 | Rao et al., Mismatched expectations (SOUPS 2016) | Users expect more deletion than sites provide | published |
| 11 | Habib et al., "It's a scavenger hunt" (CHI 2020) | Deletion choices hard to find and use | published |
| 39 | Habib and Cranor, Privacy choice usability (SOUPS 2022) | Usability evaluation covers the user side only | published |
| 40 | Bumiller et al., Too Many Zombies (CHI 2026) | Barriers to deleting accounts | published |
| 13 | Nouwens et al., Dark patterns after the GDPR (CHI 2020) | CUT (peripheral: consent) | |
| 12 | Utz et al., (Un)informed consent (CCS 2019) | CUT (peripheral: consent) | |
| 41 | Mathur et al., Dark patterns at scale (CSCW 2019) | CUT (peripheral: shopping sites) | |
| 42 | Schaub et al., Design space for privacy notices (SOUPS 2015) | CUT (peripheral: notices) | |
| 44 | Leon et al., Why Johnny can't opt out (CHI 2012) | CUT (peripheral: tracking opt-out) | |
| 45 | Gray et al., Dark (patterns) side of UX (CHI 2018) | CUT (peripheral: dark patterns taxonomy) | |

## Counts
Keep: group 1 = 8, group 2 = 8, group 3 = 15, group 4 = 10. Total KEEP = 41. Cut = 9 (Di Martino, Unrolling SGD, WMDP, Nouwens, Utz, Mathur, Schaub, Leon, Gray).
Group 4 keep count: rows 50, 43, 20, 23, 38, 21, 22, 11, 39, 40 = 10.

## Notes for the decision
- A cut paper stays in `papers/review/` as proof of reading. Cutting only means it is not cited.
- If you want one dark-pattern citation, keep Mathur (it measured prevalence), and cut Nouwens, Utz, Gray.
- Li CHI 2026 is cited for its idea only under the preprint rule; its numbers are not to be quoted.
