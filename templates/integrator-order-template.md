---
reconciled_with: handoff-process@7.1.0
---
<!-- scope: meta -->
<!--
  templates/integrator-order-template.md — the INTEGRATOR seat's standing order
  (`protocols/HANDOFF_PROCESS.md` §1). The integrator merges; it does not build, fix a
  lane's work, or weaken a check.

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

You merge; you do not build, and you do not weaken a check. The batch's common rules bind you too —
**nobody waits for the operator** above all. No time limit other than the close below.

- **Base:** main `<sha>`. **Transport root:** the `CLAUDE_PROMPTS_DIR` environment variable.
- **Claim (step 0):** `uv run --locked python scripts/claim.py claim INTEGRATOR-<BATCH>` before
  binding the seat; refused (exit 3) means another integrator session already holds this order.
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
2. **Merge in an integration worktree, not on `main`.** A worktree `.claude/worktrees/integrate-<batch>`
   on branch `worktree-integrate-<batch>` from `origin/main` (`merge_path.py integration-name
   --batch <BATCH>` prints the name). Merge the lane there `--no-ff` with the JOURNAL anchor;
   regenerate generated files on the merged tree; `merge_receipt.py open`, then `moment:merge`
   with `HARNESS_MERGE=<the merge sha>` (it runs `models`, the review packet and the gate list;
   each gate and each organ leaves a run event in the private state directory, not in git).
3. **Verify once per check, as cheaply as honesty allows.**
   - *Split attribution:* test files the lane did not change are compared against the registry
     (`--since`); test files it changed or added run once on the merged tree, and their reds are
     the lane's.
   - One ship-gate diff, base against merge; no duplicate ship-gate leg (record it if unavoidable).
   - `merge_path.py verify-local --lane <lane> --slug <lane>` is the direct call of the gate list
     with one receipt step per gate, for a seat whose `moment:merge` is stopped by an organ outside
     the merge's own diff — record the stop; it does not stand in for a refusal.
   - <documentation tier / memory gate — as merged organs make them available>
4. **Land: the integration branch first.** `merge_path.py land --slug <lane> --batch <BATCH> --sha
   <merge> --base <origin/main as fetched before the merge>` pushes the merge to
   `worktree-integrate-<batch>`, reads CI's verdict for that sha (push runs only, completed runs
   only; per-OS, test by test against the base run), re-checks that `origin/main` is
   still the base, and only then pushes the same sha to `main`. Two classes refuse and leave
   `main` untouched: a test red on the merge and green on the base, and a non-pass state of a
   required check (`IN-PROGRESS`, `CANCELLED`, `TIMED-OUT`, `SKIPPED`, a missing required context,
   a poll timeout, `GH-UNAVAILABLE`). A red present on both sides is FLAGGED with its bucket into
   the receipt, not refused; an unregistered one is carried into the digest as `ROWS-OWED`.
   Then `git merge --ff-only origin/main` in the primary, `merge_receipt.py close`,
   and remove the integration worktree and its branch at batch close.
   - *Ruleset:* arming `deploy/conductor-required-checks.ruleset.json` is the integrator's act at
     batch close, after a rehearsal that comes first (`merge_path.py ruleset rehearse`, then
     `ruleset apply --rehearsal <record>`, a dry run until `--execute`, refused without a record
     showing every required context `success`); write it as `OPERATOR-ACTION` where the GO is not
     yet recorded, do not execute it before the rehearsal.
   - *Skipped by decision* (each with its reason in the receipt, none re-dated, none removed from
     `harness.yaml`): `go_reader` — the apply step names the operator's GO itself;
     `test_pairing` — replaced by the test-level per-OS compare; `known_reds_refresh` — a refresh
     at every merge is a laundering route, the compare only reads the registry.
5. **Teardown of the lane:** its job, its worktree, its branch local and on origin, and its claim
   marker (`claim.py release <lane-contract-name>` — no `--session` needed: at most one marker
   ever exists for that name, so this releases it whoever claimed it); then `no_leftovers.py verify
   --lane <slug> --contract <lane-contract-name>` to verify all of it, marker included, is gone.
6. **Receipt:** the `STATE` line with pickup, handback and push times (the receipt's STAGES line
   carries each stage's minutes); the ledger row written.

## Refusals and repairs

A refusal is written only by you, as `to-browser/REFUSED-<slug>.md` with the headers
`from: the INTEGRATOR` and `repair N of 2`, naming what failed and the sync rule (origin only).
A lane refused twice is `FAILED`. Apply the pre-authorized rulings of the common rules; do not
weaken a check to make a merge pass.

Right after writing that file, distil it: `uv run --locked python scripts/learning_distiller.py
run --integrator to-browser/SESSION-integrator-<BATCH>-<date>.md --dispatcher
to-browser/SESSION-dispatcher-<BATCH>-<date>.md --refused to-browser/REFUSED-<slug>.md` — one
candidate row proposed at the moment of refusal rather than held for the close (ruling h: this
organ still files nothing).

## Waiting — a handback wakes you

Between merges you wait on an event, with a timer behind it:

1. **Event wake.** One Monitor on `uv run --locked python scripts/lane_end_guard.py watch` (after a
   cycle add `--since <the previous wake>`, so a handback that landed in between is reported). A
   lane's Stop hook leaves a wake file in your machine's private state directory the moment its
   closing `HANDBACK` line lands, and the command prints one `WAKE <lane> <closing line>` per new
   file: pickup within 30 s. The wake is the signal; the lane's `to-browser/SESSION-<slug>.md`
   stays the evidence you merge from.
2. **Cron fallback.** `CronCreate`, recurring, every 10 min, one foreground check per wake: it
   catches a handback the Monitor missed (an expired Monitor, a hook that did not fire).
3. **Every wake, event or cron, runs the transport sweep.** `uv run --locked python
   scripts/transport_lint.py sweep --since <the previous wake>`: exit 1 prints one
   `<path>: <code>: <reason>` line per non-conforming file. Paste the lines into your receipt as
   `TRANSPORT-LINT` and name the writer. The sweep renames, moves and deletes nothing.
4. **Lint before you write.** A harness writer (`transport.write`) lints on its own. A transport
   file you write by hand — your receipt `SESSION-integrator-<batch-slug>.md`, a `STATE-` file, a
   `REFUSED-<slug>.md`, the `DIGEST-<BATCH>-<date>.md` — is drafted under your job tmp, passes
   `uv run --locked python scripts/transport_lint.py check <draft>` (exit 0), and is then copied
   to the transport.

## Close — when every lane is MERGED or FAILED, or at <time>, whichever comes first

1. Re-run the connection walk on `main`; run `moment:batch-close` with `HARNESS_BATCH=<BATCH>`.
2. **Cost line (R7, F3):** `uv run --locked python scripts/quota_watch.py record` (appends
   the per-user ledger `QUOTA-READS.jsonl` in the OS state directory, writes a `QUOTA-WARN-<date>.md` on any crossing), then `uv run
   --locked python scripts/quota_watch.py line --cloud-sessions <n>` (`<n>` from `claude agents
   --json`) for the digest's `[quota]` line — both if `lane-quota-watch` is MERGED; otherwise by
   hand, each figure with its own command — Codespaces core-hours used/remaining, Actions
   minutes used, Copilot credits used (Enterprise login), cloud sessions used.
3. **Learn from this batch's refusals (ruling h — this organ proposes rows, it does not file
   them):** `uv run --locked python scripts/learning_distiller.py run --integrator
   to-browser/SESSION-integrator-<BATCH>-<date>.md --dispatcher
   to-browser/SESSION-dispatcher-<BATCH>-<date>.md --refused to-browser/REFUSED-<slug1>.md
   [--refused to-browser/REFUSED-<slug2>.md ...]` — one `--refused` per refusal file this batch
   wrote (§ Refusals and repairs above already ran it once per file as each was written; this is
   the whole-batch pass over all of them together) — paste the candidate rows into the digest.
4. Write `to-browser/DIGEST-<BATCH>-<date>.md` (at most 15 KB): the cost line; per merge the sha,
   pickup-to-push minutes and the verdict; the medians; reaps; operator inputs (target 0); the
   registry and baseline id; what is left and its state; the zero-leftovers proof; the
   learning-distiller candidate rows from step 3; and a
   **MORNING** section listing every `DECIDED-BY-LANE`, `OPERATOR-ACTION` and `QUESTION` the
   lanes left.
5. Write `to-browser/STATE-BATCH-<BATCH>.md` reading `CLOSED <time>`.
6. Stop every Monitor, poll and shell of yours, and stop.

## State file

After every `STATE` line you append to your receipt, also write
`to-browser/STATE-<batch-slug>.json` (schema `dev-knowledge-seat-state/1`,
`scripts/seat_state.py`), one call:
`uv run --locked python scripts/seat_state.py write --path to-browser/STATE-<batch-slug>.json
--role integrator --batch <BATCH> --base-sha <sha> --lanes-json <path-or-json>`. Each lane carries
exactly one of `MERGED|IN-FLIGHT|QUEUED|REFUSED|FAILED|REPORTED`, with evidence
(`session_file`, the verbatim `STATE` line, and the sha where one exists) — the same facts your
receipt line already states, in the one place a fresh session reads first instead of the whole
receipt. `WAITING` in your own receipt vocabulary above is `IN-FLIGHT` in the state file; the
writer maps it.

## Cycle — hand over to a fresh session of the same role

Hand over at least every 3 h since you bound your seat, or when your context nears its threshold,
whichever comes first — and only at a **no-merge point**: no integration worktree is open
(`.claude/worktrees/integrate-<batch>` is removed, or not yet created) and no CI wait is in flight
for a landed sha. A merge in flight is finished first: a handover that loses one is worse than a
long session. One session ran 15.7 h in FOUNDATION; the ceiling is what prevents a second.

1. **Write down where you stand.** The state file (above), a final `STATE` line, and the transport
   sweep (`uv run --locked python scripts/transport_lint.py sweep --since <the previous wake>`), so
   the successor starts on a clean transport.
2. **The successor claims and binds first.** A fresh integrator session starts the same way this one
   did: it claims `INTEGRATOR-<BATCH>-cycle-<n>` (`claim.py claim`; `<n>` counts the handovers),
   binds its own seat (`seat_registry.py bind --role integrator --batch <BATCH>`), and rebinds from
   the state file (`scripts/seat_state.py read --path to-browser/STATE-<batch-slug>.json`) instead of
   rereading the whole night's receipt. It starts its own Monitor and cron (Waiting, above).
3. **The successor reads the receipt back three times, 30 s apart.** The last `STATE` line of
   `to-browser/SESSION-integrator-<batch-slug>.md`: three identical reads show the outgoing seat is
   quiet. A line that changed means it was still merging — wait for the next no-merge point.
4. **Only then does the outgoing seat release.** Stop every Monitor (`TaskStop`), delete every cron
   job (`CronDelete`) and end every poll and shell of yours, then `claim.py release` your own claim
   name (`INTEGRATOR-<BATCH>` or your `-cycle-<m>`) and run `seat_registry.py unbind` once. Nothing of
   yours outlives your last message.

The incoming seat picks up the merge queue where the state file says it stood; a state file older
than its own staleness bound is a signal the outgoing seat died mid-cycle, not a file to trust.
