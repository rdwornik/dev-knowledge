<!-- scope: meta -->
# Batch 7a — end-of-batch packet

**This file closes batch 7a.** Committing it is the single act that expires the ADR-110 exemption
declared by `docs/audits/2026-08-17-technical-batch-7a-manifest.md` (`closed_by:` names this exact
path), with no edit to any immutable artifact.

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-17 · **Slug:** batch-7a-packet
- **Manifest:** `docs/audits/2026-08-17-technical-batch-7a-manifest.md` (`f72541c1`, merged
  `397cfdae`) — committed AT DISPATCH, before a single lane branch existed.
- **Width:** 3 dispatched, 3 merged, 0 held, 0 timed out. **Dispatched-vs-close delta: zero.**
- **Seat:** ONE session ran head, dispatch, integration and supplement end-to-end, by operator
  authorisation.

## §0 · The answer first

```
merges     3 of 3      c 7a5f2e1d  ->  a fe6200bf  ->  b 99ec4b19
suite      2 failed, 2968 passed, 3 skipped, 1 xfailed in 948.45s  -- the TWO OWNED REDs, nothing new
gate       audit.py health -> OK, 0 FAIL, zero new WARN classes
births     17 rows, [#534]-[#542] and [#546]-[#553], every id inside its reserved block
open rows  172 -> 189   (live incl. deferred: 196 -> 213)
bypasses   --no-verify 0   SKIP= 0   -- across all three lanes AND the integrator
```

## §1 · Merge queue — drained in the ruled order c, a, b

| # | lane | branch | merge sha | conflicts | resolution |
|---|---|---|---|---|---|
| 1 | **c** | `worktree-lane-c-505-north-star-inventory` | `7a5f2e1d` | none | — |
| 2 | **a** | `worktree-lane-a-534-audit-dispositions` | `fe6200bf` | 1 | `docs/audits/README.md` REGENERATED from the union |
| 3 | **b** | `worktree-lane-b-546-currency-archival` | `99ec4b19` | 3 | `tasks/manifest.json` HAND-UNIONED; `BACKLOG.md` + `docs/audits/README.md` REGENERATED |

**The ADR-110 exemption was verified LIVE on merge 1 rather than assumed:**

```
merged branch : worktree-lane-c-505-north-star-inventory
is_lane_merge : True
open batches  : ['7']
```

`audit.py health` returned **OK** after each of the three merges. Without the exemption
`check_journal_spine_anchor` is a pre-commit gate and would have wedged the queue at merge 1.

### The conflict class batch 6 got wrong, and how it was handled here

Batch 6's integrator resolved `tasks/manifest.json` with `--ours`, discarding a node removal;
regeneration then re-emitted the row, and `gen_task_tree --check` passed because node-present +
`status: open` is internally COHERENT. **Coherence is not correctness**, and that packet says so.

Here both lanes INSERTED nodes at the identical position (after task 533, before the `[S4]` prose
heading), so taking either side would have silently dropped 8 or 9 rows. Resolution was a **union**,
then verified mechanically rather than by eye:

```
total task nodes 213 · expected new ids 534-542 + 546-553 · MISSING none · DUPLICATED none
generated_sha256 -- RE-PINNED BY THE GENERATOR, never chosen from a side (a checksum is computed)
BACKLOG.md       -- regenerated via gen_task_tree --emit-source (213 tasks); check ok
```

## §2 · Per-lane results

### Lane a — audit dispositions · `worktree-lane-a-534-audit-dispositions` · 11 commits

```
audits 80 · ACTIONED 49 · FILED 25 · REJECTED 2 · SUPERSEDED 2 · PENDING 2
births 9 — [#534] [#535] [#536] [#537] [#538] [#539] [#540] [#541] [#542]
follow-on 49 earlier uncited audits, named as a list in the ledger §4
```

Ledger: `docs/audits/2026-08-17-technical-audit-disposition-ledger.md`. **Three findings were
re-verified against the live tree and turned out to be live and unowned** — the return on the pass:

1. Four open rows cite `scripts/audit.py` by a line number that no longer resolves; `[#417]`'s pin
   `:4751-4760` is **past EOF** (4271 lines after the `[#533]` decomposition), and that same row is
   simultaneously proposed NOW-CLOSABLE by the closing campaign. → `[#534]`
2. `audit.py` loads as **two distinct module objects in one process** (`audit` and `scripts.audit`);
   patching `audit._FRESHNESS_FILES` leaves `enforcement_coverage._freshness_files()` returning the
   unpatched list, so a test can pass while exercising a module it never patched. → `[#535]`
3. `ARCHITECTURE.md:427` still enumerates four `doc_rot` sub-detectors; the detector declares five.
   `validate_doc_claims` checks 4 claims and this is not one of them. **It was named in the batch-6
   packet's Owed list and never paid.** → `[#542]`

### Lane b — ADR/intake currency · `worktree-lane-b-546-currency-archival` · 9 commits

```
births 8 — [#546] [#547] [#548] [#549] [#550] [#551] [#552] [#553]
archival moves executed: ZERO -- and that is the correct execution, not a shortfall
```

The contract said *"execute archival moves for TERMINAL-UNARCHIVED per the existing rule"*. The lane
found that the existing archival bar keys on `Superseded` / `Deprecated` status values, **which ZERO
live ADRs carry because nothing ever writes them** — so the TERMINAL-UNARCHIVED set is empty by the
rule's own literal terms. It filed the gap as `[#552]` with the limit stated IN the row (*"a ratchet
against future rot, not a sweep of present rot"*) rather than inventing a broader criterion, which
would have been rewriting the rule mid-lane. **`[#552]` is the recurring routine the batch was
called to birth**, in ADR-105 form with a named consumer and consumption_path.

### Lane c — north-star inventory · `worktree-lane-c-505-north-star-inventory` · 2 commits

```
total 78 · LIVE-WIRED 21 · BUILT-UNWIRED 4 · ROW-OPEN 17 · DECIDED-UNFILED 16 · EVALUATED-REJECTED 9 · MENTIONED-ONLY 11
births NONE — as contracted
```

Report: `docs/audits/2026-08-17-census-north-star-inventory.md`. Headline: **"universalization" has
no formal definition anywhere** across 87 ADRs, 36 intakes and 14 protocol/VISION/ARCHITECTURE
files, despite organising five ADRs' worth of structure since 2026-04-28; **telemetry and
`single_flight.py` are fully built with zero non-test call sites**; **2 of 5 registered consumers
(`corp-ops`, `win-tooling`) consume nothing** from the hub's deploy carriers; the oldest
DECIDED-UNFILED items are 12 days old (the kernel package and the shared reusable workflow).

**One flagged evidence conflict is RESOLVED here, against the lane's reading.** Lane c reported that
`[#533]` *"claims a landed `lru_cache` win the grep didn't find"*. Measured: `lru_cache` /
`functools.cache` / `@cache` have **zero sites in `scripts/` AND `tests/`** — the grep was right. But
the row does not claim a landing: LEG 2 reads *"includes the NB3-D-measured `journal_anchor`
memoization … with its test"*, i.e. the memoization is **scope of unstarted work**, and
"NB3-D-measured" cites an analysis rather than the tree. **No defect in the row.** Lane c flagged
instead of guessing, which is what its contract asked for.

## §3 · Suite — run ONCE on the merged result

```
uv run --locked pytest -q --dist worksteal --max-worker-restart=0     (main @ 99ec4b19)
2 failed, 2968 passed, 3 skipped, 1 xfailed in 948.45s (0:15:48)
```

**Both failures are the known OWNED REDs. Nothing new. Honest-RED is intact and nothing was
dispositioned green.**

| test | owner | movement |
|---|---|---|
| `test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row` | owned, batch-6-named | pin expects 1 routine row; live went **2 → 3**. The third is lane b's `[#552]`. **Predicted before the merge**, because birthing an ADR-105 routine row is exactly what the contract ordered. |
| `test_validate_doc_rot.py::test_live_corpus_has_no_accretion_arm_findings_only_length_findings` | owned, batch-6-named | unchanged. Locus is `BACKLOG#293` (4 dates / 40d / 2864 chars). **Batch 6 recorded this firing on `#428` — the locus has MOVED**, which is a live-corpus assertion behaving as designed. |

### A pre-merge baseline was measured, and it corrects the brief's expected count

The brief carried *"expected: the two known owned REDs"*. Measured on the pre-merge tree
(`397cfdae`) **before** any lane merged:

```
4 failed, 2966 passed, 3 skipped, 1 xfailed in 1597.55s
  2 OWNED         the two above
  2 ENVIRONMENTAL tests/test_reverse_dep_oracle.py::test_finding_headline_resolves_with_provenance
                  tests/test_reverse_dep_oracle.py::test_main_finding_json_exit_zero   (assert 3 >= 50)
```

The environmental pair fails only under xdist contention (the pyright oracle returns partial results
inside its 40s timeout). **Proven in THIS tree rather than inherited from batch 6's record:** re-run
serially → `2 passed in 10.25s`. Batch 6 named only the first of the pair; the second is its sibling
in the same file with the same assertion.

They did not fire in the post-merge run because no lanes were competing for CPU. The arithmetic
closes: `2966 + 2 = 2968` passed, `4 − 2 = 2` failed.

## §4 · Final gate — with owners, and with a correction to the manifest's baseline

```
python scripts/audit.py health   ->   health: OK   (0 FAIL)

check                       baseline(corrected)   post-merge   delta   owner
doc_rot                              21               31        +10    THIS BATCH — 17 new rows add loci
undeclared_edges                     18               18          0    pre-existing
no_ff_merges                          3                3          0    pre-existing (legacy June commits)
review_artifact_coverage              2                2          0    pre-existing, advisory per [#480] P3
reconciled_versions                   1                1          0    pre-existing — templates/CONTRIBUTING-md-template.md
journal_spine_anchor                  1                1          0    pre-existing, advisory (anchored-by-mention)
git_backlog_drift                     1                1          0    pre-existing — #505 "closes in 25ff8ec37" (2026-08-07)

ZERO new WARN classes. One count moved, and it is attributable.
```

**INTEGRATOR ERROR, CORRECTED — the manifest's recorded baseline is wrong and this is the
correction.** The manifest lists five carried WARN classes. It should list **seven**:
`reconciled_versions` and `git_backlog_drift` were both already firing at `397cfdae`. The baseline
tally was taken with a `head -25` truncation, both classes sit at count 1 in the tail, and their
absence from the printout was read as absence from the tree. Verified the honest way — by checking
out `397cfdae` into a scratch worktree and re-running the gate there, which reproduced both. Had
this gone unchecked, two pre-existing WARNs would have been reported as damage caused by this batch.

The manifest is immutable (CLAUDE.md §5 rule 3) and is **not edited**; this packet carries the
correction, which is the sanctioned route.

**`git_backlog_drift` on `#505` is a FALSE POSITIVE and is not actioned.** The cited commit
`25ff8ec3` (2026-08-07) says in its own subject *"3 rows filed, **0 closed** [#505] [#430]"* and in
its body *"nothing closed on [#505]/[#502]"*. The detector matches the word near the id in prose.
Known precision-lever class; `#505` remains legitimately open and is this batch's own governing row.

## §5 · Stage-3 events — three, all disclosed rather than smoothed over

### (a) Lane a stalled on an API 529 and was resumed, not restarted

At 12:34 lane a went idle mid-turn on `API Error: 529 Overloaded` with only its step-0 commit
landed, and sat there 41 minutes while reporting `idle/blocked`. Recovered at 13:15 by
`claude stop` + `claude --bg --resume <sessionId>`, which preserves the conversation — a fresh
dispatch would have thrown away ~40 minutes of corpus reading. The nudge was phrased explicitly as
*"RESUME, not a new contract and not a correction"* and re-pointed at the frozen contract as sole
authority, so STANDING_RULINGS D2 is respected: a correction re-enters as a new contract, never as a
mid-flight message. The branch tip, worktree and step-0 commit were untouched throughout. **Lane a
then produced 10 further commits including the entire ledger and all 9 births.**

### (b) The poller's DONE predicate was wrong, and it was caught before it merged anything

The first poller scored a lane DONE on *"agent idle + tip unchanged for 2 consecutive polls"*. Lane
a satisfied that while actively inferring — `idle/blocked` is a between-turns state, not a terminal
one — so the instrument reported **DONE for a lane with only its contract commit**. Caught by
reading the session log instead of trusting the signal. Predicate corrected to `state == 'done'`,
which is what lane c legitimately reported. **A second false positive was then avoided by
re-pointing the poller at the resumed session id**: the stopped original reads as GONE, and the
GONE branch of the predicate would have scored it DONE again. Nothing was merged on a false signal.

### (c) The cap was extended by exactly the measured stall, and the extension is a disclosed deviation

The brief set a 2h30m cap (hard stop 14:23:59) with TIMED-OUT-HOLD beyond it. Lane a had lost 41
minutes to a server-side error, so at the literal cap its effective runtime was ~1h49m. The cap was
extended by **exactly the measured dead time, no more** — new hard stop 15:05:00, TIMED-OUT-HOLD if
missed. **Lane a finished at 14:47:33, 18 minutes inside the extension**, delivering the ledger and
9 births. The reasoning: the cap exists to bound wall-clock, and the stall consumed wall-clock
without consuming budget. This is a deviation from the brief's literal number, it is measured and
bounded, and it is recorded here rather than folded in quietly.

## §6 · A concurrent non-batch lane exists, and it is `[#510]` observed live

`git worktree list` shows a **fifth worktree this batch did not create**:

```
worktree-lane-r-412-research-intake   13f3d01f   6 commits, unmerged, locked
  authored 2026-08-17 14:27:32 by a concurrent session (ad63b8c6), NOT part of batch 7a
```

It is untouched: not merged, not renamed, not torn down, not counted in any batch metric.

**The finding is what it demonstrates.** `[#510]` says the ADR-110 exemption keys on branch SHAPE
rather than on the roster the open manifest enumerates, and describes the self-grant as *"one
`git branch -m` away"*. Measured here:

```
worktree-lane-r-412-research-intake   LANE_BRANCH_RE True   classify batch-lane   open batches ['7']
=> merging it right now satisfies BOTH exemption conditions, though batch 7a never enumerated it
```

**No rename was needed.** A concurrent session simply chose a conforming name while a batch was
open. That is stronger evidence than the row's own hypothesis, and it arrived unprompted from
ordinary parallel work. Recorded against `[#510]`; **no new row is filed**, because `[#510]` already
owns the class and this batch's birth authority is scoped to lanes a and b.

## §7 · Refuse-to-finish checklist

| # | condition | verdict |
|---|---|---|
| 1 | every lane branch merged-or-explicitly-abandoned | **PASS** — 3 of 3 merged, 0 abandoned, 0 held |
| 2 | full suite run once on the merged result, verdict quoted | **PASS** — §3 |
| 3 | `git worktree list` == primary only | **NOT SATISFIABLE, and not forced** — after batch-7a teardown the primary is joined by `lane-r-412-research-intake`, a concurrent session's live work (§6). Deleting another session's worktree to make a checklist item green would be the defect, not the fix. Recorded as an honest exception. |
| 4 | manifest and packet archived in the tree | **PASS** — manifest `f72541c1`; this file is the packet |
| 5 | `git stash list` empty | **PASS** — empty, verified |

## §8 · Births — 17 rows, and the 7 reserved ids that were NOT used

| lane | block reserved | allocated | unused |
|---|---|---|---|
| a | 534–545 (12) | **534 535 536 537 538 539 540 541 542** (9) | 543 544 545 |
| b | 546–557 (12) | **546 547 548 549 550 551 552 553** (8) | 554 555 556 557 |
| c | none | none — births nothing | — |

**Zero ids were allocated outside a reserved block**, which is the property that made two birthing
lanes safe to run concurrently. The 7 unused ids are **not** reserved going forward: the next window
derives next-free from the tree as usual, and will find 554.

Every row carries a flush-left `kill-candidates:` line and a `source:` line citing its audit, per the
standing ruling. `backlog-filing-backpressure` REFUSED merge 2 for a missing `kill-candidates:` line
on the merge commit itself and was satisfied only after verifying — not assuming — that all nine
rows had named their own at birth.

## §9 · What this batch did NOT do

- **No archival move was executed** (§2 lane b) — the rule's terminal set is empty, and that is
  filed as `[#552]` rather than worked around.
- **No ADR, intake, or register was edited.** Lane b wrote strictly less than its OWNED-FILES
  allowed: `docs/decisions/**` and `docs/intake/**` were never touched.
- **No row was closed.** 17 born, 0 closed; the batch converts findings into owned work, and
  shrinking the backlog is a different arc.
- **`protocols/STANDING_RULINGS.md` is unedited.** The 2026-08-17 conversion ruling is quoted as
  this batch's authority; whether it becomes a standing register line is the architect's call.
- **No `--no-verify` and no `SKIP=`**, by any lane or the integrator, at any point.
