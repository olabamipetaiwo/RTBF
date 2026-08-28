# RTBF Chatbot Deletion Study — Project Update

Taiwo Olabamipe · University of Central Florida

---

## Where We Are

- Participant survey: **complete**, screened, and fully analyzed (n=177)
- Statistical results: **cross-validated** across two independent pipelines
- Paper draft: results section for the survey largely written
- Technical audit (6 platforms): **not started** — separate workstream

---

## The Data

- 219 raw responses → 177 in the final analysis base
- Screened for attention checks and prior deletion experience
- Within-subject design: same participants rated a **less-sensitive**
  and a **more-sensitive** data-deletion scenario
- Sample: skews young (73% under 45), 62% bachelor's+, strong baseline
  privacy knowledge (5.06/6 correct on average)

---

## Analysis Rigor

- Every statistical test run through **two independent pipelines**
  (original `statsmodels`/`pingouin` stack vs. a from-scratch `scipy`-only
  reimplementation)
- 101 tests compared: **Pearson r = 0.9999**, **0 significance flips**
- Gives confidence the reported numbers aren't implementation artifacts

---

## Finding 1 — No Deletion Method Wins Outright

- Tested whether any method is statistically best on protection,
  effort, or perceived loss
- **Protection and loss:** no method separates from the others, at all
- **Effort:** the only scale with real separation — but even the
  best method ("delete this single conversation") only beats *one*
  rival, not all of them

---

## Finding 2 — Sensitivity Changes Feelings, Not Method Choice

- Willingness to delete rises significantly (+0.39) when data is
  more sensitive
- Perceived protection also rises significantly (+0.13)
- Effort and felt loss **don't move at all**
- Notably: *which method* you use never predicts protection — only
  *how sensitive the data feels* does

---

## Finding 3 — The Training-Data Blind Spot

- "This won't be used to train the model" is the **least-believed**
  outcome of deletion, for every method, in both scenarios
- 65–85% of participants don't expect deletion to stop their data
  from training the AI
- Consistent across the whole method set — not specific to any one
  deletion button

---

## Finding 4 — People Don't Verify, and the Gap Is Growing

- "I didn't know how to check" is the single most common response
  to "how did you verify deletion worked?" (~45% of the time)
- Participants consistently say they'd *ideally* use a heavier-duty
  method than the one they actually use
- That gap **widens**, not narrows, as sensitivity rises — the
  disconnect is biggest exactly when it matters most


---

## Next Steps

1. Code/analyze the elicited deletion-request prompts participants wrote
2. Use those prompts to run the technical audit across the 6 platforms
3. Draft Methodology section
4. Finish Introduction + Abstract
