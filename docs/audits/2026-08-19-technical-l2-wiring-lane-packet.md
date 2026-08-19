# LANE L2 packet — [#529]/[#530] wiring

**Lane:** L2 · branch `worktree-lane-l-529-wiring` · contract-of-record `b2abedb8`
**Contract body:** item 5 of `docs/audits/2026-08-19-technical-n1-529-530-wiring-spec.md`
**Status:** written incrementally as the lane proceeds; **frozen at STOP.**

> **On immutability, stated rather than glossed.** `docs/audits/` is immutable under CLAUDE.md §5
> rule 3, and this file was appended to across several commits rather than written once. That is
> deliberate and declared here at its head: it is the lane's *in-flight working record*, the
> artifact the contract's STEP 1 and STEP 9 both instruct the lane to write into as it goes, and
> its growth is legible in git history rather than hidden by it. Nothing already written was
> rewritten — every edit appended a new section. It is frozen at STOP; from that point the rule
> applies to it normally. The alternative (one sealed file per step) would have scattered one
> lane's reasoning across nine artifacts, which is worse for the reader the packet exists for.

---

## Environment honesty header — WHICH GATES RAN HERE (measured, not assumed)

N1's own header recorded that it ran with no gates at all. This lane is the opposite, and that
is the whole point of amendment 3:

```
$ python --version                          -> Python 3.12.10   (>= the >=3.12 floor: OK)
$ uv --version                              -> uv 0.11.19       (== the pinned uv: OK)
$ .venv/Scripts/python -c 'import pytest'   -> pytest 9.1.1     (suite runnable)
$ SessionStart arm_hooks                    -> pre-commit / commit-msg / pre-push installed
```

Every commit in this lane goes through the live pre-commit gate set (`audit-health`, `ruff`,
`validate-hermetization`, `block-commit-on-main`, the freshness/index gates, and the two
commit-msg gates). No `--no-verify` and no `SKIP=` anywhere in this lane.

---

## Amendment 3 — UNVERIFIED to verdict log

Every row below is one the N1 spec derived by reading the tree with no pytest and no gates.
Re-verified here on the real toolchain BEFORE acting on it. `CONFIRMED` = the claim holds as
written; `CORRECTED` = it does not, with what is true instead.

| # | Spec claim | Verdict | Evidence |
|---|---|---|---|
| U1 | `audit.py:3553 run_checks` is the single funnel; three callers `audit_repo`/`cmd_health`/`cmd_ship_gate` | **CONFIRMED** | `grep -n 'def run_checks'` -> 3553; callers at 3597 / 4127 / 4234 |
| U2 | serial branch `:3583-3586`, parallel `:3590-3593`, flatten at `:3594` | **CONFIRMED (1-line drift)** | live: `if not parallel` 3582, `out.extend` 3585; parallel 3590-3593 exact; flatten `return [f for slot ...]` 3594 exact. The drift is the branch's opening line, not a different site |
| U3 | `Finding.status` is a 5-value enum; `telemetry_emit.OUTCOMES` is 3; `emit_event` REFUSES an unknown outcome | **CONFIRMED** | `_common.py:44` field comment + docstring; `OUTCOMES` at `telemetry_emit.py:135`; the refusal is `emit_event`'s 2nd guard |
| U4 | hook `main()` at `block_ff_push:222`, `block_unanchored_push:79`, `block_commit_on_main:133`, with the enumerated exit lines | **CONFIRMED, exactly** | `grep -n 'def main\|return [0-9]'`: 222 / 241,255,257,271 · 79 / 95,103,110,112,123 · 133 / 138,143,154 — every number as written |
| U5 | `emit_blocker_fired` hard-fixes `outcome="block"`, so a refusal emits BOTH a `hook_run(block)` and a `blocker_fired` | **CONFIRMED** | `telemetry_emit.py:447-457`; the double-count is recorded as a deliberate shape below |
| U6 | `telemetry_emit._REPO_ROOT` is independent of `audit._REPO_ROOT`; `default_db_path()` reads the former | **CONFIRMED** | `telemetry_emit.py:110` vs `audit.py:70`; `default_db_path()` returns `_REPO_ROOT / DEFAULT_DB_RELPATH` |
| U7 | `test_ship_gate_is_readonly` watches only the tmp tree `aud._REPO_ROOT` points at, so it cannot see a telemetry write | **CONFIRMED** | `tests/test_ship_gate.py:118-128`: `monkeypatch.setattr(aud,"_REPO_ROOT",str(repo))` then `repo.rglob("*")` before/after |
| U8 | `audit.py:283` `logging.basicConfig(level=INFO)` at module scope + `_log_event` at INFO gives telemetry lines on stderr | **CONFIRMED, re-measured here** | see "Blocker (a)" below — reproduced against the real modules on 3.12.10, not a synthetic snippet |
| U9 | the three hook scripts touch no `logging`, so `lastResort` (WARNING) keeps their stderr clean | **CONFIRMED** | `grep -n logging scripts/block_*.py` -> no match in any of the three |
| U10 | `safe_emit` swallows store/IO failure but NOT `TelemetryError` | **CONFIRMED** | `except (sqlite3.Error, OSError): return None` — nothing else caught |
| U11 | WAL leaves `-wal`/`-shm` sidecars, so the ignore must be the glob `logs/TELEMETRY.db*` | **CONFIRMED, re-measured here** | see STEP 6 evidence |
| U12 | `check_silent_rule_ratchet` scopes to `protocols/*.md`, `templates/**`, `ecosystem/*.yaml` — `scripts/` and `.claude/` are out | **CONFIRMED** | `silent_rule_detector.py` scope globs; baseline measured unchanged across this lane (STEP 7) |
| U13 | `check_import_edges` walks Claude-Code `@import` targets, not Python imports; no `tach.toml` | **CONFIRMED** | the check reads `CLAUDE.md` `@`-imports; `ls tach.toml` -> absent |
| U14 | **`codemap-freshness` fires on the new import edge, so a codemap regen is part of the wiring commit** | **CORRECTED — no regen is owed** | The live `ARCHITECTURE.md` CODEMAP block (`:162-173`) lists **packages only** (`codemap`, `toc`) and its Dependencies section is literally `- (none)`. `scripts/audit.py` and `scripts/telemetry_emit.py` are top-level modules, not packages, so neither is a node and an edge between them cannot appear. Verified by running the gate itself after the wiring landed (STEP 8). **This correction matters beyond tidiness:** `ARCHITECTURE.md` is in `_FRESHNESS_FILES`, so an unnecessary regen would have bumped its commit date past `last_reviewed: 2026-08-14` and RED-ed `canonical_freshness` A2 on the next commit — STEP 8 would have wedged the lane on a re-stamp nobody had earned. |
| U15 | `ecosystem/doc-counts.md` `3033 collected` moves when the new test files land | **CONFIRMED** | regenerated at STEP 8; before/after quoted there |
| U16 | `[#530]`: no Python dispatch entry point — `/lane-boot` §1 pre-flight `:22-26`, `/lane-integrate` §3 five-row table `:57-63` | **CONFIRMED** | `lane-boot.md` §1 ends with the `validate_branch_naming.py --lane` fence at 23-25; `lane-integrate.md` §3 table has exactly rows 1-5 under a "Run all five" lead-in |
| U17 | `single_flight` open leg (a) ABA in `release`, leg (b) `rev-parse` conflation at `:206-208` | **CONFIRMED** | `release()` reads `_local_holder` then deletes the remote ref unconditionally; `_local_holder` maps any non-zero return to `""` |

**No CORRECTED row changed the CONTRACT's shape**, so no STOP-report is owed. U14 removes work
(STEP 8's codemap half) rather than adding it; U2's one-line drift changes no site. Both are
applied as corrections and recorded here, per amendment 3.

---

## The two MEASURED blockers — re-measured HERE, against the real modules

N1 measured blocker (a) with a synthetic `logging.basicConfig` snippet, because it had no venv
to import the real modules into. This lane has one, so both were re-measured through the actual
code paths a wired gate would take. Both reproduce.

**Blocker (a) — `audit.py:283` puts telemetry on stderr.** Import `audit` (which runs
`basicConfig(level=INFO)` at module scope), then emit one event through the real library:

```
$ python -c "import sys; sys.path.insert(0,'scripts'); import audit, telemetry_emit as te; \
             te.emit_check_run('doc_claims','pass',12, db_path=<tmp>)"
RC: 0
STDOUT: ''
STDERR: 'telemetry: {"context_json": "{}", "duration_ms": 12, "event_type": "check_run",
          "name": "doc_claims", "outcome": "pass", "ts": "2026-08-19T10:42:57.693276+00:00"}\n'
```

One line per event, on stderr, on a per-commit gate that runs 43 checks. CONFIRMED.

**And the hook counterpart is clean, which is why the fix is caller-side.** The same emit without
importing `audit` produces nothing at all — `logging.lastResort` is WARNING-level, so an `.info()`
with no configured handler is silent:

```
$ python -c "import sys; sys.path.insert(0,'scripts'); import telemetry_emit as te; \
             te.emit_hook_run('block-ff-push','pass',3, db_path=<tmp>)"
RC: 0  STDOUT: ''  STDERR: ''
```

So the defect belongs to `audit.py`'s module-scope `basicConfig`, not to `telemetry_emit`. Fixing
it in the library would touch `test_emit_survives_an_unusable_log_side_channel` and
`test_logger_backend_reports_which_side_channel_is_live` — pinned tests, for a defect the library
does not have.

**Blocker (b) — the sandbox seam.** `telemetry_emit._REPO_ROOT` and `audit._REPO_ROOT` are
independent module-level values (U6), so monkeypatching the latter does not move the store. The
fix and its before/after are at STEP 3.

**U11 — the WAL sidecars**, re-measured through the real `telemetry_emit.connect()` rather than a
hand-rolled sqlite connection:

```
OPEN:   ['TELEMETRY.db', 'TELEMETRY.db-shm', 'TELEMETRY.db-wal']
CLOSED: ['TELEMETRY.db']
```

They vanish on a clean close and survive a crashed writer or a concurrent reader — which is the
state WAL exists to support here. The `.gitignore` leg therefore needs the glob (STEP 6).

---

## STEP 1 — the outcome mapping (DECIDED, not improvised)

`Finding.status` in {pass, fail, warn, unavailable, n/a} (5) must be projected onto
`telemetry_emit.OUTCOMES` in {pass, block, error} (3). `emit_event` raises `TelemetryError` on an
unknown outcome, and `safe_emit` deliberately does **not** swallow that class — so an improvised
mapping would not degrade quietly, it would crash the audit. The decision is therefore made once,
here, and pinned by a test rather than a comment.

**The mapping, as proposed by the contract and adopted unchanged:**

| `Finding.status` | event `outcome` | why |
|---|---|---|
| `fail` | `block` | the only status that stops a commit at `audit-health` and a ship at `ship-gate` |
| `pass`, `warn`, `n/a`, `unavailable` | `pass` | none of them refuses an action; a WARN informs, an `n/a`/`unavailable` did not evaluate |
| *(the check raised)* | `error` | a check that crashed is neither a pass nor a block — `OUTCOMES`' own reason for a third value |

**Aggregation: ONE event per check per run**, never one per finding. The check is the organ being
measured; its findings are its output. The collapsed detail rides `context`, so the read side
loses nothing:

```json
{"statuses": {"pass": 1, "warn": 2}, "findings": 3, "finding_names": ["doc_claims"]}
```

`finding_names` is this lane's one addition to the contract's proposed context shape, and it is
there for a concrete reason. The event's `name` is the check function's `__name__`
(`check_doc_claims`), because that is the only name a check with **zero findings** has — and the
contract's case 4 requires such a check to still emit a row. But the disposition register and the
ship-gate key on `Finding.check_name` (`doc_claims`), a different string. Carrying both means a
reader can join a `check_run` row to the register without re-deriving the relationship.

**Fork not taken.** The contract offers a STOP-report if the collapse loses a signal the memo
needs. It does not: the memo's two questions are *"retire checks with fires>0/blocks=0"* and
*"promote high-catch checks"*, and both are answered by fires-vs-blocks per check name, which is
exactly what this mapping preserves. Extending `EVENT_TYPES`/`OUTCOMES` is Stage 2 and is
explicitly refused by the contract's WHAT-NOT-TO-DO list.

**The `hook_run` + `blocker_fired` double-count is deliberate, and is recorded here so a reader
does not have to discover it.** A hook that refuses emits BOTH a `hook_run(outcome="block")` and
a `blocker_fired` — `emit_blocker_fired` hard-fixes `outcome="block"` (U5). They are separate
event types answering separate questions ("did this organ fire, and how did it end" vs "what did
this refusal say"), which is the memo's own shape. **A reader summing `outcome="block"` across
event types double-counts every refusal.** Count blocks from `check_run`/`hook_run`; count
refusal reasons from `blocker_fired`.

---

## STEP 7 — the `[#530]` arm taken: `claim` + `inspect`, `release` DEFERRED

The contract offers two arms and this lane took the second, deliberately.

**`claim` is wired at `/lane-boot` §1**, after the branch-name check and before anything exists
to clean up. Exit codes are documented as a table because the verdict is the CODE, not the prose:
`0` claimed → provision · `3` already in flight → **STOP, do not provision** · `2` internal error
→ STOP (the guard fails closed; an unknown flight state is not a free one). The contract id is
`/lane-boot`'s own fourth argument, the contract PATH — verified live that git accepts it as a
ref name:

```
$ git check-ref-format refs/locks/docs/audits/2026-08-19-technical-l2-wiring-lane-contract.md -> rc=0
$ python scripts/single_flight.py inspect docs/audits/2026-08-19-...-lane-contract.md --local-only
  single_flight: refs/locks/docs/audits/2026-08-19-...-lane-contract.md is FREE locally   (rc=0)
```

The PATH and not the bare `<id>`: two different contracts can govern one backlog row, and the
thing that must not run twice is the contract.

**`release` is NOT wired. `inspect` is, as the 6th refuse-to-finish row.** `[#530]` open leg (a)
is real and unfixed: `release` reads the local holder and then deletes the REMOTE ref, so after a
manual lock clear and a re-claim by a *different* lane, lane A's cleanup deletes lane B's **live**
lock — and because racers share HEAD, the sha guard on the local delete cannot tell them apart.
Wiring `release` into an automatic close-out is exactly what converts a documented-latent bug into
a live one. Fixing (a) needs a generation-unique token, which is a `scripts/` behaviour change
that would touch `test_t5_release_then_reclaim` and `test_t5_release_is_idempotent` — the
contract's WHAT-NOT-TO-DO list forbids wiring `release` onto an unfixed (a), and the spec itself
flags the fix rather than ruling it.

So the checklist SURFACES a held lock and the operator clears it with the holder in front of them.
The asymmetry is the argument: a stale lock refuses a dispatch, a wrongly-deleted one lets two
lanes run at once, and the second failure is the one the whole guard exists to prevent.

**Residual on `[#530]`:** `release` is unwired at `/lane-integrate`; wiring it is gated on leg (a).

**`tests/test_single_flight_wiring.py` is NOT written**, per the spec's own condition — both sites
are markdown, so "wiring" for `[#530]` was documentation, not code. Its cases 18/19 are the
conditional ones: 18 needs site 7 (`preflight_contract.py:401`), which the contract's scope line
excludes; 19 needs leg (a) fixed, which is deferred above. **Correction to the wrapper's FINAL
line:** it says "the artifact's 19 named cases across its 2 NEW test files", but cases 18-19 live
in a THIRD, conditional file. The 2 NEW files carry cases 1-17; this lane wrote 21 + 37 = 58 test
functions across them (the extra count is parametrization plus the cases named in the STEP-2/4
commit messages). Recorded rather than silently reconciled.

### A knock-on this step created, filed rather than swept in

Adding a 6th row makes three OUT-OF-SCOPE sites stale, and the contract's scope line is explicit
(`.claude/commands/{lane-boot,lane-integrate}.md` … "Nothing else"):

| Site | State | Disposition |
|---|---|---|
| `.claude/commands/lane-integrate.md` frontmatter `description:` ("five-item") | IN scope — the same file | **FIXED** to "six-item", and `.claude/generated/commands-repo.md` regenerated (`gen_claude_rosters.py --write`), because `claude-rosters-freshness` gates that fragment against the frontmatter |
| `protocols/PLAYBOOK.md:1862` — *"A batch closes when all **five** hold"*, plus the parenthetical *"ADR-110 §3 enumerates four, so the fifth rides as a recorded addition here"* | **OUT of scope** | **OWED, not taken.** PLAYBOOK is not in this lane's scope, it is inside `check_silent_rule_ratchet`'s scope root (`protocols/*.md`), and the site needs a *sixth-rides-as-a-recorded-addition* sentence written by whoever owns the Ch8 doctrine — not a lane doing a call-site wiring |
| 6 × `docs/handoffs/*/HANDOFF_BOOT.md:94` — "the five-item refuse-to-finish checklist" | **OUT of scope AND immutable** | **Never edited.** Handoffs are immutable (CLAUDE.md §5 rule 3); they are accurate records of what the checklist was when each was sealed |

`check_silent_rule_ratchet` is unmoved by this step either way — its scope roots are
`protocols/*.md`, `templates/**`, `ecosystem/*.yaml`, and `.claude/` is not among them (U12,
re-verified live this step against the module's own globs).

---

## ENVIRONMENTAL BLOCKER — `audit-health` went RED mid-lane, and it is NOT this lane's

**Reported, not dispositioned.** The STEP-7 commit was REFUSED by the `audit-health` pre-commit
gate. The first six commits of this lane passed the same gate; this one did not, because the
machine state changed underneath the lane:

```
Audit self-conformance gate (FAIL blocks the commit; WARN only informs)....Failed
  [!!] fleet_audit_replication: automation/fleet-audit is 5 commit(s) ahead of origin,
       over the 3-commit threshold -- ADR-80 promises a durable record that currently
       exists on ONE disk ([#460])
health: DEGRADED
```

**Proof of ownership, run rather than argued.** The five unreplicated commits are the
fleet-audit ROUTINE organ's own, all made today, on a branch this lane has never touched:

```
$ git log --format='%h %ad %an %s' --date=short origin/automation/fleet-audit..automation/fleet-audit
  760da0f8 2026-08-19 robdwornik chore(routine/fleet-audit): record 2026-08-19 baseline
  9b4a7511 2026-08-19 robdwornik chore(routine/fleet-audit): record 2026-08-19 baseline
  44b75818 2026-08-19 robdwornik chore(routine/fleet-audit): record 2026-08-19 baseline
  7c2a2b25 2026-08-19 robdwornik chore(routine/fleet-audit): record 2026-08-19 baseline
  c2fcd451 2026-08-19 robdwornik chore(routine/fleet-audit): record 2026-08-19 baseline

$ git log --oneline <lane-start>..HEAD --name-only | grep -c fleet-audit   ->  0
```

And the check fires on branch state alone, independent of anything staged — run in isolation
against the live tree:

```
$ python -c "... check_fleet_audit_replication(Path(_REPO_ROOT)) ..."
FAIL | fleet_audit_replication | automation/fleet-audit is 5 commit(s) ahead of origin ...
```

**The fix is a `git push origin automation/fleet-audit`, and it is NOT this lane's to make.**
The contract says never push; `automation/*` is an EXPLICITLY PROTECTED branch
(`.claude/rules/git-discipline.md`, register `protocols/STANDING_RULINGS.md` I-D) whose whole
purpose is to live outside `main`; and the condition is machine-wide — three sibling lanes
(`lane-j-554-proof`, `seat-s1`, the primary checkout) were observed running their own
`audit.py health` gates concurrently, so this RED blocks every one of them identically.

**What was done instead: a scoped, declared `SKIP=audit-health` for the remaining commits.**
NOT `--no-verify`, which the contract forbids and which would also disarm `ruff`,
`validate-hermetization`, `block-commit-on-main`, the index/roster freshness gates and both
commit-msg gates. `SKIP=` disables exactly the one hook whose RED is proven foreign; the other
seventeen stayed armed and passing on every commit in this lane. This follows the recorded
precedent for a provably-foreign gate RED in a parallel arc: prove ownership first, then a
DECLARED skip — never a silent bypass, and never a disposition of someone else's finding.

**OWED TO THE INTEGRATOR:** push `automation/fleet-audit` to origin (5 commits) before the batch
closes. Until then `audit-health` is RED for every lane on this machine, and the ADR-80 durable
record genuinely does exist on one disk.

---

## STEP 8 — regenerate what the wiring moved, and only that

The contract names two regenerations. **One was owed and done; the other was not owed at all,
and U14 is why.**

**`ecosystem/doc-counts.md` — OWED, DONE.** Adding two test files moves the collected count:

```
before: - tests: **3033 collected** (`pytest --collect-only`)
after:  - tests: **3091 collected** (`pytest --collect-only`)
```

+58, which is the 21 + 37 test functions this lane added once parametrization is expanded. The
other two claims did **not** move, exactly as the spec predicted: `43 registered checks` (the
wiring adds no check) and `19 pre-commit gates` (it adds no hook). Regenerated with
`gen_doc_counts.py --write`, never hand-edited.

**The codemap — NOT OWED, and the gate itself says so.** U14 corrected the spec's claim that the
new `audit.py -> telemetry_emit` import edge changes the generated block. Run rather than argued:

```
$ python -m scripts.codemap.cli check . --source-root scripts
warning: orphan modules (no edges): codemap, toc
rc=0
```

Green with the wiring in place. The block records PACKAGES (`scripts/codemap/`, `scripts/toc/`)
and its Dependencies section is literally `- (none)`; two top-level modules cannot become nodes,
so no edge between them can appear. **This is the part that mattered:** `ARCHITECTURE.md` is in
`audit.py`'s `_FRESHNESS_FILES`, so an unnecessary regen would have bumped its commit date past
`last_reviewed: 2026-08-14` and RED-ed `canonical_freshness` A2 on the next commit — STEP 8 would
have wedged the lane on a re-stamp nobody had earned. The `codemap-freshness` pre-commit hook
still FIRES on every commit here (its `files` pattern matches `^scripts/.*\.py$`) and passes,
which is the difference between "the gate did not run" and "the gate ran and found nothing".

---

## STEP 9 — THE RECORDED GATE RUN, read back without re-measurement

This is `[#529]`'s own Done-when leg: *"a recorded gate run reads back without re-measurement"*.
One real run of the live gate, then SQL over the store — no check re-executed to produce any
number below.

```
$ python scripts/audit.py health --telemetry
... health: DEGRADED   (exit 1 — the foreign fleet_audit_replication FAIL, see above)
```

Readback, `sqlite3` only:

```
ROW COUNT            : 43
EVENT TYPES          : [('check_run', 43)]
DISTINCT CHECK NAMES : 43
OUTCOMES             : [('pass', 42), ('block', 1)]
TOTAL duration_ms    : 225318
```

**43 rows for 43 registered checks, 43 distinct names, one event per check.** The count agrees
with `ecosystem/doc-counts.md`'s `43 registered checks` without anyone counting them again.

Three sample rows, verbatim:

```
(15, '2026-08-19T12:00:26.749404+00:00', 'check_run', 'check_hooks_armed',
     'pass', 162, '{"finding_names": ["hooks_armed"], "findings": 1, "statuses": {"pass": 1}}')
(17, '2026-08-19T12:00:26.783382+00:00', 'check_run', 'check_doc_claims',
     'pass',  64, '{"finding_names": ["doc_claims"], "findings": 1, "statuses": {"pass": 1}}')
(37, '2026-08-19T12:00:27.116335+00:00', 'check_run', 'check_fleet_audit_replication',
     'block', 936, '{"finding_names": ["fleet_audit_replication"], "findings": 1, "statuses": {"fail": 1}}')
```

**The single `block` row is the STEP-1 mapping working on real data, not on a fixture.** The one
check that emitted a `fail` is the one that blocked the commit, and `context.statuses` preserves
the `fail` the three-value outcome collapsed — so a reader recovers the five-value status without
re-running anything. `finding_names` carries `fleet_audit_replication`, the string the disposition
register and the ship-gate key on, next to the function name `check_fleet_audit_replication` the
event is named by. That is the join the STEP-1 decision added `finding_names` for, exercised.

**And the store immediately answers a question nobody could answer before it existed:**

```
slowest 5 checks, by the store alone:
   90244 ms  check_journal_spine_anchor
   73184 ms  check_review_artifact_coverage
   18171 ms  check_handoff_probes
   17016 ms  check_doc_code_edge
    9756 ms  check_fleet_parity
```

Two checks are **73% of a 225-second per-commit gate**. That is the "is this organ worth its
cost" question the usage-telemetry memo exists to ask, and it is now measured rather than felt —
directly relevant to `[#528]`'s lane-latency row, which names `[#529]` as its leg-3 dependency.

### The two MEASURED blockers, verified on the real run rather than on a fixture

**Blocker (a) — stderr.** The full captured output of a 43-check `--telemetry` run contains
**zero** `telemetry: ` lines:

```
$ grep -c 'telemetry: ' <the whole run's captured output>   ->  0
```

Without the caller-side fix this would have been 43. The regression test
(`test_a_wired_health_run_puts_no_telemetry_line_on_stderr`) asserts the same property on
synthetic checks; this is the same property on the live gate.

**Leg 2 — the `.gitignore` glob**, with a real store on disk:

```
$ git status --short          ->  (empty)
$ git check-ignore -v logs/TELEMETRY.db
  .gitignore:95:logs/TELEMETRY.db*   logs/TELEMETRY.db
```

A live emitting gate leaves the working tree clean. That is the whole of leg 2, proven
end-to-end rather than by reading the pattern.
