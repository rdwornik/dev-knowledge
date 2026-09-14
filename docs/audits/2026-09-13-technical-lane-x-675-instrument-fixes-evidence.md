# lane-x-675-instrument-fixes — the three `[#675]` false-pass holes, resolved and closed

Consumers: `[#742]`, `[#743]`, `[#744]` — the three rows the integrator seat filed at batch-X3
close, which this lane implements against. Parent `[#675]` stays OPEN (operator NO-GO on
closing it, ratification item 3); this lane closes none of the four — a lane hands back a
branch and closure is the operator's act.

**Lane:** `lane-x-675-instrument-fixes` · branch `worktree-lane-x-675-instrument-fixes` ·
contract `LANE-x-675-instrument-fixes.md` · base `dbac84b8`.

---

## Part 1 — the locators, resolved in THIS tree (step 1)

The contract's rule 6: *"a line number is a claim until opened"*. All three were opened at
`dbac84b8`, the same commit the review and the integrator read them on. **All three hold, and
all three defects are still present.** Nothing had drifted.

### `[#742]` — `scripts/actions_verdict.py:205-213`

The locator is exact. Lines 206-213 are the second `gh` call:

```
206:    jobs = ["gh", "run", "view", str(match["databaseId"]), "--json", "jobs"]
207:    try:
208:        proc = subprocess.run(jobs, cwd=..., capture_output=True,
209:                              text=True, timeout=GH_TIMEOUT_S, check=False)
210:        match["jobs"] = json.loads(proc.stdout or "{}").get("jobs", []) if proc.returncode == 0 \
211:            else []
212:    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
213:        match["jobs"] = []
```

Every failure mode — non-zero exit (line 211), `OSError`, `subprocess.TimeoutExpired` (a
`SubprocessError` subclass) and `json.JSONDecodeError` (line 213) — lands on the same
`match["jobs"] = []`. `verdict_for` then computes `failing = set()` over that empty list and
returns `STATE_PASS`. **An unreadable job list renders as a clean pass.**

The row's own observation holds too: the FIRST `gh` call, at 190-200, raises
`ActionsUnavailable` on exactly these conditions. The module already knows how to say *"I could
not read this"*; the second call simply does not use it.

**A second-order defect found while resolving this one, not in the row.** `verdict_for`'s
baseline leg (240-249) reads the baseline run's jobs through the same `fetch`. An unreadable
baseline job list yields `base_jobs = {}` with `base_read = True`, so `base_failing` is empty
and **every** failing job at the tip is attributed as `newly_failing` → `STATE_REGRESSED`. That
is a false *accusation* rather than a false pass — the same hole with the sign flipped — and it
is fixed in the same pass because it is the same missing distinction.

### `[#743]` — the step-0 collision extractor, `scripts/seat_refusals.py:303-339`

Two independent legs both require a directory, so a root-level file is invisible twice over:

- `_CONTRACT_PATH_RE` (305-306) requires `(?:\.?[A-Za-z0-9_][A-Za-z0-9_.-]*/)+` — **one or more**
  path segments ending in `/`. `ARCHITECTURE.md` produces no match at all.
- `_WRITE_ROOTS` (310-314) is a tuple of directory prefixes, and the filter is
  `path.startswith(_WRITE_ROOTS)`. Even if the regex matched, the root has no admitting prefix.

**The hole is live in THIS batch, and it was measured, not reasoned about.** Running the
step-0 refusal over wave 4's own four frozen contracts:

```
file-collision: PASS -- 4 contract(s), 21 declared path(s), no file claimed twice
```

with the per-lane footprints reading:

```
LANE-x-628-docs-cut              -> protocols/ESSENTIALS.md, protocols/PLAYBOOK.md,
                                    scripts/canonical_docs.py, tests/test_claude_md_byte_cap.py
LANE-x-664-dead-callers          -> scripts/boundary_report.py, scripts/cloud_provisioning.py,
                                    tests/test_e2e_consumer_lifecycle.py
LANE-x-664-delete-list-execution -> .claude/settings.json, scripts/archive_row_body.py, ... (13)
LANE-x-675-instrument-fixes      -> scripts/actions_verdict.py
```

`lane-x-628-docs-cut` declares `ARCHITECTURE.md` in its Done-contract and it does not appear.
`lane-x-664-delete-list-execution` declares `.pre-commit-config.yaml` and it does not appear.
The two happen not to collide with each other, so **the PASS above is correct by luck rather
than by check** — which is the row's whole claim, now with this batch's own numbers behind it.

**A third observation, on this lane's own footprint.** `LANE-x-675-instrument-fixes` extracts
exactly ONE path — `scripts/actions_verdict.py` — while this lane demonstrably writes three
scripts. `scripts/seat_refusals.py` and `scripts/merge_receipt.py` are named in the contract's
**Steps** section, and `declared_footprint` reads the **Done-contract** section only. That is a
deliberate, measured choice documented in the function's own docstring (whole-file extraction
made every lane share references and the refusal meaningless), and it is not this row's scope
to change. It is recorded because it bounds what the fixed check can promise: widening the
extractor to see root-level files does not widen it to see paths declared outside the
Done-contract, and a reader of a future PASS should know which of the two limits they are
relying on.

### `[#743]` sub-question — does `file_purpose_graph._REL_PATH_RE` share the blindness?

**Yes, and byte-for-byte.** `scripts/file_purpose_graph.py:677-678` is character-identical to
`seat_refusals._CONTRACT_PATH_RE`:

```
r"(?:^|[\s`'\"(\[])((?:\.?[A-Za-z0-9_][A-Za-z0-9_.-]*/)+[A-Za-z0-9_.-]+\.[A-Za-z0-9]{1,6})"
```

That identity is intentional — `_CONTRACT_PATH_RE`'s own comment says so: *"Same shape
`file_purpose_graph._REL_PATH_RE` uses, deliberately: two organs disagreeing about what counts
as a path is a class of defect this repo already carries."* The consequence is that a task row
naming `ARCHITECTURE.md`, `CLAUDE.md`, `pyproject.toml` or `.pre-commit-config.yaml` in its body
produces **no `IMPLEMENTS` edge**, so `graph-task-coverage` cannot see that the row claims the
file.

The disposition of that finding is recorded in Part 3, after the fix that answers it.

### `[#744]` — `scripts/merge_receipt.py:449-466`, `median_report`

`wanted = [r for r in receipts if r.kind == kind]` is the only filter. Nothing reads `closed`,
nothing reads `failed_steps()`, nothing reads `missing_required()`. Two further surfaces make
the same unchecked claim in prose:

- `read_ledger` (369) is docstringed *"Every closed receipt, oldest first"* and filters nothing.
- `MedianReport.render` prints `n=… closed receipt(s)` and, at n=0, *"holds no closed … receipt
  yet"*.

**This hole is not hypothetical either — it is fully realised in the live ledger.**
`logs/MERGE-RECEIPTS.jsonl` holds exactly two rows, and **both have failed steps**:

```
lane-x-675-step-4  kind=arc  steps=[lint, regen, regen-organ, targeted, targeted-retry,
                                    targeted-code, targeted-livetree]  FAILED=[targeted, targeted-retry]
lane-x-675-step-7  kind=arc  steps=[targeted-lane]                     FAILED=[targeted-lane]
```

and the tool at `dbac84b8` reports, over exactly that data:

```
arc minutes over n=2 closed receipt(s)
  median   9.4 min   (target 3.6: under 30 -> MET)
  range    0.0 .. 18.7 min
  per merge 0.0, 18.7
```

A **0.0-minute** entry — one receipt that recorded a single step, which failed — is half the
sample, and the instrument answers **"target 3.6: MET"**. That is `[#675]`'s filed failure class
verbatim: a reader returning a plausible, flattering value because the discriminating field is
absent from what it looks at.

---

## Part 2 — per hole: the RED witness, the commit that greened it, the row it discharges

Every witness below **failed on the defect**, not on a missing name. Where a first run errored
on an undeclared constant, the constant was declared first — a pure declaration with no
behaviour — so the recorded RED is the behavioural one.

### `[#742]` — `actions_verdict`, an unreadable job list is not an empty one

```
RED       11 failed, 19 passed
          test_an_UNREADABLE_job_list_is_NEVER_a_PASS[non-zero-exit]
              AssertionError: assert 'PASS' != 'PASS'
          ... identically for [OSError] [TimeoutExpired] [malformed-JSON]
GREEN     dfe72365   tests/test_actions_verdict.py  30 passed
DISCHARGES [#742]   (not closed — closure is the operator's act)
```

The fix rests on one distinction: **`None` means "not read", `[]` means "read, and there were
none"** — two facts the old code spelled the same way, in a module whose entire argument is that
it never does that. A fourth absence state `JOBS-UNREADABLE` carries its own remedy (retry) and
is distinct from `PASS` and from every failure state.

**The witnesses stay RED on reintroduction**, and that is a design property rather than a hope.
They drive the *real* `fetch_run` with `subprocess` stubbed, so the bug's own `except` branch is
what they exercise. A witness that stubbed `fetch` instead would have tested the fix's shape
rather than the bug's absence, and restoring `match["jobs"] = []` would sail straight through it.

**Propagated to every rendering caller**, per the Done-when. `file_purpose_graph why` reports
three consumers, none of which renders a verdict; `review_packet` mentions the module only in a
docstring and `graph_queries` only as an orphan-census disposition. The one surface that renders
a verdict for a human is `.claude/commands/lane-integrate.md`, whose *"three absences are three
verdicts"* line and refuse-to-finish row **2b** both now carry the fourth.

**Second-order defect fixed in the same pass** — the baseline leg, described in Part 1. Unread
baseline jobs now mean `UNATTRIBUTED`, which is what they always meant.

### `[#743]` — `seat_refusals`, a root-level file is a file

```
RED       8 failed, 77 passed
          test_two_lanes_declaring_the_same_ROOT_LEVEL_file_are_REFUSED
              Failed: DID NOT RAISE SeatRefusal
          test_a_root_level_TRACKED_file_is_extracted[ARCHITECTURE.md]
              AssertionError: assert set() == {'ARCHITECTURE.md'}
          ... and for .pre-commit-config.yaml, pyproject.toml, CLAUDE.md, uv.lock, package.json
GREEN     ed93586f   tests/test_seat_refusals.py  85 passed
DISCHARGES [#743]
```

The five **negative** tests — transport filenames, prose nouns, absolute operator paths — were
green *before* the fix and are green after. That is what makes them regression tests rather than
decoration.

**Library-first, and it is why this fix adds no roster.** The admission is
`validate_hermetization.SANCTIONED_TIER1_FILES` — the shape-spec-derived set ADR-101 already
refuses new root files against, i.e. the repo's one answer to *"what may sit at the root"*.
Retyping it would have created exactly the defect `_CONTRACT_PATH_RE`'s own comment names, and a
root file admitted by a future ruling now reaches this check for free. A test pins the two sets
equal, so they cannot drift apart silently.

**A closed set, not a glob** — the row's explicit anti-regression clause. The root branch of the
regex is a longest-first literal alternation built from that set, so `LANE-x-000-other.md`,
`MATRIX.md`, `REVIEW.md` and every other root-shaped prose noun stay out **by construction**,
not by a second filter a later simplification could drop.

**Measured before shipping**, because this module's founding rule is that a refusal overstating
its reach is worse than none. Across **all 57 contracts on the transport**, the widening made
five root files visible and produced exactly **one** over-claiming contract — this lane's own,
which carries `[#743]`'s row body verbatim *inside* its Done-contract, where the row enumerates
`ARCHITECTURE.md`, `.pre-commit-config.yaml` and `pyproject.toml` as examples. **Excluding it,
zero in-batch false collisions.**

That one case is pinned as behaviour rather than patched around, and the framing is deliberate:
**the checker is right and that contract is mis-shaped.** `declared_footprint` reads the
Done-contract because that section is write-shaped; the sanctioned home for a carried row body is
its own section — which is exactly what the pre-existing
`test_the_footprint_is_read_from_the_DONE_CONTRACT_not_the_whole_file` fixture already assumes.
Recorded as the function's second honest limit and pinned by
`test_a_row_body_QUOTED_INSIDE_the_done_contract_reads_as_a_declaration`.

### `[#744]` — `merge_receipt`, a median over incomplete receipts is not a median

```
RED       9 failed, 21 passed
          test_an_INCOMPLETE_receipt_is_EXCLUDED_from_the_median
              AssertionError: only the complete receipts are counted   (n was 7, not 3)
          test_median_STRICT_is_the_TARGET_axis_and_NOT_the_completeness_axis
              got "n=2 closed receipt(s) / median 20.5 min (target 3.6: under 30 -> MET)"
GREEN     8bc3ea98   tests/test_merge_receipt.py  30 passed
DISCHARGES [#744]
```

**The live ledger, unchanged, before and after.** This is the clearest single piece of evidence
this lane produced, because the data is real and untouched:

```
BEFORE (dbac84b8)
  arc minutes over n=2 closed receipt(s)
    median   9.4 min   (target 3.6: under 30 -> MET)
    per merge 0.0, 18.7

AFTER (8bc3ea98), same two rows
  arc minutes: NO RECEIPTS. The median is undefined, not zero -- logs/MERGE-RECEIPTS.jsonl
  holds no COMPLETE closed arc receipt yet. (2 INCOMPLETE arc receipt(s) EXCLUDED ...)
    EXCLUDED lane-x-675-step-4: 2 step(s) failed (targeted, targeted-retry)
    EXCLUDED lane-x-675-step-7: 1 step(s) failed (targeted-lane)
```

`"n=2 closed receipt(s)"` was false — nothing had checked `closed` — and `"target 3.6: MET"` was
a pass built from a receipt that measured nothing.

**The predicate is one function**, `Receipt.incompleteness_reason()`, which returns *why* rather
than a bare boolean — for the argument `REMEDIES` makes one organ over: an exclusion a reader
cannot account for looks like a bug in the tool, and a bare count does not say whether the ledger
is dirty or the merges are. Four legs: never closed · no steps recorded · any failed step · and,
**for merge receipts only**, a missing `REQUIRED_STEP`.

**Leg 4's scoping is a decision, not an oversight.** `REQUIRED_STEPS` is the *integrator's* walk,
and this module's own docstring says an arc *"pays no merge and no teardown"*; holding an arc to
it would make `median --kind arc` permanently `n=0` for a reason that is not incompleteness. Legs
1–3 bind both kinds, and a test pins the distinction in both directions.

**`--strict` — decided, documented, pinned.** It is the **target** axis and **not** the
completeness axis. Completeness filtering is unconditional and has no flag, because a flag would
make this very false pass opt-outable: a median over incomplete receipts is not a laxer reading
of the number, it is a different number. The pinning test asserts identical `n` with and without
the flag, and that only the exit code differs.

**Three pre-existing tests changed fixtures, stated plainly.** They fed `median_report` from
`_receipt_with`, whose docstring claimed a *"closed-shape receipt"* while never setting `closed`
and recording one step out of four. The predicate correctly refuses those, so the fixtures moved
to a genuinely complete helper and the docstring's false claim was removed. **Every assertion in
those three is unchanged** — the fixtures got stricter; the tests did not get weaker.

---

## Part 3 — the `[#743]` sub-question, answered and SPLIT with the reason measured

**Does `file_purpose_graph._REL_PATH_RE` share the blindness? Yes, character-for-character.**
Part 1 records the identity. **It is not fixed here, and the reason is a measurement rather than
a preference.**

Applying the *same* closed-set widening to task-row bodies was measured over all 491 rows:

```
618 new IMPLEMENTS edges, by target:
    468  BACKLOG.md          <- the generated view EVERY row mentions
     38  CLAUDE.md
     21  .pre-commit-config.yaml
     21  ARCHITECTURE.md
     15  pyproject.toml
     11  JOURNAL.md
    ...  the remaining 44 across 11 more root files
```

**Three-quarters of the gain is one generated view.** `_REL_PATH_RE`'s consumer filters
candidates by `(root / rel).is_file()`, and that filter cannot tell a *mention* from a *claim* the
way a write-shaped Done-contract section can — every task row names the view it is rendered into.
A file "implemented by" **468 open rows** is claimed by none of them, so the same change that
*completes* the collision check would *degrade* `graph-task-coverage`.

Fixing it properly needs a different design — mention-versus-claim, generated views excluded —
which is a different question from the one `[#743]` asks. Two further facts bound the decision:
it is `[#664]`'s organ, and a **concurrent wave-4 lane** (`lane-x-664-delete-list-execution`)
declares `tests/test_graph_spine.py`, the graph's own test surface.

**Split, not skipped.** The contract's own words are *"either fixed with it or split with a
stated reason"*; this is the stated reason, with its numbers.

---

## Part 4 — what this lane did NOT do, and decisions taken under V-2

- **No row filed for any of the three holes.** `[#742]` `[#743]` `[#744]` were filed by the
  integrator seat and reached this tree through `main` (see below). Contract rule 1.
- **Nothing closed.** `[#675]` stays OPEN per the operator's NO-GO, and the three children are
  handed back, not closed — closure is the operator's act.
- **No JOURNAL entry, no index regeneration, no merge toward `main`, no push.** The integrator's
  surfaces, untouched.
- **No `--no-verify`, and no hook bypassed.** Every commit passed the full gate set on its own.
  The `graph-task-coverage` refusal the contract warned about never fired, because the sync below
  brought the claiming rows into this tree.

**Decisions taken per contract defaults and reported rather than asked (V-2):**

1. **A sync merge of `main` into this lane** (`c498bf4a`). `audit-health` hard-blocked the second
   commit with `[!!] journal_spine_anchor` on `c0e0722f`. The gate's own diagnostic discriminated
   it: `anchored in this tree: False` / `anchored at main: True` — the recorded **tree-lag**
   signature, not a gap. Merging **local** `main` is the fix (local, because that is the ref the
   check resolves, whatever the remedy text says about `origin/main`). This is a sync, not an
   integration: no lane branch touched, nothing pushed, nothing merged toward `main`.
2. **`.claude/commands/lane-integrate.md` edited**, though the mechanical footprint extractor
   reports only `scripts/actions_verdict.py` for this contract. `[#742]`'s frozen Done-when
   requires the new state reach *"every caller that renders a verdict"*, and that file is the only
   such caller. The frozen Done-when outranks the Steps skeleton; the edit is two state
   enumerations and nothing else.
3. **`ecosystem/doc-counts.md` regenerated in each test-adding commit.**
   `doc-counts-pytest-freshness` is a blocking commit gate, and deferring it to the integrator
   yields zero commits. Ownership was confirmed by arithmetic each time, not assumed.

**One pre-existing suite failure, attributed and not mine.**
`tests/test_v6_frozen_contract.py::test_fr6_repo_root_and_cross_repo_are_codified_and_cli_mapped`
fails in the wider impacted set. Its own module docstring declares the file **"INTENTIONALLY RED
at freeze"** — it is `[#446]`'s frozen-contract register, asserting mechanisms the build has not
written. It imports only `gen_handoff` and `verify_handoff_probes`, so this lane's diff cannot
reach it.

---

## Part 5 — the handback

```
branch    worktree-lane-x-675-instrument-fixes
base      dbac84b8
commits   cce1426e  the locator record (step 1)
          c498bf4a  sync merge of main -- the anchor gate's own prescribed fix
          dfe72365  [#742]  actions_verdict
          ed93586f  [#743]  seat_refusals
          8bc3ea98  [#744]  merge_receipt
targeted  146 passed  (test_actions_verdict 30 + test_seat_refusals 85 + test_merge_receipt 30,
                       run with uv run --locked, plus this artifact's commit)
ruff      clean on every touched file
stash     git stash list -- EMPTY
owed      the integrator regenerates docs/audits/README.md on the merged result ([#590]); this
          lane affirmatively did not touch it
```

**One observation for the integrator, offered and not acted on.** Step 0 for wave 4 would now
REFUSE, on `.pre-commit-config.yaml` and `ARCHITECTURE.md`, and one of the two claimants on each
is this lane's own contract quoting `[#743]`'s row body inside its Done-contract (Part 2). The
real claims — `lane-x-628-docs-cut` on `ARCHITECTURE.md`, `lane-x-664-delete-list-execution` on
`.pre-commit-config.yaml` — do not collide with each other. The refusal is doing its job; the
contract shape is what wants re-cutting, and that is a dispatcher-side fix rather than a lane's.

