"""`check_residual_completeness` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL. The `validate_residual_completeness` dual-import is reproduced in
`audit.py`'s `scripts.`-first order and `audit.py` re-exports `_vrc` from here, so
`monkeypatch.setattr(aud._vrc, "find_unfilled", ...)` still reaches this module's `_vrc`.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding

# ARC-5 residual-completeness gate — refuses a bundle shipping a hand-authored FILL-IN region
# still carrying its generator placeholder; same module-import + thin-adapter shape; tests
# monkeypatch `_vrc.find_unfilled`.
try:
    from scripts import validate_residual_completeness as _vrc
except ImportError:
    import validate_residual_completeness as _vrc


def check_residual_completeness(repo_path: Path) -> list[Finding]:
    """ARC-5 residual-completeness gate: a handoff bundle may not ship a hand-authored
    FILL-IN region still carrying the generator's `_(fill: ...)_` placeholder.

    Closes a witnessed failure: the ARC-5 inbound bundle merged with §1 ("THE HEADLINE"),
    §2 and §4 ("the residual's core payload") as literal unfilled templates, and no organ
    objected. The generator scaffolds those regions and cannot author them, so landing-time
    is the only catchable moment.

    FAIL-class (gating, like check_handoff_probes): one FAIL Finding per unfilled region, so
    the #147 ship-gate dispositions each independently.

    Diff-triggered / prospective-only (the check_safe_removal shape + the ADR-101
    grandfathering rule): only bundle files added or modified vs HEAD are scanned; a clean
    tree is an instant PASS. Already-committed bundles are historical artifacts, the same
    reasoning check_handoff_probes uses for validating only the active bundle. Stated
    plainly: this does not retroactively fail the ARC-5 bundle that motivated it, but it
    would have failed the commit that landed it.

    ANTI-BLUFF NON-COLLISION: asserts only that the placeholder was replaced — never that a
    value is present, and never on PROBES.md. A demand for concrete content would push an
    author to write the ship-gate verdict / WARN count / drifted #id that probe P7 and the
    verify_handoff_probes answer-hint rung require to be ABSENT. Full rationale and the two
    pinning tests: scripts/validate_residual_completeness.py.

    Fail-soft on any error (never wedge audit-health). Read-only (Layer 2, ADR-28/36).
    """
    try:
        unfilled = _vrc.find_unfilled(Path(repo_path))
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("residual_completeness", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if not unfilled:
        return [Finding("residual_completeness", "pass",
                        "no unfilled FILL-IN region in changed handoff bundle files")]
    return [
        Finding("residual_completeness", "fail",
                f"{u.path}: FILL-IN region '{u.region}' still carries the generator "
                f"placeholder (a hand-authored residual shipped as a template)".replace("|", "/"))
        for u in unfilled
    ]
