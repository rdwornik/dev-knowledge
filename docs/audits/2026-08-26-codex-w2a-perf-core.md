# Codex Review — w2a-perf-core

**Date:** 2026-08-26
**Branch:** `worktree-w2a-perf-core`
**HEAD:** `96804ab6`
**Diff range:** `852e145c..HEAD`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 1/0/0/0 <!-- Critical/High/Medium/Low. Counted from the Findings section below, not from the console tail. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/journal_anchor.py is the ADR-85 anchoring predicate shared by the pre-push HARD leg (block_unanchored_push) and the audit backstop (check_journal_spine_anchor). A wrong ANCHORED verdict lets an unanchored push through; a wrong UNANCHORED verdict blocks every commit in the repo. Both directions matter, the false-clean one more.
- [#587]: _anchor_index builds a map from 7-char lowercase-hex short to (present, recorded) in ONE pass. Is short in index.present really equivalent to the short in journal substring test it replaces, for every input? Check the hex-run window enumeration, the non-hex fallback, and the line-class (present/recorded) split against the pre-inversion body.
- [#588]: _introduced_from_map derives irstparent..sha from one git rev-list --parents --timestamp --all. Is the exclusion walk plus the date-priority-queue walk exactly git rev-list A..B in BOTH set and ORDER? Order is output: mention_not_record_warnings emits one string per introduced commit in this order and the audit joins the first five into its evidence.
- Cache safety: three lru_caches now (_entries, _anchor_index_tuple, _parent_map) plus _introduced_tuple and an unbounded _MAP_GENERATION dict. Can any of them serve a STALE answer in a long-lived process (the audit runner holds one process across 46 checks; a test commits mid-process)? Is rebuild-on-miss sound, and can it loop or thrash?
- Fail-closed posture: AnchorError must never be swallowed into a pass. Check that the new eturn None deferral paths do not convert an error into a clean answer, and that exceptions are still uncached.

---

## Findings
## CRITICAL

### scripts/journal_anchor.py:265 — Parent-map cache can return a stale Git graph

**What:** `_spine_map_for` rebuilds only when the requested SHA is absent, but Git’s resolved parent graph for an existing SHA can change through shallow-history deepening or replace/graft refs.  
**Why:** An old map can then derive an obsolete, potentially too-large introduced set and return `ANCHORED` when current `git rev-list firstparent..sha` would not—allowing an unanchored push through.  
**Fix direction:** Invalidate or refuse reuse of the parent map when mutable graph metadata can change; ensure a map is only trusted while the Git graph view it represents is unchanged.

## HIGH

(none)

## MEDIUM

(none)

## LOW

(none)

---

## Lane disposition (added by the lane, 2026-08-26 — not part of the reviewer's output)

**CRITICAL / `journal_anchor.py:265` — parent-map cache can return a stale Git graph:
MECHANISM CONFIRMED, CONSEQUENCE REFUTED. Not code-fixed; documented, tested and bounded.**

The mechanism is real and was accepted: `_spine_map_for` rebuilds only on a MISS, so a SHA
already in the snapshot is answered from it for the life of the process, and git reports a
*view* of the object graph that a shallow deepen or a `replace`/graft ref can move.

The stated consequence — *"an obsolete, potentially too-large introduced set … return ANCHORED
… allowing an unanchored push through"* — was **measured and is the wrong direction**:

- **Static shallow clone: ZERO divergence.** `git rev-list firstparent..sha` is truncated at
  the same boundary the map is, so the batch introduces nothing git does not already do.
  Pinned by `test_a_shallow_clone_does_not_make_the_map_disagree_with_git`.
- **Deepen mid-process: the stale snapshot UNDER-reports.** On the fixture the stale set was
  missing 2 commits and had 0 extra — a strict SUBSET. `is_anchored` is `any(...)` over that
  set, so a subset can only turn TRUE into FALSE: the entry is reported UNANCHORED and the gate
  REFUSES. That is fail-CLOSED, which is the posture this module exists to hold. Pinned by
  `test_a_view_that_moves_under_the_snapshot_fails_CLOSED`, which asserts the strict-subset
  relation AND the predicate consequence.

**Why it is not closed in code:** detecting a view mutation requires a git read PER CALL, which
is precisely the per-SHA spawn [#588] exists to remove — the fix would undo the row. The
residual is a `replace`/graft ref created inside the seconds-long lifetime of a gate process,
and that window is **not new**: `_introduced_tuple`'s `lru_cache` has fixed answers for a whole
process since [#533]. Recorded at `journal_anchor.py::_spine_map_for` as a named honest limit
with the measurement attached, rather than left for a later reader to rediscover.

Nothing else at Critical/High/Medium, so no ≥medium fix was owed. Full context:
`docs/audits/2026-08-26-technical-w2a-perf-core.md` §11.