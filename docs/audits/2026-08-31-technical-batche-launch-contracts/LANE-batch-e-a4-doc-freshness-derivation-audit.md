# LANE batch-e-a4-doc-freshness-derivation-audit — every living doc: its DECLARED freshness against what git actually says. Audit only, no repair, no re-stamp.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `cloud` — an off-machine lane, repo-bound and receipt-gated, on the `claude/` prefix.

```
Dispatch-CloudV2 LANE-batch-e-a4-doc-freshness-derivation-audit.md -Title 'batch-e-a4-doc-freshness-derivation-audit'
```

The operator runs the line above verbatim. The **whole file is the brief** — it travels in a
JSON body, so one file is one lane and never a multi-lane bundle — and the dispatch binds
Revision `main`. `Dispatch-CloudV2` carries no `-Effort` parameter, so this lane's tier is on
the record in the routing table above rather than on the command line. Permission mode is
`bypassPermissions`. A cloud session clones from `origin`, so every input this contract names
is pushed before dispatch: it cannot see an unpushed branch or a local file.

## Worktree pairing

slug `batch-e-a4-doc-freshness-derivation-audit` -> branch `claude/batch-e-a4-doc-freshness-derivation-audit` -> contract `LANE-batch-e-a4-doc-freshness-derivation-audit.md`

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

**493 tracked `.md` files carry a `last_reviewed` field**, and the audit compares each against
that file's git history — a per-file history walk over a corpus of 2,761 files / 42,083,797 B
~= 19.6M tokens = **92x the 213,225-token budget** (75% of the 284.3k floor in
`~/.claude/ROUTING.md`). The git-log leg cannot be packaged into a single shot at all. **CLOUD.**

## Write-scope (frozen)

**NONE — this lane writes no tree file.** Its entire output is one artifact returned by harvest,
printed in full as the final assistant message. **ZERO rows, ZERO tree writes, ZERO commits.**
If a hook or closure proposal invites a commit, decline and say the lane is read-only by contract.

## The premise this lane tests

The brief states it as fact: *"PLAYBOOK shows 2026-08-01 after last night's edits — hand-maintained
dates lie."* **Test it, do not assume it.** Report the measured figure for
`protocols/PLAYBOOK.md` explicitly — declared `last_reviewed` vs its true last content commit —
whichever way it comes out. A brief premise that survives measurement is worth as much as one
that falls.

## Done-contract (immutable)

1. **A table over every living doc**: path, declared `last_reviewed`, declared `version` (if any),
   last content-modifying commit date from git, and the **delta in days**. Sort by delta descending.
2. **Distinguish a CONTENT commit from a TOUCH.** A whitespace, regeneration or index-refresh
   commit is not a review-invalidating change. State the rule you used and apply it consistently —
   a delta computed off `git log -1` alone will over-report and is not the deliverable.
3. **The gated set named separately.** `scripts/canonical_docs.py::FRESHNESS_FILES` +
   `scripts/audit.py::_HUB_ONLY_FRESHNESS_FILES` compute the set the A2 freshness gate actually
   enforces. Report (a) gated-and-stale, (b) gated-and-fresh, (c) **ungated-and-stale** — class
   (c) is the finding that funds HY-1, because it is the part no gate is watching.
4. **Every doc carrying NO `last_reviewed` at all**, listed — an absent stamp is not a fresh one.
5. **A derivation design, as text**: how a `last_reviewed` could be DERIVED from git rather than
   hand-maintained, what it would break, and which of the 493 files could not be derived that way
   and why. HY-1 is the consumer; this lane drafts, it does not build.
6. **No file is re-stamped, no commit is proposed.** Measuring while repairing corrupts the measure.

## Steps

1. Compute the living-doc set. Read `canonical_docs.py` and `audit.py` for the gated set rather
   than guessing it.
2. Per file, walk git history and classify commits CONTENT vs TOUCH by your stated rule.
3. Build the table; segregate the three gated classes; list the unstamped.
4. Draft the derivation design.
5. Print the audit in full as the final message. It returns by harvest.

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
