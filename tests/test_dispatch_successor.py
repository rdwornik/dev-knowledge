"""RED-first witnesses for the `successor` verb: a fresh lane cut from a named BASE (not main's tip).

`SuccessorRequest` + `successor_lane` create `<repo>/.claude/worktrees/<slug>` on `worktree-<slug>` at the
resolved base sha, run the pre-launch moment BEFORE the worktree exists, spawn a FIRST-RUN prompt (no
repair wording), and leave a `kind: successor` LAUNCH receipt. Real git, fake spawn/prelaunch.
Also pins the batch requirement on the existing `repair` verb.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

import dispatch as d

SLUG = "lane-succ-x"
BATCH = "E2.0"
MODEL = "claude-sonnet-5-5"


@pytest.fixture(autouse=True)
def receipts(tmp_path, monkeypatch):
    target = tmp_path / "receipts"
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(target))
    return target


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout.strip()


def _commit(repo: Path, name: str, msg: str) -> str:
    (repo / name).write_text(msg, encoding="utf-8")
    _git(repo, "add", name)
    _git(repo, "-c", "user.name=t", "-c", "user.email=t@example.invalid", "commit", "-q", "-m", msg)
    return _git(repo, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "hub"
    root.mkdir()
    _git(root, "init", "-q", "-b", "main")
    return root


@pytest.fixture
def shas(repo):
    a = _commit(repo, "a.txt", "base A")
    _git(repo, "branch", "side", a)
    b = _commit(repo, "b.txt", "main tip B")
    return a, b


@pytest.fixture
def contract(tmp_path):
    path = tmp_path / "LANE-SUCC.md"
    path.write_text("# LANE\n", encoding="utf-8")
    return path


def _tree(repo: Path) -> Path:
    return repo / ".claude" / "worktrees" / SLUG


def _request(contract, base, **over):
    kw = dict(slug=SLUG, contract=contract, base=base, batch=BATCH, model=MODEL, effort="high")
    kw.update(over)
    return d.SuccessorRequest(**kw)


class _Spawn:
    def __init__(self, returncode=0):
        self.calls, self.returncode = [], returncode

    def __call__(self, argv, env, cwd, log_path=None):
        self.calls.append((list(argv), Path(cwd)))
        return d.Spawned(returncode=self.returncode, stdout="backgrounded abcd1234\n", pid=1)


class _Prelaunch:
    def __init__(self, passed=True, reason="", tree=None):
        self.calls, self.result, self.tree, self.tree_existed = [], d.PreLaunch(passed, reason), tree, None

    def __call__(self, request, repair=False):
        self.calls.append((request, repair))
        if self.tree is not None:
            self.tree_existed = self.tree.exists()
        return self.result


def _run(request, repo, spawn=None, pre=None):
    spawn = spawn or _Spawn()
    pre = pre or _Prelaunch()
    return d.successor_lane(request, repo_root=repo, spawn=spawn, environ={}, prelaunch=pre)


def _branches(repo: Path) -> str:
    return _git(repo, "branch", "--list", f"worktree-{SLUG}")


# --- request ------------------------------------------------------------------------------------

def test_argv_is_a_first_run_launch_with_no_repair_wording_and_no_worktree_flag(contract):
    request = _request(contract, "abc")
    argv = request.argv
    joined = " ".join(argv).lower()

    assert "refusal" not in joined and "repair" not in joined and "fix only" not in joined
    assert argv[-1] == f"Read and execute the frozen contract at {contract}"
    assert request.prompt == d.LaunchRequest(
        slug=SLUG, provider="anthropic", model=MODEL, effort="high", permission_mode="bypassPermissions",
        contract=contract, batch=BATCH).prompt
    assert request.session_name == SLUG
    assert "--bg" in argv and "--model" in argv and "--effort" in argv and "--permission-mode" in argv
    assert argv[argv.index("-n") + 1] == SLUG
    assert "--worktree" not in argv


# --- worktree creation --------------------------------------------------------------------------

def test_a_call_creates_the_worktree_at_the_base_not_the_main_tip(repo, shas, contract):
    a, b = shas
    spawn = _Spawn()

    _run(_request(contract, a), repo, spawn)

    tree = _tree(repo)
    assert tree.is_dir()
    assert _git(tree, "rev-parse", "HEAD") == a != b
    assert _git(tree, "rev-parse", "--abbrev-ref", "HEAD") == f"worktree-{SLUG}"
    (argv, cwd), = spawn.calls
    assert cwd == tree


def test_base_may_be_a_ref_name_and_the_receipt_records_the_resolved_sha(repo, shas, contract):
    a, _ = shas

    _run(_request(contract, "side"), repo)

    assert _git(_tree(repo), "rev-parse", "HEAD") == a
    body = json.loads((d.receipts_dir() / f"LAUNCH-{SLUG.upper()}.json").read_text(encoding="utf-8"))
    assert body["base"] == a and len(body["base"]) == 40


# --- pre-launch ---------------------------------------------------------------------------------

def test_prelaunch_gets_a_launch_request_with_repair_false_before_the_worktree_exists(repo, shas, contract):
    a, _ = shas
    pre = _Prelaunch(tree=_tree(repo))

    _run(_request(contract, a), repo, pre=pre)

    (launch, repair), = pre.calls
    assert repair is False
    assert pre.tree_existed is False
    assert isinstance(launch, d.LaunchRequest)
    assert (launch.slug, launch.provider, launch.model, launch.effort, launch.batch, launch.contract) == (
        SLUG, "anthropic", MODEL, "high", BATCH, contract)


def test_a_prelaunch_refusal_raises_and_leaves_no_worktree_or_branch(repo, shas, contract):
    a, _ = shas
    spawn, pre = _Spawn(), _Prelaunch(False, "REFUSED [x]: y")

    with pytest.raises(d.DispatchRefused) as refused:
        _run(_request(contract, a), repo, spawn, pre)

    assert "REFUSED [x]: y" in str(refused.value.message)
    assert spawn.calls == []
    assert not _tree(repo).exists()
    assert _branches(repo) == ""


# --- receipt ------------------------------------------------------------------------------------

def test_the_receipt_records_a_successor_launch(repo, shas, contract):
    a, _ = shas

    _run(_request(contract, a), repo)

    body = json.loads((d.receipts_dir() / f"LAUNCH-{SLUG.upper()}.json").read_text(encoding="utf-8"))
    assert body["organ"] == "launch" and body["kind"] == "successor"
    assert body["batch"] == BATCH and body["base"] == a
    assert body["job_id"] == "abcd1234"


# --- refusals before any side effect ------------------------------------------------------------

@pytest.mark.parametrize("what", ["bad-base", "empty-batch", "bogus-batch", "junk-batch", "no-contract"])
def test_refusals_spawn_nothing_run_no_prelaunch_and_create_no_worktree(repo, shas, contract, tmp_path, what):
    a, _ = shas
    over = {"bad-base": dict(base="nonexistent-ref"), "empty-batch": dict(batch=""),
            "bogus-batch": dict(batch="bogus"), "junk-batch": dict(batch="E2.0junk"),
            "no-contract": dict(contract=tmp_path / "missing.md")}[what]
    over.setdefault("base", a)
    over.setdefault("contract", contract)
    request = d.SuccessorRequest(**{**dict(slug=SLUG, batch=BATCH, model=MODEL, effort="high"), **over})
    spawn, pre = _Spawn(), _Prelaunch()

    with pytest.raises(d.DispatchRefused):
        _run(request, repo, spawn, pre)

    assert spawn.calls == [] and pre.calls == []
    assert not _tree(repo).exists()


# --- existing worktree --------------------------------------------------------------------------

def test_an_existing_worktree_at_the_same_base_is_reused(repo, shas, contract):
    a, _ = shas
    _git(repo, "worktree", "add", "-q", "-b", f"worktree-{SLUG}", str(_tree(repo)), a)
    spawn, pre = _Spawn(), _Prelaunch()

    _run(_request(contract, a), repo, spawn, pre)

    assert len(spawn.calls) == 1
    (_, repair), = pre.calls
    assert repair is True


def test_an_existing_worktree_at_a_different_commit_is_refused(repo, shas, contract):
    a, b = shas
    _git(repo, "worktree", "add", "-q", "-b", f"worktree-{SLUG}", str(_tree(repo)), b)
    spawn, pre = _Spawn(), _Prelaunch()

    with pytest.raises(d.DispatchRefused) as refused:
        _run(_request(contract, a), repo, spawn, pre)

    assert SLUG in str(refused.value.message)
    assert spawn.calls == []


# --- spawn failure ------------------------------------------------------------------------------

def test_a_failed_spawn_raises_and_leaves_no_success_receipt(repo, shas, contract):
    a, _ = shas

    with pytest.raises(d.LaunchRefused):
        _run(_request(contract, a), repo, _Spawn(returncode=1))

    path = d.receipts_dir() / f"LAUNCH-{SLUG.upper()}.json"
    if path.exists():
        assert json.loads(path.read_text(encoding="utf-8")).get("exit_code") != 0


# --- CLI ----------------------------------------------------------------------------------------

def _no_spawn(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("spawn_process must not be called")
    monkeypatch.setattr(d, "spawn_process", boom)


def test_cli_successor_with_a_bogus_batch_exits_nonzero_and_spawns_nothing(repo, shas, contract, monkeypatch):
    a, _ = shas
    _no_spawn(monkeypatch)

    out = CliRunner().invoke(d.cli, ["successor", SLUG, str(contract), "--base", a, "--batch", "bogus",
                                     "--model", MODEL, "--effort", "low", "--repo-root", str(repo)])

    assert out.exit_code != 0
    assert not _tree(repo).exists()


def test_cli_successor_command_exposes_base_batch_model_and_effort():
    command = d.cli.commands["successor"]

    assert {"base", "batch", "model", "effort"} <= {p.name for p in command.params}


# --- the repair verb requires a batch too -------------------------------------------------------

def test_repair_lane_with_an_empty_batch_is_refused_and_spawns_nothing(tmp_path, contract):
    tree = tmp_path / "repo" / ".claude" / "worktrees" / SLUG
    tree.mkdir(parents=True)
    spawn = _Spawn()
    request = d.RepairRequest(slug=SLUG, attempt=1, model=MODEL, effort="high", contract=contract, batch="")

    with pytest.raises(d.DispatchRefused) as refused:
        d.repair_lane(request, repo_root=tmp_path / "repo", spawn=spawn, environ={}, prelaunch=_Prelaunch())

    assert "batch" in str(refused.value.message)
    assert spawn.calls == []


def test_cli_repair_with_a_bogus_batch_exits_nonzero(tmp_path, contract, monkeypatch):
    (tmp_path / "repo" / ".claude" / "worktrees" / SLUG).mkdir(parents=True)
    _no_spawn(monkeypatch)

    out = CliRunner().invoke(d.cli, ["repair", SLUG, str(contract), "--batch", "bogus", "--model", MODEL,
                                     "--effort", "high", "--repo-root", str(tmp_path / "repo")])

    assert out.exit_code != 0
