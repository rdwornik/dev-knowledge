# LANE batch-e-a7-agy-admission-and-quota-visibility — is `agy` admitted for the ANALYSIS role, and where would the operator see agy/Gemini quota burn? Status report only, no admission act.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `cloud` — an off-machine lane, repo-bound and receipt-gated, on the `claude/` prefix.

```
Dispatch-CloudV2 LANE-batch-e-a7-agy-admission-and-quota-visibility.md -Title 'batch-e-a7-agy-admission-and-quota-visibility'
```

The operator runs the line above verbatim. The **whole file is the brief** — it travels in a
JSON body, so one file is one lane and never a multi-lane bundle — and the dispatch binds
Revision `main`. `Dispatch-CloudV2` carries no `-Effort` parameter, so this lane's tier is on
the record in the routing table above rather than on the command line. Permission mode is
`bypassPermissions`. A cloud session clones from `origin`, so every input this contract names
is pushed before dispatch: it cannot see an unpushed branch or a local file.

## Worktree pairing

slug `batch-e-a7-agy-admission-and-quota-visibility` -> branch `claude/batch-e-a7-agy-admission-and-quota-visibility` -> contract `LANE-batch-e-a7-agy-admission-and-quota-visibility.md`

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

The admission half resolves from three hub registries plus the `[#578]` record; the quota half
needs a network read of live Google/agy documentation. Neither leg is large. **Routed CLOUD by
operator instruction (batch brief §1(A): parallel, zero local load), NOT on a sizing argument** —
and because the quota leg needs an unblocked network the operator host may not have.

## Write-scope (frozen)

**NONE — this lane writes no tree file.** Its entire output is one artifact returned by harvest,
printed in full as the final assistant message. **ZERO rows, ZERO tree writes, ZERO commits.**
If a hook or closure proposal invites a commit, decline and say the lane is read-only by contract.

## THE ADMISSION ANSWER IS ALREADY IN THE TREE — reconcile, do not re-derive

`ecosystem/provider-registry.yaml`, the `antigravity` row, states it in the repo's own words:

> **"NO ROLE, AND THE CONSEQUENCE IS NAMED RATHER THAN ACTED ON. Admitting `agy` would give the
> REFUSED `gemini-3.7-flash` family a SECOND route to this fleet... That is a `[#578]` RERUN
> QUESTION, not a registry act: this row records that the route exists and stops there."**

So the freeze-time answer to *"is agy admitted for the analysis role?"* is **NO — registered
present, deliberately unroled.** Your job is to **verify that is still true at HEAD** and to make
the consequence legible, not to re-discover it and not to change it.

**This lane does NOT admit `agy`.** Admission is an operator/architect act gated on `[#578]`.
A status report that arrives having admitted anything has exceeded its contract.

## Done-contract (immutable)

1. **The admission status, verified at HEAD**, across every surface that could carry it:
   `ecosystem/provider-registry.yaml`, `ecosystem/routing-table.yaml`,
   `ecosystem/substrate-registry.yaml`, `~/.claude/ROUTING.md`'s in-repo counterpart, and
   `protocols/STANDING_RULINGS.md`. If two surfaces disagree, **that disagreement is the finding**.
2. **What admitting it for the ANALYSIS role would actually unblock**, concretely: the batch brief
   routes *"whole-repo analysis -> agy when admitted"*, and this batch's coherence/orphan scan is
   the first would-be consumer. State what that scan would cost on each alternative route.
3. **The `[#578]` rerun question resolved to its live status** — open, deferred, or closed — by
   reading `tasks/`, not by assuming.
4. **THE QUOTA CURVE — this is what the operator specifically asked for.** Answer, with evidence:
   where does agy/Gemini consumption become VISIBLE? A console page, a CLI verb, an API endpoint,
   a billing surface. Name the exact surface and how to reach it. If the network is blocked,
   **say the fetch failed and report what the hub already records** — a fabricated URL is worse
   than a declared gap. State plainly which facts came from the network and which from the tree.
5. **A drafted `quota-source` field spec** for whichever registry should carry it — the decision
   tree carries *"The quota-source field"* as a CORRECTION-TO-THE-RECORD, so reconcile against
   that correction before proposing anything.
6. **No file written, no commit, no row, no registry edit.**

## Steps

1. Read the five surfaces in item 1; build the agreement table.
2. Resolve `[#578]` and the decision-tree quota-source correction.
3. Attempt the live-docs fetch for the quota surface; declare success or failure explicitly.
4. Draft the `quota-source` field spec.
5. Print the report in full as the final message. It returns by harvest.

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
