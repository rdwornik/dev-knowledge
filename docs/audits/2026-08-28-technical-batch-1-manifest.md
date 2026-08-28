---
batch: batch-1-2026-08-28
status: open
closed_by: docs/audits/2026-08-28-technical-batch1-end-of-batch-packet.md
---

# Batch-1 manifest — 2026-08-28 · SEQ 2 · ADR-110 shape

**This file is the gate-readable manifest.** `scripts/batch_manifest.py` resolves open
batches with `MANIFEST_GLOB = "docs/audits/*-batch-*-manifest.md"`, so the manifest has to
sit **directly under `docs/audits/`** and carry that name shape to be seen at all.

**The dispatch record — frozen contract, Q1-Q4 substrate cut, lane roster, merge order and
the dispatch-time measurements — lives at**
`docs/audits/2026-08-28-technical-batch1-launch-contracts/` (`MANIFEST.md` plus the
operator's frozen `BATCH1-LANE-CONTRACTS-2026-08-28.md`). That directory is the record; this
file is the key.

## What this manifest grants, stated precisely

While `status: open` and `closed_by:` names a path absent from the tree, `batch_manifest.exempt()`
covers the **declared-integration-arc** spine entries — and it covers **exactly** the merges
whose merged branch matches `validate_branch_naming.LANE_BRANCH_RE`, i.e.
`worktree-lane-<letter>-<id>-<slug>`.

**It does NOT cover a non-lane merge.** `is_lane_merge()` fails CLOSED on a non-merge, an
unparseable subject, a git failure or an off-grammar branch name. The dispatch arc
(`docs/batch-1-dispatch`) and the integration arc (`docs/batch-1-integration`) are ordinary
author-chosen `docs/` branches by ADR-110's own convention, so **they anchor in `JOURNAL.md`
like any other arc** — the exemption never reaches them.

That distinction was learned the hard way in this batch and is written here so the next seat
does not re-learn it: the dispatch merge was left unanchored on the assumption that an open
batch covered it. It did not, and `journal_spine_anchor` FAILed — which blocks **every**
commit in **every** lane through the `audit-health` pre-commit gate, not just the integrator's.

## Lanes

| lane | branch | rows |
|---|---|---|
| L1 | `worktree-lane-a-577-agents-md-lockstep` | [#577] + [#584] |
| L2 | `worktree-lane-b-608-journal-tiling-seam` | [#608] |
| L3 | `worktree-lane-c-491-fanout-acceptance` | none closed |
| L4 | `worktree-lane-d-459-architecture-slim` | none closed (executes ruling W2/D5) |
| L5 | `worktree-lane-e-613-routing-table` | [#613] |

Merge order: L2 → L1 → L4 → L5 → L3, `--no-ff`, one at a time.

The exemption expires by itself when `closed_by` lands, because `docs/audits/` is immutable
and a mutable `status:` flag would be no expiry at all.
