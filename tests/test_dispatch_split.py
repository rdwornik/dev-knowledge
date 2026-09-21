"""The contract table, the prompts directory and the commit witness -- the parts of the wave-3 split
that survive LANE-W3-B.

SUPERSEDED BY R-W3-2 (2026-09-21): the 2026-09-19 split said the hub PLANS and GOVERNS while a
caller-side shim SPAWNS, and that a governor stops a lane past its cap. R-W3-2 moved the spawn into
`dispatch.py launch` and made `govern` a monitor that never stops a lane (N3). The tests that
pinned the old split -- "the hub spawns nothing", "no launch verb", "a bound lane over its cap is
stopped" -- were replaced by `tests/test_dispatch_launch.py`, which asserts the opposite on purpose.

Nothing here launches `claude`, `codex` or `gh`.
"""
from __future__ import annotations

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


# --- DONE-WHEN 1: an unbindable launch is REFUSED and its lane STOPPED, never left running ------


# --- DONE-WHEN 2: the split ---------------------------------------------------------------------


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


