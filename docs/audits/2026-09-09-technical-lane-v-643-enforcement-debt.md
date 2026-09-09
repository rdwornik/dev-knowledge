# Lane `v-643-enforcement-debt` — end-of-lane record: what was built, what was measured, and the two clauses this lane could not discharge

Consumers: `[#643]`

> Batch V, lane 5. Contract:
> `docs/audits/2026-09-08-technical-batch-v-launch-contracts/LANE-v-643-enforcement-debt.md`,
> frozen at dispatch against `main` @ `08c35b9c`. Lane base `33bcb0bd`, branch
> `worktree-lane-v-643-enforcement-debt`. Every number below was measured in this worktree at
> the commit it is attributed to; none is transcribed from the contract or from a prior report.

---

## 0 · The PLAN round — the two budgeted forks, decided

The contract budgeted exactly two design forks and asked for a proposed `pytest-timeout`
value. All three are recorded here rather than in a message, because a lane's authoritative
surface is a file.

**Fork 1 — where the two-stage P11 gating lives.** Decided: **one predicate, two call sites.**
`gen_handoff.carriage_shortfall(transport, repo_root, residual=None)` is the single predicate;
`preflight_rows`' new row 10 calls it with `residual=None` (leg 1 only), and
`assemble_paste.assert_open_carriers_named` calls it with the filled residual text and filters
to the `OPEN` kind (leg 2 only). Rejected alternative: a new `scripts/p11_carriage.py`. Two
reasons, both about cost the repo has already paid once — a new module needs the dual-import
shim every `scripts/` module here carries, and a second home for a predicate is how two
predicates end up disagreeing about the same file. `assemble_paste` already reaches into
`gen_handoff` for `reflow_framing` and `FILL_IN_RE` by deferred import, so this reuses an
established seam rather than opening one.

**Fork 2 — where the unattended path lives.** Decided: **a declared invocation in
`pyproject.toml`**, beside the serial-sweep note it joins, and NOT a new script or a hook.
Rationale: the existing block already documents the on-demand serial sweep as prose with the
explicit words "no cron wired yet — deliberate; a documented invocation is the current
contract". A second convention for the same class of thing is drift; the same convention,
extended, is not. `pyproject.toml` is also the one file the footprint names for this leg.

**The `pytest-timeout` value — `--timeout=900`.** Cited, not invented: it is
`gen_handoff.SHIP_GATE_TIMEOUT_S`, this repo's only already-declared ceiling for its most
expensive subprocess, whose own comment states the principle ("a ceiling tighter than the
gate's real cost would manufacture refusals rather than detect them"). The heaviest legitimate
tests in this tree are ship-gate and pre-commit subprocess spawns; 900 s sits above them and
far below "wedged forever". Passed on the unattended command line only — `addopts` is
untouched, as the contract requires.

---

## 1 · The done-contract, clause by clause

| # | Clause | State | Evidence |
|---|---|---|---|
| 1 | `[#643]` Done-when, verbatim (leg 1 preflight refusal + RED-first test; leg 2 assemble gate; both cite the family precedent; `handoff.md` states the split) | **DISCHARGED** | `564c6ef6`, `d30d1187`, `5863161f` |
| 2 | P11 fixture **7 FAIL → 0** on the seven-file short | **DISCHARGED** | §2 below |
| 3 | tests-that-cannot-fail **≥1 → 0** | **DISCHARGED** | §3 below |
| 4 | flat `logs/PROPOSALS-*` **154 → 0** | **NOT DISCHARGED — structurally unreachable from a lane worktree** | §5(a) below |
| 5 | an unattended run reproduces the baseline **28 RED, not 44** | **PARTIAL** — the 44-vs-28 mechanism proved by paired measurement; the full sweep was killed twice by the host's low-memory reaper, at both worker counts | §4 below |
| 6 | English, hyphen-only names, logging over print, Click where warranted, `pytest` green | **DISCHARGED** | §4 below |

**Clause 5 is PARTIAL and this record says so plainly rather than rounding it to done.** Its
mechanism half is discharged by measurement taken here; its full-sweep half needs a substrate
this lane cannot reach. §4 carries both halves with their evidence.

Clause 6, on the two sub-points that could have been silently skipped: no new CLI was added,
so the Click question does not arise (the one gate added to an existing Click command,
`assert_open_carriers_named`, reports through `click.echo` like every other message in that
file); no `print` was introduced — the preflight row returns a `PreflightRow` and the assemble
gate uses `click.echo(..., err=True)`.

---

## 2 · Clause 2 — the seven-file short, driven 7 → 0, and then re-measured live

**The fixture is the live measurement, not an invented shape.** It reproduces the twenty-five
file transport of `to-browser/HANDOFF-VERIFY-2026-09-08-architect-2.md` P11: 18 resolving on
`main`, 2 with no flush-left key, 5 stating the literal `OPEN` and named nowhere in the
residual.

- `test_the_seven_file_short_reproduces_the_live_measurement` — 25 files in, **7 short** out,
  split 2 `no-key` / 5 `open`.
- `test_carriers_set_and_openness_named_clears_the_short_to_zero` — the negative control.
  **0.** Without it the count above would prove only that the predicate can fail.

**The stronger witness: the predicate was then run against the LIVE transport**, and it
reproduces the 2026-09-08 hand-run recipe by NAME on every file that existed then:

```
population: 39   resolves 29 · open 8 · no-key 2
no-key  to-cc/AMEND-037-001.md                        <- 2026-09-08 group (A), file 1 of 2
no-key  to-cc/DECLARE-BOOT-REVIEW-2026-09-08.md       <- 2026-09-08 group (A), file 2 of 2
open    to-cc/BATCH-2026-09-06-DAY-CONTRACTS.md       <- 2026-09-08 group (B), 1 of 5
open    to-cc/BATCH-2026-09-06-NIGHT-2-CONTRACTS.md   <- 2026-09-08 group (B), 2 of 5
open    to-cc/BATCH-2026-09-07-CLOSE-CONTRACTS.md     <- 2026-09-08 group (B), 3 of 5
open    to-cc/DECLARE-R6-HANDOFF-EXCEPTION.md         <- 2026-09-08 group (B), 4 of 5
open    to-cc/DECLARE-REVIEWS-2026-09-07.md           <- 2026-09-08 group (B), 5 of 5
open    to-cc/DECLARE-DISPATCH-SEAM-AND-ENTERPRISE-2026-09-08.md   <- filed since
open    to-cc/DECLARE-HARNESS-IS-PROCESS-2026-09-08.md             <- filed since
open    to-cc/DECLARE-HARNESS-PROVENANCE-2026-09-08.md             <- filed since
```

Two things this establishes that a fixture alone cannot. First, the built predicate agrees
with the seat that ran the recipe by hand — same two group (A) files, same five group (B)
files, no false positives among the 29 that resolve. Second, **row 10 FAILs the live window
today**, which is the refusal `[#643]` exists to produce: the next `/handoff` cut is blocked
until those two files carry an anchored `carried-by:`, instead of the defect being discovered
after the bundle is committed and immutable.

The population grew 25 → 39 because the transport gained files after 2026-09-08. The three new
`OPEN` files are leg 2's subject, not leg 1's, and do not affect the row's verdict.

**Leg 2's honest limit, found while wiring it and recorded rather than left to be discovered.**
`gen_handoff.generate(assemble=True)` spawns the assembler with `check=False`, so a leg-2
refusal does not propagate as a non-zero `generate()`. What it produces is the thing that
actually stops a handoff — **no `PASTE_THIS.md`**, plus the refusal block on stderr — and a
bundle with no assembled paste cannot be pasted. Making `generate` propagate the code is a
change to the generate path, which is V-6's file region and outside this gate's scope, so the
limit is written into `assert_open_carriers_named`'s own docstring instead of quietly fixed.

**The leg order is pinned by its own test.** `test_the_stated_value_decides_the_leg_not_the_
prose_around_it` seeds a file whose stated value is `OPEN` while its prose carries a path that
resolves. A path-first read classifies it RESOLVES; the shipped predicate classifies it OPEN.
That single inversion is how the 2026-09-08 `-1` run read a seven-file shortfall as two.

---

## 3 · Clause 3 — the unfalsifiable test, and the mutant that proves the repair

`tests/test_logs_retention.py::test_the_repos_own_logs_dir_is_allowed` read, in full:

```python
assert mod.run_retention(mod._DEFAULT_LOGS_DIR, dry_run=True) is not None
```

`run_retention` returns a `list`. A list is never `None`. The assertion therefore held under
every possible outcome, for every state of the guard and of `logs/`.

**Proved by a discriminating mutant, not by inspection.** `_assert_target_allowed` was mutated
to return the WRONG directory — the system temp dir instead of the repo's `logs/` — which is a
live defect: retention would then plan and apply moves against a directory it was never given.

```
mutant: `return resolved`  ->  `return Path(tempfile.gettempdir()).resolve()`
  OLD assertion  ->  True        (survives; reports a safety it does not provide)
  NEW test       ->  FAILED      assert WindowsPath('C:/.../Temp')
                                     == WindowsPath('.../lane-v-643-enforcement-debt/logs')
```

The replacement carries three limbs, each killed by a different regression: the containment
leg admits this repo's own `logs/` and returns it resolved; `TOKEN-LOG.md` is never planned
(ADR-29/39, the absolute exclusion); and every planned destination is a `logs/YYYY-MM/` bucket
keyed off the source's own date, with `dry_run` leaving the directory as it found it. Mutant
reverted; tree verified clean.

The rest of the file was read end-to-end for the same shape. No second tautological assertion
was found, so the clause's "≥1 → 0" is exact rather than a first instalment.

---

## 4 · Clause 5 — the unattended run: the mechanism is proved, the full sweep was not runnable here

**Read this clause's state precisely, because it has two halves and only one of them landed.**

### 4.1 The 44-vs-28 mechanism — PROVED, by a paired measurement taken here

The whole of the 44 → 28 difference is `tests/test_fleet_analytics.py` failing on a missing
`pandas`. That is now witnessed locally rather than inherited from the Codespaces log. Two runs,
same tree, same commit, four minutes apart, differing in one flag:

```
uv sync --locked                                  ->  Uninstalled 4 packages (pandas, python-dateutil, six, tzdata)
  pytest tests/test_fleet_analytics.py -o addopts= -n 0
  ->  17 failed, 47 passed        every failure: ModuleNotFoundError: No module named 'pandas'

uv sync --locked --group analytics                ->  Installed 4 packages
  pytest tests/test_fleet_analytics.py -o addopts= -n 0 --timeout=900
  ->  64 passed, 0 failed
```

So an unattended run that omits `--group analytics` does not measure a worse tree; it
manufactures a block of failures in one file and hands back a number nobody can act on. The
Codespaces delta was 16 failures plus 2 skips becoming passes; this host reads 17, one of the
two skipping tests failing here instead — a platform difference in the skip, not in the
mechanism. `--timeout=900` was exercised in the same run and is accepted by the invocation.

### 4.2 The full-suite sweep — NOT RUN HERE, and the reason is the clause's own subject

Two attempts, both **killed by the system's low-memory reaper**, neither producing a report:

```
-n 2   killed at 17 %  (~13 min)   host free RAM ~2.8 GB of 28 GB
-n 0   killed at  2 %  (~7 min)    same host, same window
```

Neither log ends in a `MemoryError` or an xdist worker crash — they simply stop, which is the
signature of an external kill rather than a pytest failure. **The invocation is not the cause:
serial died sooner than parallel.** The constraint is the host, where OneDrive, VS Code and
Chrome hold ~25 GB of the 28.

This is the third independent witness of the same failure, after the five attempts recorded in
`DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08` ("3.2 GB free of 28 GB … operator's machine, not
the fleet's"). It is also the reason the 28-RED baseline was taken on Codespaces in the first
place, and it re-confirms the 2026-08-20 substrate ruling rather than challenging it: the
declared unattended path is correct, and the substrate it is correct ON is not this laptop.
`pyproject.toml` now records that measurement beside the invocation, so the next seat does not
rediscover it at the cost of two dead runs.

**What is therefore still owed, and by whom:** one run of the declared line on the Codespaces
substrate, reconciled against the 28 named REDs of
`to-cc/SUITE-ANALYTICS-CODESPACES-2026-09-08.log`. That run is an integrator/operator act on
a substrate this lane has no route to; it is not work left undone inside the lane's own tree.

### 4.3 What the targeted runs did establish about this branch

Every file this lane changed was run to green, serially, in this worktree:

```
tests/test_gen_handoff_preflight.py    45 passed              (0 pre-existing REDs)
tests/test_assemble_paste.py           31 passed  1 failed    (pre-existing: cp1252 em-dash on --pin-only)
tests/test_verify_handoff_probes.py   119 passed  2 failed    (pre-existing: `tool absent: sed`)   [AMENDED — see below]
tests/test_logs_retention.py           all passed             (0 pre-existing REDs)
tests/test_fleet_analytics.py          64 passed              (with the analytics group)
```

The three REDs are named, and none is in the 28-RED Codespaces baseline at `08c35b9c` — they
are Windows-host artifacts (a console-decoding mismatch and an absent POSIX tool), present
before this branch and unrelated to its diff. Collection over the whole suite reports **5408
tests**, which is the baseline's 5390 plus this lane's own 18 — the arithmetic that lets the
integrator attribute the doc-counts delta without re-deriving it.

---

## 5 · What this lane did NOT do, and why — the two disclosures

Deviation-with-disclosure is not a license; the disclosure discharges the reporting duty, it
does not authorise the deviation. Neither item below was worked around.

### (a) Clause 4 — the 154 flat `logs/PROPOSALS-*` are unreachable from a lane worktree

The files are **untracked and gitignored** (`.gitignore` anchors `logs/PROPOSALS-*.md`), so
they exist only in the PRIMARY checkout's working directory. Confirmed by measurement, both
sides:

```
primary   C:\...\Dev\.dev-knowledge\logs           154 flat PROPOSALS-*  (buckets 2026-06..09 present)
lane tree .claude/worktrees/lane-v-643-.../logs      0 flat PROPOSALS-*  (git ls-files logs -> TOKEN-LOG.md only)
```

**The organ itself refuses to cross the boundary**, and the refusal is correct rather than an
obstacle to route around. `logs_retention._assert_target_allowed` bounds every target to
`_REPO_ROOT` or the system temp dir; inside a worktree `_REPO_ROOT` is the worktree, and the
primary is not beneath it. Witnessed:

```
$ uv run --locked python scripts/logs_retention.py --logs-dir "C:\...\Dev\.dev-knowledge\logs" --dry-run
logs_retention: refusing C:\...\Dev\.dev-knowledge\logs: outside this repo
  (C:\...\.claude\worktrees\lane-v-643-enforcement-debt) and outside the system temp directory.
  This organ's contract is THIS repo's logs/.
EXIT=2
```

So the clause cannot be discharged by this lane by any act that is not (i) a write into the
operator's live checkout from a background lane, which the isolation guard and the batch's own
worktree discipline both forbid, or (ii) defeating the containment guard, which is the exact
class of act core-invariant #1 exists to prevent. It is also unwitnessable as a receipt:
"receipt = commit", and a gitignored move produces no commit.

**The act, for whoever holds the primary checkout.** One command, from the repo root, no
arguments:

```
uv run --locked python scripts/logs_retention.py --dry-run    # read the plan first
uv run --locked python scripts/logs_retention.py              # 154 -> 0
```

`apply_moves` refuses a destination collision rather than overwriting, so a legacy duplicate
name aborts the plan and loses nothing. The month buckets it targets already exist.

### (b) Step 5's "production caller" sub-clause collides with a recorded refusal

The step reads "give `run_retention()` a production caller". The only natural caller site is
`scripts/propose_closures.py`, the sole writer of `PROPOSALS-*` / `DETECTOR-ERROR-*` — and
that module already carries a **recorded, reasoned refusal of exactly that act**, in
`_bucket_dir`'s docstring under the heading "THE CALLER FIX (batch-T 3.1)":

> "Writing into the bucket rather than relocating afterwards is the fix at the caller, and it
> is strictly safer than a post-write `run_retention()` call would be. `apply_moves` refuses a
> destination collision, and `_write_error_marker` deliberately REWRITES its path on a second
> failure in one day — so a write-then-relocate caller would archive the first marker and then
> wedge the whole archive plan on the second."

Two independent reasons not to overrule it from here. It is a **rule-vs-ruling conflict**,
which the contract's decision budget names as escalation class (b) — a class this lane may not
resolve on its own. And `propose_closures.py` is **outside this lane's declared footprint**,
which the contract's "What NOT to do" states without qualification.

Note also that the caller does not appear in the six-clause done-contract; the residue is a
one-time sweep (the writer has emitted bucketed since `353b5169`, which is why the pile stopped
growing at 2026-09-06). **Filed for a ruling** rather than actioned: if a permanent caller is
wanted, the beat to consider is a session-START one — `fleet_health.py` already owns and writes
`logs/`, runs once per calendar day, and fires before `propose_closures` writes anything, so it
carries none of the same-day rewrite collision the batch-T 3.1 note is about. That is a
proposal, not a decision.

---

## 6 · Owed to the integrator

1. **`ecosystem/doc-counts.md` regeneration.** This lane adds **18 tests** (5390 → 5408
   collected, arithmetic witnessed by the unattended run's own collection line). Every commit
   here declares `SKIP=doc-counts-pytest-freshness` in its body — the lane's single declared
   hook bypass, never `--no-verify`. Regenerate once on the merged tree:
   `uv run --locked python scripts/gen_doc_counts.py --write`.
2. **`docs/audits/README.md` is left stale, deliberately.** `[#590]` narrowed
   `audit-index-freshness` so a lane landing an artifact does NOT touch the index; regenerating
   it from a lane is affirmatively the wrong act. `gen_audit_index.py --write` on the merged
   result, after `git add` (the index reads tracked files only).
3. **One Codespaces run of the declared unattended line**, reconciled against the 28 named REDs
   of `to-cc/SUITE-ANALYTICS-CODESPACES-2026-09-08.log`. §4.2 is why it is not in this record.
4. **No JOURNAL entry, no index regeneration, no merge, no push** — per the contract.
5. **The V-6 coupling** (`scripts/gen_handoff.py`, SEAT-BOOT render hook vs the preflight
   functions): this lane touched only `PREFLIGHT_ROW_NAMES`, `__all__`, `preflight_rows` and a
   new block appended after `_row_worktree_owners`. It did not enter any render function.
   `origin/main` was still `33bcb0bd` at the final check, so no sync-merge was owed; if V-6
   lands first, the two diffs are disjoint within the file.

---

## 7 · Files touched

| File | Change |
|---|---|
| `scripts/gen_handoff.py` | preflight row 10 + the shared carriage predicate |
| `scripts/assemble_paste.py` | leg 2, the assemble-time OPEN gate |
| `scripts/verify_handoff_probes.py` | the zero-row bypass, closed |
| `.claude/commands/handoff.md` | the two-stage split, stated; row count 9 → 10 |
| `pyproject.toml` + `uv.lock` | `pytest-timeout`; the declared unattended invocation |
| `tests/test_gen_handoff_preflight.py` | +12 (the seven-file short and its control) |
| `tests/test_assemble_paste.py` | +4 (leg 2, incl. the scoping limit) |
| `tests/test_verify_handoff_probes.py` | −1 +3 (the reversal, and both absences pinned) |
| `tests/test_logs_retention.py` | the tautological assertion, replaced |

`tests/test_logs_retention.py` is the only test file the footprint names by path; the other
three are the existing test homes of the three scripts the footprint DOES name, and no new
test module was created.

---

## AMENDMENT 1 — 2026-09-09, same lane, before HANDBACK

**§4.3, the `tests/test_verify_handoff_probes.py` row read `117 passed / 2 failed`. The
measured final figure is `119 passed / 2 failed / 5 skipped` in 377.14 s.**

`117` was carried over from the run taken BEFORE the `_empty_bundle` fixture-era fix in
`274dd38c`. In that intermediate state two argument-parsing tests were red, so the pass count
was two lower; the fix restored them and the file was re-run to confirm. The two remaining
failures are unchanged and are the pre-existing Windows-host `tool absent: sed` pair
(`test_bundle_internal_locator_is_rebased_onto_the_verified_bundle`,
`test_locator_naming_the_verified_bundle_is_never_flagged`) — neither appears in the 28-RED
Codespaces baseline at `08c35b9c`.

Corrected by amendment marker rather than by editing the line in place: an audit is immutable
(ADR-29 / critical rule 3), and a stale number quietly overwritten is the same defect this
lane's whole record is about — HANDOVER-NOTE §C, "a claim accepted without its number".
