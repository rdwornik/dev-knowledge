---
id: "[#397]"
title: "scripts/ target structure — rule on the mapped grouping, then (maybe) move"
status: open
priority: P3
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#397] [P3][M] **scripts/ target structure — rule on the mapped grouping, then (maybe) move** — the 2026-07-22 hygiene lane produced the first full scripts/ inventory + caller-impact map (~50 files, ZERO orphans): groupings audit-core 1 · standalone gates 7 · ALL_CHECKS members 14 · freshness generators 4 · manual generators 5 · codemap/toc packages 12 · reporters 4 · session hooks 7 · Tier-1 twins 2 · scheduler 2; highest move-impact `audit.py` (~8 caller sites), `validate_reconciliation.py`/`validate_backlog.py` (~5 each, + plugin-twin parity); several are deploy-manifest-declared so a path change ripples into the deploy contract. NO moves executed — flat may be the right answer. · Done when: the operator rules adopt/reject on the mapped structure AND (if adopt) moves land with every caller site updated + tests green, or flat-is-fine is recorded with the map as the navigation aid · refs docs/audits/2026-07-22-technical-hygiene-pre-handoff-inventory.md §2, #396 · kill-candidates: none — first structural map of scripts/; #396 owns only the gitenv slice · serialize-group: audit-py
