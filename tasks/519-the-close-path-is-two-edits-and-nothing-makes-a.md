---
id: "[#519]"
title: "The close path is two edits, and nothing makes a half-done close visible"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: architecture
generates: BACKLOG.md
---

- [#519] [P1][M] **The close path is two edits, and nothing makes a half-done close visible** — a close is a terminal `status:` in `tasks/<id>-*.md` AND removal of its node from `tasks/manifest.json`; the second is the load-bearing half. Frontmatter is DERIVED (`emit_task_file_text` re-templates it from the body every emit), so a status-only close is silently REVERTED by the next `--emit-source` — the very command that regenerates BACKLOG.md — which reports "refreshed derived frontmatter in N task file(s)" and reads as success. Witnessed `cd38fb8a`: 3 closes claimed, 194 rows before and after, every gate green throughout — correctly, since nothing was incoherent. Repaired `a62d988e`, caught by an unrelated cross-check, not by any organ. · Done when: a test seeds a status-only close, runs the generator, and FAILS on the revert — the close path is atomic, or its non-atomicity is gate-visible · refs scripts/gen_task_tree.py, ADR-107 §6.3, `a62d988e` · kill-candidates: none — [#500] owns the Stop advisory's closure-RECOGNITION heuristic, [#440] ledger completeness against a DELETED record; neither covers a close that half-lands · serialize-group: architecture
