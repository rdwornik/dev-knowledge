---
batch: 0
status: open
closed_by: docs/audits/2026-08-10-technical-batch-night-cloud-packet.md
---

# Night batch, 2026-08-09/10 (cloud lanes N-A · N-B · N-C) — manifest, committed at INTEGRATION

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-10 · **Slug:** batch-night-cloud-manifest
- **Protocol:** ADR-110 + PLAYBOOK Ch8 "The batch protocol". Width **3**, one wave, read-only.
- **Authority:** operator dispatch of the evening of 2026-08-09; archived by the ARC-5 integration
  arc of 2026-08-10.
- **Predecessor:** the 2026-08-09 night batch — manifest
  `docs/audits/2026-08-09-technical-batch-night-manifest.md`, packet
  `docs/audits/2026-08-09-technical-batch-night-packet.md` (both committed, so that batch is
  CLOSED and no exemption was live when this file landed; verified by
  `batch_manifest.open_batches(.)` → `[]` immediately before writing).

## Provenance — why this file is committed at INTEGRATION, and why that costs nothing here

> **This manifest is committed at INTEGRATION, not at dispatch.** The night batch of 2026-08-09/10
> was dispatched without one — recorded here rather than concealed, in the shape batch 3's manifest
> established. It declares the batch OPEN in the present tense so the integration arc can archive
> it against a fact in the tree; it does not claim to have existed earlier, and no timestamp in it
> is back-dated. "Commit the manifest at DISPATCH" stands as the correct practice and was not met.

**What that lateness did NOT cost, stated precisely, because the batch-3 precedent would predict a
cost that did not arrive here.** Batch 3's late manifest was expensive because the missing ADR-110
declared-integration-arc exemption made its ten-branch merge queue mechanically unrunnable. This
batch is immune to that failure for two independent reasons, and **either one alone is sufficient**:

1. **The lanes merged nothing and the queue is one branch long.** All three lanes ran **read-only**:
   they committed their reports to their own branch and pushed. Zero merges to `main` overnight,
   zero rows born, zero rows closed, zero rows edited. A one-merge queue cannot strand itself
   between an unanchored spine entry and a JOURNAL that can only be written after the merges — the
   integrating arc's own JOURNAL entry names the single merge's contents directly.
2. **The exemption could not have applied to this batch even if this manifest had landed at
   dispatch.** `batch_manifest.LANE_BRANCH_RE` is `^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$`, and
   the branch these lanes were assigned is `claude/night-batch-cloud-lanes-a4mpkp` — a cloud-session
   lane prefix (CLAUDE.md §4, one of the four machine-produced prefixes), which that regex does not
   match. `is_lane_merge` therefore returns `False` for this arc's merge, and `exempt()` returns the
   empty set no matter what any manifest declares. **A `claude/*` branch is outside the exemption's
   reach by construction**, which is the reading the 2026-08-09 packet §1 already relied on when it
   held the conformance dailies out of scope.

So this file is an **archival declaration**, not a gate key. It buys the record; it does not buy —
and could not have bought — a single relaxed check. That distinction is recorded here so a later
reader does not infer from the manifest's existence that this arc integrated under an exemption. It
did not: every commit of the ARC-5 integration arc ran the full gate set, with **zero `SKIP=`, zero
`--no-verify`, and zero force-pushes**.

**Expiry is automatic and needs no edit.** `docs/audits/` is immutable (CLAUDE.md §5 rule 3), so
openness is deliberately not a mutable flag anyone flips: this batch is open exactly while
`docs/audits/2026-08-10-technical-batch-night-cloud-packet.md` is ABSENT from the committed tree,
and the packet's landing ends it with no edit anywhere.

## Two fields derived live, in the shape the predecessor manifest established

**1. The filename is `...-technical-batch-night-cloud-manifest.md`.** `MANIFEST_GLOB` is
`docs/audits/*-batch-*-manifest.md`, matched with `PurePosixPath.match`. Verified against the
parser before writing, all three spellings that were in play:

```
True   2026-08-10-technical-batch-night-cloud-manifest.md
True   2026-08-10-technical-batch-night-manifest.md
False  2026-08-10-technical-night-batch-manifest.md
```

The `night-batch` word order — the natural English one, and the one the branch name itself uses —
**fails the glob**: after the only `-batch-` there is no further `-manifest.md` left to consume. A
manifest the reader cannot enumerate declares nothing. The `-cloud-` token then distinguishes this
batch from the previous night's `2026-08-09-technical-batch-night-manifest.md`, which is a distinct
batch with its own committed packet. The name satisfies `validate_hermetization` Rule B: class token
`technical` from the closed ADR-101 11-class enum, slug `batch-night-cloud-manifest` lowercase-kebab.

**2. `batch: 0` — the sentinel, for the same reason the predecessor used it.**
`tests/test_batch_manifest.py::test_the_live_repos_own_manifest_is_well_formed` asserts
`b.batch.isdigit()` against every live open manifest. This batch genuinely has no number: it sits
outside the 1/2/3 execution sequence and the next execution batch is 4. The field is reporting-only
— `batch_manifest` reads it with `fm.get("batch", "?")` and gates openness on `status:` and
`closed_by:` alone — so the path, not the number, is the disambiguator.

## Class, and the standing rule the lanes ran under

**Class:** read-only research and verification. **No lane merges to `main` overnight; no lane files
or closes a BACKLOG row.** Every proposal in every report is a **candidate** for the batch-4
planning GO, ruled against demonstrated close capacity.

## Width — 3 lanes, ONE cloud session, ONE branch

Recorded as it actually ran, not as the width-3 file-disjoint table it would have been on the
operator's machine. **All three lanes ran in a single cloud session against a single designated
branch**, because a cloud session receives all three lane sections in one prompt and may push only
its assigned branch. The lanes are therefore file-disjoint by report path but **not** process-
isolated, and their gate posture is shared rather than per-lane.

| Lane | Subject | Report path |
|---|---|---|
| N-A | Satisfied-row census — which open rows recent work has already discharged | `docs/audits/2026-08-10-technical-satisfied-row-census.md` |
| N-B | Decision-sheet verification — every claim on the ruling surface, independently established | `docs/audits/2026-08-10-technical-decision-sheet-verification.md` |
| N-C | Origin branch census — every ref on `origin`, classified | `docs/audits/2026-08-10-technical-origin-branch-census.md` |

- **Branch:** `claude/night-batch-cloud-lanes-a4mpkp`, tip `fe81e896`, carrying all three reports in
  one commit.
- **Gate posture — hand-run, NOT gate-passed**, declared by the lanes themselves rather than
  discovered at integration: `uv 0.8.17` against the `==0.11.19` pin at `pyproject.toml:25` makes
  every `uv run --locked` hook entry refuse, and the clone's `.git/hooks/` held only samples. Hand-run
  and passing in the cloud clone: `validate_hermetization.py` (exit 0 against the real staged set) and
  `gen_audit_index.py --check` (exit 0 after regen). Not run there: `pytest`, `normalize_headers.py`,
  `audit.py health` (structurally unpassable in any cloud clone — its `operational_ok` leg counts
  resolvable sibling repos, always zero). **The integrating arc re-runs the full local gate set**;
  that re-run, not the cloud clone's partial one, is this batch's gate evidence.
- **Recurrence, not news:** this is the **fourth** appearance of the uv-pin class fleet-wide and the
  second consecutive night of it. It is already carried as intake #27 §A row 36 with a PROPOSED (not
  ruled) class change to `cloud-channel precondition`. This manifest records the recurrence; it rules
  nothing.

## Closure contract

The batch closes when **all** of the following hold, and committing
`docs/audits/2026-08-10-technical-batch-night-cloud-packet.md` is the single act that discharges the
last of them:

1. all three reports are merged to `main`;
2. the JOURNAL anchor `fe81e896` created and could not discharge is attached by the integrating arc;
3. the end-of-batch packet reports **opened / closed / net / open-total**, states the filter
   `open-total` was measured on (STANDING_RULINGS H2), and records the dispatched-vs-close width delta.

Each report's `## Needs a ruling` section carries the questions no operator was reachable to answer
overnight. **Adjudicating them is NOT a closure condition of this batch** — they are architect input
for the batch-4 planning GO, and this manifest does not manufacture an obligation the dispatch did
not carry.

## Births — ZERO

No BACKLOG row is born, closed, or edited by this batch or by the arc that archives it.

## Baseline at manifest commit

- `main` @ `e67fb8db`, pushed, working tree clean at branch time; integration branch
  `docs/arc5-night-batch-archive`.
- `python scripts/audit.py health` → **`health: OK`** before this file was written (two advisory
  `[~~]` rows standing: `preflight_backlog_ids`, `review_artifact_coverage`).
- `batch_manifest.open_batches(.)` → `[]` — the 2026-08-09 batch is closed by its committed packet,
  so this manifest inherits no stale exemption and opens the only live batch.
- JOURNAL entry `(a)` for 2026-08-10 already exists (ARC-4); this arc's is `(b)`.

## One standing consequence of an open batch, stated so it is not discovered mid-arc

`gen_handoff.assert_batch_boundary` **refuses to cut a handoff bundle while a batch is open**
(WINDOW = BATCH). Any bundle work in this arc therefore lands **after** the closing packet, which is
correct sequencing rather than an obstacle — and never a bypass.

## What this manifest deliberately does NOT do

- It does not claim an exemption, for the two independent reasons in the provenance section above.
- It does not adjudicate any lane's `## Needs a ruling` section — that is the architect's, at the
  batch-4 planning GO.
- It does not touch, reap, or propose the deletion of any branch, including the six
  `claude/conformance-*` dailies N-C found absent from `main`. Those are explicitly protected and
  out of this batch's scope.
