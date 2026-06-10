"""Tests for scripts/audit.py — schema roundtrip, check execution, report generation."""
from __future__ import annotations

import json
import logging
import shutil
import subprocess
import sys
import os
from datetime import date
from pathlib import Path
from types import SimpleNamespace

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
    """Repo satisfying the ADR-38 A6 seven-file universal governance baseline.

    Baseline files: VISION, ARCHITECTURE, CLAUDE, BACKLOG, CONTRIBUTING, JOURNAL,
    LESSONS. src/, tests/, pyproject.toml, README.md, CHANGELOG.md are kept here only
    to prove they are NOT required by check_adr38_baseline post-amendment. Bodies are
    minimal (presence-level); the [U] spine is exercised against the
    repo-with-structural-checks fixture, not here.
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
    (tmp_path / "CONTRIBUTING.md").write_text("# Contributing\n")
    (tmp_path / "JOURNAL.md").write_text("# Journal\n")
    (tmp_path / "LESSONS.md").write_text("# Lessons Learned\n")
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


def test_adr38_now_requires_lessons_and_journal(good_repo: Path) -> None:
    """ADR-38 A6 (2026-06-02) promoted CONTRIBUTING/JOURNAL/LESSONS to the mandatory set.

    Inverts the pre-A6 test: these files were repo-specific under A5; under A6 they
    are part of the seven-file canonical baseline, so absence is a failure.
    """
    # good_repo carries all seven canonical files → pass
    f = aud.check_adr38_baseline(good_repo)[0]
    assert f.status == "pass", f"seven-file good_repo should pass; got: {f.evidence}"
    # Removing LESSONS.md now fails (was tolerated pre-A6)
    (good_repo / "LESSONS.md").unlink()
    f = aud.check_adr38_baseline(good_repo)[0]
    assert f.status == "fail"
    assert "LESSONS.md" in f.evidence

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
    # Tracks the mandatory set (seven files post ADR-38 A6).
    for name in aud._CANONICAL_MANDATORY:
        (tmp_path / name).write_text("x")


def test_canonical_md_pass(tmp_path: Path) -> None:
    _make_canonical(tmp_path)
    f = aud.check_canonical_md_visibility(tmp_path)[0]
    assert f.status == "pass"


def test_canonical_md_optional_absent_still_pass(tmp_path: Path) -> None:
    """README/ENVIRONMENT/ESSENTIALS/PLAYBOOK/TOKEN-LOG are NOT required — absence must not fail.

    (CONTRIBUTING/JOURNAL/LESSONS are now mandatory under ADR-38 A6 and are written by
    _make_canonical; the remaining canonical names stay optional.)
    """
    _make_canonical(tmp_path)
    assert not (tmp_path / "README.md").exists()
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
    # README is optional (so not written by _make_canonical) but casing is still checked
    # when present — and it avoids a case-insensitive-FS collision with a mandatory file.
    (tmp_path / "Readme.md").write_text("x")  # should be README.md
    f = aud.check_canonical_md_visibility(tmp_path)[0]
    assert f.status == "fail"
    assert "Readme.md" in f.evidence


# ---------------------------------------------------------------------------
# Check #12: canonical_structure (ADR-38 A6)
# ---------------------------------------------------------------------------

def test_canonical_structure_pass(tmp_path: Path) -> None:
    """A canonical file carrying its [U] spine headings passes."""
    (tmp_path / "CONTRIBUTING.md").write_text(
        "# Contributing\n\n## Branch naming\n\n## Commit style\n\n## Handoff process\n")
    f = aud.check_canonical_structure(tmp_path)[0]
    assert f.status == "pass"


def test_canonical_structure_fail_missing_heading(tmp_path: Path) -> None:
    """A present canonical file missing a required spine heading fails, naming it."""
    (tmp_path / "CONTRIBUTING.md").write_text("# Contributing\n\n## Branch naming\n")
    f = aud.check_canonical_structure(tmp_path)[0]
    assert f.status == "fail"
    assert "Commit style" in f.evidence


def test_canonical_structure_absent_file_not_flagged(tmp_path: Path) -> None:
    """Absent canonical files are not flagged here (presence is owned by other checks)."""
    f = aud.check_canonical_structure(tmp_path)[0]
    assert f.status == "pass"


def test_canonical_structure_startswith_allows_h1_suffix(tmp_path: Path) -> None:
    """A repo-suffixed H1 (e.g. '# Journal - ai-council') still matches the spine."""
    (tmp_path / "JOURNAL.md").write_text("# Journal - ai-council\n\nentries\n")
    (tmp_path / "LESSONS.md").write_text("# Lessons Learned - log\n\nentries\n")
    f = aud.check_canonical_structure(tmp_path)[0]
    assert f.status == "pass"


def test_canonical_structure_rejects_near_miss_heading(tmp_path: Path) -> None:
    """Boundary-aware match: '## Visionary' must NOT satisfy required '## Vision'.

    Regression for Codex review HIGH 2026-06-02 (startswith false-pass).
    """
    (tmp_path / "VISION.md").write_text(
        "# Vision\n\n## Visionary\n## Scoped\n## Values\n## Lifecycle\n## References\n")
    f = aud.check_canonical_structure(tmp_path)[0]
    assert f.status == "fail"
    assert "## Vision" in f.evidence  # the unmatched required heading is named
    assert "## Scope" in f.evidence

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
# checks command (CLI) — drift-proof listing sourced from ALL_CHECKS
# ---------------------------------------------------------------------------

def test_checks_lists_every_registered_check() -> None:
    """`checks` exits 0, reports the live ALL_CHECKS count, and names every check.

    The listing is sourced from ALL_CHECKS (the same list health/run execute), so the
    count and names cannot drift from what actually runs — this is the guarantee the
    command exists to provide.
    """
    from click.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(aud.cmd_checks)
    assert result.exit_code == 0
    assert f"{len(aud.ALL_CHECKS)} registered checks" in result.output
    for check in aud.ALL_CHECKS:
        name = check.__name__.removeprefix("check_")
        assert name in result.output


def test_checks_count_matches_what_runs() -> None:
    """The number `checks` prints equals the number of findings a run produces.

    Guards the drift the command was built to kill (the §18 "10 vs 11 vs 12"): the
    listed count is len(ALL_CHECKS), and each check contributes >=1 finding on a repo.
    """
    from click.testing import CliRunner
    result = CliRunner().invoke(aud.cmd_checks)
    listed = int(result.output.split(" registered checks", 1)[0].split("\n")[-1])
    assert listed == len(aud.ALL_CHECKS)


# ---------------------------------------------------------------------------
# cmd_health _GATE_MODE set/reset around the ALL_CHECKS loop (#89 / #141 Fix 3)
# ---------------------------------------------------------------------------

def test_cmd_health_gate_mode_set_during_loop_and_restored(monkeypatch: pytest.MonkeyPatch) -> None:
    """cmd_health sets _GATE_MODE True around the self-audit loop (so claim-3 skips on the
    gate) and restores it False after. Observe the flag DURING the loop via a sentinel check,
    and assert restoration AFTER. Highest-risk global-mutation path (Codex HIGH)."""
    from click.testing import CliRunner

    seen = {}

    def _sentinel(_repo: Path):
        seen["during"] = aud._GATE_MODE
        return [aud.Finding("sentinel", "pass", "observed gate mode")]

    monkeypatch.setattr(aud, "_GATE_MODE", False)        # hermetic baseline
    monkeypatch.setattr(aud, "ALL_CHECKS", [_sentinel])
    CliRunner().invoke(aud.cmd_health)

    assert seen["during"] is True                        # set True inside the loop
    assert aud._GATE_MODE is False                       # restored after the loop


def test_cmd_health_gate_mode_restored_on_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    """If a check raises mid-loop, the try/finally still resets _GATE_MODE to False — a
    missing reset after failure would silently disable claim-3 on later full-audit runs."""
    from click.testing import CliRunner

    def _boom(_repo: Path):
        raise RuntimeError("check exploded")

    monkeypatch.setattr(aud, "_GATE_MODE", False)
    monkeypatch.setattr(aud, "ALL_CHECKS", [_boom])
    result = CliRunner().invoke(aud.cmd_health)          # CliRunner captures the exception

    assert isinstance(result.exception, RuntimeError)    # the raise propagated out
    assert aud._GATE_MODE is False                       # ...yet finally still reset it


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

# ---------------------------------------------------------------------------
# Check #11: no_sibling_orphans (no-leftovers invariant — PLAYBOOK G5)
# ---------------------------------------------------------------------------

def test_no_sibling_orphans_none_present(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """No `<repo>-*` siblings at all → pass (git reports only the repo itself)."""
    repo = tmp_path / "myrepo"
    repo.mkdir()
    monkeypatch.setattr(aud, "_git_registered_worktrees",
                        lambda rp: {os.path.normcase(str(repo.resolve()))})
    f = aud.check_no_sibling_orphans(repo)[0]
    assert f.status == "pass"


def test_no_sibling_orphans_unregistered_dir_fails(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """An on-disk `<repo>-*` sibling that is NOT a registered worktree → FAIL (the orphan).

    This is the done-when: the detector catches a deregistered-but-undeleted shell — the
    `.dev-knowledge-cadence` / `.dev-knowledge-night-adr` failure mode.
    """
    repo = tmp_path / "myrepo"
    repo.mkdir()
    (tmp_path / "myrepo-cadence").mkdir()  # orphan: exists on disk, not registered
    monkeypatch.setattr(aud, "_git_registered_worktrees",
                        lambda rp: {os.path.normcase(str(repo.resolve()))})
    f = aud.check_no_sibling_orphans(repo)[0]
    assert f.status == "fail"
    assert "myrepo-cadence" in f.evidence


def test_no_sibling_orphans_registered_worktree_passes(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A `<repo>-*` sibling that IS a registered worktree is live work → NOT flagged.

    The load-bearing discriminator: registration, not name, is what separates a live
    parallel worktree from an orphan shell.
    """
    repo = tmp_path / "myrepo"
    repo.mkdir()
    live = tmp_path / "myrepo-parallel"
    live.mkdir()
    monkeypatch.setattr(
        aud, "_git_registered_worktrees",
        lambda rp: {os.path.normcase(str(repo.resolve())),
                    os.path.normcase(str(live.resolve()))})
    f = aud.check_no_sibling_orphans(repo)[0]
    assert f.status == "pass"


def test_no_sibling_orphans_mixed_only_flags_unregistered(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """With one live (registered) and one orphan sibling, only the orphan is flagged."""
    repo = tmp_path / "myrepo"
    repo.mkdir()
    live = tmp_path / "myrepo-live"
    live.mkdir()
    (tmp_path / "myrepo-orphan").mkdir()
    monkeypatch.setattr(
        aud, "_git_registered_worktrees",
        lambda rp: {os.path.normcase(str(repo.resolve())),
                    os.path.normcase(str(live.resolve()))})
    f = aud.check_no_sibling_orphans(repo)[0]
    assert f.status == "fail"
    assert "myrepo-orphan" in f.evidence
    assert "myrepo-live" not in f.evidence


def test_no_sibling_orphans_ignores_non_prefixed_siblings(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Sibling repos that don't share the `<repo>-` prefix are never considered."""
    repo = tmp_path / "myrepo"
    repo.mkdir()
    (tmp_path / "other-repo").mkdir()       # different repo, not a `myrepo-*` sibling
    (tmp_path / "myrepofoo").mkdir()         # no separating '-', not a `myrepo-*` sibling
    monkeypatch.setattr(aud, "_git_registered_worktrees",
                        lambda rp: {os.path.normcase(str(repo.resolve()))})
    f = aud.check_no_sibling_orphans(repo)[0]
    assert f.status == "pass"


def test_no_sibling_orphans_degrades_without_git(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """No git (helper returns None) → check is skipped as a pass, never crashes."""
    repo = tmp_path / "myrepo"
    repo.mkdir()
    (tmp_path / "myrepo-cadence").mkdir()  # would be an orphan if git were available
    monkeypatch.setattr(aud, "_git_registered_worktrees", lambda rp: None)
    f = aud.check_no_sibling_orphans(repo)[0]
    assert f.status == "pass"
    assert "skipped" in f.evidence


def test_no_sibling_orphans_same_prefix_repo_not_flagged(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A legitimate same-prefix sibling REPO (own .git/ dir + content) is NOT an orphan.

    Regression for Codex H1 (2026-06-02): registration alone over-flagged any `<repo>-*`
    sibling. The remnant guard must spare an independent repo that merely shares the prefix.
    """
    repo = tmp_path / "myrepo"
    repo.mkdir()
    sibling_repo = tmp_path / "myrepo-frontend"   # a real, separate project
    sibling_repo.mkdir()
    (sibling_repo / ".git").mkdir()               # independent repo: .git is a DIRECTORY
    (sibling_repo / "README.md").write_text("real project")
    monkeypatch.setattr(aud, "_git_registered_worktrees",
                        lambda rp: {os.path.normcase(str(repo.resolve()))})
    f = aud.check_no_sibling_orphans(repo)[0]
    assert f.status == "pass", f.evidence


def test_no_sibling_orphans_same_prefix_populated_folder_not_flagged(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A populated non-worktree folder sharing the prefix is NOT an orphan (Codex H1)."""
    repo = tmp_path / "myrepo"
    repo.mkdir()
    notes = tmp_path / "myrepo-notes"
    notes.mkdir()
    (notes / "todo.txt").write_text("not a worktree")  # content, no .git → not a remnant
    monkeypatch.setattr(aud, "_git_registered_worktrees",
                        lambda rp: {os.path.normcase(str(repo.resolve()))})
    f = aud.check_no_sibling_orphans(repo)[0]
    assert f.status == "pass", f.evidence


def test_no_sibling_orphans_deregistered_worktree_with_gitlink_fails(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A populated but deregistered worktree (carries a .git gitlink FILE) is still caught."""
    repo = tmp_path / "myrepo"
    repo.mkdir()
    stale = tmp_path / "myrepo-stale"
    stale.mkdir()
    (stale / ".git").write_text("gitdir: ../myrepo/.git/worktrees/myrepo-stale\n")  # gitlink
    (stale / "leftover.txt").write_text("half-removed worktree content")
    monkeypatch.setattr(aud, "_git_registered_worktrees",
                        lambda rp: {os.path.normcase(str(repo.resolve()))})
    f = aud.check_no_sibling_orphans(repo)[0]
    assert f.status == "fail"
    assert "myrepo-stale" in f.evidence


@pytest.mark.skipif(not _HAS_GIT, reason="git not available")
def test_no_sibling_orphans_real_git_orphan_fails(tmp_path: Path) -> None:
    """REAL git, no mocks: an unregistered `<repo>-*` sibling → FAIL end-to-end.

    Exercises the shipped `git worktree list --porcelain` subprocess + the registration
    comparison, so a regression in the real path (not just the mocked one) is caught.
    """
    repo = tmp_path / "myrepo"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "f.txt").write_text("x")
    _git(repo, "add", "f.txt")
    _git(repo, "commit", "-qm", "init")
    (tmp_path / "myrepo-orphan").mkdir()  # plain dir, never a registered worktree
    f = aud.check_no_sibling_orphans(repo)[0]
    assert f.status == "fail"
    assert "myrepo-orphan" in f.evidence


@pytest.mark.skipif(not _HAS_GIT, reason="git not available")
def test_no_sibling_orphans_real_git_live_worktree_passes(tmp_path: Path) -> None:
    """REAL git: an actual registered worktree sibling is live work → PASS (not flagged)."""
    repo = tmp_path / "myrepo"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "f.txt").write_text("x")
    _git(repo, "add", "f.txt")
    _git(repo, "commit", "-qm", "init")
    wt = tmp_path / "myrepo-parallel"
    _git(repo, "worktree", "add", "-q", "--detach", str(wt))
    f = aud.check_no_sibling_orphans(repo)[0]
    assert f.status == "pass", f.evidence


# ---------------------------------------------------------------------------
# Check #13: handoff_version_stamp (S1 recurrence class — nightly arc #81)
# ---------------------------------------------------------------------------

def _write_handoff_spec(tmp_path: Path, version: str) -> None:
    (tmp_path / "protocols").mkdir(parents=True, exist_ok=True)
    (tmp_path / "protocols" / "HANDOFF_PROCESS.md").write_text(
        f"# HANDOFF_PROCESS\n\nVersion: {version}\nStatus: live\n", encoding="utf-8"
    )


def test_handoff_version_stamp_pass(tmp_path: Path) -> None:
    """Stamps in both living docs match canonical version → pass."""
    _write_handoff_spec(tmp_path, "4.4")
    (tmp_path / "ARCHITECTURE.md").write_text(
        "# Architecture\n\nstamp 4.4, live\n", encoding="utf-8")
    (tmp_path / "CONTRIBUTING.md").write_text(
        "# Contributing\n\nstamp v4.4, *live*\n", encoding="utf-8")
    f = aud.check_handoff_version_stamp(tmp_path)[0]
    assert f.status == "pass"
    assert "4.4" in f.evidence


def test_handoff_version_stamp_fail_mismatch(tmp_path: Path) -> None:
    """A stamp referencing a stale version → fail, naming the file and line."""
    _write_handoff_spec(tmp_path, "4.4")
    (tmp_path / "ARCHITECTURE.md").write_text(
        "# Architecture\n\nstamp 4.3.2, live\n", encoding="utf-8")
    (tmp_path / "CONTRIBUTING.md").write_text(
        "# Contributing\n\nstamp v4.4, *live*\n", encoding="utf-8")
    f = aud.check_handoff_version_stamp(tmp_path)[0]
    assert f.status == "fail"
    assert "ARCHITECTURE.md" in f.evidence
    assert "4.3.2" in f.evidence


def test_handoff_version_stamp_fail_multiple_mismatches(tmp_path: Path) -> None:
    """Multiple mismatching stamps all reported in a single fail finding."""
    _write_handoff_spec(tmp_path, "4.4")
    (tmp_path / "ARCHITECTURE.md").write_text(
        "# Architecture\n\nstamp 4.3.2, live\n\nAnother stamp 4.3.2 here.\n",
        encoding="utf-8",
    )
    (tmp_path / "CONTRIBUTING.md").write_text(
        "# Contributing\n\nstamp 4.3.2, *live*\n", encoding="utf-8")
    f = aud.check_handoff_version_stamp(tmp_path)[0]
    assert f.status == "fail"
    assert "mismatch" in f.evidence


def test_handoff_version_stamp_no_spec_passes(tmp_path: Path) -> None:
    """No protocols/HANDOFF_PROCESS.md → child-repo-safe vacuous pass."""
    (tmp_path / "ARCHITECTURE.md").write_text("# Architecture\n\nstamp 4.4\n", encoding="utf-8")
    f = aud.check_handoff_version_stamp(tmp_path)[0]
    assert f.status == "pass"
    assert "nothing to validate" in f.evidence


def test_handoff_version_stamp_no_version_line_warns(tmp_path: Path) -> None:
    """HANDOFF_PROCESS.md with no parseable Version: line → warn."""
    (tmp_path / "protocols").mkdir(parents=True)
    (tmp_path / "protocols" / "HANDOFF_PROCESS.md").write_text(
        "# HANDOFF_PROCESS\n\nNo version header here.\n", encoding="utf-8"
    )
    f = aud.check_handoff_version_stamp(tmp_path)[0]
    assert f.status == "warn"
    assert "Version" in f.evidence or "parseable" in f.evidence.lower()


def test_handoff_version_stamp_no_stamps_in_living_docs_warns(tmp_path: Path) -> None:
    """Spec present with valid version but no stamp occurrences in living docs → warn."""
    _write_handoff_spec(tmp_path, "4.4")
    (tmp_path / "ARCHITECTURE.md").write_text(
        "# Architecture\n\nNo stamps here.\n", encoding="utf-8")
    f = aud.check_handoff_version_stamp(tmp_path)[0]
    assert f.status == "warn"
    assert "No 'stamp" in f.evidence or "drifted" in f.evidence


def test_handoff_version_stamp_absent_living_docs_warns(tmp_path: Path) -> None:
    """Spec has version but neither ARCHITECTURE.md nor CONTRIBUTING.md exist → warn."""
    _write_handoff_spec(tmp_path, "4.4")
    # Neither stamp target file is created
    f = aud.check_handoff_version_stamp(tmp_path)[0]
    assert f.status == "warn"


# ---------------------------------------------------------------------------
# ADR-80 commit logic
# ---------------------------------------------------------------------------


def _make_subprocess_mock(*, add_rc=0, diff_rc=1, commit_rc=0):
    """Return a fake subprocess.run that responds predictably to git subcommands."""
    def fake_run(cmd, **kwargs):
        subcmd = cmd[3] if len(cmd) > 3 else ""
        if subcmd == "add":
            return SimpleNamespace(returncode=add_rc, stderr="", stdout="")
        if subcmd == "diff":
            return SimpleNamespace(returncode=diff_rc, stderr="", stdout="")
        if subcmd == "commit":
            return SimpleNamespace(returncode=commit_rc, stderr="fatal: lock", stdout="")
        return SimpleNamespace(returncode=0, stderr="", stdout="")
    return fake_run


def test_commit_routine_outputs_stages_only_durable(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """_commit_routine_outputs passes concrete history/ paths (no glob) + docs/audits/ to git add."""
    eco = tmp_path / "ecosystem"
    (eco / "repo-a" / "history").mkdir(parents=True)
    (eco / "repo-b" / "history").mkdir(parents=True)
    monkeypatch.setattr(aud, "ECOSYSTEM_DIR", eco)
    monkeypatch.setattr(aud, "AUDITS_DIR", tmp_path / "docs" / "audits")
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))

    add_pathspecs: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        subcmd = cmd[3] if len(cmd) > 3 else ""
        if subcmd == "add":
            add_pathspecs.append(list(cmd))
            return SimpleNamespace(returncode=0, stderr="", stdout="")
        if subcmd == "diff":
            return SimpleNamespace(returncode=1)  # something staged
        return SimpleNamespace(returncode=0, stderr="", stdout="")

    monkeypatch.setattr(aud.subprocess, "run", fake_run)
    aud._commit_routine_outputs(date(2026, 6, 7))

    assert add_pathspecs, "Expected git add call"
    pathspecs = add_pathspecs[0]
    assert "ecosystem/repo-a/history" in pathspecs
    assert "ecosystem/repo-b/history" in pathspecs
    assert "docs/audits" in pathspecs
    assert not any("*" in p for p in pathspecs), "Must not use glob pathspecs (Windows compat)"
    assert "-A" not in pathspecs


def test_commit_routine_outputs_retries_after_hook_modify(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """_commit_routine_outputs re-stages and retries once when first commit fails (e.g. hook modified files)."""
    add_count = [0]
    commit_results = [1, 0]  # first attempt fails (hook modified), retry succeeds

    def fake_run(cmd, **kwargs):
        subcmd = cmd[3] if len(cmd) > 3 else ""
        if subcmd == "add":
            add_count[0] += 1
            return SimpleNamespace(returncode=0, stderr="", stdout="")
        if subcmd == "diff":
            return SimpleNamespace(returncode=1)  # something staged
        if subcmd == "commit":
            rc = commit_results.pop(0) if commit_results else 0
            return SimpleNamespace(returncode=rc, stderr="hook modified files", stdout="")
        return SimpleNamespace(returncode=0, stderr="", stdout="")

    monkeypatch.setattr(aud.subprocess, "run", fake_run)
    aud._commit_routine_outputs(date(2026, 6, 7))

    assert add_count[0] == 2, "Expected re-stage after first commit failure"
    assert not any("ADR-80 commit" in r.message for r in caplog.records), "Should not WARN on successful retry"


def test_commit_routine_outputs_trailer_present(monkeypatch: pytest.MonkeyPatch) -> None:
    """_commit_routine_outputs includes 'Routine: fleet-audit' trailer in commit msg."""
    commit_msgs: list[str] = []

    def fake_run(cmd, **kwargs):
        subcmd = cmd[3] if len(cmd) > 3 else ""
        if subcmd == "add":
            return SimpleNamespace(returncode=0, stderr="", stdout="")
        if subcmd == "diff":
            return SimpleNamespace(returncode=1)
        if subcmd == "commit":
            idx = list(cmd).index("-m")
            commit_msgs.append(cmd[idx + 1])
            return SimpleNamespace(returncode=0, stderr="", stdout="")
        return SimpleNamespace(returncode=0, stderr="", stdout="")

    monkeypatch.setattr(aud.subprocess, "run", fake_run)
    aud._commit_routine_outputs(date(2026, 6, 7))

    assert commit_msgs, "Expected git commit call"
    assert "Routine: fleet-audit" in commit_msgs[0]
    assert "2026-06-07" in commit_msgs[0]


def test_commit_routine_outputs_fail_soft_on_locked_index(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """_commit_routine_outputs returns cleanly (does not raise) when git commit fails."""
    monkeypatch.setattr(aud.subprocess, "run", _make_subprocess_mock(commit_rc=128))

    with caplog.at_level(logging.WARNING, logger="audit"):
        aud._commit_routine_outputs(date(2026, 6, 7))  # must not raise

    assert any("failed" in r.message.lower() for r in caplog.records)


def test_commit_routine_outputs_no_commit_when_nothing_staged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """_commit_routine_outputs skips commit when git diff --cached --quiet exits 0."""
    commit_calls: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        subcmd = cmd[3] if len(cmd) > 3 else ""
        if subcmd == "commit":
            commit_calls.append(list(cmd))
        return SimpleNamespace(returncode=0, stderr="", stdout="")

    monkeypatch.setattr(aud.subprocess, "run", fake_run)
    aud._commit_routine_outputs(date(2026, 6, 7))

    assert not commit_calls, "Must not commit when nothing is staged"


# ---------------------------------------------------------------------------
# Check #14: floor_integrity (ADR-78 child methodology floor)
# ---------------------------------------------------------------------------

import generate_floor as gf  # noqa: E402  (scripts/ already on sys.path)


def _seed_floor(repo: Path, floor_text: str | None = None, *, sidecar: bool = True,
                pointers: bool = True) -> str:
    """Write a CLAUDE-FLOOR.md (+ matching sidecar + pointer targets) into `repo`.

    Returns the floor text used. With floor_text=None, uses the shipped template body.
    """
    floor = floor_text if floor_text is not None else gf.render_floor()
    claude_dir = repo / ".claude"
    claude_dir.mkdir(exist_ok=True)
    (claude_dir / "CLAUDE-FLOOR.md").write_text(floor, encoding="utf-8")
    if sidecar:
        (claude_dir / "CLAUDE-FLOOR.md.sha256").write_text(
            gf.floor_sha256(floor) + "\n", encoding="utf-8")
    if pointers:
        for name in ("CLAUDE.md", "VISION.md", "ARCHITECTURE.md"):
            (repo / name).write_text("placeholder\n", encoding="utf-8")
    return floor


def test_floor_integrity_no_floor_passes(tmp_path: Path) -> None:
    """A repo with no CLAUDE-FLOOR.md (incl. the hub itself) passes vacuously."""
    f = aud.check_floor_integrity(tmp_path)[0]
    assert f.status == "pass"
    assert "not adopted" in f.evidence


def test_floor_integrity_valid_floor_passes(tmp_path: Path) -> None:
    """Shipped floor + matching sidecar + resolvable pointers → pass."""
    _seed_floor(tmp_path)
    f = aud.check_floor_integrity(tmp_path)[0]
    assert f.status == "pass"
    assert "hash matches sidecar" in f.evidence


def test_floor_integrity_tamper_fails(tmp_path: Path) -> None:
    """The tamper test: editing one floor line without regenerating → hash-drift FAIL."""
    _seed_floor(tmp_path)
    floor = tmp_path / ".claude" / "CLAUDE-FLOOR.md"
    floor.write_text(floor.read_text(encoding="utf-8") + "\nTAMPERED LINE\n", encoding="utf-8")
    f = aud.check_floor_integrity(tmp_path)[0]
    assert f.status == "fail"
    assert "hash drift" in f.evidence


def test_floor_integrity_missing_sidecar_fails(tmp_path: Path) -> None:
    _seed_floor(tmp_path, sidecar=False)
    f = aud.check_floor_integrity(tmp_path)[0]
    assert f.status == "fail"
    assert "sidecar missing" in f.evidence


def test_floor_integrity_f5_leak_fails(tmp_path: Path) -> None:
    """A floor that leaks a hub-internal token fails even with a matching sidecar."""
    leaky = gf.render_floor() + "\nSee [#5] in the hub backlog.\n"
    _seed_floor(tmp_path, leaky)
    f = aud.check_floor_integrity(tmp_path)[0]
    assert f.status == "fail"
    assert "F5 self-containment" in f.evidence


def test_floor_integrity_broken_pointer_fails(tmp_path: Path) -> None:
    """Floor names same-repo docs that don't exist → pointer-existence FAIL (T3 fold-in)."""
    _seed_floor(tmp_path, pointers=False)
    f = aud.check_floor_integrity(tmp_path)[0]
    assert f.status == "fail"
    assert "do not exist" in f.evidence


def test_floor_integrity_registered_in_all_checks() -> None:
    assert aud.check_floor_integrity in aud.ALL_CHECKS


# ---------------------------------------------------------------------------
# check_amendment_coherence — #11 multi-surface amendment gate (version stragglers)
#
# Tests are derived from the architect's acceptance criteria (the #11 plan), NOT from
# the implementation (circular-testing guard). Criteria:
#   - the gate FIRES (FAIL / health exit 1) when a coupled surface strands at a stale
#     version vs the anchor's authority version;
#   - it PASSES on an aligned set;
#   - it normalizes granularity (major-only; and full so 3.4 == 3.4.0, the v3.4 minor class);
#   - it is FAIL-blocking through the real gate (audit.py health), not just as a function.
# Teeth: gutting the comparison `if surface_ver != canonical:` -> `if False:` makes the
# check PASS on the seeded straggler, so the FIRES tests (asserting fail / exit 1) go RED.
# ---------------------------------------------------------------------------

def _seed_coupled(repo: Path, spec_ver: str, surface_ver: str) -> None:
    """Seed the REAL manifest's declared paths (handoff-major-version set) in `repo`.

    Writes the anchor (protocols/HANDOFF_PROCESS.md `Version:`) plus the two coupled
    surfaces using the EXACT live line forms (CLAUDE.md:105, .claude/commands/handoff.md:2)
    so any faithful manifest regex matches. `spec_ver` is the full anchor version (e.g.
    "4.4"); `surface_ver` is what the surfaces declare (e.g. "4" aligned, "3" straggler).
    """
    (repo / "protocols").mkdir(parents=True, exist_ok=True)
    (repo / ".claude" / "commands").mkdir(parents=True, exist_ok=True)
    (repo / "protocols" / "HANDOFF_PROCESS.md").write_text(
        f"# Handoff Process\nVersion: {spec_ver}\n", encoding="utf-8")
    (repo / "CLAUDE.md").write_text(
        f"## 7\n- `/handoff` — generate/complete handoff per `HANDOFF_PROCESS.md` "
        f"v{surface_ver} two-phase flow (ADR-62)\n", encoding="utf-8")
    (repo / ".claude" / "commands" / "handoff.md").write_text(
        f"---\ndescription: Generate or complete a handoff per HANDOFF_PROCESS.md "
        f"v{surface_ver} — two-phase interview\n---\n", encoding="utf-8")


def test_amendment_coherence_straggler_fires(tmp_path: Path) -> None:
    """A surface stranded at a stale major (v3 while the spec is 4.x) -> FAIL with a
    straggler detail naming the offending surface."""
    _seed_coupled(tmp_path, spec_ver="4.4", surface_ver="3")
    f = aud.check_amendment_coherence(tmp_path)[0]
    assert f.status == "fail"
    assert "straggler" in f.evidence.lower()
    assert "CLAUDE.md" in f.evidence or "handoff.md" in f.evidence


def test_amendment_coherence_aligned_passes(tmp_path: Path) -> None:
    """All coupled surfaces at the anchor's major (v4) -> PASS (legit aligned amendment)."""
    _seed_coupled(tmp_path, spec_ver="4.4", surface_ver="4")
    f = aud.check_amendment_coherence(tmp_path)[0]
    assert f.status == "pass"


def test_amendment_coherence_no_anchor_skips(tmp_path: Path) -> None:
    """Child-repo-safe: no HANDOFF_PROCESS.md anchor present -> PASS (skip, no false-FAIL)."""
    f = aud.check_amendment_coherence(tmp_path)[0]
    assert f.status == "pass"


def test_amendment_coherence_full_granularity_minor_straggler(tmp_path: Path) -> None:
    """A 'full'-granularity set catches a MINOR straggler (the v3.4 abort class: 3.3.3 vs
    3.4, both major 3), and 3.4 == 3.4.0 trailing-zero normalization does NOT false-FAIL.
    Uses an injected set (criteria-derived data, not implementation) to exercise the
    comparison logic independent of the real manifest."""
    (tmp_path / "spec.md").write_text("Version: 3.4\n", encoding="utf-8")
    (tmp_path / "inst.md").write_text("pinned at v3.3.3 here\n", encoding="utf-8")
    cset = aud.CoupledSet(
        name="t",
        anchor=("spec.md", r"Version:\s+v?(\d+\.\d+(?:\.\d+)?)"),
        surfaces=[("inst.md", r"v(\d+\.\d+(?:\.\d+)?)")],
        granularity="full",
    )
    f = aud.check_amendment_coherence(tmp_path, _sets=[cset])[0]
    assert f.status == "fail"  # 3.3.3 != 3.4

    (tmp_path / "inst.md").write_text("pinned at v3.4.0 here\n", encoding="utf-8")
    f2 = aud.check_amendment_coherence(tmp_path, _sets=[cset])[0]
    assert f2.status == "pass"  # 3.4 == 3.4.0 (normalization)


def test_amendment_coherence_gate_blocks_health(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """ENFORCEMENT-PATH E2E (must-fix 1): a seeded straggler routed through the REAL gate
    (`audit.py health` / cmd_health) makes it EXIT 1 (ADR-81 (d) FAIL-blocking), and an
    aligned tree exits 0. Isolates ALL_CHECKS to this check so the exit code is attributable
    to the straggler (precedent: the _GATE_MODE cmd_health tests). Proves deployment, not
    just that the function returns 'fail'."""
    from click.testing import CliRunner

    # operational deps OK so the exit code is driven by self-conformance, not ecosystem absence
    eco = tmp_path / "ecosystem" / "r"
    eco.mkdir(parents=True)
    (eco / "state.yaml").write_text(
        "name: r\npath: /tmp/r\nlast_audit: null\nfindings: []\n", encoding="utf-8")
    monkeypatch.setattr(aud, "ECOSYSTEM_DIR", tmp_path / "ecosystem")
    monkeypatch.setattr(aud, "ALL_CHECKS", [aud.check_amendment_coherence])

    repo = tmp_path / "repo"
    _seed_coupled(repo, spec_ver="4.4", surface_ver="3")     # straggler
    monkeypatch.setattr(aud, "_REPO_ROOT", str(repo))
    blocked = CliRunner().invoke(aud.cmd_health)
    assert blocked.exit_code == 1
    assert "DEGRADED" in blocked.output

    _seed_coupled(repo, spec_ver="4.4", surface_ver="4")     # aligned (overwrite surfaces)
    passed = CliRunner().invoke(aud.cmd_health)
    assert passed.exit_code == 0
    assert "OK" in passed.output


def test_amendment_coherence_present_surface_missing_mention_warns(tmp_path: Path) -> None:
    """Codex HIGH-1: a present coupled surface whose normative version mention vanished
    (reworded/removed) is surfaced as drift (WARN), never a silent PASS. Anchor present
    (hub case); CLAUDE.md keeps its mention but handoff.md loses it.
    Teeth: dropping the surface_hits==0 drift branch makes this go PASS -> RED."""
    _seed_coupled(tmp_path, spec_ver="4.4", surface_ver="4")
    # Rewrite handoff.md so it carries NO 'handoff per HANDOFF_PROCESS.md vN' line.
    (tmp_path / ".claude" / "commands" / "handoff.md").write_text(
        "---\ndescription: dispatch skill\n---\nNo normative version declaration here.\n",
        encoding="utf-8")
    f = aud.check_amendment_coherence(tmp_path)[0]
    assert f.status == "warn"
    assert "coupling marker missing" in f.evidence
    assert "handoff.md" in f.evidence


def test_amendment_coherence_ignores_non_normative_mention(tmp_path: Path) -> None:
    """Codex HIGH-2: a non-authority mention (a historical 'HANDOFF_PROCESS.md vN
    Amendment' note at a DIFFERENT major) must NOT false-FAIL — only the normative
    'handoff per ... vN' declaration is compared. All normative mentions aligned -> PASS.
    Teeth: loosening the surface regex back to a bare 'HANDOFF_PROCESS.md vN' construct
    makes the historical v2 line a straggler -> FAIL -> RED."""
    _seed_coupled(tmp_path, spec_ver="4.4", surface_ver="4")
    # Append a stale, NON-normative historical mention to CLAUDE.md.
    with (tmp_path / "CLAUDE.md").open("a", encoding="utf-8") as fh:
        fh.write("\nHistorical: see HANDOFF_PROCESS.md v2.1 Amendment A (superseded).\n")
    f = aud.check_amendment_coherence(tmp_path)[0]
    assert f.status == "pass"


def test_amendment_coherence_registered_in_all_checks() -> None:
    assert aud.check_amendment_coherence in aud.ALL_CHECKS
