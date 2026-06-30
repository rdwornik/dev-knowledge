"""Tests for the global Codex-reviewer-config carrier (ADR-92 C3).

Covers the (three-state) reconcile model on the global-config carrier
(deploy/carrier_globalconfig.py) against the ADR-92 contract:

- absent user config: ABSENT -> apply -> verify passes (file byte-identical to source);
- drifted user config: differs -> PRESENT_DRIFTED -> apply -> verify;
- idempotency: apply then apply again writes nothing (byte-identical);
- verify reports failures (absent / drifted) rather than silently passing;
- detect/verify INDEPENDENCE (D9): each survives the other's judgment helper being
  sabotaged, proving they share no correctness-judgment code path;
- the injectable user-config base (param / CODEX_HOME) — so the REAL ~/.codex/ is
  NEVER touched: every carrier here is built with user_config_base = a temp dir.

No network; the hub source (codex/AGENTS.md) is read live so tests track the real
shipped reviewer-config bytes.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import carrier_globalconfig as cgc  # noqa: E402
import contract  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parent.parent
# The shipped hub source — read live so tests track the real reviewer-config bytes.
_SOURCE = _REPO_ROOT / "codex" / "AGENTS.md"
# The carrier now deploys the COMMITTED (LF) blob, not the working-tree file (which
# autocrlf renders CRLF on Windows). The expected deployed bytes are therefore the
# LF-normalized source — computed here INDEPENDENTLY of the carrier (== the git blob).
_EXPECTED = _SOURCE.read_bytes().replace(b"\r\n", b"\n")
_GC_TARGET = {"source_path": "codex/AGENTS.md", "target_filename": "AGENTS.md"}


def _carrier(user_base: Path) -> cgc.GlobalConfigCarrier:
    # repo_root is UNUSED by this user-scoped carrier; the injected user_base keeps
    # every test OFF the real ~/.codex/.
    return cgc.GlobalConfigCarrier(_REPO_ROOT, user_config_base=user_base)


def _target_file(user_base: Path) -> Path:
    return user_base / "AGENTS.md"


# ---------------------------------------------------------------------------
# absent -> apply -> verify
# ---------------------------------------------------------------------------


def test_absent_detects_then_applies_and_verifies(tmp_path):
    user_base = tmp_path / "codex"
    car = _carrier(user_base)
    assert not _target_file(user_base).exists()
    assert car.detect(_GC_TARGET) is contract.CarrierState.ABSENT

    result = car.apply(_GC_TARGET)
    assert result.changed is True
    assert result.changes  # structured output: enumerated what it wrote

    assert _target_file(user_base).read_bytes() == _EXPECTED
    assert car.detect(_GC_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_GC_TARGET).ok is True


def test_apply_creates_user_dir_if_absent(tmp_path):
    # The whole ~/.codex/ chain is absent — apply must create it (a user dir).
    user_base = tmp_path / "fresh" / ".codex"
    assert not user_base.exists()
    _carrier(user_base).apply(_GC_TARGET)
    assert user_base.is_dir()
    assert _target_file(user_base).read_bytes() == _EXPECTED


def test_apply_copies_byte_identical(tmp_path):
    _carrier(tmp_path).apply(_GC_TARGET)
    assert _target_file(tmp_path).read_bytes() == _EXPECTED  # LF canonical (committed blob)


def test_apply_deploys_lf_no_crlf(tmp_path):
    # Regression guard for the Windows-text-mode-CRLF class: the deployed config
    # must be LF-only, never CRLF (reading the working-tree file on a Windows hub
    # previously propagated CRLF into ~/.codex/AGENTS.md).
    _carrier(tmp_path).apply(_GC_TARGET)
    deployed = _target_file(tmp_path).read_bytes()
    assert b"\r\n" not in deployed
    assert b"\r" not in deployed


# ---------------------------------------------------------------------------
# drifted -> reconcile
# ---------------------------------------------------------------------------


def test_drifted_detects_then_reconciles(tmp_path):
    _target_file(tmp_path).write_bytes(b"# stale reviewer config\n")
    car = _carrier(tmp_path)
    assert car.detect(_GC_TARGET) is contract.CarrierState.PRESENT_DRIFTED

    result = car.apply(_GC_TARGET)
    assert result.changed is True
    assert car.detect(_GC_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_GC_TARGET).ok is True
    assert _target_file(tmp_path).read_bytes() == _EXPECTED


# ---------------------------------------------------------------------------
# idempotency — apply twice writes nothing the second time
# ---------------------------------------------------------------------------


def test_apply_is_idempotent(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_GC_TARGET)
    before = _target_file(tmp_path).read_bytes()

    second = car.apply(_GC_TARGET)
    after = _target_file(tmp_path).read_bytes()
    assert second.changed is False
    assert second.changes == ()
    assert before == after  # byte-identical: no spurious rewrite


# ---------------------------------------------------------------------------
# verify reports failures (not a silent pass)
# ---------------------------------------------------------------------------


def test_verify_on_absent_is_not_ok(tmp_path):
    result = _carrier(tmp_path / "codex").verify(_GC_TARGET)
    assert result.ok is False
    assert any("absent" in f for f in result.failures)


def test_verify_on_drifted_reports_failure(tmp_path):
    _target_file(tmp_path).write_bytes(b"# stale reviewer config\n")
    result = _carrier(tmp_path).verify(_GC_TARGET)
    assert result.ok is False
    assert any("differs" in f for f in result.failures)


# ---------------------------------------------------------------------------
# D9 — verify is independent of detect (no shared correctness-judgment path)
# ---------------------------------------------------------------------------


def test_verify_does_not_route_through_detect_classifier(tmp_path, monkeypatch):
    """Sabotage detect's judgment (_classify_global); verify must still pass."""
    car = _carrier(tmp_path)
    car.apply(_GC_TARGET)

    def _boom(*_a, **_k):
        raise AssertionError("verify must not call detect's _classify_global (D9)")

    monkeypatch.setattr(cgc, "_classify_global", _boom)
    assert car.verify(_GC_TARGET).ok is True  # independent path — unaffected


def test_detect_does_not_route_through_verify_judge(tmp_path, monkeypatch):
    """Sabotage verify's judgment (_verify_global); detect must still classify."""
    car = _carrier(tmp_path)
    car.apply(_GC_TARGET)

    def _boom(*_a, **_k):
        raise AssertionError("detect must not call verify's _verify_global (D9)")

    monkeypatch.setattr(cgc, "_verify_global", _boom)
    assert car.detect(_GC_TARGET) is contract.CarrierState.PRESENT_CORRECT


# ---------------------------------------------------------------------------
# injectable user-config base — the REAL ~/.codex/ is never touched
# ---------------------------------------------------------------------------


def test_injected_base_overrides_default(tmp_path):
    car = cgc.GlobalConfigCarrier(_REPO_ROOT, user_config_base=tmp_path)
    assert car.user_config_base == tmp_path  # injection wins over ~/.codex


def test_codex_home_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    car = cgc.GlobalConfigCarrier(_REPO_ROOT)  # no explicit base
    assert car.user_config_base == tmp_path  # CODEX_HOME beats the ~/.codex default
