# Lane z-0 — the quality-requirements register: end-of-lane packet

**Lane:** `lane-z-0-quality-requirements` · **Branch:** `worktree-lane-z-0-quality-requirements`
**Row:** `[#765]` · **Decision budget:** V-2 · **Date:** 2026-09-15
**Implements:** AMEND-NIGHT-PLAN-002 (AN2-1 … AN2-5), AMEND-NIGHT-PLAN-001
**Consumers:** `[#765]` — this lane's row; and `[#782]`, the duplicate the dispatcher filed
(see *Open items* 1, which the integrator resolves)

---

## 1. What changed

Six commits, each a whole act, plus one sync merge.

`docs(765)` — the row, filed FIRST as the contract's step 1 requires: `tasks/765-…md`, a
`tasks/manifest.json` node at the `[S3]` story position, and `BACKLOG.md` regenerated.

`feat(765)` — `ecosystem/quality-requirements.yaml`, the register itself, seeded from
AN2-2's four MEASURED attributes.

`feat(765)` — tonight's four availability findings, each entered as its own requirement
rather than folded into one.

`Merge branch 'main'` @ `0ee3d161` — spine sync, forced by `journal_spine_anchor`. Two
conflicts in the generated BACKLOG pair, both resolved by hand rather than by regenerating
over the markers; the `[S3]` node hunk was an addition on both sides and all three nodes
(765, 782, 783) were kept. See *Open items* 1 and 2b.

`feat(765)` — the register becomes READ: `scripts/quality_requirements.py`,
`tests/test_quality_requirement_trips.py`, `tests/test_quality_requirements.py`, the
`quality-requirements-freshness` pre-commit hook, the generated `ARCHITECTURE.md` section,
and one `not-an-edge` verdict row in `scripts/graph_queries.py` (*Open items* 5).

`feat(765)` — the floor declares the register a MUST:
`templates/child-methodology-floor.md.tmpl` gains one section,
`templates/child-methodology-floor.sha256` moves `4d268f32..` → `e8c62d24..`, and
`deploy/manifest-v1.5.0.yaml`'s `anchors.floor_sha256` is re-pinned to match.
Budgets measured, not asserted: **887 → 1211 tokens** against the 1500 ceiling, F5 clean,
no URLs, and the silent-rule ratchet **428 → 429** against a baseline of 447 — the one
token is the tier word `MUST` itself, spelled out so the register's `declared_in:` resolves
to something a reader can grep rather than infer. `release_lint --version v1.5.0` reports
`C5-floor-pin: … == sidecar == template bytes`, 0 FAIL.

`docs(765)` — this packet.

### The register, as it stands

Sixteen requirements over four attributes. **Four are `measured`**; twelve are
`candidate`. The split is the artifact, not the count:

```
QR-PERF-001   measured   scripts/impacted_tests.py      a changed script selecting zero tests is refused
QR-AVAIL-001  measured   scripts/seat_refusals.py       a wait with no declaration inside _WAIT_WINDOW is refused
QR-OBS-001    measured   scripts/merge_receipt.py       a merge with no complete receipt is refused
QR-OBS-002    measured   scripts/provider_registry.py   a model with no price is refused
QR-PERF-002/003/004       candidate
QR-AVAIL-002 … 008        candidate
QR-RES-001                candidate
QR-OBS-003                candidate
```

A `candidate` carries **no** `organ` field. That asymmetry is enforced, not conventional:
the schema leg refuses a candidate that names one, with a negative control
(`test_a_candidate_that_names_an_organ_is_REFUSED`) proving the refusal fires.

### The leg that makes `measured` mean something

The done-contract's words: *"a `measured` entry whose trip-test passes unconditionally is a
REFUSAL, not a pass."* A path check cannot see that, so each trip body is written as a
**function of its organ** — `trip_qr_perf_001(organ, tmp_path)` takes the thing it tests as
an argument — and is run twice: against the live organ, where it must pass; and against a
**neutered stand-in**, the real module with exactly one refusal replaced by a permissive
one, where it must raise `AssertionError` carrying the word VIOLATED.

`AssertionError` specifically, and the marker specifically. A trip that blew up with a
`TypeError` against the stand-in would also "fail", and would prove the stand-in malformed
rather than the trip attentive.

Every trip also carries a **conforming control** — a covered script, a declared wait, a
complete receipt, a priced model — because a gate that refuses everything satisfies a
refusal test and is as useless as one that refuses nothing.

23 tests. Green.

---

## 2. Proposed diffs — found here, NOT repaired here

Each is outside this lane's declared footprint. They are recorded, not done.

**(a) `ARCHITECTURE.md` pins a superseded manifest's carrier count, twice.** Ch4's
deploy-orchestrator bullet and the ADR-92 entry under Governing ADRs both read
*"(v1.4.0: seven declared, six implemented: true, editor-config false)"*. Measured live:
v1.4.0 declares 7/6, and the **current** manifest v1.5.0 declares **9/6** — `boot-inversion`
and `conductor` joined and are `implemented: false`. Both sentences pin a count from a
superseded manifest one clause after telling the reader to read the live roster instead,
which is the anti-pattern they are warning about. Found by reading the file end to end for
the `last_reviewed` stamp, which is what the stamp is supposed to buy.

**(b) `scripts/graph_queries.py` restates its own register's size in prose, and the number
is stale.** `EDGE_COMPUTATIONS`' docstring says *"The twenty-one verdicted sites"* and
`test_edge_class_census.py` says *"Twenty files, twenty-one rows."* The register held 22
rows before this lane touched it — the self-catch row that the query's own arming commit
forced. It now holds 23. The two pinned numbers that matter (`private == 18`,
`reconciled == 3`) are correct and untouched; only the prose counts drift. This is the
repo's own "never restate a count in prose" rule, unenforced on the module that enforces
counting rules. Not repaired here because the drift predates this lane and the file is
another lane's surface.

**(c) The register's first finding about itself: the memory floor has no organ.**
QR-RES-001 — *"a lane does not start when free memory is below the floor"* — is a
`candidate`, and it stays one because **nothing reads free memory**.
`seat_refusals.lane-ceiling` refuses on a lane **count**, which is a proxy that fails in the
direction that hurts: six small lanes pass the ceiling and exhaust the box, one large lane
fails it and would have been fine. AN2-2 lists resource-control as a measured attribute
because the *incident* was measured; the *enforcement* was not. This is exactly the entry
the `candidate` status exists to hold honestly, and it is the strongest argument the
register makes for its own shape.

---

## 3. Open items — for the integrator

**1. `[#765]` and `[#782]` are the same row, and `[#782]` says so.** While this lane was
filing, main landed `tasks/782-the-quality-requirements-register-…md`, filed by the
dispatcher at freeze with the same title, the same theme/story, and a Done-when that is
this lane's done-contract. Its body names the resolution and the resolver: *"this is a known
duplication risk the integrator must resolve: lane 0 is instructed to file or amend its own
row as its first commit and cannot see this branch… If it did, AMEND that row into this one
rather than keeping both."* The lane leaves both standing — closing or merging a row is the
integrator's act, and the instruction is already written. **Every artifact this lane
produced cites `[#765]`**, so the amend direction that costs least is `[#782]`'s body
absorbing `[#765]`'s, keeping `[#765]` as the live id; the opposite direction requires
rewriting the commit trail's citations.

**2. Two index hooks are owed at integration**, declared by name in each commit body rather
than bypassed with `--no-verify`:

- `SKIP=doc-counts-pytest-freshness` — 23 tests added, so the `pytest_collected` claim in
  `ecosystem/doc-counts.md` trails the tree.
- `SKIP=organ-index-freshness` — fired twice, for two different files in the hook's trigger
  set. `.pre-commit-config.yaml` gained a hook, so `ecosystem/organ-index.md` is stale by
  exactly one organ; and the floor commit edits `deploy/manifest-v1.5.0.yaml`, which the
  same hook watches.

Both are one act on the merged tree and a conflict surface per lane, which is why the
contract reserves them to the integrator.

**2b. `audit-health` is skipped on this lane's later commits, and the gap is MAIN'S.** This
is the one skip the lane did not plan for, so it is reported with its evidence rather than
its conclusion.

The lane's fourth commit was refused by `journal_spine_anchor` with **four** unanchored
first-parent spine entries. The gate's prescribed remedy — `git merge origin/main` — was
run, and it cleared **three** of the four. The fourth is the current tip of main,
`0ee3d161`. Run through the gate's own discriminator, the one its refusal text prints:

```
introduced: ['0ee3d161...', '1da24766...']
anchored in this tree: False
anchored at main:      False
```

Both False. False-here-with-True-at-main is the tree-lag class the merge fixes; **both**
False is a real gap on main. Its cause is visible in the commit itself: `1da24766` is a
JOURNAL entry anchoring `df50ed4a`, a SHA it did not introduce, so the merge that carried
the entry cannot be anchored by it — a single-commit arc cannot anchor its own merge.

**The lane cannot close it without breaking its contract.** Closing it means appending to
`JOURNAL.md`, which this lane's frozen contract reserves to the integrator in so many
words, and which is append-only newest-first, so a lane writing one hands the integrator a
conflict on their own surface. The alternative — waiting for an anchor only another seat
can author — stalls a finished lane.

So `SKIP=audit-health` is declared in each affected commit body with this evidence. The
blast radius was **measured, not assumed**: this tree's audit reports exactly one `[!!]`,
and it is this one; every other check in the suite passes. Nothing this lane commits is
unanchored, and `block-unanchored-push` still fails CLOSED at push time, so the gap cannot
reach `main` through this branch. **The integrator closes it with their next JOURNAL entry
naming `0ee3d161` or `1da24766`** — after which nothing here needs revisiting.

**3. `ARCHITECTURE.md` is a collision risk with night-plan lane 9.** This lane inserts one
new section before `## Automation axes`, and re-stamps `last_reviewed`. Any other lane
touching the same file this batch conflicts on both. The section is deliberately
**unnumbered**: the chapters readers navigate by are cited by number from `CLAUDE.md` §3 and
from lane contracts, and a numbered insertion here would renumber citations that resolve
today.

**4. Two gate-forced couplings, both recorded rather than worked around.**
`graph-orphan-census` refuses a script no wiring surface reaches, so the module, the
pre-commit hook that wires it, and the `ARCHITECTURE.md` marker section its own
regen-and-diff leg reads had to land in ONE commit — the register's doctrine applied to the
register's machinery, which is the right way round.
`task_tree_coherence` refuses an unregistered row file, so filing `[#765]` forced
`gen_task_tree.py --emit-source` in the same commit, against the contract's "no index
regeneration". Declared in the commit body as a gate-forced exception.

**5. `graph-edge-class-census` fired a false positive, and the fix is a row, not a
suppression.** The predicate is `extracts and (scans or reads)` and its own docstring says
it favours **recall over precision**, so a module compiling two regexes and reading files
matches whether or not it discovers anything. `scripts/quality_requirements.py` discovers
nothing: `organ:` and `trip_test:` are written **by hand** in the register and the reader
only resolves each declared side to a path that exists. The remedy the refusal itself names
is to add a verdict row, and the register already carries the negative status for precisely
this case, so one `not-an-edge` row was added. The pinned counts did not move.

**6. An id-collision race cost this lane a rename.** The row was filed at `[#763]`; main
landed `[#763]`/`[#764]` in the same window. Recovery was `git mv` + a text substitution +
restoring `tasks/manifest.json` and `BACKLOG.md` from HEAD + a fast-forward, then re-filing
at `[#765]`. A lane cannot allocate a task id safely while its siblings run — the next
free id is read from a tree that is moving.

**7. One register error, found by writing the trip-test, and corrected.** QR-AVAIL-001's
metric said a declaration must sit "within 12 lines" of the wait it declares. The organ's
constant is `seat_refusals._WAIT_WINDOW = 10`. The metric now names the constant rather than
transcribing its value. The finding is the method, not the typo: writing the trip is what
read the organ, and a register written without its trips would have kept the wrong number.

**8. The AN1-3 correction is recorded in the register, on the entry it corrects.**
QR-PERF-003's `note:` carries it rather than leaving it in the amendment: AN1-3 named
`graph-rebuild` and `audit-health` together as the heaviest local operation, and on wall
time they are within 2.5 s of each other — but on memory they are not comparable.
Re-measured 2026-09-15 on a quiet box: audit-health peaks at **768 MB** against
graph-rebuild's **50 MB**, about 15×. Only one of the two is memory-heavy, and on a box
whose binding constraint is memory rather than time that is the difference that decides
which gate to move. Recorded on the entry rather than absorbed into it, so a reader of the
register sees the corrected premise without needing the amendment that produced it.

---

## 4. TRIGGER and CONSUMER

*"An organ with no trigger and no named consumer is refused at freeze."*

**TRIGGER:** the `quality-requirements-freshness` pre-commit hook, on any staged change to
`ecosystem/quality-requirements.yaml`, `scripts/quality_requirements.py`, `ARCHITECTURE.md`
or `tests/test_quality_requirement_trips.py`. Plus `tests/test_quality_requirements.py` in
the suite, which carries the mutation leg the hook cannot run.

**CONSUMERS:** `ARCHITECTURE.md`'s *Quality requirements* section (generated from the
register, byte-diffed against it); `templates/child-methodology-floor.md.tmpl`, which makes
the register a MUST every consumer repo inherits; and the lane-5 log-review routine
(AN2-3), whose loop closes by turning a reviewed incident into a register entry.

**A fleet consequence of the third, recorded in the manifest rather than left to be
discovered at deploy:** every consumer carrying `.claude/CLAUDE-FLOOR.md` now holds the
*previous* floor bytes with a sidecar that matches them, so each consumer's own
`floor-hash-verify` keeps passing while the fleet diverges from the hub canonical.
Converging it is the floor carrier's job and re-deploying it is an operator act, not a
lane's.

---

## 5. Verification

Targeted, per the lane rule — the impacted set for this lane's diff, selected by
`impacted_tests.py` rather than chosen by hand:

```
tests/test_quality_requirements.py + tests/test_quality_requirement_trips.py   23 passed
tests/test_edge_class_census.py                                               24 passed
tests/test_generate_floor.py + test_deploy_floor.py + test_floor_conformance.py  196 passed
uv run --locked ruff check                                                     clean
scripts/quality_requirements.py check                                          exit 0
scripts/generate_floor.py check                    1211/1500 tokens, F5 clean, no URLs
deploy/release_lint.py --version v1.5.0            0 FAIL, 1 WARN (C2-tag, operator's)
scripts/silent_rule_detector.py                    429 against a baseline of 447
git stash list                                     empty
```

The full suite is **not** run here: in a lane the targeted tests for that lane's diff run,
and the full suite runs once, at integration.
