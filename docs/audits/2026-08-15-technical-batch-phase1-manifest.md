---
batch: 5
status: open
closed_by: docs/audits/2026-08-15-technical-batch-phase1-packet.md
---

# Batch 5 (phase-1) — manifest, committed AT INTEGRATION (after dispatch, before the merge queue)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-15 · **Slug:** batch-phase1-manifest
- **Protocol:** ADR-110 + its 2026-08-07 amendment (the declared integration arc) + PLAYBOOK Ch8
  "The batch protocol". Width **7** dispatched (lanes M, N, O, P, Q, R, S), one wave.
- **Authority:** the phase-1 architect rulings R1–R7 of 2026-08-15, issued on
  `PHASE1-REVIEW-PACKET.md` (operator's Downloads, off-repo — this manifest is its in-repo
  carrier for the parts that bind the tree). **R1 is the ruling this file discharges.**
- **Predecessor:** batch 4 — manifest `docs/audits/2026-08-11-technical-batch-4-manifest.md`,
  packet `docs/audits/2026-08-11-technical-batch-4-packet.md` (both committed, so that batch is
  CLOSED). Verified immediately before writing this file:
  `batch_manifest.open_batches(.)` → `[]`. **This manifest inherits no stale exemption and opens
  the only live batch.**

## Provenance — why this file is late, stated rather than concealed

> **This manifest is committed AT INTEGRATION, not at dispatch.** All seven lanes were dispatched
> without one, ran to completion, and were reviewed before it existed. It declares the batch OPEN
> in the present tense so the merge queue can run under the ADR-110 exemption; it does not claim
> to have existed earlier, and no timestamp in it is back-dated.

This is the **fourth consecutive batch** to miss the commit-at-dispatch condition (batch 3 late,
the night cloud batch late, batch 4 late, this one late — and later than any of them, since the
prior three were at least mid-flight). Recorded as a recurrence, not as news: `[#505]` leg 1
remains unmet, and this file is a partial repair of that regression, **not** a discharge of the
row. Two lanes (M §7 and P §8.1) independently flagged the absence rather than filing one
themselves, which was the correct call — a batch manifest is outside a lane's manifest.

**Expiry is automatic and needs no edit.** `docs/audits/` is immutable (CLAUDE.md §5 rule 3), so
openness is deliberately not a mutable flag anyone flips: this batch is open exactly while
`docs/audits/2026-08-15-technical-batch-phase1-packet.md` is ABSENT from the committed tree, and
that packet's landing ends the exemption with no edit anywhere. Verified absent from `HEAD` before
writing (`git cat-file -e HEAD:<packet>` → does not exist).

## Lane roster — width 7, one wave

All seven branches were cut from **`d62796ad`**, verified lane by lane
(`git merge-base main <lane>` → `d62796ad` ×7): **zero inter-lane git dependencies.**

| Lane | Branch | Tip | Rows | Bucket | Contract of record |
|---|---|---|---|---|---|
| **S** | `worktree-lane-s-w20-draft-landing` | `6516f6e2` | none (W2-0 conversion drafts) | finish-line | `docs/audits/2026-08-15-technical-w20-draft-landing-lane-contract.md` |
| **Q** | `worktree-lane-q-293-satellite` | `82d128f8` | `[#293]` | feature/satellite | `docs/audits/2026-08-15-technical-293-consumer-runbook-fan-out-lane-contract.md` |
| **R** | `worktree-lane-r-gateclose-drain8` | `41c040b4` | drains `#344 #423 #430 #415 #487 #428`; holds `#523 #514` | finish-line | `docs/audits/2026-08-15-technical-gateclose-drain8-lane-contract.md` |
| **N** | `worktree-lane-n-528-legs12-latency` | `03814f6c` | `[#528]` legs 1+2 | hub-introspection | `docs/audits/2026-08-15-technical-528-legs12-latency-lane-contract.md` |
| **M** | `worktree-lane-m-529-telemetry-emit` | `d45fdb9e` | `[#529]` | feature | `docs/audits/2026-08-15-technical-529-telemetry-emit-lane-contract.md` |
| **P** | `worktree-lane-p-530-single-flight` | `11b0cbdb` | `[#530]` | feature | `docs/audits/2026-08-15-technical-530-single-flight-lane-contract.md` |
| **O** | `worktree-lane-o-527-block-main` | `9732daea` | `[#527]` | hub-introspection | `docs/audits/2026-08-15-technical-527-block-main-lane-contract.md` |

**Every contract of record is committed on its own LANE BRANCH, not on `main`** — stated so a
reader does not resolve them against `main` and conclude the manifest cites vapour. Each reaches
`main` when its lane merges. This satisfies I-D3 (a contract living only in the prompts dir is not
a fact in the tree) **retrospectively**, which is the honest description: the lanes self-served
their contracts, and no roster existed for them to register against until now.

**Lane P's tip moved after review.** The review packet records `73da833c`; the tip above is
`11b0cbdb`, which adds the integrator fixup ruled by **R2** (one line: `errors="replace"` on the
`_cli` helper's `subprocess.run`, copying lane O's already-solved pattern for the identical
cp1252-vs-strict-utf8 class). Re-measured in a DEFAULT shell with `PYTHONUTF8` explicitly unset:
**20 passed, exit 0** (before the fix, 19 passed / 1 failed in the same shell).

## Ruled merge order (R4)

**S → Q → R → N → M → P → O.** Fixed by the architect, not derived here. O is last because it
arms a new commit-time gate (`block-commit-on-main`) that changes the rules for every commit after
it lands: the queue completes under today's rules and the new gate governs from a clean edge.

## R1 — the authorization line for the four new files in M and P

The architect grants the authorization/exemption line for the four files lanes M and P add, which
are the ruled births `[#529]` and `[#530]`:

| Path | Lane | Row |
|---|---|---|
| `scripts/telemetry_emit.py` | M | `[#529]` |
| `tests/test_telemetry_emit.py` | M | `[#529]` |
| `scripts/single_flight.py` | P | `[#530]` |
| `tests/test_single_flight.py` | P | `[#530]` |

**Stated honestly: this authorization is belt-and-braces, not load-bearing, and the difference is
worth recording.** Run live against the gate before writing this file,
`validate_hermetization.classify()` returns `None` (admit) for all four paths — `scripts/` and
`tests/` are long-established allowlisted homes under ADR-101, so Rule A, Rule B and the Rule C
home allowlist each admit them without any grant. The authorization therefore records an
**operator decision that these two births land**, and does not paper over a refusal that never
happened. Claiming otherwise would misrepresent what the gate did.

Lane O's `scripts/block_commit_on_main.py` / `tests/test_block_commit_on_main.py` were checked
through the same call and likewise admit; they are named here for completeness, not authorized,
because `[#527]` is a pre-existing row rather than a birth of this batch.

## THE HAZARD THIS BATCH CARRIES INTO ITS OWN MERGE QUEUE — two lanes get NO exemption

**Lanes S and R are REFUSED by the ratified lane grammar.** Measured live against
`validate_branch_naming.LANE_BRANCH_RE` (`^worktree-lane-[a-z]-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$`),
which `batch_manifest.is_lane_merge` imports as the single definition of that grammar:

```
branch                                  strict
worktree-lane-s-w20-draft-landing       False    <- id slot is `w20`, not \d+
worktree-lane-q-293-satellite           True
worktree-lane-r-gateclose-drain8        False    <- no id slot at all
worktree-lane-n-528-legs12-latency      True
worktree-lane-m-529-telemetry-emit      True
worktree-lane-p-530-single-flight       True
worktree-lane-o-527-block-main          True
```

**So the ADR-110 declared-integration-arc exemption covers five of seven merges, not seven.** The
S and R merges land unanchored, non-exempt first-parent spine entries, and
`check_journal_spine_anchor` returns **FAIL** — which, because `audit-health` is a *pre-commit*
gate, wedges every subsequent commit in the queue. S is merge #1 and R is merge #3, so the wedge
would fire almost immediately.

**This is the third occurrence of the same class.** Batch 4's manifest filed it against its W4/W6
(`worktree-lane-d-conversions-w1`, `worktree-lane-f-arch-soft-obs`) and resolved it by *removing*
both lanes from the roster. The class is not the two branch names; it is that **the grammar is
enforced nowhere at provisioning** — `validate_branch_naming` is read-only and wired into no gate,
and a lane dispatched straight through `claude --worktree <name>` never passes `/lane-boot` step 1.
`batch_manifest.py`'s own honest-limits block says exactly this. An off-enum lane name is still
freely creatable; what it silently loses is the exemption.

### How this batch resolves it — by ANCHORING, not by renaming or reordering

The three ways out the batch-4 manifest named were: reorder the queue, rename the branches to
carry a sentinel id (`\d+` accepts `0`), or anchor the two merges by hand. **The first two are
unavailable or undesirable here** — the merge order is ruled by R4 and is not the integrator's to
change, and reordering would not help anyway because the strict grammar is *already* on `main`
(unlike batch 4, where the hazard was a future landing). Renaming would work but invents two
sentinel ids for lanes that have no row id to carry, and mutates refs the review packet and the
lane commit bodies both cite by name.

**So the third route is taken, and it is the primary mechanism rather than an exemption:** the
JOURNAL entry that rides *this* manifest arc (`2026-08-15 (b)`) names the lane tips `6516f6e2`
(S) and `41c040b4` (R) on an explicit `Anchors:` record line. `journal_anchor.is_anchored` holds
that a spine entry is anchored when JOURNAL names ≥1 SHA the entry **introduced** — both tips are
commits that already exist on their lane branches, and each is introduced by its own merge. Both
merges are therefore anchored from the instant they land, by the gate's ordinary predicate, with
no exemption involved and nothing renamed.

**The honest limit of that route, stated so it is not discovered later:** it works because the
anchoring predicate is a text match over JOURNAL, and it lets an integrator anchor a merge
*before* making it. That is a real property of the mechanism, not a hole this batch opened — but
it is used here deliberately and disclosed, rather than relied on quietly. The five conforming
lanes are left to the ADR-110 exemption, which is what that exemption exists for; only the two
lanes the exemption *cannot* reach are anchored this way.

**Recorded as a finding for the packet, not birthed as a row here:** this manifest births no
BACKLOG row (see below). The provisioning-time enforcement gap is the packet's to carry forward.

## Process-lane cap — the arithmetic, reported not adjudicated

PLAYBOOK Ch8: *"at most 1/4 of a batch's lanes target methodology or hub-process surfaces"*,
evaluated against **dispatched width** (ADR-110 amendment 2026-08-08), floor arithmetic, under the
I-D10 three-way split (feature/satellite · finish-line · hub-introspection).

At width **7** the cap permits **⌊7/4⌋ = 1** hub-process lane. The roster as dispatched carries
**2** in the `hub-introspection` bucket:

- **N** — `[#528]` legs 1+2 lands doctrine in `protocols/PLAYBOOK.md` and moves a
  `protocols/ESSENTIALS.md` freshness stamp. Methodology surface by any reading.
- **O** — `[#527]` arms a new pre-commit gate on the hub's own commit path and edits
  `.pre-commit-config.yaml`. A hub-process surface, though it is also a shipped mechanism.

**Over by exactly one lane.** Width 8 would be the first roster admitting two (`⌊8/4⌋ = 2`).

**This is recorded, not ruled.** The operator dispatched this roster; the cap is doctrine carried
by intake #27, is mechanized in nothing, and a manifest is not the place to overturn a dispatch.
Ch8 requires the **end-of-batch packet** to report the close-width delta — this line is the input
to that report, so the overage is discharged deliberately or recorded as a known exceedance, never
discovered afterwards. The bucket assignment for **O** is the debatable one and is flagged as
such: read as a shipped feature rather than a hub-process surface, the roster is within cap.

## Baseline at manifest commit

- `main` @ `d62796ad`, clean working tree at branch time; integration branch
  `docs/phase1-batch-manifest`.
- `batch_manifest.open_batches(.)` → `[]` — no batch open, no exemption inherited.
- `docs/audits/2026-08-15-technical-batch-phase1-packet.md` absent from `HEAD` (the closer is live).
- `python scripts/audit.py health` → **`health: OK`** on bare `main` before any merge. This is the
  baseline every later gate reading is measured against, so a WARN appearing after the queue is
  attributable to the queue rather than inherited.
- `git worktree list` = 8 entries: primary + all seven lanes (`lane-n-…` locked, the other six
  unlocked).
- `git stash list` empty.
- JOURNAL entry `2026-08-15 (a)` already exists; this arc's is `(b)`, derived from `JOURNAL.md` at
  merge time rather than from any contract, and the integration wrap re-derives its own letter the
  same way.

## Two mechanical facts derived live against the parser, before writing

**1. The filename matches `MANIFEST_GLOB`.** `batch_manifest.MANIFEST_GLOB` is
`docs/audits/*-batch-*-manifest.md`, matched with `PurePosixPath.match` against the basename.
Verified against the parser itself:

```
True    2026-08-15-technical-batch-phase1-manifest.md
False   2026-08-15-technical-528-legs12-manifest.md
```

The second line matters: **lane N ships its own `-manifest.md`** and it does **not** match the
batch glob (no `-batch-` token). That is correct and is stated so a reader does not mistake a
lane-scoped manifest for a second open batch — it declares nothing to `open_batches()`.
`_valid_closer()` was likewise run against the `closed_by` value above → `True`.

**2. `batch: 5` — a digit, because a test pins it.**
`tests/test_batch_manifest.py::test_the_live_repos_own_manifest_is_well_formed` asserts
`b.batch.isdigit()` against every live open manifest; batch 3's manifest shipped a date-shaped
value and was RED from the moment it landed. The field is reporting-only —
`batch_manifest` reads it as `fm.get("batch", "?")` and gates openness on `status:` and
`closed_by:` alone — but a malformed value leaves the mechanism working while failing the repo's
own well-formedness pin.

## Closure contract

The batch closes when **all** of the following hold, and committing
`docs/audits/2026-08-15-technical-batch-phase1-packet.md` is the single act that discharges the
last of them and expires the ADR-110 exemption:

1. the merge queue is drained in the R4 order — every lane branch merged with a SHA, or explicitly
   abandoned with a reason;
2. full suite run **once** on the merged result, verdict quoted;
3. the R7 owed items land: lane N's six declined/owed items dispositioned, the `[#529]` / `[#530]`
   / `[#528]` row updates applied at the `tasks/` source, Q's JOURNAL allocation, and the `[#528]`
   row drain per Y-3 ownership;
4. **R2's two real P1s are appended as open legs to `[#530]`** (ABA release race; `rev-parse`
   conflation) and **`[#530]` stays OPEN** — merged is not closed;
5. **R6's denominator correction** lands at `tasks/293-*.md` source (ADR-104's 8 non-hub members
   govern over row prose); the cross-repo seeding itself stays operator-gated and is NOT executed;
6. **R3's rejection** of terra's Layer-2 claim on lane P is recorded in the persisted terra
   artifact; the CLAUDE.md §5 rule-4 descriptive falsity is carried as a packet wrap item and
   **CLAUDE.md is not edited** for it;
7. **R5** — the two PLAYBOOK-cited night-2 reports land byte-faithful in `docs/audits/` so the
   doctrine's SHA citations resolve on `main`, and all 8 night-2 branches are re-verdicted in the
   teardown table v2 (**proposals only — nothing is deleted**);
8. teardown is proposed, not executed: worktree removal waits on the operator naming which board
   sessions are closed;
9. `git stash list` empty — a surviving entry gets a recorded disposition, never a blind `drop`;
10. the packet reports opened / closed / net / open-total with the filter it was measured on
    (STANDING_RULINGS H2), records the **dispatched-vs-close width delta**, and disposes of the two
    observations this manifest files: the **process-lane cap overage** and the **off-grammar
    stranding of S and R**.

## One standing consequence of an open batch, stated so it is not discovered mid-arc

`gen_handoff.assert_batch_boundary` **refuses to cut a handoff bundle while a batch is open**
(WINDOW = BATCH). Any bundle work therefore lands **after** the closing packet, which is correct
sequencing rather than an obstacle — and never a bypass.

## What this manifest deliberately does NOT do

- It does not reorder the merge queue (R4 rules it), rename any branch, or delete anything.
- It does not adjudicate the process-lane cap overage or the O bucket assignment — both are named
  as the operator's call and reported to the packet.
- It does not birth, close, or edit a single BACKLOG row. **Births — ZERO.**
