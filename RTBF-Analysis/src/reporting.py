"""Shared helper so every step script saves its terminal output for reproducibility.

Usage pattern: build up the same lines you print to the terminal, then call
save_report(script_name, lines) once at the end of the script's __main__ block.
"""

import datetime
import os

RESULTS_DIR = "outputs/results"
GUARD_MARKER = "## DON'T CLEAR THIS"


def save_report(name: str, lines: list[str]) -> str:
    """Write `lines` to outputs/results/<name>.md, prefixed with a run timestamp.

    Content is wrapped in a fenced code block so table alignment from
    pandas .to_string() output renders correctly instead of being reflowed.

    If the file already has a "## DON'T CLEAR THIS" section (hand-written
    interpretation notes), that section is carried over verbatim instead of
    being overwritten by the fresh run.
    """
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, f"{name}.md")
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")

    preserved = ""
    if os.path.exists(path):
        with open(path) as f:
            existing = f.read()
        marker_idx = existing.find(GUARD_MARKER)
        if marker_idx != -1:
            preserved = existing[marker_idx:].rstrip()

    with open(path, "w") as f:
        f.write(f"# {name}\n\n")
        f.write(f"_Run at {timestamp}_\n\n")
        f.write("```text\n")
        f.write("\n".join(lines) + "\n")
        f.write("```\n")
        if preserved:
            f.write("\n" + preserved + "\n")

    return path
