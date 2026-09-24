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

**ONE RECEIPT PER MERGE, opened and closed inside each lane's block** (`[#675]` target 3.1 —
"per-step minutes recorded into the receipt, so the merge stops being one opaque wall number and
becomes an itemised one"; changed from one-per-batch by `[#750]`). The commands are in the
per-lane sequence below; `median` runs once, at the end of the walk.

**Why per merge.** One receipt per batch made `REQUIRED_STEPS` satisfiable by whichever lane
recorded a step id first, left target 3.1's itemised view of *a merge* nowhere to live, and made
`median` a median over BATCHES printed as "median merge minutes" — the `kind`-field failure with
the discriminator moved one level out. Each receipt now also carries the **merge SHA** it timed,
which is what lets §3 row 2d refuse a merge that landed without one.

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

**Open this merge's receipt first** — the clock starts before the handback verdict, because the
verdict is part of the merge's cost:

```bash
uv run --locked python scripts/merge_receipt.py open --slug lane-<letter>-<id>-<slug> --batch <n>
```

**Then verdict the lane's HANDBACK line — before the merge, not after it** (D-1, 2026-09-06:
"REVIEW IS A LANE ACT … the integrator refuses a `review=NONE` code branch. Zero reviews cannot
recur silently"):

```bash
uv run --locked python scripts/merge_receipt.py time --slug lane-<letter>-<id>-<slug> --step handback --class ceremony -- \
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

**The order is the one this repo already rules: merge locally, verify, push, THEN tear down.** The
"verify" and the post-teardown check are not steps typed out here — they are the `merge` and
`teardown` **moments** declared in `ecosystem/harness.yaml`, called by name, so the organs a moment
runs are the declaration's and not this file's. This file names the calls; the declaration owns
which organs and in what order (comparator, review packet, gate list, test pairing; then the
no-leftovers check). A moment leaves one receipt per organ under `logs/receipts/` and exits
non-zero if any required organ did.

The steps, in order — the block below is ONE `&&` chain so that **each step runs only if the
one before it exited 0**. A refusal at step 2 or in the race therefore cannot reach the push, and a
failed push cannot reach the teardown; pasted as separate lines, the same commands would push
regardless (Codex terra review, CRITICAL, `docs/audits/2026-09-20-codex-l4-integrator-surface.md`):

1. **MERGE locally** (`M` is the merge commit).
2. **VERIFY** — `moment:merge`, called after the local merge. It runs the ordered-vs-actual model
   comparator FIRST (a disagreement exits non-zero and stops the moment before anything else is
   spent), then the review packet, then the gate list (`scripts/gates.py`: audit, ship-gate, ruff,
   impacted tests — one verdict artifact), then test pairing. `HARNESS_CHANGED` is a placeholder the
   declared row requires: after a merge the packet reads the file list off the merge commit itself,
   so no list is typed here and none can be abbreviated. Then suite and review run CONCURRENTLY, not
   review queued behind the suite (`[#675]` target 3.3); the reviewer is handed
   `logs/receipts/MOMENT-MERGE-REVIEW-PACKET.md`, written by the moment.
3. **PUSH** (option A of the PUSH FIRST box below).
4. **READ ACTIONS** — `merge_receipt.py actions`, right after the push (the PUSH FIRST box below
   explains why not before): it reads this merge's Actions run and records its STATE on the
   receipt, which must still be OPEN here (`load_receipt` refuses a slug with no open receipt).
5. **TEAR DOWN, THEN CLOSE THE RECEIPT, THEN `moment:teardown`** (R-W4-4: `merge_receipt open`
   before `models`, `merge_receipt close` before `moment:teardown`). Inside this step the order is
   itself load-bearing: `git worktree remove` is timed against the STILL-OPEN receipt (closing
   first would leave that duration unrecorded as `UNRECORDED` instead of `teardown`), closing the
   receipt commits its one-line ledger append so the tree is clean, and only THEN does
   `moment:teardown` run — which verifies the removal was complete. Closing after `moment:teardown`
   is the connection test's first recorded stop: the scratch file `logs/.merge-receipt-$L.json`
   stays untracked until `close` deletes it, and `no_leftovers`'s working-tree-clean check FAILs on
   it.

```bash
R="uv run --locked python scripts/merge_receipt.py"
L="lane-<letter>-<id>-<slug>"
DOIT="uv run --locked doit -f scripts/dodo.py"

$R time --slug $L --step merge --class ceremony -- git merge --no-ff worktree-$L \
&& M=$(git rev-parse HEAD) \
&& HARNESS_LANE=$L HARNESS_BATCH=<n> HARNESS_CONTRACT="$CLAUDE_PROMPTS_DIR/LANE-<letter>-<id>-<slug>.md" \
   HARNESS_HANDBACK="<the HANDBACK line>" HARNESS_CHANGED=$M \
   $R time --slug $L --step assemble --class ceremony -- $DOIT moment:merge \
&& $R race --slug $L \
   --job "suite:tests=uv run --locked pytest -q --dist worksteal --max-worker-restart=0" \
   --job "review:review=<the reviewer, handed the packet above>" \
&& git push \
&& $R actions --slug $L --sha $M \
&& $R time --slug $L --step teardown --class ceremony -- git worktree remove .claude/worktrees/$L \
&& git worktree prune \
&& git branch -d worktree-$L \
&& $R close --slug $L \
&& git add logs/MERGE-RECEIPTS.jsonl \
&& git commit -q -m "chore(receipts): close the merge receipt for $L" \
&& HARNESS_LANE=$L $DOIT moment:teardown
```

**Then, standalone — NOT chained onto the walk above, and NOT a gate:** record CI's verdict
beside the local one (LANE-5A-6). Nothing has read CI's own ~8-minute result as data before now,
so the integrator has been recomputing locally for an hour every time; this reads it and files it
next to the LOCAL verdict (`logs/receipts/MOMENT-MERGE-GATES-VERDICT.json`) so the morning packet
can read how often the two already agree — the evidence owed before CI can become the gate. `$M`
and `$L` are still in scope from the chain above; the organ needs the worktree for neither.

```bash
uv run --locked python scripts/ci_verdict.py --ref $M \
  > logs/receipts/CI-VERDICT-$L.json 2>logs/receipts/CI-VERDICT-$L.log; true
cat logs/receipts/CI-VERDICT-$L.json
```

**`; true`, deliberately.** `ci_verdict.py` exits non-zero on every verdict but a clean `green`
(the same convention `actions_verdict.py` uses, for the same reason — a gate silent on success
has not been read, it has been assumed) — but that convention is for a caller that treats the
exit code as a gate, and this walk does not, tonight. CI ran 20/20 red against a stale baseline
on 2026-09-23 (`to-browser/DIGEST-AUDIT-CROSSCHECK-2026-09-23.md`); chaining this onto the walk
would refuse every merge in the batch on a disagreement the batch exists to MEASURE, not enforce.
The JSON on disk is the record; the walk's own exit code stays whatever the chain above decided.

**It POLLS, in-process, for up to 15 minutes by default** (`--timeout`; CI's own run costs about
8 minutes, measured). A run still in progress past the timeout reads back `not-run`, naming the
run id so a plain re-run (`scripts/ci_verdict.py --ref $M`) picks it up once CI finishes — a
retry, not a refusal.

**A non-zero exit from step 2 is a REFUSAL, and it is recorded.** The comparator's exit code is
its verdict: the `models` verb exits 0 only when the tier the contract ordered is the tier
the lane's transcript shows it ran — a divergence, an unverifiable split and an empty store all
exit non-zero. `doit` stops at the first failed organ, so a refused comparison means no gate ran,
and the failed organ's receipt (`logs/receipts/MOMENT-MERGE-MODELS.json`, `exit_code`) is the
record. **Do not push and do not tear down.** The local merge commit stays where it is: undoing it
is a `git reset`, which is destructive and which this command never runs — hold the lane, tell the
operator, and stop the walk (the next lane would merge on top of it). The gate list is the same
shape: `logs/receipts/MOMENT-MERGE-GATES-VERDICT.json` names each gate, its exit code and its
duration, and a RED verdict is a refusal to push, not a note.

**Why the review range is not `main..worktree-$L` any more — one line:** after the merge, main
already contains the branch, so that range is **empty by construction**; the packet now reads the
merge commit against its first parent (`<merge>^1..<merge>`), which is non-empty for the same
reason. `review_packet.py` swaps an empty range for the merge's own and refuses to render one it
cannot resolve.

**Honest limit, inherited from the declaration and not fixable from this file.** The `models` row
carries no `--worktree`, so it reads the transcript filed under the checkout the moment runs in —
the primary — rather than under the lane's worktree, and the verdict can be `no-transcript` or a
reading of the integrator's own session. That fails CLOSED (non-zero), never as a false pass, but
it means step 2 refuses until the declared row names the lane's worktree. Recorded in
`to-browser/QUESTION-lane-l4-integrator-surface.md`; the declaration is L1/L7's file, not this
lane's.

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
a gate"). That is the `$R actions --slug $L --sha $M` call already in the chain above, positioned
right after the push and before teardown — the receipt is still OPEN there, which `actions` needs.

**Where the local suite is barred** (no `race --job suite:...` on this box), pass `--step suite`:
the Actions read then IS the receipt's `suite` step. Without it `actions` records under `actions`,
`suite` stays UNRECORDED, and every receipt on that box is incomplete however carefully it is read
(measured 2026-09-16: all four batch-AA receipts, `[#805]`).

**Do not pass `--baseline`. It is DERIVED from `<sha>^1`**, so the differential means *what this
merge changed* without you having to get it right at every merge of a six-merge walk. Pass it only
to **assert** what you expect: a value that is not the merge's first parent is **REFUSED**, and the
refusal names both commits.

**Why it is derived rather than supplied, which is a correction to how this section read at
`02c6ed5d`.** The baseline SELECTS the verdict. Attribute a merge that broke `pytest` against some
older commit where `pytest` also failed and a `REGRESSED` merge reads `PRE-EXISTING`, the receipt
COMPLETES, and row 2d exits 0 — `[#744]`'s false pass reached through the one input that was still
typed while `--state`'s absence guarded the front door. The realistic route is an ordinary slip:
`--baseline main` instead of `sha^1`, or one copy-pasted from the previous lane's block. Found by
Codex `gpt-5.6-terra` reviewing `[#750]` and fixed by derivation, so the correct reading is the
default and the wrong one is unavailable. **A SHA whose first parent cannot be read REFUSES** rather
than falling back to no baseline, because `UNATTRIBUTED` from a silent failure and `UNATTRIBUTED`
from an honest unknown are different facts and one of them is a bug.

**The baseline actually read is RECORDED on the step and PRINTED in the summary** (`vs <sha>`), so a
`PRE-EXISTING` can be checked rather than taken on trust.

> ### PUSH FIRST. This verb reads a run that does not exist until the merge is on origin.
>
> **`actions` cannot be run on an unpushed merge commit.** GitHub has no run for a SHA it has
> never seen, so `verdict_for` returns `NO-RUN` — which is unreadable, which is INCOMPLETE, which
> makes **row 2d refuse the merge**. Measured, not reasoned: `actions_verdict.py --sha <a local
> unpushed commit>` prints `NO-RUN` with the remedy *"Either the push has not landed, the workflow
> did not fire, or the run is against a different SHA"*. **A `NO-RUN` here almost always means the
> first of those three.**
>
> **`IN-PROGRESS` is also unreadable**, so a run that has not finished refuses too. Re-run
> `actions` under its own `--step` id when it completes: `suite_verdict()` is **last-wins**, so the
> good read supersedes the `IN-PROGRESS` one and the receipt completes. Retrying is the mechanism,
> not a workaround.
>
> **RESOLVED 2026-09-20 by the frozen L4 contract (clause 1: "merge locally, verify, push, then
> tear down"): OPTION (A), push per merge.** The block below is written that way. It was open
> (`[#750]`, escalated at handback) because this file used to push **once**, after the last lane,
> while this read sits inside each lane's block — and those two cannot both be right. The options
> as they were put:
>
> * **(A) push per merge**, inside this block, before this read. Keeps each receipt's span honest —
>   one merge, one wall time. Costs: every merge pays its own pre-push gates, and with no open batch
>   manifest it forces an anchor arc per merge.
> * **(B) keep the single end-of-batch push** and do `actions` + `close` per merge afterwards. One
>   push, but it **corrupts the measurement**: merge A's receipt stays open across the merging of
>   B, C and D, so A's wall absorbs their ceremony — precisely the inflation `[#675]` exists to
>   itemise. Not recommended.
>
> **`close` must follow `actions` and must itself finish before `moment:teardown` runs (R-W4-4);
> `actions` must follow the push.** That ordering holds under either choice; the walk now pushes
> inside each lane's block, before `actions`.
>
> **The finding underneath is older than `[#750]` and worth stating once.** `[#675]` target 3.2
> asks for *"the integrator READING the result"*, and this walk has read the verdict pre-push since
> before `[#750]` existed. Under the old code that surfaced as `ok=False` and vanished into the
> same blanket incompleteness that made `[#744]`'s predicate unreachable — so nobody could see the
> read was structurally impossible. **Target 3.2 has never been satisfiable by this walk**,
> independent of the receipt work. Fixing the predicate is what made the ordering visible.

**This verb replaced a `time --step actions -- actions_verdict.py …` prefix, and the difference
is the whole of ruling AY1-1** (`[#750]`). The prefix recorded only the child's **exit code**, and
since `Verdict.ok` is `state == PASS`, a `PRE-EXISTING` red arrived as `ok=False` — so while
`main`'s Actions `pytest` job is pre-existing red, **every** receipt was INCOMPLETE however clean
the merge, `median` stayed UNDEFINED rather than low, and row 2d below would have refused every
merge in this repo on its first day. `actions` records the **state by name** — `PASS`,
`PRE-EXISTING`, `REGRESSED`, `NO-RUN`, `IN-PROGRESS`, `GH-UNAVAILABLE`, `JOBS-UNREADABLE`,
`UNATTRIBUTED` — binds the receipt to the merge SHA it read, prints the same verdict you would
have read, and **exits with the same code**: non-zero on `PRE-EXISTING` included.

**COMPLETE is not a statement that the run was green**, and both halves matter. `PASS` or
`PRE-EXISTING` makes the receipt a usable measurement *with the state on its face* — in the
rendered summary and in the ledger row — so nobody can read it as a clean run. `REGRESSED`, or a
state that says the result could not be read, makes it INCOMPLETE and refuses the merge. Nothing
here forces a step to exit 0; that is `[#744]`'s false pass and AY1-1 rules it out by name.

**There is deliberately no way to TYPE a state onto a receipt** — no `--state` flag on any verb,
and a test asserts each absence. So `GH-UNAVAILABLE` refuses the merge rather than offering a way
round itself: you record that the result was NOT read, which is what target 3.2 asks for, instead
of typing the green the tool declined to find. On `JOBS-UNREADABLE`, **retry the read** — a second
`actions` call under its own `--step` id supersedes the first, and both stay on the receipt.

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

**Close each lane's receipt, and commit the ledger append, BEFORE `moment:teardown`** (R-W4-4) —
both calls are already in the chain above, right after `git branch -d worktree-$L`: `close` prints
the itemised view, `git add` + `git commit` land the one-line append to the durable, append-only
`logs/MERGE-RECEIPTS.jsonl` (the `logs/TOKEN-LOG.md` class, kept so a median over a real run of
merges — `[#675]` target 3.6 — has receipts that outlive the run that produced them). Committing it
**per lane**, not batched at the end, is the other half of the same fix: an uncommitted append is
itself a dirty path, and `no_leftovers`'s working-tree-clean check would refuse the very next
lane's teardown on it exactly as it refused on the uncommitted scratch file before this ordering
existed.

`median` and row 2d's `require` still run ONCE, after the LAST lane:

```bash
uv run --locked python scripts/merge_receipt.py median   # ONCE, at the end -- every merge so far, WITH its spread
```

**`require` reads the LEDGER, so it needs every receipt already closed** — which each lane did,
before its own `moment:teardown`, above. An open receipt is one it cannot see, and the row would
refuse a merge you did itemise.

**The itemised view now accounts for the WHOLE arc, which it did not before `[#750]`.** Wall time
is the span `opened -> closed`; the summed-children figure keeps its own name (`RECORDED`); and
the difference is printed as `UNRECORDED` and folded into the baseline's residual-ceremony bucket,
so `tests + residual` adds up to the arc rather than to the part of it that happened to be
wrapped. Ledger row `lane-x-675-step-7` is why: a **3h01m20s** arc recorded `wall_seconds: 1.776`
— the duration of its one timed child — and 72.7 of the baseline's 84 minutes live in exactly
those gaps. Read `UNRECORDED` as the honest size of the ceremony nobody timed, not as noise.

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
forces `--strict`. Since `[#750]` an unprefixed step is at least visible *in aggregate* — it lands
in `UNRECORDED`, so it shows as ceremony nobody attributed rather than as no time at all. The
second limit is that wall time here is shared-machine time, so each receipt records how many lane
worktrees were in flight beside it.

**Honest limit — the refusal in row 2d is scoped to a RANGE and is wired into no hook.** It
judges the merges in the range you hand it. Armed tree-wide it would refuse every merge that
predates the receipt; run at commit time it would query an Actions run that cannot exist yet. It
is a checklist row with an exit code, which is what makes it a refusal rather than a memo — and
like every other row here, it is only run because you run it.

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
| 2b | Every merge's Actions result was READ and its verdict recorded ([#675] 3.2) | `uv run --locked python scripts/merge_receipt.py actions --slug <lane> --sha <merge>` was run per merge, **after that merge was pushed** (§2's PUSH FIRST box — pre-push it reads `NO-RUN` and row 2d refuses), and its output is in the batch packet. **Do not pass `--baseline`:** it is derived from `<sha>^1` and a value that is not the first parent is refused, because the baseline selects the verdict. **"Recorded" is now literal, not a habit** (`[#750]`): the state is on the receipt and in the ledger row by name, which is what row 2d then reads — so this row and that one are the same fact checked at two moments, the reading and the ledger. A `PRE-EXISTING` verdict is an OPEN item with the failing jobs NAMED — it is not a pass, and "the run was red before us" is a recorded fact rather than a reason to skip the row. It is nonetheless COMPLETE for row 2d, and those two statements do not conflict: the merge is measurable, and the red is still owed to the packet. `NO-RUN` / `IN-PROGRESS` / `GH-UNAVAILABLE` / `JOBS-UNREADABLE` are each recorded as themselves; none of them is ever written down as green. `JOBS-UNREADABLE` means the run was found and its jobs were not, so the suite result is UNKNOWN — retry the read before recording it, and record the unknown rather than an assumption if it persists ([#742]) |
| 2c | Every reviewed lane was handed a PRE-ASSEMBLED packet, and review was not cut ([#675] 3.5) | `logs/receipts/MOMENT-MERGE-REVIEW-PACKET.md` was written by the merge moment for each reviewed lane (the receipts home is per checkout and gitignored, so read it before the next lane's moment overwrites it) and the reviewer was pointed at it. The packet's **declared vs actual** section is read, not skimmed: a `WRITTEN BUT NOT DECLARED` entry is an OPEN item, because the contract forbids edits outside the declared footprint and the dispatch-time refusal cannot see them by construction |
| 2d | Every merge in the walk range carries a COMPLETE `kind=merge` receipt ([#750], ruling AY1-1) | `uv run --locked python scripts/merge_receipt.py require --range <the FIRST merge's first parent>..HEAD` exits 0, run after the last `close`. It enumerates the first-parent merge commits in the range and REFUSES any that no complete receipt names — a **missing** receipt, or one whose suite verdict is `REGRESSED` or unreadable. It NAMES the merges that passed as well as the ones that did not, and a range holding **no merge at all** says so rather than printing OK, because "0 of 0 unreceipted" is exactly the plausible-value failure `[#675]` is filed about. A bad range **fails CLOSED**. **THREE** ways to read a refusal wrong, and the first is the one that will actually happen: (i) a `NO-RUN` verdict on every merge means **you have not pushed yet** — `actions` reads a run that does not exist until the merge is on origin, so this row refuses the whole batch if the reads ran pre-push (see §2's PUSH FIRST box; `IN-PROGRESS` behaves the same and is fixed by re-reading, since the verdict is last-wins); (ii) an OPEN receipt is invisible to it (close first); (iii) a `PRE-EXISTING` suite verdict is COMPLETE — the row does not refuse a merge for main being red before it |
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

**Two rows are now mechanized, and only two.**

- §2's `audit.py handback` exits non-zero on a code branch reporting no review, so THAT refusal
  is a command's exit code rather than a seat's memory — and `review_artifact_coverage` reads the
  same token off the persisted artifact afterwards, so a review claimed at the queue and absent
  from the record is visible later too. The verdict reads the LINE: it cannot tell a review that
  ran from a line that says one did.
- Row **2d**'s `merge_receipt.py require` exits non-zero on a merge in the range that no complete
  receipt names (`[#750]`). Its own honest limit is the mirror of the handback one: it reads the
  LEDGER, so it cannot tell a merge that was itemised from a receipt that says it was. What it
  closes is the silent case — a merge that landed with no receipt at all, which until `[#750]`
  nothing could even ask about, because a receipt named no merge.

Everything else on the checklist above is still an integrator running a list.
