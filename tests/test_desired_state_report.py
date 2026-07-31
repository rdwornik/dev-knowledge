"""RED-first spec tests for the ADR-109 divergence report ([#382] W4).

Written and WITNESSED FAILING before scripts/desired_state_report.py exists. The
frozen W4 contract: surface × repo × {conform | diverge | declared} rendered from
the loaded FleetModel (pandas, analytics group); declared-divergence rows (waivers,
gate_rev_ahead, dispositions) render DECLARED never red; the terra-H5
matched/unmatched waiver join lands here; an HONEST LIMITS block rides IN the
report output; flat/fenced rendering (CLAUDE.md §4); read-only.

Verdict semantics pinned here (and stated in the report's own limits block):
"conform" = NO divergence is declared or observable in hub-side records for the
cell — it is NOT a live probe result; probe execution stays fleet_parity's.
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

pytest.importorskip("pandas")

import test_desired_state_loader as tl  # noqa: E402  (fixture source strings reused)


def _r():
    from scripts import desired_state_report
    return desired_state_report


def _loader():
    from scripts import desired_state_loader
    return desired_state_loader


@pytest.fixture
def fleet_dir(tmp_path):
    eco = tmp_path / "ecosystem"
    eco.mkdir()
    (eco / "registry.md").write_text(tl.REGISTRY_MD, encoding="utf-8")
    (eco / "deployed-versions.yaml").write_text(tl.DEPLOYED_VERSIONS, encoding="utf-8")
    (eco / "parity-surfaces.yaml").write_text(tl.PARITY_SURFACES, encoding="utf-8")
    (eco / "satellite-onboarding-rulings.yaml").write_text(tl.ONBOARDING_RULINGS, encoding="utf-8")
    (eco / "index.yaml").write_text(tl.INDEX_YAML, encoding="utf-8")
    (tmp_path / ".methodology.yaml").write_text(tl.METHODOLOGY_YAML, encoding="utf-8")
    deploy = tmp_path / "deploy"
    deploy.mkdir()
    (deploy / "manifest-v1.4.0.yaml").write_text(tl.MANIFEST_YAML, encoding="utf-8")
    return tmp_path


@pytest.fixture
def model(fleet_dir):
    return _loader().load_fleet_model(fleet_dir)


# --- frame shape ------------------------------------------------------------------------

def test_build_report_shape(model):
    df = _r().build_report(model)
    assert list(df.columns) == [".dev-knowledge", "ai-council", "corp-monorepo",
                                "corp-ops", "corp-sca-time-automation"]
    assert "journal-file" in df.index and "precommit-hub-block" in df.index
    assert "corpus-version" in df.index  # the derived G11 row
    assert set(df.values.ravel()) <= {"conform", "diverge", "declared", "·"}


# --- declared never renders red ---------------------------------------------------------

def test_gate_rev_ahead_renders_declared(model):
    df = _r().build_report(model)
    assert df.loc["precommit-hub-block", "corp-monorepo"] == "declared"


def test_repo_tier_override_renders_declared(model):
    # corp-monorepo carries a repo-keyed LOCAL override on journal-file — a per-repo
    # declared divergence at the tier level, never a red cell.
    df = _r().build_report(model)
    assert df.loc["journal-file", "corp-monorepo"] == "declared"
    assert df.loc["journal-file", ".dev-knowledge"] == "conform"


def test_waiver_join_lands_here(fleet_dir):
    """terra H5 (deferred to W4): a surface whose waiver_component matches a loaded
    parity-waiver declaration renders DECLARED on the register-owner column (hub —
    the only .methodology.yaml this repo can read)."""
    p = fleet_dir / "ecosystem" / "parity-surfaces.yaml"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "  - id: journal-file\n    kind: path\n",
        "  - id: journal-file\n    kind: path\n    waivable: true\n    waiver_component: ruff-gate\n"),
        encoding="utf-8")
    model = _loader().load_fleet_model(fleet_dir)
    df = _r().build_report(model)
    assert df.loc["journal-file", ".dev-knowledge"] == "declared"


def test_audit_disposition_renders_declared(model):
    """The third mechanism: an audit-disposition joined by the <surface>/<repo>
    concern grammar renders DECLARED (none load live yet — the register is not
    among the seven sources; the LOGIC is contract-bound now)."""
    m = __import__("ecosystem.schema.desired_state", fromlist=["x"])
    d = m.DeclaredDivergence(kind="audit-disposition", concern_id="journal-file/ai-council",
                             effect="suppress-warning", organ="fleet_parity",
                             provenance=m.Provenance(reason="test disposition"))
    desired = model.desired.model_copy(update={"divergences": model.desired.divergences + (d,)})
    patched = m.FleetModel(desired=desired, observed=model.observed)
    df = _r().build_report(patched)
    assert df.loc["journal-file", "ai-council"] == "declared"


# --- the derived corpus-version row (G11 computable) ------------------------------------

def test_corpus_version_row_verdicts(model):
    df = _r().build_report(model)
    row = df.loc["corpus-version"]
    assert row["ai-council"] == "diverge"        # 1.3.1 deployed vs declared target 1.4.0
    assert row["corp-monorepo"] == "declared"    # gate_rev_ahead sanctions the gap
    assert row["corp-ops"] == "diverge"          # ruled full, nothing deployed (C3), undeclared
    assert row[".dev-knowledge"] == "·"          # hub is the source — no corpus expectation


# --- rendering: flat, fenced, honest ----------------------------------------------------

def test_render_is_fenced_and_flat(model):
    out = _r().render_report(model)
    assert out.startswith("```") and out.rstrip().endswith("```")
    table_lines = [ln for ln in out.splitlines() if ln.startswith("|")]
    assert table_lines, "no table rendered"
    assert not any("  " in ln for ln in table_lines), "column padding found — must be flat"


def test_render_carries_honest_limits_and_staleness(model):
    out = _r().render_report(model)
    assert "HONEST LIMITS" in out
    assert "hub-side declarations" in out
    assert "fleet_parity" in out          # probe execution stays the checker's
    assert "2026-07-11T12:30:02" in out   # C8: the observed rollup's staleness stamp
    assert "disposition-register" in out  # not among the seven loaded sources — said so


def test_render_carries_summary_counts(model):
    out = _r().render_report(model)
    assert "declared:" in out and "diverge:" in out and "conform:" in out


# --- read-only --------------------------------------------------------------------------

def test_report_writes_nothing(fleet_dir, model):
    seven = ["ecosystem/registry.md", "ecosystem/index.yaml",
             "ecosystem/deployed-versions.yaml", "ecosystem/parity-surfaces.yaml",
             "ecosystem/satellite-onboarding-rulings.yaml", ".methodology.yaml",
             "deploy/manifest-v1.4.0.yaml"]
    before = {p: (fleet_dir / p).read_bytes() for p in seven}
    _r().render_report(model)
    for p in seven:
        assert (fleet_dir / p).read_bytes() == before[p]


@pytest.mark.live_repo
def test_live_report_renders_the_real_fleet():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    model = _loader().load_fleet_model(root)
    r = _r()
    df = r.build_report(model)
    assert list(df.columns) == [".dev-knowledge", "ai-council", "corp-monorepo",
                                "corp-ops", "corp-sca-time-automation"]
    assert len(df.index) >= 80  # the 81-surface set + the derived corpus row
    assert df.loc["precommit-hub-block", "corp-monorepo"] == "declared"
    out = r.render_report(model)
    assert out.startswith("```") and "HONEST LIMITS" in out
