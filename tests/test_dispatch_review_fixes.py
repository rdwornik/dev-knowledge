"""Binding a lane to its own usage -- what survives of the wave-3 review rounds after LANE-W3-B.

Artifacts: docs/audits/2026-09-19-codex-wave3-dispatch-split*.md. Those rounds hardened a governor
that STOPPED a lane; R-W3-2 / N3 made `govern` a monitor, so the rounds' "stop the right lane"
findings became "monitor the right lane" and the tests below keep the part that still matters: the
monitor must bind the lane it was asked about, never a neighbour, and an unreadable state is a
recorded row, not an escaped exception and not an action against a lane.

`_control` (the read-only control-plane call) is replaced by a listing; nothing is started.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

import dispatch as d

_SID = "11111111-2222-3333-4444-555555555555"
_OURS = {"id": "abcd1234", "sessionId": _SID, "state": "working",
         "cwd": "C:\\repo\\.claude\\worktrees\\wave3-witness"}
_OTHER = {"id": "deadbeef", "sessionId": "99999999-0000-0000-0000-000000000000",
          "state": "working", "cwd": "C:\\repo\\.claude\\worktrees\\some-other-lane"}


@pytest.fixture(autouse=True)
def _receipts_in_tmp(tmp_path, monkeypatch):
    """`govern` appends spend rows under the receipts dir: never the checkout's own `logs/receipts/`."""
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(tmp_path / "receipts"))


def _transcript(root: Path, session_id: str, tokens: int) -> None:
    target = root / "any-dir"
    target.mkdir(parents=True, exist_ok=True)
    record = {"message": {"id": "m1", "model": "claude-haiku-4-5",
                          "usage": {"input_tokens": tokens, "output_tokens": 0}}}
    (target / f"{session_id}.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")


def _listing(*entries):
    return lambda argv: subprocess.CompletedProcess(argv, 0, json.dumps(list(entries)), "")


def _commands_seen(monkeypatch, *entries):
    """Serve a listing and record every argv `_control` is asked to run: a monitor may only LIST."""
    seen = []

    def control(argv):
        seen.append(list(argv))
        return _listing(*entries)(argv)
    monkeypatch.setattr(d, "_control", control)
    monkeypatch.setattr(d, "commit_witness", lambda slug: ("DONE", "1 commit"))
    return seen


def _govern(tmp_path, *args, cap="1000"):
    return CliRunner().invoke(d.cli, ["govern", *args, "--slug", "wave3-witness", "--token-cap", cap,
                                      "--interval", "0", "--bind-polls", "2", "--max-polls", "2",
                                      "--sessions-root", str(tmp_path / "sessions")])


def test_a_lane_whose_id_was_not_read_is_found_by_its_worktree_and_monitored(tmp_path, monkeypatch):
    """The launch output may carry no readable id. The listing names each lane's cwd, which for a
    `--bg --worktree` lane is `.../worktrees/<slug>` -- so the lane is FOUND by slug and monitored."""
    _transcript(tmp_path / "sessions", _SID, tokens=5_000)
    seen = _commands_seen(monkeypatch, {"id": "zzzz9999", "state": "working", "cwd": "C:\\repo"}, _OURS)
    result = _govern(tmp_path)
    assert result.exit_code == d.EXIT_OVER_CAP
    assert all(argv[:3] == ["claude", "agents", "--json"] for argv in seen), seen


def test_a_lane_that_cannot_be_identified_is_unobserved_and_nothing_is_touched(tmp_path, monkeypatch):
    seen = _commands_seen(monkeypatch, {"id": "zzzz9999", "state": "working", "cwd": "C:\\r"})
    result = _govern(tmp_path)
    assert result.exit_code == d.EXIT_UNOBSERVED
    assert "identif" in result.output.lower() and "not touched" in result.output.lower()
    assert all(argv[:3] == ["claude", "agents", "--json"] for argv in seen), seen


def test_two_live_lanes_for_one_slug_are_ambiguous_not_guessed(monkeypatch):
    cwd = "C:\\repo\\.claude\\worktrees\\wave3-witness"
    monkeypatch.setattr(d, "_control", _listing({"id": "a1", "state": "working", "cwd": cwd},
                                                {"id": "b2", "state": "working", "cwd": cwd}))
    assert d.find_lane_by_slug("wave3-witness") is None


def test_a_provisional_id_that_belongs_to_another_lane_is_never_monitored(tmp_path, monkeypatch):
    """A false id (the first 8-hex token in some output) names a NEIGHBOUR. The bound entry's
    worktree must be the slug's, else the lane is rediscovered by worktree -- so the spend recorded
    is ours, not the neighbour's."""
    _transcript(tmp_path / "sessions", _SID, tokens=5_000)
    _commands_seen(monkeypatch, _OTHER, _OURS)
    result = _govern(tmp_path, "deadbeef")
    assert result.exit_code == d.EXIT_OVER_CAP


def test_a_provisional_id_of_another_lane_and_no_lane_for_the_slug_is_unobserved(tmp_path, monkeypatch):
    seen = _commands_seen(monkeypatch, _OTHER)
    result = _govern(tmp_path, "deadbeef")
    assert result.exit_code == d.EXIT_UNOBSERVED and "not touched" in result.output.lower()
    assert all(argv[:3] == ["claude", "agents", "--json"] for argv in seen), seen


def test_a_transcript_that_cannot_be_read_is_unobservable_not_an_escaped_exception(monkeypatch):
    """An exception from the transcript reader (malformed numeric usage, a filesystem error) must
    become an unreadable row, never end the monitor."""
    def boom(session_id, sessions_root=None):
        raise ValueError("invalid literal for int()")
    monkeypatch.setattr(d.lc, "seat_usage", boom)
    assert d._session_reader("sid")() is None


def test_a_monitor_that_crashes_says_so_and_exits_4_with_the_lane_untouched(tmp_path, monkeypatch):
    _transcript(tmp_path / "sessions", _SID, tokens=10)
    seen = _commands_seen(monkeypatch, _OURS)

    def broken(lane_id):
        raise RuntimeError("the liveness probe blew up")
    monkeypatch.setattr(d, "lane_alive", broken)
    result = _govern(tmp_path, "abcd1234")
    assert result.exception is None or isinstance(result.exception, SystemExit)
    assert result.exit_code == d.EXIT_UNOBSERVED and "not touched" in result.output.lower()
    assert all(argv[:3] == ["claude", "agents", "--json"] for argv in seen), seen


def test_an_interrupt_ends_the_monitor_and_nothing_else(tmp_path, monkeypatch):
    seen = _commands_seen(monkeypatch, _OURS)

    def interrupted(lane_id):
        raise KeyboardInterrupt
    monkeypatch.setattr(d, "bind_lane", interrupted)
    result = _govern(tmp_path, "deadbeef")
    assert result.exit_code == d.EXIT_UNOBSERVED and "interrupted" in result.output.lower()
    assert all(argv[:3] == ["claude", "agents", "--json"] for argv in seen), seen


def test_a_lane_that_is_not_listed_at_all_is_unobserved_and_nothing_is_touched(tmp_path, monkeypatch):
    seen = _commands_seen(monkeypatch)
    result = _govern(tmp_path, "abcd1234")
    assert result.exit_code == d.EXIT_UNOBSERVED
    assert all(argv[:3] == ["claude", "agents", "--json"] for argv in seen), seen
