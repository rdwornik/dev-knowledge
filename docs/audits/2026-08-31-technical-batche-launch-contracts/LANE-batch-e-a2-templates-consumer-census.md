# LANE batch-e-a2-templates-consumer-census — a consumer census of templates/, separating live carriers from dead stock, with a retention rule proposed per class. Census only, no ruling.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `cloud` — an off-machine lane, repo-bound and receipt-gated, on the `claude/` prefix.

```
Dispatch-CloudV2 LANE-batch-e-a2-templates-consumer-census.md -Title 'batch-e-a2-templates-consumer-census'
```

The operator runs the line above verbatim. The **whole file is the brief** — it travels in a
JSON body, so one file is one lane and never a multi-lane bundle — and the dispatch binds
Revision `main`. `Dispatch-CloudV2` carries no `-Effort` parameter, so this lane's tier is on
the record in the routing table above rather than on the command line. Permission mode is
`bypassPermissions`. A cloud session clones from `origin`, so every input this contract names
is pushed before dispatch: it cannot see an unpushed branch or a local file.

## Worktree pairing

slug `batch-e-a2-templates-consumer-census` -> branch `claude/batch-e-a2-templates-consumer-census` -> contract `LANE-batch-e-a2-templates-consumer-census.md`

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

`templates/` holds **47 tracked files**, but the census question is who CONSUMES them, and that
sweeps the tree: **554 tracked files reference `templates/`**, inside a corpus of 2,761 files /
42,083,797 B ~= 19.6M tokens = **92x the 213,225-token budget** (75% of the 284.3k floor in
`~/.claude/ROUTING.md`). Multi-turn tree-walking, where compaction silently drops content.
**CLOUD.**

## Write-scope (frozen)

**NONE — this lane writes no tree file.** Its entire output is one artifact returned by harvest,
printed in full as the final assistant message. **ZERO rows, ZERO tree writes, ZERO commits.**
If a hook or closure proposal invites a commit, decline and say the lane is read-only by contract.

## Done-contract (immutable)

1. **Every file under `templates/` classified** as: **CARRIER** (shipped to a consumer by a
   `deploy/manifest-v*.yaml` entry), **HUB-LOCAL LIVE** (read by a hub generator, validator or
   command), **REFERENCE-ONLY** (cited by docs, read by nothing), or **DEAD STOCK** (no consumer
   at all). Evidence per classification — the citing line, the manifest entry, the resolving code.
2. **The t-shirt-size and workspace templates specifically located and verdicted.** The brief
   names them as retirement candidates. Confirm they exist before verdicting them; if they do
   not, say so — that is a refuted premise, and it is reported, not repaired.
3. **A RETENTION RULE per class, drafted as text** — a mechanism ("a template with no consumer
   for N days is retired by <organ>"), not a one-off cleanup list. The rule is the deliverable;
   the current list is its first input.
4. **`templates/archive/` treated separately** — an already-archived template is not dead stock,
   and conflating the two would propose deleting the record.
5. **No live source is deleted and no commit is proposed.** Measure only.

## Steps

1. Enumerate `templates/` from `git ls-files`. Re-measure the 47 figure at HEAD; report any delta.
2. Resolve consumers per file: search the tracked tree for the path, the basename, and the
   basename minus extension. Check `deploy/manifest-v*.yaml` for carrier entries explicitly.
3. Classify with evidence. Draft the retention rules.
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
