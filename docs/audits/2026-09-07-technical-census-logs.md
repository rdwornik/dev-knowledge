# Census — `logs/` (SWEEP 2026-09-07, lane S-07, READ-ONLY)

consumer: `[#626]` — the open row that owns `logs/` retention and the exemption retirement; its
Done-when clause *"a live run relocates the accumulated files"* is the clause this census measures.
Substantive citation by path: `tasks/626-logs-retention-exempts-the-prefixes-that-accumulate.md`.
Secondary: `intake #66` (the observable-harness direction that names `logs/proposals/`), `ADR-29` /
ADR-39 (the append-only rule that fixes `TOKEN-LOG.md` in place).

- **Base:** `claude/census-logs` off `origin/main` @ `21576e3a4fe77373c936247e6560263b7cd3fbd2`
- **Mode:** read-only. Nothing under `logs/` was moved, deleted, edited or renamed. Every verdict below
  is a **PROPOSAL** for the operator to rule.
- **Gemini fan-out: NONE** — `which gemini` exits 1; the CLI is absent from this container. **Gemini-read
  files: 0. Fabricated locators: 0** (no fan-out ran, so there were no returned locators to re-open).
  Absence is reported as absence, not as clean. **Copilot Enterprise offload was NOT used and is NOT
  available** — `#75` is unratified; recorded here so nobody later claims otherwise.

---

## Lane question — the flat `PROPOSALS-*` / `DETECTOR-ERROR-*` count

### The count NOW is **0**, and the word "now" has to be split three ways

| Measurement | Command | Result |
|---|---|---|
| Flat artifacts **tracked in the index** at `21576e3` | `git ls-files logs/` | `logs/TOKEN-LOG.md` only → **0 flat `PROPOSALS-*` / `DETECTOR-ERROR-*`** |
| Flat artifacts **on disk in this checkout** | `ls -la logs/` | one file, `TOKEN-LOG.md` → **0** |
| Flat artifacts **present-but-ignored** | `git status --ignored --short logs/` | empty output → **0** |

The **tracked** zero is a real, fleet-wide fact and it is the one that matters: exactly one flat artifact
ever reached the index in this repo's history — `logs/DETECTOR-ERROR-2026-09-05.md` — and it was deleted
in the same commit that fixed the writer. Witness:

```
git log --all --diff-filter=AD --name-status -- logs/DETECTOR-ERROR-2026-09-05.md
  353b516  D  logs/DETECTOR-ERROR-2026-09-05.md
  bcf21b1  A  logs/DETECTOR-ERROR-2026-09-05.md   (+ 3 earlier merge-side adds)
git log --all --diff-filter=A --name-only -- logs/
  logs/DETECTOR-ERROR-2026-09-05.md
  logs/TOKEN-LOG.md
```

The other two zeros are **worth nothing as evidence about the operator's machine.** This is an ephemeral
cloud clone; `PROPOSALS-*` and `DETECTOR-ERROR-*` are gitignored per-run ephemera that never travel with
a clone. The last measured local residue is **141 flat dated files at `a39edb2d`**, recorded 2026-09-06
in `353b516`'s own commit body and again in `tests/test_propose_closures_bucket_write.py:11`. Nothing
since has relocated them (see **R5**). So the operator's local flat count is **presumed still ≈141 and
is not verifiable from here.** Treat the tracked zero as the answer; treat the disk zero as an artifact
of where this lane is standing.

### The caller is NOT still writing flat — the fix holds, in both twins

Read-witnesses (`scripts/propose_closures.py` = hub, `plugins/tier1-lifecycle/scripts/propose_closures.py`
= the LIVE Stop-hook copy):

| Seam | Hub | Plugin twin |
|---|---|---|
| `_month_bucket()` returns `logs/YYYY-MM` | `:392` | `:411` |
| `_next_free_dated_path()` returns `_month_bucket(logs_dir, day) / cand` | `:465` | `:484` |
| `_write_artifact()` — `mkdir(parents=True)` then write into the bucket | `:470`–`:473` | `:489`–`:492` |
| `_write_error_marker()` — marker bucketed too | `:544` | `:559` |

Execution-witness (both modules loaded by path, called against a scratchpad temp dir, **nothing written
into the repo** — the temp dir was empty afterwards):

```
HUB  _next_free_dated_path -> 2026-09/PROPOSALS-2026-09-07-01.md
PLUG _next_free_dated_path -> 2026-09/PROPOSALS-2026-09-07-01.md
```

Pinned by `tests/test_propose_closures_bucket_write.py` (204 lines, every location test parametrized over
both twins), notably `test_a_full_run_leaves_ZERO_flat_dated_files:108` and
`test_the_error_MARKER_is_bucketed_too:127`. **Not executed here** — see *Honest limits*.

### Locator correction on the brief's SHA

The contract says the batch-T V2 fix "landed at `92b7aaa9`". Resolved:

- `92b7aaa9` = `Merge branch 'docs/batch-t-anchor-5' -- anchor the manifest amendment`, **1 file changed,
  `JOURNAL.md` +63**. That is the JOURNAL anchor, not the fix.
- `353b5169` = `fix(logs): propose_closures writes into logs/YYYY-MM/, the caller the retention rule
  never had` — **7 files**: both twins, `tests/test_propose_closures{,_bucket_write,_detector_error}.py`,
  `ecosystem/doc-counts.md`, and the deletion of `logs/DETECTOR-ERROR-2026-09-05.md`. That is the fix.
- Ancestry: `353b516` → `92b7aaa9` → `21576e3` (all `git merge-base --is-ancestor` = YES).

Both are in this base's history and **the fix holds**. The brief's SHA is not wrong about the outcome,
only about which commit carries the code.

### What the folder should contain "per its README" — there is no README

`logs/README.md` **does not exist and never has**: `git log --all -- logs/README.md` returns nothing. The
question as posed has no answer, and that absence is itself the finding. The de-facto specification is
distributed across four surfaces, none of which is a front door:

1. **`.gitignore` lines 24–178** — the richest surface: ~15 path declarations, each with a prose
   rationale block explaining *why* the artifact is ephemeral. This is the real spec.
2. **`scripts/logs_retention.py`** module docstring — the shape rule (a dated file directly under
   `logs/` belongs in `logs/YYYY-MM/`) and the absolute `TOKEN-LOG.md` exclusion (`:71`).
3. **`CLAUDE.md` §4** — the naming grammar: UPPERCASE-KEBAB stem, extension honest to the format
   (`[#395]`, ruled 2026-07-22).
4. **`ARCHITECTURE.md`** Ch2 organ rows (`:438`, `:463`, `:465`, `:691`–`:693`) — which organ writes
   which digest.

**Spec vs reality:** the spec says the folder's *committed* surface should be exactly one file, and it
is. That part is correct by design. But two of the ~15 declarations in surface (1) have holes (**R1**,
**R4**), and the surface that would catch them does not exist (**R6**) — so the one place the spec
actually lives is also the one place nothing checks.

---

## Inventory

### A — present in the tree at `21576e3`

| Path | Bytes | Lines | Tracked | Producer / owner | Last content commit | Verdict |
|---|---|---|---|---|---|---|
| `logs/TOKEN-LOG.md` | 6709 | 130 | yes | `/session-summary` (7-day staleness → `ccusage --json` snapshot, newest-first prepend) — `protocols/PLAYBOOK.md:1242`, `:5276`; canonical in `protocols/HANDOFF_PROCESS.md` §15 | `428656f` (2026-09-05) | **KEEP** |

That is the entire present contents of `logs/`. One file.

### B — the declared surface (gitignored ephemera; producer + ignore-coverage measured, not the files themselves)

Every row's ignore state is from `git check-ignore -q <path>` against this base. No file was created to
test it.

| Declared path | Producer (witness) | `.gitignore` decl. | `check-ignore` | Verdict |
|---|---|---|---|---|
| `logs/YYYY-MM/PROPOSALS-*.md` | `propose_closures._write_artifact` — hub `:470`, plugin `:489` | `:34` | IGNORED | **KEEP** |
| `logs/YYYY-MM/DETECTOR-ERROR-*.md` | `propose_closures._write_error_marker` — hub `:512`, plugin `:527` | `:35` | IGNORED | **KEEP** |
| `logs/PROPOSALS-*.md` (flat, legacy) | no current producer — pre-`353b516` residue | `:26` | IGNORED | **ARCHIVE** → `logs/YYYY-MM/` (R5) |
| `logs/DETECTOR-ERROR-*.md` (flat, legacy) | no current producer — pre-`353b516` residue | **none** | **NOT-IGNORED** | **ARCHIVE** → `logs/YYYY-MM/` (R1, R5) |
| `logs/FLEET-HEALTH.md` | `scripts/fleet_health.py:44` `_HEALTH_FILE` | `:39` | IGNORED | **KEEP** |
| `logs/ENFORCEMENT-COVERAGE.md` | `scripts/enforcement_coverage.py:70` `_DIGEST_PATH` | `:44` | IGNORED | **KEEP** |
| `logs/LIVED-WORKFLOW.md` | `deploy/lived_sandbox/cli.py:35` `_REPORT` | `:48` | IGNORED | **KEEP** |
| `logs/BOUNDARY-DRIFT.md` | `scripts/boundary_report.py:43` `_BOUNDARY_FILE` | `:52` | IGNORED | **KEEP** |
| `logs/FLEET-ANALYTICS.md` | `scripts/fleet_analytics.py:106` `_ANALYTICS_FILE` | `:58` | IGNORED | **KEEP** |
| `logs/FLEET-PARITY.md` | `scripts/fleet_parity.py:122` `DIGEST_PATH` | `:64` | IGNORED | **KEEP** |
| `logs/PARITY-EVENTS.jsonl` (+ `.1`) | `scripts/fleet_parity.py:123` `EVENTS_PATH` | `:65`, `:66` | IGNORED | **KEEP** |
| `logs/OPERATOR-LOAD.csv` | `scripts/fleet_health.py:131` `LOAD_CSV_NAME` (`append_load_row`) | `:74` | IGNORED | **KEEP** |
| `logs/.session-override-token` | `.claude/commands/override.md:52` (PowerShell block); read by `scripts/session_end_backpressure.py:148,:246` | `:98` | IGNORED | **KEEP** |
| `logs/OVERRIDES.md` | `.claude/commands/override.md:46`–`:51` — producer exists but the command is **RETIRED** (ADR-85 amend. §A2) and writes telemetry only | `:99` | IGNORED | **KEEP** (see R7) |
| `logs/COHERENCE-NUDGE.log` | `scripts/coherence_nudge.py:41` `_LOG_PATH` | `:105` | IGNORED | **KEEP** |
| `logs/TELEMETRY.db` (+ `-wal`, `-shm`) | `scripts/telemetry_emit.py:167` `DEFAULT_DB_RELPATH` | `:119` (`TELEMETRY.db*`) | IGNORED | **KEEP** |
| `logs/GENAI-TELEMETRY.db` (+ `-wal`, `-shm`) | `scripts/cost_usage_telemetry.py:104` `DEFAULT_DB_RELPATH`; WAL via `:239`,`:248` | **none** | **NOT-IGNORED** | **KEEP** — but the ignore rule is missing (R4) |
| `logs/prompts/` | `scripts/trace_writer.py:30` `_DEFAULT_OUT_DIR` | `:178` | IGNORED | **KEEP** |

---

## Proposals

Grouped by verdict. Each carries a witness. Nothing here was executed.

### KEEP

**K1 · `logs/TOKEN-LOG.md`.** Witness: append-only by ADR-29 / ADR-39 with **no archival carve-out** —
the 2026-07-17 amendment is `LESSONS.md`-only in as many words, and `scripts/logs_retention.py:22`–`:29`
restates that and enforces it structurally via `TOKEN_LOG_NAME` (`:71`) rather than relying on the date
regex missing it. Live consumer: `/session-summary`'s 7-day staleness check
(`protocols/PLAYBOOK.md:5276`). Last content commit `428656f`, 2026-09-05. **Do not touch this file** —
relocating it, even byte-identically, is the one act the retention organ is built to refuse.

**K2 · the sixteen gitignored declared paths in Inventory B.** Each has a named live producer at a cited
`file:line`. Zero orphan declarations were found — the census specifically hunted for one and did not
find one. (`logs/LIVED-WORKFLOW.md` looked orphaned under a `scripts/` + `plugins/` grep and is not: its
producer is `deploy/lived_sandbox/cli.py:35`. Recorded so the next census does not re-raise it.)

### ARCHIVE

**A1 · the ≈141 legacy flat dated artifacts on the operator's machine → `logs/YYYY-MM/`.** Witness: the
count is `353b516`'s commit body and `tests/test_propose_closures_bucket_write.py:11`, measured at
`a39edb2d`; the destination grammar is `scripts/logs_retention.py`'s `_DATED_RE` + `parse_dated_month`.
The mechanism to do it exists and is tested (`tests/test_logs_retention.py`). **It has no caller** — see
R5. This is the open half of `[#626]`'s Done-when and it is proposed, not performed: this lane is
read-only, the files are not in this checkout, and a wrong move corrupts the closure detector's
pending-window baseline, which is the row's own recorded risk.

### RETIRE

**None proposed.** No file or declaration under `logs/` was found to have lost its producer outright.
`logs/OVERRIDES.md` is the nearest candidate and it is deliberately **not** proposed for retirement — see
R7.

### UNDETERMINED

**U1 · `plugins/tier1-lifecycle/tests/test_plugin_paths.py:98` — verdict is read-only, not run.** See
R2. I could not execute the test (no pytest in this container), so the failure is inferred from source,
not witnessed. It is recorded as UNDETERMINED rather than upgraded on confidence.

**U2 · the operator's live flat count.** Stated as ≈141-presumed above. Not measurable from this lane.

### Residual defects found — reported, NOT fixed

**R1 · `.gitignore` has no FLAT `logs/DETECTOR-ERROR-*.md` rule, and this is the exact hole that put a
run artifact in the index.** Measured:

```
git check-ignore -q logs/PROPOSALS-2026-09-07-01.md      -> IGNORED
git check-ignore -q logs/DETECTOR-ERROR-2026-09-07.md    -> NOT-IGNORED     <-- the hole
git check-ignore -q logs/2026-09/PROPOSALS-2026-09-07-01.md   -> IGNORED
git check-ignore -q logs/2026-09/DETECTOR-ERROR-2026-09-07.md -> IGNORED
```

`.gitignore:26` covers flat `PROPOSALS-*.md`; `:34`/`:35` cover both prefixes one level deep. Flat
`DETECTOR-ERROR-*.md` is covered by nothing. `scripts/propose_closures.py:400`–`:403` already names this
in its own docstring — *"one of which (`DETECTOR-ERROR-2026-09-05.md`) reached the INDEX, because
`.gitignore` anchors `DETECTOR-ERROR-*.md` one level deep only"* — so the defect is **known and recorded
but not closed.** Post-`353b516` it is latent in this repo (the writer no longer emits flat), which is
why it survived: the fix removed the *producer* of the hazard without closing the *hole*. Any legacy
flat marker on the operator's disk is a live untracked-and-not-ignored file today.

**R2 · a plugin test still globs flat while the writer it exercises buckets.**
`plugins/tier1-lifecycle/tests/test_plugin_paths.py:98`:

```python
proposals = list((host / "logs").glob("PROPOSALS-*.md"))
assert proposals, f"no proposals written to host logs/; stderr={result.stderr}"
```

`Path.glob` there is non-recursive. The test runs the plugin script as a subprocess against a temp host
repo; `_write_artifact` → `_next_free_dated_path` → `_month_bucket(logs, today) / name` lands the file at
`host/logs/2026-09/PROPOSALS-2026-09-07-01.md`, which that glob cannot match. `353b516` changed 7 files
and **this was not one of them**; the file's last touching commit predates the fix
(`git log -3 -- plugins/tier1-lifecycle/tests/test_plugin_paths.py` → `428656f`). `pyproject.toml`
declares no `testpaths`, no `norecursedirs`, and there is no root or `tests/` `conftest.py`, so default
rootdir recursion does collect this file. Expected consequence: `:99` fails. **Not run** — U1.

**R3 · the `#98` empty-regeneration safety net is stale in both twins.** `scripts/propose_closures.py:587`
(and the plugin twin at the corresponding site) still builds the **pre-grammar flat bare name**:

```python
target = _LOGS_DIR / f"PROPOSALS-{date.today().isoformat()}.md"
if not strong and not weak and target.exists():
    ...
    return 0
```

Two grammar changes have passed it by: the per-run `-NN` sequence (operator declaration 2026-09-04, see
`_next_free_dated_path`'s docstring) and bucketing (`353b516`). The writer has not produced a name of
that shape since. The hazard it was built for is also gone — the plugin docstring's premise,
*"`_write_artifact` overwrites `PROPOSALS-<date>.md` unconditionally"*, is no longer true, because
`_next_free_dated_path` returns a name `_existing_anywhere` says is free and therefore never overwrites.
Residual live effect, narrow but real: if a **legacy** flat `PROPOSALS-<today>.md` exists carrying a
still-open unchecked id, `main()` returns 0 early and writes **nothing** that day — inverting the module's
own *"its ABSENCE is the loud failure signal"* contract (`:529`) by way of a guard that no longer guards
anything. Decays to zero once R5's residue is cleared.

**R4 · `logs/GENAI-TELEMETRY.db` is not ignored, and it reproduces the exact failure the sibling glob
exists to prevent.** `scripts/cost_usage_telemetry.py:104` sets
`DEFAULT_DB_RELPATH = Path("logs") / "GENAI-TELEMETRY.db"`, and `:239`/`:248` open it with
`telemetry_emit.WAL_PRAGMAS`, so a live run leaves `-wal` and `-shm` sidecars. `.gitignore:119` is
`logs/TELEMETRY.db*` — anchored to the *other* store's stem:

```
git check-ignore -q logs/TELEMETRY.db          -> IGNORED
git check-ignore -q logs/TELEMETRY.db-wal      -> IGNORED
git check-ignore -q logs/GENAI-TELEMETRY.db    -> NOT-IGNORED    <-- the hole
git check-ignore -q logs/GENAI-TELEMETRY.db-wal-> NOT-IGNORED
```

`.gitignore:110`–`:118` states in its own words why the glob rather than the bare name: *"A bare
`logs/TELEMETRY.db` would leave a stray `-wal` dirtying `git status` and tripping session-end
backpressure: the exact failure this leg was filed to prevent."* That reasoning was written for one store
and the second store was added without it.

**R5 · `scripts/logs_retention.py` still has ZERO production callers.** A grep for `logs_retention` across
every `.py` / `.json` / `.yaml` / `.toml` in the tree returns: its own module, **six docstring prose
references** (`fleet_health.py:585`, `review_closures.py:200`, `propose_closures.py:305,395,419,421`), and
its two test files. No hook, no gate, no CLI, no `main()` invokes `run_retention()`. This is unchanged
from the state `353b516`'s commit body described on 2026-09-06. The consequence is precise: batch-T fixed
the **writer**, so new artifacts are born bucketed and the bleeding stopped — but **no organ can relocate
the ≈141 files already flat.** `[#626]`'s Done-when names *"a live run relocates the accumulated files"*;
that clause is not discharged, and `[#626]` remains correctly open.

**R6 · nothing gates `logs/` at all.** `grep -rln logs scripts/audit_checks/` returns **zero files**. No
registered audit check and no pre-commit hook inspects `logs/` naming, contents, or ignore coverage. The
`[#395]` UPPERCASE-KEBAB + honest-extension convention (CLAUDE.md §4, ruled 2026-07-22) is an
instruction with no mechanism. R1 and R4 are both ignore/naming defects of exactly the class a mechanism
would have caught, and both survived months in a repo that gates 23 other things at commit time.

**R7 · `logs/OVERRIDES.md` — a live producer behind a retired command.** `.claude/commands/override.md`
still writes it (`:46`–`:51`) and still writes `logs/.session-override-token` (`:52`), but the command's
own frontmatter reads *"RETIRED (ADR-85 amendment 2026-08-03 §A2) — discharges no gate; arms a local
telemetry token only"*, and CLAUDE.md §7 says the same. `deploy/carrier_mesh.py:90` still carries both
paths in `_GITIGNORE_IGNORES`, i.e. still ships the ignore lines to deployed children. **Not proposed for
retirement:** the command explicitly keeps the file as override-rate telemetry (`:66`), which is a stated
purpose, not an oversight. Recorded so a later sweep does not mistake "retired command" for "dead file".

---

## Counts before → proposed after

| Metric | Before (measured at `21576e3`) | Proposed after |
|---|---|---|
| Files present in `logs/` in this checkout | 1 (`TOKEN-LOG.md`) | 1 — **no change** |
| Files tracked under `logs/` | 1 | 1 — **no change** |
| Flat `PROPOSALS-*` / `DETECTOR-ERROR-*`, **tracked** | 0 | 0 — **no change** |
| Flat `PROPOSALS-*` / `DETECTOR-ERROR-*`, **operator-local** | ≈141 (presumed; last measured `a39edb2d`) | 0, via A1 — **requires an operator-run `run_retention()`; not performed here** |
| Declared `logs/` paths with a live producer | 17 of 17 | 17 — **no change** |
| Declared `logs/` paths NOT covered by `.gitignore` | **2** (flat `DETECTOR-ERROR-*.md`; `GENAI-TELEMETRY.db*`) | 0, via R1 + R4 |
| Production callers of `logs_retention.run_retention()` | **0** | ≥1, via R5 |
| Audit checks / gates policing `logs/` | **0** | ≥1, via R6 |
| Files this lane created, moved, edited or deleted under `logs/` | — | **0** |
| Files this lane created anywhere | — | **1** (this census) |

**Net proposed change to `logs/` contents in this repo: zero.** Every proposal above is either a
`.gitignore` amendment, a caller/gate wiring, or a relocation that can only run on the operator's machine.

---

## Honest limits

What I could **not** establish, stated as such rather than padded over:

1. **The operator's actual flat count.** This is an ephemeral cloud clone. `PROPOSALS-*` and
   `DETECTOR-ERROR-*` are gitignored per-run ephemera and do not survive a clone, so the disk-level zero
   I measured is a property of *where this lane is standing*, not of the folder. The ≈141 figure is
   inherited from `353b516`'s commit body at `a39edb2d` — a **relay of a prior measurement, not a
   witness of mine.** It could be higher (a week of runs since) or lower (a manual sweep). Only the
   *tracked* zero is my own evidence.

2. **No test was run — at all.** `uv run --locked pytest` refuses: `Required uv version ==0.11.19 does
   not match the running version 0.8.17`. There is no `.venv` and `python3 -c "import pytest"` raises
   `ModuleNotFoundError`. So **R2 is a reading, not a run** (U1), and my statement that
   `tests/test_propose_closures_bucket_write.py` pins the fix is a statement about the file's *contents*,
   not about it passing. The one execution-witness I do have is the direct module load reported above,
   which exercised `_next_free_dated_path` / `_month_bucket` in isolation against a scratchpad temp dir
   with no dependencies. That is narrow and I am not stretching it.

3. **Whether any deployed child still runs a pre-`353b516` plugin twin.** R1's hole is latent in the hub
   because the hub's writer buckets. A child on an older `tier1-lifecycle` would still emit flat, and
   `deploy/carrier_mesh.py` ships `.gitignore` lines to children — so the hole could be live somewhere
   downstream. I have no access to any child repo from this lane and did not guess.

4. **Whether the `.session-override-token` reader is still load-bearing.**
   `scripts/session_end_backpressure.py:246` still reads the token, while
   `.claude/commands/override.md:61` says *"nothing consults the token"*. One of those is stale. Tracing
   which would mean following the Stop hook's control flow past the `logs/` boundary, which is another
   lane's folder, so I stopped at recording the disagreement.

5. **`ecosystem/doc-counts.md` claims 5187 collected tests** and was bumped by `353b516`. I could not
   re-collect (limit 2), so I cannot confirm whether R2's test is inside that count. My claim that it is
   collected rests on config reading — no `testpaths`, no `norecursedirs`, no `conftest.py` — not on a
   `--collect-only` run.

6. **The authority file was not read.** The contract names
   `to-cc\BATCH-2026-09-07-SWEEP-CONTRACTS.md` (5422 B) as the frozen authority that wins over the
   working copy. It is not in this repo and not on this container's filesystem (`find /` for that name
   returns nothing) — it lives on the operator's Drive transport. I executed against the working copy in
   the brief alone. **If the two disagree, this census followed the wrong one and does not know it.**

7. **No Gemini fan-out and no Copilot offload.** `gemini` is not on PATH: fan-out **NONE**, Gemini-read
   files **0**, fabricated locators **0**. Copilot Enterprise is unavailable pending `#75`. Every locator
   in this census was opened by me directly. That is a smaller net than the contract intended, and it is
   reported as a reduced net rather than as a clean one.

8. **No gate fired on this census.** `.git/hooks/` in this container holds nothing but the stock
   samples — `pre-commit install` was never run here and `pre_commit` is not importable
   (`ModuleNotFoundError`), which follows from limit 2's broken `uv` pin. So `consumer_at_landing`,
   `audit-health`, `audit-index-freshness`, `validate-hermetization`, `audit-title-gate` and `ruff` did
   **not** run against this file. I substituted hand-checks for the two that would most likely refuse it:
   `_CITATION_RES` (`scripts/consumer_at_landing.py:133`) re-run by hand over the file's text matches
   `[#626]`, `ADR-29` and `intake #66`; the `# ` title heading is line 1. Those are proxies for the gates,
   not the gates. The integrator's merge is the first point at which this file meets them.

9. **The known RED on main is untouched and unclaimed.**
   `test_manifest_link_route.py::test_the_class_enum_is_the_hermetization_module_s_own_object` is not
   this lane's, was not chased, and is not asserted about — I could not have run it in any case (limit 2).
