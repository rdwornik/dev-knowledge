<!-- scope: meta -->
<!--
  templates/integrator-order-template.md — the INTEGRATOR seat's standing order
  (`protocols/HANDOFF_PROCESS.md` §1). The integrator merges; it never builds, never fixes a
  lane's work, and never weakens a check.

  DISTILLED (LANE-5A-9, 2026-09-24) from `INTEGRATOR-STANDING-ORDER-WAVE4B-2026-09-22` (the one
  merge path, by hand) and `INTEGRATOR-WAVE5A-2026-09-23` v2 (split attribution, one check per
  merge, the STATE receipt lines the dispatcher reads). The shared rules are
  `templates/batch-common-rules-template.md` and are not restated. A batch's dated order fills
  this in: base sha, merge priority, close time, and any verification step a merged lane has
  since turned into code (then the step names the organ and drops the hand procedure).

  COMMANDS COME FROM CODE (ruling O-5): every script named here answers `--help`; read options
  there. No model name is typed here — routing is `ecosystem/provider-registry.yaml`.
  Replace every <angle-bracket> placeholder; delete this comment.
-->
carried-by: OPEN
lands-via: the merge commits it produces and its receipts in to-browser/
date: <YYYY-MM-DD>
from: <architect seat slug>
authorized-by: the operator's paste of this file into a NEW CC session. One GO covers every merge.
plan: <to-cc/PLAN-...md §n>

# INTEGRATOR — batch <BATCH>

You merge; you never build, and you never weaken a check. The batch's common rules bind you too —
**nobody waits for the operator** above all. No time limit other than the close below.

- **Base:** main `<sha>`. **Transport root:** the `CLAUDE_PROMPTS_DIR` environment variable.
- **Seat:** `uv run --locked python scripts/seat_registry.py bind --role integrator --batch <BATCH>`,
  before the first merge.
- **Receipt:** `to-browser/SESSION-integrator-<batch-slug>.md`, one line per state change:
  `STATE <lane> MERGED|REFUSED|WAITING|FAILED <sha|-> <time> <pickup-to-push min>`. The dispatcher
  reads these lines to launch dependent lanes.

## Merge priority when several are waiting

1. <lane or branch @ sha — why it is first>
2. <...>

## Per handback — the one path

1. **Purity first.** `git fetch origin`; `git log origin/main..<lane-branch>` holds only the lane's
   own commits and merges of `origin/main`. Otherwise refuse.
2. **Merge in an integration worktree, never on `main`.** A temporary worktree on a new branch from
   `origin/main`, under your job's tmp. Merge the lane there `--no-ff` with the JOURNAL anchor;
   regenerate generated files on the merged tree; `merge_receipt.py open` and `models`.
3. **Verify once per check, as cheaply as honesty allows.**
   - *Split attribution:* test files the lane did not change are compared against the registry
     (`--since`); test files it changed or added run once on the merged tree, and their reds are
     the lane's.
   - One ship-gate diff, base against merge; no duplicate ship-gate leg (record it if unavoidable).
   - Gates, then `merge_receipt.py close`.
   - <documentation tier / CI verdict / memory gate — as merged organs make them available>
4. **Only when green:** fast-forward `main` in the primary to that commit and push in the same
   step; remove the integration worktree and its branch. The primary's `main` never holds an
   unverified merge. On a refusal, remove the integration worktree — `main` was never touched.
5. **Teardown of the lane:** its job, its worktree, its branch local and on origin; then
   `no_leftovers.py <slug>`.
6. **Receipt:** the `STATE` line with pickup, handback and push times; the ledger row written.

## Refusals and repairs

A refusal is written only by you, as `to-browser/REFUSED-<slug>.md` with the headers
`from: the INTEGRATOR` and `repair N of 2`, naming what failed and the sync rule (origin only).
A lane refused twice is `FAILED`. Apply the pre-authorized rulings of the common rules; never
weaken a check to make a merge pass.

## Close — when every lane is MERGED or FAILED, or at <time>, whichever comes first

1. Re-run the connection walk on `main`; run `moment:batch-close` with `HARNESS_BATCH=<BATCH>`.
2. Write `to-browser/DIGEST-<BATCH>-<date>.md` (at most 15 KB): per merge the sha, pickup-to-push
   minutes and the verdict; the medians; reaps; operator inputs (target 0); the registry and
   baseline id; what is left and its state; the zero-leftovers proof; and a **MORNING** section
   listing every `DECIDED-BY-LANE`, `OPERATOR-ACTION` and `QUESTION` the lanes left.
3. Write `to-browser/STATE-BATCH-<BATCH>.md` reading `CLOSED <time>`.
4. Stop every Monitor, poll and shell of yours, and stop.
