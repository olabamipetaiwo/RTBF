"""DIDR command line: one command per pipeline stage (see README.md)."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from didr import config, tracking, workbook  # noqa: E402


def stage(folder: str, module: str):
    """Load a stage module from its numbered folder (folder names follow the
    figure, so they are not importable as packages)."""
    path = ROOT / folder / f"{module}.py"
    spec = importlib.util.spec_from_file_location(f"didr_stage_{module}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cmd_init(a) -> None:
    path = workbook.create(overwrite=a.overwrite)
    print(f"Created {path}")
    if a.design:
        with open(a.design, newline="") as f:
            rows = [r for r in csv.DictReader(f) if r.get("Test case ID")]
        import openpyxl
        wb = openpyxl.load_workbook(path)
        ws = wb[workbook.SHEET]
        for r, row in enumerate(rows, start=2):
            for header in workbook.USER_COLUMNS:
                if row.get(header):
                    ws.cell(row=r, column=workbook.COLUMNS[header], value=row[header].strip())
        wb.save(path)
        print(f"Added {len(rows)} test cases from {a.design}")


def cmd_generate(a) -> None:
    n = stage("1_fact_generation", "generate_facts").generate(seed=a.seed, overwrite=a.overwrite)
    print(f"Generated facts for {n} test cases")


def cmd_sample(a) -> None:
    stage("3_deletion", "sample_requests").sample(
        Path(a.requests), target=a.target, floor=a.floor, seed=a.seed,
        keep_all_data_requests=a.keep_all_data_requests,
    )


def _each(ids: list[str], fn) -> None:
    failed = 0
    for tc_id in ids:
        try:
            fn(tc_id)
        except Exception as exc:
            failed += 1
            print(f"{tc_id}: FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
    if failed:
        sys.exit(1)


def cmd_inject(a) -> None:
    mod = stage("2_injection", "inject")
    _each(a.ids, mod.inject)


def cmd_delete(a) -> None:
    mod = stage("3_deletion", "delete")
    ids = a.ids or tracking.due("injected", "deletion_due_at")
    _each(ids, lambda i: mod.delete(i, force=a.force, manual=a.manual))


def cmd_recall(a) -> None:
    mod = stage("4_recall", "recall")
    ids = a.ids or tracking.due("deleted", "recall_due_at")
    _each(ids, lambda i: mod.recall(i, force=a.force))


def cmd_classify(a) -> None:
    stage("5_classification", "classify").classify()


def cmd_status(a) -> None:
    state = tracking.load()
    now = datetime.now(timezone.utc)
    for tc in workbook.test_cases():
        e = state.get(tc.id)
        if e is None:
            print(f"{tc.id}: {tc['Status'] or 'listed'}")
            continue
        due_field = {"injected": "deletion_due_at", "deleted": "recall_due_at"}.get(e["status"])
        if due_field:
            due = datetime.fromisoformat(e[due_field])
            what = "deletion" if due_field == "deletion_due_at" else "recall"
            note = f"{what} DUE" if now >= due else f"{what} due {e[due_field]}"
        else:
            note = tc["Recall outcome"] or "recalled; run classify"
        print(f"{tc.id}: {e['status']} -- {note}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create the workbook")
    s.add_argument("--design", help="CSV with Test case ID, Agent, Injection method, Deletion method, Account")
    s.add_argument("--overwrite", action="store_true")
    s.set_defaults(fn=cmd_init)

    s = sub.add_parser("generate", help="stage 1: synthetic fact generation")
    s.add_argument("--seed", type=int, default=20260824)
    s.add_argument("--overwrite", action="store_true", help="regenerate facts that already exist")
    s.set_defaults(fn=cmd_generate)

    s = sub.add_parser("sample-requests", help="stage 3 input: stratified sampling of deletion requests")
    s.add_argument("--requests", required=True, help="CSV with a 'request' column")
    s.add_argument("--target", type=int, default=120)
    s.add_argument("--floor", type=int, default=15)
    s.add_argument("--seed", type=int, default=42)
    s.add_argument("--keep-all-data-requests", action="store_true")
    s.set_defaults(fn=cmd_sample)

    s = sub.add_parser("inject", help="stage 2: data injection")
    s.add_argument("ids", nargs="+")
    s.set_defaults(fn=cmd_inject)

    s = sub.add_parser("delete", help="stage 3: data deletion (default: all due)")
    s.add_argument("ids", nargs="*")
    s.add_argument("--force", action="store_true", help="run before the 48-hour wait has passed")
    s.add_argument("--manual", action="store_true", help="record a deletion performed by hand")
    s.set_defaults(fn=cmd_delete)

    s = sub.add_parser("recall", help="stage 4: data recall (default: all due)")
    s.add_argument("ids", nargs="*")
    s.add_argument("--force", action="store_true", help="run before the 30-day wait has passed")
    s.set_defaults(fn=cmd_recall)

    s = sub.add_parser("classify", help="stage 5: recall outcome classification")
    s.set_defaults(fn=cmd_classify)

    s = sub.add_parser("status", help="show stage and due times")
    s.set_defaults(fn=cmd_status)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
