---
id: "[#529]"
title: "Telemetry v1 EMIT — stage-1 events from the gate mesh"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: environment
generates: BACKLOG.md
---

- [#529] [P1][M] **Telemetry v1 EMIT — stage-1 events from the gate mesh** — born 2026-08-15 (adjudication D4.3): the telemetry leg had no owning row, and "row-is-the-spec" pointed at an intake. **Contract of record: intake #29 Fold A** (`ACCEPTED`), whose leg reads "Zero births by this leg". Design: the usage-telemetry memo in `docs/archive/` (`c3c7aa90`) — events `check_run`/`hook_run`/`blocker_fired`, SQLite WAL + structlog, both Adopt (v1 core). **Pointer correction:** the leg's `ROADMAP` reference resolves to no tracked file; the live carrier is the frozen roadmap north-star audit. **Constraints bound in** (night-2 quality scan M-2/M-3): assert non-shallow and decline to emit rather than emit a truncated git metric; report `unknown` not `0` where a coverage signal's only evidence is a non-call reference; emit skip counts with their host capability vector · Done when: the three stage-1 events emit from live gate runs into a WAL-mode SQLite store via structlog with a test per event type, each constraint carries a test, and a recorded gate run reads back without re-measurement · refs intake #29 Fold A, the usage-telemetry memo, [#528] leg 3, the first consumer · kill-candidates: none — no open row owns telemetry emission; [#528] consumes it · serialize-group: environment
