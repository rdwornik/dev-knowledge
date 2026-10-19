"""RED tests: M1 phase rows need a registry role, M2 repair needs a batch, M3 occupancy under repair."""
import sys; sys.path.insert(0, "/workspaces/dev-knowledge/scripts")  # noqa: E702
import json
import subprocess
from pathlib import Path

import pytest

import subst_gate as sg
import dispatch as d
import worktree_occupancy as wo

SONNET = "claude-sonnet-5-5"
TERRA = "gpt-5.6-terra"
SLUG = "lane-repair-x"
BATCH = "E2.0"

_PHASE_ROWS = {
    "implement": f"| implement code (lane head) | {SONNET} | local |",
    "red": "| write the RED / isolated tests | Copilot CLI (default model) | codespace |",
    "copilot": "| review, Copilot half | Copilot CLI (default model) | codespace |",
    "codex": f"| review, Codex half | {TERRA} | local |",
    "verify": f"| isolated verify | {SONNET} | local |",
    "orchestrate": f"| orchestrate the batch | {SONNET} | local |",
}


def _contract(*, head=SONNET, dispatch=SONNET, rows=None, lane="lane-x", table=True):
    rows = dict(_PHASE_ROWS, **(rows or {}))
    text = (
        f"# LANE {lane} -- a test contract\n\n"
        "| Model | Mode | Effort |\n|---|---|---|\n"
        f"| {head} | execute | high |\n\n"
        "## Dispatch\n\n```\n"
        f"claude --bg -n {lane} --model {dispatch} --effort high --permission-mode bypassPermissions "
        f"--worktree {lane} \"Read and execute the frozen contract\"\n```\n\n"
    )
    if table:
        text += "| Phase | Model | Substrate |\n|---|---|---|\n" + "\n".join(rows.values()) + "\n"
    return text


def _problems(text, **kw):
    kw.setdefault("lane", "lane-x")
    kw.setdefault("batch", "E2.0")
    return sg.contract_problems(text, **kw)


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


@pytest.fixture
def plain_repo(tmp_path):
    repo = tmp_path / "plain"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.invalid")
    _git(repo, "config", "user.name", "t")
    (repo / "f.txt").write_text("x", encoding="utf-8")
    _git(repo, "add", "f.txt")
    _git(repo, "commit", "-q", "-m", "init")
    return repo


# --- M1 ------------------------------------------------------------------------------------------

def test_m1_a_phase_row_with_no_registry_role_is_refused_in_an_applicable_batch():
    text = _contract(rows={"build": "| build | grok-4.7 | codespace |"})
    problems, _ = _problems(text, launch_model=SONNET)
    assert any(p.startswith("REFUSED [model-per-role]") and "phase 'build' maps to no registry role" in p
               for p in problems), problems


def test_m1_the_default_conforming_contract_has_no_problems():
    problems, _ = _problems(_contract(), launch_model=SONNET)
    assert problems == []


def test_m1_no_phase_table_in_an_old_batch_is_not_applicable():
    problems, _ = _problems(_contract(table=False), batch="Y")
    assert problems == []


# --- M2 ------------------------------------------------------------------------------------------

def _repair_cli(tmp_path, repo_root, monkeypatch, extra):
    from click.testing import CliRunner
    monkeypatch.delenv("HARNESS_BATCH", raising=False)
    contract = tmp_path / "LANE.md"
    contract.write_text("# LANE\n", encoding="utf-8")
    seen, spawned = [], []
    monkeypatch.setattr(d, "run_prelaunch",
                        lambda request, repair=False: seen.append(request.batch) or d.PreLaunch(True))
    monkeypatch.setattr(d, "spawn_process",
                        lambda argv, env, cwd, log_path=None: spawned.append(argv)
                        or d.Spawned(0, "backgrounded abcd1234\n", 1))
    out = CliRunner().invoke(d.cli, ["repair", SLUG, str(contract), "--model", "claude-sonnet-5-5",
                                     "--effort", "high", "--repo-root", str(repo_root), *extra])
    return out, seen, spawned


def test_m2_a_repair_with_no_batch_and_no_receipt_is_refused(tmp_path, repo_root, monkeypatch):
    out, seen, spawned = _repair_cli(tmp_path, repo_root, monkeypatch, [])
    assert out.exit_code != 0
    assert "--batch" in out.output
    assert seen == [] and spawned == []


def test_m2_a_repair_with_an_explicit_batch_and_no_receipt_runs(tmp_path, repo_root, receipts, monkeypatch):
    out, seen, spawned = _repair_cli(tmp_path, repo_root, monkeypatch, ["--batch", "E2.0"])
    assert out.exit_code == 0, out.output
    assert seen == ["E2.0"]
    assert len(spawned) == 1
    body = json.loads((receipts / f"LAUNCH-{SLUG.upper()}.json").read_text(encoding="utf-8"))
    assert body["batch"] == "E2.0"


def test_m2_a_repair_of_a_pre_e2_batch_still_runs(tmp_path, repo_root, monkeypatch):
    out, seen, spawned = _repair_cli(tmp_path, repo_root, monkeypatch, ["--batch", "E1.5"])
    assert out.exit_code == 0, out.output
    assert seen == ["E1.5"]
    assert len(spawned) == 1


# --- M3 ------------------------------------------------------------------------------------------

def test_m3_a_bare_directory_that_is_not_a_worktree_is_refused_under_repair(plain_repo, monkeypatch):
    monkeypatch.setenv("HARNESS_REPAIR", "1")
    (plain_repo / ".claude" / "worktrees" / SLUG).mkdir(parents=True)
    assert _occupancy(plain_repo, []) != 0


def test_m3_the_real_lane_worktree_is_accepted_under_repair(lane_repo, monkeypatch):
    monkeypatch.setenv("HARNESS_REPAIR", "1")
    assert _occupancy(lane_repo, []) == 0


def test_m3_a_registered_worktree_with_no_lane_branch_is_refused_under_repair(plain_repo, monkeypatch):
    monkeypatch.setenv("HARNESS_REPAIR", "1")
    _git(plain_repo, "worktree", "add", "-q", "--detach", str(plain_repo / ".claude" / "worktrees" / SLUG))
    assert _occupancy(plain_repo, []) != 0


def test_m3_a_busy_session_in_the_lane_tree_still_refuses_under_repair(lane_repo, monkeypatch):
    monkeypatch.setenv("HARNESS_REPAIR", "1")
    busy = [{"id": "abcd1234", "cwd": str(lane_repo / ".claude" / "worktrees" / SLUG),
             "kind": "background", "status": "busy", "state": "working"}]
    assert _occupancy(lane_repo, busy) == 1




# --- R2: M3 wrong branch -------------------------------------------------------------------------

def test_r2_m3_the_lane_own_worktree_on_its_branch_is_accepted(lane_repo, monkeypatch):
    monkeypatch.setenv("HARNESS_REPAIR", "1")
    assert _occupancy(lane_repo, []) == 0


def test_r2_m3_a_lane_worktree_switched_to_another_branch_is_refused(lane_repo, monkeypatch):
    monkeypatch.setenv("HARNESS_REPAIR", "1")
    tree = lane_repo / ".claude" / "worktrees" / SLUG
    _git(tree, "checkout", "-q", "-b", "other")
    assert f"worktree-{SLUG}" in _git(lane_repo, "branch", "--list")
    assert _occupancy(lane_repo, []) != 0


def test_r2_m3_a_detached_lane_worktree_is_refused(lane_repo, monkeypatch):
    monkeypatch.setenv("HARNESS_REPAIR", "1")
    tree = lane_repo / ".claude" / "worktrees" / SLUG
    _git(tree, "checkout", "-q", "--detach")
    assert f"worktree-{SLUG}" in _git(lane_repo, "branch", "--list")
    assert _occupancy(lane_repo, []) != 0


def test_r2_m3_check_raises_for_a_wrong_branch_worktree(lane_repo, monkeypatch):
    monkeypatch.setenv("HARNESS_REPAIR", "1")
    tree = lane_repo / ".claude" / "worktrees" / SLUG
    _git(tree, "checkout", "-q", "-b", "other")
    with pytest.raises(wo.OccupancyError):
        wo.check(SLUG, lane_repo, sessions=[])


# --- R2: M2 malformed batch ----------------------------------------------------------------------

@pytest.mark.parametrize("b", ["x", "E2.0junk"])
def test_r2_m2_repair_cli_refuses_a_malformed_batch(tmp_path, repo_root, monkeypatch, b):
    out, seen, spawned = _repair_cli(tmp_path, repo_root, monkeypatch, ["--batch", b])
    assert out.exit_code != 0
    assert "batch" in out.output.lower()
    assert seen == [] and spawned == []


def test_r2_m2_a_well_formed_batch_is_accepted(tmp_path, repo_root, monkeypatch):
    problems, _ = _problems(_contract(), batch="E2.0", launch_model=SONNET)
    assert problems == []
    out, _seen, _spawned = _repair_cli(tmp_path, repo_root, monkeypatch, ["--batch", "E2.0"])
    assert out.exit_code == 0, out.output


def test_r2_m2_an_older_grammatical_batch_is_not_applicable():
    problems, notes = _problems(_contract(table=False), batch="E1.0")
    assert problems == []
    assert any("not applicable" in n for n in notes), notes


def test_r2_m2_batch_applies_rejects_junk_and_accepts_e2():
    assert sg.batch_applies("E2.0junk") is False
    assert sg.batch_applies("E2.0") is True
