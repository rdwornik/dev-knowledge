---
id: "[#500]"
title: "The Stop hook's BACKLOG advisory reads a correctly-closed task as \"nothing closed\""
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
generates: BACKLOG.md
---

- [#500] [P3][S] **The Stop hook's BACKLOG advisory reads a correctly-closed task as "nothing closed"** — it wants a structural-marker CHANGE in place, but since ADR-107 a closure DELETES the row from the generated `BACKLOG.md` and the terminal state moves to `tasks/<id>-*.md` (`status: closed`) with the manifest node removed. A pure deletion matches no pattern, so **every correctly-closed row reads as nothing-closed** — an advisory firing hardest when the work was done right gets ignored. Witnessed on [#498] and verified against git, not assumed (1 file changed, 1 deletion; row count 1 -> 0). · Done when: the advisory recognises row-DELETION plus the paired `tasks/*.md` terminal-status flip as a closure signal, pinned by a test that closes a row the sanctioned way and asserts the advisory stays silent · refs scripts/session_end_backpressure.py, scripts/gen_task_tree.py, ADR-107 §6.3, ADR-85 §A5, #498 · kill-candidates: none — no open row owns the session-end BACKLOG advisory's closure heuristic
