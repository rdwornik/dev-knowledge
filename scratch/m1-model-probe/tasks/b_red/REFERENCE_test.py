"""KEY (never shown to a cell): the reference RED test for [#1572], used to prove the checker can
tell a good RED test from a bad one. Copied to tests/ in a throwaway clone only."""
from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

import dispatch as d
from test_dispatch_queue import _contract


@pytest.fixture(autouse=True)
def receipts(tmp_path, monkeypatch):
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(tmp_path / "receipts"))


def test_queue_skips_an_already_launched_lane_and_fires_the_rest(tmp_path, monkeypatch):
    root = tmp_path / "root"
    root.mkdir()
    contracts = [_contract(tmp_path, f"LANE-{n}.md", n, head="claude") for n in ("lane-1", "lane-2", "lane-3")]
    spawned: list[str] = []

    def fake_spawn(argv, env, cwd, log_path=None):
        spawned.append(argv[argv.index("-n") + 1])
        return d.Spawned(returncode=0, stdout="backgrounded abcd1234\n", pid=4321)

    def fake_agents():
        live = [{"id": "live0001", "sessionId": "sid-0", "name": "lane-1",
                 "cwd": str(root / ".claude" / "worktrees" / "lane-1"), "state": "working", "status": "busy"}]
        for i, name in enumerate(spawned):
            live.append({"id": "abcd1234", "sessionId": f"sid-{i + 1}", "name": name,
                         "cwd": str(root / ".claude" / "worktrees" / name), "state": "working", "status": "busy"})
        return live

    monkeypatch.setattr(d, "run_prelaunch", lambda request: d.PreLaunch(passed=True))
    monkeypatch.setattr(d, "spawn_process", fake_spawn)
    monkeypatch.setattr(d, "list_agents", fake_agents)

    out = CliRunner().invoke(d.cli, ["queue", *map(str, contracts), "--repo-root", str(root), "--floor-mb", "0"])
    assert out.exit_code == 0, f"queue must not halt on an already-launched lane (exit 5): {out.output}"
    assert "lane-2" in spawned and "lane-3" in spawned, spawned
    assert "lane-1" not in spawned
    assert "already-launched" in out.output
