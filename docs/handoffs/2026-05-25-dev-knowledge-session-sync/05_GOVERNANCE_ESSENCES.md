# Governance Essences — 2026-05-25-dev-knowledge-session-sync

<!-- scope: meta -->

Operational essences for the ADRs explicitly cited in `07_ACTION_PLAN.md`.
These are 2-4 sentence summaries, NOT full ADR text. Read the full ADR in the
repo (path given) before acting on anything load-bearing.

---

## ADR-42 — Handoff Format v3

Defines the live handoff convention: three-stage flow (Stage 1 question →
Stage 2 architect response → Stage 3 folder generation) producing a flat
multi-file bundle that carries full VISION/PLAYBOOK/ESSENTIALS invariant copies
plus a SHA-256 manifest. This is the canonical authority for handoffs and
remains in force (ADR-45 did not supersede it). Operational mechanics live in
`protocols/HANDOFF_PROCESS.md` (currently v3.3.3).

Full ADR: `docs/decisions/ADR-42-handoff-format-v3.md`

## ADR-45 — Handoff Architecture v4 (explored, NOT adopted)

A v4 design that explored collapsing the bundle and rewriting the mechanical
gates; it was rolled back the same night it was attempted and never adopted.
Its `Supersedes: ADR-42` header claim was formally **withdrawn 2026-05-25**
(strikethrough + Amendment block preserve the record). ADR-45 supersedes
nothing and stands as a frozen design exploration. Any future bundle-consolidation
decision must explicitly re-open ADR-45 (amend it, or supersede ADR-42 with a
new ADR) — it is not a routine template edit.

Full ADR: `docs/decisions/ADR-45-handoff-architecture-v4.md`

## ADR-49 — Consolidate Past-Recording Files

Retires `CHANGELOG.md` (and `BACKLOG_ARCHIVE.md`) from this repo; the JOURNAL
`Changes:` line plus git history replace the CHANGELOG. Any lingering
"append … CHANGELOG" instruction in living docs is residual drift and should be
struck (see Directive 5, `protocols/SESSION_SETUP.md:209`).

Full ADR: `docs/decisions/ADR-49-consolidate-past-recording-files.md`

## ADR-28 — Three-Layer Architecture (Layer-2-never-executes)

Establishes the three-layer ecosystem model in which `.dev-knowledge` is
Layer 2: governance/methodology, not execution. Layer 2 never runs orchestration
scripts — `scripts/` holds read-only validators only. This underpins BOUNDARY 4
("add no orchestration scripts").

Full ADR: `docs/decisions/ADR-28-three-layer-architecture.md`
