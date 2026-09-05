# LANE lane-r-000-zc-candidates — file two integrator-carried candidates in the Z-C shape

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

**Batch R5P, lane 3 of 3. DOCS-ONLY.** No BACKLOG row — `000` is the no-row id, and
**filing a row is the one thing this lane must not do.**

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-r-000-zc-candidates LANE-r-000-zc-candidates.md -Effort high
```

**Model is the repo default `opus`, and that is forced rather than chosen:** the contract
validator's dispatch-line regex admits `-Effort` but NOT `-Model`, so a line carrying an

explicit model FAILS `gen_lane_contract.py check`. The table above therefore states the
default the launch will actually use, so contract and launch cannot disagree.
## Worktree pairing

slug `lane-r-000-zc-candidates` -> branch `worktree-lane-r-000-zc-candidates` -> contract `LANE-r-000-zc-candidates.md`

## Intent

File the two candidates the integrator was carrying as **Z-C-shaped CANDIDATEs — NOT rows**:

- **(a) `SessionStart` refuses a non-integrator session on the primary.** Filed from a
  WITNESSED failure: a commit landed on `main` while `block-commit-on-main` reported Passed.
  The gate is **not** defective — it was probed live and refuses correctly. The race is
  TOCTOU: pre-commit ran the mesh with HEAD on a feature branch, a concurrent session
  checked out `main` during the hook run, and git re-resolved HEAD at ref-write time. A
  client-side pre-commit hook cannot hold an atomic claim on HEAD, so no hardening inside
  that hook closes it. **State the honest limit in the entry:** a SessionStart refusal
  NARROWS the window, it does not prove it shut.
- **(b) `window_metrics` gains the ten-line SCORECARD.** Library-first is the binding
  constraint, not a preference: every row is computable from surfaces the repo already
  maintains, so a new store would be a second source of truth for numbers that already have
  one. Carry the evidence: the ship-gate headline read 133/134/136/137 across one window,
  twice at a byte-identical tree, because roughly half its WARN lines are calendar-driven
  `doc_rot`. **The trend column is the feature.**

## Where these land — read this before writing a line

`protocols/STANDING_RULINGS.md` section **Z-C closed at three**. Later Z-C-shaped candidates
**append as their own new section** — that is the live precedent, not a workaround: see
**AB** (`/handoff-verify` FORM probe, "Z-C-shaped") and **AD** (Batch G filings, "the
CANDIDATE register (Z-C shape)"). The last section is **AD**, so these land as a **new
section AE**. **Do NOT edit section Z-C itself.** Read the file's own "Editing note (read
before adding an entry)" first and conform to it.

ADR-111 admits exactly one path — **CANDIDATE, then ADR-98 intake, then ratification** — so
nothing filed here draws from the ledger and nothing here is a commitment.

## Two premises the dispatcher resolved — inherit these, do not re-litigate

1. **"reconciled against intakes #68/#69" DOES NOT RESOLVE.** Intake numbering is the
   ordinal position in `docs/intake/` sorted by name, **plus 10** (verified: position 50 =
   intake #60, position 53 = intake #63). The corpus has 57 numbered docs, so it **tops out
   at #67**. #68 and #69 do not exist. **Do not create them and do not guess which docs were
   meant.** Discharge the reconciliation term the honest way: verify neither candidate
   duplicates an existing intake doc, and **report in the packet that #68/#69 are
   unlocatable, with the numbering rule above as the evidence.**
2. **A COLLIDING BRANCH ALREADY EXISTS.** `worktree-file-candidates` @ `26d7d743`
   ("chore(tasks): file [#635] and [#636] — the two integrator-ruling candidates, filed not
   built") is **unmerged** and files these SAME two items as **BACKLOG rows** in `tasks/` +
   `tasks/manifest.json` + `BACKLOG.md`. This contract says **CANDIDATEs, no rows** — the
   opposite disposition. **You are not to reconcile, revert, or touch that branch.** Your
   footprint is `STANDING_RULINGS.md` only, which is file-disjoint from it, so both can
   exist without conflicting. **Record the collision prominently in your hand-back packet**
   so the integrator rules on which disposition survives. That ruling is not yours.

## Done-contract (immutable)

1. A new section **AE** in `protocols/STANDING_RULINGS.md` records both candidates in the
   Z-C shape — explicitly CANDIDATEs, explicitly not rows, drawing nothing from the ledger.
2. Each entry carries its **evidence** and its **honest limit** (as above).
3. The packet reports: the #68/#69 unlocatable finding, and the `worktree-file-candidates`
   collision.
4. Any gate that fires on the edit is satisfied, not bypassed.

## Decision budget

**V-2 — escalates on three classes only:** (a) curated-baseline touches, (b) genuine
rule-vs-ruling conflicts, (c) fork classes with no standing ruling. Everything else is
decided per this contract and **reported in the end packet**, never asked.

## Steps

1. Read `protocols/STANDING_RULINGS.md` sections Z-C, AB, AD and the Editing note. **COMMIT**
   nothing; this is reading.
2. Write section AE with both candidates. **COMMIT**
3. Final: one end-of-lane artifact (what landed, the two reported findings above, open
   items), **COMMIT, then STOP.**

## What NOT to do

- **NO BACKLOG ROWS.** No `tasks/` file, no `tasks/manifest.json` edit, no `BACKLOG.md`
  regeneration. If a habit reaches for `gen_task_tree.py`, that is this lane failing.
- **No edit to section Z-C**, and no renumbering of existing sections.
- No touching `worktree-file-candidates`, its branch, or its rows.
- No merges, no pushes to `main` — commit-and-STOP.
- No JOURNAL entry — the integrator owns the anchor. Name your SHAs in the hand-back packet.
- No edits outside `protocols/STANDING_RULINGS.md`.
