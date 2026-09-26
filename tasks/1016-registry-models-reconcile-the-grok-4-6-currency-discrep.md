---
id: "[#1016]"
title: "registry-models: reconcile the grok-4.6 currency discrepancy rather than leaving it filed"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1016] [P2][S] **registry-models: reconcile the grok-4.6 currency discrepancy rather than leaving it filed** - N1 lane registry-models filed the discrepancy (`grok models` re-run 2026-09-25 disagreed with Part Z's same-night reading of the identical command) as a dated `currency_exception` rather than resolving it -- `ecosystem/provider-registry.yaml` providers.review.xai.grok-4.6 lines ~694-708. Owed: an actual re-verification run that either re-pins the model or extends the exception with a second independent reading. · Done when: a fresh `grok models` reading (or its documented unavailability) is recorded in the registry, and either the pin changes or the `currency_exception` gains a second independent confirming reading · refs `ecosystem/provider-registry.yaml`, DIGEST-WAVE5B-N1-2026-09-25 ROWS-OWED (registry-models) · kill-candidates: none -- no open row tracks this reconciliation
