---
id: "[#586]"
title: "Suite RED — `test_no_gate_hook_or_script_reads_the_export` has no `ecosystem/` naming-vs-reading carve-out (packet ARC-G, C04)"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#586] [P3][S] **Suite RED — `test_no_gate_hook_or_script_reads_the_export` has no `ecosystem/` naming-vs-reading carve-out (packet ARC-G, C04)** — Regenerating the dashboard REDs the suite because the test has no `ecosystem/` carve-out distinguishing NAMING the export from READING it — a false positive that punishes a correct regen. · Full body as born (nothing deleted, relocated for D-2): `docs/audits/2026-08-26-technical-birth-row-bodies-579-586.md` · Done when: `test_no_gate_hook_or_script_reads_the_export` is green with an `ecosystem/` carve-out distinguishing naming from reading (or with a recorded reason for refusing one), regenerating `ecosystem/conformance.html` and `ecosystem/conformance.md` no longer REDs the suite, and the naming-vs-reading rule is stated once in a durable home rather than duplicated per scan · refs tests/test_export_backlog_view.py, scripts/export_backlog_view.py, ecosystem/conformance.md, docs/audits/2026-08-23-technical-lane-dashboard-commit-path.md, docs/audits/2026-08-25-technical-register-ruling-packet.md §3 ARC-G, #171 · source: packet row C04 (ARC-G), via `protocols/STANDING_RULINGS.md` section U · kill-candidates: none — the closed view-layer row cannot carry a fix, and `[#171]` owns no test predicate
