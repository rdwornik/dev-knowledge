# LANE lane-r-000-docrot-arm2 — doc_rot ARM 2 reports the CORPUS, not one WARN per row

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

**Batch R5P, lane 1 of 3.** Operator-declared (R5 B5). No BACKLOG row — `000` is the
no-row id, and this lane files none. `[#532]` is CLOSED and is the arc that BUILT the two
arms; this lane reshapes ARM 2's OUTPUT only.

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-r-000-docrot-arm2 LANE-r-000-docrot-arm2.md -Effort high
```

**Model is the repo default `opus`, and that is forced rather than chosen:** the contract
validator's dispatch-line regex admits `-Effort` but NOT `-Model`, so a line carrying an
explicit model FAILS `gen_lane_contract.py check`. The table above therefore states the
default the launch will actually use, so contract and launch cannot disagree.

## Worktree pairing

slug `lane-r-000-docrot-arm2` -> branch `worktree-lane-r-000-docrot-arm2` -> contract `LANE-r-000-docrot-arm2.md`

## Intent

`doc_rot` ARM 2 (`backlog-row-length`, `scripts/validate_doc_rot.py`) currently emits ONE
WARN PER ROW over the declared ceiling. Make it emit **ONE corpus-level Finding** instead:
the COUNT over ceiling, the p50/p75/p90 of row length, and a trend term versus the previous
run. **1320 stays the reference line** (`_BACKLOG_ROW_CEILING`) — it is reported against,
not changed.

## Done-contract (immutable)

1. ARM 2 emits exactly **ONE** Finding for the whole corpus, carrying: count over ceiling,
   p50/p75/p90 of row length, and a trend term. **MEASURE the before-count and state it** —
   do not restate a number from this contract or from a module comment; both are stale by
   construction (CLAUDE.md §4, "never restate a count").
2. **Every other doc_rot arm is byte-identical in output.** ARM 1 (`backlog-accretion`) and
   the non-BACKLOG detectors are untouched. Prove it, do not assert it.
3. A **seeded test** with a 3-row fixture over the ceiling yields **1 Finding naming 3**.
4. `pytest` green on the targeted tests for this diff.

## Frozen defaults — decided here so the lane does not spend a round-trip

- **The trend term.** Emit a trend versus the previous run **only if an existing surface
  already records a prior value**. If none does, emit the term as `n/a (no prior run
  recorded)` and say so in the packet. **Do NOT create a new store** — a new store is a
  second source of truth for a number, and that is the class this repo refuses. This is a
  frozen default, not an escalation.
- **Finding severity stays whatever ARM 2 emits today.** Collapsing N WARNs into 1 Finding
  is a reporting change; it is not a promotion to FAIL.
- **A row over the ceiling is still LONG, not ROT** — the module's own words. The Finding
  text keeps that posture.

## Decision budget

**V-2 — escalates on three classes only:** (a) curated-baseline touches, (b) genuine
rule-vs-ruling conflicts, (c) fork classes with no standing ruling. Everything else is
decided per the frozen defaults above and **reported in the end packet**, never asked.
A lane that discovers a refuted premise PAUSEs with the fact.

## Steps

1. Run ARM 2 as it stands and **record the live per-row WARN count** — the before number.
   **COMMIT** nothing yet; this is measurement.
2. RED first: write the 3-row-over-ceiling fixture test asserting ONE Finding naming 3, and
   the test that pins the other arms' output unchanged. Watch them fail. **COMMIT**
3. Reshape ARM 2's emission to the corpus-level Finding. Targeted tests green. **COMMIT**
4. Final: one end-of-lane artifact (before/after counts, what changed, open items),
   **COMMIT, then STOP.**

## What NOT to do

- **No ceiling change.** `_BACKLOG_ROW_CEILING` stays 1320.
- **No ARM 1 change.** Not its predicate, not its output, not its fixture.
- No new persistence store for the trend term (see frozen defaults).
- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP.
- No JOURNAL entry — the integrator owns the anchor. Name your SHAs in the hand-back packet.
- No BACKLOG row, no index regeneration, no edits outside
  `scripts/validate_doc_rot.py` and its tests.
