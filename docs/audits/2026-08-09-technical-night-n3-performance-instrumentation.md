# NIGHT LANE N3 — Why everything takes so long: measured bottlenecks and the instrumentation design

**Date:** 2026-08-09
**Lane:** N3 (night batch, cloud runtime)
**Branch:** `claude/new-session-mdmwu1`
**Mode:** execute — the contract was the plan
**Model:** opus, xhigh

---

## 0. Measurement environment — read this before believing any absolute number

Every number below carries one of three provenance tags. The discipline the contract asked for
is enforced literally: no claim without a number or an explicit `UNMEASURED` tag.

- **`[RECORD]`** — reproduced from the committed repo record (git, JOURNAL, audits). Portable.
- **`[HERE]`** — measured by me in this cloud container. **Not comparable in absolute terms to
  the operator's machine.**
- **`[UNMEASURED]`** — reasoning, not measurement.

**The container is materially different from the operator's machine, and this bounds section 1:**

| | Operator machine `[RECORD]` | This container `[HERE]` |
|---|---|---|
| Cores (`-n auto` resolves to this) | 16 | **4** |
| Python | 3.12 via `uv sync --locked` | 3.12.3 (venv) |
| `uv` | 0.11.19 (pinned) | **0.8.17 — pin unsatisfiable** |
| Suite result | `1 failed, 2716 passed` | `31 failed, 2680 passed` |

**`uv run --locked` cannot execute in this container at all.** `pyproject.toml` sets
`required-version = "==0.11.19"`; the installed `uv` is 0.8.17 and `uv self update 0.11.19`
returns *"version 0.11.19 was not found for the app uv in workspace uv"*. Every `uv` invocation
inside the project dir aborts before doing anything — including `uv venv`. I measured through a
hand-built 3.12 venv with the `dev` group installed by hand. **This is itself a finding: a clean
cloud clone cannot run this repo's declared gate environment**, which is the same class of
container-vs-local divergence the 2026-08-07 (m) and 2026-08-08 (a) JOURNAL entries already
recorded.

**The clone is SHALLOW** (`git rev-parse --is-shallow-repository` → `true`; 310 commits, boundary
`2b7274d0`, 2026-08-04). That single fact explains the gate posture here, and it reproduces —
independently — the diagnosis the 2026-08-08 (a) JOURNAL entry already made. `audit.py health`
exits **1 (DEGRADED)** in this container on exactly four legs, **all four container artifacts**:

- `repos registered (none)` — no fleet siblings exist in a single-repo clone.
- `canonical_freshness: 4 stale` (`VISION.md`, `ESSENTIALS.md`, `SESSION_SETUP.md`,
  `AI_COUNCIL_PROCESS.md`) — **the same four** the night container flagged on 2026-08-08, which
  the local re-run then cleared. JOURNAL entry (a) called them *"a stale-`main` artifact of the
  container, not inherited debt."* **That diagnosis is confirmed here by an independent
  reproduction.**
- `hooks_armed` — `.git/hooks/` holds only samples; pre-commit is not installed in this clone.
- `journal_spine_anchor` — `AnchorError: disposition floor 24882f8cc is not an ancestor of main
  … Not a valid object name`. `git cat-file -t 24882f8cc` fails: the floor **predates the shallow
  boundary**. Not an anchoring defect; an object the clone does not have.

**No commit gate fired on this report and none was bypassed** — the hooks are simply not armed
in this clone. **No `--no-verify` and no `SKIP=` was used anywhere in this lane.** I ran the two
gates that *are* meaningful here by hand instead: `validate_hermetization.py` (exit 0 — the
filename is Rule-A/Rule-B clean) and `gen_audit_index.py --check`, which was stale and which I
**regenerated with `--write`**, since adding a file to `docs/audits/` is exactly what that gate
guards.

The 31 failures here are container artifacts, not regressions — **verified, not assumed**: I
re-ran them in isolation (`-n 0`, single file) and they reproduce identically, so they are not
ordering effects. They decompose as: 20 × `tests/test_fleet_analytics.py` (`ModuleNotFoundError`
— the `analytics` group's `pandas` is deliberately not in `dev`), 5 × `test_reverse_dep_oracle`
+ 2 × `test_safe_remove`/`test_legibility_graph` (no language server present), and 4 audit/
boundary legs that read live fleet state absent from a single-repo clone. **UNAVAILABLE in this
clone** (gitignored, per the contract's instruction to mark them): `logs/FLEET-HEALTH.md`,
`logs/PARITY-EVENTS.jsonl`, `logs/COHERENCE-NUDGE.log`, `logs/OVERRIDES.md`,
`logs/PROPOSALS-*.md`. Only `logs/TOKEN-LOG.md` is committed.

**What survives the container difference:** file counts, corpus sizes, code structure, per-check
*relative* cost, git timestamps, and the worktree-amplification *ratio* (measured as a controlled
sweep where every arm ran under identical conditions). What does not: absolute suite wall-clock.

---

## 1. The finding that starts this lane — verified, and it is not what it says on the tin

### 1a. The claim, and what the record actually supports

The claim, stated three times in the record — `docs/audits/2026-08-08-technical-batch-3-packet.md:67`,
`JOURNAL.md:187`, and Amendment 2 of the consolidation report:

> *"Suite runtime fell 31m43s → 8m59s on the same repo, and the cause is the teardown: the
> morning baseline ran with 13 linked worktrees registered, this one with none. A ÷3.5 swing
> from worktree hygiene alone."*

**Both endpoints reproduce from the record `[RECORD]`:**

- `31m43s` — `docs/audits/2026-08-08-technical-batch-3-consolidation-report.md:422`:
  `1 failed, 2550 passed, 4 skipped in 1903.85s (0:31:43)`
- `8m59s` — `docs/audits/2026-08-08-technical-batch-3-packet.md:46`:
  `1 failed, 2716 passed, 3 skipped, 1 xfailed in 539.12s (0:08:59)`

**But the cited pair is confounded, and the record contains a cleaner one the claim does not use.**

The 31m43s run collected **2555** tests. The 8m59s run collected **2721** — 166 more, because ten
lanes merged in between. The comparison therefore changes *two* variables (worktree count **and**
test population), and attributing the whole swing to one of them is not supported by that pair.

The clean pair is already in the record and was not used. `JOURNAL.md:641-642`, entry
**2026-08-08 (a)**, that same morning, from the primary tree:

```
1 failed, 2550 passed, 4 skipped in 532.28s (8m52s)
```

**Identical composition to the 31m43s run — 2550 passed, 4 skipped, 1 failed, 2555 collected.**
Same repo, same day, same test set.

> **The defensible measurement is 532.28s → 1903.85s, a ×3.58 inflation at constant test
> population** — 22m51s of pure overhead. That is *stronger* evidence than the claim it replaces,
> because it holds the test set fixed. The reported ÷3.5 is right in magnitude and right in
> direction; it is right for a reason the report did not isolate.

A third figure exists and is inconsistent with the other two: the consolidation report's own
Amendment says *"Suite runtime dropped from 31m43s to **8m23s**"* (line 668) while quoting
`2 failed ... in 8m23s` at line 644 — that is the **pre-repin** run; `8m59s` is the **post-repin**
re-run. Two different runs, both real. The packet and JOURNAL quote 8m59s; the report's own prose
quotes 8m23s. Minor, but it is the kind of divergence that outlives the session that made it.

### 1b. The mechanism — proven in code, then measured

I tested the four candidate mechanisms the contract named. **Three are refuted with evidence.**

**Collection scope — REFUTED `[HERE]`.** Worktrees live in-repo at `.claude/worktrees/`
(`.gitignore:22`). Pytest defines no `norecursedirs`, `testpaths`, or `conftest.py` anywhere in
this repo — **verified: `find . -name conftest.py` returns nothing.** So pytest's *default*
`norecursedirs` applies, and its `.*` pattern excludes any dot-directory — including `.claude`.
Corroborated by the record itself: the 31m43s run collected 2555, exactly the count on a
worktree-free tree. **Pytest never collected a single test out of a worktree.**

**rootdir resolution — REFUTED `[HERE]`.** `rootdir` is pinned by `pyproject.toml` at the primary
checkout and does not move with worktree count.

**File watching — REFUTED `[HERE]`.** No watcher plugin is installed; `dev` declares
`pytest` + `pytest-xdist` only.

**Plugin/conftest discovery — REFUTED `[HERE]`.** No conftest.py exists to discover.

**The actual mechanism: five live tests walk the repo root with a skip-list that does not know
about `.claude`.** `tests/test_toc.py:262` and `tests/test_normalize_headers.py:222` each define:

```python
_SKIP_PARTS = {".venv", ".git", "node_modules", "__pycache__", ".pytest_cache"}
```

and then, at `tests/test_toc.py:323` and `tests/test_normalize_headers.py:225-226`:

```python
files = [p for p in sorted(root.rglob("*.md")) if not _SKIP_PARTS.intersection(p.parts)]
```

`rglob` does not honour `norecursedirs`, and `.claude` is not in `_SKIP_PARTS`. So each of these
tests walks, **reads, and CommonMark-parses** every markdown file in every registered worktree.
Five tests do this — one in `test_toc.py`, four in `test_normalize_headers.py`
(`_corpus()` is called at lines 246, 313, 356, 438).

The corpus is not small `[HERE]`: **1,633 markdown files, 20.8 MB**, of which `JOURNAL.md` alone
is **2.29 MB**. With 13 worktrees each holding a full checkout, that becomes ~22,900 files and
~291 MB — read and parsed, five times over.

**This is a known-solved problem in this very repo, and the fix is already written down.**
Three different exclusion conventions coexist:

| Site | Corpus source | Excludes worktrees? |
|---|---|---|
| `scripts/validate_reconciliation.py:64` | `rglob` + `_EXCLUDE_DIRS` incl. `".claude"` | **yes** — comment: *"nested CC worktree checkouts (full duplicate trees)"* |
| `scripts/enforcement_coverage.py:303,715` | `rglob` + `part == "worktrees"` | **yes** |
| `scripts/silent_rule_detector.py:151` | **`git ls-files -s -z`** | **yes, structurally** |
| `tests/test_toc.py`, `tests/test_normalize_headers.py` | `rglob` + `_SKIP_PARTS` | **NO** |

`validate_reconciliation.py`'s comment says its exclude set *"Mirrors the exclude sets in audit.py
/ verify_handoff_probes.py"*. The production scanners all know. **The two test files are the
outlier**, and they are the ones that cost 23 minutes.

`silent_rule_detector.py:151-161` states the canonical answer, already ruled in a **terra HIGH
re-review on 2026-07-27**:

> *"The corpus is defined by what git TRACKS, not by what the filesystem happens to walk …
> `Path.glob`/`rglob` inherits the host filesystem's case semantics … It also means an untracked
> scratch draft cannot inflate the metric."*

An in-repo standard exists, was ruled a fortnight before the incident, and two files predate it.

### 1c. Quantifying it — a controlled sweep

Absolute suite times here are not comparable to the operator's box, so I measured the **ratio**
under a controlled sweep in an isolated sandbox (a byte-copy of the tracked tree in scratchpad;
**the real repo was never given a worktree**). Each arm ran the same five tests, `-n 0`, with
*N* full-tree copies planted at `.claude/worktrees/lane-*`.

| Worktrees | md files | Corpus × | Wall `[HERE]` | vs N=0 | cost ÷ corpus |
|---|---|---|---|---|---|
| 0 | 1,633 | 1.00× | **71.80 s** | 1.00× | 1.000 |
| 3 | 6,532 | 4.00× | **289.84 s** | 4.04× | 1.009 |
| 6 | 11,431 | 7.00× | **527.92 s** | 7.35× | 1.050 |
| 13 | 22,862 | 14.00× | **1086.56 s** | **15.13×** | **1.081** |

**The cost is slightly superlinear in corpus size** — 15.13× wall at 14.00× corpus, an 8%
excess that grows monotonically across the arms. The likely cause is visible in the code: both
call sites wrap the walk in **`sorted(root.rglob(...))`**, so path sorting is O(n log n) on top of
the linear read-and-parse. **Added serial work at 13 worktrees: 1014.8 s (16m55s).** Nothing in
the code caps it.

**Reconciliation with the observed 22m51s `[RECORD]` — and this is where I have to correct my own
first reading.** It is tempting to book the whole ×3.58 against this mechanism. **The arithmetic
does not support that**, and saying so is the point of the discipline:

- The 5 corpus tests are **independent units** under `--dist load`. With 16 workers and 2,555
  tests, they land on different workers, so their contribution to *wall* clock is the **critical
  path** — the single slowest one — not the serial sum.
- At the measured 15.13× scaling, the slowest (`test_corpus_no_code_block_line_is_ever_modified`,
  base 22.89 s) grows to **≈346 s (5.8 min)**. Critical-path delta: **≈5m23s**.
- Observed delta: **22m51s**. **The tree walk explains ≈24% of it.**

> **The mechanism in §1b is real, proven in code, and measured — but on a 16-core machine it
> accounts for roughly a quarter of the observed slowdown. About 17 minutes remain unexplained by
> it.** My earlier framing ("the right order of magnitude") was too generous; the sweep is what
> corrected it.

**The named candidate for the remainder, which I can size only as "large" `[UNMEASURED]`.** The
consolidation report records **8 of the worktrees `locked` at ~20:45, and 1 by ~22:00** —
*"Lane sessions released their locks while this arc ran."* A locked worktree means a **live lane
session**. The 31m43s run was therefore executing `-n auto` (**16 workers**) on a 16-core box
**while up to 8 other Claude sessions were active**, several plausibly running their own gates and
their own 16-worker suites. That is severe CPU oversubscription, and it inflates *every* test, not
five of them.

**The two causes are confounded and multiplicative, not additive** — contention stretches the
already-inflated corpus tests too. In this data the same 13 worktrees are simultaneously the extra
files **and** the proxy for concurrent sessions, and **no experiment in the record separates
them.**

**This changes the remedy, which is why it matters.** "Worktree hygiene" is at best a quarter of
the answer. The larger lever is almost certainly *"do not run the integration suite while lane
sessions are live"* — and unlike the code fix, that one is free. Both should be taken; only one
of them has a measured saving.

### 1d. Suite runtime anatomy — where the ~9 minutes go

Full suite `[HERE]`, `-n auto` on 4 cores: **`31 failed, 2680 passed, 9 skipped, 1 xfailed in
462.81s (0:07:42)`**, 2,721 collected.

**Collection is not the problem.** `pytest -n 0 --collect-only -q` → **2721 tests collected in
4.97s** — **1.1%** of the run. Under `-n auto` collection is paid *per worker*, so on the
operator's 16 workers it is ~16 × 5 s ≈ 80 s of CPU, but overlapped; still not the sink.

**`-n auto` resolves to `os.cpu_count()`** — 16 on the operator's box `[RECORD]`
(the consolidation report says so at line 458), 4 here `[HERE]`. Distribution mode is xdist's
default `--dist load` (no `--dist` in `addopts`): tests are handed to workers one at a time.

**The suite is wait-bound, not CPU-bound — and this is the headline of this section.** The shell
`time` for the full run reports **`user 4m3.8s` + `sys 0m25.9s` = 269.7 s of CPU against 462.8 s
of wall on 4 cores.** That is **14.6% CPU utilisation** — average parallelism 0.58 of a single
core. The workers are overwhelmingly *blocked*, not computing.

Two named, measured causes account for much of it `[HERE]`:

- **Language-server timeouts: ~83 s.** `scripts/reverse_dep_oracle.py:65` sets
  `DEFAULT_WARM_TIMEOUT = 20.0`. Four tests sit on it almost exactly —
  `test_safe_remove.py::test_real_oracle_allows_orphan_removal` 20.90 s,
  `test_reverse_dep_oracle.py::test_run_oracle_fail_soft_when_no_langserver` 20.89 s,
  `test_legibility_graph_conformance.py::test_graph_oracles_registered_and_operational` 20.81 s,
  `…::test_cell_code_code_fires` 20.60 s. That is **pure sleep** when no language server is
  present. Running `tests/test_reverse_dep_oracle.py` alone takes **127.99 s** for 21 tests, ~100 s
  of it timeout.
- **The five corpus walkers: 77.95 s** (§1b), the top two being the two slowest tests in the suite.

Together these are **161 s of measured test-body time against a 462.8 s wall — two identifiable,
fixable causes.** Note the framing: that is 35% of the wall *expressed as serial test time*, not a
35% wall saving. Under `-n auto` both classes already overlap other work, so removing them shortens
the critical path by ~23 s + ~21 s, not by 161 s (§6).

The remaining tail is subprocess spawn latency — `git`, `pre-commit`, real-repo fixtures. **27 test
files use `spec_from_file_location` and there are 79 `sys.path` mutations across the test suite**;
each module load re-executes a 5,072-line `audit.py` and friends.

**The instrument defect the contract names, and where it invalidates timing.** Because tests load
modules via `spec_from_file_location` and mutate a **shared worker's** `sys.path`, import success
is order-dependent, and the parallel aggregate undercounts import breakage: a module that only
imports because an earlier test on the *same worker* fixed the path reads as healthy. **Its
timing consequence is the part usually missed:** `--durations` attributes the *entire* cost of a
first import to whichever test happened to trigger it on that worker. So per-test durations are
**worker-history-dependent**, and a test's rank can move between runs without its own work
changing. Concretely, this invalidates:

- Any conclusion of the form *"test X is slow"* for a test whose cost is dominated by a **first
  import** rather than its own body.
- Any cross-run comparison of the durations table at fixed `-n`, since assignment differs.

It does **not** invalidate the two conclusions I lean on above: the corpus walkers (~20 s of
measured file I/O and CommonMark parsing each) and the langserver timeouts (a wall-clock deadline)
are dominated by their own bodies, not by import. **`-n 0` is the only trustworthy instrument for
per-test attribution**, and every per-test number I quote as load-bearing was taken there or is
body-dominated.

---

## 2. Gate mesh cost — the 41 checks are not the bottleneck, and this is the section's finding

I instrumented every member of `ALL_CHECKS` (`scripts/audit.py:4177`) individually against the
live repo `[HERE]`. **Count confirmed: exactly 41.**

> **The entire gate mesh costs 11.66 seconds.**

Against a ~9-minute suite and a ~2-hour integration, **the gate mesh is ~0.2% of an integration
arc.** The contract's suspicion that 41 checks are a cost centre is **refuted by measurement**.
No cheap win lives here, and effort spent optimising it is misdirected.

The distribution is extremely skewed — **three checks are 83.5% of the total**:

```
seconds    pct   check
  6.598  56.6%   check_doc_code_edge
  1.807  15.5%   check_doc_claims
  1.334  11.4%   check_doc_structure
  0.341   2.9%   check_handoff_probes
  0.325   2.8%   check_review_artifact_coverage
  0.296   2.5%   check_undeclared_edges
  0.232   2.0%   check_fleet_parity
  0.157   1.3%   check_reconciled_versions
  0.143   1.2%   check_membership_agreement
  ... 32 further checks, each < 0.08s, together 0.43s (3.7%)
 11.663 100.0%   TOTAL (41 checks)
```

**Always-run:** all 41. There are **no subset constants** — no `HEALTH_CHECKS`,
`SHIP_GATE_CHECKS` or `DEFAULT_CHECKS` exist. All five CLI entry points (`run` 4712, `repo` 4799,
`health` 4856, `ship-gate` 4964, `checks` 5051) iterate the same list. The only tiering is a
`_GATE_MODE` flag that `cmd_health` sets to skip the expensive pytest subprocess in
`validate_doc_claims` (`scripts/validate_doc_claims.py:23` — *"EXPENSIVE (subprocess) → evaluated
only when run_expensive=True"*). **That is the one place a subset already exists in spirit, and
it is the right design; nothing else needs it, because nothing else is expensive.**

**I/O-bound:** `check_doc_code_edge` (two full `scripts/*.py` walks + `tokenize`),
`check_doc_claims` (spawns pytest under ship-gate), `check_doc_structure` (reads the doc corpus).

**Redundant traversals — one real, and it is small.** `scripts/validate_doc_code_edge.py` walks
`code_root.rglob("*.py")` **twice** — once in `find_code_sites` (line 161) and once in
`iter_code_rule_ids` (line 189) — each time re-reading and re-`tokenize`-ing every file in
`scripts/`. Merging them into a single pass that yields both the ID set and the site list would
save roughly half of 6.6 s ≈ **3 s per gate run**. Real, correct, and **worth ~3 seconds** — which
is precisely why it should not be prioritised.

**Superlinear in repo size:** **none found.** Every check is linear or better in file count. The
per-check `iterdir()` calls (lines 642, 671, 694, 790, 1012, 2085, 3805) are single-level and
cheap. `check_doc_code_edge` is O(rules × files) in principle, but the rule set is registry-scoped
by `ecosystem/doc-code-edge.yaml`'s `declaration_docs:` list — the #194 doc-site-scoping fix
already bounded it.

**Worktree amplification does not reach the gate mesh**, and this is by construction rather than
luck: `check_doc_code_edge` passes an explicit include-list for docs and `repo_path / "scripts"`
as `code_root` (`scripts/audit.py:2321-2325`), so neither side can wander into `.claude/`. The
gate mesh is *already* built to the standard the two test files miss.

---

## 3. The 2h12m integration — phase breakdown from its own commits

The `2h12m` figure `[RECORD]` is `JOURNAL.md:30`: *"batch 3 dispatched with no manifest and cost a
2h12m integrator run that reached the precondition gate and correctly STOPPED before merge #1."*

Reconstructed from the first-parent spine `[RECORD]` (`git log --first-parent`, timestamps +0200):

**Attempt 1 — the STOP (~2h12m).**

| Time | Commit | Event |
|---|---|---|
| 19:02:57 | `ae339ac` | prior arc closes; integrator inherits |
| — | — | inventory, second-seat review of 10 lanes, **one full suite: 31m43s** |
| 21:28:58 | `3a9120e` | consolidation report merged — STOPPED at the precondition gate |
| 21:39:28 | `5ba0070` | Amendment 1 (the worktree-count correction) |

**Of the ~2h12m, 31m43s — 24% — was one suite run**, and it produced no merge. The arc's own
report (line 458) drew the right conclusion at the time: at `/lane-integrate`'s mandated
suite-after-every-merge, *"10 lanes … is roughly 5.3 hours of suite time alone."*

**Attempt 2 — the successful drain (1h27m44s).**

| Time | Commit | Event | Δ |
|---|---|---|---|
| 22:16:11 | `121499d` | manifest lands; exemption armed | — |
| 22:19:24 | `d608b6f` | merge 1 — intakes | 3m13s |
| 22:24:38 | `764f06c` | merge 2 — lane E | 5m14s |
| 22:33:17 | `2928cf1` | merge 3 — lane 290 | 8m39s |
| 22:36:45 | `946d904` | merge 4 — lane 280/315 | 3m28s |
| 22:39:41 | `15cc3ec` | merge 5 — groom sheet | 2m56s |
| 22:42:02 | `08aea7a` | merge 6 — lane C | 2m21s |
| 22:44:26 | `2732f16` | merge 7 — archival audit | 2m24s |
| 22:47:19 | `e3821ae` | merge 8 — pythonpath | 2m53s |
| 22:49:55 | `1a4b11b` | merge 9 — seeded-defect | 2m36s |
| 22:52:26 | `87b993a` | merge 10 — closure wave | 2m31s |
| 23:00:27 | `f98d126` | eight row closes | 8m01s |
| 23:20:06 | `679ccbc` | test repin (merge-caused failure) | 19m39s |
| 23:43:55 | `bedcf3f` | batch 3 closes | 23m49s |

**Phase split of attempt 2:**

| Phase | Wall | Share |
|---|---|---|
| Merge queue (10 merges, incl. every generated-file conflict) | **33m02s** | 38% |
| Close-out: suite + row closes + diagnosis + repin + packet | **51m29s** | 59% |
| Manifest precondition | 3m13s | 4% |
| **Total** | **1h27m44s** | |

**Total batch-3 integration cost: ~3h40m across both attempts** — of which **~2h12m produced
nothing mergeable**, spent on a precondition (a missing manifest) that a one-line artifact at
dispatch would have satisfied. That bill is exactly what `ee4fd140` pays forward.

**Conflict resolution on generated files was not the sink.** Ten merges in 33m02s is **3m18s
average**, and that interval contains *all* of it — the JOURNAL records *"nine index collisions
plus the doc-counts one"*, **every one resolved by regeneration, never by hand**. The 8m39s
outlier (merge 3) is the largest single conflict cost visible, and it is 6 minutes above the
median. **Regeneration-by-default is already the practice, and it is already cheap.**

### What the same work would cost under the three counterfactuals

**(a) One suite on the merged result only — ALREADY DONE, and it is what made attempt 2 viable.**
Attempt 2 ran **one** suite (8m59s), not ten. Under `/lane-integrate` §2 as literally written —
a full suite after every merge — the same queue would have cost **10 × 8m59s ≈ 1h30m** of suite
time post-teardown, or **10 × 31m43s ≈ 5h17m** pre-teardown `[RECORD, arithmetic]`. **Measured
saving of the batched-suite ruling: ~1h21m at teardown-clean rates.** The ruling is already
banked; the residual action is to reconcile `/lane-integrate` §2's text with what the integrator
actually and correctly did.

**(b) Generated files resolved by regeneration by default — ALREADY THE PRACTICE, saving ~0.**
The measured saving is not in the resolution but in the *correctness*: the JOURNAL records that
**both doc-counts sides were wrong** (lane E carried 2555→2570, lane 280/315 carried 2555→2582;
merged truth 2721). Hand-picking either side would have committed a number nobody counted. **The
win here is a correctness win, not a time win — do not book it as a saving.**

**(c) Fewer standing worktrees.** Attempt 1 ran exactly one suite, so the *observed* saving from
running teardown-clean is **22m44s** (31m43s − 8m59s), or **22m51s** on §1a's cleaner
constant-composition pair — **17% of the 2h12m**. Had attempt 1 also drained the queue under a
per-merge-suite rule, the saving would have been the ~3h47m difference between the two arithmetic
figures above.

**But that 22m51s must not be booked against the code fix.** Per §1c, the tree-walk mechanism
accounts for ≈5m23s of it; the rest is most plausibly contention from the up-to-8 live lane
sessions, which teardown also removes. **Teardown-before-suite buys ~23 min, measured. The §6 code
fix buys ~5m23s of that, measured. The two are not the same lever and the difference is not
rhetorical** — the code fix is permanent and unconditional; the teardown effect is only available
to an integrator willing to wait for the lanes to finish.

---

## 4. Session-time anatomy across the day

Arc boundaries taken as first-parent merge-to-merge intervals `[RECORD]` for 2026-08-08:

| Span | Arc | Duration |
|---|---|---|
| 12:07:53 → 12:22:07 | night-branch merge → ledger truth | 14m14s |
| 12:22:07 → 13:32:45 | intake #27 ledger truth | 1h10m38s |
| 13:32:45 → 15:01:24 | architect bundle cut | 1h28m39s |
| 15:01:24 → 19:02:57 | PHASE-0 → dispatch-surface (lanes running in parallel) | 4h01m33s |
| 19:02:57 → 21:28:58 | **batch-3 attempt 1 (STOP)** | 2h26m01s |
| 21:39:28 → 22:16:11 | re-dispatch preparation | 36m43s |
| 22:16:11 → 22:52:26 | **merge queue** | 36m15s |
| 22:52:26 → 23:43:55 | **close-out** | 51m29s |
| 23:43:55 → 00:00:46 | review artifact | 16m51s |
| 00:00:46 → 00:13:30 | review artifact conformed | 12m44s |
| 00:13:30 → 00:46:12 | night-batch manifest | 32m42s |

**I could not verify the contract's "2h43m" figure.** `grep` for `2h43`, `2h 43`, `2:43` and
`163 min` across every tracked `.md` returns **nothing**. The nearest arc-shaped intervals are
19:02:57→21:39:28 = **2h36m31s** (attempt 1 including its amendment) and the 4h01m33s PHASE-0 span.
Per the contract's own discipline: **a reported figure I could not verify is a finding, not a
fact.** The `~9 minutes` low end is likewise unlocated as a stated figure, though 12m44s
(the review-artifact conformance arc) is the shortest arc I can measure.

### The three largest sinks, with evidence

**Sink 1 — Precondition failures discovered late: ~2h12m in one day `[RECORD]`.** Attempt 1 ran
inventory, ten second-seat reviews and a 31m43s suite before reaching a gate it could not pass,
and correctly stopped **before merge #1**. The precondition (a committed batch manifest) is
machine-checkable at dispatch and costs one file. The record shows this is a *class*, not an
instance — `JOURNAL.md:22-46` names **three occurrences in two days** of "a surface authored from
prose intent rather than from its parser": the `batch:` field that granted a working exemption
while failing its well-formedness pin (08-08 h), the review artifact that recorded a real review
and satisfied no coverage leg (08-08 l), and the manifest filename that `MANIFEST_GLOB` would not
have matched (08-09 a). **The third cost nothing, because it was checked against the parser
before the artifact existed.** That is the whole lesson, already learned, and it is the cheapest
end of the largest sink.

**Sink 2 — Suite runs at inflated cost: 31m43s in a single arc, ~23m of it avoidable `[RECORD]`.**
§1 and §3(c).

**Sink 3 — Review loops: 1h44m40s in one lane `[RECORD]`.** Below.

### The 15-pass reviewer loop — did its marginal value justify its cost?

Source: `docs/audits/2026-08-08-codex-lane-290-floor-teeth.md`. I priced it from its own pass
HEADs `[RECORD]`:

| Pass | HEAD | Time | Δ | C | H |
|---|---|---|---|---|---|
| 1 | `5abc96a9` | 18:28:09 | — | 1 | 1 |
| 2 | `6a0b53b1` | 18:56:14 | 28m05s | 2 | 1 |
| 3 | `0be4df56` | 19:11:55 | 15m41s | 1 | 3 |
| 4 | `bd818c09` | 19:17:55 | 6m00s | 1 | 0 |
| 5 | `d6f3fdb3` | 19:24:45 | 6m50s | 0 | 1 |
| 6 | `3c3ac7df` | 19:29:48 | 5m03s | 2 | 0 |
| 7 | `e09d5606` | 19:39:39 | 9m51s | 0 | 1 |
| 8 | `1c481df6` | 19:43:37 | 3m58s | 0 | 1 |
| 9 | `836f6f42` | 19:51:10 | 7m33s | 0 | 3 |
| 10 | `523f0c86` | 19:56:39 | 5m29s | 0 | 2 |
| 11 | `349433a4` | 20:00:04 | 3m25s | 0 | 1 |
| 12 | `70f2ec53` | 20:03:06 | 3m02s | 0 | 1 |
| 13 | `9b9800b1` | 20:06:48 | 3m42s | 0 | 1 |
| 14 | `8969ba2f` | 20:12:49 | 6m01s | 0 | 1 |
| 15 | (clean) | — | — | 0 | 0 |

**Loop cost: 1h44m40s** from first fix to last (18:28:09 → 20:12:49); **1h59m22s** to the lane tip
`b6d81501` at 20:27:31. **Yield: 7 Critical + 17 High = 24 findings; 21 accepted and fixed, 3
refuted.**

**Assessment — the loop was worth running, and it was the wrong shape.**

The value did not decay to zero: **every pass through 14 found at least one accepted defect**, and
the artifact's stopping condition was stated rather than assumed (pass 15 clean *and* the reviewer
agreeing the residue was category (b)). A loop that finds a real defect on its fourteenth pass is
not a loop that ran too long. Three findings were refuted with reasons, and the reviewer
*withdrew* one of its own (D9) — the loop was adversarial in both directions, which is what makes
its output trustworthy.

But the severity profile is the tell. **All 7 Criticals landed by pass 6 (19:29:48).** Passes 7–14
cost **43m01s — 41% of the loop — and returned 11 High and zero Critical.** And the artifact says
every accepted finding across all 14 passes *"was one shape — a command that pre-commit or the
shell would reject, or never reach, read as fully armed."* **Twenty-one instances of one defect
class, found one at a time, at ~5 minutes each.**

The loop's own record names the fix: at **pass 9** *"the hand-rolled flag walk [was] replaced by
argparse itself."* That is the library-first move, taken 8 passes and ~1h23m in. It did not end
the loop — passes 10–14 found 6 more High — but those had migrated to the *shell-lexing* layer
(`exec` prefixes, POSIX continuations, dangling redirections, `env -u`, `env -0`), which is
`shlex`'s problem and was being hand-rolled too. **Hand-rolled parsing of a command line was the
cost driver, and the loop was the instrument that discovered, expensively and incrementally, that
it should not have been hand-rolled.**

**Verdict: the loop's marginal value justified its cost given the code it was reviewing; the code
should not have needed it.** The generalisable rule is not "cap the loop" — capping at pass 6
would have shipped 11 real defects. It is: **when three consecutive passes return findings of the
same shape, stop fixing instances and replace the mechanism.** That trigger would have fired at
pass 3 (~19:11) and plausibly saved most of the following hour. This is the same library-first
discipline §5 is required to apply to itself, and it is why §5's design proposes writing almost
no new code.

---

## 5. The instrumentation design (the deliverable that outlives tonight)

**Requirement, verbatim** (`docs/intake/2026-08-08-func-multi-model-execution-and-distillation.md:25`):

> *"(a) instrumentation before machinery — per-arc phase/time/token logging via hooks (session
> duration, per-phase wall-clock, model mix), two windows of data"*

Acceptance (line 37): *"S3a producing per-arc breakdowns in packets."*

### 5.0 Library-first — what already exists (mandatory, and it changes the design)

I checked before proposing. **Four of the five things S3a asks for are already captured; almost
nothing needs to be built.**

| Need | Existing mechanism | Status |
|---|---|---|
| Session duration, per-message timestamps | **Claude Code transcript JSONL** — every hook payload carries `transcript_path`; each line has an ISO timestamp | **already recorded, unharvested** |
| Per-message model + token usage | Same JSONL: `message.model`, `message.usage.{input_tokens, output_tokens, cache_read_input_tokens, cache_creation_input_tokens}` | **already recorded, unharvested** |
| Lane / branch attribution | Same JSONL: **`gitBranch` on every record** | **already recorded, unharvested** |
| Sub-agent cost split (the S2 acceptance criterion) | Same tree: **`…/<session>/subagents/agent-*.jsonl`**, one file per sub-agent; `isSidechain` on the parent records | **already recorded, unharvested** |
| Token/cost aggregation | **`ccusage --json`** — already the tool behind `logs/TOKEN-LOG.md` (every entry says *"via ccusage --json"*) | **already in use, weekly** |
| Phase boundaries | **git first-parent spine** — this entire report's §3 and §4 were reconstructed from it, with no instrumentation at all | **already sufficient for coarse phases** |
| Metrics reporter with an honest-gap discipline | **`scripts/window_metrics.py`** (191 LOC, [#461]) — computes 4 of 6 metrics, prints `NOT COMPUTED` with a reason for the other 2 | **the pattern to extend, not replace** |
| Event-stream artifact format | **`logs/PARITY-EVENTS.jsonl`** — an existing gitignored JSONL append stream | **the precedent to follow** |
| Suite phase timing | `pytest --durations` (stdlib to the runner) | **already available** |
| Per-check timing | `ALL_CHECKS` is an introspectable list; §2 timed it in 30 lines of throwaway script | **available, no organ needed** |

**This is verified, not recalled.** I parsed this lane's own live transcript
(`~/.claude/projects/-home-user-dev-knowledge/<session>.jsonl`, 352 records at the time of
reading) and confirmed every field the design below depends on:

```
record types   : assistant 198 · user 94 · attachment 26 · last-prompt 24 · queue-operation 10
top-level keys : timestamp · sessionId · cwd · gitBranch · type · uuid · parentUuid
                 message · toolUseResult · version · permissionMode · effort · isSidechain …
usage keys     : input_tokens · output_tokens · cache_read_input_tokens
                 cache_creation_input_tokens · service_tier · server_tool_use …
models seen    : claude-opus-5 (198)
timestamps     : 2026-08-08T22:53:38.281Z … 2026-08-08T23:25:09.769Z  (ISO-8601, ms, UTC)
```

Three fields are better than the requirement asked for: **`gitBranch`** gives per-record lane
attribution for free (no correlation step); **`effort`** records the reasoning tier; and the
**`subagents/agent-*.jsonl`** side-files make the fan-out split directly measurable — which is
S2's acceptance criterion (*"its packet reports the split"*) satisfied by the same reader, at no
extra cost.

**The consequence is the design.** S3a says *"via hooks"*, and the temptation is a `PreToolUse`/
`PostToolUse` pair timing every tool call. **That would be the hand-rolled flag walk of §4.**
Claude Code already writes a complete, timestamped, per-message, per-model, token-attributed
event log for every session. The correct instrumentation is a **reader**, not a **recorder**.

Anti-goal, stated plainly: **do not add a `PostToolUse` hook.** It fires on every tool call, is on
the latency path of the operator's session, and would re-record data that already exists on disk.

### 5.1 What fires

**One hook: `SessionEnd`.** Not `Stop` — `Stop` fires at every turn boundary and the ADR-85
amendment of 2026-08-03 already established what happens to organs mounted there
(*"an organ that can be exhausted cannot carry teeth"*, nine identical firings, silent
auto-bypass). Session-level accounting belongs at the session boundary, exactly once.

```
SessionEnd → uv run --locked python scripts/arc_metrics.py --record
```

**Posture: fail-soft, never blocking, timeout 15s.** It writes an artifact; it gates nothing. A
measurement organ that can block a session will be bypassed and then distrusted — the same
failure the `/override` retirement recorded.

**Its whole job is to read `transcript_path` from the hook payload and reduce it.** It does not
observe the session; it post-processes a file the runtime already wrote.

### 5.2 What is recorded

One JSONL line per session, appended to **`logs/ARC-METRICS.jsonl`** — conforming to the §9
naming rule (UPPERCASE-KEBAB stem; `.jsonl` because it is an event stream) and to the
`PARITY-EVENTS.jsonl` precedent. **Gitignored**, like every other `logs/` stream except
`TOKEN-LOG.md`.

```json
{
  "schema": 1,
  "session_id": "…",
  "started": "2026-08-08T19:02:57+02:00",
  "ended":   "2026-08-08T21:28:58+02:00",
  "wall_s": 8761,
  "repo": ".dev-knowledge",
  "branch": "worktree-lane-290-floor-teeth",
  "head_at_end": "b6d81501",
  "spine_commits": ["3a9120e"],
  "models": {"claude-opus-5": {"msgs": 412, "out_tokens": 1043221},
             "claude-haiku-4-5": {"msgs": 38, "out_tokens": 21044}},
  "subagents": [{"id": "agent-ad134a…", "model": "claude-haiku-4-5",
                 "out_tokens": 11402, "wall_s": 69}],
  "tokens": {"in": 91233, "out": 1064265,
             "cache_read": 8812004, "cache_creation": 402118},
  "phases": [
    {"name": "retrieval",    "wall_s": 1102, "basis": "read-tool spans"},
    {"name": "build",        "wall_s": 3980, "basis": "edit/write spans"},
    {"name": "verification", "wall_s": 2314, "basis": "pytest/audit spans"},
    {"name": "review",       "wall_s": 1201, "basis": "codex spans"},
    {"name": "waiting",      "wall_s":  164, "basis": "residual"}
  ],
  "suite_runs": [{"wall_s": 1903.85, "collected": 2555, "failed": 1}],
  "not_computed": {"operator_idle": "indistinguishable from model latency in the transcript"}
}
```

**Phase derivation, and its honest limit.** Phases are classified from the **tool-call sequence
already in the transcript** — a span is `verification` if bounded by a `Bash` call matching
`pytest|audit\.py|ruff`, `build` by `Edit|Write`, `retrieval` by `Read|Grep|Glob`, `review` by
`codex`. Residual time is `waiting`. **This is a heuristic and the field must say so** — the
`basis` key exists to make every number's derivation visible, and `not_computed` carries the
`window_metrics.py` discipline forward: **operator think-time is not separable from model latency
in the transcript, so it is reported as a named gap rather than as a number.** A metric nobody
computes is a claim; a metric computed from an unstated heuristic is worse.

### 5.3 Where it lands, and how it aggregates

- **Per session:** one line appended to `logs/ARC-METRICS.jsonl` (gitignored, ephemeral).
- **Per batch:** `scripts/arc_metrics.py --batch <n>` emits **one line for the packet**, which is
  the acceptance criterion (*"producing per-arc breakdowns in packets"*):

```
arc-metrics batch 3: 12 arcs · wall 9h41m · retrieval 18% · build 34% · verification 29%
  · review 11% · waiting 8% · out-tokens 4.21M (opus 94% / haiku 6%) · suite runs 3 (61m04s)
  · NOT COMPUTED: operator idle
```

Flat, `key: value`, fenced — per the §4 output-formatting rule, so the operator can copy it into
browser chat without the TUI painting box-drawing glyphs into it.

- **Per window:** extend `scripts/window_metrics.py` rather than adding a seventh reporter. It
  already owns "the operator window metrics, computed instead of claimed", already renders a
  labelled table, and already prints `NOT COMPUTED` with reasons. **Adding arc-time as metrics 7–9
  there is a ~40-line change; a new reporter is a new surface to keep coherent.**

**Reconciliation with `logs/TOKEN-LOG.md`:** it stays. It is the *weekly, cross-repo, cost*
record from `ccusage`; this is the *per-arc, in-repo, phase* record. They should agree on token
totals, and disagreement is itself a signal — worth a `--reconcile` mode that diffs the two, in a
later leg, not this one.

### 5.4 What the first two windows would let us decide

The intake is explicit that (b) and (c) may not be scoped before (a) has data. Named in advance,
so the data cannot be retrofitted to a conclusion:

1. **Is the distillation engine worth building at all?** Decide by: `retrieval` share of arc wall.
   Tonight's single-arc reconstruction suggests context assembly is *not* the dominant phase —
   verification and review are. **If two windows confirm `retrieval` < 20%, S3b/S3c should be
   descoped**, and this report's §6 list is the better use of the same effort. That is a
   falsifiable prediction, recorded now.
2. **Which of the three candidate engine shapes?** `contract-payload distiller` wins only if
   `retrieval` is front-loaded; `packet condenser` only if `build` tail-heavy; `gate-context
   slimmer` only if `verification` dominates.
3. **Is the model mix right?** `out_tokens` by model against phase. The session-level opus-default
   is explicitly out of scope for change, but the *within-session* S1/S2 routing is exactly what
   this measures.
4. **Is the review loop shape a systemic cost or a lane-290 outlier?** One arc is an anecdote
   (§4). Two windows of `review` share answers it — and the §4 "three passes, same shape → replace
   the mechanism" trigger becomes checkable rather than advisory.

### 5.5 Cost of the design

One new script (~120 LOC), one `SessionEnd` hook line, one `.gitignore` entry, a ~40-line
extension to `window_metrics.py`, tests. **No new dependency:** the transcript is JSONL and `json`
is stdlib; `ccusage` is already an established external tool used by `TOKEN-LOG.md` and is not
required by this path.

---

## 6. Cheap wins — ranked by measured saving ÷ effort

Ranked by measured saving per unit effort. **Every unmeasured item is tagged as such and ranked
below every measured one.**

| # | Win | Measured saving | Effort | Basis |
|---|---|---|---|---|
| **0** | **Do not run the integration suite while lane worktrees are locked** (i.e. teardown, or wait, before the suite) | **~23 min per suite run** observed; **~17 min of it is the un-isolated contention share** | **zero code** — a sequencing rule | §1a pair; §1c reconciliation |
| **1** | **Add `.claude`/`worktrees` to `_SKIP_PARTS` in `tests/test_toc.py:262` and `tests/test_normalize_headers.py:222`** | **≈5m23s critical-path per suite run whenever worktrees are registered** | **2 lines** | §1c sweep: 15.13× at 14× corpus |
| **2** | Better version of #1: switch both corpora to `git ls-files`, per the 2026-07-27 terra ruling already implemented at `scripts/silent_rule_detector.py:151` | same, plus **3.9× faster enumeration** (58.4 ms → 15.1 ms), platform-stable, and O(1) in worktree count | ~15 lines | `[HERE]` benchmark: **identical 1633-file set, set-difference 0** |
| **3** | Skip or mark the 4 language-server tests when no server is present, instead of burning `DEFAULT_WARM_TIMEOUT` | **~83 s per suite run** (4 × ~20.8 s) | small — the `slow` marker tier already exists | `[HERE]` durations; `scripts/reverse_dep_oracle.py:65` |
| **4** | Reconcile `/lane-integrate` §2 with practice: one suite on the merged result, not one per merge | **~1h21m per 10-lane batch** | doc change + ruling | §3(a) arithmetic on measured 8m59s |
| **5** | Single-pass `scripts/*.py` walk in `validate_doc_code_edge` (merge lines 161 and 189) | **~3 s per gate run** | ~20 lines | §2 per-check timing |
| **6** | Mechanise the worktree prune — see below | **UNMEASURED**, but bounds #1's exposure | — | §6a |

**Items 1 and 2 are the same fix at two quality levels. Item 2 is the one to take** — it is the
standard this repo already ruled, it is faster, and it cannot rot the way a hand-maintained skip
list does. Neither changes behaviour: the file set is provably identical on the current tree.

**How #0 and #1/#2 relate — they partly overlap, and the residual is the point.** Teardown (#0)
removes *both* causes at once, so on an arc that can wait for its lanes, #1/#2 adds nothing. Its
value is precisely the case where teardown is **not** available: a mid-batch suite run, a lane
session running its own gate inside a live batch, a `/ship` pre-flight with sibling lanes open.
**#0 is the bigger number; #1/#2 is the one that still works when #0 cannot be applied** — which,
per `check_stale_worktrees`'s own "MID-BATCH IS A PASS" docstring, is the normal condition during
exactly the batches that hurt.

**Combined measured effect, stated carefully.** In a **worktree-free** tree `[HERE]`, causes #1
and #3 account for **161 s of measured test-body time** — 77.95 s of corpus walking plus 83.2 s of
language-server timeout — against a 462.8 s wall. That is **35% of the wall as serial test time**;
the *wall* saving from removing them is smaller than 161 s, because under `-n auto` these tests
already run concurrently with others. **The honest floor is the critical-path saving: ~21 s (the
slowest langserver timeout) plus ~23 s (the slowest corpus test) if both classes vanish.** The
large numbers only appear once worktrees are registered, and even then §1c caps the tree-walk
share at ≈5m23s. **No line of this table should be read as "the suite gets 35% faster."**

### 6a. Worktree hygiene as a standing organ — is the weekly prune mechanised?

**No. `check_stale_worktrees` (`scripts/audit.py:1213`) is a detector, not a prune, and by its own
design it cannot fire on the condition that cost 23 minutes.**

- **Posture: WARN only**, by ruling — ADR-110 §3 arms no gate, and [#505] scopes it to WARN-tier.
- **Horizon: `_STALE_WORKTREE_HORIZON_DAYS = 7`** (`scripts/audit.py:1034`), strictly — *"reaching
  the horizon is still live."*
- **Its docstring rules the batch-3 condition a PASS, deliberately:** *"MID-BATCH IS A PASS,
  deliberately: during a running batch every lane worktree is registered and recently committed.
  An organ that fired then would alarm through the whole run it exists to close."*

**That reasoning is correct and I am not proposing to change it.** The point is narrower and it is
the finding: **the organ that exists cannot see the cost, because the cost is not staleness.**
Thirteen *fresh, legitimate, mid-batch* worktrees inflated the suite ×3.58. The prune is doctrine
(`scripts/audit.py:1031` — *"mechanized weekly prune stays"*) but I found **no scheduled task that
runs it**: `scripts/setup-fleet-scheduler.ps1` contains no worktree reference, and `config/`
holds only `requirements-dev.txt`.

**The right remedy is #2 plus #0, not a prune.** Make the suite's cost **invariant to worktree
count** (#2), and separately stop running it under 8-way session contention (#0). Between them the
hygiene question stops being a performance question at all — it reverts to being purely about
unclosed work, which is what `check_stale_worktrees` is actually for and is already good at.

### 6b. Explicitly UNMEASURED — my ideas, honestly labelled

Ranked below everything above, because I did not measure any of them:

- **`-n auto` may be the wrong sizing.** `[UNMEASURED]` The suite ran at **14.6% CPU utilisation**
  `[HERE]` — that part is measured. The *inference* that `-n` should therefore exceed
  `os.cpu_count()` for wait-bound work is not: I did not run the `-n 4` vs `-n 8` vs `-n 16`
  comparison on a fixed tree, and the 2026-08-06 adoption measurement (serial 1785.61s → `-n auto`
  330–359s, ~5.2×) is the only sizing evidence in the record. **This is the single highest-value
  measurement not taken tonight**, it costs two suite runs, and it should be taken before anyone
  changes `addopts`.
- **Subprocess spawn cost across the suite.** `[UNMEASURED]` Many tests spawn real `git` and
  `pre-commit`. A session-scoped fixture could amortise repo setup. I did not measure how much of
  the wait-bound residual this is.
- **Per-worker collection.** `[UNMEASURED]` Collection is 4.97 s per process; at `-n 16` that is
  ~80 s of CPU. Whether it is on the critical path, I did not measure.
- **`check_doc_claims`'s pytest subprocess under ship-gate.** `[UNMEASURED]` `_GATE_MODE` already
  skips it for `health`; I measured the check at 1.807 s with the subprocess *not* taken, so the
  ship-gate figure is higher by roughly a `--collect-only` (~5 s `[HERE]`). Not independently timed.

---

## 7. Needs a ruling

1. **Take fix #2 (git-tracked corpus) in the two test files?** It is a test-file change, and this
   lane was told to edit no test — so it is proposed, not made. It is the largest measured win in
   this report and it re-applies a standard the repo already ruled on 2026-07-27.

2. **The bigger lever is the one with no number on it — do we rule it anyway?** §1c shows the
   proven tree-walk mechanism accounts for **≈24%** of the observed slowdown; the **8
   concurrently-locked lane sessions** are the named candidate for the other ~76% and are
   **unmeasured**. Fix #2 is worth taking regardless (it is 15 lines and permanent) and would
   *also* make the next measurement clean by removing the confound. **But the recommendation with
   the larger expected value — "an integration suite does not run while lane worktrees are
   locked" — rests on inference, not measurement.** Ruling it costs nothing and probably saves
   ~17 min per arc; I flag plainly that I am recommending it without a number, which is exactly
   the thing this report otherwise refuses to do.

3. **The 8m23s / 8m59s divergence** (§1a): the consolidation report's prose says one, the packet
   and JOURNAL say the other. Both are real runs. Does this need an amendment marker, or is it
   below the bar?

4. **The contract's `2h43m` and `~9 minutes` arc figures are unlocated in the tracked record**
   (§4). If they came from a surface I cannot see — an untracked log, a `/stats` reading, the
   operator's own notes — S3a's design should harvest that surface too, and I should be told what
   it is. If they were estimates, that is exactly the gap S3a exists to close.

5. **Should `/lane-integrate` §2 be amended** to say one suite on the merged result (§3a)? The
   integrator already did the right thing against the letter of the command; the text is what is
   now wrong, and it is worth ~1h21m per batch.

6. **Is the §4 "three passes, same shape → replace the mechanism" trigger worth writing down** as
   a standing ruling for reviewer loops? It is derived from one lane's evidence (n=1), which is
   below this repo's usual bar for a register entry — hence a question, not a proposal.

---

## Appendix — reproduction commands

```
# §1 corpus + the proposed fix, benchmarked (identical 1633-file set)
python -c "from pathlib import Path;import subprocess;R=Path('.');\
S={'.venv','.git','node_modules','__pycache__','.pytest_cache'};\
a={p for p in R.rglob('*.md') if not S.intersection(p.parts)};\
b={R/x for x in subprocess.run(['git','ls-files','-z','*.md'],capture_output=True).stdout.decode().split(chr(0)) if x};\
print(len(a),len(b),len(a-b))"

# §1d collection cost                pytest -n 0 --collect-only -q
# §1d full suite + slowest tests     pytest -q --durations=60
# §2  per-check gate mesh timing     see scratchpad timecheck.py (times each ALL_CHECKS member)
# §3  integration spine              git log --first-parent --format="%h|%ci|%s"
# §4  reviewer-loop pass timing      git log -1 --format="%h %ci" <pass-HEAD>
```

**Cleanup:** the measurement sandbox (`wt-sandbox`, `wt-template`), the hand-built venv and the
timing scripts were created **outside the repo** in the session scratchpad. **The real repo was
never given a worktree, and no tracked file was modified by any measurement.** Verified:
`git worktree list` returns 1 line; `git status --porcelain` shows only this report.
