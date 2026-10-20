"""RED-first witnesses for the pre-launch wiring of the model-per-role gate.

The gate organ is declared in `ecosystem/harness.yaml`'s `pre-launch` moment, the Codespace launcher
runs the pre-launch BEFORE it touches `gh` (P1-B04), and `run_prelaunch` tells the organs which model
the launch actually uses.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

import dispatch as d

REPO = Path(__file__).resolve().parents[1]
SID = "11111111-2222-3333-4444-555555555555"

CONTRACT = """# LANE lane-subst -- a test contract

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Dispatch

```
claude --bg -n lane-subst --model sonnet --effort high --permission-mode bypassPermissions --worktree lane-subst "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-SUBST.md"
```

slug `lane-subst` -> branch `worktree-lane-subst`
"""


@pytest.fixture
def contract(tmp_path):
    path = tmp_path / "LANE-SUBST.md"
    path.write_text(CONTRACT, encoding="utf-8")
    return path


@pytest.fixture(autouse=True)
def receipts(tmp_path, monkeypatch):
    target = tmp_path / "receipts"
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(target))
    return target


# --- the declared organ -------------------------------------------------------------------------

def test_the_pre_launch_moment_declares_the_model_per_role_organ():
    doc = yaml.safe_load((REPO / "ecosystem" / "harness.yaml").read_text(encoding="utf-8"))
    moment = next(m for m in doc["moments"] if m["name"] == "pre-launch")
    organ = next((o for o in moment["organs"] if o["id"] == "model_per_role"), None)
    assert organ is not None, "pre-launch declares no model_per_role organ"
    command = " ".join(organ["command"]).replace("\\", "/")
    assert "scripts/subst_gate.py" in command and "contract" in organ["command"]
    assert organ["receipt"].startswith("MOMENT-PRE-LAUNCH-")


# --- P1-B04: the Codespace launcher runs pre-launch before gh -----------------------------------

def _invoke_codespace_exec(contract):
    return CliRunner().invoke(d.cli, [
        "codespace-exec", str(contract), "--repo", "me/repo", "--branch", "main", "--slug", "lane-subst",
        "--argv-json", '["claude","-p"]', "--batch", "E2.0"])


def test_codespace_exec_refused_by_pre_launch_never_calls_gh_or_codespace_exec(contract, monkeypatch):
    spawned = []
    monkeypatch.setattr(d, "run_prelaunch",
                        lambda *a, **k: d.PreLaunch(False, "REFUSED [model-per-role]: x"))

    def must_not_run(*a, **k):
        raise AssertionError("codespace_exec ran after a refused pre-launch")
    monkeypatch.setattr(d, "codespace_exec", must_not_run)
    for name in ("run", "Popen"):
        monkeypatch.setattr(subprocess, name, lambda *a, _n=name, **k: spawned.append((_n, a)))

    out = _invoke_codespace_exec(contract)

    assert out.exit_code == d.EXIT_REFUSED == 5, out.output
    def _program(call):
        argv = call[1][0] if call[1] else ""
        return Path(str(argv[0] if isinstance(argv, (list, tuple)) else argv).split()[0]).stem if argv else ""
    assert not [c for c in spawned if _program(c) == "gh"], "a gh call was made"
    assert "REFUSED [model-per-role]: x" in out.output


def test_codespace_exec_runs_pre_launch_first_then_codespace_exec_once(contract, monkeypatch):
    order = []
    monkeypatch.setattr(d, "run_prelaunch", lambda *a, **k: order.append("run_prelaunch") or d.PreLaunch(True))

    def fake_exec(*a, **k):
        order.append("codespace_exec")
        return d.ExecResult(ok=True, name="cs-1")
    monkeypatch.setattr(d, "codespace_exec", fake_exec)

    out = _invoke_codespace_exec(contract)

    assert out.exit_code == 0, out.output
    assert order == ["run_prelaunch", "codespace_exec"]


def test_codespace_exec_really_runs_the_pre_launch_moment_with_nothing_stubbed(contract, monkeypatch):
    """Repair 1 (item 5): `test_dispatch_codespace.py` stubs `run_prelaunch` for the whole file, so THIS is
    the witness that the verb runs the real moment -- the real `doit moment:pre-launch` refuses this
    launch (which organ speaks first depends on the box: no live integrator, or model-per-role on the
    head row `sonnet`), and `codespace_exec` is never reached."""
    def must_not_run(*a, **k):
        raise AssertionError("codespace_exec ran although the real pre-launch refused the contract")
    monkeypatch.setattr(d, "codespace_exec", must_not_run)

    out = _invoke_codespace_exec(contract)

    assert out.exit_code == d.EXIT_REFUSED == 5, out.output
    assert "pre-launch refused lane-subst: REFUSED [" in out.output, out.output


# --- launch_lane: the existing shape, shown beside the new refusal ------------------------------

class _FakeClaude:
    def __init__(self, jobs):
        self.calls, self.jobs = [], jobs

    def __call__(self, argv, env, cwd, log_path=None):
        self.calls.append(list(argv))
        name = argv[argv.index("-n") + 1]
        self.jobs.append({"id": "abcd1234", "sessionId": SID, "name": name,
                          "cwd": str(Path(cwd) / ".claude" / "worktrees" / name),
                          "state": "working", "status": "busy"})
        return d.Spawned(returncode=0, stdout="backgrounded abcd1234\n", pid=4321)


def _launch(contract, tmp_path, prelaunch):
    jobs = []
    spawn = _FakeClaude(jobs)
    request = d.request_from_contract(contract, batch="E2.0")
    result = d.launch_lane(request, prelaunch=prelaunch, spawn=spawn, agents=lambda: jobs, cwd=tmp_path)
    return result, spawn


def test_a_launch_whose_pre_launch_refuses_a_substituted_contract_spawns_nothing(contract, tmp_path):
    spawn = _FakeClaude([])
    with pytest.raises(d.LaunchRefused):
        d.launch_lane(d.request_from_contract(contract, batch="E2.0"),
                      prelaunch=lambda r: d.PreLaunch(False, "REFUSED [model-per-role]: substituted"),
                      spawn=spawn, agents=lambda: [], cwd=tmp_path)
    assert spawn.calls == []


def test_a_launch_whose_pre_launch_passes_spawns_once(contract, tmp_path):
    _result, spawn = _launch(contract, tmp_path, lambda r: d.PreLaunch(True))
    assert len(spawn.calls) == 1


# --- run_prelaunch hands the launch model to the organs -----------------------------------------

def test_run_prelaunch_passes_the_launch_model_to_the_organs(contract, monkeypatch):
    seen = {}

    def fake_run(argv, **kw):
        seen["env"] = kw.get("env") or {}
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")
    monkeypatch.setattr(d.subprocess, "run", fake_run)
    request = d.request_from_contract(contract, batch="E2.0")

    d.run_prelaunch(request)

    assert request.model
    assert seen["env"]["HARNESS_MODEL"] == request.model


# --- review-fix witnesses: the launch model is read from every spelling of the flag -----------------

@pytest.mark.parametrize("argv,expected", [
    (["claude", "--model", "grok-4.7"], "grok-4.7"),
    (["claude", "--model=grok-4.7"], "grok-4.7"),
    (["codex", "exec", "-m", "gpt-5.6-terra"], "gpt-5.6-terra"),
    (["claude", "-p"], ""),
])
def test_the_planned_launch_model_is_read_from_every_spelling(argv, expected):
    assert d.planned_model(argv) == expected


def test_codespace_exec_hands_pre_launch_the_equals_form_model(contract, monkeypatch):
    seen = []
    monkeypatch.setattr(d, "run_prelaunch", lambda request, *a, **k: seen.append(request.model) or d.PreLaunch(True))
    monkeypatch.setattr(d, "codespace_exec", lambda *a, **k: d.ExecResult(ok=True, name="cs-1"))
    out = CliRunner().invoke(d.cli, [
        "codespace-exec", str(contract), "--repo", "me/repo", "--branch", "main", "--slug", "lane-subst",
        "--argv-json", '["claude","--model=grok-4.7"]', "--batch", "E2.0"])
    assert out.exit_code == 0, out.output
    assert seen == ["grok-4.7"]


# --- E2-SG-2: one strict batch grammar `E<n>.<n>` enforced at the CLI ----------------------------

def _no_spawn(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("spawned / ran a subprocess before the batch grammar refusal")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)


@pytest.mark.parametrize("batch", ["E2.0junk", "B1", "E2.0 "])
def test_e2sg2_launch_refuses_a_malformed_batch_before_the_contract(batch, tmp_path, monkeypatch):
    monkeypatch.delenv("HARNESS_BATCH", raising=False)
    _no_spawn(monkeypatch)
    out = CliRunner().invoke(d.cli, ["launch", str(tmp_path / "NOPE.md"), "--batch", batch])
    assert out.exit_code == 5, out.output
    assert "REFUSED [batch-grammar]" in out.output


def test_e2sg2_launch_accepts_a_well_formed_batch_grammar(tmp_path, monkeypatch):
    monkeypatch.delenv("HARNESS_BATCH", raising=False)
    out = CliRunner().invoke(d.cli, ["launch", str(tmp_path / "NOPE.md"), "--batch", "E2.0"])
    assert "batch-grammar" not in out.output


def test_e2sg2_launch_with_no_batch_is_not_a_grammar_refusal(tmp_path, monkeypatch):
    monkeypatch.delenv("HARNESS_BATCH", raising=False)
    out = CliRunner().invoke(d.cli, ["launch", str(tmp_path / "NOPE.md")])
    assert "batch-grammar" not in out.output


def test_e2sg2_launch_refuses_a_malformed_env_batch(tmp_path, monkeypatch):
    monkeypatch.setenv("HARNESS_BATCH", "junk")
    _no_spawn(monkeypatch)
    out = CliRunner().invoke(d.cli, ["launch", str(tmp_path / "NOPE.md")])
    assert out.exit_code == 5, out.output
    assert "REFUSED [batch-grammar]" in out.output


@pytest.mark.parametrize("batch", ["B1", "E2.0junk"])
def test_e2sg2_codespace_exec_refuses_a_malformed_batch_and_runs_nothing(batch, contract, monkeypatch):
    def must_not_run(*a, **k):
        raise AssertionError("ran after a batch-grammar refusal")
    monkeypatch.setattr(d, "run_prelaunch", must_not_run)
    monkeypatch.setattr(d, "codespace_exec", must_not_run)
    _no_spawn(monkeypatch)
    out = CliRunner().invoke(d.cli, [
        "codespace-exec", str(contract), "--repo", "me/repo", "--branch", "main", "--slug", "lane-subst",
        "--argv-json", '["claude","-p"]', "--batch", batch])
    assert out.exit_code == 5, out.output
    assert "REFUSED [batch-grammar]" in out.output


def test_e2sg2_codespace_exec_good_batch_still_reaches_run_prelaunch(contract, monkeypatch):
    reached = []
    monkeypatch.setattr(d, "run_prelaunch", lambda *a, **k: reached.append(1) or d.PreLaunch(False, "x"))
    out = _invoke_codespace_exec(contract)
    assert reached == [1], out.output
    assert "batch-grammar" not in out.output
