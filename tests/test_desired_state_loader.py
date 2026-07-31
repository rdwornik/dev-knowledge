"""RED-first spec tests for the ADR-109 desired-state loader ([#382] W3).

Written and WITNESSED FAILING before scripts/desired_state_loader.py exists. The
frozen W3 contract: ONE validated FleetModel from ALL seven live sources
(registry.md, index.yaml, deployed-versions.yaml, parity-surfaces.yaml,
satellite-onboarding-rulings.yaml, .methodology.yaml, deploy/manifest-v1.4.0.yaml);
membership = union with disagreements resolving toward deployed-versions.yaml and
loading as model FACTS never errors; the sanctioned corp-monorepo 1.2.0-vs-v1.3.1
divergence loads as DECLARED; index.yaml staleness surfaced as a model field;
read-only against the fleet — zero files written.

Fixtures reproduce the registry-prep dossier conflicts C1–C8
(docs/audits/2026-07-31-technical-382-registry-prep-dossier.md §i.4).
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _loader():
    from scripts import desired_state_loader
    return desired_state_loader


def _schema():
    from ecosystem.schema import desired_state
    return desired_state


# --- fixture fleet (mini versions of the seven live sources) ----------------------------

REGISTRY_MD = """# Fleet registry

| Repo | Path | Purpose | Status |
|------|------|---------|--------|
| `.dev-knowledge` | C:\\Dev\\.dev-knowledge | Methodology hub | source (hub — methodology origin) |
| `ai-council` | C:\\Dev\\ai-council | Council engine | registered · onboarded (v1.2.0) |
| `corp-monorepo` | C:\\Dev\\corp-monorepo | Corp work | registered · onboarded (v1.2.0) |
| `corp-ops` | C:\\Dev\\corp-ops | Ops | registered · unonboarded |
| `corp-sca-time-automation` | C:\\Dev\\corp-sca | SCA | registered · unonboarded (floor-carrying) |
| `win-tooling` | C:\\Dev\\win-tooling | Windows tooling | registered · methodology-unonboarded |
"""

DEPLOYED_VERSIONS = """repos:
  .dev-knowledge:
    deployed_methodology_version: null
    deployed_date: null
    source_tag: null
  ai-council:
    deployed_methodology_version: "1.3.1"
    deployed_date: "2026-07-11"
    source_tag: "v1.3.1"
  corp-monorepo:
    deployed_methodology_version: "1.2.0"
    deployed_date: "2026-07-07"
    source_tag: "v1.2.0"
  corp-ops:
    deployed_methodology_version: null
    deployed_date: null
    source_tag: null
  corp-sca-time-automation:
    deployed_methodology_version: null
    deployed_date: null
    source_tag: null
"""

PARITY_SURFACES = """version: 1.3.0
fleet:
  .dev-knowledge: {role: hub}
  ai-council: {role: consumer}
  corp-monorepo: {role: consumer}
  corp-ops: {role: pre-deploy}
  corp-sca-time-automation: {role: pre-deploy}
surfaces:
  - id: journal-file
    kind: path
    tier: {hub: MUST, consumer: MUST, corp-monorepo: LOCAL}
    probe: {type: path_tracked, path: JOURNAL.md}
    ownership:
      value: methodology-generic
      reason: every governed repo journals
      provenance:
        - {kind: audit, repo: .dev-knowledge, ref: 2026-07-11 fleet audit}
  - id: precommit-hub-block
    kind: precommit-hook
    tier: {consumer: MUST}
    probe: {type: precommit_remote, repo_token: dev-knowledge, expected_rev_from: deployed-versions, ancestry: true}
    ownership:
      value: methodology-generic
      reason: the hub gate block is the corpus carrier
      provenance:
        - {kind: backlog, repo: .dev-knowledge, ref: "#328"}
    local_names: {.dev-knowledge: arm_hooks.py}
    gate_rev_ahead:
      corp-monorepo:
        gate_tag: v1.3.1
        reason: >-
          Enforcement gate uplifted ahead of corpus; corpus stays 1.2.0 BY DESIGN.
        provenance:
          - {kind: git-tag, repo: .dev-knowledge, ref: v1.3.1}
          - {kind: backlog, repo: .dev-knowledge, ref: "#336"}
"""

ONBOARDING_RULINGS = """version: 1
rulings:
  corp-ops:
    profile: full
    ruled_by: operator
    ruled_date: "2026-07-16"
    census_ref: docs/audits/2026-07-16-census.md
  corp-sca-time-automation:
    profile: full
    ruled_by: operator
    ruled_date: "2026-07-16"
    census_ref: docs/audits/2026-07-16-census.md
"""

METHODOLOGY_YAML = """sanctioned_divergences:
  - component: ruff-gate
    reason: hub gates ruff in system form pending #334 migration
    review_date: 2026-09-01
  - component: token-log
    reason: append-only local artifact, not a corpus surface
    review_date: 2026-10-25
"""

INDEX_YAML = """generated: '2026-07-11T12:30:02'
repos:
  - name: ai-council
    path: C:\\Dev\\ai-council
    last_audit: '2026-07-11'
    findings:
      - check_name: handoff_stamp
        evidence: All stamp occurrences match canonical HANDOFF_PROCESS v5.7
        status: pass
  - name: win-tooling
    path: C:\\Dev\\win-tooling
    last_audit: '2026-07-11'
    findings:
      - check_name: deployed_methodology_version
        evidence: win-tooling not listed in deployed-versions.yaml (ADR-91)
        status: warn
"""

MANIFEST_YAML = """methodology_version: "1.4.0"
source_tag: v1.4.0
"""


@pytest.fixture
def fleet_dir(tmp_path):
    eco = tmp_path / "ecosystem"
    eco.mkdir()
    (eco / "registry.md").write_text(REGISTRY_MD, encoding="utf-8")
    (eco / "deployed-versions.yaml").write_text(DEPLOYED_VERSIONS, encoding="utf-8")
    (eco / "parity-surfaces.yaml").write_text(PARITY_SURFACES, encoding="utf-8")
    (eco / "satellite-onboarding-rulings.yaml").write_text(ONBOARDING_RULINGS, encoding="utf-8")
    (eco / "index.yaml").write_text(INDEX_YAML, encoding="utf-8")
    (tmp_path / ".methodology.yaml").write_text(METHODOLOGY_YAML, encoding="utf-8")
    deploy = tmp_path / "deploy"
    deploy.mkdir()
    (deploy / "manifest-v1.4.0.yaml").write_text(MANIFEST_YAML, encoding="utf-8")
    return tmp_path


def _load(fleet_dir):
    return _loader().load_fleet_model(fleet_dir)


def _repo(model, rid):
    return next(r for r in model.desired.repos if r.id == rid)


# --- the one validated model ------------------------------------------------------------

def test_load_returns_one_validated_fleet_model(fleet_dir):
    m = _schema()
    fm = _load(fleet_dir)
    assert isinstance(fm, m.FleetModel)
    assert fm.desired.schema_version == "1.0.0"


def test_all_seven_sources_recorded_with_write_policy(fleet_dir):
    fm = _load(fleet_dir)
    paths = {s.path for s in fm.desired.sources}
    assert paths == {
        "ecosystem/registry.md",
        "ecosystem/index.yaml",
        "ecosystem/deployed-versions.yaml",
        "ecosystem/parity-surfaces.yaml",
        "ecosystem/satellite-onboarding-rulings.yaml",
        ".methodology.yaml",
        "deploy/manifest-v1.4.0.yaml",
    }
    assert all(s.write_policy in ("round-trip-unknown-byte-stable",
                                  "third-party-writers-barred") for s in fm.desired.sources)


# --- C1: membership disagreement is a FACT, resolution toward deployed-versions ---------

def test_c1_membership_union_and_resolution(fleet_dir):
    ld = _loader()
    fm = _load(fleet_dir)
    ids = {r.id for r in fm.desired.repos}
    assert "win-tooling" in ids  # union: registry+index only — loads, never errors
    wt = _repo(fm, "win-tooling")
    assert "deployed-versions" not in wt.membership
    assert "registry-md" in wt.membership and "index-yaml" in wt.membership
    members = ld.resolve_fleet_members(fm.desired)
    assert set(members) == {".dev-knowledge", "ai-council", "corp-monorepo",
                            "corp-ops", "corp-sca-time-automation"}


# --- C2: registry.md contradicts deployed-versions — both preserved, no error -----------

def test_c2_registry_version_contradiction_is_data(fleet_dir):
    fm = _load(fleet_dir)
    ai = _repo(fm, "ai-council")
    assert ai.deployed.version == "1.3.1"
    raw = dict(ai.status_raw)["registry-md"]
    assert "v1.2.0" in raw  # the stale claim survives verbatim beside the anchor value


# --- C3: ruled target vs observed null — coexisting typed assertions --------------------

def test_c3_ruled_full_with_nothing_deployed(fleet_dir):
    fm = _load(fleet_dir)
    ops = _repo(fm, "corp-ops")
    assert ops.deployed.version is None
    kinds = {(a.semantics, a.mapped_stage) for a in ops.assertions}
    assert ("desired", "full") in {(s.value, st.value) for s, st in kinds}


# --- C4: the sanctioned corp divergence loads as DECLARED -------------------------------

def test_c4_corp_gate_rev_ahead_loads_as_declared(fleet_dir):
    fm = _load(fleet_dir)
    corp = _repo(fm, "corp-monorepo")
    assert corp.deployed.version == "1.2.0"  # never "fixed" to 1.3.1
    gra = [d for d in fm.desired.divergences if d.kind == "gate-rev-ahead"]
    assert len(gra) == 1
    assert gra[0].gate_tag_raw == "v1.3.1"
    assert gra[0].effect == "declare-only"
    surf = next(s for s in fm.desired.surfaces if s.id == "precommit-hub-block")
    assert surf.gate_rev_ahead == (("corp-monorepo", gra[0].concern_id),)


# --- C5: four lifecycle vocabularies survive raw beside one mapped stage ----------------

def test_c5_lifecycle_raw_beside_mapped(fleet_dir):
    fm = _load(fleet_dir)
    sca = _repo(fm, "corp-sca-time-automation")
    reg = next(a for a in sca.assertions if a.source_surface == "registry")
    assert reg.raw_value == "registered · unonboarded (floor-carrying)"
    assert reg.mapped_stage == "floor_only"
    assert sca.floor_carrying is True


# --- C6: name is the join key; path is carried where sources hold it --------------------

def test_c6_join_on_name_path_carried(fleet_dir):
    fm = _load(fleet_dir)
    ai = _repo(fm, "ai-council")
    assert ai.path is not None and ai.path.endswith("ai-council")
    hub = _repo(fm, ".dev-knowledge")
    assert hub.id == ".dev-knowledge"  # leading dot byte-exact


# --- C7: both suppression vocabularies coexist in one type, one-per-concern -------------

def test_c7_two_suppression_vocabularies_one_type(fleet_dir):
    fm = _load(fleet_dir)
    waivers = [d for d in fm.desired.divergences if d.kind == "parity-waiver"]
    assert {w.concern_id for w in waivers} == {"ruff-gate", "token-log"}
    assert all(w.effect == "waive" for w in waivers)
    # coexists with the gate-rev-ahead declaration under root one-per-concern validation
    assert any(d.kind == "gate-rev-ahead" for d in fm.desired.divergences)


# --- C8: derived-registry staleness is surfaced, never repaired -------------------------

def test_c8_index_staleness_surfaced(fleet_dir):
    fm = _load(fleet_dir)
    assert fm.observed.generated_raw == "2026-07-11T12:30:02"
    names = {o.repo_id for o in fm.observed.repos}
    assert names == {"ai-council", "win-tooling"}


def test_c8_index_file_not_rewritten(fleet_dir):
    before = (fleet_dir / "ecosystem" / "index.yaml").read_bytes()
    _load(fleet_dir)
    assert (fleet_dir / "ecosystem" / "index.yaml").read_bytes() == before


# --- roles, tier mapping, manifest anchors ----------------------------------------------

def test_roles_load_but_do_not_bear_lifecycle(fleet_dir):
    fm = _load(fleet_dir)
    assert _repo(fm, ".dev-knowledge").role == "hub"
    ai = _repo(fm, "ai-council")
    assert ai.role == "consumer"
    assert not any(a.source_surface == "parity" and a.semantics != "role-classification"
                   for a in ai.assertions)


def test_tier_map_becomes_applicability_repo_overrides_role(fleet_dir):
    fm = _load(fleet_dir)
    surf = next(s for s in fm.desired.surfaces if s.id == "journal-file")
    rules = {(r.selector_kind.value, r.selector): r.posture.value for r in surf.applicability}
    assert rules[("role", "hub")] == "MUST"
    assert rules[("repository", "corp-monorepo")] == "LOCAL"  # repo key typed as repository
    assert surf.tier_raw  # the verbatim block is retained (D5)


def test_manifest_cut_loaded(fleet_dir):
    fm = _load(fleet_dir)
    assert fm.desired.manifest.methodology_version == "1.4.0"
    assert fm.desired.manifest.source_tag == "v1.4.0"


# --- read-only against the LIVE fleet ---------------------------------------------------

@pytest.mark.live_repo
def test_live_repo_loads_clean_and_writes_nothing():
    import subprocess
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dirty_before = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                                  capture_output=True, text=True).stdout
    fm = _loader().load_fleet_model(root)
    dirty_after = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                                 capture_output=True, text=True).stdout
    assert dirty_after == dirty_before  # zero files written
    members = _loader().resolve_fleet_members(fm.desired)
    assert set(members) == {".dev-knowledge", "ai-council", "corp-monorepo",
                            "corp-ops", "corp-sca-time-automation"}
    corp = next(r for r in fm.desired.repos if r.id == "corp-monorepo")
    assert corp.deployed.version == "1.2.0"
    assert any(d.kind == "gate-rev-ahead" and d.gate_tag_raw == "v1.3.1"
               for d in fm.desired.divergences)
    assert fm.observed.generated_raw is not None  # C8 stamp surfaced from the live rollup
