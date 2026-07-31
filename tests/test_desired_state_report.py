"""Spec tests for the ADR-109 divergence report ([#382] W4).

RED-first per wave discipline; POST-FREEZE AMENDMENTS recorded (terra W4 review,
docs/audits/2026-07-31-codex-382-w4-report.md, 6 High — all accepted):
- H1: "conform" redefined honestly as no-divergence-DECLARED (the declaration
  layer); the "observable in hub-side records" clause was vacuous — no reliable
  surface⇄finding join exists until the G9 crosswalk populates (#383-era).
- H2: the corpus row consults the RULING — null deployment is the C3 diverge only
  under a desired-full assertion; otherwise the cell is n/a.
- H3: gate declarations self-invalidate — deployed source_tag reaching gate_tag_raw
  drops the DECLARED and the cell falls through to the target comparison.
- H4: a repo-keyed tier override is DECLARED only when it DIFFERS from the resolved
  role posture; an equal or baseline-less repo rule is just the posture.
- H5: verdict semantics are pandas-free (`build_matrix`); only the DataFrame
  integration legs gate on pandas, so a dev-group run still collects the contract.
- H6: the negative/precedence matrix below.
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

import test_desired_state_loader as tl  # noqa: E402  (fixture source strings reused)

MEMBERS = [".dev-knowledge", "ai-council", "corp-monorepo", "corp-ops",
           "corp-sca-time-automation"]


def _r():
    from scripts import desired_state_report
    return desired_state_report


def _loader():
    from scripts import desired_state_loader
    return desired_state_loader


def _write_fleet(tmp_path, deployed=None, parity=None, rulings=None):
    eco = tmp_path / "ecosystem"
    eco.mkdir()
    (eco / "registry.md").write_text(tl.REGISTRY_MD, encoding="utf-8")
    (eco / "deployed-versions.yaml").write_text(deployed or tl.DEPLOYED_VERSIONS, encoding="utf-8")
    (eco / "parity-surfaces.yaml").write_text(parity or tl.PARITY_SURFACES, encoding="utf-8")
    (eco / "satellite-onboarding-rulings.yaml").write_text(rulings or tl.ONBOARDING_RULINGS,
                                                           encoding="utf-8")
    (eco / "index.yaml").write_text(tl.INDEX_YAML, encoding="utf-8")
    (tmp_path / ".methodology.yaml").write_text(tl.METHODOLOGY_YAML, encoding="utf-8")
    deploy = tmp_path / "deploy"
    deploy.mkdir()
    (deploy / "manifest-v1.4.0.yaml").write_text(tl.MANIFEST_YAML, encoding="utf-8")
    return tmp_path


@pytest.fixture
def fleet_dir(tmp_path):
    return _write_fleet(tmp_path)


@pytest.fixture
def model(fleet_dir):
    return _loader().load_fleet_model(fleet_dir)


# --- matrix semantics (pandas-free — terra H5) ------------------------------------------

def test_build_matrix_shape_and_vocabulary(model):
    mx = _r().build_matrix(model)
    assert "journal-file" in mx and "precommit-hub-block" in mx and "corpus-version" in mx
    for row in mx.values():
        assert list(row) == MEMBERS
        assert set(row.values()) <= {"conform", "diverge", "declared", "·"}


def test_gate_rev_ahead_renders_declared(model):
    assert _r().build_matrix(model)["precommit-hub-block"]["corp-monorepo"] == "declared"


def test_differing_repo_override_is_declared_equal_is_not(fleet_dir):
    # corp's LOCAL differs from the consumer MUST → declared (a real departure);
    # an override EQUAL to the role posture is not a departure (terra H4).
    p = fleet_dir / "ecosystem" / "parity-surfaces.yaml"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "tier: {hub: MUST, consumer: MUST, corp-monorepo: LOCAL}",
        "tier: {hub: MUST, consumer: MUST, corp-monorepo: LOCAL, ai-council: MUST}"),
        encoding="utf-8")
    mx = _r().build_matrix(_loader().load_fleet_model(fleet_dir))
    assert mx["journal-file"]["corp-monorepo"] == "declared"
    assert mx["journal-file"]["ai-council"] == "conform"  # equal override — no departure
    assert mx["journal-file"][".dev-knowledge"] == "conform"


def test_repo_only_tier_is_posture_not_departure(fleet_dir):
    """terra H4: a surface keyed ONLY by repo id has no role baseline — its rule IS
    the applicability, never a declared departure."""
    p = fleet_dir / "ecosystem" / "parity-surfaces.yaml"
    p.write_text(p.read_text(encoding="utf-8") + """
  - id: corp-local-surface
    kind: path
    tier: {corp-monorepo: MUST}
    probe: {type: path_tracked, path: X.md}
    ownership:
      value: project
      reason: corp-only surface
      provenance:
        - {kind: backlog, repo: .dev-knowledge, ref: "#1"}
""", encoding="utf-8")
    mx = _r().build_matrix(_loader().load_fleet_model(fleet_dir))
    assert mx["corp-local-surface"]["corp-monorepo"] == "conform"
    assert mx["corp-local-surface"]["ai-council"] == "·"


def test_waiver_join_declares_hub_column_only(fleet_dir):
    """terra H5 (W3-deferred) + H6: matched waiver declares the register-owner (hub)
    column; consumer columns are untouched (their registers are unreadable here)."""
    p = fleet_dir / "ecosystem" / "parity-surfaces.yaml"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "  - id: journal-file\n    kind: path\n",
        "  - id: journal-file\n    kind: path\n    waivable: true\n    waiver_component: ruff-gate\n"),
        encoding="utf-8")
    mx = _r().build_matrix(_loader().load_fleet_model(fleet_dir))
    assert mx["journal-file"][".dev-knowledge"] == "declared"
    assert mx["journal-file"]["ai-council"] == "conform"


def test_audit_disposition_renders_declared(model):
    m = __import__("ecosystem.schema.desired_state", fromlist=["x"])
    d = m.DeclaredDivergence(kind="audit-disposition", concern_id="journal-file/ai-council",
                             effect="suppress-warning", organ="fleet_parity",
                             provenance=m.Provenance(reason="test disposition"))
    desired = model.desired.model_copy(update={"divergences": model.desired.divergences + (d,)})
    patched = m.FleetModel(desired=desired, observed=model.observed)
    assert _r().build_matrix(patched)["journal-file"]["ai-council"] == "declared"


# --- the corpus-version row (G11/C3; terra H2/H3) ---------------------------------------

def test_corpus_version_row_verdicts(model):
    row = _r().build_matrix(model)["corpus-version"]
    assert row["ai-council"] == "diverge"        # 1.3.1 vs declared target 1.4.0, undeclared
    assert row["corp-monorepo"] == "declared"    # gate v1.3.1 NOT yet reached (deployed v1.2.0)
    assert row["corp-ops"] == "diverge"          # ruled full + nothing deployed = the C3 gap
    assert row[".dev-knowledge"] == "·"          # the hub IS the source


def test_null_deployment_without_full_ruling_is_not_c3(tmp_path):
    """terra H2: null deployment diverges ONLY under a desired-full ruling."""
    rulings = tl.ONBOARDING_RULINGS.replace("""  corp-sca-time-automation:
    profile: full
    ruled_by: operator
    ruled_date: "2026-07-16"
    census_ref: docs/audits/2026-07-16-census.md
""", "")
    model = _loader().load_fleet_model(_write_fleet(tmp_path, rulings=rulings))
    row = _r().build_matrix(model)["corpus-version"]
    assert row["corp-sca-time-automation"] == "·"  # no ruling, no corpus expectation recorded
    assert row["corp-ops"] == "diverge"            # its full ruling remains — still C3


def test_gate_declaration_self_invalidates_on_reaching_tag(tmp_path):
    """terra H3: deployed source_tag reaching gate_tag_raw drops the DECLARED; the
    cell falls through to the target comparison (still behind 1.4.0 → diverge)."""
    deployed = tl.DEPLOYED_VERSIONS.replace(
        'deployed_methodology_version: "1.2.0"', 'deployed_methodology_version: "1.3.1"'
    ).replace('deployed_date: "2026-07-07"\n    source_tag: "v1.2.0"',
              'deployed_date: "2026-07-30"\n    source_tag: "v1.3.1"')
    model = _loader().load_fleet_model(_write_fleet(tmp_path, deployed=deployed))
    row = _r().build_matrix(model)["corpus-version"]
    assert row["corp-monorepo"] == "diverge"  # declaration self-invalidated, gap undeclared


def test_corpus_equality_is_conform(tmp_path):
    deployed = tl.DEPLOYED_VERSIONS.replace(
        'deployed_methodology_version: "1.3.1"', 'deployed_methodology_version: "1.4.0"'
    ).replace('source_tag: "v1.3.1"', 'source_tag: "v1.4.0"')
    model = _loader().load_fleet_model(_write_fleet(tmp_path, deployed=deployed))
    assert _r().build_matrix(model)["corpus-version"]["ai-council"] == "conform"


# --- rendering: flat, fenced, honest ----------------------------------------------------

def test_render_is_fenced_and_flat(model):
    out = _r().render_report(model)
    assert out.startswith("```") and out.rstrip().endswith("```")
    table_lines = [ln for ln in out.splitlines() if ln.startswith("|")]
    assert table_lines and not any("  " in ln for ln in table_lines)


def test_render_carries_honest_limits_and_staleness(model):
    out = _r().render_report(model)
    assert "HONEST LIMITS" in out
    assert "hub-side declarations" in out
    assert "fleet_parity" in out
    assert "2026-07-11T12:30:02" in out
    assert "disposition-register" in out
    assert "G9" in out  # H1: the observational join awaits the crosswalk — said so


def test_render_carries_summary_counts(model):
    out = _r().render_report(model)
    assert "declared:" in out and "diverge:" in out and "conform:" in out


# --- read-only (terra H6: whole-tree, incl. no NEW files) -------------------------------

def test_report_touches_no_file_and_creates_none(fleet_dir, model):
    def snapshot():
        return {str(p): p.read_bytes() for p in fleet_dir.rglob("*") if p.is_file()}
    before = snapshot()
    _r().render_report(model)
    assert snapshot() == before


# --- pandas integration (analytics group; the only pandas-gated legs — terra H5) --------

def test_build_report_dataframe(model):
    pd = pytest.importorskip("pandas")
    df = _r().build_report(model)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == MEMBERS
    assert df.loc["precommit-hub-block", "corp-monorepo"] == "declared"


@pytest.mark.live_repo
def test_live_report_renders_the_real_fleet():
    pytest.importorskip("pandas")
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    model = _loader().load_fleet_model(root)
    r = _r()
    df = r.build_report(model)
    assert list(df.columns) == MEMBERS
    assert len(df.index) >= 80
    assert df.loc["precommit-hub-block", "corp-monorepo"] == "declared"
    out = r.render_report(model)
    assert out.startswith("```") and "HONEST LIMITS" in out
