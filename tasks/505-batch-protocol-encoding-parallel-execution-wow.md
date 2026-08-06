---
id: "[#505]"
title: "Batch-protocol encoding — the parallel-execution way-of-working as versioned repo artifacts"
status: open
priority: P1
size: M
theme: "[E3] Lessons feedback loop"
story: "[S10] Codify recurring patterns into the methodology"
serialize-group: playbook
generates: BACKLOG.md
---

- [#505] [P1][M] **Batch-protocol encoding — the parallel-execution way-of-working as versioned repo artifacts** — the batch shape (lanes, contracts, budgets, integrator, teardown) lives in seat memory and dies with the seat: unclosed parallel work (the operator's #1 pain), per-lane environment errors, zero portability. Track 1 of intake #26, items 1–7; ADR-110 §1–§3 carries the enumeration and this row deliberately does not restate it. **Coupling, not conflict:** [#441] gates WHEN parallel is allowed (its four-condition test is live PLAYBOOK Ch8 text); this row defines HOW a batch runs once it is — keep one launch test, not two. · Done when: a fresh seat runs a full batch from repo artifacts alone; batch-1 executes under it with exactly 2 operator touches; hygiene WARN and branch-prefix enum are validator-checked; the refuse-to-finish checklist is mechanical · footprint: `protocols/PLAYBOOK.md`, `.claude/commands/`, handoff templates/generator pointer, hygiene organ site · refs intake #26, ADR-110, #429 (cross-ref only), #441 · kill-candidates: none — no open row owns the parallel-execution protocol · serialize-group: playbook
