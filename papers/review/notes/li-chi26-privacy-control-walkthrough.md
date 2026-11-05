# Li, Wu, Li, Gui, Luo. Privacy Control in Conversational LLM Platforms: A Walkthrough Study

CHI 2026, 26 pages, DOI 10.1145/3772318.3791054. File: `4_users/li-chi26-privacy-control-walkthrough.pdf` (arXiv v1 copy, Feb 2026). Read in full, including Method, Findings, Discussion and Limitations. Page references use the paper's section, table and figure numbers.

Authors' affiliations: Zhuoyang Li (Eindhoven), Yanlai Wu and Yao Li (University of Central Florida, yao.li@ucf.edu), Xinning Gui (Penn State), Yuhan Luo (City University of Hong Kong). Two authors are at UCF; check whether Yao Li is the same Yao Li whose 2026-10-07 decisions shaped our statistics.

## Question
How do conversational LLM platforms govern data practices and give users controls to manage their data (Section 1)? The aim is the interface level: what an end user can see and do.

## Method
- Application walkthrough (Light et al.), an expert-driven inspection of features. The authors state it is not a cognitive walkthrough, which examines how a first-time user carries out tasks (footnote 1, Section 3.1).
- Platform selection (Sections 3.2.1 to 3.2.3): searched Google, Bing and Yahoo for LLMs (top 30, 20 and 20 results; period Nov 2022 to Jun 2024) and extracted 310 LLMs. Excluded 196 non-commercial models and 47 not built by U.S.-headquartered organizations, leaving 58 models traced to 9 platforms. Screening criteria (conversational interface, general-purpose, widely used with a reported user base) removed Replika, Goody-2 and Wordtune. Final six: Character.ai, ChatGPT, Claude, Gemini, Meta AI, Pi (Table 1). Individual-use versions only.
- Walkthrough window: Nov 19 2024 to Jan 2 2025, platform by platform (Table 1). Each platform was inspected signed out, signed in unpaid, and signed in paid; a second account was used to inspect shared content (Section 3.3.2).
- Steps: boarding page, conversation interface (short neutral stimuli such as "My name is Johnny. I am an HCI researcher" and "Remember..." to trigger memory), chat history side panel, customization panel, settings page, other controls, logout after deleting data (Section 3.3.2).
- Data: screenshots and field notes, ChatGPT 95, Character.ai 49, Claude 38, Gemini 33, Meta AI 17, Pi 13 (Section 3.3.2). Analysis done manually, with a hybrid scheme: the privacy-policy annotation scheme of Wilson et al. adapted (Table 2) plus inductive codes for the walkthrough (Section 3.4).
- Scope they chose to leave out: "any screenshots or notes outside this scope were excluded", because the analysis "should focus only on interface-level data control options, rather than back-end or undocumented mechanisms, because such implementations cannot be reliably verified through a walkthrough method" (Section 3.3.2, initial walkthrough protocol).

## Findings that matter to us
1. All six policies claim users can access, update, correct or delete their data (Section 4.1.1, Table 3).
2. Three controllable data types: chat history, memory, customized objects (Section 4.2, Table 4).
3. Deletion granularity differs (Section 4.2.1, Table 5):
   - Only Character.ai deletes individual messages.
   - ChatGPT, Claude, Gemini and Meta AI delete by chat session; Claude can delete multiple sessions by keyword search; Gemini can delete conversational rounds within a chosen time frame (last hour, last day, always, custom range).
   - ChatGPT, Claude, Gemini and Meta AI offer delete-all chat history in account settings.
   - Pi offers no deletion of chat history in Table 5.
4. Memory is "derived" data, stored as snippets that capture what the model decided to keep, usually rephrased; it exists on ChatGPT and Gemini, with a similar "pinned message" feature on Character.ai (Section 4.2.2). Snippets work across sessions.
5. Natural-language control: ChatGPT and Gemini let users tell the model to "remember" or "forget" (Section 4.3.1). Both show a visible indicator when memory is used or changed.
6. Local versus global effects (Section 4.3.3): only "delete all chat history" has a global effect. Deleting a ChatGPT chat leaves memory in place ("To clear any memories from this chat, visit your settings"); deleting a memory snippet leaves the chat transcript; deleting a Gemini chat does not touch saved info; Character.ai "Remove" hides the character and chat but does not erase it from storage, and the data can be retrieved later.
7. Retrospective versus proactive control (Section 4.3.2): all platforms offer retrospective control; only ChatGPT (Temporary Chat) and Gemini (turn off activity, auto-delete after 3, 18 default, or 36 months) offer a proactive form. Gemini shared links expire after six months by default.
8. Character.ai says popular public characters may be kept after the user deletes their data and account (Section 4.1.4).
9. Discussion (Section 5.2): natural-language control "can create a tension between control freedom and clarity"; users "might feel they have more control... when, in reality, the inherent ambiguity of NL control can affect their ability to foresee, verify, and review how their data is being handled". They call for "clear execution boundaries and verifiable outcomes", and for standards on "interpretability, auditability, and minimum functional guarantees for privacy-related NL commands" (Section 5.2.2).

## Their stated limits (Section 6, Section 3.1.2)
Interface level only; no user perspective; a snapshot (six U.S. platforms, two months, interfaces change); no Grok; no non-U.S. platforms; no test of whether a control works. They say follow-up user studies and cross-cultural work are needed.

## How it differs from our paper
- They document what the controls offer. We test what happens after a deletion request: for six agents we run recall checks on synthetic facts after each method, and we compare outcomes with what 177 participants expected.
- They explicitly set back-end behavior aside as unverifiable by a walkthrough. Our post-deletion analysis tests exactly that behavior from the outside.
- They have no users; our survey gives users' expectations (permanent deletion, verification) for the same kinds of controls.
- Agents overlap on ChatGPT, Claude and Gemini. They also cover Character.ai, Meta AI and Pi; ours includes Copilot, Perplexity and DeepSeek (check the final list in Section 3 before writing).
- Their local/global finding (Section 4.3.3) is the interface-level counterpart of our result that deleting a conversation may leave a fact in memory.

## Use in our paper
- Strong fit for the Introduction and Related Work, as the closest prior work and as support for "documentation says deletion is available" (Section 4.1.1).
- Their Section 5.2.2 sentence about "verifiable outcomes" can motivate the post-deletion analysis.
- Need to check: whether their wording on "memory" and "forget" prompts maps onto our deletion-request prompt method.

## Open questions after reading
- Whether the final CHI text differs from this arXiv v1 (page numbers, numbers). Check against the ACM version before quoting.
