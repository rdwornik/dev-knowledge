# lane-y-750-merge-receipts — the receipt names its merge, the verdict STATE decides, and wall time is the span

Consumers: `[#750]` — the row this lane filed and implements against; it stays **OPEN**, because a
lane hands back a branch and closure is the operator's act. Parents `[#675]` (targets 3.1/3.2/3.3/3.6)
and `[#744]` (the completeness predicate this lane makes reachable) also stay open — the reasoning is
in the row's own `kill-candidates:` line and is not restated here. `[#752]` is sequenced behind this
lane on `scripts/merge_receipt.py` and should read Part 5 before it starts. The seat cutting batch Y's
first receipt wants **Part 4** — verb, argument shape, and the four things to get right.

**Lane:** `lane-y-750-merge-receipts` · batch Y slot 1 · branch `worktree-lane-y-750-merge-receipts` ·
contract `docs/audits/2026-09-14-technical-batch-y-launch-contracts/LANE-y-750-merge-receipts.md` ·
base `e6acb23e` · ruling **AY1-1** (`to-cc/AMEND-BATCH-Y-ROSTER-001.md`, quoted verbatim in
`docs/audits/2026-09-14-technical-batch-y-manifest.md`).

**Commit-and-STOP. Nothing was pushed, nothing of this lane's was merged into `main`, no index was
regenerated.** One sync-merge of `main` INTO the lane, and that is the only merge here.

```
c3cdd0b2  test(merge-receipt): RED-first witnesses ......... 469 +, 34 -   (4 files)
d91603a8  feat(merge-receipt): the three defects ........... 466 +, 26 -   (2 files)
5109a2fd  docs(lane-integrate): the wiring ................. 98 +, 34 -    (1 file)
55466a71  chore(sync): merge main @ 999fdd54 ............... sync only, no lane work
<this>    docs(audits): this packet
                       lane diff vs main 1033 +, 94 -  (6 files, packet excluded)
```

The sync was taken for one reason and it is worth naming: it lets this lane's **final commit run
`audit-health` ARMED**, instead of carrying the declared `SKIP=audit-health` that the first three
commits each declared for one foreign FAIL. See Part 3 item 1.

---

## Part 1 — what changed

### The three defects the row names, and what each one now does

**(1) Completeness reads the suite's verdict STATE, per ruling AY1-1.**
`Receipt.incompleteness_reason()` went from four legs to six. The old leg 3 refused any step with
`ok=False`; the suite step's `ok` came from `actions_verdict.Verdict.ok`, which is
`state == STATE_PASS` under a docstring that says *"ONLY `PASS` is ok. Every other state is non-zero,
including PRE-EXISTING"*. While `main`'s Actions `pytest` job is pre-existing red, that leg refused
**every** receipt however clean the merge — so `[#744]`'s predicate was **unreachable**, not merely
wrong, and the refusal this same lane adds would have refused every merge in the repo on day one.

`PASS` and `PRE-EXISTING` are now COMPLETE with the state recorded **by name** on the step, in the
ledger row and in the summary. `REGRESSED`, the five unreadable states (`NO-RUN`, `IN-PROGRESS`,
`GH-UNAVAILABLE`, `JOBS-UNREADABLE`, `UNATTRIBUTED`) and an absent verdict are INCOMPLETE, and the
refusal names the state **and** carries `actions_verdict.REMEDIES`' own next action for it.

Two design choices worth the integrator's eye, because both are load-bearing:

- **Scoped BY CLASS, not by a list of step names.** `judged_by_verdict()` is
  `self.kind == KIND_MERGE and step.step_class == CLASS_TESTS`. A name list goes stale the first
  time an integrator renames a step; `step_class` already means *what kind of work this was*. Every
  `tests`-class step on a merge receipt is a reading of the suite.
- **Last verdict wins.** `suite_verdict()` returns the last recorded state, so a `JOBS-UNREADABLE`
  read that is retried under its own `--step` id is **superseded** by the retry rather than poisoning
  the receipt. That is the shape the command file's retry instruction needs to be honest.

**Arcs are exempt from the new leg**, by the same argument leg 6 already makes for `REQUIRED_STEPS`:
an arc reads no Actions run for a merge SHA because there is no merge, so requiring a state would make
`median --kind arc` permanently n=0 for a reason that is not incompleteness. An arc keeps the
exit-code reading it always had.

**The exit code left the predicate and did not leave the report.** `render_summary()` prints each
step's state beside its ok/FAILED. Removing it from both would have laundered a red step into silence
and become the false pass this change exists to refuse; one test asserts exactly that pair.

**(2) `wall_seconds` is the arc's span.** It was the sum of the timed children. Verified against the
live ledger, by re-reading both existing rows through the new arithmetic:

```
lane-x-675-step-7  kind=arc  stored wall_seconds=1.776
                   WALL 181.33 min   RECORDED 0.03 min   UNRECORDED 181.30 min
lane-x-675-step-4  kind=arc  stored wall_seconds=1121.543
                   WALL  28.90 min   RECORDED 18.69 min  UNRECORDED  10.21 min
```

The old arithmetic keeps the name it was always computing — `recorded_seconds()`, a **coverage**
figure with the raced group counted once, so target 3.3's saving is still measured — and
`unrecorded_seconds()` is the difference. The baseline's 72.7 minutes of residual ceremony live
exactly there: in the gaps *between* timed steps. `baseline_split()` folds the remainder into the
residual bucket, so `tests + residual` now sums to the **arc** rather than to the part of it that
happened to be wrapped in a stopwatch. Where concurrency makes the two views differ by the raced
overlap, `render_summary()` **reports** the disagreement rather than clamping it.

A new leg 3 guards the door this opened: `opened`/`closed` that do not parse as an ordered pair make
the span **UNKNOWN**, not `0.0` — and `0.0` is precisely the flattering value leg 2 exists to refuse.

**(3) A merge that lands without a COMPLETE receipt is REFUSED.** `Receipt.merge_sha` is new and is
what made the question answerable at all: the receipt named no commit, so *"does this merge have a
receipt"* had no answer.

- `record_actions_verdict()` / the **`actions`** verb replaces the
  `time --step actions -- actions_verdict.py …` prefix. The prefix recorded the child's exit code and
  threw the state away; the verb calls the reader directly, records the state by name, binds the merge
  SHA, prints the same verdict the integrator would have read, and exits with the same code —
  non-zero on `PRE-EXISTING` included.
- `first_parent_merges()` **fails CLOSED**. A bad range raises rather than returning `[]`, because an
  empty list means *"no merges here"* and `require` would then report every merge as receipted. That
  is verbatim the hole `[#742]` closed one organ over, where an errored `gh` call became an empty job
  list and printed PASS.
- `audit_merges()` is a pure function over (SHA list, ledger), prefix-tolerant in both directions, so
  the refusal is testable without a git fixture. **An arc cannot discharge a merge** — an arc pays no
  merge and no teardown, so accepting one would let the cheapest row in the ledger satisfy the bar for
  the most expensive act.
- `render_require()` **names its own vacuity**, because *"0 of 0 unreceipted"* is exactly the
  plausible, flattering value `[#675]` is filed about.

Both legs verified against the real repo, not only against fixtures:

```
$ merge_receipt.py require --range 02212112..e6acb23e
merge receipts over 02212112..e6acb23e: 2 merge commit(s)
  REFUSED e6acb23e190d: NO RECEIPT -- no kind=merge row in logs/MERGE-RECEIPTS.jsonl names this merge. …
  REFUSED 8a41c650820b: NO RECEIPT -- no kind=merge row in logs/MERGE-RECEIPTS.jsonl names this merge. …
  -> 2 of 2 merge(s) landed without a COMPLETE receipt: e6acb23e190d, 8a41c650820b. …
exit=1

$ merge_receipt.py require --range main..main
merge receipts over main..main: NO MERGE COMMIT in the range -- nothing was checked, which is NOT the
same as a clean walk. If you expected merges here, the range is wrong: …
exit=0
```

Both real merges are refused **correctly**: the two rows in the live ledger are `kind=arc`, so neither
discharges a merge, and neither carries a merge SHA because nothing could record one until this lane.

### There is no way to type a verdict onto a receipt

A test asserts the absence across `actions`, `time` and `close`. A `--state PASS` flag would put
`[#744]`'s false pass one keystroke away: the integrator whose `gh` is unavailable could type the
green the tool declined to read. So `GH-UNAVAILABLE` **refuses the merge rather than offering a way
round itself** — which is what target 3.2 asks for, *"record explicitly that the result was NOT read,
never that it passed"*.

### The wiring (`.claude/commands/lane-integrate.md`)

- **One receipt per merge**, opened and closed inside each lane's block. It was one per **batch**,
  which made `REQUIRED_STEPS` satisfiable by whichever lane recorded a step id first and made `median`
  a median over BATCHES printed as *"median merge minutes"*. `open` runs **before** the handback
  verdict, because that verdict is part of the merge's cost; `close` is the last act of the per-lane
  sequence; `median` and row 2d run once, after the last lane.
- **`actions` replaces the `time`-prefixed `actions_verdict.py` call**, with AY1-1 stated where the
  integrator reads it, plus the two halves that must travel together: COMPLETE is not a statement that
  the run was green, and PRE-EXISTING is not a pass.
- **New checklist row 2d** — `require --range <FIRST merge's first parent>..HEAD` exits 0 — and
  **row 2b re-pointed** off `actions_verdict.py`, which this walk no longer runs.
- Two stale claims fixed, both invalidated by this lane's own work: *"One row is now mechanized, and
  only one"* → **two**; and *"it times what it is asked to time"* is still true but no longer the whole
  story, because an unprefixed step now surfaces as UNRECORDED rather than as no time at all.

### Tests

RED-first per ADR-108 §B: commit `c3cdd0b2` is 42 failing witnesses and the row, landed **before** any
enforcing code. The three the contract names by name are all present — a merge with no receipt fails, a
`REGRESSED` receipt fails, a `PRE-EXISTING` receipt PASSES — plus the 3h01m-recorded-as-1.776 s span.

**MEASURED at `5109a2fd`: 172 passed, 0 failed** —
`pytest -n 0 tests/test_merge_receipt.py tests/test_actions_verdict.py tests/test_seat_refusals.py`,
22.58 s. That is the complete impacted set: `impacted_tests.py select --changed` returns
`test_merge_receipt.py test_seat_refusals.py` for `scripts/merge_receipt.py`, and
`test_actions_verdict.py` is included because this commit imports `actions_verdict` for the first
time. Per `[#528]` the full suite runs once, at integration.

---

## Part 2 — proposed diffs (nothing here was written)

Three items belong to surfaces this lane does not own. Each is **reported, not edited**, per the
contract's declared footprint.

**(a) `scripts/graph_queries.py` — the orphan disposition prose for `merge_receipt.py` is now narrower
than the module.** It reads *"(open / time / race / close across the merge walk)"*. The walk now also
invokes `actions` and `require`. That is the `[#664]` wiring-surface list's row to change, and the
disposition's own `owner` field says so. Proposed: extend the parenthetical to
`(open / time / race / actions / require / close across the merge walk)`. No behaviour depends on it —
the disposition is prose, and the census passes today.

**(b) `ecosystem/doc-counts.md` — one `gen_doc_counts.py --write` is owed on the merged tree, and the
staleness is NOT this lane's.** Measured at `55466a71`:

```
$ gen_doc_counts.py --check
     match  audit_check_count     (file 55   / actual 55)
  mismatch  precommit_hook_count  (file 32   / actual 33)
  mismatch  pytest_collected      (file 6111 / actual 5860)
```

I had recorded this as self-inflicted in all three commit bodies, on the reasoning that a lane which
adds tests moves the `pytest_collected` claim. **The measurement says otherwise, and the direction is
the proof:** `actual` is 251 **below** the claim *with every one of this lane's tests already counted*.
Adding tests can only raise `actual`, so the claim was already too high at main's tip and this lane's
additions move it **toward** the claim, not away. `precommit_hook_count` (32 vs 33) this lane does not
touch at all — it added no hook.

The regen is still owed and the integrator seat has **accepted** it; what changes is the diagnosis, so
whoever runs it knows it is discharging pre-existing drift rather than tidying after batch Y slot 1.
Note the known trap: `gen_doc_counts.py` reads **HEAD**, not the merged worktree, so running it
mid-merge writes the pre-sync count — run it after the merge commit exists.

**(c) `docs/audits/README.md` — not regenerated, deliberately.** `[#590]` narrowed
`audit-index-freshness` to the index and its generator precisely so a lane writing an artifact does
not have to touch the shared file; that narrowing put this file in 6 of the last 7 conflicted merges
before it landed. The integrator is gate-of-record for it. **Verified**: the hook's `files:` pattern
does not match this artifact, so nothing is owed in this lane's commits.

---

## Part 3 — open items

**1. This final commit declares NO hook skip at all, and `audit-health` runs ARMED.** `--no-verify`
was not used anywhere in this lane. **Measured at `55466a71`: `health: OK`, 0 FAIL, 142 WARN, and not
one finding names this lane's packet or any file this lane wrote.** The three earlier commits each
declared two named skips; both are gone here, for different reasons, and the difference matters:

- `audit-health` — **skip DROPPED.** Commits `c3cdd0b2`, `d91603a8` and `5109a2fd` each declared it for
  **one** foreign FAIL: `journal_spine_anchor` on `e6acb23e`, the tip of `main` at this lane's base. It
  was diagnosed with `journal_anchor`'s own two-leg split rather than a grep, because the two legs are
  what separate a real gap from the tree-lag false positive. Two entries were unanchored at lane start
  and only one of them was a gap:

  | Entry | this tree | at main | disposition |
  |---|---|---|---|
  | `8a41c650` | False | True | **tree lag** — fixed by `git merge --ff-only main` (this lane had zero commits at the time, so no merge commit was created and staged work stayed intact) |
  | `e6acb23e` | False | False | **real gap on main**, already pushed. Its introduced set was only its own SHA plus JOURNAL commit `f5384ac4`, which main's JOURNAL did not name — the single-commit-arc-cannot-anchor-its-own-merge trap, where fixing the gap one entry down opens an identical one up |

  **Closed by the integrator seat at `999fdd54`** with a two-commit arc (`e6cc52ae` substantive,
  `869c8b23` journal last) — the shape that closes behind itself. This lane synced onto it at
  `55466a71` and re-ran the gate armed; `journal_spine_anchor` is green on both predicates, and they
  were checked separately because they ask different questions: `range_is_anchored(floor..tip)` is what
  `block_unanchored_push` reads, `unanchored_on_spine` against the committing tree is what
  `check_journal_spine_anchor` reads. **The skip was not a standing exemption and it is gone.**
- `doc-counts-pytest-freshness` — **not skipped, and not silenced either: it does not apply to this
  commit.** Its `files:` filter is
  `(^tests/.*\.py$|^conftest\.py$|^pyproject\.toml$|^ecosystem/doc-counts\.md$)` and this commit stages
  one path, `docs/audits/…-packet.md`, which matches none of them — so the hook reports *"no files to
  check"* on its own terms rather than being bypassed. The claim it gates **is** still stale, and
  Part 2 item (b) re-diagnoses why that is not this lane's doing. Do not read a clean run of this final
  commit as evidence the count is fresh; it is evidence this commit cannot have moved it.

**2. The refusal is a checklist row rather than a hook, and the integrator seat handed this lane the
reason that makes that decision load-bearing rather than merely convenient.** I had two reasons: armed
tree-wide, `require` would refuse every merge that predates the receipt, and armed at commit time it
would query an Actions run that cannot exist yet. **There is a third and it is stronger: a `--no-ff`
merge runs NO pre-commit hooks at all.** `pre-merge-commit` is absent from
`default_install_hook_types` (`[pre-commit, commit-msg, pre-push]`), and git runs `pre-merge-commit` —
not `pre-commit` — when it auto-commits a merge. **Verified two ways in this lane**: the resolved hooks
directory holds `pre-commit`, `commit-msg` and `pre-push` and no `pre-merge-commit`; and this lane's
own sync-merge at `55466a71` ran the commit-msg hooks and **zero** pre-commit hooks, which is a fifth
data point on the integrator seat's 4-for-4.

The consequence for receipt work generally, which is why it belongs here and not only in a gate audit:
**any receipt field populated from a commit-time gate is empty on merges specifically** — the one
commit class receipts exist to measure. And for row 2d in particular, arming `require` as a pre-commit
hook would not merely have been wrongly timed; it would **never have fired on a merge at all**. Row 2d
is therefore the enforcement point by necessity, and its two honest limits are written beside it: an
**OPEN** receipt is invisible to `require` (close first), and a `PRE-EXISTING` suite verdict is
COMPLETE — the row does not refuse a merge for `main` being red before it arrived.

**3. `require` reads the LEDGER, so it cannot tell a merge that was itemised from a receipt that says
it was.** This is the mirror of the handback row's limit and is stated as such in the command file.
What row 2d closes is the **silent** case: a merge that landed with no receipt at all, which until
this lane nothing could even ask about.

**4. Row `[#750]` adds one in-band `backlog-row-length` WARN** (body > 1320 chars). The
`backlog-accretion` leg does **not** fire: it needs a ≥30-day history span and this row's history spans
2026-09-12→14.

**5. Footprint deviation, disclosed rather than escalated.** `tests/test_merge_receipt.py` is not in
the contract's declared footprint, but Done-contract clause 1 requires a RED-first witness and there is
no other home for one. The frozen Done-contract outranks the Steps skeleton's *"no edits outside the
declared footprint"*, so this was decided per the V-2 budget's contract defaults. Same reasoning for
this artifact, which Step 4 requires by name. `tasks/750-…md`, `tasks/manifest.json` and `BACKLOG.md`
are the three acts of filing the row Step 3 requires.

**6. Ledger back-compatibility is honest, not convenient.** `merge_sha` and `verdict_state` default to
`None` on a row written before `d91603a8`, so those rows read as INCOMPLETE — which is the truth: those
merges were never judged on a verdict state. Defaulting either to something convenient would back-date
a judgement nobody made.

**7. `-m live_repo` is 14 failed / 136 passed, measured at `5109a2fd` — before the sync — and none of
the 14 is this lane's.** The
lane's own impacted set is 172 passed / 0 failed (Part 1). Attribution was **measured, not asserted**:
the only two failures over a live population a new file of this lane could have entered were checked by
enumerating the actual delta.

- `test_proof_layer.py::test_the_live_guard_population_is_at_or_below_its_baseline` — delta is **19
  guards, all in `test_fleet_analytics.py` (17) and `test_worktree_seed.py` (2)**. None in
  `test_merge_receipt.py`.
- `test_consumer_at_landing.py::test_the_live_corpus_measures_and_the_baseline_matches_it` — the
  unconsumed set names `1a-L01.md` and siblings, none of them this lane's.

The remaining 12 read corpora this lane's diff does not touch: four `test_normalize_headers.py` and one
`test_toc.py` failing on *"corpus implausibly small (0) — glob is wrong"*, plus
`test_handoff_modes.py`, `test_desired_state_loader.py` (a pydantic `Probe` validation error),
`test_desired_state_schema.py`, `test_export_backlog_view.py`, `test_gen_handoff.py`,
`test_doc_code_edge.py` and `test_validate_doc_rot.py`. **They are reported here rather than filed** —
filing rows for a red suite this lane did not cause is the scope overrun `[#675]` clause 1 warns about,
and the integrator is the seat that sees the merged tree they should be measured against.

**8. One gate-set finding, credited to the integrator seat, deliberately NOT filed by this lane — and
the instance being fixed did not fix the class.** The two journal-anchor organs disagree on scope:
`block_unanchored_push._verdict` calls `_ja.range_is_anchored(...)` — **range**-anchored — while
`audit.check_journal_spine_anchor` calls `_ja.unanchored_on_spine(...)` — **every**-entry-anchored. A
push can therefore pass the pre-push gate and leave `audit-health` red, which is exactly the state
this lane found `main` in. `999fdd54` discharged the **instance**; the two predicates still disagree,
so the next one-commit arc reopens it. This lane supplied the locus pair; the finding is the
integrator's to carry into its close packet.

**9. AY1-1 as implemented, stated against the integrator seat's own reading, because one clause
differs.** Three of four agree exactly: `PASS` and `PRE-EXISTING` are COMPLETE with the state named;
`REGRESSED` is INCOMPLETE and refuses; unparseable output refuses rather than defaulting either way.
The fourth needs care. The integrator seat's reading is that `NO-RUN`, `IN-PROGRESS`, `UNATTRIBUTED`,
`GH-UNAVAILABLE` and `JOBS-UNREADABLE` are *"not the merge's fault and each carries its cause string"*.
**This implementation carries the cause string AND still refuses**, because the ruling's own text makes
unreadability a refusal rather than a pass: *"`REGRESSED`, or a verdict that cannot be read, is
INCOMPLETE and refuses the merge."* Not-the-merge's-fault and refuses-the-merge are not in tension —
the refusal is not a verdict on the merge, it is a refusal to certify a cost nobody measured, and
target 3.2 asks for exactly that: *"record explicitly that the result was NOT read, never that it
passed."* The remedy is to make the state readable (retry `JOBS-UNREADABLE` under its own `--step` id;
wait out `IN-PROGRESS`; restore `gh`) and `suite_verdict()`'s last-wins rule is what lets a retry
supersede the bad read. If the operator wants those five to pass rather than refuse, that is an
amendment to AY1-1 and not a reading of it.

**10. ESCALATED, NOT DECIDED — where the push sits in the walk, and the target-3.2 finding under it.**
This is the one item on this list that needs a ruling before batch Y's receipts mean anything, and it
is a defect in what this lane shipped at `057259eb`: `actions` was wired inside each lane's block while
the walk pushes once after the last lane, so every read would have returned `NO-RUN` and row 2d would
have refused the whole batch. Caught after the packet's first version, fixed in the command file and
corrected in Part 4 and in the handback message. **Full statement, the two candidate topologies, and
the measurement argument against (B) are in the boxed correction in Part 4** — the short form is that
`actions` must follow the push and `close` must follow `actions`, which holds either way, and only the
push's position is open. It is a fork class with no standing ruling, so per the V-2 budget it is handed
up rather than taken.

Underneath it: **`[#675]` target 3.2 has never been satisfiable by this walk**, independent of this
lane. The pre-push read predates `[#750]`; the old flattened predicate hid it by refusing every
receipt for an unrelated reason. That belongs in the integrator's close packet as a CANDIDATE, with
(A)/(B) named, and it is not filed here — filing it is the scope overrun `[#675]` clause 1 warns about.

---

## Part 4 — the invocation, for the seat cutting the first receipt

The integrator seat asked for verb, argument shape and where it writes, so that batch Y's first receipt
is cut with one instrument rather than two. Read off `--help` at `55466a71`, not from memory. **One
receipt per merge**, opened and closed inside that merge's own block — the same sequence
`.claude/commands/lane-integrate.md` now carries.

```bash
R="merge-<lane>"; L="lane-<letter>-<id>-<slug>"

# 1. before the handback verdict, because that verdict is part of the merge's cost
merge_receipt.py open   --slug "$R" --batch y --kind merge

# 2. each step you want itemised; an UNPREFIXED step is not untimed, it lands in UNRECORDED
merge_receipt.py time   --slug "$R" --step <id> -- <command>
merge_receipt.py race   --slug "$R" ...                # concurrent steps, raced group counted once

# --- THE MERGE MUST BE PUSHED BEFORE THE NEXT LINE. See the boxed warning below. ---

# 3. the suite verdict -- this REPLACES `time --step actions -- actions_verdict.py ...`
merge_receipt.py actions --slug "$R" --sha <the MERGE commit> --baseline <its FIRST PARENT>

# 4. after `actions`, never before it; appends to logs/MERGE-RECEIPTS.jsonl, prints the summary
merge_receipt.py close  --slug "$R"

# 5. ONCE, after the last lane
merge_receipt.py median --kind merge
merge_receipt.py require --range "<the FIRST merge's first parent>..HEAD"
```

> ### CORRECTION — `actions` MUST FOLLOW THE PUSH, and the first version of this Part said otherwise
>
> **An unpushed merge commit has no Actions run**, so `actions` records `NO-RUN`, which is
> unreadable, which is INCOMPLETE, which makes **row 2d refuse the merge**. Measured against this
> lane's own unpushed tip: `actions_verdict.py --sha 057259eb --baseline 55466a71` → `NO-RUN`, with
> the tool's own remedy naming *"the push has not landed"* first.
>
> **`[#750]`'s own failure mode, reintroduced by ORDERING rather than by predicate** — a refusal
> wired to a read that happens before the thing it reads can exist would have refused all of
> batch Y and recorded `NO-RUN` as the suite state of six clean merges. Caught after `057259eb`
> and fixed in `.claude/commands/lane-integrate.md` in the following commit; the handback message
> carried the same wrong order and was corrected in a follow-up.
>
> **Workaround that needs no ruling:** merge → push → wait for the run → `actions` → `close`.
> `IN-PROGRESS` is unreadable too, so re-run `actions` under its own `--step` id when the run
> finishes — `suite_verdict()` is last-wins, so the good read supersedes it.
>
> **WHERE THE PUSH SITS IS UNRESOLVED AND IS NOT A LANE'S CALL** — escalated, not decided. This
> walk pushes **once** after the last lane while the read sits inside each lane's block, and those
> cannot both be right. **(A) push per merge:** each receipt's span stays honest, but every merge
> pays its own pre-push gates and, with no open batch manifest, forces an anchor arc per merge.
> **(B) keep one end-of-batch push**, then `actions` + `close` per merge afterwards: one push, but
> merge A's receipt stays open across B, C and D, so A's wall absorbs their ceremony — exactly the
> inflation `[#675]` exists to itemise. **(A) is the recommendation; neither was taken.**
>
> **The finding underneath predates `[#750]`.** Target 3.2 asks for *"the integrator READING the
> result"*, and this walk has read pre-push all along. Under the old code that surfaced as
> `ok=False` and disappeared into the blanket incompleteness that made `[#744]`'s predicate
> unreachable — so the impossibility was invisible. **Target 3.2 has never been satisfiable by this
> walk**, independent of the receipt work. Fixing the predicate is what exposed it.

**Where it writes.** An open receipt lives at `logs/.merge-receipt-<slug>.json`; `close` appends one
row to `logs/MERGE-RECEIPTS.jsonl` and removes the open file. `require` and `median` write nothing.

**Four things to get right, each for a reason:**

- **`--baseline` is the merge's FIRST PARENT.** Omitted, a failure is `UNATTRIBUTED`, which **cannot**
  discharge a merge — the differential is what makes the verdict mean *"what this merge changed"*.
- **`--sha` is the merge commit**, and it is what binds the receipt to the merge. Without it `require`
  cannot see the receipt at all, so step 3 is not optional garnish: it is the step that makes the
  merge receipted.
- **`actions` exits non-zero on `PRE-EXISTING`**, deliberately, and that is **not** a refusal — the
  receipt is COMPLETE. Do not wrap it in anything that treats non-zero as a failed merge; that is the
  exact conflation ruling AY1-1 exists to end.
- **`close` before `require`, and `actions` before `close`.** An open receipt is invisible to
  `require`, so an unclosed receipt looks identical to an unreceipted merge — and `close` removes the
  open receipt file, so a verdict not recorded before it can never be added afterwards.

There is **no flag on any verb** that can hand a verdict state to a receipt, on `actions`, `time` or
`close`, and a test asserts each absence. If `gh` is unavailable the merge is refused rather than
certified — see Part 3 item 9 for how that reading differs from the integrator seat's.

---

## Part 5 — for `[#752]`, sequenced behind this lane on `scripts/merge_receipt.py`

Read this before starting. Five things moved that a later lane will trip over:

1. `wall_seconds()` is now **derived** from `opened`/`closed` and is no longer a stored field that is
   read back. `recorded_seconds()` is the old arithmetic. A test that asserts on `wall_seconds()` after
   setting only step durations will now read the span.
2. `StepTiming` gained `verdict_state: Optional[str]`; `Receipt` gained `merge_sha: Optional[str]`.
   Both default to `None` and both round-trip through `to_dict`/`from_dict`.
3. `to_dict()` emits three **derived** keys — `recorded_seconds`, `unrecorded_seconds`,
   `suite_verdict`. They are outputs, not inputs; `from_dict()` does not read them back.
4. `incompleteness_reason()` is six ordered legs. The order is load-bearing: a receipt that never
   closed, or whose span cannot be read, must be refused **before** anything reads a verdict off it.
5. The module now imports `actions_verdict` through the standard dual import shim. Importing is not
   executing — `verdict_for` READS a run's conclusion and writes nothing — and `verdict_for`'s own
   `fetch` seam is passed through, so a test drives the real state machine instead of asserting a state
   it typed itself.
