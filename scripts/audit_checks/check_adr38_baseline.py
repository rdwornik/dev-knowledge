"""`check_adr38_baseline` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL. No logic, naming, formatting or docstring change; `audit.py`
re-exports the name, so `audit.check_adr38_baseline` is the same function object as before.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding

# CLOUD-4 v2 (R2 §1.5 GO-b) — canonical filenames come from the one registry.
try:
    from scripts import canonical_docs
except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoints
    import canonical_docs


def check_adr38_baseline(repo_path: Path) -> list[Finding]:
    """ADR-38 (amendments A5 2026-05-23, A6 2026-06-02) universal governance baseline.

    Checks the governance documents every repo must carry — not code structure.
    The repo-tier system is deprecated, so there is no per-tier branching. Code
    layout (src/, tests/, pyproject.toml) is scoped to code projects per the
    amendment and is NOT part of this universal governance check (governance-only
    repos such as .dev-knowledge have no src/ or pyproject.toml). README.md is
    optional (deprecated from the baseline); CHANGELOG.md was removed by ADR-49.
    CLAUDE.md is covered by check_claude_md, so it is not duplicated here.

    A6 (2026-06-02) promoted CONTRIBUTING.md, JOURNAL.md and LESSONS.md from optional
    to the mandatory seven-file canonical set — superseding the A5 "JOURNAL/LESSONS
    remain repo-specific" line.
    """
    # CLOUD-4 v2 (R2 §1.5 GO-b): the mandatory seven minus CLAUDE.md, derived from the one
    # canonical-doc-name registry rather than retyped. Membership and order are unchanged.
    required_files = list(canonical_docs.ADR38_BASELINE_REQUIRED)

    missing_files = [f for f in required_files if not (repo_path / f).exists()]

    if missing_files:
        status = "fail"
        evidence = f"Missing required: {missing_files}"
    else:
        status = "pass"
        evidence = "All ADR-38 universal governance baseline files present"
    return [Finding("adr38_baseline", status, evidence)]
