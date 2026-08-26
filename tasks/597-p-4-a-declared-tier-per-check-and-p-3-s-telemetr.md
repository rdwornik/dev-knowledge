---
id: "[#597]"
title: "P-4 — a declared tier per check, and P-3's telemetry window FIRST"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#597] [P2][M] **P-4 — a declared tier per check, and P-3's telemetry window FIRST** — Every check runs at every stage. The full suite is 1526.5 s on bare main and 1870.1 s on the merged result, and `-n auto` is already the baseline, so the remaining lever is running less, not running wider. MEASURE-FIRST is binding: no check is retiered without a number. · Done when: P-3's telemetry window lands FIRST and records a per-check cost, every check declares the tier it runs at (commit / push / integration), every tier decision cites its measured cost in the commit that makes it — a check demoted without a number is a defect, not a shortcut — and NO check is made faster by being made weaker · refs docs/intake/2026-08-26-tech-loop-tax-and-gate-performance.md (intake #54), docs/audits/2026-08-26-verification-batch-1-close-packet.md sections 8 and 11, scripts/audit.py, pyproject.toml, protocols/PLAYBOOK.md Ch5 · source: intake #54 (I-PERF), row P-4, gated on P-3 · kill-candidates: none — no open row owns per-check cost or stage tiering; `[#242]` and `[#153]` concern what checks assert, never when they run · serialize-group: audit-py
