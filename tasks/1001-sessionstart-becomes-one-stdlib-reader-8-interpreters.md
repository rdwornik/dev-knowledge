---
id: "[#1001]"
title: "SessionStart becomes one stdlib reader -- 8 interpreters to 1, p90 under 2s"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#1001] [P1][M] **SessionStart becomes one stdlib reader -- 8 interpreters to 1, p90 under 2s** - S2 proposed row 1 (`docs/audits/2026-09-23-technical-hook-architecture.md` §5): 8 SessionStart interpreters start in parallel on every boot, p50 7-16s in-session against 1-4s isolated, and `surface_triage.ps1` timed out on 23 of about 31 boots · Done when: over 20 real boots the SessionStart p90 is at most 2s with zero timeouts, measured from transcript attachments; no SessionStart entry makes a network call or writes anything except the seat event; the hook-rate scan, the conductor/triage `gh` polls and the changelog probe run only in a detached producer · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-hook-architecture.md`, `docs/audits/2026-09-23-technical-hook-architecture-appendix.md`, `.claude/settings.json`, `scripts/lane_end_guard.py` · kill-candidates: none -- no open row collapses SessionStart to one reader
