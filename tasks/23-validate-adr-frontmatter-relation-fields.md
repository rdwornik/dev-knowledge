---
id: "[#23]"
title: "Validate ADR frontmatter relation-fields"
status: deferred
priority: P3
size: S
theme: "[E4] Decision management"
story: "[S11] Keep the decision corpus navigable and contradiction-aware"
generates: BACKLOG.md
---

- [#23] [P3][S] Validate ADR frontmatter relation-fields (supersedes/related/amends resolvable) — narrowed from the full navigable graph: graph rendering is dropped until witnessed navigation pain. Resolves the #112 depends-on (this relation-field validator is the piece #112's Option-B amend path needs). · Done when: an audit check flags an ADR whose supersedes/related/amends frontmatter names a non-existent ADR-id, with tests · refs posture-audit I1, #112 · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
