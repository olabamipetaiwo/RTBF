"""Tests for src/audit_outcomes.py: every cell of Table tab:consistency-rule and
every branch of the recoverability rule. Run from RTBF-Analysis/:

    python tests/test_audit_outcomes.py
"""

import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import audit_outcomes as ao  # noqa: E402

ALL_RECOV = (ao.RECOVERED, ao.NOT_RECOVERED, ao.INDETERMINATE, ao.PENDING_REVIEW)
INTERFACES = (ao.CHANGED, ao.UNCHANGED, ao.NOT_OBSERVABLE, None)


def verdict(commitment, interface, recov):
    return ao.policy_consistency(commitment, interface, recov)[0]


def test_deletes_row_of_the_table() -> None:
    for recov, interface in product(ALL_RECOV, INTERFACES):
        got = verdict(ao.DELETES, interface, recov)
        if recov == ao.RECOVERED or interface == ao.UNCHANGED:
            want = ao.CONTRADICTED  # "recovered, or interface unchanged"
        elif recov == ao.NOT_RECOVERED and interface in (ao.CHANGED, ao.NOT_OBSERVABLE):
            want = ao.CONSISTENT  # "not recovered, and interface not unchanged"
        else:
            want = ao.INDETERMINATE  # "otherwise"
        assert got == want, (recov, interface, got, want)


def test_does_not_delete_row_of_the_table() -> None:
    for recov, interface in product(ALL_RECOV, INTERFACES):
        got = verdict(ao.DOES_NOT_DELETE, interface, recov)
        want = ao.CONSISTENT if recov == ao.RECOVERED else ao.INDETERMINATE  # never contradicted
        assert got == want, (recov, interface, got)


def test_other_commitment_types_never_get_a_verdict() -> None:
    for commitment, recov, interface in product(("NO COMMITMENT", "UNRELATED", "NOT TESTABLE"), ALL_RECOV, INTERFACES):
        assert verdict(commitment, interface, recov) == ao.INDETERMINATE, (commitment, recov, interface)


def test_no_verdict_before_recall_or_for_file_cells() -> None:
    assert verdict(ao.DELETES, ao.UNCHANGED, ao.NOT_RECALLED) == ao.NOT_RECALLED  # even with an unchanged interface
    assert verdict(ao.DELETES, None, ao.FILE_TAXONOMY) == ao.FILE_TAXONOMY
    assert verdict(None, ao.CHANGED, ao.RECOVERED) == ao.INDETERMINATE  # commitment type missing


def test_typed_requests_have_a_not_observable_interface() -> None:
    assert ao.effective_interface_change("NL forget prompt", None) == ao.NOT_OBSERVABLE
    assert ao.effective_interface_change("NL forget command", ao.UNCHANGED) == ao.NOT_OBSERVABLE  # definition wins
    assert ao.effective_interface_change("Delete conversation", ao.CHANGED) == ao.CHANGED
    assert ao.effective_interface_change("Delete conversation", None) is None


def stat(r1=ao.NOT_FOUND, r2=ao.NA, r3=ao.NOT_FOUND):
    return {"r1": r1, "r2": r2, "r3": r3}


def test_any_find_is_recovered_whatever_the_layer() -> None:
    for retention in (None, "no_signal", "acknowledged", "denied", "shown", "claimed"):
        for probe in ao.PROBES:
            statuses = stat()
            statuses[probe] = ao.FOUND
            assert ao.recoverability(statuses, "I1", retention)[0] == ao.RECOVERED, (probe, retention)


def test_miss_counts_only_when_the_platform_kept_the_fact() -> None:
    for retention in ao.RETAINED:
        assert ao.recoverability(stat(), "I1", retention)[0] == ao.NOT_RECOVERED
    for retention in (None, "no_signal", "acknowledged", "denied"):
        assert ao.recoverability(stat(), "I1", retention)[0] == ao.INDETERMINATE, retention


def test_r2_blank_counts_for_i2_and_i3_unless_denied() -> None:
    blank_page = stat(r2=ao.NOT_FOUND)
    for injection in ("I2", "I3"):
        assert ao.recoverability(blank_page, injection, "no_signal")[0] == ao.NOT_RECOVERED, injection
        assert ao.recoverability(blank_page, injection, "denied")[0] == ao.INDETERMINATE, injection
    assert ao.recoverability(blank_page, "I1", "no_signal")[0] == ao.INDETERMINATE  # offhand mention, nothing shown
    assert ao.recoverability(blank_page, "I1", "shown")[0] == ao.NOT_RECOVERED
    # a platform with no memory page contributes nothing
    assert ao.recoverability(stat(r2=ao.NA), "I3", "no_signal")[0] == ao.INDETERMINATE


def test_pending_review_blocks_a_not_recovered_call() -> None:
    assert ao.recoverability(stat(r3=ao.PENDING), "I1", "shown")[0] == ao.PENDING_REVIEW
    assert ao.recoverability(stat(r1=ao.FOUND, r3=ao.PENDING), "I1", "shown")[0] == ao.RECOVERED  # a find wins


def test_not_recalled_and_file_cells() -> None:
    blank = {"r1": ao.NOT_RECALLED, "r2": ao.NOT_RECALLED, "r3": ao.NOT_RECALLED}
    assert ao.recoverability(blank, "I1", "shown")[0] == ao.NOT_RECALLED
    assert ao.recoverability(stat(), "FILE", None)[0] == ao.FILE_TAXONOMY


def test_probe_status_parsing() -> None:
    p = ao.probe_status
    assert p("TOKEN FOUND (auto, open-1)") == ao.FOUND
    assert p("NOT FOUND (auto)") == ao.NOT_FOUND
    assert p("N/A (no memory UI)") == ao.NA
    assert p("N/A") == ao.NA
    assert p("REVIEW (auto, attempt-1): token with a negation, refusal or question cue -- needs human review") == ao.PENDING
    assert p("PARTIAL (auto, open-2/followup): only Nutcase of the token -- needs human review") == ao.PENDING
    assert p(None) == ao.NOT_RECALLED and p("") == ao.NOT_RECALLED
    # a human review overrides the automatic label
    assert p("REVIEW (auto, attempt-1): ...", "NOT FOUND") == ao.NOT_FOUND
    assert p("REVIEW (auto, attempt-1): ...", "FOUND") == ao.FOUND
    assert p("NOT FOUND (auto)", "FOUND") == ao.FOUND
    assert p("REVIEW (auto, attempt-1): ...", "UNCLEAR") == ao.PENDING  # goes to a second reviewer
    assert p("N/A", "VERBATIM") == ao.FOUND and p("NOT FOUND (auto)", "PARAPHRASED") == ao.FOUND
    assert p("TOKEN FOUND (auto)", "ABSENT") == ao.NOT_FOUND


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
