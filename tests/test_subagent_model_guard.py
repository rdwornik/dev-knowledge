"""RED witnesses: the Agent-tool PreToolUse guard `scripts/hooks/subagent_model_guard.py`.

Subagents may only run the registry's read model (haiku) or the seat-orchestrator Sonnet for
bounded probes; Opus and an unset model are refused.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

_ROOT = Path(__file__).resolve().parents[1]
_GUARD = _ROOT / "scripts" / "hooks" / "subagent_model_guard.py"
_REGISTRY = _ROOT / "ecosystem" / "provider-registry.yaml"


def _load():
    assert _GUARD.is_file(), "scripts/hooks/subagent_model_guard.py does not exist"
    spec = importlib.util.spec_from_file_location("subagent_model_guard", _GUARD)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(_ROOT / "scripts"))
    spec.loader.exec_module(mod)
    return mod


def _registry() -> dict:
    return yaml.safe_load(_REGISTRY.read_text(encoding="utf-8"))


def _ids() -> tuple[str, str]:
    roles = _registry()["roles"]
    haiku = next(e["model"] for e in roles["read"]["order"] if e["provider"] == "anthropic")
    sonnet = roles["seat-orchestrator"]["order"][0]["model"]
    return haiku, sonnet


def _tool_input(model=None) -> dict:
    ti = {"prompt": "p", "description": "d", "subagent_type": "general-purpose"}
    if model is not None:
        ti["model"] = model
    return ti


def test_allowed_models_come_from_the_registry():
    mod = _load()
    haiku, sonnet = _ids()
    allowed = set(mod.allowed_models())
    assert {haiku, sonnet} <= allowed
    assert allowed - {haiku, sonnet} <= {"haiku", "sonnet"}


@pytest.mark.parametrize("model,verdict", [
    (None, "deny"), ("", "deny"), ("opus", "deny"), ("claude-opus-5-5", "deny"), ("Opus", "deny"),
    ("haiku", "allow"), ("sonnet", "allow"), ("gpt-5", "deny"),
])
def test_decision_table(model, verdict):
    mod = _load()
    got, reason = mod.decide(_tool_input(model), mod.allowed_models())
    assert got == verdict, reason
    if verdict == "deny":
        assert "ecosystem/provider-registry.yaml" in reason
        assert "haiku" in reason and "sonnet" in reason


def test_the_two_exact_registry_ids_are_allowed():
    mod = _load()
    for model in _ids():
        assert mod.decide(_tool_input(model), mod.allowed_models())[0] == "allow", model


def _run(payload: str):
    return subprocess.run([sys.executable, str(_GUARD)], input=payload, capture_output=True,
                          text=True, cwd=str(_ROOT))


def test_main_denies_an_agent_call_with_no_model():
    assert _GUARD.is_file(), "guard script missing"
    proc = _run(json.dumps({"tool_name": "Agent", "tool_input": _tool_input()}))
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)["hookSpecificOutput"]
    assert out["hookEventName"] == "PreToolUse" and out["permissionDecision"] == "deny"
    assert "provider-registry" in out["permissionDecisionReason"]


def test_main_allows_haiku_silently():
    assert _GUARD.is_file(), "guard script missing"
    proc = _run(json.dumps({"tool_name": "Agent", "tool_input": _tool_input("haiku")}))
    assert proc.returncode == 0 and proc.stdout.strip() == ""


def test_main_ignores_other_tools():
    assert _GUARD.is_file(), "guard script missing"
    proc = _run(json.dumps({"tool_name": "Bash", "tool_input": {"command": "ls"}}))
    assert proc.returncode == 0 and proc.stdout.strip() == ""


def test_main_fails_closed_on_unparseable_stdin():
    assert _GUARD.is_file(), "guard script missing"
    proc = _run("not json")
    assert proc.returncode == 0
    assert json.loads(proc.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_settings_wire_the_guard_and_default_subagents_to_haiku():
    settings = json.loads((_ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    entries = [e for e in settings["hooks"]["PreToolUse"]
               if "Agent" in e.get("matcher", "").split("|")
               and any("subagent_model_guard.py" in h.get("command", "") for h in e.get("hooks", []))]
    assert entries, "no PreToolUse entry with matcher `Agent` running subagent_model_guard.py"
    assert settings.get("env", {}).get("CLAUDE_CODE_SUBAGENT_MODEL") == "haiku"


def test_settings_matcher_covers_both_agent_and_task():
    settings = json.loads((_ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    entries = [e for e in settings["hooks"]["PreToolUse"]
               if any("subagent_model_guard.py" in h.get("command", "") for h in e.get("hooks", []))]
    assert entries
    for e in entries:
        assert {"Agent", "Task"} <= set(e["matcher"].split("|")), e["matcher"]


def test_opus_is_denied_even_if_the_allowed_list_contains_it():
    mod = _load()
    got, _ = mod.decide(_tool_input("claude-opus-5-5"), ["claude-opus-5-5", "haiku", "sonnet"])
    assert got == "deny"


@pytest.mark.parametrize("model,verdict", [
    (" haiku ", "allow"), ("\tsonnet\n", "allow"), (" opus ", "deny"),
    (5, "deny"), (["opus"], "deny"), (["haiku"], "deny"), ({"m": "haiku"}, "deny"), (True, "deny"),
    ("inherit", "deny"), ("opusplan", "deny"), ("sonnet[1m]", "deny"),
])
def test_decision_table_hardening(model, verdict):
    mod = _load()
    got, reason = mod.decide({"prompt": "p", "model": model}, mod.allowed_models())
    assert got == verdict, reason


def test_main_denies_a_task_call_with_no_model():
    proc = _run(json.dumps({"tool_name": "Task", "tool_input": _tool_input()}))
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"


def _broken_import_copy(tmp_path: Path) -> Path:
    # provider_registry is absent next to this copy, so `import provider_registry` fails
    hooks = tmp_path / "hooks"
    hooks.mkdir()
    copy = hooks / "subagent_model_guard.py"
    copy.write_text(_GUARD.read_text(encoding="utf-8"), encoding="utf-8")
    return copy


def _run_copy(copy: Path, payload: dict, cwd: Path):
    env = {k: v for k, v in __import__("os").environ.items() if k != "PYTHONPATH"}
    return subprocess.run([sys.executable, str(copy)], input=json.dumps(payload), capture_output=True,
                          text=True, cwd=str(cwd), env=env)


@pytest.mark.parametrize("tool", ["Agent", "Task"])
def test_main_fails_closed_when_the_registry_module_cannot_be_imported(tmp_path, tool):
    copy = _broken_import_copy(tmp_path)
    proc = _run_copy(copy, {"tool_name": tool, "tool_input": _tool_input("haiku")}, tmp_path)
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)["hookSpecificOutput"]
    assert out["permissionDecision"] == "deny"
    assert "provider_registry" in out["permissionDecisionReason"]


def test_a_broken_registry_import_stays_silent_for_other_tools(tmp_path):
    copy = _broken_import_copy(tmp_path)
    proc = _run_copy(copy, {"tool_name": "Bash", "tool_input": {"command": "ls"}}, tmp_path)
    assert proc.returncode == 0 and proc.stdout.strip() == "", proc.stderr
