# lane-y-752-declared-model-runs — end-of-lane packet

> **What changed · proposed diffs · open items.** Step 4 of lane
> `lane-y-752-declared-model-runs`, and the last act of the lane. Commit-and-STOP:
> nothing was merged into `main`, nothing was pushed, no index was regenerated, no
> JOURNAL entry was written.
>
> **Which part do you want first.** The integrator wants **PART 1** (three commits, what
> is in each) and **PART 6** (what is owed at the merge). A seat recording a receipt's
> model pair wants **PART 4** — verb, argument shape, what it refuses. A seat writing or
> freezing a lane contract wants **PART 3**, the corpus reading: nine live contracts
> declared a mode that has never reached a launcher argument.

---

## PART 0 — The hole, in one paragraph

A contract's routing row is a declaration. Until this lane nothing RESOLVED it into the
flags a launcher honours, and nothing VERIFIED that the lane which came back had run at
the tier that was ordered. The two halves compound: an order nothing resolves can be
silently re-decided by the launcher, and an order nothing verifies cannot detect that it
was. `lane-x-689-conductor-e-proof` is the witnessed case — it ordered `opusplan`, ran
`claude-sonnet-5`, and its receipt recorded the merge SHA, the suite verdict state, the
baseline attributed against and per-step minutes, but no field naming the model the work
was actually done at. An arc run at a tier nobody ordered was indistinguishable from the
arc that was ordered, and fed a median printed as the cost of that order.

---

## PART 1 — What changed

Three commits on `worktree-lane-y-752-declared-model-runs`, base `5cff84f6`.

```
b2d1bcdc  test(752)  RED-first witnesses across three modules, and row [#752]
cf17d449  feat(752)  mode-to-flag resolution, and the ran-model read
a9aa67a6  feat(752)  the ordered-not-equal-ran refusal on the receipt
```

Files, with what each gained:

- `scripts/dispatch_surface.py` (+355) — `resolve_launch()` turns a declared
  `(model, mode, effort, shape, slug)` into the flags that shape's launcher honours, or
  into refusals naming what cannot be honoured and why. `contract_findings()` reads a
  frozen contract and returns the same. A Click CLI: `resolve` prints the line, `check`
  reports refusals and exits non-zero.
- `scripts/routing_agreement.py` (+213) — `session_slug` / `transcript_paths` /
  `ran_models` / `ran_model` read a lane's OWN transcript out of the session store;
  `compare_order` is the PURE verdict over `(ordered, ran)`; `model_reading` is the two
  composed, with the tally riding the detail.
- `scripts/merge_receipt.py` (+148) — `Receipt.ordered_model` / `Receipt.ran_model`, a
  new **leg 4** in `incompleteness_reason()`, a MODEL line in `render_summary()`,
  `record_model_reading()`, and a `models` CLI verb.
- `tests/test_dispatch_surface.py` (+203, 17 tests) ·
  `tests/test_routing_agreement.py` (+129, 10 tests) ·
  `tests/test_merge_receipt.py` (+140, 12 tests) — the RED-first witnesses, written and
  committed before the code that turns them green (ADR-108 §B).
- `tasks/752-a-contracts-declared-model-and-mode-reach-no-fla.md` (new) +
  `tasks/manifest.json` + `BACKLOG.md` + `ecosystem/doc-counts.md` — row `[#752]` filed
  as the three acts it takes, and the two generated surfaces regenerated.

### The three design decisions worth reviewing

**1. The vocabulary is READ, never restated.** `MODEL_ENUM` / `EFFORT_ENUM` /
`MODE_ENUM` / `SHAPE_ENUM` and the routing-row grammar live in `gen_lane_contract`,
which owns them because it is what bakes them into a contract. `dispatch_surface`
reaches them through a lazy `_vocabulary()` — lazy because `gen_lane_contract` imports
`gen_handoff`, which imports back into this layer — and `_grammar()` turns a rename into
a loud `DispatchResolutionError` naming the missing symbol. A fifth copy of a launch
vocabulary is the exact defect this row was filed on.

**2. `background_honoured_modes()` is DERIVED, never listed.** A mode is honourable for
a `--bg` lane exactly when its `--permission-mode` is the one such a lane can run under.
A separate list would be free to drift, and a drifted list is how `plan` stayed
declarable-and-unresolvable for as long as it did. A mode in `MODE_ENUM` with no row in
the permission-mode table is a REFUSAL, not a default: defaulting the gap would silently
re-decide the mode, which is `[#717]` one field over.

**3. The order is typed; the run is READ.** `ordered_model` is an input, because a
contract's routing row declares it and nothing else can. `ran_model` has no flag — not
`--ran`, not `--ran-model`, not `--actual`, not `--force`, under any spelling, and a test
asserts each absence by name. A seat able to type what it wished had run would produce a
receipt that agrees with itself, and agreement with itself is exactly what x-689 already
had.

---

## PART 2 — The proofs, measured on the live tree

Every figure below was produced by running the shipped code in this worktree, not read
off a design note.

**The dispatcher, both directions.**

```
resolve  LANE-y-752-declared-model-runs.md
  -> claude --bg --model opus --effort xhigh --permission-mode bypassPermissions
     --worktree lane-y-752-declared-model-runs                              exit 0
     byte-identical to that contract's own ## Dispatch fence

check    LANE-x-689-conductor-e-proof.md
  -> REFUSED: "model 'opusplan' is INERT on a `--bg` lane: ..."             exit 1
```

**The transcript read, both directions, through the receipt CLI.**

```
models --slug y-752 --ordered opus     --worktree <this lane's worktree>
  -> agree -- ordered 'opus' and ran 'claude-opus-5'; tally claude-opus-5 x363    exit 0

models --slug x-689 --ordered opusplan --worktree <lane-x-689-conductor-e-proof>
  -> unverifiable-tier -- ordered 'opusplan', ran 'claude-sonnet-5': a SPLIT tier
     ...; tally claude-sonnet-5 x193                                              exit 1
```

**This lane's own arc is the positive control.** The contract ordered `opus`; the
transcript says `claude-opus-5`, 363 of 363 assistant messages. The organ discriminates
— it does not refuse everything.

**One correction to a figure this code quotes.** `BACKGROUND_INERT_MODELS` carries the
frozen audit measurement, *"84 of 84 assistant messages"*. Read live today the x-689
session store tallies **193**, still 100% `claude-sonnet-5`, still zero Opus. The
denominator grew because that directory accumulated later sessions; the conclusion did
not move. The constant keeps the audited figure because it cites an audit — the larger
live reading is recorded here rather than silently substituted for it.

---

## PART 3 — The corpus reading, and why this organ is wired into NO gate

`dispatch_surface.py check` was run over **every** launch-contract bundle in
`docs/audits/` — 18 bundles, 140 contract files.

```
older 9 bundles (2026-08-25 .. 2026-09-05):  74 read, 33 refusals
recent 8 bundles (2026-09-06 .. 2026-09-13): 66 read, 11 refusals
batch Y (2026-09-14):                         6 read,  0 refusals
```

The 33 in the older half are all one class — **no `| Model | Mode | Effort |` routing
row at all**, because those contracts predate the routing row being baked in, and some
of the files in those directories (`CUT.md`, `PLAN.md`) are not contracts. The 11 in the
recent half are the substantive ones:

- **NINE contracts declared `mode: plan` under `**Shape:** local`.**
  `LANE-v-000-offload-admission`, `LANE-v-000-shape-spec-clauses`,
  `LANE-v-000-window-rulings`, `LANE-v-642-assembly-debt-rows`,
  `LANE-v-643-enforcement-debt`, `LANE-v-664-delivery-spine`,
  `LANE-w-278-impacted-test-selection`, `LANE-w-684-pretooluse-guard-root`,
  `LANE-x-664-delivery-spine`. Every one of them dispatched byte-identically to
  `execute`: `MODE_ENUM` has carried `plan` since it was written, and nothing anywhere
  ever turned that column into a launcher argument. This is the second defect, and it is
  MEASURED rather than hypothesised — nine lanes ordered a mode the launcher has never
  once honoured.
- **TWO carried `opusplan` onto a `--bg` line** — `LANE-x-664-spine-armed` and
  `LANE-x-689-conductor-e-proof`, the second being the lane the measurement comes from.

**Zero contracts in the whole corpus were refused by the fence-drop leg.** That leg
guards against a `## Dispatch` fence that omits `--model`, `--effort` or
`--permission-mode` — the defect the generator once had. It found nothing today, so it
is a regression guard rather than a live finding, and this packet says so rather than
letting a clean run read as a catch.

**This is exactly why nothing arms it.** Lane contracts live in immutable audit bundles,
and the corpus holds contracts that legitimately froze values this organ now refuses —
x-689 among them, by operator ruling on the day. Armed tree-wide, `contract_findings`
would refuse 44 frozen artifacts: a ratchet against the record rather than a check on
new work. The organ therefore ships as a library plus a CLI, wired into no hook, and
says so in its own docstring. **Where it belongs is FREEZE time**, beside
`gen_lane_contract.check_contract`, which refuses a contract as it is written — and that
is a change to a module outside this lane's declared footprint. It is PART 5 item 1.

---

## PART 4 — For the seat recording a model pair on a receipt

```
merge_receipt.py models --slug <slug> --ordered <tier> [--worktree <dir>]
```

Four things to get right:

1. **`--ordered` takes the contract's tier, not a model id.** `opus`, `sonnet`, `haiku`.
   A tier outside that set is REPORTED (`unknown-tier`), never guessed at.
2. **There is no flag for what ran, and that is the design.** The verb reads the session
   store or it records the gap.
3. **`--worktree` defaults to the repo root.** A lane reading its own arc can omit it.
   An integrator recording an arc is not standing in that arc's worktree and must name
   the directory — the transcript is filed under the session's WORKING DIRECTORY, so a
   lane that ran elsewhere files nowhere the reader looks. That absence is reported with
   the slug it looked under, so it is diagnosable rather than mysterious.
4. **Exit follows the STATE: 0 only on `agree`.** A gap exits non-zero too (Z-G4) — a
   check that cannot compute its ground truth must not read as a pass to anything
   shelling out to it.

**What leg 4 refuses, and what it lets through.** It fires on both `merge` and `arc`
receipts, and skips on exactly one state: `unread`, meaning the receipt carries NEITHER
field. That is the `[#750]` scoping decision re-made — every ledger row written before
these fields existed carries neither, and refusing a corpus of clean merges to arm a new
field is `Verdict.ok`'s trap with a new field in it. Everything else is a reported gap:
a divergence, a half-recorded pair (one field without the other), a split tier no
transcript can discharge, a tier the reader does not know. **Silence is not agreement** —
an empty tally agrees with every order ever placed.

Leg 4 binds an ARC as well as a MERGE deliberately. Legs 5 and 7 are merge-only because
an arc reads no Actions run and pays no teardown; but an arc is ordered at a tier exactly
as a merge is, and `lane-x-689` WAS an arc. Scoping the model leg to merges would have
put the witness that motivates it outside the predicate it motivates.

---

## PART 5 — Proposed diffs (NOT made by this lane, and why)

Each is outside the declared footprint. None was started.

1. **Arm the contract check at FREEZE time.** Add the `dispatch_surface.contract_findings`
   call to `gen_lane_contract.check_contract`, so a contract is refused as it is written
   rather than after it has been frozen and dispatched. This is the wiring that makes
   PART 3's nine `mode: plan` contracts impossible to produce again. Out of footprint:
   `scripts/gen_lane_contract.py`. Sized S — one call and its test.

2. **Decide what `mode: plan` should DO for a background lane.** This lane refuses it
   with a remedy in the text (*"Declare `execute` and let the contract BE the plan, or
   dispatch this at an attended shape"*), which is the honest answer for a column nothing
   honours. The alternative — resolving `plan-then-auto` to a real two-phase dispatch —
   is a launcher capability question, not a dispatcher one, and belongs to whoever owns
   the dispatch verbs. **A functional question, ADR-108 §A: the operator rules it.**

3. **Have `/lane-integrate` record the pair.** The receipt can now hold it and the CLI
   can now read it; nothing calls the verb during the merge walk. One line in the
   integrator's checklist per lane. Out of footprint: `.claude/commands/lane-integrate.md`.

4. **The x-689 receipt, if one is ever written.** Reading that arc today yields
   `unverifiable-tier`, which under leg 4 makes the receipt INCOMPLETE. That is correct
   and should stay correct: the arc happened, its minutes are real, and what it cannot
   do is stand as a measurement of the order it was given.

---

## PART 6 — Open items and what is owed at the merge

**The lane SYNCED onto main at the end, and the two generated files were resolved by
hand.** This lane's base is `5cff84f6`; `main` moved under it twice during step 4 —
`b864e7d0`, then `5bf1236c` — as the integrator landed its census-row and regeneration
work. The step-4 commit was then blocked by `audit-health`:
`journal_spine_anchor: 5bf1236c carries no JOURNAL anchor`. The check's own two-leg
diagnostic was run unmodified and returned `anchored in this tree: False` /
`anchored at main: True` — the tree-lag PHANTOM, not a gap, and `git merge main` is the
recorded fix for exactly that answer. It is at `c41f993d`.

Two generated files conflicted, and **neither was regenerated over its markers** —
regenerating a conflicted generated file absorbs the `<<<<<<<` text into the output,
turning a visible conflict into silent corruption. The markers were stripped first, one
hunk each, and only then were the generators run:

- `tasks/manifest.json` — one hunk, the `generated_sha256` line. Every node merged
  cleanly; main's census rows and this lane's `[#752]` are all present.
  `gen_task_tree.py --emit-source` re-pinned the digest: *BACKLOG.md already current
  (331 tasks)*.
- `ecosystem/doc-counts.md` — one hunk, the collected-test count: 5904 (this lane) vs
  5900 (main), two claims about a tree that is now neither. `gen_doc_counts.py --write`
  measured the merged tree: **5938**.

Verified after resolution rather than assumed: zero markers left in either file,
`"task": 752` still in the manifest, the row still rendered in `BACKLOG.md`. A sync that
silently dropped this lane's own row is the worst outcome available at that step, so it
was checked.

That conflicted merge required an explicit `git commit`, which means it **ran the full
pre-commit stack** — a plain `--no-ff` merge runs none — and `audit-health` passed armed
on it, confirming the phantom was the lag and nothing else.

**Regenerated surfaces, declared.** `BACKLOG.md` (+1 line) and `ecosystem/doc-counts.md`
were regenerated by this lane because filing row `[#752]` and adding 39 tests moves both,
and the commit gates require them current. No other index was touched — the audits index
in particular was not regenerated, per the contract's own prohibition, and it does not
need to be: `audit-index-freshness` is scoped by `[#590]` to the index and its generator,
so this packet's own file does not trip it.

**No hook skip is declared by any commit in this lane.** All three commits ran the full
33-hook stack armed, all Passed, and `--no-verify` was not used anywhere.

**The whole impacted selection was run, and every red was attributed by PAIRED RUN
rather than by argument.** `impacted_tests.py select` over this lane's three changed
modules returns **66 files**. All 66 were run in this tree:

```
files  1..32   2603 tests   1452 passed   22 failed   17 skipped   16m40s (-n 6)
files 33..66   1126 tests   1121 passed    5 failed    5 skipped   16m39s (-n 6)
                            ----------    --
                            2573 passed   27 failed  (26 distinct tests)
```

Every one of the 27 was then re-run at `5cff84f6` — this lane's base, in a throwaway
detached worktree on the same box, minutes apart — and **every one reproduced, name for
name**:

```
test_governance_health.py         7  AttributeError: 'NoneType' has no attribute 'strip'
test_gen_handoff.py               5  probe counts 15!=13, 6!=5, live FM-2 unavailable
test_funnel_lifecycle.py          4  LifecycleUnreadable: docs/intake/2026-09-11-tech-...
test_canonical_docs.py            2  PLAYBOOK stamp / derived-leg class
test_audit.py                     1  live fleet not green (settings-local-block)
test_doc_code_edge.py             1  assert 4 == 1
test_enforcement_coverage.py      1  anchor-gate probe
test_funnel_coverage.py           1  committed baseline vs live measurement
test_stale_worktrees.py           1  linked-worktrees reader vs the primary
test_reverse_dep_oracle.py        1  assert 3 == 1
test_validate_doc_rot.py          1  citation regex false-strips 5 identifiers
test_v6_frozen_contract.py        1  R6 unbuilt: --repo-root + --cross-repo rejected
test_routing_agreement.py         1  the live routing table (see below)
```

Not one is attributable to this lane's diff. `test_stale_worktrees` is worth a note: it
fails in ANY linked worktree, and in the baseline run its assertion named the throwaway
worktree's own path — it is sensitive to where it runs from, not to what changed. Both
throwaway worktrees were removed and each removal verified; the provision→cleanup
round-trip left the tree identical.

**One pre-existing red INSIDE a file this lane edited, reported and not fixed.**
`tests/test_routing_agreement.py::test_the_live_table_is_well_formed` (line 109) asserts
`roles["adversarial"] == ["sol"]` while `ecosystem/routing-table.yaml` binds that row to
`codex` — REBOUND 2026-09-05 per architect inbox 002-B, the yaml itself saying *"Restore
`sol` here once it is installed"*. This lane added tests to that file and did not touch
that one; the fix is a one-token edit to either the test or the table, and choosing which
is a ruling about whether `sol` is coming back. **Out of footprint, so reported rather
than decided.**

**Test results for this lane's own surface**, re-run in the MERGED tree after the sync
above, so the figure describes what the integrator will merge rather than what this lane
had before it:

```
tests/test_dispatch_surface.py + test_routing_agreement.py + test_merge_receipt.py
  129 passed, 1 failed   -- the one failure being the pre-existing routing-table row
ruff check (all three modules)   All checks passed!
```

The 66-file impacted selection and its paired baseline were measured at `a9aa67a6`, this
lane's tip before the sync; the sync brought in main's `[#751]` and `[#761]` work, which
this lane does not touch and did not re-measure. The full suite runs once, at
integration, which is where that measurement belongs.

---

## PART 7 — Decision-budget report (V-2)

Nothing was escalated, because nothing fell in the three escalating classes. No curated
baseline was touched, no rule-vs-ruling conflict arose, and every fork below had a
standing ruling to decide it. Per V-2 these are **reported here rather than asked**:

1. **Step 3 was pulled forward, ahead of step 2.** Forced by the tree, not chosen:
   `graph-task-coverage` refused `tests/test_dispatch_surface.py` at step 1 because no
   OPEN row claimed it, and `[#717]` — the only other row the file named — is closed. The
   row had to exist before the witnesses could commit. Contract content unchanged; only
   the order of two commits moved.
2. **`contract_findings` wired into no gate.** Decided on the corpus measurement in
   PART 3, recorded as proposed diff 1 rather than done silently.
3. **`record_model_reading` records no `StepTiming`.** A `StepTiming` would add the
   duration of a directory read to `recorded_seconds` and shift the
   baseline-commensurable split. The reading is a fact ABOUT the arc, not a step OF it —
   as `merge_sha`, the other fact about the arc, is a field and not a step.
4. **`opusplan` reads as `unverifiable-tier`, not as its Sonnet half.** Accepting
   `claude-sonnet-5` as agreement with `opusplan` would certify the exact collapse that
   made the x-689 window advisory; refusing it as divergence would wrongly refuse an
   attended seat that finished its plan phase. Z-G4 already names the honest third
   answer: a reported gap.
5. **An unparseable JSONL line is skipped, not fatal.** A live transcript is appended to
   while it is read, so its last line is routinely half-written. Refusing the file on one
   would make every reading of a running lane report nothing — an absence manufactured by
   the instrument, which is the failure this organ exists to avoid on the other side.
6. **A refused launch emits NO flags.** Emitting the survivors would hand a seat a line
   that is most of a command, which is how a partial refusal becomes a launch.

No premise of this contract was refuted, so no PAUSE was owed (Q10).
