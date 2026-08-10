---
id: "[#310]"
title: "Define the cold-bundle annotation surface + annotate the 07-05 bundle as-cold"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: handoff
generates: BACKLOG.md
---

- [#310] [P3][S] Define the cold-bundle annotation surface + annotate the 07-05 bundle as-cold — no surface marks an immutable bundle cold/incomplete (no README, index or sidecar precedent — M15); the 07-05 bundle leaks 8 `(fill:` markers but is immutable → annotate-not-backfill. Options: a `.cold` sidecar or a status leg in the runbook; never edit rendered files. **2nd instance, NEW door — RE-CUT (08-10):** `--allow-suffix` re-renders FILL-IN regions EMPTY, so the `-2` sibling nearly shipped 4 unfilled regions minus its predecessor's residual; refused by `residual_completeness` (`86078062`). Carry-forward UNOWNED, not birthed; [#422] nearest, not owner. · Done when: a sanctioned cold-annotation surface is defined AND the 07-05 architect bundle is recorded as-cold on it (no rendered bundle file edited, no retrospective fabricated) · refs docs/handoffs/README.md, docs/handoffs/2026-07-05-dev-knowledge-architect/, ADR-101, #292 · kill-candidates: #292 — REFUTED at 9fc1a8b4: escape premise FALSE, `validate_residual_completeness.py:33-35` is prospective-only and grandfathers this bundle (8 `(fill:` live). Do NOT re-propose · serialize-group: handoff · DEFER — peg: post-Wave-1
