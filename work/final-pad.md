## Tasks

Two sections: **Not done** (open tasks, below) and **Done** (at the end, with what changed in the paper).

Part A tasks don't depend on any other task, and no other task waits on them. Do them in any order.
Part B tasks depend on each other. Do them in the order listed; each one says what it needs.
"(was N)" gives the old task number.

---

## Not done

### A. Independent tasks (any order)

**A2. Remove the stealth patch from the artifact** (was 7; your decision, 2026-11-09). The paper part is done: removed from `tech_analysis.tex`, `ethics.tex` and `refs.bib` on 2026-11-10.
- **Artifact code:** stealth is wired in functionally, not just mentioned:
  - `tester/flows/base.py` (`USE_STEALTH`);
  - `chatgpt.py`, `claude.py`, `copilot.py`, `perplexity.py`, `gemini.py`;
  - `tester/requirements.txt`.

  Removing it changes how the code runs (Claude/Perplexity sessions were blocked without it), so decide whether to strip the code path or leave the automation code out of the artifact.
- **Artifact docs:** `RTBF-Prompt/notes/PROJECT_STATUS.md` and `tester/CLAUDE.md`. Exclude the paper drafts in `RTBF-Analysis/paper/` and `backup/` from the artifact.
- **Artifact scope (your decision, 2026-11-10):** code + guide only; users bring their own accounts. Replace the hardcoded emails in `tester/config.py` with a user-filled config; leave out `accounts.md`, `sessions/`, `transcripts/`, `data/`.
- **README note (your instruction, 2026-11-10):** say the automation reflects the agents' interfaces at the time of the study (Aug to Nov 2026) and that the platforms may have changed since, so it may not run as-is.
- **Risk (noted, your call):** the reviewer already flagged it (`review/codex.md:92`), and the CFP asks how harm to live systems was minimised.

**A6, figure part. Change "31 days" to "≥30 days" in the DIDR figure** (`figures/DIDR.png`; you, in your figure tool). The text and caption already say "at least 30 days"; the shortest gap was 30.2 days.

---

### B. Dependent tasks (in this order)

---

## Done

**A1. Report accounts, sequencing and configuration** (2026-11-10).
- `tech_analysis.tex`: new paragraph "Accounts and timeline": U.S., default settings, shared prompt account and main account, separate accounts for broad deletions, the 48-hour and 30-day intervals.
- `tech_analysis.tex`, start of "Outcome Measures and Analysis": test cases aren't independent observations, so results are reported descriptively.
- Decided against: an account table, account counts, the Copilot migration date.
- Source numbers: `RTBF-Analysis/src/accounts_timeline.py` → `outputs/results/accounts_timeline.md`.

**A2, paper part. Remove the stealth patch** (2026-11-10). Removed from `tech_analysis.tex`, `ethics.tex` and `refs.bib`. The artifact part is still open under Not done.

**A3. Survey-vs-experiment data mismatch** (was 13; `review/review.md` Weakness 5). The paper part is done (2026-11-10): one clause added to `tech_analysis.tex` (synthetic fact generation): "so the recall results reflect how agents handle everyday facts rather than sensitive information." No Limitations sentence: the paper doesn't test sensitivity.
- **If a reviewer raises it, the rebuttal answer (Feb 16):**
  > "We used non-sensitive synthetic facts so that safety filters would not block injection or recall, which would make deletion outcomes unobservable. Participants' expected deletion outcomes did not differ significantly between the less and more sensitive scenarios (Table~\ref{tab:gee-full}; e.g., permanent deletion OR = 1.30, future conversations OR = 0.92), so the comparison in RQ4 does not depend on the sensitivity of the data. Testing sensitive data is future work."
- **Source:** `RTBF-Analysis/outputs/results/pooled_gee.md`. Other MS vs. LS ORs: training 1.20 (n.s.); current conversation 0.69 (unadjusted p = .021).

**A4. Fix survey reporting and interpretation** (2026-11-10), all in `user_study.tex`:
- **"Would choose":** the prose now matches the live question (all methods, select all); the old "never used" version was in the survey's Trash.
- **Preference gap:** the 47–50% (select all) and 8–14% (pick one) figures are kept, with a note that they aren't directly comparable; no "gap".
- **Participant flow:** 235 → 217 (17 incomplete, 1 attention check) → 177 (36 no experience, 4 missing); `tech_analysis.tex:102` says "209 of the 217 participants with complete responses".
- **"Consistent":** now "no statistically detectable difference", naming the small method groups (29 and 30); no CIs.
- **Finding 1:** the effect is credited to the scenario, not to data sensitivity.

**A5. Disclose how participant requests were edited** (2026-11-10), no numbers in the text, per your decision:
- `tech_analysis.tex`, after "We submitted the remaining 133 requests…": requests referring to the scenario's location were adapted to refer to the synthetic fact (cheese-press example); the rest were sent as written.
- `tech_analysis.tex`, after the coding paragraph: codes describe the original wording; for *data named*, adapted requests referred to the synthetic fact.
- `user_study.tex:98`: "deletion requests adapted from those written by survey participants".
- Not done, by choice: recoding *data named* on the sent text. For a reviewer: 113 of the 133 sent were adapted, 20 sent as written (`nl_forget_prompts_138_final.csv`, `swapped`); I0350 also got a grammar fix.

**A6. Fix internal inconsistencies, text part** (2026-11-10):
- `user_study.tex:46`: the eight methods are now the six in Table 1 plus account deletion and filing a request, each with its reason for not being tested.
- `user_study.tex:32`: (7) → (6); the commented-out section stays out.
- `tab:gee-full`: the caption explains "Other" (too rare, p = 1 in Holm); row "Ask to forget" → "Deletion-request prompt".
- `fig:scales` caption: 317 responses from 165 participants; the per-method counts overlap.

**A7. Copilot's full procedure and the privacy dashboard: no change needed** (2026-11-10). The dashboard SKIP began on 2026-10-05; Copilot's full procedure in the paper (CO-I2-E6, and CO-IF-E-MAX in the supplemental cases) ran on 2026-09-13. The code at that time (`4eb6df5`, `_erase_maximal`) ran all four steps with no error handling, and the deletion finished, so the dashboard step ran. "All applicable controls" (`tech_analysis.tex:86`) holds. Limit: the erase record has no per-step log.

**B1. Placeholder results: closed by your decision** (2026-11-10). You judged it not a problem. As of today the paper's 865 base still includes 61 predicted results (49 Copilot, 12 Gemini) from `src/provisional_fill.py`; `paper/sections/provisional.md` lists every affected number if recall results come in.

**B2. Name the primary recall endpoint** (2026-11-10), no breakdown or counts in the text, per your decision:
- `tech_analysis.tex`, Outcome Measures: recall success = value in any new-conversation recall response on the account, or found by the UI-based check. The same-conversation check doesn't contribute, was run last so it couldn't influence the others, and was taken because participants verify that way (`\label{sec:user_verification}` added to the RQ2 subsection of `user_study.tex`).
- `tech_analysis.tex`, Data recall: each check in its own new conversation; second wording in the same conversation.
- "resurface" → "be retrievable" where it describes agents (`tech_analysis.tex` incl. Findings 5 and 7 and the `tab:expectation-outcome` caption; `intro.tex` RQ3); `discussion.tex:72` → "can still be retrieved". Kept: indirect-check description, participants' reports, title.
- `tab:expectation-outcome` caption: response bases added (164, 73, 41, 39). Table numbers re-checked against `src/expectation_vs_outcome.py`: all match.
- CH-NLF-I0371 (found only by the UI-based check): correctly recall success; no change.
- For a reviewer: 146 direct, 13 indirect (all also direct), 1 UI-only, 15 via another case's recall prompt (`outputs/tables/audit_outcomes_provisional.csv`).


----

Side question:  which one are  CH-NLF-I0371, GE-I1-E3, CH-I2-E1 and CO-I2-E3.
-run review again anf dix abstract


----

**B3. Separate scope mismatch, misleading confirmation and documentation contradiction** (2026-11-10), all in `tech_analysis.tex`:
- **(c) Contradictions:** the prompt-based sentence now says "Among the prompt-based test cases, 319…"; the UI-action sentence is limited to deletion "performed through the interface" (22 of 23); new sentence for the 13 chat-typed UI-action cases (3 consistent, 2 contradicted); all four contradictions (CH-NLF-I0371, GE-I1-E3, CH-I2-E1, CO-I2-E3) described as "documentation says it removes the information, yet it remained retrievable".
- **(b) Complied but retrieved:** after the 11/101 sentence, the 11 complied cases are described, with the CH-NLF-I0355 example (yoga studio: "Done… won't use or recall it in future conversations", then returned the name 30+ days later). No new label, per `terms.txt`.
- **(a) Scoped deletion:** done with B4 below.

**B4. Frame ChatGPT's recall as scoped deletion with a copy left in the original chat** (2026-11-10). After the "107 … ChatGPT" sentence in Documentation consistency: deletion behaved as documented, but the original chat stayed and the fact came back in a new chat; ChatGPT didn't return it in the original chat in 104 of 107 cases, so users verifying there would think it was deleted (→ `sec:user_verification`); we can't tell which copy was used. Source: `src/chatgpt_same_chat.py` → `outputs/results/chatgpt_same_chat.md`. The task's "107 → 108" was wrong: 107 is correct for prompt-based cases (108 included a UI-action case).

**B5. Reframing adopted** (2026-11-10): agents keep user information in several places; a single deletion reaches only some of them; documented cases instead of pooled rates.
- **Title** (`main.tex:83`): "…Post-Deletion Data Recall in Commercial LLM Agents" (was "Resurfacing"). **Update the title on HotCRP too.**
- **Abstract:** rewritten and shortened (276 → ~175 words); no pooled rate, no "varied more across agents"; ChatGPT as the documented example.
- **Intro** RQ3/RQ4 sentences (`intro.tex:79–81`): same framing, ChatGPT example.
- **RQ3 results** (`tech_analysis.tex`): counts without percentages, outcomes reported per agent; "No deletion method consistently prevented recall" (false) → only the most extensive procedure prevented recall in every determinable case (7 recall failed, 0 recall success); Finding 3: retrievable on five of six agents + most extensive procedure.
- **Conclusion** (two sentences) and **Discussion opening** (`discussion.tex:8`): same framing.
- Left as is: `discussion.tex:118` (can't-tell share in Limitations).

**B6. Fix the headline recall number** (2026-11-10), done through B5: no pooled rate anywhere ("18.7%", "41.1%", "162 of 865" all gone). The abstract and intro give the finding in words; the RQ3 results give the three counts without percentages and point to the per-agent table (`tab:outcomes-agent`). The bounds aren't needed because no rate appears. `discussion.tex:118` (can't-tell share in Limitations) kept. 162 → 161: closed in B2, no change.

**B7. Narrow the deletion claims** (2026-11-10):
- **Definition** (`tech_analysis.tex`, after the recall-failed rule): recall failed = value not retrieved, not deleted; without a no-deletion baseline it can't be attributed to the deletion method.
- **Storage evidence** (after the "Memory updated" rule): direct injection into a saved-memory page counts as storage, with an empty page at recall as evidence; recall failed split: 225 interface notification, 3 agent only, 4 direct injection (CL-I2-E3, CL-I3-E2, CL-I3-E4, CL-I3-E5). Source: `src/storage_evidence.py` → `outputs/results/storage_evidence.md`.
- **Causal wording:** "prevented recall" (my B5 wording, RQ3 opening and Finding 3) → "the only deletion method with no recall success among determinable test cases"; Claude's 141 recall-failed cases qualified (may reflect retrieval, not deletion); "resulted in" → "was followed by" for the Claude UI-action methods.
- **Limitations** (`discussion.tex`, observability): DeepSeek, Gemini and Perplexity support no comparison; no no-deletion baseline or pre-deletion recall check, so no attribution and no rankings.
- Finding 4's cross-agent claim is left for B8.


**B8. Bring the method and agent claims in line with the data** (2026-11-10). No numbers added to the text:
- **Finding 4:** cross-agent claim now rests on the same deletion requests sent to every agent: recall success frequent on ChatGPT, never on Claude after those requests; differences "may reflect how each agent stores and retrieves information"; wording part kept.
- **"Only" claim** (`tech_analysis.tex:336`, Finding 3): the privacy dashboard (Copilot) also had no recall success, so "only" removed; `:336` names the dashboard, Finding 3 says nothing was retrieved after each agent's most extensive procedure.
- **"Three methods"** (`:338`): the 29%–50% and 7–13 figures covered four methods; clearing all saved memories added, count dropped.
- **Custom instructions** (Methods, after the 13 chat-requested cases): sentence added saying ChatGPT's clearing of custom instructions was also tested and is not in `tab:methods` (3 test cases in the 865).
- **Intro `:81` / Conclusion `:13`:** "every deletion method we evaluated" → "each of the deletion methods participants selected most often" (matches the RQ4 scope at `:510`).
- **Causal wording:** "resulted in"/"produced" → "was followed by" at `:340`, `:450`, `:512`, `:514`, `:519`, `:578` and Finding 7; `:340` and `:519` no longer repeat the table counts and point to `tab:expectation-outcome`.
- **Full outcome table:** left out of the paper by your decision; kept for the rebuttal. Source: `src/outcomes_agent_by_method.py` → `outputs/results/outcomes_agent_by_method.md` (agent × method, checks the 162 / 232 / 471 totals).

**B9. Restate the RQ4 comparison as an existence result** (2026-11-10):
- Text and Finding 7 already made the existence claim after B8 ("each of these methods was followed by recall success in at least some test cases").
- **Table `tab:expectation-outcome`:** group headers "Survey" and "DIDR experiments", "Expected (% of responses)", and the caption now says the two parts describe different observations and are not comparable rates. All numbers unchanged.
- **"Deletion-request prompts showed similar gaps"** merged into one sentence: "Deletion-request prompts were also followed by recall success in some test cases (Table …)."

**B10. Counts behind "26%–78%"** (2026-11-10), `tech_analysis.tex:576`, no numbers in the text, per your preference:
- Range replaced by the two opposite directions: ChatGPT (most) and Perplexity (about a quarter) didn't return the fact in the original conversation yet it was retrieved in a new one (users would wrongly think it deleted); Claude (most) and Copilot (about half) repeated it in the original conversation yet it wasn't retrieved in a new one (users would wrongly think deletion failed).
- Counts for reviewers: ChatGPT 104/133, Perplexity 8/31, Claude 86/131, Copilot 29/58. Source: `src/checks_vs_outcome.py` → `outputs/results/checks_vs_outcome.md` (rechecked against the CSV today).
