---
name: yao-li-meeting-2026-10-07
description: RTBF paper edits from Yao Li meeting 2026-10-07 — writing style (frame/report/interpret), CFA, CI removal, abbreviations, table restructuring, S&P venue framing
metadata:
  type: project
---

Yao Li meeting 2026-10-07 produced these directives for the paper:

1. **Writing style** — every results paragraph must follow Frame (remind reader what was measured) / Report (numbers) / Interpret (what it means). DONE 2026-10-07, all 12 paragraphs rewritten.

2. **CFA replaces EFA** — scales come from existing literature, so CFA (not EFA) is correct. Report factor loadings > .6, AVE > .5, Cronbach's alpha > .8, run for LS, MS, Pooled separately. DONE 2026-10-07, src/cfa.py written, tab:cfa-fit table in paper.

3. **Remove 95% CIs** — clutters narrative. DONE 2026-10-07, all 6 instances removed, bootstrap methodology sentence trimmed.

4. **Abbreviations LS/MS/Pooled** — defined in scenario-creation paragraph, applied globally. DONE 2026-10-07.

5. **Table 7 (method-scales)** — add method-comparison and scenario-comparison test-statistic rows. DONE 2026-10-07.

6. **Combine Tables 8+9** — expectations and verification merged into one table* with bold separator. DONE 2026-10-07.

7. **S&P framing** — venue needs threat model / problem / solution structure. Brainstorm solutions for the problems found. Reference: PINFINDER paper (arxiv 2502.11208). NOT YET STARTED.

**Why:** professor's direct feedback on scientific writing quality; the paper read like a stats printout, not a guided tour of findings.
**How to apply:** maintain the frame/report/interpret pattern in any future paragraph additions; keep CIs out unless professor reverses.
