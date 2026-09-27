"""Witnesses for `scripts/seat_state.py` (LANE-5B3-10-orchestrator-cycling, Done-contract
item 1): "A test proves a fresh session reconstructs the in-flight set from a state file
written by a simulated earlier one, and that a torn or stale file is refused, not trusted."
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from click.testing import CliRunner

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
for p in (REPO_ROOT, SCRIPTS):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import seat_state as ss  # noqa: E402


def _evidence(session_file="to-browser/SESSION-integrator-wave5b-n3-2026-09-26.md",
             receipt_line=None, sha=None):
    return {"session_file": session_file, "receipt_line": receipt_line, "sha": sha}


def _row(state, **kw):
    return {"state": state, "sha": kw.pop("sha", None), "evidence": _evidence(**kw)}


# --- build_state / write_state: validation -------------------------------------------------

def test_build_state_rejects_unknown_role():
    with pytest.raises(ss.SeatStateError):
        ss.build_state(role="lane", batch="WAVE5B-N3", base_sha="abc123", lanes={})


def test_build_state_rejects_state_outside_the_enum():
    with pytest.raises(ss.SeatStateError):
        ss.build_state(role="integrator", batch="WAVE5B-N3", base_sha="abc123",
                       lanes={"lane-a": _row("BOUND")})


def test_build_state_rejects_a_row_with_no_evidence_session_file():
    with pytest.raises(ss.SeatStateError):
        ss.build_state(role="integrator", batch="WAVE5B-N3", base_sha="abc123",
                       lanes={"lane-a": {"state": "MERGED", "evidence": {}}})


def test_build_state_maps_the_integrator_receipts_waiting_to_in_flight():
    state = ss.build_state(role="integrator", batch="WAVE5B-N3", base_sha="abc123",
                           lanes={"lane-a": _row("WAITING")})
    assert state.lanes["lane-a"].state == "IN-FLIGHT"


def test_build_state_requires_batch_and_base_sha():
    with pytest.raises(ss.SeatStateError):
        ss.build_state(role="integrator", batch="", base_sha="abc123", lanes={})
    with pytest.raises(ss.SeatStateError):
        ss.build_state(role="integrator", batch="WAVE5B-N3", base_sha="", lanes={})


# --- the round trip: a fresh session reconstructs the in-flight set ------------------------

def test_a_fresh_session_reconstructs_the_in_flight_set_from_a_simulated_earlier_write(tmp_path):
    """The Done-contract's own words: a state file written by a simulated EARLIER session, read
    by a fresh one that never saw the night's receipts."""
    path = tmp_path / "STATE-WAVE5B-N3.json"
    earlier_session_lanes = {
        "lane-organ-wirings-verify": _row(
            "MERGED", sha="46af641f",
            receipt_line="STATE lane-organ-wirings-verify MERGED 46af641f 2026-09-26T20:47 226"),
        "lane-wire-quota-distiller": _row(
            "REFUSED",
            receipt_line="STATE lane-wire-quota-distiller REFUSED - 2026-09-26T18:04 -"),
        "lane-moments-fire": _row(
            "FAILED",
            receipt_line="STATE lane-moments-fire FAILED - 2026-09-27T01:16 -"),
        "lane-process-agent-architecture": _row(
            "REPORTED",
            receipt_line="STATE lane-process-agent-architecture REPORTED - 2026-09-26T16:51 -"),
        "lane-decision-debt": _row("IN-FLIGHT",
                                   receipt_line="picked up 21:42, verification in progress"),
        "lane-orchestrator-cycling": _row("QUEUED",
                                          receipt_line="held on wire-quota-distiller MERGED"),
    }
    written = ss.write_state(path, role="integrator", batch="wave5b-n3", base_sha="abb03452",
                             lanes=earlier_session_lanes, written_by="session-earlier")
    assert written.batch == "WAVE5B-N3"  # normalised upper-case

    # A FRESH reader: no shared state with the writer beyond the file on disk.
    fresh = ss.read_state(path)
    assert fresh.role == "integrator"
    assert fresh.base_sha == "abb03452"
    assert fresh.in_flight() == ["lane-decision-debt", "lane-orchestrator-cycling"]
    assert fresh.by_state("MERGED") == ["lane-organ-wirings-verify"]
    assert fresh.by_state("REFUSED") == ["lane-wire-quota-distiller"]
    assert fresh.by_state("FAILED") == ["lane-moments-fire"]
    assert fresh.by_state("REPORTED") == ["lane-process-agent-architecture"]
    # Evidence survives the round trip, verbatim -- a fresh session can cite it.
    assert (fresh.lanes["lane-organ-wirings-verify"].evidence.receipt_line
           == earlier_session_lanes["lane-organ-wirings-verify"]["evidence"]["receipt_line"])
    assert fresh.lanes["lane-organ-wirings-verify"].sha == "46af641f"


def test_write_state_is_atomic_no_temp_file_left_behind(tmp_path):
    path = tmp_path / "STATE.json"
    ss.write_state(path, role="dispatcher", batch="B", base_sha="deadbee",
                   lanes={"lane-a": _row("QUEUED")})
    leftovers = list(tmp_path.glob(".*"))
    assert leftovers == [], f"a temp file survived the write: {leftovers}"


# --- torn: refused, not trusted -------------------------------------------------------------

def test_read_state_refuses_a_file_that_is_not_json(tmp_path):
    path = tmp_path / "STATE.json"
    path.write_text("{not json at all", encoding="utf-8")
    with pytest.raises(ss.SeatStateError, match="torn"):
        ss.read_state(path)


def test_read_state_refuses_a_file_with_the_wrong_schema(tmp_path):
    path = tmp_path / "STATE.json"
    path.write_text(json.dumps({"schema": "something-else/1"}), encoding="utf-8")
    with pytest.raises(ss.SeatStateError, match="torn"):
        ss.read_state(path)


def test_read_state_refuses_a_file_missing_a_required_field(tmp_path):
    path = tmp_path / "STATE.json"
    valid = json.loads(json.dumps(ss.build_state(
        role="integrator", batch="B", base_sha="abc", lanes={}).to_dict()))
    del valid["base_sha"]
    path.write_text(json.dumps(valid), encoding="utf-8")
    with pytest.raises(ss.SeatStateError, match="torn"):
        ss.read_state(path)


def test_read_state_refuses_a_lane_row_with_an_invalid_state(tmp_path):
    path = tmp_path / "STATE.json"
    state = ss.build_state(role="integrator", batch="B", base_sha="abc", lanes={})
    data = state.to_dict()
    data["lanes"]["lane-a"] = {"state": "SOMETHING", "evidence": {"session_file": "x"}}
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ss.SeatStateError):
        ss.read_state(path)


def test_read_state_refuses_nonexistent_file(tmp_path):
    with pytest.raises(ss.SeatStateError):
        ss.read_state(tmp_path / "does-not-exist.json")


# --- stale: refused, not trusted -------------------------------------------------------------

def test_read_state_refuses_a_file_older_than_the_stale_bound(tmp_path):
    path = tmp_path / "STATE.json"
    old_ts = (datetime.now(timezone.utc) - timedelta(minutes=ss.STALE_AFTER_MIN + 1))
    ss.write_state(path, role="integrator", batch="B", base_sha="abc",
                   lanes={"lane-a": _row("IN-FLIGHT")}, now=old_ts.isoformat(timespec="seconds"))
    with pytest.raises(ss.SeatStateError, match="STALE"):
        ss.read_state(path)


def test_read_state_accepts_a_file_just_inside_the_stale_bound(tmp_path):
    path = tmp_path / "STATE.json"
    recent_ts = (datetime.now(timezone.utc) - timedelta(minutes=ss.STALE_AFTER_MIN - 1))
    ss.write_state(path, role="integrator", batch="B", base_sha="abc",
                   lanes={"lane-a": _row("IN-FLIGHT")}, now=recent_ts.isoformat(timespec="seconds"))
    fresh = ss.read_state(path)
    assert fresh.in_flight() == ["lane-a"]


def test_read_state_max_age_min_is_a_parameter_not_a_guess_baked_in(tmp_path):
    path = tmp_path / "STATE.json"
    old_ts = (datetime.now(timezone.utc) - timedelta(minutes=10))
    ss.write_state(path, role="integrator", batch="B", base_sha="abc",
                   lanes={"lane-a": _row("IN-FLIGHT")}, now=old_ts.isoformat(timespec="seconds"))
    with pytest.raises(ss.SeatStateError, match="STALE"):
        ss.read_state(path, max_age_min=5.0)


# --- CLI ---------------------------------------------------------------------------------------

def test_cli_write_then_read_round_trip(tmp_path):
    path = tmp_path / "STATE.json"
    lanes_json = json.dumps({"lane-a": _row("MERGED", sha="cafef00d")})
    runner = CliRunner()
    write_result = runner.invoke(ss.cli, ["write", "--path", str(path), "--role", "integrator",
                                         "--batch", "WAVE5B-N3", "--base-sha", "abb03452",
                                         "--lanes-json", lanes_json])
    assert write_result.exit_code == 0, write_result.output
    assert "in-flight = []" in write_result.output

    read_result = runner.invoke(ss.cli, ["read", "--path", str(path)])
    assert read_result.exit_code == 0, read_result.output
    assert "MERGED: ['lane-a']" in read_result.output


def test_cli_write_accepts_lanes_json_from_a_file(tmp_path):
    lanes_path = tmp_path / "lanes.json"
    lanes_path.write_text(json.dumps({"lane-a": _row("QUEUED")}), encoding="utf-8")
    path = tmp_path / "STATE.json"
    runner = CliRunner()
    result = runner.invoke(ss.cli, ["write", "--path", str(path), "--role", "dispatcher",
                                   "--batch", "B", "--base-sha", "abc",
                                   "--lanes-json", f"@{lanes_path}"])
    assert result.exit_code == 0, result.output
    assert ss.read_state(path).in_flight() == ["lane-a"]


def test_cli_read_reports_a_torn_file_as_a_clean_failure_not_a_traceback(tmp_path):
    path = tmp_path / "STATE.json"
    path.write_text("not json", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(ss.cli, ["read", "--path", str(path)])
    assert result.exit_code != 0
    assert "torn" in result.output
