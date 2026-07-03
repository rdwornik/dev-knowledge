"""Tests for deploy/carrier_mesh.py — the enforcement-mesh carrier (Axis-1 transfer, #236).

Mirrors tests/test_deploy_floor.py: an oracle computed independently of the carrier (the hub
bytes), a tmp_path consumer, and absent->apply->verify / idempotent / drifted / verify-failures /
D9-independence coverage, plus the two merge-preservation cases (Stop hook added beside an
existing SessionStart; the override-token .gitignore block added beside an existing .claude/* block).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import carrier_mesh as cm  # noqa: E402
import contract  # noqa: E402

# Oracle: the hub bytes the carrier deploys, read straight from the hub (not via the carrier).
_SEB = cm._hub_bytes(cm._HUB_SEB)
_GATE = cm._hub_bytes(cm._HUB_FRESHNESS_GATE)
_OVERRIDE = cm._hub_bytes(cm._HUB_OVERRIDE_CMD)


def _carrier(repo: Path) -> cm.MeshCarrier:
    return cm.MeshCarrier(repo)


def _read(repo: Path, rel: str) -> str:
    return cm._read_text(repo / rel)


# --- absent -> apply -> verify ------------------------------------------------

def test_absent_detects_then_applies_and_verifies(tmp_path):
    car = _carrier(tmp_path)
    assert car.detect(None) is contract.CarrierState.ABSENT

    result = car.apply(None)
    assert result.changed is True
    # seb + freshness gate + override.md + Stop hook + .gitignore block (logs/ is runtime-created).
    assert len(result.changes) == 5

    assert _read(tmp_path, cm.SEB_REL) == _SEB
    assert _read(tmp_path, cm.FRESHNESS_GATE_REL) == _GATE
    assert _read(tmp_path, cm.OVERRIDE_CMD_REL) == _OVERRIDE
    assert car.detect(None) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(None).ok is True


def test_stop_hook_and_gitignore_shape(tmp_path):
    _carrier(tmp_path).apply(None)
    settings = json.loads((tmp_path / cm.SETTINGS_REL).read_text(encoding="utf-8"))
    stop_cmds = [h["command"]
                 for g in settings["hooks"]["Stop"] for h in g["hooks"]]
    assert any("session_end_backpressure" in c for c in stop_cmds)
    gi = [ln.strip() for ln in _read(tmp_path, cm.GITIGNORE_REL).splitlines()]
    assert "logs/.session-override-token" in gi and "logs/OVERRIDES.md" in gi  # ephemeral ignored
    assert "!.claude/commands/override.md" in gi and "!.claude/commands/" in gi  # re-include negations


# --- idempotent ---------------------------------------------------------------

def test_apply_is_idempotent(tmp_path):
    car = _carrier(tmp_path)
    car.apply(None)
    seb_before = (tmp_path / cm.SEB_REL).read_bytes()
    settings_before = (tmp_path / cm.SETTINGS_REL).read_bytes()

    second = car.apply(None)
    assert second.changed is False
    assert second.changes == ()
    assert (tmp_path / cm.SEB_REL).read_bytes() == seb_before
    assert (tmp_path / cm.SETTINGS_REL).read_bytes() == settings_before


# --- drifted -> reconcile -----------------------------------------------------

def test_drifted_script_edited_detects_then_reconciles(tmp_path):
    car = _carrier(tmp_path)
    car.apply(None)
    (tmp_path / cm.SEB_REL).write_text(_SEB + "\n# TAMPER\n", encoding="utf-8", newline="\n")
    assert car.detect(None) is contract.CarrierState.PRESENT_DRIFTED

    result = car.apply(None)
    assert result.changed is True
    assert car.detect(None) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(None).ok is True


def test_drifted_when_stop_hook_missing(tmp_path):
    """Scripts present but no Stop hook wired -> DRIFTED (present but not enforcing)."""
    car = _carrier(tmp_path)
    car.apply(None)
    (tmp_path / cm.SETTINGS_REL).write_text('{"hooks": {}}\n', encoding="utf-8")
    assert car.detect(None) is contract.CarrierState.PRESENT_DRIFTED


# --- verify reports failures (not a silent pass) ------------------------------

def test_verify_on_absent_is_not_ok(tmp_path):
    result = _carrier(tmp_path).verify(None)
    assert result.ok is False
    assert any("missing" in f for f in result.failures)
    assert any("Stop hook" in f for f in result.failures)


# --- merge preservation: existing SessionStart + existing .gitignore block ----

def test_stop_hook_preserves_existing_sessionstart(tmp_path):
    """Deploying beside a floor SessionStart hook adds Stop, preserves SessionStart."""
    (tmp_path / ".claude").mkdir()
    (tmp_path / cm.SETTINGS_REL).write_text(json.dumps({
        "hooks": {"SessionStart": [{"matcher": "",
                  "hooks": [{"type": "command", "command": "python .claude/check_floor_hash.py"}]}]}
    }, indent=2), encoding="utf-8")
    _carrier(tmp_path).apply(None)
    data = json.loads((tmp_path / cm.SETTINGS_REL).read_text(encoding="utf-8"))
    ss = [h["command"] for g in data["hooks"]["SessionStart"] for h in g["hooks"]]
    st = [h["command"] for g in data["hooks"]["Stop"] for h in g["hooks"]]
    assert any("check_floor_hash" in c for c in ss)         # preserved
    assert any("session_end_backpressure" in c for c in st)  # added


def test_gitignore_preserves_existing_floor_block(tmp_path):
    (tmp_path / cm.GITIGNORE_REL).write_text(".claude/*\n!.claude/CLAUDE-FLOOR.md\n", encoding="utf-8")
    _carrier(tmp_path).apply(None)
    gi = [ln.strip() for ln in _read(tmp_path, cm.GITIGNORE_REL).splitlines()]
    assert ".claude/*" in gi                                  # floor block preserved
    assert "!.claude/CLAUDE-FLOOR.md" in gi
    assert "logs/.session-override-token" in gi               # mesh block added


# --- D9: detect and verify are independent -----------------------------------

def test_verify_does_not_route_through_detect(tmp_path, monkeypatch):
    car = _carrier(tmp_path)
    car.apply(None)

    def _boom(*_a, **_k):
        raise AssertionError("verify must not call detect's _classify_mesh (D9)")

    monkeypatch.setattr(cm, "_classify_mesh", _boom)
    assert car.verify(None).ok is True


def test_detect_does_not_route_through_verify(tmp_path, monkeypatch):
    car = _carrier(tmp_path)
    car.apply(None)

    def _boom(*_a, **_k):
        raise AssertionError("detect must not call verify's _verify_mesh (D9)")

    monkeypatch.setattr(cm, "_verify_mesh", _boom)
    assert car.detect(None) is contract.CarrierState.PRESENT_CORRECT


# --- registered in the deploy tool factory -----------------------------------

def test_registered_in_make_carriers(tmp_path):
    import tool  # noqa: E402
    carriers = tool.make_carriers(tmp_path)
    assert cm.MeshCarrier.carrier_id in carriers
    assert isinstance(carriers[cm.MeshCarrier.carrier_id], cm.MeshCarrier)


# --- REGRESSION: override.md committable under the floor .claude/* + a logs/ ignore ----

def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def test_override_md_committable_under_floor_and_logs_ignore(tmp_path):
    """Deploy defect found 2026-07-03: the floor carrier's `.claude/*` block silently swallows
    .claude/commands/override.md (and a consumer's `logs/` dir-form ignore swallows anything under
    logs/), so `git add -A` skips override.md -> no committed /override -> the fire's committed-state
    clone reports a false `absent` and hub-parity breaks. The mesh gitignore block must RE-INCLUDE
    override.md. Reproduces ai-council's exact ignore shape."""
    repo = tmp_path / "consumer"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / ".gitignore").write_text(
        ".claude/*\n!.claude/CLAUDE-FLOOR.md\n!.claude/CLAUDE-FLOOR.md.sha256\nlogs/\n",
        encoding="utf-8")
    car = cm.MeshCarrier(repo)
    car.apply(None)
    # present AND committable (not gitignored) AND actually staged by add -A.
    assert (repo / cm.OVERRIDE_CMD_REL).exists()
    assert not cm._is_gitignored(repo, cm.OVERRIDE_CMD_REL), "override.md must re-include past .claude/*"
    _git(repo, "add", "-A")
    staged = _git(repo, "diff", "--cached", "--name-only").stdout.splitlines()
    assert cm.OVERRIDE_CMD_REL in staged, f"override.md not staged; staged={staged}"
    # verify() independently catches committability (fails if the negation were missing).
    assert car.verify(None).ok is True
    # the ephemeral override token stays ignored.
    assert cm._is_gitignored(repo, "logs/.session-override-token")
