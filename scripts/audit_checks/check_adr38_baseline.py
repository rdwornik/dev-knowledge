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
    repos such as .dev-knowledge have no src/ or pyproject.toml). CHANGELOG.md was
    removed by ADR-49. CLAUDE.md is covered by check_claude_md, so it is not
    duplicated here.

    README.md — decommissioned docstring claim, ADR-114 `Decommission` item (c),
    executed by [#614] lane-b. This docstring read "README.md is optional
    (deprecated from the baseline)" until 2026-08-29. A5's deprecation is
    SUPERSEDED by ADR-114 (Accepted 2026-08-29) in that single respect: the hub's
    root README.md is recreated and supersedes VISION.md as the canonical purpose
    document. The check's BEHAVIOUR is deliberately unchanged — README.md is not in
    ADR38_BASELINE_REQUIRED, so its absence still does not fail here, because only 2
    of the 8 ADR-104 children carry one and this check runs fleet-wide. Promoting it
    into canonical_docs.CANONICAL_MANDATORY is the sequenced fleet migration
    (ADR-114 option (C)), not a docstring fix. So: no longer "deprecated", not yet
    "required" — optional to the FLEET, canonical at the HUB.

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
