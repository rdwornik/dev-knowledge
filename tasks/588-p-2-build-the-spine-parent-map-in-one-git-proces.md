---
id: "[#588]"
title: "P-2 — build the spine parent-map in ONE git process"
status: open
priority: P1
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#588] [P1][S] **P-2 — build the spine parent-map in ONE git process** — The first-parent spine scan spawns a git process per commit; subprocess spawns inside a loop are the measured hot shape. One `git rev-list --parents` call builds the whole parent-map. Pure refactor: the FF-signature and its verdicts must not move. · Done when: the spine scan issues one git invocation regardless of range length, `validate_no_ff.find_violations` returns byte-identical verdicts on a fixture range before and after (a test pins that equivalence), `block-ff-push` and the `no_ff_merges` WARN still share the one signature, and the before/after timing is recorded from the same command · refs docs/intake/2026-08-26-tech-loop-tax-and-gate-performance.md (intake #54), scripts/validate_no_ff.py, scripts/block_ff_push.py, scripts/journal_anchor.py, #153 · source: intake #54 (I-PERF), row P-2 · kill-candidates: none — `[#153]` owns enforcement completeness and asserts nothing about how the spine is walked · serialize-group: audit-py
