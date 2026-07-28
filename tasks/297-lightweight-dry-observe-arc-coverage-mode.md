---
id: "[#297]"
title: "Lightweight/dry `observe-arc` coverage mode"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#297] [P3][S] Lightweight/dry `observe-arc` coverage mode (ai-council pilot G7) — `lived_sandbox.cli observe-arc` requires `ANTHROPIC_API_KEY` and, once given it, spawns a long-running BILLED child arc (timed out at 4m40s, killed), so the #215 "coverage n-of-6" leg can't be produced read-only/cheaply from a headless harness (the mesh FIRING was still proven by the other Informant rows — only the n-of-6 number is env-constrained). Add a dry mode that reports per-organ FIRED/ARMED/SILENT from static inspection of armed hooks + config, without a live billed child. · Done when: an `observe-arc` dry/coverage mode reports per-organ armed/fired state with no billed child spawn, with a test · refs deploy/lived_sandbox/, scripts/enforcement_coverage.py, #215, #236 · serialize-group: audit-py · DEFER — peg: post-Wave-1
