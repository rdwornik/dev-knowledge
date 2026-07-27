---
id: "[#434]"
title: "Conformance-branch extraction pass — one bounded arc, read-only over the branches"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
source: BACKLOG.md
derived: true
---

- [#434] [P2][M] **Conformance-branch extraction pass — one bounded arc, read-only over the branches** — aggregate every nightly digest, one row per night: date · findings claimed · real defects · fixed since · false positives. Live set at filing: **7** branches, `claude/conformance-2026-07-21` through `-27` (verified, not assumed). Binding rulings, verbatim: **RULING 1 do-not-merge (ADR-84 writer isolation). RULING 2 do-not-bulk-delete before extraction. The pre-registered verdict fork: digests surfaced real actionable findings -> producer works, was merely unconsumed, earns a named morning-loop slot; digests surfaced nothing beyond noise across the span -> producer is mis-scoped, RESHAPE or RETIRE. Sharp test: did ANY nightly digest flag "ratified through ADR-103" while ADR-104/105 existed and bound?** **FORK RULED — option (1) STAYS; ruling + its binding caveat verbatim in `docs/decisions/README.md`.** · Done when: the aggregate is committed as one dated artifact AND the fork is ruled in the same window · refs #419, #426, #428, ADR-84 · kill-candidates: none — #419 frames the unconsumed-output defect; this extracts the evidence deciding it · serialize-group: settings-json
