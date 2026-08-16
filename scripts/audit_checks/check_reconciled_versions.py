"""`check_reconciled_versions` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL. The `# rule: coherence-spec-reconciled` annotation above the `def`
travels with it. The `validate_reconciliation` dual-import is reproduced in `audit.py`'s
`scripts.`-first order and `audit.py` re-exports `_vr` from here, so
`monkeypatch.setattr(aud._vr, ...)` and this module's `_vr` remain the SAME module object.
"""

from __future__ import annotations

from pathlib import Path

from ._common import _na, Finding

# Coherence-spine reconciliation checker — same module-import + thin-adapter shape.
try:
    from scripts import validate_reconciliation as _vr
except ImportError:
    import validate_reconciliation as _vr


# rule: coherence-spec-reconciled
def check_reconciled_versions(repo_path: Path) -> list[Finding]:
    """Coherence-spine reconciliation gate: a dependent's declared `reconciled_with`
    version must match the spec's CURRENT (live) version.

    A dependent doc declares `reconciled_with: <spec-id>@<version>` in its frontmatter;
    the checker resolves the spec via the registry (validate_reconciliation._SPEC_REGISTRY),
    reads its version LIVE, and compares. In v1 exactly one edge is declared
    (docs/handoffs/README.md -> handoff-process). Generic: a child repo with no
    `reconciled_with` edge is a no-op PASS, so this no-ops on the fleet.

    FAIL-class (gating) on a version mismatch — fail-closed: a dependent still claiming an
    old spec version is the drift this exists to block. One Finding per mismatch so the
    #147 ship-gate dispositions each independently (same contract as git_backlog_drift /
    handoff_probes). A checker that cannot read its OWN inputs (malformed frontmatter,
    unknown spec-id, spec absent/unparseable) -> WARN: fail-OPEN on its own error, never a
    synthesized FAIL. Fail-soft on any unexpected error. Read-only. Logic lives in
    scripts/validate_reconciliation.py.

    The mismatch remediation points at the re-stamp flow (run check-against-spec, then bump
    reconciled_with) — but this gate gates the VERSION MISMATCH only. Running or passing
    check-against-spec is DELIBERATELY never a gate condition here: the semantic skill is
    triggered by the re-stamp flow, not the ship-gate (check-against-spec v1 scope). #205.
    """
    try:
        results = _vr.reconcile(Path(repo_path))
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("reconciled_versions", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    findings: list[Finding] = []
    for r in results:
        if r.status == "mismatch":
            findings.append(Finding("reconciled_versions", "fail",
                (f"{r.dependent_path} declares {r.spec_id}@{r.declared} but spec is "
                 f"{r.current} - re-stamp flow: run check-against-spec "
                 f"(py scripts/validate_reconciliation.py emits the invocation), then "
                 f"bump reconciled_with").replace("|", "/")))
        elif r.status in ("malformed", "unknown-spec"):
            findings.append(Finding("reconciled_versions", "warn",
                (f"{r.dependent_path}: {r.status} ({r.current})").replace("|", "/")))
    if findings:
        return findings
    n = len(results)
    # Status follows the BRANCH, not the call site ([#465] leg 1): edges that were checked and
    # matched are a real `pass`; zero declared edges is a skip and must not borrow that pass.
    if n:
        return [Finding("reconciled_versions", "pass",
                        f"{n} reconciled_with edge(s) match live spec version(s)")]
    return [_na("reconciled_versions", "NOT-APPLICABLE", "no reconciled_with edges declared")]
