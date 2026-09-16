---
batch: AB
seq: 1
status: open
closed_by: docs/audits/2026-09-16-technical-batch-ab-close-packet.md
---

# Batch AB — manifest (dispatch half) · 2026-09-16

**Seat:** dispatcher (background, Opus 5) · **Batch:** AB, wave 1 of
`to-browser/PLAN-2026-09-16-execution-order.md` · **Base at fire:** `main` `f746ddf9` plus this
manifest's merge · **Ceiling:** 3 lanes against 6 (`seat_refusals lane-ceiling` PASS).

**This file is committed BEFORE any lane boots.** Batch AA dispatched six lanes with no manifest,
and that single absence produced four task-id reallocations, two quality-register collisions, a
JOURNAL letter collision and an unarmed integration exemption (`[#804]`). A THIRD renumber by the
same defect was found at this batch's step 0 (§5).

**Contracts are pinned by hash, NOT copied in-tree — a recorded deviation from Ch8's in-tree
copy.** They live in the prompts dir; the in-tree copies were written and then REFUSED by
`validate_substrate` rule `substrate-teardown-enum-coverage` (all three: `worktree-lane-ab-*` is
not admitted by `validate_branch_naming.is_lane_branch`). That rule has no manifest-declaration
input, and its commit-time adapter gates every `LANE-*.md` under a launch-contracts directory, so
committing them would need a gate bypass. The refusal is TRUE — these lanes are invisible to batch
teardown and to the exemption until `[#809]` lands — so the honest shape is to pin them here and
land the in-tree copies after lane 2 widens the grammar (§6). Teardown of these three lanes is
therefore MANUAL for the integrator.

| Contract (prompts dir) | sha256 |
|---|---|
| `LANE-ab-808-guard-timeout.md` | `25ece4228dd36439f2b38547e65e827fd765a401e33a4fc2142735ec3ea031d2` |
| `LANE-ab-804-id-allocator.md` | `6e80adff343ecdcbfaa0a70a85da627927e17e05ca55ceb86024aac1484f541f` |
| `LANE-ab-810-substrate-repair.md` | `356f6f4df0f38205f787d7991c07ff472af71b5145a84a451fc574204cbfb00e` |

`dispatch <contract> -DryRun`, run for all three before this commit, resolved each to
`claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree <slug> …`.

---

## 1 · The GO, recorded

Operator ruling in chat, 2026-09-16, on the dispatcher's step-0 halt: **route A (LOCAL), with
corrections.** Quoted where it binds:

> "(a) Retire a07a1f47 and d8c134ee — operator's word, both finished. (b) The operator frees the
> memory. (c) He opens the integrator seat himself from the boot render. (d) Then dispatch, but
> TWO lanes, not four, and add one repair lane, so THREE total"

> "HELD, with reasons stated in the manifest rather than dropped silently"

> "Branch names: WIDEN the pattern, do not recycle a letter."

> "your refusal was right on all three counts: 'Codespace is proven live' was MY premise from a
> lane packet, and the repo cannot read that proof … A proof an organ cannot read is not a proof."

## 2 · The lanes

| # | Lane | Rows | Substrate | Ordered model / effort |
|---|---|---|---|---|
| 1 | `lane-ab-808-guard-timeout` | `[#808]` | LOCAL | opus / high |
| 2 | `lane-ab-804-id-allocator` | `[#804]` `[#788]` `[#809]` | LOCAL | opus / high |
| R | `lane-ab-810-substrate-repair` | `[#810]` | LOCAL (also touches `win-tooling`) | opus / high |

**Ran model is NOT recorded here** — this file lands before any lane exists, so a ran-model
column would be a prediction. Ordered-vs-ran is recorded in the dispatch receipts (JOURNAL) and
read off each lane's transcript at integration.

**Model rationale:** the Ch8 routing matrix makes opus the default for any `.dev-knowledge` arc and
for gate and organ code; all three lanes are gate/organ code whose failure poisons downstream
work. None is a sonnet-class self-contained chore.

**Integration:** the operator opens the integrator seat himself, LOCAL and INTERACTIVE, from the
boot render. Suggested merge order: **2 first** (it widens `LANE_BRANCH_RE`, `[#809]`, so the
lane merges after it can match the grammar), then R, then 1.

## 3 · Id blocks — reserved here, before any lane runs

The allocator `[#804]` asks for does not exist yet, so this manifest is the allocator for this
batch: disjoint blocks, reserved in the committed tree before the first lane boots. Measured
free at reservation: max task id across every local and remote ref = 807; no `[#808]`-`[#826]`
in the prompts dir.

| Holder | Filed now | Block for new ids |
|---|---|---|
| lane 1 | `[#808]` | 811-814 |
| lane 2 | `[#809]` (filed with it by ruling) | 815-818 |
| lane R | `[#810]` | 819-822 |
| integrator | — | 823-826 |

**Honest limit:** a reservation in a LOCAL commit is invisible to a worktree or clone that cannot
see this commit — exactly `[#788]`'s defect. It holds for this batch because all three lanes base
on a local `main` that contains it. It is not the fix; lane 2 is.

## 4 · HELD — not dropped

| Plan # | Lane | Held until | Reason |
|---|---|---|---|
| 3 | Model routing (`[#752]`) | lane 2 LANDS | It finishes aa-12's work at `e17c6200` on `worktree-lane-aa-12-enforced-routing`, whose row was renumbered 787 -> `[#793]`, and main's `[#793]` is now a different row ("A withdrawn lane's live worktree built a rival organ"). It carries `[#752]` and drops the 793 row. Dispatching it before the allocator lands would make its renumber a fourth instance of the same bug. |
| 4 | Conductor reads the freeze (`[#802]`) | lane R produces a heartbeat | Held by operator ruling behind the substrate repair. CI enforcement stays OFF regardless: `main` carries 62 frozen failures and enforcing today blocks every merge; enabling it is a separate ruling after lane 4 lands. |

Wave 2 and 3 of the plan are untouched and not part of this batch.

## 5 · Step-0 evidence (why this batch is three LOCAL lanes)

- `seat_refusals lane-ceiling --check-worktrees`: PASS (4 as first planned, 3 as ruled).
- `batch_manifest.open_batches()`: `[]` before this file.
- `resource_lifecycle admit`: **exit 1** at step 0 — free 1.80 GB < 3.00 GB reserve, 5 live seats
  against a computed ceiling of 1; non-Claude memory 23.4 GB. Two finished seats were retired on
  operator word (`a07a1f47`, `d8c134ee`; `resource_lifecycle teardown`, no survivors). Admission is
  re-run immediately before the first dispatch; the operator frees the memory.
- **CODESPACE was not dispatchable:** `validate_substrate` leg 8 (`RULE_HEARTBEAT_DEAD`) arms
  2026-09-16 and `substrate_heartbeat.read_receipt` returned `readings={}`. The
  `substrate-heartbeat` workflow failed both runs (35017551689, 35090026934): the Actions runner
  installed uv 0.12.15 (`version: "latest"`, under a comment claiming it reads the pin) against
  `==0.11.19`, exit 2. Separately, the Codespace runner launches `claude -p` with no `--model`
  (`[#810]`), so an explicit model was not expressible there at all.
- **A green workflow alone does not satisfy leg 8:** the workflow uploads an artifact nothing
  reads; leg 8 reads a MACHINE-LOCAL receipt. Lane R's done-when names both legs.
- **CLOUD was not eligible:** all lanes are gate-dependent (Ch8 Layer 1 Q1), and leg 8 covers
  cloud too.
- **Tracked-vs-deployed drift:** `win-tooling/config/dispatch-helpers/DispatchHelpers.psm1` differs
  from the deployed `~/.dispatch-helpers` module by ~746 lines, deployed AHEAD. Lane R reconciles
  before editing.

## 6 · Branch names do not match the ratified grammar — on purpose, and recorded

`LANE_BRANCH_RE` admits one batch letter; all 26 are spent (measured over merge subjects on all
refs). Batch AA's `worktree-lane-aa-*` never matched, so its merges received no ADR-110 exemption
— which is why `audit-health` fired on every intermediate commit of that integration. By ruling,
the grammar is WIDENED (`[#809]`, lane 2), never recycled. These contracts were emitted with
`gen_lane_contract emit --loose-slug`; lane merges before lane 2 lands will not receive the
exemption, and `validate_substrate` refuses their in-tree copies (see the header).

## 7 · Kill-candidates

none — `[#808]` is the time bound, distinct from `[#768]`'s refusal channel; `[#809]` is the
grammar, distinct from `[#804]`'s allocator; `[#810]` is the substrate's model leg, distinct from
`[#752]`'s transcript and receipt legs.
