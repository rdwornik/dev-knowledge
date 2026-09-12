# Lane `lane-x-734-retire-stage-2` — retire-stage evidence log (second attempt)

> Working evidence artifact for `LANE-x-734-retire-stage-2.md`, the SECOND run of the
> AX13-2/AX13-3 retire stage (`[#734]`). The first run's record is
> `docs/audits/2026-09-11-technical-lane-x-734-retire-evidence.md` (on `main` at `f1711e3d`);
> this contract was rewritten from it. Appended to across the lane's steps; the final section
> is the end-of-lane artifact. Tool output is recorded verbatim, never narrated.
>
> Governance consumers: `[#734]` (the owning row), `[#267]` (live reader of
> `deploy/lived_sandbox/arc.py`), `ADR-106` §5, `ADR-109`, `ADR-110`, `ADR-89` (the oracle's
> honest limit), `intake #86` (the census fixture).

## Step 1 — preconditions, and the re-execution of the reverse-dep oracle

### Precondition 1: the pinned langserver was vendored

`npm install` — `added 1 package, and audited 2 packages`;
`node_modules/pyright/langserver.index.js` present afterwards. `package.json`'s sole declared
dependency is `pyright@1.1.410` and `package-lock.json` is committed, so this restores a
**declared, pinned, checked-in** dependency (the same class of act as `uv sync --locked`).
The working tree was clean immediately after the install — `node_modules/` stays gitignored and
out of this lane's commits, verified rather than assumed.

### Precondition 2: the oracle ran at its DEFAULT per-symbol timeout

No `--timeout` was passed. The first run's `--timeout 300` is a per-QUERY timeout, not a total
budget, and cost it ~20 minutes of zero output before it was killed.

### Run 1 — the eight-module set exactly as the contract's Step 1 words it

`uv run --locked python scripts/safe_remove.py <the eight modules>`, verbatim:

```
safe-removal verdict: UNSAFE
removal set: scripts/boundary_headers.py, scripts/boundary_report.py, scripts/cloud_provisioning.py, scripts/desired_state_loader.py, scripts/desired_state_report.py, scripts/probe_child_backlogs.py, scripts/seed_runbook.py, scripts/validate_onboarding_rulings.py
reason: 12 surviving referrer(s) would dangle on removal (completeness: complete)

surviving referrers (would dangle on removal):
- tests/test_desired_state_loader.py:186 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_loader.py:383 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:67 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:92 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:113 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:126 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:159 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:172 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:181 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_report.py:260 -> load_fleet_model (scripts/desired_state_loader.py)
- tests/test_desired_state_loader.py:228 -> resolve_fleet_members (scripts/desired_state_loader.py)
- tests/test_desired_state_loader.py:389 -> resolve_fleet_members (scripts/desired_state_loader.py)

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

**The contract's Step 1 premise — "confirm the SAFE verdict still holds" — does NOT hold as
worded.** That is recorded first, before any reading of it, because the re-execution was the
point of the step.

### Why this is not the tree having changed

A history query for the three implicated files over the range `f1711e3d..HEAD`
(`tests/test_desired_state_loader.py`, `tests/test_desired_state_report.py`,
`scripts/desired_state_loader.py`) returns **empty**: they are byte-unchanged since the tree
the first run measured. The divergence is therefore in the **oracle run**, not in the tree.
**This lane could not determine what made the first run report SAFE on an identical tree, and
marks the evidence as stopping here** rather than reconstructing a cause it cannot witness.

### What the 12 referrers actually are, and the tool's own escape

All 12 are in `tests/test_desired_state_loader.py` and `tests/test_desired_state_report.py` —
the **dedicated tests of two of the removal targets**. `safe_remove.py`'s own module docstring
rules this case explicitly:

> Test-only importers ARE real referrers (removing the module breaks the test) -> blocking on
> them is correct; **co-removing the test is the escape.**

And `evaluate_removal`'s contract (`scripts/safe_remove.py:183`): *"a referrer SURVIVES iff its
file is NOT itself in the removal set."*

The Done-contract's clause 1 defines this lane's unit of removal as **module + dedicated test +
`graph_queries.py` Disposition entry + `test_graph_spine.py` `CENSUS_SCRIPT_ORPHANS` entry** —
the test is part of the removal unit, not a survivor of it. Run 1 asked a narrower question
than the contract's own removal unit: it held the dedicated tests fixed while removing their
modules. Run 2 asks the contract's question, and is recorded below.

**Run 2 was still executing when this section was committed.** It is recorded verbatim below
before Step 3 acts on the `desired_state_*` pair. Step 2 does not wait on it and does not need
to: run 1 already reports **zero** surviving referrers for all six of clause 1's targets, and
adding files to a removal set can only REMOVE survivors from the result, never add them
(`evaluate_removal`: a referrer survives *iff its file is not itself in the removal set*). Run
2's verdict can therefore change the disposition of the `desired_state_*` pair, and cannot
change the six.

**This is resolution IN-contract, not a deviation:** the frozen Done-contract clause defines the
removal unit; the Steps skeleton's "eight-module set" phrasing is the looser statement of it.
No decision-budget class is spent.

### Why six of the eight produced ZERO surviving referrers

Not because they have no tests — all six have dedicated tests. Because of the oracle's declared
static-only limit, and the two test-import styles in this repo differ exactly where it bites:

- `tests/test_desired_state_loader.py:32` does `from scripts import desired_state_loader`, then
  `_loader().load_fleet_model(...)`. Pyright resolves the package import and the attribute, so
  the oracle SEES the referrer.
- `tests/test_cloud_provisioning.py` does `sys.path.insert(0, .../"scripts")` then
  `import cloud_provisioning as cp`. Pyright cannot follow a runtime `sys.path` mutation, so
  those referrers are INVISIBLE to the oracle.

So the six targets' clean result is a **limit-bounded pass, not proof of no test coupling** —
exactly the false-PASS class ADR-89 declares and `safe_remove.py` restates. It is recorded as
such here rather than reported as a clean bill. The coupling is handled the same way either
way: clause 1 co-removes each module's dedicated test.

### Run 2 — INVALIDATED BY THIS LANE'S OWN CONCURRENCY, and recorded rather than quietly re-run

Removal set = the eight modules + the two coupled `desired_state_*` tests. Verbatim:

```
safe-removal verdict: UNVERIFIABLE
removal set: scripts/boundary_headers.py, scripts/boundary_report.py, scripts/cloud_provisioning.py, scripts/desired_state_loader.py, scripts/desired_state_report.py, scripts/probe_child_backlogs.py, scripts/seed_runbook.py, scripts/validate_onboarding_rulings.py, tests/test_desired_state_loader.py, tests/test_desired_state_report.py
reason: 2 symbol(s)/module(s) the oracle could not verify (WARN + allow; honest-limit)

unverifiable (WARN + allow):
- scripts/seed_runbook.py: module not present in query root
- scripts/validate_onboarding_rulings.py: module not present in query root

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

**The cause is this lane, not the tree.** The CLI path queries the LIVE repo, and Step 2's
deletions landed in the working tree WHILE this run was still reading it — so two modules
vanished from the query root mid-run. That is a measurement artifact of running a live-tree
oracle concurrently with a deletion, and it is recorded as one.

**It is NOT read as a pass, even though it reports zero surviving referrers.** The contract's
own clause binds here: *"An inconclusive tool result is not a pass. A silent or `UNVERIFIABLE`
verdict means KEEP, with the reason recorded."* An `UNVERIFIABLE` obtained by deleting the
subject mid-query is the weakest possible evidence, and the zero-referrer line is a
consequence of the gap rather than a finding against it.

What it does show, and all it shows: the 12 referrers of run 1 are absent once the two coupled
tests are inside the removal set — the direction run 1 predicted. Run 3 measures it cleanly.

**Operational lesson, recorded for the next lane:** `safe_remove.py`'s CLI reads the live tree,
so it must not run concurrently with the deletions it is adjudicating. Sequence the oracle and
the `git rm`, or the verdict measures the race instead of the question.

### Run 3 — the clean measurement of the one open question

The six clause-1 targets are settled by run 1 (zero surviving referrers each, completeness
`complete`). The only question run 2 was asked and could not answer cleanly is the
`desired_state_*` pair. Run 3 puts exactly that removal unit to the oracle, on a tree that is
stable for the duration — all four of its files are present and untouched:

`scripts/safe_remove.py scripts/desired_state_loader.py scripts/desired_state_report.py
tests/test_desired_state_loader.py tests/test_desired_state_report.py`

Its verdict is recorded in Step 3 below, and Step 3 does not act before it lands.

## Step 2 — the six clause-1 targets deleted, with all four coupled surfaces each

### What was deleted

Each target moved with its module, its dedicated test, its `graph_queries.py`
`ORPHAN_DISPOSITIONS` entry and its `tests/test_graph_spine.py` `CENSUS_SCRIPT_ORPHANS` entry —
clause 1's four coupled surfaces, none left behind:

- `scripts/boundary_headers.py` + `tests/test_boundary_headers.py`
- `scripts/boundary_report.py` + `tests/test_boundary_report.py` (the coupled pair, moved together)
- `scripts/cloud_provisioning.py` + `tests/test_cloud_provisioning.py`
- `scripts/seed_runbook.py` + `tests/test_seed_runbook.py`
- `scripts/validate_onboarding_rulings.py` + `tests/test_onboarding_rulings.py`
- `scripts/probe_child_backlogs.py` + `tests/test_probe_child_backlogs.py`

**12 files, 5,180 lines.**

### The test pairing was RESOLVED, not guessed

`tests/test_onboarding_rulings.py` does not carry its module's name, so a name-pattern sweep
would have missed it and left an orphaned test importing a deleted module. The pairing came
from the organ rather than from a guess:

```
uv run --locked python scripts/impacted_tests.py select --changed <the six modules>
tests/test_boundary_headers.py tests/test_boundary_report.py tests/test_cloud_provisioning.py tests/test_onboarding_rulings.py tests/test_probe_child_backlogs.py tests/test_seed_runbook.py
```

Six modules, six tests, one-to-one.

### Targeted tests: 34 passed, 1 failed — and the failure is NOT this lane's

`uv run --locked pytest tests/test_graph_spine.py -q -n 0` → **1 failed, 34 passed**.

The failure is `test_a_disposition_register_entry_cannot_manufacture_its_own_trigger`, and its
subject is **`scripts/worktree_seed.py`** — a file this lane does not touch, delete, or
disposition.

**Attributed by a PAIRED BASELINE/TIP RUN rather than by argument.** The lane diff was set
aside (tagged stash, applied back by SHA, dropped by verified SHA) and the same single test run
against the untouched base:

```
FAILED tests/test_graph_spine.py::test_a_disposition_register_entry_cannot_manufacture_its_own_trigger
AssertionError: dispositioned processes reported as triggered -- the register is laundering its own subject: ['scripts/worktree_seed.py']
1 failed in 19.90s
```

Identical failure, identical single item, on the base tree. **Pre-existing RED, inherited by
this lane, not caused by it.**

Its cause, from the graph rather than from inspection
(`file_purpose_graph.py why scripts/worktree_seed.py`): the file has **two live consumers** —
`is triggered by file:.claude/settings.json` and `is imported by file:scripts/gen_lane_contract.py`
— so it is genuinely triggered and its `ORPHAN_DISPOSITIONS` entry is stale. The register is
recording "this has no trigger" about a file that acquired one. **Open item for the integrator:
`scripts/worktree_seed.py`'s disposition entry should be removed (it was wired, which is the
good outcome the register's own comment describes).** Out of this lane's footprint, so it is
flagged and not fixed.

### One consequence recorded rather than left to be discovered

Deleting `scripts/validate_onboarding_rulings.py` and its test removes the only machine-check
of `ecosystem/satellite-onboarding-rulings.yaml`, which **stays in the tree**. That register's
schema teeth and its "four operator rulings encoded exactly" assertion went with the test. The
deletion is GO'd and is executed; the consequence is named here so it is a known cost rather
than a later surprise.

## Step 3 — the `desired_state_*` pair, and the block the first run could not clear

### Run 3, verbatim — the clean measurement

Removal set = exactly the contract's removal unit for this pair. Tree stable throughout (all
four files present and untouched; the Step 2 deletions had already landed, so nothing moved
underneath it):

```
safe-removal verdict: SAFE
removal set: scripts/desired_state_loader.py, scripts/desired_state_report.py, tests/test_desired_state_loader.py, tests/test_desired_state_report.py
reason: no surviving referrers; every removed symbol resolved clean

limit: static-Python-only (dynamic/getattr/string-keyed/cross-language edges are INVISIBLE -> a non-blocking false PASS is possible; never a false FAIL).
```

**SAFE, with the explicit "no surviving referrers; every removed symbol resolved clean" the
Done-contract asks for** — and it is the contract's removal unit that produces it, which is the
whole content of run 1's UNSAFE. The three runs tell one story: the pair is safe to remove
*with* its tests and unsafe to remove *without* them, which is what clause 1 already said.

### The ARCHITECTURE.md edit (clause 2's footprint extension)

The first run reversed this deletion because `test_the_live_tree_carries_no_dangling_process_
reference` went RED on `ARCHITECTURE.md:503-504`, and fixing it was outside that lane's
footprint. Clause 2 puts it inside this one's.

**The line numbers were RESOLVED before editing, as clause 2 requires.** `503-504` still
resolve exactly: line 503 opens `scripts/desired_state_loader.py` and line 504 carries
`scripts/desired_state_report.py`. The file had not moved for this passage.

**Why only that passage.** The refusal predicate is `graph_queries._PROSE_PROCESS_RE` =
`(?:scripts|plugins)/[A-Za-z0-9_./-]+\.(?:py|ps1)`, applied to `ARCHITECTURE.md` alone
(`PROSE_SURFACE`). It matches **path-shaped** references only. The retired modules from Step 2
also appear in `ARCHITECTURE.md` — lines 479-480 — but as bare backticked names
(`` `boundary_headers.py` ``), which the regex does not match; that is why Step 2's six
deletions did not RED this gate and this pair's did. Recorded because the asymmetry is not
obvious and a future lane will meet it.

Two edits, both inside "the `desired_state_*` prose":

1. The **organ-class paragraph** now states what is true: one part live, two retired, with the
   date, the owning row, the oracle verdict and a pointer to this artifact.
2. The **ADR-109 §9 codemap-scope paragraph** named "the loader→schema edge" as a cost
   accepted. That edge no longer exists. The sentence is corrected rather than left to become
   the next lane's stale locator — the same defect class this lane is cleaning.

**ADR-109 is NOT repealed, and the prose says so explicitly.** The decision described a
three-part class; the typed contract stands, the reading half is gone, and rebuilding it would
be a new act needing its own row. An ADR partially unimplemented is recorded as partially
unimplemented — saying "partial when it is partial" is the standing rule, and quietly rewriting
the passage as though ADR-109 had always described one part would have been the dishonest
alternative. **Flagged for the architect:** ADR-109's own text still describes the three-part
class and now over-describes the tree.

### Verification

`uv run --locked pytest tests/test_graph_spine.py -q -n 0` → **34 passed, 1 failed** — the
same pre-existing `scripts/worktree_seed.py` failure attributed to the base in Step 2, and
nothing else.

The three deletion-sensitive tests, run by name:

```
tests/test_graph_spine.py::test_the_live_tree_carries_no_dangling_process_reference
tests/test_graph_spine.py::test_the_disposition_register_names_no_file_that_is_gone
tests/test_graph_spine.py::test_the_live_orphan_census_reaches_zero_against_its_stated_class
3 passed in 2.40s
```

**`test_the_live_tree_carries_no_dangling_process_reference` is GREEN** — the gate that
reversed the first run's deletion is satisfied, not bypassed. Clause 2 is delivered: the pair
is deleted, all four coupled surfaces each, **4 files, 1,219 lines**.

## Step 4 — the three stale claims retracted; the tombstone BLOCKED by a different, real tooth

### The contract's finding is CONFIRMED: release_lint does not block a tombstone

The contract's central claim — that the first run's stated blocker was stale prose rather than
a live constraint — is **correct, and was measured rather than argued**. This lane wrote the
`/override` tombstone into `deploy/manifest-v1.5.0.yaml` and ran the release lint against it:

```
release-lint ok   C6-components: 25 components valid; all 6 implemented carriers covered
release-lint: 0 FAIL, 1 WARN, 7 pass
```

**C6 accepts the tombstone.** `ALLOWED_STATUSES = {"active", "removed"}`
(`deploy/release_lint.py:101`); the unlock commit `1fbdf6f3` is an ancestor of `f1711e3d`
(verified with `git merge-base --is-ancestor`), so tombstones were already legal when the first
run decided they were not; the manifest's own field table records `removed` as *"legal as of
v1.2.0 (P2)"*; and `ruff-gate` sits in the same file as a live `status: removed` entry.

### But the tombstone still does not land — and the real blocker is a LIVE TOOTH, not prose

With the same entry in place:

```
FAILED tests/test_override_command_removed.py::test_override_command_stays_removed
AssertionError: /override is back, in whole or in part — manifest node present: manifest-v1.5.0.yaml id=override-command.
```

`tests/test_override_command_removed.py` ([#683] regression tooth) refuses **any** component
whose `id` is `override-command`, **whatever its status**:

```python
if any(c.get("id") == _COMPONENT_ID for c in components):
    violations.append(f"manifest node present: {manifest_path.name} id={_COMPONENT_ID}")
```

Note which leg fired: **only the bare-id predicate**. The tombstone carried no `artifacts:`, so
the test's `artifacts[].path` leg ("manifest still ships …") passed, and the payload leg passed
because the payload is genuinely gone. The single thing the tooth objects to is the existence
of the lifecycle record.

### This is a genuine rule-vs-ruling conflict — ESCALATED, not resolved in-lane

Two live governance surfaces contradict each other for this exact component:

- `deploy/manifest-v1.5.0.yaml`'s own field table: a removed component's *"manifest entry is
  **retained as a tombstone**; the remove leg prunes its artifacts from the consumer."*
- `tests/test_override_command_removed.py`: no node with that id may exist, at any status.

AX13-3 asks for the retroactive tombstone; `[#683]` forbids the node. **Both cannot be
satisfied.** That is decision-budget class **(b)**, an explicit escalation class, and it is
**not** a re-escalation of anything this contract settled: the contract settled that
*release_lint C6* does not block (true, and confirmed above). The blocker this lane found is a
different surface the contract did not know about.

**The tombstone entry was REVERTED rather than landed, and the tooth was left un-weakened.** A
lane does not quietly relax a regression tooth to satisfy its own deliverable — that is the
same move, in the opposite direction, as the first run believing stale prose.

**The one-line resolution, for the operator/architect to rule on:** scope the id predicate to
`status: active` components. The test's stated intent — *"Node and payload are ONE act"*, aimed
at a node that ships a working-looking escape hatch — is already carried by its other two legs,
and a tombstone with no `artifacts:` trips neither. If the operator rules the other way, AX13-3's
"tombstone `/override`" clause should be struck as unsatisfiable rather than left open.

### What DID land: the three retractions (clause 3's documentation half)

All three stale claims are retracted in place, each replaced with the accurate constraint and
each naming the measurement above rather than asserting it:

1. **`deploy/release_lint.py` module docstring** — the "only `status: active` is legal this
   release" paragraph. Replaced with an explicit RETRACTION recording that it had been false
   since `1fbdf6f3`, that a lane believed it over the constant four lines below it, and that the
   live rule is the constant.
2. **`deploy/manifest-v1.5.0.yaml` `enforcement-mesh` description** — the vestigial `.gitignore`
   block was justified by "this release ships no `status: removed` tombstone". Replaced with the
   real reason: the mesh carrier has no prune leg for a `.gitignore` region — **a carrier gap,
   not a lifecycle prohibition**. The distinction matters because the false version implied the
   block would clear itself when P2 arrived; it will not.
3. **The `override-command` comment block** (written by `5e17ecd7`, the removal commit itself) —
   now carries the retraction, both gate results verbatim, the conflict, and the proposed
   one-line resolution.

**This is the finding the contract said is worth more than the tombstone, and it is now
stronger than the contract expected:** the prose had been outgrown by the code *and* the act
the prose was blocking is blocked anyway, by a surface nobody had checked. Two lanes in a row
consulted a stale sentence and neither consulted the executable rule beside it.

### Verification

- `deploy/release_lint.py --version 1.5.0` → **0 FAIL, 1 WARN (C2, expected pre-release),
  7 pass** — identical to the pre-Step-4 baseline, which is the Done-contract's requirement.
- `pytest tests/test_override_command_removed.py tests/test_release_lint.py` → **43 passed**.
  The tooth is green because the tombstone was reverted, not because it was loosened.

### Addendum — the A2 freshness gate forced an end-to-end re-read, and the re-read found more drift

Step 3's `ARCHITECTURE.md` edit made its `last_reviewed: 2026-09-10` stamp stale, and
`canonical_freshness` is **commit-based**: it passed at Step 3's own commit and FAILed the
**next** one (`audit.py health` → `canonical_freshness: ARCHITECTURE.md: last_reviewed
2026-09-10 predates last edit 2026-09-12`), blocking Step 4.

The predicate is `reviewed < git_date` (`scripts/canonical_freshness_gate.py:185`), so a
same-day stamp satisfies it. **The stamp was not simply moved.** This repo's convention is
that `last_reviewed` means *re-read end-to-end and confirmed accurate, or drift filed*, and
every prior stamp on this file states "re-read the file end-to-end from disk". So the file was
read end-to-end — all 1,306 lines — before the stamp moved. Neither `--no-verify` nor a
stamp-without-a-read was taken; both would have converted a real gate into a formality.

**The re-read found drift this lane's contract did not send it to fix, and it was this lane's
own deletions that caused it.** `ARCHITECTURE.md` Ch2's organ table carried rows for
`boundary_report.py` and `boundary_headers.py` — **both deleted in Step 2** — still marked
**ARMED (manual)**. The map was asserting that two non-existent scripts were live organs.

Both rows are now **RETIRED**, which is a status this chapter's own legend already defines
(*"RETIRED = removed, kept only as a record"*), so no new vocabulary was invented.

**And the `boundary_headers` row records a consequence rather than only a fact:** the #312
Form-A boundary markers in `CLAUDE.md` remain the source of truth, but nothing now regenerates
or `--check`s the reader-visible headers derived from them — **those headers can now drift
silently** — and open ticket **#369** (that generator's pre-commit wiring) is **moot and needs
dispositioning**. Flagged for the integrator; dispositioning another row is not this lane's
act.

### The blind spot this exposes, which is the more portable finding

**No gate caught those two false ARMED rows.** `test_the_live_tree_carries_no_dangling_process_
reference` stayed green across both Step 2 and Step 3, because
`graph_queries._PROSE_PROCESS_RE` matches **path-shaped** references only:

```python
_PROSE_PROCESS_RE = re.compile(r"(?:scripts|plugins)/[A-Za-z0-9_./-]+\.(?:py|ps1)")
```

Ch2's organ rows name their organs as **bare backticked filenames** (`` `boundary_headers.py` ``),
which that regex does not match. So the repo's one defence against "prose naming a process the
graph lacks" is blind to the single table most likely to name one — the organ map.

This is the same shape as the `/override` finding in this step and the `desired_state` finding
in Step 3: **a surface that reads as authoritative, is not checked, and had been outgrown.**
Three instances in one lane. Recorded here, and in the `ARCHITECTURE.md` stamp itself, because
the next deletion lane will meet it.

**Open item for the integrator/architect:** widen the dangling-reference predicate to catch a
bare `<name>.py` inside the Ch2 organ table, or accept the gap explicitly. This lane does not
widen a live refusal predicate on its own motion — that is a mechanism change, not a cleanup.

### Verification after the re-stamp

`uv run --locked python scripts/audit.py health` → **`health: OK`** (the
`canonical_freshness` FAIL cleared; no new FAIL introduced).

## Step 5 — `deploy/lived_sandbox/` dispositioned FILE BY FILE

Clause 4 asked for a per-file disposition the first run was not scoped to make, and expected
most of it to land as *KEPT-as-inconclusive*, since seven of the eight return FPG-1 `REFUSED`.

**The per-file work changes that answer. Seven of the eight are KEPT on POSITIVE evidence, not
on inconclusiveness** — and the eighth (`__init__.py`) on a structural necessity. `REFUSED`
here turns out to mean *FPG-1's governed inputs do not reach this file*, not *nothing reads
this file*.

### The FPG-1 re-run, verbatim (today's tree, not inherited)

Re-executed per file. `arc.py`:

```
path     : deploy/lived_sandbox/arc.py
purpose  : Lived-workflow sandbox — the GATED-MESH ARC driver + GATE-0 (Slice B; [#252]).

consumers (1) -- what reads this
  - is implemented by    task:267                                             [task-implements]
```

The other seven, each identically:

```
REFUSED: deploy/lived_sandbox/<name>.py: nothing explains this file. It is on disk and no governed input (doc-code-edge registry, audits index, consumer-at-landing citation, tasks/ depends-on, deploy manifest) names it. A file nothing explains is a defect, not a mystery.
```

Reproduced exactly against the first run. `[#267]` re-verified live: `status: open`, and its
`refs` line names `deploy/lived_sandbox/arc.py (ARC_PROMPT)`.

### Three readers FPG-1's governed-input set cannot see

1. **Intra-package imports.** Read off the modules themselves:

```
arc.py       -> observe, oracle, spawn
cli.py       -> arc, isolation, spawn   (+ consumer, DEFERRED at cli.py:142)
consumer.py  -> arc, observe, oracle, spawn
isolation.py -> spawn
observe.py   -> oracle
oracle.py    -> (none)
spawn.py     -> (none)
```

2. **Tests.** Three modules import all eight: `tests/test_lived_sandbox.py` (isolation, spawn),
   `tests/test_lived_sandbox_consumer.py` (arc, cli, consumer, observe, oracle, spawn),
   `tests/test_lived_sandbox_observer.py` (arc, oracle). `pytest --collect-only` over the three:
   **117 tests collected**.

3. **`ARCHITECTURE.md:1007`** carries a dedicated row for the directory in the
   *Execution substrates* table, describing it as *"the only organ that measures whether the
   carried methodology actually **engages** in a consumer-shaped session, rather than whether it
   is **present**"*, citing the Fable architecture review 2026-07-04 §6 and `[#252]`.

### Per-file disposition

- **`arc.py` — KEEP. LIVE READER.** Open row `[#267]` names it directly as `ARC_PROMPT`. The
  contract's own clause-4 ruling, re-verified rather than carried.
- **`observe.py` — KEEP. LIVE BY INHERITANCE.** Imported by `arc.py:30`, which is the confirmed
  live file. Deleting it breaks the one member nobody disputes.
- **`oracle.py` — KEEP. LIVE BY INHERITANCE.** Imported by `arc.py:31` and by `observe.py:28`.
- **`spawn.py` — KEEP. LIVE BY INHERITANCE.** Imported by `arc.py:32`, `cli.py:31`,
  `isolation.py:17` and `consumer.py:29` — the most-depended-on file in the package.
- **`cli.py` — KEEP. THE PACKAGE ENTRYPOINT.** `python -m lived_sandbox.cli observe-arc` is the
  documented invocation (its own docstring; `docs/audits/2026-07-05-ai-council-measurement-2.md`
  records a real run through it). It imports `arc.py`.
- **`consumer.py` — KEEP. REACHED BY A DEFERRED IMPORT.** `cli.py:142` does
  `from . import consumer as _consumer` **inside** `cmd_observe_consumer`, so no module-level
  scan sees the edge. This is precisely the invisible-edge class ADR-89 declares for the static
  oracle, met here in FPG-1's import input instead.
- **`isolation.py` — KEEP.** Imported by `cli.py:30`; carries the Slice A isolation proof
  (`docs/audits/2026-07-04-codex-lived-sandbox-slice-a.md` audits it by name).
- **`__init__.py` — KEEP. STRUCTURALLY REQUIRED.** Every `from . import X` above resolves
  through it. Deleting it breaks the package outright. Its `REFUSED` verdict is the clearest
  demonstration that `REFUSED` is not a deadness signal: no governed input names a package
  marker, and none ever will.

**Verdict: all 8 KEPT. ZERO deletions from `deploy/lived_sandbox/`** — which is also what the
contract's "do not delete any file on a `REFUSED` verdict" bound requires, reached here by
positive evidence rather than by the bound alone.

### The finding this step actually produces

**`REFUSED` from FPG-1 `why` is not evidence of deadness, and this directory is the clean
demonstration.** Eight files, all `REFUSED` except one — and on inspection the package is a
documented organ with 117 tests, an entrypoint, an open backlog row, and a dense internal
import graph. FPG-1's governed inputs (doc-code-edge registry, audits index,
consumer-at-landing citation, `tasks/` depends-on, deploy manifest) simply do not include
**Python imports** or **test coverage** for a `deploy/` path.

Its refusal text — *"A file nothing explains is a defect, not a mystery"* — reads as a verdict
about the FILE when it is a verdict about the REGISTRY's reach. On this corpus it produced a
**7-of-8 false-positive rate**.

**Open item for the architect (ADR-118's live subject, so it lands in the right lap):** either
teach FPG-1's `why` to consider import and test edges for non-`scripts/` paths — it already
holds `imports` as an edge kind for the `scripts/` corpus — or narrow the refusal's wording so
it claims what it can support: *no governed input names this file*, not *nothing explains* it.
This lane does not change a refusal's semantics on its own motion.

**Recorded against clause 4's expectation, honestly:** the contract predicted this step would
record seven KEEPS as inconclusive. It instead records seven KEEPS as **positively live**. That
is a better outcome for the tree and a worse one for the census, whose `GARBAGE-CANDIDATE`
framing of this directory rested on the same blind spot.
