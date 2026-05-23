"""Tests for scripts/audit.py — schema roundtrip, check execution, report generation."""
from __future__ import annotations

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
