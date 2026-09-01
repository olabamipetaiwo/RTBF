# DeepSeek — policy excerpts

## Sources
- https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html — DeepSeek Privacy Policy (fetched 2026-08-28, direct WebFetch succeeded)

## No memory feature exists (I2/I3 not applicable; already confirmed live this project)
> "DeepSeek has no built-in memory at all — no saved memories, no custom instructions, nothing carried between chats." (secondary-source summary, consistent with this project's own live verification, ENUMERATION's R2 row: "No memory UI exists. Citation: Q13 in-product verification 'verified absent, July 2026' + docs.")

This is why DeepSeek is the only platform in this battery with a single injection type (I1) and no memory-targeted erasure mechanisms — there is nothing for E2 (bulk history)/E3 (NL forget) to act on beyond conversation history itself, and R2 (memory settings inspection) is structurally N/A.

## Chat/conversation retention (E1/E2)
> "We keep this Personal Data for as long as you have an account. This Personal Data includes your account Personal Data, input and payment Personal Data." — DeepSeek Privacy Policy

No separate retention period disclosed for conversation data specifically, beyond "as long as the account is active."

## Deletion mechanics
> "You can manage your chat history. Should you choose to do so, you may also copy or delete your chat history via your settings." — DeepSeek Privacy Policy

> Account deletion: "you will not be able to reactivate your account or retrieve any of the content or Personal Data in connection with your account."

## Backend deletion window — explicitly NOT disclosed (a real, citable gap)
> The policy states only that data will be destroyed/deleted/erased/anonymized "as permitted or required under applicable laws," **without specifying a duration**. No 30-day (or any other) backend-propagation window is stated anywhere in the policy, unlike Claude/ChatGPT/Copilot/Perplexity, which all disclose an explicit ~30-day figure.

This is itself worth citing directly in this cell's Expected-outcome text: DeepSeek is the one platform in this battery whose own privacy policy does **not** commit to any specific post-deletion propagation timeline, which is a relevant methodological caveat for how confidently a "PASS" here can be interpreted (this project's 31-day recall delay is not corroborated by DeepSeek's own stated policy the way it is for the other 4 platforms that disclose ~30 days).

## NL forget prompt (E3)
Per ENUMERATION's own notes: "Expected-null by architecture; RUN anyway (pre-registered)" — no persistent layer for a forget command to act on given the confirmed absence of any memory feature. This project's own architectural finding, not new from this policy pass, but it's the one cell on this platform where the *reasoning* is unusually strong (not just "no policy text found" but "no memory feature exists at all, confirmed live").
