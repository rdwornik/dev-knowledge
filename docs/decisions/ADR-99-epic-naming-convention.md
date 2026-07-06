# ADR-99: Epic-naming convention — Track-X now, ADR-66 story-map fleet-wide at P6

- **Status:** Accepted
- **Date:** 2026-07-07
- **Decision tier:** Architecture (Path A — direct operator ruling, 2026-07-07 architect ratification session)
- **Related:** ADR-66 (BACKLOG story-map hierarchy — the convergence target), ADR-41 (cross-session / per-repo dedicated-chat routing — where the ai-council rename executes), ADR-91 (methodology corpus versioning — the P6 corpus roll this piggy-backs on), #162 (the "architect" actor-vs-mode vocab-collision — the same class this fixes), #221 (deploy the corpus across the fleet — the P6 roll that carries convergence)
- **Decommission:** none
- **Source:** 2026-07-07 architect ratification session (operator ruling R2); consumes the draft `docs/audits/2026-07-07-DRAFT-epic-naming-convention-proposal.md` on branch `drafts/2026-07-07-proposals` @ `3da29ea` **by ratification, not by merge** (tag `archive/drafts-2026-07-07`).

## Context

Two backlog-vocabulary schemes coexist in the fleet (draft §1):

| | Hub (`.dev-knowledge`) | ai-council |
|---|---|---|
| **Scheme** | ADR-66 story-map: `## Theme` → `### Story` → `- [#id] [P][size] task` | "Epic A / Epic B / Epic C" free-letter labels |
| **Identity** | monotonic `[#id]`, never reused | positional letter, re-used across initiatives |
| **Enforced by** | `validate_backlog.py` + `git_backlog_drift` + `backlog-id-on-close` | convention only, no validator |
| **Traceability** | `closes [#id]` → git is the closure record | letter has no commit-linkage |

The collision: the same word **"epic"** means an **ADR-66 story-map story** in the hub and a **lettered work-stream** in ai-council. A cross-repo reader (or a fleet-scale tool) cannot tell which "epic" a reference means. This is the **same vocab-collision class as #162** (architect = Layer-1 actor vs handoff mode).

## Decision

Adopt the draft's option **(D) now → (A) at P6**:

1. **(D) now — reconcile the WORD, keep the schemes.** Rename ai-council's lettered "Epic X" to **"Track X"** (the operator-confirmed default term), killing the *word* collision immediately at near-zero cost. "epic" is thereafter reserved fleet-wide for the ADR-66 / §14a-lane sense; ai-council's streams are "Track X".
2. **(A) at P6 — converge on one scheme.** When the methodology corpus rolls to ai-council (**P6 / #221**), carry the ADR-66 story-map + `validate_backlog` as part of that deploy, converging on **one enforced, traceable, non-colliding scheme fleet-wide** — the story-map adoption piggy-backs on a deploy already touching the consumer, so it costs no separate arc.
3. **Execution locus — ai-council's dedicated chat only (ADR-41).** The Track-X rename **executes in ai-council's dedicated chat**, NEVER from the hub. **This ADR records the convention; it does not touch ai-council** (Layer-2 hub↛sibling boundary, ADR-28/41).

## Consequences

- **Easier:** the cross-repo "which epic?" ambiguity disappears immediately (Track vs epic are now distinct words); fleet tooling no longer carries the ambiguity; the P6 convergence lands the enforced story-map + validators on ai-council as a rider on an already-scheduled deploy.
- **Interim state (honest):** until P6, two *structural* schemes still exist — hub ADR-66 story-map, ai-council Track-X lettered streams — but the **names no longer collide**. The `[#id]` monotonic traceability + validator suite reach ai-council only at P6.
- **This ADR changes no file in ai-council.** The rename is queued to ai-council's chat (ADR-41); the hub records the convention only.

## Alternatives considered

- **(A) one convention (hub ADR-66 story-map) fleet-wide, now.** The end-state, but the migration cost is paid immediately instead of piggy-backed on the P6 deploy already touching the consumer — deferred to P6, not rejected.
- **(B) lettered epics fleet-wide.** Rejected on its face: throws away `[#id]` monotonic traceability + the whole `validate_backlog` / `git_backlog_drift` suite (ADR-65/66) — a strict regression.
- **(C) both stand, explicitly scoped (no rename).** Rejected: the *word* collision persists; every cross-repo reference must qualify (`hub #id` / `ai-council Epic B`) and fleet tooling must carry the ambiguity forever. (D) kills the collision atomically at near-zero cost — the #162-class fix.
