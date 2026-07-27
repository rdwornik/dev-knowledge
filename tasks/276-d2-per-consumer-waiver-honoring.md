---
id: "[#276]"
title: "D2 per-consumer waiver-honoring"
status: open
priority: P2
size: M
theme: "[E6] Cross-repo universalization"
story: "[S16] Manage the methodology as a living thing (essence lifecycle: transfer · sync · PRUNE)"
source: BACKLOG.md
derived: true
---

- [#276] [P2][M] D2 per-consumer waiver-honoring — a `.methodology.yaml` divergence-allowlist the deploy tool actually READS, on BOTH legs. PRUNE leg: once corp-monorepo records 1.2.0, a future remove-leg run (v1.3.x+) re-enters the sweep and REFUSEs on corp's consumer-owned ruff (URL-matches the ruff-gate tombstone). ADD/converge leg (FOLD 2026-07-11): `--execute` re-appends `codemap-freshness`, which BOTH live consumers legitimately exclude — re-adding it breaks them. The P4 `.methodology.yaml` allowlist is Informant-side only; neither deploy leg consults it. Build the allowlist consumed by `detect_prune` AND the add-loop (pairs with #245's last-deployed-bytes oracle); + standardize the waiver-recording convention — all sanctioned divergences declared in `.methodology.yaml`, an inline comment a courtesy duplicate only. · Done when: a consumer-declared divergence for a component causes BOTH the prune sweep to SKIP it (no REFUSE-abort) AND the add/converge leg to NOT re-append it (no re-break) on a previously-deployed consumer, with tests · refs ADR-96 amendment 2026-07-06, deploy/carrier_precommit.py, deploy/tool.py, .methodology.yaml, #245, #244, #221
