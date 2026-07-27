---
id: "[#351]"
title: "Fleet-Python-upgrade ticket"
status: open
priority: P3
size: M
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
serialize-group: pre-commit-config
source: BACKLOG.md
derived: true
---

- [#351] [P3][M] Fleet-Python-upgrade ticket ("always newest Python" — RULING-PY, 2026-07-18) — RULING-PY set the ruff baseline at py311 NOW (corp floor ≥3.11) and ticketed the standing direction "always newest Python" as a deferred fleet lift, NOT an immediate baseline bump. Design + execute a coordinated fleet-wide interpreter/target-version upgrade path (hub + corp-monorepo + ai-council), ONE coordinated arc, never per-repo drift; carry the target-version as manifest/carrier material so the next repo inherits it (RULING-W replication). · Done when: a coordinated fleet Python/target-version upgrade path is defined AND the newest-Python baseline is either raised fleet-wide in one arc or recorded deferred-with-next-review-date · refs RULING-PY (docs/handoffs/2026-07-18-dev-knowledge-architect/), #332, #334, deploy/manifest-v1.3.1.yaml · kill-candidates: none — operator-ruled RULING-PY follow-up (the ticketed lift); #332 is dep-version parity, #334 the ruff-id migration — neither subsumes the interpreter upgrade · serialize-group: pre-commit-config
