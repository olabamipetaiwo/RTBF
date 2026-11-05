"""Scan the paper sections for terms that paper/terms.txt forbids.

Run from paper/:   python3 -I terms_lint.py
Text inside ``...'' quotes and table rows of quoted survey wording (\\ding) is skipped.
Every hit is a candidate; fix it or confirm it is quoted wording.
"""

import re
from pathlib import Path

BANNED = {
    r"respondent": "participant",
    r"\bchatbots?\b": "agent (chatbot only inside quoted survey wording)",
    r"\bforget": "delete/deletion request (forget only inside quoted prompts)",
    r"behavioral audit|technical audit": "Post-Deletion Behavioral Analysis",
    r"\beras(?:ure|ed|e)\b|\bremoval\b": "data deletion",
    r"\bmaximal\b": "the most extensive deletion",
    r"\bindeterminate\b": "unresolved / can't tell",
    r"cannot tell|can not tell": "can't tell (outcome noun)",
    r"both scenarios combined|combined scenarios": "Pooled (spelled out in captions)",
    r"\bpolic(?:y|ies)\b": "documentation (policy only for a regulation)",
    r"\btokens?\b": "synthetic fact / value",
    r"\bchecks? (?:that|whether|it)\b|\bchecked\b": "verify (check only for our UI-based check, attention checks)",
    r"came back|did not come back": "recall success / recall failed",
}
QUOTE = re.compile(r"``.*?''")

for path in sorted(Path("sections").glob("*.tex")):
    if path.name == "appendix.tex":
        continue
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if "\\ding" in line or line.lstrip().startswith("%"):
            continue
        text = QUOTE.sub("", line)
        for pattern, use in BANNED.items():
            for match in re.finditer(pattern, text, re.I):
                start = max(0, match.start() - 40)
                print(f"{path.name}:{number}: [{match.group(0)}] use {use} :: ...{text[start:match.end() + 30].strip()}")
