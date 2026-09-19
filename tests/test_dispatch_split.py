"""Wave-3 L3 split -- the hub PLANS and GOVERNS a lane, a caller-side shim SPAWNS it. RED-first.

Two rulings bind this file (protocols/BUILD-LIST.md Decisions, 2026-09-19 "Dispatch / Layer 2"):

  LAYER-2   the hub ships the code, the caller runs it. `scripts/dispatch.py` plans and governs;
            it never starts a lane. CLAUDE.md section 5 rule 4.
  TOKEN CAP a default `--bg --worktree` launch binds its OWN usage with no `--slug-dir`; a launch
            whose usage cannot be bound, or that runs over its cap, is REFUSED / STOPPED -- never
            left running and reported as ungoverned.

Nothing here launches `claude`, `codex` or `gh`. The control-plane seams (`bind_lane`, `stop_lane`,
`lane_alive`) are replaced by recorders, and the session store is a temp directory.
"""
from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

import dispatch as d
import lane_cost as lc

REPO = Path(__file__).resolve().parents[1]
SHIM = REPO / "templates" / "dispatch-shim.ps1"

CONTRACT = """# LANE wave3-witness -- a test contract

| Model | Mode | Effort |
|---|---|---|
| haiku | execute | low |

## Steps
1. Do nothing.
"""


SID = "11111111-2222-3333-4444-555555555555"
CWD = "C:\\repo\\.claude\\worktrees\\wave3-witness"  # a `--bg --worktree` lane's cwd is its worktree


def _usage(fresh: int = 0) -> lc.TokenUsage:
    return lc.TokenUsage(input_tokens=fresh, calls=1)


def _transcript(root: Path, session_id: str, tokens: int, directory: str = "any-dir") -> Path:
    """One session transcript, filed under an arbitrary directory: binding is by SESSION ID."""
    target = root / directory
    target.mkdir(parents=True, exist_ok=True)
    path = target / f"{session_id}.jsonl"
    record = {"message": {"id": "m1", "model": "claude-haiku-4-5",
                          "usage": {"input_tokens": tokens, "output_tokens": 0}}}
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    return path


class _Seams:
    """Recorders for the three control-plane calls a govern run makes."""

    def __init__(self, monkeypatch, binding=None, alive=True):
        self.stopped: list[str] = []
        monkeypatch.setattr(d, "bind_lane", lambda lane_id: binding)
        monkeypatch.setattr(d, "find_lane_by_slug", lambda slug: None)
        monkeypatch.setattr(d, "stop_lane", lambda lane_id: self.stopped.append(lane_id) or True)
        monkeypatch.setattr(d, "lane_alive", lambda lane_id: alive)


def _govern(root: Path, *extra: str, cap: str = "1000"):
    return CliRunner().invoke(d.cli, ["govern", "abcd1234", "--slug", "wave3-witness",
                                      "--token-cap", cap, "--interval", "0",
                                      "--sessions-root", str(root), *extra])


# --- DONE-WHEN 1: an unbindable launch is REFUSED and its lane STOPPED, never left running ------

def test_a_lane_whose_usage_cannot_be_read_is_stopped_not_left_running():
    """The unit form. Before the fix an unobservable lane was REPORTED ungoverned and left to run
    -- 'fails loud, does not cap'. Now it is stopped, and the exit code is a refusal."""
    stopped = []
    verdict = d.govern(cap=100, read_usage=lambda: None, stop=lambda: stopped.append(True) or True,
                       sleep=lambda s: None, blind_polls=3)
    assert stopped == [True], "an unbindable lane must be STOPPED, not left running"
    assert verdict.exit_code == d.EXIT_REFUSED != d.EXIT_UNGOVERNED


def test_a_default_launch_that_cannot_be_bound_is_refused_and_the_lane_stopped(
        tmp_path, monkeypatch):
    """No `--slug-dir`, no session id in the agent listing: nothing to bind. REFUSED, stopped."""
    seams = _Seams(monkeypatch, binding=None)
    result = _govern(tmp_path)
    assert seams.stopped == ["abcd1234"], "the unbound lane must be stopped"
    assert result.exit_code == d.EXIT_REFUSED
    assert "UNGOVERNED" not in result.output


def test_a_bound_lane_whose_transcript_never_appears_is_refused_and_stopped(
        tmp_path, monkeypatch):
    """Bound to a session id, but no transcript for it exists: the usage is still unreadable."""
    seams = _Seams(monkeypatch, binding=d.LaneBinding(SID, CWD))
    result = _govern(tmp_path)
    assert seams.stopped == ["abcd1234"]
    assert result.exit_code == d.EXIT_REFUSED


def test_a_bound_lane_over_its_cap_is_stopped_with_no_slug_dir(tmp_path, monkeypatch):
    """The transcript is found by SESSION ID under an arbitrary directory -- no slug matching,
    no `--slug-dir`. Its usage passes the cap: the lane is stopped, exit is CAP EXCEEDED."""
    sid = "11111111-2222-3333-4444-555555555555"
    _transcript(tmp_path, sid, tokens=5_000)
    seams = _Seams(monkeypatch, binding=d.LaneBinding(sid, CWD))
    result = _govern(tmp_path, cap="1000")
    assert seams.stopped == ["abcd1234"]
    assert result.exit_code == d.EXIT_CAP_EXCEEDED
    assert "5000" in result.output and "1000" in result.output


def test_a_bound_lane_under_its_cap_is_left_alone(tmp_path, monkeypatch):
    sid = "11111111-2222-3333-4444-555555555555"
    _transcript(tmp_path, sid, tokens=50)
    seams = _Seams(monkeypatch, binding=d.LaneBinding(sid, CWD), alive=False)
    monkeypatch.setattr(d, "commit_witness", lambda slug: ("DONE", "1 commit"))
    result = _govern(tmp_path, cap="1000")
    assert seams.stopped == [] and result.exit_code == 0


# --- DONE-WHEN 2: the split ---------------------------------------------------------------------

def test_the_hub_dispatch_module_spawns_no_lane():
    """No `Popen`, no `os.system`, and no `subprocess.run` of a PLAN's argv. `subprocess.run` is
    still allowed for the control plane (`claude stop`, `claude agents`, `git`), which is not a
    spawn of a lane."""
    tree = ast.parse((REPO / "scripts" / "dispatch.py").read_text(encoding="utf-8"))
    spawns = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in {"Popen", "system", "startfile"}:
            spawns.append(node.attr)
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "run" and node.args
                and isinstance(node.args[0], ast.Attribute) and node.args[0].attr == "argv"):
            spawns.append("run(plan.argv)")
    assert spawns == []


def test_the_cli_exposes_plan_and_govern_and_no_launch_verb():
    assert {"plan", "govern"} <= set(d.cli.commands)
    assert "launch" not in d.cli.commands, "a `launch` verb is a hub script that spawns a lane"


def test_the_shim_ships_from_the_hub_and_has_no_model_or_effort_default():
    """[#717]: a default model silently re-decides the most expensive constant on the line."""
    assert SHIM.is_file(), f"the caller-side shim must ship from the hub at {SHIM}"
    text = SHIM.read_text(encoding="utf-8")
    assert "$TokenCap" in text and "Mandatory" in text
    assert "'opus'" not in text and '"opus"' not in text
    assert "[string]$Model =" not in text and "[string]$Effort =" not in text


def test_the_shim_spawns_and_the_hub_plans_and_governs():
    text = SHIM.read_text(encoding="utf-8")
    assert "dispatch.py" in text and " plan" in text and "govern" in text
    assert "--bg" not in text, "the argv comes from the hub's plan; the shim hard-codes none of it"


# --- DONE-WHEN 4: the three preserved behaviours ------------------------------------------------

def test_model_and_effort_come_from_the_contract_table(tmp_path):
    contract = tmp_path / "LANE-wave3-witness.md"
    contract.write_text(CONTRACT, encoding="utf-8")
    result = CliRunner().invoke(d.cli, ["plan", str(contract), "--token-cap", "1000"])
    assert result.exit_code == 0, result.output
    plan = json.loads(result.output)
    assert plan["model"] == "haiku" and plan["effort"] == "low"
    assert plan["argv"][plan["argv"].index("--model") + 1] == "haiku"
    assert plan["argv"][plan["argv"].index("--effort") + 1] == "low"
    assert plan["slug"] == "wave3-witness"


def test_a_contract_with_no_model_effort_table_is_refused_not_defaulted_to_opus(tmp_path):
    contract = tmp_path / "LANE-no-table.md"
    contract.write_text("# LANE no-table\n\nJust prose.\n", encoding="utf-8")
    result = CliRunner().invoke(d.cli, ["plan", str(contract), "--token-cap", "1000"])
    assert result.exit_code != 0
    assert "opus" not in result.output.lower().replace("no default", "")
    assert "model" in result.output.lower()


@pytest.mark.parametrize("row", ["| | execute | high |", "| sonnet | execute | turbo |",
                                 "| sonnet | execute |"])
def test_a_table_with_an_unparseable_model_or_effort_is_refused(tmp_path, row):
    contract = tmp_path / "LANE-bad.md"
    contract.write_text(f"| Model | Mode | Effort |\n|---|---|---|\n{row}\n", encoding="utf-8")
    result = CliRunner().invoke(d.cli, ["plan", str(contract), "--token-cap", "1000"])
    assert result.exit_code != 0
    assert "No such command" not in result.output, "refused by `plan`, not absent"
    assert "model" in result.output.lower() or "effort" in result.output.lower()


def test_an_explicit_model_flag_overrides_the_contract(tmp_path):
    contract = tmp_path / "LANE-wave3-witness.md"
    contract.write_text(CONTRACT, encoding="utf-8")
    plan = json.loads(CliRunner().invoke(
        d.cli, ["plan", str(contract), "--token-cap", "1000", "--model", "sonnet"]).output)
    assert plan["model"] == "sonnet"


def test_the_prompts_dir_is_read_from_the_user_scope_value_before_the_process_copy():
    """The Windows User registry is the authority; a stale process copy loses to it."""
    got = d.prompts_dir(environ={"CLAUDE_PROMPTS_DIR": r"C:\stale"}, home="/h",
                        root_exists=lambda p: True,
                        user_scope=lambda name: r"C:\authority" if name == "CLAUDE_PROMPTS_DIR" else None)
    assert str(got) == r"C:\authority"


def test_the_process_copy_is_the_fallback_when_no_user_scope_value_exists():
    got = d.prompts_dir(environ={"CLAUDE_PROMPTS_DIR": r"C:\proc"}, home="/h",
                        root_exists=lambda p: True, user_scope=lambda name: None)
    assert str(got) == r"C:\proc"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          check=True).stdout.strip()


@pytest.fixture
def repo(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "t")
    _git(root, "config", "commit.gpgsign", "false")
    (root / "a.txt").write_text("a")
    _git(root, "add", "a.txt")
    _git(root, "commit", "-q", "-m", "base")
    monkeypatch.chdir(root)
    return root


def test_done_means_a_commit_a_lane_that_committed_nothing_is_failed(repo):
    _git(repo, "branch", "worktree-wave3-witness")
    verdict, reason = d.commit_witness("wave3-witness")
    assert verdict == "FAILED" and "no commit" in reason


def test_done_means_a_commit_a_lane_that_committed_is_done(repo):
    _git(repo, "switch", "-q", "-c", "worktree-wave3-witness")
    (repo / "b.txt").write_text("b")
    _git(repo, "add", "b.txt")
    _git(repo, "commit", "-q", "-m", "lane work")
    verdict, reason = d.commit_witness("wave3-witness")
    assert verdict == "DONE" and "1" in reason


def test_done_means_a_commit_an_absent_branch_is_failed_not_done(repo):
    assert d.commit_witness("never-created")[0] == "FAILED"


def test_done_means_a_commit_git_that_cannot_be_asked_is_unwitnessed(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # not a repository
    assert d.commit_witness("wave3-witness")[0] == "UNWITNESSED"


def test_a_lane_that_finishes_under_cap_but_committed_nothing_does_not_exit_zero(
        tmp_path, monkeypatch):
    sid = "11111111-2222-3333-4444-555555555555"
    _transcript(tmp_path, sid, tokens=50)
    _Seams(monkeypatch, binding=d.LaneBinding(sid, CWD), alive=False)
    monkeypatch.setattr(d, "commit_witness", lambda slug: ("FAILED", "no commit on the branch"))
    result = _govern(tmp_path, cap="1000")
    assert result.exit_code == d.EXIT_NO_COMMIT != 0
    assert "FAILED" in result.output
