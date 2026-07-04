"""Layer-1 (hermetic, offline) tests for the lived-workflow OBSERVER + engages ORACLE
(Slice B; [#252]). The oracle loads the essence-spec's engages: triples; the observer
derives its verdict from three EXTERNAL channels only (transcript-events / hook-stdout /
git-state) and NEVER from inner-session narration (C1). The live arc + the real frozen
fixtures (arc-green / arc-silent, the C4 discrimination proof) are in the skip-gated
acceptance section at the bottom, produced by the operator's live freeze (Step 7)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "deploy"))
from lived_sandbox import oracle as orc  # noqa: E402

_MANIFEST_V120 = _REPO / "deploy" / "manifest-v1.2.0.yaml"

_GATED_SIX = {
    "floor-sessionstart-guard",
    "floor-hash-verify-hook",
    "canonical-freshness",
    "hub-toc-hooks",
    "session-end-backpressure",
    "propose-closures-stop-hook",
}


# --- the engages oracle (C2 data, loaded — not hand-coded) ---


def test_oracle_loads_the_real_v120_manifest():
    o = orc.load_oracle(_MANIFEST_V120)
    assert o.version == "1.2.0"
    assert len(o.expectations) == 13  # every component carries a triple


def test_oracle_gated_active_is_exactly_the_six():
    o = orc.load_oracle(_MANIFEST_V120)
    assert {e.component_id for e in o.gated_active} == _GATED_SIX


def test_oracle_ruff_tombstone_is_gated_absent():
    o = orc.load_oracle(_MANIFEST_V120)
    assert {e.component_id for e in o.gated_absent} == {"ruff-gate"}
    ruff = o.by_id("ruff-gate")
    assert ruff.absent is True and ruff.signature == "Ruff lint gate"


def test_oracle_observed_not_gated_excludes_the_six():
    o = orc.load_oracle(_MANIFEST_V120)
    ids = {e.component_id for e in o.observed_not_gated}
    assert _GATED_SIX.isdisjoint(ids)
    assert "methodology-floor" in ids          # git-state channel -> observed, not gated
    assert "review-closures-command" in ids    # operator-invoke -> OUT-OF-ARC


def test_oracle_string_expect_is_present_signature():
    o = orc.load_oracle(_MANIFEST_V120)
    canon = o.by_id("canonical-freshness")
    assert canon.signature == "canonical_freshness" and canon.absent is False


def test_oracle_load_for_version_resolves_the_manifest():
    o = orc.load_for_version("1.2.0")
    assert {e.component_id for e in o.gated_active} == _GATED_SIX


def test_oracle_empty_expect_raises():
    with pytest.raises(orc.OracleError):
        orc._parse_expect("x", "   ")


def test_oracle_absent_mapping_without_signature_raises():
    with pytest.raises(orc.OracleError):
        orc._parse_expect("x", {"absent": True})
