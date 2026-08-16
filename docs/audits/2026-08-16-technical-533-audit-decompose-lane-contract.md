## §C · CONTRACTS (amended roster of 11, architect ruling D-1v2 2026-08-16) — ex-ante buckets: finish-line/feature = a–i, hub-introspection = x, m (2 of 2 at width 11)
COMMON (applies to every lane, verbatim law): auto mode; own worktree/branch only; `uv sync --locked --group analytics` first; PYTHONUTF8=1 on console errors; T_start = packet line 1; step 0 commits contract-of-record + prints OWNED-FILES manifest; edit nothing outside it (regen surfaces excluded); tasks/ edits at SOURCE then `gen_task_tree.py --emit-source`; targeted tests only (full suite = integration, once); no merges, no pushes to main, no births, no register edits unless the contract names them; decision budget: STOP only for curated-baseline touch, rule-vs-ruling conflict, or unruled fork — else decide-and-report in ONE packet; commit-and-STOP.

## LANE m — CONTRACT-M533-DECOMPOSE.md · worktree `worktree-lane-m-533-audit-decompose` [HUB]

Execute `[#533]`: decompose the `scripts/audit.py` check monolith into `scripts/audit_checks/` — one module per check plus an ordered registry — leaving `audit.py` a **thin facade**.

**OWNED-FILES:** `scripts/audit.py` · the new `scripts/audit_checks/**` · `tasks/533-*.md` (row status at source). **`tests/test_audit.py` is READ-ONLY to this lane** — read it, run it, do not edit it. That single restriction is what keeps this lane disjoint from every other lane on the roster, so treat an urge to edit it as a STOP-and-report, not a judgement call.

**Why this lane exists, so the constraint is not mistaken for fussiness.** The batch-6 pre-dispatch matrix refused to dispatch two hub lanes because both had to edit `audit.py` — `check_hooks_armed` (`:1625`) and `check_stale_worktrees` (`:1221`) — a collision with nothing to do with either lane's subject. Two unrelated checks cannot be worked in parallel because they share a file. You are fixing that constraint, which means **you must not become an instance of it**.

**Steps.**

1. **Mechanical extraction.** One module per check under `scripts/audit_checks/`, **module name = check name** (`check_hooks_armed` → `scripts/audit_checks/check_hooks_armed.py`, or the same stem without the `check_` prefix if you adopt that convention — pick ONE and apply it uniformly, and state which in the packet). **ZERO logic change.** Move code; do not improve it, rename variables, fix a lint, tidy a docstring, or "while I'm here" anything. A behavioural diff is a lane failure even if the behaviour is better.
2. **Ordered registry** preserving today's `ALL_CHECKS` **order AND count**. Baseline measured on the unchanged tree at lane start: **`len(audit.ALL_CHECKS) == 43`**. Order is load-bearing — output order is part of the byte-identical proof.
3. **Facade compatibility.** `audit.py` keeps **every public entrypoint and every CLI verb byte-compatible**. The git hooks call it (`audit-health` is a pre-commit gate; `ship-gate` and `health` are invoked by name), so *nothing outside this lane's OWNED-FILES may need editing*. If you find yourself wanting to edit a caller, the facade is wrong — fix the facade.
4. **Golden proof, and it is a byte-comparison rather than a judgement.** Capture `python scripts/audit.py health` output on the unchanged tree BEFORE the refactor, capture it again AFTER, and prove them **byte-identical**. Do the same for any other CLI verb you touch. Then run the targeted test files for the touched surface green. Quote both in the packet: the diff command you ran and its empty result.

**The escape hatch, and it is mandatory rather than optional.** Any check that **resists mechanical extraction** — shared module-level state, a helper closed over by several checks, an import cycle, anything where moving it is not a pure move — is **LEFT IN THE FACADE and REPORTED**. Do not redesign it mid-lane. A partial decomposition with an honest list of what stayed and exactly why is the *successful* outcome of this lane; a complete one bought with a behaviour change is a failure. `[#533]`'s Done-when is written to accept exactly this.

**Known traps, so they cost you minutes rather than hours.**
- `ALL_CHECKS` **count pins live in several places outside this lane's files** (`ARCHITECTURE.md`, `.claude/commands/handoff-verify.md`, `.claude/commands/preflight.md`, `deploy/release_lint.py`, plus test pins). The count must therefore stay **43** — you are not authorised to edit those sites, and preserving the count is what makes that unnecessary. Re-grep rather than trusting any single stated number; that count has drifted before.
- `audit.py` is **5243 lines** at lane start. Extract in reviewable batches with a commit per batch, not one giant commit.
- Several checks import sibling modules by path with a `gitenv` scrub already in place; preserve that import style exactly rather than "modernising" it.
- `audit.py health` is a **pre-commit gate on your own commits**. If your refactor breaks it you will be unable to commit — that is the gate working. Fix forward; never `--no-verify`, never `SKIP=`.

**Merge position:** this lane merges **LAST** in the batch-6 queue (`a b c e f g d h i x m`), so the queue completes on today's structure and batch 7 boots on yours. Nothing else in the batch is merged against your moving foundation.

**Row update:** set `[#533]`'s status at the `tasks/` source and regenerate; do **not** hand-edit `BACKLOG.md`.
