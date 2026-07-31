"""RED-first spec tests for the ADR-109 desired-state schema v1 ([#382] W2).

Written and WITNESSED FAILING before any model code exists (ADR-108 §B: RED-first
witnesses, frozen after freeze). The import is deliberately per-test via _m() so the
RED run fails each test with ModuleNotFoundError (a witnessed failure, not a
collection error), and the assertions run unchanged once ecosystem/schema/ lands.

Spec source: ADR-109 §3 (findings as constraints) + §7 (adjudicated sol-vs-CC shape).
Constraint keys: finding 1 opaque byte-exact identity · finding 2 write-path policy
as data · finding 4 preserve-raw · finding 5 lineage/provenance · finding 7
allocation honesty (concurrent_prevention never claims prevention).
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _m():
    from ecosystem.schema import desired_state
    return desired_state


def _err():
    from pydantic import ValidationError
    return ValidationError


# --- root contract ----------------------------------------------------------------------

def test_schema_version_is_literal_1_0_0():
    m = _m()
    fleet = m.FleetDesiredState(schema_version="1.0.0")
    assert fleet.schema_version == "1.0.0"
    with pytest.raises(_err()):
        m.FleetDesiredState(schema_version="1.1.0")


def test_models_are_frozen():
    m = _m()
    fleet = m.FleetDesiredState(schema_version="1.0.0")
    with pytest.raises(_err()):
        fleet.schema_version = "2.0.0"


# --- finding 1: identity opaque + byte-exact --------------------------------------------

def test_repo_id_opaque_verbatim_including_leading_dot():
    m = _m()
    repo = m.Repo(id=".dev-knowledge")
    assert repo.id == ".dev-knowledge"


def test_repo_id_refuses_non_string():
    m = _m()
    with pytest.raises(_err()):
        m.Repo(id=382)


def test_task_id_never_normalized():
    m = _m()
    row = m.TaskRow(id="[#433]", body="- [#433] pilot row")
    assert row.id == "[#433]"


# --- finding 4: preserve-raw ------------------------------------------------------------

def test_depends_on_bare_and_hashed_both_preserved_verbatim():
    m = _m()
    bare = m.TaskRow(id="[#383]", body="x", depends_on="382")
    hashed = m.TaskRow(id="[#112]", body="x", depends_on="#23")
    assert bare.depends_on == "382"
    assert hashed.depends_on == "#23"


def test_task_row_unknown_frontmatter_keys_survive():
    m = _m()
    row = m.TaskRow(id="[#1]", body="x", **{"verified_by": "operator"})
    assert row.model_dump()["verified_by"] == "operator"


def test_edge_raw_declaration_preserved_byte_exact():
    m = _m()
    raw = 'reconciled_with: handoff-process@6.0.1'
    e = m.Edge(
        kind="doc2doc",
        src=m.EntityRef(id_space="path", id="CLAUDE.md"),
        dst=m.EntityRef(id_space="spec-id", id="handoff-process"),
        enforcement="fail-gating",
        raw=raw,
    )
    assert e.raw == raw


# --- observed state ---------------------------------------------------------------------

def test_deployed_state_all_null_is_legal():
    m = _m()
    ds = m.DeployedState()
    assert ds.version is None and ds.source_tag is None


def test_deployed_state_partial_null_refused():
    m = _m()
    with pytest.raises(_err()):
        m.DeployedState(version="1.3.1", deployed_date="2026-07-11", source_tag=None)


# --- surfaces (parity grammar absorbed) -------------------------------------------------

def _ownership(m):
    return m.Ownership(value="methodology-generic", reason="test",
                       provenance=[m.ProvenanceRef(kind="backlog", ref="#382")])


def test_surface_ownership_is_mandatory():
    m = _m()
    with pytest.raises(_err()):
        m.Surface(id="precommit-hub-block", kind="precommit-hook",
                  applicability=[], probe=m.Probe(type="precommit_remote"))


def test_applicability_posture_enum_closed():
    m = _m()
    ok = m.ApplicabilityRule(selector_kind="repository", selector="corp-monorepo", posture="MUST")
    assert ok.posture == "MUST"
    with pytest.raises(_err()):
        m.ApplicabilityRule(selector_kind="role", selector="consumer", posture="MAYBE")


def test_probe_unknown_params_preserved():
    m = _m()
    p = m.Probe(type="precommit_remote", repo_token="dev-knowledge", ancestry=True)
    dumped = p.model_dump()
    assert dumped["repo_token"] == "dev-knowledge" and dumped["ancestry"] is True


# --- divergences: two vocabularies, one type (C7/G14) -----------------------------------

def _prov(m):
    return m.Provenance(reason="test", refs=[m.ProvenanceRef(kind="backlog", ref="#336")])


def test_gate_rev_ahead_is_declare_only_never_waives():
    m = _m()
    d = m.DeclaredDivergence(kind="gate-rev-ahead", concern_id="precommit-hub-block/corp-monorepo",
                             effect="declare-only", gate_tag_raw="v1.3.1", provenance=_prov(m))
    assert d.waives_must is False
    with pytest.raises(_err()):
        m.DeclaredDivergence(kind="gate-rev-ahead", concern_id="x", effect="waive",
                             gate_tag_raw="v1.3.1", provenance=_prov(m))


def test_one_per_concern_uniqueness_within_mechanism():
    m = _m()
    d1 = m.DeclaredDivergence(kind="parity-waiver", concern_id="ruff-gate",
                              effect="waive", provenance=_prov(m))
    d2 = m.DeclaredDivergence(kind="parity-waiver", concern_id="ruff-gate",
                              effect="waive", provenance=_prov(m))
    with pytest.raises(_err()):
        m.FleetDesiredState(schema_version="1.0.0", divergences=[d1, d2])


# --- edges + crosswalk (G9) -------------------------------------------------------------

def test_edge_kind_and_id_space_enums_closed():
    m = _m()
    with pytest.raises(_err()):
        m.Edge(kind="doc2metric",
               src=m.EntityRef(id_space="path", id="a"),
               dst=m.EntityRef(id_space="path", id="b"),
               enforcement="warn-only")
    with pytest.raises(_err()):
        m.EntityRef(id_space="vibe-id", id="x")


def test_crosswalk_requires_two_members_and_closed_relation():
    m = _m()
    one = m.EntityRef(id_space="surface-id", id="precommit-hub-block")
    two = m.EntityRef(id_space="hook-id", id="block-ff-push")
    ok = m.Crosswalk(organ="hub-block gate", members=[one, two], relation="same-organ")
    assert len(ok.members) == 2
    with pytest.raises(_err()):
        m.Crosswalk(organ="x", members=[one], relation="same-organ")
    with pytest.raises(_err()):
        m.Crosswalk(organ="x", members=[one, two], relation="feels-related")


# --- lifecycle (D2: role is NOT lifecycle-bearing) --------------------------------------

def test_lifecycle_assertion_preserves_raw_and_semantics():
    m = _m()
    a = m.LifecycleAssertion(source_surface="registry", semantics="observed",
                             raw_value="registered · unonboarded (floor-carrying)",
                             mapped_stage="floor_only")
    assert a.raw_value == "registered · unonboarded (floor-carrying)"
    with pytest.raises(_err()):
        m.LifecycleAssertion(source_surface="registry", semantics="vibes",
                             raw_value="x", mapped_stage="full")


def test_parity_role_does_not_map_into_lifecycle_except_hub():
    m = _m()
    assert m.lifecycle_from_parity_role("hub") == m.LifecycleStage.source
    assert m.lifecycle_from_parity_role("consumer") is None
    assert m.lifecycle_from_parity_role("pre-deploy") is None


# --- finding 7: allocation honesty ------------------------------------------------------

def test_allocation_rule_never_claims_concurrent_prevention():
    m = _m()
    rule = m.AllocationRule(namespace="task-id", ledger_surface="tasks/",
                            next_free_rule="max(id in tasks/) + 1",
                            closed_ids_remain_allocated=True,
                            retirement_policy="retain-allocation-record",
                            duplicate_id_policy="refuse",
                            collision_detection_stage="merge-gate",
                            concurrent_prevention="not-provided")
    assert rule.concurrent_prevention == "not-provided"
    with pytest.raises(_err()):
        m.AllocationRule(namespace="task-id", ledger_surface="tasks/",
                         next_free_rule="max(id in tasks/) + 1",
                         closed_ids_remain_allocated=True,
                         retirement_policy="retain-allocation-record",
                         duplicate_id_policy="refuse",
                         collision_detection_stage="merge-gate",
                         concurrent_prevention="prevented")


# --- finding 5: lineage direction honesty (post-flip semantics) -------------------------

def test_residue_manifest_source_of_truth_requires_generates():
    m = _m()
    ok = m.ResidueManifest(role="source-of-truth", generates="BACKLOG.md",
                           generated_sha256="ab" * 32)
    assert ok.generates == "BACKLOG.md"
    with pytest.raises(_err()):
        m.ResidueManifest(role="source-of-truth")


def test_residue_manifest_derived_requires_source_and_forbids_generates():
    m = _m()
    ok = m.ResidueManifest(role="derived", source="BACKLOG.md")
    assert ok.source == "BACKLOG.md"
    with pytest.raises(_err()):
        m.ResidueManifest(role="derived", source="BACKLOG.md", generates="BACKLOG.md")


# --- finding 2: write policy as data ----------------------------------------------------

def test_write_policy_enum_is_closed():
    m = _m()
    rec = m.SourceRecord(path="ecosystem/parity-surfaces.yaml", role="declarative",
                         write_policy="third-party-writers-barred")
    assert rec.write_policy == "third-party-writers-barred"
    with pytest.raises(_err()):
        m.SourceRecord(path="x", role="declarative", write_policy="anyone-may-write")
