---
id: "[#285]"
title: "Extend hub freshness gating to PLAYBOOK"
status: deferred
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S13] Keep canonical files accurate"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#285] [P3][S] Extend hub freshness gating to PLAYBOOK — SESSION_SETUP + AI_COUNCIL_PROCESS joined `_FRESHNESS_FILES` (fleet-census A-2 ruling, 2026-07-08) after a genuine re-read + `last_reviewed` stamp, but PLAYBOOK (3705 lines — the largest, most load-bearing canonical doc) was DEFERRED: it carries no `last_reviewed` frontmatter (a prose "Last updated" line only) and a genuine end-to-end re-read is its own arc — a bare stamp to green a gate is forbidden. Add `last_reviewed` frontmatter + `protocols/PLAYBOOK.md` to `_HUB_ONLY_FRESHNESS_FILES` only after a real re-read; pairs naturally with #213 (PLAYBOOK rule/history condensation). · absorbs #67 #18 #27 #39 #217 #219 (PLAYBOOK/ESSENTIALS doctrine + surface edits, folded into this re-read) · Done when: `protocols/PLAYBOOK.md` carries `last_reviewed` frontmatter, `protocols/PLAYBOOK.md` is a member of `_HUB_ONLY_FRESHNESS_FILES` in `scripts/audit.py`, `test_freshness_includes_hub_only_protocol_docs` no longer asserts PLAYBOOK's absence, and the re-read is evidenced by per-section notes in the commit that stamps it — not by the stamp alone · refs scripts/audit.py (_HUB_ONLY_FRESHNESS_FILES), scripts/canonical_freshness_gate.py, protocols/PLAYBOOK.md, #213, docs/audits/2026-07-08-fleet-consistency-census.md Part 4 · serialize-group: audit-py · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
