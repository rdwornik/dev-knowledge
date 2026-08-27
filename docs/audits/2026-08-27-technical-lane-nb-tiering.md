# lane-nb-tiering — commit/ship tiers ([#597]) + the slow-marker selector ([#598])

> Lane report. Batch: night of 2026-08-26/27, lane `lane-nb-tiering`, branch
> `worktree-lane-nb-tiering`, LOCAL worktree, gates armed. Contract: `lane-nb-tiering.md` (frozen).
> Evidence inputs: `docs/audits/2026-08-26-technical-perf-recon.md` (PERF-RECON, rows B4/B9/B10)
> and the W2A lane's step-0 telemetry ranking (`worktree-w2a-perf-core`,
> `docs/audits/2026-08-26-technical-w2a-perf-core.md` §2/§5).

## Headline

`_GATE_MODE` — a module global that **2 of 46** checks consulted — is retired for a tier
**declared per check** and read by the runner. The commit gate now runs **36 of 46**; the other
ten run at ship. Measured on this tree, per-commit check work falls **476,497 ms → 198,728 ms
(−58.3%)**; against the post-W2A reference run it is **302,693 → 83,435 ms (−72.4%)**. Ship-gate's
finding stream is **byte-identical** — 149 findings, 46 checks, proved side by side in one process
against one tree, not asserted.

**Wall-clock on this tree barely moved (172.6 s → 162.0 s), and that is the honest result, not a
buried one.** This branch predates W2A's `journal_anchor` repair, so `check_journal_spine_anchor`
costs 162 s here and Amdahl-bounds the run on its own. It is commit-tier **by design** (FAIL-capable;
it is the ADR-85 backstop), so tiering cannot and should not remove it. The lever this lane pulled is
visible in the *work* number, and it becomes visible in the *wall* number the moment W2A merges.

**[#598] is NOT covered by this file.** Its gating measurement — the two `pytest --durations=25`
passes whose result decides whether the marker sweep happens at all — had not returned when this
artifact was sealed, and an audit artifact is immutable once committed, so it cannot be completed in
place afterwards. Rather than seal a verdict ahead of its evidence, [#598]'s measurement, its
long-pole/long-tail verdict and the B10 fix land in the sibling artifact
`docs/audits/2026-08-27-technical-lane-nb-tiering-durations.md`, committed by act 2. **This file
makes no claim about the test suite's shape.**

---

## 1. Substrate honesty

Every number below was produced on the operator's Windows workstation, with the [#529] telemetry
switch on, by the command the pre-commit hook runs:

```
DEV_KNOWLEDGE_TELEMETRY=1 PYTHONUTF8=1 uv run --locked python scripts/audit.py health --parallel
```

Six sibling lane worktrees existed on disk throughout (`lane-g2-consume-recon`, `lane-h-handoff-mech`,
`lane-na-gates`, `prompts-revocation`, `w2a-perf-core`, `w2b-surfaces`, `w2c-codespace-repair`), and
`main` sits at `08b0d192` — a commit **this branch does not contain**. Three consequences, stated
rather than smoothed:

- **Host contention is a confound in every wall-time here, not a controlled variable.** Cross-run
  comparisons of individual checks carry scheduling noise. The one comparison this lane rests on —
  46-check work vs 36-check work — is a difference of *which checks ran*, which contention cannot
  manufacture.
- **The byte-identity proof does NOT use a before-run and an after-run.** `main` moves under this
  worktree, so two runs at two times would let an unrelated merge masquerade as a behaviour change.
  The harness loads the pre-change module and the post-change module side by side in ONE process
  against ONE working tree (§3). Discipline borrowed from W2A §4.
- **This tree lacks [#587]/[#588].** The tier decisions were therefore made against W2A's
  **post**-fix ranking (`db4aeea2`), which is the world the tiering lands into, and confirmed against
  this lane's own pre-fix ranking. The two rankings agree on the ship set; §2 shows both.

---

## 2. The measured input, and the assignment rule

The contract's measure-first input is W2A's telemetry ranking. The published table in that report is
the top ten; the full 46 rows were read from its store
(`.claude/worktrees/w2a-perf-core/logs/TELEMETRY.db`, run `db4aeea2`, read-only).

**The rule, stated once rather than re-argued per row.** A check is `TIER_SHIP` only when **BOTH**:

- **(a) it cannot emit `fail`.** `cmd_health` exits 1 on a `fail` alone — a WARN-only check's
  commit-time verdict is one line among a hundred and blocks nothing. Its teeth are at ship-gate,
  which REDs on any undispositioned WARN. So moving it does not weaken it; it relocates it to where
  it already had force. This is how [#597]'s bar — *"NO check is made faster by being made
  weaker"* — is met by construction rather than by assertion.
- **(b) it costs ≥1 s of measured wall time.** Everything else stays at commit, **including** the
  sub-second WARN-only checks: `doc_rot` 128 ms, `no_ff_merges` 410 ms, `preflight_backlog_ids`
  102 ms, `enforcement_coverage` 39 ms, `deployed_methodology_version` 322 ms. Moving those buys
  nothing measurable and costs their awareness line. **A tier decision with no payoff is not a
  decision**, and [#597] asks every decision to cite its number — including the decision to keep.

Fail-capability was determined per check from its own docstring/ruling, not from today's observed
verdict: an observed WARN proves only that a `fail` path was not *reached*, which is what a latent
one looks like. Three of the ten say it in their own source (`doc_code_edge`: *"NEVER FAILs this
arc"*; `undeclared_edges`: *"wired as a ship-gate WARN leg … never FAIL"*; `doc_structure`:
*"never FAIL -> never blocks the audit-health commit gate"*), and two are asserted structurally by
the suite (`review_artifact_coverage`, `funnel_coverage` — no hard-verdict literal appears in the
function).

### The assignment table — the ten ship-tier members

`ms` = `duration_ms` in run `db4aeea2`; `%` = share of that run's 302,693 ms of check time.

```
check                             ms      %       why ship
review_artifact_coverage      128428  42.43   WARN-tier by the [#480] P3 ruling; hard leg deferred
doc_code_edge                  36617  12.10   "NEVER FAILs this arc" (ADR-89 OQ3 data-gated)
undeclared_edges               22530   7.44   #179 was ALREADY "a ship-gate WARN leg" (2026-07-03)
fleet_parity                   14520   4.80   EXCEPTION - FAIL-capable; cross-repo argument below
funnel_coverage                 6219   2.05   WARN-tier by ruling (M3 zero-baseline ratchet)
doc_structure                   4531   1.50   WARN-only by its own docstring
git_backlog_drift               3911   1.29   WARN-only awareness organ (#90a)
stale_worktrees                 2420   0.80   WARN-tier by ruling (ADR-110 s1 item 4)
doc_claims                        82   0.03   EXCEPTION - _GATE_MODE consumer #2
generated_artifact_freshness       0   0.00   EXCEPTION - _GATE_MODE consumer #1 (0 ms BECAUSE it
                                              already skipped; the tier makes that declared)
                     ship total 219258  72.44
                   commit total  83435  27.56   (36 checks)
```

**Three exceptions, each with its own argument, because the rule alone does not carry them.**

- **`fleet_parity` is FAIL-capable and ship anyway.** Cost alone would not justify it — a
  FAIL-capable check earns its commit-time seat. The argument is that the property is **cross-repo**:
  parity drift is caused by what happens in the *other* repos of the fleet, and a hub commit cannot
  create it. Gating every hub commit on the state of five other working trees prices each commit at
  another repo's drift while preventing none of it. The arc boundary is where a fleet-wide claim can
  honestly be made. **Given up, stated:** a parity regression introduced elsewhere now surfaces at
  ship rather than at the next hub commit — later, and named rather than smoothed. This discharges
  the follow-up the check filed against itself in 2026-07-18 (*"the walk is ~8s … ship-gate-only
  scoping is a filed follow-up, not this arc"*), which had grown from ~8 s to 14.5 s while filed.
- **`doc_claims` at 82 ms would fail rule (b) outright.** It is ship-tier because it is one of the
  two checks `_GATE_MODE` existed for: it ran at commit in a *degraded* posture, everything but the
  expensive claim-3, suppressed by `run_expensive=not _GATE_MODE`. Declaring the whole check
  ship-tier says the same thing without a global. **Absorbing these two IS what "generalize
  `_GATE_MODE`" means** — leaving the global alive for them would have been renaming, not
  generalizing.
- **`generated_artifact_freshness` measures 0 ms for a reason that is easy to misread.** It is 0
  *because* it already returned an early `n/a` under `_GATE_MODE` — it was a hand-rolled ship tier
  before one existed. Its docstring said so (*"ship-gate-only leg — skipped at the audit-health
  commit gate"*). The declaration replaces the branch; the leg's body no longer has a commit-time
  path at all.

### Both rankings agree on the ship set

The set was chosen against `db4aeea2` (post-W2A) and re-checked against this lane's own baseline run
`31fc363a` (pre-W2A). No member changes side:

```
run                                   all-46 sum   ship-tier(10)      commit-tier(36)   commit Amdahl bound
db4aeea2  W2A, post-#588, quietest        302693   219258 (72.4%)      83435 (27.6%)   handoff_probes  27234
f0caf15a  W2A, pre-#587 baseline          564383   279131 (49.5%)     285252 (50.5%)   spine_anchor   197808
31fc363a  this lane, before               476497   238635 (50.1%)     237862 (49.9%)   spine_anchor   162146
```

The two pre-W2A rows show why the wall-time win is not visible on this branch: half the removed cost
is real, and the half that remains is one check.

---

## 3. Byte-identity on ship-gate — proved, not asserted

The row's constraint is that ship-gate is unchanged. Two independent arguments, given in the order
of increasing force.

**By construction.** `cmd_ship_gate` passes **no** tier, and `runs_at_tier(check, None)` is `True`
for every check — so the active set, the slot construction and the flatten are the same objects
doing the same work. The only two behavioural expressions that changed evaluate to what they
evaluated to at ship time before: `check_generated_artifact_freshness`'s deleted `if _GATE_MODE:`
branch was never taken at ship (`_GATE_MODE` was `False` there), and `run_expensive=not _GATE_MODE`
was `not False` — now written `True`.

**By measurement.** A harness loads the **pre-change** `audit.py` (from `git show HEAD:`) and the
**post-change** one into ONE process, against ONE working tree, and runs the exact call `ship-gate`
makes. The pre-change copy is written beside the real one in `scripts/` — every constant derives
from `__file__` at import, so loading it from anywhere else would silently audit a different tree —
and deleted in a `finally`.

```
observable                     before   after   verdict
findings emitted                  149     149   IDENTICAL
distinct check_names               46      46   IDENTICAL
(check_name, status, evidence)   list    list   IDENTICAL, compared IN ORDER
                                               VERDICT: BYTE-IDENTICAL
```

Compared as an ordered **list**, never as a set: order is `CHECK_ORDER`, and `CHECK_ORDER` is part
of the output contract the git hooks read.

The harness additionally asserts the baseline is the right one — the pre module HAS `_GATE_MODE` and
it is `False`; the post module does NOT have it — so a mis-loaded module fails loudly instead of
producing a vacuous match.

---

## 4. What changed in the code

**The tier is declared in the registry, and the shape makes silence impossible.** Every `ALL_CHECKS`
entry is `_tier(TIER_COMMIT, check_x)` / `_tier(TIER_SHIP, check_x)` — the tier is a *required
positional argument*, so an entry cannot be added without stating one. The wrapper stamps the
function and returns it unchanged, so the list is still a list of the same callables and no consumer
(`detect_unconditionally_inert_checks`, `check_doc_code_coverage_drift`, `CHECK_ORDER`, the tests
that monkeypatch `ALL_CHECKS`) sees a different type.

Stamping the function rather than keying a side table on `__name__` is deliberate: **16 of the 46
checks live in `scripts/audit_checks/`**, and a name-keyed table would silently mis-tier a renamed
check — the seam-detaches-silently class `audit_checks/registry.py` documents.

**`tier_of` defaults to `TIER_COMMIT`, and that default is the strict direction** — an undeclared
check runs everywhere, so silence costs wall time and never coverage. The default exists for the
test seam (a monkeypatched sentinel must not have to know about tiers), **not** as a licence to
omit: `test_every_all_checks_member_declares_a_gate_tier` fails by name on any undeclared member.
An unknown tier string RAISES at import, because a typo that degraded to a default would move a
check off the commit gate with nobody noticing.

**`runs_at_tier` is a subset test, never equality.** Written as `tier_of(check) == tier`, ship-gate
would SKIP every commit-tier check — the exact inverse of what a ship gate is for, and invisible to
any test that only exercised the commit path. That inversion has its own test.

**A deferred check is enumerated, not omitted.** Its slot carries one `n/a` finding —
`declared ship-tier -- not run at the commit gate ([#597] …)` — so `health` still names all 46
organs and the operator can see at the commit gate what the commit gate did not do. Silence would
make a deferred check indistinguishable from a deleted one, which is the `handoff_tag_canonicity`
failure class this module already refuses in `detect_unconditionally_inert_checks`.

**A deferred check emits NO telemetry row.** Its `duration_ms` would be ~0, and a run of zeros would
silently re-rank the very table tier decisions are read from — the next person to profile would
conclude the ship-tier checks are free. No row beats a fabricated one. Confirmed live: the after-run
`0621bae4` carries **36** `check_run` rows, not 46.

**`cmd_health` lost its `try/finally`, and the absence is the point.** The tier is an argument, so
there is no global for a raising check to leave set.

**Thread-pool width is sized to the checks that actually run** (`sum(runs) or 1`), not to
`len(active)` — a pool of 46 threads to run 36 checks would be a quiet waste — and still floored at
1, because `ThreadPoolExecutor(max_workers=0)` raises and an all-deferred list is a legitimate call.

---

## 5. Measured before / after

```
label                      command                                   exit   wall_ms   checks   sum(duration_ms)
before-parallel  run 31fc363a   audit.py health --parallel               1    172600       46             476497
after-tiered     run 0621bae4   audit.py health --parallel               1    162006       36             198728
```

- **Check work: 476,497 → 198,728 ms (−58.3%).**
- **Wall: 172.6 s → 162.0 s (−6.1%).** Bounded by `check_journal_spine_anchor` at 158,982 ms in the
  after-run — 80.0% of remaining check time, on a branch without [#587]/[#588].
- **Findings printed: 142 → 76.** The deferred organs emit one Finding per locus/concern, so ten
  deferrals collapse a large WARN population into ten `n/a` lines.
- **The FAIL set is unchanged**, and this is the load-bearing safety check: exactly one `[!!]`
  before and after, the same one — `journal_spine_anchor` on `08b0d192`. Nothing this lane did
  turned a check red or green.

**Secondary effect, observed and NOT claimed as a result.** Several surviving checks got faster
between the two runs beyond noise (`reconciled_versions` 20,793 → 3,089 ms; `handoff_probes`
27,865 → 22,237 ms), plausibly because removing ten I/O-heavy checks frees bandwidth inside the
8-wide pool. It is a single pair of runs on a contended host; it is reported because it is in the
data, and it is not attributed.

**Projected, once W2A merges** — arithmetic on measured per-check numbers, explicitly not a measured
wall time: commit-tier work becomes **83,435 ms** with `check_handoff_probes` (27,234 ms) as the new
Amdahl bound. **That check is FAIL-capable and this lane does not move it.** Making it diff-triggered
is a different row's work, and it is the named residual.

---

## 6. Tests

No assertion was weakened or deleted. Four `_GATE_MODE` tests were **replaced** rather than removed,
and each replacement states what property it inherited:

- `test_cmd_health_gate_mode_set_during_loop_and_restored` → `test_cmd_health_runs_the_commit_tier`
  (the wiring, observed through a ship-tier sentinel that must not run).
- `test_cmd_health_gate_mode_restored_on_exception` →
  `test_cmd_health_leaves_no_state_behind_when_a_check_raises`. The old test guarded a global whose
  reset a raise could skip; the property is now **structural**. It is asserted anyway — by
  `not hasattr(aud, "_GATE_MODE")` plus a live re-run after the raise — because *"the bug is
  impossible now"* is a claim that deserves a test.
- the same pair in `tests/test_audit_parallel.py`, kept there because the parallel path builds
  `slots` differently (pre-seeded deferrals + a sparse future map) and that is where a
  serial/parallel divergence would hide.
- `test_check_passes_run_expensive_false_in_gate_mode` →
  `test_check_runs_every_claim_and_is_deferred_off_the_commit_gate`, which asserts **both** halves
  (the check always runs complete; the commit tier never runs it) — either alone would pass while
  the expensive claim silently stopped running anywhere.

Added: the declaration refusal; the unknown-tier raise; the default; the nested-ladder
(equality-bug) guard; commit-tier deferral in **both** modes; `tier=None`/`ship` run-everything;
the no-telemetry-for-a-deferral guard; and the worker-width sizing including the all-deferred
floor-at-1 case.

```
tests/test_audit_parallel.py                      20 passed  (167 s)
tests/test_validate_doc_claims.py                 42 passed  ( 27 s)
tests/test_audit.py + tests/test_ship_gate.py    230 passed, 2 failed  (277 s)
ruff check scripts/audit.py tests/test_audit.py tests/test_audit_parallel.py
           tests/test_validate_doc_claims.py       clean
```

**The two failures are pre-existing and are not this lane's**, proved rather than dispositioned.
`test_health_ok_with_registered_repo` and `test_health_stays_ok_with_na_status` both assert
`cmd_health` exits 0 against the LIVE repo. The **pre-edit baseline run of that same code path
already exited 1** (§5, run `31fc363a`) on the foreign `journal_spine_anchor` FAIL — so both tests
were red on this tree before the first character of this lane was written. Ownership of that FAIL is
proved in §8.

Per the batch cadence the FULL suite is the integrator's, run once at integration; this lane ran the
targeted files covering its diff — plus the two `--durations` full-suite runs [#598] explicitly
required, which are measurement, not a green verdict (§7).

---

## 7. [#598] — deliberately not in this artifact

The row's own done-when narrows on a measurement, and the contract makes that binding: *"First run
`pytest --durations=25` (parallel + `-n 0` reference) and record both tables — if the suite is
long-pole (top25 >20% wall), STOP the marker sweep, report, and fix nothing (the row narrows per
its own done-when)."*

That measurement had not returned when this file was sealed. Two facts decided the split rather
than a preference: an audit artifact is **immutable once committed** (CLAUDE.md §5 rule 3), so a
placeholder section here could never be corrected in place; and this lane's first attempt at the
measurement was **lost to a session boundary**, making "hold act 1 uncommitted until it returns"
a bet with hours of proved work on the table.

So [#598] gets its own artifact: `docs/audits/2026-08-27-technical-lane-nb-tiering-durations.md`,
carrying both duration tables, the long-pole/long-tail verdict, whatever that verdict licenses
(marker sweep + PLAYBOOK Ch5 cadence line + coverage lint, or an explicit STOP), and the B10 fix
at `validate_doc_claims.py`. **Nothing in this file asserts anything about the suite's shape** —
the headline says so too, because a reader who saw only §7 should not have to infer it.

**One honest consequence of committing act 1 first**, recorded here rather than discovered in the
numbers: this commit's pre-commit hooks execute while the duration arms are running, so a bounded
contention window sits inside them. It is small — the heaviest hook, `audit-health`, is the one
this commit declares a `SKIP` for (§8), so what runs is the fast set — but it is non-zero. The
sibling artifact states it as a confound and applies its criterion on the serial arm, where a
top-25-share-of-wall ratio is well-defined.

---

## 8. Declared bypasses

`check_journal_spine_anchor` FAILs on `08b0d192` — *"Merge branch
'chore/workspace-provider-roots-2026-08-26'"*, a commit on `main` that this branch does not contain.
Ownership is proved three ways, not claimed:

- **(a) Not mine:** `git merge-base --is-ancestor 08b0d192 HEAD` → exit 1 (false).
- **(b) Not lane tree-lag:** the anchor is absent from **both** this worktree's `JOURNAL.md` and
  `main`'s own (`git show main:JOURNAL.md`), so the sync-merge remedy would buy nothing. This is the
  test that decides between a `SKIP` and a sync-merge, and it comes out against the merge.
- **(c) Not exemptible:** `batch_manifest.open_batches('.')` → `[]`, so the ADR-110
  declared-integration-arc exemption is unavailable.

Same shape, same three-part proof, and the same conclusion as W2A §8 on the immediately preceding
merge. `SKIP=audit-health` drops ONE hook; ruff, the ADR-101 hermetization gate, the
provider-registry gate and both commit-msg gates ran on every commit. `--no-verify` was not used.

---

## 9. Honest limits

- **The wall-time win is not demonstrated on this branch and cannot be.** −6.1% is what tiering buys
  while one commit-tier check costs 162 s. The −58.3% work figure and the −72.4% projection are the
  real claims; anyone reading only the wall number should read this paragraph.
- **The projection is arithmetic, not a measurement.** It sums measured per-check durations from a
  run this lane did not produce, on a tree this lane does not have. It will be a measurement after
  the integrator merges W2A.
- **Rule (a) rests on `cmd_health`'s exit condition, which is code, not doctrine.** If a future
  change made `health` block on WARNs, ten checks would silently stop gating commits they would then
  be expected to gate. Nothing currently asserts that coupling. It is named here rather than left to
  be discovered.
- **Fail-capability was read from docstrings and rulings, not proved.** A check whose docstring says
  *"never FAIL"* while its delegate can emit one would be mis-tiered, and this lane's static scan
  reads only each check function's own body — delegated verdicts (`fleet_parity`'s helper) were
  caught by hand, and a future one might not be.
- **`scripts/audit_checks/registry.py` still names `_GATE_MODE` twice in prose** (a docstring list of
  test-patched seams, and the `check_doc_claims` row comment). Both are now stale. They were left
  **deliberately**: the contract puts `scripts/audit_checks/` out of bounds as lane-na's territory,
  and a two-word comment edit is not worth a merge collision in another lane's file. Owed, with
  locators.
- **This lane edits `ALL_CHECKS`, and lane-na adds checks to it.** That is a guaranteed integration
  conflict — and a *loud* one, which is the good case: a new check added without a `_tier(...)`
  wrapper fails `test_every_all_checks_member_declares_a_gate_tier` by name rather than quietly
  joining the commit gate.
- **Which checks belong in the commit tier is a per-repo judgement**, as PERF-RECON Q4 says. The
  mechanism travels with the corpus; this repo's assignment does not necessarily.

---

## 10. Disposition

ACTIONED — [#597] executed and committed by this artifact's commit. [#598] is **OPEN at this
commit** and is dispositioned by its own artifact (§7). Commits are named in the end packet.
