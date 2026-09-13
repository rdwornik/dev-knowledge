"""`check_safe_removal` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL. The `safe_remove` dual-import is reproduced in `audit.py`'s
`scripts.`-first order and `audit.py` re-exports `_sr` from here, so
`monkeypatch.setattr(aud._sr, "check_removal", ...)` still reaches this module's `_sr`.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding

# #195 code→code safe-removal gate (consumes the #193 reverse-dep oracle) — same module-import
# + thin-adapter shape as the validators above; tests monkeypatch `_sr.check_removal`.
try:
    from scripts import safe_remove as _sr
except ImportError:
    import safe_remove as _sr


def check_safe_removal(repo_path: Path) -> list[Finding]:
    """#195 code->code safe-removal gate: removing a scripts/ module while a live EXTERNAL
    referrer still uses one of its top-level symbols FAILs, naming the referrer. The consumer
    that gives the #193 reverse-dep oracle teeth (GAP-1) and the automated form of the manual
    "scan references before cutting" (LESSONS 2026-06-03) — guards the 2026-03-14 bulk-restore
    failure class (removing still-needed files).

    Diff-triggered: a clean tree (no scripts/*.py deletion vs HEAD) is an instant PASS — no
    Pyright cost. On an actual removal, safe_remove.check_removal materializes a query root
    (working scripts/ + removed module(s) restored from HEAD) and queries the oracle there.

    FAIL-class (gating, like check_handoff_probes): one FAIL Finding per SURVIVING referrer so
    the #147 ship-gate dispositions each independently. The oracle's inability to verify (Pyright
    absent -> oracle-unavailable, or an `ambiguous` symbol) is a single WARN — fail-OPEN + ALLOW
    (operator ruling #195), never a synthesized FAIL. Check's own error -> WARN (fail-soft, never
    wedge audit-health). RESOLVE-ONLY / read-only (Layer 2): the oracle spawns Pyright for
    analysis and writes only a temp dir; this writes no repo files. Logic lives in
    scripts/safe_remove.py.

    HONEST LIMIT (inherited from the oracle): static-Python-only. Dynamic/getattr/string-keyed/
    cross-language referrers are INVISIBLE -> a non-blocking false PASS is possible here, never a
    false FAIL. The reliable catch is the pre-removal CLI (queries the live repo); the automatic
    build-time path's cross-module fidelity depends on Pyright resolving the materialized copy.
    """
    try:
        verdict = _sr.check_removal(Path(repo_path))
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("safe_removal", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if verdict.status == "safe" and not verdict.removal_set:
        return [Finding("safe_removal", "pass", "no scripts/*.py module removal in the diff")]
    findings: list[Finding] = []
    # One FAIL per surviving referrer (atomic disposition unit) — the load-bearing block.
    for r in verdict.surviving_referrers:
        findings.append(Finding(
            "safe_removal", "fail",
            (f"{r['referrer']}:{r['line']} still references {r['symbol']} from removed "
             f"{r['module']} — co-remove the referrer or keep the module").replace("|", "/")))
    # All unverifiable symbols collapse to ONE WARN (honest static-only limit; allow).
    if verdict.unverifiable:
        reasons = ", ".join(sorted({u["reason"] for u in verdict.unverifiable}))
        findings.append(Finding(
            "safe_removal", "warn",
            (f"{len(verdict.unverifiable)} symbol(s) unverifiable ({reasons}) for removal of "
             f"{', '.join(verdict.removal_set)} — WARN+allow, static-only limit").replace("|", "/")))
    # A SAFE verdict downgraded to REVIEW on a bare-stem string-literal hit — one WARN naming
    # every hit site (same collapse shape as `unverifiable` above; never a block).
    if verdict.status == "review":
        sites = ", ".join(f"{h['file']}:{h['line']}" for h in verdict.review_hits)
        findings.append(Finding(
            "safe_removal", "warn",
            (f"removal of {', '.join(verdict.removal_set)} downgraded from SAFE to REVIEW — "
             f"bare stem found as a string literal at {sites} (possible dynamic/string-keyed "
             f"reference the oracle cannot see)").replace("|", "/")))
    if findings:
        return findings
    return [Finding("safe_removal", "pass",
                    (f"removal of {', '.join(verdict.removal_set)} has no surviving referrers")
                    .replace("|", "/"))]
