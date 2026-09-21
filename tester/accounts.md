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
| Gemini | `GE-I2-E6` | `olataiwo839@gmail.com` (confirmed via account dropdown, "Taiwo Ola") | `sessions/gemini__maximal_i2.json` (still needs myactivity merge before E6's activity-delete component can run) | Working, re-injected 2026-09-09 (token: "Essay Segment") |
| Copilot | `CO-I2-E6` | `experimentanchor@gmail.com`  | `sessions/copilot__maximal_i2.json`  | Working |
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
| `CH-I2-E4` | `CH-I1-E4` | Clear all memories | `noreply.ayodev@gmail.com` (user-supplied, replaced `experimenttt62@gmail.com` -- blocked by Google 2026-09-09) | `sessions/chatgpt__conflict_i2.json` | Was erased 2026-09-09 on the OLD account; that result is now moot. **Re-injected fresh 2026-09-09 on the new account** (not void -- a normal restart, same as every other migration this session): new token "Demeanor Puritan", erasure due 2026-09-12, recall ~31 days after whenever it's erased again. |
| `CH-I2-E6` | `CH-I1-E6` | Clear all chat history (bulk) | `noreply.ayodev@gmail.com` | `sessions/chatgpt__conflict_i2.json` | Same as CH-I2-E4 above -- re-injected fresh, token "Abacus Engine Backside Kilobyte", erasure due 2026-09-12. |

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
| `CL-I3-E3` | `CL-I1-E3` | Clear all memories | `noreply.ayodev@gmail.com` (user-supplied, replaced `experimenttt62@gmail.com` -- blocked by Google 2026-09-09) | `sessions/claude__conflict_i3.json` | **Not yet set up** -- needs a fresh cookie export + re-injection. Was still injected (not erased) when the block happened, nothing lost. |

#### `conflict_i2` (Copilot) -- role: I2 cells conflicting with CO-I1-E2/CO-I1-E5

| Cell | Conflicts with (already on main) | Erasure action | Email | Session file | Status |
|---|---|---|---|---|---|
| `CO-I2-E2` | `CO-I1-E2` | Delete all memory | `dummybox90@gmail.com` | `sessions/copilot__conflict_i2.json` | Working, injected 2026-09-07 |
| `CO-I2-E5` | `CO-I1-E5` | Privacy Dashboard | `dummybox90@gmail.com` | `sessions/copilot__conflict_i2.json` | Working, injected 2026-09-07 |


#### `conflict_i2` (Gemini) -- role: I2 cell conflicting with GE-I1-E5

| Cell | Conflicts with (already on main) | Erasure action | Email | Session file | Status |
|---|---|---|---|---|---|
| `GE-I2-E5` | `GE-I1-E5` | Delete all Saved info | `noreply.ayodev@gmail.com` (user-supplied, replaced `experimenttt62@gmail.com` -- blocked by Google 2026-09-09) | `sessions/gemini__conflict_i2.json` | **Not yet set up** -- session was already dead (confirmed live) when the block was found; needs a fresh cookie export + re-injection. Was still injected (not erased), nothing lost. |

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
| `GE-I1-E3` | Delete all activity | `ogunwalepelumi06@gmail.com` (user-supplied, replaced `olacoderpad@gmail.com` per user 2026-09-09) | `sessions/gemini__recall_conflict.json` | **Not yet set up** -- main account has 5 other cells erased but not yet recalled (GE-I1-E1, GE-I1-E5, GE-I2-E1, GE-I2-E4, GE-IF-E-CONV); running this blanket action there first would risk corrupting their recall results. Needs a fresh cookie export + re-injection. |
| `GE-I2-E3` | Delete all activity | `ogunwalepelumi06@gmail.com` (user-supplied, replaced `olacoderpad@gmail.com` per user 2026-09-09) | `sessions/gemini__recall_conflict.json` | Same account/reasoning as GE-I1-E3 -- shares the same blanket surface, one account covers both. **Not yet set up** -- needs a fresh cookie export + re-injection. |

### `recall_conflict` (Copilot) -- role: same pattern -- blanket erasure that would corrupt pending recalls

| Cell | Erasure action | Email | Session file | Status |
|---|---|---|---|---|
| `CO-I1-E5` | Privacy Dashboard | `noreply.ayodev@gmail.com` (user-supplied, replaced `experimenttt62@gmail.com` -- blocked by Google 2026-09-09 before this account was ever set up) | `sessions/copilot__recall_conflict.json` | **Not yet set up** -- main account has 7 cells erased but not yet recalled (CO-I1-E1/E2/E3, CO-I2-E1/E3/E4, CO-IF-E-CONV). Needs a fresh cookie export (copilot.microsoft.com + localStorage + the account.microsoft.com/privacy/copilot cross-domain merge) + re-injection. |
| `CO-I2-E5` | Privacy Dashboard | `noreply.ayodev@gmail.com` | `sessions/copilot__recall_conflict.json` | Was on `conflict_i2` (`dummybox90@gmail.com`), which conflicted with its own group-mate `CO-I2-E2` (erased, recall pending). Same account/reasoning as CO-I1-E5 -- shares the same blanket surface, one account covers both. **Not yet set up**. |

### `recall_conflict` (Claude) -- role: same pattern, proactive (not yet materialized)

| Cell | Erasure action | Email | Session file | Status |
|---|---|---|---|---|
| `CL-I1-E3` | Clear all memories | `olataiwo839@gmail.com` | `sessions/claude__recall_conflict.json` | **Not yet set up** -- no conflict yet (nothing on the Claude main account has been erased), but will become one once CL-I1-E1/E2/E4, CL-I2-E1/E2/E4, CL-I3-E1/E2/E4 are erased and awaiting recall. Isolating now to avoid hitting this later. Picked over anchorexperiment+001@gmail.com deliberately -- unverified whether Claude's signup normalizes "+"-aliases to the same account. |

### `ui_migration_i1`/`ui_migration_i2`/`ui_migration_file` (Copilot) -- role: MAXIMAL cells moved off a Copilot new-UI conversation-history migration delay

Not an account-sharing conflict (each was already isolated) -- Microsoft's
new Copilot UI hadn't finished migrating these accounts' older
conversation history in ("Previous conversations from old Copilot take a
few minutes to appear," 0 conversations visible including the one
injected here), confirmed live 2026-09-09 and not resolved after
rechecks. Moved per direct instruction rather than keep waiting.

| Cell | Erasure action | Email | Session file(s) | Status |
|---|---|---|---|---|
| `CO-I1-E6` | MAXIMAL | `olataiwo839@gmail.com` | `sessions/copilot__ui_migration_i1.json` | **Not yet set up** -- needs cookies + localStorage (Auth0-based login) for copilot.microsoft.com, plus the account.microsoft.com/privacy/copilot cross-domain merge (MAXIMAL includes the Privacy Dashboard component), + re-injection. |
| `CO-I2-E6` | MAXIMAL | `olacoderpad@gmail.com` | `sessions/copilot__ui_migration_i2.json` | Same as above, different account. **Not yet set up**. |
| `CO-IF-E-MAX` | Maximal combination (all erasure mechanisms) | `ogunwalepelumi06@gmail.com` (user-supplied, replaced `noreply.ayodev@gmail.com` per user 2026-09-09) | `sessions/copilot__ui_migration_file.json` | Same as above, different account. **Not yet set up**. |

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

**Correction, 2026-09-13**: Gemini does NOT share `astrataiwo@gmail.com`
with the other 5 platforms -- it's on a separate account,
`olaoluwaboluwatife001@gmail.com`. This was initially missed: the Gemini
display name "Olaoluwa Boluwatife" was wrongly assumed 2026-09-12 to just
be astra's real Google profile name; it's actually a genuinely different
account. User-confirmed 2026-09-13. Only Gemini deviates from the
single-shared-account design.

| Platform | Email | Session file | Status |
|---|---|---|---|
| ChatGPT | `astrataiwo@gmail.com` | `sessions/chatgpt__nlforget.json` | Working. Injection COMPLETE (138/138), 2026-09-12. |
| Claude | `astrataiwo@gmail.com` | `sessions/claude__nlforget.json` | Working. Injection COMPLETE (138/138), 2026-09-12. |
| Gemini | `olaoluwaboluwatife001@gmail.com` | `sessions/gemini__nlforget.json` | Working. Session degraded mid-run twice (2026-09-12 and 2026-09-13), each time needing a fresh cookie export -- resolved. Injection COMPLETE (138/138), confirmed 2026-09-17 via `run_tracking.json` and the NL FORGET sheet's RUN_STATUS column. |
| Copilot | `astrataiwo@gmail.com` | `sessions/copilot__nlforget.json` | Working. Needed both cookies + localStorage (Auth0-based, same pattern as DeepSeek) -- see `_manual_localstorage_copilot__nlforget.json`. Injection COMPLETE (138/138), 2026-09-12. |
| Perplexity | `astrataiwo@gmail.com` | `sessions/perplexity__nlforget.json` | Working. Injection COMPLETE (138/138), 2026-09-12. |
| DeepSeek | `astrataiwo@gmail.com` | `sessions/deepseek__nlforget.json` | Working. Needed both cookies + localStorage (`userToken`/`settingsJwt`/`__appKit_userInfo`) -- cookies alone left it unauthenticated, see `flows/deepseek.py`. Injection COMPLETE (138/138), 2026-09-12. |

#### Testing-input interference mapping (professor asked, 2026-09-17)

All 138 prompts per platform share ONE account (5 platforms on
`astrataiwo@gmail.com`, Gemini on `olaoluwaboluwatife001@gmail.com`), so
interference between cells is handled per-cell, not per-account. Each
cell's own `deletion_locus` (coded in
`RTBF-Prompt/data/nl_forget_prompts_138_final.csv`, column `deletion_locus`,
keyed by `item_id` -- that file is the full 138-row mapping, not
duplicated here) determines its handling at erasure time:

| `deletion_locus` | Count/138 | Scope | Interference handling |
|---|---:|---|---|
| `unspecified` | 49 | targets only its own referent | none needed -- unique token/referent per cell is sufficient (baseline design assumption, see `tester/CLAUDE.md`'s "Contamination control" section) |
| `memory` | 23 | targets only its own referent | same as above |
| `conversation` | 23 | targets only its own referent | same as above |
| `backend_db` | 11 | targets only its own referent | same as above |
| `prospective` | 14 | targets only its own referent | same as above |
| `account_all` | 18 | whole account | **held back, not run** -- would wipe the other 137 cells' data on the same account. See `tester/erasure_scheduler.py`'s `_is_held_back_nlf_account_all()` (added 2026-09-17). Excluded from every erasure batch until each gets its own dedicated account (still unset up); even destructive-last ordering (`_breadth_rank()`) only protects the other 120 from these 18 -- it doesn't protect the 18 from each other, since the first to run still wipes the shared account before the rest get their turn. |

**Why the 120 don't interfere with each other or the 18**: each targets
only its own token/referent -- confirmed by design, not yet independently
verified live per-platform (see project memory
`deletion-location-reconciliation`'s "handling assumes deletion_locus
coding is accurate" caveat).

**Outstanding**: the 18 `account_all` cells need their own dedicated
accounts before they can run (18 new accounts, reused across all 6
platforms per the cross-platform-reuse-is-safe finding above -- not
18-per-platform). Not yet created.

