<!-- scope: meta -->

# ADR-64 — BACKLOG.md architecture: lean active file, status-priority taxonomy, per-repo routing, narrow schema validator

**Status:** Accepted — 2026-06-01, via AI Council debate (pick mode, 4-model panel + openai synthesizer, 2 rounds).
**Transcript:** `docs/decisions/transcripts/council-out-20260601_103339-pick-council-backlog-architecture-2026-05-31.md`
**Supersedes/amends:** reconciles PLAYBOOK §10 to ADR-47; does **not** revive `BACKLOG_ARCHIVE.md` (CLAUDE.md §5 stands).
**Related:** ADR-39 (living-files), ADR-41 (backlog architecture / per-repo ownership), ADR-47 (organization / done-items-leave), ADR-48 (audit-admission rule). Diagnosis: `docs/audits/2026-05-31-backlog-architecture-diagnosis.md`.

## Context

`BACKLOG.md` had reached 871 lines / 107 entries (66 open, 41 done retained in-place), with named-stream sections routing only 15% of open items and 56% living in four session-arc-named sections. The operator (ADHD/autism; priority-one actionable surface) could not identify next actions at a glance. The diagnosis established the root cause as a **methodology contradiction** (PLAYBOOK §10 teaches an archive flow ADR-47 retired and CLAUDE.md §5 forbids), not a grooming lapse — so fixing the file without fixing the contradiction would re-bloat it. A four-axis Council debate was convened to decide the architecture.

## Decision

1. **Done-item disposition — remove (Q1-A).** Done items leave `BACKLOG.md`; git history (closing commit SHAs + dates, already embedded) is the record. No collapsed stubs, no archive file. This *is* the existing ADR-47 convention; in-file retention was drift.

2. **Section taxonomy — status-and-priority with a coordination carveout (Q2-A).** Sections become `## Now` · `## Open — P1` · `## Open — P2` · `## Open — P3` · `## Blocked` · `## Coordination`. Named-stream (A/B/C/D) and session-arc sections are **retired as headers**; repo affiliation survives as a `repo:` entry field, not a section.

3. **Existing child-repo items — relocate (Q3-A).** The ~20 child-repo *execution* items move to their target repos' BACKLOGs, after per-item triage: execution → child repo; genuine cross-repo governance/coordination → kept in `.dev-knowledge` as a pointer, never a duplicate task. **Relocation is execution in child repos → separate sessions in those repos (ADR-41); not directed from `.dev-knowledge`.**

4. **Schema enforcement — restore + narrow read-only validator (Q4-B, narrow).** Restore the rigid entry schema and the `open/in-progress/blocked/done` vocabulary. Add `scripts/validate_backlog.py` (read-only, Layer-2 compliant). **Hard-fail** on objective violations only: invalid status word, missing required fields, any `done` entry present, malformed structure. **Warning-only** (never block) on `## Now` size/staleness. *This was the one non-consensus axis (4-A dissent on a strict ADR-48 reading); 4-B-narrow adopted because the schema/vocabulary drift is already documented and manual discipline is a stated non-viable constraint.*

## Consequences

- The active file drops from 107 entries to ~46 (purge 41 done + relocate ~20 child-repo), small enough that priority grouping works without sub-streams.
- **Migration is execution** — incremental, one revertable commit per batch (purge / relocate / restructure / validator). Not a big-bang. Done in a follow-on CC session, not auto-executed.
- **PLAYBOOK §10 must be reconciled** (strike the forbidden `BACKLOG-archive/` line; set disposition to "done items leave"; fix vocabulary) — the unambiguous parts are Path-A; the disposition wording is now settled by this ADR.
- BACKLOG line 70 ("stream taxonomy / 33% kill-criterion") is **obsolete** (kill criterion withdrawn in ADR-48) and is subsumed by this decision.

### Open implementation questions — resolve in the migration spec BEFORE editing the file
The debate flagged these as unresolved; pinning them is a prerequisite (resolving the schema before editing avoids a partial fix):
1. Child-repo migration mechanics — triage rule, backlink/cross-ref format, split-brain avoidance, the coordination-pointer rule.
2. Exact minimal schema — required fields; whether `repo:` is required on all entries; whether `## Blocked` replaces or coexists with `status: blocked` (no double-listing).
3. `## Now` mechanics — pointers vs full entries; seed count; refresh trigger; soft-limit number; staleness age.
4. Whether `in-progress` gets its own surface or `## Now` is the in-progress/next surface.

### Signals to revisit
- `git log` retrospection of done items becomes frequent pain → add a **read-only generated "recently done" view** (not a managed archive).
- `## Now` consistently empty/stale >30 days → the curated-surface model isn't working; reconsider.
- Active file grows past ~80 open items → check for items leaking back from child repos, or whether `repo:` needs to become structure.
- Validator false-positive rate exceeds ~10% of `BACKLOG.md`-touching commits → loosen rules before disabling.
