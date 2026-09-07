"""`check_adr_status_grammar` — the `[#242]` ADR status-grammar/enum gate (lane L3).

The thin ADAPTER half of a two-site rule; the logic lives in `scripts/validate_adr_status.py`.
Same module-import + thin-adapter shape as `check_safe_removal` / `check_doc_claims`, and the
same 2-site `multi_site:` declaration those use (`ecosystem/doc-code-edge.yaml`).

REGISTERED SINCE. The fenced registration diff this module originally shipped for the
integrator to apply — `docs/audits/2026-08-23-technical-lane-status-grammar.md` §Step 4 — has
landed: `audit_checks/registry.py` carries the import and the `ALL_CHECKS` membership, and
`audit.py` tiers it at `TIER_COMMIT`. The check therefore BLOCKS a commit on a FAIL, which is
what makes each leg's arming level (FAIL vs WARN) a live decision rather than a report format.
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

    Nine rules, armed at two levels because the corpus cannot pass all nine today:

      FAIL — `enum` (value outside the declared domain), `single-field` (a file must carry
             exactly one status field). Both measure **0** on the live corpus at merge base
             `aeec0fd1`, so arming them is free and they cannot RED a clean tree.
             Two REQUIRED-SECTION legs join them: `flip-condition` (an ADR above the
             grandfather mark that does not name the condition under which its decision
             reverses) and `alternatives-considered` (one that justifies nothing it did not
             choose — operator ruling DECLARE-F-2-2026-09-07 §A, thesis T-04). Both measure
             **0** at arming, because the one ADR above the mark carries both sections.
      WARN — the same two defects on an ADR at or below the mark:
             `flip-condition-legacy` (**89** of 90 live ADRs — only ADR-117 names its flip)
             and `alternatives-considered-legacy` (**32** of 90). Each detail carries a
             per-file disposition path. Arming those populations at FAIL would wedge every
             commit in the repo against pre-existing files, which is an outage rather than
             enforcement.
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
    defects += _vas.duplicate_id_defects(fields, missing)
    # The REQUIRED-SECTION legs. They re-read the same files rather than riding `scan_zone`'s
    # parse, because `scan_zone` returns status FIELDS and discards the text a section rule
    # needs; the alternative was widening its return type for one caller. `CorpusUnusable` from
    # here is caught by the same handler above — the zone was already proved readable, so this
    # raises only on a race, and a race must not escape as an unhandled OSError.
    try:
        defects += _vas.required_section_defects(decisions)
    except _vas.CorpusUnusable as exc:
        return [Finding("adr_status_grammar", "warn",
                        f"corpus unusable (required-section legs): {exc}".replace("|", "/"))]

    # The index is HALF this check's subject ([#242]'s Done-when leg). An absent or unreadable
    # README must therefore be loud: returning `pass` while the coherence leg silently did not
    # run is the vacuous pass this gate exists to prevent (terra HIGH-5). The read is inside
    # the guarded path so a race between `is_file()` and `read_text` cannot escape as an
    # unhandled OSError either.
    readme = decisions / "README.md"
    index_error = ""
    try:
        index = _vas.index_effective_status(readme.read_text(encoding="utf-8", errors="replace"))
    except OSError as exc:
        index, index_error = {}, f"ADR index unreadable ({exc}) — coherence leg DID NOT RUN"

    if not index_error:
        defects += _vas.coherence_defects(_vas.header_status_map(fields, missing), index)

    fails = [d for d in defects if d.rule in _vas.FAIL_RULES]
    warns = [d for d in defects if d.rule not in _vas.FAIL_RULES]

    def _tally(defects_: list) -> str:
        counts: dict[str, int] = {}
        for d in defects_:
            counts[d.rule] = counts.get(d.rule, 0) + 1
        return ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "none"

    if fails:
        # The FAIL evidence carries the WARN tally and any index error TOO. Reporting only the
        # blocking defects silently discarded every other governance defect the run had
        # already computed, so a FAIL made the rest invisible (terra R7-HIGH-3). The Finding
        # STATUS stays `fail` — this widens the evidence, not the verdict.
        ev = f"{len(fails)} blocking defect(s): " + "; ".join(
            f"{d.rule} {d.subject} — {d.detail}" for d in fails[:8])
        if len(fails) > 8:
            ev += f" (+{len(fails) - 8} more)"
        ev += f" || also detected: {_tally(warns)}"
        if index_error:
            ev += f" || {index_error}"
        return [Finding("adr_status_grammar", "fail", ev.replace("|", "/"))]

    if warns or index_error:
        ev = (f"{len(fields)} ADR status field(s); 0 enum/single-field defects; "
              f"baseline WARNs: " + _tally(warns))
        if index_error:
            ev += f" | {index_error}"
        return [Finding("adr_status_grammar", "warn", ev.replace("|", "/"))]

    return [Finding("adr_status_grammar", "pass",
                    f"{len(fields)} ADR status field(s): one grammar, declared enum, "
                    f"header == README index")]


def _vas_na(name: str) -> Finding:
    """`n/a` with the machine-readable subject-absent reason (the `_common._na` contract)."""
    from ._common import _NA_SUBJECT_ABSENT, _na
    return _na(name, _NA_SUBJECT_ABSENT,
               "no docs/decisions/ in this repo — only the hub carries an ADR corpus")
