# [#502] Shape B (`pythonpath`) — measurement, not adoption

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-08 · **Slug:** 502-pythonpath-measurement
- **Source-session:** hub sandbox worktree `lane-502-pythonpath-measure`, branch
  `worktree-lane-502-pythonpath-measure`; base `3ed60c4c`
- **Status:** MEASUREMENT ONLY. **Zero adoptions, zero `pyproject.toml` change survives this commit.**
  The experimental edits were applied, measured, and discarded; only this report and the mandated
  `docs/audits/README.md` regen are committed.
- **Model:** one Opus-class seat (orchestration + classification); haiku fan-out for census retrieval only.
- **Consumer:** the architect, who rules on adoption. This report recommends nothing beyond what the
  numbers show.

**The question this arc was given:** with Shape B in place and the test-side `sys.path.insert` lines
removed, **how many tests break, and are the breaks real coupling or nothing?**

**The answer:** as literally specified (`pythonpath = ["."]`), **67 of 99 test files fail to collect** —
and **every one of those failures is bucket (b)**, an import needing a different path root, with **zero**
real hidden coupling and **zero** noise. With the path root corrected to `[".", "scripts", "deploy"]`,
the suite is **outcome-identical to baseline: 2 failed / 2544 passed / 9 skipped, the same two
pre-existing REDs, zero delta failures**, and every test file collects standalone. Shape B works in this
repo, but only at the corrected roots — `["."]` alone is not a viable spelling of it here.

---

## §1 Census (live) — memo confirmed, with one correction

Measured on the live tree at `3ed60c4c` via `git`-tracked `*.py` only.

| Area | Occurrences | Files | Memo claimed | Verdict |
|---|---|---|---|---|
| `tests/` | 75 | 71 | 75-in-71 | confirmed |
| `scripts/` | **18** | 15 | 19-in-15 | **corrected −1 occurrence** (file count confirmed) |
| `deploy/` | 6 | 6 | 6-in-6 | confirmed |
| **Total** | **99** | **92** | 100 / 92 | occurrences **99, not 100**; file count confirmed |

`conftest.py`: **absent everywhere** in the repo — confirmed (`**/conftest.py` → no matches).

**Substrate correction that matters more than the count:** `scripts/` and `deploy/` contain **no
`__init__.py`**. The only `__init__.py` files under them belong to the `scripts/codemap`,
`scripts/toc` and `deploy/lived_sandbox` subpackages. Tests therefore import **bare module names**
(`import audit`, `import tool`, `import carrier_precommit`), not dotted paths. This single fact
determines the entire Arm 1 result below.

### 1a. One of the 75 test-side sites is not an executable insert

`tests/test_enforcement_coverage.py:389` is:

```
f"sys.path.insert(0, r'{ec._SCRIPTS_DIR}')\n"
```

— an f-string that **generates the source of a pre-commit hook script**, written to `tmp_path` and run
as a **subprocess**. It is data, not an import bootstrap. pytest's `pythonpath` configures the pytest
process's `sys.path` and has no effect on a spawned subprocess, so Shape B can neither remove nor
replace this site. The removal in §3 was regex-anchored (`^\s*sys\.path\.insert\(`) specifically to
leave it alone: **74 removed, 1 correctly skipped, 74 + 1 = 75.**

---

## §2 Method

All three suite runs used the **identical command**, from the worktree root:

```
uv run pytest -q
```

Environment: `uv sync --locked --group analytics` (the analytics group is required in a fresh lane
venv, else ~17 pandas REDs appear that have nothing to do with this experiment).

**A second instrument was necessary.** The parallel default (`addopts = "-n auto"`) proved to be an
**unreliable instrument for this specific question**, for a reason documented in §4a: `sys.path`
pollution leaks between test modules that share an xdist worker, so the aggregate error count
understates true per-file breakage by a factor of three. Each configuration was therefore **also**
probed per-file in isolation:

```
uv run pytest --collect-only -q -n 0 -p no:cacheprovider <one test file>
```

one process per test file, 99 files. This is the honest measure of whether a file can stand on its own.

---

## §3 What the experiment changed

- `pyproject.toml`: one line added directly under `[tool.pytest.ini_options]`.
- `tests/**.py`: **74 `sys.path.insert(...)` lines deleted across 71 files** (the 75th left in place per §1a).
- **Untouched, deliberately:** all 18 `scripts/` and all 6 `deploy/` insertions — Shape B is test-time
  only, and that limitation is itself a finding (§5). The contract's held-by-live-lane exclusion list
  (`scripts/audit.py`, `scripts/batch_manifest.py`, `scripts/fleet_*.py`, `scripts/gitenv.py`,
  `deploy/carrier_floor.py`, `deploy/manifest-v*.yaml`) is entirely non-test and was therefore never
  in scope for the edit; no file on that list was modified at any point.

Diff shape at the moment of measurement: `72 files changed, 1 insertion(+), 74 deletions(-)`.

---

## §4 Results

| Configuration | failed | passed | skipped | errors | duration | **isolated collection failures** |
|---|---|---|---|---|---|---|
| **Baseline** (75 inserts, no `pythonpath`) | 2 | 2544 | 9 | 0 | 789.04s (13m09s) | **0 / 99** |
| **Arm 1** — `pythonpath = ["."]` (contract-literal) | 1 | 1929 | 6 | **20** | 427.36s (7m07s) | **67 / 99** |
| **Arm 2** — `pythonpath = [".", "scripts", "deploy"]` | 2 | 2544 | 9 | 0 | 615.27s (10m15s) | **0 / 99** |

**The two baseline failures are pre-existing and environmental, not caused by anything in this arc:**

- `tests/test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary` — inverts by
  construction inside a linked worktree (the lane's own path *is* a linked worktree).
- `tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row` — asserts
  `"1 declared routine row"`; the live BACKLOG now declares 2. Landed work from another lane.

Both appear identically in baseline and Arm 2, so they cancel in the delta. **Arm 2's delta against
baseline is zero on every axis: same failures, same pass count, same skip count.**

**Durations are not a finding.** This machine ran other lanes concurrently throughout; the baseline's
789s against the `pyproject.toml` comment's recorded 330–360s is contention, not regression. The three
durations are reported for completeness and should not be read as a performance comparison.

### 4a. Why the parallel run undercounts — the instrument defect

Arm 1's parallel run reported **20** collection errors. Isolated, the same configuration produces **67**.
The 47-file gap is not flake; it has a specific mechanism:

Several test files load `scripts/` modules by **file path** via `importlib.util.spec_from_file_location`,
bypassing `sys.path` entirely — e.g. `tests/test_validate_backlog.py`,
`tests/test_session_end_backpressure.py`, `tests/test_window_metrics.py`,
`tests/test_validate_hermetization.py` (all four collect fine in isolation, precisely because they never
needed `sys.path`). Those `scripts/` modules then execute their **own module-level**
`sys.path.insert(0, _SCRIPTS_DIR)` — e.g. `scripts/fleet_analytics.py:110`, `scripts/boundary_headers.py:57`,
`scripts/block_unanchored_push.py:53`, `scripts/codemap_hook.py:12`, `scripts/toc_hook.py:12`. That
insertion mutates the **worker process's** `sys.path`, so every test module imported *later in the same
xdist worker* silently inherits a working path.

Consequence: under Arm 1, whether a given test file imports **depends on which worker it lands in and
what ran before it**. `tests/test_ship_gate.py` (`import audit as aud`) passed in the parallel run and
**fails in isolation**. That is order-dependent success — the failure mode a parallel suite is worst at
reporting. It is recorded here because it generalises beyond this arc: **for any question about import
wiring, the `-n auto` aggregate is not admissible evidence; the per-file isolated probe is.**

### 4b. Classification of every Arm 1 delta failure

Required buckets: (a) real coupling the insert was hiding, (b) an import that needs a different path
root, (c) noise/flake.

| Bucket | Count | Evidence |
|---|---|---|
| (a) real coupling | **0** | No failure had any signature other than a missing bare module. Zero import cycles, zero fixture-ordering breaks, zero state leakage surfaced. |
| **(b) different path root** | **67** | Every one of the 67 isolated failures raised `ModuleNotFoundError: No module named '<bare>'` across **39 distinct modules** — all of them files sitting in `scripts/` or `deploy/`, neither of which is on the path under `["."]`. |
| (c) noise/flake | **0** | Arm 1 was not re-run for flake because there was nothing unexplained to re-run: 67 of 67 failures carry a deterministic missing-module signature, and Arm 2 reproduces baseline exactly. |

Missing-module frequency (top of 39 distinct): `audit` ×20, `carrier_precommit` ×4, `carrier_floor` ×2,
`carrier_plugin` ×2, `contract` ×2, `fleet_parity` ×2, `gen_handoff` ×2, `lived_sandbox` ×2, then 31
modules at ×1 (`validate_doc_claims`, `validate_no_ff`, `gen_task_tree`, `toc`, `codemap`,
`worktree_seed`, `release_lint`, …).

**Every single Arm 1 failure is bucket (b), and bucket (b) is fully discharged by Arm 2.** The count of
tests that break because the insert was hiding something real is **zero**.

---

## §5 Residual — what Shape B cannot reach

Shape B is a **pytest** setting. It configures the path of the pytest process and nothing else.

**24 non-test insertions are structurally out of its reach** (the memo said 25; the live count is 24,
per the §1 `scripts/` correction):

- **`scripts/` — 18 occurrences in 15 files.** These run when a git hook or CLI invokes the script
  directly (`uv run --locked python scripts/<x>.py`), with no pytest in the process at all.
  14 of the 18 are indented — lazy/conditional inserts inside functions or `try` blocks.
  Sites: `block_ff_push.py:65`, `block_unanchored_push.py:53`, `boundary_headers.py:57`,
  `boundary_report.py:46`, `check_seal_identity.py:33`, `codemap_hook.py:12`,
  `desired_state_loader.py:29`, `desired_state_report.py:39`, `enforcement_coverage.py:323,741`,
  `fleet_analytics.py:110`, `fleet_health.py:277`, `fleet_parity.py:93`,
  `gen_handoff.py:398,494,573`, `gen_intake_tree.py:77`, `toc_hook.py:12`.
- **`deploy/` — 6 occurrences in 6 files:** `carrier_floor.py:67`, `release_lint.py:157`, `tool.py:58`,
  `lived_sandbox/arc.py:37`, `lived_sandbox/observe.py:385`, `lived_sandbox/spawn.py:30`.

**Plus 1 test-side site Shape B cannot remove:** `tests/test_enforcement_coverage.py:389` (§1a) — a
subprocess-code string literal.

So of the 99 live occurrences, Shape B can retire **74**, and **25 sites remain** (24 non-test + 1
test-side literal). Adoption would therefore **reduce, not eliminate**, the `sys.path.insert` idiom in
this repo — and the surviving `scripts/` module-level inserts are exactly the ones that produce the §4a
cross-worker pollution, which would persist unchanged.

---

## §6 What adoption would cost — derived only from measurements

Adopting Shape B at the **corrected** roots costs **one line in `pyproject.toml` and the deletion of 74
lines across 71 test files**, and buys a suite whose measured outcome is **indistinguishable from
baseline** (2/2544/9 both ways, same two REDs) while every test file additionally collects **standalone**
(0/99 isolated failures, matching baseline's 0/99). No test needed rewriting; no import needed
re-rooting beyond the config line; no fixture or ordering change was required.

The measured caveats, all of which are properties of the repo rather than objections to Shape B:

1. **`pythonpath = ["."]` — the exact spelling the contract froze — is not viable here.** It breaks 67 of
   99 files, because `scripts/` and `deploy/` are not packages and tests import bare module names. Any
   adoption must be `[".", "scripts", "deploy"]`. The `["."]` figure is the measurement of a spelling,
   not of the shape.
2. **Coverage is partial: 74 of 99 sites.** 25 sites survive (§5), all of them outside pytest's reach.
   A claim that Shape B "removes the `sys.path` idiom" would be false; "removes it from the test tree,
   except one string literal" is the true statement.
3. **The `scripts/`-side inserts keep leaking across xdist workers** (§4a) whether or not Shape B is
   adopted. Shape B does not fix that, and does not make it worse.
4. **The three durations are contention-dominated** and support no performance claim in either direction.

Two things this arc deliberately does not do: it makes **no recommendation on adoption**, and it says
nothing about Shape A or Shape C. Shape C is excluded without an ADR (it reverses the recorded
`package = false` stance); Shape A is permitted-not-mandated per `[#430](a)` / STANDING_RULINGS F5.
The architect rules.

---

## §7 Provenance and disposal

- Baseline, Arm 1 and Arm 2 were run in that order in the same worktree, same venv, same command.
- **The experiment was discarded before the commit** (`git checkout -- .`), and the discard was verified
  rather than assumed: `pythonpath` occurrences in `pyproject.toml` back to **0**, `sys.path.insert`
  occurrences under `tests/` back to **75**, `git status` clean, HEAD unmoved at `3ed60c4c`.
- The baseline isolated probe (0/99) was run **after** the discard, on the restored tree, which is what
  makes it a like-for-like control for Arm 2's 0/99 rather than a claim about a tree that no longer existed.
- No `pyproject.toml` change is part of this commit. The only files committed are this report and the
  hook-mandated `docs/audits/README.md` regeneration.
