---
id: "[#245]"
title: "Add-path status-awareness"
status: deferred
priority: P2
size: M
theme: "[E6] Cross-repo universalization"
story: "[S16] Manage the methodology as a living thing (essence lifecycle: transfer · sync · PRUNE)"
generates: BACKLOG.md
---

- [#245] [P2][M] Add-path status-awareness — the deploy add-path (`deploy/tool.py` execute + each carrier `apply`) is blind to `status: removed`; the manifest status should be the single source of truth for the consumer surface, read by BOTH the add-path and the prune-sweep. Today the re-add tug-of-war is avoided only by manually dropping a pruned component from its carrier's add-target, which BREAKS for anchor-coupled / identified-by-its-only-content entries (the hub-toc-hooks case, FU-2). Teach the add-path to honor `status: removed` (skip re-adding), threading the removed-set already computed in the prune sweep into `apply`. Also generalizes the hash-guard oracle to LAST-DEPLOYED bytes (per-consumer sidecar, the floor-carrier precedent) so a source-drifted component still classifies correctly. Tier-2/post-P2. · absorbs #246 (hub-toc-hooks retirement gated on this landing) · Done when: the add-path skips re-adding a `status: removed` component (no manual add-target drop needed) AND a source-drifted prune target classifies against last-deployed bytes, with tests · refs deploy/tool.py, deploy/contract.py, ADR-96, #244, #246 · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
