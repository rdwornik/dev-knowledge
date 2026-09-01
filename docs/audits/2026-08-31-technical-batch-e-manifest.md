---
batch: E
seq: 1
shape: ADR-110 — DERIVE -> architect's cut -> FREEZE -> DISPATCH; 7 cloud read-only censuses (executed) + 15 committing lanes + 1 codespace admission probe (executed, RED)
dispatched: 2026-08-31
status: open
closed_by: docs/audits/2026-09-01-technical-batch-e-close-packet.md
substrate: LOCAL (14) + CLOUD (1, DM-4 by ruling CUT-4)
---

# BATCH E — HERMETIZATION · THE MANIFEST

**This file is the gate-readable manifest.** `scripts/batch_manifest.py` resolves open batches
with `MANIFEST_GLOB = "docs/audits/*-batch-*-manifest.md"`, reads every input from **HEAD**, and
grants the ADR-110 exemption only when the manifest is TRACKED, `status: open`, and `closed_by:`
names a shape that CAN resolve and is ABSENT from the tree. All four hold here.

**`closed_by:` is set at DISPATCH, not at close** (prerequisite 0c). A manifest carrying no
`closed_by:` opens nothing at all, because an exemption that cannot expire is not an exemption.

## THE TEARDOWN ENUM — read this before tearing anything down (prerequisite 0a)

`LANE_BRANCH_RE` is `^worktree-lane-[a-z]-\d+-<slug>$`. **It matches ONE letter then digits.**
The first cut of this batch named its lanes `dc-1`, `hy-4` and so on — two letters — and
**every one of the 14 local lanes was therefore outside the enum the teardown and the ADR-110
exemption both iterate.** That is precisely the defect that stranded ADR-116 on `claude/lane-f`,
and it was caught **at freeze by predicate 5**, not at integration. The lanes below carry
conforming names as a result.

**The teardown iterates THIS TABLE, not a branch glob.** One lane runs off-machine on the
`claude/` prefix, which no `worktree-*` glob can see.

## THE LANES — 15 committing, frozen 2026-08-31

Operator name, conforming slug, branch, substrate, blocked-by. **Contracts are in
`docs/audits/2026-08-31-technical-batche-launch-contracts/`.**

```
DC-1   lane-a-1-vision-to-readme                 worktree-lane-a-1-...    local   —
DC-23  lane-b-2-essentials-and-claude-md         worktree-lane-b-2-...    local   DC-1
DC-4   lane-c-3-root-contract                    worktree-lane-c-3-...    local   —
DC-5   lane-d-4-ai-council-instantiation         worktree-lane-d-4-...    local   DC-4
DM-1   lane-e-5-eval-sda1-harbor                 worktree-lane-e-5-...    local   tier (B) draft
DM-2   lane-f-6-observability-otel               worktree-lane-f-6-...    local   tier (B) draft
DM-3   lane-g-7-typed-multi-layer-graph          worktree-lane-g-7-...    local   —  (DRAFTING)
DM-4   lane-h-8-local-memory-tier-l-evaluation   claude/lane-h-8-...      cloud   —  (TIER-L EVAL)
DM-5   lane-i-9-distiller-filing-amendment       worktree-lane-i-9-...    local   —  (FILING)
DM-6   lane-j-10-equilibrium-checkpoint-...      worktree-lane-j-10-...   local   —  (FILING)
HY-1   lane-k-11-derived-doc-freshness           worktree-lane-k-11-...   local   A4 harvest + DC-1
HY-2   lane-l-12-logs-retention-rule             worktree-lane-l-12-...   local   —
HY-3   lane-m-13-templates-disposition           worktree-lane-m-13-...   local   A1 + A2 harvest
HY-4   lane-n-14-trends-burndown-and-quota-panel worktree-lane-n-14-...   local   —
HY-5   lane-o-15-wintooling-local-default        worktree-lane-o-15-...   local   —  (CROSS-REPO)
```

**DM-4 is the one non-`worktree-` lane.** It carries a recorded
`**Substrate deviation:** substrate-teardown-enum-coverage`, discharged by this manifest naming
it. The teardown must reach `claude/lane-h-8-local-memory-tier-l-evaluation` explicitly.

**HY-5 runs IN `win-tooling`, not in the hub.** Layer 2 never executes: the hub rules, the
consumer carries. Its teardown is win-tooling's, not this repo's.

## THE FREEZE GATE — six predicates, run 2026-08-31

`scripts/validate_substrate.py` over all 15 contracts:

```
REFUSE findings: 0
WARN findings:   2, both OVERRIDDEN by a recorded deviation (kept, never removed)
  · DM-4  substrate-teardown-enum-coverage    — cloud lane, enumerated in this manifest
  · DC-1 <-> HY-1  substrate-lane-write-scope-disjoint
        — a DELIBERATE, SEQUENCED overlap on scripts/canonical_docs.py. Merge order is
          frozen DC-1 -> HY-1 and the integrator verifies DC-1 has merged before
          dispatching HY-1.
```

Predicates 5 and 6 arrived with this batch (0a and CUT-6). They are fully armed HERE, at freeze;
the commit-time adapter grandfathers the pre-existing corpus by a per-leg arm date so a leg
written today does not retro-gate a dispatch that already happened.

**THE FREEZE GATE IS SCOPED TO THE LANES BEING FROZEN — the 15 above — and that scoping is
stated rather than assumed.** Run over the whole directory it also REFUSES all seven tier-(A)
contracts, on predicate 5, because they pair to `claude/…` branches. That is a TRUE finding
about an already-executed dispatch: those seven ran 16:44–16:50 on 2026-08-31, **hours before
predicate 5 existed**. Editing them to satisfy a validator written afterwards would falsify what
was actually dispatched — the same ruled basis on which `lane-contract-check` grandfathers the
batch-1 contracts. **Their discharge is this manifest's teardown table, which names all seven**,
which is exactly what predicate 5's own refusal text asks for: *"Declare the lane in the manifest
and record the deviation."*

**The lane-contract SHAPE gate is NOT scoped** — it runs over all 22 contracts in the directory
and exits 0. Three real defects surfaced there and were fixed rather than excused: a
`Dispatch-Lane` line written with `-Slug` instead of the positional
`<slug> <file> -Effort <tier>` form (14 lanes), a contract filename carrying a `batch-e-` prefix
that broke the 1:1 slug-to-file pairing (15 lanes — batch identity comes from the DIRECTORY,
as batch D did it), and DM-4 declaring `cloud` while carrying no `## Receipt gate` (Q5).

## TIER (A) — EXECUTED, 7 of 7. Read-only, zero commits.

Dispatched 2026-08-31 16:44–16:50 CEST, all `Ok=True` / `Bound=True`, all harvested
(186,734 bytes total). Session ids and receipts:
`docs/audits/2026-08-31-technical-batche-launch-contracts/PLAN.md` section 1.
Cloud lanes on the `claude/` prefix — **outside `LANE_BRANCH_RE`, so the teardown must reach
them from this manifest**. They wrote nothing and created no commits, so no merge is owed.

## TIER (C) — EXECUTED, RED. Committing lanes stay LOCAL.

`docs/audits/2026-08-31-verification-codespace-admission-probe.md`.
L1 Ok=TRUE (transport only) · **L2 RemoteExitCode=1** · **L3 HEAD comparison NOT MEASURED** ·
gate NOT RUN. The container's agent returned *"Not logged in"* in 47 ms. Z-G3's entry condition
is **NOT met**; the router-ADR entry condition is **NOT** recorded as MET. Codespace
`batche-c-admission-pgw54jqwv7qf65rj` is STOPPED (compute billing ended); delete deliberately.

## MERGE ORDER

```
1.  DC-1                        (unblocks DC-23, HY-1)
2.  DC-23                       (its LAST act is conditional on DC-1 being merged)
3.  DC-4  ->  DC-5
4.  DM-3 · DM-5 · DM-6 · HY-2 · HY-4 · HY-5   (disjoint; any order)
5.  DM-1 · DM-2                 (after tier (B) drafts land)
6.  DM-4                        (cloud; harvest, no merge — it writes no tree file)
7.  HY-1                        (after A4 harvest AND DC-1 merged)
8.  HY-3                        (after A1 + A2 harvest)
```

## THE JOURNAL ANCHOR IS FORCED, NOT OPTIONAL

DM-4 runs on `claude/`, which `LANE_BRANCH_RE` cannot match, so `check_journal_spine_anchor`
sees its merge as unanchored and the queue wedges. **Pre-anchor:** commit a real artifact on a
branch, then a JOURNAL entry naming that artifact's SHA **plus every lane branch tip SHA**, and
merge that `--no-ff` FIRST. The batch carries **two JOURNAL entries, not one** — said here
rather than discovered. Never reach for `SKIP=audit-health` when the flagged merges are ours.

## REFUSE-TO-FINISH

The batch does not close while any item is open: every lane merged or explicitly abandoned with
a reason, every worktree removed AND its removal verified, every branch deleted **locally and on
origin**, tier (A) and DM-4 harvested, and the close packet landed at the `closed_by:` path
above. Removing this manifest's `status: open` before that is closing the batch by assertion.

---

# ORCHESTRATION-STATE NOTE — 2026-09-01, appended for a fresh orchestrator seat

> **In-file amendment marker** (CLAUDE.md §5 rule 3), appended on operator instruction so a
> replacement seat boots from the manifest rather than from a chat. Everything above this line
> stands as frozen at dispatch.
>
> **THIS NOTE IS UNCOMMITTED AT THE MOMENT OF WRITING.** The operator's stop order was
> "commit nothing new, merge nothing", so it is on disk in the working tree and not in git.
> First act of the next seat: read it, then decide whether to commit it.

## 1 · Batch-E lane states — 13 of 15 MERGED, 14 of 15 RESOLVED

```
DC-1   lane-a-1-vision-to-readme                 MERGED   ea1e32a9
DC-23  lane-b-2-essentials-and-claude-md         SPLIT    -- see §2, the live item
DC-4   lane-c-3-root-contract                    MERGED   1a3c378b
DC-5   lane-d-4-ai-council-instantiation         MERGED   76f184fb   << needs anchor, §3
DM-1   lane-e-5-eval-sda1-harbor                 MERGED   (reviewed pre-merge, 2 findings)
DM-2   lane-f-6-observability-otel               MERGED   (reviewed pre-merge, 1 HIGH fixed)
DM-3   lane-g-7-typed-multi-layer-graph          MERGED   7b0cbf14
DM-4   lane-h-8-local-memory-tier-l-evaluation   HARVESTED (cloud; owes no merge)
DM-5   lane-i-9-distiller-filing-amendment       MERGED   bea4c623
DM-6   lane-j-10-equilibrium-checkpoint          MERGED   b7fef9b9
HY-1   lane-k-11-derived-doc-freshness           MERGED   9b736ce2
HY-2   lane-l-12-logs-retention-rule             MERGED   1c92024f   << needs anchor, §3
HY-3   lane-m-13-templates-disposition           MERGED   4bc754b4
HY-4   lane-n-14-trends-burndown-and-quota-panel MERGED   720d3e09
HY-5   lane-o-15-wintooling-local-default        MERGED   32d19df (in win-tooling)
```

Hub worktrees: **only DC-3's** (`.claude/worktrees/lane-b-3-claude-md-genre`). All other lane
worktrees and branches are torn down, locally and on origin.

## 2 · DC-3 — ADJUDICATED PARTIAL ACCEPT, awaiting the split. THE LIVE ITEM.

Branch `worktree-lane-b-3-claude-md-genre`, single commit **`6f226b34`**, 9 files, +77/-223.
**Not merged. Do not merge as-is.** Operator adjudication 2026-09-01:

- **ACTS TWO + THREE — ACCEPTED.** Reconstruct them ALONE on a fresh branch from `6f226b34`, or
  revert Act One's hunks on the lane branch. Content: the CLAUDE.md genre changes, both
  ObsidianVault deletions, the dropped VISION lines, and the PLAYBOOK relocations of the
  branch-prefix / TUI rationale. **Merge that with a terra review and its tally.** VISION.md then
  leaves the root per DC-1's archival.
  - **CAUTION, measured 2026-09-01 and not yet re-tested after the split:** moving `VISION.md`
    out of the root made `audit.py health` exit 1 on `vision_md: VISION.md absent at repo root`
    (a FAIL, so it refuses every commit in the repo) and REDded
    `test_gen_handoff_still_extracts_the_live_vision_section`. Re-measure before relying on the
    archival step; if it still blocks, the archival is a separate act from Acts Two + Three.
- **ACT ONE — NOT MERGED** (the ESSENTIALS deletion, the floor-template edit, ~20 PLAYBOOK
  citation fixes, the "How Claude thinks" relocation). It contradicts ruling 1 — DC-2 is now
  `[#628]`, fleet-coupled — and leaves the tree deploy-broken: the floor sha256 goes stale against
  its hash-guarded carrier, `release_lint` C5 would FAIL, and `VISION:46` / README references
  dangle. **Preserve the diff as `[#628]`'s INPUT ARTIFACT**: its guard-tracing research narrows
  that arc's scope from A3's ten breaking consumers to the measured set. The arc lands it with
  RELOCATION (not deletion), sha regeneration, C5 green, the consumer HUB-region handled, and
  sequenced with v1.5.0.

## 3 · PENDING ANCHORS — do this BEFORE any further merge

`journal_spine_anchor` reports **four** unanchored first-parent spine entries on `main`:

```
13fb1538   1d814abc   1c92024f   76f184fb
```

DC-3's own commit rode a `SKIP=audit-health` citing this gap as pre-existing. **Operator ruling:
verify that cause and ANCHOR these four FIRST — no further merge rides on a skipped health gate.**
Anchor by landing a JOURNAL entry naming commits these merges INTRODUCED (never the merge SHAs
themselves — a merge cannot name its own hash; see PLAYBOOK's night-batch chapter, "the anchor
tail is a two-commit problem").

## 4 · UNCOMMITTED WORK ON DISK — two places

1. **This note**, in this file.
2. **`win-tooling`, branch `docs/canonical-restamp-2026-09-01`** — the attended stamp lane
   (ruling 6) is DONE but ITS COMMIT NEVER LANDED. `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md` and
   `BACKLOG.md` are modified in the working tree. All three docs were re-read end to end
   (83 + 126 + 444 lines), stamped `last_reviewed: "2026-09-01"`, and carry a review-record
   blockquote naming what the read found; the drift is filed as win-tooling `[#8]`.
   **`canonical_freshness` PASSES and `toc-freshness` PASSES** (the latter needed TOC markers that
   had never existed — a second pre-existing wedge, fixed not bypassed). The commit was refused by
   **`codemap-freshness`**, which is the third wedge in that repo and is NOT yet diagnosed.
   A prepared commit message is at `~/.claude/jobs/0ccc13f1/tmp/` — but that job dir is deleted
   with the job, so re-author rather than rely on it.

## 5 · OPEN ASKS AND FILED DEFECTS

**Two integrator defects, ruled 2026-09-01, NOT yet filed as rows:**
- **(a)** The "contract-amendment form" left a ruled-out act EXECUTABLE. DC-3 was dispatched by
  appending an amendment saying "do not perform Act One" to a contract that still CONTAINED Act
  One — and the lane performed it. **A split ruling must REISSUE the contract through the
  validator**, not annotate it.
- **(b)** Slug renumbering between draft and dispatch (`lane-b-2-…` in the manifest vs
  `lane-b-3-…` dispatched). **The manifest's lane enum and the contract slug must match at
  freeze** — this belongs as a predicate.

**Blocked / owed elsewhere:**
- `[#276]` is **`status: deferred`** and gates BOTH consumer instantiations — neither ruff-gate
  divergence is drift (both declared, ai-council's ruled 2026-07-12); the deploy tool simply does
  not read the waivers. See `docs/audits/2026-09-01-technical-ruff-gate-divergence-classification.md`.
- **v1.5.0: NOT to be tagged** until the round-2 §5 checklist is witnessed (operator).
- Batch-E **close packet** is deliberately ABSENT (`closed_by:` above), which keeps the ADR-110
  exemption armed. It owes the six pre-merge tallies; the post-merge round is at
  `docs/audits/2026-09-01-verification-batche-post-merge-terra-round.md`.
- **BATCH-F** seeds F0–F7 are specified in the operator's 2026-09-01 message and not yet derived.

## 6 · Where the window's own record lives

`docs/audits/2026-09-01-technical-night-window-report.md` — the window report against N1–N9, with
four in-file amendments. `JOURNAL.md` carries entries 2026-08-31 (m) through 2026-09-01 (q).
