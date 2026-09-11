# X1-1 close packet — `decision_coverage` arms, and 112 decided-but-unscheduled things become countable

<!-- lane lane-x-692-decision-coverage, branch worktree-lane-x-692-decision-coverage ·
     contract LANE-x-692-decision-coverage.md (frozen) · batch X slot X1-1 · row [#692] ·
     cited by tasks/692-decision-coverage-a-decided-thing-is-never-unscheduled-again.md -->

## 1 · What this lane did

Built `decision_coverage` — the organ that refuses when an **accepted decision has neither an
implementing row nor a written "no implementation required" disposition** — and wired it into
four consumers: a pre-commit refusal, a handoff-bundle artifact, a handoff onboarding probe,
and the SessionStart digest. Filed the two rows the contract orders (`[#735]`, `[#736]`) and
wrote X1-1's six carried AX clauses into `[#692]`'s own row.

Four commits, in the contract's order:

```
0f3b726d  docs(batch-x): file [#735] and [#736], and write X1-1's six AX clauses into [#692]
e0349ba9  test(decisions): RED-first witnesses for decision_coverage -- A9-1..A9-3
82f6a8a0  feat(decisions): decision_coverage refuses an accepted decision no row implements
1f9a18da  feat(decisions): the handoff carries the decision ledger and fleet_health reports A9-3
```

A fifth commit lands this packet and the one fixture correction the closing full-suite
comparison earned (§4 item 4).

**The measurement that made this row worth building**, taken on the live tree:

```
decisions accepted-but-unexecuted : 112
oldest                            : 143 days
carrying an implements: key       : 0   (the key did not exist)
```

## 2 · What changed

### New

- `scripts/decision_coverage.py` — the organ. Population from the **documents**, relation from
  the **persisted store**. The split is the design, not a compromise: FPG-1 mints `adr:N` only
  for an ADR something *cites*, so a query reading its population off the graph would be
  structurally blind to the uncited, unimplemented decision this organ exists to find.
- `tests/test_decision_coverage.py` — 65 witnesses. 51 written and run RED before any build
  code existed (ADR-108 §B); 14 more for the step-4 wiring.
- `docs/audits/2026-09-11-technical-x1-1-decision-coverage-close-packet.md` — this file.
- `tasks/735-…` (AX4-1 floor declaration, with AX8-4, AX9-4, AX10-3 folded in) and
  `tasks/736-…` (AX13-1, component lifecycle as data), filed per AX12-1.

### Changed

- `scripts/file_purpose_graph.py` — **FPG-1 INPUT 8**, `decision-implements`. Added to the
  graph and not to a script (ADR-118 §1). Runs ROW → DECISION, one direction only, over
  **every** row open or closed; the row's status rides in the edge `detail`.
- `scripts/gen_task_tree.py` — derives the `implements:` frontmatter key from a `· implements:`
  body clause, exactly as `depends-on` and `serialize-group` are derived, because leg-2
  frontmatter honesty re-renders every task file from its own body and refuses a byte
  difference. A key with no deriver would be hand-editable, inert and silently wrong.
- `scripts/validate_backlog.py` — owns the key's **grammar** (`ADR-n | intake-n | DECLARE-… |
  AMEND-…`, case-sensitive, fullmatch) and **reference existence**. A transport token is
  grammar-checked only, stated rather than silently skipped.
- `.pre-commit-config.yaml` — `decision-coverage`, immediately before `impacted-tests-guard`.
- `scripts/gen_handoff.py` — `_write_decision_ledger` (A9-2's artifact half).
- `scripts/verify_handoff_probes.py` — `_undisposed_decisions`, the `P13-decision-ledger` rung
  (A9-2's probe half).
- `scripts/fleet_health.py` — `decision_health_line` (A9-3).
- `tasks/692-…` — the AX12-1 carriage block, `implements:`, the AX9-4 discharge, `floor: hub-only`.
- `tests/test_file_purpose_graph.py` — the `len(INPUTS)` pin, 7 → 8.

## 3 · Decisions made under the V-2 budget, reported here rather than asked

None of the six is a curated-baseline touch, a rule-vs-ruling conflict, or a fork class with no
standing ruling — the only three classes the budget escalates on.

### 3.1 · The era bound — `ARM_DATE = 2026-09-11` bounds the REFUSALS and nothing else

112 accepted decisions carried no `implements:` key because the key did not exist. An unbounded
commit-tier refusal would refuse **every commit in the repo** on a defect the committer cannot
legally repair — the argument `audit.py` already settled by keeping `check_funnel_lifecycle` at
SHIP rather than COMMIT tier, and `consumer_at_landing.ARM_DATE` is the precedent in terms.

So the bound applies to the gates only. The **ledger lists** the whole population, the **metric
counts** it, and `Metrics.grandfathered` states on every run the size of what the gate declines
to refuse. A bound that is not measured is an exemption. It is pinned from both sides by tests
so it can neither widen into a wedge nor quietly evaporate.

### 3.2 · The transport class collapses onto P11 rather than growing a rival predicate

A `DECLARE-`/`AMEND-` whose `carried-by:` resolves on `main` has landed as an in-repo object
this population already measures on its own terms, so the file is `done` and the question has
**moved** rather than been dropped. Measured: 95 of 104 resolve, 7 carry no key, 2 are OPEN. Of
the nine undischarged, eight predate ARM_DATE and exactly one is in-era —
`AMEND-CV-V10-001`, which the batch X manifest §4 already rules OUT OF POPULATION as another
workstream. That quoted ruling is the disposition register's **only** entry. A register with one
earned row is the difference from a set of paper suppressions.

### 3.3 · `floor: hub-only` for `decision_coverage` (AX4-1, applied to this lane's own output)

The population includes the `CLAUDE_PROMPTS_DIR` transport and the intake funnel's ACCEPTED
tier, and no consumer carries either. Promotion to MUST is `[#735]`'s to carry. **No
`ecosystem/parity-surfaces.yaml` row was written** — a parity row for a component whose
declaration mechanism does not exist yet would RED the sweep on a key nothing reads.

### 3.4 · `fleet_health` reads the two in-repo classes only, and the line SAYS SO

Measured: the transport leg costs **~23 s**, the two in-repo classes **~1.4 s**. The cost is
P11's existing `gen_handoff.carriage_verdicts`, which spawns one `git cat-file` per carrier
token across ~96 transport files. SessionStart runs on every session and cannot pay that.

The narrowing is **labelled** (`Metrics.transport_measured`) rather than left to be inferred,
and that is not decoration: `executing` and `done` are carried almost entirely by the transport
class, so an unlabelled narrow line would print two clean-looking zeros that are false as
statements about the repo. The whole population stays one command away
(`decision_coverage.py metrics`) and rides in every bundle's `DECISION_LEDGER.md`.

### 3.5 · A stale store is REPORTED at session start, never rebuilt

Measured: a cold graph rebuild is **~16 s** against ~1.5 s warm. The rebuild belongs to the
`graph-rebuild` pre-commit hook that owns it (`[#664]` clause 1) and is paid there at the next
commit either way. But "not measured" and "nothing to report" are different facts, so the line
says which one it is rather than falling silent. New predicate `store_is_stale`, documented as
something a **gate never calls** — `check` still goes through `ensure` unconditionally, because
a stale graph does not fail, it answers wrongly.

### 3.6 · `STANDING_RULINGS.md` is deliberately NOT in the population

`[#721]` owns that fourth class. Counting it here would have built a second definition of the
same thing against a row already filed for it.

## 4 · Five defects found and fixed during the build

All five were found by a **live witness, the suite, or a run against `main` for comparison** — none by review —
and all five were fixed in the module or the fixture rather than in an assertion.

1. **`stale_dispositions` reported every transport disposition as stale whenever the transport
   was not measured.** "Absent" and "not measured" are different facts (DEFECT E-29), and a
   register that self-reports as rotten whenever `CLAUDE_PROMPTS_DIR` is unresolved is a
   register nobody reads. A class that was not measured is now not judged.
2. **An OPEN implementing row now OUTRANKS a resolving carriage.** Reading carriage first made
   every carried AMEND `done` the moment its text landed — including ones whose lanes were
   still running, which is precisely the decided-and-unscheduled blindness this organ removes.
3. **The ledger writer touched trees it was only reporting on.** Resolving the population calls
   `graph_store.ensure`, which creates `<repo>/.git/fpg-graph/FPG.db` — and in a tree with no
   git history that *materialises a `.git` directory*, after which `_tracked_under` stopped
   short-circuiting on "not a git repo" and raised `BundleCollisionError`. Six regeneration
   tests went red on a side effect of a surfacing artifact. Now HUB-ONLY by `_is_hub`, which is
   the correct scoping on its own terms too.
4. **This suite held the live graph store open for the whole session.** `live_store` was
   session-scoped, so under xdist one worker held the store's `-wal` open for twenty minutes
   while a sibling worker tried to rebuild it — and on Windows `gs.ensure`'s swap-into-place
   cannot proceed against an open reader. Six `tests/test_graph_spine.py` tests raised
   `StoreUnreadable` on this branch and on neither `main` nor a serial run. A test file that
   reds other people's tests by existing is a defect in the test file. The store is now opened
   for as long as a read takes and closed; the **population** is computed once and carried
   instead of the handle.
5. **The probe rung imported the organ before checking its scope.** `decision_coverage` pulls in
   `file_purpose_graph` and through it `validate_backlog`; a fixture repo that puts its own
   `scripts/` on `sys.path` resolves that chain to a one-line stub and raises `NameError`. None
   of the rung's three bounds needs the organ in order to decide, so scope is established first.

## 5 · Proposed diffs — repairs this lane did NOT make, with owners

Every item was **measured**, not assumed. The five `tests/test_gen_handoff.py` REDs were proven
inherited by extracting `main` with `git archive main | tar -x` into a scratch tree and running
the same five there: byte-identical assertions, on a tree this lane has never touched.

### 5.1 · `scripts/graph_queries.py` — `ORPHAN_DISPOSITIONS` names a deleted file

- **RED:** `tests/test_graph_spine.py::test_the_disposition_register_names_no_file_that_is_gone`
- **Cause:** the register names `.claude/commands/override.md`, deleted on `main` by `5e17ecd7`
  (`[#683]`, batch W).
- **Repair:** remove that one dict entry.
- **Owner:** the live `[#664]` sibling lane — `graph_queries.py` is its file. Editing it here
  would break the no-edits-outside-footprint rule *and* guarantee a conflict on that lane's
  register.

### 5.2 · `tests/test_gen_handoff.py` — the v7.1 probe-row pins were never updated

- **REDs:** `test_dogfood_no_probe_row_carries_an_answer_value` (asserts 13, actual 15),
  `test_dogfood_generated_bundle_has_no_failing_probe` (13 / 15),
  `test_epic_bundle_has_no_failing_probe` (5 / 6),
  `test_suffixed_bundle_probes_resolve_against_their_own_directory`.
- **Cause:** `5cb41d6b` ("v7.1 pack — probe-core is rows, P8 gains a second leg, P11 lands",
  2026-09-07, on `main`) took the v5 template from 13 rows to 15 (`P8b`, `P11`) and the epic
  template from 5 to 6. The three count pins and the P8b source anchor
  (`protocols/OPERATOR-INTERFACE.md`) were not moved with them.
- **Repair:** update the three counts and resolve or degrade the `P8b` source.
- **Owner:** the v7.1 arc.

### 5.3 · `docs/intake/2026-09-11-tech-batch-x-roster.md` — unparseable YAML frontmatter

- **RED:** `tests/test_gen_handoff.py::test_funnel_health_renders_no_unavailable_against_the_live_repo`
- **Cause:** `mapping values are not allowed here`, **line 4, column 697** — an unquoted `rows:`
  inside the long plain-scalar `origin:` value. `funnel_lifecycle` therefore raises
  `LifecycleUnreadable` (Z-G4) on the live tree.
- **Second, unlogged consequence:** `fleet_health`'s `[funnel]` digest line is **silently absent
  at every SessionStart today**. It is fail-soft, so nothing is red at the boot surface and
  nothing says so. Every FM-2 field in a generated bundle's `FUNNEL_HEALTH.md` reads
  `unavailable` for the same reason.
- **Repair:** one pair of quotes around the `origin:` value.
- **Owner:** batch X lane 0 (`lane-x-000-batch-x-roster-lands`, intake 93).

### 5.4 · `BACKLOG.md` is over its byte bar

- **RED:** `tests/test_gen_task_tree.py::test_the_live_view_is_under_the_589_done_when_byte_bar`
- **Cause:** 88,956 B on `main` against a 72,000 B bar — already breached by **16,956 B** before
  this lane existed. This lane's delta is **+464 B**, from the two rows step 1 of the contract
  orders it to file.
- **Owner:** LEDGER row **D8**, status OWES-OPERATOR. Grooming is archival and archival is
  D6/D7.

### 5.5 · Two generated indices are stale — the integrator regenerates once at the merge

- `ecosystem/organ-index.md`: stale for **two** reasons and only one is this lane's. On `main`
  it still carries a `/override` command row and claims `command 13`, while
  `.claude/commands/override.md` was deleted by `5e17ecd7` (`[#683]`, batch W); this lane adds
  the `decision-coverage` git-hook row (git-hook 29 → 30).
- `ecosystem/doc-counts.md`: `pytest_collected` 5752 → 5817 and `precommit_hook_count` 29 → 30.
- **Owner:** the integrator (Q1 — gate-of-record, one regeneration on the merged result).
  Regenerating here would land batch W's correction under this lane's id.

### 5.6 · `gen_handoff._resolves_on_main` is not memoized — the ~23 s

- **Cause:** one `git cat-file -e main:<token>` subprocess per carrier token, ~96 carriers.
- **Consequence:** a handoff cut now pays it twice (leg 2 at assemble time, and the ledger);
  on the unsealed path the two `verify_handoff_probes` rungs each pay it once. Recorded as an
  HONEST LIMIT in both docstrings rather than fixed.
- **Repair:** memoize the predicate for the life of one process. Tokens repeat heavily across
  carriers (`docs/decisions/`, `tasks/`, …).
- **Owner:** P11 / `[#643]` — `gen_handoff.py`'s carriage leg, outside this lane's footprint.

## 6 · Open items owed by this lane

1. **Relocate `DECISION_DISPOSITIONS` out of the module.** It is a one-entry dict in
   `scripts/decision_coverage.py` today. `graph_queries.ORPHAN_DISPOSITIONS` sets the precedent
   and `[#736]` §"the manual precursor" names the same hazard: a hand-curated register inside a
   module has no time axis and no schema. The destination is a data file
   (`ecosystem/disposition-register.yaml`), designed together with `[#736]`'s `lifecycle:` key
   and `[#735]`'s `floor:` key rather than three times separately.
2. **`floor: hub-only` is a declaration with no mechanism yet.** `[#735]` carries the promotion.
   Nothing reads the key until AX4-1's declaration surface exists.
3. **`tests/test_decision_coverage.py` takes ~3 minutes**, almost all of it the session-scoped
   live-transport fixture paying §5.6's cost. It shrinks to seconds the moment that is fixed.
4. **The `implements:` key is in use on three rows only** — `[#692]`, `[#735]`, `[#736]`, the
   rows this lane owns. Every other accepted decision is grandfathered and countable. Closing
   that gap is what the ledger and the metric exist to drive, one batch at a time.

## 7 · Evidence

```
live population            : 112 accepted / 7 executing / 81 done / oldest unexecuted 143d
                             (112 grandfathered)
transport carriage         : 95 resolves / 7 no-key / 2 OPEN, of 104
disposition register       : 1 entry (declare:AMEND-CV-V10-001), reason + owner both present
FPG-1 inputs               : 8, set-equality asserted against the live tree
pre-commit hooks           : 30
witnesses                  : 65 in tests/test_decision_coverage.py, all green
lane suites at close       : 412 passed (decision_coverage, verify_handoff_probes,
                             fleet_health, file_purpose_graph)
inherited REDs             : 6, each proven on `main` and listed in §5 with an owner
bypasses declared          : doc-counts-pytest-freshness (3 commits), organ-index-freshness (1)
```
