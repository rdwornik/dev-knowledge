---
name: lane-integrate
description: Walk a batch's merge queue serially from the primary checkout, then run the four-item refuse-to-finish checklist mechanically — the batch does not close while an item is open.
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
uv run --locked pytest -q            # this lane's merge, on the merged tree
git worktree remove .claude/worktrees/lane-<letter>-<id>-<slug>
git worktree prune
git branch -d worktree-lane-<letter>-<id>-<slug>
```

- **One merge at a time.** A red suite stops the chain and surfaces — the next lane waits.
- **Teardown is part of the merge, not a follow-up** (MERGE IS ATOMIC; and teardown is *two*
  branches when a provisioning branch exists — `.claude/rules/git-discipline.md`).
- `git worktree remove` silently no-ops on a locked directory. Re-check rather than assume.
- A lane that will not be merged is **explicitly abandoned**: record the disposition and the
  reason. Silence is not a disposition.

## 3. The refuse-to-finish checklist

Run all four. The batch stays open while any one of them is open — this checklist is the
mechanical form of the close-out, so an item is checked because its command was run, not because
it seemed fine.

| # | Condition | How it is checked |
|---|---|---|
| 1 | Every lane branch merged-or-explicitly-abandoned | `git branch --list 'worktree-lane-*'` is empty, and every planned lane has a merge SHA or a recorded abandonment |
| 2 | Full suite run once on the merged result | `uv run --locked pytest -q` on the final merged `main`, verdict quoted |
| 3 | `git worktree list` == primary only | run it; one line of output |
| 4 | Manifest/packet archived | the lane manifest and end-of-batch packet are committed in the tree |

Then push, and confirm the tree is clean:

```bash
git push
git status --short
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
