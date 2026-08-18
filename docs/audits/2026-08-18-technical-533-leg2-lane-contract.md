<!-- Provenance: verbatim copy of the frozen lane contract dispatched to this session
     (`~/Downloads/LANE-A-533-leg2.md`), landed as contract-of-record per ADR-110.
     Operator amendment at dispatch (the only one): the `--worktree` flag had already
     provisioned `.claude/worktrees/lane-a-533-leg2` on branch `worktree-lane-a-533-leg2`,
     so STEP 0's manual `git worktree add` line is SUPERSEDED -- STEP 0 is this commit.
     Also stated at dispatch: timings taken under concurrent lane load are indicative and
     are to be flagged as such; the authoritative quiet-tree measure happens at integration.
     Contract body below is unedited. -->

# LANE A — #533 LEG 2: MEMOIZATION + PARALLEL CHECK EXECUTION

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — contract-is-the-plan, NO plan-mode | high |

> Fresh CC session (`/clear`). Worktree lane — you never touch the primary checkout and you
> NEVER merge. Commit-and-STOP.

**Worktree (STEP 0):** `git worktree add ../worktree-lane-a-533-leg2 -b worktree-lane-a-533-leg2 main`
— branch name verified against `scripts/validate_branch_naming.py` `LANE_BRANCH_RE` (T0.6, 4/4 PASS).
**Governing row:** `[#533]` LEG 2 only (the row's final clause, ruled 2026-08-16). Closing this leg
does NOT close the row — acceptance clause governs, not Done-when.
**ADR-110:** save this prompt as
`docs/audits/2026-08-18-technical-533-leg2-lane-contract.md` and COMMIT it as your first commit.

**Baseline (Phase-0, quiet tree, do not re-measure):** hook invocation
`uv run --locked python scripts/audit.py health` = **median 290.9 s** (spread 4.9%). The recorded
42.2 s of 2026-08-15 is stale by 6.9× and the regression is UNDIAGNOSED — which is why STEP 1
exists.

## PINNED-BY-TESTS (do not detach)
- `tests/test_audit.py` — **DO NOT TOUCH THIS FILE AT ALL.** Its 25 monkeypatch seams
  (`_is_hub`/`_REPO_ROOT` et al.) belong to the seam leg. Your test work lives in NEW files only.
- `scripts/audit_checks/registry.py` `CHECK_ORDER` — order is load-bearing; results MUST be
  emitted in registry order regardless of completion order, and the existing order tests must
  stay green untouched.
- `tests/test_validate_hermetization.py::test_rule_c_blocks_a_new_package_dir_under_an_allowlisted_parent`
  — you add no new homes; every file you add lives in an existing allowlisted location.

## UNDERSTAND
- Problem: 291 s of hook tax on EVERY commit by every lane; the ruled mechanisms are `lru_cache`
  on `journal_anchor._entries` (:214) and stdlib `ThreadPoolExecutor` over the 43-check registry
  (measured I/O-bound 2026-08-16 — no `ProcessPoolExecutor`, no hand-rolled threading).
- Risk: the 6.9× regression postdates the lru_cache memo; optimizing without attribution may miss
  the actual mass. A stale anchor cache is WORSE than slow — it produces false push-gate verdicts.
- Scope: `scripts/audit.py` (runner loops :3542/:4102/:4202 + `--parallel` CLI),
  `scripts/audit_checks/registry.py`, `scripts/journal_anchor.py`, NEW
  `tests/test_journal_anchor.py`, NEW `tests/test_audit_parallel.py`. Nothing else.
- Blast radius if the memo is wrong: `audit.py`, `batch_manifest.py`, `block_unanchored_push.py`,
  `enforcement_coverage.py` all import `journal_anchor`.

## STEPS
**STEP 0 — worktree + contract commit** (above). `COMMIT`

**STEP 1 — ATTRIBUTION BEFORE OPTIMIZATION.** One serial `health` run with per-check wall-time
capture (time around the runner loop — a temporary local measurement, not committed
instrumentation; a table in the artifact, exact method recorded). Deliver: 43-row table, descending.
**Fork (report, don't improvise):** if one check holds >50% of wall AND is CPU-bound or
algorithmically pathological, STOP-report before threading — threading an algorithmic defect is
the wrong fix. Otherwise proceed. `COMMIT` (table into the lane artifact)

**STEP 2 — TEST-FIRST: `tests/test_journal_anchor.py` (NEW).** Cases, written and RED before any
cache code: (a) memoized second call returns identical entries; (b) **append-between-runs** —
JOURNAL.md grows between two calls in ONE process → second call sees the new entry (cache keys on
file identity `(path, mtime_ns, size)` or is invalidated per run); (c) output byte-identity vs
uncached on a fixed fixture. `COMMIT`

**STEP 3 — implement the memo** in `journal_anchor.py` (single responsibility: caching lives in
this module, not in callers). Green the STEP-2 tests. `COMMIT`

**STEP 4 — TEST-FIRST: `tests/test_audit_parallel.py` (NEW).** Parity: serial vs parallel runs on
the same tree produce byte-identical check verdicts AND identical emission order (CHECK_ORDER).
`COMMIT`

**STEP 5 — ThreadPoolExecutor runner** behind `--parallel/--no-parallel` (default: **serial** —
flipping the hook's default is a separate ruling, not this lane's). Worker count = CLI option
(`--workers`, default `min(8, n_checks)`) — config, never a hardcoded literal. Results collected
concurrently, emitted strictly in CHECK_ORDER. Green STEP-4. `COMMIT`

**STEP 6 — MEASURE.** On the worktree, quiet: 3× serial-uncached (sanity vs 291 s), 3× serial-cached,
3× `--parallel` cached. Record medians + speedup factors in the lane artifact AND in the closing
commit message (the acceptance clause requires it). `COMMIT`

## FINAL
Targeted suites `-n 0` (in-lane tests are always `-n 0`): the two NEW files +
`tests/test_adr85_integration_enforcement.py`, `tests/test_batch_manifest.py`,
`tests/test_review_artifact_coverage.py` (indirect journal_anchor consumers) + the registry order
tests. All green → **commit-and-STOP**. STOP packet: attribution table top-5 · measured medians +
speedups · files touched · any fork taken. **NO merge, no push to main, no touching the primary
checkout.**

## WHAT NOT TO DO
No edits to `tests/test_audit.py` · no check extraction (leg 1) · no hook-default flip · no new
dependencies (stdlib only) · no committed instrumentation · no `git add -A` · no `--no-verify` ·
no merge.
