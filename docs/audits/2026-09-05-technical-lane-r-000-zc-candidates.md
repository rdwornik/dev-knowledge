# Lane packet — `lane-r-000-zc-candidates` (batch R5P, lane 3 of 3, DOCS-ONLY)

**Consumers:** `protocols/STANDING_RULINGS.md` section **AE** — the section this lane wrote, and
the durable home of both findings below. Also consumed by the batch R5P integrator seat, which
owes the ruling recorded under "Open items".

**Lane:** `lane-r-000-zc-candidates` · branch `worktree-lane-r-000-zc-candidates` · contract
`LANE-r-000-zc-candidates.md` · model `opus`, mode `execute`, effort `high` · budget **V-2**.
**No BACKLOG row** — `000` is the no-row id, and filing a row was the one act barred.

## What landed

One commit, one file, 83 insertions and zero deletions.

```
811399a6  docs(rulings): section AE files two integrator-carried candidates in the Z-C shape
          protocols/STANDING_RULINGS.md | 83 +++++++++++++++
```

New section **AE** in `protocols/STANDING_RULINGS.md`, appended after AD and before the
*Editing note*. Both items are recorded in the **Z-C shape** — explicitly CANDIDATEs, explicitly
not rows, with no peg, no owner and no size band, drawing nothing from the ledger. ADR-111 admits
one path only: CANDIDATE → intake (ADR-98) → ratification.

- **AE-1 · `SessionStart` refuses a non-integrator session on the primary checkout.** Carries its
  evidence (a commit landed on `main` while `block-commit-on-main` reported *Passed*; the gate was
  probed live and refuses correctly, so it is not defective — the race is TOCTOU on HEAD identity)
  and its honest limit (a client-side pre-commit hook cannot hold an atomic claim on HEAD for the
  duration of its own run, so a `SessionStart` refusal **narrows** the window and does not prove it
  shut).
- **AE-2 · `window_metrics` gains the ten-line SCORECARD.** Carries its evidence (the ship-gate
  headline read **133 / 134 / 136 / 137** across one window, two of those readings at a
  byte-identical tree, because roughly half its WARN lines are calendar-driven `doc_rot`; the trend
  column is the feature) and its honest limit (library-first binds — every row is computable from
  surfaces the repo already maintains, so a SCORECARD row that cannot be computed prints its reason
  the way `[#461]`'s two existing `NOT COMPUTED` rows do, rather than acquiring a store).

**Section Z-C was not edited and no section was renumbered.** Section AE is a new section, which is
the live precedent — AB and AD are both Z-C-shaped candidate registers appended after Z-C closed at
three. The file's own *Editing note* was read first; its declarative-phrasing constraint is
retired post-R12 (this register is in `silent_rule_detector.EXCLUDED_RELPATHS`), and no `landed:`
predicate block was declared, because a candidate has nothing landed to predicate on.

## The two findings the contract required this packet to report

### 1. "reconciled against intakes #68/#69" is UNLOCATABLE — a finding, not a gap to fill

Intake numbering is the ordinal position in `docs/intake/` sorted by name, **plus 10** (rule as
verified at dispatch: position 50 = intake #60, position 53 = intake #63). The corpus holds **57
numbered docs** — re-counted in this lane: 58 `*.md` in `docs/intake/` minus `README.md`, with
`archive/` and `manifest.json` outside the count — so numbering **tops out at #67**. Intakes #68
and #69 do not exist.

**Nothing was created and nothing was guessed.** The reconciliation term is discharged the honest
way instead — neither candidate duplicates an existing intake doc, and the nearest neighbour is
named inside each AE entry:

| Candidate | Nearest existing intake | Why it is not a duplicate |
|---|---|---|
| AE-1 | `2026-08-17-tech-repository-autonomy-and-gate-liveness.md` | Reaches `block-commit-on-main`, but on `current_branch()` returning `None` on any non-zero git exit — a fail-open question INSIDE the hook. AE-1 is a HEAD-identity race OUTSIDE it. |
| AE-2 | `2026-07-30-func-operator-decision-routing-and-standards.md` | Records that `window_metrics.py`'s refusal to supply a window boundary is correct and stands. That is a **constraint AE-2 must respect**, cited as such in the entry — not the same object. |
| AE-2 | `2026-08-17-tech-fleet-config-standardization.md` §6.4 | R18, a per-repo × per-rule **fleet conformance** scorecard, recorded NOT-BORN with un-parking conditions. Fleet-grained and consumer-facing; AE-2 is window-grained and hub-local. Named in AE so the two are not merged by name collision. |

### 2. A colliding branch files these same two items in the OPPOSITE disposition

`worktree-file-candidates` @ `26d7d743` — *"chore(tasks): file [#635] and [#636] — the two
integrator-ruling candidates, filed not built"* — is **unmerged** (`git branch --merged main` does
not list it) and files them as BACKLOG **rows**:

```
BACKLOG.md
tasks/635-sessionstart-refuses-a-non-integrator-session-on-the-primary.md
tasks/636-window-metrics-gains-a-ten-line-scorecard.md
tasks/manifest.json
```

This lane filed them as **CANDIDATEs, no rows**. The two file sets are **disjoint** — that branch
touches no `protocols/` file and this lane touched nothing else — so both can exist in the tree
without conflicting. **The dispositions are not compatible**, and one has to give way: ADR-111
admits exactly one path from CANDIDATE to row, and rows filed directly bypass it.

**That ruling is the integrator's and was not made here.** Nothing on that branch, its rows or its
history was touched, reconciled or reverted by this lane.

## Gates — satisfied, not bypassed

No `SKIP=`, no `--no-verify`, on either commit attempt.

The first commit attempt was refused by `audit-health` with one `[!!]`:
`journal_spine_anchor` naming two first-parent spine merges above the disposition floor —
`c710ece0` and `54c2b8c2`, both 2026-09-05, **neither of them this lane's**. Diagnosed with the
`journal_anchor.unanchored_on_spine` split rather than assumed:

```
before ff   MY TREE : ['c710ece0...', '54c2b8c2...']     MAIN : []
after  ff   MY TREE : []                                  MAIN : []
```

Empty against `main`'s own `JOURNAL.md` and non-empty against the lane tree is **lane tree-lag**,
not a real gap — the check walks `main`'s spine from the shared refs but reads `JOURNAL.md` from
the local working tree. The lane held **zero** commits at that point and none of the four files
differing from `main` was dirty here, so the remedy was `git merge --ff-only main`
(`ac2c6a15 → c710ece0`), which creates **no merge commit**. Re-diagnosed after the
fast-forward — empty in both trees — and only then re-committed. Second attempt: every hook
Passed, `audit-health` included.

`consumer_at_landing` is pre-empted for this artifact by the `Consumers:` line above.

## Open items

1. **The disposition ruling — CANDIDATE (this lane) versus ROW (`worktree-file-candidates`).**
   Owner: the batch R5P integrator. Not this lane's call, and deliberately left open.
2. **`docs/audits/README.md` is now stale** and this lane left it that way on purpose. `[#590]`
   narrowed `audit-index-freshness` on 2026-08-26 so a lane landing an artifact no longer touches
   the index — regenerating it in a lane is affirmatively the wrong act, because that one file was
   in 6 of the last 7 conflicted merges. The integrator regenerates once on the merged result with
   `gen_audit_index.py --write`, `git add` first. **Recorded so the owed regen is not invisible.**
3. **Nothing else is owed by this lane.** No JOURNAL entry was written — the integrator owns the
   anchor; the SHAs are named in "What landed" above. No push, no merge: commit-and-STOP.

## Footprint

```
protocols/STANDING_RULINGS.md                             (section AE, +83 / -0)
docs/audits/2026-09-05-technical-lane-r-000-zc-candidates.md   (this packet)
```

No `tasks/` file, no `tasks/manifest.json` edit, no `BACKLOG.md` regeneration, no
`gen_task_tree.py` run, no edit to section Z-C, no renumbering, no touch of
`worktree-file-candidates`.

---

## ERRATUM 1 — two findings were overtaken by events before this packet landed (2026-09-05)

*Appended by the integrator at merge time under architect ruling 2026-09-05 evening. Audits are
immutable, so this rides as an appended marker and edits nothing above. It corrects two
findings; every other finding in this packet stands.*

**§1 — "Intakes #68 and #69 do not exist."** WITHDRAWN. They were **not on `main` at the time
of writing**; they are listed in `docs/intake/README.md` as part of #65–#70. Section AD of
`protocols/STANDING_RULINGS.md` states that intake #68 "does exist", so the packet as written
contradicted the register it was filed alongside. The derivation that produced the claim — a
57-doc count yielding a #67 ceiling — is left standing above as the reasoning of record; only
its conclusion is withdrawn. No guess was made about which docs were meant, and that part of
the finding is unaffected.

**§2 — the colliding branch, and the ruling said to be owed.** WITHDRAWN as stated. The packet
recorded `worktree-file-candidates` as **unmerged**, the two dispositions as incompatible with
"one has to give way", and the ruling as the integrator's and "not made here". By the time this
packet merged, all three were false:

- the branch **merged at `8ea8023a`**;
- the rows `[#635]` / `[#636]` were **dropped at `e3d2ac34`** on recorded operator consent,
  because they had been filed bypassing the ADR-111 funnel;
- **the CANDIDATE shape stood.** The disposition this lane chose is the one that survived, and
  the ruling the packet said was owed has been made.

**Why this is an erratum and not a defect in the lane.** Both findings were TRUE when written
and were falsified by concurrent work between the lane's freeze and its merge — the same
overtaken-premise class the lane itself was held for. A packet is a dated record; the honest
repair is to date the correction rather than to rewrite the record.
