# RTBF Chatbot Deletion Study — Project Update

Taiwo Olabamipe · University of Central Florida

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


----

The deletion-location definition was refined after piloting, and the
reliability reported here comes from coding under the final definition. A
location counts only when the prompt names it with an explicit referent
(conversation or chat, memory, account, or a database, server, or
training data); quantifiers such as ``all'' and generic containers such
as ``history'' or ``messages'' do not qualify. When a prompt names
several locations, a named database governs over a conversation or
memory, and a forward-looking clause governs over a named conversation.