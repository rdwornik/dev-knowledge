"""Codex terra fourth pass (docs/audits/2026-09-19-codex-wave3-dispatch-split-rereview-3.md), as it
stands after LANE-W3-B.

CRITICAL 1 -- a stale ENDED record for the same worktree must not be accepted as the lane. Still
true: a monitor bound to a `done` record would record a finished lane's spend as the new lane's.
CRITICAL 2 -- the shim needed a hub verb that stops a lane by its worktree. That verb (`stop`) was
REMOVED by R-W3-2 / N3: nothing in `dispatch.py` may end a run. The test below asserts it is gone.
"""
from __future__ import annotations

import json
import subprocess

import pytest
from click.testing import CliRunner

import dispatch as d

_SID = "11111111-2222-3333-4444-555555555555"
_CWD = "C:\\repo\\.claude\\worktrees\\wave3-witness"
_LIVE = {"id": "abcd1234", "sessionId": _SID, "state": "working", "cwd": _CWD}
_STALE = {"id": "deadbeef", "sessionId": "99999999-0000-0000-0000-000000000000",
          "state": "done", "cwd": _CWD}


@pytest.fixture(autouse=True)
def _receipts_in_tmp(tmp_path, monkeypatch):
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(tmp_path / "receipts"))


def _listing(*entries):
    return lambda argv: subprocess.CompletedProcess(argv, 0, json.dumps(list(entries)), "")


def _transcript(root, session_id, tokens):
    target = root / "any-dir"
    target.mkdir(parents=True, exist_ok=True)
    record = {"message": {"id": "m1", "model": "claude-haiku-4-5",
                          "usage": {"input_tokens": tokens, "output_tokens": 0}}}
    (target / f"{session_id}.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")


def test_a_stale_ended_record_for_the_same_worktree_is_not_accepted_as_the_lane(tmp_path, monkeypatch):
    _transcript(tmp_path / "sessions", _SID, tokens=5_000)
    monkeypatch.setattr(d, "_control", _listing(_STALE, _LIVE))
    monkeypatch.setattr(d, "commit_witness", lambda slug: ("DONE", "1 commit"))
    binding = d.bind_lane("deadbeef")
    assert binding is not None and binding.live is False, "the stale record reads as ended"
    assert d._bind("deadbeef", "wave3-witness", 2, 0)[0] == "abcd1234", "the LIVE lane is the one bound"
    result = CliRunner().invoke(d.cli, ["govern", "deadbeef", "--slug", "wave3-witness",
                                        "--token-cap", "1000", "--interval", "0", "--bind-polls", "2",
                                        "--max-polls", "1", "--sessions-root", str(tmp_path / "sessions")])
    assert result.exit_code == d.EXIT_OVER_CAP


def test_there_is_no_verb_that_stops_a_lane_by_its_worktree():
    assert "stop" not in d.cli.commands
    assert not hasattr(d, "stop_lane") and not hasattr(d, "_recover")
