# Test account map


## Main accounts (used by every cell NOT in the MAXIMAL isolation list)

| Platform | Email | Session file | Status (2026-09-01) |
|---|---|---|---|
| ChatGPT | `olacoderpad@gmail.com` | `sessions/chatgpt.json` | Working |
| Claude | `anchorexperiment@gmail.com`  | `sessions/claude.json` | Working |
| Gemini | `anchorexperiment@gmail.com` | `sessions/gemini.json` | Working |
| Copilot | `anchorexperiment@gmail.com`  | `sessions/copilot.json` |  Holds `CO-I1-E4` (chat `831d160b-130e-0064-77ba-a01675aa9828`). Shared: never "Delete all memory". |
| Perplexity | `anchorexperiment@gmail.com` | `sessions/perplexity.json` | Not re-checked |
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
| Copilot | ~~`CO-I1-E6`~~ | `olabamipet@gmail.com`  | `sessions/copilot__maximal_i1.json` (+ privacy merge) | Stale: `CO-I1-E6` moved to `ui_migration_i1` 2026-09-09. |
| DeepSeek | `DE-I1-E4` | `olabamipet@gmail.com` | `sessions/deepseek__maximal_i1.json` | Working |
| Perplexity | `PE-I1-E6` | -- | -- | **Skipped** (tier-blocked, see below) |

### `maximal_i2` (role: I2 MAXIMAL cells)

| Platform | Cell | Email / display name | Session file | Status |
|---|---|---|---|---|
| ChatGPT | `CH-I2-E7` | `experimentanchor@gmail.com` (confirmed via Settings > Account) | `sessions/chatgpt__maximal_i2.json` | Working |
| Claude | `CL-I2-E5` | `experimentanchor@gmail.com` (confirmed via account dropdown) | `sessions/claude__maximal_i2.json` | Working |
| Gemini | `GE-I2-E6` | `olataiwo839@gmail.com` (confirmed via account dropdown, "Taiwo Ola") | `sessions/gemini__maximal_i2.json` (still needs myactivity merge before E6's activity-delete component can run) | Working, re-injected 2026-09-09 (token: "Essay Segment") |
| Copilot | ~~`CO-I2-E6`~~ | `experimentanchor@gmail.com`  | `sessions/copilot__maximal_i2.json`  | Stale: `CO-I2-E6` moved to `ui_migration_i2` 2026-09-09. |
| Perplexity | `PE-I2-E6` | -- | -- | **Skipped** (tier-blocked) |

### `maximal_i3` (role: I3 MAXIMAL cells -- only Claude/ChatGPT have an I3 condition)

| Platform | Cell | Email / display name | Session file | Status |
|---|---|---|---|---|
| ChatGPT | `CH-I3-E7` | `anchorexperiment+001@gmail.com` | `sessions/chatgpt__maximal_i3.json` | Working |
| Claude | `CL-I3-E5` | `olacoderpad@gmail.com`  | `sessions/claude__maximal_i3.json` | Working |

### `maximal_file` (role: FILE-substudy MAXIMAL cells)

| Platform | Cell | Email / display name | Session file | Status |
|---|---|---|---|---|
| ChatGPT | `CH-IF-E-MAX` | `participantone@rtbfexperiment.com.ng` (confirmed via Settings > Account) | `sessions/chatgpt__maximal_file.json` | Working |
| Claude | `CL-IF-E-MAX` | `participantone@rtbfexperiment.com.ng` (confirmed via account dropdown) | `sessions/claude__maximal_file.json` | Working |
| Gemini | `GE-IF-E-MAX` | `teeola48@gmail.com`  | `sessions/gemini__maximal_file.json` (+ myactivity merge) | Working |
| Copilot | ~~`CO-IF-E-MAX`~~ | `teeola48@gmail.com`  | `sessions/copilot__maximal_file.json` | Stale: `CO-IF-E-MAX` moved to `ui_migration_file` 2026-09-09. |
| DeepSeek | `DE-IF-E-MAX` | `experimentanchor@gmail.com`  | `sessions/deepseek__maximal_file.json` | Working |
| Perplexity | `PE-IF-E-MAX` | -- | -- | **Skipped** (tier-blocked) |

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

| Cell | Conflicts with (already on main) | Erasure action | Email | Session file | Status |
|---|---|---|---|---|---|
| `CH-I2-E4` | `CH-I1-E4` | Clear all memories | `noreply.ayodev@gmail.com`  | `sessions/chatgpt__conflict_i2.json` | Erased 2026-09-09 on the old account (moot). Re-injected 2026-09-09 on the new one, token "Demeanor Puritan", erasure due 2026-09-12. |
| `CH-I2-E6` | `CH-I1-E6` | Clear all chat history (bulk) | `noreply.ayodev@gmail.com` | `sessions/chatgpt__conflict_i2.json` | Re-injected 2026-09-09, token "Abacus Engine Backside Kilobyte", erasure due 2026-09-12. |

Confirmed safe to share: `CH-I2-E4`/`CH-I2-E6` don't conflict with EACH
OTHER (different blanket surfaces -- memory vs. chat history), only each
with its own sibling already on the main account.

#### `conflict_i3` (ChatGPT) -- role: I3 cells conflicting with CH-I1-E4/CH-I1-E6

| Cell | Conflicts with (already on main) | Erasure action | Email | Session file | Status |
|---|---|---|---|---|---|
| `CH-I3-E4` | `CH-I1-E4` | Clear all memories | ~~`theexperimentdummy@gmail.com`~~ **BLOCKED by Google 2026-09-09** -- moved to `olataiwo839@gmail.com` (confirmed via page HTML, also used for Gemini's `maximal_i2` group) | `sessions/chatgpt__conflict_i3.json` | Working, re-injected 2026-09-09 (token: "Starting Quantum Rescuer") |
| `CH-I3-E6` | `CH-I1-E6` | Clear all chat history (bulk) | ~~`theexperimentdummy@gmail.com`~~ **BLOCKED by Google 2026-09-09** -- moved to `olataiwo839@gmail.com` | `sessions/chatgpt__conflict_i3.json` | Working, re-injected 2026-09-09 (token: "Jaundice Supper Gauntlet") |



#### `conflict_i2` (Claude) -- role: I2 cell conflicting with CL-I1-E3

| Cell | Conflicts with (already on main) | Erasure action | Email | Session file | Status |
|---|---|---|---|---|---|
| `CL-I2-E3` | `CL-I1-E3` | Clear all memories | `dummybox90@gmail.com` | `sessions/claude__conflict_i2.json` | Working, injected 2026-09-07 |

#### `conflict_i3` (Claude) -- role: I3 cell conflicting with CL-I1-E3

| Cell | Conflicts with (already on main) | Erasure action | Email | Session file | Status |
|---|---|---|---|---|---|
| `CL-I3-E3` | `CL-I1-E3` | Clear all memories | `noreply.ayodev@gmail.com` | `sessions/claude__conflict_i3.json` | Erased 2026-09-13 (per tracking). |

#### `conflict_i2` (Copilot) -- role: I2 cells conflicting with CO-I1-E2/CO-I1-E5

| Cell | Conflicts with (already on main) | Erasure action | Email | Session file | Status |
|---|---|---|---|---|---|
| `CO-I2-E2` | `CO-I1-E2` | Delete all memory | `dummybox90@gmail.com` | `sessions/copilot__conflict_i2.json` | Working, injected 2026-09-07 |
| ~~`CO-I2-E5`~~ | `CO-I1-E5` | Privacy Dashboard | `dummybox90@gmail.com` | `sessions/copilot__conflict_i2.json` | Stale: `CO-I2-E5` moved to `recall_conflict` (row below). |


#### `conflict_i2` (Gemini) -- role: I2 cell conflicting with GE-I1-E5

| Cell | Conflicts with (already on main) | Erasure action | Email | Session file | Status |
|---|---|---|---|---|---|
| `GE-I2-E5` | `GE-I1-E5` | Delete all Saved info | `noreply.ayodev@gmail.com`  | `sessions/gemini__conflict_i2.json` | Erased 2026-09-13 (per tracking). |

### `instability` (Gemini) -- role: cells migrated off the unstable main account

| Cell | Erasure action | Email | Session file | Status |
|---|---|---|---|---|
| `GE-I1-E4` | Delete individual Saved info item | `dummybox90@gmail.com` | `sessions/gemini__instability.json` | Working, re-injected 2026-09-09 (token: "Trimming Brink") |
| `GE-I2-E2` | Delete individual Saved info item | `dummybox90@gmail.com` | `sessions/gemini__instability.json` | Working, re-injected 2026-09-09 (token: "Yodel Scheme Cinema") |

### `instability2` (Gemini) -- role: second migration off the unstable main account

| Cell | Erasure action | Email | Session file | Status |
|---|---|---|---|---|
| `GE-I1-E2` | Delete single conversation | `experimentanchor@gmail.com` | `sessions/gemini__instability2.json` | Working, re-injected 2026-09-09 (token: "Coping Quarterly") |

### `recall_conflict` (Gemini) -- role: blanket erasure that would corrupt pending recalls on the main account

| Cell | Erasure action | Email | Session file | Status |
|---|---|---|---|---|
| `GE-I1-E3` | Delete all activity | `ogunwalepelumi06@gmail.com`  | `sessions/gemini__recall_conflict.json` | Erased by hand 2026-09-13 at myactivity.google.com (Google blocks automation); no screenshots on file. |
| `GE-I2-E3` | Delete all activity | `ogunwalepelumi06@gmail.com` | `sessions/gemini__recall_conflict.json` | Erased by hand 2026-09-13 at myactivity.google.com (Google blocks automation); no screenshots on file. |

### `recall_conflict` (Copilot) -- role: same pattern -- blanket erasure that would corrupt pending recalls

| Cell | Erasure action | Email | Session file | Status |
|---|---|---|---|---|
| `CO-I1-E5` | Privacy Dashboard | `noreply.ayodev@gmail.com`  | `sessions/copilot__recall_conflict.json` | Erased 2026-09-13 (per tracking). |
| `CO-I2-E5` | Privacy Dashboard | `noreply.ayodev@gmail.com` | `sessions/copilot__recall_conflict.json` | Erased 2026-09-13 (per tracking). |

### `recall_conflict` (Claude) -- role: same pattern, proactive (not yet materialized)

| Cell | Erasure action | Email | Session file | Status |
|---|---|---|---|---|
| `CL-I1-E3` | Clear all memories | `olataiwo839@gmail.com` | `sessions/claude__recall_conflict.json` | Erased 2026-09-13 (per tracking). |

### `ui_migration_i1`/`ui_migration_i2`/`ui_migration_file` (Copilot) -- role: MAXIMAL cells moved off a Copilot new-UI conversation-history migration delay

Not an account-sharing conflict (each was already isolated) -- Microsoft's
new Copilot UI hadn't finished migrating these accounts' older
conversation history in ("Previous conversations from old Copilot take a
few minutes to appear," 0 conversations visible including the one
injected here), confirmed live 2026-09-09 and not resolved after
rechecks. Moved per direct instruction rather than keep waiting.

| Cell | Erasure action | Email | Session file(s) | Status |
|---|---|---|---|---|
| `CO-I1-E6` | MAXIMAL | `olataiwo839@gmail.com` | `sessions/copilot__ui_migration_i1.json` | Injected 2026-09-10. Erased 2026-09-29 16:30 EDT (per tracking). |
| `CO-I2-E6` | MAXIMAL | `olacoderpad@gmail.com` | `sessions/copilot__ui_migration_i2.json` | Erased 2026-09-13. |
| `CO-IF-E-MAX` | Maximal combination (all erasure mechanisms) | `ogunwalepelumi06@gmail.com` | `sessions/copilot__ui_migration_file.json` | Erased 2026-09-13. |

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


| Platform | Email | Session file | Status |
|---|---|---|---|
| ChatGPT | `astrataiwo@gmail.com` | `sessions/chatgpt__nlforget.json` | Working. Injected 138/138 2026-09-12. Verified 2026-09-23. |
| Claude | `astrataiwo@gmail.com` | `sessions/claude__nlforget.json` | Working. Injected 138/138 2026-09-12. Verified 2026-09-23. |
| Gemini | `olaoluwaboluwatife001@gmail.com` | `sessions/gemini__nlforget.json` | Working. Injected 138/138 (confirmed 2026-09-17). Session degraded 2026-09-12 and 09-13, fresh export each time. Logged out 2026-09-23, re-exported and verified same day (importer reads `_manual_export_gemini__nlforget.json`, with the underscore). |
| Copilot | `astrataiwo@gmail.com` | `sessions/copilot__nlforget.json` | Session works on `copilot.com` (re-captured 2026-09-23, verified read-only). Sending is blocked by "Verify you are human"; not bypassed, extending stealth is the user's call. `flows/copilot.py` updated for the new site (read-only parts verified); `run_tracking.json` refs converted (old URL in `injection_ref_legacy`). 13 pending cells erased by hand 2026-09-23 (deviation: `CO-NLF-I0060`). Recall probes send messages, so they are at risk (battery 2026-10-08, NL-forget 2026-10-19). |
| Perplexity | `astrataiwo@gmail.com` | `sessions/perplexity__nlforget.json` | Working. Injected 138/138 2026-09-12. Verified 2026-09-23. |
| DeepSeek | `astrataiwo@gmail.com` | `sessions/deepseek__nlforget.json` | Working (needs cookies + localStorage, see `flows/deepseek.py`). Injected 138/138 2026-09-12. Verified 2026-09-23. |

#### Testing-input interference handling (revised 2026-09-23)

All 138 prompts per platform share ONE account (5 platforms on
`astrataiwo@gmail.com`, Gemini on `olaoluwaboluwatife001@gmail.com`), so
interference between cells is handled per cell, not per account.


**Status:** 120 prompts (720 cells) were erased before 2026-09-23. The other 13
prompts were erased on 2026-09-23 on Claude, ChatGPT, Perplexity, DeepSeek and
Gemini (65 of 78 cells); Copilot's 13 wait on its login (see the Copilot row).

**Why the run prompts should not interfere with each other:** each typed sentence
names only its own referent. That is by wording and by design, not yet
independently verified live per platform; no recall has run yet, so no wide
deletion could have been observed.

