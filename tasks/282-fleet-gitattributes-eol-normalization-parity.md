---
id: "[#282]"
title: "Fleet `.gitattributes` EOL-normalization parity"
status: open
priority: P3
size: S
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
generates: BACKLOG.md
---

- [#282] [P3][S] Fleet `.gitattributes` EOL-normalization parity — 4 consumers lack `.gitattributes` (ai-council, corp-ops, corp-sca-time-automation, demo-prep); no EOL normalization on Windows repos (hub + corp-monorepo + life-architect have it). Target shape `* text=auto eol=lf` (+ `*.ps1` CRLF where relevant); executes per-repo in Wave 1 (ADR-41 — consumer-side, queue-only here). **Progress 1/4 (2026-07-08):** ai-council done; remaining corp-ops, corp-sca, demo-prep. · Done when: each of the 4 consumers carries a `.gitattributes` with the target normalization (per-repo tracked, n≥1 recorded) · refs docs/audits/2026-07-08-fleet-consistency-census.md Part 1
