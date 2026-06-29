"""Tests for the per-repo methodology-floor carrier (ADR-92 C4).

Covers the (three-state) reconcile model on the floor carrier
(deploy/carrier_floor.py) against the ADR-92 contract:

- absent floor: ABSENT -> apply -> verify passes (floor + sidecar written under the
  consumer's .claude/);
- drifted (floor edited / sidecar missing / sidecar stale): PRESENT_DRIFTED -> apply
  -> verify;
- idempotency: apply then apply again writes nothing (byte-identical);
- verify reports failures rather than silently passing;
- detect/verify INDEPENDENCE (D9): each survives the other's judgment helper being
  sabotaged;
- the carrier writes ONLY the consumer tree — apply() does NOT refresh the HUB's
  templates/child-methodology-floor.sha256 anchor (the differentiator from shelling
  out to generate_floor.py generate --out-dir).

The consumer is a temp dir; the floor is rendered from the real hub template. No
network, no real consumer repos, and the hub tree is left untouched.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import carrier_floor as cf  # noqa: E402
import contract  # noqa: E402

_FLOOR_TARGET = {
    "floor_path": ".claude/CLAUDE-FLOOR.md",
    "sidecar_path": ".claude/CLAUDE-FLOOR.md.sha256",
}

# Oracle: the corpus-state floor body + digest, computed independently of the
# carrier's own helper (straight from the hub generator's public functions).
_FLOOR_BODY = cf.gf.render_floor()
_FLOOR_DIGEST = cf.gf.floor_sha256(_FLOOR_BODY)


def _carrier(repo: Path) -> cf.FloorCarrier:
    return cf.FloorCarrier(repo)


def _floor_file(repo: Path) -> Path:
    return repo / ".claude" / "CLAUDE-FLOOR.md"


def _sidecar_file(repo: Path) -> Path:
    return repo / ".claude" / "CLAUDE-FLOOR.md.sha256"


# ---------------------------------------------------------------------------
# absent -> apply -> verify
# ---------------------------------------------------------------------------


def test_absent_detects_then_applies_and_verifies(tmp_path):
    car = _carrier(tmp_path)
    assert not _floor_file(tmp_path).exists()
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.ABSENT

    result = car.apply(_FLOOR_TARGET)
    assert result.changed is True
    assert len(result.changes) == 2  # floor + sidecar, enumerated (structured output)

    assert _floor_file(tmp_path).exists()
    assert _sidecar_file(tmp_path).exists()
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_FLOOR_TARGET).ok is True


def test_apply_writes_floor_and_sidecar_matching_hub_render(tmp_path):
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    # floor body is byte-for-byte the hub render (LF-normalized read to be autocrlf-proof)
    assert cf.gf.normalize(_floor_file(tmp_path).read_text(encoding="utf-8")) == _FLOOR_BODY
    # sidecar records the matching content-integrity digest
    assert cf._read_sidecar_hash(_sidecar_file(tmp_path)) == _FLOOR_DIGEST


def test_floor_written_under_consumer_claude_dir(tmp_path):
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    assert (tmp_path / ".claude").is_dir()  # the consumer's own CC config dir, created


# ---------------------------------------------------------------------------
# drifted -> reconcile (three drift shapes)
# ---------------------------------------------------------------------------


def test_drifted_floor_edited_detects_then_reconciles(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    # tamper the floor body — content hash no longer matches the corpus digest.
    _floor_file(tmp_path).write_text(_FLOOR_BODY + "\nTAMPER\n", encoding="utf-8", newline="\n")
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED

    result = car.apply(_FLOOR_TARGET)
    assert result.changed is True
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_FLOOR_TARGET).ok is True


def test_drifted_sidecar_missing_detects_drifted(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _sidecar_file(tmp_path).unlink()  # floor intact, sidecar gone
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED

    car.apply(_FLOOR_TARGET)
    assert car.verify(_FLOOR_TARGET).ok is True


def test_drifted_sidecar_stale_detects_drifted(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _sidecar_file(tmp_path).write_text("0" * 64 + "\n", encoding="utf-8", newline="\n")
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED

    car.apply(_FLOOR_TARGET)
    assert cf._read_sidecar_hash(_sidecar_file(tmp_path)) == _FLOOR_DIGEST  # re-pinned
    assert car.verify(_FLOOR_TARGET).ok is True


# ---------------------------------------------------------------------------
# idempotency — apply twice writes nothing the second time
# ---------------------------------------------------------------------------


def test_apply_is_idempotent(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    floor_before = _floor_file(tmp_path).read_bytes()
    sidecar_before = _sidecar_file(tmp_path).read_bytes()

    second = car.apply(_FLOOR_TARGET)
    assert second.changed is False
    assert second.changes == ()
    assert _floor_file(tmp_path).read_bytes() == floor_before
    assert _sidecar_file(tmp_path).read_bytes() == sidecar_before


# ---------------------------------------------------------------------------
# verify reports failures (not a silent pass)
# ---------------------------------------------------------------------------


def test_verify_on_absent_floor_is_not_ok(tmp_path):
    result = _carrier(tmp_path).verify(_FLOOR_TARGET)
    assert result.ok is False
    assert any("floor absent" in f for f in result.failures)


def test_verify_reports_floor_and_sidecar_failures(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _floor_file(tmp_path).write_text(_FLOOR_BODY + "\nTAMPER\n", encoding="utf-8", newline="\n")
    _sidecar_file(tmp_path).unlink()
    failures = car.verify(_FLOOR_TARGET).failures
    assert any("floor content hash" in f for f in failures)
    assert any("sidecar absent" in f for f in failures)


# ---------------------------------------------------------------------------
# D9 — verify is independent of detect (no shared correctness-judgment path)
# ---------------------------------------------------------------------------


def test_verify_does_not_route_through_detect_classifier(tmp_path, monkeypatch):
    """Sabotage detect's judgment (_classify_floor); verify must still pass."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)

    def _boom(*_a, **_k):
        raise AssertionError("verify must not call detect's _classify_floor (D9)")

    monkeypatch.setattr(cf, "_classify_floor", _boom)
    assert car.verify(_FLOOR_TARGET).ok is True  # independent path — unaffected


def test_detect_does_not_route_through_verify_judge(tmp_path, monkeypatch):
    """Sabotage verify's judgment (_verify_floor); detect must still classify."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)

    def _boom(*_a, **_k):
        raise AssertionError("detect must not call verify's _verify_floor (D9)")

    monkeypatch.setattr(cf, "_verify_floor", _boom)
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT


# ---------------------------------------------------------------------------
# consumer-scoped — apply() never mutates the HUB canonical SHA anchor
# ---------------------------------------------------------------------------


def test_apply_does_not_refresh_hub_canonical_sha(tmp_path):
    # The differentiator from `generate_floor.py generate --out-dir` (which refreshes
    # the hub anchor as a side-effect): this carrier writes ONLY the consumer tree.
    hub_anchor = cf.gf.HUB_CANONICAL_SHA
    assert hub_anchor.exists()
    before = hub_anchor.read_bytes()

    _carrier(tmp_path).apply(_FLOOR_TARGET)

    assert hub_anchor.read_bytes() == before  # hub anchor untouched
