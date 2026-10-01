"""Tests for the Codex-review organ carrier ([#1328], deploy/carrier_codexreview.py).

Covers the (three-state) reconcile model against the [#1328] contract:

- absent organ: ABSENT -> apply -> verify passes (both files byte-identical to hub source);
- drifted organ (one or both files stale): PRESENT_DRIFTED -> apply -> verify;
- partial presence (one file present, one absent) reads PRESENT_DRIFTED, not PRESENT_CORRECT;
- idempotency: apply then apply again writes nothing (byte-identical);
- verify reports failures (absent / drifted) per file, rather than silently passing;
- detect/verify INDEPENDENCE (D9): each survives the other's judgment helper being
  sabotaged, proving they share no correctness-judgment code path;
- the injectable user-config base (param / CLAUDE_CONFIG_DIR) — so the REAL ~/.claude/
  is NEVER touched: every carrier here is built with user_config_base = a temp dir;
- byte-identity: the hub-tracked source is byte-identical to what the carrier installs
  (the [#1328] Done-when's core claim) — no newline translation, no drift introduced by
  the copy mechanism itself.

No network; the hub sources (deploy/codex-review.ps1, deploy/codex-review.md) are read
live so tests track the real shipped organ bytes.
"""
from __future__ import annotations

from pathlib import Path

import carrier_codexreview as ccr  # noqa: E402
import contract  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parent.parent
_PS1_SOURCE = _REPO_ROOT / "deploy" / "codex-review.ps1"
_MD_SOURCE = _REPO_ROOT / "deploy" / "codex-review.md"
_LIB_SOURCE = _REPO_ROOT / "deploy" / "codex-review-lib.ps1"
_ORGAN_TARGET = {
    "organ_paths": [
        {"source_path": "deploy/codex-review.ps1", "target_rel": "bin/codex-review.ps1"},
        {"source_path": "deploy/codex-review.md", "target_rel": "commands/codex-review.md"},
        {"source_path": "deploy/codex-review-lib.ps1", "target_rel": "bin/codex-review-lib.ps1"},
    ]
}


def _carrier(user_base: Path) -> ccr.CodexReviewCarrier:
    # repo_root is UNUSED by this user-scoped carrier; the injected user_base keeps
    # every test OFF the real ~/.claude/.
    return ccr.CodexReviewCarrier(_REPO_ROOT, user_config_base=user_base)


def _ps1_target(user_base: Path) -> Path:
    return user_base / "bin" / "codex-review.ps1"


def _md_target(user_base: Path) -> Path:
    return user_base / "commands" / "codex-review.md"


def _lib_target(user_base: Path) -> Path:
    return user_base / "bin" / "codex-review-lib.ps1"


# ---------------------------------------------------------------------------
# absent -> apply -> verify
# ---------------------------------------------------------------------------


def test_absent_detects_then_applies_and_verifies(tmp_path):
    user_base = tmp_path / "claude"
    car = _carrier(user_base)
    assert not _ps1_target(user_base).exists()
    assert not _md_target(user_base).exists()
    assert not _lib_target(user_base).exists()
    assert car.detect(_ORGAN_TARGET) is contract.CarrierState.ABSENT

    result = car.apply(_ORGAN_TARGET)
    assert result.changed is True
    assert len(result.changes) == 3  # all three files written, enumerated

    assert _ps1_target(user_base).read_bytes() == _PS1_SOURCE.read_bytes()
    assert _md_target(user_base).read_bytes() == _MD_SOURCE.read_bytes()
    assert _lib_target(user_base).read_bytes() == _LIB_SOURCE.read_bytes()
    assert car.detect(_ORGAN_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_ORGAN_TARGET).ok is True


def test_apply_creates_user_dirs_if_absent(tmp_path):
    user_base = tmp_path / "fresh" / ".claude"
    assert not user_base.exists()
    _carrier(user_base).apply(_ORGAN_TARGET)
    assert (user_base / "bin").is_dir()
    assert (user_base / "commands").is_dir()


def test_apply_is_byte_identical_to_hub_source(tmp_path):
    """The [#1328] Done-when's core claim: the hub-tracked source is byte-identical to
    what the carrier installs -- no newline translation, no drift."""
    _carrier(tmp_path).apply(_ORGAN_TARGET)
    assert _ps1_target(tmp_path).read_bytes() == _PS1_SOURCE.read_bytes()
    assert _md_target(tmp_path).read_bytes() == _MD_SOURCE.read_bytes()
    assert _lib_target(tmp_path).read_bytes() == _LIB_SOURCE.read_bytes()
    # All three hub sources are CRLF (the live organ's native line ending) -- a silent LF
    # flip would defeat the whole point of this carrier (module docstring).
    assert b"\r\n" in _PS1_SOURCE.read_bytes()
    assert b"\r\n" in _MD_SOURCE.read_bytes()
    assert b"\r\n" in _LIB_SOURCE.read_bytes()


# ---------------------------------------------------------------------------
# drifted / partial -> reconcile
# ---------------------------------------------------------------------------


def test_drifted_detects_then_reconciles(tmp_path):
    (tmp_path / "bin").mkdir(parents=True)
    (tmp_path / "commands").mkdir(parents=True)
    _ps1_target(tmp_path).write_bytes(b"# stale codex-review wrapper\r\n")
    _md_target(tmp_path).write_bytes(b"# stale command doc\r\n")
    car = _carrier(tmp_path)
    assert car.detect(_ORGAN_TARGET) is contract.CarrierState.PRESENT_DRIFTED

    result = car.apply(_ORGAN_TARGET)
    assert result.changed is True
    assert car.detect(_ORGAN_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_ORGAN_TARGET).ok is True


def test_partial_presence_is_drifted_not_correct(tmp_path):
    """One file present-and-correct, one entirely absent (a third kept correct too) ->
    PRESENT_DRIFTED, not PRESENT_CORRECT (a false "nothing to do" would leave the missing
    file unreconciled)."""
    (tmp_path / "bin").mkdir(parents=True)
    _ps1_target(tmp_path).write_bytes(_PS1_SOURCE.read_bytes())
    _lib_target(tmp_path).write_bytes(_LIB_SOURCE.read_bytes())
    assert not _md_target(tmp_path).exists()
    car = _carrier(tmp_path)
    assert car.detect(_ORGAN_TARGET) is contract.CarrierState.PRESENT_DRIFTED

    result = car.apply(_ORGAN_TARGET)
    assert result.changed is True
    assert len(result.changes) == 1  # only the missing file was written
    assert car.verify(_ORGAN_TARGET).ok is True


# ---------------------------------------------------------------------------
# idempotency — apply twice writes nothing the second time
# ---------------------------------------------------------------------------


def test_apply_is_idempotent(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_ORGAN_TARGET)
    ps1_before = _ps1_target(tmp_path).read_bytes()
    md_before = _md_target(tmp_path).read_bytes()
    lib_before = _lib_target(tmp_path).read_bytes()

    second = car.apply(_ORGAN_TARGET)
    assert second.changed is False
    assert second.changes == ()
    assert _ps1_target(tmp_path).read_bytes() == ps1_before
    assert _md_target(tmp_path).read_bytes() == md_before
    assert _lib_target(tmp_path).read_bytes() == lib_before


# ---------------------------------------------------------------------------
# verify reports failures (not a silent pass)
# ---------------------------------------------------------------------------


def test_verify_on_absent_is_not_ok(tmp_path):
    result = _carrier(tmp_path / "claude").verify(_ORGAN_TARGET)
    assert result.ok is False
    assert len(result.failures) == 3
    assert any("absent" in f for f in result.failures)


def test_verify_on_drifted_reports_per_file_failure(tmp_path):
    (tmp_path / "bin").mkdir(parents=True)
    _ps1_target(tmp_path).write_bytes(b"# stale\r\n")
    result = _carrier(tmp_path).verify(_ORGAN_TARGET)
    assert result.ok is False
    assert any("differs" in f for f in result.failures)
    assert any("codex-review.ps1" in f for f in result.failures)


# ---------------------------------------------------------------------------
# D9 — verify is independent of detect (no shared correctness-judgment path)
# ---------------------------------------------------------------------------


def test_verify_does_not_route_through_detect_classifier(tmp_path, monkeypatch):
    """Sabotage detect's judgment (_classify_organ); verify must still pass."""
    car = _carrier(tmp_path)
    car.apply(_ORGAN_TARGET)

    def _boom(*_a, **_k):
        raise AssertionError("verify must not call detect's _classify_organ (D9)")

    monkeypatch.setattr(ccr, "_classify_organ", _boom)
    assert car.verify(_ORGAN_TARGET).ok is True  # independent path — unaffected


def test_detect_does_not_route_through_verify_judge(tmp_path, monkeypatch):
    """Sabotage verify's judgment (_verify_organ); detect must still classify."""
    car = _carrier(tmp_path)
    car.apply(_ORGAN_TARGET)

    def _boom(*_a, **_k):
        raise AssertionError("detect must not call verify's _verify_organ (D9)")

    monkeypatch.setattr(ccr, "_verify_organ", _boom)
    assert car.detect(_ORGAN_TARGET) is contract.CarrierState.PRESENT_CORRECT


# ---------------------------------------------------------------------------
# injectable user-config base — the REAL ~/.claude/ is never touched
# ---------------------------------------------------------------------------


def test_injected_base_overrides_default(tmp_path):
    car = ccr.CodexReviewCarrier(_REPO_ROOT, user_config_base=tmp_path)
    assert car.user_config_base == tmp_path  # injection wins over ~/.claude


def test_claude_config_dir_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    car = ccr.CodexReviewCarrier(_REPO_ROOT)  # no explicit base
    assert car.user_config_base == tmp_path  # CLAUDE_CONFIG_DIR beats the ~/.claude default
