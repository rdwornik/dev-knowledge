"""Codex terra fourth pass (docs/audits/2026-09-19-codex-wave3-dispatch-split-rereview-3.md).

CRITICAL 1 -- a stale ENDED record for the same worktree must not be accepted as the lane.
CRITICAL 2 -- the shim needs a hub verb that stops a lane by its worktree, so a governor that failed
to even start can be recovered; that verb is `stop`.
"""
from __future__ import annotations

import json
import subprocess

from click.testing import CliRunner

import dispatch as d

_SID = "11111111-2222-3333-4444-555555555555"
_CWD = "C:\\repo\\.claude\\worktrees\\wave3-witness"
_LIVE = {"id": "abcd1234", "sessionId": _SID, "state": "working", "cwd": _CWD}
_STALE = {"id": "deadbeef", "sessionId": "99999999-0000-0000-0000-000000000000",
          "state": "done", "cwd": _CWD}


def _listing(*entries):
    return lambda argv: subprocess.CompletedProcess(argv, 0, json.dumps(list(entries)), "")


def _transcript(root, session_id, tokens):
    target = root / "any-dir"
    target.mkdir(parents=True, exist_ok=True)
    record = {"message": {"id": "m1", "model": "claude-haiku-4-5",
                          "usage": {"input_tokens": tokens, "output_tokens": 0}}}
    (target / f"{session_id}.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")


def test_a_stale_ended_record_for_the_same_worktree_is_not_accepted_as_the_lane(
        tmp_path, monkeypatch):
    """CRITICAL (dispatch.py:783): a false shim id that names an old `done` record for the same
    worktree used to bind, get stopped, and leave the newly launched live lane uncapped."""
    _transcript(tmp_path, _SID, tokens=5_000)
    stopped = []
    monkeypatch.setattr(d, "_control", _listing(_STALE, _LIVE))
    monkeypatch.setattr(d, "stop_lane", lambda lane_id: stopped.append(lane_id) or True)
    result = CliRunner().invoke(d.cli, ["govern", "deadbeef", "--slug", "wave3-witness",
                                        "--token-cap", "1000", "--interval", "0",
                                        "--bind-polls", "2", "--sessions-root", str(tmp_path)])
    assert "deadbeef" not in stopped, "a finished record must never be the verified lane"
    assert stopped == ["abcd1234"] and result.exit_code == d.EXIT_CAP_EXCEEDED


def test_stop_verb_stops_the_one_live_lane_for_a_worktree_and_exits_5(monkeypatch):
    stopped = []
    monkeypatch.setattr(d, "_control", _listing(_STALE, _LIVE))
    monkeypatch.setattr(d, "stop_lane", lambda lane_id: stopped.append(lane_id) or True)
    result = CliRunner().invoke(d.cli, ["stop", "--slug", "wave3-witness"])
    assert stopped == ["abcd1234"] and result.exit_code == d.EXIT_REFUSED


def test_stop_verb_with_no_live_lane_stops_nothing_and_exits_4(monkeypatch):
    stopped = []
    monkeypatch.setattr(d, "_control", _listing(_STALE))
    monkeypatch.setattr(d, "stop_lane", lambda lane_id: stopped.append(lane_id) or True)
    result = CliRunner().invoke(d.cli, ["stop", "--slug", "wave3-witness"])
    assert stopped == [] and result.exit_code == d.EXIT_UNGOVERNED
    assert "running" in result.output.lower()


def test_stop_verb_whose_stop_fails_exits_4(monkeypatch):
    monkeypatch.setattr(d, "_control", _listing(_LIVE))
    monkeypatch.setattr(d, "stop_lane", lambda lane_id: False)
    result = CliRunner().invoke(d.cli, ["stop", "--slug", "wave3-witness"])
    assert result.exit_code == d.EXIT_UNGOVERNED
