- Q14 — what should the actual PDF file contain? Default leans toward one fixed template mirroring "survey Scenario B" (a synthetic appointment-prep document). Blocks the substudy — nobody can build injection until this document actually exists.
- Q15 — include DeepSeek or not? Default leans IN ("cheap, uniform"). This one's marked not blocking — it's a scope call, not a prerequisite.
- Q16 — accept the verification procedure as written? It's: upload the file, check memory settings for the token; if it's not there, explicitly ask the platform to summarize the document (forcing it to actually read it), then check again — logging which of those two conditions is what actually produced extraction. Default leans ACCEPT. Blocks the substudy.

CH-IF-E-MAX injection succeeded this time — the quota block is gone. Extraction observed: "extracted only after forced read" (token appeared only after explicitly asking ChatGPT to summarize the doc, not spontaneously or in memory). Erasure is now due 2026-09-02T05:22:27 UTC (48h from now). Transcript/screenshot saved under transcripts/chatgpt/CH-IF-E-MAX/.


Per-platform breakdown (narrow first → broad/account-wide last):

- ChatGPT (16): narrow = Delete conversation ×3, Delete conversation containing file ×1, Clear custom instructions ×3 → broad last = Clear all memories ×3, Clear all chat history (bulk) ×3, MAXIMAL ×3
- Claude (14): narrow = Delete conversation ×3, Delete individual memory edit ×3, Delete conversation containing file ×1 → broad last = Clear all memories ×3, MAXIMAL ×3, Maximal combination ×1
- Copilot (12): narrow = Conversation history deletion ×2, Granular facts editor ×2, Delete conversation containing file ×1 → broad last = Delete all memory ×2, Privacy Dashboard ×2, MAXIMAL ×2, Maximal combination ×1
- DeepSeek (5): narrow = Delete single conversation ×1, Delete conversation containing file ×1 → broad last = Delete all history ×1, MAXIMAL ×1, Maximal combination ×1
- Gemini (12): narrow = Delete single conversation ×2, Delete single Saved info item ×2, Delete conversation containing file ×1 → broad last = Delete all activity ×2, Delete all Saved info ×2, MAXIMAL ×2, Maximal combination ×1
