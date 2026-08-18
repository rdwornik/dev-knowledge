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

- [#523] [P2][M] **Executive-index render leg on the generated `BACKLOG.md`** — the wall-of-text is a **renderer defect, not a data defect**: the file renders every row body inline, so a reader asking *what is open* reads ~190 task lines to find out. Add a **priority-sorted index at the top of the generated file** — P1→P3, one line per live row, `id · one-line title · link to tasks/<id>` — leaving the per-row bodies below unchanged. Owner is the **ADR-107 strangler renderer**: a LEG on existing work, not a new machinery family. · Done when: the `BACKLOG.md` opens with a P1→P3 index of one line per live row, AND `--check` still verifies it byte-identically against the tree, AND `--roundtrip` still proves losslessness, AND a `--status` (or equivalent) render mode prints velocity + horizon + top-priority ids from live data · refs ADR-107, #439, #433, scripts/gen_task_tree.py · kill-candidates: none — [#439] is closed on a met Done-when and [#433] owns ADR-107 §6.2; neither covers the render leg · serialize-group: architecture · source: docs/audits/2026-08-12-technical-roadmap-north-star-frozen.md §2 (*Backlog READABLE*; the richer render is the same owner's later candidate) + protocols/STANDING_RULINGS.md M-11 A4 (the birth ruling that keeps [#439] closed)
