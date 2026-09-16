# Lane ab-802 — the conductor judges CI by the frozen suite baseline

**Lane:** `lane-ab-802-conductor-freeze` · **Branch:** `worktree-lane-ab-802-conductor-freeze` ·
**Batch:** AB (`docs/audits/2026-09-16-technical-batch-ab-manifest.md`, amended by
`docs/audits/2026-09-16-technical-batch-ab-manifest-amendment-1.md`) · **Date:** 2026-09-16

Consumers: [#802]

## 1 · Premise — the locators, checked before anything was built

**Contract identity.** `sha256` of the frozen contract read at boot
(`H:\My Drive\CLAUDE PROMPT DIR\LANE-ab-802-conductor-freeze.md`):
`7ecc8b30ee367f25a3cd2dc0b6a148af0cf3847e595208f9f6bc849f6764b944`. That matches the pin in the
batch AB manifest amendment 1's lane table (row `lane-ab-802-conductor-freeze`), so this is the
contract that was dispatched.

**Base.** `f8ca1d40` (merge of batch AB amendment 1 onto `main`).

**`logs/SUITE-BASELINE-FREEZE.md`, read in full.** Frozen at `b5270d636774abedff1b00cb0a9c7fb3698c226e`
(main, batch Y close packet merge), Actions `conductor` run `34901604346`, `push`,
2026-09-14T21:57:23Z. Command `uv run --locked pytest -q --tb=short`, resolved to **4 workers**
(`-n auto` on `ubuntu-latest`). Result **51 failed, 5863 passed, 22 skipped, 2 xfailed** in
229.75s. Two same-day amendments already live in the file:

- **The worker count is PINNED to `-n 4`** (2026-09-15 amendment). A consumer must resolve and
  REPORT its own worker count, REFUSE on mismatch (NOT-COMPARABLE, never a pass), and treat a
  missing/stale freeze file the same way.
- **One node id is SHA-dependent** (`test_preflight_contract.py::test_every_claim_class_the_brief_names_is_extractable`,
  because `preflight_contract` silently skips an all-digit short SHA). Recorded as NOT absorbed
  into the frozen set — a live, un-ratified CANDIDATE, disposition owned elsewhere.

**Membership rule, stated in the file as load-bearing:** by test node id, never by count. A
failure inside the 51 is PRE-EXISTING; outside is a REGRESSION; a member that passes is the
expected direction, not a rule failure.

**`docs/audits/2026-09-15-technical-batch-z-close-packet.md`, "Defect three".** The freeze file's
own roster rendering is already truncated for one entry —
`tests/test_dispatch_conformance.py::test_head_token_normalises_the_way_the_reader_normalises[`
— because that parametrize id embeds a space (`"C:\Program Files\claude.exe" --bg-claude`) and
whitespace-delimited extraction breaks on it. The full id lives in
`docs/audits/2026-09-13-technical-lane-x-664-delete-list-execution-evidence.md:293`. The close
packet attributes fixing this to `[#763]` (re-measurement), not to a consumer reading the file as
committed. This lane's gate reads the file AS COMMITTED and does not attempt to reconstruct the
truncated id — see §6 open items.

**`scripts/conductor.py` and `.github/workflows/conductor.yml`, read in full.** `conductor.py` is
Layer-2/read-only, carries the phase gate and the §6 metrics, and a dual-import shim so it works
both as `scripts.conductor` (tests) and as a bare script (the workflow). The `pytest` job in
`conductor.yml` today runs `uv run --locked pytest -q --tb=short` (via `addopts = "-n auto"`, not
the pinned `-n 4`) and its own exit code IS the job's exit code — so main's pre-existing failures
(51 in the frozen file; the batch AB manifest amendment states 62 today, unmeasured by this lane
per contract) make the `pytest` required-check context red on every push, which is [#802]'s
stated symptom ("the conductor emails on every push"). `ruff`, `seal`, `terra` and `phase-gate`
are untouched by this lane's footprint. `deploy/conductor-required-checks.ruleset.json` carries
exactly the three contexts `pytest`, `ruff`, `seal`, `enforcement: disabled` — read, not edited,
per the contract's binding addition.

**Discrepancy against the batch AB manifest amendment, recorded and resolved by contract
primacy.** Amendment 1 §4 ("Checked and NOT sequenced") says *"`actions_verdict.py` is 802's"*.
`scripts/actions_verdict.py` already exists and belongs to `[#675]`/`[#742]` — a job-CONCLUSION
differential the integrator runs at merge time (`gh run view` job list vs. a baseline SHA), a
different layer from this row's node-id comparison inside the `pytest` job itself. The frozen
Done-contract (immutable) states the module explicitly: *"one module (`scripts/conductor.py`)
and one workflow"*. Followed as written; `actions_verdict.py` is not touched by this lane, so the
manifest's sequencing concern is moot in practice regardless of which reading is right.

## 2 · RED-first witnesses (`4a647dbe`)

Recorded run on the pre-build code (`0caae8a7`): **17 failed** over the new tests, each failing
on its own, not at collection:

```
AttributeError: module 'conductor_under_test' has no attribute 'parse_suite_baseline'
AttributeError: module 'conductor_under_test' has no attribute 'parse_failed_node_ids'
AttributeError: module 'conductor_under_test' has no attribute 'suite_gate'
AttributeError: module 'conductor_under_test' has no attribute 'render_suite_gate'
SystemExit: 2 -- error: argument command: invalid choice: 'suite-gate'
AssertionError: the pytest job must run at the freeze's pinned worker count
17 failed in 14.87s
```

The two RED-first legs the contract names: **a synthetic failure OUTSIDE the frozen set turns
the job red** (`test_suite_gate_a_failure_outside_the_frozen_set_fails`) — and **one INSIDE does
not** (`test_suite_gate_a_failure_inside_the_frozen_set_passes`,
`test_suite_gate_no_failures_at_all_passes`). Also witnessed pre-build: a missing baseline, a
stale/malformed one, a cross-worker-count comparison, and a broken pytest invocation (exit code
neither 0 nor 1) — each its own test, each failing for the right reason before the gate existed.

## 3 · The gate (`8dfe92ba`)

`scripts/conductor.py` gains `parse_suite_baseline`, `parse_failed_node_ids`, `suite_gate` and
`render_suite_gate`, plus a `suite-gate` CLI subcommand
(`conductor.py suite-gate --pytest-output <file> --workers N [--pytest-exit N] [--out F]`).
`.github/workflows/conductor.yml`'s `pytest` job now runs the freeze file's own pinned
comparison command (`pytest -q --tb=short -n 4`, replacing the unpinned `-n auto` from
`addopts`), captures it, and gates the job's exit on the suite-gate verdict rather than
pytest's raw exit code. `pytest`'s own exit is still recorded and shown in the step summary;
it no longer decides the job. Every run's report lands in `$GITHUB_STEP_SUMMARY` and as an
uploaded artifact (`pytest-<sha>`, `pytest.out` + `suite-gate.out`).

**Membership is by node id, both directions.** `regressions = failed - frozen`,
`pre_existing = failed & frozen` — a set difference and intersection, not a count. Worker-count
mismatch and a missing/stale baseline both return `verdict: fail` with `reason` naming why,
before any node-id comparison runs.

**Found live, fixed in the same commit: the [#664] edge-class ratchet.** `parse_suite_baseline`
gave `conductor.py` its first `import re` and its first two-plus-regex shape, which the
`graph-edge-class-census` pre-commit hook classifies as a candidate five-kind corpus-structure
edge computation with no verdict — a real, correctly-firing gate, not a false alarm. Verdicted
`not-an-edge` in `scripts/graph_queries.py::EDGE_COMPUTATIONS`, on the same reasoning as the
existing `quality_requirements.py` / `substrate_provenance.py` rows: the frozen roster is a
DECLARED relation a human wrote by hand into `logs/SUITE-BASELINE-FREEZE.md` at freeze time,
read back rather than discovered by scanning the corpus — and a pytest node id is sub-file
granularity FPG-1 has no path to represent in the first place (the very fragility "Defect
three" already found). `private` stayed 18, `reconciled` stayed 3 (both test-pinned in
`tests/test_edge_class_census.py`); `edge-class-census: OK` locally.

## 4 · Verdict

**Targeted suite:** `tests/test_conductor.py` (52) + `tests/test_edge_class_census.py` (24) —
**76 passed**, 0 failed. `ruff check` clean on `scripts/conductor.py`,
`scripts/graph_queries.py`, `tests/test_conductor.py`. No full suite run on this workstation,
per the contract's binding constraint — the gate's own correctness against the LIVE frozen 51
(or main's current, unmeasured count) is only provable on the conductor's own runner, which is
[#763]'s and the integrator's territory, not this lane's.

**Done-contract, checked clause by clause:**
- compares by node id against `logs/SUITE-BASELINE-FREEZE.md` — done, set-based (§3)
- reports success naming the pre-existing set — done (`render_suite_gate`'s `pre-existing`
  block, `suite_gate`'s `reason` string)
- fails loudly on a member outside it — done, names each regression
- fails on a missing or stale baseline — done, two distinct paths, both `NOT COMPARABLE`
- records its own resolved worker count and refuses a cross-worker-count comparison — done;
  `--workers 4` is passed explicitly (matching the `-n 4` the workflow invoked pytest with, so
  there is no `auto`-resolution step to distrust), and any other value is refused as
  `NOT COMPARABLE`
- both RED-first legs witnessed — done (§2)

**Binding additions, checked:** CI enforcement untouched (`deploy/conductor-required-checks.ruleset.json`
not edited; `enforcement: disabled` and the three contexts unchanged); the baseline was READ
only, never re-measured; docs/code in English; logging not print (the module already used
`logging` before this lane, and the new code adds none); targeted pytest green.

## 5 · Decisions taken under the budget, none escalated

1. **Module identity.** Batch AB manifest amendment 1 §4 says *"`actions_verdict.py` is 802's"*.
   Followed the frozen Done-contract instead, which names `scripts/conductor.py` explicitly —
   `actions_verdict.py` belongs to `[#675]`/`[#742]`, a different (job-conclusion, merge-time)
   layer. Not touched. See §1.
2. **"Stale baseline" defined as parse-incomplete, not SHA-ancestry.** The freeze file says
   staleness is "checkable against this file's own Measured at SHA and Source run id" — read as
   "these fields must be present and parseable," not as a git-ancestry check against `HEAD`. An
   ancestry check would need `fetch-depth: 0` on the `pytest` job (added nowhere else needs it)
   and a defined behavior for an indeterminate git result, for a property ("this exact freeze
   was superseded by a later one that edited this same file") the freeze file has no other
   machine-readable marker for. Left as a possible follow-up, not implemented.
3. **Worker count reported by construction, not parsed from pytest's own banner.** `-n auto`'s
   banner line (`N workers [M items]`) is suppressed by `-q`; rather than dropping `-q` (the
   freeze file's own pinned command keeps it) or adding a second parse path, the workflow passes
   `--workers 4` literally, matching the `-n 4` it told pytest to run at. An explicit `-n INT` is
   not `-n auto` — there is no resolution step to distrust, unlike the hazard the freeze file's
   amendment warns about.
4. **A broken pytest run (exit code neither 0 nor 1) is refused, not silently read as clean.**
   Not named in the Done-when in those words, but required by it: an empty failed-node-id set
   from an interrupted or internally-erroring pytest process is indistinguishable from a clean
   run unless the exit code is also checked, and a fail-open reading of "no failures parsed"
   would be exactly the C5 class (`SUITE-BASELINE-FREEZE.md`'s own "a guard that must refuse
   does not refuse") this whole lane exists to avoid reproducing.
5. **`[#664]` edge-class registry row.** Not this lane's declared footprint on paper, but the
   only way to land `scripts/conductor.py`'s new shape without either leaving a real governance
   registry silently wrong or reaching for `SKIP` on a gate that was correctly firing and whose
   registry is precisely the sanctioned remedy for this situation (§3). Treated as a required
   companion to the primary edit, the same way `ORPHAN_DISPOSITIONS` rows accompany a new script
   in sibling lanes' practice, not as scope creep.

## 6 · Open items for the integrator / [#763]

- **The batch-Z close-packet "Defect three" node id.** `logs/SUITE-BASELINE-FREEZE.md`'s own
  roster rendering truncates
  `tests/test_dispatch_conformance.py::test_head_token_normalises_the_way_the_reader_normalises[`
  (a parametrize id embedding a space). This gate reads the file as committed, so a real failure
  of that exact test will report as `regressions` (a false positive) rather than
  `pre_existing`, reproducing the close packet's finding inside this gate rather than a manual
  diff. Already attributed to `[#763]` there; not fixed here, per the contract's binding
  addition that the baseline is read-only in this lane.
- **A stronger, SHA-ancestry-based staleness check** is possible (§5.2) but not built; today's
  check covers "present and parseable," not "this exact freeze predates a later one."
- **This gate's correctness against a real 51-or-62-member run** is unverified from this
  workstation (Windows, no full suite per contract) and is only provable on `ubuntu-latest` at
  the next push — the integrator's or `[#763]`'s territory.
- **`ecosystem/doc-counts.md`'s `pytest_collected` count** is stale after this lane's 17 new
  tests (6350 → 6367, `SKIP`ped per-commit, lane-ab-804 precedent) — the integrator owns
  `gen_doc_counts.py --write` on the merged tree, alongside `docs/audits/README.md`
  regeneration for this file.
