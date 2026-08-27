---
id: "[#130]"
title: "Memory-hygiene review"
status: deferred
priority: P3
size: S
theme: "[E3] Lessons feedback loop"
story: "[S9] Make lessons an active feedback loop, not a passive archive"
generates: BACKLOG.md
---

- [#130] [P3][S] Memory-hygiene review — periodic pass over the CC auto-memory + the `gotchas` skill: flag duplicate/overlapping entries, stale or RETIRED cleanup candidates, and MEMORY.md index cap-proximity; surface candidates as a digest into the morning funnel for ratification (operator-gated — never auto-delete, per the no-delete invariant). Plus a **capture-time scrub arm**: scrub a gotcha/memory at the moment of write (dedupe-against-existing before append), not only via the periodic pass — the cheaper intervention point. · Done when: one hygiene pass emits a ratify-only candidates digest to a `docs/audits/<date>-technical-*` artifact with per-class counts (duplicates / stale-RETIRED / cap-proximity), and the gotcha/memory write path carries a dedupe-against-existing step proven by a test that seeds a duplicate and asserts it is caught at write time · refs MEMORY.md, ~/.claude/skills/gotchas, #4 · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
