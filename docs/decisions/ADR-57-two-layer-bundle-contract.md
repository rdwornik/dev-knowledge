# ADR-57: Two-layer bundle contract

- **Status:** Accepted
- **Date:** 2026-05-26
- **Related:** ADR-42 (handoff format v3 — extends its invariant-only bundle rule), ADR-49 (JOURNAL convention — operational-layer source), `protocols/HANDOFF_PROCESS.md`
- **Decommission:** none (additive — existing invariant floor unchanged; operational layer added)
- **Source:** AI Council debate Q2, 2026-05-26 — `docs/decisions/transcripts/council-out-20260526_143605-pick-2026-05-25-handoff-council-Q2-bundle-content-composition.md` (Recommended Decision L840-884; Action Items L910-936)

## Context

The current bundle ships full VISION/PLAYBOOK/ESSENTIALS (the invariant floor) but
not skills, gotchas, or JOURNAL slices.

- `docs/research/2026-05-25-handoff-failures-evidence.md` records the operator's
  tension: removing PLAYBOOK/ESSENTIALS breaks prompt generation ("bez playbooka
  i bez essentials prompty są źle generowane"), yet the operator also argued the
  load-bearing artifacts for execution are skills/gotchas/JOURNAL "wtedy kiedy
  jest to potrzebne" (when needed).
- The bundle does two different jobs: PLAYBOOK/ESSENTIALS drive normative
  alignment + prompt generation; skills/gotchas/JOURNAL support execution. The
  current contract only covers the first.

A pure fixed-union model adds the missing artifacts but is unbounded; a pure
per-session selection model over-trusts the sender and weakens drift detection.

## Decision

Adopt a **two-layer bundle contract**.

- **Governance floor (unconditional, every handoff):** VISION, PLAYBOOK,
  ESSENTIALS. Full copies. Prevents norm hallucination; preserves drift detection.
- **Operational layer (scoped to declared next-session scope):** relevant skills,
  gotchas, and JOURNAL slices — selected by a published, table-driven mapping, not
  ad-hoc sender judgment.
- **`next_session_scope` field** added to the bundle, from a controlled
  vocabulary: `code-implementation`, `architecture-decision`, `audit-work`,
  `documentation`, `mixed-uncertain` (fail-safe → treat as worst-case / full).
- **Scope → artifact mapping table** ships with this rule change (defined in
  `HANDOFF_PROCESS.md` and `HANDOFF_FOLDER_TEMPLATE.md`).
- skills/gotchas/JOURNAL are added to the **formal bundle inventory** under the
  operational layer.

The full invariant floor is preserved now; the bundle-size/attention concern is
delegated to Q5 (ADR-42 amendment), which keeps full copies and adds integrity
tracking rather than shrinking the payload.

## Consequences

- The bundle now carries execution-support artifacts scoped to the next session's
  declared work, instead of omitting them entirely.
- Drift detection and norm-anchoring (the only empirically-working safeguards) are
  untouched.
- A controlled scope vocabulary + mapping table replaces ad-hoc curation.
- The bundle may remain heavy until Q5 delivery improvements — accepted; Q5 keeps
  full invariants by decision, so size is managed by integrity tracking, not
  removal.
- Bundle inventory grows: floor (3 invariants) + per-scope operational artifacts.

## Risks (from Q2 risk register, L886-908)

- **Context crowding persists near-term** → mark Q5 urgent; measure token load +
  failure rates.
- **Scope mapping wrong/incomplete** → start with the small enumerated set above;
  log misses; revise quickly.
- **Casual scope selection recreates ad-hoc curation** → require declared scope
  from the controlled vocabulary + checklist-derived inclusions.
- **Operational layer becomes a dumping ground** → no free-form additions without
  updating the mapping table/ADR.
- **Fixed floor preserved formally but ignored due to size** → instrument
  prompt-quality regressions, drift incidents, operator size complaints,
  evidence that receivers miss present rules.

## Alternatives considered

- **Pure fixed-union** (always ship everything) — rejected: unbounded growth.
- **Pure per-session selection** (sender picks all content) — rejected:
  over-trusts sender, weakens drift detection where evidence is strongest.

## Trace

Scope vocabulary is intentionally small and conservative at launch; expand only by
amending the mapping table here + in `HANDOFF_PROCESS.md`. Q2 AI7 factual
dependency (does prompt-gen tooling need PLAYBOOK/ESSENTIALS physically in-bundle?)
resolved: browser chat cannot read the filesystem → in-bundle required.

---

## Amendment 2026-05-29 — evidence file relocation

> Append-only reference correction per ADR-39 (immutable body preserved). Grounds:
> `docs/audits/2026-05-29-handoff-v3.4-process-audit.md` finding E1.

The Context section above cites the empirical-basis evidence file at
`docs/research/2026-05-25-handoff-failures-evidence.md`. That file was relocated to
**`docs/archive/2026-05-25-handoff-failures-evidence.md`** by the 2026-05-28
ADR-60 archive triage. The original path in the body is retained for historical
accuracy; the current canonical path is the `docs/archive/` one.
