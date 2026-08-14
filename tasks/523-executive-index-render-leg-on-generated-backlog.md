---
id: "[#523]"
title: "Executive-index render leg on the generated `BACKLOG.md`"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: architecture
generates: BACKLOG.md
---

- [#523] [P2][M] **Executive-index render leg on the generated `BACKLOG.md`** — the wall-of-text is a **renderer defect, not a data defect** (ROADMAP 2026-08-12 §2, *Backlog READABLE*): the file renders every row body inline, so a reader asking *what is open* reads ~190 task lines to find out. Add a **priority-sorted index at the top of the generated file** — P1→P3, one line per live row, `id · one-line title · link to tasks/<id>` — leaving the per-row bodies below unchanged. Owner is the **ADR-107 strangler renderer**: a LEG on existing work, not a new machinery family. Born rather than appended to `[#439]` by operator ruling A4 (register M-11): that row is closed on a met Done-when. The ROADMAP’s *richer render* is the same owner’s later candidate, out of scope here. **LEG — 2026-08-14 (packet-close), attached, not a new row:** a status-query surface — one command answering "where are we" (H2 velocity line: opened/closed/net/open-total · horizon: the ROADMAP-shaped windows-out read · top-priority ids: the current P1 set) — fits this same renderer's scope, since both are read surfaces over the same live BACKLOG/tasks data; land it as a second render mode on the strangler renderer rather than a new command family. · Done when: the `BACKLOG.md` opens with a P1→P3 index of one line per live row, AND `--check` still verifies it byte-identically against the tree, AND `--roundtrip` still proves losslessness, AND a `--status` (or equivalent) render mode prints velocity + horizon + top-priority ids from live data · refs ADR-107, #439, #433, scripts/gen_task_tree.py · kill-candidates: none — [#439] is closed on a met Done-when and [#433] owns ADR-107 §6.2; neither covers the render leg · serialize-group: architecture
