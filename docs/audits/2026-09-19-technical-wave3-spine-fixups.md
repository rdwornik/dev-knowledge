# wave3-spine-fixups — stage 6 wired, doit state moved out of the checkout

Lane `wave3-spine-fixups`, base `main` @ `8b474f64`. Commits: `4825e25e` (RED), `49681647` (fix).

## Premises re-verified
All held: `harness.yaml` stage 6 `command: null`; `DOIT_CONFIG` had no `dep_file`; `.gitignore` had no doit entry;
`stage_library_first.py` had `check`/`deptry`/`run`. One correction: doit's default db lands **beside the dodo
file** (`scripts/.doit.db.*`), not at the repo root — the RED test looks in both.

## RED output (commit `4825e25e`, on base)
```
FAILED tests/test_dodo.py::test_real_spine_gets_past_stage_6_on_the_dispatch_subject - AssertionError ... STOP: stage 6 does not exist -- library-first has no command in harness.yaml (it must fill: library-first)
FAILED tests/test_dodo.py::test_stage_6_fill_round_trips_through_the_check_and_prose_is_still_refused - AssertionError: stage 6 must carry a command
FAILED tests/test_dodo.py::test_dodo_config_points_state_outside_the_repo - KeyError: 'dep_file'
FAILED tests/test_dodo.py::test_dodo_state_is_unique_per_checkout - AttributeError: module 'dodo_under_test' has no attribute '_state_file'
FAILED tests/test_dodo.py::test_running_the_spine_creates_no_doit_state_in_the_repo - AssertionError: the spine left ['.doit.db.dat', '.doit.db.dir'] in the repo...
5 failed, 7 deselected in 26.86s
```

## The fix
- Stage 6: `scripts/stage_library_first.py emit` (additive subcommand) runs `python -m deptry .` with the
  tree-derived `--known-first-party` list and prints a fenced `$ <command>` + the real deptry output + `exit=N`.
  It exits with deptry's own code. `check`, `COMMAND_HEADS`, the regexes and the refusal paths are untouched;
  `tests/test_stage_library_first.py` is unmodified. No `[tool.deptry]` waiver added — deptry was already clean.
  Scope: whole tree (deptry's granularity is the project, not a diff).
- The shown command line is `uv run --locked python -m deptry . [+ --known-first-party xN, derived from the tree]`;
  the real invocation uses `sys.executable -m deptry`. Head `uv` is in `COMMAND_HEADS`.
- Doit state: `dodo.py` `_state_file(root)` = `<tempdir>/dev-knowledge-doit/<sha256(root)[:16]>.db`, parent created.
  Unique per checkout, so `wave3-answerable` and the primary never share a lock. `.gitignore` not needed.

## Acceptance 1 — spine on `WIRE` / `dispatch` (worktree)
Stage 6 passes (deptry: `Scanning 183 files... Success! No dependency issues found.`). Run STOPS at stage 7:
```
usage: validate_substrate.py [-h] [--repo-root REPO_ROOT] [--rules]
                             paths [paths ...]
validate_substrate.py: error: the following arguments are required: paths
.  stage:07-substrate
TaskFailed - taskid:stage:07-substrate
Command failed: '['uv', 'run', '--locked', 'python', 'scripts/validate_substrate.py', '--rules']' returned 2
```
This is a **non-null command failing (exit 2)** — stage 7's argv omits the required `paths`. Out of scope; **not fixed**.
Stages 8–12 were therefore not exercised, and stage 11 (`token-cap`, `command: null`) is still ahead.

## Acceptance 2 — clean tree after two runs
After commit `49681647`, spine run 1 then `git status --short` -> (empty). Spine run 2 then `git status --short` -> (empty).
Runs done from the worktree; **the operator re-runs from the primary after merge.**

## Tests / lint
`tests/test_dodo.py` + `tests/test_stage_library_first.py`: 24 passed (`-n 2`; box was not measured for a higher `-n`).
`ruff check` on the three touched python files: clean. Full suite not run (contract: impacted only).
`scripts/impacted_tests.py select --ref main` was **not** run separately — the two named files were the whole set
this diff can touch by name; flagged as skipped, not verified.

## Codex terra review
Model: `gpt-5.6-terra`, `codex exec review --base main`, stdin closed. `review` mode takes no free-text prompt
alongside `--base`, so the two attack questions (a)/(b) were **not** passed. Result: no findings; summary line
"stage-6 command is wired ... output is compatible with the existing contract checker, and doit state is isolated
outside the checkout per worktree." Recorded as **review=NONE** (no findings, targeted questions unasked) — not "clean".
Open for the operator: (a) `emit` output is real deptry output, but `check` cannot tell that from a fabricated block
(L5's stated anti-claim, unchanged).

## Tokens
ORDERED 100k. ACTUAL (session `79da37c1`, deduped by request): input 48 + output 11,108 + cache-creation 65,712
= ~77k fresh; cache reads 2,005,322 (context re-reads, not fresh input). Within order on the fresh measure.
