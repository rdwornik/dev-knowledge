"""RED-first witnesses for item 2b: a repair goes through the pre-launch moment too.

`repair_lane` gains `prelaunch`, `RepairRequest` gains `batch`, `run_prelaunch` gains `repair`, and
`worktree_occupancy` stops refusing the lane's OWN tree under HARNESS_REPAIR=1 (a busy session
there still refuses).
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

import dispatch as d
import worktree_occupancy as wo

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

SLUG = "lane-repair-x"
BATCH = "E2.0"


@pytest.fixture(autouse=True)
def receipts(tmp_path, monkeypatch):
    target = tmp_path / "receipts"
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(target))
    return target


@pytest.fixture
def repo_root(tmp_path):
    root = tmp_path / "repo"
    (root / ".claude" / "worktrees" / SLUG).mkdir(parents=True)
    return root


def _request(tmp_path, **over):
    contract = tmp_path / "LANE-REPAIR.md"
    contract.write_text("# LANE\n", encoding="utf-8")
    kw = dict(slug=SLUG, attempt=2, model="claude-sonnet-5-5", effort="high", contract=contract,
              batch=BATCH)
    kw.update(over)
    return d.RepairRequest(**kw)


class _Spawn:
    def __init__(self):
        self.calls = []

    def __call__(self, argv, env, cwd, log_path=None):
        self.calls.append((list(argv), Path(cwd)))
        return d.Spawned(returncode=0, stdout="backgrounded abcd1234\n", pid=1)


class _Prelaunch:
    def __init__(self, passed=True, reason=""):
        self.calls, self.result = [], d.PreLaunch(passed, reason)

    def __call__(self, request, repair=False):
        self.calls.append((request, repair))
        return self.result


# --- repair_lane --------------------------------------------------------------------------------

def test_a_repair_refused_by_pre_launch_raises_and_spawns_nothing(tmp_path, repo_root):
    spawn, pre = _Spawn(), _Prelaunch(False, "REFUSED [model-per-role]: substituted")

    with pytest.raises(d.DispatchRefused) as refused:
        d.repair_lane(_request(tmp_path), repo_root=repo_root, spawn=spawn, environ={}, prelaunch=pre)

    assert spawn.calls == []
    assert "REFUSED [model-per-role]" in str(refused.value.message)


def test_a_repair_hands_pre_launch_a_launch_request_built_from_the_repair_request(tmp_path, repo_root):
    pre = _Prelaunch()
    request = _request(tmp_path)

    d.repair_lane(request, repo_root=repo_root, spawn=_Spawn(), environ={}, prelaunch=pre)

    (launch, repair), = pre.calls
    assert repair is True
    assert isinstance(launch, d.LaunchRequest)
    assert (launch.slug, launch.provider, launch.model, launch.effort, launch.permission_mode,
            launch.contract, launch.batch) == (SLUG, "anthropic", request.model, request.effort,
                                               request.permission_mode, request.contract, BATCH)


def test_a_repair_cleared_by_pre_launch_spawns_once_and_leaves_a_repair_receipt(tmp_path, repo_root, receipts):
    spawn = _Spawn()

    d.repair_lane(_request(tmp_path), repo_root=repo_root, spawn=spawn, environ={}, prelaunch=_Prelaunch())

    assert len(spawn.calls) == 1
    body = json.loads((d.receipts_dir() / f"LAUNCH-{SLUG.upper()}.json").read_text(encoding="utf-8"))
    assert body["organ"] == "launch" and body["kind"] == "repair"
    assert body["attempt"] == 2 and body["batch"] == BATCH


def test_a_repair_with_no_worktree_is_still_refused_before_pre_launch_or_spawn(tmp_path):
    spawn, pre = _Spawn(), _Prelaunch()

    with pytest.raises(d.DispatchRefused):
        d.repair_lane(_request(tmp_path), repo_root=tmp_path / "no-repo", spawn=spawn, environ={},
                      prelaunch=pre)

    assert spawn.calls == [] and pre.calls == []


# --- run_prelaunch: HARNESS_REPAIR -------------------------------------------------------------

def _capture_env(monkeypatch):
    seen = {}

    def fake_run(argv, **kw):
        seen["env"] = kw.get("env") or {}
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")
    monkeypatch.setattr(d.subprocess, "run", fake_run)
    return seen


def _launch_request(tmp_path):
    return d.LaunchRequest(slug=SLUG, provider="anthropic", model="claude-sonnet-5-5", effort="high",
                           permission_mode="bypassPermissions", contract=tmp_path / "c.md", batch=BATCH)


def test_run_prelaunch_sets_harness_repair_only_for_a_repair(tmp_path, monkeypatch):
    monkeypatch.delenv("HARNESS_REPAIR", raising=False)
    seen = _capture_env(monkeypatch)

    d.run_prelaunch(_launch_request(tmp_path), repair=True)
    assert seen["env"].get("HARNESS_REPAIR") == "1"

    d.run_prelaunch(_launch_request(tmp_path))
    assert "HARNESS_REPAIR" not in seen["env"]


# --- worktree_occupancy under HARNESS_REPAIR ---------------------------------------------------

def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout


@pytest.fixture
def lane_repo(tmp_path):
    repo = tmp_path / "hub"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.invalid")
    _git(repo, "config", "user.name", "t")
    (repo / "f.txt").write_text("x", encoding="utf-8")
    _git(repo, "add", "f.txt")
    _git(repo, "commit", "-q", "-m", "init")
    _git(repo, "worktree", "add", "-q", "-b", f"worktree-{SLUG}", str(repo / ".claude" / "worktrees" / SLUG))
    return repo


def _occupancy(repo, sessions):
    sf = repo.parent / "sessions.json"
    sf.write_text(json.dumps(sessions), encoding="utf-8")
    return wo.main([SLUG, "--repo-root", str(repo), "--sessions-file", str(sf)])


@requires_git
def test_a_lane_tree_is_occupied_without_the_repair_flag(lane_repo, monkeypatch):
    monkeypatch.delenv("HARNESS_REPAIR", raising=False)
    assert _occupancy(lane_repo, []) == 1


@requires_git
def test_the_repair_flag_lets_the_lanes_own_worktree_directory_and_branch_through(lane_repo, monkeypatch):
    monkeypatch.setenv("HARNESS_REPAIR", "1")
    assert _occupancy(lane_repo, []) == 0


@requires_git
def test_the_repair_flag_does_not_let_a_busy_session_through(lane_repo, monkeypatch):
    monkeypatch.setenv("HARNESS_REPAIR", "1")
    busy = [{"id": "abcd1234", "cwd": str(lane_repo / ".claude" / "worktrees" / SLUG),
             "kind": "background", "status": "busy", "state": "working"}]
    assert _occupancy(lane_repo, busy) == 1
