---
id: "[#218]"
title: "Safe-removal gate M2+M3 boundary"
status: deferred
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S6] Know what depends on code before removing it (ADR-89 computed edges)"
serialize-group: code-edge
generates: BACKLOG.md
---

- [#218] [P1][M] Safe-removal gate M2+M3 boundary — the **L3 real-deletion lifecycle gap** (the deferred phases of #195): there is no L3 deletion step, and M2+M3 are the legs that make REAL deletion safe. Extend the code→code (M1) gate (`scripts/safe_remove.py`, check #24) to the rest of the direct-boundary union: **M2** (computed path / dotted-module refs) + **M3** (declared-prose reverse-deps), each with its own compute-vs-declare posture — a cross-kind boundary, not a transitive walk; fail-closed on partial. #195 delivered M1 only. **Posture binds:** **P1**; **TDD proves the non-destruction paths FIRST** (a fixture shows the gate REFUSING before any destructive path runs); the arc **rides #487's first close batch**; and the **operator authorizes the destructive merge as a named gate**. · Done when: the gate refuses a removal with an M2 referrer AND an M3 referrer on a fixture — non-destruction paths proven first and the destructive merge carrying its named operator authorization · refs #195, ADR-89, #196, docs/audits/2026-06-20-removal-closure-spike-findings.md, #489 (retired duplicate), #487 · serialize-group: code-edge · DEFER — peg: rides #487's first close batch (FR-8a)
