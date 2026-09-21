"""Shared paths and platform config -- this project reads the experiment
design and injection/erasure/recall text from RTBF-Prompt rather than
duplicating any of it."""

from pathlib import Path

TESTER_ROOT = Path(__file__).parent
RTBF_ROOT = TESTER_ROOT.parent
PROMPT_REPO = RTBF_ROOT / "RTBF-Prompt"

MASTER_XLSX_PATH = PROMPT_REPO / "data" / "RTBF Experiments.xlsx"
SESSIONS_DIR = TESTER_ROOT / "sessions"
TRANSCRIPTS_DIR = TESTER_ROOT / "transcripts"

# Login URLs only -- account creation is handled manually (see
# login_setup.py), not by this project. Verify/update these against the
# live sites; not yet confirmed against real DOM.
PLATFORMS = {
    "claude": "https://claude.ai/login",
    "chatgpt": "https://chatgpt.com/auth/login",
    "gemini": "https://gemini.google.com/",
    "copilot": "https://copilot.microsoft.com/",
    "perplexity": "https://www.perplexity.ai/",
    "deepseek": "https://chat.deepseek.com/sign_in",
}


def session_path(platform: str, label: str | None = None) -> Path:
    """`label` selects a secondary, independently-logged-in account for
    this platform (e.g. "maximal_i2") instead of the main
    sessions/<platform>.json -- added 2026-08-31 because MAXIMAL cells
    are deliberately account-wide/blanket erasures, and multiple MAXIMAL
    cells sharing one account would wipe each other's anchors before
    their own turn (confirmed: every platform has 2-4 MAXIMAL cells on
    what was previously a single shared account). One MAXIMAL cell per
    platform stays on the main account (schedulable last, as usual); the
    rest each need their own dedicated account via this label."""
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform: {platform!r}, expected one of {list(PLATFORMS)}")
    if label:
        return SESSIONS_DIR / f"{platform}__{label}.json"
    return SESSIONS_DIR / f"{platform}.json"


# Main-account email per platform, used by any cell NOT in
# MAXIMAL_ACCOUNT_LABEL below -- see accounts.md for how each was
# confirmed (live, via Settings/Account page or account dropdown, not
# guessed from a display name).
MAIN_ACCOUNT_EMAIL: dict[str, str] = {
    "chatgpt": "olacoderpad@gmail.com",
    "claude": "anchorexperiment@gmail.com",
    "gemini": "anchorexperiment@gmail.com",
    "copilot": "anchorexperiment@gmail.com",
    "perplexity": "anchorexperiment@gmail.com",
    "deepseek": "anchorexperiment@gmail.com",
}

# Dedicated account email per (platform, label) -- see accounts.md for the
# full per-cell breakdown and how each was confirmed. Originally MAXIMAL-
# only; extended 2026-09-07 to also cover "structural conflict" cells
# (conflict_i2/conflict_i3 labels below) -- same underlying need (this
# cell's own erasure action can't share an account with a sibling testing
# the same blanket surface), just not a MAXIMAL cell itself. Proposed
# emails, not yet set up as of this writing -- anchorexperiment+00N@gmail.com
# plus-tag pattern, same as the already-working anchorexperiment+001
# (CH-I3-E7's maximal_i3 email above).
MAXIMAL_ACCOUNT_EMAIL: dict[tuple[str, str], str] = {
    ("chatgpt", "maximal_i1"): "olabamipet@gmail.com",
    ("chatgpt", "maximal_i2"): "experimentanchor@gmail.com",
    ("chatgpt", "maximal_i3"): "anchorexperiment+001@gmail.com",
    ("chatgpt", "maximal_file"): "participantone@rtbfexperiment.com.ng",
    ("claude", "maximal_i1"): "olabamipet@gmail.com",
    ("claude", "maximal_i2"): "experimentanchor@gmail.com",
    ("claude", "maximal_i3"): "olacoderpad@gmail.com",
    ("claude", "maximal_file"): "participantone@rtbfexperiment.com.ng",
    ("gemini", "maximal_i1"): "olabamipet@gmail.com",
    # Corrected 2026-09-09: was wrongly recorded as "olacoderpad@gmail.com"
    # -- confirmed WRONG by the user (never used for any Gemini experiment;
    # likely explains why GE-I2-E6's saved-info list looked empty when
    # checked live that day -- probably the wrong account, not data loss).
    # Briefly considered reusing theexperimentdummy@gmail.com, but the
    # user opted for a brand-new dedicated account instead:
    # olataiwo839@gmail.com. GE-I2-E6 re-injected fresh here.
    ("gemini", "maximal_i2"): "olataiwo839@gmail.com",
    ("gemini", "maximal_file"): "teeola48@gmail.com",
    ("copilot", "maximal_i1"): "olabamipet@gmail.com",
    ("copilot", "maximal_i2"): "experimentanchor@gmail.com",
    ("copilot", "maximal_file"): "teeola48@gmail.com",
    ("deepseek", "maximal_i1"): "olabamipet@gmail.com",
    ("deepseek", "maximal_file"): "experimentanchor@gmail.com",
    # -- structural conflict, 2026-09-07, not yet set up --
    # CH-I2-E4/CH-I2-E6 don't conflict with EACH OTHER (different blanket
    # surfaces: memory vs. chat history) -- each only conflicts with its
    # own sibling already on the main account (CH-I1-E4/CH-I1-E6), so one
    # shared account covers both, same reasoning as CO-I2-E2/CO-I2-E5
    # below. Same for CH-I3-E4/CH-I3-E6. dummybox90@gmail.com and
    # anchorexperiment+003@gmail.com were considered but are unused here --
    # reserved for a different account need later.
    # Moved off experimenttt62@gmail.com 2026-09-09 (blocked by Google) per
    # DIRECT INSTRUCTION, despite CH-I2-E4/CH-I2-E6 already being erased --
    # accepted tradeoff: noreply.ayodev@gmail.com never saw the original
    # injection/erasure, so these two cells' October recall is no longer a
    # meaningful test (it would trivially show "no memory" regardless of
    # real model behavior) and must be recorded as VOID, not run normally.
    # See MASTER col Notes for both cells.
    ("chatgpt", "conflict_i2"): "noreply.ayodev@gmail.com",
    # Corrected 2026-09-09: theexperimentdummy@gmail.com was blocked by
    # Google (account-level block, not just an expired session -- and
    # with no recovery email/phone on a disposable dummy account, there's
    # no way to regain access if a future cookie export ever expires
    # either). Moved to olataiwo839@gmail.com (already set up for
    # Gemini's maximal_i2 group) -- CH-I3-E4/CH-I3-E6 re-injected fresh.
    ("chatgpt", "conflict_i3"): "olataiwo839@gmail.com",
    ("claude", "conflict_i2"): "dummybox90@gmail.com",
    # Moved off experimenttt62@gmail.com 2026-09-09: same Google block as
    # above. CL-I3-E3 was still injected (not yet erased), so nothing lost --
    # user supplied noreply.ayodev@gmail.com as the replacement, used
    # across all three still-pending platforms (Claude/Gemini/Copilot) that
    # depended on the blocked account.
    ("claude", "conflict_i3"): "noreply.ayodev@gmail.com",
    ("copilot", "conflict_i2"): "dummybox90@gmail.com",
    # Moved off experimenttt62@gmail.com 2026-09-09 -- same reasoning as
    # claude/conflict_i3 above. GE-I2-E5 was still injected, re-injected
    # fresh on noreply.ayodev@gmail.com.
    ("gemini", "conflict_i2"): "noreply.ayodev@gmail.com",
    # -- instability migration, 2026-09-09: GE-I1-E4/GE-I2-E2 moved off the
    # unstable anchorexperiment@gmail.com main account (repeated
    # "Something went wrong (7)" errors, an expired-cookie session that
    # returned a logged-out page instead of the real saved-info list) per
    # the user's 2026-09-08 retry-then-migrate decision.
    ("gemini", "instability"): "dummybox90@gmail.com",
    # -- second instability migration, 2026-09-09: GE-I1-E2's own
    # conversation couldn't be found on the main account (turned out to be
    # confounded by a Google reCAPTCHA network block hitting mid-search,
    # not confirmed data loss -- but the main account's repeat flakiness
    # makes it worth isolating regardless). Distinct label/account from
    # the original "instability" migration (dummybox90@gmail.com) so this
    # doesn't pile a third cell onto that account -- experimentanchor@
    # gmail.com chosen because it's never been used for any Gemini cell
    # and has proven stable (not a disposable dummy account) on
    # ChatGPT/Claude/Copilot.
    ("gemini", "instability2"): "experimentanchor@gmail.com",
    # -- recall-conflict migration, 2026-09-09: GE-I1-E3/GE-I2-E3's own
    # erasure ("Delete all activity") is account-wide on myactivity.google.com,
    # and the main account (anchorexperiment@gmail.com) has 5 OTHER cells
    # already erased but not yet recalled (GE-I1-E1, GE-I1-E5, GE-I2-E1,
    # GE-I2-E4, GE-IF-E-CONV -- recall due Oct 8-11). This is a variant of
    # the "structural conflict" pattern the original 2026-09-07 audit didn't
    # check for: it only looked for blanket-vs-blanket erasure conflicts,
    # not blanket-erasure-vs-pending-recall (running this now would wipe
    # the account's broader activity log before those 5 cells' indirect-
    # recall/R3 leakage tests run, which could suppress genuine leakage
    # rather than reflect it). Both cells share the same blanket surface,
    # so one shared dedicated account covers both (same reasoning as
    # PE-I1-E3/PE-I2-E3 sharing one "delete all threads" account).
    # olacoderpad@gmail.com was considered but the user ruled it out for
    # Gemini specifically (2026-09-09) -- ogunwalepelumi06@gmail.com
    # (user-supplied) used instead.
    ("gemini", "recall_conflict"): "ogunwalepelumi06@gmail.com",
    # -- same recall-conflict pattern found on Copilot, 2026-09-09: CO-I1-E5
    # (main account) has 7 sibling cells erased-but-not-recalled; CO-I2-E5
    # (conflict_i2 account) has its own group-mate CO-I2-E2 in the same
    # state. Both are the identical "Privacy Dashboard" blanket surface, so
    # one shared account covers both (same reasoning as GE-I1-E3/GE-I2-E3
    # above -- whichever runs first satisfies the test for both).
    # experimenttt62@gmail.com was the original choice but got blocked by
    # Google 2026-09-09 before this account was ever set up -- moved to
    # noreply.ayodev@gmail.com (user-supplied) instead, same as
    # claude/conflict_i3 and gemini/conflict_i2 above.
    ("copilot", "recall_conflict"): "noreply.ayodev@gmail.com",
    # -- proactive, not yet materialized, 2026-09-09: CL-I1-E3 (Claude main
    # account, "Clear all memories") has no erased-but-unrecalled sibling
    # YET, but will once its narrower account-mates (CL-I1-E1/E2/E4,
    # CL-I2-E1/E2/E4, CL-I3-E1/E2/E4) get erased -- the existing narrow-
    # before-broad rule only sequences erasure, not the full ~31-day
    # recall window, so isolating now avoids hitting this same problem
    # later. olataiwo839@gmail.com: never used for Claude before -- picked
    # over anchorexperiment+001@gmail.com deliberately, since that's a
    # "+"-aliased address and this project has never confirmed whether
    # Claude's signup normalizes plus-tags to the same underlying account
    # (see the open "email-aliasing risk" item in PROJECT_STATUS.md) --
    # not worth relying on unverified alias behavior for account isolation.
    ("claude", "recall_conflict"): "olataiwo839@gmail.com",
    # -- Copilot new-UI conversation-history migration delay, 2026-09-09:
    # CO-I1-E6/CO-I2-E6/CO-IF-E-MAX's original accounts (maximal_i1/i2/file)
    # hit a live Microsoft-side transition, unrelated to any account-sharing
    # conflict -- see MAXIMAL_ACCOUNT_LABEL comment above. Three distinct
    # accounts since these stay MAXIMAL (must not share with each other).
    ("copilot", "ui_migration_i1"): "olataiwo839@gmail.com",
    ("copilot", "ui_migration_i2"): "olacoderpad@gmail.com",
    ("copilot", "ui_migration_file"): "ogunwalepelumi06@gmail.com",
    # -- NL-forget-prompt study, resolved 2026-09-11 (see
    # RTBF-Prompt/PROJECT_STATUS.md's "NL-forget-prompt factorial study:
    # scope and account policy" section, superseded design -- final design
    # is 138 authoritative prompts x 6 platforms, additive to the 13
    # existing blocked_on_prompt_set cells). ONE dedicated account, reused
    # across all 6 platforms (not 6 separate accounts) -- same pattern as
    # anchorexperiment@gmail.com already being shared across Claude/Gemini/
    # Copilot/Perplexity/DeepSeek, since per-platform data is siloed
    # regardless of a shared login email. Deliberately NOT
    # anchorexperiment+003@gmail.com (the other spare on file) -- unverified
    # "+"-alias risk, same reasoning already applied to Claude's
    # recall_conflict group. Not yet signed up live on any platform as of
    # this entry, and no cell_ids reference this label yet -- the 828-cell
    # sheet/loader this label will actually serve hasn't been built. Wiring
    # this in ahead of that build so the credential mapping already exists
    # once it is.
    ("chatgpt", "nlforget"): "astrataiwo@gmail.com",
    ("claude", "nlforget"): "astrataiwo@gmail.com",
    # Corrected 2026-09-13: Gemini's nlforget account is NOT astrataiwo@gmail.com
    # -- it's a separate account, olaoluwaboluwatife001@gmail.com (user
    # correction; "Olaoluwa Boluwatife" showing as the Gemini display name was
    # wrongly assumed 2026-09-12 to just be astra's real profile name -- it's
    # actually a genuinely different account). Only Gemini deviates from the
    # single-shared-account design; the other 5 platforms are still astrataiwo.
    ("gemini", "nlforget"): "olaoluwaboluwatife001@gmail.com",
    ("copilot", "nlforget"): "astrataiwo@gmail.com",
    ("perplexity", "nlforget"): "astrataiwo@gmail.com",
    ("deepseek", "nlforget"): "astrataiwo@gmail.com",
}


def account_email(cell_id: str, platform: str) -> str:
    """Single source of truth for "which email ran this cell" -- used both
    to backfill the xlsx's Email column and to write it going forward on
    every injection. Mirrors accounts.md; keep both in sync if an account
    ever needs to change."""
    label = MAXIMAL_ACCOUNT_LABEL.get(cell_id)
    if label:
        return MAXIMAL_ACCOUNT_EMAIL.get((platform, label), "")
    return MAIN_ACCOUNT_EMAIL.get(platform, "")


# Cell -> dedicated-account label, for every MAXIMAL cell, PLUS (2026-09-07)
# every "structural conflict" cell -- a cell whose own erasure action is
# genuinely account-wide/blanket (no narrower real-product equivalent) AND
# shares its account with a sibling cell testing that SAME blanket action
# (different injection type). Whichever of the group runs first is a valid
# test; every other cell in the group would find nothing of its own left
# to erase once the first ran, so it needs the same isolation MAXIMAL cells
# get -- see PROJECT_STATUS.md's "'Structural conflict' cells identified"
# section for the full audit and rationale. The group's first/"main
# account" cell is deliberately NOT listed here (it stays on the shared
# account, same as before this fix); only the other cell(s) in each group
# need a dedicated account.
#
# Every MAXIMAL cell gets its own account -- none of them, including the
# platform's "first" one, share an account with any other cell (narrow or
# MAXIMAL) -- see session_path()'s docstring. Simplified 2026-08-31 from an
# earlier "one stays on main" design: keeping the main account entirely
# free of MAXIMAL erasures removes it from the destructive-actions-run-
# last scheduling question altogether, not just for sibling MAXIMAL cells.
MAXIMAL_ACCOUNT_LABEL: dict[str, str] = {
    "CL-I1-E5": "maximal_i1",
    "CL-I2-E5": "maximal_i2",
    "CL-I3-E5": "maximal_i3",
    "CL-IF-E-MAX": "maximal_file",
    "CH-I1-E7": "maximal_i1",
    "CH-I2-E7": "maximal_i2",
    "CH-I3-E7": "maximal_i3",
    "CH-IF-E-MAX": "maximal_file",
    "GE-I1-E6": "maximal_i1",
    "GE-I2-E6": "maximal_i2",
    "GE-IF-E-MAX": "maximal_file",
    # -- moved off maximal_i1/i2/file 2026-09-09: those accounts' Copilot
    # sessions hit a live product transition ("Previous conversations from
    # old Copilot take a few minutes to appear" -- sidebar showed 0
    # conversations, including the one injected here) that hadn't resolved
    # after multiple rechecks. Not an account-sharing conflict (each cell
    # was already isolated) -- moved per direct instruction rather than
    # keep waiting on Microsoft's migration. Each needs its own fresh
    # account since these are still MAXIMAL cells.
    "CO-I1-E6": "ui_migration_i1",
    "CO-I2-E6": "ui_migration_i2",
    "CO-IF-E-MAX": "ui_migration_file",
    "PE-I1-E6": "maximal_i1",
    "PE-I2-E6": "maximal_i2",
    "PE-IF-E-MAX": "maximal_file",
    "DE-I1-E4": "maximal_i1",
    "DE-IF-E-MAX": "maximal_file",
    # -- structural conflict, 2026-09-07, not yet set up --
    "CH-I2-E4": "conflict_i2",
    "CH-I2-E6": "conflict_i2",
    "CH-I3-E4": "conflict_i3",
    "CH-I3-E6": "conflict_i3",
    "CL-I2-E3": "conflict_i2",
    "CL-I3-E3": "conflict_i3",
    "CO-I2-E2": "conflict_i2",
    "CO-I2-E5": "conflict_i2",
    "GE-I2-E5": "conflict_i2",
    "GE-I1-E4": "instability",
    "GE-I2-E2": "instability",
    "GE-I1-E2": "instability2",
    "GE-I1-E3": "recall_conflict",
    "GE-I2-E3": "recall_conflict",
    "CO-I1-E5": "recall_conflict",
    "CO-I2-E5": "recall_conflict",
    "CL-I1-E3": "recall_conflict",
}
