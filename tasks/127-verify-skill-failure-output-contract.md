---
id: "[#127]"
title: "verify skill failure-output contract"
status: deferred
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#127] [P3][S] verify skill failure-output contract — on failure the `verify` skill emits an **actionable** block (file, expected, received, directive) per the backpressure spec, giving an iterate-until-green loop a deterministic feedback signal; success output stays the 3-line compact form · Done when: a seeded failure produces the file/expected/received/directive block and success stays 3-line · refs #104 (verify-as-skill lineage), #126 · enrichment — failure outputs also carry a semantic exit code + expected-vs-got context (not just a directive) so an iterate-until-green loop gets a machine-distinguishable signal (anti-retry-loop) · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
