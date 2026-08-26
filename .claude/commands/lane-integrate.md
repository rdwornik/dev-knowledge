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

For each lane, in order:

```bash
git merge --no-ff worktree-lane-<letter>-<id>-<slug>
uv run --locked pytest -q --dist worksteal --max-worker-restart=0   # this lane's merge, on the merged tree
git worktree remove .claude/worktrees/lane-<letter>-<id>-<slug>
git worktree prune
git branch -d worktree-lane-<letter>-<id>-<slug>
```

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
| 3 | `git worktree list` == primary only | run it; one line of output |
| 4 | Manifest/packet archived | the lane manifest and end-of-batch packet are committed in the tree |
| 4b | Audits index regenerated once, after the last merge ([#590]) | `uv run --locked python scripts/gen_audit_index.py --check` exits 0 on the final merged `main`. It is `merge=ours`-pinned, so every merge leaves it stale by construction — this is the step that makes taking it out of the merge path safe rather than lossy |
| 5 | `git stash list` is empty | run it; empty output. An entry that stays gets a recorded disposition — never a silent pass, and never a blind `drop` |
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
