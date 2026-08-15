# CONTRACT Q — [#293] satellite runbook fan-out · worktree `lane-q-293-satellite`
**Purpose:** serve the fleet: `tasks/293-consumer-runbook-fan-out.md` (UN-DEFERRED 2026-08-09, "0 of 6 consumers seeded", DUE THIS WINDOW per X-15). Deliver exactly what the row's Done-when states — read the row FIRST; row-is-the-spec.
**OWNED-FILES manifest:** the runbook files the ROW names. Zero invented paths: every destination is derived from the row + quoted governance (Folder Governance / hub PLAYBOOK); QUOTE the source for each home in the packet BEFORE writing. If the row's Done-when requires touching another repo (satellite checkouts), STOP-and-report with the derived plan instead — cross-repo writes are not authorized by this contract.

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
Problem: hub serves nobody until consumers can run it. Risk: seeding runbooks into invented homes. Failure mode: "done" without the row's own metric met.

## Steps
1. COMMIT — per-consumer runbooks per the row's spec (one commit per coherent group), each home justified by a quoted source.
2. Targeted checks: any doc hooks touching your files. Packet: row's Done-when clause-by-clause vs delivered, 0/6 → n/6 stated. STOPPED.
