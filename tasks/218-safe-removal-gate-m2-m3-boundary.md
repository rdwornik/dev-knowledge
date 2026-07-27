---
id: "[#218]"
title: "Safe-removal gate M2+M3 boundary"
status: deferred
priority: P3
size: M
theme: "[E2] Enforced governance"
story: "[S6] Know what depends on code before removing it (ADR-89 computed edges)"
serialize-group: code-edge
source: BACKLOG.md
derived: true
---

- [#218] [P3][M] Safe-removal gate M2+M3 boundary (the deferred phases of #195) — extend the code→code (M1) safe-removal gate (`scripts/safe_remove.py`, audit check #24 — refuses removing a `scripts/` module while a live external **code** referrer survives) to the rest of the removal's heterogeneous direct-boundary union: **M2** (computed path / dotted-module string refs) + **M3** (declared-prose reverse-deps), each with its own compute-vs-declare posture — a direct cross-kind boundary, not a transitive walk; fail-closed on partial/oracle-unavailable. #195 delivered M1 only (operator-approved close 2026-06-26). · Done when: the gate refuses a removal with an M2 (path/dotted-module) referrer AND with an M3 (declared-prose) referrer on a fixture, extending #195's M1 catch to the full union · refs #195 (M1 delivered), ADR-89, #196 (closure-spike findings), docs/audits/2026-06-20-removal-closure-spike-findings.md · serialize-group: code-edge · DEFER — peg: first removal M1 doesn't cover
