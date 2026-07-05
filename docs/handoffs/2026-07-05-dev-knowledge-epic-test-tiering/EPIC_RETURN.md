# EPIC RETURN — test-tiering · (filled by the lane at close)
<!-- scope: meta -->

Required before any merge (HANDOFF_PROCESS §14b). Fill each section; keep the headers.
Closure is claimed on the epic done-contract's **hard metric**, never on "committed".

## 1. Commits + branch state

- `ca20073` feat(tier1-lifecycle): S1 — ship pre-flight pytest runs parallel via -n auto [#260]
- `b59f035` feat(tests): S2 — diff-shaped ship pre-flight selection via live_repo marker [#260]
- `3b87161` docs(tests): S3 — full serial suite documented as the nightly/on-demand path [#260]
- `8f3547b` feat(deps): S4 — #257 dep-isolation decision + dev toolchain declared (PEP 735) [#260]
- (+ the lane-close commit carrying this fill + the JOURNAL entry)

Branch `epic/test-tiering`, clean tree at close. Suite green ON THE BRANCH at `8f3547b`:

```
1294 passed, 7 skipped in 106.85s (0:01:46)   # py -m pytest -n auto --dist worksteal -q
```

## 2. Contract-vs-outcome per story

- **S1 — met.** /ship step 4 runs `pytest -n auto` (now folded into the S2 branching). Timed
  evidence: 162.06s under concurrent-agent load, then 127.23s / 122.96s / 106.85s clean —
  vs 582s serial (2026-07-05 profile). Parallel evidenced.
- **S2 — met, with one adjudication (§3.1).** Docs-only class MEASURED **~34s**
  (`pytest -m live_repo`: 50 nodes, 18.9s test / 21.2s wall + `audit.py ship-gate` 13.1s)
  — **inside the ≤60s budget**. Code-diff class MEASURED 1m47s–2m16s over 4 clean runs,
  median ≈ **2m05s** — identical to the figure #256's own profile set the budget from;
  strictly 3–7s over a literal 120s on the median run, floor-bound by the single 90s
  `test_e2e_five_paths` E2E (splitting it = a test-content edit, outside this boundary).
- **S3 — met.** Full-serial invocation (`py -m pytest -q`, ~9m42s) documented in
  `pyproject.toml` `[tool.pytest.ini_options]` with its purpose (catches what parallelism
  masks) and the parallel-full equivalent. Invocable as documented; no cron wired (per
  contract: a documented invocation suffices).
- **S4 — met.** Isolation decision RECORDED in `pyproject.toml`: system-Python documented
  policy, not a venv (rationale in-file; venv would force `.pre-commit-config.yaml`
  interpreter-path edits — escalation trigger 3, so declined inside the lane). Toolchain
  declared via PEP 735 `[dependency-groups] dev` (pytest, pytest-xdist>=3.8, ruff>=0.15.5,
  pre-commit, pyyaml); reproducibility proven: `py -m pip install --group dev --dry-run`
  (pip 26.1.1) resolves all.

**Done-contract verdict:** docs-only budget MET on measurement; code-diff budget met under
the #256 "~2min" framing, 3–7s over a strict 120s reading (root adjudicates §3.1); full-suite
path documented; gates green on branch modulo the environmental E4 artifact (§3.3). No
coverage loss unaccounted (§3.2 accounting).

## 3. Self-adjudications + ARCHITECT-REVIEW-PENDING

1. **Code-diff budget reading (REVIEW-PENDING).** #256 profiled 2m05s and set "budget
   ~2min"; the EPIC_BOOT contract wrote "≤2min". Measured median = the profile's own 2m05s.
   The remaining lever (splitting the 90s `test_e2e_five_paths`) is a test-content edit the
   boundary forbids. Lane claims S2 met under the source framing; root rules whether strict
   120s demands a follow-up test-split task.
2. **live_repo curation = 36 functions (50 nodes) vs the "~20–30" estimate.** Slightly
   larger because classification of all 59 test files found the honest breaks-on-md-edit
   set to be 36 (incl. the wholly-live `test_handoff_modes.py`, module-marked). Edits kept
   to markers + the enabling `import pytest` in 5 files that lacked it — no test body
   touched; judged inside the markers grant, not a broad sweep. Coverage accounting:
   docs-only (all-`.md` diff) deselects only tmp_path-hermetic tests (unchanged code) and
   live-YAML tests (a YAML edit declassifies the diff to code); ship-gate still runs every
   doc gate; code diffs run the full suite.
3. **E4 boot probe RED = worktree-name artifact.** `deployed_methodology_version` keys the
   registry by `repo_path.name`; this worktree's dir name `epic-test-tiering` is absent →
   the one undispositioned WARN → RED. Not caused by, and not fixable from, this lane
   (registry is out-of-boundary; adding a fake entry would violate its write-contract).
   Expected GREEN on the primary at integration. Booted on that root-cause.
4. **One transient failure, identity lost.** 1 of 5 full parallel runs (the first `-x` run,
   134.55s) had a single test fail; two immediate re-runs green; the green run cleared
   `.pytest_cache/v/cache/lastfailed` before the name was captured. Reported honestly:
   unreproduced, unidentified. The S3 serial path is the designed catcher; §4 proposes a
   watch item.
5. **Venv declined inside the lane** (S4): decision authority was "decide + implement" per
   the story, and the venv arm force-touches out-of-boundary files — so the lane chose the
   documented-policy arm rather than escalate a boundary breach for an option it judged
   worse on the merits (rationale recorded in `pyproject.toml`).

## 4. Proposed BACKLOG delta

For the ROOT to apply at integration (lane applied none of these):

- **Close #256** — evidence: measured budgets (§2 S1/S2/S3), commits `ca20073`/`b59f035`/`3b87161`.
- **Close #257** — evidence: decision recorded + implemented, reproducible install proven, commit `8f3547b`.
- **Close [#260]** (epic block; all 4 story checkboxes ticked by the lane) once the root
  declares closure on the done-contract.
- **New task (P3, root's call per §3.1):** split/mark the 90s `test_e2e_five_paths` long
  pole (e.g. parametrize its five paths) to bring the code-diff class strictly under 120s —
  requires the test-content grant this lane didn't have.
- **New task (P3, optional):** flake watch — one unreproduced single-test failure under
  xdist (§3.4); first serial-nightly run that catches a name closes or escalates it.

## 5. Merge-readiness checklist

- [x] Diff touches ONLY the declared FILE-BOUNDARY (`git diff --name-only main...HEAD` audited: BACKLOG.md · plugins/tier1-lifecycle/commands/ship.md · pyproject.toml · 8 tests/*.py markers-only · + JOURNAL.md and this bundle file in the close commit)
- [x] No merges to main performed from this lane
- [x] JOURNAL entry on the branch names this lane's session SHAs (`ca20073`/`b59f035`/`3b87161`/`8f3547b`)
- [x] Working tree clean; suite green on the branch (1294 passed, 7 skipped in 106.85s at `8f3547b`)
