from __future__ import annotations

import os
import re
from pathlib import Path

import decide_checks as dc
import pytest

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


def test_design_audit_passes_subagent_brief_exclusions(tmp_path):
    """Every brief in the design audit names the excluded roots."""
    audit = _only_file("docs/audits/*-technical-design-view.md", "design audit")
    text = audit.read_text(encoding="utf-8")
    section_match = re.search(
        r"(?ms)^## Subagent briefs[ \t]*\r?\n(.*?)(?=^## |\Z)", text)
    assert section_match, "No ## Subagent briefs section found"

    section = section_match.group(1)
    headings = list(re.finditer(r"(?m)^### Brief (?P<number>\d+)[ \t]*$", section))
    brief_files = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(section)
        brief = section[heading.end():end]
        text_block = re.search(r"(?ms)^```text[ \t]*\r?\n(.*?)^```[ \t]*$", brief)
        assert text_block, f"Brief {heading.group('number')} has no fenced text block"
        brief_file = tmp_path / f"brief-{heading.group('number')}.md"
        brief_file.write_text(text_block.group(1), encoding="utf-8")
        brief_files.append(brief_file)

    assert brief_files, "No subagent briefs found"
    assert dc.check_subagent_brief_exclusions(brief_files, repo_root=_REPO) == []


def test_design_audit_evaluators_and_response_coverage():
    """Date-matched evaluator files pass attestation and response coverage checks."""
    prompts_dir = os.environ.get("CLAUDE_PROMPTS_DIR")
    if not prompts_dir:
        pytest.skip("CLAUDE_PROMPTS_DIR is not set")

    audit = _only_file("docs/audits/*-technical-design-view.md", "design audit")
    date_match = re.match(r"(?P<date>\d{4}-\d{2}-\d{2})-", audit.name)
    assert date_match, f"Design audit filename has no leading date: {audit.name}"
    eval_files = [
        Path(prompts_dir) / "to-browser" / f"EVAL-VIEW-E30-{evaluator}-{date_match.group('date')}.md"
        for evaluator in ("sol", "grok")
    ]
    missing = [str(path) for path in eval_files if not path.is_file()]
    if missing:
        pytest.skip(f"Missing evaluator file(s): {', '.join(missing)}")

    assert dc.check_evaluator_attestation(eval_files, "claude-sonnet-5.5") == []
    assert dc.check_response_coverage(eval_files, audit) == []


def test_adr_and_audit_paths_resolve():
    """Every locator in the ADR and design audit resolves in this repository."""
    audit = _only_file("docs/audits/*-technical-design-view.md", "design audit")
    adr = _only_file("docs/decisions/ADR-*-the-system-view.md", "system-view ADR")
    assert dc.check_paths_resolve([audit, adr], repo_root=_REPO) == []
