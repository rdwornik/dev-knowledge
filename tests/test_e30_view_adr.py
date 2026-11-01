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


def _transport_eval_files() -> list[Path]:
    """The date-matched EVAL files on the operator transport, or [] when it is not there."""
    prompts_dir = os.environ.get("CLAUDE_PROMPTS_DIR")
    audits = list(_REPO.glob("docs/audits/*-technical-design-view.md"))
    if not prompts_dir or len(audits) != 1:
        return []
    date_match = re.match(r"(?P<date>\d{4}-\d{2}-\d{2})-", audits[0].name)
    if not date_match:
        return []
    files = [
        Path(prompts_dir) / "to-browser" / f"EVAL-VIEW-E30-{evaluator}-{date_match.group('date')}.md"
        for evaluator in ("sol", "grok")
    ]
    return files if all(path.is_file() for path in files) else []


@pytest.mark.skipif(
    not _transport_eval_files(),
    reason=(
        "EVAL records live on the operator transport (CLAUDE_PROMPTS_DIR); CI has none. "
        "Run locally with CLAUDE_PROMPTS_DIR set to gate evaluator attestation and response coverage."
    ),
)
def test_design_audit_evaluators_and_response_coverage():
    """Date-matched evaluator files pass attestation and response coverage checks."""
    audit = _only_file("docs/audits/*-technical-design-view.md", "design audit")
    eval_files = _transport_eval_files()
    assert eval_files, "evaluator files vanished after collection"
    assert dc.check_evaluator_attestation(eval_files, "claude-sonnet-5.5") == []
    assert dc.check_response_coverage(eval_files, audit) == []


_BARE_LOCATOR = re.compile(r"(?<![\w/.-])((?:[\w.-]+/)*[\w.-]+\.(?:py|md|yaml|yml|json|toml|txt|ps1)):(\d+)(?!\d)")


def test_adr_and_audit_paths_resolve():
    """Every locator in the ADR and design audit resolves in this repository.

    The decide check reads backtick-marked locators only; the ADR and audit cite most of theirs
    as bare prose (`path:line`), so this test also resolves those directly: the file exists and
    has at least that many lines.
    """
    audit = _only_file("docs/audits/*-technical-design-view.md", "design audit")
    adr = _only_file("docs/decisions/ADR-*-the-system-view.md", "system-view ADR")
    assert dc.check_paths_resolve([audit, adr], repo_root=_REPO) == []

    seen = 0
    unresolved: list[str] = []
    for doc in (audit, adr):
        for match in _BARE_LOCATOR.finditer(doc.read_text(encoding="utf-8")):
            rel, line = match.group(1), int(match.group(2))
            target = _REPO / rel
            if not target.is_file():
                # a named file the lane itself does not own, or a transport path: not a repo locator
                if rel.startswith(("to-browser/", "to-cc/")):
                    continue
                unresolved.append(f"{doc.name}: {rel}:{line} (no such file)")
                continue
            seen += 1
            if sum(1 for _ in target.open(encoding="utf-8", errors="replace")) < line:
                unresolved.append(f"{doc.name}: {rel}:{line} (file is shorter)")
    assert seen > 0, "no bare path:line locator was found; the pattern no longer matches the documents"
    assert unresolved == []
