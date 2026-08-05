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

- [#218] [P1][M] Safe-removal gate M2+M3 boundary (the deferred phases of #195) — extend the code→code (M1) safe-removal gate (`scripts/safe_remove.py`, audit check #24 — refuses removing a `scripts/` module while a live external **code** referrer survives) to the rest of the removal's heterogeneous direct-boundary union: **M2** (computed path / dotted-module string refs) + **M3** (declared-prose reverse-deps), each with its own compute-vs-declare posture — a direct cross-kind boundary, not a transitive walk; fail-closed on partial/oracle-unavailable. #195 delivered M1 only (operator-approved close 2026-06-26). **RE-SCOPED 2026-08-05 (architect ruling, absorbing the [#489] night draft — retired as a duplicate):** this row is the **L3 real-deletion lifecycle gap**, not merely a gate-scope extension — the lifecycle has no L3 deletion step at all, and M2+M3 are the legs that make REAL deletion safe. What the ruling adds is POSTURE, not scope, and it binds: **P1** (raised from P3); **TDD proves the non-destruction paths FIRST** — a fixture demonstrates the gate REFUSING before any destructive path is exercised, never the reverse; the arc **rides #487's first close batch** (FR-8a); and the **operator authorizes the destructive merge as a named gate**, never as an implicit consequence of a green suite. · Done when: the gate refuses a removal with an M2 (path/dotted-module) referrer AND with an M3 (declared-prose) referrer on a fixture, extending #195's M1 catch to the full union — with the non-destruction paths proven first and the destructive merge carrying its named operator authorization · refs #195 (M1 delivered), ADR-89, #196 (closure-spike findings), docs/audits/2026-06-20-removal-closure-spike-findings.md, #489 (retired duplicate), docs/audits/2026-08-05-technical-night-batch-morning-report.md §6.1, #487 · serialize-group: code-edge · DEFER — peg: rides #487's first close batch (FR-8a)
