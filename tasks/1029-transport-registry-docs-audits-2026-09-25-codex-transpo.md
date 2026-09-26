---
id: "[#1029]"
title: "transport-registry: docs/audits/2026-09-25-codex-transport-registry.md has no consumer"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1029] [P3][S] **transport-registry: docs/audits/2026-09-25-codex-transport-registry.md has no consumer** - `scripts/consumer_at_landing.py` currently reports this file "cited by no governance surface and not in the arm-time baseline" (confirmed live, 2026-09-25). The 300 stray transport files it also names are `lane-transport-strays`' work, not filed here. · Done when: the file is cited by a row, ADR, register entry or intake, and `scripts/consumer_at_landing.py`'s output no longer names it · refs `docs/audits/2026-09-25-codex-transport-registry.md`, `scripts/consumer_at_landing.py` · kill-candidates: none -- no open row cites this audit
