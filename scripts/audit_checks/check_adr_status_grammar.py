"""`check_adr_status_grammar` — the `[#242]` ADR status-grammar/enum gate (lane L3).

The thin ADAPTER half of a two-site rule; the logic lives in `scripts/validate_adr_status.py`.
Same module-import + thin-adapter shape as `check_safe_removal` / `check_doc_claims`, and the
same 2-site `multi_site:` declaration those use (`ecosystem/doc-code-edge.yaml`).

NOT YET REGISTERED. This module is deliberately not wired into `ALL_CHECKS` by the lane that
wrote it: `audit.py`, `audit_checks/registry.py` and `ecosystem/doc-code-edge.yaml` are shared
with two sibling lanes in this batch, so the registration ships as a **fenced diff** in
`docs/audits/2026-08-23-technical-lane-status-grammar.md` §Step 4 for the integrator to apply.
Until that diff lands this module is imported by nothing but its tests — dead by design, not
by oversight.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding

try:
    from scripts import validate_adr_status as _vas
except ImportError:
    import validate_adr_status as _vas


# rule: governance-adr-status
def check_adr_status_grammar(repo_path: Path) -> list[Finding]:
    """`[#242]` ADR status coherence: one grammar, a declared enum, header == README index.

    Enforces the `Status:` domain that `docs/decisions/README.md` §"Status enum" DECLARES but
    that nothing checked — that section says in terms *"Nothing checks this enum … a validator
    is available work and is not claimed here."* ADR-94 filed the need, naming header↔README
    coherence and Pattern-B go-forward as the two legs.

    Six rules, armed at two levels because the corpus cannot pass all six today:

      FAIL — `enum` (value outside the declared domain), `single-field` (a file must carry
             exactly one status field). Both measure **0** on the live corpus at merge base
             `aeec0fd1`, so arming them is free and they cannot RED a clean tree.
      WARN — `grammar` (47), `coherence` (3), `wrapped-value` (1), `duplicate-id` (2),
             `unindexed` (0). Arming `grammar` at FAIL would RED-block every commit on day
             one against 47 pre-existing divergences, which is a normalization mandate this
             lane does not hold; the baseline is recorded instead. **A WARN with a recorded
             baseline is a measurement, not a gate** — promoting these legs needs either a
             normalization pass or a ratchet, and neither is claimed here.

    Child-repo-safe: a repo with no `docs/decisions/` yields `n/a` (subject-absent), not a
    FAIL — only the hub carries an ADR corpus.

    HONEST ENFORCEMENT LIMITS — the module's own, restated because they bound what a green
    verdict means:
      * It checks SHAPE and DOMAIN, never correctness. Nothing here says an ADR's status is
        the RIGHT status; `coherence` reports that two surfaces disagree and deliberately does
        not guess which is wrong.
      * The README-index side is PROSE, not a field. The effective status is read from the
        index's free-text Title column via three measured marker forms, defaulting to
        `Accepted` on no marker (the file's own convention). A genuinely status-less row is
        therefore indistinguishable from an Accepted one.
      * `Superseded`/`Deprecated` are carried by ZERO live ADRs, so any archival bar keyed on
        them is unreachable against the live corpus — `[#552]`'s observation, re-measured.
        This check does not fix that; it makes it visible.
      * Read-only (Layer 2). It normalizes nothing and edits no status line. Whether a status
        line MAY be reshaped at all is governed by ADR-94 + standing ruling L-11, not by this
        check.
    """
    decisions = Path(repo_path) / "docs" / "decisions"
    if not decisions.is_dir():
        return [_vas_na("adr_status_grammar")]

    try:
        fields, missing, extra = _vas.scan_zone(decisions)
    except _vas.CorpusUnusable as exc:
        # An unreadable corpus is louder than a defect, never a silent pass. WARN rather than
        # FAIL so a transient read error cannot wedge the audit-health commit gate, matching
        # check_safe_removal's fail-soft posture for its own errors.
        return [Finding("adr_status_grammar", "warn",
                        f"corpus unusable: {exc}".replace("|", "/"))]

    defects = _vas.corpus_defects(fields, missing, extra)
    defects += _vas.duplicate_id_defects(fields)

    readme = decisions / "README.md"
    if readme.is_file():
        headers: dict[str, str] = {}
        for f in fields:
            num = _vas.adr_number(f.path)
            if num:
                headers.setdefault(num, f.value or f.raw[:40])
        defects += _vas.coherence_defects(
            headers,
            _vas.index_effective_status(readme.read_text(encoding="utf-8", errors="replace")))

    fails = [d for d in defects if d.rule in _vas.FAIL_RULES]
    warns = [d for d in defects if d.rule not in _vas.FAIL_RULES]

    if fails:
        ev = f"{len(fails)} blocking defect(s): " + "; ".join(
            f"{d.rule} {d.subject} — {d.detail}" for d in fails[:8])
        if len(fails) > 8:
            ev += f" (+{len(fails) - 8} more)"
        return [Finding("adr_status_grammar", "fail", ev.replace("|", "/"))]

    if warns:
        counts: dict[str, int] = {}
        for d in warns:
            counts[d.rule] = counts.get(d.rule, 0) + 1
        ev = (f"{len(fields)} ADR status field(s); 0 enum/single-field defects; "
              f"baseline WARNs: "
              + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
        return [Finding("adr_status_grammar", "warn", ev.replace("|", "/"))]

    return [Finding("adr_status_grammar", "pass",
                    f"{len(fields)} ADR status field(s): one grammar, declared enum, "
                    f"header == README index")]


def _vas_na(name: str) -> Finding:
    """`n/a` with the machine-readable subject-absent reason (the `_common._na` contract)."""
    from ._common import _NA_SUBJECT_ABSENT, _na
    return _na(name, _NA_SUBJECT_ABSENT,
               "no docs/decisions/ in this repo — only the hub carries an ADR corpus")
