"""P1 golden-diff — the essence-spec manifest conversion is behavior-preserving.

The essence-spec v1 conversion added ``anchors:`` / ``components:`` /
``doc_shapes:`` to ``deploy/manifest-v1.1.0.yaml`` and changed NOTHING the
deploy tool reads. These tests pin that claim against the frozen pre-essence
snapshot (``tests/fixtures/manifest-v1.1.0-pre-essence.yaml``):

- the ``carriers:`` section (plus version/tag) is DEEP-EQUAL to the snapshot —
  the tool's entire input surface is unchanged by construction;
- driving the REAL ``tool.assess`` code path over both manifests with identical
  stub carriers yields an IDENTICAL DeploymentPlan (items, out-of-scope rows,
  and the exact ``target`` handed to every carrier's ``detect``).

If either test reds, the conversion changed deploy behavior and P1 is wrong.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import contract  # noqa: E402
import tool  # noqa: E402
from contract import CarrierState  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parents[1]
LIVE_MANIFEST = _REPO_ROOT / "deploy" / "manifest-v1.1.0.yaml"
PRE_ESSENCE_FIXTURE = _REPO_ROOT / "tests" / "fixtures" / "manifest-v1.1.0-pre-essence.yaml"


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Structural equivalence — the tool's input surface is unchanged.
# ---------------------------------------------------------------------------


def test_carriers_section_deep_equal_to_pre_essence_snapshot():
    live, old = _load(LIVE_MANIFEST), _load(PRE_ESSENCE_FIXTURE)
    assert live["carriers"] == old["carriers"]
    assert live["methodology_version"] == old["methodology_version"]
    assert live["source_tag"] == old["source_tag"]


def test_essence_sections_present_and_inert_shape():
    """The NEW sections exist; nothing was removed from the old representation."""
    live, old = _load(LIVE_MANIFEST), _load(PRE_ESSENCE_FIXTURE)
    assert set(old) <= set(live)  # every pre-essence key survives
    for key in ("anchors", "components", "doc_shapes"):
        assert key in live and live[key], f"essence section {key!r} missing/empty"


# ---------------------------------------------------------------------------
# Golden-diff through the REAL assess code path.
# ---------------------------------------------------------------------------


class RecordingStubCarrier(contract.Carrier):
    """Fixed detect state; records the exact target the tool hands it."""

    def __init__(self, carrier_id: str, state: CarrierState) -> None:
        self.carrier_id = carrier_id
        self._state = state
        self.seen_targets: list[object] = []

    def detect(self, target):
        self.seen_targets.append(target)
        return self._state

    def apply(self, target):  # pragma: no cover - assess must never call it
        raise AssertionError("assess called apply()")

    def verify(self, target):  # pragma: no cover - assess must never call it
        raise AssertionError("assess called verify()")


# One deterministic state per carrier, deliberately covering every non-error
# CarrierState so the plan rows exercise each action mapping.
_STATES = {
    "global-config": CarrierState.PRESENT_CORRECT,
    "tier1-plugin": CarrierState.PRESENT_DRIFTED,
    "precommit": CarrierState.PRESENT_WRONG_VERSION,
    "floor": CarrierState.ABSENT,
    "enforcement-mesh": CarrierState.PRESENT_CORRECT,
}


def _assess_plan(manifest_path: Path):
    manifest = _load(manifest_path)
    ctx = tool.PreflightContext(
        repo="golden-consumer",
        version="v1.1.0",
        bare_version="1.1.0",
        repo_root=Path("/golden/consumer"),
        source_tag=str(manifest["source_tag"]),
        manifest=manifest,
        manifest_path=manifest_path,
    )
    carriers = {cid: RecordingStubCarrier(cid, state) for cid, state in _STATES.items()}
    plan = tool.assess(ctx, carrier_factory=lambda _root: carriers)
    targets = {cid: c.seen_targets for cid, c in carriers.items()}
    return plan, targets


def test_golden_diff_assess_plan_identical():
    plan_old, targets_old = _assess_plan(PRE_ESSENCE_FIXTURE)
    plan_new, targets_new = _assess_plan(LIVE_MANIFEST)

    # Identical plan rows (carrier, order, implemented, state, action, error) ...
    assert plan_new.items == plan_old.items
    # ... identical out-of-scope surfacing (l0_scope payloads) ...
    assert plan_new.out_of_scope == plan_old.out_of_scope
    # ... and every carrier received the exact same desired-state target.
    assert targets_new == targets_old

    # Sanity: the plan actually exercised all five carriers (not vacuous).
    assert len(plan_new.items) == 5
    assert {i.carrier_id for i in plan_new.items} == set(_STATES)
