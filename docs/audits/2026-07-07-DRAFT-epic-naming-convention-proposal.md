# DRAFT — Epic naming convention proposal (hub story-map vs ai-council "Epic A/B/C")

> **STATUS: DRAFT — decision-reserved.** Overnight mission Block 4, unmerged branch. A proposal
> with a recommendation; the architect rules. Part of the consolidation-wave "epic-naming
> universalization" ask (2026-07-06 SUPPLEMENT).

## 1. The two conventions in the wild

| | Hub (`.dev-knowledge`) | ai-council |
|---|---|---|
| **Scheme** | ADR-66 story-map: `## Theme` → `### Story` → `- [#id] [P][size] task` | "Epic A / Epic B / Epic C" free-letter labels |
| **Identity** | monotonic `[#id]`, never reused (burned like a departed id) | positional letter, re-used across initiatives |
| **Enforced by** | `validate_backlog.py` (schema) + `git_backlog_drift` + `backlog-id-on-close` | convention only, no validator |
| **Traceability** | `closes [#id]` → git is the closure record | letter has no commit-linkage |

The collision: the same word "epic" means an **ADR-66 story-map story** in the hub and a
**lettered work-stream** in ai-council. A cross-repo reader (or a fleet-scale tool) cannot tell
which "epic" a reference means. This is the same **vocab-collision class** as #162 (architect =
Layer-1 actor vs handoff mode).

## 2. Options

- **(A) One convention — the hub ADR-66 story-map, fleet-wide.** ai-council adopts themes/stories/
  `[#id]` tasks; "Epic A/B/C" retires. Pro: one enforced, traceable, non-colliding scheme; the
  hub's validators roll to consumers (the [#244]/P6 deploy path already carries `validate_backlog`
  via the tier1-lifecycle plugin). Con: ai-council migration cost; the letter labels are
  lightweight and its contributors know them.
- **(B) One convention — lettered epics, fleet-wide.** The hub adopts "Epic A/B/C". Pro: lighter.
  Con: throws away `[#id]` monotonic traceability + the whole validator suite (ADR-65/66) — a
  strict regression; rejected on its face.
- **(C) None — both stand, explicitly scoped.** Document that "epic" is repo-scoped: hub = ADR-66
  story, ai-council = lettered stream; a cross-repo reference always qualifies (`hub #id` /
  `ai-council Epic B`). Pro: zero migration. Con: the collision persists; fleet tooling must carry
  the ambiguity.
- **(D) Reconcile the WORD, keep the schemes.** Rename ai-council's "Epic A/B/C" to a
  non-colliding term (e.g. "Track A/B/C" or "Workstream A"), reserving "epic" for the ADR-66
  §14a-lane sense fleet-wide. Pro: kills the collision cheaply, no story-map migration. Con: still
  two structural schemes, just non-colliding names.

## 3. Recommendation (draft — architect rules)

**(D) now, migrate toward (A) at the P6 fleet roll.** Rename ai-council's lettered "Epic X" to
**"Track X"** (or the operator's preferred term) to kill the *word* collision immediately at near-
zero cost — this is the #162-class fix (disambiguate the vocab atomically). Then, **when the
methodology corpus rolls to ai-council (P6 / #221)**, carry the ADR-66 story-map + `validate_backlog`
as part of that deploy, converging on **(A)** with the migration piggy-backed on a deploy that is
already touching the consumer — so the story-map adoption costs no separate arc. Until P6, "epic"
= the ADR-66/§14a sense fleet-wide; ai-council's streams are "Track X". **File an ADR** (ADR-66
amendment or new) if adopted. **Decision reserved** — especially the term ("Track" vs the
operator's choice) and whether to wait for P6 or migrate ai-council's story-map now.
