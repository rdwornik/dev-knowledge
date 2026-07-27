---
id: "[#285]"
title: "Extend hub freshness gating to PLAYBOOK"
status: open
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S13] Keep canonical files accurate"
serialize-group: audit-py
source: BACKLOG.md
derived: true
---

- [#285] [P3][S] Extend hub freshness gating to PLAYBOOK — SESSION_SETUP + AI_COUNCIL_PROCESS joined `_FRESHNESS_FILES` (fleet-census A-2 ruling, 2026-07-08) after a genuine re-read + `last_reviewed` stamp, but PLAYBOOK (3705 lines — the largest, most load-bearing canonical doc) was DEFERRED: it carries no `last_reviewed` frontmatter (a prose "Last updated" line only) and a genuine end-to-end re-read is its own arc — a bare stamp to green a gate is forbidden. Add `last_reviewed` frontmatter + `protocols/PLAYBOOK.md` to `_HUB_ONLY_FRESHNESS_FILES` only after a real re-read; pairs naturally with #213 (PLAYBOOK rule/history condensation). · absorbs #67 #18 #27 #39 #217 #219 (PLAYBOOK/ESSENTIALS doctrine + surface edits, folded into this re-read) · Done when: PLAYBOOK is genuinely re-read end-to-end, carries a `last_reviewed` stamp, and is in `_FRESHNESS_FILES` (audit-health gates it) with `test_freshness_includes_hub_only_protocol_docs` updated (drop its PLAYBOOK-absent assertion) · refs scripts/audit.py (_HUB_ONLY_FRESHNESS_FILES), scripts/canonical_freshness_gate.py, protocols/PLAYBOOK.md, #213, docs/audits/2026-07-08-fleet-consistency-census.md Part 4 · serialize-group: audit-py
