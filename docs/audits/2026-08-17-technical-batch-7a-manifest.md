---
batch: 7
status: open
closed_by: docs/audits/2026-08-17-technical-batch-7a-packet.md
---

# Batch 7a — manifest, committed AT DISPATCH

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-17 · **Slug:** batch-7a-manifest
- **Protocol:** ADR-110 + its 2026-08-07 amendment (the declared integration arc) + PLAYBOOK Ch8
  "The batch protocol". Width **3** dispatched (lanes a b c), one wave.
- **Authority:** `SESSION-CLOSE-BATCH-7A.md` (operator's prompts dir, off-repo), whose §A this file
  discharges, and the **architect standing ruling of 2026-08-17** quoted below. The operator
  authorised one orchestrator to run §A–§D end-to-end without further round-trips, so the head,
  the dispatch, the integration and the supplement are all one seat this batch.
- **Predecessor:** batch 6 (phase 2) — manifest
  `docs/audits/2026-08-16-technical-batch-6-manifest.md`, packet
  `docs/audits/2026-08-16-technical-batch-6-packet.md` (both committed, so that batch is CLOSED).
  Verified live immediately before writing this file: `batch_manifest.open_batches('.')` → `[]`.
  **This manifest inherits no stale exemption and opens the only live batch.**

## The architect standing ruling this batch executes

> *Audit-to-row conversion authority, 2026-08-17.* Every audit artifact carries exactly one
> disposition: **ACTIONED** (conclusion already live — cite the commit), **FILED** (a row owns it —
> cite the id), **REJECTED** (a ruling declined it — cite it), **SUPERSEDED** (a later artifact
> replaced it — cite it). An undisposed audit is a defect, not a document. Births under this ruling
> are pre-authorised: one row per commit, flush-left `kill-candidates:`, a `source:` line citing the
> audit, and no row for a conclusion already ACTIONED.

Lanes **a** and **b** quote it in every commit body; lane **c** births nothing and does not.

## `batch: 7` — a digit, deliberately, while the batch is called 7a

`tests/test_batch_manifest.py::test_the_live_repos_own_manifest_is_well_formed` asserts
`b.batch.isdigit()` against **every live open manifest**. `batch: 7a` would therefore be RED from
the moment it landed — the exact failure batch 3 shipped with a date-shaped value. The frontmatter
field carries the digit `7`; the filename, title and `closed_by:` carry `7a`, which is what the
operator's prompt names it. Stated here rather than left to be discovered, because a reader who
greps `7a` in the frontmatter and finds `7` should find the reason in the same file.

This is not a licence to renumber: a genuine batch 7 later today or tomorrow gets its own manifest
and its own `closed_by:`, and openness is decided per-manifest by whether its closer is absent from
the committed tree — not by the `batch:` value, which the exemption logic never compares.

## Lane roster — width 3, one wave

All three lanes cut from the same `main` tip, which is the merge that lands this manifest:
**zero inter-lane git dependencies by construction.**

| Lane | Worktree (bare name passed to `--worktree`) | Branch git creates | Ids reserved | Bucket | Contract of record | Model / effort |
|---|---|---|---|---|---|---|
| **a** | `lane-a-534-audit-dispositions` | `worktree-lane-a-534-audit-dispositions` | **534–545** | finish-line | `CONTRACT-CLOSE-A-audits.md` | opus / high |
| **b** | `lane-b-546-currency-archival` | `worktree-lane-b-546-currency-archival` | **546–557** | finish-line | `CONTRACT-CLOSE-B-currency.md` | opus / medium |
| **c** | `lane-c-505-north-star-inventory` | `worktree-lane-c-505-north-star-inventory` | **none — births nothing** | finish-line | `CONTRACT-CLOSE-C-northstar.md` | sonnet / medium |

**Every contract of record lives in the operator's prompts dir at dispatch and is committed into
the tree by its own lane's step 0**, at `docs/audits/2026-08-17-technical-batch-7a-lane-<x>-contract.md`.
Stated so a reader does not resolve those filenames against `main` and conclude the manifest cites
vapour: they are off-repo at this instant, by design, and each reaches the tree when its lane
commits. That is `[#505]` clause 1 — falsified four times by chat-window contract delivery, hence
the committed-contract standing rule (STANDING_RULINGS I-D3).

## Reserved id blocks — the thing that makes concurrent births safe

Derived live before dispatch, from four independent sources that all agree:

```
tasks/ filenames     max = 533
BACKLOG.md           max = 533
git log --all        max = 533
JOURNAL.md           max = 533

documented synthetic / foreign hits EXCLUDED per standing precedent (c2f10440):
  [#777]     synthetic trip-test
  [#999]     synthetic trip-test  (tests/test_e2e_consumer_lifecycle.py, tests/test_gen_task_tree.py)
  [#900-905] fixtures in tests/test_check_backlog_filing.py
  [#715-721] fixtures in tests/test_audit.py + docs/audits/2026-07-26-codex-routine-consumers-check.md
  [#999999]  a documentation EXAMPLE in docs/audits/2026-08-04-codex-483-preflight-contract.md
  [#6235]    a GitHub issue number, not a backlog id

MAX REAL BRACKETED ID : 533
NEXT FREE ID          : 534
unused ids in 500..533: none  (allocation is monotonic; nothing is reused)

BLOCK A (lane a) = 534 535 536 537 538 539 540 541 542 543 544 545
BLOCK B (lane b) = 546 547 548 549 550 551 552 553 554 555 556 557
blocks disjoint       : True
clash with any real id: NONE
```

A lane allocating outside its block is a defect, not a convenience — that is the one rule that
makes two birthing lanes safe to run at the same time.

## Grammar — checked BEFORE provisioning, and re-checked against LIVE refs after

Batch 6 AMENDMENT 2 is the reason this section has two halves. There, the §B step-9 grammar gate
tested the names the roster *intended*; `claude --worktree <name>` prefixes `worktree-` when it
creates the branch, the dispatch passed the intended BRANCH name as the WORKTREE name, and all
twelve branches were born `worktree-worktree-lane-…` — **0 of 12** exempt, not 12 of 12. The check
had passed on the wrong input.

**So this roster passes the BARE name to `--worktree`**, and both the input and the output are
checked:

```
LANE_WORKTREE_RE  ^lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$
LANE_BRANCH_RE    ^worktree-lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$

BARE (--worktree arg)              worktreeRE   BRANCH git will create                     branchRE   classify
lane-a-534-audit-dispositions      PASS         worktree-lane-a-534-audit-dispositions     PASS       batch-lane
lane-b-546-currency-archival       PASS         worktree-lane-b-546-currency-archival      PASS       batch-lane
lane-c-505-north-star-inventory    PASS         worktree-lane-c-505-north-star-inventory   PASS       batch-lane

TOTAL 3 | refused: 0
identity pin  batch_manifest.LANE_BRANCH_RE is validate_branch_naming.LANE_BRANCH_RE  ->  True
```

The constant is the enum's own, imported — `batch_manifest` holds no second spelling of the grammar
(`[#514]`). **So the ADR-110 exemption covers three of three merges**, subject to the live-ref
re-check the packet will carry.

**The class is still not closed and this roster does not close it.** The grammar is enforced
NOWHERE AT PROVISIONING — `validate_branch_naming` is read-only and wired into no gate, and a lane
dispatched straight through `claude --worktree` never passes `/lane-boot` step 1. That is `[#531]`,
open, deferred out of batch 6 and not dispatched here either. A conforming roster is a checked
roster, not a gated one.

## 3×3 OWNED-FILES intersection — derived, not assumed

Per §A step 6, over the three contracts' OWNED-FILES headers, excluding the regen surfaces every
lane necessarily touches (`BACKLOG.md`, `tasks/manifest.json`, `docs/audits/README.md`):

```
        lane a        lane b        lane c
lane a  --self--      clear         clear
lane b  clear         --self--      clear
lane c  clear         clear         --self--

pairs checked : 3
COLLISIONS    : 0 of 3  -- roster is disjoint, dispatch is CLEAR
```

The three lanes are disjoint by **genre**, not by luck: lane a writes one new `docs/audits/` file
plus `tasks/534-545`; lane b writes `docs/decisions/**` and `docs/intake/**` plus `tasks/546-557`;
lane c writes one new `docs/audits/` file and nothing else. The two `docs/audits/` writers share a
directory but no file, and a directory is not a collision.

**Two generated surfaces are assigned to lane b rather than left ambient**, because only lane b
moves their inputs: `.claude/generated/recent-adrs.md` (gated by `claude-rosters-freshness`, fires
on ADR headers) and `docs/intake/README.md` + the intake residue carrier (gated by
`intake-index-freshness`, and needing a SECOND, non-hook-gated generator `gen_intake_tree.py` whose
omission FAILs `intake_tree_coherence`). Assigning them keeps them out of the ambient set where
two lanes could both regenerate them.

**One currency coupling is declared rather than prevented:** lane c inventories every ADR and every
intake while lane b archives terminal ones. Lane c's report is a snapshot of its branch point and is
correct as such; it is READ-ONLY to `docs/decisions/**` and `docs/intake/**`, so there is no git
collision — only a content-currency note, which is exactly why the merge order below puts the
read-only report first.

## Process-lane cap — declared EX-ANTE, and within cap

PLAYBOOK Ch8: *"at most 1/4 of a batch's lanes target methodology or hub-process surfaces"*,
evaluated against **dispatched width** (ADR-110 amendment 2026-08-08), floor arithmetic, under the
I-D10 three-way split (feature/satellite · finish-line · hub-introspection).

```
width 3  ->  cap = floor(3/4) = 0 hub-process lanes
declared ->  0
verdict  ->  WITHIN CAP
```

All three lanes are `finish-line`: a and b close out standing debt (undisposed audits, rotting
ADRs/intakes), c produces a read-only report. **None edits `scripts/`, `tests/`, `protocols/`, a
hook, or any living doc** — which is what keeps the cap satisfiable at width 3, where the floor
permits none. The `feature/satellite` bucket is empty.

## Merge order — c, a, b

Ruled by §C of the operator's prompt and restated here so the packet can be checked against it:

```
c  ->  a  ->  b
```

- **c first** — read-only, births nothing, so it cannot perturb the id space or the task tree.
- **a second** — lands block-a births and the disposition ledger that lane b's step-3 row cites.
- **b last** — lands block-b births plus the archival moves and the index regens, on top of a
  task tree that is already settled.

## Baseline at manifest commit — the numbers every later gate reading is measured against

- `main` @ `4154b61f`, **== `origin/main`**, working tree clean, `git worktree list` = 1 entry
  (primary only), `git stash list` empty.
- `batch_manifest.open_batches('.')` → `[]` — no batch open, no exemption inherited.
- `docs/audits/2026-08-17-technical-batch-7a-packet.md` **absent** from `HEAD` (the closer is live);
  `_valid_closer()` on that path → `True`.
- `python scripts/audit.py health` → **`health: OK`**, 0 FAIL.
- **Carried WARNs at baseline**, so they are not later mistaken for queue damage:

  ```
  doc_rot                   21
  undeclared_edges          18
  no_ff_merges               3
  review_artifact_coverage   2   (7 unlinked code-impact merges + 1 untallied artifact)
  journal_spine_anchor       1   (advisory: anchored-by-mention, not by an 'Anchors:' record line)
  ```

- JOURNAL entry `2026-08-17 (a)` already exists; this arc's integration entry derives its own
  letter from `JOURNAL.md` at commit time rather than from this file.

## Two mechanical facts derived live against the parser, before writing

**1. The filename matches `MANIFEST_GLOB`.** `batch_manifest.MANIFEST_GLOB` is
`docs/audits/*-batch-*-manifest.md`, matched with `PurePosixPath.match`. Verified against the parser
itself: `2026-08-17-technical-batch-7a-manifest.md` → `True`. The packet path → `False`, which is
correct: the closer must not itself be readable as a manifest.

**2. Both names pass the ADR-101 refusal gate.** `validate_hermetization.classify()` on
`docs/audits/2026-08-17-technical-batch-7a-manifest.md` and on the packet path → no violation
(class `technical`, well-formed slug, lowercase kebab).

## Closure contract

The batch closes when **all** of the following hold, and committing
`docs/audits/2026-08-17-technical-batch-7a-packet.md` is the single act that discharges the last of
them and expires the ADR-110 exemption:

1. the merge queue is drained in the order **c a b** — every lane branch merged with a SHA, or
   explicitly held with a reason (HOLD is a recorded disposition, never silence);
2. full suite run **once** on the merged result, verdict quoted;
3. **honest-RED is in force**: the only tolerated REDs are the known owned ones carried from
   baseline. Any NEW red means `main` is **NOT pushed**, the packet attributes the failure, and the
   run stops. No RED is ever dispositioned green;
4. **zero `--no-verify` and zero `SKIP=`** across the whole batch, integrator included;
5. teardown runs for **MERGED lanes only** (`worktree remove` + `prune` + `branch -d`, **never
   `-D`**); HOLD and TIMED-OUT lanes keep their worktrees and branches untouched for the operator;
6. `git stash list` empty — a surviving entry gets a recorded disposition, never a blind `drop`;
7. the packet reports the dispatched-vs-close width delta and disposes of every HOLD by name.

**Timeout disposition, declared ex-ante:** lanes are polled every 5 minutes to a cap of 2h30m. A
lane not done at cap is **TIMED-OUT-HOLD** — never merged, worktree and branch kept, named in the
packet. A hold is a disposition, and the batch closes around it rather than waiting on it.

## One standing consequence of an open batch, stated so it is not discovered mid-arc

`gen_handoff.assert_batch_boundary` **refuses to cut a handoff bundle while a batch is open**
(WINDOW = BATCH). The §D supplement therefore lands **after** the closing packet, which is correct
sequencing rather than an obstacle — and never a bypass.

## What this manifest deliberately does NOT do

- It does not reorder the merge queue, rename any branch, or delete anything.
- It does not birth, close, or edit a single BACKLOG row. **Births — ZERO.** The 24 reserved ids are
  *reserved*, not allocated: no `tasks/` file exists for any of them at this instant, and each is
  born by its own lane's own commit or not at all.
- It does not edit `protocols/STANDING_RULINGS.md` or any register. The 2026-08-17 ruling is quoted
  here as this batch's authority; whether it becomes a standing register line is the architect's
  call, not this file's.
