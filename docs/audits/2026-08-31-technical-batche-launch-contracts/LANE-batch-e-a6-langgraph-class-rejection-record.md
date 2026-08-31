# LANE batch-e-a6-langgraph-class-rejection-record — a recorded rejection for the orchestration-framework class, reconciled against every prior verdict. Record only, no build, no adoption.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `cloud` — an off-machine lane, repo-bound and receipt-gated, on the `claude/` prefix.

```
Dispatch-CloudV2 LANE-batch-e-a6-langgraph-class-rejection-record.md -Title 'batch-e-a6-langgraph-class-rejection-record'
```

The operator runs the line above verbatim. The **whole file is the brief** — it travels in a
JSON body, so one file is one lane and never a multi-lane bundle — and the dispatch binds
Revision `main`. `Dispatch-CloudV2` carries no `-Effort` parameter, so this lane's tier is on
the record in the routing table above rather than on the command line. Permission mode is
`bypassPermissions`. A cloud session clones from `origin`, so every input this contract names
is pushed before dispatch: it cannot see an unpushed branch or a local file.

## Worktree pairing

slug `batch-e-a6-langgraph-class-rejection-record` -> branch `claude/batch-e-a6-langgraph-class-rejection-record` -> contract `LANE-batch-e-a6-langgraph-class-rejection-record.md`

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

**14 tracked files mention LangGraph / LangChain / AutoGen / CrewAI**, and the reconcile leg must
resolve every prior verdict across `docs/audits/`, `docs/archive/`, `docs/decisions/` and
`docs/intake/` — a targeted sweep, not a whole-tree one. It would fit a single shot.
**Routed CLOUD by operator instruction (batch brief §1(A): parallel, zero local load), NOT on a
sizing argument** — stating the real reason rather than manufacturing one.

## Write-scope (frozen)

**NONE — this lane writes no tree file.** Its entire output is one artifact returned by harvest,
printed in full as the final assistant message. **ZERO rows, ZERO tree writes, ZERO commits.**
If a hook or closure proposal invites a commit, decline and say the lane is read-only by contract.

## The prior record this must reconcile against (resolve each before citing it)

- `docs/audits/2026-08-30-technical-autonomy-decision-tree.md` — CORRECTIONS-TO-THE-RECORD carries
  *"Orchestration frameworks — LangGraph, LangChain, AutoGen, CrewAI, Microsoft Agent Frame..."*
  as a correction, and separately DISCHARGES `pydantic-ai, openai-agents, smolagents, Google ADK`.
  **The class already has a partial verdict.** This lane makes it a RECORD, it does not re-decide it.
- `docs/archive/2026-04-24-multi-agent-debate-patterns.md:116` — the decision tree states this line
  still carries a claim about AutoGen that the tree calls stale ("AutoGen is abandonware").
  **Resolve that locator before repeating either claim.**
- ADR-111 §1(d) — recorded rejection as anti-relitigation is already ADR-carried. Cite the
  mechanism; do not re-invent it.
- The synthesis reason, quoted once because it covers most of the class:
  **"PLURALITY BUYS LITTLE; ASYMMETRY AND HETEROGENEITY BUY A LOT."**

## Done-contract (immutable)

1. **One rejection record, in the repo's recorded-rejection shape**, covering the
   orchestration-framework class: what is rejected, **the reason**, the evidence, and the
   **trigger that would reopen it** — a rejection with no reopening condition is a prejudice.
2. **Reconciled, not duplicated.** For every framework in the class, state whether a prior verdict
   already exists and where. Where one exists, the record CITES it. Only genuinely unverdicted
   members get a new verdict. **Reconcile-before-birth is the binding rule of this batch.**
3. **The class boundary drawn explicitly** — what counts as "LangGraph-class" and what does not.
   `pydantic-ai` and `smolagents` are already DISCHARGED, which is a different disposition from
   REJECTED; do not silently merge the two.
4. **NO BUILD, NO ADOPTION, NO TRIAL.** The brief says "no build" and it is load-bearing.
5. **Name the destination** — ADR, `protocols/STANDING_RULINGS.md`, or an audit under
   `docs/audits/` with a class in the closed enum. One destination, argued.
6. **No file written, no commit, no row.**

## Steps

1. Enumerate the class from the tracked tree; resolve every prior-verdict locator above.
2. Build the per-framework verdict reconciliation table (framework | prior verdict | where | new?).
3. Draft the rejection record with reason + reopening trigger.
4. Print it in full as the final message. It returns by harvest.

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
