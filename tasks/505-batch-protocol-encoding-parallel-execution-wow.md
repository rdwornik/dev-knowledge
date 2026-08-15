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

- [#505] [P1][M] **Batch-protocol encoding — the parallel-execution way-of-working as versioned repo artifacts** — the batch shape (lanes, contracts, budgets, integrator, teardown) lives in seat memory and dies with the seat: unclosed parallel work, per-lane environment errors, zero portability. Track 1 of intake #26 items 1–7; ADR-110 §1–§3 carries the enumeration. **Coupling, not conflict:** [#441] gates WHEN parallel is allowed, this row HOW a batch runs once it is — one launch test, not two. **Clause 1 has been falsified four times** by pasted/downloaded contract delivery — hence the committed-contract standing rule (register `protocols/STANDING_RULINGS.md` I-D3). **Clause 2 was re-pegged** from a past-tense finish line to the *next* batch; the clause-strike question is settled, no further strike owed (register M-7 / `N2-R1-08`) · Done when: a fresh seat runs a full batch from repo artifacts alone; **the next batch executes under it with its operator-touch count recorded in the batch manifest**; hygiene WARN and branch-prefix enum are validator-checked; the refuse-to-finish checklist is mechanical · refs intake #26, ADR-110, #429 (cross-ref only), #441 · clause 2 → PLAYBOOK Ch8 · kill-candidates: none — no open row owns the parallel-execution protocol · serialize-group: playbook
