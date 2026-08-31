# LANE batch-e-a1-single-file-folder-census — measure every single-file folder in the hub against Z-G5, and census what consumes each. Census only, no ruling, no deletion.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `cloud` — an off-machine lane, repo-bound and receipt-gated, on the `claude/` prefix.

```
Dispatch-CloudV2 LANE-batch-e-a1-single-file-folder-census.md -Title 'batch-e-a1-single-file-folder-census'
```

The operator runs the line above verbatim. The **whole file is the brief** — it travels in a
JSON body, so one file is one lane and never a multi-lane bundle — and the dispatch binds
Revision `main`. `Dispatch-CloudV2` carries no `-Effort` parameter, so this lane's tier is on
the record in the routing table above rather than on the command line. Permission mode is
`bypassPermissions`. A cloud session clones from `origin`, so every input this contract names
is pushed before dispatch: it cannot see an unpushed branch or a local file.

## Worktree pairing

slug `batch-e-a1-single-file-folder-census` -> branch `claude/batch-e-a1-single-file-folder-census` -> contract `LANE-batch-e-a1-single-file-folder-census.md`

One lane = one contract file = one branch, so an open lane resolves to the contract that
created it and an orphan is attributable at a glance (ADR-110, fifth per-lane requirement).
A cloud lane runs on the `claude/` prefix, not `worktree-`: the branch is created by the
cloud transport, not by a local worktree provisioner.

## Receipt gate

This lane runs off-machine, so it carries a receipt (`protocols/STANDING_RULINGS.md` Q5).
Both fields, checked as a conjunction — either one alone reports a success the other refutes:

- `git-source-resolves-non-empty:` `<the resolved git source, non-empty>`
- `first-assistant-text-echoed:` `<total line count of this brief, and its final line verbatim>`

A dispatch missing either half is treated as not having started, and is re-dispatched. The
lane also branches fresh off `origin/main` and leaves files it did not author and this
contract does not name exactly as found (Q4).

## Substrate sizing (freeze-time, measured)

The census sweeps the whole tracked tree: **2,761 tracked files / 42,083,797 B ~= 19.6M tokens
= 92x the 213,225-token budget** (75% of the 284.3k floor in `~/.claude/ROUTING.md`). It cannot
be packaged into one self-contained shot, and it needs multi-turn tree-walking where compaction
silently drops content — fatal for a census whose whole value is completeness. **CLOUD.**

## Write-scope (frozen)

**NONE — this lane writes no tree file.** Its entire output is one artifact returned by harvest,
printed in full as the final assistant message. **ZERO rows, ZERO tree writes, ZERO commits.**
If a hook or closure proposal invites a commit, decline and say the lane is read-only by contract.

## PREMISE CORRECTION CARRIED INTO THE CONTRACT (read this first)

The batch brief names this lane *"conflict/ single-file-folder consumer census"*. **There is no
`conflict/` directory** — not in this repo (0 tracked files under `conflict/`), not in any of the
six sibling fleet repos on the operator host, and no tracked `.md`/`.py`/`.yaml` file cites
`conflict/` as a path. Measured at freeze, 2026-08-31.

The subject is therefore **Z-G5's actual discipline** — `protocols/STANDING_RULINGS.md` Z-G5,
*"No single-file folders, ever"* — applied to the whole tracked tree. A freeze-time count gives
**44 tracked directories holding exactly one file**. That number is the starting point, not the
answer: some are legitimate (a generated sidecar, a sealed bundle), and saying which precisely
is the deliverable.

If you find evidence that `conflict/` existed and was removed, report it — do not reinstate it.

## Done-contract (immutable)

1. **Every single-file tracked directory enumerated**, with: path, the one file, its genre, the
   date it became single-file (from git history), and whether Z-G5 actually bites on it.
2. **Per folder, its CONSUMERS** — what reads that path: a validator, a gate, a generated index,
   a doc citation, a manifest. Distinguish a REAL CONSUMER (behaviour or content depends on the
   path) from a MENTION, and give the evidence for each classification.
3. **A disposition COLUMN, not a disposition ACT.** For each: `fold` / `keep-with-reason` /
   `retire`. **Measure, never delete a live source** — this lane removes nothing and proposes
   no commit.
4. **Name the Z-G5 exceptions the repo has already granted implicitly** — a folder that is
   single-file today and passes every gate is an exception nobody recorded. Those are the
   finding.

## Steps

1. Enumerate tracked single-file directories from `git ls-files`. Do not trust the number 44 —
   re-measure at HEAD and report any delta with the freeze figure.
2. For each, resolve consumers by searching the tracked tree for the path and its basename.
3. Classify REAL CONSUMER vs MENTION with evidence.
4. Print the census in full as the final message. It returns by harvest.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per contract
defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10): deviation-with-disclosure
is not a license — the disclosure discharges the reporting duty, it does not authorise the
deviation. **Report a refuted premise; do not repair it by inventing a subject.**

Gate note: a cloud image may carry the wrong `uv`; invoke `python3` directly and **declare that
you did**. Never report a gate result you did not observe. **This lane runs NO gate and asserts
none** — it is read-only by contract, so it carries no test leg.

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once at the merge (Q1).
- No edits outside this lane's declared footprint. Prose in English; hyphen-only names.
