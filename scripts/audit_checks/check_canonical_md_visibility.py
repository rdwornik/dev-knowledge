"""`check_canonical_md_visibility` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL, together with the two canonical-name constants it owns. No logic,
naming, formatting or docstring change; `audit.py` re-exports all three names —
`_CANONICAL_MANDATORY` in particular is read by `tests/test_audit.py` as `aud._CANONICAL_MANDATORY`.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding

# CLOUD-4 v2 (R2 §1.5 GO-b) — canonical filenames come from the one registry.
try:
    from scripts import canonical_docs
except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoints
    import canonical_docs

# Canonical files universally mandatory at repo root (ADR-38 A5 / ADR-51).
# ADR-38 A6 (2026-06-02): the seven-file canonical set is mandatory for every repo.
# CONTRIBUTING/JOURNAL/LESSONS were promoted from optional (A5) to mandatory here so
# cross-repo navigation is identical (the same seven anchors in every repo).
# Kept a LIST, not a tuple: `tests/test_audit.py` reads it as `aud._CANONICAL_MANDATORY`
# and the re-export contract is a name, a value and a type.
_CANONICAL_MANDATORY = list(canonical_docs.CANONICAL_MANDATORY)

# All canonical names whose casing is checked when present (mandatory + optional
# + .dev-knowledge-only). Presence is required only for _CANONICAL_MANDATORY.
_CANONICAL_ALL = list(canonical_docs.CANONICAL_ALL)


def check_canonical_md_visibility(repo_path: Path) -> list[Finding]:
    """Mandatory canonical files present + correct ALL-CAPS casing (ADR-59 D2).

    Requires the seven universal files (ADR-38 A6 / A5 / ADR-51). Optional and
    .dev-knowledge-only canonical files are NOT required, but if present (under any
    casing) they must use the canonical ALL-CAPS spelling — a mis-cased canonical
    file breaks the visual clustering the pattern exists to produce.
    """
    missing = [f for f in _CANONICAL_MANDATORY if not (repo_path / f).exists()]

    canonical_lower = {name.lower(): name for name in _CANONICAL_ALL}
    miscased = []
    for p in repo_path.iterdir():
        if not p.is_file():
            continue
        canonical = canonical_lower.get(p.name.lower())
        if canonical and p.name != canonical:
            miscased.append(f"{p.name} (expected {canonical})")

    if missing:
        return [Finding("canonical_md_visibility", "fail",
                        f"Missing mandatory canonical files: {missing}")]
    if miscased:
        return [Finding("canonical_md_visibility", "fail",
                        f"Mis-cased canonical files: {sorted(miscased)}")]
    return [Finding("canonical_md_visibility", "pass",
                    f"Mandatory canonical files present + correctly cased: {_CANONICAL_MANDATORY}")]
