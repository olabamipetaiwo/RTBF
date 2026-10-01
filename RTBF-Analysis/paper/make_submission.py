#!/usr/bin/env python3
"""Build the anonymous submission copy of paper.tex.

paper.tex is the working file: it keeps author notes, TODOs and the real
author block as comments. The submitted source must not leak identity, so
this script writes paper_submission.tex with every full-line comment removed
and then checks the result.

Checks (any failure exits non-zero, so a bad copy is never mistaken for a
clean one):
  * no unwritten placeholder text (TBWL) is left in the output;
  * the submission-number placeholder \\#XXX is replaced (pass --number);
  * no author name, email, affiliation or IRB identifier appears anywhere in
    the output, including inline comments and the \\hypersetup metadata.

Warnings (reported, not failures): inline comments that were kept, because a
trailing % can be load-bearing in LaTeX, and the count of TODO notes that
were stripped, so removing them does not hide unfinished work.

Usage:
    python make_submission.py [--number 123] [--src paper.tex] [--out paper_submission.tex]
"""

import argparse
import re
import sys
from pathlib import Path

# Identity strings that must never reach the submitted source. Full names only
# for people: bare surnames such as "Li" or "Wang" occur in citations.
IDENTITY_PATTERNS = {
    "author name": r"Taiwo|Olabamipe|Xueqiang|Yao Li|Jihwan",
    "email address": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "affiliation": r"Central Florida|\bUCF\b",
    "IRB identifier": r"MOD\d{5,}",
}
PLACEHOLDER = re.compile(r"TBWL")
SUBMISSION_NUMBER = r"\#XXX"
INLINE_COMMENT = re.compile(r"(?<!\\)%(.+)$")


def strip_full_line_comments(lines: list[str]) -> tuple[list[str], int]:
    kept, todos = [], 0
    for line in lines:
        if line.lstrip().startswith("%"):
            todos += "TODO" in line
            continue
        kept.append(line)
    return kept, todos


def check(text: str, number: str | None) -> list[str]:
    problems = []
    if PLACEHOLDER.search(text):
        count = len(PLACEHOLDER.findall(text))
        problems.append(f"{count} unwritten placeholder(s) (TBWL) in the output")
    if SUBMISSION_NUMBER in text:
        problems.append(f"submission number {SUBMISSION_NUMBER} not replaced (pass --number)")
    for label, pattern in IDENTITY_PATTERNS.items():
        for lineno, line in enumerate(text.splitlines(), 1):
            for match in re.finditer(pattern, line):
                problems.append(f"{label} '{match.group(0)}' at output line {lineno}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--src", type=Path, default=Path("paper.tex"))
    ap.add_argument("--out", type=Path, default=Path("paper_submission.tex"))
    ap.add_argument("--number", help="HotCRP submission number to replace \\#XXX")
    args = ap.parse_args()

    lines = args.src.read_text(encoding="utf-8").splitlines()
    kept, todos = strip_full_line_comments(lines)
    text = "\n".join(kept) + "\n"
    if args.number:
        text = text.replace(SUBMISSION_NUMBER, rf"\#{args.number}")
    args.out.write_text(text, encoding="utf-8")

    inline = [
        (i, m.group(0).strip())
        for i, line in enumerate(text.splitlines(), 1)
        if (m := INLINE_COMMENT.search(line))
    ]
    print(f"{args.src} -> {args.out}: {len(lines)} lines in, {len(kept)} out")
    print(f"stripped {len(lines) - len(kept)} full-line comments ({todos} were TODO notes)")
    for lineno, comment in inline:
        print(f"WARNING inline comment kept at output line {lineno}: {comment[:70]}")

    problems = check(text, args.number)
    for problem in problems:
        print(f"FAIL {problem}")
    print("OK: clean submission copy" if not problems else f"{len(problems)} problem(s): do not submit")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
