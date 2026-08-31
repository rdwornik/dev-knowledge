# LANE batch-e-a5-harness-portability-map — turn AUT-R4-A's harness-portability finding into a drafted doctrine section. Draft only, no ruling, no landing.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `cloud` — an off-machine lane, repo-bound and receipt-gated, on the `claude/` prefix.

```
Dispatch-CloudV2 LANE-batch-e-a5-harness-portability-map.md -Title 'batch-e-a5-harness-portability-map'
```

The operator runs the line above verbatim. The **whole file is the brief** — it travels in a
JSON body, so one file is one lane and never a multi-lane bundle — and the dispatch binds
Revision `main`. `Dispatch-CloudV2` carries no `-Effort` parameter, so this lane's tier is on
the record in the routing table above rather than on the command line. Permission mode is
`bypassPermissions`. A cloud session clones from `origin`, so every input this contract names
is pushed before dispatch: it cannot see an unpushed branch or a local file.

## Worktree pairing

slug `batch-e-a5-harness-portability-map` -> branch `claude/batch-e-a5-harness-portability-map` -> contract `LANE-batch-e-a5-harness-portability-map.md`

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

The primary input is one audit —
`docs/audits/2026-08-29-technical-aut-r4a-harness-evals-observability.md` — and it fits a single
shot comfortably. **This lane is routed CLOUD by operator instruction (batch brief §1(A):
"dispatch FIRST, all in parallel, zero local load"), NOT because it exceeds the 213,225-token
budget.** Recording the real reason rather than manufacturing a sizing argument: the routing is
a parallelism decision, and it is honest to say so.

## Write-scope (frozen)

**NONE — this lane writes no tree file.** Its entire output is one artifact returned by harvest,
printed in full as the final assistant message. **ZERO rows, ZERO tree writes, ZERO commits.**
If a hook or closure proposal invites a commit, decline and say the lane is read-only by contract.

## Where this comes from

The autonomy decision tree (`docs/audits/2026-08-30-technical-autonomy-decision-tree.md`) routes
*"The harness-portability map"* as **`not-a-candidate`** — the single leaf of that class among 55.
Read that routing before you draft: `not-a-candidate` means it is not a backlog row, **not** that
it is worthless. The brief asks for it as a **doctrine section draft**, which is exactly the shape
a `not-a-candidate` finding takes when it is real but unfileable.

## Done-contract (immutable)

1. **A drafted doctrine section, in full prose, ready to be cut by the architect** — titled,
   scoped, and written in this repo's voice (assertive, evidence-citing, no hedging).
2. **It answers one question:** which parts of this repo's instruction corpus are PORTABLE across
   harnesses (Claude Code, Codex, agy/Gemini, a cloud session, a codespace) and which are
   harness-bound — and **what the boundary rule is**, stated so a future author can apply it
   without asking.
3. **Reconciled against what already exists, before a word is written.** At minimum:
   `AGENTS.md` (the ADR-115 portable layer), ADR-115 itself, `ecosystem/provider-registry.yaml`
   (the nine provider/model seams), and `deploy/global-instructions-codex.md`. If the doctrine
   already exists somewhere, **say so and point at it instead of restating it** — a duplicated
   doctrine section is the failure mode this repo spends most of its enforcement budget preventing.
4. **Name its destination.** PLAYBOOK chapter, an ADR, or `AGENTS.md`. One destination, argued.
5. **No file written, no commit, no row.** The draft returns by harvest as text.

## Steps

1. Read the AUT-R4-A audit and the decision-tree leaf.
2. Reconcile against `AGENTS.md`, ADR-115, `ecosystem/provider-registry.yaml`, ADR-101.
3. Draft the section. State the boundary rule as a rule, not as a description.
4. Print the draft in full as the final message. It returns by harvest.

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
