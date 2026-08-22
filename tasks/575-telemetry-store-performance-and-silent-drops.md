---
id: "[#575]"
title: "Telemetry store: 98.5% of an emit, and silent drops under concurrent writers"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: environment
generates: BACKLOG.md
---

- [#575] [P2][M] **Telemetry store: 98.5% of an emit, and silent drops under concurrent writers** — measured by the tel lane, not estimated. The store leg is **16.4 ms/event, 98.5% of an emit**, because a connection is opened, pragma'd, schema-checked and torn down *per event* — ~0.7 s on every wired `audit.py health` run, straight against the felt-speed mandate. Worse: **8 concurrent writers produced `database is locked` despite `busy_timeout=5000`, and `safe_emit` swallows that class — those events drop SILENTLY**, under exactly the concurrency this repo runs. **R6(c) folds in here by ruling:** the store path moves to `git rev-parse --git-common-dir`, so linked worktrees share one durable store instead of each writing a per-worktree DB teardown deletes; `--show-toplevel` stays correct elsewhere. · Done when: per-event cost drops with a before/after measurement, ≥8 concurrent writers no longer drop events silently (retry or surface, with a test), and the store resolves via `--git-common-dir` with a two-worktree test · refs `scripts/telemetry_emit.py`, `fleet_analytics._git_common_dir`, R6(c), `docs/audits/2026-08-21-technical-lane-tel-run-id.md` §3, §5 · kill-candidates: none — `[#529]` and `[#565]` closed on their own legs · serialize-group: environment
