# Right to Be Forgotten
## Data-Deletion Methods for AI Chatbots

Survey analysis — results readout
Presented to Brandon & Li

---

## Why & What We Did

**Question:** Do people trust and use AI chatbot deletion methods (clear chat, wipe memory, delete account) equally — and does that change when data is more sensitive?

**Design:** Within-subject survey, same question battery run twice —
- **Q4** = less-sensitive data scenario
- **Q5** = more-sensitive data scenario

7 deletion methods tested; rated protection, effort, benefit-loss, willingness, expectations, verification, confidence, ideal method.

---

## Sample

```
eligible respondents        : 182
paired base (both scenarios): 177
```

US-only, all prior chatbot users, skews young (73% under 45). ChatGPT/Gemini near-universal; Claude/Copilot mid-tier.

**Analysis:** descriptive pass → formal tests (Kruskal-Wallis, Wilcoxon, McNemar, Stuart-Maxwell, Holm-corrected) → global re-correction across all ~101 tests as a rigor check.

Scale reliability: all 6 scales α = 0.87–0.92 (solid).

---

## Headline Finding: Willingness Rises With Sensitivity

```
mean willingness:  less = 3.98   more = 4.37
p < .0001   r = +0.55   (largest effect in the study)
```

- "Definitely yes": 76 → 102 respondents.
- Doesn't differ by *which* method used — it's about disposition to delete, not method.
- **Survives every correction, including the strictest global one.**

---

## Method Differences: Effort Is What Separates Them

| Scale | Result |
|---|---|
| Protection | ns, both scenarios |
| **Effort** | **SIG, both scenarios** |
| Benefit loss | ns, both scenarios |

- "Delete this conversation" = easiest
- "Delete a specific saved memory" = hardest, and highest felt loss

---

## Scenario Effect: Protection Rises, Not Effort

Same respondents, less → more sensitive data:

| Scale | Result |
|---|---|
| **Protection** | **SIG**, p=.0018, r=0.38 |
| Effort / Benefit loss | ns |

Framing effect: feels more protective when data feels more sensitive — but doesn't feel more/less burdensome.

⚠️ Method choice doesn't move protection; data sensitivity does.

---

## Switching, Verification, Calibration

- **Switching:** 36% change method less→more, but no systematic escalation (Stuart-Maxwell ns). Notable lead: 15 abandon "ask chatbot to forget" (doesn't survive correction).
- **Verification:** tracks interface feedback, not actual protection — people check methods that "talk back," not ones that matter most.
- **Calibration:** used-vs-ideal gap exists for nearly every method, and **widens** as sensitivity rises (e.g. "ask to forget" gap: 33 → 42 pts).
- **Blind spot:** 65–85% don't expect deletion to stop model training use, regardless of method.

---

## Demographics & Rigor Check

- Age / tenure explain **none** of the core effects — good null, findings generalize across the sample.
- Across ~101 tests: 31 raw-significant → 22 survive FDR → **14 survive strictest global correction.**
- Bulletproof: willingness↑, effort-by-method, calibration gaps, verification-by-method.
- Softer than it looks: protection scenario-shift (fails strictest global bar, still likely real).

---

## What We Infer

1. **Willingness to delete rises sharply with sensitivity** — strongest, most defensible claim.
2. **Effort, not protection, differentiates methods.**
3. Felt protection under sensitivity is a **perception effect**, not proof behavior improves.
4. **Want-use gap widens** exactly when stakes are highest.
5. Verification tracks **interface feedback**, not real protection.
6. Persistent **trust gap on training-data use**.

---

## Limitations

- Self-reported intent, not observed behavior.
- Sample: young, US-only, chatbot-literate — limited generalizability.
- Some method groups very small (n=2–9) — underpowered.
- ~1/3 of raw-significant results don't survive full correction (flagged throughout).

---

## Discussion

- Follow up on "ask to forget" abandonment — real or noise?
- Is the training-data expectation gap a comms/UI fix?
- Verification-UX experiment: does visible feedback change trust/checking behavior?
- Add second screening gate (prior deletion experience)?

**Open floor.**
