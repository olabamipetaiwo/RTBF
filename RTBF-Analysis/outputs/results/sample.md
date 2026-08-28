# sample

_Run at 2026-08-25T23:53:27_

```text
sample: n = 177

=== demographics ===
           variable        response   n   pct
                Age 25-34 years old  56  31.6
                Age 35-44 years old  45  25.4
                Age 18-24 years old  29  16.4
                Age 45-54 years old  27  15.3
                Age 55-64 years old  17   9.6
                Age   65+ years old   3   1.7
        Lives in US             Yes 177 100.0
Ever used a chatbot             Yes 177 100.0

=== usage x tenure (users only) ===
            Less than 6 months  6 to 12 months  1 to 2 years  2+ years  total_users
ChatGPT                     27              21            60        68          176
Gemini                      38              47            53        26          164
Claude                      45              38            26        11          120
Copilot                     43              30            30        17          120
Perplexity                  35              16            14         9           74
Deepseek                    25              18            17         4           64

saved -> outputs/figures/fig1_ai_tenure.png
saved -> outputs/figures/fig2_age_distribution.png
saved -> outputs/figures/fig3_chatbot_adoption_share.png
saved -> outputs/figures/fig4_tenure_pct_stacked.png
saved -> outputs/figures/fig5_adoption_rate.png
```

## DON'T CLEAR THIS
## Interpretation

3. Sample (sample.md) — who these numbers generalize to

- 100% US-based, 100% prior chatbot users (these were eligibility criteria, not findings). Age skews young: 73% under 45, only 11% over 55.

- ChatGPT near-universal (176/177, 99.4%), Gemini widely used (164, 92.7%), Claude/Copilot mid-tier (120 each, 67.8%), Perplexity/Deepseek least used (74 and 64, 41.8%/36.2%) and also the most recently-adopted (shortest tenure).

- Read: any per-method finding you report should be caveated as "young, US, experienced-chatbot-user population," and platform-specific results (if you ever split by which chatbot someone was thinking of) will be much better powered for ChatGPT/Gemini than for Deepseek
