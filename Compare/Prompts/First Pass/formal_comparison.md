1. Re-code 50 or all 139?
Re-code the same 50 first, not the full set. The reason: the original 50-item pass was two coders working independently with no shared codebook (RTBF-Prompt/data/context.md:114) — that's why you got only 2/7 dimensions aligning. Now that you have one shared codebook, you need a fresh reliability check using it before trusting it at scale — recoding the same 50 lets you compute agreement/kappa per dimension against a common standard, apples to apples. If you jumped straight to all 139 and the codebook still has soft spots (Verb's low variance, the mixed-type ~14% cases, the two open Location/Justification questions), you'd find out after coding 139 prompts instead of after 50.

2. After coding, what next? Standard sequence from here:
- Compute percent agreement + Cohen's kappa per dimension on the 50-item shared-codebook recode.
- Adjudicate anything that still disagrees (use the notes column flags — e.g., the mixed-type items, the two data-quality-flagged non-deletion items).
- If agreement's solid, extend coding to the remaining ~89 prompts to cover all 139 — codebook's proven at that point, so this could be split between the two of you rather than double-coded.
- Reconcile into one final labeled dataset.
- Move into the thematic write-up, tied back to the quantitative survey findings — this is listed as the qualitative coding sub-effort's closeout step in RTBF-Prompt/data/context.md:142.

- which of the 8 dimensions they actually intend to manipulate as factors vs. hold fixed. Likely candidates to hold fixed rather than vary: What (probably locked to the study's two existing scenarios — location vs. health — rather than a free factor), and possibly Accompanying Request (5 levels is a lot to manipulate deliberately; it may stay observational/coded-only rather than a designed factor). Cutting the factor list down before fractioning matters a lot — going from 8 factors to, say, 5 designed ones (Form, Tone, Verb, Justification, Location) drops the full factorial from ~8,100 to 3×3×3×2×5 = 270, which a modest fraction (e.g., 16-32 runs) covers far more comfortably.


