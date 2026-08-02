---
id: "[#474]"
title: "`gen_task_tree --write` is a destructive-adjacent path that warns but still executes"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#474] [P3][S] **`gen_task_tree --write` is a destructive-adjacent path that warns but still executes** — witnessed live 2026-08-02 during the [#473] arc: `--write` is IMPORT/RECOVERY (it rebuilds `tasks/` FROM the generated `BACKLOG.md`, the wrong direction post-[#439]-flip) and sits one keystroke from `--emit-source`, the normal regen. Invoked by mistake it re-derived 17 task filenames from their titles, emitted them as new files, rewrote `manifest.json` to point at the new names, and left the originals as "rename remnants" — recovered only because every orphan had a tracked same-id counterpart to diff against. **The flag already prints a warning and then does it anyway**, which is the shape the fleet has ruled against elsewhere: the RM-8 `BundleCollisionError` refuses rather than warns, and `--prune` is refused outright (ADR-107 §6.3). A warning that does not gate is a nudge, and a nudge is not a guard on a path that rewrites the source of truth. Candidate shapes: require an explicit `--force` alongside `--write`, or refuse when `tasks/` already holds files whose ids the import would re-slug (the exact witnessed case), or both. · Done when: an accidental `--write` against a populated `tasks/` tree refuses rather than executing, with the escape hatch named in the refusal message, and a test pins the refusal · refs [#473], [#439], ADR-107 §6.3 (`--prune` refused), scripts/gen_task_tree.py, JOURNAL 2026-08-02 (b) · kill-candidates: none — [#439] shipped the strangler flip that made `--write` the wrong direction but left the flag ungated; no open row owns generator-flag safety
