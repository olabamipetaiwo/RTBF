"""Injection and deletion methods (paper, Table 1) and each agent's implementation of them."""

from __future__ import annotations

AGENTS = ("chatgpt", "claude", "gemini", "copilot", "perplexity", "deepseek")

INJECTION_METHODS = {
    "prompt": "I1",
    "memory-request prompt": "I2",
    "UI action": "I3",
}

# Workbook deletion method -> agent -> the flow's ERASURE_DISPATCH key.
DELETION_METHODS: dict[str, dict[str, str]] = {
    "deletion-request prompt": {
        "chatgpt": "NL forget prompt",
        "claude": "NL forget command",
        "gemini": "NL forget prompt",
        "copilot": "NL forget command",
        "perplexity": "NL forget prompt",
        "deepseek": "NL forget prompt",
    },
    "delete a single conversation": {
        "chatgpt": "Delete conversation",
        "claude": "Delete conversation",
        "gemini": "Delete single conversation",
        "copilot": "Conversation history deletion",
        "perplexity": "Delete single thread",
        "deepseek": "Delete single conversation",
    },
    "clear all conversation history": {
        "chatgpt": "Clear all chat history (bulk)",
        "gemini": "Delete all activity",
        "perplexity": "Delete all threads",
        "deepseek": "Delete all history",
    },
    "delete a specific saved memory": {
        "claude": "Delete individual memory edit",
        "gemini": "Delete single Saved info item",
        "copilot": "Granular facts editor",
    },
    "clear all saved memories": {
        "chatgpt": "Clear all memories",
        "claude": "Clear all memories",
        "gemini": "Delete all Saved info",
        "copilot": "Delete all memory",
    },
    "use a privacy dashboard": {"copilot": "Privacy Dashboard"},
    "clear custom instructions": {"chatgpt": "Clear custom instructions"},
    "most extensive procedure": {
        "chatgpt": "MAXIMAL",
        "claude": "MAXIMAL",
        "gemini": "MAXIMAL",
        "copilot": "MAXIMAL",
        "perplexity": "Delete all threads",
        "deepseek": "MAXIMAL",
    },
}

PROMPT_DELETION_METHODS = ("deletion-request prompt",)

# Automated browsers are rejected here; do these by hand and record with --manual.
MANUAL_STEPS = {
    ("gemini", "clear all conversation history"),
    ("copilot", "use a privacy dashboard"),
}


def injection_code(method: str) -> str:
    if method not in INJECTION_METHODS:
        raise ValueError(f"unknown injection method {method!r}; expected one of {list(INJECTION_METHODS)}")
    return INJECTION_METHODS[method]


def dispatch_key(method: str, agent: str) -> str:
    if method not in DELETION_METHODS:
        raise ValueError(f"unknown deletion method {method!r}; expected one of {list(DELETION_METHODS)}")
    if agent not in DELETION_METHODS[method]:
        raise ValueError(f"deletion method {method!r} is not available on {agent}")
    return DELETION_METHODS[method][agent]
