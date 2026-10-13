"""Tests for scripts/hooks/reuse_gate.py -- the PreToolUse reuse gate (batch BW lane
`lane-bw-735-reuse-gate`, `[#735]` nearest; R96 D7, package T5.2).

RED-first: written before the module existed. Organised as the lane's Done-contract:

  1. DENY     a Write/Edit creating a NEW file under `scripts/` or `.claude/` is refused when the
              active lane contract's Done-contract does not name it AND no `why` record for a
              neighbour exists for this lane.
  2. ALLOW    an existing file; a named file (or a named directory below the guarded root); a new
              file after a recorded `why` search; any path outside `scripts/` and `.claude/`.
              Outside a lane (no active contract) the rule allows AND logs -- never a wedge.
  3. REMEDY   the deny message is ONE line and names `/why <neighbour>` or naming the file.
  4. WIRE     registered in `.claude/settings.json` through the shared launcher, and the declared
              command works under bash, pwsh and Windows PowerShell (the launcher's own harness).

The pure core (`decide`) takes the repo root and the environment as arguments, so every leg runs
against a throwaway mini-repo rather than the live tree.
"""
from __future__ import annotations

import importlib.util
import json
import logging
import os
import subprocess
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SCRIPT = _REPO / "scripts" / "hooks" / "reuse_gate.py"
_SETTINGS = _REPO / ".claude" / "settings.json"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gate = _load("reuse_gate", _SCRIPT)

_LANE = "lane-x-1-demo"
_CONTRACT = """\
# LANE lane-x-1-demo -- a demo

## Context

Mentions `scripts/context_only.py`, which is NOT in the Done-contract.

## Done-contract (immutable)

1. Build `scripts/named_tool.py` and its test.
2. Anything under `scripts/sub/` belongs to this lane.
3. The usage test tries to create an unnamed `scripts/x_probe.py` and is denied.

## Decision budget

Mentions `scripts/after_only.py`.
"""


@pytest.fixture
def mini(tmp_path):
    """A lane worktree `<tmp>/worktrees/lane-x-1-demo` carrying its frozen contract in-tree."""
    root = tmp_path / "worktrees" / _LANE
    contracts = root / "docs" / "audits" / "2026-01-01-technical-batch-x-launch-contracts"
    contracts.mkdir(parents=True)
    (contracts / "LANE-x-1-demo.md").write_text(_CONTRACT, encoding="utf-8")
    (root / "scripts" / "hooks").mkdir(parents=True)
    (root / "scripts" / "existing.py").write_text("x = 1\n", encoding="utf-8")
    (root / "scripts" / "hooks" / "neighbour.py").write_text("y = 1\n", encoding="utf-8")
    (root / ".claude" / "commands").mkdir(parents=True)
    (root / "docs" / "notes").mkdir(parents=True)
    env = {"HARNESS_RECEIPTS_DIR": str(tmp_path / "receipts")}
    return root, env


def _write(path: str, cwd: Path, field: str = "file_path", tool: str = "Write") -> dict:
    return {"hook_event_name": "PreToolUse", "session_id": "s-1", "cwd": str(cwd),
            "tool_name": tool, "tool_input": {field: path, "content": "z = 1\n"}}


# ============================================================== 1. DENY

def test_a_new_unnamed_file_under_scripts_is_denied(mini):
    root, env = mini
    decision, reason = gate.decide(_write("scripts/unnamed_new.py", root), root, env)
    assert decision == "block", reason


def test_a_new_unnamed_file_under_dot_claude_is_denied(mini):
    root, env = mini
    decision, _ = gate.decide(_write(".claude/commands/new-cmd.md", root), root, env)
    assert decision == "block"


def test_an_absolute_path_and_copilots_path_field_are_denied_too(mini):
    root, env = mini
    target = str(root / "scripts" / "hooks" / "fresh.py")
    assert gate.decide(_write(target, root), root, env)[0] == "block"
    # Copilot CLI 1.0.96 sends Write as tool_input.path (measured in-lane, 2026-10-13).
    assert gate.decide(_write(target, root, field="path"), root, env)[0] == "block"


def test_a_path_the_done_contract_calls_unnamed_is_not_named(mini):
    root, env = mini
    assert gate.decide(_write("scripts/x_probe.py", root), root, env)[0] == "block"


def test_a_path_named_only_outside_the_done_contract_is_not_named(mini):
    root, env = mini
    assert gate.decide(_write("scripts/context_only.py", root), root, env)[0] == "block"
    assert gate.decide(_write("scripts/after_only.py", root), root, env)[0] == "block"


def test_a_why_record_from_another_directory_or_lane_does_not_count(mini):
    root, env = mini
    gate.record_why(root, "docs/notes/a.md", "answered", env)               # wrong directory
    receipts = Path(env["HARNESS_RECEIPTS_DIR"])
    with (receipts / gate.WHY_RECORD_NAME).open("a", encoding="utf-8") as fh:  # wrong lane
        fh.write(json.dumps({"lane": "lane-other", "path": "scripts/existing.py"}) + "\n")
    assert gate.decide(_write("scripts/unnamed_new.py", root), root, env)[0] == "block"


# ============================================================== 2. ALLOW

def test_an_edit_to_an_existing_file_is_allowed(mini):
    root, env = mini
    assert gate.decide(_write("scripts/existing.py", root, tool="Edit"), root, env)[0] == "allow"
    assert gate.decide(_write("scripts/existing.py", root), root, env)[0] == "allow"


def test_a_new_file_the_done_contract_names_is_allowed(mini):
    root, env = mini
    assert gate.decide(_write("scripts/named_tool.py", root), root, env)[0] == "allow"


def test_a_new_file_in_a_directory_the_done_contract_names_is_allowed(mini):
    root, env = mini
    assert gate.decide(_write("scripts/sub/anything.py", root), root, env)[0] == "allow"


def test_a_new_file_after_a_recorded_why_for_a_neighbour_is_allowed(mini):
    root, env = mini
    assert gate.decide(_write("scripts/hooks/fresh.py", root), root, env)[0] == "block"
    assert gate.record_why(root, "scripts/hooks/neighbour.py", "answered", env) is not None
    assert gate.decide(_write("scripts/hooks/fresh.py", root), root, env)[0] == "allow"


def test_a_refused_why_still_records_the_search(mini):
    root, env = mini
    gate.record_why(root, "scripts/existing.py", "refused", env)
    assert gate.decide(_write("scripts/unnamed_new.py", root), root, env)[0] == "allow"


def test_any_path_outside_the_guarded_roots_is_allowed(mini, tmp_path):
    root, env = mini
    assert gate.decide(_write("docs/notes/new.md", root), root, env)[0] == "allow"
    assert gate.decide(_write("tests/test_new.py", root), root, env)[0] == "allow"
    outside = str(tmp_path / "elsewhere" / "scripts" / "x.py")
    assert gate.decide(_write(outside, root), root, env)[0] == "allow"


def test_a_tool_that_writes_nothing_is_allowed(mini):
    root, env = mini
    payload = {"tool_name": "Read", "cwd": str(root),
               "tool_input": {"file_path": "scripts/unnamed_new.py"}}
    assert gate.decide(payload, root, env)[0] == "allow"
    assert gate.decide({"tool_name": "Bash", "tool_input": {"command": "ls"}}, root, env)[0] == "allow"


def test_outside_a_lane_the_rule_allows_and_logs(tmp_path, caplog):
    root = tmp_path / "primary"                       # not under a `worktrees/` directory
    (root / "scripts").mkdir(parents=True)
    with caplog.at_level(logging.INFO, logger="reuse_gate"):
        decision, _ = gate.decide(_write("scripts/unnamed_new.py", root), root, {})
    assert decision == "allow"
    assert any("no active lane" in r.getMessage() for r in caplog.records), caplog.text


def test_a_lane_with_no_contract_on_disk_allows_and_logs(tmp_path, caplog):
    root = tmp_path / "worktrees" / "integrate-x"     # a worktree that is not a contracted lane
    (root / "scripts").mkdir(parents=True)
    with caplog.at_level(logging.INFO, logger="reuse_gate"):
        decision, _ = gate.decide(_write("scripts/unnamed_new.py", root), root, {})
    assert decision == "allow"
    assert any("no active lane contract" in r.getMessage() for r in caplog.records), caplog.text


def test_the_disable_switch_allows_and_logs(mini, caplog):
    root, env = mini
    env = {**env, gate.DISABLE_ENV: "1"}
    with caplog.at_level(logging.INFO, logger="reuse_gate"):
        assert gate.decide(_write("scripts/unnamed_new.py", root), root, env)[0] == "allow"
    assert gate.DISABLE_ENV in caplog.text


@pytest.mark.parametrize("payload", [None, [], {"tool_name": "Write"},
                                     {"tool_name": "Write", "tool_input": {"file_path": 7}}])
def test_a_malformed_payload_is_allowed(mini, payload):
    root, env = mini
    assert gate.decide(payload, root, env)[0] == "allow"


# ============================================================== 3. REMEDY

def test_the_deny_message_is_one_line_naming_the_remedy(mini):
    root, env = mini
    _, reason = gate.decide(_write("scripts/hooks/fresh.py", root), root, env)
    assert "\n" not in reason
    assert "/why scripts/hooks/neighbour.py" in reason
    assert "name the file in the contract" in reason
    assert "scripts/hooks/fresh.py" in reason


# ============================================================== the record's producer

def test_file_purpose_graph_why_writes_the_record(mini, monkeypatch):
    """`file_purpose_graph.py why` is the record's producer: running it in a lane leaves a record
    the gate then reads (answered or refused -- the search is what is recorded)."""
    root, env = mini
    import file_purpose_graph as fpg   # bare: `pythonpath` carries scripts/ (pyproject)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setenv("HARNESS_LANE", _LANE)
    fpg._main(["why", "scripts/hooks/neighbour.py", "--repo-root", str(root)])
    assert gate.decide(_write("scripts/hooks/fresh.py", root), root, env)[0] == "allow"


def test_outside_a_lane_record_why_writes_nothing(tmp_path):
    root = tmp_path / "primary"
    (root / "scripts").mkdir(parents=True)
    assert gate.record_why(root, "scripts/a.py", "answered", {}) is None
    assert not (root / "logs").exists()


# ============================================================== 4. WIRE

def test_main_prints_a_block_and_exits_2(mini, monkeypatch, capsys):
    root, env = mini
    monkeypatch.setattr(gate, "REPO_ROOT", root)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    monkeypatch.delenv("HARNESS_LANE", raising=False)
    monkeypatch.setattr("sys.stdin", _Stdin(json.dumps(_write("scripts/unnamed_new.py", root))))
    assert gate.main() == 2
    out = capsys.readouterr()
    assert json.loads(out.out.strip())["decision"] == "block"
    assert "/why" in out.err


class _Stdin:
    def __init__(self, text: str):
        self._text = text

    def read(self) -> str:
        return self._text


_LAUNCHER_REL = "scripts/hooks/hook_launcher.py"
_SHAPE = ('uv run --locked python ${CLAUDE_PROJECT_DIR:+"$CLAUDE_PROJECT_DIR/' + _LAUNCHER_REL
          + '"} $(git rev-parse --no-revs --no-flags -- ./$(git rev-parse --path-format=relative'
          ' --show-toplevel)' + _LAUNCHER_REL + ') -m os ')


def _reuse_gate_entries() -> list[tuple[str, dict]]:
    groups = json.loads(_SETTINGS.read_text(encoding="utf-8"))["hooks"]["PreToolUse"]
    return [(g["matcher"], h) for g in groups for h in g["hooks"]
            if "reuse_gate.py" in h.get("command", "")]


def test_registered_once_through_the_shared_launcher():
    entries = _reuse_gate_entries()
    assert len(entries) == 1, entries
    matcher, hook = entries[0]
    assert hook["command"] == _SHAPE + "scripts/hooks/reuse_gate.py"
    assert isinstance(hook.get("timeout"), int) and hook["timeout"] > 0
    for tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        assert tool in matcher.split("|")


# --- through each real shell, reusing the scope guard's harness -------------------------------

_shells = _load("scope_guard_hook_command", _REPO / "tests" / "test_scope_guard_hook_command.py")


def _shell_env(**extra) -> dict:
    drop = {"CLAUDE_PROJECT_DIR", "GIT_DIR", "GIT_WORK_TREE", "HARNESS_LANE",
            "HARNESS_RECEIPTS_DIR", "DEV_KNOWLEDGE_REUSE_GATE_DISABLE"}
    return {**{k: v for k, v in os.environ.items() if k not in drop}, **extra}


def _run_declared(shell: str, cwd: Path, payload: dict, env: dict) -> subprocess.CompletedProcess:
    argv = _shells._SHELLS[shell]()
    if argv is None:
        pytest.skip(f"{shell} is not runnable here")
    (_, hook), = _reuse_gate_entries()
    return subprocess.run([*argv, hook["command"]], cwd=cwd, env=env, input=json.dumps(payload),
                          capture_output=True, text=True, timeout=180)


@pytest.mark.parametrize("shell", sorted(_shells._SHELLS))
def test_in_a_lane_the_declared_command_denies_an_unnamed_new_file(shell, tmp_path):
    """This lane's own frozen contract is the fixture: `scripts/x_probe.py` is the file its
    Done-contract item 5 calls unnamed."""
    env = _shell_env(HARNESS_LANE="lane-bw-735-reuse-gate", HARNESS_RECEIPTS_DIR=str(tmp_path))
    payload = _write("scripts/x_probe.py", _REPO)
    proc = _run_declared(shell, _REPO, payload, env)
    assert proc.returncode != 0, (shell, proc.returncode, proc.stdout, proc.stderr)
    assert json.loads(proc.stdout.strip().splitlines()[-1])["decision"] == "block", proc.stdout


@pytest.mark.parametrize("shell", sorted(_shells._SHELLS))
def test_in_a_lane_the_declared_command_allows_an_existing_file(shell, tmp_path):
    env = _shell_env(HARNESS_LANE="lane-bw-735-reuse-gate", HARNESS_RECEIPTS_DIR=str(tmp_path))
    proc = _run_declared(shell, _REPO, _write("scripts/hooks/reuse_gate.py", _REPO), env)
    assert proc.returncode == 0, (shell, proc.returncode, proc.stdout, proc.stderr)


@pytest.mark.parametrize("shell", sorted(_shells._SHELLS))
def test_outside_a_git_tree_the_declared_command_exits_cleanly(shell, tmp_path):
    probe = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=tmp_path,
                           env=_shell_env(), capture_output=True, text=True)
    if probe.returncode == 0:
        pytest.skip(f"{tmp_path} is inside a git tree ({probe.stdout.strip()})")
    proc = _run_declared(shell, tmp_path, _write("scripts/x_probe.py", tmp_path), _shell_env())
    assert proc.returncode == 0, (shell, proc.returncode, proc.stdout, proc.stderr)
    assert "Traceback" not in proc.stderr, proc.stderr
