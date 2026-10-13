"""Acknowledgment inter-rater agreement (Gwet's AC1 only).

Sources: ./Taiwo-Acknowledgment Coding.xlsx and ./Jihwan-Acknowledgment Coding.xlsx
(sheet "Acknowledgment").

Codes: complied, partial, refused, deflected, silently ignored, other, no reply.
Empty rows (UI-only erasures with no reply text) are excluded.

Writes agreement_report.md and disagreements.csv here.

Usage: python3 compute_agreement.py
"""

import csv
from collections import Counter
from pathlib import Path

import openpyxl

HERE = Path(__file__).parent
TAIWO_FILE = HERE / "Taiwo-Acknowledgment Coding.xlsx"
JIHWAN_FILE = HERE / "Jihwan-Acknowledgment Coding.xlsx"
SHEET = "Acknowledgment"
CODE_COL = 5  # column E in both workbooks


def normalize(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def load(path: Path) -> dict[str, dict]:
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[SHEET]
    d = {}
    for r in range(2, ws.max_row + 1):
        cell_id = ws.cell(r, 1).value
        if not cell_id:
            continue
        cell_id = str(cell_id).strip()
        code = normalize(ws.cell(r, CODE_COL).value)
        platform = normalize(ws.cell(r, 2).value)
        request = ws.cell(r, 3).value
        reply = ws.cell(r, 4).value
        note = ws.cell(r, 6).value if ws.max_column >= 6 else None
        d[cell_id] = {
            "code": code if code else None,
            "platform": platform,
            "request": str(request)[:200] if request else "",
            "reply": str(reply)[:200] if reply else "",
            "note": str(note).strip() if note else "",
        }
    return d


def gwet_ac1(a: list[str], b: list[str]) -> float:
    n = len(a)
    ca, cb = Counter(a), Counter(b)
    po = sum(x == y for x, y in zip(a, b)) / n
    cats = set(a) | set(b)
    if len(cats) < 2:
        return 1.0
    pi = {c: (ca[c] + cb[c]) / (2 * n) for c in cats}
    pe = sum(p * (1 - p) for p in pi.values()) / (len(cats) - 1)
    return (po - pe) / (1 - pe)


def main() -> None:
    taiwo = load(TAIWO_FILE)
    jihwan = load(JIHWAN_FILE)

    both_coded = sorted(
        cid for cid in taiwo
        if cid in jihwan and taiwo[cid]["code"] and jihwan[cid]["code"]
    )
    n = len(both_coded)

    a = [taiwo[cid]["code"] for cid in both_coded]
    b = [jihwan[cid]["code"] for cid in both_coded]

    agree = sum(x == y for x, y in zip(a, b))
    ac1 = gwet_ac1(a, b)

    # Category distribution
    all_cats = sorted(set(a) | set(b))
    dist_t = Counter(a)
    dist_j = Counter(b)

    # Confusion matrix
    confusion: dict[tuple[str, str], int] = Counter()
    for x, y in zip(a, b):
        confusion[(x, y)] += 1

    # Disagreements
    dis_rows = []
    for cid, tc, jc in zip(both_coded, a, b):
        if tc != jc:
            t_info = taiwo[cid]
            j_info = jihwan[cid]
            dis_rows.append({
                "cell_id": cid,
                "platform": t_info["platform"],
                "request": t_info["request"],
                "reply": t_info["reply"],
                "taiwo": tc,
                "jihwan": jc,
                "jihwan_note": j_info.get("note", ""),
            })

    # Per-platform breakdown
    platforms = sorted({taiwo[cid]["platform"] for cid in both_coded})
    plat_stats = {}
    for plat in platforms:
        pa = [taiwo[c]["code"] for c in both_coded if taiwo[c]["platform"] == plat]
        pb = [jihwan[c]["code"] for c in both_coded if jihwan[c]["platform"] == plat]
        p_n = len(pa)
        p_agree = sum(x == y for x, y in zip(pa, pb))
        p_ac1 = gwet_ac1(pa, pb) if p_n >= 2 else 1.0
        plat_stats[plat] = (p_n, p_agree, p_ac1)

    # Write disagreements.csv
    with (HERE / "disagreements.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cell_id", "platform", "erasure_request", "reply_excerpt",
                     "taiwo", "jihwan", "adjudicated_value", "adjudication_notes"])
        for row in dis_rows:
            w.writerow([
                row["cell_id"], row["platform"],
                row["request"], row["reply"],
                row["taiwo"], row["jihwan"], "", "",
            ])

    # Write agreement_report.md
    lines = [
        f"# Acknowledgment Inter-Rater Agreement (Gwet's AC1, n={n})",
        "",
        f"**Coders:** Taiwo, Jihwan",
        f"**Items coded:** {n} (cells with a reply to code; {len(taiwo) - n} UI-only rows excluded)",
        "",
        "## Overall",
        "",
        f"| Metric | Value |",
        f"|---|---|",
        f"| Raw agreement | {agree}/{n} ({100 * agree / n:.1f}%) |",
        f"| Gwet's AC1 | {ac1:.3f} |",
        f"| Disagreements | {len(dis_rows)} |",
        "",
        "## Category distribution",
        "",
        "| Category | Taiwo | Jihwan |",
        "|---|---|---|",
    ]
    for cat in all_cats:
        lines.append(f"| {cat} | {dist_t[cat]} | {dist_j[cat]} |")

    lines += [
        "",
        "## Per-platform agreement",
        "",
        "| Platform | n | Agreement | % | AC1 |",
        "|---|---|---|---|---|",
    ]
    for plat in platforms:
        pn, pa, pac1 = plat_stats[plat]
        lines.append(f"| {plat} | {pn} | {pa}/{pn} | {100 * pa / pn:.1f}% | {pac1:.3f} |")

    lines += [
        "",
        "## Confusion matrix (Taiwo rows x Jihwan columns)",
        "",
        "| | " + " | ".join(all_cats) + " |",
        "|---" * (len(all_cats) + 1) + "|",
    ]
    for rt in all_cats:
        vals = [str(confusion.get((rt, rc), 0)) for rc in all_cats]
        lines.append(f"| **{rt}** | " + " | ".join(vals) + " |")

    lines += [
        "",
        f"## Disagreements ({len(dis_rows)} cells)",
        "",
        "| Cell ID | Platform | Taiwo | Jihwan | Reply excerpt |",
        "|---|---|---|---|---|",
    ]
    for row in dis_rows:
        reply = row["reply"].replace("|", "/").replace("\n", " ")[:100]
        lines.append(
            f"| {row['cell_id']} | {row['platform']} | {row['taiwo']} "
            f"| {row['jihwan']} | {reply}{'...' if len(row['reply']) > 100 else ''} |"
        )
    lines.append("")

    (HERE / "agreement_report.md").write_text("\n".join(lines))

    # Console output
    print(f"n = {n}")
    print(f"Agreement: {agree}/{n} ({100 * agree / n:.1f}%)")
    print(f"Gwet's AC1: {ac1:.3f}")
    print(f"Disagreements: {len(dis_rows)}")
    print()
    for plat in platforms:
        pn, pa, pac1 = plat_stats[plat]
        print(f"  {plat:12s} {pa}/{pn} ({100 * pa / pn:.1f}%)  AC1={pac1:.3f}")


if __name__ == "__main__":
    main()
