---
batch: 3
seq: 4
shape: "ADR-110 - ONE architect-cut batch -> 4 local file-disjoint lanes + 2 cloud read-only + 1 local synthesis -> ONE integrator queue"
dispatched: 2026-08-29
status: open
substrate: "LOCAL (5) + CLOUD (2)"
---

# BATCH-D MANIFEST - 2026-08-29 - SEQ 4 - the gate-readable key

**This file is the gate-readable manifest**, and it is being written LATE, which is itself the
finding it exists to prevent. `scripts/batch_manifest.py` resolves open batches with
`MANIFEST_GLOB = "docs/audits/*-batch-*-manifest.md"`, reads every input from **HEAD**, and grants
the ADR-110 declared-integration-arc exemption only to `--no-ff` merges of branches matching
`validate_branch_naming.LANE_BRANCH_RE` while a committed manifest declares an open batch.

**Why it is late, recorded rather than quietly backfilled.** Batch D was frozen, dispatched, and
had two lanes merged before this key existed. The consequence was immediate and I misdiagnosed it
three separate times: every batch-D lane merge flagged `journal_spine_anchor`, and each time I
treated it as an anchoring mistake to repair rather than as the ABSENCE OF THE EXEMPTION that
should have covered it. `lane-g` named the real cause from inside the batch. The trap is already
recorded in this repo's own memory - *"a batch without a committed manifest is unintegrable -
check before merge #1"* - and the check was not run before merge #1.

## The lanes

| Lane | Branch | Substrate | Status |
|---|---|---|---|
| a | `worktree-lane-a-619-fm-coupling-repair` | local | MERGED `28bb3002` |
| b | `worktree-lane-b-614-vision-to-readme` | local | MERGED `023a7797` |
| c | `worktree-lane-c-000-claude-md-regenre` | local | HELD - blocked by lane b on `CLAUDE.md` |
| d | `worktree-lane-d-000-codex-fate` | local | MERGED `c2c59281` as a REFUSAL - premise refuted (Z-G5). SUPERSEDED by lane h |
| h | `worktree-lane-h-000-codex-universalise` | local | the re-cut: universalise only, widened scope, operator-ruled |
| e | `claude/lane-e-000-essentials-census` | cloud | HARVESTED |
| f | `claude/lane-f-000-adr81-fuzzy-band` | cloud | HARVESTED; ADR-116 sits on its branch |
| g | `worktree-lane-g-000-autonomy-synthesis` | local | MERGED `f7b8fbdd` |

**The dispatch record** - the seven frozen contracts, the substrate cut, the merge order and the
freeze-time measurements - lives at `docs/audits/2026-08-29-technical-batchd-launch-contracts/`.
That directory is the record; this file is the key.

**What this manifest does NOT cover.** The integrator branches (`docs/batchd-*`, `docs/postnight-*`)
are ordinary author-chosen `docs/` branches, outside `LANE_BRANCH_RE`, so they anchor in
`JOURNAL.md` like any other arc. The exemption is for lane merges only, and widening it would be a
design act with a governance cost rather than a convenience.
