# Phase 0 baselines — commit-tax, mutation pilot, hotspot ranking, lane-grammar verify

> **EXTERNAL EVIDENCE — advisory until ratified, never doctrine by virtue of existing.**
> **STATUS: DRAFT.** This document decides nothing, adopts nothing, and births no BACKLOG row.
> No config file, dependency, hook, workflow or protocol was edited by the arc that produced it.

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-18
- **Arc:** phase 0 — baselines + preconditions · branch `docs/phase0-baselines`
- **Measurement host:** operator host, primary checkout, quiet tree (sole writer; CPU 1% at start;
  no other local job ran during any measurement)
- **Tree measured:** `409374fd12e931fff03cf4a6a781a7fe2b4984a0` (= `main` = `origin/main` at start)

**What this is.** The four inputs later acts of this session consume. It records measurements and
landings only. Every command is quoted verbatim so each number is reproducible by paste.

---

## T0.1 — audit-health commit-tax on a quiet tree

**What was measured.** The pre-commit hook's own `entry`, not an abstract script — the commit-tax
is the cost of the invocation the gate actually makes. Quoted from `.pre-commit-config.yaml:172`:

```
entry: uv run --locked python scripts/audit.py health
```

The same file's comment at `.pre-commit-config.yaml:171` claims **`~1.4s`**.

**Command run (3x, serially, nothing else running):**

```
uv run --locked python scripts/audit.py health
```

| run | wall time | exit | verdict line |
|---|---|---|---|
| 1 | 290.875 s | 0 | `health: OK` |
| 2 | 287.878 s | 0 | `health: OK` |
| 3 | 302.092 s | 0 | `health: OK` |

- **median: 290.9 s** · min 287.9 s · max 302.1 s · **spread 14.2 s (4.9 % of median)**
- The spread is small, so the reading is stable, not a one-off outlier.

**Interpreter-path pair (one run each, back to back, same quiet tree):**

| path | command | wall time | exit |
|---|---|---|---|
| venv-direct | `.venv/Scripts/python.exe scripts/audit.py health` | 287.274 s | 0 |
| uv (hook path) | `uv run --locked python scripts/audit.py health` | 283.606 s | 0 |

**Interpreter gap: none.** `uv run --locked` measured 3.7 s **faster** (1.3 %) than direct venv
Python — inside the run-to-run spread above. `uv` resolution overhead is not a contributor, and the
"it's the interpreter path" hypothesis is dead. Both paths run the same `Python 3.12.10`;
`uv 0.11.19`.

### Verdict line

**The regression is REAL.** Median 290.9 s against the recorded 42.2 s is **6.9x** — well past the
>=5x threshold, and nowhere near the ~2x that would have made 42.2 s a contention artifact. The
2026-08-18 recon reading of 373 s was inflated by CPU contention (373 s -> 290.9 s quiet, ~22 %
attributable to load), but contention explains only that margin, **not the 6.9x gap itself**. The
`~1.4s` comment at `.pre-commit-config.yaml:171` is stale by more than two orders of magnitude.

**Decision-relevance for L1's value claim:** every commit in this repo pays ~291 s of
`audit-health` before anything else in the hook chain runs. A cost model built on 42.2 s — or on
the file's own `~1.4s` — understates the per-commit tax by 6.9x / 208x respectively.

---

## T0.2 — [#502] mutation pilot (remote)

**Remote trigger exists**, so the fork-c local-fallback default was **not** taken:
`.github/workflows/report-only-wall.yml` declares `workflow_dispatch` at workflow level, and the
`mutation-pilot` job's `if:` short-circuits on `github.event_name == 'workflow_dispatch'`. Local
execution was never an option regardless — the job's own comment records that mutmut requires
`fork()`, which Windows does not provide.

**Dispatched:** `gh workflow run "report-only wall" --ref main`

**Run:** <https://github.com/rdwornik/dev-knowledge/actions/runs/32127150367> (`workflow_dispatch`,
head `409374fd`) · `changes` 11 s OK · `record` 8 m 42 s OK · **`mutation-pilot` 1 m 50 s**, mutmut
exit `1`.

### Result: the pilot RAN and produced ZERO survivor data

| quantity | value |
|---|---|
| mutants generated | **2291** (1 file mutated, 95 ignored, 0 unmodified; 51.97 s to generate) |
| killed | 0 |
| survived | 0 |
| **not checked** | **2291 (100 %)** |

The run stopped early. mutmut's own diagnostic, verbatim from `mutmut.out`:

```
Stopping early, because tests recorded trampoline hits but none match any mutant key. It looks
like tests import the source under a different module path than mutmut sees from the file path.
Recorded keys (e.g.): ['fleet_analytics.x__git', 'fleet_analytics.x__git_common_dir', ...]
Expected keys (e.g.): ['scripts.fleet_analytics.x__atomic_write', 'scripts.fleet_analytics.x__git', ...]
Common causes: a pythonpath setting in pytest config, conftest sys.path injection, or a source dir
other than ./, src/, or source/.
```

**Reading, stated plainly.** The tests import `fleet_analytics` (the suite puts `scripts/` on
`sys.path`); mutmut derives `scripts.fleet_analytics` from the file path. The two key spaces never
intersect, so no mutant is ever attributed to a test, and mutmut halts rather than report a false
100 % survival. This is a **configuration/import-path mismatch, not a test-quality signal** — the
2291 `not checked` entries say nothing whatsoever about `tests/test_fleet_analytics.py`.

**Not new, and now larger.** The workflow's own LA-4 comment records the identical outcome at an
earlier scope: *"every one of those runs reported all 84 mutants `not checked`"*. The failure mode
is unchanged; only the mutant count has grown 84 -> 2291.

**Input to decision 6, honestly stated:** the pilot **cannot** yield a surviving-mutant count in
its current configuration, and no run of it will until the module-path mismatch is resolved. The
calibration case the workflow names (`test_canonical_path_survives_a_cycle`) was never exercised.
The open leg of [#502] is therefore still open, and this arc adds no ADOPT/REJECT verdict — that is
the architect's.

**Artifacts:** run artifact `mutation-pilot-409374fd...` (id 9320833974, 8797 B, 90-day retention).

---

## T0.6 — `LANE_BRANCH_RE` verify (read-only)

**Pattern, quoted verbatim** — `scripts/validate_branch_naming.py:85`, with `_SLUG` from line 78:

```
_SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
LANE_BRANCH_RE = re.compile(rf"^worktree-lane-[a-z]-\d+-{_SLUG}$")
```

Fully expanded: `^worktree-lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$`

It is defined **once**, in the enum module, and imported by `scripts/batch_manifest.py:134`
(`tests/test_batch_manifest.py:586` asserts the two names resolve to the same object).

**Assertions** — `re.fullmatch` against the live compiled pattern:

| candidate lane branch | result |
|---|---|
| `worktree-lane-a-533-leg2` | **PASS** |
| `worktree-lane-b-529-wiring` | **PASS** |
| `worktree-lane-c-554-devcontainer` | **PASS** |
| `worktree-lane-d-558-vision` | **PASS** |

**4/4 PASS. No rename is required for the coming lane batch.** Nothing was renamed.

---

## T0.5 — section-D churn x complexity hotspot baseline

### The binding sentence, quoted verbatim from intake #31 section D

> **Refactor only where high churn ∩ high complexity, tests first where coverage is thin;
> everywhere else, ratchets + opportunistic improvement as agents touch the code.**

Section D's stated procedure order: *"churn-vs-complexity hotspot analysis (change frequency is the
better-supported signal; a small fraction of files typically carries most of the work) · complexity
and file-length distributions · coverage on the hotspots · duplication rate · dependency cycles."*
This arc executes **steps 1 and 2**; coverage, duplication and cycles are not run here and are
recorded as open below.

### Method (library-first; no new committed scripts, no new dependency)

**Churn window: 180 days.** Section D names no window — **fork-c default taken and recorded here.**

Complexity via the `radon` family section C of the same intake names, installed **ephemerally**
through `uv run --with` (the pattern the workflow already uses for mutmut): no `pyproject.toml`
entry, no `uv.lock` churn, nothing added to the operator environment.

```
# churn: commit-touch count per tracked .py file, 180-day window
git log --since="180 days ago" --pretty=format: --name-only -- '*.py' \
  | grep -E '\.py$' | sort | uniq -c | sort -rn

# complexity + file length (two invocations to cover every tracked .py home)
uv run --locked --with radon==6.0.1 python -m radon cc  -s --total-average -j scripts/ tests/
uv run --locked --with radon==6.0.1 python -m radon raw -j scripts/ tests/
uv run --locked --with radon==6.0.1 python -m radon cc  -s -j deploy/ plugins/ ecosystem/ .claude/
uv run --locked --with radon==6.0.1 python -m radon raw -j deploy/ plugins/ ecosystem/ .claude/
```

Score = `churn x cyclomatic`, where cyclomatic is the **sum of every block's complexity in the
file** and churn is the file's commit-touch count in the window. Corpus: `git ls-files '*.py'`.

**Corpus coverage, stated honestly:** 257 tracked `.py`; **223 scored**; 34 unscored because radon
finds no function/class block in them (package `__init__.py` files, codemap test fixtures, and the
three module-level-only files `scripts/toc_hook.py`, `scripts/codemap_hook.py`,
`scripts/audit_checks/registry.py`). Those 34 score 0 by construction, so none is a hidden hotspot.
Total corpus `churn x cc` = 272 845.

### Ranked hotspots (top 20)

| # | file | churn 180d | cyclomatic | sloc | churn x cc | cum % |
|---|---|---|---|---|---|---|
| 1 | `scripts/audit.py` | 135 | 709 | 2230 | 95715 | 35.1% |
| 2 | `tests/test_audit.py` | 65 | 637 | 1590 | 41405 | 50.3% |
| 3 | `scripts/fleet_parity.py` | 24 | 507 | 1527 | 12168 | 54.7% |
| 4 | `tests/test_fleet_parity.py` | 18 | 408 | 1079 | 7344 | 57.4% |
| 5 | `tests/test_doc_code_edge.py` | 41 | 155 | 435 | 6355 | 59.7% |
| 6 | `tests/test_verify_handoff_probes.py` | 20 | 311 | 743 | 6220 | 62.0% |
| 7 | `tests/test_lived_sandbox_observer.py` | 20 | 279 | 602 | 5580 | 64.1% |
| 8 | `tests/test_gen_task_tree.py` | 17 | 270 | 625 | 4590 | 65.7% |
| 9 | `tests/test_fleet_health.py` | 13 | 341 | 820 | 4433 | 67.4% |
| 10 | `deploy/carrier_floor.py` | 21 | 209 | 498 | 4389 | 69.0% |
| 11 | `scripts/gen_task_tree.py` | 19 | 231 | 676 | 4389 | 70.6% |
| 12 | `tests/test_deploy_floor.py` | 21 | 196 | 633 | 4116 | 72.1% |
| 13 | `tests/test_gen_handoff.py` | 15 | 228 | 554 | 3420 | 73.3% |
| 14 | `tests/test_enforcement_coverage.py` | 15 | 195 | 531 | 2925 | 74.4% |
| 15 | `deploy/tool.py` | 13 | 212 | 919 | 2756 | 75.4% |
| 16 | `scripts/enforcement_coverage.py` | 10 | 251 | 717 | 2510 | 76.3% |
| 17 | `scripts/fleet_health.py` | 14 | 179 | 522 | 2506 | 77.3% |
| 18 | `scripts/verify_handoff_probes.py` | 16 | 154 | 324 | 2464 | 78.2% |
| 19 | `tests/test_reverse_dep_oracle.py` | 24 | 73 | 155 | 1752 | 78.8% |
| 20 | `deploy/carrier_precommit.py` | 6 | 285 | 642 | 1710 | 79.4% |

**Concentration:** top-5 = **59.7 %** · top-10 = **69.0 %** · top-20 = **79.4 %** of total
`churn x cc`. Section D's premise — *"a small fraction of files typically carries most of the
work"* — **holds on this corpus, and strongly**: 2 files (0.9 % of the scored corpus) carry
**50.3 %**.

**`scripts/audit.py` is the hotspot**, at 35.1 % alone — 2.3x the next entry, and simultaneously
the highest churn (135) and the highest complexity (709) in the corpus. Its test file is #2.
Together the `audit.py` pair is over half the total. Note this is the same module T0.1 measures at
291 s.

### Complexity and file-length distributions (section D procedure step 2)

| metric (n=223 scored files) | median | p75 | p90 | p95 | max |
|---|---|---|---|---|---|
| sloc | 150 | 238 | 424 | 633 | 2230 |
| cyclomatic total per file | 54 | 94 | 158 | 229 | 709 |

Files > 500 sloc: **19**. Files > 1000 sloc: **4**. The distribution is long-tailed — the p95 file
is 4.2x the median and the max is 14.9x it.

### Mapping to section B's six gated items — MAPPING ONLY, no adoption verdicts

Adoption verdicts on section B are the architect's; this paragraph says only where each item would
land if adopted. **B-1 (ruff family expansion, `C901`/`PLR0912/0913/0915/1702`)** and **B-3 (count
ratchets)** bind hardest on rows 1–3: `scripts/audit.py` (cc 709, 2230 sloc), `tests/test_audit.py`
and `scripts/fleet_parity.py` are where a branch/size rule would fire first, and where a
baseline-and-ratchet rather than a fix-now posture is the difference between a landable gate and a
wall — B-1's own "per-file ignores for tests" carve-out is load-bearing here, since **11 of the top
20 are test files**. **B-2 (one type checker with a baseline)** sizes off the same rows: the
baseline's initial debt is dominated by rows 1–4, which are 57.4 % of the corpus score. **B-4
(import-linter contracts)** cannot be sized from this measurement at all — dependency cycles are
procedure step 5 and were not run. **B-5 (agent PostToolUse/PreToolUse gates)** is churn-driven
rather than complexity-driven, so it is row 1 and row 5 (`tests/test_doc_code_edge.py`, churn 41 at
modest cc 155) that would feel it most. **B-6 (config package + copier propagation)** is not
addressed by this measurement — it is a distribution concern, not a hotspot one. Section D's "tests
first where coverage is thin" clause **cannot be discharged from this artifact**: coverage on the
hotspots is procedure step 3 and was not measured.

### Open legs of section D's procedure, not run here

Coverage on the hotspots (step 3) · duplication rate (step 4) · dependency cycles (step 5). Each is
a separate measurement; none is implied by the table above.

---

## What this arc did NOT do

No fix, trim, birth, disposition or ruling execution. No script committed, no workflow edited, no
dependency added (`radon` and `mutmut` were both ephemeral `uv run --with` installs; `uv.lock` and
`pyproject.toml` are untouched). No path added outside `docs/audits/`. `LANE_BRANCH_RE` was read,
never modified, and nothing was renamed.
