"""`check_adr38_baseline` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL. No logic, naming, formatting or docstring change; `audit.py`
re-exports the name, so `audit.check_adr38_baseline` is the same function object as before.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding


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
    required_files = ["VISION.md", "ARCHITECTURE.md", "BACKLOG.md",
                      "CONTRIBUTING.md", "JOURNAL.md", "LESSONS.md"]

    missing_files = [f for f in required_files if not (repo_path / f).exists()]

    if missing_files:
        status = "fail"
        evidence = f"Missing required: {missing_files}"
    else:
        status = "pass"
        evidence = "All ADR-38 universal governance baseline files present"
    return [Finding("adr38_baseline", status, evidence)]
