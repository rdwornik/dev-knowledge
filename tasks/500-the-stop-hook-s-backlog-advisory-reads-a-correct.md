---
id: "[#500]"
title: "The Stop hook's BACKLOG advisory reads a correctly-closed task as \"nothing closed\" — the post-ADR-107 closure model removes the row entirely"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
generates: BACKLOG.md
---

- [#500] [P3][S] **The Stop hook's BACKLOG advisory reads a correctly-closed task as "nothing closed" — the post-ADR-107 closure model removes the row entirely** — witnessed live 2026-08-05: after `[#498]` was closed through the sanctioned path the advisory still reported *"N commit(s) ahead of origin/main with no structural-marker change in BACKLOG.md"*. Verified against git rather than assumed: `git diff --stat origin/main..HEAD -- BACKLOG.md` reported **1 file changed, 1 deletion(-)**, and the `- [#498]` row count went **1 on origin/main -> 0 on HEAD**. The closure WAS reflected. The heuristic looks for a structural-marker CHANGE (an `[#id]`/status/checkbox edit in place), but since ADR-107 a closure DELETES the row from the generated `BACKLOG.md` and the terminal state lives in `tasks/<id>-*.md` (`status: closed`) with the manifest node removed. A pure deletion matches none of its patterns, so **every correctly-closed row under the current model reads to this hook as nothing-closed** — an advisory that fires hardest exactly when the work was done right teaches operators to ignore it. · Done when: the advisory recognises row-DELETION plus the paired `tasks/*.md` terminal-status flip as a closure signal, pinned by a test that closes a row the sanctioned way and asserts the advisory stays silent · refs scripts/session_end_backpressure.py, scripts/gen_task_tree.py, ADR-107 §6.3, ADR-85 amendment 2026-08-03 §A5 (the advisory posture), #498 (the witnessed instance) · kill-candidates: none — no open row owns the session-end BACKLOG advisory's closure heuristic
