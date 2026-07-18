# Night-audit E1 empirical probe -- fire evidence

Night-audit cycle-close · Leg E1 (empirical) · ADR-101 class `verification`; sandbox-isolated; real command output

All experimental work ran in a throwaway sandbox at
`C:/Users/1028120/AppData/Local/Temp/claude/C--Users-1028120-Documents-Dev--dev-knowledge--claude-worktrees-night-audit-cycle-close/187c6161-1b47-4466-93c7-b5554b882e23/scratchpad/e1-sandbox`.
Neither the WORKTREE nor the PRIMARY tree was written to except this one report file
(verified: `git status --porcelain` in both trees before/after showed no changes
attributable to this leg -- PRIMARY clean throughout, WORKTREE's pre-existing
untracked files belong to sibling night-audit legs, not this one).

## Proof A -- fleet_parity MUST-uniform probes fire

**Step 1 -- existing negative-fixture suite.** Ran the repo's own test file against
the worktree checkout:

```
$ cd <WORKTREE> && py -m pytest tests/test_fleet_parity.py -q
......................................................                   [100%]
54 passed in 195.59s (0:03:15)
```

54/54 passed (54 `def test_` functions in the file, confirmed by grep count --
matches the pytest tally exactly, so this is a real full-suite run, not a subset).

**Honest gap found:** grepping `tests/test_fleet_parity.py` for the 4 ARC-4 leg-1
universal-key surface ids (`ruff-target-version`, `ruff-line-length`,
`ruff-required-version`, `pytest-minversion`) and for their probe type
(`file_contains`) returns **zero matches**. The suite's existing `MUST_ABSENT`
fixture tests (e.g. lines 704/710, `test_...` around `src-dir` /
`docs-handoffs-dir`) exercise the `dir_tracked` probe type on synthetic
fixture repos, not `file_contains` on the real fleet. So the 54-test suite proves
the verdict ENGINE fires MUST-absent correctly in general, but does **not**
directly exercise these 4 specific rows. That gap is exactly what Step 2 below
closes empirically, against real fleet data.

**Step 2 -- seeded live divergence.** Copied the real manifest
(`ecosystem/parity-surfaces.yaml`, 46554 bytes) into the sandbox twice
(`parity-surfaces-baseline.yaml` unmutated, `parity-surfaces-seeded.yaml` with
one edit: the `ruff-line-length` row's probe token changed from
`'line-length = 120'` to `'line-length = 88'` -- i.e. the MUST-uniform expected
value is mutated so every real fleet member now diverges from the checker's
expectation, without touching any consumer file). Drove `fleet_parity.walk()`
in-process (imported straight from the worktree `scripts/` dir) with
`hub_root=<WORKTREE>` and `manifest_path=<sandbox copy>` -- the documented
override params (`walk(run_date, *, hub_root=..., manifest_path=..., ...)`,
`scripts/fleet_parity.py` L1788-1792). `walk()` itself performs no writes (only
its CLI wrapper `main()` writes the digest/events, per L1890-1909); calling
`walk()` directly is therefore a pure read-only probe against the real fleet
(hub = worktree, consumers = real sibling repos resolved via the standard
dev-dir fallback), and never touches PRIMARY.

Driver script: `<sandbox>/proof-a/run_probe.py`. Real output, both runs, verbatim:

```
=== BASELINE (unmutated sandbox copy) run (manifest=parity-surfaces-baseline.yaml) ===
total findings: 196; universal-key findings: 12; BLOCKING among universal-key findings: 0
repo_id                    surface_id               verdict          evidence
.dev-knowledge             pytest-minversion        AT-PARITY        present + faithful: pyproject.toml contains 'minversion = "9.0"'
ai-council                 pytest-minversion        AT-PARITY        present + faithful: pyproject.toml contains 'minversion = "9.0"'
corp-monorepo              pytest-minversion        AT-PARITY        present + faithful: pyproject.toml contains 'minversion = "9.0"'
.dev-knowledge             ruff-line-length         AT-PARITY        present + faithful: pyproject.toml contains 'line-length = 120'
ai-council                 ruff-line-length         AT-PARITY        present + faithful: pyproject.toml contains 'line-length = 120'
corp-monorepo              ruff-line-length         AT-PARITY        present + faithful: pyproject.toml contains 'line-length = 120'
.dev-knowledge             ruff-required-version    AT-PARITY        present + faithful: pyproject.toml contains 'required-version = ">=0.15.5"'
ai-council                 ruff-required-version    AT-PARITY        present + faithful: pyproject.toml contains 'required-version = ">=0.15.5"'
corp-monorepo              ruff-required-version    AT-PARITY        present + faithful: pyproject.toml contains 'required-version = ">=0.15.5"'
.dev-knowledge             ruff-target-version      AT-PARITY        present + faithful: pyproject.toml contains 'target-version = "py311"'
ai-council                 ruff-target-version      AT-PARITY        present + faithful: pyproject.toml contains 'target-version = "py311"'
corp-monorepo              ruff-target-version      AT-PARITY        present + faithful: pyproject.toml contains 'target-version = "py311"'

=== SEEDED (ruff-line-length token mutated to 'line-length = 88') run (manifest=parity-surfaces-seeded.yaml) ===
total findings: 196; universal-key findings: 12; BLOCKING among universal-key findings: 3
repo_id                    surface_id               verdict          evidence
.dev-knowledge             pytest-minversion        AT-PARITY        present + faithful: pyproject.toml contains 'minversion = "9.0"'
ai-council                 pytest-minversion        AT-PARITY        present + faithful: pyproject.toml contains 'minversion = "9.0"'
corp-monorepo              pytest-minversion        AT-PARITY        present + faithful: pyproject.toml contains 'minversion = "9.0"'
.dev-knowledge             ruff-line-length         MUST-absent      MUST surface absent: pyproject.toml contains 'line-length = 88'
ai-council                 ruff-line-length         MUST-absent      MUST surface absent: pyproject.toml contains 'line-length = 88'
corp-monorepo              ruff-line-length         MUST-absent      MUST surface absent: pyproject.toml contains 'line-length = 88'
.dev-knowledge             ruff-required-version    AT-PARITY        present + faithful: pyproject.toml contains 'required-version = ">=0.15.5"'
ai-council                 ruff-required-version    AT-PARITY        present + faithful: pyproject.toml contains 'required-version = ">=0.15.5"'
corp-monorepo              ruff-required-version    AT-PARITY        present + faithful: pyproject.toml contains 'required-version = ">=0.15.5"'
.dev-knowledge             ruff-target-version      AT-PARITY        present + faithful: pyproject.toml contains 'target-version = "py311"'
ai-council                 ruff-target-version      AT-PARITY        present + faithful: pyproject.toml contains 'target-version = "py311"'
corp-monorepo              ruff-target-version      AT-PARITY        present + faithful: pyproject.toml contains 'target-version = "py311"'

=== SUMMARY ===
baseline blocking count (4 universal keys): 0
seeded   blocking count (4 universal keys): 3
PROOF A ASSERTION: PASS -- baseline=0 blocking, seeded>=1 blocking
```

### Per-key verdict table (baseline -> seeded)

| surface_id | tier | baseline verdict (all 3 fleet members) | seeded verdict (all 3 fleet members) | fired? |
|---|---|---|---|---|
| ruff-target-version | MUST/MUST | AT-PARITY x3 | AT-PARITY x3 (untouched key) | n/a -- control |
| ruff-line-length | MUST/MUST | AT-PARITY x3 | **MUST-absent x3** | YES |
| ruff-required-version | MUST/MUST | AT-PARITY x3 | AT-PARITY x3 (untouched key) | n/a -- control |
| pytest-minversion | MUST/MUST | AT-PARITY x3 | AT-PARITY x3 (untouched key) | n/a -- control |

The mutated key alone flips from 0 to 3 blocking `MUST-absent` verdicts (one per
fleet member that carries the row: `.dev-knowledge` hub, `ai-council`,
`corp-monorepo` -- `corp-ops`/`corp-sca` are `pre-deploy` and rendered
`skipped-pre-deploy`, not walked); the other 3 keys stay at-parity in both runs,
confirming the probe fires precisely on the seeded key and nowhere else
(no bleed-through).

## Proof B -- two-tier gate (compliant proceeds / unsanctioned blocks)

### Pure classifier calls

Imported `validate_hermetization` straight from the worktree `scripts/` dir (no
subprocess, no git) and called `classify(path)` directly:

```
COMPLIANT: classify('docs/audits/2026-07-19-technical-night-demo.md') -> None
VIOLATION new top-level dir: classify('newdir/foo.md') -> "unsanctioned new top-level directory 'newdir/' -- Tier-1 dirs are a closed set (ADR-101 section 1); surface a new top-level dir via an ADR-101 amendment before creating it"
VIOLATION new docs genre folder: classify('docs/newgenre/x.md') -> "unsanctioned new docs genre folder 'docs/newgenre/' -- Tier-2 genres are a closed set (ADR-101 section 1); a new artifact class nests under an existing genre or is surfaced via an ADR-101 amendment"
VIOLATION off-grammar audit name (uppercase/underscore): classify('docs/audits/2026-07-19-BADCLASS_Report.md') -> "casing: '2026-07-19-BADCLASS_Report.md' must be all-lowercase kebab-case everywhere incl. the .md extension (no UPPERCASE, no _underscore_, no CamelCase; only a `.` inside the slug for a repo/version token) -- ADR-101 R4"
VIOLATION off-grammar audit name (unknown class): classify('docs/audits/2026-07-19-notaclass-x.md') -> "class: '2026-07-19-notaclass-x.md' has no CLOSED-enum <class> token after the date (ADR-101 R3: technical/functional/qa/census/verification/ecosystem-audit/conformance-nightly-digest/changelog-review/codex/fresh-eyes/incident-evidence; whole-token longest-match)"
```

| input | return value | classified as |
|---|---|---|
| `docs/audits/2026-07-19-technical-night-demo.md` | `None` | compliant -- proceeds |
| `newdir/foo.md` | Rule A: unsanctioned top-level dir | BLOCK |
| `docs/newgenre/x.md` | Rule A: unsanctioned docs genre | BLOCK |
| `docs/audits/2026-07-19-BADCLASS_Report.md` | Rule B: R4 casing violation | BLOCK |
| `docs/audits/2026-07-19-notaclass-x.md` | Rule B: no closed-enum class token | BLOCK |

All 5 match the expected classification exactly.

### Integration -- throwaway git repo, hook wired via `core.hooksPath`

Built a disposable git repo at `<sandbox>/proof-b-repo`, copied
`validate_hermetization.py` in, and wired it as a `core.hooksPath` pre-commit
hook (`.githooks/pre-commit` -> `py validate_hermetization.py`, no `--no-verify`
used on any of the test commits below).

**1. Compliant commit (expect proceed, exit 0):**

```
$ git add docs/audits/2026-07-19-technical-night-demo.md
$ git commit -m "docs: add compliant night-demo audit"
[master 1e3ce48] docs: add compliant night-demo audit
 1 file changed, 1 insertion(+)
 create mode 100644 docs/audits/2026-07-19-technical-night-demo.md
EXIT_CODE=0
```

**2. Violation commit -- Rule A, unsanctioned top-level dir (expect refuse, exit 1):**

```
$ git add newdir/foo.md
$ git commit -m "chore: attempt unsanctioned top-level dir add"
validate_hermetization: refused -- ADR-101 hermetization violation(s):
  newdir/foo.md: unsanctioned new top-level directory 'newdir/' -- Tier-1 dirs are a closed set (ADR-101 section 1); surface a new top-level dir via an ADR-101 amendment before creating it
  The tree is hermetic (ADR-101): a new top-level entry / docs genre, or an off-grammar audit filename, is a deliberate ADR-101 amendment -- not a drive-by add. Bypass (peer-hook parity): git commit --no-verify.
EXIT_CODE=1
---git status---
A  newdir/foo.md
```

File stays staged, never committed (`git log` confirms HEAD is still the compliant
commit `1e3ce48` at this point).

**3. Violation commit -- Rule B, off-grammar audit filename (expect refuse, exit 1):**

```
$ git add docs/audits/2026-07-19-BADCLASS_Report.md
$ git commit -m "chore: attempt off-grammar audit filename"
validate_hermetization: refused -- ADR-101 hermetization violation(s):
  docs/audits/2026-07-19-BADCLASS_Report.md: casing: '2026-07-19-BADCLASS_Report.md' must be all-lowercase kebab-case everywhere incl. the .md extension (no UPPERCASE, no _underscore_, no CamelCase; only a `.` inside the slug for a repo/version token) -- ADR-101 R4
  The tree is hermetic (ADR-101): a new top-level entry / docs genre, or an off-grammar audit filename, is a deliberate ADR-101 amendment -- not a drive-by add. Bypass (peer-hook parity): git commit --no-verify.
EXIT_CODE=1
---git status---
A  docs/audits/2026-07-19-BADCLASS_Report.md
---git log---
1e3ce48 docs: add compliant night-demo audit
6df2169 seed
```

Final `git log` shows exactly ONE audit-doc commit landed (the compliant one);
both violations (Rule A and Rule B) were refused at commit time and never
entered history. Two-tier gate confirmed both ways, on both rules.

## Proof C -- sandbox pattern (seed for S9a)

Reusable convention demonstrated by this leg, precise enough to codify as the
dynamic/sandbox-testing stage referenced by S9 gap (a):

1. **Worktree-based scratch copy, never the primary.** All mutated fixtures
   (manifests, config files) are `cp`'d from the WORKTREE (the git-tracked
   source of truth being audited) into a scratchpad directory OUTSIDE any
   git-tracked tree. Mutation happens ONLY on the scratch copy; the source file
   is read but never opened for write. This gives a negative-test fixture that
   is byte-identical to production except for the one seeded divergence, without
   ever risking a stray `git add`/commit in a tracked tree.
2. **Import-and-drive over subprocess, when the tool exposes a pure/documented
   seam.** `fleet_parity.py` exposes `walk(run_date, *, hub_root=..., manifest_path=...)`
   as an explicit override-friendly seam (the same seam its own test suite and
   `audit.py::check_fleet_parity` use). Importing the module straight from the
   WORKTREE's `scripts/` dir (`sys.path.insert`) and calling `walk()` directly
   is faster and more precise than shelling out to the CLI, and -- verified by
   reading the source -- performs strictly fewer side effects than the CLI
   (`walk()` writes nothing; only `main()` writes the digest/events files), so
   it is the correct read-only probe entry point. The general rule: before
   building a sandbox probe, read the target script far enough to find its
   pure/parametrized core function and drive THAT, not the CLI wrapper, unless
   the CLI's own exit-code/argv contract is what's under test.
3. **Output-redirect isolation for anything that DOES write.** For a tool with
   no pure seam (or when the CLI contract itself is the thing being tested,
   as in Proof B), point every writable path at the sandbox: run inside a
   throwaway git repo, pass `--no-write`/`--no-events`-style flags where
   available, or (as done here) skip the writing entry point (`main()`)
   entirely in favor of the pure one (`walk()`).
4. **Throwaway git repo for hook/gate integration proofs.** `git init` a
   disposable repo under the sandbox, copy in only the artifact under test
   (here: `validate_hermetization.py`), wire it via `core.hooksPath` pointing
   at a local `.githooks/` dir (avoids touching the real `.git/hooks` of any
   tracked repo, and avoids needing `pre-commit` installed). Drive it with real
   `git add` / `git commit` cycles -- never `--no-verify` when the point IS to
   prove the hook fires -- and assert on the real exit code + `git log` state
   (did the violating commit actually land, or not).
5. **Negative-test discipline.** Every probe pairs a baseline (unmutated
   copy / compliant input, expect 0 blocking / exit 0) with a seeded run
   (one deliberate divergence, expect >=1 blocking / exit 1) run back to back
   with the SAME driver, so the contrast is apples-to-apples and the delta is
   attributable to exactly the one seeded change (Proof A's 3 control keys
   staying AT-PARITY in both runs is the evidence the mutation didn't leak).
6. **Cleanup-free by construction.** Because nothing is ever created inside a
   git-tracked tree except the one final report, there is no teardown step for
   the probes themselves -- the entire sandbox directory (manifests, driver
   scripts, throwaway git repos) can be deleted wholesale with no effect on
   WORKTREE or PRIMARY. (The sandbox dir itself is left in place per this run's
   instructions for orchestrator spot-verification; it is not git-tracked.)

## Verdict

| Proof | Result | Decisive evidence |
|---|---|---|
| A -- fleet_parity MUST-uniform probes fire | **PASS** | baseline (unmutated manifest, real fleet): 0/12 universal-key findings blocking. Seeded (1 of 4 keys mutated): 3/12 blocking (`MUST-absent` x3, one per carrying fleet member), other 3 keys unchanged at AT-PARITY. Existing 54-test suite (`test_fleet_parity.py`) passes 54/54 but has NO dedicated fixture for these 4 rows / the `file_contains` probe type -- this empirical run is the first direct fire-proof of these specific rows against real fleet data. |
| B -- two-tier gate (compliant proceeds / unsanctioned blocks) | **PASS** | 5/5 pure `classify()` calls matched expected verdict (1 compliant `None`, 4 violations across both rules). Integration: compliant commit landed (exit 0, `1e3ce48`); Rule A violation refused (exit 1, file stayed staged, never committed); Rule B violation refused (exit 1, file stayed staged, never committed). Final `git log` shows exactly one audit-doc commit. |
| C -- sandbox pattern recorded | **PASS** | Pattern above (worktree-scratch-copy + pure-seam-drive + output-redirect isolation + throwaway git repo + negative-test pairing + no-teardown-needed) is precise enough to codify as the S9a dynamic-testing stage; it is the exact pattern this leg executed for both A and B. |
