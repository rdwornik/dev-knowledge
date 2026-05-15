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
tier: standard
owner: robdwornik@gmail.com
scale: M
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
    """Minimal ADR-38-compliant repo fixture."""
    (tmp_path / "src" / "my_pkg").mkdir(parents=True)
    (tmp_path / "src" / "my_pkg" / "__init__.py").write_text("")
    (tmp_path / "tests").mkdir()
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'my_pkg'\nversion = '0.1'\n")
    (tmp_path / "README.md").write_text("# Readme\n")
    (tmp_path / "VISION.md").write_text(GOOD_VISION)
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
    assert f.status in ("pass", "warn")  # warn allowed if ARCHITECTURE.md absent


def test_adr38_missing_readme(good_repo: Path) -> None:
    (good_repo / "README.md").unlink()
    f = aud.check_adr38_baseline(good_repo)[0]
    assert f.status == "fail"
    assert "README.md" in f.evidence


def test_adr38_missing_src(good_repo: Path) -> None:
    import shutil
    shutil.rmtree(good_repo / "src")
    f = aud.check_adr38_baseline(good_repo)[0]
    assert f.status == "fail"
    assert "src" in f.evidence


def test_adr38_missing_pyproject(good_repo: Path) -> None:
    (good_repo / "pyproject.toml").unlink()
    f = aud.check_adr38_baseline(good_repo)[0]
    assert f.status == "fail"
    assert "pyproject.toml" in f.evidence


def test_adr38_bad_repo(bad_repo: Path) -> None:
    """Repo with only README.md fails multiple checks."""
    f = aud.check_adr38_baseline(bad_repo)[0]
    assert f.status == "fail"


def test_adr38_no_lessons_or_journal_checked(good_repo: Path) -> None:
    """LESSONS.md and JOURNAL.md are .dev-knowledge-specific — NOT checked by ADR-38 baseline."""
    # Neither file exists in good_repo; check must still pass
    assert not (good_repo / "LESSONS.md").exists()
    assert not (good_repo / "JOURNAL.md").exists()
    f = aud.check_adr38_baseline(good_repo)[0]
    assert f.status in ("pass", "warn"), (
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
    # adr38 may be pass or warn (ARCHITECTURE.md optional)
    assert statuses.get("adr38_baseline") in ("pass", "warn")

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
# Check #4: dated_entries_format (ADR-46)
# ---------------------------------------------------------------------------

def test_check_dated_entries_passes_on_good_lessons() -> None:
    findings = aud.check_dated_entries_format(FIXTURES / "dated-entries-good")
    lessons_f = next(f for f in findings if "LESSONS" in f.evidence or f.check_name == "dated_entries_lessons")
    assert lessons_f.status == "pass", lessons_f.evidence


def test_check_dated_entries_passes_on_good_journal() -> None:
    findings = aud.check_dated_entries_format(FIXTURES / "dated-entries-good")
    journal_f = next(f for f in findings if "JOURNAL" in f.evidence or f.check_name == "dated_entries_journal")
    assert journal_f.status == "pass", journal_f.evidence


def test_check_dated_entries_passes_on_good_changelog() -> None:
    findings = aud.check_dated_entries_format(FIXTURES / "dated-entries-good")
    changelog_f = next(f for f in findings if "CHANGELOG" in f.evidence or f.check_name == "dated_entries_changelog")
    assert changelog_f.status == "pass", changelog_f.evidence


def test_check_dated_entries_fails_wrong_date_format(tmp_path: Path) -> None:
    (tmp_path / "CHANGELOG.md").write_text(
        (FIXTURES / "dated-entries-bad" / "wrong-date-format.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    findings = aud.check_dated_entries_format(tmp_path)
    assert any(f.status == "fail" for f in findings), [f.evidence for f in findings]


def test_check_dated_entries_fails_wrong_header_level(tmp_path: Path) -> None:
    (tmp_path / "CHANGELOG.md").write_text(
        (FIXTURES / "dated-entries-bad" / "wrong-header-level.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    findings = aud.check_dated_entries_format(tmp_path)
    assert any(f.status == "fail" for f in findings), [f.evidence for f in findings]


def test_check_dated_entries_fails_wrong_ordering(tmp_path: Path) -> None:
    (tmp_path / "CHANGELOG.md").write_text(
        (FIXTURES / "dated-entries-bad" / "wrong-ordering.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    findings = aud.check_dated_entries_format(tmp_path)
    assert any(f.status == "fail" for f in findings), [f.evidence for f in findings]


def test_check_dated_entries_warns_lessons_no_scope_tag(tmp_path: Path) -> None:
    (tmp_path / "LESSONS.md").write_text(
        (FIXTURES / "dated-entries-bad" / "lessons-no-scope-tag.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    findings = aud.check_dated_entries_format(tmp_path)
    assert any(f.status == "warn" for f in findings), [f.evidence for f in findings]


def test_check_dated_entries_warns_changelog_no_groupings(tmp_path: Path) -> None:
    (tmp_path / "CHANGELOG.md").write_text(
        (FIXTURES / "dated-entries-bad" / "changelog-no-groupings.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    findings = aud.check_dated_entries_format(tmp_path)
    assert any(f.status == "warn" for f in findings), [f.evidence for f in findings]


def test_check_dated_entries_skips_fenced_code_blocks(tmp_path: Path) -> None:
    """File with dates only inside fenced blocks must NOT pass on that basis."""
    (tmp_path / "CHANGELOG.md").write_text(
        (FIXTURES / "dated-entries-bad" / "fenced-code-trap.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    findings = aud.check_dated_entries_format(tmp_path)
    # The file has no real H2 date headings outside the fenced block; must not be pass
    assert not any(f.status == "pass" for f in findings), [f.evidence for f in findings]


# ---------------------------------------------------------------------------
# Check #5: backlog_organization (ADR-47)
# ---------------------------------------------------------------------------

def test_check_backlog_passes_on_good(tmp_path: Path) -> None:
    (tmp_path / "BACKLOG.md").write_text(
        (FIXTURES / "backlog-good" / "BACKLOG.md").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (tmp_path / "BACKLOG_ARCHIVE.md").write_text(
        (FIXTURES / "backlog-good" / "BACKLOG_ARCHIVE.md").read_text(encoding="utf-8"), encoding="utf-8"
    )
    findings = aud.check_backlog_organization(tmp_path)
    assert all(f.status in ("pass", "warn") for f in findings), [f.evidence for f in findings]
    assert any(f.status == "pass" for f in findings)


def test_check_backlog_fatal_done_in_active(tmp_path: Path) -> None:
    (tmp_path / "BACKLOG.md").write_text(
        (FIXTURES / "backlog-bad" / "done-in-active.md").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (tmp_path / "BACKLOG_ARCHIVE.md").write_text("# Archive\n", encoding="utf-8")
    findings = aud.check_backlog_organization(tmp_path)
    assert any(f.status == "fail" for f in findings), [f.evidence for f in findings]


def test_check_backlog_fatal_no_archive(tmp_path: Path) -> None:
    (tmp_path / "BACKLOG.md").write_text(
        (FIXTURES / "backlog-good" / "BACKLOG.md").read_text(encoding="utf-8"), encoding="utf-8"
    )
    # No BACKLOG_ARCHIVE.md created
    findings = aud.check_backlog_organization(tmp_path)
    assert any(f.status == "fail" for f in findings), [f.evidence for f in findings]


def test_check_backlog_fatal_wrong_entry_heading(tmp_path: Path) -> None:
    (tmp_path / "BACKLOG.md").write_text(
        (FIXTURES / "backlog-bad" / "wrong-entry-heading.md").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (tmp_path / "BACKLOG_ARCHIVE.md").write_text("# Archive\n", encoding="utf-8")
    findings = aud.check_backlog_organization(tmp_path)
    assert any(f.status == "fail" for f in findings), [f.evidence for f in findings]


def test_check_backlog_fatal_missing_required_fields(tmp_path: Path) -> None:
    (tmp_path / "BACKLOG.md").write_text(
        (FIXTURES / "backlog-bad" / "missing-required-fields.md").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (tmp_path / "BACKLOG_ARCHIVE.md").write_text("# Archive\n", encoding="utf-8")
    findings = aud.check_backlog_organization(tmp_path)
    assert any(f.status == "fail" for f in findings), [f.evidence for f in findings]


def test_check_backlog_warn_over_300_lines(tmp_path: Path) -> None:
    (tmp_path / "BACKLOG.md").write_text(
        (FIXTURES / "backlog-warn" / "over-300-lines.md").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (tmp_path / "BACKLOG_ARCHIVE.md").write_text("# Archive\n", encoding="utf-8")
    findings = aud.check_backlog_organization(tmp_path)
    assert any(f.status == "warn" for f in findings), [f.evidence for f in findings]


def test_check_backlog_warn_stream_over_15_open(tmp_path: Path) -> None:
    (tmp_path / "BACKLOG.md").write_text(
        (FIXTURES / "backlog-warn" / "stream-over-15-open.md").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (tmp_path / "BACKLOG_ARCHIVE.md").write_text("# Archive\n", encoding="utf-8")
    findings = aud.check_backlog_organization(tmp_path)
    assert any(f.status == "warn" for f in findings), [f.evidence for f in findings]


def test_check_backlog_warn_cross_stream_over_33pct(tmp_path: Path) -> None:
    # Build a BACKLOG where Cross-stream has >33% of open items
    content = """\
# BACKLOG

<!-- scope: meta -->

## Stream A: work

### [P1] [open] Stream A item 1
- **What:** Item.
- **Why:** Reason.
- **Added:** 2026-05-15 by rob (test)
- **Status:** open

## Cross-stream / Ecosystem

### [P1] [open] Cross item 1
- **What:** Cross item.
- **Why:** Reason.
- **Added:** 2026-05-15 by rob (test)
- **Status:** open

### [P1] [open] Cross item 2
- **What:** Cross item 2.
- **Why:** Reason.
- **Added:** 2026-05-15 by rob (test)
- **Status:** open
"""
    (tmp_path / "BACKLOG.md").write_text(content, encoding="utf-8")
    (tmp_path / "BACKLOG_ARCHIVE.md").write_text("# Archive\n", encoding="utf-8")
    findings = aud.check_backlog_organization(tmp_path)
    # 1 Stream A + 2 Cross-stream = 3 total open; Cross-stream = 66% > 33%
    assert any(f.status == "warn" for f in findings), [f.evidence for f in findings]
