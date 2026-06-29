"""Tests for the deploy-runbook pre-commit reference carrier (ADR-92 C1).

Covers the four-state reconcile model on the pre-commit carrier
(deploy/carrier_precommit.py) against the ADR-92 contract (deploy/contract.py):

- clean repo: target absent -> apply -> verify passes;
- drifted repo: required hook missing -> PRESENT_DRIFTED -> apply -> verify;
- wrong-version repo: present + complete but wrong rev -> PRESENT_WRONG_VERSION;
- apply-twice idempotency: apply then apply again writes nothing;
- detect/verify INDEPENDENCE (D9): each survives the other's judgment helper
  being sabotaged, proving they share no correctness-judgment code path;
- the shipped v1.0.0 manifest parses and declares the full carrier set.

Fixtures are temp repo dirs with crafted .pre-commit-config.yaml — no network,
no real consumer repos.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import carrier_precommit as cp  # noqa: E402
import contract  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parent.parent
_MANIFEST = _REPO_ROOT / "deploy" / "manifest-v1.0.0.yaml"

# The real shipped pre-commit target (so tests track the live ruff pin).
_PC_TARGET = next(
    c for c in yaml.safe_load(_MANIFEST.read_text(encoding="utf-8"))["carriers"]
    if c["id"] == "precommit"
)["target"]
_RUFF_REPO = "https://github.com/astral-sh/ruff-pre-commit"
_RUFF_REV = "v0.15.5"


def _write_config(repo: Path, data: dict) -> Path:
    path = repo / ".pre-commit-config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8", newline="\n")
    return path


def _carrier(repo: Path) -> cp.PrecommitCarrier:
    return cp.PrecommitCarrier(repo)


# ---------------------------------------------------------------------------
# clean repo — target absent -> apply -> verify passes
# ---------------------------------------------------------------------------


def test_clean_repo_detects_absent_then_applies_and_verifies(tmp_path):
    car = _carrier(tmp_path)
    assert not (tmp_path / ".pre-commit-config.yaml").exists()
    assert car.detect(_PC_TARGET) is contract.CarrierState.ABSENT

    result = car.apply(_PC_TARGET)
    assert result.changed is True
    assert result.changes  # enumerated what it wrote (structured output)

    assert car.detect(_PC_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_PC_TARGET).ok is True


def test_apply_creates_file_with_ruff_gate(tmp_path):
    _carrier(tmp_path).apply(_PC_TARGET)
    data = yaml.safe_load((tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    ruff = next(r for r in data["repos"] if r["repo"] == _RUFF_REPO)
    assert ruff["rev"] == _RUFF_REV
    assert any(h["id"] == "ruff" for h in ruff["hooks"])


def test_apply_preserves_existing_unrelated_repos(tmp_path):
    _write_config(tmp_path, {"repos": [{"repo": "local", "hooks": [{"id": "my-hook"}]}]})
    _carrier(tmp_path).apply(_PC_TARGET)
    data = yaml.safe_load((tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    repos = {r["repo"] for r in data["repos"]}
    assert "local" in repos and _RUFF_REPO in repos  # both present — merge, not overwrite


# ---------------------------------------------------------------------------
# drifted repo — required hook missing -> PRESENT_DRIFTED
# ---------------------------------------------------------------------------


def test_drifted_missing_hook_detects_drifted_then_reconciles(tmp_path):
    # ruff repo present at correct rev but the `ruff` hook is absent (drift).
    _write_config(
        tmp_path,
        {"repos": [{"repo": _RUFF_REPO, "rev": _RUFF_REV, "hooks": [{"id": "ruff-format"}]}]},
    )
    car = _carrier(tmp_path)
    assert car.detect(_PC_TARGET) is contract.CarrierState.PRESENT_DRIFTED

    result = car.apply(_PC_TARGET)
    assert result.changed is True
    assert car.verify(_PC_TARGET).ok is True
    # the consumer's own hook is preserved alongside the reconciled ruff hook.
    data = yaml.safe_load((tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    ruff = next(r for r in data["repos"] if r["repo"] == _RUFF_REPO)
    ids = {h["id"] for h in ruff["hooks"]}
    assert {"ruff", "ruff-format"} <= ids


# ---------------------------------------------------------------------------
# wrong-version repo — present + complete but wrong rev -> PRESENT_WRONG_VERSION
# ---------------------------------------------------------------------------


def test_wrong_version_detects_then_repins(tmp_path):
    _write_config(
        tmp_path,
        {"repos": [{"repo": _RUFF_REPO, "rev": "v0.14.0", "hooks": [{"id": "ruff"}]}]},
    )
    car = _carrier(tmp_path)
    assert car.detect(_PC_TARGET) is contract.CarrierState.PRESENT_WRONG_VERSION

    car.apply(_PC_TARGET)
    assert car.detect(_PC_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_PC_TARGET).ok is True
    data = yaml.safe_load((tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    ruff = next(r for r in data["repos"] if r["repo"] == _RUFF_REPO)
    assert ruff["rev"] == _RUFF_REV


# ---------------------------------------------------------------------------
# idempotency — apply twice writes nothing the second time
# ---------------------------------------------------------------------------


def test_apply_is_idempotent(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_PC_TARGET)
    before = (tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8")

    second = car.apply(_PC_TARGET)
    after = (tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    assert second.changed is False
    assert second.changes == ()
    assert before == after  # byte-identical: no spurious rewrite


# ---------------------------------------------------------------------------
# D9 — verify is independent of detect (no shared correctness-judgment path)
# ---------------------------------------------------------------------------


def test_verify_does_not_route_through_detect_classifier(tmp_path, monkeypatch):
    """Sabotage detect's judgment (_classify); verify must still pass on a good tree."""
    car = _carrier(tmp_path)
    car.apply(_PC_TARGET)

    def _boom(*_a, **_k):
        raise AssertionError("verify must not call detect's _classify (D9)")

    monkeypatch.setattr(cp, "_classify", _boom)
    monkeypatch.setattr(cp, "_find_repo", _boom)
    assert car.verify(_PC_TARGET).ok is True  # independent path — unaffected


def test_detect_does_not_route_through_verify_judge(tmp_path, monkeypatch):
    """Sabotage verify's judgment (_verify_satisfied); detect must still classify."""
    car = _carrier(tmp_path)
    car.apply(_PC_TARGET)

    def _boom(*_a, **_k):
        raise AssertionError("detect must not call verify's _verify_satisfied (D9)")

    monkeypatch.setattr(cp, "_verify_satisfied", _boom)
    assert car.detect(_PC_TARGET) is contract.CarrierState.PRESENT_CORRECT


def test_verify_reports_failures_when_target_unmet(tmp_path):
    # An empty config: verify must report the missing pin (not silently pass).
    _write_config(tmp_path, {"repos": []})
    result = _carrier(tmp_path).verify(_PC_TARGET)
    assert result.ok is False
    assert any(_RUFF_REPO in f for f in result.failures)


def test_verify_on_absent_config_is_not_ok(tmp_path):
    result = _carrier(tmp_path).verify(_PC_TARGET)
    assert result.ok is False


# ---------------------------------------------------------------------------
# the shipped manifest — parses + declares the full carrier set
# ---------------------------------------------------------------------------


def test_manifest_declares_all_four_carriers_one_implemented():
    data = yaml.safe_load(_MANIFEST.read_text(encoding="utf-8"))
    assert data["methodology_version"] == "1.0.0"
    ids = [c["id"] for c in data["carriers"]]
    assert ids == ["global-config", "tier1-plugin", "precommit", "floor"]
    implemented = [c["id"] for c in data["carriers"] if c["implemented"]]
    assert implemented == ["precommit"]  # only the reference carrier this slice


def test_manifest_precommit_target_carries_live_ruff_pin():
    pc = next(c for c in yaml.safe_load(_MANIFEST.read_text(encoding="utf-8"))["carriers"]
              if c["id"] == "precommit")
    repos = pc["target"]["required_repos"]
    ruff = next(r for r in repos if r["repo"] == _RUFF_REPO)
    assert ruff["rev"] == _RUFF_REV
    assert any(h["id"] == "ruff" for h in ruff["hooks"])
