"""RED-first spec tests for the ADR-109 desired-state schema v1 ([#382] W2).

Written and WITNESSED FAILING before any model code exists (ADR-108 §B: RED-first
witnesses, frozen after freeze). The import is deliberately per-test via _m() so the
RED run fails each test with ModuleNotFoundError (a witnessed failure, not a
collection error), and the assertions run unchanged once ecosystem/schema/ lands.

Spec source: ADR-109 §3 (findings as constraints) + §7 (adjudicated sol-vs-CC shape).
Constraint keys: finding 1 opaque byte-exact identity · finding 2 write-path policy
as data · finding 4 preserve-raw · finding 5 lineage/provenance · finding 7
allocation honesty (concurrent_prevention never claims prevention).

POST-FREEZE AMENDMENTS (recorded, not silent — terra review 2026-07-31,
docs/audits/2026-07-31-codex-382-w2-schema-v1.md): three witnessed assertions were
corrected on review findings H3/H7 — the derived-manifest case now constructs the
required source hash pair, and the Enforcement vocabulary is the ADR-109 §6 normative
`fail | warn` (the freeze protects the spec from drift, not from reviewed correction).
The "review-driven additions" section below is the terra-triage RED-first batch.
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
        enforcement="fail",  # AMENDED post-freeze: terra H7 — ADR-109 §6 vocabulary is fail|warn
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
               enforcement="warn")  # AMENDED post-freeze: terra H7 — ADR-109 §6 vocabulary
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
    # AMENDED post-freeze: terra H3 — a derived manifest carries the source HASH pair
    # (ADR-107 §4 clause 3 / finding 6); source alone was an under-specified spec case.
    ok = m.ResidueManifest(role="derived", source="BACKLOG.md", source_sha256="ab" * 32)
    assert ok.source == "BACKLOG.md"
    with pytest.raises(_err()):
        m.ResidueManifest(role="derived", source="BACKLOG.md", source_sha256="ab" * 32,
                          generates="BACKLOG.md")


# --- finding 2: write policy as data ----------------------------------------------------

def test_write_policy_enum_is_closed():
    m = _m()
    rec = m.SourceRecord(path="ecosystem/parity-surfaces.yaml", role="declarative",
                         write_policy="third-party-writers-barred")
    assert rec.write_policy == "third-party-writers-barred"
    with pytest.raises(_err()):
        m.SourceRecord(path="x", role="declarative", write_policy="anyone-may-write")


# --- review-driven additions (terra 2026-07-31, RED-first before the fix commit) --------

def test_component_layer_exists_and_is_queryable():
    """terra CRITICAL: ADR-109 §7 D3 — the §E query spine, population-bounded."""
    m = _m()
    comp = m.ComponentSpec(id="block-ff-push", kind="hook", ownership="hub")
    assert comp.id == "block-ff-push"
    asg = m.ComponentAssignment(repo_id="ai-council", component_id="block-ff-push",
                                desired_presence="present")
    assert asg.desired_presence == "present"
    with pytest.raises(_err()):
        m.ComponentSpec(id="x", kind="vibe", ownership="hub")
    with pytest.raises(_err()):
        m.ComponentAssignment(repo_id="r", component_id="c", desired_presence="everywhere")


def test_root_carries_components_assignments_and_lineage():
    """terra CRITICAL: the adjudicated root requires the D3 layer + finding-5 lineage."""
    m = _m()
    fleet = m.FleetDesiredState(
        schema_version="1.0.0",
        components=(m.ComponentSpec(id="c1", kind="hook", ownership="hub"),),
        assignments=(m.ComponentAssignment(repo_id="r1", component_id="c1",
                                           desired_presence="present"),),
        lineage=(m.Lineage(mode="generates", from_surface="tasks/", to_surface="BACKLOG.md"),),
    )
    assert fleet.components[0].id == "c1"
    assert fleet.lineage[0].mode == "generates"


def test_fleet_model_composes_desired_and_observed():
    """terra CRITICAL: D1 — the composition view exists; desired and observed stay typed apart."""
    m = _m()
    fm = m.FleetModel(desired=m.FleetDesiredState(schema_version="1.0.0"),
                      observed=m.ObservedFleetState())
    assert fm.desired.schema_version == "1.0.0"


def test_lineage_mode_enum_closed():
    m = _m()
    with pytest.raises(_err()):
        m.Lineage(mode="related-to", from_surface="a", to_surface="b")


def test_nested_identity_positions_refuse_bytes():
    """terra H1: identity containers are StrictStr all the way down."""
    m = _m()
    with pytest.raises(_err()):
        m.Repo(id="x", membership=frozenset([b"ai-council"]))
    with pytest.raises(_err()):
        m.ResidueManifest(role="derived", source="BACKLOG.md", source_sha256="ab" * 32,
                          row_order=(b"433-x.md",))


def test_edge_accepts_optional_strict_id():
    m = _m()
    e = m.Edge(id="edge-1", kind="doc2doc",
               src=m.EntityRef(id_space="path", id="a"),
               dst=m.EntityRef(id_space="path", id="b"),
               enforcement="fail")
    assert e.id == "edge-1"
    with pytest.raises(_err()):
        m.Edge(id=7, kind="doc2doc",
               src=m.EntityRef(id_space="path", id="a"),
               dst=m.EntityRef(id_space="path", id="b"),
               enforcement="fail")


def test_surface_retains_raw_tier_block():
    """terra H2 (accepted part): D5 — the raw tier map is retained beside the model form."""
    m = _m()
    s = m.Surface(id="s", kind="path", applicability=(), probe=m.Probe(type="dir_exists"),
                  ownership=_ownership(m), tier_raw="{hub: MUST, corp-monorepo: LOCAL}")
    assert s.tier_raw == "{hub: MUST, corp-monorepo: LOCAL}"


def test_derived_manifest_refuses_missing_hash():
    """terra H3: source without source_sha256 is an incomplete provenance pair."""
    m = _m()
    with pytest.raises(_err()):
        m.ResidueManifest(role="derived", source="BACKLOG.md")


def test_allocation_rule_v1_permits_only_not_provided():
    """terra H4: 'externally-coordinated' is a prevention-shaped claim with no organ behind it."""
    m = _m()
    with pytest.raises(_err()):
        m.AllocationRule(namespace="task-id", ledger_surface="tasks/",
                         next_free_rule="max(id in tasks/) + 1",
                         closed_ids_remain_allocated=True,
                         retirement_policy="retain-allocation-record",
                         duplicate_id_policy="refuse",
                         collision_detection_stage="merge-gate",
                         concurrent_prevention="externally-coordinated")


def test_divergence_kind_effect_mapping_enforced():
    """terra H5 (accepted part): the full kind→effect map, not only gate-rev-ahead."""
    m = _m()
    with pytest.raises(_err()):
        m.DeclaredDivergence(kind="parity-waiver", concern_id="x",
                             effect="suppress-warning", provenance=_prov(m))
    with pytest.raises(_err()):
        m.DeclaredDivergence(kind="audit-disposition", concern_id="x",
                             effect="waive", provenance=_prov(m))


def test_source_mirror_extras_are_deep_frozen():
    """terra H6: extras holding lists would make 'frozen' a fiction — they become tuples."""
    m = _m()
    p = m.Probe(type="precommit_remote", required_hook_ids=["backlog-id-on-close", "block-ff-push"])
    assert isinstance(p.required_hook_ids, tuple)
    assert p.required_hook_ids == ("backlog-id-on-close", "block-ff-push")


def test_enforcement_vocabulary_is_the_adr_normative_set():
    """terra H7 / grok H4: ADR-109 §6 — fail | warn | never-gates | inert, nothing else."""
    m = _m()
    assert {e.value for e in m.Enforcement} == {"fail", "warn", "never-gates", "inert"}
    with pytest.raises(_err()):
        m.Edge(kind="doc2doc",
               src=m.EntityRef(id_space="path", id="a"),
               dst=m.EntityRef(id_space="path", id="b"),
               enforcement="fail-gating")


# --- review-driven additions (grok shadow 2026-07-31, RED-first before the fix commit) --

def test_task_id_refuses_int():
    """grok H5: the frozen round-trip test never pinned coercion refusal."""
    m = _m()
    with pytest.raises(_err()):
        m.TaskRow(id=433, body="x")


def test_refkind_accepts_live_audit_kind():
    """grok C1: `kind: audit` is a live provenance kind on disk (parity-surfaces.yaml)."""
    m = _m()
    ref = m.ProvenanceRef(kind="audit", ref="2026-07-11 fleet audit")
    assert ref.kind == "audit"


def test_surface_sparse_fields_hold_disk_shapes():
    """grok C2: join/pending_migration/local_names are structured on disk, not scalars."""
    m = _m()
    s = m.Surface(id="ruff-gate", kind="precommit-hook", applicability=(),
                  probe=m.Probe(type="precommit_hook"), ownership=_ownership(m),
                  join=m.Join(manifest_component="ruff-gate"),
                  pending_migration=m.PendingMigration(to="ruff-check", ticket="#334"),
                  local_names=((".dev-knowledge", "arm_hooks.py"),))
    assert s.join.manifest_component == "ruff-gate"
    assert s.pending_migration.ticket == "#334"


def test_ownership_refuses_blank_reason_and_empty_provenance():
    """grok H3: the parity grammar mandates non-blank reason + non-empty provenance."""
    m = _m()
    with pytest.raises(_err()):
        m.Ownership(value="project", reason="   ",
                    provenance=(m.ProvenanceRef(kind="backlog", ref="#1"),))
    with pytest.raises(_err()):
        m.Ownership(value="project", reason="real reason", provenance=())


def test_gate_rev_ahead_requires_gate_tag():
    """grok M2: the declare-only validator's second leg, untested until now."""
    m = _m()
    with pytest.raises(_err()):
        m.DeclaredDivergence(kind="gate-rev-ahead", concern_id="x",
                             effect="declare-only", provenance=_prov(m))


def test_sot_manifest_refuses_dual_claim():
    """grok M3: source-of-truth carrying source/source_sha256 is false in the same breath."""
    m = _m()
    with pytest.raises(_err()):
        m.ResidueManifest(role="source-of-truth", generates="BACKLOG.md",
                          generated_sha256="ab" * 32, source="BACKLOG.md")


def test_allocation_literals_closed():
    """grok M4: every Literal leg refuses its illegal values, not only concurrent_prevention."""
    m = _m()
    base = dict(namespace="task-id", ledger_surface="tasks/",
                next_free_rule="max(id in tasks/) + 1",
                closed_ids_remain_allocated=True,
                retirement_policy="retain-allocation-record",
                duplicate_id_policy="refuse",
                collision_detection_stage="merge-gate",
                concurrent_prevention="not-provided")
    for bad in (dict(closed_ids_remain_allocated=False),
                dict(retirement_policy="delete"),
                dict(duplicate_id_policy="allow")):
        with pytest.raises(_err()):
            m.AllocationRule(**{**base, **bad})


def test_contract_forbids_extras_and_mirrors_stay_frozen():
    """grok M5: the extra=forbid vs extra=allow split, pinned on both sides."""
    m = _m()
    with pytest.raises(_err()):
        m.Repo(id="x", surprise_key="y")
    p = m.Probe(type="dir_exists")
    with pytest.raises(_err()):
        p.type = "file_exists"


def test_root_joins_gate_rev_refs_to_divergences():
    """grok M6: a Surface gate_rev_ahead reference must resolve to a gate-rev-ahead
    divergence in the same fleet — a dangling reference is a silent lost payload."""
    m = _m()
    surf = m.Surface(id="precommit-hub-block", kind="precommit-hook", applicability=(),
                     probe=m.Probe(type="precommit_remote"), ownership=_ownership(m),
                     gate_rev_ahead=(("corp-monorepo", "precommit-hub-block/corp-monorepo"),))
    with pytest.raises(_err()):
        m.FleetDesiredState(schema_version="1.0.0", surfaces=(surf,))
    ok = m.FleetDesiredState(
        schema_version="1.0.0", surfaces=(surf,),
        divergences=(m.DeclaredDivergence(kind="gate-rev-ahead",
                                          concern_id="precommit-hub-block/corp-monorepo",
                                          effect="declare-only", gate_tag_raw="v1.3.1",
                                          provenance=_prov(m)),))
    assert ok.surfaces[0].gate_rev_ahead[0][1] == ok.divergences[0].concern_id


def test_deployed_state_pin_observation():
    """grok M7: ADR-109 §8 — the model says per row what it cannot see."""
    m = _m()
    ds = m.DeployedState()
    assert ds.pin_observation_status == "unavailable"
    with pytest.raises(_err()):
        m.DeployedState(pin_observation_status="guessed")


def test_root_carries_manifest_cut_task_rows_and_residue():
    """grok M8 + H2: ManifestCut, task rows and residue manifests are reachable from the root."""
    m = _m()
    fleet = m.FleetDesiredState(
        schema_version="1.0.0",
        manifest=m.ManifestCut(methodology_version="1.4.0", source_tag="v1.4.0"),
        task_rows=(m.TaskRow(id="[#433]", body="- [#433] pilot"),),
        residue_manifests=(m.ResidueManifest(role="source-of-truth", generates="BACKLOG.md",
                                             generated_sha256="ab" * 32),))
    assert fleet.manifest.source_tag == "v1.4.0"
    assert fleet.task_rows[0].id == "[#433]"


def test_strict_bools_refuse_coercion():
    """grok M1: contract booleans are strict — 1/'true' are not True."""
    m = _m()
    with pytest.raises(_err()):
        m.Repo(id="x", registered=1)
    with pytest.raises(_err()):
        m.Repo(id="x", floor_carrying="true")


def test_lifecycle_role_unknown_raises():
    """grok L3: an unknown parity role is an error, never a silent None."""
    m = _m()
    with pytest.raises(ValueError):
        m.lifecycle_from_parity_role("superhub")


@pytest.mark.live_repo
def test_enums_match_parity_surfaces_on_disk():
    """grok M9: lock the enum↔disk coincidence — silent vocabulary drift is the failure mode
    this schema exists to kill."""
    import yaml
    m = _m()
    root = os.path.join(os.path.dirname(__file__), "..")
    with open(os.path.join(root, "ecosystem", "parity-surfaces.yaml"), encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    kinds = {s["kind"] for s in data["surfaces"]}
    probe_types = {s["probe"]["type"] for s in data["surfaces"] if "probe" in s}
    ownership_values = {s["ownership"]["value"] for s in data["surfaces"] if "ownership" in s}
    postures = set()
    for s in data["surfaces"]:
        for v in s.get("tier", {}).values():
            postures.add(v)
    assert kinds <= {e.value for e in m.SurfaceKind}, kinds
    assert probe_types <= {e.value for e in m.ProbeType}, probe_types
    assert ownership_values <= {e.value for e in m.OwnershipValue}, ownership_values
    assert postures <= {e.value for e in m.Posture}, postures
