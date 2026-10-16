"""windows_gate: the known-reds-aware judgement behind the `windows-gate` required context
(ADR-127 AMENDMENT 2, repair 1 of REFUSED-linux-first-ci-2026-10-16).

The first gate read the raw matrix conclusion and was red on every Windows-sensitive merge while a
known red existed on the Windows leg. These tests pin the verdict-shaped reading: pass on success,
pass where the base is red too, FAIL on a new red / non-test failure / missing leg / unreadable
input -- and never advisory.
"""
from __future__ import annotations

from dataclasses import dataclass

import windows_gate as wg

_KNOWN = "tests/test_archive_row_body.py::test_every_committed_record_still_proves_out"
_NEW = "tests/test_x.py::test_new"


def _out(*ids):
    return "\n".join(f"FAILED {i} - AssertionError: x" for i in ids) + "\n"


@dataclass
class Reg:
    workers: int = 4


def _compare(new=(), flagged=()):
    def fake(tip, base, registry, **kw):
        return {"new": sorted(set(tip) - set(base)) if new == "derive" else list(new),
                "flagged": [{"id": i, "bucket": "b", "note": "n"} for i in flagged],
                "signature_changed": []}
    return fake


def test_a_green_leg_passes():
    assert wg.judge("success", None, None, None)[0]


def test_a_red_leg_whose_only_reds_are_the_bases_passes(monkeypatch):
    monkeypatch.setattr(wg.kr, "compare_to_base", _compare(new="derive", flagged=[_KNOWN]))

    ok, reason = wg.judge("failure", _out(_KNOWN), _out(_KNOWN), Reg())

    assert ok, reason


def test_a_new_red_fails(monkeypatch):
    monkeypatch.setattr(wg.kr, "compare_to_base", _compare(new="derive"))

    ok, reason = wg.judge("failure", _out(_KNOWN, _NEW), _out(_KNOWN), Reg())

    assert not ok and _NEW in reason


def test_a_missing_or_cancelled_or_skipped_leg_fails():
    for conclusion in ("skipped", "cancelled", "timed_out", "absent", ""):
        assert not wg.judge(conclusion, None, None, None)[0], conclusion


def test_a_red_leg_with_unreadable_inputs_fails_closed():
    assert not wg.judge("failure", None, _out(_KNOWN), Reg())[0]          # tip log missing
    assert not wg.judge("failure", _out(_KNOWN), None, Reg())[0]          # base log missing
    assert not wg.judge("failure", _out(_KNOWN), _out(_KNOWN), None)[0]   # registry missing


def test_a_non_test_failure_fails(monkeypatch):
    monkeypatch.setattr(wg.kr, "compare_to_base", _compare())

    ok, reason = wg.judge("failure", "INTERNALERROR> boom\n" + _out(_KNOWN), _out(_KNOWN), Reg())

    assert not ok and "INTERNALERROR" in reason


def test_a_red_leg_that_names_no_test_fails():
    assert not wg.judge("failure", "something broke\n", _out(_KNOWN), Reg())[0]


def test_the_cli_exit_code_follows_the_verdict(tmp_path, capsys):
    assert wg.main(["--leg-conclusion", "success"]) == 0
    assert wg.main(["--leg-conclusion", "cancelled"]) == 1
    assert wg.main(["--leg-conclusion", "failure", "--tip-out", str(tmp_path / "none")]) == 1
    assert "FAIL" in capsys.readouterr().out
