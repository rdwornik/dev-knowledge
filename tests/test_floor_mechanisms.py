"""Teeth for the floor-mechanism declaration and its two-sided drift check.

The rule under test is 024's packaging rule — every floor mechanism is a manifest
COMPONENT with a version and a drift check on BOTH sides — plus DECLARE-F's F-1
split. Each teeth test injects exactly ONE defect and requires the checker to name
it, so the rule is demonstrated rather than asserted.

The live-manifest test is deliberately first: it is the one that fails when a later
seat adds a sixth mechanism and forgets a leg.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import floor_mechanisms as fm

_REPO_ROOT = Path(__file__).resolve().parents[1]
_MANIFEST = _REPO_ROOT / "deploy" / "manifest-v1.5.0.yaml"


def _well_formed(**over) -> fm.Mechanism:
    base = dict(
        id="floor-probe",
        version="1.5.0",
        split="push",
        divergence="YES — measured per-consumer hook roster.",
        waivable=True,
        payload_state="present",
        payload_blocker="",
        payload_source="scripts/arm_hooks.py",
        hub_probe={"path": "scripts/arm_hooks.py"},
        consumer_probe={"path": ".pre-commit-config.yaml"},
        declared_in="components",
    )
    base.update(over)
    return fm.Mechanism(**base)


# ---------------------------------------------------------------------------
# The live manifest
# ---------------------------------------------------------------------------


def test_live_manifest_declares_five_mechanisms_across_both_blocks():
    spec = fm.load_manifest(_MANIFEST)
    mechs = fm.load_mechanisms(spec)
    assert [m.id for m in mechs] == [
        "floor-hooks-armed",
        "floor-waiver-register",
        "floor-seal-report",
        "floor-roles-table",
        "floor-freshness-registry",
    ]
    assert sum(1 for m in mechs if m.shippable) == 2


def test_every_live_mechanism_is_well_formed():
    """The rule that decays silently: a mechanism added later with one drift leg."""
    mechs = fm.load_mechanisms(fm.load_manifest(_MANIFEST))
    problems = [p for m in mechs for p in fm.validate_mechanism(m)]
    assert problems == [], problems


def test_pre_existing_components_are_untouched_by_the_mechanism_reader():
    """The 21 components that predate this block declare no `mechanism:` and are ignored."""
    spec = fm.load_manifest(_MANIFEST)
    mech_ids = {m.id for m in fm.load_mechanisms(spec)}
    plain = [c["id"] for c in spec["components"] if c["id"] not in mech_ids]
    assert len(plain) == 21
    assert "methodology-floor" in plain and "canonical-freshness" in plain


def test_every_live_mechanism_hub_leg_resolves_or_names_its_blocker():
    """A pending mechanism must carry a measured blocker; a present one must probe clean."""
    for mech in fm.load_mechanisms(fm.load_manifest(_MANIFEST)):
        verdict = fm.hub_drift(mech, _REPO_ROOT)
        if mech.shippable:
            assert verdict.state == fm.OK, f"{mech.id}: {verdict.detail}"
        else:
            assert mech.payload_blocker, f"{mech.id} is pending with no blocker"


# ---------------------------------------------------------------------------
# Shape teeth — one injected defect each
# ---------------------------------------------------------------------------


def test_one_sided_drift_is_refused():
    """024 requires a check on BOTH sides; one leg is not two."""
    problems = fm.validate_mechanism(_well_formed(consumer_probe={}))
    assert any("drift.consumer.path is required" in p for p in problems)
    assert not any("drift.hub.path" in p for p in problems)


def test_missing_version_is_refused():
    assert any("version is required" in p for p in fm.validate_mechanism(_well_formed(version="")))


def test_split_outside_the_f1_enum_is_refused():
    problems = fm.validate_mechanism(_well_formed(split="sideways"))
    assert any("not in ['push', 'pull']" in p for p in problems)


def test_unanswered_divergence_question_is_refused():
    """'A component you cannot classify is a finding, not a coin flip.'"""
    problems = fm.validate_mechanism(_well_formed(divergence=""))
    assert any("legitimate per-consumer divergence" in p for p in problems)


def test_pull_leg_cannot_be_waivable():
    """Fleet-uniform by construction and per-consumer waivable are contradictory."""
    problems = fm.validate_mechanism(_well_formed(split="pull", waivable=True))
    assert any("contradicts" in p for p in problems)
    assert fm.validate_mechanism(_well_formed(split="pull", waivable=False)) == []


def test_pending_payload_without_a_blocker_is_refused():
    problems = fm.validate_mechanism(_well_formed(payload_state="pending", payload_blocker=""))
    assert any("requires a measured blocker" in p for p in problems)


# ---------------------------------------------------------------------------
# Drift legs
# ---------------------------------------------------------------------------


def test_hub_leg_separates_absent_from_drifted(tmp_path):
    """Presence is not identity: the token is what makes the file the thing declared."""
    # payload_source is cleared so this test isolates the IDENTITY probe; the source
    # leg has its own test above.
    absent = fm.hub_drift(
        _well_formed(payload_source="", hub_probe={"path": "nope.py"}), tmp_path
    )
    assert absent.state == fm.ABSENT

    (tmp_path / "nope.py").write_text("nothing here", encoding="utf-8")
    drifted = fm.hub_drift(
        _well_formed(payload_source="", hub_probe={"path": "nope.py", "contains": "HOOK_TYPES"}),
        tmp_path,
    )
    assert drifted.state == fm.DRIFT and "HOOK_TYPES" in drifted.detail

    (tmp_path / "nope.py").write_text("HOOK_TYPES = ()", encoding="utf-8")
    clean = fm.hub_drift(
        _well_formed(payload_source="", hub_probe={"path": "nope.py", "contains": "HOOK_TYPES"}),
        tmp_path,
    )
    assert clean.clean


def _hub_with_record(tmp_path: Path, version) -> Path:
    hub = tmp_path / "hub"
    (hub / "ecosystem").mkdir(parents=True)
    (hub / fm.DEPLOYED_VERSIONS).write_text(
        yaml.safe_dump({"repos": {"acme": {"deployed_methodology_version": version}}}),
        encoding="utf-8",
    )
    return hub


@pytest.mark.parametrize(
    "recorded, expected",
    [("1.2.0", fm.BEHIND), ("1.5.0", fm.OK), ("1.6.0", fm.OK), (None, fm.UNKNOWN)],
)
def test_consumer_leg_compares_the_recorded_version_to_the_declared_one(
    tmp_path, recorded, expected
):
    """A consumer can hold the artifact and still be behind — one leg cannot see that."""
    hub = _hub_with_record(tmp_path, recorded)
    consumer = tmp_path / "acme"
    consumer.mkdir()
    (consumer / ".pre-commit-config.yaml").write_text("repos:\n", encoding="utf-8")
    verdict = fm.consumer_drift(
        _well_formed(consumer_probe={"path": ".pre-commit-config.yaml", "contains": "repos:"}),
        consumer,
        hub_root=hub,
        consumer_name="acme",
    )
    assert verdict.state == expected


def test_consumer_leg_reports_the_artifact_before_the_version(tmp_path):
    """An absent artifact makes the version comparison moot, so it is reported first."""
    hub = _hub_with_record(tmp_path, "1.2.0")
    consumer = tmp_path / "acme"
    consumer.mkdir()
    verdict = fm.consumer_drift(
        _well_formed(consumer_probe={"path": ".pre-commit-config.yaml"}),
        consumer,
        hub_root=hub,
        consumer_name="acme",
    )
    assert verdict.state == fm.ABSENT


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


def test_plan_writes_nothing_into_the_consumer_tree(tmp_path):
    """The contract-critical property: a dry run that writes into a consumer is a breach."""
    consumer = tmp_path / "acme"
    consumer.mkdir()
    (consumer / ".methodology.yaml").write_text("sanctioned_divergences: []\n", encoding="utf-8")
    before = sorted(p.name for p in consumer.rglob("*"))

    text = fm.plan(consumer, hub_root=_REPO_ROOT, manifest=_MANIFEST, consumer_name="acme")

    assert sorted(p.name for p in consumer.rglob("*")) == before
    assert "NO DEPLOY PERFORMED" in text


def test_plan_names_every_mechanism_and_each_pending_blocker(tmp_path):
    consumer = tmp_path / "acme"
    consumer.mkdir()
    text = fm.plan(consumer, hub_root=_REPO_ROOT, manifest=_MANIFEST, consumer_name="acme")
    for mech in fm.load_mechanisms(fm.load_manifest(_MANIFEST)):
        assert f"[{mech.id}]" in text
        assert f"version={mech.version}" in text
        if not mech.shippable:
            assert "NO-OP — hub holds no payload" in text


# ---------------------------------------------------------------------------
# Reviewer round 1 (codex/terra, 2026-09-07) — one test per HIGH finding
# ---------------------------------------------------------------------------


def test_a_present_payload_must_name_its_source():
    """H3 — without payload.source, 'the hub holds a payload' is an unchecked claim."""
    problems = fm.validate_mechanism(_well_formed(payload_source=""))
    assert any("payload.source" in p for p in problems)


def test_hub_leg_fails_when_the_declared_source_is_missing(tmp_path):
    """H3 — the probe can pass while the file the carrier would SHIP does not exist."""
    (tmp_path / "probe.py").write_text("TOKEN", encoding="utf-8")
    verdict = fm.hub_drift(
        _well_formed(
            payload_source="ship-me.md",
            hub_probe={"path": "probe.py", "contains": "TOKEN"},
        ),
        tmp_path,
    )
    assert verdict.state == fm.ABSENT and "payload.source" in verdict.detail


def _verdict_for_recorded(tmp_path: Path, recorded) -> fm.DriftResult:
    hub = _hub_with_record(tmp_path, recorded)
    consumer = tmp_path / "acme"
    consumer.mkdir()
    (consumer / ".pre-commit-config.yaml").write_text("repos:\n", encoding="utf-8")
    return fm.consumer_drift(
        _well_formed(consumer_probe={"path": ".pre-commit-config.yaml"}),
        consumer,
        hub_root=hub,
        consumer_name="acme",
        waived=frozenset(),
    )


@pytest.mark.parametrize("recorded", ["1.5.0rc1", "one.five.zero", "v1.5.0-hotfix"])
def test_a_non_numeric_recorded_version_is_UNKNOWN_never_guessed(tmp_path, recorded):
    """H1 — an earlier draft ordered `1.5.0rc1` ABOVE `1.5.0`: a false-CLEAN verdict.

    UNKNOWN is the point: the failure this replaces was not "wrong verdict", it was
    "confident wrong verdict", so an unparseable version now claims nothing.
    """
    assert _verdict_for_recorded(tmp_path, recorded).state == fm.UNKNOWN


def test_a_short_but_numeric_version_still_compares(tmp_path):
    """The strictness is on NON-NUMERIC chunks only, and deliberately so.

    `1.5` is off the ADR-91 vMAJOR.MINOR.PATCH grammar but (1, 5) < (1, 5, 0) is both
    computable and correct, so it yields BEHIND rather than UNKNOWN. Refusing it would
    trade a right answer for no answer and buy no safety — the H1 hazard is a
    false-CLEAN, which this cannot produce.
    """
    assert _verdict_for_recorded(tmp_path, "1.5").state == fm.BEHIND


def test_a_malformed_deployed_versions_register_is_UNKNOWN_not_an_exception(tmp_path):
    """MED — the docstring promises UNKNOWN; a raise would kill the whole plan."""
    hub = tmp_path / "hub"
    (hub / "ecosystem").mkdir(parents=True)
    (hub / fm.DEPLOYED_VERSIONS).write_text("repos: [unbalanced\n", encoding="utf-8")
    assert fm.read_deployed_version(hub, "acme") is None


def _consumer_waiving(tmp_path: Path, component: str, *, review_date: str) -> Path:
    consumer = tmp_path / "acme"
    consumer.mkdir()
    (consumer / ".methodology.yaml").write_text(
        yaml.safe_dump(
            {"sanctioned_divergences": [
                {"component": component, "reason": "consumer pins its own hook roster",
                 "review_date": review_date},
            ]}
        ),
        encoding="utf-8",
    )
    return consumer


def test_a_valid_consumer_waiver_is_honored_and_never_planned_over(tmp_path):
    """H2 — planning a deploy over a sanctioned divergence is the [#276] re-break."""
    consumer = _consumer_waiving(tmp_path, "floor-probe", review_date="2099-01-01")
    verdict = fm.consumer_drift(
        _well_formed(id="floor-probe"), consumer, hub_root=_REPO_ROOT, consumer_name="acme"
    )
    assert verdict.state == fm.WAIVED


def test_an_expired_waiver_fails_CLOSED(tmp_path):
    """The time-box is policed by the Informant's engine, not re-implemented here."""
    consumer = _consumer_waiving(tmp_path, "floor-probe", review_date="2020-01-01")
    verdict = fm.consumer_drift(
        _well_formed(id="floor-probe"), consumer, hub_root=_REPO_ROOT, consumer_name="acme"
    )
    assert verdict.state != fm.WAIVED


def test_a_waiver_against_a_pull_mechanism_is_reported_not_obeyed(tmp_path):
    """Fleet-uniform-by-construction and per-consumer-waivable are contradictory."""
    consumer = _consumer_waiving(tmp_path, "floor-probe", review_date="2099-01-01")
    verdict = fm.consumer_drift(
        _well_formed(id="floor-probe", split="pull", waivable=False),
        consumer,
        hub_root=_REPO_ROOT,
        consumer_name="acme",
    )
    assert verdict.state == fm.DRIFT and "contradicts its classification" in verdict.detail


def test_plan_refuses_a_malformed_declaration_instead_of_planning_a_deploy(tmp_path):
    """H4 — a shape rule that only prints a note is advisory, and this one is not."""
    spec = fm.load_manifest(_MANIFEST)
    for comp in spec["components"]:
        if comp.get("id") == "floor-hooks-armed":
            comp["mechanism"]["split"] = "sideways"
    injected = tmp_path / "manifest-injected.yaml"
    injected.write_text(yaml.safe_dump(spec), encoding="utf-8")

    consumer = tmp_path / "acme"
    consumer.mkdir()
    (consumer / ".pre-commit-config.yaml").write_text("repos:\n", encoding="utf-8")
    text = fm.plan(consumer, hub_root=_REPO_ROOT, manifest=injected, consumer_name="acme")
    assert "REFUSE — malformed declaration" in text
    assert "WOULD DEPLOY — sideways" not in text


def test_plan_refuses_to_deploy_a_shippable_component_over_hub_drift(tmp_path):
    """A hub-side RED is a REFUSE, never a deploy — the leg that did not exist before."""
    spec = fm.load_manifest(_MANIFEST)
    for comp in spec["components"]:
        if comp.get("id") == "floor-hooks-armed":
            comp["mechanism"]["drift"]["hub"]["contains"] = "TOKEN-THAT-IS-NOT-THERE"
    injected = tmp_path / "manifest-injected.yaml"
    injected.write_text(yaml.safe_dump(spec), encoding="utf-8")

    consumer = tmp_path / "acme"
    consumer.mkdir()
    (consumer / ".pre-commit-config.yaml").write_text("repos:\n", encoding="utf-8")
    text = fm.plan(consumer, hub_root=_REPO_ROOT, manifest=injected, consumer_name="acme")
    assert "REFUSE — hub-side drift" in text
