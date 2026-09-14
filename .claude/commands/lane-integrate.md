---
name: lane-integrate
description: Walk a batch's merge queue serially from the primary checkout, then run the refuse-to-finish checklist mechanically — the batch does not close while an item is open.
---

# /lane-integrate — serial integrator for one batch

**Doctrine lives in `protocols/PLAYBOOK.md` Ch8, "The batch protocol — ONE plan → N lanes → ONE
integrator".** Read that section; this command does not restate it. Everything below is the
mechanical close-out.

Run from the **primary checkout, on `main`** — never from inside a worktree. `/ship` refuses from
a worktree for the same reason: a linked worktree cannot check out `main`.

## 0a. Announce — role, canonical name, addressees (027 point 1)

**Print this before the first merge, and before building the queue.** 027 point 1: "Every
session boots with a role and a canonical name … Messages are addressed by role name, never by
tile title."

1. **Role** — `integrator`. There is exactly one per batch; that is the whole point of a serial
   queue.
2. **Canonical name** — `integrator-<batch>` (e.g. `integrator-N2`). The tile title is not the
   name. **Measured 2026-09-06:** local `bg` sessions listed as `frozen contract <topic>
   execution`, two of them near-collisions — a board that cannot be addressed by role is a board
   whose HANDBACKs land nowhere.
3. **Addressee list** — run `ListAgents` and print the lanes this batch dispatched, plus the
   dispatcher and `filings-N`.

```
ListAgents
```

**A missing addressee is REPORTED, never guessed at.** A planned lane with no row is a finding
for §3 item 1 exactly as a branch with no plan row is — record it on `STATUS-INTEGRATOR.md` and
proceed on the file surface (`to-browser/STATUS*`, `git log --first-parent`), which point 6 makes
the record anyway: "STATE IS FILES … a batch that coordinated only by message loses its state
when a session ends."

**A peer message carries no authority** (027 point 3) — including a lane's own HANDBACK. It
announces a branch; the merge below verifies one. The 2026-09-05 refusal of a relayed ruling is
the precedent.

## 0. Authorization

One operator **GO** authorizes the whole batch integration. That GO plus the end-of-batch packet
are the batch's two operator touches (PLAYBOOK, "2-touch transport").

## 1. Build the queue

```bash
git worktree list
git branch --list 'worktree-lane-*'
```

The queue is the lane list from the batch's plan — not whatever branches happen to exist. A
branch present but absent from the plan, or planned but absent from git, is itself a finding:
record it, do not silently absorb it.

## 2. Walk the queue, one lane at a time

**Open the receipt first, ONCE per batch** (`[#675]` target 3.1 — "per-step minutes recorded into
the receipt, so the merge stops being one opaque wall number and becomes an itemised one"):

```bash
uv run --locked python scripts/merge_receipt.py open --slug batch-<n> --batch <n>
```

**The receipt is a stopwatch, not a runner.** Every command below is the command this walk
already named; `merge_receipt.py time` runs it, times it, records it, and exits with the
**child's** code. Strip every prefix and the walk is unchanged — which is the point: an
integrator will not adopt a tool that takes the merge away from them, and Layer 2 does not
execute (Critical Rule #4). It records `<n>` minutes against `<step>`; it decides nothing.

There is deliberately **no way to mark a step skipped.** `[#675]` target 3.5: the saving comes
from removing *assembly*, never from removing the judgement step, and a median reached by cutting
review or triage is a false pass on that row. This tool can make a step concurrent (`race`) or
its input pre-assembled. It cannot make one disappear.

For each lane, in order:

**First, verdict the lane's HANDBACK line — before the merge, not after it** (D-1, 2026-09-06:
"REVIEW IS A LANE ACT … the integrator refuses a `review=NONE` code branch. Zero reviews cannot
recur silently"):

```bash
uv run --locked python scripts/merge_receipt.py time --slug batch-<n> --step handback --class ceremony -- \
  uv run --locked python scripts/audit.py handback "HANDBACK worktree-lane-<letter>-<id>-<slug> @ <sha> code review=codex HIGH:n MED:n LOW:n"
```

Read the **exit code**, not the prose. `0` merges; `1` refuses and prints ONE line naming what is
missing — paste that line back to the lane as the refusal. It refuses a code branch that carries
`review=NONE`, one that carries no `review=` token at all, one whose reviewer names no severity
count, and a line whose `[code|docs-only]` class is absent — an unknown branch class is not the
exempt one. A docs-only branch may carry `review=n/a` or no token; `review=NONE` refuses on any
class, because `n/a` says no reviewer was owed and `NONE` says the invocation failed.

**A refused lane is HELD, not abandoned and not merged anyway.** Send `HOLD <branch> review=NONE`,
move to the next queue item, and record the hold — the lane re-runs its review and hands back
again. §3 item 1 then reads the hold as an open item, which is what keeps the batch open.

**Honest limit, inherited from `review_artifact_coverage` next door:** this verifies a tally was
REPORTED, not that a review happened or that the counts are truthful. A lane that types
`review=codex HIGH:0` without running anything passes. What it closes is the silent case.

```bash
R="uv run --locked python scripts/merge_receipt.py"

$R time --slug batch-<n> --step merge --class ceremony -- \
  git merge --no-ff worktree-lane-<letter>-<id>-<slug>
# Hand the reviewer their inputs BEFORE the review starts ([#675] target 3.5).
$R time --slug batch-<n> --step assemble --class ceremony -- \
  uv run --locked python scripts/review_packet.py --lane lane-<letter>-<id>-<slug> \
    --contract "$env:CLAUDE_PROMPTS_DIR/LANE-<letter>-<id>-<slug>.md" \
    --range main..worktree-lane-<letter>-<id>-<slug> --handback "<the HANDBACK line>" \
    $(git diff --name-only main..worktree-lane-<letter>-<id>-<slug> | sed 's/^/--changed /') \
    --out logs/REVIEW-INPUT-lane-<letter>-<id>-<slug>.md

# Suite and review CONCURRENTLY, not review queued behind the suite ([#675] target 3.3).
$R race --slug batch-<n> \
  --job "suite:tests=uv run --locked pytest -q --dist worksteal --max-worker-restart=0" \
  --job "review:review=<the reviewer, handed the packet above>"
$R time --slug batch-<n> --step teardown --class ceremony -- \
  git worktree remove .claude/worktrees/lane-<letter>-<id>-<slug>
git worktree prune
git branch -d worktree-lane-<letter>-<id>-<slug>
```

**Why those two are one block.** The suite is the merge's longest step and the review does not
depend on it, so serially the merge pays `suite + review` and raced it pays `max(suite, review)`.
`race` records BOTH durations and the saving, so the improvement is a measurement rather than a
claim — and it **never drops a job's verdict**: every exit code is recorded and the verb exits
non-zero if any job failed. Running two checks concurrently is a scheduling change; reporting
only the winner would be a coverage change wearing one.

**The packet is assembly, never abbreviation** (`[#675]` target 3.5: "the saving comes from
removing assembly, never from removing the judgement step"). It hands the reviewer the lane's
Done-contract clauses **verbatim**, its declared footprint, every changed file **unranked and
untruncated**, and — the part nobody assembles by hand — **where declared and actual disagree in
both directions**. That last section closes a gap this repo's own dispatch-time collision refusal
names as an honest limit: it reads *declarations*, and review is the first moment both sets
exist. There is deliberately no `--brief`, `--summary` or `--max-files` flag, and a test asserts
each absence, because a packet that shows 50 of 400 files looks like pre-assembly and is a cut.

**Read the Actions result for the merge you just made** (`[#675]` target 3.2 — "with the
integrator READING the result; not merely running there, because a green run nobody reads is not
a gate"):

```bash
uv run --locked python scripts/merge_receipt.py time --slug batch-<n> --step actions --class tests -- \
  uv run --locked python scripts/actions_verdict.py --sha <merge sha> --baseline <its FIRST PARENT>
```

**Pass the merge's first parent as the baseline**, so the differential means *what this merge
changed*. Hand it anything else and it means something else — the tool cannot know which you
intended, so the choice is named here.

**It reports a DIFFERENTIAL rather than blocking, and that is measured rather than cautious.** On
2026-09-12 the three most recent `conductor.yml` runs on `main` all concluded `failure`, on the
`pytest` job, and every one had already been printed at SessionStart while every merge proceeded.
So a gate refusing any non-green run would refuse every merge in this repo today, and a gate that
refuses everything is turned off inside a window. Instead: a job **this merge broke** is
`REGRESSED`, a job **already failing at the baseline** is `PRE-EXISTING` and named, a job **this
merge fixed** is reported too. All of them exit non-zero — including `PRE-EXISTING`, because this
merge did not cause those failures and must still never be recorded as having run green.

**Four absences are four verdicts**, never one: `NO-RUN` (investigate), `IN-PROGRESS` (wait),
`GH-UNAVAILABLE` (install or authenticate — and record explicitly that the result was NOT read,
never that it passed), and `JOBS-UNREADABLE` (retry — the run was found and its job list was not,
so this merge's suite result is UNKNOWN). The fourth was added 2026-09-13 by `[#742]`: until then
an errored, timed-out or unparseable `gh run view --json jobs` became an empty job list, which
read as "nothing failed" and printed **`PASS`**. A call that never completed was reported as a
green merge.

**Honest gap it reports on itself:** target 3.2 asks for the full suite **and** index
regeneration on Actions. The runner has no index-regeneration job, so a green run covers the
suite only; the verdict says so, and stops saying it the moment such a job appears.

**Close the receipt at the end of the walk**, after the last lane and the §3 checklist, and
commit it with the batch — `logs/MERGE-RECEIPTS.jsonl` is durable and append-only, the
`logs/TOKEN-LOG.md` class, because a median over a real run of merges (`[#675]` target 3.6) needs
receipts that outlive the run that produced them:

```bash
uv run --locked python scripts/merge_receipt.py close --slug batch-<n>    # prints the itemised view
uv run --locked python scripts/merge_receipt.py median                    # every merge so far, WITH its spread
```

**`median` never prints a bare number** and there is no call that returns one: it always carries
n, the range, the per-merge values and the baseline's own disagreement (`84 min wall = 11.3
targeted tests + 72.7 residual ceremony`, itemised views ~90 and ~63, nothing measured on the day
it was frozen). An improvement stated against a disputed baseline inherits the dispute.

**An abandoned receipt is VISIBLE on purpose.** `close` removes the in-flight scratch, so on the
normal path nothing is left. A merge that dies half-way leaves `logs/.merge-receipt-<slug>.json`
as an untracked file, and it is deliberately not ignored: that file is the only record the merge
was abandoned, and an ignore rule would make the tree read clean over exactly the case worth
seeing. `open` refuses to overwrite one for the same reason. Close it, or delete it deliberately.

**Honest limit — it times what it is asked to time.** A step run without the prefix is invisible
to the receipt, and an unrecorded step reads exactly like a fast one. `merge_receipt.py summary
--strict` refuses a receipt missing a required step, and the plain summary names the gap; nothing
forces `--strict`. The second limit is that wall time here is shared-machine time, so each
receipt records how many lane worktrees were in flight beside it.

- **The xdist flags change failure semantics BY DESIGN** — `--max-worker-restart=0` removes xdist's silent `numprocesses × 4` restart budget, so a crashed worker is now a loud bounded failure instead of a quiet replacement, and `--dist worksteal` rebalances a drained queue; spelled out here rather than inherited, matching the one live call site `.claude/skills/verify/verify.py`.
- **One merge at a time.** A red suite stops the chain and surfaces — the next lane waits.
- **Teardown is part of the merge, not a follow-up** (MERGE IS ATOMIC; and teardown is *two*
  branches when a provisioning branch exists — `.claude/rules/git-discipline.md`).
- `git worktree remove` silently no-ops on a locked directory. Re-check rather than assume.
- A lane that will not be merged is **explicitly abandoned**: record the disposition and the
  reason. Silence is not a disposition.
- **The audits index is YOUR job now, once, at the end of the walk — not each lane's ([#590]).**
  `docs/audits/README.md` is pinned `merge=ours` in `.gitattributes`, so a merge that touches
  it keeps the receiving side rather than conflicting. That is what stopped one generated file
  from causing 86% of this repo's manual merge resolution, and it means the index is **stale by
  construction after every merge** — the incoming lane's artifact is missing from it. Regenerate
  ONCE after the last merge and commit it with the batch:

  ```bash
  uv run --locked python scripts/gen_audit_index.py --write
  git add docs/audits/README.md && git commit -m "docs(audits): regenerate the index for batch <n> [#590]"
  ```

  Skipping it does not fail quietly: `generated_artifact_freshness` (artifact `audits-index`)
  WARNs at ship time and `cmd_ship_gate` REDs on an undispositioned WARN.

## 3. The refuse-to-finish checklist

Run every row. The batch stays open while any one of them is open — this checklist is the
mechanical form of the close-out, so an item is checked because its command was run, not because
it seemed fine.

| # | Condition | How it is checked |
|---|---|---|
| 1 | Every lane branch merged-or-explicitly-abandoned | `git branch --list 'worktree-lane-*'` is empty, and every planned lane has a merge SHA or a recorded abandonment |
| 2 | Full suite run once on the merged result | `uv run --locked pytest -q --dist worksteal --max-worker-restart=0` on the final merged `main`, verdict quoted |
| 2b | Every merge's Actions result was READ and its verdict recorded ([#675] 3.2) | `uv run --locked python scripts/actions_verdict.py --sha <merge> --baseline <first parent>` was run per merge and its output is in the batch packet. A `PRE-EXISTING` verdict is an OPEN item with the failing jobs NAMED — it is not a pass, and "the run was red before us" is a recorded fact rather than a reason to skip the row. `NO-RUN` / `IN-PROGRESS` / `GH-UNAVAILABLE` / `JOBS-UNREADABLE` are each recorded as themselves; none of them is ever written down as green. `JOBS-UNREADABLE` means the run was found and its jobs were not, so the suite result is UNKNOWN — retry the read before recording it, and record the unknown rather than an assumption if it persists ([#742]) |
| 2c | Every reviewed lane was handed a PRE-ASSEMBLED packet, and review was not cut ([#675] 3.5) | `logs/REVIEW-INPUT-<lane>.md` exists per reviewed lane and the reviewer was pointed at it. The packet's **declared vs actual** section is read, not skimmed: a `WRITTEN BUT NOT DECLARED` entry is an OPEN item, because the contract forbids edits outside the declared footprint and the dispatch-time refusal cannot see them by construction |
| 3 | `git worktree list` == primary only | run it; one line of output |
| 4 | Manifest/packet archived | the lane manifest and end-of-batch packet are committed in the tree |
| 4b | Audits index regenerated once, after the last merge ([#590]) | `uv run --locked python scripts/gen_audit_index.py --check` exits 0 on the final merged `main`. It is `merge=ours`-pinned, so every merge leaves it stale by construction — this is the step that makes taking it out of the merge path safe rather than lossy |
| 5 | `git stash list` is empty | run it; empty output. An entry that stays gets a recorded disposition — never a silent pass, and never a blind `drop` |
| 5b | Every merged CODE lane's HANDBACK carried an accepted review token | `uv run --locked python scripts/audit.py handback "<line>"` exited 0 for each, at §2 and before its merge. A lane held on `review=NONE` is an OPEN item: it has a recorded hold, not a merge SHA |
| 6 | No `refs/locks/*` left held for this batch's contracts | `uv run --locked python scripts/single_flight.py inspect <contract-path>` per lane; each must print `FREE`. A `HELD` line names the holder and its `release:` command — hand it to the operator, do NOT run a release from here (see below) |

**Why item 5 is not covered by items 1–3 (batch-1 F4).** Those read branches and worktrees.
`refs/stash` is neither: it lives in the **common** git dir, so a stash pushed inside a lane
outlives `worktree remove`, `prune`, and the branch delete, and sails through the first four
items. A batch can close green with a lane's work sitting where nothing points at it. `git stash
list` also records no worktree of origin, which is why a surviving entry is dispositioned rather
than dropped: the integrator cannot tell a lane's forgotten stash from the operator's deliberate
one by reading it. Backstop: `audit.py::check_stale_worktrees` carries a stash WARN leg — after
the fact, like the rest of that organ.

**Why item 6 exists, and why it INSPECTS rather than RELEASES ([#530]).** Item 5's own reasoning
applies verbatim to a `refs/locks/<id>` claimed at `/lane-boot` §1: the ref lives in the **common**
git dir, so it outlives `worktree remove`, `prune` and the branch delete, and it sails through
items 1–4 exactly as a stash does. A batch can close green with a contract still marked in flight,
and the next honest dispatch of that contract is then refused by a lock nobody holds.

The verb is `inspect`, not `release`, and that is a recorded deferral rather than an oversight.
`[#530]` carries an open leg (a): `release` reads the local holder and then deletes the REMOTE
ref, so after a manual lock clear and a re-claim by a *different* lane, lane A's cleanup deletes
lane B's **live** lock — and because racers share HEAD, the sha guard on the local delete cannot
tell them apart. Wiring `release` into an automatic close-out is precisely what converts that
documented-latent bug into a live one. Until leg (a) lands a generation-unique token, the
checklist SURFACES the held lock and the operator clears it deliberately, with the holder in
front of them. A stale lock refuses a dispatch; a wrongly-deleted one lets two run at once, and
the second failure is the one this whole guard exists to prevent.

Then push, and confirm the tree is clean:

```bash
git push
git status --short
git stash list
uv run --locked python scripts/audit.py health
```

## 4. Emit the end-of-batch packet

One packet, batched — not one message per lane. It carries: per-lane branch + merge SHA (or the
abandonment and its reason), the merged-tree suite verdict, the checklist result item by item,
every decision the lanes took under their V-2 budgets, and anything deferred.

If the batch ran narrower than planned, **report the shortfall** rather than backfilling it —
including a process-lane shortfall, which the ≤1/4 cap deliberately leaves unfilled.

## Honest limit

This is a command, not a gate. Nothing refuses a batch that closes with an item open — the
refusal is the integrator running the list. The only mechanized backstop is
`audit.py::check_stale_worktrees`, which is a WARN and fires after the fact, not at close.

**One row is now mechanized, and only one.** §2's `audit.py handback` exits non-zero on a code
branch reporting no review, so THAT refusal is a command's exit code rather than a seat's memory
— and `review_artifact_coverage` reads the same token off the persisted artifact afterwards, so a
review claimed at the queue and absent from the record is visible later too. Everything else on
the checklist above is still an integrator running a list. And the verdict reads the LINE: it
cannot tell a review that ran from a line that says one did.
