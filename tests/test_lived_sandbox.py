"""Layer-1 (hermetic, offline) tests for the lived-workflow sandbox SPAWN + isolation scaffold
(Slice A). The live isolated `claude -p` proof is skipif-guarded (deliberate, never in offline
CI); everything else — the isolation verdict logic, config writing, stream parsing, the teardown
blast-radius guard, api-key loading, and the frozen isolation fixtures — is deterministic. The
observer + engages-spec oracle live in Slice B (not here)."""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "deploy"))
import floor_conformance as fc  # noqa: E402
from lived_sandbox import isolation as iso  # noqa: E402
from lived_sandbox import spawn as sp  # noqa: E402

_FIXTURES = _REPO / "tests" / "fixtures" / "lived-workflow"
_SECRET_RE = re.compile(r"sk-ant-[A-Za-z0-9_-]{8}")


# --- isolation verdict logic (the correctness property, encoded) ---

def _result(a: bool, b: bool, exitA: int = 0, exitB: int = 0) -> iso.IsolationResult:
    return iso.IsolationResult(marker="M", present_in_configA=a, absent_in_configB=b,
                               exitA=exitA, exitB=exitB, transcriptA=None, transcriptB=None,
                               tempdir=Path("."))


def test_isolation_passes_only_when_both_legs_hold():
    assert _result(True, True).passed
    assert not _result(True, False).passed   # sentinel leaked into configB -> NOT isolated
    assert not _result(False, True).passed   # positive control dead -> proof is untrustworthy
    assert not _result(False, False).passed


def test_isolation_requires_successful_child_exits():
    """Codex CRITICAL 2026-07-04: a FAILED child whose SessionStart hook fired before the failure
    must NOT count as a proof (false-green = measuring a facade)."""
    assert _result(True, True, exitA=0, exitB=0).passed
    assert not _result(True, True, exitA=1, exitB=0).passed   # configA run failed
    assert not _result(True, True, exitA=0, exitB=1).passed   # configB run failed


def test_isolation_summary_names_the_verdict():
    assert "PROVEN" in _result(True, True).summary()
    assert "FAILED" in _result(True, False).summary()
    assert "FAILED" in _result(True, True, exitA=1).summary()


# --- isolated-config writing ---

def test_write_isolated_config_empty_hooks(tmp_path):
    cfg = sp.write_isolated_config(tmp_path / "cfg")
    assert json.loads((cfg / "settings.json").read_text(encoding="utf-8")) == {"hooks": {}}


def test_write_isolated_config_sentinel_hook(tmp_path):
    cfg = sp.write_isolated_config(tmp_path / "cfg", session_start_marker="MARK123")
    data = json.loads((cfg / "settings.json").read_text(encoding="utf-8"))
    cmd = data["hooks"]["SessionStart"][0]["hooks"][0]["command"]
    assert "MARK123" in cmd and cmd.startswith("python -c")


def test_hook_print_rejects_unsafe_marker():
    with pytest.raises(sp.SandboxError):
        sp._hook_print("bad; rm -rf /")


# --- stream-json parsing (best-effort, skips non-JSON lines) ---

def test_parse_stream_skips_nonjson():
    assert sp._parse_stream('{"a":1}\nnot json\n{"b":2}\n') == [{"a": 1}, {"b": 2}]


# --- api-key loading (change #4: env, then DEV_SECRETS_ENV; never a hardcoded path) ---

def test_load_api_key_from_env(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "FAKEKEY_ENV")
    assert sp.load_api_key() == "FAKEKEY_ENV"


def test_load_api_key_from_secrets_file(monkeypatch, tmp_path):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    env = tmp_path / ".env"
    env.write_text('export ANTHROPIC_API_KEY="FAKEKEY_FILE"\n', encoding="utf-8")
    monkeypatch.setenv("DEV_SECRETS_ENV", str(env))
    assert sp.load_api_key() == "FAKEKEY_FILE"


def test_load_api_key_missing_raises(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("DEV_SECRETS_ENV", raising=False)
    with pytest.raises(sp.SandboxError):
        sp.load_api_key()


# --- teardown blast-radius guard (reuses floor_conformance._rmtree_guarded — "no leftovers") ---

def test_teardown_refuses_outside_temp_root(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    with pytest.raises(fc.ConformanceError):
        fc._rmtree_guarded(outside, tmp_path / "some-other-root")
    assert outside.exists()  # guard raised BEFORE deleting


def test_teardown_deletes_the_root(tmp_path):
    root = tmp_path / "root"
    (root / "sub").mkdir(parents=True)
    (root / "sub" / "f.txt").write_text("x", encoding="utf-8")
    sp.teardown(root)
    assert not root.exists()


def test_teardown_refuses_outside_system_temp(monkeypatch, tmp_path):
    """Codex CRITICAL 2026-07-04: teardown must REFUSE a path outside the system temp dir (the
    guard's trusted parent is the system temp root, not the vacuous temp_root.parent)."""
    fake_temp = tmp_path / "systemp"
    fake_temp.mkdir()
    monkeypatch.setattr(sp.tempfile, "gettempdir", lambda: str(fake_temp))
    inside = fake_temp / "lived-sandbox-x"
    inside.mkdir()
    outside = tmp_path / "precious"
    outside.mkdir()
    with pytest.raises(sp.SandboxError):
        sp.teardown(outside)
    assert outside.exists()          # refused BEFORE deleting
    sp.teardown(inside)              # under (faked) system temp -> deleted
    assert not inside.exists()


def test_child_env_extra_env_cannot_override_protected(tmp_path):
    """Codex HIGH 2026-07-04: extra_env may add safe keys but must NOT override the
    isolation-critical CLAUDE_CONFIG_DIR / ANTHROPIC_API_KEY / CLAUDE_PROJECT_DIR."""
    env = sp._child_env(tmp_path / "cfg", "REALKEY", {
        "CLAUDE_CONFIG_DIR": "/evil", "CLAUDE_PROJECT_DIR": "/outer",
        "ANTHROPIC_API_KEY": "WRONGKEY", "PRE_COMMIT_HOME": "/pc"})
    assert env["CLAUDE_CONFIG_DIR"] == str(tmp_path / "cfg")   # not /evil
    assert env["ANTHROPIC_API_KEY"] == "REALKEY"              # not WRONGKEY
    assert "CLAUDE_PROJECT_DIR" not in env                    # dropped, not reintroduced
    assert env["PRE_COMMIT_HOME"] == "/pc"                    # safe addition allowed


def test_spawn_wraps_missing_claude(monkeypatch, tmp_path):
    """Codex HIGH 2026-07-04: a missing `claude` / launch failure surfaces as SandboxError, not a
    raw traceback (the CLI is the operator stop point)."""
    def boom(*_a, **_k):
        raise FileNotFoundError("no claude on PATH")
    monkeypatch.setattr(sp.subprocess, "run", boom)
    with pytest.raises(sp.SandboxError):
        sp.spawn(tmp_path / "work", "hi", config_dir=tmp_path / "cfg", api_key="K")


# --- the FROZEN isolation fixtures are real evidence (marker in A, not B; and no secret) ---

@pytest.mark.skipif(not (_FIXTURES / "isolation-configA-sentinel.jsonl").exists(),
                    reason="isolation fixtures not captured (run cli prove-isolation --freeze)")
def test_frozen_fixtures_carry_the_isolation_evidence():
    a = (_FIXTURES / "isolation-configA-sentinel.jsonl").read_text(encoding="utf-8")
    b = (_FIXTURES / "isolation-configB-isolated.jsonl").read_text(encoding="utf-8")
    assert "LSANDBOX_SENTINEL" in a          # positive control fired
    assert "LSANDBOX_SENTINEL" not in b      # isolation held
    assert not _SECRET_RE.search(a)          # no key was ever frozen
    assert not _SECRET_RE.search(b)


# --- live isolated spawn (skipif: needs `claude` + a key + explicit opt-in; never offline CI) ---

@pytest.mark.skipif(shutil.which("claude") is None or not os.environ.get("LIVED_SANDBOX_LIVE"),
                    reason="live spawn: set LIVED_SANDBOX_LIVE=1, have `claude` on PATH + a key")
def test_live_isolation_proof_holds():
    result = iso.prove_isolation(model="haiku")
    assert result.passed, result.summary()
