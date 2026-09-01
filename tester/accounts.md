# Test account map


## Main accounts (used by every cell NOT in the MAXIMAL isolation list)

| Platform | Email | Session file | Status (2026-09-01) |
|---|---|---|---|
| ChatGPT | `olacoderpad@gmail.com` | `sessions/chatgpt.json` | Working (re-exported today) |
| Claude | `anchorexperiment@gmail.com`  | `sessions/claude.json` | Working (re-exported and confirmed today) |
| Gemini | `anchorexperiment@gmail.com` | `sessions/gemini.json` | Working |
| Copilot | `anchorexperiment@gmail.com`  | `sessions/copilot.json` | Working |
| Perplexity | `anchorexperiment@gmail.com` | `sessions/perplexity.json` | Not re-checked this session |
| DeepSeek | `anchorexperiment@gmail.com` | `sessions/deepseek.json` | Working |



## Dedicated MAXIMAL accounts (one per MAXIMAL cell, see config.py's
`MAXIMAL_ACCOUNT_LABEL` -- built 2026-08-31/09-01 because MAXIMAL cells
are account-wide/blanket erasures and can't share an account with a
sibling MAXIMAL cell without wiping each other's anchors first)



### `maximal_i1` (role: I1 MAXIMAL cells)

| Platform | Cell | Email / display name | Session file | Status |
|---|---|---|---|---|
| ChatGPT | `CH-I1-E7` | `olabamipet@gmail.com` | `sessions/chatgpt__maximal_i1.json` | Working |
| Claude | `CL-I1-E5` | `olabamipet@gmail.com`  | `sessions/claude__maximal_i1.json` | Working |
| Gemini | `GE-I1-E6` | `olabamipet@gmail.com` | `sessions/gemini__maximal_i1.json` (myactivity merge still pending, see Pending items) | Working |
| Copilot | `CO-I1-E6` | `olabamipet@gmail.com`  | `sessions/copilot__maximal_i1.json` (+ privacy merge) | Working |
| DeepSeek | `DE-I1-E4` | `olabamipet@gmail.com` | `sessions/deepseek__maximal_i1.json` | Working |
| Perplexity | `PE-I1-E6` | -- | -- | **Skipped** (tier-blocked, see below) |

### `maximal_i2` (role: I2 MAXIMAL cells)

| Platform | Cell | Email / display name | Session file | Status |
|---|---|---|---|---|
| ChatGPT | `CH-I2-E7` | `experimentanchor@gmail.com` (confirmed via Settings > Account) | `sessions/chatgpt__maximal_i2.json` | Working |
| Claude | `CL-I2-E5` | `experimentanchor@gmail.com` (confirmed via account dropdown) | `sessions/claude__maximal_i2.json` | Working |
| Gemini | `GE-I2-E6` | `olacoderpad@gmail.com`  | `sessions/gemini__maximal_i2.json` (+ myactivity merge) | Working |
| Copilot | `CO-I2-E6` | `experimentanchor@gmail.com`  | `sessions/copilot__maximal_i2.json`  | Working |
| Perplexity | `PE-I2-E6` | -- | -- | **Skipped** (tier-blocked) |

### `maximal_i3` (role: I3 MAXIMAL cells -- only Claude/ChatGPT have an I3 condition)

| Platform | Cell | Email / display name | Session file | Status |
|---|---|---|---|---|
| ChatGPT | `CH-I3-E7` | `anchorexperiment+001@gmail.com` | `sessions/chatgpt__maximal_i3.json` | Working |
| Claude | `CL-I3-E5` | `olacoderpad@gmail.com` | `sessions/claude__maximal_i3.json` | Working |

### `maximal_file` (role: FILE-substudy MAXIMAL cells)

| Platform | Cell | Email / display name | Session file | Status |
|---|---|---|---|---|
| ChatGPT | `CH-IF-E-MAX` | `participantone@rtbfexperiment.com.ng` (confirmed via Settings > Account) | `sessions/chatgpt__maximal_file.json` | Working |
| Claude | `CL-IF-E-MAX` | `participantone@rtbfexperiment.com.ng` (confirmed via account dropdown) | `sessions/claude__maximal_file.json` | Working |
| Gemini | `GE-IF-E-MAX` | `teeola48@gmail.com`  | `sessions/gemini__maximal_file.json` (+ myactivity merge) | Working |
| Copilot | `CO-IF-E-MAX` | `teeola48@gmail.com`  | `sessions/copilot__maximal_file.json` | Working |
| DeepSeek | `DE-IF-E-MAX` | `experimentanchor@gmail.com`  | `sessions/deepseek__maximal_file.json` | Working |
| Perplexity | `PE-IF-E-MAX` | -- | -- | **Skipped** (tier-blocked) |

## Perplexity MAXIMAL cells -- deliberately not isolated

`PE-I1-E6`, `PE-I2-E6`, `PE-IF-E-MAX` stay on the main Perplexity account.
`_erase_maximal()` unconditionally raises `NotImplementedError` there
regardless of which account it's on -- this project's Perplexity test
account is Free tier, tier-gated out of Memory entirely (confirmed live,
403 on the underlying API), and the user explicitly decided not to
upgrade to Pro just to unlock this. Revisit only if that decision changes.

