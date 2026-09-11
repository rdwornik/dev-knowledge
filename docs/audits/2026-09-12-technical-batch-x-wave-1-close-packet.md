# Batch X wave 1 - close packet (integration half) - 2026-09-12

**Seat:** integrator - **Batch:** X, wave 1 - **Base:** `main` = `0be08b3c` at wave start
**Lanes handed back:** 6 - **Merged:** 5 - **Refused:** 1

> **The refusal is the headline.** `lane-x-734-retire-stage` was REFUSED, not merged. Its six
> deletions break two live executable references that the lane's own oracle, its own targeted
> tests, and this seat's first verification pass all missed. Section 3 is that finding in full.

---

## 1 - Per-lane result

| lane | row(s) | merged SHA | review tally | targeted suite | verdict |
|---|---|---|---|---|---|
| W-2' `lane-w-684-pretooluse-guard-root` | `[#684]` | `3a8ee7a8` | HIGH:1 MED:0 LOW:0 | 312 passed / 320.5s | MERGE |
| lane-5 `lane-x-716-dispatch-defects` | `[#716]` `[#717]` `[#718]` | `eccb5814` | HIGH:1 MED:0 LOW:0 | 184 passed / 37.6s | MERGE |
| X1-1 `lane-x-692-decision-coverage` | `[#692]` | `a77e3302` | HIGH:1 MED:0 LOW:0 | 100 passed / 269.4s | MERGE |
| X1-2 `lane-x-689-conductor-e` | `[#689]` | `6463ca9c` | HIGH:2 MED:0 LOW:0 | 94 passed / 10.9s | MERGE (1 conflict) |
| X-DEL `lane-x-734-retire-stage` | `[#734]` | -- | HIGH:2 MED:4 LOW:0 | -- | **REFUSE** |
| X1-5 `lane-x-664-delivery-spine` | `[#664]` `[#727]` | `11c7c8b1` | HIGH:1 MED:1 LOW:0 | 116 passed / 39.8s | MERGE (1 conflict) |

Reviewer: `gpt-5.6-codex` (codex-cli 0.153.4), one fresh review per lane against
`main...<lane>`, code files only. Every tally is recorded **unmodified**; where this seat graded
a finding differently, the grade and its evidence are in the merge commit body and in section 4.
**The tally is not the verdict** -- `audit.py handback` returned `MERGE` on x-734's HIGH:2 MED:4,
which is D-1 working as designed: the gate asserts a review RAN and is NAMED; severity triage is
the integrator's act.

**Suite:** 5752 collected at wave start, **6061** after the five merges (**+309**).
**Ship gate:** RED at wave start and RED at wave end on the **same single hard-fail**, which
this wave neither caused nor repaired; undispositioned WARNs 66 to 78 -- section 5.
**Full suite on the merged tree: 38 failed, 6019 passed, 4 skipped in 52:05. THIRTY of the 38
already failed before the wave. Eight are new -- section 12.**

---

## 2 - The anchor, paid once instead of six times

`batch_manifest.open_batches()` returns **0**. The batch X manifest carries no `status: open`
and no `closed_by:` -- it opens with a heading and its first `---` is a horizontal rule at line
13 -- and `open_batches` fails toward no-exemption on missing frontmatter. Verified unrepaired
on `main` and on both live dispatcher branches. Separately measured: **0 of 6 lanes wrote a
JOURNAL entry on its own branch.**

Without intervention every one of the six merges lands unanchored and blocks the next commit in
the repo, including the next merge in the queue -- five blocked merges and five repair arcs.

STANDING_RULINGS B2/B6 put the anchor **on the branch ahead of the merge**, because a merge
commit cannot name its own hash. So this seat wrote ONE two-commit arc naming all six lane tips
and merged it first (`1b17a766`). Every subsequent lane merge then landed already anchored:
`health: OK` after each, and both pre-push gates passed on both pushes.

**This is the generalisable lesson of the wave.** Anchoring after the fact is the REPAIR shape.
Anchoring ahead is the law's shape, and at six lanes it is the difference between one arc and
five.

---

## 3 - X-DEL refused: what the oracle, the tests and this seat all missed

`[#734]`'s lane deleted six `scripts/` modules and their six dedicated tests on a
reverse-dependency oracle verdict of **SAFE, no surviving referrers** for every target. The
verdict is wrong for two of them, and both failures are invisible to a green suite.

**Finding 1 -- `.devcontainer/provision.sh` still EXECUTES a deleted module.** Six call sites:

```
349:  uv run --no-sync python scripts/cloud_provisioning.py --quiet history || CHANGED=...
350:  uv run --no-sync python scripts/cloud_provisioning.py history --repair || rc=$?
367:  uv run --no-sync python scripts/cloud_provisioning.py --quiet ecosystem || CHANGED=...
368:  uv run --no-sync python scripts/cloud_provisioning.py ecosystem --repair || rc=$?
585:  uv run --no-sync python scripts/cloud_provisioning.py --quiet history
587:  uv run --no-sync python scripts/cloud_provisioning.py --quiet ecosystem
```

Any devcontainer provision or verification run reaches a missing script.

**Finding 2 -- a live E2E test dynamically loads a deleted module.**
`tests/test_e2e_consumer_lifecycle.py::_load_boundary()` uses
`importlib.util.spec_from_file_location("boundary_report", HUB/"scripts"/"boundary_report.py")`
and is called at the Stage 5/6 assertion. Under `RUN_E2E=1` it fails on a missing file.

**Why nothing caught it, which is the part worth keeping.** Four instruments were pointed at
this question and all four share one blind spot:

1. **The lane's reverse-dep oracle** models Python `import` graphs. `provision.sh` invokes by
   **shell command**; the E2E test loads by **importlib from a path string**. Neither is an
   import edge, so neither is an edge the oracle can see.
2. **The lane's targeted tests** were green because the E2E test is gated behind `RUN_E2E=1`
   and `provision.sh` runs only inside a devcontainer.
3. **The lane deleted `tests/test_cloud_provisioning.py`** -- which contained
   `test_provision_sh_runs_the_history_repair_before_arming_hooks`, the one assertion over
   `provision.sh`'s call list. The module, its wiring test and the breakage all left together.
   `provision.sh`'s own comment at :231 states the residual hazard in as many words: *"deleting
   the call below therefore still leaves the suite green."*
4. **This seat's first verification pass.** It grepped `*.py *.yaml *.yml *.json *.toml *.ps1
   *.cfg` for imports, pre-commit rows, manifest component paths and command-position runs, and
   reported **zero referrers for all six**. It was wrong twice: the glob set excluded `.sh`, and
   an `import`-statement regex cannot see `importlib.util.spec_from_file_location`. The fresh
   review found both. **A verification instrument that reports zero is making a claim about its
   own coverage, not about the tree** -- recorded here because this seat made the mistake it is
   describing.

**This is the batch's recurring defect in its tenth instance and its purest form: a pin that
does not cover the thing that can change.** Every earlier instance was a gate whose scope missed
a mutation. Here it is a *deletion-safety oracle* whose edge model misses the two ways this repo
actually invokes a script.

**Disposition.** `[#734]` is NOT closed and `worktree-lane-x-734-retire-stage` is NOT torn down
-- its commits are the only copy of the work. The repair is one of: (a) keep
`cloud_provisioning.py` and `boundary_report.py` (restoring their tests) and delete only the
four clean targets; or (b) re-scope the GO footprint to cover `provision.sh` and
`test_e2e_consumer_lifecycle.py` so the invocations go in the same act. Both are decisions above
this seat. **The four other targets -- `boundary_headers.py`, `probe_child_backlogs.py`,
`seed_runbook.py`, `validate_onboarding_rulings.py` -- were re-checked including `.sh` and
dynamic-load forms and have no executable referrer.**

---

## 4 - The five merged HIGHs, and how each was graded

Every one was reproduced or resolved against the source before grading. None was graded on the
reviewer's say-so, and none was graded down for convenience.

**W-2' -- fleet_parity.hook_invokes_script certifies a guard that never runs.** CONFIRMED
empirically by this seat: a short-circuit prefix (true OR-OR python ...), a never-taken
conjunction (false AND-AND python ...) and a post-exit segment (exit 0; python ...) each return
True. **Graded MED.** The defect is in a DETECTOR, not the guard; the guard itself is now
fail-closed on every path. The detector's threat model is drift, and a short-circuit prefix is
forgery -- and ADR-28/36 forbid Layer 2 executing what it reads, so a string-reading checker
cannot be sound against forgery. The actionable remainder is narrower than the finding: the
module docstring claims it errs in *"the safe direction to be wrong in"*, and these three cases
err in the unsafe direction. **It overstates its own guarantee.**

**lane-5 -- the generator still emits a Dispatch-Lane fence the verb refuses (F8).** **Does not
land against this diff.** `[#718]` is about WHERE the generator writes (`_default_out_dir()`
returned `Path.cwd()`), not which fence it carries. **F8 is real and remains open, owned by no
row.**

**X1-1 -- decision_coverage.py reads untracked evidence.** CONFIRMED: the file contains **zero**
occurrences of the worktree-skew guard, while `graph_queries.py` applies `_worktree_skew` to the
same class of evidence and its docstring says *"the untracked leg is exactly the hole"*.
**Graded MED** because LEG 2 is armed and refuses on every in-era accepted decision regardless of
what the commit touched, *"because leg 1 alone is satisfiable by never touching the file again"*
-- so the bypass buys one commit on one machine and fails loudly in every other clone and in CI.
Also checked: the hook is `always_run: true` with its own subject computation, so the W-7
self-disarm shape is absent by construction.

**X1-2 -- conductor.py --out can write into a child repo (filed CRITICAL).** **Graded MED.**
The flag defaults to None and the default sink is stdout; `--repo-root` defaults to this repo.
ADR-28/36 forbid a script whose FUNCTION drives child-repo state; by the review reading, every
generator with an out-flag would violate the invariant. Separately verified:
`deploy/conductor-required-checks.ruleset.json` ships enforcement disabled, so it is DECLARED,
not applied, and does not arm the required checks that are mutually exclusive with this repo own
no-ff landing protocol.

**X1-2 -- _archived() passes with a live duplicate body.** **STANDS as HIGH, and it is the
sharpest merged finding of the wave.** Three surfaces disagree:

- `conductor.py:105` docstring -- *"the row body lives under tasks/archive/ **rather than**
  tasks/"*
- `conductor.py:106` code -- globs `tasks/archive/` only; never looks at `tasks/`
- `test_conductor.py` -- `_tree()` writes the LIVE `tasks/10-slug.md`, the test then adds
  `tasks/archive/10-slug.md` and asserts **pass**

A COPY instead of a MOVE certifies as archived, and the fail branch own evidence string
(*"the body is still live in tasks/"*) names the condition the pass path never tests. **The test
does not merely miss the bug -- it defends it**, which is worse than absent coverage because the
fix must now change a green assertion. Merged because the organ is new, is *"declaration-only
until batch X waves close"* per the deploy roster, and nothing consumes its verdict yet.

**X1-5 -- the deny-and-point wrapper fails closed and wedges Bash/PowerShell/Grep.** **Does not
land.** It requires a non-zero exit to read as DENY. A PreToolUse hook refuses on exit code **2**
specifically, and this repo encodes that in two places:
`tests/test_prompts_guard_hook_wiring.py:176` -- *"under AX15-1 the command maps every status
except 0 to 2"* -- and the settings.json note that the existence test exists *"so that a missing
CLAUDE_PROJECT_DIR cannot make python exit 2 -- which a PreToolUse hook reads as DENY"*. AX15-1
had to BUILD that mapping to achieve fail-closed; if any non-zero already refused, the mapping
would have been unnecessary. `deny_and_point.py` returns 0 on every path except its own protocol
denial (lines 661, 663, 668 return 0; line 667 returns 2), so 127 or 1 passes through and
ALLOWS. **The two hooks fail in opposite directions on purpose:** a safety guard that cannot
evaluate must refuse; a routing nudge that cannot evaluate must not wedge the session. The
accompanying MED stands -- the fail-open is *implicit*, resting on the exit-code contract rather
than on a test that executes the wired command with no interpreter.

---

## 5 - Ship gate, and the defect this wave did not cause

Ship gate is **RED at both ends of the wave**, on one hard-fail organ:

```
[!!] funnel_lifecycle: ground truth uncomputable (Z-G4):
     docs/intake/2026-09-11-tech-batch-x-roster.md: frontmatter parsed to {} --
     id and status are both unreadable, so its lifecycle position cannot be computed
```

**This is the same defect as section 2, in a second artifact.** Batch X dispatcher produced two
machine-read surfaces -- the manifest and the intake roster -- and **both** carry frontmatter the
reading organ cannot parse. One costs the batch its ADR-110 exemption; the other is the ship
gate only hard-fail. Neither was introduced by this wave, and neither is this seat to repair:
both are landed `docs/`-immutable artifacts belonging to another seat.

Each merged lane new audit artifact also adds one `funnel_coverage` WARN until dispositioned;
that is the funnel normal intake path, not a regression.

---

## 6 - Evidenced closures, one operator word (AX10-1, per [#730])

`[#730]` standard: **id - Done-when verbatim - merged SHA - the proving test or gate** -- and
the load-bearing clause is the refusal: *a row with NO witness is not listed, rather than listed
with a weaker claim.* Five rows qualify.

**`[#716]`** -- *Done when: a lane base equals main HEAD at dispatch, asserted by a TEST rather
than by the setting value -- so a dispatcher on a non-main branch cannot satisfy it accidentally;
the RED-first witness FAILS against today unset configuration before the fix makes it green; and
the mandatory step-0 sync is retired from the lane-contract template only in the same change that
makes that test green*
- merged `eccb5814` - proven by `tests/test_worktree_seed.py`

**`[#717]`** -- *Done when: the launch line is RENDERED FROM the contract Model row rather than
omitting it, and a test asserts the rendered line model equals that row -- a RED-first witness
that FAILS today against a sonnet contract whose carried line dispatches at opus*
- merged `eccb5814` - proven by `tests/test_gen_lane_contract.py`; independently re-run by this
seat, confirming the checker admits BOTH the new -Model form and the frozen no-Model form, so no
already-frozen contract goes RED (the F1 trap)

**`[#718]`** -- *Done when: the generator writes lane contracts to the location the verb reads,
both resolved from ONE key rather than from two independently-correct literals, and a test
asserts the written path equals the path the verb resolves -- a RED-first witness that FAILS
against today split before the fix makes it green*
- merged `eccb5814` - proven by `tests/test_gen_lane_contract.py`

**`[#727]`** -- *Done when: a PreToolUse hook on Bash and Grep DENIES a raw search (grep, rg,
find, Select-String) over the governed questions AX9-1 enumerates, with exception text naming the
organ to run instead; a RED-first trip-test sends a raw grep and asserts BOTH the denial and the
pointer; ordinary non-governed searching is unaffected, proven by a test that a plain string
search still runs*
- merged `11c7c8b1` - proven by `tests/test_deny_and_point.py` (116 passed) and by the live
wiring verified post-merge: 3 PreToolUse blocks, deny_and_point matcher Bash-PowerShell-Grep,
JSON valid - the lane own audit records *"[#727] is complete against its Done-when, every clause
above is discharged with a witness"*

**`[#692]`** -- *Done when: to-cc/AMEND-SESSION-PLAN-009.md A9-1, A9-2 and A9-3, carried
verbatim* - merged `a77e3302` - proven by `tests/test_decision_coverage.py` and by the
`decision-coverage` pre-commit row, ARMED and passing on every commit in this wave - the four
items its audit owes are follow-on work carried by `[#735]` and `[#736]`, not unmet clauses

### REFUSED from the list, each with the reason

- **`[#734]`** -- its lane is refused; no merge, therefore no witness. Section 3.
- **`[#684]`** -- **witness PARTIAL, blocked externally.** The mechanism legs are closed
  (fail-closed on all paths, matcher narrowed, RED-first tests present) but the Done-when also
  requires *"one non-Claude CLI smoke passes under the guard"*, and the lane measured that the
  honour-set on this machine is cursor-agent alone -- authenticated but usage-limited -- while
  codex and copilot do not read `.claude/settings.json` at all, so a pass from either is vacuous.
  **This needs an operator disposition, not a closure word:** the clause cannot be discharged on
  this machine today.
- **`[#664]`** -- its own lane records *"[#664] stays OPEN and that is conforming"*; the row is
  deliberately split across waves.
- **`[#689]`** -- its Done-when is four outcome numbers that must MOVE (phase transitions without
  operator action, operator hours per feature, pastes per week). A merge cannot witness a metric
  moving, and the lane additionally records precondition P3 as NOT MET.

---

## 7 - Net-row overdraft (AX11-4)

Filed by this wave, both carried by lane filing commits with their own kill-candidates lines:
**`[#735]`** (floor declaration mandatory) and **`[#736]`** (component lifecycle as data), from
X1-1. `tasks/manifest.json` went **588 to 590 nodes** and **no node was removed**, checked
because absence from that manifest IS the closure mechanism.

```
filed this wave         : 2     [#735] [#736]
closed this wave        : 0     closure is the operator act; section 6 proposes 5
net rows, this wave     : +2
net rows, window-to-date: +47   measured at 11c7c8b1
```

The batch W close packet reported the window at **+45** as of `0be08b3c`; this wave adds 2.
**`[#737]` is NOT counted** -- it is filed on `worktree-dispatch-x14-freeze`, which has not
merged, so it is not on the tree and is excluded rather than counted early. If the five closures
in section 6 are granted, the window moves to **+42**.

---

## 8 - Merge minutes: test time vs ceremony

Wall clock 23:06 to 00:30 = **84 minutes** for six verdicts and five merges.

| lane | merged at | targeted test | ceremony | what the ceremony was |
|---|---|---|---|---|
| (anchor arc) | 23:09 | -- | 3 min | writing and merging the six-tip anchor |
| W-2' | 23:38 | 5.3 min | ~24 min | review, empirical reproduction of the HIGH, triage |
| lane-5 | 00:00 | 0.6 min | ~21 min | review, F1 re-run, scope analysis of the HIGH |
| X1-1 | 00:03 | 4.5 min | ~3 min | review pre-run in parallel; manifest-node audit |
| X1-2 | 00:21 | 0.2 min | ~18 min | conflict resolve, **two failed commits**, index regen |
| X1-5 | 00:30 | 0.7 min | ~9 min | conflict resolve in settings.json, JSON verification |
| X-DEL | -- | 0 min | ~12 min | review, two-finding verification, refusal |

```
targeted test time : 11.3 min   (13%)
ceremony           : 72.7 min   (87%)
```

**Where the ceremony actually went**, since ceremony is not one thing:

- **Review and triage, about 40 min.** Irreducible, and the point of the exercise -- it is what
  caught X-DEL and what correctly declined to block on three findings that did not land.
- **Conflicts, about 12 min** across two lanes, caused by non-disjointness (section 9).
- **Index regeneration, about 8 min**, including two commits rejected by organ-index-freshness
  before the cause was read. Reserved to the integrator by each lane no-index-regeneration
  bound, so it is correctly here and not in the lanes -- but it is **unbudgeted in the protocol**.
- **Anchoring, about 3 min**, paid once. Per-merge it would have been about 15 min plus five more
  merge commits.

Running two Codex reviews in parallel with the previous lane merge removed roughly 20 minutes of
serial wait; the 3-minute ceremony on X1-1 is that effect in one row.

---

## 9 - The lanes were NOT file-disjoint

ADR-110 asks a batch for file-disjoint lanes. Wave 1 was not:

| file | lanes touching it |
|---|---|
| `.claude/settings.json` | W-2', lane-5, X1-2, X1-5 |
| `ecosystem/doc-counts.md` | W-2', X1-2, X-DEL |
| `scripts/validate_backlog.py` | X1-1, X1-2 |
| `scripts/graph_queries.py` | X-DEL, X1-5 |
| `scripts/fleet_health.py` | W-2', X1-1 |
| `ecosystem/parity-surfaces.yaml` | W-2', X1-5 |

Two produced real conflicts. **Both resolved by keeping BOTH sides** -- textual collisions at
shared insertion points, not semantic disagreements:

- `validate_backlog.py` -- X1-1 implements-checks and X1-2 phase-enum both appended at the same
  call site. Verified after resolution: validate_backlog OK (9 themes, 26 stories, 313 tasks) and
  the phase census reports build 1, unphased 312. Both features run.
- `.claude/settings.json` -- the conflict was confined to the documentation string, where X1-5
  carried a copy of the prompts-guard paragraph predating AX15-1. HEAD post-AX15-1 text kept;
  the X1-5 deny-and-point paragraph grafted in. Verified: 3 PreToolUse blocks, correct matchers,
  JSON valid.

**The disjointness rule earned its place here.** Both conflicts were cheap because both were
additive; a semantic collision between two PreToolUse hooks in settings.json would not have been.
The rule should be checked at FREEZE, when the lane set is chosen -- a dispatcher can compute the
overlap from the contracts declared surfaces before anything is fired.

---

## 10 - What each lane made work, and what it did not

**W-2' -- MADE WORK:** the prompts guard fails closed on every inability to evaluate and permits
only on a PROVEN pass (rc 0 AND stdout exactly the guard own OK marker), closing the
inferred-permit hole where an exit of 0 from a shim was read as a check that never ran. Each
refusal names its cause and its fix. Matcher narrowed off the match-all form, preserving the
break-glass route. **DID NOT:** the M7 non-Claude smoke -- externally blocked, section 6. And
fleet_parity certifies short-circuited invocations, section 4.

**lane-5 -- MADE WORK:** all three dispatch defects, and cleared the F1 trap that would have
turned every frozen contract RED. **DID NOT:** F8. Generator-emitted contracts remain
categorically unlaunchable by the ruled verb dispatch, because gen_lane_contract check requires a
Dispatch-Lane fence and Invoke-Dispatch.ps1 refuses that exact fence. **No row owns F8.** It
survives on being nobody, which is exactly how a known defect persists.

**X1-1 -- MADE WORK:** decision coverage is armed, two-legged and era-bounded, with the
grandfathered population counted rather than refused; the hook cannot be disarmed by its own
wiring. **DID NOT:** apply the skew guard its sibling query already uses, section 4.

**X1-2 -- MADE WORK:** conductor E exists -- phase gate, Actions runner, phase enum in
validate_backlog, a required-checks ruleset shipped safely disabled. **DID NOT:** _archived()
checks the wrong half of a move and its test defends the gap, section 4. P3 recorded NOT MET.

**X-DEL -- MADE WORK:** the *evidence discipline*, which is the durable part. It refused to
delete four targets it could not clear, named a genuine rule-vs-ruling conflict
(config/requirements-dev.txt: the ADR-106 standing no-delete invariant against the batch bundled
GO) and deferred rather than resolving it by fiat, and reversed one deletion when targeted tests
RED-ded. **DID NOT:** the deletions themselves, section 3.

**X1-5 -- MADE WORK:** deny-and-point is wired, fails open in the correct direction, refuses with
a pointer rather than a bare no, and leaves ordinary search untouched. `[#727]` complete.
**DID NOT:** the `[#664]` spine migration -- deliberately split across waves, conforming.

---

## 11 - Carried out of this wave

**For the dispatcher (blocking future waves):**

1. The batch X **manifest** needs `status: open` and `closed_by:`, or every wave-2 and later
   merge pays the anchor tax again. In-file amendment marker, since it is landed and immutable.
2. `docs/intake/2026-09-11-tech-batch-x-roster.md` frontmatter parses to an empty mapping -- the
   ship gate only hard-fail.
3. Two dispatcher branches are unmerged and were not in this wave queue:
   `worktree-dispatch-x1-freeze` (2 commits -- the X-DEL sonnet re-route and the fire receipts)
   and `worktree-dispatch-x14-freeze` (4 commits -- `[#737]` and the X1-4 freeze).

**For grooming (CANDIDATEs, none filed by this seat):**

4. `fleet_parity.hook_invokes_script` -- refuse certification on short-circuit and post-exit
   segments; correct the docstring safe-direction claim.
5. `decision_coverage` -- apply `_worktree_skew` to implements-edge evidence.
6. `conductor._archived` -- require the live body ABSENCE; change the fixture to model a move.
7. `conductor --out` -- restrict to a hub-local path.
8. `deny_and_point` -- a test that executes the wired command with no interpreter and asserts
   permit.
9. **F8** -- the mutually-exclusive contract-fence gates. Owned by no row.
10. **ADR-110 disjointness should be computed at FREEZE**, section 9.

---

*Close packet written by the integrator seat, 2026-09-12. Every SHA, count and quotation in this
file was resolved against the tree before it was written.*

---

## 12 - The full suite on the merged tree, and the first baseline in this batch

`pytest -n 4` at `11c7c8b1`: **38 failed, 6019 passed, 4 skipped in 3125s (52:05)**.

A raw failure count is not a finding, so this seat baselined it: a throwaway worktree at
`0be08b3c` (the pre-wave commit) ran the same 38 node ids. **Thirty of them already failed.**

```
failing at 11c7c8b1 (post-wave) : 38
failing at 0be08b3c (pre-wave)  : 30   of the same 38
NEW, caused by this wave        :  8
```

**So main was ALREADY RED before this wave, by 30 tests.** That is the more important number and
it had not been measured: the full suite is owed once per batch at integration and had not
completed in this batch (three OOMs). This is the first completed run, and it says the tree
carries 30 standing failures that no wave introduced.

### The eight the wave introduced, each attributed

Every one is **cross-cutting**. Not one is a lane-local bug, and not one could have been caught by
the targeted tests each lane correctly ran -- which is precisely the argument for a full suite at
integration rather than per lane.

1-3. **`test_desired_state_loader` / `test_desired_state_report` / `test_desired_state_schema`** --
   `pydantic ValidationError: 1 validation error for Probe`, and the schema enum assertion fails.
   W-2' and X1-5 both added rows to `ecosystem/parity-surfaces.yaml`; the desired-state probe enum
   does not admit the new kind. **The enum is a pin that did not cover the surface that changed.**

4. **`test_graph_spine::test_a_disposition_register_entry_cannot_manufacture_its_own_trigger`** --
   *"dispositioned processes reported as triggered -- the register is laundering its own subject:
   ['scripts/worktree_seed.py']"*. lane-5 gave `worktree_seed.py` a trigger while it remained in
   the orphan-disposition register. The two surfaces must move together and one moved.

5. **`test_proof_layer::test_the_live_guard_population_is_at_or_below_its_baseline`** -- lane-5's
   new `test_worktree_seed.py` guard is above the ratchet baseline. A known shape in this repo: a
   new test trips the proof-layer ratchet, and the baseline is a governed artifact, so raising it
   is a DECISION, not a regeneration. Left for that decision rather than bumped here.

6-7. **`test_reverse_dep_oracle` (2)** -- the symbol `Finding` now resolves to **3 definitions**
   where the test expects 1: *"3 definitions; re-run with --file to disambiguate"*. X1-1's
   `decision_coverage.py` and X1-2's `conductor.py` each introduce a `Finding`. **Two lanes,
   each individually correct, collided on a name a third organ treats as unique.** No review of
   either diff alone could have seen it.

8. **`test_manifest_link_route::test_the_class_enum_is_the_hermetization_module_s_own_object`** --
   fails under the full parallel run and passes when re-run alone, so it is order- or
   worker-dependent rather than a clean regression. Recorded as such rather than attributed.

### What this seat did and did not do about them

**Did not repair them, deliberately.** Items 4 and 5 are governed registers and ratchets whose
whole purpose is to force a decision when they trip; bumping a baseline or editing a disposition
register to make a red test green is the exact act those organs exist to prevent an author from
performing quietly. Items 1-3 and 6-7 are cross-lane design collisions that need an owner, not an
integrator patch. All are named here with their causes so the repair is a filing decision rather
than a rediscovery.

**Also measured, and new:** the `graph-rebuild` pre-commit hook ([#664] clause 1, merged in this
wave) cannot swap `FPG.db` while a test run holds `FPG.db-wal` open -- *"could not swap in the
rebuilt store after 20 attempts... a reader is holding it open"*. **Running the suite blocks every
commit on this machine.** Two organs from the same row contend on one file, and nothing declares
the contention.

---

*Section 12 added at close, after the full suite completed. Every number in it was measured, and
the pre-wave baseline was run rather than assumed.*
