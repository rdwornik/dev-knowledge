---
id: "[#349]"
title: "Mechanize session-discipline inheritance"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#349] [P2][M] Mechanize session-discipline inheritance — the test-then-close gate travels via mechanism, not operator reminder (operator priority-program item 4, 2026-07-18) — a fresh browser/session must inherit "a session ends only after proper testing + the close sequence" from a boot/gate mechanism (SessionStart context + a Stop-gate), never from the operator re-stating it. Overlaps #344 Ask 1 (the session-close refusal-gate) — this is the inheritance/transmission half; reconcile scope when built. · Done when: a boot-injected + Stop-gated mechanism carries the test-then-close discipline with a test per leg, and one cold-session run is recorded in a docs/audits/ artifact; or this row is closed as folded into [#344] with the fold recorded in protocols/STANDING_RULINGS.md · refs #344, ADR-85, scripts/session_end_backpressure.py, protocols/DEFINITION_OF_DONE.md · kill-candidates: #344 (Ask 1 session-close gate — this may fold into it; keep separate until the inheritance-vs-refusal split is ruled) · serialize-group: audit-py
