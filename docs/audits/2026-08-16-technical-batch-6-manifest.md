---
batch: 6
status: open
closed_by: docs/audits/2026-08-16-technical-batch-6-packet.md
---

# Batch 6 (phase-2) — manifest, committed AT DISPATCH

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-16 · **Slug:** batch-6-manifest
- **Protocol:** ADR-110 + its 2026-08-07 amendment (the declared integration arc) + PLAYBOOK Ch8
  "The batch protocol". Width **12** dispatched (lanes a b c d e f g h i x y l), one wave.
  Lane **k** (`[#293]` cross-repo seeding) is defined in the pack but **NOT dispatched** — it is
  operator-word-gated and no word was given, so it is absent from this roster rather than
  silently carried.
- **Authority:** the phase-2 architect rulings §A1–§A10 of 2026-08-16, issued on
  `PHASE2-MAX-PACK.md` (operator's Downloads, off-repo — this manifest is its in-repo carrier
  for the parts that bind the tree). **§B step 7 is the ruling this file discharges.**
- **Predecessor:** batch 5 (phase 1) — manifest
  `docs/audits/2026-08-15-technical-batch-phase1-manifest.md`, packet
  `docs/audits/2026-08-15-technical-batch-phase1-packet.md` (both committed, so that batch is
  CLOSED). Verified live immediately before writing this file:
  `batch_manifest.open_batches(.)` → `[]`. **This manifest inherits no stale exemption and opens
  the only live batch.**

## This is the first manifest committed BEFORE its lanes run — `[#505]` leg 1

The prior **four consecutive batches** missed the commit-at-dispatch condition (batch 3 late, the
night cloud batch late, batch 4 late, batch 5 latest of all — committed at integration, after all
seven lanes had already run and been reviewed). `[#505]` leg 1 has been unmet that whole time.

**This file is committed before a single lane is dispatched.** The exact sequencing, stated so the
claim is checkable rather than asserted:

1. Position-0 acts 1–6 commit and this manifest commits as act 7, all on
   `chore/phase2-position0`;
2. that branch merges `--no-ff` to `main` and pushes;
3. **then** the twelve `claude --bg` lane sessions are dispatched.

So at the moment this file is written **none of the twelve branches exists yet**. The roster below
therefore declares the batch's INTENT — the names that will be provisioned — not observed refs, and
it says so rather than implying it enumerates live branches. The end-of-batch packet is what
records the tips actually produced. That is the honest form of "at dispatch", and it is the first
time the condition has been met at all.

## Lane roster — width 12, one wave

All twelve lanes cut from the same `main` tip, which is the merge of `chore/phase2-position0`:
**zero inter-lane git dependencies by construction.** The two `<W3_ID>` / `<DOCROT_ID>` slots the
pack left open were resolved by the Position-0 births to **531** (W3, lane-grammar) and **532**
(doc_rot arms), and the worktree names below carry the substituted ids.

| Lane | Branch (to be provisioned) | Rows | Bucket | Contract of record (at dispatch) |
|---|---|---|---|---|
| **a** | `worktree-lane-a-409-conversions` | `#409 #410 #411 #419` | finish-line | `CONTRACT-W2A.md` |
| **b** | `worktree-lane-b-210-conversions` | `#210 #285 #361` | finish-line | `CONTRACT-W2B.md` |
| **c** | `worktree-lane-c-146-conversions` | `#146 #266 #438 #443` | finish-line | `CONTRACT-W2C.md` |
| **d** | `worktree-lane-d-351-conversions` | `#351 #385 #393 #484 #502` | finish-line | `CONTRACT-W2D.md` |
| **e** | `worktree-lane-e-82-conversions` | `#82 #145 #239 #263` | finish-line | `CONTRACT-W2E.md` |
| **f** | `worktree-lane-f-130-conversions` | `#130 #274 #350 #417` | finish-line | `CONTRACT-W2F.md` |
| **g** | `worktree-lane-g-271-conversions` | `#271 #324 #391 #412 #491` | finish-line | `CONTRACT-W2G.md` |
| **h** | `worktree-lane-h-310-ledger-docs` | `#310 #428` (+ K1 declares, 14 re-annotations) | finish-line | `CONTRACT-L8-LEDGER-DOCS.md` |
| **i** | `worktree-lane-i-277-issues-evidence` | `#277` (+ 15 triage Issues) | finish-line | `CONTRACT-L9-ISSUES-EVIDENCE.md` |
| **x** | `worktree-lane-x-532-docrot-arms` | `[#532]` | **hub-introspection** | `CONTRACT-H1-DOCROT-ARMS.md` |
| **y** | `worktree-lane-y-531-grammar-gate` | `[#531]` | **hub-introspection** | `CONTRACT-H2-GRAMMAR-GATE.md` |
| **l** | `worktree-lane-l-348-detector-tests` | `#348 #426 #505` | **hub-introspection** | `CONTRACT-H3-DETECTOR-TESTS.md` |

**Every contract of record lives in the operator's prompts dir at dispatch and is committed into
the tree by its own lane's step 0.** Stated so a reader does not resolve those filenames against
`main` and conclude the manifest cites vapour: they are off-repo at this instant, by design, and
each reaches the tree when its lane commits.

## THE OFF-GRAMMAR HAZARD THAT WEDGED BATCH 5 DOES NOT EXIST HERE

Batch 5 shipped two lanes (`worktree-lane-s-w20-draft-landing`, id slot `w20`;
`worktree-lane-r-gateclose-drain8`, no id slot) that `validate_branch_naming.LANE_BRANCH_RE`
REFUSED, silently forfeiting the ADR-110 exemption and forcing a hand-anchoring workaround.
Batch 4 hit the same class and resolved it by dropping two lanes from its roster.

**All twelve names on this roster were run through that regex before this file was written**, per
§B step 9 — the same constant `batch_manifest.is_lane_merge` imports as the single definition of
the grammar:

```
pattern  ^worktree-lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$

PASS  worktree-lane-a-409-conversions        PASS  worktree-lane-g-271-conversions
PASS  worktree-lane-b-210-conversions        PASS  worktree-lane-h-310-ledger-docs
PASS  worktree-lane-c-146-conversions        PASS  worktree-lane-i-277-issues-evidence
PASS  worktree-lane-d-351-conversions        PASS  worktree-lane-x-532-docrot-arms
PASS  worktree-lane-e-82-conversions         PASS  worktree-lane-y-531-grammar-gate
PASS  worktree-lane-f-130-conversions        PASS  worktree-lane-l-348-detector-tests

TOTAL 12 | refused: 0
```

**So the ADR-110 exemption covers twelve of twelve merges.** This is the first roster to reach zero
refusals.

**The class is still not closed, and this roster does not close it.** The grammar remains enforced
nowhere at provisioning — that is exactly `[#531]`, born at Position 0 and dispatched to lane **y**
in this batch. A conforming roster is a checked roster, not a gated one: nothing prevents the next
one from being off-grammar. Lane y is the fix; this section is the measurement.

## Process-lane cap — declared EX-ANTE, and within cap

PLAYBOOK Ch8: *"at most 1/4 of a batch's lanes target methodology or hub-process surfaces"*,
evaluated against **dispatched width** (ADR-110 amendment 2026-08-08), floor arithmetic, under the
I-D10 three-way split (feature/satellite · finish-line · hub-introspection).

At width **12** the cap permits **⌊12/4⌋ = 3** hub-process lanes. The roster declares **exactly 3**:

- **x** — `[#532]`, amends the `doc_rot` detector. Hub-introspection by any reading.
- **y** — `[#531]`, arms a provisioning-time ref gate on the hub's own branch creation.
- **l** — `#348`/`#426`/`#505`, edits `tests/test_audit.py` pins and audit detector files.

**Within cap, 3 of 3, and declared BEFORE dispatch rather than reconstructed afterwards** — which is
the D10 requirement and the difference from batch 5, whose overage (2 permitted 1) was recorded
retrospectively as an exceedance. That phase-1 exceedance is carried to this batch's packet as a
register line per §A4; it is not re-litigated here.

The remaining nine lanes are `finish-line`: seven Wave-2 conversion lanes (a–g), the ledger/doc
lane (h) and the issues/evidence lane (i). None ships a feature, so the `feature/satellite` bucket
is empty this batch — lane k would have filled it and was not dispatched.

## Baseline at manifest commit

- `main` @ `ce1dade1` at arc start; this manifest commits on `chore/phase2-position0` @ `e123947c`
  and reaches `main` with the Position-0 `--no-ff` merge.
- `batch_manifest.open_batches(.)` → `[]` — no batch open, no exemption inherited.
- `docs/audits/2026-08-16-technical-batch-6-packet.md` absent from `HEAD` (the closer is live);
  `_valid_closer()` on that path → `True`.
- `python scripts/audit.py health` → **`health: OK`** on the Position-0 arc before dispatch. This
  is the baseline every later gate reading is measured against, so a WARN appearing after the queue
  is attributable to the queue rather than inherited.
- `git worktree list` = 1 entry (primary only). `git stash list` empty.
- Known carried WARNs at baseline, so they are not later mistaken for queue damage: `doc_rot` 9
  loci (7 inherited + the 2 rows born at Position 0, which are the rows that fix the detector);
  `review_artifact_coverage` 2 unlinked (both dispositioned) + 1 untallied;
  `undeclared_edges` 20; `preflight_backlog_ids` 1.
- JOURNAL entry `2026-08-16 (a)` already exists; this arc's is `(b)`, derived from `JOURNAL.md` at
  commit time rather than from any contract, and the integration wrap re-derives its own letter
  the same way.

## Two mechanical facts derived live against the parser, before writing

**1. The filename matches `MANIFEST_GLOB`.** `batch_manifest.MANIFEST_GLOB` is
`docs/audits/*-batch-*-manifest.md`, matched with `PurePosixPath.match` against the basename.
Verified against the parser itself: `2026-08-16-technical-batch-6-manifest.md` → `True`.

**2. `batch: 6` — a digit, because a test pins it.**
`tests/test_batch_manifest.py::test_the_live_repos_own_manifest_is_well_formed` asserts
`b.batch.isdigit()` against every live open manifest; batch 3's manifest shipped a date-shaped
value and was RED from the moment it landed.

## Closure contract

The batch closes when **all** of the following hold, and committing
`docs/audits/2026-08-16-technical-batch-6-packet.md` is the single act that discharges the last of
them and expires the ADR-110 exemption:

1. the merge queue is drained in the §D order **a b c e f g d h i l x y** — every lane branch
   merged with a SHA, or explicitly held with a reason (HOLD is a recorded disposition, never
   silence);
2. full suite run **once** on the merged result with the worksteal flags, verdict quoted;
3. the §D wrap items land: `SUITE_ONELINE_TOKEN` correction-by-append in the wrap JOURNAL entry,
   the untestable-denominator re-measure against live 195, promotions D3.1–D3.5, the W5 phase-1
   exceedance register line, and the explicit *"`#371` left un-ruled"* line;
4. **honest-RED is in force**: the only tolerated RED is the one known pre-existing
   `routine_consumers` live pin, which lane l may FIX — in which case 0 RED is the expectation. Any
   other RED means `main` is NOT pushed and the packet attributes the failure;
5. teardown runs for MERGED lanes only (`worktree remove` + `prune` + `branch -d`, never `-D`);
   HOLD and TIMED-OUT lanes keep their worktrees and branches untouched for the operator;
6. `git stash list` empty — a surviving entry gets a recorded disposition, never a blind `drop`;
7. the packet reports the dispatched-vs-close width delta and disposes of every HOLD by name.

## One standing consequence of an open batch, stated so it is not discovered mid-arc

`gen_handoff.assert_batch_boundary` **refuses to cut a handoff bundle while a batch is open**
(WINDOW = BATCH). Any bundle work therefore lands **after** the closing packet, which is correct
sequencing rather than an obstacle — and never a bypass.

## What this manifest deliberately does NOT do

- It does not reorder the merge queue (§D rules it), rename any branch, or delete anything.
- It does not adjudicate the phase-1 cap overage — §A4 ruled that a recorded exceedance, and this
  batch's packet carries the register line.
- It does not birth, close, or edit a single BACKLOG row. **Births — ZERO** (the two births of this
  arc are Position-0 acts, committed before this file and cited by it, not made here).
