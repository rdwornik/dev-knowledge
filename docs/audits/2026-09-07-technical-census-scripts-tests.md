# Census — `scripts/` + `tests/` (SWEEP 2026-09-07, read-only)

**Consumer:** `[#397]` (`scripts/` target structure — the CLOSED row whose "first full
`scripts/` inventory + caller-impact map (~50 files, ZERO orphans)" this census re-measures
and supersedes), `[#493]` (the silent scheduled fleet-baseline task — this census resolves
the consumer question for both of that row's non-Python organs), `intake #73` (home grammar,
the RELOCATE target vocabulary). Full per-file tables:
`docs/audits/2026-09-07-technical-census-scripts-tests-appendix.md`.

**READ-ONLY.** Nothing was moved, deleted, edited or renamed. Every verdict below is a
PROPOSAL the operator rules. Measured at `21576e3` on branch `claude/census-scripts-tests`.

**Headline, stated before the tables because it is the finding:** across 358 tracked files in
the two folders, **the census proposes zero removals**. Every file carries a witness. That is
not the same as "the tree is clean" — it is the honest output of a rule that treats a *found*
consumer as evidence and an *absent* one as nothing. What the sweep actually turned up is
three narrower defects (§ Proposals B) and one stale governance record: `[#397]`'s map,
closed on ~50 files, now describes a folder of **135**.

## Inventory

### Shape

| folder | tracked files | bytes |
|---|---:|---:|
| `scripts/` | 135 | 3,043,911 |
| `tests/` | 223 | 4,339,597 |
| **total** | **358** | **7,383,508** |

`scripts/` decomposes as 99 top-level files (95 `.py`, 3 `.ps1`, 1 `.task.xml`) plus four
sub-packages: `audit_checks/` 24, `codemap/` 7, `toc/` 4, `hooks/` 1.
`tests/` decomposes as 160 `test_*.py` plus 63 files under `fixtures/` (13 fixture
directories). There is no `conftest.py` anywhere — the import substrate is
`pyproject.toml`'s `pythonpath = [".", "scripts", "deploy"]` (the `[#521]` Shape B ruling),
not a root conftest.

### `scripts/` by wiring surface

A file may appear on several rows; the rows are surfaces, not a partition.

| surface | files | where the wiring is read from |
|---|---:|---|
| pre-commit hook | 28 | `.pre-commit-config.yaml` + `.pre-commit-hooks.yaml` |
| `audit_checks` registry | 24 | `scripts/audit_checks/registry.py` imports |
| deploy manifest | 21 | `deploy/manifest-v*.yaml` |
| command / skill / workflow | 18 | `.claude/commands|skills|workflows/` |
| session hook | 8 | `.claude/settings.json` |
| plugin (`tier1-lifecycle`) | 8 | `plugins/**` |
| CI | 4 | `.github/workflows/report-only-wall.yml` |
| **no wiring surface at all** | **53** | — library modules and operator-invoked CLIs |

**85 of 135** files under `scripts/` carry `if __name__ == "__main__"`. Operator invocation is
therefore the single largest consumer class in this folder, and it is the one class no gate,
hook or manifest records. The repo already knows this and has an organ for it —
`check_routine_consumers`, which reads `routine:` declarations off **open** backlog rows —
but that organ cannot see a routine whose row has closed, a limitation `[#461]` states
against itself in `tasks/461-mechanize-window-report-metrics.md:13`.

### `tests/` by how a test reaches its subject

| mechanism | files | note |
|---|---:|---|
| bare-name `import` | 121 | resolved by the `pythonpath` substrate |
| `importlib.spec_from_file_location` | 20 | explicit path load, bypasses the substrate |
| `subprocess` spawn | 15 | the script is run as a process (hooks, CLIs) |
| live-tree read | 4 | asserts against the repo tree, imports no module |

### Verdict distribution

| verdict | `scripts/` | `tests/` (incl. fixtures) |
|---|---:|---:|
| KEEP | 135 | 223 |
| RELOCATE | 0 | 0 |
| ARCHIVE | 0 | 0 |
| RETIRE | 0 | 0 |
| UNDETERMINED | 0 | 0 |

Per-file rows with the witness for each: appendix §A1 (135 scripts), §A2 (160 tests), §A3 (13
fixture directories).

## Proposals

### A · KEEP — 358 files, all four hand-checked near-misses included

The automated rule left four `scripts/` files with no machine-visible consumer. All four
resolve on inspection, and the resolutions are recorded here because each names a *class* of
consumer the scan does not model:

| file | witness | class the scan missed |
|---|---|---|
| `scripts/codemap_hook.py:1-16` | `.pre-commit-hooks.yaml:26,35` — `entry: scripts/codemap_hook.py check .` | the CHILD-facing hook-source manifest, not the hub's own config |
| `scripts/toc_hook.py:1-16` | `.pre-commit-hooks.yaml:44,52` — `entry: scripts/toc_hook.py check` | same |
| `scripts/setup-fleet-scheduler.ps1:53,67` | open row `[#493]`, `tasks/493-…:12` names it by path; the script registers the `\DevKnowledge\fleet-baseline` task that runs `scripts/fleet_health.py` | a Windows Task Scheduler installer — no Python edge exists to find |
| `scripts/fleet-baseline.task.xml` | exported by `setup-fleet-scheduler.ps1:35,67`; named by the same open row `[#493]` | a data artifact consumed by a `.ps1`, not by code |

Both `_hook.py` wrappers are mode `100755` (`git ls-files -s`), which `language: script`
requires — checked, not assumed.

### B · Three defects to file — reported, not fixed

**B1 · The two child-facing hook entrypoints are the only *Python* files under `scripts/` that
no test mentions.** Verified by `grep -rlF <basename> tests/` and `grep -rlw <stem> tests/`
over all 135 files: exactly four come back empty — `codemap_hook.py`, `toc_hook.py`,
`setup-fleet-scheduler.ps1`, `fleet-baseline.task.xml`. The `.ps1`/`.xml` pair is Windows-only
and outside a Python harness, which is a stated constraint rather than a gap; the other two are
not. `tests/test_codemap.py:281` and `tests/test_toc.py:165` do spawn the real CLIs
(`python -m codemap.cli`, `python -m toc.cli`), which is the path **the hub** runs —
`.pre-commit-config.yaml:60,68` invoke `python -m scripts.codemap.cli` /
`python -m scripts.toc.cli` directly. The path a **consumer repo** runs is the wrapper, and the
wrapper's one interesting behaviour — the `sys.path.insert` that makes `codemap` importable
from inside the *cloned* hook repo — is executed by nothing in this suite. The distributed
surface is the untested one. No open row owns this.

**B2 · `cost_usage_telemetry.py` is a live "library only" module with no row that owns wiring
it.** Answering the brief's named question directly:

- It self-declares the class, `scripts/cost_usage_telemetry.py:2-3`: *"Library only; no call
  sites -- same posture `telemetry_emit.py` shipped at Stage 1."*
- Measured, that declaration is exactly true today: **zero** importers outside `tests/`, zero
  wiring surfaces, one test (`tests/test_cost_usage_telemetry.py`, 6 test functions, loading
  it via `importlib.spec_from_file_location` at line 26 rather than importing it).
- Its own stated precedent has since graduated. `telemetry_emit.py` now has **six** in-tree
  consumers besides `cost_usage_telemetry.py` itself: five AST imports (`audit.py`,
  `block_commit_on_main.py`, `block_ff_push.py`, `governance_health.py`, `single_flight.py`)
  plus one explicit path-load, `gen_trend_dashboard.py:98`
  (`spec_from_file_location("dev_knowledge_telemetry_emit", …/telemetry_emit.py)`).
  `gen_dashboard.py:51` and `file_purpose_graph.py:71` name it in prose only — the former
  states outright that it does *not* import it "and a test pins that", so they are excluded.
  `cost_usage_telemetry.py` does import it, for the `[#565]` `run_id` correlation. "Same
  posture as `telemetry_emit` at Stage 1" is therefore a claim about a *transitional* state,
  and the transition is what nothing tracks.
- **`grep -rl cost_usage_telemetry tasks/` returns nothing.** The module is cited by six paths
  under `docs/audits/` — five artifacts plus its own lane contract,
  `2026-08-31-technical-batche-launch-contracts/LANE-f-6-observability-otel.md` — and by
  `JOURNAL.md`, and by **no backlog row, open or closed** (`tasks/` is searched recursively,
  `tasks/archive/` included). Its collector seam is deliberately unimplemented (`resolve_exporter` raises
  `CollectorNotAvailable` because no `opentelemetry-*` package is declared — an ADR-106 gate),
  which is correct and stated; but the *wiring* question, which is not gated by anything, has
  no owner.

Proposal: **KEEP** the module, and file one row owning the graduation — either a named call
site or a recorded decision that the emitter stays dormant pending the ADR-106 dependency act.
This census does not file it; filing is the operator's.

**B3 · `[#397]`'s inventory is stale by a factor of 2.7 and the row is closed.**
`tasks/397-scripts-target-structure-rule-on-the-mapped-grou.md:13` records the 2026-07-22
hygiene lane's map: *"~50 files, ZERO orphans"*, with groupings summing to ~58. Today's count
is **135**. The row closed on "flat-is-fine is recorded with the map as the navigation aid" —
so the navigation aid is the deliverable that survived, and it now describes a folder less
than half this size. The zero-orphans finding still replicates (this census reproduces it at
135 files); the map does not. A closed row cannot be reopened by preference, so the proposal
is that this census's appendix §A1 **is** the refreshed navigation aid, cited from wherever
`[#397]`'s map is cited today.

### C · Tests whose subject no longer exists — none found

Two independent passes, both negative:

1. **Import resolution.** Every non-stdlib module imported by all 160 `test_*.py` files was
   resolved against the tracked tree under the `pythonpath` substrate. One unresolved name
   came back — `scripts.x` in `tests/test_audit.py` — and it is a fixture *string* inside a
   synthetic source body, not an import of `tests/test_audit.py` itself.
2. **Repo-root-anchored path citations.** Every `_ROOT / "…" / "…"` chain in `tests/` was
   resolved against the working tree. Exactly two do not exist, and **both are deliberate
   negative assertions**: `tests/test_deploy_docs.py:326` asserts `not (_REPO_ROOT /
   "INSTALL.md").exists()` (pinning that the hub never self-deploys the plugin's `INSTALL.md`,
   which lives at `plugins/tier1-lifecycle/INSTALL.md` — verified present), and
   `tests/test_fleet_shape_spec.py:120` asserts `not (_ROOT / "docs" / "dashboard").exists()`
   (pinning that admission to the genre grammar and existence in the tree are different acts).
   A non-existent path is the assertion, not a rot signal.

The naive heuristic — "`test_foo.py` with no `scripts/foo.py`" — flags 67 of 160 files and is
worthless: the repo tests behaviours and properties (`test_skip_is_not_pass.py`,
`test_green_by_skip_sweep.py`, `test_writer_integrity.py`) at least as often as it tests
modules. It is reported here only so nobody re-runs it and mistakes it for a finding.

Similarly, all 22 `scripts/audit_checks/check_*.py` modules are named by ≥2 test files each
(2–6, measured); the "16 untested audit_checks modules" that a filename-only scan produces is
an artifact of the scan, because those tests name the **check function**, not the file.

## Counts before → proposed after

| | before | proposed after | delta |
|---|---:|---:|---:|
| `scripts/` files | 135 | 135 | 0 |
| `tests/` files | 223 | 223 | 0 |
| total tracked files in scope | 358 | 358 | 0 |
| total bytes | 7,383,508 | 7,383,508 | 0 |
| files proposed for RELOCATE / ARCHIVE / RETIRE | — | 0 | — |
| new backlog rows proposed (B1, B2, B3) | — | 3 | +3 |

The census proposes **no file movement**. Its output is three rows and one refreshed map.

## Honest limits

What this census could NOT establish, in descending order of how much it costs the reader:

1. **The "last content commit" witness class was unavailable.** This clone is **shallow** —
   `.git/shallow` exists, 17 grafts, 278 commits, history begins 2026-09-01. Every file under
   `scripts/` and `tests/` therefore dates to 2026-09-05, -06 or -07, which is the graft
   boundary talking, not the file's age. The brief sanctions three witness classes; **one of
   the three was structurally unusable here**, so every verdict in this census rests on
   consumer-grep or generator provenance alone. A file genuinely untouched since June is
   indistinguishable from one edited yesterday. Anyone wanting the staleness axis must re-run
   the age half against a full clone.
2. **Nothing in this census was executed.** `uv run --locked` refuses in this container —
   `Required uv version ==0.11.19 does not match the running version 0.8.17` — so the repo's
   own oracles were read, never run: `reverse_dep_oracle.py` (Pyright-driven reverse
   dependencies), `safe_remove.py` (its consuming removal gate), `audit.py health`,
   `check_routine_consumers`, `file_purpose_graph.py`. Those are the repo's *authoritative*
   answer to this census's question and this census did not consult them. Everything reported
   here is a second, weaker, hand-rolled measurement of the same tree. The pre-commit hooks
   are also **not armed in this container** (`.git/hooks/pre-commit` absent), so this commit
   was not gate-checked; the integrator's merge is the first time these two files meet a gate.
   Per the brief, no test suite was run.
3. **The consumer scan is a lower bound on liveness, never an upper bound on death.** It
   models imports (AST, plus a regex recovery for the `from scripts import foo as _f` form the
   AST records as a bare `scripts` — 30+ real edges that would otherwise have been dropped),
   verbatim filename/dotted-name tokens, and eight named wiring surfaces. It does **not** model:
   dynamic dispatch, `getattr`, string-keyed registries, a script invoked from a shell one-liner
   in an operator's head, or a consumer in a sibling repo under `Dev/`. It also does not model
   **path-loading**, and this tree has live instances of it: `gen_trend_dashboard.py:98`
   reaches `telemetry_emit.py` through `spec_from_file_location`, and 20 of the 160 test files
   reach their subject the same way. Every one of those makes a *dead* file look alive. So
   "zero RETIRE" means **no file was proven dead**, not that none is. `safe_remove.py:21-25`
   records the same limit for the repo's own gate, and this scan is weaker than that gate.
4. **The 53 files with no wiring surface were not individually adjudicated for necessity.**
   They have a witness (an importer, a test, or a governance mention) and so they are KEEP. But
   "something imports it" and "the repo would be worse without it" are different questions, and
   only the first was asked. A genuine subtraction pass over that tier is a different, slower
   exercise than a census.
5. **The `.ps1` tier is unmeasured beyond its references.** Three PowerShell files
   (`billing_leak_sentinel.ps1`, `setup-fleet-scheduler.ps1`, `surface_triage.ps1`) and one
   Task Scheduler XML are Windows organs; this is Linux. Their references were resolved, their
   behaviour was not, and `[#493]` is open precisely because the scheduled task they configure
   has been observed silent. Whether the scheduler pair still *works* is outside what a file
   census can say.
6. **The authority file was not read.** The brief instructs "Read that file yourself" for
   `to-cc\BATCH-2026-09-07-SWEEP-CONTRACTS.md` (5422 B). It is on the operator's Drive
   transport and is **not present in this container** (searched the filesystem; absent). This
   census was executed against the brief's working copy alone. If the two disagree, the frozen
   contract wins and this artifact is wrong in whatever respect they differ.
7. **Two small imprecisions in the generated table, stated rather than hidden.** The
   `audit registry` surface counts 24 rather than 22 because `_common.py` and `registry.py`
   match their own names in the registry file; the substantive claim — that all 22
   `check_*.py` modules are imported by `registry.py:52-122` — was checked by reading the
   imports. And a witness reading "named in N test file(s)" is a weaker edge than
   "test importer": it means the filename appears in a test, which for a subprocess-spawned
   script is the real edge and for anything else may be a mention in a docstring.

**Gemini fan-out: NONE.** `which gemini` returns nothing — the CLI is not on PATH in this
container. **This is an absence, not a clean result:** no retrieval or ranking pass was
performed, so nothing in this census was cross-read by a second reader. Gemini-read files: 0.
Fabricated locators counted: 0 — vacuously, since no locators were returned to check.
**Copilot Enterprise offload was NOT used and was NOT available** — it is gated on `intake #75`
(`docs/intake/2026-09-06-tech-copilot-offload-role-and-account-map.md`), which is not ratified.
Recorded here so no later reader concludes otherwise.

Every locator in this artifact was opened before it was cited. Three claims drafted from a
mechanical pass were **wrong on inspection and corrected** before landing: the fixture-consumer
map (`lived-workflow`, `repo-with-structural-checks` and
`manifest-v1.1.0-pre-essence.yaml` each name a different test than the draft asserted), the
`codemap_hook.py`/`toc_hook.py` verdict (drafted UNDETERMINED against
`.pre-commit-config.yaml`, resolved by `.pre-commit-hooks.yaml`), and the
`desired_state_report.py` orphan reading (dissolved by
`tests/test_desired_state_report.py:35`, a `from scripts import …` edge the AST pass had
dropped). Those three are the measured error rate of the mechanical pass on this tree.
