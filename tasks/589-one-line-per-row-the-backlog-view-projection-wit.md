---
id: "[#589]"
title: "One line per row — the BACKLOG view projection, with a size assertion that cannot be silently undone"
status: open
priority: P1
size: M
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
serialize-group: architecture
depends-on: "#523"
generates: BACKLOG.md
---

- [#589] [P1][M] **One line per row — the BACKLOG view projection, with a size assertion that cannot be silently undone** — The view renders each row's FULL body: 191 rows carry 245,486 B at a mean 1,284 B/row against 37,533 B of scaffolding. A one-line projection of the same rows measures 22,127 B — 59,660 B total, a 79% cut and 91% off the row payload, with ZERO information loss because the bodies already live in `tasks/`. · Done when: the generated view emits one line per row (`id · theme · status · title · one-line · pointer to tasks/<id>.md`), `gen_task_tree.py --check` carries a size assertion that FAILS on a deliberately inflated view (a test plants one), every field the old view rendered is either in the new line or reachable from its pointer, and `BACKLOG.md` measures under 70,000 bytes on an unchanged `tasks/` · refs docs/intake/2026-08-26-tech-append-only-surfaces-and-views.md (intake #49), docs/audits/2026-08-26-technical-hub-diagnostic.md section 7 Q1, scripts/gen_task_tree.py, ADR-107, #563 · source: intake #49 (I1), the VIEW half · kill-candidates: none — `[#523]` renders an executive index OVER the generated file and would consume this projection rather than duplicate it · **RE-BASELINE 2026-09-01 (architect's ruling, batch-F cut —0(a)): 70,000 -> 72,000 B, recorded HERE because this row's own subject is an assertion that may not be silently undone.** The groom ran FIRST and is the reason the raise is lawful rather than convenient: 223 manifest nodes, ZERO carrying a terminal status, tree coherent, and all three STRONG closure candidates REFUSED on content verification — `[#430]` is open on half (b) with only (a) landed, `[#554]`'s Done-when needs an in-container `pytest -m 'not slow'` and a VPS `devcontainer up` that no receipt shows, and `[#614]` was a false positive off this arc's own reference tags. Measured composition at the raise: 70,276 B total = 32,383 B of 223 row lines (mean 145 B) + 37,893 B of scaffolding, which is **54% of the file and not rows at all**. New headroom 1,724 B, about 11 rows — one batch's filing, so the next breach arrives inside a batch instead of silently. `_VIEW_ROW_BYTE_CEILING` and the 100,000 per-commit gate are UNTOUCHED: only the point-in-time total moved · serialize-group: architecture · depends-on: #523
