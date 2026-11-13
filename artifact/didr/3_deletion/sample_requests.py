"""Stage 3 input: group deletion requests by keyword and draw a stratified random sample."""

from __future__ import annotations

import csv
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

from didr import config, methods, workbook

GROUP_PATTERNS: list[tuple[str, str]] = [
    ("backend_db", r"\b(database|data ?base|server|backend|back-end|training (data|set)|all available files|"
                   r"all files|private and public|wherever .*stored|everywhere|third[- ]part|from (your|the) system)\b"),
    ("account_all", r"\b(all (my|the)? ?(personal )?(data|information|info)|everything (you|about)|all data about me|"
                    r"my account|entire account|delete .*account|close .*account|all (my )?location|all the data|"
                    r"any (and all|data)|all personal)\b"),
    ("memory", r"\b(memory|remember|memoris?ed|memoriz?ed|saved|stored?|what you know about me|you'?ve stored|"
               r"retain|keep on file|you have (for|on|about) me|collected about me|have (for|about) me)\b"),
    ("prospective", r"\b(don'?t (use|store|keep|save)|do not (use|store|keep|save|reference)|going forward|in future|"
                    r"future conversation|stop (storing|keeping|using)|no longer)\b"),
    ("conversation", r"\b((this|that|our|the|previous|current|prior) (chat|conversation|thread|session)|"
                     r"conversation (we|i) (just )?had|conversation (on|about)|chat history|(conversation |chat )?history|"
                     r"what i (just )?(sent|said|typed|shared|submitted|mentioned)|this message|"
                     r"from (this |the )?(chat|history|conversation)|from here)\b"),
]
ALL_DATA_GROUP = "account_all"  # would erase other test cases on a shared account


def keyword_group(request: str) -> str:
    for name, pattern in GROUP_PATTERNS:
        if re.search(pattern, request, flags=re.I):
            return name
    return "unspecified"


def stratified_sample(rows: list[dict], target: int, floor: int, seed: int) -> list[dict]:
    """Proportional allocation with a per-group minimum of `floor`."""
    rng = random.Random(seed)
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row["group"]].append(row)
    picked = []
    for name in sorted(groups):
        members = groups[name]
        k = len(members) if len(members) <= floor else max(floor, round(target * len(members) / len(rows)))
        picked.extend(rng.sample(members, min(k, len(members))))
    rng.shuffle(picked)
    return picked


def load_requests(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        if "request" not in (reader.fieldnames or []):
            raise SystemExit(f"{path}: needs a 'request' column")
        texts = [r["request"].strip() for r in reader if r["request"].strip()]
    unique = {" ".join(t.casefold().split()): t for t in reversed(texts)}
    return [{"request": t, "group": keyword_group(t)} for t in reversed(unique.values())]


def sample(requests_csv: Path, target: int = 120, floor: int = 15, seed: int = 42,
           keep_all_data_requests: bool = False, path: Path | None = None) -> int:
    rows = load_requests(requests_csv)
    picked = stratified_sample(rows, target, floor, seed)
    if not keep_all_data_requests:
        picked = [r for r in picked if r["group"] != ALL_DATA_GROUP]
    _save_sample(picked)

    targets = [tc for tc in workbook.test_cases(path) if tc["Deletion method"] in methods.PROMPT_DELETION_METHODS]
    if missing := [tc.id for tc in targets if not tc["Entity"]]:
        raise SystemExit(f"Run `generate` first; no entity yet for {missing[:5]}")
    updates = {
        tc.id: {"Deletion request text": row["request"].replace("{entity}", tc["Entity"])}
        for tc, row in zip(targets, picked)
    }
    if updates:
        workbook.update(updates, path)
    counts = Counter(r["group"] for r in picked)
    print(f"Sampled {len(picked)} of {len(rows)} requests ({', '.join(f'{g} {n}' for g, n in sorted(counts.items()))}); "
          f"{len(updates)} of {len(targets)} prompt-based test cases filled")
    return len(updates)


def _save_sample(picked: list[dict]) -> None:
    out = config.RESULTS_DIR / "sampled_requests.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["item", "request", "group"])
        writer.writeheader()
        writer.writerows({"item": f"R{i:04d}", **row} for i, row in enumerate(picked, start=1))
