"""`check_canonical_structure` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL, together with `_CANONICAL_SPINE` and the `_heading_present` helper it
exclusively owns. No logic, naming, formatting or docstring change; `audit.py` re-exports all
three names — `scripts/boundary_report.py` reads `audit._CANONICAL_SPINE`.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding

# CLOUD-4 v2 (R2 §1.5 GO-b) — canonical filenames come from the one registry.
try:
    from scripts import canonical_docs
except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoints
    import canonical_docs


# ADR-38 A6 (2026-06-02): the universal [U] heading spine each canonical file must
# carry. Presence-only (not strict order) — child-repo-safe; the [R]/[C] sections
# (repo-specific / conditional) vary per repo and are deliberately NOT asserted.
# A heading matches if any line .startswith() the substring, so a repo's own H1 suffix
# (e.g. "# Journal - ai-council") still matches. The substrings are taken from
# .dev-knowledge's own canonical files, so the self-only health gate passes by
# construction. BACKLOG.md hierarchy beyond "## Big picture" is covered by
# validate_backlog.py, not duplicated here.
# The spine bodies are unchanged; only their KEYS now come from the registry, so a
# canonical-filename decision moves the key together with the value it addresses.
_CANONICAL_SPINE = {name: list(spine) for name, spine in canonical_docs.CANONICAL_SPINE.items()}


def _heading_present(lines: list[str], heading: str) -> bool:
    """True if some line IS `heading` or continues it past a word boundary.

    Boundary-aware so a repo-specific suffix matches but a near-miss does not:
    `## Purpose [CORE]` and `# Journal - ai-council` satisfy `## Purpose` / `# Journal`,
    while `## Visionary` and `# Journalized` do NOT satisfy `## Vision` / `# Journal`
    (the char after the heading must be absent or a non-word boundary, not a letter or
    digit). Closes Codex review HIGH 2026-06-02 (startswith false-pass).
    """
    n = len(heading)
    for line in lines:
        if not line.startswith(heading):
            continue
        rest = line[n:]
        if rest == "" or not (rest[0].isalnum() or rest[0] == "_"):
            return True
    return False


def check_canonical_structure(repo_path: Path) -> list[Finding]:
    """Each present canonical file carries its [U] heading spine (ADR-38 A6).

    Asserts the universal navigation backbone only — presence of required headings,
    not their order, and not the [R]/[C] sections that legitimately vary per repo. A
    canonical file that is ABSENT is not flagged here (presence is owned by
    check_adr38_baseline / check_canonical_md_visibility); this check validates the
    shape of files that exist. Read-only and child-repo-safe: a not-yet-unified repo
    FAILs, surfacing the structural gap without blocking .dev-knowledge (health is
    self-only).
    """
    missing: list[str] = []
    for fname, required in _CANONICAL_SPINE.items():
        fpath = repo_path / fname
        if not fpath.exists():
            continue
        lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
        for heading in required:
            if not _heading_present(lines, heading):
                missing.append(f"{fname}: {heading!r}")
    if missing:
        return [Finding("canonical_structure", "fail",
                        f"Canonical file(s) missing required spine heading(s): {missing}")]
    return [Finding("canonical_structure", "pass",
                    "All present canonical files carry their required [U] spine headings")]
