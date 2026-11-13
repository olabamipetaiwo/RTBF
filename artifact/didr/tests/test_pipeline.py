"""Offline pipeline tests with a fake agent; no browser. Run: python -m pytest tests/"""

from __future__ import annotations

import csv
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pipeline  # noqa: E402
from didr import config, tracking, workbook  # noqa: E402

DESIGN = ROOT / "examples" / "design.csv"
REQUESTS = ROOT / "examples" / "example_requests.csv"


@pytest.fixture()
def wb_path(tmp_path, monkeypatch):
    """A fresh workbook, run state and results folder per test."""
    path = tmp_path / "cases.xlsx"
    monkeypatch.setattr(config, "WORKBOOK_PATH", path)
    monkeypatch.setattr(config, "RESULTS_DIR", tmp_path / "results")
    monkeypatch.setattr(tracking, "STATE_PATH", tmp_path / "state.json")
    from didr import shared_files
    monkeypatch.setattr(shared_files, "LOCK_PATH", tmp_path / ".lock")
    workbook.create(path)
    import openpyxl
    wb = openpyxl.load_workbook(path)
    ws = wb[workbook.SHEET]
    with DESIGN.open(newline="") as f:
        for r, row in enumerate(csv.DictReader(f), start=2):
            for h in workbook.USER_COLUMNS:
                if row.get(h):
                    ws.cell(row=r, column=workbook.COLUMNS[h], value=row[h])
    wb.save(path)
    return path


def test_workbook_round_trip(wb_path):
    cases = list(workbook.test_cases())
    assert [c.id for c in cases][:3] == ["CH-01", "CH-02", "CH-03"]
    workbook.update_one("CH-01", {"Status": "x"})
    assert workbook.get("CH-01")["Status"] == "x"
    with pytest.raises(KeyError):
        workbook.update_one("NOPE", {"Status": "x"})


def test_generate_is_deterministic_and_unique(wb_path):
    gen = pipeline.stage("1_fact_generation", "generate_facts")
    n = gen.generate()
    first = {c.id: (c["Entity"], c["Value"], c["Disclosure sentence"]) for c in workbook.test_cases()}
    assert n == len(first)
    gen.generate(overwrite=True)
    second = {c.id: (c["Entity"], c["Value"], c["Disclosure sentence"]) for c in workbook.test_cases()}
    assert first == second
    values = [v for _, v, _ in first.values()]
    entities = [e for e, _, _ in first.values()]
    assert len(set(values)) == len(values) and len(set(entities)) == len(entities)
    for entity, value, sentence in first.values():
        assert 2 <= len(value.split()) <= 4
        assert value in sentence and entity in sentence
    for c in workbook.test_cases():
        assert c["Value"] not in c["Direct recall prompt"]
        assert c["Value"] not in c["Indirect recall prompt"]
        if c["Deletion method"] == "deletion-request prompt":
            assert c["Entity"] in c["Deletion request text"]


def test_generate_rejects_unavailable_method(wb_path):
    workbook.update_one("PE-01", {"Deletion method": "clear all saved memories"})
    gen = pipeline.stage("1_fact_generation", "generate_facts")
    with pytest.raises(ValueError, match="not available on perplexity"):
        gen.generate()


def test_sample_requests_fills_prompt_cases(wb_path):
    pipeline.stage("1_fact_generation", "generate_facts").generate()
    sampler = pipeline.stage("3_deletion", "sample_requests")
    assert sampler.keyword_group("Erase it from your database") == "backend_db"
    assert sampler.keyword_group("Delete all my personal data.") == "account_all"
    n = sampler.sample(REQUESTS, target=10, floor=2, seed=1)
    assert n == 3  # CH-01, CL-01, DE-01 use deletion-request prompts
    for c in workbook.test_cases():
        if c["Deletion method"] == "deletion-request prompt":
            assert "{entity}" not in c["Deletion request text"]
            assert "all my personal data" not in c["Deletion request text"].lower()


def test_schedule_enforces_waits(wb_path):
    tracking.mark_injected("CH-01", "https://example/chat/1")
    with pytest.raises(RuntimeError, match="not due"):
        tracking.require("CH-01", "injected", "deletion_due_at", force=False)
    tracking.require("CH-01", "injected", "deletion_due_at", force=True)
    e = tracking.get("CH-01")
    gap = datetime.fromisoformat(e["deletion_due_at"]) - datetime.fromisoformat(e["injected_at"])
    assert gap == timedelta(hours=48)
    e = tracking.mark_deleted("CH-01")
    gap = datetime.fromisoformat(e["recall_due_at"]) - datetime.fromisoformat(e["deleted_at"])
    assert gap == timedelta(days=30)


class FakePage:
    url = "https://example/chat/1"

    def __init__(self, events):
        self.events = events

    def goto(self, url):
        self.events.append(f"goto:{url}")

    def wait_for_timeout(self, ms):
        pass


class FakeFlow:
    HAS_MEMORY_UI = True
    platform = "chatgpt"

    def __init__(self, replies, memory_page):
        self.events: list[str] = []
        self.replies = replies
        self.memory_page = memory_page
        self.page = FakePage(self.events)
        self.memory_shot_path = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read_memory_settings(self):
        self.events.append("ui")
        return self.memory_page

    def new_conversation(self):
        self.events.append("new")

    def open_conversation(self, ref):
        self.events.append(f"open:{ref}")

    def send_message(self, text):
        self.events.append(f"msg:{text}")
        return self.replies.get(text, "I'm not sure what you named it.")


def test_recall_order_and_scoring(wb_path, monkeypatch):
    pipeline.stage("1_fact_generation", "generate_facts").generate()
    tc = workbook.get("CH-01")
    recall = pipeline.stage("4_recall", "recall")
    flow = FakeFlow({tc["Direct recall prompt"]: f"You called it {tc['Value']}."}, "Memory summary | Saved memories | likes tea")
    monkeypatch.setattr(recall, "open_flow", lambda agent, account: flow)
    monkeypatch.setattr(recall, "save_screenshot", lambda *a, **k: None)
    monkeypatch.setattr(recall, "evidence_dirs", lambda *a: (Path("."), Path(".")))
    monkeypatch.setattr(recall, "save_json", lambda *a, **k: None)
    tracking.mark_injected("CH-01", "https://example/chat/1")
    tracking.mark_deleted("CH-01")
    recall.recall("CH-01", force=True)

    msgs = [e for e in flow.events if e != "new" and not e.startswith("goto")]
    assert msgs == [
        "ui",
        f"msg:{tc['Indirect recall prompt']}", f"msg:{tc['Indirect recall follow-up']}",
        f"msg:{tc['Direct recall prompt']}", f"msg:{tc['Direct recall follow-up']}",
        "open:https://example/chat/1", f"msg:{tc['Direct recall prompt']}",
    ]
    tc = workbook.get("CH-01")
    assert tc["UI-based check result"] == "NOT FOUND (auto)"
    assert tc["Indirect recall result"] == "NOT FOUND (auto)"
    assert tc["Direct recall result"].startswith("TOKEN FOUND")
    assert tc["Same-conversation result"].startswith("TOKEN FOUND")  # reported separately


@pytest.mark.parametrize("results, evidence, expected", [
    ({"Direct recall result": "TOKEN FOUND (auto, direct-1)"}, None, "recall success"),
    ({"UI-based check result": "TOKEN FOUND (auto)"}, "no evidence", "recall success"),
    ({"Direct recall result": "NOT FOUND (auto)"}, "yes (notification)", "recall failed"),
    ({"Direct recall result": "NOT FOUND (auto)"}, "no evidence", "can't tell"),
    ({"Direct recall result": "PARTIAL (auto, direct-1): only Taps"}, "yes (notification)", "needs review"),
    ({"Direct recall result": "NOT FOUND (auto)"}, "review (agent confirmation)", "needs review"),
])
def test_classification_rules(results, evidence, expected):
    classify = pipeline.stage("5_classification", "classify")
    assert classify.classify_row(results, evidence) == expected


def test_same_conversation_never_counts():
    classify = pipeline.stage("5_classification", "classify")
    row = {"Direct recall result": "NOT FOUND (auto)", "Same-conversation result": "TOKEN FOUND (auto)"}
    assert classify.classify_row(row, "yes (notification)") == "recall failed"
