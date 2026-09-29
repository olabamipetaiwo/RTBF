
### Known limitations (for the write-up)

- Attribution on shared accounts: handled by unique referent and token per cell, the 5 held-back generic prompts, and narrow-before-broad ordering.
- Only interface-observable: absence of a token does not show backend or training-data deletion.
- Platform replies can claim deletion, refuse, or point to Settings; a claim is unverified until recall.
- Uneven platforms: Perplexity's test account is locked out of Memory and DeepSeek has no memory, so neither gets the settings-panel check (R2).
- Fragile automation: selectors break, Cloudflare and bot checks interfere, rate limits force batching (ChatGPT throttled after about 44 attempts), expired sessions can give false "success" replies.
- Long timeline: erasure 48 hours after injection, recall 31 days after erasure, so a design mistake is costly once collection starts.