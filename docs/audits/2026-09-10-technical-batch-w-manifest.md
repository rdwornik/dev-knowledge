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
W-7  lane-w-278-impacted-test-selection    DISPATCH  local      opus  plan     #278    a changed file selects its tests; a commit selecting none is REFUSED
W-8  lane-w-000-three-decisions-become-rows DISPATCH local      opus  execute  no row  three ruled decisions become rows, sources quoted verbatim   [MERGES FIRST]
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

## AMENDED AFTER DISPATCH — W-6 OUT, W-8 IN, ON AN ARCHITECT RULING

**This amendment is marked rather than silent, because a manifest is an immutable audit and its
lane fence is a machine surface.** The section below it ("W-6 IS HELD") is the text this amendment
supersedes; it is **kept, not swapped out**, so the supersession is visible.

`AMEND-BATCH-W-004` proposed **W-8** — three ruled decisions filed as rows — with the note *"W-8
fits under the ADR-110 ceiling while W-6 is held."* **The ceiling organ refused it, verbatim:**

```
REFUSED [lane-ceiling]: the plan names 7 lanes against a ceiling of 6; the excess is
lane-w-000-three-decisions-become-rows -- hand the excess back to the plan -> they are the next
batch's opening rows; the batch does not proceed until the plan is re-cut to <=6 (the bound is
integration capacity, which is serial)
```

**A held lane still counts**, and AW2-2 is what settles it — it enumerates the six as *"W-1, W-2,
W-3, W-4, W-6, W-7"*, W-6 among them. The dispatcher refused rather than dispatching a seventh and
reporting the number afterwards, which is the move the ceiling exists to forbid.

**The architect's ruling of 2026-09-11 re-cut the plan** rather than waiving the ceiling: *"W-6 moves
to batch X; W-8 is admitted in its place under the ceiling — record this in the manifest's dispatch
half, then dispatch W-8 and mark it first in the integrator's queue."*

- **W-6 leaves batch W** and its contract leaves `docs/audits/2026-09-10-technical-batch-w-launch-contracts/`,
  because `[#630]` requires **set equality both ways** between that directory and the fence above — a
  fence row removed without the file is a refusal at the next commit. `[#687]` is untouched and
  unclosed; the lane is re-frozen in batch X, where its A7-1 dependency on W-3's `skipped_gates`
  writer is satisfied by a merged W-3 rather than waited on. The contract as frozen here survives at
  the prompts dir root.
- **W-8 enters in its place**, and **merges FIRST, before any other W lane** (AW4-1). Its contract
  carries one correction the dispatcher's preflight found: AW4-1 row 1 cites *"RATIFICATION-2026-09-10
  D2"*, and `to-browser/RATIFICATION-2026-09-10.md` carries **no D2** — the Drive-style duplicate
  `to-browser/RATIFICATION-2026-09-10 (1).md` does. The contract names the path that holds it.
- **Row-id collisions are refused at merge and returned to the LATER lane, never renumbered**
  (AW4-2). Four surfaces now touch `tasks/`: W-1, W-5, W-8 — and W-6 is gone, which removes the
  frontmatter-across-existing-rows writer that made the three-way `tasks/` coupling the batch's one
  real serialization risk.

**The count after the re-cut is six: W-1, W-2, W-3, W-4, W-7, W-8.** The ceiling is satisfied by
arithmetic, not by exception.

## W-6 IS HELD, AND THE CONDITION IS CHECKABLE — SUPERSEDED BY THE AMENDMENT ABOVE

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

## AMENDED AFTER DISPATCH — W-3 AND W-4 RE-CUT LOCAL, BECAUSE THE CODESPACE CUT PRODUCED NOTHING

**Marked rather than silent**, on the same ground as the W-6/W-8 amendment above: a manifest is an
immutable audit, so the frontmatter `substrate:` block and the `## THE LANES` fence are **left
exactly as dispatched** and this section is where the change lives. Both still read `codespace` for
W-3 and W-4, deliberately — they record what was frozen and dispatched on 2026-09-10, which is what
a dispatch-half record is for, and no gate reads either surface for a substrate token
(`batch_manifest.manifest_lane_slugs` reads the fence for SLUGS only, and `check_substrate_declaration`
reads the CONTRACTS, not this file). A reader who needs the live substrate reads this section.

**Authority:** AW5-3, `to-cc/AMEND-BATCH-W-005.md` (2026-09-11), carried by this manifest. The
re-dispatch is the operator's act of 2026-09-11, which also ordered the substrate change and its
reason recorded here.

### The reason is the receipt of the first cut, not a preference

W-3 and W-4 fell to Q4 and were frozen CODESPACE. Both were dispatched as codespace lanes on
2026-09-10 and **both produced ZERO WORK.** That is measured, not inferred — at re-dispatch:

- neither `worktree-lane-w-638-proof-layer-skipif` nor `worktree-lane-w-683-override-manifest-node`
  existed in `git branch -a`, and neither existed in `git ls-remote --heads origin` (the remote was
  read live rather than off a cached `origin/` ref);
- both containers were `Shutdown` — `lane-w-638-proof-layer-skipif-54r7jgp544p27w7g`, last used
  `2026-09-11T00:36:08+02:00`, and `lane-w-683-override-manifest-pgw54jq97xr37gqp`,
  `2026-09-11T00:37:35+02:00`.

**Q1 makes LOCAL admissible; the zero-work outcome makes it the choice.** PLAYBOOK Ch8 Layer-1 Q1
routes a gate-dependent result away from cloud to *"codespace or local"* and does not pick between
them, so Q1 alone cannot re-cut a lane — AW5-3 says exactly that (*"Q1 admits local for
gate-dependent lanes; the codespace cut produced zero work"*). Both Done-whens are gate-dependent:
W-3's turns on four `proof_layer` guards and a skipped proof reading NOT-PROVEN, W-4's on
`release_lint`. On the operator's Windows primary those gates are armed, which is the property the
container run failed to convert into work.

**The defect is filed, not absorbed.** AW5-3 files the codespace zero-work class — a detached long
lane, the known residual risk — as a row at batch close. This section records the substrate change;
it does not diagnose the container.

### What AW-4 keeps and what it loses

AW-4 bound all three codespace lanes to *"the receipt is a RED list, never a verdict, and the
acceptance verdict is re-derived by the integrator on the Windows primary before merge (FR-8)"*.
On a local lane the **receipt half has no subject** — there is no container, no ssh transport and no
`receipt.json`. **FR-8 is untouched**: the integrator still re-derives each acceptance verdict on
the primary before merge, and for these two lanes that re-derivation is now the only verdict there
ever was rather than the second of two. AW-4 still binds W-6 in full, which stays CODESPACE in
batch X.

### The launch lines are the generator's, and the freeze is intact

The two lines were read out of `gen_lane_contract.dispatch_command(slug, file, 'high', 'local')`
rather than composed at the seat — the same rule the dispatch half already records (*"the launch
line is carried by the generator per substrate, never composed at the seat"*). Recorded here as a
**receipt**, not as a launch site; PLAYBOOK Ch8's dispatch table remains the sole literal-command
site and `dispatch_drift`'s corpus is that section alone.

```
Dispatch-Lane lane-w-683-override-manifest-node LANE-w-683-override-manifest-node.md -Effort high
Dispatch-Lane lane-w-638-proof-layer-skipif LANE-w-638-proof-layer-skipif.md -Effort high
```

Both were `-DryRun` first, per AMEND-BATCH-V-002 §1 — the same discipline that caught this batch's
two verb defects at step 0. Both DryRuns resolved their contract against the prompts dir ROOT and
derived the branch the pairing line names.

**The contracts were NOT reissued**, and that is why the substrate change reaches the lanes as an
amendment. Both frozen files still declare `**Shape:** codespace` and carry their receipt-gate
section, and both are still **byte-identical** to their in-tree copies — SHA-256 verified at
re-dispatch, `A5A8458C…` for W-3 and `0D939E97…` for W-4. `[#630]` set equality is therefore
undisturbed and the six-row fence is unchanged.

**The pairing line survives the re-cut untouched**, which is the one thing that makes an amendment
sufficient here: a codespace lane and a local lane commit on the **same** `worktree-` prefix (R-ENUM
leg 3), so each lane's branch is exactly what its contract names and no teardown or ADR-110
exemption has to learn a new name.

**One drift this leaves standing, named rather than fixed.** `check_substrate_declaration` reads the
contracts, which still declare `codespace`, so for these two lanes the audit's substrate reading
now describes the frozen cut and not the live one. Editing an immutable frozen contract to silence
that would cost the freeze and the `[#630]` byte-identity above; it is recorded here as a known,
bounded disagreement between a frozen declaration and a later amendment — the same shape as this
file's W-7 sequencing ruling, where the frozen body says the opposite of what governs.

### A TRANSPORT DEFECT THE RE-DISPATCH FOUND, because the receipts are incomplete without it

`Dispatch-Lane`'s **third positional argument silently does not arrive.** PLAYBOOK Ch8 documents it
as *"an amendment appended without reissuing the contract"* — precisely the mechanism a substrate
re-cut wants — and `DispatchHelpers` v1.6.0 `Start-DispatchLane` builds the prompt as
``"$prompt`n`n$Extra"``. The `claude` launcher is a `.cmd` shim, and the argument is **truncated at
that first newline** on the way through it, so the session receives the pointer sentence and nothing
else. Measured on both lanes, off their own transcripts: W-4's first user message is 106 characters
and W-3's is 102 — each exactly `Read and execute the frozen contract at <path>`, with a 2,016-byte
and a 1,432-byte amendment dropped. It is not a quoting error at the seat: the second attempt passed
a **single-line** `Extra` with no angle brackets or shell metacharacters and was truncated
identically, because the module's own `` `n`n `` join is what the shim cuts at. Both dispatches also
print a stray `'m' is not recognized as an internal or external command` — the tail of the same
re-parse, which appears whether or not the `Extra` contains a newline.

**Both amendments were delivered out of band instead**, by cross-session message to the live lane
sessions (`f3df87fa` for W-4, `af33ba9b` for W-3), each while the lane was still in its first turn
and before it had acted on the superseded sections. The delivery is therefore on the record here
rather than in the dispatch line, and **the dispatch line above is an honest record of what was
typed, not of what the lane read.** A seat relying on the third positional for anything load-bearing
is relying on a mechanism that does not work on this machine.

## AMENDED AFTER DISPATCH — THE THREE 2026-09-11 DISPATCHES: A W-2 FIX LANE AND TWO BATCH-X PREPARATORY LANES

**Marked rather than silent**, same ground as the two amendments above. The frontmatter and the
`## THE LANES` fence are again **left exactly as dispatched**: none of these three adds a fence
row, and none adds a launch contract to
`docs/audits/2026-09-10-technical-batch-w-launch-contracts/`. `[#630]` set equality therefore
still holds at six both ways, and the ADR-110 ceiling is still satisfied by arithmetic. The
reasons differ per lane and are stated below, because "it did not change the fence" is a
different fact for a resumed lane than for a lane of the next batch.

**Authority:** the operator's dispatch of 2026-09-11; AW6-2 for the W-2 fix lane. All three are
LOCAL, all three were launched from generator-carried lines, and all three were DryRun first.

### W-2 fix — the SAME lane resumed, on its own branch, and the ruled verb refuses that

AW6-2 is the "else" branch of AW5-2 (*"otherwise HELD and a fix lane is dispatched"*) and
requires the work *"on W-2's branch `8634f5f6`"*. That requirement and the ruled verb are
incompatible, and the incompatibility is by design rather than a defect:

- the generator-carried local line is
  `Dispatch-Lane lane-w-684-pretooluse-guard-root LANE-w-684-pretooluse-guard-root.md -Effort high`,
  and its DryRun returned
  `[lane] SKIP -- branch 'worktree-lane-w-684-pretooluse-guard-root' already exists; not dispatching a second lane.`
  Guard 1 exists so a second lane cannot collide with a live one; it is correct here and was not
  worked around.
- `claude --worktree` only ever **creates** a worktree (`--worktree [name]`: *"Create a new git
  worktree for this session"*), so **no ruled verb can target an existing branch.**

So the transport is the PLAYBOOK's documented fallback — the same argument set
`Start-DispatchLane` builds, minus `--worktree`, with cwd set to W-2's existing worktree —
and the deviation is recorded here rather than left in a terminal. **The alternative was refused
on two counts:** a new slug mints a new branch, which is (a) not "W-2's branch" and (b) a seventh
slug in a batch at the ceiling, which the ceiling organ refuses while handing the excess back to
the plan. Reusing W-2's slug and branch keeps the count at six and adds nothing to the fence —
this is one lane resumed, not a new one. Its frozen contract is untouched and still governs the
work already on `8634f5f6`; the fix contract governs only what remains.

**AW6-2's stated premise is FALSE, and the correction is carried into the fix contract rather
than silently worked around.** AW6-2 says *"generated from the integrator's W-2 review tally:
resolve the unresolved HIGH"*. There is no such tally and there is no unresolved HIGH on W-2,
because **no review of that branch was ever run.** From `to-browser/SESSION-integrator.md`: the
queue line reads `W-2 … @ 8634f5f6 code EXIT 1 HELD review=NONE`; the refusal reads *"code branch
carries no `review=` token"*; §9 records that W-2's artifact carries *"no reviewer tally of any
kind"*; and §10 is titled *"W-2 CANNOT CLEAR ITS HOLD — its session is dead"*, stating *"I did not
run the reviews myself. D-1 makes review a LANE act."* §10 leaves three ways out to the operator
— authorise an integrator-run review as a deviation, re-dispatch the lane to review its own
branch, or close with W-2 held and `[#684]` unlanded. **The 2026-09-11 dispatch chose the
second.** The lane therefore PRODUCES the review that never existed rather than resolving
another seat's findings, and the fix contract instructs it not to manufacture a HIGH to match the
amendment's wording. AW6-2's merge condition is the operative one and is forward-looking:
*"Merges only on a fresh Codex review with no unresolved HIGH."*

**One Done-when leg may remain externally blocked, and that is named up front rather than
discovered.** The A7-6 / M7 smoke is non-vacuous only against a reader that HONOURS
`.claude/settings.json`. W-2 measured the honour-set on this machine as exactly
`{cursor-agent}` — `codex` and `copilot` were measured NOT to honour it, so they read straight
through the broken hook and are vacuous instruments rather than passing ones — and `cursor-agent`
was authenticated but usage-limited. At this dispatch it is still installed at
`2026.09.08-6caf4ff`; **its quota was deliberately not probed, so as not to spend the one budget
the lane needs.** The fix contract orders a fail-fast probe as step 1 and admits a re-measured
external block as a legitimate outcome, without weakening the clause.

### X-0 and X-R — batch X's preparatory lanes, recorded here because this is the live manifest

Neither is a batch-W lane. They are recorded in this file because it is the open manifest at
their dispatch and the operator ordered all three recorded together; **they merge AFTER batch
W**, by that same instruction. `gen_lane_contract.py check` confirms the separation
mechanically: *"contract-manifest predicate ([#630]): 2 contract(s), none in this repo — 0
checked"*. Both contracts pass the shape gate at `shape local` with the slug, branch and command
agreeing.

- **X-0 `lane-x-000-batch-x-roster-lands`** — TEXT-ONLY. Lands
  `to-cc/DECLARE-BATCH-X-ROSTER-2026-09-11.md` with `AMEND-BATCH-X-ROSTER-001` (which FREEZES the
  roster) and `-002` applied, as `docs/intake/2026-09-11-tech-batch-x-roster.md` at
  `intake-id: 92` (`91` is the highest present), files every NEW row with its Done-when as
  written and an `implements:` key pointing at that intake, and regenerates `BACKLOG.md`.
- **X-R `lane-x-000-window-rules-land`** — TEXT-ONLY. Writes
  `to-cc/DECLARE-WINDOW-RULES-2026-09-11.md` sections A and B into
  `protocols/STANDING_RULINGS.md` as ONE new dated section — **`AH`**, the file running A…AG —
  fold-first, a rule already in the repo cited rather than duplicated; section C's two close acts
  become rows.

**AMEND-BATCH-X-ROSTER-002 is downstream of this batch's own reporting.** AX2-1 corrects X1-6's
premise — A7-1's *"`skipped_gates`' writer is W-3's output"* was narrower than it read, because
W-3 produced a per-guard IDENTITY (`Guard.key = module::target`) and not a writer callable — so
X1-6 now builds the writer itself with W-3 as a dependency. The gap was raised by W-3 at handback
and reported before X was cut, which is the sequence the re-cut to LOCAL made possible.

### The one real serialization risk, removed by construction rather than left to the merge

X-0 and X-R **both** file rows, both touch `tasks/manifest.json` and both regenerate
`BACKLOG.md`, while running concurrently on separate branches. A row-id collision is refused at
merge and returned to the LATER lane, never renumbered (AW4-2) — so a collision costs that lane
its work. Two things are therefore frozen in the contracts rather than discovered:

- **Reserved, disjoint id blocks.** X-0 takes `693` upward and is barred from passing `719`; X-R
  takes exactly `720` and `721`, and a third id is a fork it must report rather than take. `692`
  is the highest id live anywhere — verified across the working tree and both unmerged lane
  branches at dispatch.
- **The regeneration overlap is the integrator's, and is declared owed rather than pre-empted.**
  Each lane regenerates correctly for its own base; neither regeneration is expected to survive
  the second merge. The integrator merges the two serially and re-runs
  `gen_task_tree.py --emit-source` on the merged tree — the same rule this manifest's coupling
  scan already applies to W-1/W-5/W-6, for the same reason: a lane that regenerates against a
  tree missing a peer's row silently drops it.

Both contracts also carry a step 0 sync to local `main`, because `main` moved twice during this
dispatch arc (W-7 at `e4929b09`, and W-4 completing), and a generator run on a lagging base
drops rows while looking clean.

### Receipts

```
X-0  lane-x-000-batch-x-roster-lands   Dispatch-Lane ... -Effort high   DryRun PASS   session bd507c18   branch up in 10s
X-R  lane-x-000-window-rules-land      Dispatch-Lane ... -Effort high   DryRun PASS   session ab913a89   branch up in 12s
W-2  lane-w-684-pretooluse-guard-root  ruled verb SKIPPED (branch exists) -> fallback  session 9f3e2a90   existing branch @ 8634f5f6, tree clean
```

**Each lane's received prompt was verified off its own transcript**, not assumed from the
dispatch echo: 104, 101 and 105 characters, each exactly the pointer sentence naming the right
contract. No third-positional `Extra` was passed to any of the three — everything they need is in
their contract files — because that positional is silently truncated away on this machine, as the
AW5-3 section above records.

### A FOURTH lane followed — X-C, whose record belongs elsewhere and is noted here only so it is not an orphan

**X-C `lane-x-000-domain-census`** was dispatched later the same day under AX6-1,
`to-cc/AMEND-BATCH-X-ROSTER-006.md`: a read-only domain census, one page per top-level folder,
whose **only** repo write is `docs/audits/2026-09-11-technical-domain-census.md`. Receipt: DryRun
PASS, session `51b95bd4`, branch `worktree-lane-x-000-domain-census` up in 11s, at **`sonnet`**.

**Its carriage is NOT this file.** AMEND-BATCH-X-ROSTER-006 declares
`carried-by: docs/intake/2026-09-11-tech-batch-x-roster.md`, so AX6-1's landed home is the batch X
intake that X-0 is creating, and X-0 was relayed AMEND-006 to fold in. This paragraph exists only
because that intake does not exist yet: a lane dispatched with its record depending on another
lane's success is precisely the orphan class batch X was cut to end, so the dispatch is noted in
the open manifest as insurance and **not** as a claim on this batch. X-C adds no fence row, no
launch contract and no task id.

Two things measured at its dispatch, recorded because both bear on lanes other than X-C:

- **`worktree.baseRef` is unset, so every lane starts on `origin/main`, which is two merges
  behind local `main`** — `3acca581` against `e4929b09` at the time of writing. X-C came up on
  the stale base; X-0 and X-R read `e4929b09` only because their step-0 sync had already run.
  The step-0 sync written into each of these contracts is therefore load-bearing rather than
  belt-and-braces: a generator run on the default base drops rows while looking clean.
- **The generator-carried local line omits the MODEL.** `dispatch_command` emits slug, file and
  `-Effort` only, while `Start-DispatchLane`'s `-Model` defaults to `opus` — so a contract
  declaring `sonnet` dispatched by its own carried line runs at opus, and the line silently
  contradicts the Model row above it. X-C was dispatched with `-Model sonnet` appended. This is
  the same class the generator exists to prevent (its docstring: a lane handed the wrong command
  is worse than a lane handed none, because a wrong command looks authoritative), and it is the
  second gap found in the local dispatch line in one day — the first being the dropped third
  positional recorded in the AW5-3 section above.

`cheapest admitted` resolved to `sonnet` against `ecosystem/provider-registry.yaml`, which is the
admission register: `claude-sonnet-5` is tier `M` with `roles: [subagent-default,
workflow-verifier]`, while **`haiku` has no row there at all** and so is not admitted — cheapest
admitted is not cheapest available.

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
