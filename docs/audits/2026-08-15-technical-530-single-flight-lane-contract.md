# CONTRACT P — [#530] single-flight dispatch guard · worktree `lane-p-530-single-flight`
**Purpose:** the ruled D5.1 design — a git ref as distributed compare-and-swap: claim `refs/locks/<contract-id>` on `origin` with `git push --force-with-lease=<ref>: origin HEAD:<ref>` (T2: an unfetched second clone is still refused; T4 trap avoided — plain push returns exit 0 on same-HEAD race). Fail CLOSED (block_ff_push posture). Plus the local same-clone fast leg: `git update-ref --stdin` `create` (exit 128 on held). Release = ref delete. NOT `refs/worktree/*` (per-worktree, invisible to primary — T9).
**OWNED-FILES manifest:** `scripts/single_flight.py` (~the ruled 18-line shape; exits 0 claimed / 3 in-flight / 2 internal) + its test file.

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
Problem: witnessed triple execution of one contract (2026-08-14), cross-machine — filesystem locks are single-host by construction. Risk: a guard that greenlights the same-HEAD race. Failure mode: trusting plain-push exit codes.

## Steps
1. COMMIT — `single_flight.py`: claim/release/inspect; refusal message prints how to inspect and release a stale hold (no TTL in git — ruled residual, option (a)).
2. COMMIT — tests against a LOCAL BARE remote fixture: T1 claim-new ok · T2 unfetched-clone refused (stale info, exit 1) · T3 different-commit plain push rejected · T4 same-HEAD via force-with-lease refused (the trap test) · T5 release+reclaim · local fast leg create/held/exit-128.
3. COMMIT — Done-when demonstration vs REAL `origin` (pre-authorized in the plan, reviewer-visible): create `refs/locks/probe-530`, prove T2/T4 properties, DELETE the probe ref, transcript into the packet. Network step — if origin unreachable, STOP-and-report (budget (c)), do not fake it.
4. Targeted run of your test file. Packet notes the "step 0 needs network" precondition as ruled. STOPPED.
