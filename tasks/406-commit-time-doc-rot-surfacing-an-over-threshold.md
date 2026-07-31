---
id: "[#406]"
title: "Commit-time doc_rot surfacing — an over-threshold BACKLOG task commits clean, reds only the NEXT ship-gate"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#406] [P3][S] **Commit-time doc_rot surfacing — an over-threshold BACKLOG task commits clean, reds only the NEXT ship-gate** — doc_rot is an audit.py ship-gate check, not a pre-commit hook, so a BACKLOG-filing commit that pushes a task over the 1200-char threshold commits cleanly and only reds the NEXT ship-gate — demonstrated by [#405] on itself this arc: filed at 1335 chars, caught only at onboarding, cost a trim-and-remerge. Options, NONE chosen (ruling, not this filing): (a) a non-blocking pre-commit nudge warning on a BACKLOG task crossing the doc_rot threshold in the staged diff (coherence-nudge precedent — surface, don't gate); (b) a pre-commit doc_rot leg (risks over-tight filing backpressure); (c) leave ship-gate-only and accept trim-and-remerge as the cost. · Done when: an architect ruling (ADR-108 §A; re-routed 2026-07-31) picks the enforcement point (or records accept-as-is) and, if a hook is chosen, it flags an over-threshold BACKLOG task in the staged diff with a test · refs scripts/audit.py, scripts/coherence_nudge.py, .pre-commit-config.yaml, #405 · kill-candidates: none — no open task owns commit-time doc_rot surfacing · serialize-group: audit-py
