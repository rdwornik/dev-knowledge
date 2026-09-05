---
batch: R5P
seq: 1
shape: ADR-110 — ONE plan -> N file-disjoint lanes -> ONE integrator. Dispatched as FOUR by the operator; THREE booted. Lane L2 was REFUSED at the dispatch gate as a duplicate of work already committed on an unmerged branch, with evidence, rather than re-built.
dispatched: 2026-09-05
status: open
closed_by: docs/audits/2026-09-05-technical-batch-r5p-close-packet.md
substrate: LOCAL (3) — all three lanes are gate-dependent, so Q1 refuses cloud
---

# BATCH R5P — DOC-ROT ARM 2, THE BUNDLE GIT-LOG HOTFIX AND THE Z-C CANDIDATES · THE MANIFEST

**This file is the gate-readable manifest**, committed AT DISPATCH and before any lane booted
— the ADR-110 §3 item this batch is being deliberate about. `scripts/batch_manifest.py`
resolves an open batch as the conjunction of four facts: the manifest is TRACKED,
`status: open`, `closed_by:` names a shape that CAN resolve, and that path is ABSENT from the
tree. All four hold at the time of writing.

## THE LANES — 3 committing

Contracts: `docs/audits/2026-09-05-technical-batch-r5p-launch-contracts/`.

```
L1  lane-r-000-docrot-arm2     local  opus  no row  ARM 2 emits ONE corpus Finding
L3  lane-r-000-bundle-gitlog   local  opus  no row  ONE git log for all handoff bundles (P1)
L4  lane-r-000-zc-candidates   local  opus  no row  two CANDIDATEs in the Z-C shape (docs)
```

**Every branch is `worktree-<slug>` and matches `LANE_BRANCH_RE`.** The operator's shorthand
names (`lane-r5p-docrot-arm2`, `lane-p1-git-log-batch`, `lane-r5p-candidates`,
`lane-r5p-docclaims-tier`) are all REFUSED by `validate_branch_naming.py` — the grammar is
`lane-<letter>-<id>-<slug>` with a ONE-letter `<letter>` and a NUMERIC `<id>`, so `r5p` and
`p1` cannot stand. Same class as batch G's two deviations; the gate is the authority over the
prompt's shorthand. `000` is the no-row id: none of the three lanes discharges a BACKLOG row,
and none files one.

## L2 WAS REFUSED AT THE DISPATCH GATE — the evidence, not the intention

The operator dispatched a fourth lane, `lane-r5p-docclaims-tier`: *"pytest_collected derived
at the commit gate, not only at TIER_SHIP."* **It was not booted, because that work is already
committed.**

`worktree-doc-claims-tiering` @ `e2995e86` — *"feat(gates): derive the collected-test-count
claim at the COMMIT gate"* — is UNMERGED, its worktree is CLEAN, `git stash list` is empty, and
no live session holds it. It is a finished commit-and-STOP lane sitting in the integrator queue.
Booting L2 would have produced a second, conflicting implementation of one gate: the exact
duplicate-dispatch class `scripts/single_flight.py` exists to refuse (exit 3: *"STOP. Do not
provision."*).

**It solves the intent by a DIFFERENT MECHANISM than the contract named, and the difference is
measured rather than incidental** — this is the part the integrator must rule on:

- The contract named `validate_doc_claims.py` + the `audit.py` tiering table. The landed commit
  touches neither. It adds a `files:`-filtered **pre-commit hook** instead.
- The recorded reason: the claim's ground truth is a `pytest --collect-only` subprocess timed at
  **29 seconds**, which fails the ALL_CHECKS cost rule for a commit-tier check. A `files:` filter
  pays it only on commits that can move the count.
- The commit states its own honest limit: a future test parametrizing over a source registry
  would move the count with no in-scope file changing, and the hook would stay silent.

**What is genuinely NOT discharged:** the contract's second closure item, *"`audit.py health`
wall-clock delta printed"*. The hook route means that delta is ~0 by construction, which is an
answer, but it is not a measurement. **Open item for the integrator**, filed here rather than
papered over.

## L4 CARRIES A COLLISION AND AN UNLOCATABLE PREMISE — both frozen into its contract

**The collision.** `worktree-file-candidates` @ `26d7d743` already files the SAME two items as
**BACKLOG rows** `[#635]`/`[#636]` (`tasks/` + `tasks/manifest.json` + `BACKLOG.md`), unmerged.
The operator's L4 says **CANDIDATEs, no rows** — the opposite disposition, and the one ADR-111
§1 actually admits (CANDIDATE -> ADR-98 intake -> ratification). L4 was booted with its
footprint narrowed to `protocols/STANDING_RULINGS.md` ONLY, which is file-disjoint from that
branch, so both can exist without a merge conflict. **The lane is forbidden to touch, revert or
reconcile that branch.** Which disposition survives is the integrator's ruling, not a lane's.

**The unlocatable premise.** The contract says *"reconciled against intakes #68/#69."* **Those
do not exist.** Intake numbering is the ordinal position in `docs/intake/` sorted by name, plus
10 — verified twice against live citations (position 50 = intake #60; position 53 = intake #63).
The corpus holds 57 numbered docs, so it tops out at **#67**. The lane is instructed to report
this rather than guess which docs were meant, and explicitly NOT to create them.

## A CONTRACT CANNOT STATE ITS OWN MODEL — recorded here because it bit this dispatch

All three contracts were authored at `sonnet` and had to be re-stated to `opus`.
`gen_lane_contract.py`'s `_DISPATCH_LINE_RE` is
`^Dispatch-Lane\s+(?P<slug>\S+)\s+(?P<file>\S+)(?:\s+-Effort\s+(?P<effort>\S+))?\s*$` — it
admits `-Effort` and **not** `-Model`, so a dispatch line carrying an explicit model FAILS the
contract check, while `Start-DispatchLane` defaults `-Model` to `opus`. A contract may therefore
state a model in its routing table that its own launch line structurally cannot carry. That is
the same silent-`--model`-drop class PLAYBOOK Ch8 records for the raw form, surviving inside the
checked surface that replaced it. The three contracts state `opus` so that table and launch
agree; **the gap itself is a CANDIDATE for the close packet**, not a row filed here.

## THE INTEGRATOR'S QUEUE

Serial, from the primary checkout, INTERACTIVE — no background seat merges. Beyond this
batch's three lanes, `worktree-doc-claims-tiering` and `worktree-file-candidates` are already
in the queue and are named above. `main` moved from `09f80530` to `ac2c6a15` during dispatch
(a concurrent seat merged `worktree-hotfix-manifest-citation`), so the queue is re-read at
integration rather than trusted from here.
