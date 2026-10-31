from __future__ import annotations

import re
from pathlib import Path

import decide_checks as dc

_REPO = Path(__file__).resolve().parents[1]


def _only_file(pattern: str, label: str) -> Path:
    """Return the sole repository file matching a design artifact pattern."""
    matches = list(_REPO.glob(pattern))
    assert matches, f"No {label} found matching {_REPO / pattern}"
    assert len(matches) == 1, f"Expected exactly one {label}; found {len(matches)}"
    return matches[0]


def test_adr_exists():
    """The system-view decision has exactly one ADR file."""
    adr_files = list((_REPO / "docs" / "decisions").glob("ADR-*-the-system-view.md"))
    assert adr_files, "No system-view ADR found in docs/decisions/"
    assert len(adr_files) == 1, f"Expected exactly one system-view ADR; found {len(adr_files)}"
    assert adr_files[0].is_file()


def test_adr_status_is_proposed():
    """The system-view ADR remains proposed before ratification."""
    adr = _only_file("docs/decisions/ADR-*-the-system-view.md", "system-view ADR")
    text = adr.read_text(encoding="utf-8")
    assert re.search(r"^- \*\*Status:\*\* Proposed\b", text, re.MULTILINE)


def test_adr_has_decide_sections():
    """The ADR includes all required decision and quality-attribute sections."""
    adr = _only_file("docs/decisions/ADR-*-the-system-view.md", "system-view ADR")
    assert dc.check_adr_sections(adr) == []


def test_design_audit_exists_and_has_decide_sections():
    """Design evidence includes the required decide artifacts."""
    audit = _only_file("docs/audits/*-technical-design-view.md", "design audit")
    text = audit.read_text(encoding="utf-8")
    assert "## Subagent briefs" in text
    assert "## Subagent claims" in text
    assert re.search(r"(?m)^Weights:", text)
    assert re.search(r"pre-mortem", text, re.IGNORECASE)


def test_design_audit_passes_matrix_and_claims_checks():
    """The design audit has a valid matrix and verifiable subagent claims."""
    audit = _only_file("docs/audits/*-technical-design-view.md", "design audit")
    assert dc.check_matrix(audit) == []
    assert dc.check_subagent_claims(audit) == []


def test_adr_and_audit_paths_resolve():
    """Every locator in the ADR and design audit resolves in this repository."""
    audit = _only_file("docs/audits/*-technical-design-view.md", "design audit")
    adr = _only_file("docs/decisions/ADR-*-the-system-view.md", "system-view ADR")
    assert dc.check_paths_resolve([audit, adr], repo_root=_REPO) == []
