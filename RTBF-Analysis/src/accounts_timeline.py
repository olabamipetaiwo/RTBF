"""
Accounts, case allocation and injection/deletion/recall windows for the 865 DIDR test cases
(paper task A1: Methods, "accounts, sequencing and configuration").

Base: outputs/tables/audit_outcomes_provisional.csv restricted to the 865 test cases that carry a
recall outcome (recall success, recall failed, can't tell), the same base as Table 4. The account
for each case comes from tester/config.py (account_email / MAXIMAL_ACCOUNT_LABEL), the single
source the tester used when it ran the case; typed-request (NL FORGET) cases ran on the
dedicated "nlforget" accounts. An account is one (agent, email) pair: the same email on two
agents is two separate accounts. Timestamps come from tester/data/run_tracking.json.

No email addresses are printed: accounts are reported by role only (the paper must stay anonymous).

    .venv/bin/python -m src.accounts_timeline
"""

import json
import sys
from pathlib import Path

import pandas as pd

from src.reporting import save_report

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tester"))
import config as tester_config  # noqa: E402

TABLE = "outputs/tables/audit_outcomes_provisional.csv"
TRACKING = ROOT / "tester" / "data" / "run_tracking.json"
OUTCOMES = {"RECOVERED", "NOT RECOVERED", "INDETERMINATE"}

ROLE = {
    "main": "main (shared by unrelated cases)",
    "nlforget": "typed-request study",
    "maximal_i1": "full deletion procedure",
    "maximal_i2": "full deletion procedure",
    "maximal_i3": "full deletion procedure",
    "maximal_file": "full deletion procedure (file upload)",
    "conflict_i2": "account-wide deletion shared with another case",
    "conflict_i3": "account-wide deletion shared with another case",
    "recall_conflict": "account-wide deletion that would reach pending recalls",
    "instability": "moved off an unstable account",
    "instability2": "moved off an unstable account",
    "ui_migration_i1": "moved after the Copilot interface migration",
    "ui_migration_i2": "moved after the Copilot interface migration",
    "ui_migration_file": "moved after the Copilot interface migration",
}


def case_accounts() -> pd.DataFrame:
    d = pd.read_csv(TABLE)
    d = d[d.recoverability.isin(OUTCOMES)].copy()
    d["sheet"] = d["sheet"].str.strip()
    nlf = d["sheet"].eq("NL FORGET")
    d["label"] = d["cell_id"].map(tester_config.MAXIMAL_ACCOUNT_LABEL).fillna("main")
    d.loc[nlf, "label"] = "nlforget"
    d["email"] = [
        tester_config.MAXIMAL_ACCOUNT_EMAIL.get((p, "nlforget"), "") if n
        else tester_config.account_email(c, p)
        for c, p, n in zip(d["cell_id"], d["platform"], nlf)
    ]
    d["account"] = d["platform"] + "|" + d["email"]
    d["role"] = d["label"].map(ROLE)
    return d


def timeline(d: pd.DataFrame) -> pd.DataFrame:
    track = json.loads(TRACKING.read_text())
    rows = []
    for cell in d["cell_id"]:
        t = track.get(cell, {})
        rows.append({"cell_id": cell, **{k: t.get(k) for k in ("injected_at", "erased_at", "recalled_at")}})
    t = pd.DataFrame(rows)
    for c in ("injected_at", "erased_at", "recalled_at"):
        t[c] = pd.to_datetime(t[c], utc=True, format="ISO8601")
    return d.merge(t, on="cell_id", how="left")


def main() -> None:
    d = timeline(case_accounts())
    lines = [f"Base: {len(d)} test cases with a recall outcome ({TABLE})."]

    if (d["email"] == "").any():
        lines.append(f"WARNING: {int((d['email'] == '').sum())} cases have no account email: "
                     f"{sorted(d.loc[d['email'] == '', 'cell_id'])[:10]}")

    lines += ["", "Accounts per agent (one account = one agent + one email):"]
    for p, g in d.groupby("platform"):
        lines.append(f"  {p}: {g['account'].nunique()} accounts, {len(g)} cases")
    lines.append(f"  total: {d['account'].nunique()} accounts")

    lines += ["", "Cases per account, by role:"]
    by_acc = (d.groupby(["platform", "role", "account"]).size().rename("cases").reset_index())
    for (p, r), g in by_acc.groupby(["platform", "role"]):
        sizes = sorted(g["cases"].tolist(), reverse=True)
        lines.append(f"  {p} | {r}: {len(g)} account(s), cases per account {sizes}")

    lines += ["", "Windows (UTC dates):"]
    for c in ("injected_at", "erased_at", "recalled_at"):
        s = d[c].dropna()
        lines.append(f"  {c}: {s.min():%Y-%m-%d} to {s.max():%Y-%m-%d} ({len(s)} of {len(d)} cases have a timestamp)")
    for sheet, g in d.groupby("sheet"):
        lines.append(f"  {sheet}: injected {g['injected_at'].min():%Y-%m-%d} to {g['injected_at'].max():%Y-%m-%d}; "
                     f"recalled {g['recalled_at'].min():%Y-%m-%d} to {g['recalled_at'].max():%Y-%m-%d}")

    gap_del = (d["erased_at"] - d["injected_at"]).dt.total_seconds() / 3600
    gap_rec = (d["recalled_at"] - d["erased_at"]).dt.total_seconds() / 86400
    lines += [
        "",
        "Intervals (the paper claims deletion >= 48 h after injection and recall >= 30 days after deletion):",
        f"  injection -> deletion: min {gap_del.min():.1f} h, median {gap_del.median():.1f} h, "
        f"cases under 48 h: {int((gap_del < 48).sum())} (missing {int(gap_del.isna().sum())})",
        f"  deletion -> recall: min {gap_rec.min():.1f} days, median {gap_rec.median():.1f} days, "
        f"cases under 30 days: {int((gap_rec < 30).sum())} (missing {int(gap_rec.isna().sum())})",
    ]
    d = d.assign(del_h=gap_del.round(1), rec_days=gap_rec.round(1))
    short = d.loc[(gap_del < 48) | (gap_rec < 30), ["cell_id", "platform", "del_h", "rec_days"]]
    no_recall = d.loc[d["recalled_at"].isna()]
    lines.append(f"  cases without a recall timestamp: {len(no_recall)} "
                 f"({no_recall['platform'].value_counts().to_dict()}; "
                 f"placeholder-filled: {int(no_recall['provisional_fill'].eq('yes').sum())})")
    if not short.empty:
        lines += ["  cases breaking an interval:"] + [f"    {r.cell_id} ({r.platform}): deletion after {r.del_h} h, recall after {r.rec_days} days"
                                                   for r in short.itertuples()]
    print(save_report("accounts_timeline", lines))


if __name__ == "__main__":
    main()
