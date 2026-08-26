---
id: "[#595]"
title: "Consumer-at-landing gate for `docs/audits/` — the subtraction mechanism"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: gates
generates: BACKLOG.md
---

- [#595] [P2][M] **Consumer-at-landing gate for `docs/audits/` — the subtraction mechanism** — 290 audit files (40% of the tree) have no human or governance consumer, and 49 are cited by nothing at all. The fleet instruments LANDING and never CONSUMPTION, so accumulation is invisible by construction. A landed artifact declares its consumer, so the class cannot silently re-form. · Done when: an added `docs/audits/` artifact declares a consumer (or an explicit `no-consumer: <reason>`), the unconsumed count does not grow window-over-window measured the SAME way the diagnostic measured it — IDENTIFIER-keyed, never filename-keyed, since a filename-keyed reaper would have proposed deleting 14 live documents and 420 live handoff files — and the check reports `info` rather than passing when it cannot resolve citations · refs docs/intake/2026-08-26-tech-loop-tax-and-gate-performance.md (intake #54), docs/audits/2026-08-26-technical-hub-diagnostic.md sections 3.1 and 7 Q3, docs/archive/README.md, ADR-101 · source: intake #54 (I-PERF), the subtraction mechanism · kill-candidates: none — no open row measures artifact CONSUMPTION; the archive rule governs deletion after the fact, not declaration at landing · serialize-group: gates
