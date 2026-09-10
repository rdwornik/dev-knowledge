---
batch: W
seq: 1
shape: ADR-110 — ONE plan -> N file-disjoint lanes -> ONE integrator. Seven contracts were cut by the browser architect seat in BATCH-2026-09-10-W-CONTRACTS.md; SIX are committing lanes and are frozen here, and the seventh (W-5) is a primary-session act rather than a lane. Four dispatch on the operator's GO of 2026-09-10 (W-1, W-2, W-7 local; W-3 codespace); one (W-4) dispatches on the same GO under its `GO delete` clause; one (W-6) is HELD at dispatch on a named, checkable condition recorded below. Lane count is six either way — a held lane is a frozen lane that has not fired, not a dropped one.
dispatched: 2026-09-10
status: open
closed_by: docs/audits/2026-09-11-technical-batch-w-close-packet.md
substrate: MIXED, and cut per lane rather than assumed — PLAYBOOK Ch8 "Layer 1" applied to each lane with the first firing question recorded in its contract. THREE lanes are LOCAL at Q2 (W-1 reads a file that exists only in the operator's prompts dir; W-2 needs a smoke against a vendor CLI authenticated on the operator's disk; W-7's Done-when reads unpushed local lane branches). THREE fall to Q4 and are CODESPACE (W-3, W-4, W-6). AW-4 binds all three codespace lanes: the receipt is a RED list, never a verdict, and the acceptance verdict is re-derived by the integrator on the Windows primary before merge (FR-8).
---

# BATCH W — THE 2026-09-10 BATCH · THE MANIFEST

**This file is the gate-readable manifest**, committed AT DISPATCH and before any lane boots.
`scripts/batch_manifest.py` resolves an open batch as the conjunction of four facts: the manifest is
TRACKED, `status: open`, `closed_by:` names a shape that CAN resolve, and that path is ABSENT from
the tree. All four hold at the time of writing.

Authorization: the operator's GO of 2026-09-10, recorded verbatim under "PROVENANCE" below. The
frozen intent set is `to-cc/BATCH-2026-09-10-W-CONTRACTS.md` (51,581 B), amended in place by
`to-cc/AMEND-BATCH-W-001.md` (AW-1..AW-4), `to-cc/AMEND-BATCH-W-002.md` (AW2-1..AW2-4) and
`to-cc/AMEND-BATCH-W-003.md` (AW3-1..AW3-3), the last of which the operator's GO names explicitly as
applied. The dispatcher's step-0 evidence is `to-browser/SESSION-dispatcher.md`.

**`<BATCH-ID>` = `W` and `<L>` = `w`, filled ONCE at step 0.** Batch letter == lane letter follows
the E/F/G/T/U/V precedent.

## THE LANES — 6 frozen committing lanes

Contracts: `docs/audits/2026-09-10-technical-batch-w-launch-contracts/`, byte-identical to the six
dispatched from the prompts dir root (SHA-256 verified at dispatch).

```
W-1  lane-w-000-harness-is-process-intake  DISPATCH  local      opus  execute  no row  DECLARE-HARNESS-IS-PROCESS lands as an intake; ZERO diff under docs/audits/
W-2  lane-w-684-pretooluse-guard-root      DISPATCH  local      opus  plan     #684    the PreToolUse guard resolves its own repo root; matcher narrows off "*"
W-3  lane-w-638-proof-layer-skipif         DISPATCH  codespace  opus  plan     #638    four proof_layer guards ruled on their merits, or a skipped proof reads NOT-PROVEN
W-4  lane-w-683-override-manifest-node     DISPATCH  codespace  opus  plan     #683    the /override manifest node and its payload leave together   [GO delete]
W-6  lane-w-687-execution-position-spine   HELD      codespace  opus  plan     #687    four spine keys in tasks/ frontmatter, each written by mechanism   [WAITS on W-3 + W-7]
W-7  lane-w-278-impacted-test-selection    DISPATCH  local      opus  plan     #278    a changed file selects its tests; a commit selecting none is REFUSED
```

> This fence is a **machine surface**, not prose: `batch_manifest.manifest_lane_slugs` reads the
> FIRST `## THE LANES` block and stops at the next heading, and
> `batch-manifest-contract-slug-agreement` ([#630]) requires **set equality both ways** between these
> slugs and the launch-contracts directory. Both sets are 6. A lane recorded outside this fence is a
> lane the teardown and the ADR-110 exemption cannot see. Nothing else in this block may carry a
> slug-shaped token — the provisioning branch for this manifest is therefore named below the next
> heading, not here, because the parser would read it as a seventh lane.

## THE MANIFEST BRANCH

This manifest was written in a linked worktree off `main` at `1c27ad4f` and merged `--no-ff`, per
core-invariant #5 and the standing operator order MERGE IS ATOMIC. The batch-opening manifest merge
takes **no ADR-110 lane exemption** — it is a normal gated merge and was gated as one.

## W-5 IS NOT A LANE, AND THAT IS WHAT KEEPS THE BATCH AT THE CEILING

AW-3 reshaped W-5 to the three SUPERSEDED OneDrive hook copies under `~/.claude/hooks` — **outside
the repo, operator global config**, executed by the primary session after the deletion GO rather
than as a worktree lane. AW2-2 states the consequence verbatim: *"Batch W is at the ADR-110 ceiling:
committing lanes W-1, W-2, W-3, W-4, W-6, W-7 (six); W-5 is a primary-session act, not a lane."*
The first render's closing claim that this batch "cannot take a seventh lane" is therefore
**superseded, and recorded as superseded** rather than swapped out.

The operator's GO sequences it: *"W-5 is a primary-session act after the lanes are dispatched."*
`scripts/setup-fleet-scheduler.ps1` is **HELD, not deleted** — open `[#493]` references it (AW-3).

## W-6 IS HELD, AND THE CONDITION IS CHECKABLE

W-6 does **not** boot on `GO W`. Its condition is that **W-3 AND W-7 are MERGED** — read off `main`'s
first-parent spine, not off the existence of a branch, because a branch that exists proves only that
a lane started.

A7-1 set the original condition — *"`skipped_gates`' writer is W-3's output → W-6 dispatches after
W-3 merges"* — and AW3-1 **adds W-7 ahead of it**. Both W-6 and W-7 can register a commit-time hook
in `.pre-commit-config.yaml`, so they are serial; AW3-1 rules which goes first (see the next
section). W-6 booted early would have no writer for one of its four keys and would have to invent
one, which its own contract forbids.

## THE ONE DISPATCHER RULING — W-7 BEFORE W-6, AND THE FROZEN BODY SAYS THE OPPOSITE

W-7's frozen section carries, verbatim, *"So: W-7 dispatches after W-6 merges"*, with a full
collision analysis behind it. **AMEND-BATCH-W-003 AW3-1 reverses exactly that call.** It is later
than the batch render, it is titled *"pre-dispatch: W-7 before W-6"*, and it engages the same
collision fact rather than overlooking it: *"Both edit `.pre-commit-config.yaml`, so they are serial;
W-6 already waits for W-3's merge and W-7 depends on nothing."* The later amendment addressing the
same question governs, and the operator's GO names AW3 as applied.

**The collision is unchanged — only which lane takes the `.pre-commit-config.yaml` slot first.** The
frozen bodies are carried into the contracts **UNEDITED**, so the supersession is visible in each
contract rather than silently swapped; each carries a `## Sequencing` section naming which text is
live. If W-6 takes the follow-up-commit-on-merge path its footprint clears `.pre-commit-config.yaml`
entirely, and the integrator may then run them concurrently — his call on a witnessed footprint, not
this manifest's on a predicted one.

## TWO VERB DEFECTS FOUND BY THE STEP-0 DRY RUN, WHICH IS WHY IT IS A REFUSAL

AMEND-BATCH-V-002 §1 made the DryRun of every generated contract the last line of step 0 because
batch V froze six contracts the live verb refused. **It fired again here, twice.**

- **The contracts were written to the wrong directory.** `Dispatch-Lane` resolves a bare filename
  against the prompts dir **ROOT**; the generator had written them to `to-cc/`, which is the
  DECLARE/AMEND/BATCH transport surface. All six REFUSED on the first pass. They were relocated to
  the root — where batch V's and batch U's contracts live — and all six then resolved.
- **`dispatch <FILE.md>` is the wrong verb for a generator-emitted contract.** AW3-1 names
  *"`dispatch` for W-1, W-2, W-7"*, but `dispatch` executes a `## Dispatch` fence **verbatim** and
  refuses any head that is not `claude`; the generator's `local` shape emits `Dispatch-Lane`. The
  live verbs are `Dispatch-Lane` and `Dispatch-Codespace`, which is what the generator carries and
  what the DryRuns proved. Recorded because the amendment and the organ disagree, and the organ is
  the one that runs.

**Had step 0 skipped the DryRun, six frozen contracts would have been handed to a verb that refuses
them** — the freeze already spent, exactly as the refusal's docstring predicts.

## THE STEP-0 REFUSALS — four, all PASS, all before the first worktree existed

`scripts/seat_refusals.py`, per SEAT-BOOT-dispatcher §2:

```
lane-ceiling --check-worktrees   PASS  6 lane(s) <= 6, checked before any worktree existed
carried-by (batch-W population)  PASS  5 of 5 file(s) governed and carried
sleeping-poll                    PASS  3 declared wait(s), each interval + bound + predicate
dryrun-step0                     PASS  6 of 6 contract(s) DryRun on the last line of step 0
```

## THE STEP-0 SHIP-GATE — hard-fail 0

`uv run --locked python scripts/audit.py health` at `1c27ad4f`: **`health: OK`**, zero hard failures.

**One WARN class this batch GROWS, recorded here rather than discovered by a lane.**
`consumer_at_landing` warns per unconsumed `LANE-*.md` under `docs/audits/`, and the six contracts
this manifest is required to carry in-tree ([#630] set equality) each add one. Batch V's eight
contracts sit in the same list. **This matters to W-4 specifically:** AW2-3 makes W-4's acceptance
*"ship-gate back to <= 45 undispositioned"*, and that target must be read against the count as this
manifest leaves it, not against the pre-dispatch count. The growth is structural to the gate that
requires the copies, not a defect the lane introduced.

## THE COUPLING SCAN — footprints, and the one real serialization risk

Footprint disjointness is recorded in the frozen contracts. Two couplings are live:

- **`.pre-commit-config.yaml` — W-6 and W-7.** Serial. AW3-1 rules W-7 first (above).
- **`tasks/` — W-1, W-5 and W-6.** W-1 and W-5 each ADD one row (a new file plus one
  `tasks/manifest.json` node); W-6 edits **frontmatter across existing rows**. File-by-file the
  footprints are disjoint so G2 does not serialize them, but all three regenerate `BACKLOG.md` and
  all three touch `tasks/manifest.json`. **The integrator merges W-6 LAST of the three** and re-runs
  `gen_task_tree.py --emit-source` on the merged tree; a lane that regenerates against a tree missing
  a peer's row silently drops it.

## WHAT THIS BATCH DOES NOT TOUCH

Recorded in the frozen intent set under "Not in batch W" and not restated here. Two items are
carried forward as **owed acts rather than lanes**:

- **AW2-4, the teardown.** *"`.claude/worktrees/review-consumption` and branch
  `docs/review-consumption-2026-09-10` (local and origin) are removed by the integrator once the
  session holding it (PID 12628) is closed."* At dispatch the worktree is gone and the branch
  `worktree-review-consumption` is still live locally. It is an open item on the integrator's
  refuse-to-finish list until it is done.
- **The M03 leg-1a re-run** goes to batch X per A7-2, which supersedes AW-5 expressly, on the ground
  that it moves no metric.

## PROVENANCE

Operator GO, 2026-09-10, verbatim:

> *"GO batch 2026-09-10-W per to-cc/BATCH-2026-09-10-W-CONTRACTS.md with to-cc/AMEND-BATCH-W-003.md
> applied. First wave now: W-1, W-2, W-7 via Dispatch-Lane (the generator-carried lines); W-3 via
> Dispatch-Codespace. GO delete: W-4 via Dispatch-Codespace now; W-5 is a primary-session act after
> the lanes are dispatched. W-6 dispatches only after W-3 and W-7 are merged; its CODESPACE cut
> stands. Commit the dispatch half of the manifest to
> docs/audits/2026-09-10-technical-batch-w-manifest.md before any lane boots. Report the resolved
> launch lines and receipts."*

That GO settles the one open routing question the dispatcher had flagged: AW3-1 lists W-6 under
`dispatch` (local) while its frozen body cuts it to CODESPACE at Q4 with AW-4 in full. **The
operator ruled the CODESPACE cut stands**, so the frozen body governs and the amendment's verb list
is an incidental listing rather than a re-cut.

Contracts frozen by `scripts/gen_lane_contract.py emit` — the launch line is carried by the
generator per substrate, never composed at the seat — with each lane's body spliced in **verbatim**
from the batch render. All six pass `gen_lane_contract.py check`.
