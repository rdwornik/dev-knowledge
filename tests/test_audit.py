"""Tests for scripts/audit.py — schema roundtrip, check execution, report generation."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import os
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest

import audit as aud

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

GOOD_VISION = """\
---
version: "1.0"
last_reviewed: 2026-05-23
owner: robdwornik@gmail.com
status: active
---

# Vision

<!-- scope: meta -->

Body text.
"""

VISION_NO_FRONTMATTER = "# Vision\n\nNo frontmatter.\n"

VISION_MISSING_KEYS = """\
---
version: "1.0"
---

# Vision
"""

VISION_BAD_YAML = """\
---
key: [unclosed
---

# Vision
"""


@pytest.fixture()
def good_repo(tmp_path: Path) -> Path:
    """Repo satisfying the ADR-38 A5 universal governance baseline.

    Baseline files: VISION.md, ARCHITECTURE.md, BACKLOG.md, CLAUDE.md. src/,
    tests/, pyproject.toml, README.md, CHANGELOG.md are kept here only to prove
    they are NOT required by check_adr38_baseline post-amendment.
    """
    (tmp_path / "src" / "my_pkg").mkdir(parents=True)
    (tmp_path / "src" / "my_pkg" / "__init__.py").write_text("")
    (tmp_path / "tests").mkdir()
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'my_pkg'\nversion = '0.1'\n")
    (tmp_path / "README.md").write_text("# Readme\n")
    (tmp_path / "VISION.md").write_text(GOOD_VISION)
    (tmp_path / "ARCHITECTURE.md").write_text("# Architecture\n")
    (tmp_path / "CHANGELOG.md").write_text("# Changelog\n")
    (tmp_path / "BACKLOG.md").write_text("# Backlog\n")
    (tmp_path / "CLAUDE.md").write_text("# Claude\n\nInstructions.\n")
    return tmp_path


@pytest.fixture()
def bad_repo(tmp_path: Path) -> Path:
    """Repo missing most required files."""
    (tmp_path / "README.md").write_text("# Readme\n")
    return tmp_path


# ---------------------------------------------------------------------------
# Schema roundtrip
# ---------------------------------------------------------------------------

def test_repo_state_roundtrip(tmp_path: Path) -> None:
    """RepoState serializes to dict and deserializes back cleanly."""
    original = aud.RepoState(
        name="test-repo",
        path="/some/path",
        last_audit="2026-05-15",
        findings=[
            aud.Finding("check_a", "pass", "all good"),
            aud.Finding("check_b", "fail", "missing file"),
        ],
    )
    d = original.to_dict()
    restored = aud.RepoState.from_dict(d)
    assert restored.name == original.name
    assert restored.path == original.path
    assert restored.last_audit == original.last_audit
    assert len(restored.findings) == 2
    assert restored.findings[0].check_name == "check_a"
    assert restored.findings[1].status == "fail"


def test_save_load_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """save_state writes YAML; load_state reads it back cleanly."""
    monkeypatch.setattr(aud, "ECOSYSTEM_DIR", tmp_path / "ecosystem")
    state = aud.RepoState(
        name="my-repo",
        path="../my-repo",
        last_audit="2026-05-15",
        findings=[aud.Finding("vision_md", "pass", "ok")],
    )
    aud.save_state(state)
    loaded = aud.load_state("my-repo")
    assert loaded is not None
    assert loaded.name == "my-repo"
    assert loaded.findings[0].status == "pass"


def test_append_history(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """append_history creates the history file and writes a markdown table."""
    monkeypatch.setattr(aud, "ECOSYSTEM_DIR", tmp_path / "ecosystem")
    state = aud.RepoState(
        name="my-repo",
        path="../my-repo",
        last_audit="2026-05-15",
        findings=[aud.Finding("claude_md", "fail", "absent")],
    )
    run_date = date(2026, 5, 15)
    aud.append_history(state, run_date)
    hist = (tmp_path / "ecosystem" / "my-repo" / "history" / "2026-05-15.md")
    assert hist.exists()
    content = hist.read_text(encoding="utf-8")
    assert "claude_md" in content
    assert "fail" in content

# ---------------------------------------------------------------------------
# Check #1: VISION.md
# ---------------------------------------------------------------------------

def test_vision_pass(good_repo: Path) -> None:
    f = aud.check_vision_md(good_repo)[0]
    assert f.status == "pass"


def test_vision_absent(tmp_path: Path) -> None:
    f = aud.check_vision_md(tmp_path)[0]
    assert f.status == "fail"
    assert "absent" in f.evidence


def test_vision_no_frontmatter(tmp_path: Path) -> None:
    (tmp_path / "VISION.md").write_text(VISION_NO_FRONTMATTER)
    f = aud.check_vision_md(tmp_path)[0]
    assert f.status == "fail"
    assert "frontmatter" in f.evidence.lower()


def test_vision_missing_keys(tmp_path: Path) -> None:
    (tmp_path / "VISION.md").write_text(VISION_MISSING_KEYS)
    f = aud.check_vision_md(tmp_path)[0]
    assert f.status == "warn"
    assert "missing keys" in f.evidence.lower()


def test_vision_bad_yaml(tmp_path: Path) -> None:
    (tmp_path / "VISION.md").write_text(VISION_BAD_YAML)
    f = aud.check_vision_md(tmp_path)[0]
    assert f.status == "fail"
    assert "parse error" in f.evidence.lower()

# ---------------------------------------------------------------------------
# Check #2: ADR-38 baseline
# ---------------------------------------------------------------------------

def test_adr38_pass(good_repo: Path) -> None:
    f = aud.check_adr38_baseline(good_repo)[0]
    assert f.status == "pass"


def test_adr38_readme_optional(good_repo: Path) -> None:
    """README.md is optional post-amendment (A5) — its absence does not fail the check."""
    (good_repo / "README.md").unlink()
    f = aud.check_adr38_baseline(good_repo)[0]
    assert f.status == "pass"


def test_adr38_missing_architecture(good_repo: Path) -> None:
    """ARCHITECTURE.md is universally mandatory post-amendment (A5)."""
    (good_repo / "ARCHITECTURE.md").unlink()
    f = aud.check_adr38_baseline(good_repo)[0]
    assert f.status == "fail"
    assert "ARCHITECTURE.md" in f.evidence


def test_adr38_missing_backlog(good_repo: Path) -> None:
    (good_repo / "BACKLOG.md").unlink()
    f = aud.check_adr38_baseline(good_repo)[0]
    assert f.status == "fail"
    assert "BACKLOG.md" in f.evidence


def test_adr38_code_structure_not_required(good_repo: Path) -> None:
    """src/, tests/, pyproject.toml are NOT part of the governance baseline (A5).

    A governance-only repo with no code layout still passes if it carries the
    mandatory governance docs.
    """
    import shutil
    shutil.rmtree(good_repo / "src")
    shutil.rmtree(good_repo / "tests")
    (good_repo / "pyproject.toml").unlink()
    f = aud.check_adr38_baseline(good_repo)[0]
    assert f.status == "pass"


def test_adr38_bad_repo(bad_repo: Path) -> None:
    """Repo with only README.md fails — missing VISION/ARCHITECTURE/BACKLOG."""
    f = aud.check_adr38_baseline(bad_repo)[0]
    assert f.status == "fail"


def test_adr38_no_lessons_or_journal_checked(good_repo: Path) -> None:
    """LESSONS.md and JOURNAL.md are repo-specific — NOT checked by ADR-38 baseline."""
    # Neither file exists in good_repo; check must still pass
    assert not (good_repo / "LESSONS.md").exists()
    assert not (good_repo / "JOURNAL.md").exists()
    f = aud.check_adr38_baseline(good_repo)[0]
    assert f.status == "pass", (
        f"ADR-38 check must not require LESSONS.md/JOURNAL.md; got: {f.evidence}"
    )

# ---------------------------------------------------------------------------
# Check #3: CLAUDE.md
# ---------------------------------------------------------------------------

def test_claude_md_pass(good_repo: Path) -> None:
    f = aud.check_claude_md(good_repo)[0]
    assert f.status == "pass"


def test_claude_md_absent(tmp_path: Path) -> None:
    f = aud.check_claude_md(tmp_path)[0]
    assert f.status == "fail"
    assert "absent" in f.evidence


def test_claude_md_empty(tmp_path: Path) -> None:
    (tmp_path / "CLAUDE.md").write_text("   \n")
    f = aud.check_claude_md(tmp_path)[0]
    assert f.status == "fail"
    assert "empty" in f.evidence

# ---------------------------------------------------------------------------
# Check #4: dot_prefix_discipline (ADR-59 D1)
# ---------------------------------------------------------------------------

def test_dot_prefix_pass_dotted_and_exceptions(tmp_path: Path) -> None:
    (tmp_path / ".ruff.toml").write_text("")
    (tmp_path / ".pre-commit-config.yaml").write_text("")
    (tmp_path / "pyproject.toml").write_text("")   # exception
    (tmp_path / "tach.toml").write_text("")         # exception (verified 2026-05-27)
    (tmp_path / "pytest.ini").write_text("")        # exception (pytest won't read .pytest.ini)
    f = aud.check_dot_prefix_discipline(tmp_path)[0]
    assert f.status == "pass"


def test_dot_prefix_pytest_ini_is_exempt(tmp_path: Path) -> None:
    # pytest.ini cannot be dot-prefixed (pytest does not read .pytest.ini), so it
    # joins the ADR-59 exception list (amendment 2026-06-02) like pyproject.toml.
    (tmp_path / "pytest.ini").write_text("[pytest]\n")
    f = aud.check_dot_prefix_discipline(tmp_path)[0]
    assert f.status == "pass"


def test_dot_prefix_fail_undotted(tmp_path: Path) -> None:
    (tmp_path / "ruff.toml").write_text("")  # should be .ruff.toml
    f = aud.check_dot_prefix_discipline(tmp_path)[0]
    assert f.status == "fail"
    assert "ruff.toml" in f.evidence


def test_dot_prefix_ignores_subfolders(tmp_path: Path) -> None:
    sub = tmp_path / "config"
    sub.mkdir()
    (sub / "settings.toml").write_text("")  # subfolder config — not a root concern
    f = aud.check_dot_prefix_discipline(tmp_path)[0]
    assert f.status == "pass"

# ---------------------------------------------------------------------------
# Check #5: canonical_md_visibility (ADR-59 D2)
# ---------------------------------------------------------------------------

def _make_canonical(tmp_path: Path) -> None:
    for name in ("VISION.md", "ARCHITECTURE.md", "CLAUDE.md", "BACKLOG.md"):
        (tmp_path / name).write_text("x")


def test_canonical_md_pass(tmp_path: Path) -> None:
    _make_canonical(tmp_path)
    f = aud.check_canonical_md_visibility(tmp_path)[0]
    assert f.status == "pass"


def test_canonical_md_optional_absent_still_pass(tmp_path: Path) -> None:
    """LESSONS/JOURNAL/CONTRIBUTING are NOT required — absence must not fail."""
    _make_canonical(tmp_path)
    assert not (tmp_path / "LESSONS.md").exists()
    f = aud.check_canonical_md_visibility(tmp_path)[0]
    assert f.status == "pass"


def test_canonical_md_missing_mandatory(tmp_path: Path) -> None:
    _make_canonical(tmp_path)
    (tmp_path / "VISION.md").unlink()
    f = aud.check_canonical_md_visibility(tmp_path)[0]
    assert f.status == "fail"
    assert "VISION.md" in f.evidence


def test_canonical_md_miscased(tmp_path: Path) -> None:
    _make_canonical(tmp_path)
    (tmp_path / "Lessons.md").write_text("x")  # should be LESSONS.md
    f = aud.check_canonical_md_visibility(tmp_path)[0]
    assert f.status == "fail"
    assert "Lessons.md" in f.evidence

# ---------------------------------------------------------------------------
# Check #6: workspace_settings (ADR-59 D3)
# ---------------------------------------------------------------------------

GOOD_WS = """\
{
  // a comment VS Code tolerates
  "folders": [{ "path": "." }],
  "settings": {
    "explorer.sortOrder": "default",
    "explorer.sortOrderLexicographicOptions": "upper",
  },
}"""


def test_workspace_settings_pass(tmp_path: Path) -> None:
    (tmp_path / ".my-repo.code-workspace").write_text(GOOD_WS)
    f = aud.check_workspace_settings(tmp_path)[0]
    assert f.status == "pass"


def test_workspace_settings_absent(tmp_path: Path) -> None:
    f = aud.check_workspace_settings(tmp_path)[0]
    assert f.status == "fail"
    assert "No .code-workspace" in f.evidence


def test_workspace_settings_wrong_value_warns(tmp_path: Path) -> None:
    bad = GOOD_WS.replace('"upper"', '"default"')
    (tmp_path / ".my-repo.code-workspace").write_text(bad)
    f = aud.check_workspace_settings(tmp_path)[0]
    assert f.status == "warn"
    assert "sortOrderLexicographicOptions" in f.evidence


def test_workspace_settings_not_dotted_warns(tmp_path: Path) -> None:
    (tmp_path / "my-repo.code-workspace").write_text(GOOD_WS)  # missing leading dot
    f = aud.check_workspace_settings(tmp_path)[0]
    assert f.status == "warn"
    assert "dot-prefix" in f.evidence


def test_workspace_settings_malformed_fails(tmp_path: Path) -> None:
    (tmp_path / ".x.code-workspace").write_text("{ not json ]")
    f = aud.check_workspace_settings(tmp_path)[0]
    assert f.status == "fail"


def test_strip_jsonc_preserves_string_slashes() -> None:
    """// inside a string value must survive; comments outside must be stripped."""
    src = '{ "url": "http://x//y", "a": 1 /* c */ }'
    assert json.loads(aud._strip_jsonc(src)) == {"url": "http://x//y", "a": 1}

# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def test_report_contains_scope_tag() -> None:
    """Report must include <!-- scope: meta --> for scope-tag validator."""
    state = aud.RepoState("test", "/path", "2026-05-15", [
        aud.Finding("vision_md", "pass", "ok")
    ])
    report = aud.generate_report([state], date(2026, 5, 15), Path("/repo"))
    assert "<!-- scope: meta -->" in report


def test_report_contains_repo_name() -> None:
    state = aud.RepoState("my-special-repo", "/path", "2026-05-15", [
        aud.Finding("vision_md", "fail", "missing")
    ])
    report = aud.generate_report([state], date(2026, 5, 15), Path("/repo"))
    assert "my-special-repo" in report


def test_report_aggregate_counts() -> None:
    states = [
        aud.RepoState("repo-a", "/a", "2026-05-15", [
            aud.Finding("vision_md", "pass", "ok"),
            aud.Finding("claude_md", "fail", "absent"),
        ]),
        aud.RepoState("repo-b", "/b", "2026-05-15", [
            aud.Finding("vision_md", "pass", "ok"),
        ]),
    ]
    report = aud.generate_report(states, date(2026, 5, 15), Path("/repo"))
    assert "2 repo(s)" in report
    assert "2 pass" in report
    assert "1 fail" in report


def test_write_report_ecosystem(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(aud, "AUDITS_DIR", tmp_path / "audits")
    content = "# Test Report\n<!-- scope: meta -->\n"
    out = aud.write_report(content, date(2026, 5, 15))
    assert out.name == "2026-05-15-ecosystem-audit.md"
    assert out.read_text(encoding="utf-8") == content


def test_write_report_single_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(aud, "AUDITS_DIR", tmp_path / "audits")
    content = "# Test Report\n"
    out = aud.write_report(content, date(2026, 5, 15), single_repo="ai-council")
    assert out.name == "2026-05-15-ai-council-audit.md"


def test_write_report_overwrites_same_day(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Same-day re-run overwrites the report (no collision suffix)."""
    monkeypatch.setattr(aud, "AUDITS_DIR", tmp_path / "audits")
    aud.write_report("first run\n", date(2026, 5, 15))
    aud.write_report("second run\n", date(2026, 5, 15))
    out = tmp_path / "audits" / "2026-05-15-ecosystem-audit.md"
    assert out.read_text(encoding="utf-8") == "second run\n"

# ---------------------------------------------------------------------------
# audit_repo integration
# ---------------------------------------------------------------------------

def test_audit_repo_unavailable(tmp_path: Path) -> None:
    state = aud.audit_repo("ghost", tmp_path / "nonexistent", date(2026, 5, 15))
    assert any(f.status == "unavailable" for f in state.findings)


def test_audit_repo_good(good_repo: Path) -> None:
    state = aud.audit_repo("good-repo", good_repo, date(2026, 5, 15))
    statuses = {f.check_name: f.status for f in state.findings}
    assert statuses.get("vision_md") == "pass"
    assert statuses.get("claude_md") == "pass"
    # adr38 governance baseline: good_repo carries VISION/ARCHITECTURE/BACKLOG
    assert statuses.get("adr38_baseline") == "pass"

# ---------------------------------------------------------------------------
# health command (CLI)
# ---------------------------------------------------------------------------

def test_health_degraded_no_ecosystem(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """health exits 1 when ecosystem/ does not exist."""
    from click.testing import CliRunner
    monkeypatch.setattr(aud, "ECOSYSTEM_DIR", tmp_path / "nonexistent")
    runner = CliRunner()
    result = runner.invoke(aud.cmd_health)
    assert result.exit_code == 1
    assert "DEGRADED" in result.output


def test_health_ok_with_registered_repo(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """health exits 0 when ecosystem/ exists and at least one repo is registered."""
    eco = tmp_path / "ecosystem" / "test-repo"
    eco.mkdir(parents=True)
    state_yaml = eco / "state.yaml"
    state_yaml.write_text("name: test-repo\npath: /tmp/test\nlast_audit: null\nfindings: []\n")
    monkeypatch.setattr(aud, "ECOSYSTEM_DIR", tmp_path / "ecosystem")
    from click.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(aud.cmd_health)
    assert result.exit_code == 0
    assert "OK" in result.output


# ---------------------------------------------------------------------------
# Fixtures path helper
# ---------------------------------------------------------------------------

FIXTURES = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# Integration: structural checks on synthetic full-fixture repo
# ---------------------------------------------------------------------------

FULL_FIXTURE = FIXTURES / "repo-with-structural-checks"


def test_audit_run_passes_structural_checks_on_synthetic_repo() -> None:
    """The 3 structural checks (vision/adr38/claude) must pass on synthetic repo."""
    run_date = date(2026, 5, 15)
    state = aud.audit_repo("synthetic", FULL_FIXTURE, run_date)
    check_names = {f.check_name for f in state.findings}
    statuses = {f.check_name: f.status for f in state.findings}

    assert "vision_md" in check_names
    assert "adr38_baseline" in check_names
    assert "claude_md" in check_names

    failures = [f for f in state.findings if f.status == "fail"]
    assert not failures, f"Unexpected failures: {[(f.check_name, f.evidence) for f in failures]}"

    assert statuses.get("vision_md") == "pass"
    assert statuses.get("claude_md") == "pass"
    assert statuses.get("adr38_baseline") in ("pass", "warn")

# ---------------------------------------------------------------------------
# Check #7: mermaid_theme_directive (ADR-51 v2)
# ---------------------------------------------------------------------------

MERMAID_PASS_FIXTURE = FIXTURES / "mermaid-theme-pass"
MERMAID_FAIL_FIXTURE = FIXTURES / "mermaid-theme-fail"


def test_mermaid_theme_directive_pass() -> None:
    """ARCHITECTURE.md with correct base+themeVariables + classDef color: must pass."""
    findings = aud.check_mermaid_theme_directive(MERMAID_PASS_FIXTURE)
    assert len(findings) == 1
    f = findings[0]
    assert f.status == "pass", f"Expected pass, got {f.status}: {f.evidence}"


def test_mermaid_theme_directive_fail_bare_dark() -> None:
    """ARCHITECTURE.md with bare 'dark' theme must fail rule 1."""
    findings = aud.check_mermaid_theme_directive(MERMAID_FAIL_FIXTURE)
    assert len(findings) == 1
    f = findings[0]
    assert f.status == "fail", f"Expected fail, got {f.status}: {f.evidence}"
    assert "base+themeVariables" in f.evidence


def test_mermaid_theme_directive_fail_classdef_missing_color() -> None:
    """classDef with fill:# but no color:# must be reported in the failure evidence."""
    findings = aud.check_mermaid_theme_directive(MERMAID_FAIL_FIXTURE)
    f = findings[0]
    assert f.status == "fail"
    assert "color:#" in f.evidence or "classDef" in f.evidence


def test_mermaid_theme_directive_no_architecture_md(tmp_path: Path) -> None:
    """Repo with no ARCHITECTURE.md passes vacuously (nothing to scan)."""
    findings = aud.check_mermaid_theme_directive(tmp_path)
    assert findings[0].status == "pass"


def test_mermaid_theme_directive_no_mermaid_blocks(tmp_path: Path) -> None:
    """ARCHITECTURE.md with no mermaid fences passes vacuously."""
    (tmp_path / "ARCHITECTURE.md").write_text("# Architecture\n\nNo diagrams here.\n")
    findings = aud.check_mermaid_theme_directive(tmp_path)
    assert findings[0].status == "pass"

# ---------------------------------------------------------------------------
# Check #8: handoff_bundle_structure (HANDOFF_PROCESS v4.3 item F)
# ---------------------------------------------------------------------------

_BUNDLE_OPTIONAL = ("01_ROLE.md", "02_METHODOLOGY.md", "03_PROJECT.md",
                    "05_NOW.md", "06_QUESTIONS.md", "07_ASK_BACK.md")


def _write_bundle(handoffs: Path, name: str, *, version: str = "4.3",
                  four_tag: bool = True, drift_section: bool = True,
                  load_bearing: bool = True, omit: tuple = (),
                  oversize: str | None = None) -> Path:
    """Build a minimal valid v4 handoff bundle, perturbable for failing fixtures."""
    d = handoffs / name
    d.mkdir(parents=True)

    readme = f"# Handoff — {name}\n\n**Generated by HANDOFF_PROCESS v{version} (status: beta)**\n\n"
    if drift_section:
        readme += "## Drift cross-check\n\nNo drift detected.\n"
    (d / "README.md").write_text(readme, encoding="utf-8")

    recent = "# 04 · What just happened\n\n## The arc\n\nNarrative.\n"
    if four_tag:
        recent += "\n## Four-tag discipline (canonical)\n\nwitnessed/recall/inferred/unknown\n"
    if load_bearing:
        recent += "\n## Load-bearing facts (cross-checked vs repo at Phase 2)\n\ntable\n"
    (d / "04_RECENT.md").write_text(recent, encoding="utf-8")

    for fname in _BUNDLE_OPTIONAL:
        (d / fname).write_text(f"# {fname}\n\ncontent\n", encoding="utf-8")

    if oversize:
        budget = aud._BUNDLE_BUDGETS[oversize]
        (d / oversize).write_text("\n".join(f"line {i}" for i in range(budget + 5)),
                                  encoding="utf-8")
    for fname in omit:
        (d / fname).unlink()
    return d


def test_handoff_bundle_pass(tmp_path: Path) -> None:
    """A complete, in-budget, stamped v4.3 bundle passes."""
    _write_bundle(tmp_path / "docs" / "handoffs", "2026-06-01-x-session")
    f = aud.check_handoff_bundle_structure(tmp_path)[0]
    assert f.status == "pass", f.evidence


def test_handoff_bundle_three_segment_stamp_validated(tmp_path: Path) -> None:
    """A patch-version stamp (v4.3.1) is detected + validated, not silently skipped.

    Regression for the 2026-05-31 finding: the stamp regex matched only two-segment
    versions, so v4.3.1 bundles were skipped (counted as 0 stamped) rather than
    validated. The four-tag section must still be required (4.3.1 >= 4.3).
    """
    _write_bundle(tmp_path / "docs" / "handoffs", "2026-06-01-x-session",
                  version="4.3.1")
    f = aud.check_handoff_bundle_structure(tmp_path)[0]
    assert f.status == "pass", f.evidence
    assert "1 stamped" in f.evidence


def test_handoff_bundle_three_segment_still_enforces_v43_rules(tmp_path: Path) -> None:
    """v4.3.1 is treated as v4.3+ — the four-tag section is required, not optional."""
    _write_bundle(tmp_path / "docs" / "handoffs", "2026-06-01-x-session",
                  version="4.3.1", four_tag=False)
    f = aud.check_handoff_bundle_structure(tmp_path)[0]
    assert f.status == "fail"
    assert "Four-tag" in f.evidence


def test_handoff_bundle_no_handoffs_dir(tmp_path: Path) -> None:
    """No docs/handoffs/ → vacuous pass (check is .dev-knowledge-specific)."""
    f = aud.check_handoff_bundle_structure(tmp_path)[0]
    assert f.status == "pass"


def test_handoff_bundle_skips_unstamped(tmp_path: Path) -> None:
    """A bundle with no v4 stamp (v3.x sync / pre-stamp v4.1) is out of scope."""
    d = tmp_path / "docs" / "handoffs" / "old-v3x"
    d.mkdir(parents=True)
    (d / "README.md").write_text("# old bundle — no v4 stamp\n", encoding="utf-8")
    (d / "00_README.md").write_text("x", encoding="utf-8")
    f = aud.check_handoff_bundle_structure(tmp_path)[0]
    assert f.status == "pass"
    assert "0 stamped" in f.evidence


def test_handoff_bundle_excludes_aborted_inprogress(tmp_path: Path) -> None:
    """aborted/ and in-progress/ are excluded even if they contain stamped files."""
    h = tmp_path / "docs" / "handoffs"
    for excluded in ("aborted", "in-progress"):
        _write_bundle(h, excluded, omit=("07_ASK_BACK.md",))  # would fail if scanned
    f = aud.check_handoff_bundle_structure(tmp_path)[0]
    assert f.status == "pass", f.evidence


def test_handoff_bundle_missing_file(tmp_path: Path) -> None:
    _write_bundle(tmp_path / "docs" / "handoffs", "b", omit=("07_ASK_BACK.md",))
    f = aud.check_handoff_bundle_structure(tmp_path)[0]
    assert f.status == "fail"
    assert "07_ASK_BACK.md" in f.evidence


def test_handoff_bundle_missing_four_tag_v43_fails(tmp_path: Path) -> None:
    """v4.3 bundle missing the four-tag section fails (v4.3+ requirement)."""
    _write_bundle(tmp_path / "docs" / "handoffs", "b", version="4.3", four_tag=False)
    f = aud.check_handoff_bundle_structure(tmp_path)[0]
    assert f.status == "fail"
    assert "Four-tag" in f.evidence


def test_handoff_bundle_v42_four_tag_not_required(tmp_path: Path) -> None:
    """v4.2 bundle without the four-tag section still passes (requirement is v4.3+)."""
    _write_bundle(tmp_path / "docs" / "handoffs", "b", version="4.2", four_tag=False)
    f = aud.check_handoff_bundle_structure(tmp_path)[0]
    assert f.status == "pass", f.evidence


def test_handoff_bundle_over_budget_fails(tmp_path: Path) -> None:
    _write_bundle(tmp_path / "docs" / "handoffs", "b", oversize="06_QUESTIONS.md")
    f = aud.check_handoff_bundle_structure(tmp_path)[0]
    assert f.status == "fail"
    assert "budget" in f.evidence


def test_handoff_bundle_missing_drift_section_fails(tmp_path: Path) -> None:
    _write_bundle(tmp_path / "docs" / "handoffs", "b", drift_section=False)
    f = aud.check_handoff_bundle_structure(tmp_path)[0]
    assert f.status == "fail"
    assert "Drift cross-check" in f.evidence

# ---------------------------------------------------------------------------
# Check #9: handoff_tag_canonicity (HANDOFF_PROCESS v4.3 item F)
# ---------------------------------------------------------------------------

_SPEC_3TAG_NO_XREF = """\
# HANDOFF_PROCESS v4

### 3.1 The Phase 1 interview (sage→apprentice frame)
<!-- scope: meta -->

Tag each claim:
- witnessed (you saw it)
- inferred (you reason from evidence)
- unknown (you don't know)

---

## 4. Next section
"""

_SPEC_3TAG_WITH_XREF = """\
# HANDOFF_PROCESS v4

### 3.1 The Phase 1 interview (sage→apprentice frame)
<!-- scope: meta -->

> Note: superseded by Amendment A — four-tag canonical.

Tag each claim:
- witnessed
- inferred
- unknown

---

## 4. Next section
"""

_SPEC_4TAG = """\
# HANDOFF_PROCESS v4

### 3.1 The Phase 1 interview (sage→apprentice frame)

- witnessed
- recall
- inferred
- unknown

---
"""


def _write_spec(tmp_path: Path, text: str) -> None:
    (tmp_path / "protocols").mkdir(parents=True, exist_ok=True)
    (tmp_path / "protocols" / "HANDOFF_PROCESS.md").write_text(text, encoding="utf-8")


def test_tag_canonicity_fail_three_tags_no_xref(tmp_path: Path) -> None:
    """§3.1 with three tags and no cross-reference is the drift the check catches."""
    _write_spec(tmp_path, _SPEC_3TAG_NO_XREF)
    f = aud.check_handoff_tag_canonicity(tmp_path)[0]
    assert f.status == "fail"
    assert "cross-reference" in f.evidence.lower()


def test_tag_canonicity_pass_with_xref(tmp_path: Path) -> None:
    _write_spec(tmp_path, _SPEC_3TAG_WITH_XREF)
    f = aud.check_handoff_tag_canonicity(tmp_path)[0]
    assert f.status == "pass"
    assert "Amendment" in f.evidence


def test_tag_canonicity_pass_four_tags(tmp_path: Path) -> None:
    _write_spec(tmp_path, _SPEC_4TAG)
    f = aud.check_handoff_tag_canonicity(tmp_path)[0]
    assert f.status == "pass"


def test_tag_canonicity_no_spec(tmp_path: Path) -> None:
    """No HANDOFF_PROCESS.md → vacuous pass (check is .dev-knowledge-specific)."""
    f = aud.check_handoff_tag_canonicity(tmp_path)[0]
    assert f.status == "pass"

# ---------------------------------------------------------------------------
# _parse_last_reviewed (frontmatter helper for check #10)
# ---------------------------------------------------------------------------

def test_parse_last_reviewed_iso_date() -> None:
    """Unquoted ISO date in frontmatter parses to a date (YAML native)."""
    assert aud._parse_last_reviewed("---\nlast_reviewed: 2026-05-24\n---\n# x\n") == date(2026, 5, 24)


def test_parse_last_reviewed_quoted_string() -> None:
    """Quoted date string parses via date.fromisoformat."""
    assert aud._parse_last_reviewed('---\nlast_reviewed: "2026-05-24"\n---\n') == date(2026, 5, 24)


def test_parse_last_reviewed_datetime_coerced_to_date() -> None:
    """A full timestamp is coerced to its date component (no date/datetime mismatch)."""
    assert aud._parse_last_reviewed(
        "---\nlast_reviewed: 2026-05-24 10:00:00\n---\n") == date(2026, 5, 24)


def test_parse_last_reviewed_none_cases() -> None:
    """No frontmatter, unclosed frontmatter, missing key, and non-date all → None."""
    assert aud._parse_last_reviewed("# no frontmatter\n") is None
    assert aud._parse_last_reviewed("---\nlast_reviewed: 2026-05-24\n") is None  # unclosed
    assert aud._parse_last_reviewed("---\nowner: rob\n---\n") is None            # key absent
    assert aud._parse_last_reviewed("---\nlast_reviewed: not-a-date\n---\n") is None

# ---------------------------------------------------------------------------
# Check #10: canonical_freshness (ADR-39 grooming cadence)
# ---------------------------------------------------------------------------

def _fm(last_reviewed: str) -> str:
    """A minimal canonical-doc body carrying a last_reviewed stamp."""
    return f"---\nlast_reviewed: {last_reviewed}\nstatus: active\nowner: rob\n---\n\n# Doc\n\nBody.\n"


@pytest.fixture()
def freshness_repo(tmp_path: Path) -> Path:
    """All four freshness-tracked files present, each stamped far in the future."""
    for name in aud._FRESHNESS_FILES:
        (tmp_path / name).write_text(_fm("2099-01-01"))
    return tmp_path


def test_freshness_all_fresh(freshness_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Stamp newer than last edit and within cadence → pass."""
    monkeypatch.setattr(aud, "_git_last_commit_date", lambda rp, fn: date(2020, 1, 1))
    f = aud.check_canonical_freshness(freshness_repo)[0]
    assert f.status == "pass", f.evidence


def test_freshness_a2_edited_since_review_fails(
        freshness_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A2 (primary): last_reviewed predates the file's last git-commit date → FAIL.

    This is the done-when: the check catches a deliberately-staled file (edited after
    its review stamp). Only VISION is staled; the others stay fresh.
    """
    (freshness_repo / "VISION.md").write_text(_fm("2026-05-24"))
    monkeypatch.setattr(
        aud, "_git_last_commit_date",
        lambda rp, fn: date(2026, 5, 28) if fn == "VISION.md" else date(2020, 1, 1))
    f = aud.check_canonical_freshness(freshness_repo)[0]
    assert f.status == "fail"
    assert "VISION.md" in f.evidence
    assert "edited but not re-reviewed" in f.evidence


def test_freshness_a1_calendar_backstop_warns(
        freshness_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A1 (backstop): stamp older than the cadence but not edited since → WARN, not FAIL."""
    for name in aud._FRESHNESS_FILES:
        (freshness_repo / name).write_text(_fm("2020-01-01"))
    monkeypatch.setattr(aud, "_git_last_commit_date", lambda rp, fn: date(2020, 1, 1))
    f = aud.check_canonical_freshness(freshness_repo)[0]
    assert f.status == "warn"
    assert "cadence" in f.evidence


def test_freshness_missing_frontmatter_warns(
        freshness_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A file lacking last_reviewed → WARN (child-repo-safe), not FAIL."""
    (freshness_repo / "CLAUDE.md").write_text("# Claude\n\nNo frontmatter.\n")
    monkeypatch.setattr(aud, "_git_last_commit_date", lambda rp, fn: date(2020, 1, 1))
    f = aud.check_canonical_freshness(freshness_repo)[0]
    assert f.status == "warn"
    assert "CLAUDE.md" in f.evidence
    assert "no parseable last_reviewed" in f.evidence


def test_freshness_absent_file_skipped(
        freshness_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """An absent tracked file is skipped (presence enforced by #1/#3/#5), not warned."""
    (freshness_repo / "CONTRIBUTING.md").unlink()
    monkeypatch.setattr(aud, "_git_last_commit_date", lambda rp, fn: date(2020, 1, 1))
    f = aud.check_canonical_freshness(freshness_repo)[0]
    assert f.status == "pass", f.evidence
    assert "CONTRIBUTING" not in f.evidence


def test_freshness_a2_dominates_a1(
        freshness_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """When one file fails A2 and another only warns A1, overall status is FAIL."""
    (freshness_repo / "VISION.md").write_text(_fm("2026-05-24"))        # A2 fail
    (freshness_repo / "ARCHITECTURE.md").write_text(_fm("2020-01-01"))  # A1 warn
    monkeypatch.setattr(
        aud, "_git_last_commit_date",
        lambda rp, fn: date(2026, 5, 28) if fn == "VISION.md" else date(2020, 1, 1))
    f = aud.check_canonical_freshness(freshness_repo)[0]
    assert f.status == "fail"
    assert "also" in f.evidence and "warn" in f.evidence


def test_freshness_degrades_without_git(
        freshness_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """No git (helper returns None) → A2 skipped; A1 still applies on the working tree."""
    for name in aud._FRESHNESS_FILES:
        (freshness_repo / name).write_text(_fm("2020-01-01"))
    monkeypatch.setattr(aud, "_git_last_commit_date", lambda rp, fn: None)
    f = aud.check_canonical_freshness(freshness_repo)[0]
    assert f.status == "warn"  # A1 backstop fires; no A2 crash

# ---------------------------------------------------------------------------
# Check #10: real-git integration (NOT mocked) — proves the shipped A2 path
# ---------------------------------------------------------------------------

_HAS_GIT = shutil.which("git") is not None


def _git(repo: Path, *args: str) -> None:
    """Run a git command in `repo` with a fixed identity (no global config dependency)."""
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
    }
    subprocess.run(["git", "-C", str(repo), *args],
                   capture_output=True, text=True, env=env, check=True)


@pytest.mark.skipif(not _HAS_GIT, reason="git not available")
def test_freshness_real_git_committed_stale_fails(tmp_path: Path) -> None:
    """REAL git, no mocks: a committed file whose stamp predates its commit → A2 FAIL.

    Exercises the shipped _git_last_commit_date subprocess + the A2 comparison end-to-end,
    so a regression in the real path (not just the mocked one) is caught (Codex H3).
    """
    _git(tmp_path, "init", "-q")
    (tmp_path / "VISION.md").write_text(_fm("2020-01-01"))  # stamp far before the commit
    _git(tmp_path, "add", "VISION.md")
    _git(tmp_path, "commit", "-qm", "add vision")
    f = aud.check_canonical_freshness(tmp_path)[0]
    assert f.status == "fail"
    assert "VISION.md" in f.evidence
    assert "edited but not re-reviewed" in f.evidence


@pytest.mark.skipif(not _HAS_GIT, reason="git not available")
def test_freshness_real_git_equal_date_passes(tmp_path: Path) -> None:
    """REAL git: stamp equal to the commit's author date (today) → clean (not '<') → PASS.

    Covers the equal-date boundary on the real path: reviewed == last edit must NOT FAIL.
    """
    _git(tmp_path, "init", "-q")
    (tmp_path / "VISION.md").write_text(_fm(date.today().isoformat()))
    _git(tmp_path, "add", "VISION.md")
    _git(tmp_path, "commit", "-qm", "add vision")
    f = aud.check_canonical_freshness(tmp_path)[0]
    assert f.status == "pass", f.evidence


@pytest.mark.skipif(not _HAS_GIT, reason="git not available")
def test_git_last_commit_date_no_history_returns_none(tmp_path: Path) -> None:
    """REAL git: an untracked (never-committed) file has no commit date → None (A2 skipped)."""
    _git(tmp_path, "init", "-q")
    (tmp_path / "VISION.md").write_text(_fm("2020-01-01"))  # written but not committed
    assert aud._git_last_commit_date(tmp_path, "VISION.md") is None


def test_git_last_commit_date_not_a_repo_returns_none(tmp_path: Path) -> None:
    """A path that is not a git repo → None (graceful degradation, no crash)."""
    (tmp_path / "VISION.md").write_text(_fm("2020-01-01"))
    assert aud._git_last_commit_date(tmp_path, "VISION.md") is None
