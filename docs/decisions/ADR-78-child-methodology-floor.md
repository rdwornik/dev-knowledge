<!-- scope: meta -->

# ADR-78 — Child methodology floor (O2 Bounded Hybrid)

- **Status:** Accepted — 2026-06-07
- **Amends:** ADR-75 (exclusion-zone register — adds `methodology_surface` zone class)
- **Related:** ADR-73 (per-repo orchestration distribution), ADR-75 (exclusion-zone register), ADR-77 (immutable-paths zone class); BACKLOG #121
- **Decommission:** none
- **Source:** Council pick 2026-06-07, unanimous post-R2; operator ratification = distillation prompt 2026-06-07. Transcript: `docs/decisions/transcripts/council-out-20260607_124757-pick-council-f2-child-floor.md`

## Context

Child repos inherit the hub methodology via a per-session handoff bundle — a copy requirement that depends on the operator remembering to upload at session start. The methodology transfer audit (2026-06-07) surfaced F2: child repo CC sessions lack an auto-loaded methodology floor, causing silent gaps when the bundle is not uploaded. The council was asked to pick between five options (O1–O5): O1 bundle-only status quo, O2 child-resident generated floor, O3 hub-pointer via CLAUDE.md includes, O4 per-repo minimal CLAUDE.md, O5 no-floor.

The council also identified F5 (scope-visibility-per-repo) as a bounding constraint: a child floor that leaks hub-internal artifacts (BACKLOG, LESSONS, handoffs, hub-only ADRs) creates scope pollution rather than clarity.

## Decision

**O2 — Bounded Hybrid** is adopted.

**1 — Floor artifact.** Each registered child repo carries a generated `CLAUDE-FLOOR.md` (≤ 1,500 tokens, conformance-enforced) and a sidecar `CLAUDE-FLOOR.md.sha256`. The child's `CLAUDE.md` references the floor file. Hub pointers are retained as labeled depth escape-hatches (not load-bearing for the child session).

**2 — Generator model.** The generator is **operator-invoked only**, at rollout moments (ADR-73 propagation pattern). It does NOT run on a schedule and does NOT make cross-repo writes autonomously. Children commit their own floor (operator runs generator → commits in the child repo). This is a strict Layer-2 invariant: no runtime or scheduled cross-repo writes from the hub.

**3 — Methodology-surface zone (ADR-75 register extension).** A new zone class — `methodology_surface` — is added to the exclusion-zone register:

| Field | Value |
|---|---|
| Zone class | `methodology_surface` |
| Whitelist (must surface) | prompt-header, valve-discipline, cadence, ship-rule, context-budget |
| F5 blacklist (must NOT surface) | hub BACKLOG, hub LESSONS, hub handoffs, hub-only ADRs (any content scoped exclusively to `.dev-knowledge` governance) |
| Rationale | A child floor that leaks hub-internal artifacts creates scope pollution; a floor that omits core working-style conventions fails to transfer the methodology. The whitelist/blacklist is the boundary. |
| Enforcing organ | Hub CI: renders the floor and greps the F5 blacklist; child pre-commit: verifies `CLAUDE-FLOOR.md.sha256` matches the committed floor; hub `/ship` gate: warns on stale registered-child hashes. Lightweight link-checker for pointer targets. |

The `methodology_surface` zone is a **content-scope** zone class, distinct from the path-exclusion zone classes in ADR-75 (P0 write-block) and ADR-77 (immutable-paths). All three zone classes are backed by enforcing organs per the "no organ = decoration" rule.

**4 — Token ceiling.** 1,500 tokens is the hard ceiling. Exceeding it is a conformance failure. The 500-token compression alternative was explicitly rejected by the council: clarity is the goal, not the metric.

**5 — Conformance wiring.**
- Child pre-commit hook verifies the sidecar hash (added to the `#114` hook family)
- Hub CI renders the floor and greps the F5 blacklist before merge
- Hub `/ship` gate warns on stale registered-child hashes
- Lightweight link-checker for pointer targets in the floor

## Open VERIFY items (recorded from council blind spots)

These must be resolved before implementation proceeds:

- **(a) `@`-include resolution:** Whether `@`-include in a child `CLAUDE.md` natively auto-resolves at CC session start — implementation is **conditional** on a positive result; must be checked FIRST before any floor template work (BACKLOG #121 VERIFY rider).
- **(b) Per-child deviation:** A mechanism for per-child floor overrides is deferred; v1 assumes one-size-fits-all floor content. If any child requires deviation, revisit before that child's rollout.

## Consequences

- Child CC sessions gain an auto-loaded methodology baseline without depending on operator bundle-upload at every session start.
- The `methodology_surface` zone formalizes the F5 boundary: what travels to children is a deliberate policy choice recorded in a verifiable register, not an editorial judgment made at generation time.
- The generator is Layer-2 compliant (read-only hub; operator-invoked writes go to the child, not initiated by the hub).
- A 3-week re-explain measurement is owed post-rollout to verify the floor reduces the methodology re-explanation burden (tracked in BACKLOG #121).
- ADR-75's register now has three zone classes: the P0 write-block (ADR-75 original), the immutable-paths class (ADR-77), and the methodology-surface class (this ADR).

## Alternatives considered

- **O1 (bundle-only status quo):** rejected — the methodology gap is real and recurs every session without a bundle upload.
- **O3 (hub-pointer includes only):** rejected as the primary mechanism — pointers are available as labeled escape-hatches but cannot be the load-bearing floor (hub lookup required at every session start is a network/availability dependency).
- **O4 (per-repo minimal CLAUDE.md authored manually):** rejected — manual authoring diverges; a generated floor with a conformance hash is maintainable; manual is not.
- **O5 (no-floor):** rejected — training data from F2 shows consistent methodology loss in child sessions.
- **500-token ceiling:** rejected — council found clarity requires more headroom than 500 tokens; 1,500 is the principled minimum.
