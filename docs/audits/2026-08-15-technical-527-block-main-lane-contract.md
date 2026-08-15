# CONTRACT O — [#527] anti-direct-to-main hook · worktree `lane-o-527-block-main`
**Purpose:** a local pre-commit hook refusing non-merge commits on `main`, per ruling D5.3: copy upstream `no-commit-to-branch`'s `git symbolic-ref HEAD` predicate + ONE added carve-out — `MERGE_HEAD` present (resolved via `git rev-parse --git-path MERGE_HEAD`, per-worktree) ⇒ allow. Armed via the existing `arm_hooks.py`/`check_hooks_armed` mechanism (row's Done-when).
**OWNED-FILES manifest:** `scripts/block_commit_on_main.py` + its test file + one `.pre-commit-config.yaml` entry. (You own the config file this phase — lane N is hard-excluded from it.)

## Common law (all phase-1 contracts)
| Model | Mode | Effort |
|---|---|---|
| per dispatch line | auto (zero design freedom beyond stated steps) | per dispatch line |
- Repo: .dev-knowledge (primary = operator's checkout; you are in your own worktree/branch).
- Read CLAUDE.md first. Gotchas: PYTHONUTF8=1 on console errors; manifest-first when closing rows; BACKLOG.md is GENERATED (edit tasks/ source + `python scripts/gen_task_tree.py --emit-source`); freshness-gated docs need a genuine full re-read before stamp moves; silent_rule_ratchet — phrase doc additions declaratively, no new must/shall/never tokens.
- Env: `uv sync --locked --group analytics` before anything (17/19 prior lane reds were this miss).
- Git: work ONLY on this lane's branch in this worktree; commit per step with the step name; NEVER merge, NEVER push main, NEVER --no-verify, NEVER SKIP=.
- T_start: first line of your packet records dispatch timestamp.
- Tiered suite law: targeted test files in-lane only; the full suite runs ONCE at batch integration, not here.
- Decision budget: decide per defaults and REPORT in one end-of-arc packet. STOP-and-report only for: (a) curated-baseline touches, (b) rule-vs-ruling conflicts, (c) a fork class with no standing ruling. Never drip questions.
- File discipline: step 0 prints your OWNED-FILES manifest; you modify NOTHING outside it (BACKLOG/manifest/audit-index regens excluded — regen-at-merge surfaces). Zero births of [#id]s. No register/STANDING_RULINGS edits unless your contract names them.
- Packet: ONE .md — T_start · manifest as executed · per-step commit shas · targeted-test evidence · deviations self-reported · final "STOPPED" line.
## What NOT to do (all lanes)
No merges · no pushes to main · no new ids · no new repo folders/paths (homes derive from quoted governance sources only) · no deleting content without an explicit contract step · no full-suite runs · no edits outside the manifest · no answering stop-hooks with new scope.

## UNDERSTAND
Problem: witnessed 2026-08-13 direct-to-main commit; push-time is too late. Risk: refusing conflicted integration merges → --no-verify culture (the wide gap). Failure mode: E4 unhandled.

## Steps
1. COMMIT — the hook script: refuse non-merge commit when HEAD resolves to main; allow when MERGE_HEAD exists; detached HEAD passes (stated hole, by design).
2. COMMIT — tests = the acceptance matrix VERBATIM as cases: E1 refused · E2 allowed · E3 clean --no-ff merge never fires the hook · E4 conflicted merge on main ALLOWED via carve-out · E5 amend on main refused · W1 worktree-on-feature allowed.
3. COMMIT — the .pre-commit-config.yaml entry (local hook) + confirm arm_hooks.py picks it up (check_hooks_armed evidence in packet).
4. Targeted run of your test file. STOPPED.
