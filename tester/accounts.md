# Test account map


## Main accounts (used by every cell NOT in the MAXIMAL isolation list)

| Platform | Email | Session file |
|---|---|---|
| ChatGPT | `olacoderpad@gmail.com` | `sessions/chatgpt.json` |
| Claude | `anchorexperiment@gmail.com`  | `sessions/claude.json` |
| Gemini | `anchorexperiment@gmail.com` | `sessions/gemini.json` |
| Copilot | `anchorexperiment@gmail.com`  | `sessions/copilot.json` |
| Perplexity | `anchorexperiment@gmail.com` | `sessions/perplexity.json` |
| DeepSeek | `anchorexperiment@gmail.com` | `sessions/deepseek.json` |



## Dedicated MAXIMAL accounts (one per MAXIMAL cell, see config.py's
`MAXIMAL_ACCOUNT_LABEL` -- built 2026-08-31/09-01 because MAXIMAL cells
are account-wide/blanket erasures and can't share an account with a
sibling MAXIMAL cell without wiping each other's anchors first)



### `maximal_i1` (role: I1 MAXIMAL cells)

| Platform | Cell | Email | Session file |
|---|---|---|---|
| ChatGPT | `CH-I1-E7` | `olabamipet@gmail.com` | `sessions/chatgpt__maximal_i1.json` |
| Claude | `CL-I1-E5` | `olabamipet@gmail.com`  | `sessions/claude__maximal_i1.json` |
| Gemini | `GE-I1-E6` | `olabamipet@gmail.com` | `sessions/gemini__maximal_i1.json` (myactivity merge still pending, see Pending items) |
| Copilot | ~~`CO-I1-E6`~~ | `olabamipet@gmail.com`  | `sessions/copilot__maximal_i1.json` (+ privacy merge) |
| DeepSeek | `DE-I1-E4` | `olabamipet@gmail.com` | `sessions/deepseek__maximal_i1.json` |
| Perplexity | `PE-I1-E6` | -- | -- |

### `maximal_i2` (role: I2 MAXIMAL cells)

| Platform | Cell | Email | Session file |
|---|---|---|---|
| ChatGPT | `CH-I2-E7` | `experimentanchor@gmail.com` | `sessions/chatgpt__maximal_i2.json` |
| Claude | `CL-I2-E5` | `experimentanchor@gmail.com` | `sessions/claude__maximal_i2.json` |
| Gemini | `GE-I2-E6` | `olataiwo839@gmail.com` | `sessions/gemini__maximal_i2.json` (still needs myactivity merge before E6's activity-delete component can run) |
| Copilot | ~~`CO-I2-E6`~~ | `experimentanchor@gmail.com`  | `sessions/copilot__maximal_i2.json`  |
| Perplexity | `PE-I2-E6` | -- | -- |

### `maximal_i3` (role: I3 MAXIMAL cells -- only Claude/ChatGPT have an I3 condition)

| Platform | Cell | Email | Session file |
|---|---|---|---|
| ChatGPT | `CH-I3-E7` | `anchorexperiment+001@gmail.com` | `sessions/chatgpt__maximal_i3.json` |
| Claude | `CL-I3-E5` | `olacoderpad@gmail.com`  | `sessions/claude__maximal_i3.json` |

### `maximal_file` (role: FILE-substudy MAXIMAL cells)

| Platform | Cell | Email | Session file |
|---|---|---|---|
| ChatGPT | `CH-IF-E-MAX` | `participantone@rtbfexperiment.com.ng` | `sessions/chatgpt__maximal_file.json` |
| Claude | `CL-IF-E-MAX` | `participantone@rtbfexperiment.com.ng` | `sessions/claude__maximal_file.json` |
| Gemini | `GE-IF-E-MAX` | `teeola48@gmail.com`  | `sessions/gemini__maximal_file.json` (+ myactivity merge) |
| Copilot | ~~`CO-IF-E-MAX`~~ | `teeola48@gmail.com`  | `sessions/copilot__maximal_file.json` |
| DeepSeek | `DE-IF-E-MAX` | `experimentanchor@gmail.com`  | `sessions/deepseek__maximal_file.json` |
| Perplexity | `PE-IF-E-MAX` | -- | -- |

## Perplexity MAXIMAL cells -- deliberately not isolated

`PE-I1-E6`, `PE-I2-E6`, `PE-IF-E-MAX` stay on the main Perplexity account.
`_erase_maximal()` unconditionally raises `NotImplementedError` there
regardless of which account it's on -- this project's Perplexity test
account is Free tier, tier-gated out of Memory entirely (confirmed live,
403 on the underlying API), and the user explicitly decided not to
upgrade to Pro just to unlock this. Revisit only if that decision changes.


### STRUCTURAL CONFLICT

(dedicated accounts for cells whose own erasure action is genuinely
account-wide/blanket AND shares its account with a sibling cell testing
that SAME blanket action -- whichever runs first invalidates the rest.
Full audit/rationale in `RTBF-Prompt/PROJECT_STATUS.md`'s "'Structural
conflict' cells identified" section and `config.py`'s
`MAXIMAL_ACCOUNT_LABEL` comment. The group's first cell stays on the main
account, as before -- only listed here are the cell(s) that need to move
off it. **Not yet set up as of 2026-09-07** -- emails proposed, nothing
logged into yet.)

#### `conflict_i2` (ChatGPT) -- role: I2 cells conflicting with CH-I1-E4/CH-I1-E6

| Cell | Conflicts with (already on main) | Erasure action | Email | Session file |
|---|---|---|---|---|
| `CH-I2-E4` | `CH-I1-E4` | Clear all memories | `noreply.ayodev@gmail.com`  | `sessions/chatgpt__conflict_i2.json` |
| `CH-I2-E6` | `CH-I1-E6` | Clear all chat history (bulk) | `noreply.ayodev@gmail.com` | `sessions/chatgpt__conflict_i2.json` |

Confirmed safe to share: `CH-I2-E4`/`CH-I2-E6` don't conflict with EACH
OTHER (different blanket surfaces -- memory vs. chat history), only each
with its own sibling already on the main account.

#### `conflict_i3` (ChatGPT) -- role: I3 cells conflicting with CH-I1-E4/CH-I1-E6

| Cell | Conflicts with (already on main) | Erasure action | Email | Session file |
|---|---|---|---|---|
| `CH-I3-E4` | `CH-I1-E4` | Clear all memories | `olataiwo839@gmail.com` | `sessions/chatgpt__conflict_i3.json` |
| `CH-I3-E6` | `CH-I1-E6` | Clear all chat history (bulk) | `olataiwo839@gmail.com` | `sessions/chatgpt__conflict_i3.json` |



#### `conflict_i2` (Claude) -- role: I2 cell conflicting with CL-I1-E3

| Cell | Conflicts with (already on main) | Erasure action | Email | Session file |
|---|---|---|---|---|
| `CL-I2-E3` | `CL-I1-E3` | Clear all memories | `dummybox90@gmail.com` | `sessions/claude__conflict_i2.json` |

#### `conflict_i3` (Claude) -- role: I3 cell conflicting with CL-I1-E3

| Cell | Conflicts with (already on main) | Erasure action | Email | Session file |
|---|---|---|---|---|
| `CL-I3-E3` | `CL-I1-E3` | Clear all memories | `noreply.ayodev@gmail.com` | `sessions/claude__conflict_i3.json` |

#### `conflict_i2` (Copilot) -- role: I2 cells conflicting with CO-I1-E2/CO-I1-E5

| Cell | Conflicts with (already on main) | Erasure action | Email | Session file |
|---|---|---|---|---|
| `CO-I2-E2` | `CO-I1-E2` | Delete all memory | `dummybox90@gmail.com` | `sessions/copilot__conflict_i2.json` |
| ~~`CO-I2-E5`~~ | `CO-I1-E5` | Privacy Dashboard | `dummybox90@gmail.com` | `sessions/copilot__conflict_i2.json` |


#### `conflict_i2` (Gemini) -- role: I2 cell conflicting with GE-I1-E5

| Cell | Conflicts with (already on main) | Erasure action | Email | Session file |
|---|---|---|---|---|
| `GE-I2-E5` | `GE-I1-E5` | Delete all Saved info | `noreply.ayodev@gmail.com`  | `sessions/gemini__conflict_i2.json` |

### `instability` (Gemini) -- role: cells migrated off the unstable main account

| Cell | Erasure action | Email | Session file |
|---|---|---|---|
| `GE-I1-E4` | Delete individual Saved info item | `dummybox90@gmail.com` | `sessions/gemini__instability.json` |
| `GE-I2-E2` | Delete individual Saved info item | `dummybox90@gmail.com` | `sessions/gemini__instability.json` |

### `instability2` (Gemini) -- role: second migration off the unstable main account

| Cell | Erasure action | Email | Session file |
|---|---|---|---|
| `GE-I1-E2` | Delete single conversation | `experimentanchor@gmail.com` | `sessions/gemini__instability2.json` |

### `recall_conflict` (Gemini) -- role: blanket erasure that would corrupt pending recalls on the main account

| Cell | Erasure action | Email | Session file |
|---|---|---|---|
| `GE-I1-E3` | Delete all activity | `ogunwalepelumi06@gmail.com`  | `sessions/gemini__recall_conflict.json` |
| `GE-I2-E3` | Delete all activity | `ogunwalepelumi06@gmail.com` | `sessions/gemini__recall_conflict.json` |

### `recall_conflict` (Copilot) -- role: same pattern -- blanket erasure that would corrupt pending recalls

| Cell | Erasure action | Email | Session file |
|---|---|---|---|
| `CO-I1-E5` | Privacy Dashboard | `noreply.ayodev@gmail.com`  | `sessions/copilot__recall_conflict.json` |
| `CO-I2-E5` | Privacy Dashboard | `noreply.ayodev@gmail.com` | `sessions/copilot__recall_conflict.json` |

### `recall_conflict` (Claude) -- role: same pattern, proactive (not yet materialized)

| Cell | Erasure action | Email | Session file |
|---|---|---|---|
| `CL-I1-E3` | Clear all memories | `olataiwo839@gmail.com` | `sessions/claude__recall_conflict.json` |

### `ui_migration_i1`/`ui_migration_i2`/`ui_migration_file` (Copilot) -- role: MAXIMAL cells moved off a Copilot new-UI conversation-history migration delay

Not an account-sharing conflict (each was already isolated) -- Microsoft's
new Copilot UI hadn't finished migrating these accounts' older
conversation history in ("Previous conversations from old Copilot take a
few minutes to appear," 0 conversations visible including the one
injected here), confirmed live 2026-09-09 and not resolved after
rechecks. Moved per direct instruction rather than keep waiting.

| Cell | Erasure action | Email | Session file(s) |
|---|---|---|---|
| `CO-I1-E6` | MAXIMAL | `olataiwo839@gmail.com` | `sessions/copilot__ui_migration_i1.json` |
| `CO-I2-E6` | MAXIMAL | `olacoderpad@gmail.com` | `sessions/copilot__ui_migration_i2.json` |
| `CO-IF-E-MAX` | Maximal combination (all erasure mechanisms) | `ogunwalepelumi06@gmail.com` | `sessions/copilot__ui_migration_file.json` |

### `nlforget` (5 platforms on one account, Gemini on a separate one) -- role: dedicated account(s) for the NL-forget-prompt study

Not a per-cell isolation entry like the groups above -- this is the
dedicated account setup for the whole NL-forget-prompt study (138
authoritative prompts x 6 platforms = 828 cells, additive to the 13
existing `blocked_on_prompt_set` cells), resolved by the user 2026-09-11.
See `RTBF-Prompt/PROJECT_STATUS.md`'s "NL-forget-prompt factorial study:
scope and account policy" section (title predates the 2026-09-11
redesign) for the full history. Wired into `config.py`'s
`MAXIMAL_ACCOUNT_EMAIL` under the `nlforget` label. **828-cell pipeline
built 2026-09-11** (own "NL FORGET" xlsx sheet, `run_cell.py` wired --
see project memory `nl-forget-pipeline-built-2026-09-11`); live injection
run via `tester/nl_forget_round_robin_scheduler.py` (see project memory
`nl-forget-adaptive-scheduler-2026-09-11` for current status/state file).


| Platform | Email | Session file |
|---|---|---|
| ChatGPT | `astrataiwo@gmail.com` | `sessions/chatgpt__nlforget.json` |
| Claude | `astrataiwo@gmail.com` | `sessions/claude__nlforget.json` |
| Gemini | `olaoluwaboluwatife001@gmail.com` | `sessions/gemini__nlforget.json` |
| Copilot | `astrataiwo@gmail.com` | `sessions/copilot__nlforget.json` |
| Perplexity | `astrataiwo@gmail.com` | `sessions/perplexity__nlforget.json` |
| DeepSeek | `astrataiwo@gmail.com` | `sessions/deepseek__nlforget.json` |

#### Testing-input interference handling (revised 2026-09-23)

All 138 prompts per platform share ONE account (5 platforms on
`astrataiwo@gmail.com`, Gemini on `olaoluwaboluwatife001@gmail.com`), so
interference between cells is handled per cell, not per account.


**Why the run prompts should not interfere with each other:** each typed sentence
names only its own referent. That is by wording and by design, not yet
independently verified live per platform; no recall has run yet, so no wide
deletion could have been observed.

