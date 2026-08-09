---
id: "[#102]"
title: "Machine-readable repo index for agent consumption"
status: deferred
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#102] [P2][M] Machine-readable repo index for agent consumption — field reports ~50k-token exploratory reads replaced by ~250-token precompiled indexes; evaluate for hub + corp · verify-first: confirm claimed tools (`stacklit`, `scip-search`) actually exist before any design · Done when: a pilot index on one repo demonstrably replaces exploratory reads in a CC session · refs #89, #91, ADR-51, research transcript 2026-06-06 · context-engineering field study (InsForge) — pilot shape: a single-call repo-topology spec (~500 tokens — structure, conventions, gate names, entry points, plus a `hints` field) consumed at UNDERSTAND time; makes the ~50k→~250-token replacement target concrete · VERIFY-FIRST DISCHARGED (ARC-4): `stacklit` EXISTS (glincker/stacklit), matches the pilot shape incl. `hints`; `scip-search` does NOT — real referent is Sourcegraph SCIP/`scip` CLI (code-nav, not repo-topology). Hub half NO — not a code repo, shape already native + gate-enforced; corp untested, NOT closed · DEFER — peg: a repo whose codemap is generator-MANAGED (#262/#295 closed 2026-07-25 — flat / single-package layouts stay hand-authored by policy, so no fleet codemap migration is coming to peg on)
