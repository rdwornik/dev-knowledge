---
id: "[#240]"
title: "Follow-up"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#240] [P3][S] Follow-up — Stage-3 audit-leg regression teeth: `check_enforcement_coverage` emits WARN on an `enforcing-local -> absent` regression once a mesh baseline exists (deferred from Stage 2's non-blocking `n/a` posture) · Done when: the leg WARNs when a consumer that showed `enforcing-local` for an organ regresses to `absent`, gated on a recorded baseline · refs scripts/audit.py (check_enforcement_coverage), scripts/enforcement_coverage.py, #236 · serialize-group: audit-py · DEFER — peg: mesh baseline n=2
