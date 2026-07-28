---
id: "[#310]"
title: "Define the cold-bundle annotation surface + annotate the 2026-07-05 architect bundle as-cold"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: handoff
generates: BACKLOG.md
---

- [#310] [P3][S] Define the cold-bundle annotation surface + annotate the 2026-07-05 architect bundle as-cold — no sanctioned surface exists to mark an immutable handoff bundle cold/incomplete (no per-bundle README, no bundle-status index/log, no sidecar precedent — HUB CONSOLIDATION M15 finding). The 07-05 architect bundle STILL leaks 8 `(fill:` markers (HANDOFF_BOOT/PASTE_THIS/RESIDUAL) but is immutable → annotate-not-backfill. Decide the surface (a `.cold` sidecar next to the bundle, OR a bundle-status leg in the operator runbook `docs/handoffs/README.md`) WITHOUT editing the rendered bundle files, then annotate the 07-05 bundle as-cold. · Done when: a sanctioned cold-annotation surface is defined AND the 07-05 architect bundle is recorded as-cold on it (no rendered bundle file edited, no retrospective fabricated) · refs docs/handoffs/README.md, docs/handoffs/2026-07-05-dev-knowledge-architect/, ADR-101, #292 · kill-candidates: #292 — if the operator rules the 07-05 bundle's cold state is adequately recorded in #292's evidence text, close without building any surface · serialize-group: handoff · DEFER — peg: post-Wave-1
