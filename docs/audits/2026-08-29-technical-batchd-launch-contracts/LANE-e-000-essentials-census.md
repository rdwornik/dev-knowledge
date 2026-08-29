# LANE lane-e-000-essentials-census — a fleet-wide census of what actually consumes ESSENTIALS, separating real consumers from mentions. Census only, no ruling.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `cloud` — an off-machine lane, repo-bound and receipt-gated, on the `claude/` prefix.

```
Dispatch-CloudV2 LANE-e-000-essentials-census.md -Title 'lane-e-000-essentials-census'
```

The operator runs the line above verbatim. The **whole file is the brief** — it
travels in a JSON body, so one file is one lane and never a multi-lane bundle —
and the dispatch binds Revision `main`. `Dispatch-CloudV2` carries no `-Effort`
parameter, so this lane's tier is on the record in the routing table above
(`opus` / `high`) rather than on the command line. Permission
mode is `bypassPermissions`, as it is for an on-machine lane.
A cloud session clones from `origin`, so every input this contract names is
pushed before dispatch: it cannot see an unpushed branch or a local file.

## Worktree pairing

slug `lane-e-000-essentials-census` -> branch `claude/lane-e-000-essentials-census` -> contract `LANE-e-000-essentials-census.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). A cloud lane runs on the `claude/` prefix, not `worktree-`: the branch is created
by the cloud transport, not by a local worktree provisioner.

## Receipt gate

This lane runs off-machine, so it carries a receipt (`protocols/STANDING_RULINGS.md` Q5).
Both fields, checked as a conjunction — either one alone reports a success the other refutes:

- `git-source-resolves-non-empty:` `<the resolved git source, non-empty>`
- `first-assistant-text-echoed:` `<the session's first assistant text, echoed back>`

A dispatch missing either half is treated as not having started, and is
re-dispatched. The lane also branches fresh off `origin/main` and leaves files it
did not author and this contract does not name exactly as found (Q4).

## Write-scope (frozen)

**NONE — this lane writes no tree file.** Its entire output is one census artifact returned by
harvest.

**SUBSTRATE CHOSEN BY THE FREEZE-TIME SIZING (architect CUT-2), not by preference.** The rule:
package into ONE self-contained shot at <=75% of the 284.3k-token floor recorded in
`~/.claude/ROUTING.md`, else route CLOUD. At freeze, `grep -rl ESSENTIALS --include=*.md --include=*.py --include=*.yaml .` over tracked
files gave **575 files / 50,963,289 B ~= 22.9M tokens = 107.5x the 213,225-token budget**. It needs
multi-turn tree-walking, and multi-turn is where compaction silently drops content — fatal for a
census whose whole value is completeness. **CLOUD.**

## Done-contract (immutable)

1. **A census distinguishing REAL consumers from mentions, per fleet member.** A naive grep
   returns 575 files; that number is noise, and saying so precisely is the deliverable.
2. **This is NOT a ruling lane.** ESSENTIALS' fate is the architect's call, taken after this
   census lands. A census that arrives with a recommendation attached has exceeded its contract.
3. **ZERO rows, ZERO tree writes, ZERO commits.** If a hook or closure proposal invites a commit,
   decline and say the lane is read-only by contract.
4. Prose in English; hyphen-only names. **This lane runs NO gate and asserts none** — it is
   read-only by contract, so it carries no test leg and has no gate result to report. A cloud
   image may carry the wrong `uv`; if anything is run at all, invoke `python3` directly and
   **declare that you did**. Never report a gate result you did not observe.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. Enumerate candidate consumers, then classify each as REAL CONSUMER vs MENTION, with the
   evidence for the classification.
2. Group by fleet member (the nine ADR-104 ids).
3. Print the census in full as the final message. It returns by harvest.

Gate note: a cloud image may carry the wrong `uv`; invoke `python3` directly and **declare that
you did**. Never report a gate result you did not observe.

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
