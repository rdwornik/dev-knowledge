---
id: "[#427]"
title: "Region templates carry a repo-POSITION-DEPENDENT path"
status: open
priority: P3
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: claude-md
source: BACKLOG.md
derived: true
---

- [#427] [P3][S] **Region templates carry a repo-POSITION-DEPENDENT path** (ai-council, 2026-07-26): `templates/claude-regions/critical-rules-records.md:1` and `antipatterns-universal.md:2` name the token log as bare `logs/TOKEN-LOG.md` — correct at the hub, wrong at every consumer, where it is `.dev-knowledge/logs/TOKEN-LOG.md`. Carried **byte-verbatim**, so no single string is true in both positions: this is a **substitution** problem, not a text fix, and rewriting the template to the `.dev-knowledge/` form only inverts the error. Not theoretical — ai-council's #97 checker reports the bare path as a non-resolving claim; its remedies were a declared divergence (taken, **time-boxed to this ticket**) or an allowlist entry (refused: it hides the class). **Load-bearing for a downstream divergence that cannot retire without it** · Done when: the carry mechanism supports a per-consumer substitution (or an explicit per-position variant), and ai-council's `claude-md-token-log-address` divergence retires by reference · refs `templates/claude-regions/`, ai-council `.methodology.yaml` + its #111, #312, #361 (same files, different defect) · kill-candidates: none · serialize-group: claude-md
