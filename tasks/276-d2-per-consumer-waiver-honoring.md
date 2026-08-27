---
id: "[#276]"
title: "D2 per-consumer waiver-honoring"
status: deferred
priority: P2
size: M
theme: "[E6] Cross-repo universalization"
story: "[S16] Manage the methodology as a living thing (essence lifecycle: transfer · sync · PRUNE)"
generates: BACKLOG.md
---

- [#276] [P2][M] D2 per-consumer waiver-honoring — a `.methodology.yaml` divergence-allowlist the deploy tool actually READS, on BOTH legs. PRUNE leg: once corp-monorepo records 1.2.0, a future remove-leg run (v1.3.x+) re-enters the sweep and REFUSEs on corp's consumer-owned ruff (URL-matches the ruff-gate tombstone). ADD/converge leg (FOLD 2026-07-11): `--execute` re-appends `codemap-freshness`, which BOTH live consumers legitimately exclude — re-adding it breaks them. The P4 `.methodology.yaml` allowlist is Informant-side only; neither deploy leg consults it. Build the allowlist consumed by `detect_prune` AND the add-loop (pairs with #245's last-deployed-bytes oracle); + standardize the waiver-recording convention — all sanctioned divergences declared in `.methodology.yaml`, an inline comment a courtesy duplicate only. · Done when: a consumer-declared divergence for a component causes BOTH the prune sweep to SKIP it (no REFUSE-abort) AND the add/converge leg to NOT re-append it (no re-break) on a previously-deployed consumer, with tests · refs ADR-96 amendment 2026-07-06, deploy/carrier_precommit.py, deploy/tool.py, .methodology.yaml, #245, #244, #221 · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
