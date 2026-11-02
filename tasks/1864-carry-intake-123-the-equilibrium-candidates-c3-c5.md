---
id: "[#1864]"
title: "Carry intake 123 — the equilibrium-night CANDIDATEs C-3, C-4, C-5 — to an ADR-111 outcome per item"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1864] [P2][S] **Carry intake 123 — the equilibrium-night CANDIDATEs C-3, C-4, C-5 — to an ADR-111 outcome per item** - this row OWNS `docs/intake/2026-11-02-tech-equilibrium-candidates-c3-c5.md` (intake 123, status SEED). The operator routed the three CANDIDATEs through the ADR-111 funnel (`RATIFICATION-2026-11-02-GROK-AND-TOKEN-D0.md`, decision 4), and they land by the one-off path of ruling Q-IN-1 = B (`to-browser/DIGEST-RULING-Q-IN-1-2026-11-02.md`, branch `docs/intake-equilibrium-c3-c5` @ f20039360). Filed as the intake's carrier row so `graph-task-coverage` sees an `implements` edge from an OPEN row (integrator Q-IN-2, dispatcher answer 2026-11-02). Scope is ONLY moving the intake through the engine: each of C-3, C-4, C-5 reaches a recorded outcome (ratified into a row, merged into an existing row, or REJECTED with a reason). This row decides none of them itself. · touches: docs/intake/2026-11-02-tech-equilibrium-candidates-c3-c5.md · Done when: the intake's `status:` is no longer SEED and each of C-3, C-4, C-5 names its outcome and the record (ratification, row id, or rejection) that carries it.
