---
id: "[#474]"
title: "`gen_task_tree --write` warns, then rewrites the source of truth anyway"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#474] [P3][S] **`gen_task_tree --write` warns, then rewrites the source of truth anyway** — `--write` is IMPORT/RECOVERY (rebuilds `tasks/` FROM the generated `BACKLOG.md` — the wrong direction post-[#439]) and sits one keystroke from `--emit-source`. Run by mistake in the [#473] arc it re-derived 17 task filenames from titles, rewrote `manifest.json` to match, and orphaned the originals; recovered only because each orphan had a tracked same-id counterpart. The fleet refuses this shape elsewhere (RM-8 `BundleCollisionError`; `--prune` refused outright, ADR-107 §6.3) — a warning that does not gate is a nudge. Candidates: an explicit `--force`, or refuse when `tasks/` already holds ids the import would re-slug. · Done when: an accidental `--write` against a populated `tasks/` tree refuses rather than executing, names its escape hatch, and a test pins the refusal · refs [#473], [#439], ADR-107 §6.3, scripts/gen_task_tree.py, JOURNAL 2026-08-02 (b) · kill-candidates: none — [#439] left the flag ungated and is closed; no open row owns generator-flag safety
