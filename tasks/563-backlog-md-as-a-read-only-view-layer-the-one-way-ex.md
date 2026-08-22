---
id: "[#563]"
title: "`Backlog.md` as a read-only view layer — the one-way exporter"
status: closed
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#563] [P2][M] **`Backlog.md` as a read-only view layer — the one-way exporter** — **RULED `ADOPT-VIEW-LAYER` 2026-08-19 — this row is the implementation, not a re-trial.** Do not re-run the trial and do not propose `Backlog.md` as the store; the measured divergence is recorded so it is not relitigated. **Three binding conditions, all three load-bearing:** (1) **one-way export only** — `tasks/` stays the single source of truth; (2) a **disposable, gitignored export dir**, regenerated per read; (3) **governance stays bespoke** — no gate, hook or script is re-pointed at the export. Why not the store, in one measurement: `backlog task archive` frees an id, the next `create` re-issues it, two files then carry `id: TASK-16`, and `backlog doctor` — its own duplicate-id checker — reports **clean**, because the archive dir sits outside its scan. Why a view is worth building: `[#533]` maps to `TASK-533` as a **lossless bijection**, so a ~130-line direct-write exporter renders all 288 rows in ~1.1 s and the board, web UI, search and `overview` read it unmodified — the whole authoritative body line lands in `## Description` verbatim, so the view is diffable against its source. The CLI is **not** a write path (it cannot set ids and has a 170-char title cliff), and `backlog/` never lands in the repo — ADR-101 Rule C would refuse the new top-level home in any case. · Done when: `scripts/export_backlog_view.py` writes the `Backlog.md` on-disk format directly from `tasks/` into a gitignored scratch dir and re-exports on every invocation, the export path is in `.gitignore` with a test asserting nothing under it is tracked, `check_active_branches` and `remote_operations` are `false` and the export is generated with `--agent-instructions none`, and a test asserts no gate, hook or script reads the export · refs docs/audits/2026-08-19-technical-backlogmd-trial.md, ADR-112, ADR-101, ADR-107, #523 · kill-candidates: none — no open row owns a backlog VIEW surface; `[#523]`'s executive-index render leg is a leg of the GENERATED `BACKLOG.md` and is a different artifact
