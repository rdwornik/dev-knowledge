"""Codex terra review of the whole wave-3 lane -- each finding gets its RED test first.

Artifact: docs/audits/2026-09-19-codex-wave3-dispatch-split.md (1 CRITICAL, 1 HIGH).
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from click.testing import CliRunner

import dispatch as d


def _transcript(root: Path, session_id: str, tokens: int) -> None:
    target = root / "any-dir"
    target.mkdir(parents=True, exist_ok=True)
    record = {"message": {"id": "m1", "model": "claude-haiku-4-5",
                          "usage": {"input_tokens": tokens, "output_tokens": 0}}}
    (target / f"{session_id}.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")


def _listing(*entries):
    return lambda argv: subprocess.CompletedProcess(argv, 0, json.dumps(list(entries)), "")


def test_a_lane_whose_id_the_shim_could_not_read_is_found_by_its_worktree_and_governed(
        tmp_path, monkeypatch):
    """CRITICAL (shim:129): a launch whose output carried no readable id was left running
    uncapped, with the operator told to stop it by hand. The listing names each lane's cwd, which
    for a `--bg --worktree` lane is `.../worktrees/<slug>` -- so the lane is FOUND by slug, bound,
    and governed like any other."""
    sid = "11111111-2222-3333-4444-555555555555"
    _transcript(tmp_path, sid, tokens=5_000)
    entry = {"id": "abcd1234", "sessionId": sid, "state": "working",
             "cwd": "C:\\repo\\.claude\\worktrees\\wave3-witness"}
    stopped = []
    monkeypatch.setattr(d, "_control", _listing({"id": "zzzz9999", "state": "working",
                                                 "cwd": "C:\\repo"}, entry))
    monkeypatch.setattr(d, "stop_lane", lambda lane_id: stopped.append(lane_id) or True)
    result = CliRunner().invoke(d.cli, ["govern", "--slug", "wave3-witness", "--token-cap", "1000",
                                        "--interval", "0", "--sessions-root", str(tmp_path)])
    assert stopped == ["abcd1234"], "the lane found by its worktree must be the one stopped"
    assert result.exit_code == d.EXIT_CAP_EXCEEDED


def test_a_lane_that_cannot_be_identified_at_all_is_the_one_honest_ungoverned(monkeypatch):
    """No id, and no listing entry for the slug: there is nothing to stop. That is UNGOVERNED
    (exit 4) and says the lane may be running -- it is not dressed up as a refusal."""
    monkeypatch.setattr(d, "_control", _listing({"id": "zzzz9999", "state": "working",
                                                 "cwd": "C:\\r"}))
    result = CliRunner().invoke(d.cli, ["govern", "--slug", "wave3-witness", "--token-cap", "1000",
                                        "--interval", "0", "--bind-polls", "2"])
    assert result.exit_code == d.EXIT_UNGOVERNED
    assert "identif" in result.output.lower() and "running" in result.output.lower()


def test_two_live_lanes_for_one_slug_are_ambiguous_not_guessed(monkeypatch):
    cwd = "C:\\repo\\.claude\\worktrees\\wave3-witness"
    monkeypatch.setattr(d, "_control", _listing({"id": "a1", "state": "working", "cwd": cwd},
                                                {"id": "b2", "state": "working", "cwd": cwd}))
    assert d.find_lane_by_slug("wave3-witness") is None


def test_a_lane_that_ended_before_its_usage_was_readable_is_refused_not_left_ungoverned():
    """HIGH (dispatch.py:190): exit 4 must mean ONE thing -- the lane may still be running. A lane
    that has already ENDED with its spend unobserved is not running: nothing is left to cap, so it
    is REFUSED (exit 5, no stop call), never the ungoverned code."""
    stopped = []
    verdict = d.govern(cap=100, read_usage=lambda: None, stop=lambda: stopped.append(1),
                       sleep=lambda s: None, alive=lambda: False, blind_polls=8)
    assert verdict.exit_code == d.EXIT_REFUSED != d.EXIT_UNGOVERNED
    assert stopped == [], "a lane that already ended has nothing to stop"


# --- the RE-review of 12977bdb (docs/audits/2026-09-19-codex-wave3-dispatch-split-rereview.md) ---

_SID = "11111111-2222-3333-4444-555555555555"
_OURS = {"id": "abcd1234", "sessionId": _SID, "state": "working",
         "cwd": "C:\\repo\\.claude\\worktrees\\wave3-witness"}
_OTHER = {"id": "deadbeef", "sessionId": "99999999-0000-0000-0000-000000000000",
          "state": "working", "cwd": "C:\\repo\\.claude\\worktrees\\some-other-lane"}


def _run_govern(tmp_path, monkeypatch, *args):
    stopped = []
    monkeypatch.setattr(d, "stop_lane", lambda lane_id: stopped.append(lane_id) or True)
    result = CliRunner().invoke(d.cli, ["govern", *args, "--slug", "wave3-witness",
                                        "--token-cap", "1000", "--interval", "0",
                                        "--bind-polls", "2", "--sessions-root", str(tmp_path)])
    return result, stopped


def test_a_provisional_id_that_belongs_to_another_lane_is_never_governed_or_stopped(
        tmp_path, monkeypatch):
    """RE-REVIEW CRITICAL (shim:129): the shim takes the first 8-hex token in the launcher's output
    as the id. A false match must not make `govern` stop ANOTHER live lane while the launched one
    runs uncapped: the bound entry's worktree must be the planned slug's, else the lane is
    rediscovered by worktree."""
    _transcript(tmp_path, _SID, tokens=5_000)
    monkeypatch.setattr(d, "_control", _listing(_OTHER, _OURS))
    result, stopped = _run_govern(tmp_path, monkeypatch, "deadbeef")
    assert "deadbeef" not in stopped, "another lane must never be stopped"
    assert stopped == ["abcd1234"] and result.exit_code == d.EXIT_CAP_EXCEEDED


def test_a_provisional_id_of_another_lane_and_no_lane_for_the_slug_is_ungoverned_not_a_stop(
        tmp_path, monkeypatch):
    monkeypatch.setattr(d, "_control", _listing(_OTHER))
    result, stopped = _run_govern(tmp_path, monkeypatch, "deadbeef")
    assert stopped == [], "the wrong lane must not be stopped"
    assert result.exit_code == d.EXIT_UNGOVERNED and "running" in result.output.lower()


def test_a_transcript_that_cannot_be_read_is_unobservable_not_an_escaped_exception(monkeypatch):
    """RE-REVIEW CRITICAL (dispatch.py:621): an exception from the transcript reader (malformed
    numeric usage, a filesystem error) escaped the governor while the lane kept running."""
    def boom(session_id, sessions_root=None):
        raise ValueError("invalid literal for int()")
    monkeypatch.setattr(d.lc, "seat_usage", boom)
    assert d._session_reader("sid")() is None


def test_an_unexpected_governor_failure_stops_the_bound_lane(tmp_path, monkeypatch):
    """The class behind that finding: whatever raises inside the governor, the lane is stopped
    rather than left running with nothing watching it."""
    _transcript(tmp_path, _SID, tokens=10)
    monkeypatch.setattr(d, "_control", _listing(_OURS))

    def broken(lane_id):
        raise RuntimeError("the liveness probe blew up")
    monkeypatch.setattr(d, "lane_alive", broken)
    result, stopped = _run_govern(tmp_path, monkeypatch, "abcd1234")
    assert stopped == ["abcd1234"], "a governor that dies must not leave the lane running"
    assert result.exit_code == d.EXIT_REFUSED


# --- the THIRD pass (docs/audits/2026-09-19-codex-wave3-dispatch-split-rereview-2.md) -------------

def test_an_interrupt_before_the_id_is_verified_never_stops_the_unverified_id(
        tmp_path, monkeypatch):
    """CRITICAL (dispatch.py:735): Ctrl-C / a control-plane failure during `_bind` used to stop
    `lane_id` -- the shim's PROVISIONAL id -- before its worktree had been checked against the slug.
    Recovery paths may stop only an id whose worktree matched."""
    def interrupted(lane_id):
        raise KeyboardInterrupt
    monkeypatch.setattr(d, "bind_lane", interrupted)
    monkeypatch.setattr(d, "find_lane_by_slug", lambda slug: None)
    result, stopped = _run_govern(tmp_path, monkeypatch, "deadbeef")
    assert stopped == [], "an unverified provisional id must never be stopped"
    assert result.exit_code == d.EXIT_UNGOVERNED


def test_a_lane_that_is_not_listed_at_all_is_ungoverned_and_nothing_is_stopped(
        tmp_path, monkeypatch):
    monkeypatch.setattr(d, "_control", _listing())
    result, stopped = _run_govern(tmp_path, monkeypatch, "abcd1234")
    assert stopped == [] and result.exit_code == d.EXIT_UNGOVERNED
    assert "running" in result.output.lower()


def test_a_stop_that_raises_inside_the_recovery_handler_is_an_exit_4_verdict_not_an_escape(
        tmp_path, monkeypatch):
    """CRITICAL (dispatch.py:741): the catch-all called `stop_lane` unprotected, so a stop that
    itself raised (or was interrupted) escaped the governor outside the exit-4/5 contract."""
    _transcript(tmp_path, _SID, tokens=10)
    monkeypatch.setattr(d, "_control", _listing(_OURS))

    def broken(lane_id):
        raise RuntimeError("the liveness probe blew up")

    def cannot_stop(lane_id):
        raise OSError("claude stop could not run")
    monkeypatch.setattr(d, "lane_alive", broken)
    monkeypatch.setattr(d, "stop_lane", cannot_stop)
    result = CliRunner().invoke(d.cli, ["govern", "abcd1234", "--slug", "wave3-witness",
                                        "--token-cap", "1000", "--interval", "0",
                                        "--bind-polls", "2", "--sessions-root", str(tmp_path)])
    assert result.exception is None or isinstance(result.exception, SystemExit)
    assert result.exit_code == d.EXIT_UNGOVERNED
    assert "running" in result.output.lower()
