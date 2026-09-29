"""Turns `expected_outcomes_draft.md` into the corrected, commitment-type expectations.

Why this exists. The draft predicted each cell as Expected PASS / FAIL / NULL and treated
any departure from a FAIL prediction as a policy contradiction. An external review (N5 in
`RTBF-Analysis/paper/review.md`) pointed out that this mixes up what a platform's text
*commits to* with what merely happens. "Deleting a conversation does not delete saved
memories" is a statement of scope: it does not promise the fact stays recoverable, so
finding the fact gone is not a contradiction of it. And 8 of the draft's 12 FAIL blocks
rested on "no policy text found" or on inference from the opposite direction, which is an
absence of a promise, not a promise of persistence.

So each cell is given a *commitment type* instead, set only from what the platform's own
published text says about the erasure action on that injection surface:

  DELETES          the text says the action removes the content
  DOES NOT DELETE  the text says the action does not reach the content (a scope statement)
  NO COMMITMENT    the text is silent; any expectation is architectural inference
  UNRELATED        the mechanism and the injection surface are architecturally separate
  NOT TESTABLE     the surface cannot be reached on this account (Perplexity Free tier)

How a verdict is derived from the type is in the master xlsx README sheet and the paper's
Methods; this file only assigns the types and their evidence.

Re-checking the draft against the platforms' pages on 2026-09-23 also corrected it in
places. The claims it made that "no policy text exists" for a chat-typed forget request
were wrong for Claude and Copilot (both document it) and, from a search extraction, for
ChatGPT; the Copilot "Granular facts editor" is not documented at all (only asking
Copilot to forget is); DeepSeek's policy does say chat history can be deleted; and the
draft grouped CH-I3-E1 (custom instructions) with the Memory cells although the Memory
forget request does not reach that field. Those are in OVERRIDES below.

    python write_expected_outcomes.py           # writes expected_outcomes.md
    python write_expected_outcomes.py --xlsx    # also fills the master xlsx (Excel closed,
                                               # erasure scheduler stopped)
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).parent
DRAFT = HERE / "expected_outcomes_draft.md"
OUTPUT = HERE / "expected_outcomes.md"
XLSX = HERE.parent / "data" / "RTBF Experiments.xlsx"

DELETES, NOT_DELETE, NO_COMMIT = "DELETES", "DOES NOT DELETE", "NO COMMITMENT"
UNRELATED, NOT_TESTABLE = "UNRELATED", "NOT TESTABLE"

# Type per draft block, keyed by the block's first cell id.
BLOCK_TYPE: dict[str, str] = {
    "CL-I1-E1": NOT_DELETE, "CL-I1-E2": DELETES, "CL-I1-E3": DELETES, "CL-I1-E4": DELETES,
    "CL-I1-E5": DELETES,
    "CH-I1-E1": DELETES, "CH-I1-E2": NOT_DELETE, "CH-I3-E2": UNRELATED, "CH-I1-E4": DELETES,
    "CH-I3-E4": UNRELATED, "CH-I1-E5": UNRELATED, "CH-I3-E5": DELETES, "CH-I1-E6": NOT_DELETE,
    "CH-I3-E6": UNRELATED, "CH-I1-E7": DELETES,
    "GE-I1-E1": NO_COMMIT, "GE-I1-E2": DELETES, "GE-I2-E2": UNRELATED, "GE-I1-E3": DELETES,
    "GE-I2-E3": UNRELATED, "GE-I1-E4": UNRELATED, "GE-I2-E4": DELETES, "GE-I1-E5": UNRELATED,
    "GE-I2-E5": DELETES, "GE-I1-E6": DELETES, "GE-I2-E6": DELETES,
    "CO-I1-E1": NO_COMMIT, "CO-I1-E2": DELETES, "CO-I1-E3": DELETES, "CO-I1-E4": NO_COMMIT,
    "CO-I1-E5": NO_COMMIT, "CO-I1-E6": DELETES,
    "PE-I1-E1": NO_COMMIT, "PE-I1-E2": DELETES, "PE-I1-E3": DELETES,
    "PE-I1-E4": NOT_TESTABLE, "PE-I1-E5": NOT_TESTABLE, "PE-I1-E6": NOT_TESTABLE,
    "DE-I1-E1": DELETES, "DE-I1-E2": DELETES, "DE-I1-E3": UNRELATED, "DE-I1-E4": DELETES,
    "CL-IF-E-CONV": NOT_DELETE, "CL-IF-E-MAX": DELETES,
    "CH-IF-E-CONV": DELETES, "CH-IF-E-MAX": DELETES,
    "GE-IF-E-CONV": DELETES, "GE-IF-E-MAX": DELETES,
    "CO-IF-E-CONV": NO_COMMIT, "CO-IF-E-MAX": DELETES,
    "PE-IF-E-CONV": DELETES, "PE-IF-E-MAX": DELETES,
    "DE-IF-E-CONV": DELETES, "DE-IF-E-MAX": DELETES,
}
# A cell whose type differs from the rest of its draft block.
# CH-I3-E1/E4 and CH-I1/I2-E5 pair ChatGPT Memory with the custom-instructions field: the Memory
# page lists custom instructions as a source Memory draws on, so "architecturally separate"
# is not safe and the documentation is silent on the pairing (decided 2026-09-24).
CELL_TYPE: dict[str, str] = {
    # FILE cells whose documentation says nothing about deleting the uploaded file (2026-09-24).
    "CO-IF-E-MAX": NO_COMMIT,  # token seen in chat text only; memory read captured no list (2026-09-24)
    "GE-IF-E-CONV": NO_COMMIT, "GE-IF-E-MAX": NO_COMMIT, "DE-IF-E-CONV": NO_COMMIT, "DE-IF-E-MAX": NO_COMMIT,
    # Extraction recorded at injection is "conversation only", so the file goes with the chat (2026-09-24).
    "CL-IF-E-CONV": DELETES,
    "CH-I3-E1": NO_COMMIT, "CH-I3-E4": NO_COMMIT, "CH-I1-E5": NO_COMMIT, "CH-I2-E5": NO_COMMIT,
    # The account's Library still held the uploaded PDF weeks after the erasure (checked by hand
    # 2026-09-24), which the retention page says a chat deletion does not remove. In both file cells
    # the token lives only in that file, so they are typed alike.
    "CH-IF-E-CONV": NOT_DELETE, "CH-IF-E-MAX": NOT_DELETE,
}


@dataclass(frozen=True)
class Override:
    """Replaces the draft's text for the given cells. `expected` and `basis` are written as
    they will appear in the xlsx (plain text); `urls` are appended to the basis."""

    cells: tuple[str, ...]
    expected: str
    basis: str
    urls: str


CLAUDE_MEMORY = "https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context"
GEMINI_MEMORY = "https://support.google.com/gemini/answer/16598469?hl=en"
COPILOT_CONTROLS = "https://support.microsoft.com/en-us/microsoft-copilot/microsoft-copilot-privacy-controls"
DEEPSEEK_POLICY = "https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html"

OVERRIDES: tuple[Override, ...] = (
    Override(
        ("CL-I1-E4", "CL-I2-E4", "CL-I3-E4"),
        "DELETES (cross-session): the documentation says a chat request to forget changes "
        "memory for the next conversation. It does not say the change applies within the "
        "same conversation.",
        "Anthropic Help Center: \"Tell Claude what you'd like it to remember, change, or "
        "forget, and the update applies to your next conversation.\" (fetched verbatim "
        "2026-09-23). Corrects the draft, which recorded no policy text for this mechanism.",
        CLAUDE_MEMORY,
    ),
    Override(
        ("GE-I1-E1", "GE-I2-E1"),
        "NO COMMITMENT: the documentation describes correcting Gemini in chat and names "
        "deleting chats as the way to remove what it remembered. It does not describe a "
        "chat request to forget as a deletion.",
        "Google Gemini Apps Help: \"Correct Gemini directly in your chat.\" and \"To delete "
        "something that Gemini remembered about you, delete all chats with this info from "
        "Gemini Apps Activity.\" (fetched verbatim 2026-09-23).",
        GEMINI_MEMORY,
    ),
    Override(
        ("GE-I1-E2", "GE-I1-E3"),
        "DELETES: the documentation names deleting the chats that hold the information as the "
        "way to remove what Gemini remembered, and notes a short delay before Gemini stops "
        "using it. Whether Gemini's automatic Memory retained the fact from a single mention "
        "is not documented; the audit treats that as a retention question (did the injection "
        "reach that surface), not as a policy prediction.",
        "Google Gemini Apps Help: \"To delete something that Gemini remembered about you, "
        "delete all chats with this info from Gemini Apps Activity.\" (fetched verbatim "
        "2026-09-23); the short-delay wording is on the same page: \"If you delete a chat, there might be a short delay before Gemini stops using it to personalize your responses.\" (fetched verbatim 2026-09-24).",
        GEMINI_MEMORY + " , https://support.google.com/gemini/answer/13278892?hl=en",
    ),
    Override(
        ("GE-I1-E6",),
        "DELETES: MAXIMAL includes the chat-deletion component (E2/E3), the documented route. "
        "The Saved-info components (E4/E5) have nothing to act on for a conversational "
        "disclosure. Whether Gemini's automatic Memory retained the fact is a retention "
        "question, not a policy prediction.",
        "Same as GE-I1-E2 and GE-I1-E3.",
        GEMINI_MEMORY,
    ),
    Override(
        ("CO-I1-E1", "CO-I2-E1"),
        "NO COMMITMENT: the documentation says conversation history can be deleted, and that "
        "deleting all Memory does not delete conversation history. It does not say whether "
        "deleting conversation history reaches Memory.",
        "Microsoft Copilot privacy controls: \"You can delete individual items from your "
        "conversation history or delete your entire conversation history in Copilot at any "
        "time.\" and, about Delete all Memory, \"Your conversation history will not be "
        "deleted.\" (the second fetched verbatim 2026-09-23). The reverse direction is not "
        "described.",
        COPILOT_CONTROLS,
    ),
    Override(
        ("CO-I1-E2", "CO-I2-E2"),
        "DELETES (same-session and cross-session): direct match, Delete all Memory removes "
        "everything Copilot stored.",
        "Microsoft Copilot privacy controls: \"To delete everything from memory in Copilot: "
        "Select your profile icon, then select Memory > Delete all Memory. Your conversation "
        "history will not be deleted.\" (fetched verbatim 2026-09-23).",
        COPILOT_CONTROLS,
    ),
    Override(
        ("CO-I1-E3", "CO-I2-E3"),
        "DELETES: the documentation says asking Copilot in chat to forget an item removes it "
        "from memory.",
        "Microsoft Copilot privacy controls (consumer Copilot): \"To delete specific items "
        "from memory, ask Copilot to forget about that information (for example, 'Forget that "
        "I like science fiction movies'). Copilot will remove that item from its memory.\" "
        "(fetched verbatim 2026-09-23). Corrects the draft, which recorded no policy text for "
        "this mechanism.",
        COPILOT_CONTROLS,
    ),
    Override(
        ("CO-I1-E4", "CO-I2-E4"),
        "NO COMMITMENT: the documentation describes deleting individual memories only by "
        "asking Copilot to forget them (E3). It does not describe a memory editor. This "
        "project's live check (flows/copilot.py) found the editor and Delete all Memory act on "
        "the same store, which is an observation, not a documented commitment.",
        "Microsoft Copilot privacy controls (fetched 2026-09-23): no sentence describes "
        "viewing, editing or deleting individual memories in a settings editor. The draft "
        "predicted a pass from the shared-store observation alone.",
        COPILOT_CONTROLS,
    ),
    Override(
        ("DE-I1-E1", "DE-I1-E2", "DE-I1-E4"),
        "DELETES (same-session and cross-session): with no separate memory store, the "
        "conversation holding the anchor is the only place it can live, and the policy says "
        "chat history can be deleted.",
        "DeepSeek Privacy Policy: \"Should you choose to do so, you may also copy or delete "
        "your chat history via your settings.\" (fetched verbatim 2026-09-23). The policy "
        "gives no retention period for deleted chat history. No memory feature exists "
        "(confirmed live).",
        DEEPSEEK_POLICY,
    ),
    Override(
        ("CH-I1-E1", "CH-I2-E1"),
        "DELETES: the documentation says you can ask ChatGPT to forget a saved memory or "
        "delete it from Memory settings. Deleting a saved memory stops its use in future "
        "personalization but does not remove mentions of it from past conversations. The page "
        "adds that it can take time for deletion and Memory updates to propagate.",
        "Wording copied from the live page on 2026-09-24. OpenAI \"Memory in ChatGPT\" (Saved "
        "memories): \"You can ask ChatGPT to forget a saved memory or delete it from Memory "
        "settings. Deleting a saved memory prevents it from being used in future "
        "personalization, but it does not remove mentions of that information from past "
        "conversations.\" Source: "
        "https://help.openai.com/en/articles/8590148-memory-in-chatgpt",
        "",
    ),
    Override(
        ("CH-I3-E1",),
        "NO COMMITMENT: the anchor lives in the custom-instructions field. The Memory "
        "documentation says that asking ChatGPT not to use information \"does not delete the "
        "underlying chat, file, email, or other source\", but it does not say whether a forget "
        "request reaches custom instructions.",
        "Wording copied from the live page on 2026-09-24. The Custom Instructions article "
        "says only that they can be edited or deleted \"for future conversations\" and never "
        "mentions Memory. The Memory article lists custom instructions among the sources "
        "Memory can draw on, but its steps for removing remembered information (memory "
        "summary, saved memories, regular and archived chats, files in Library, connected "
        "apps) do not include custom instructions, and it never says that erasing one deletes "
        "the other. Source: "
        "https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions , "
        "https://help.openai.com/en/articles/8590148-memory-in-chatgpt",
        "",
    ),
    Override(
        ("CH-I1-E2", "CH-I2-E2"),
        "DOES NOT DELETE (same-session and cross-session): the documentation says deleting "
        "the original chat does not automatically delete a separate saved memory.",
        "Wording copied from the live page on 2026-09-24. OpenAI \"Memory in ChatGPT\" (Saved "
        "memories): \"Saved memories are stored separately from chat history. Deleting the "
        "original chat does not automatically delete a separate saved memory.\" Also: "
        "\"Deleting a chat alone does not necessarily delete a separate saved memory created "
        "from that chat.\" Source: "
        "https://help.openai.com/en/articles/8590148-memory-in-chatgpt",
        "",
    ),
    Override(
        ("CH-I3-E2",),
        "UNRELATED: the custom-instructions field was never part of a conversation to delete "
        "in the first place.",
        "Wording copied from the live page on 2026-09-24. The Custom Instructions article "
        "says only that they can be edited or deleted \"for future conversations\" and never "
        "mentions Memory. The Memory article lists custom instructions among the sources "
        "Memory can draw on, but its steps for removing remembered information (memory "
        "summary, saved memories, regular and archived chats, files in Library, connected "
        "apps) do not include custom instructions, and it never says that erasing one deletes "
        "the other. Source: "
        "https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions , "
        "https://help.openai.com/en/articles/8590148-memory-in-chatgpt",
        "",
    ),
    Override(
        ("CH-I1-E4", "CH-I2-E4"),
        "DELETES (same-session and cross-session): the documentation says Delete and turn off "
        "memory deletes the remembered information shown in the summary and turns Memory off, "
        "without deleting past chats. It adds that logs of deleted saved memories may be kept "
        "for up to 30 days.",
        "Wording copied from the live page on 2026-09-24. OpenAI \"Memory in ChatGPT\" (Memory "
        "summary): \"Delete and turn off memory deletes the remembered information shown in "
        "the summary and turns Memory off. It does not delete past chats.\" Also: \"It can take "
        "time for deletion and Memory updates to propagate. OpenAI may retain logs of deleted "
        "saved memories for up to 30 days for safety and debugging purposes.\" Source: "
        "https://help.openai.com/en/articles/8590148-memory-in-chatgpt",
        "",
    ),
    Override(
        ("CH-I3-E4",),
        "NO COMMITMENT: the Memory documentation's steps for removing remembered information "
        "(memory summary, saved memories, chats, Library files, connected apps) do not "
        "include custom instructions, and it does not say whether clearing memory affects "
        "them.",
        "Wording copied from the live page on 2026-09-24. The Custom Instructions article "
        "says only that they can be edited or deleted \"for future conversations\" and never "
        "mentions Memory. The Memory article lists custom instructions among the sources "
        "Memory can draw on, but its steps for removing remembered information (memory "
        "summary, saved memories, regular and archived chats, files in Library, connected "
        "apps) do not include custom instructions, and it never says that erasing one deletes "
        "the other. Source: "
        "https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions , "
        "https://help.openai.com/en/articles/8590148-memory-in-chatgpt",
        "",
    ),
    Override(
        ("CH-I1-E5", "CH-I2-E5"),
        "NO COMMITMENT: the anchor was never typed into custom instructions, and the "
        "documentation does not say that clearing them affects saved memories or chats.",
        "Wording copied from the live page on 2026-09-24. The Custom Instructions article "
        "says only that they can be edited or deleted \"for future conversations\" and never "
        "mentions Memory. The Memory article lists custom instructions among the sources "
        "Memory can draw on, but its steps for removing remembered information (memory "
        "summary, saved memories, regular and archived chats, files in Library, connected "
        "apps) do not include custom instructions, and it never says that erasing one deletes "
        "the other. Source: "
        "https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions , "
        "https://help.openai.com/en/articles/8590148-memory-in-chatgpt",
        "",
    ),
    Override(
        ("CH-I3-E5",),
        "DELETES (same-session and cross-session): direct match — the field the anchor was "
        "typed into is cleared.",
        "Wording copied from the live page on 2026-09-24. OpenAI \"ChatGPT Custom "
        "Instructions\": \"You can edit or delete custom instructions at any time for future "
        "conversations.\" Disabling steps: \"[Optional] Delete your instructions from the "
        "relevant fields.\" Source: "
        "https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions",
        "",
    ),
    Override(
        ("CH-I1-E6", "CH-I2-E6"),
        "DOES NOT DELETE (same-session and cross-session): bulk deletion is still scoped to "
        "conversations, not Memory — same gap as E2.",
        "Wording copied from the live page on 2026-09-24. Same Memory quotes as the "
        "single-chat cells: \"Saved memories are stored separately from chat history. Deleting "
        "the original chat does not automatically delete a separate saved memory.\" The "
        "retention article covers chats only and does not mention Memory: \"When you delete a "
        "saved chat: ChatGPT removes it from your account view immediately. OpenAI schedules "
        "it for permanent deletion from its systems within 30 days\" (unless de-identified or "
        "a legal or security obligation applies). Source: "
        "https://help.openai.com/en/articles/8590148-memory-in-chatgpt , "
        "https://help.openai.com/en/articles/8983778-chat-and-file-retention-in-chatgpt",
        "",
    ),
    Override(
        ("CH-I3-E6",),
        "UNRELATED: same architectural separation as CH-I3-E2, at bulk scale.",
        "Wording copied from the live page on 2026-09-24. The Custom Instructions article "
        "says only that they can be edited or deleted \"for future conversations\" and never "
        "mentions Memory. The Memory article lists custom instructions among the sources "
        "Memory can draw on, but its steps for removing remembered information (memory "
        "summary, saved memories, regular and archived chats, files in Library, connected "
        "apps) do not include custom instructions, and it never says that erasing one deletes "
        "the other. Source: "
        "https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions , "
        "https://help.openai.com/en/articles/8590148-memory-in-chatgpt",
        "",
    ),
    Override(
        ("CH-I1-E7", "CH-I2-E7", "CH-I3-E7"),
        "DELETES (same-session and cross-session): MAXIMAL includes both E4 (effective for "
        "I1/I2's Memory-store anchor) and E5 (effective for I3's field-anchor) — whichever "
        "surface actually holds the anchor, MAXIMAL's matching component clears it.",
        "Wording copied from the live page on 2026-09-24. Combines the Memory wording of the "
        "clear-all-memories cells and the Custom Instructions wording of the "
        "clear-custom-instructions cells. Source: "
        "https://help.openai.com/en/articles/8590148-memory-in-chatgpt , "
        "https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions",
        "",
    ),
    Override(
        ("PE-I1-E1", "PE-I2-E1"),
        "NO COMMITMENT (architectural inference, same-session and cross-session): no "
        "described backend trigger for a chat-typed forget request.",
        "Wording copied from the live page on 2026-09-24. No policy text found addressing "
        "this mechanism. Neither the Self-Serve Data Deletion article nor the retention "
        "article addresses asking the chatbot to forget. Docs checked: "
        "https://www.perplexity.ai/help-center/en/articles/11564562-self-serve-data-deletion "
        ", "
        "https://www.perplexity.ai/help-center/en/articles/10354873-how-long-does-perplexity-retain-my-search-history-profile-data-and-personal-information",
        "",
    ),
    Override(
        ("PE-I1-E2", "PE-I2-E2"),
        "DELETES in practice on this Free-tier account: thread deletion removes the only "
        "place the anchor can exist, since Memory is unreachable (DECISIONS Q7). This tests "
        "thread deletion only; it does not test whether a paid-tier Memory would keep a copy.",
        "Wording copied from the live page on 2026-09-24. Perplexity Help Center, \"Self-Serve "
        "Data Deletion\" (Deleting specific Sessions): \"To remove a single thread or specific "
        "post you've created ... select \\\"Delete\\\" thread.\" The page states no undo condition "
        "for a single thread. Source: "
        "https://www.perplexity.ai/help-center/en/articles/11564562-self-serve-data-deletion",
        "",
    ),
    Override(
        ("PE-I1-E3", "PE-I2-E3"),
        "DELETES in practice on this Free-tier account: thread deletion removes the only "
        "place the anchor can exist, since Memory is unreachable (DECISIONS Q7). This tests "
        "thread deletion only; it does not test whether a paid-tier Memory would keep a copy.",
        "Wording copied from the live page on 2026-09-24. Perplexity Help Center, \"Self-Serve "
        "Data Deletion\" (Deleting all your threads): \"If you want to remove all content "
        "you've published without deleting your account ... Select \\\"Delete all threads\\\". "
        "This action cannot be undone.\" Source: "
        "https://www.perplexity.ai/help-center/en/articles/11564562-self-serve-data-deletion",
        "",
    ),
    Override(
        ("PE-I1-E4", "PE-I2-E4"),
        "NOT TESTABLE on this Free-tier account (Q7: Memory unreachable). No policy claim is "
        "made for this cell.",
        "Wording copied from the live page on 2026-09-24. Not testable on the Free-tier test "
        "account: Memory is Pro-tier-gated (DECISIONS Q7). The live retention article says "
        "nothing about Memory. The sentence recorded here before (\"Perplexity may retain a "
        "log of cleared memories for up to 30 days ...\") is not on that page, and the "
        "\"Turning off one does not affect the other\" sentence is not on the deletion page; "
        "both are removed until their source is found. Docs checked: "
        "https://www.perplexity.ai/help-center/en/articles/10354873-how-long-does-perplexity-retain-my-search-history-profile-data-and-personal-information "
        ", "
        "https://www.perplexity.ai/help-center/en/articles/11564562-self-serve-data-deletion",
        "",
    ),
    Override(
        ("PE-I1-E5", "PE-I2-E5"),
        "Same as PE-*-E4, bulk scale: NOT TESTABLE on this account.",
        "Wording copied from the live page on 2026-09-24. Not testable on the Free-tier test "
        "account: Memory is Pro-tier-gated (DECISIONS Q7). The live retention article says "
        "nothing about Memory. The sentence recorded here before (\"Perplexity may retain a "
        "log of cleared memories for up to 30 days ...\") is not on that page, and the "
        "\"Turning off one does not affect the other\" sentence is not on the deletion page; "
        "both are removed until their source is found. Docs checked: "
        "https://www.perplexity.ai/help-center/en/articles/10354873-how-long-does-perplexity-retain-my-search-history-profile-data-and-personal-information "
        ", "
        "https://www.perplexity.ai/help-center/en/articles/11564562-self-serve-data-deletion",
        "",
    ),
    Override(
        ("PE-I1-E6", "PE-I2-E6"),
        "NOT TESTABLE on this Free-tier account for the Memory-clearing components "
        "(structurally can't execute, per this project's own `_erase_maximal()` "
        "implementation); the thread-deletion components alone would show the same "
        "in-practice PASS as E2/E3, but MAXIMAL as designed cannot fully execute here.",
        "Wording copied from the live page on 2026-09-24. Not testable on the Free-tier test "
        "account: Memory is Pro-tier-gated (DECISIONS Q7). The live retention article says "
        "nothing about Memory. The sentence recorded here before (\"Perplexity may retain a "
        "log of cleared memories for up to 30 days ...\") is not on that page, and the "
        "\"Turning off one does not affect the other\" sentence is not on the deletion page; "
        "both are removed until their source is found. Docs checked: "
        "https://www.perplexity.ai/help-center/en/articles/10354873-how-long-does-perplexity-retain-my-search-history-profile-data-and-personal-information "
        ", "
        "https://www.perplexity.ai/help-center/en/articles/11564562-self-serve-data-deletion "
        "The MAXIMAL cell also rests on this project's own architecture "
        "(flows/perplexity.py).",
        "",
    ),
    Override(
        ("CH-IF-E-CONV",),
        "DOES NOT DELETE (same-session and cross-session): the documentation says deleting a "
        "chat does not delete a file that remains saved in Library. ChatGPT's Library on the "
        "cell's account still lists copies of CH-IF-E-CONV.pdf on 2026-09-24; the most recent "
        "copy, labelled as modified 2 weeks earlier, matches the injection on 2026-09-08 and "
        "outlasted the conversation's erasure on 2026-09-10.",
        "OpenAI \"Chat and file retention in ChatGPT\" (Files saved to Library), wording copied "
        "from the live page on 2026-09-24: \"Deleting a chat does not delete a file that "
        "remains saved in Library. Delete the file from Library when you also want to remove "
        "the saved Library copy.\" Observed: the account's Library lists CH-IF-E-CONV.pdf and "
        "four numbered copies on 2026-09-24, after the conversation was deleted on 2026-09-10 "
        "(screenshot: "
        "tester/transcripts/chatgpt/CH-IF-E-CONV/screenshots/manual_library_check_2026-09-24.png; "
        "dates are the Library's relative labels). Source: "
        "https://help.openai.com/en/articles/8983778-chat-and-file-retention-in-chatgpt",
        "",
    ),
    Override(
        ("CH-IF-E-MAX",),
        "DOES NOT DELETE (same-session and cross-session): the token is held only by the "
        "uploaded file. This cell's MAXIMAL erasure deletes the conversation, clears all "
        "memories and clears custom instructions, and none of these reaches a file saved in "
        "Library: the documentation says deleting a chat does not delete such a file, and "
        "lists files in Library as a separate source to remove. The memory summary after the "
        "forced read named the file but did not contain the token.",
        "OpenAI \"Chat and file retention in ChatGPT\" (Files saved to Library), wording copied "
        "from the live page on 2026-09-24: \"Deleting a chat does not delete a file that "
        "remains saved in Library. Delete the file from Library when you also want to remove "
        "the saved Library copy.\" OpenAI \"Memory in ChatGPT\" (Remove remembered information "
        "from its sources): \"Also remove the information from any other sources where it "
        "appears\" and the list includes \"files in Library\". Observed: the account's Library "
        "lists CH-IF-E-MAX.pdf and CH-IF-E-MAX(1).pdf on 2026-09-24, after the erasure on "
        "2026-09-09; the copy labelled 2 weeks ago matches the injection on 2026-09-07 "
        "(screenshot: "
        "tester/transcripts/chatgpt/CH-IF-E-MAX/screenshots/manual_library_check_2026-09-24.png; "
        "dates are the Library's relative labels). Source: "
        "https://help.openai.com/en/articles/8983778-chat-and-file-retention-in-chatgpt , "
        "https://help.openai.com/en/articles/8590148-memory-in-chatgpt",
        "",
    ),
    Override(
        ("PE-IF-E-CONV",),
        "DELETES in practice on this Free-tier account: injection never completed cleanly "
        "(blocked on a repeated Cloudflare-pattern failure at the forced-read step, "
        "2026-08-28), but per the Q7 tier-gate, no Memory extraction is possible on this "
        "account regardless — conversation deletion would remove the only place the anchor "
        "could exist.",
        "Wording copied from the live page on 2026-09-24. Perplexity Help Center, \"Self-Serve "
        "Data Deletion\" (Deleting a specific file or image): \"Files are kept for 30 days by "
        "default. To delete uploads, delete the entire session.\" Same Q7-tier-gate reasoning "
        "as the PE thread-deletion cells. Source: "
        "https://www.perplexity.ai/help-center/en/articles/11564562-self-serve-data-deletion",
        "",
    ),
    Override(
        ("PE-IF-E-MAX",),
        "Same as CONV — DELETES in practice, same tier-gating reasoning; injection also not "
        "yet completed for this cell.",
        "Wording copied from the live page on 2026-09-24. Perplexity Help Center, \"Self-Serve "
        "Data Deletion\" (Deleting a specific file or image): \"Files are kept for 30 days by "
        "default. To delete uploads, delete the entire session.\" Same Q7-tier-gate reasoning "
        "as the PE thread-deletion cells. Source: "
        "https://www.perplexity.ai/help-center/en/articles/11564562-self-serve-data-deletion",
        "",
    ),
    Override(
        ("CL-I1-E2", "CL-I2-E2", "CL-I3-E2"),
        "DELETES (same-session and cross-session): individually deleting the memory topic "
        "that stored the anchor removes it.",
        "Anthropic Help Center: memory is stored as individually addressable topics — \"See "
        "exactly what Claude remembers about you in Settings > Memory. Everything Claude "
        "remembers is listed under Topics. Select any topic to read it, then use the edit "
        "icon to change it or select 'Delete' to remove it.\" (fetched 2026-09-24) Source: "
        "https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context",
        "",
    ),
    Override(
        ("CL-I1-E3", "CL-I2-E3", "CL-I3-E3"),
        "DELETES (same-session and cross-session): a full memory reset removes everything, "
        "including the injected anchor.",
        "Anthropic Help Center: \"Reset memory: Permanently deletes all memories including "
        "project memories. Once you select this option and click 'Reset memory,' this cannot "
        "be undone.\" (fetched 2026-09-24) Source: "
        "https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context",
        "",
    ),
    Override(
        ("CL-IF-E-CONV",),
        "DELETES: this cell's extraction was recorded as \"into conversation only\" at "
        "injection, and the documentation says deleting a claude.ai chat deletes its attached "
        "files. Memory entries generated from a deleted conversation are not removed, but "
        "none was observed for this cell; the memory listing at recall will show whether one "
        "formed.",
        "Anthropic Claude Platform Docs, \"Retrieve and delete chats, files, and projects\" (an "
        "Enterprise page describing claude.ai behaviour; the test account is Free tier and "
        "the consumer Help Center does not address files): \"When a user deletes a chat in "
        "claude.ai, its message content, attached files, tool-generated files, and artifacts "
        "are deleted with it.\" (fetched 2026-09-24). Anthropic Help Center: \"When a "
        "conversation expires or is deleted, related memory entries generated from it won't "
        "be removed, but you can delete individual memories at any time.\" (fetched verbatim "
        "2026-09-23). Applied to this cell's own recorded extraction outcome. Source: "
        "https://platform.claude.com/docs/en/manage-claude/compliance-content-data , "
        "https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context",
        "",
    ),
    Override(
        ("CL-IF-E-MAX",),
        "DELETES: MAXIMAL deletes the conversation, which the documentation says deletes its "
        "attached files, and resets memory, so both places the content could be are covered.",
        "Same as CL-*-E5 and CL-IF-E-CONV. Source: "
        "https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context",
        "",
    ),
    Override(
        ("GE-IF-E-CONV",),
        "NO COMMITMENT: this cell's extraction was recorded as \"into conversation only\" at "
        "injection, so the content lives in the chat and its uploaded file. The documentation "
        "says deleting a chat deletes \"any content created in that chat (like Canvas docs and "
        "apps) and the related activity\", but no sentence says an uploaded file is deleted.",
        "Google Gemini Apps Help, \"Find & manage your recent chats\" (fetched 2026-09-24): \"If "
        "you delete a chat in pinned and recent chats, it also deletes any content created in "
        "that chat (like Canvas docs and apps) and the related activity from Gemini Apps "
        "Activity.\" The \"Upload & analyze files in Gemini Apps\" page (fetched 2026-09-24) "
        "describes a storage limit for uploads, but no sentence says deleting a chat deletes "
        "an uploaded file. Applied to this cell's own recorded extraction outcome. Source: "
        "https://support.google.com/gemini/answer/13666746?hl=en , "
        "https://support.google.com/gemini/answer/14903178?hl=en",
        "",
    ),
    Override(
        ("GE-IF-E-MAX",),
        "NO COMMITMENT: same reasoning as CONV. MAXIMAL also deletes Gemini Apps Activity, "
        "which the documentation says starts removal \"from the product and our systems\", but "
        "no sentence names an uploaded file.",
        "Same as GE-IF-E-CONV. Source: "
        "https://support.google.com/gemini/answer/13666746?hl=en , "
        "https://support.google.com/gemini/answer/13278892?hl=en , "
        "https://support.google.com/gemini/answer/14903178?hl=en",
        "",
    ),
    Override(
        ("DE-IF-E-CONV",),
        "NO COMMITMENT: this cell's extraction was recorded as \"into conversation only\" "
        "(DeepSeek has no memory feature). The policy says users may \"copy or delete your "
        "chat history via your settings\", but no sentence says deleting chat history deletes "
        "an uploaded file.",
        "DeepSeek Privacy Policy (fetched 2026-09-24): \"Should you choose to do so, you may "
        "also copy or delete your chat history via your settings.\" and \"We retain Personal "
        "Data for as long as necessary to provide our Services and for the other purposes set "
        "out in this Privacy Policy.\" Neither says an uploaded file is deleted with the chat. "
        "Applied to this cell's own recorded extraction outcome. Source: "
        "https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html",
        "",
    ),
    Override(
        ("DE-IF-E-MAX",),
        "NO COMMITMENT: same reasoning as CONV.",
        "Same as DE-IF-E-CONV. Source: "
        "https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html",
        "",
    ),
    Override(
        ("CO-IF-E-CONV",),
        "NO COMMITMENT: the token appears in the conversation text captured at injection but "
        "not in the memory list read at the same time (which held other cells' facts), so the "
        "content is in the chat and its uploaded file. The documentation says uploaded files "
        "are stored for up to 18 months and does not say that deleting a conversation removes "
        "them.",
        "Microsoft Privacy FAQ for Copilot (fetched 2026-09-24): \"If you share a file with "
        "Copilot (for example, uploading an image or document and asking Copilot to summarize "
        "it), the file will be stored securely for a short time (no longer than 18 months) "
        "and then automatically deleted.\" The page does not say that deleting a conversation "
        "removes the file. Applied to this cell's own injection transcript. Source: "
        "https://support.microsoft.com/en-us/topic/privacy-faq-for-microsoft-copilot-27b3a435-8dc9-4b55-9a4b-58eeb9647a7f",
        "",
    ),
    Override(
        ("CO-IF-E-MAX",),
        "NO COMMITMENT: at injection the token is in the conversation text, and the memory "
        "read captured no list, so a memory copy is not established. The documentation says "
        "Delete all Memory removes everything Copilot stored, but that uploaded files are "
        "stored for up to 18 months, and it does not say that deleting a conversation or "
        "memory removes them.",
        "Microsoft Copilot privacy controls: \"To delete everything from memory in Copilot: "
        "Select your profile icon, then select Memory > Delete all Memory. Your conversation "
        "history will not be deleted.\" (fetched verbatim 2026-09-23). Microsoft Privacy FAQ "
        "for Copilot (fetched 2026-09-24): \"If you share a file with Copilot (for example, "
        "uploading an image or document and asking Copilot to summarize it), the file will be "
        "stored securely for a short time (no longer than 18 months) and then automatically "
        "deleted.\" Source: "
        "https://support.microsoft.com/en-us/microsoft-copilot/microsoft-copilot-privacy-controls "
        ", "
        "https://support.microsoft.com/en-us/topic/privacy-faq-for-microsoft-copilot-27b3a435-8dc9-4b55-9a4b-58eeb9647a7f",
        "",
    ),
)

_CELL_ID = re.compile(r"[A-Z]{2}-(?:I\d|IF)-E[\w-]+")


def relabel(text: str, ctype: str) -> str:
    """Renames the draft's PASS / FAIL / NULL labels to the commitment types."""
    fail = ctype if ctype in (NOT_DELETE, NO_COMMIT) else NOT_DELETE
    text = text.replace("Expected PASS", DELETES).replace("Expected FAIL", fail)
    text = text.replace("EXPECTED-NULL", UNRELATED)
    return text.replace("N/A", NOT_TESTABLE) if ctype == NOT_TESTABLE else text


_EMPHASIS = re.compile(r"(?<![-\w])\*|\*(?![-\w])")


def _plain(text: str) -> str:
    """Drops markdown emphasis asterisks but keeps wildcards such as the * in "CL-*-E1"."""
    return _EMPHASIS.sub("", text).strip()


@dataclass
class Record:
    cell: str
    ctype: str
    expected: str
    basis: str


def build_records(draft_text: str) -> tuple[list[Record], list[tuple[str, str, list[str], list[Record]]]]:
    """Returns every cell's record, plus each draft block (heading, body, cells, records)."""
    override_for = {cell: ov for ov in OVERRIDES for cell in ov.cells}
    blocks = re.split(r"\n### ", draft_text)[1:]
    all_records: list[Record] = []
    parsed = []
    for block in blocks:
        heading = block.split("\n")[0]
        cells = _CELL_ID.findall(heading.split(" (")[0])
        expected = re.search(r"\*\*Expected outcome:\*\*\s*(.*)", block).group(1)
        basis = re.search(r"\*\*Citation basis:\*\*\s*(.*)", block).group(1)
        urls = re.search(r"\*\*Source URL\(s\):\*\*\s*(.*)", block).group(1)
        records = []
        for cell in cells:
            ctype = CELL_TYPE.get(cell) or BLOCK_TYPE[cells[0]]
            if cell in override_for:
                ov = override_for[cell]
                rec = Record(cell, ctype, ov.expected, f"{ov.basis} Source: {ov.urls}" if ov.urls else ov.basis)
            else:
                rec = Record(cell, ctype, _plain(relabel(expected, ctype)), f"{_plain(basis)} Source: {_plain(urls)}")
            records.append(rec)
        all_records += records
        parsed.append((heading, block, cells, records))
    return all_records, parsed


_STATUS = """\
**Status: corrected, not a draft.** Supersedes `expected_outcomes_draft.md`, which is kept unchanged as the input this file is generated from (`write_expected_outcomes.py`). Every cell has a *commitment type* (DELETES / DOES NOT DELETE / NO COMMITMENT / UNRELATED / NOT TESTABLE) instead of Expected PASS / FAIL / NULL, assigned only from what the platform's own published text says about the erasure action on that injection surface. The reasons and how a verdict is derived are in `write_expected_outcomes.py`'s docstring and the master xlsx README sheet.

**Corrections found when the draft was re-checked on 2026-09-23:** (1) the draft recorded "no policy text found" for a chat-typed forget request on every platform; Claude and consumer Copilot both document it (fetched verbatim), and so does ChatGPT's Memory page (ChatGPT's and Perplexity's pages return HTTP 403 to fetch, so their wording was copied by hand from the live pages on 2026-09-24); Gemini documents chat *correction* and names deleting chats as the deletion route, so it stays NO COMMITMENT; Perplexity's two pages say nothing about asking the chatbot to forget. (2) The Copilot Granular facts editor is not documented, only asking Copilot to forget is, so CO-*-E4 is NO COMMITMENT. (3) CH-I3-E1 was grouped with the Memory cells; it and the other ChatGPT pairings of Memory with the custom-instructions field (CH-I3-E4, CH-I1-E5, CH-I2-E5) are NO COMMITMENT, because the Memory page lists custom instructions as a source but says nothing about clearing one affecting the other. (4) DeepSeek's policy does state that chat history can be deleted. (5) Gemini's same-session/cross-session split was dropped: the documented route (delete the chats) has no such split, and whether Gemini's automatic Memory retained the fact from one mention is a retention question, not a policy prediction. The 13 expected outcomes previously typed into the xlsx came from dry runs (observations), not policy text, and are replaced; they remain in the git history.

**FILE SUBSTUDY cells (12):** their predictions are conditioned on the extraction outcome observed at injection ("into conversation only" / "into both"), so they depend on a measurement made before erasure.
"""


def write_markdown(draft_text: str, parsed) -> None:
    out = draft_text
    head_end = out.index("\n---\n")
    out = "# Commitment types and expected outcomes, from platform documentation\n\n" + _STATUS + out[head_end:]
    for heading, block, cells, records in parsed:
        types = {r.ctype for r in records}
        if len(types) == 1:
            type_line = records[0].ctype
        else:
            type_line = "; ".join(f"{', '.join(r.cell for r in records if r.ctype == t)}: {t}" for t in sorted(types))
        # Records that share text are written once; cells with their own text are listed apart.
        distinct: dict[tuple[str, str], list[str]] = {}
        for r in records:
            distinct.setdefault((r.expected, r.basis), []).append(r.cell)
        if len(distinct) == 1:
            expected, basis = next(iter(distinct))
            replacement = (
                f"**Commitment type:** {type_line}\n**Expected outcome:** {expected}\n"
                f"**Citation basis:** {basis}\n**Source URL(s):** see Citation basis"
            )
        else:
            replacement = f"**Commitment type:** {type_line}\n" + "\n".join(
                f"**Expected outcome ({', '.join(c)}):** {e}\n**Citation basis ({', '.join(c)}):** {b}"
                for (e, b), c in distinct.items()
            )
        new_block = re.sub(
            r"\*\*Expected outcome:\*\*.*\n\*\*Citation basis:\*\*.*\n\*\*Source URL\(s\):\*\*.*",
            lambda _m: replacement, block, count=1,
        )
        out = out.replace(block, new_block, 1)
    OUTPUT.write_text(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--xlsx", action="store_true", help="also fill the master xlsx")
    args = parser.parse_args()

    draft_text = DRAFT.read_text()
    records, parsed = build_records(draft_text)
    write_markdown(draft_text, parsed)
    counts: dict[str, int] = {}
    for r in records:
        counts[r.ctype] = counts.get(r.ctype, 0) + 1
    print(f"{len(records)} cells -> {OUTPUT.name}: {counts}")
    if args.xlsx:
        from write_expected_outcomes_xlsx import fill_workbook  # noqa: PLC0415  (kept apart: openpyxl edit)

        fill_workbook(XLSX, records)


if __name__ == "__main__":
    main()
