# Batch 6 (phase-2) — end-of-batch packet

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-16 · **Slug:** batch-6-packet
- **Closes:** `docs/audits/2026-08-16-technical-batch-6-manifest.md` (its declared `closed_by`).
  Committing this file expires the ADR-110 declared-integration-arc exemption automatically, with
  no edit anywhere.
- **Operator-facing record:** `~/Downloads/PHASE2-AUTORUN-PACKET.md` carries the full run narrative,
  per-stage evidence and the decision list. This file is the in-repo closer and records what binds
  the tree.

## Result

**12 of 12 lanes merged.** Dispatched width 11 (a b c d e f g h i x m) plus lane k, which was
dispatched outside this run and admitted by ruling.

```
51d7fa08 a   40dd51d8 b   b4862b9b c   65cd26a0 e (PARTIAL — tip HELD)
8e8d55a2 f   9997bc32 g   4ca67eed d   b150bfe4 h
fa746e14 i   e2403a44 x   94f9307b k   d714cfea m
121c3417 [#532] close restored (integrator repair)
b5054945 wrap acts (i)-(vii) + ledger
e32093fd D-A layout re-point of the three [#533] oracle pins
```

**Every merge passed the full gate stack. No `--no-verify` and no `SKIP=` at any point in the
batch**, including where `block-commit-on-main` refused a repair commit and `audit-health` blocked a
merge — both were fixed forward.

## Close-width delta (Ch8)

Dispatched 11, closed 12. The delta is `+1`: lane **k** was provisioned and dispatched outside this
run, blocked on an operator authorisation it correctly refused to self-grant, and was admitted to
the queue by ruling once its gate cleared.

## Rows

- **Born:** `[#531]` (lane-grammar enforcement at provisioning), `[#532]` (doc_rot two-arm split),
  `[#533]` (audit.py decomposition). Three, all ruled.
- **Closed:** `[#527]` (Position 0, with its honest limit verbatim) and `[#532]` (lane x).
- **Converted:** 29 Done-when clauses across lanes a–g. **Closes zero rows by design** — conversion
  buys verdictability, not closure.
- **Blocked:** `[#293]` → BLOCKED-ON-RULING after lane k's self-reverted seeding.
- **Open with a dated PARTIAL marker:** `[#533]`, 16 of 43 checks extracted — the contract's
  success condition, not a shortfall.
- Live rows: **196**.

## Suite

```
uv run --locked pytest -q --dist worksteal --max-worker-restart=0
2 owned REDs — the boot-state posture (ruled D-A)
```

Both are OWNED and unpinned-at by ruling:

- `test_routine_consumers_live_backlog_governs_exactly_one_row` — batch-7 lane **l**'s named
  subject; deferred by D-1v2, so nothing in this roster could clear it.
- `test_live_corpus_has_no_accretion_arm_findings_only_length_findings` — ARM 1 correctly fires on
  `BACKLOG#428` (3 dates spanning 52d). The detector is right; the pin is a live-corpus assertion
  that lane h's ruled edit changed.

**A third apparent RED was triaged and is environmental, not a defect:**
`test_finding_headline_resolves_with_provenance` fails at 16 xdist workers
(`assert 3 >= 50`) and **passes serially** — the pyright oracle returns partial results under
contention within its 40s timeout.

## Two integrator errors, both found, repaired, and recorded

1. **The merge resolver reverted lane x's `[#532]` close.** It treated `tasks/manifest.json` as
   generated and took `--ours`, discarding a node removal; regeneration re-emitted the row. `main`
   carried the row OPEN while its own merge commit said "closes [#532]". **No gate caught it** —
   `gen_task_tree --check` passed because node-present + `status: open` is internally COHERENT.
   **Coherence is not correctness.** Repaired at `3def2821`; the corrected resolver then REFUSED
   lanes k and m for the same class and both were resolved deliberately.
2. **The dispatch line doubled the `worktree-` prefix**, so 0 of 12 branches matched
   `LANE_BRANCH_RE` and the manifest's "zero refusals" claim was false. Found by lane x,
   corroborated by k and m. Repaired by uniform rename; **12 of 12 pass**; withdrawn in the
   manifest's AMENDMENT 2.

## Carried to batch 7

- **Lanes l and y** re-plan against the decomposed tree; contracts untouched.
- **`[#533]` leg 2** (parallel check execution) — measured this batch: `audit.py health` is
  **I/O-bound**, so `ThreadPoolExecutor` is indicated and the ruling's `ProcessPoolExecutor`
  condition is not met.
- **Class 2 (`_gitenv`) and class 3 (N-1 landing-predicate re-point)** are SEPARATE ruling items,
  deliberately not folded into lane m's seam leg.
- **Detector-gap candidate:** `gen_task_tree --check` needs a closed-in-history-vs-open-in-manifest
  leg — nothing compares the tree against its own history.
- **Lane contracts gain a PINNED-BY-TESTS section** listing which live-tree properties their work
  legitimately changes. Five witnesses this batch: *OWNED-FILES bounds writes, not test-pin
  dependencies.*
- **Owed:** the D3.1–D3.5 promotions, `ARCHITECTURE.md:427`, and the `[#415]`/`[#425]` Form-E
  repairs.

## Teardown

**Not run in this arc.** Twelve worktrees and twelve lane branches are intact, `git stash list`
empty. `git branch -d worktree-lane-e-82-conversions` will REFUSE by design — its held tip
`f5c5e9dd` is a lane-authored JOURNAL entry that was deliberately not merged — and that refusal is
reported, never forced with `-D`.
