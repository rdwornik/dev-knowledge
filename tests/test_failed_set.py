"""Batch G — the stdlib failed-set reader that delta-A2 acceptance compares against.

The tests that matter here are the NEGATIVE ones. This reader's whole job is to make "nothing
was failing" and "nothing was measured" distinguishable, so the absence case is the property,
not an edge case.
"""
from __future__ import annotations

import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import failed_set as fs  # noqa: E402


def _cache(tmp_path, nodeids):
    p = tmp_path / "lastfailed"
    p.write_text(json.dumps({n: True for n in nodeids}, indent=2),
                 encoding="utf-8", newline="\n")
    return p


def test_an_absent_cache_RAISES_rather_than_reporting_an_empty_set(tmp_path):
    """The load-bearing negative: an empty base set would let any lane 'prove' it broke nothing."""
    with pytest.raises(fs.FailedSetError, match="absent"):
        fs.read_lastfailed(tmp_path / "never-written")


def test_a_cache_that_is_not_a_mapping_FAILS_rather_than_degrading_to_zero(tmp_path):
    p = tmp_path / "lastfailed"
    p.write_text("[]", encoding="utf-8", newline="\n")
    with pytest.raises(fs.FailedSetError):
        fs.read_lastfailed(p)


def test_a_genuinely_green_run_reads_as_an_empty_set_not_an_error(tmp_path):
    """The other half of the same property — an empty cache is a real, readable measurement."""
    assert fs.read_lastfailed(_cache(tmp_path, [])) == set()


def test_comparison_is_on_SETS_so_reordering_is_not_drift(tmp_path):
    base = {"t.py::a", "t.py::b"}
    regressions, fixed = fs.compare(base, {"t.py::b", "t.py::a"})
    assert (regressions, fixed) == (set(), set())


def test_a_new_failure_is_a_REGRESSION_and_a_disappeared_one_is_FIXED():
    regressions, fixed = fs.compare({"t.py::was"}, {"t.py::now"})
    assert regressions == {"t.py::now"}
    assert fixed == {"t.py::was"}


def test_fixing_a_base_failure_without_adding_one_is_a_PASS(tmp_path):
    """delta A2 is 'do not make it worse', so a strict improvement exits 0."""
    base = tmp_path / "base.json"
    base.write_text(json.dumps(fs.build_record({"t.py::a", "t.py::b"}, "abc1234", "local")),
                    encoding="utf-8", newline="\n")
    rc = fs.main(["--cache", str(_cache(tmp_path, ["t.py::a"])), "--compare", str(base)])
    assert rc == 0


def test_a_regression_exits_NONZERO(tmp_path):
    base = tmp_path / "base.json"
    base.write_text(json.dumps(fs.build_record({"t.py::a"}, "abc1234", "local")),
                    encoding="utf-8", newline="\n")
    rc = fs.main(["--cache", str(_cache(tmp_path, ["t.py::a", "t.py::new"])), "--compare",
                  str(base)])
    assert rc == 1


def test_a_base_artifact_of_an_unknown_schema_is_REFUSED(tmp_path):
    base = tmp_path / "base.json"
    base.write_text(json.dumps({"nodeids": ["t.py::a"]}), encoding="utf-8", newline="\n")
    with pytest.raises(fs.FailedSetError, match="schema"):
        fs.load_record(base)


def test_emit_round_trips_through_load_record(tmp_path):
    out = tmp_path / "out" / "base.json"
    rc = fs.main(["--cache", str(_cache(tmp_path, ["t.py::a", "t.py::b"])),
                  "--emit", str(out), "--substrate", "codespace"])
    assert rc == 0
    assert fs.load_record(out) == {"t.py::a", "t.py::b"}
    assert json.loads(out.read_text(encoding="utf-8"))["substrate"] == "codespace"


def test_a_missing_cache_exits_2_rather_than_0_through_the_CLI(tmp_path):
    """A reported gap that exited 0 would read as a pass to anything shelling out to this."""
    assert fs.main(["--cache", str(tmp_path / "nope"), "--emit", str(tmp_path / "o.json")]) == 2


def _report(tmp_path, body):
    p = tmp_path / "run.txt"
    p.write_text(body, encoding="utf-8", newline="\n")
    return p


def test_the_run_report_is_read_when_the_cache_cannot_be_trusted(tmp_path):
    """Measured 2026-09-02: a full `-n auto` run rewrote `nodeids` and left `lastfailed` a day
    stale — 45 nodeids against the 13 the run reported. The report is the authority."""
    body = ("FAILED tests/a.py::t_one - AssertionError: nope\n"
            "ERROR tests/b.py::t_two\n"
            "13 failed, 4856 passed, 4 skipped in 841.43s\n")
    assert fs.read_report(_report(tmp_path, body)) == {"tests/a.py::t_one", "tests/b.py::t_two"}


def test_ansi_colouring_does_not_hide_a_failure(tmp_path):
    """A coloured FAILED line keeps a leading ESC after naive bracket-stripping and would then
    match nothing — silently dropping a real failure out of the base set."""
    esc = chr(27)
    body = (f"{esc}[31mFAILED tests/a.py::t_one - boom{esc}[0m\n"
            "1 failed, 2 passed in 1.0s\n")
    assert fs.read_report(_report(tmp_path, body)) == {"tests/a.py::t_one"}


def test_a_parametrised_nodeid_survives_the_ansi_strip(tmp_path):
    body = "FAILED tests/a.py::t_one[case-1] - boom\n1 failed in 1.0s\n"
    assert fs.read_report(_report(tmp_path, body)) == {"tests/a.py::t_one[case-1]"}


def test_a_green_run_report_reads_as_an_empty_set(tmp_path):
    assert fs.read_report(_report(tmp_path, "4856 passed, 4 skipped in 800s\n")) == set()


def test_a_file_that_is_not_a_pytest_report_RAISES_rather_than_forgiving_everything(tmp_path):
    """An empty set from an unrecognised file is the false base this module exists to prevent."""
    with pytest.raises(fs.FailedSetError, match="pytest run report"):
        fs.read_report(_report(tmp_path, "some unrelated log output\n"))


def test_an_absent_report_RAISES(tmp_path):
    with pytest.raises(fs.FailedSetError, match="absent"):
        fs.read_report(tmp_path / "nope.txt")


def test_the_emitted_record_names_WHICH_source_produced_it(tmp_path):
    """Two sources exist and they disagreed by 32 nodeids once; a record that did not say which
    one it came from would be unauditable."""
    out = tmp_path / "base.json"
    fs.main(["--from-report", str(_report(tmp_path, "FAILED tests/a.py::t - x\n1 failed in 1s\n")),
             "--emit", str(out)])
    assert json.loads(out.read_text(encoding="utf-8"))["source"] == "run-report"
