---
batch: 4
status: open
closed_by: docs/audits/2026-08-11-technical-batch-4-packet.md
---

# Batch 4 — manifest, committed MID-FLIGHT (after dispatch, before the merge queue)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-11 · **Slug:** batch-4-manifest
- **Protocol:** ADR-110 + its 2026-08-07 amendment + PLAYBOOK Ch8 "The batch protocol".
  Width **6** dispatched (W1–W6), one wave.
- **Authority:** the batch-4 GO of 2026-08-11 (`3aaf5140`, merged `3b711e87`) — intakes #28–#32
  ratified as one act, `[#513]` amended, `[#521]`/`[#522]` born; plus the operator's unblock
  directive of this session naming the W1–W6 roster below.
- **Predecessor:** the 2026-08-09/10 night cloud batch — manifest
  `docs/audits/2026-08-10-technical-batch-night-cloud-manifest.md`, packet
  `docs/audits/2026-08-10-technical-batch-night-cloud-packet.md` (both committed, so that batch is
  CLOSED). Verified immediately before writing this file: `batch_manifest.open_batches(.)` → `[]`.
  **This manifest inherits no stale exemption and opens the only live batch.**

## Provenance — why this file is late, stated rather than concealed

> **This manifest is committed MID-FLIGHT, not at dispatch.** Batch 4 was dispatched without one;
> W1 and W2 are already provisioned and running (`worktree-lane-a-514-lane-regex`,
> `worktree-lane-b-270-fleet-audit`, both locked worktrees with commits). It declares the batch
> OPEN in the present tense so the merge queue can run under the ADR-110 exemption; it does not
> claim to have existed earlier, and no timestamp in it is back-dated. Batch 2's "commit the
> manifest at DISPATCH" condition stands as the correct practice and was **not** met by batch 4.

This is the **third consecutive batch** to miss the dispatch condition (batch 3 late, the night
cloud batch late, batch 4 late). Recorded as a recurrence, not as news: `[#505]` leg 1 remains
unmet, and this file is a partial repair of that regression, **not** a discharge of the row.

**What the lateness cost here, precisely.** W1's contract step 0 is *"copy THIS file byte-identical
… beside the batch-4 manifest (the manifest's W1 row names the path) … update the manifest W1 row
from PENDING-CONTRACT to the committed path in the same commit."* With no manifest in the tree
there is no W1 row to name a path and none to update — **step 0 was literally unexecutable**, which
is the unblock this file discharges. W1 and W2 each self-served the first half anyway, committing
their contract of record to their own lane branch (see the roster), so only the row-update half was
stranded; this manifest lands those two rows already resolved.

**Expiry is automatic and needs no edit.** `docs/audits/` is immutable (CLAUDE.md §5 rule 3), so
openness is deliberately not a mutable flag anyone flips: this batch is open exactly while
`docs/audits/2026-08-11-technical-batch-4-packet.md` is ABSENT from the committed tree, and the
packet's landing ends the exemption with no edit anywhere. Verified absent from `HEAD` before
writing (`git cat-file -e HEAD:<packet>` → does not exist).

## Lane roster — width 6, one wave

Each lane names its **contract of record** — the in-repo path, per the I-D3 self-serve rule that
a contract living only in the prompts dir is not a fact in the tree.

| Lane | Worktree / branch | Rows | Bucket | Contract of record |
|---|---|---|---|---|
| **W1** | `worktree-lane-a-514-lane-regex` | `[#514]` + `[#510]` | hub | `docs/audits/2026-08-11-technical-batch-4-w1-lane-contract.md` |
| **W2** | `worktree-lane-b-270-fleet-audit` | `[#270]` | feature | `docs/audits/2026-08-11-technical-batch-4-w2-lane-contract.md` |
| **W3** | `worktree-lane-c-513-landing-predicate` | `[#513]` (as amended) | finish-line | **PENDING-CONTRACT** |
| **W4** | `worktree-lane-d-conversions-w1` | census P1/P2 conversions | finish-line | **PENDING-CONTRACT** |
| **W5** | `worktree-lane-e-132-<slug>` | `[#132]` | feature | **PENDING-CONTRACT** |
| **W6** | `worktree-lane-f-arch-soft-obs` | I-D2 scope | hub | **PENDING-CONTRACT** |

**The two resolved contracts are committed on their LANE BRANCHES, not on `main`** — stated so a
reader does not resolve them against `main` and conclude the manifest cites vapour:

- W1 — `e0de6bba` on `worktree-lane-a-514-lane-regex` (lane tip `b412ba7d` at manifest commit)
- W2 — `7ef6f50f` on `worktree-lane-b-270-fleet-audit` (lane tip = that commit at manifest commit)

Both reach `main` when their lane merges. The four `PENDING-CONTRACT` rows are lanes not yet
dispatched or not yet self-served; each resolves by its own step 0.

**On the row-update leg, and the immutability tension it carries.** W1/W2 land here already
resolved, so neither needs to touch this file. W3–W6 flipping `PENDING-CONTRACT` to a path would
be an **in-place edit of an immutable `docs/audits/` artifact** (CLAUDE.md §5 rule 3). The batch-3
manifest hit the same wall and resolved it with an appended, fully-disclosed amendment marker —
that is the standing precedent and the safe default here: **append a marker, never silently
rewrite a row**, and the end-of-batch packet carries the final contract paths regardless. This
manifest **records the tension; it does not rule on it.** A contract instruction that requires
editing an immutable artifact is a defect in the instruction, and it is filed as an observation
for the packet rather than adjudicated by the file it is about.

## Two mechanical facts derived live against the parser, before writing

**1. The filename matches `MANIFEST_GLOB`.** `batch_manifest.MANIFEST_GLOB` is
`docs/audits/*-batch-*-manifest.md`, matched with `PurePosixPath.match`. Verified against the
parser, both spellings that were in play:

```
True   2026-08-11-technical-batch-4-manifest.md
False  2026-08-11-technical-batch4-manifest.md
```

The unhyphenated `batch4` spelling **fails the glob** — there is no `-batch-` token to consume. A
manifest the reader cannot enumerate declares nothing. The name also satisfies
`validate_hermetization` Rule B: class token `technical` from the closed ADR-101 11-class enum,
slug `batch-4-manifest` lowercase-kebab.

**2. `batch: 4` — a digit, because a test pins it.**
`tests/test_batch_manifest.py::test_the_live_repos_own_manifest_is_well_formed` asserts
`b.batch.isdigit()` against every live open manifest; batch 3's manifest shipped
`batch: 2026-08-08-batch-3` and was RED from the moment it landed. The field is reporting-only —
`batch_manifest` reads it as `fm.get("batch", "?")` and gates openness on `status:` and
`closed_by:` alone — but a malformed value leaves the mechanism working while failing the repo's
own well-formedness pin, which is the class that survives a batch and is inherited by the next.
`_valid_closer()` was likewise run against the `closed_by` value above → `True`.

## THE ONE HAZARD THIS BATCH CARRIES INTO ITS OWN MERGE QUEUE — stated so it is not discovered mid-arc

**W1's deliverable can strand W4 and W6.** W1 unifies the two rival `LANE_BRANCH_RE` constants onto
the STRICT grammar (`^worktree-lane-[a-z]-\d+-<slug>$`) and scopes `exempt()` to it (`[#510]`).
Four of the six dispatched branch names carry an `<id>`; **two do not.** Measured live against both
constants at manifest commit:

```
branch                                     strict  loose
worktree-lane-a-514-lane-regex             True    True
worktree-lane-b-270-fleet-audit            True    True
worktree-lane-c-513-landing-predicate      True    True
worktree-lane-d-conversions-w1             False   True
worktree-lane-e-132-organ-index            True    True
worktree-lane-f-arch-soft-obs              False   True
```

Today the ADR-110 exemption keys on the **loose** constant, so all six are covered. **The moment
W1's steps 1–2 land on `main`, W4 and W6 stop being lane merges for exemption purposes** — their
merges would produce unanchored first-parent spine entries with no exemption, i.e. the exact
`audit-health` wedge batch 3 hit at merge #1. This was foreseen in the batch-4 execution-plan draft
(§3.2, which recorded `lane-f-architecture-soft-sweep` as **REFUSED** by the strict validator) and
it is now a live property of the dispatched roster.

**Three ways out, none of them taken here** — the choice is the integrator's or the operator's, and
naming it in the manifest is the point:

1. **Order the queue so W4 and W6 merge BEFORE W1.** Costs nothing, needs no rename, and is the
   only option that changes no artifact. This manifest recommends it.
2. **Rename the two branches** to carry a sentinel id (the draft's `lane-f-0-…` device — `\d+`
   accepts `0`). Costs a worktree rename mid-flight.
3. **Anchor those two merges by hand** — a JOURNAL entry naming each merge's introduced SHA, which
   is what the exemption exists to avoid doing five times per batch.

**W1 must not resolve this by loosening the grammar.** Its own contract forbids it ("anything that
stops matching is a finding, not a reason to widen"), and widening to fit two badly-named branches
would silently re-bless the id-less shapes the row exists to eliminate.

## Process-lane cap — the arithmetic, reported not adjudicated

PLAYBOOK Ch8: *"at most 1/4 of a batch's lanes target methodology or hub-process surfaces"*,
evaluated against **dispatched width**. At width 6 that permits **1** whole lane. The roster as
dispatched carries **2** lanes in the `hub` bucket (W1, W6) — W1's own contract names itself "the
batch's cap slot", which W6 then makes a second occupant. If the two `finish-line` lanes (W3, W4)
count as hub-process rather than product, the ratio rises further.

**This is recorded, not ruled.** The operator dispatched this roster with these buckets; the cap is
doctrine carried by intake #27 and is mechanized in nothing, and a manifest is not the place to
overturn a dispatch. Ch8 requires the **end-of-batch packet** to report the close-width delta —
this line is the input to that report, so the overage is discharged deliberately or recorded as a
known exceedance, never discovered afterwards.

## Baseline at manifest commit

- `main` @ `5259b0f0`, pushed, working tree clean at branch time; integration branch
  `docs/batch-4-manifest`.
- `batch_manifest.open_batches(.)` → `[]` — no batch open, no exemption inherited.
- `docs/audits/2026-08-11-technical-batch-4-packet.md` absent from `HEAD` (the closer is live).
- `git worktree list` = 3 entries: primary + `lane-a-514-lane-regex` (`b412ba7d`, locked) +
  `lane-b-270-fleet-audit` (`7ef6f50f`, locked). W3–W6 not yet provisioned.
- JOURNAL entries `(a)`–`(i)` already exist for 2026-08-11; this arc's is the next free letter,
  derived from `JOURNAL.md` at merge time rather than from any contract.

## Closure contract

The batch closes when **all** of the following hold, and committing
`docs/audits/2026-08-11-technical-batch-4-packet.md` is the single act that discharges the last of
them and expires the ADR-110 exemption:

1. the merge queue is drained — every lane branch merged with a SHA, or explicitly abandoned with
   a reason;
2. every `PENDING-CONTRACT` row above has resolved to a committed in-repo contract path, or the
   lane is recorded as never dispatched;
3. the named rows are closed with ADR-65 evidence: `[#514]` `[#510]` `[#270]` `[#513]` `[#132]`;
4. full suite run once on the merged result;
5. teardown complete — `git worktree list` == primary only, F1 verify-before-destroy on every
   removal, and **both** branches per teardown (work + provisioning);
6. `git stash list` empty — a surviving entry gets a recorded disposition, never a blind `drop`;
7. the packet reports **opened / closed / net / open-total**, states the filter `open-total` was
   measured on (STANDING_RULINGS H2), records the **dispatched-vs-close width delta**, and
   disposes of the two observations this manifest files: the **process-lane cap overage** and the
   **strict-grammar stranding of W4/W6**.

## One standing consequence of an open batch, stated so it is not discovered mid-arc

`gen_handoff.assert_batch_boundary` **refuses to cut a handoff bundle while a batch is open**
(WINDOW = BATCH). Any bundle work in this batch therefore lands **after** the closing packet, which
is correct sequencing rather than an obstacle — and never a bypass.

## What this manifest deliberately does NOT do

- It does not adjudicate the process-lane cap overage, rename any branch, or reorder the merge
  queue — it names all three as the integrator's or operator's call.
- It does not rule on the immutability tension in the W3–W6 row-update leg; it names the batch-3
  amendment-marker precedent as the safe default.
- It does not birth, close, or edit a single BACKLOG row. **Births — ZERO.**

---

## AMENDMENT — 2026-08-11, integrator rulings (browser seat), recorded as markers not row edits

**Nothing above this line is altered, and the frontmatter is untouched** — `status: open` and
`closed_by:` stand, so the batch stays open and the ADR-110 exemption is unchanged by this
amendment. The two hazards this manifest filed came back ruled; both rulings are recorded here as
appended markers, per the batch-3 precedent this same seat has now ratified as standard (A-4 below).

### A-1 · W6 is DROPPED from the batch-4 active roster

The W6 row above (`worktree-lane-f-arch-soft-obs`, I-D2 scope, hub bucket) leaves the active
roster. **Active width becomes 5 (W1–W5).** Reasons as ruled, all three recorded:

1. **optional** — the lane is not load-bearing for any other lane's completion;
2. **collides with live W2 on `ARCHITECTURE.md`**;
3. **carries no id** — `worktree-lane-f-arch-soft-obs` is rejected by the strict lane grammar.

**Reason 2 is recorded as ruled but was NOT corroborated at recording time, and saying so is the
point of a register.** Measured against the tree when this marker was written: W2's contract of
record (`7ef6f50f`) does not name `ARCHITECTURE.md` anywhere, and `git diff --name-only
main...worktree-lane-b-270-fleet-audit` returns `.gitignore`, the contract itself,
`docs/audits/README.md`, `ecosystem/doc-counts.md`, `scripts/fleet_health.py` and
`tests/test_fleet_health.py` — no `ARCHITECTURE.md`. The same probe against
`worktree-lane-a-514-lane-regex` also returns zero `ARCHITECTURE.md` paths. W2 is mid-flight, so
its final footprint may still grow to meet the claim; it had not at recording time. **The drop is
not weakened by this**: reasons 1 and 3 are independently sufficient, and reason 3 is verified
(the strict-grammar measurement is in the hazard section above). Recorded rather than smoothed
over, so a later reader does not inherit an uncorroborated collision as established fact.

### A-2 · W4 is not contracted until it carries a row id — G-2 resolved as ids-before-contract

The W4 row above (`worktree-lane-d-conversions-w1`, census P1/P2 conversions) stays
`PENDING-CONTRACT` and is **gated**: it becomes contractable once its work carries a BACKLOG row
id, not before. This resolves G-2 in the **ids-before-contract** direction — a lane is named from
a row, rather than a row being back-filled to fit a lane already dispatched.

### A-3 · Consequence: both filed hazards are resolved by REMOVAL, not by ordering — W1 is not delayed

The manifest's hazard section recommended merging W4/W6 before W1. **That recommendation is
superseded**, and the ruling is the better instrument:

- **The stranding hazard dissolves.** Its whole content was that two id-less branches would lose
  the exemption the moment W1's strict-grammar unification landed. W6 leaves the roster; W4 cannot
  be contracted until it carries an id, and a lane named `lane-d-<id>-conversions-w1` satisfies the
  strict grammar. **The id-less set becomes empty**, so W1's deliverable strands nothing and needs
  no delay.
- **The cap overage clears.** At active width 5 the ≤1/4 cap permits 1 hub-process lane; with W6
  gone, W1 is its sole occupant.

This is worth stating plainly because it inverts the manifest's own recommendation: the hazard was
real, and the fix was to change the roster rather than the queue order.

### A-4 · The amendment-marker route for manifest row flips is RATIFIED as standard

The manifest above recorded a tension — a lane contract instructing a lane to flip its own
`PENDING-CONTRACT` row would edit an immutable `docs/audits/` artifact (CLAUDE.md §5 rule 3) — and
named the batch-3 appended-marker precedent as the safe default without ruling on it. **That
default is now the ratified standard**: a manifest row flip lands as an appended, fully-disclosed
amendment marker, never as a silent in-place rewrite of the row. This marker is itself the first
application of the ratified form.

### A-5 · `[#505]` leg 1 — the mid-flight manifest is packet input

The provenance section's observation — this manifest was committed mid-flight, the **third
consecutive batch** to miss the commit-at-dispatch condition — is carried forward as **input to the
end-of-batch packet**, alongside the two dispositions above. It closes nothing: `[#505]` leg 1
stays unmet and this batch does not discharge it.

### Merge order and current posture

Merge order is unchanged and stays **on the seat's APPROVE, as lanes finish** — no queue order is
fixed by this amendment. The batch is HELD for lane packets.

---

## AMENDMENT — 2026-08-11, appended by W5: the W5 row resolves to a committed contract path

**Appended, not edited.** The roster table above still reads `PENDING-CONTRACT` in the W5 row and
that row is left byte-untouched: `docs/audits/` is immutable (CLAUDE.md §5 rule 3 — *"supersede
with a new file or an in-file amendment marker; never edit in place"*), and this file's own
"row-update leg" section names the batch-3 appended-marker device as the safe default. This is
that device, used as named. A reader resolving the W5 row reads the table **and** this marker.

**The resolution.**

| Lane | Worktree / branch | Rows | Bucket | Contract of record |
|---|---|---|---|---|
| **W5** | `worktree-lane-e-132-feature` | `[#132]` | feature | `docs/audits/2026-08-11-technical-batch-4-w5-lane-contract.md` |

The contract is committed **on the lane branch `worktree-lane-e-132-feature`, not on `main`** —
the same standing this file records for W1 and W2 — and it is byte-identical to the prompts-dir
original `W5-LANE-132-FEATURE.md` (SHA256
`cdcb3b9783a058e1fbfa0733a815eeba5670f85cca784cada65b70c392f29f99`, both files hashed and compared
before the commit). It reaches `main` when W5 merges.

**Two facts the roster's own numbers get slightly wrong, corrected here rather than in place.**

1. **The dispatched slug is `feature`, not `organ-index`.** The strict/loose measurement table in
   "THE ONE HAZARD" above enumerates `worktree-lane-e-132-organ-index`, which is the name the
   execution-plan draft anticipated; the branch the operator actually dispatched is
   `worktree-lane-e-132-feature`. **The hazard's conclusion is unchanged** — re-measured live in
   this lane against `validate_branch_naming.LANE_BRANCH_RE`, `worktree-lane-e-132-feature` →
   `True`, so W5 carries an `<id>` under the strict grammar exactly as the row predicted and is
   **not** one of the two lanes W1's deliverable can strand. W4 and W6 remain the only two.
2. **W5 is dispatched, so the "W3–W6 not yet provisioned" baseline line is one lane stale.** At
   this commit `git worktree list` reads 4 entries: primary + `lane-a-514-lane-regex` +
   `lane-b-270-fleet-audit` + `lane-e-132-feature` (all three lanes locked). Recorded as drift in
   a point-in-time baseline, not as a defect — the baseline section is accurate as of the
   manifest's own commit and is not being rewritten to stay current.

**Disjointness re-witnessed at this commit, per STANDING_RULINGS G2** (witnessed footprints, never
row prose). `git diff --name-only main...<lane>` against both live lanes:

- **substantive-file overlap with W1 and W2: ZERO.** W1 holds `scripts/batch_manifest.py`,
  `tests/test_batch_manifest.py`, `CLAUDE.md`, `templates/claude-regions/session-start-protocol.md`,
  `tasks/510-*`, `tasks/514-*`; W2 holds `.gitignore`, `scripts/fleet_health.py`,
  `tests/test_fleet_health.py`. W5's footprint intersects neither set.
- The files W5 *does* share with them — `docs/audits/README.md`, `ecosystem/doc-counts.md`,
  `BACKLOG.md`, `tasks/manifest.json`, `JOURNAL.md` — are **generated or batch-coordination
  surfaces, excluded from the disjointness question** by the execution-plan draft §5.2 ("Generated
  files … are excluded … by the §4 clause and the ARC-5 resolve-by-regeneration precedent"). W1 and
  W2 already both touch the first two. This is reported, not treated as the contract's
  STOP-and-report trigger, because a reading under which it were would make every lane in every
  batch stop at step 0.
- **`CLAUDE.md` and `ARCHITECTURE.md` are OUT OF SCOPE for W5**, per its contract's "What NOT to
  do" and the execution-plan draft §5.2 one-owner rule. W5 therefore **owes the integrator a
  `CLAUDE.md` §9 pre-commit-roster row** for the freshness hook it ships. That owed row is named
  again in W5's end packet.
