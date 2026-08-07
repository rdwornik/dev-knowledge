---
batch: 2
status: open
closed_by: docs/audits/2026-08-07-technical-batch-2-packet.md
---

# Batch 2 — manifest, committed at DISPATCH

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-07 · **Slug:** batch-2-manifest
- **Protocol:** ADR-110 + PLAYBOOK Ch8 "The batch protocol". Width **6**, two waves.
- **Authority:** dispatched by the operator; this file is the plan, frozen at dispatch.
- **Predecessor:** batch 1 (`df815c7..319f885d`), packet
  `docs/audits/2026-08-06-technical-batch-1-integration-packet.md`, independently verified in
  `docs/audits/2026-08-06-technical-batch1-verification.md`.

## Why this file exists, and what changed since batch 1

Batch 1 archived **half** its evidence: the end-of-batch packet landed, the manifest never did,
because the lane contracts were delivered as chat prompts. The close-out's item 4 therefore
passed on a technicality while the batch's *intent* had already evaporated — reconstructable
from its outcome, not from its plan. Ch8 now requires the manifest **at dispatch**, and this is
the first one.

**It is also load-bearing at the gate, which batch 1's would not have been.** The ADR-110
amendment 2026-08-07 (R-1) keys the declared-integration-arc exemption to a committed manifest
declaring an **open** batch: while this file says `status: open` and its `closed_by:` packet is
absent from the tree, `audit.py::check_journal_spine_anchor` skips unanchored `worktree-lane-*`
merges — and reports that it did, naming this file. That replaces batch 1's
`SKIP=audit-health`, which disabled the entire check registry twice and would five times here.

**Expiry is automatic and needs no edit.** `docs/audits/` is immutable (CLAUDE.md §5 rule 3), so
openness is deliberately *not* a mutable `status:` flag anyone flips. The exemption dies the
moment `docs/audits/2026-08-07-technical-batch-2-packet.md` exists. That packet carries the
**dispatch** date rather than the close date, precisely so this file could name it before it
existed — manifest and packet are a matched, pre-declared pair.

## Lane roster

Six lanes, two waves. **Wave 2's contracts are declared here but not yet authored** — the lanes,
their rows, and their footprints are frozen by this file; the prompts follow.

### Wave 1 — dispatched with this manifest

| Lane | Branch | Rows | Size | Class |
|---|---|---|---|---|
| lane-1 | `worktree-lane-1-490-parity-manifest` | [#490] + [#430] | M+M | feature/consumer |
| lane-2 | `worktree-lane-2-429-worktree-portability` | [#429] | M | **process** |
| lane-3 | `worktree-lane-3-320-fleet-backup` | [#320] | S | feature/consumer |

### Wave 2 — declared, prompts pending

| Lane | Branch | Rows | Size | Class |
|---|---|---|---|---|
| lane-4 | `worktree-lane-4-283-corp-dedup` | [#283] | S | feature/consumer |
| lane-5 | `worktree-lane-5-416-aicouncil-codemap` | [#416] | S | feature/consumer |
| lane-6 | `worktree-lane-6-393-corpsca-rot` | [#393] | S | feature/consumer |

Branch names follow the Ch8 grammar `worktree-lane-<n>-<id>-<slug>`, a refinement of the
`worktree-<name>` prefix (no new enum member, so no ruling needed) and matched 1:1 with their
contract files. `scripts/validate_branch_naming.py` classifies them; the R-1 exemption keys on
the `worktree-lane-*` shape, so these names are what make it apply.

## Footprints — exclusive ownership, declared here because the rows do not

**None of the six rows carries a `footprint:` field.** That is batch-1 finding **LB-1** repeating
at scale: a row whose done-when forces a file its footprint never named. Rather than dispatch on
that, ownership is declared here and **this table is the arbitration surface** — a lane that
needs a path outside its block escalates rather than takes it.

| Lane | EXCLUSIVELY owns | Explicitly NOT this lane's |
|---|---|---|
| lane-1 | `ecosystem/parity-surfaces.yaml`, `scripts/fleet_parity.py`, `tests/test_fleet_parity*.py`, `ecosystem/dependency-baseline.yaml` | anything under `.github/`; `scripts/audit.py` beyond the `check_fleet_parity` call site |
| lane-2 | `.worktreeinclude`, worktree-provisioning scripts + their tests | `scripts/audit.py`; `scripts/fleet_parity.py` |
| lane-3 | no hub source files — operates on sibling-repo git state; writes only its own audit artifact | every hub source file |
| lane-4 | `corp-monorepo` working tree only (consumer worktree/branch shape, RULING-W) | every hub file |
| lane-5 | `ai-council/ARCHITECTURE.md` only (consumer worktree/branch shape, RULING-W) | every hub file |
| lane-6 | `corp-sca` working tree only; disposition recorded in its own artifact | every hub file |

**The one real collision, resolved by co-location rather than by ordering.** [#490] and [#430]
both touch `scripts/fleet_parity.py`, so they are ONE lane. Ch8: a dependency chain lives inside
a single lane, because a lane is the unit that can carry order and the integrator has no way to
express a cross-lane merge constraint.

**Serialize-group note, recorded so it is not discovered at merge time.** [#430] (lane-1) and
[#393] (lane-6) both declare `serialize-group: audit-py`. They are in **different waves**, which
serialises them by construction. If wave 2 is ever pulled forward, this pair is the first thing
to re-check.

**Shared generated surfaces — regenerate, never hand-merge.** `docs/audits/README.md` collided at
width 3 and will collide on most merges at width 6. Every lane writing an audit artifact
**pre-declares its filename here**, and the integrator resolves every collision with
`gen_audit_index.py --write`, never by hand (batch-1 gate firing #3: a hand-merge reads
correctly and fails its own hook). Same rule for `ecosystem/doc-counts.md` and `BACKLOG.md`.

Pre-assigned audit filenames (ADR-101 Rule B verified at authoring time, per F3):

- lane-1 `docs/audits/2026-08-07-technical-lane-1-parity-manifest.md`
- lane-2 `docs/audits/2026-08-07-technical-lane-2-worktree-portability.md`
- lane-3 `docs/audits/2026-08-07-technical-lane-3-fleet-backup.md`
- lane-4 `docs/audits/2026-08-07-technical-lane-4-corp-dedup.md`
- lane-5 `docs/audits/2026-08-07-technical-lane-5-aicouncil-codemap.md`
- lane-6 `docs/audits/2026-08-07-technical-lane-6-corpsca-rot.md`

## Quota accounting — 5 feature / 1 process

The ≤1/4 process-lane cap binds from batch 2. At width 6 it permits **at most 1** process lane,
so **≥5 must be non-process**. This batch runs **5 feature/consumer + 1 process** (lane-2,
[#429] worktree provisioning — hub methodology tooling, and the only lane whose subject is the
method itself).

**The reading this rests on, stated plainly because it is the load-bearing judgement and it is
the operator's, not mine.** Under the operator directive, *consumer-class* = **acts on consumer
repos or on fleet outcomes**. Lanes 3–6 act directly on sibling repos (`corp-monorepo`,
`ai-council`, `corp-sca`, and the three repos holding unpushed work); lane-1 makes the fleet
parity surface measure 9/9 members instead of a third. Under a **stricter** reading — *product
work, i.e. non-methodology feature development* — this repo supplies **zero** such lanes by
construction, and batch 2 would have to draw from consumer backlogs the hub does not own. That
alternative was surfaced in the 2026-08-07 morning packet and the operator ruled the first
reading. Recorded here so the count is auditable against a stated definition rather than an
assumed one. Batch 1, for comparison, ran **3/3 process**.

## Conditions ledger — the three GO conditions from the batch-1 verification §9

| # | Condition | State | Evidence |
|---|---|---|---|
| 1 | Batch manifest committed at dispatch | **MET** | this file |
| 2 | R-1 adjudicated, or the skip pre-authorized in writing | **MET** | approved as drafted and BUILT: ADR-110 `## Amendment — 2026-08-07`, `scripts/batch_manifest.py`, `tests/test_batch_manifest.py` (11 tests). `SKIP=audit-health` is retired for intermediate merges. |
| 3 | Every lane gets its review artifact up front | **REQUIRED CLAUSE in every lane contract** | each contract carries a mandatory codex/terra review of its own code-impact diff, with a parseable `**Tally:**`; the wrapper now emits the field on every artifact (LC-1) |

**Condition 3 binds the integrator too.** The morning arc is the counter-example: its own merge
`2f2edd2b` was flagged by `review_artifact_coverage` for exactly the gap lanes A and B were, and
the retroactive review then found two real defects in it. An integrator arc that touches
`scripts/` or `tests/` carries a review like any lane.

## Baseline at dispatch

- `main` @ the PRE-2 merge; **ship-gate GREEN** (cleared by three real retroactive reviews and
  one cited disposition — no force-greening).
- Suite: **2 pre-existing REDs**, both failing identically on bare `main`
  (`test_routine_consumers_live_backlog_governs_exactly_one_row`,
  `test_check_fleet_parity_green_on_live_repo` — [#430], which lane-1 owns).
- `git worktree list` == primary only; `git stash list` empty (Ch8 close-out item 5).

## What this batch is the test of

**[#505] clause 1 — *"a fresh seat runs a full batch from repo artifacts alone"* — is falsified
until a batch runs from a committed manifest.** This file is that manifest, and batch 2 is that
test. The row stays OPEN until the batch closes against it; closing it earlier would ratify the
gap as satisfied. Clause 2 (*exactly 2 operator touches*) has never been measured — the
end-of-batch packet records the count, so it becomes evidenceable for the first time.

## Close-out — the five items this batch cannot finish without

Per Ch8 (four from ADR-110 §3, the fifth added 2026-08-07 on batch-1 F4):

1. every lane branch merged-or-explicitly-abandoned
2. full suite run once on the merged result
3. `git worktree list` == primary only
4. manifest (this file) **and** packet archived
5. `git stash list` empty — a surviving entry gets a recorded disposition, never a blind `drop`

Committing `docs/audits/2026-08-07-technical-batch-2-packet.md` at close is what discharges item
4 **and** expires the R-1 exemption. The two are the same act by design.
