"""Same contract as src/reporting.py's save_report(), pointed at this folder's
own outputs/ so the original outputs/results/*.md are never touched.
"""

import datetime
import os

RESULTS_DIR = "scipy_analysis/outputs/results"
GUARD_MARKER = "## DON'T CLEAR THIS"


def save_report(name: str, lines: list[str]) -> str:
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
