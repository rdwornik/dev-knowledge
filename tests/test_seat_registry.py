"""RED-first witnesses for `scripts/seat_registry.py` -- `[#833]`, lane ab-833.

THE ABSENCE THESE TESTS RETIRE. Wedged, absent and starved were three separately-filed symptoms
(`[#648]`, `[#805]`, `[#808]`, `[#682]`) of one missing field. On 2026-09-17 the absence was
demonstrated on this lane itself: a second session was dispatched onto lane ab-833 while its owner
was live, and nothing anywhere recorded that the lane had an owner.

WHAT IS PINNED, and each is a removal test:

  * `state` is WRITTEN ONLY BY AN EVENT. A payload that carries its own `state` -- which is what a
    model asserting a seat's condition in prose would produce -- is REFUSED at write time, and a
    row appended by hand whose `state` disagrees with its event is DISCARDED at read time. The
    write-time refusal alone would not be enough: anyone can append a line to a file.
  * the four values are derived from event timestamps only: `live` inside the threshold, `wedged`
    for a seat silent mid-turn, `starved` for a seat that ended its turn and was never fed, `absent`
    for a dead process, a removed lane worktree, or a `SessionEnd`.
  * the thresholds carry provenance, and the SessionStart line names a stalled seat unasked.

No test here needs git or a skip guard: the registry is a file, and every clock and process probe
is injected, so the proof cannot be skipped on the machine that breaks the property.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from click.testing import CliRunner

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import seat_registry as reg  # noqa: E402
from seat_refusals import SeatRefusal  # noqa: E402

T0 = datetime(2026, 9, 17, 10, 47, tzinfo=timezone.utc)
LANE_CWD = "C:/Dev/.dev-knowledge/.claude/worktrees/lane-ab-833-seat-registry"


def _event(path: Path, event: str, session: str, *, at: datetime, cwd: str = "C:/Dev/hub",
           pid: str = "4242", **extra) -> dict:
    payload = {"hook_event_name": event, "session_id": session, "cwd": cwd, **extra}
    return reg.record_event(payload, path=path, now=at, env={"CLAUDE_PID": pid})


def _seats(path: Path, *, now: datetime, alive: bool = True, exists: bool = True):
    return {s.session_id: s for s in reg.seats(path, now=now,
                                               pid_alive=lambda _pid: alive,
                                               path_exists=lambda _p: exists,
                                               transcript_mtime=lambda _p: None)}


# --- one field, written only by an event ---------------------------------------------------------

def test_a_model_authored_state_write_is_refused(tmp_path):
    """The heart of Done (1): a caller cannot hand the registry a state."""
    path = tmp_path / "seats.jsonl"
    with pytest.raises(SeatRefusal, match="model-authored-state"):
        reg.record_event({"hook_event_name": "Stop", "session_id": "s1", "state": "live"},
                         path=path, now=T0, env={})
    assert not path.exists(), "a refused write must leave nothing behind"


def test_a_payload_that_is_not_a_hook_event_is_refused(tmp_path):
    with pytest.raises(SeatRefusal, match="not-an-event"):
        reg.record_event({"hook_event_name": "IAmWorkingOnIt", "session_id": "s1"},
                         path=tmp_path / "seats.jsonl", now=T0, env={})


def test_no_verb_accepts_a_state(tmp_path):
    """The CLI is the other route a model has to the file. No verb takes `--state`."""
    result = CliRunner().invoke(reg.cli, ["bind", "--role", "integrator", "--batch", "AB",
                                          "--state", "live"])
    assert result.exit_code != 0
    assert "--state" in result.output


def test_the_writer_sets_state_from_the_event(tmp_path):
    path = tmp_path / "seats.jsonl"
    assert _event(path, "SessionStart", "s1", at=T0)["state"] == "live"
    assert _event(path, "SessionEnd", "s1", at=T0 + timedelta(minutes=1))["state"] == "absent"


def test_a_hand_appended_row_whose_state_disagrees_with_its_event_is_discarded(tmp_path):
    path = tmp_path / "seats.jsonl"
    _event(path, "SessionStart", "s1", at=T0)
    forged = {"schema": reg.SCHEMA, "kind": "event", "event": "SessionEnd", "state": "live",
              "session_id": "s1", "ts": (T0 + timedelta(minutes=5)).isoformat()}
    stateonly = {"schema": reg.SCHEMA, "kind": "state", "state": "live", "session_id": "s2",
                 "ts": T0.isoformat()}
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(forged) + "\n" + json.dumps(stateonly) + "\n")
    seats = _seats(path, now=T0 + timedelta(minutes=6))
    assert set(seats) == {"s1"}, "a row the writer could not have produced is not a seat"
    assert seats["s1"].state == "live", "the forged SessionEnd must not have ended s1"


def test_a_bind_carries_role_and_batch_and_never_a_state(tmp_path):
    path = tmp_path / "seats.jsonl"
    row = reg.bind("integrator", "AB", session_id="s1", path=path, now=T0)
    assert "state" not in row
    with pytest.raises(SeatRefusal, match="unknown-role"):
        reg.bind("janitor", "AB", session_id="s1", path=path, now=T0)


def test_a_bind_without_a_runtime_session_id_is_refused(monkeypatch):
    """The CLI binds the id the RUNTIME gave the seat, never one typed on a command line."""
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    result = CliRunner().invoke(reg.cli, ["bind", "--role", "integrator", "--batch", "AB"])
    assert result.exit_code == 1
    assert "CLAUDE_CODE_SESSION_ID" in result.output


# --- the four values, derived from timestamps ----------------------------------------------------

def test_a_lane_seat_takes_role_and_batch_from_its_worktree(tmp_path):
    path = tmp_path / "seats.jsonl"
    _event(path, "SessionStart", "s1", at=T0, cwd=LANE_CWD)
    seat = _seats(path, now=T0)["s1"]
    assert (seat.role, seat.batch, seat.lane) == ("lane", "AB", "lane-ab-833-seat-registry")


def test_a_primary_checkout_seat_is_unbound_until_it_binds(tmp_path):
    path = tmp_path / "seats.jsonl"
    _event(path, "SessionStart", "s1", at=T0)
    assert _seats(path, now=T0)["s1"].role is None
    reg.bind("integrator", "ab", session_id="s1", path=path, now=T0)
    seat = _seats(path, now=T0)["s1"]
    assert (seat.role, seat.batch) == ("integrator", "AB")


def test_live_inside_the_threshold(tmp_path):
    path = tmp_path / "seats.jsonl"
    _event(path, "SessionStart", "s1", at=T0)
    assert _seats(path, now=T0 + timedelta(minutes=reg.WEDGED_AFTER_MIN - 1))["s1"].state == "live"


def test_silent_mid_turn_past_the_threshold_is_wedged(tmp_path):
    path = tmp_path / "seats.jsonl"
    _event(path, "SessionStart", "s1", at=T0)
    later = T0 + timedelta(minutes=reg.WEDGED_AFTER_MIN + 1)
    assert _seats(path, now=later)["s1"].state == "wedged"


def test_a_turn_ended_and_never_fed_past_the_threshold_is_starved(tmp_path):
    """`[#805]`'s integrator: last tool call 21:43, the operator's ruling 08:17 -- waiting, not slow."""
    path = tmp_path / "seats.jsonl"
    _event(path, "SessionStart", "s1", at=T0)
    _event(path, "Stop", "s1", at=T0 + timedelta(minutes=5))
    later = T0 + timedelta(minutes=5 + reg.STARVED_AFTER_MIN + 1)
    assert _seats(path, now=later)["s1"].state == "starved"


def test_a_runtime_transcript_write_after_the_stop_is_activity(tmp_path):
    """The transcript is written by the harness, not the model, so its mtime is an event time."""
    path = tmp_path / "seats.jsonl"
    _event(path, "SessionStart", "s1", at=T0, transcript_path="t.jsonl")
    _event(path, "Stop", "s1", at=T0 + timedelta(minutes=5), transcript_path="t.jsonl")
    now = T0 + timedelta(minutes=5 + reg.STARVED_AFTER_MIN + 1)
    fresh = now - timedelta(minutes=1)
    seats = {s.session_id: s for s in reg.seats(path, now=now, pid_alive=lambda _p: True,
                                                path_exists=lambda _p: True,
                                                transcript_mtime=lambda _p: fresh)}
    assert seats["s1"].state == "live"


def test_a_dead_process_is_absent(tmp_path):
    path = tmp_path / "seats.jsonl"
    _event(path, "SessionStart", "s1", at=T0)
    assert _seats(path, now=T0, alive=False)["s1"].state == "absent"


def test_a_removed_lane_worktree_is_absent(tmp_path):
    path = tmp_path / "seats.jsonl"
    _event(path, "SessionStart", "s1", at=T0, cwd=LANE_CWD)
    assert _seats(path, now=T0, exists=False)["s1"].state == "absent"


def test_session_end_is_absent(tmp_path):
    path = tmp_path / "seats.jsonl"
    _event(path, "SessionStart", "s1", at=T0)
    _event(path, "SessionEnd", "s1", at=T0 + timedelta(minutes=1))
    assert _seats(path, now=T0 + timedelta(minutes=2))["s1"].state == "absent"


def test_a_fresh_bind_with_no_event_yet_reads_live(tmp_path):
    """D23: the seat used to read `absent` until its first hook event arrived, long enough for
    a dispatcher to refuse a launch onto a seat that had, in fact, just bound
    (SESSION-integrator-wave4b-2026-09-22.md s1). A bind alone is a seat that just started."""
    path = tmp_path / "seats.jsonl"
    reg.bind("integrator", "AB", session_id="s1", path=path, now=T0)
    seat = _seats(path, now=T0)["s1"]
    assert seat.state == "live"


def test_a_bind_with_no_event_ever_ages_to_wedged_not_absent(tmp_path):
    path = tmp_path / "seats.jsonl"
    reg.bind("integrator", "AB", session_id="s1", path=path, now=T0)
    later = T0 + timedelta(minutes=reg.WEDGED_AFTER_MIN + 1)
    seat = _seats(path, now=later)["s1"]
    assert seat.state == "wedged"


def test_every_state_is_in_the_closed_enum():
    assert reg.STATES == ("live", "wedged", "absent", "starved")
    assert reg.ROLES == ("dispatcher", "integrator", "lane", "browser")
    assert set(reg.EVENT_STATE.values()) <= set(reg.STATES)


def test_every_threshold_carries_its_provenance():
    for name in ("WEDGED_AFTER_MIN", "STARVED_AFTER_MIN", "SURFACE_LOOKBACK_HOURS"):
        assert isinstance(getattr(reg, name), (int, float))
        assert len(reg.THRESHOLD_PROVENANCE.get(name, "")) > 80, f"{name} has no provenance"


def test_an_unreadable_registry_reads_as_no_seats(tmp_path):
    assert reg.seats(tmp_path / "missing.jsonl", now=T0) == []


# --- self-surfacing at SessionStart ------------------------------------------------------------

def test_the_session_start_line_names_a_stalled_seat_unasked(tmp_path):
    path = tmp_path / "seats.jsonl"
    _event(path, "SessionStart", "integrator-1", at=T0)
    reg.bind("integrator", "AB", session_id="integrator-1", path=path, now=T0)
    _event(path, "SessionStart", "lane-1", at=T0, cwd=LANE_CWD)
    _event(path, "Stop", "lane-1", at=T0 + timedelta(minutes=1), cwd=LANE_CWD)
    now = T0 + timedelta(minutes=reg.STARVED_AFTER_MIN + 10)
    line = reg.seat_health_line(path, now=now, pid_alive=lambda _p: True,
                                path_exists=lambda _p: True, transcript_mtime=lambda _p: None)
    assert line.startswith("[seats]")
    assert "WEDGED" in line and "integrator AB" in line
    assert "STARVED" in line and "lane-ab-833-seat-registry" in line


def test_the_session_start_line_is_silent_over_an_empty_registry(tmp_path):
    assert reg.seat_health_line(tmp_path / "none.jsonl", now=T0) is None


def test_a_hook_leg_never_raises(tmp_path, monkeypatch):
    """A reporter must never stop a session from starting or a turn from ending."""
    monkeypatch.setattr(reg, "REGISTRY_PATH", tmp_path / "no" / "such" / "\0bad")
    assert reg.record_hook_event({"hook_event_name": "Stop", "session_id": "s1"}) is None
    assert reg.record_hook_event({"state": "live"}) is None


# --- the event writers: the two hook legs that already fire ----------------------------------------
#
# No new hook registration (`.claude/settings.json` is sequenced behind ab-808). These prove the two
# existing legs WRITE, and write nothing for a payload that is not a hook payload -- the guard that
# keeps a suite run inside a live Claude Code session out of the real registry.

def test_the_stop_hook_leg_records_a_stop_event(tmp_path, monkeypatch):
    import io

    import session_end_backpressure as seb
    path = tmp_path / "seats.jsonl"
    monkeypatch.setattr(reg, "REGISTRY_PATH", path)
    payload = {"hook_event_name": "Stop", "session_id": "stop-1", "stop_hook_active": True,
               "cwd": LANE_CWD}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    assert seb.main() == 0
    rows = reg.read_rows(path)
    assert [(r["event"], r["state"], r["session_id"]) for r in rows] == [("Stop", "live", "stop-1")]


def test_the_stop_hook_leg_writes_nothing_without_a_session(tmp_path, monkeypatch):
    import io

    import session_end_backpressure as seb
    path = tmp_path / "seats.jsonl"
    monkeypatch.setattr(reg, "REGISTRY_PATH", path)
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({"stop_hook_active": True})))
    assert seb.main() == 0
    assert not path.exists()


def test_the_session_start_leg_records_a_start_event(tmp_path, monkeypatch):
    import resource_lifecycle as rl
    path = tmp_path / "seats.jsonl"
    monkeypatch.setattr(reg, "REGISTRY_PATH", path)
    monkeypatch.setattr(rl, "process_table", lambda: [])
    monkeypatch.setattr(rl, "sample", lambda **_kw: [])
    payload = {"hook_event_name": "SessionStart", "session_id": "start-1", "cwd": "C:/Dev/hub",
               "source": "startup"}
    result = CliRunner().invoke(rl.cli, ["session-start"], input=json.dumps(payload))
    assert result.exit_code == 0, result.output
    rows = reg.read_rows(path)
    assert [(r["event"], r["state"], r["session_id"]) for r in rows] == [
        ("SessionStart", "live", "start-1")]


def test_the_session_start_leg_refuses_a_payload_that_asserts_its_own_state(tmp_path, monkeypatch):
    import resource_lifecycle as rl
    path = tmp_path / "seats.jsonl"
    monkeypatch.setattr(reg, "REGISTRY_PATH", path)
    monkeypatch.setattr(rl, "process_table", lambda: [])
    monkeypatch.setattr(rl, "sample", lambda **_kw: [])
    payload = {"hook_event_name": "SessionStart", "session_id": "s1", "state": "live"}
    result = CliRunner().invoke(rl.cli, ["session-start"], input=json.dumps(payload))
    assert result.exit_code == 0, "a refused event must not stop a session from starting"
    assert not path.exists()

# --- the SessionStart surface: fleet_health's digest prints the line unasked ------------------------

def test_fleet_health_surfaces_a_wedged_integrator_at_session_start(tmp_path, monkeypatch):
    import os

    import fleet_health
    path = tmp_path / "seats.jsonl"
    monkeypatch.setattr(reg, "REGISTRY_PATH", path)
    then = datetime.now(timezone.utc) - timedelta(minutes=reg.WEDGED_AFTER_MIN + 15)
    reg.record_event({"hook_event_name": "SessionStart", "session_id": "int-wedged",
                      "cwd": str(tmp_path)}, now=then, env={"CLAUDE_PID": str(os.getpid())})
    reg.bind("integrator", "AB", session_id="int-wedged", now=then)
    line = fleet_health.seat_health_line(tmp_path)          # tmp_path is no repo: no open batches
    assert line and line.startswith("[seats]")
    assert "WEDGED" in line and "integrator AB int-wed" in line


def test_the_seat_line_names_an_open_batch_nobody_receives(tmp_path):
    path = tmp_path / "seats.jsonl"
    _event(path, "SessionStart", "lane-1", at=T0, cwd=LANE_CWD)
    line = reg.seat_health_line(path, now=T0, open_batches=["ab"], pid_alive=lambda _p: True,
                                path_exists=lambda _p: True, transcript_mtime=lambda _p: None)
    assert "NO LIVE INTEGRATOR for batch AB" in line


def test_fleet_health_main_prints_the_seat_line():
    """The wiring half: a surface no boot path calls does not surface anything."""
    import inspect

    import fleet_health
    assert "seat_health_line(_REPO_ROOT)" in inspect.getsource(fleet_health.main)