"""Provenance table: where every number in Methods and Results comes from.

Reads paper/paper.tex between \\section{Methodology} and \\section{Discussion},
extracts every number, and looks for it in the saved outputs of the analysis
scripts (SciPy outputs in scipy_analysis/ and src/ outputs). For each paper line
the saved output that explains most of its numbers is reported as the line's
source; a number that this source does not print is listed as an exception and
must be explained either by another saved output or by an entry in MANUAL below.

Run: python -m src.number_sources   (writes docs/number_sources.md)
Rerun after any change to the paper's numbers or to a saved output.
"""
from __future__ import annotations

import collections
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper" / "paper.tex"
OUT = ROOT / "docs" / "number_sources.md"

SOURCES = (sorted((ROOT / "outputs" / "results").glob("*.md"))
           + sorted((ROOT / "outputs" / "tables").glob("*.csv"))
           + sorted((ROOT / "scipy_analysis" / "outputs" / "results").glob("*.md"))
           + sorted((ROOT / "scipy_analysis" / "outputs" / "tables").glob("*.csv"))
           + [ROOT.parent / "RTBF-Prompt" / "results_217" / "run_log.md",
              ROOT.parent / "RTBF-Prompt" / "results" / "prompt_clean.md",
              ROOT.parent / "Compare" / "Fourth Pass" / "agreement_report.md"])

# Numbers that no analysis output prints, each with the reason and the place it
# is recorded. A number is listed by its text as it appears in the paper.
MANUAL: dict[str, str] = {
    "200": "design target (planned sample size), not a result",
    "235": "raw Qualtrics rows; printed by src/screen.py get_bases() (base chain 235-218-181-177)",
    "276": "138 coded prompts x 2 coders (agreement_report.md: 138 items)",
    "798": "audit cells run: 133 prompts x 6 platforms (RTBF Experiments.xlsx NL FORGET sheet)",
    "828": "audit cells injected: 138 prompts x 6 platforms (RTBF Experiments.xlsx NL FORGET sheet)",
    "16.5": "36 / 218 never-deleted of complete respondents; both counts printed in outputs/results/screen.md",
    "62.1": "(75 + 35) / 177 bachelor's or graduate degree; counts in outputs/tables/sample_demographics.csv",
}

# Numbers that sit in a different output than the rest of their paper line.
# Each was opened and compared by hand on 2026-10-01; value = the output that prints it.
CONFIRMED: dict[str, str] = {
    "47.5": "outputs/results/calibration.md (chosen-method %, less scenario)",
    "45.2": "outputs/results/calibration.md (chosen-method %, more scenario)",
    "12.4": "outputs/results/calibration.md (calibration gap)",
    "176": "outputs/results/stats.md STEP 6 (113/176 stayed on the same method; Stuart-Maxwell sample)",
    "95": "'95% CI' label; the intervals are in outputs/results/effect_cis.md",
    "0.23": "outputs/results/effect_cis.md (willingness CI lower bound)",
    "5.06": "outputs/results/knowledge.md (mean knowledge score)",
    "3.66": "outputs/results/scenario_shift.md (protection less=3.659)",
    "3.79": "outputs/results/scenario_shift.md (protection more=3.792)",
    "0.21": "outputs/results/effect_cis.md (protection CI upper bound .211)",
    ".002": "outputs/results/scenario_shift.md (protection p_holm=.0018)",
    "0.06": "outputs/results/effect_cis.md (protection CI lower bound .059)",
    "18.42": "outputs/results/stats.md (less | effort KW H)",
    "16.98": "outputs/results/stats.md (more | effort KW H)",
    "58.5": "outputs/results/pooled_gee.md (single conversation, permanently deleted)",
    "375": "RTBF-Prompt/results/prompt_clean.md (unique phrasings)",
}

NUM = re.compile(r"(?<![\w.])[-+]?(?:\d+\.\d+|\.\d+|\d+)(?![\w])")
FRAC = re.compile(r"(\d+)\s*/\s*(\d+)")
STRIP = re.compile(r"\\cite\w*\{[^}]*\}|\\label\{[^}]*\}|\\S?\\?ref\{[^}]*\}|~\\ref\{[^}]*\}"
                   r"|\\url\{[^}]*\}|\\(?:sub)*section\{[^}]*\}")


def load_values() -> dict[Path, set[float]]:
    """Every number in each source, plus x100 (stored fractions) and a/b ratios."""
    values: dict[Path, set[float]] = {}
    for f in SOURCES:
        if not f.exists():
            continue
        text = f.read_text(errors="ignore")
        vals: set[float] = set()
        for m in NUM.finditer(text):
            x = abs(float(m.group(0)))
            vals.update((x, x * 100))
        for a, b in FRAC.findall(text):
            if int(b):
                vals.add(100 * int(a) / int(b))
        values[f] = vals
    return values


def hits(value: float, decimals: int, values: dict[Path, set[float]]) -> list[Path]:
    tol = 0.5 * 10 ** -decimals + 1e-9
    return [f for f, vals in values.items() if any(abs(x - abs(value)) < tol for x in vals)]


def main() -> None:
    lines = PAPER.read_text().split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("\\section{Methodology}"))
    end = next(i for i, l in enumerate(lines) if l.startswith("\\section{Discussion}"))
    values = load_values()

    heading = "Methodology"
    rows, exceptions = [], []
    for i in range(start, end):
        raw = lines[i]
        m = re.match(r"\\(?:sub)*section\{([^}]*)\}", raw)
        if m:
            heading = m.group(1)
        m = re.match(r"\\textbf\{([^}]*)\}", raw)
        label = m.group(1).rstrip(".") if m else None
        if raw.lstrip().startswith("%"):
            continue
        body = STRIP.sub("", raw).replace("\\%", "").replace("$", "")
        found = []
        for m in NUM.finditer(body):
            t = m.group(0).lstrip("+-")
            if re.fullmatch(r"(19|20)\d\d", t) or ("." not in t and int(float(t)) < 10):
                continue
            decimals = len(t.split(".")[1]) if "." in t else 0
            found.append((t, hits(float(t), decimals, values)))
        if not found:
            continue
        counts = collections.Counter(f for _, h in found for f in h)
        best = counts.most_common(1)[0][0] if counts else None
        loose = [t for t, h in found if not h and t not in MANUAL and t not in CONFIRMED]
        other = [f"{t} ({', '.join(sorted({x.name for x in h})[:2])})" for t, h in found
                 if h and best not in h and t not in MANUAL and t not in CONFIRMED]
        manual = [t for t, _ in found if t in MANUAL]
        rows.append((i + 1, heading, len(found), best, manual))
        if loose or other:
            exceptions.append((i + 1, heading, best, loose, other))

    total = sum(r[2] for r in rows)
    out = ["# Number sources (Methods and Results)", "",
           "Generated by `python -m src.number_sources`. For each paper line with numbers, the saved",
           "output that prints most of them. Exceptions are numbers that source does not print.", "",
           f"Lines with numbers: {len(rows)}; numbers checked: {total}; "
           f"lines with an unexplained number: {len(exceptions)}.", "",
           "## Numbers recorded by hand (not printed by any analysis output)", "",
           "| Number | Reason |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in MANUAL.items()]
    out += ["", "## Numbers printed by a different output than their line's main source (checked by hand)", "",
            "| Number | Printed by |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in CONFIRMED.items()]
    out += ["", "## Exceptions to review", "",
            "| Line | Section | Line's source | No saved output prints | Printed only by another output |",
            "|---|---|---|---|---|"]
    for ln, h, best, loose, other in exceptions:
        out.append(f"| {ln} | {h} | {best.name if best else '-'} | {', '.join(loose) or '-'} | {', '.join(other) or '-'} |")
    out += ["", "## Line to source", "", "| Line | Section | Numbers | Main source |", "|---|---|---|---|"]
    for ln, h, n, best, _ in rows:
        out.append(f"| {ln} | {h} | {n} | {best.relative_to(ROOT.parent).as_posix() if best else 'manual list'} |")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("\n".join(out) + "\n")
    print("\n".join(out[:5]))
    print("\n".join(l for l in out if l.startswith("| ") and l.split("|")[1].strip().isdigit() and int(l.split("|")[1]) in {e[0] for e in exceptions}))
    print("saved ->", OUT)


if __name__ == "__main__":
    main()
