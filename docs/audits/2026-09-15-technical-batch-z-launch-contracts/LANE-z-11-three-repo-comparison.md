# LANE lane-z-11-three-repo-comparison -- Read-only comparison of three public repos against this methodology: a matrix of gaps, rows worth closing, and an explicit list of what we will NOT adopt

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `cloud` -- an off-machine lane, repo-bound and receipt-gated, on the `claude/` prefix.

```
Dispatch-CloudV2 LANE-z-11-three-repo-comparison.md -Title 'lane-z-11-three-repo-comparison'
```

The operator runs the line above verbatim. The **whole file is the brief** -- it
travels in a JSON body, so one file is one lane and never a multi-lane bundle --
and the dispatch binds Revision `main`. `Dispatch-CloudV2` carries no `-Effort`
parameter, so this lane's tier is on the record in the routing table above
(`opus` / `high`) rather than on the command line. Permission
mode is `bypassPermissions`, as it is for an on-machine lane.
A cloud session clones from `origin`, so every input this contract names is
pushed before dispatch: it cannot see an unpushed branch or a local file.

## Worktree pairing

slug `lane-z-11-three-repo-comparison` -> branch `claude/lane-z-11-three-repo-comparison` -> contract `LANE-z-11-three-repo-comparison.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). A cloud lane runs on the `claude/` prefix, not `worktree-`: the branch is created
by the cloud transport, not by a local worktree provisioner.

## Receipt gate

This lane runs off-machine, so it carries a receipt (`protocols/STANDING_RULINGS.md` Q5).
Both fields, checked as a conjunction -- either one alone reports a success the other refutes:

- `git-source-resolves-non-empty:` `<the resolved git source, non-empty>`
- `first-assistant-text-echoed:` `<the session's first assistant text, echoed back>`

A dispatch missing either half is treated as not having started, and is
re-dispatched. The lane also branches fresh off `origin/main` and leaves files it
did not author and this contract does not name exactly as found (Q4).

## Done-contract (immutable)

1. A matrix of gaps across the three repos, each gap resolved to a concrete surface in THIS repo that would change.
2. Two explicit lists: rows worth closing (each a filed candidate), and what we will NOT adopt WITH the reason -- the second list is mandatory, so a later reader cannot re-litigate a rejection as an oversight.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted. This lane runs NO suite: substrate `cloud`
   carries no armed hook, and PLAYBOOK Ch8 Layer-1 Q1 routes gate-dependent work away
   from it -- a suite run there reports green about a tree no gate inspected.

## Decision budget

**V-2 -- this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license -- the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. Pick the three comparison repos and state WHY each earns the slot. **COMMIT**
2. Build the gap matrix, read-only. **COMMIT**
3. Write both lists -- adopt-candidates, and will-not-adopt-with-reason. **COMMIT, then STOP.**
4. Final: one end-of-lane artifact (what changed - proposed diffs - open items), `git stash list` EMPTY, **COMMIT, then STOP.** This lane declares substrate `cloud` and therefore runs NO gate: PLAYBOOK Ch8 Layer-1 Q1 routes gate-dependent work away from cloud because no hook is armed there, and a suite run in a cloud session would report green about a tree no gate inspected.

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch -- commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry -- that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration -- the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
