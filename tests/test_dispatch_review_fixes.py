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
