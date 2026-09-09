# LANE lane-v-664-delivery-spine — Wire FPG-1 as the delivery spine: persist the graph and make three queries refuse at commit tier.

| Model | Mode | Effort |
|---|---|---|
| opus | plan | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-v-664-delivery-spine LANE-v-664-delivery-spine.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #664 · lane-v-664-delivery-spine]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-v-664-delivery-spine` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-v-664-delivery-spine` -> branch `worktree-lane-v-664-delivery-spine` -> contract `LANE-v-664-delivery-spine.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Footprint and pins

**THE CONTRACT IS PASSED BY REPO PATH.** The dispatch line above carries the bare filename
because the 1:1 pairing gate requires it; the integrator dispatches with
`docs/audits/2026-09-08-technical-batch-v-launch-contracts/LANE-v-664-delivery-spine.md`.
Measured 2026-09-09: the `CLAUDE_PROMPTS_DIR` copies of the V-2, V-3 and V-4 contracts were each
about 700 B short of their frozen originals, missing the entire `AMEND-BATCH-V-002` block, so a
bare-filename dispatch resolves against the transport and can run a lane on a pre-amendment
contract.

**The row.** `[#664]`, filed on main at `3b50ea9f`, last task of `[S3]`. Read the row body
first — it is this contract's own summary and records three departures from DECLARE-SPINE
section 3 that this lane inherits.

**`DECLARE-RECOVERY-2026-09-09` calls the spine row `[#644]`, and that id is WRONG.** `[#644]`
belongs to lane V-4's "the 2026-08-29 deploy freeze has never been ruled" — a different, live
row. The DECLARE was written before V-4's twenty rows landed and predicted an id consumed in
between. Cite `[#664]`. Do not edit the DECLARE; do not close `[#644]`.

**This lane OWNS, and nothing outside it:**

- `scripts/file_purpose_graph.py` and any new module for persistence and the three queries
- `tests/` for the modules it touches
- `.pre-commit-config.yaml` — ONLY to add the hooks the three queries need
- `docs/audits/2026-09-09-technical-lane-v-664-delivery-spine.md` — the end-of-lane artifact

**PINNED OUT — touching any of these is a STOP:**

- `BACKLOG.md`, `tasks/`, `tasks/manifest.json` — `[#664]` is already filed; this lane files no
  row and closes none
- `docs/audits/README.md`, `ecosystem/organ-index.md`, `ecosystem/doc-counts.md` — the
  integrator regenerates once on the merged result (`[#590]`)
- `JOURNAL.md` — the integrator's surface (`STANDING_RULINGS.md` P-1)
- `ecosystem/organ-registry.yaml` — **the registry is a QUERY over the graph, not a file.** The
  2026-09-09 paste extending it to 216 rows is RETRACTED; writing rows into it is the exact
  defect this lane exists to end
- `ARCHITECTURE.md` prose — Ch2 is RENDERED by this lane's mechanism; the hand rewrite is step D
  of the recovery plan and a different lane
- every other lane's branch and worktree

## Done-contract (immutable)

1. **The graph is PERSISTED and rebuilt on every commit** — a queryable artifact (sqlite;
   stdlib, no new dependency). Print node and edge counts read back from the persisted artifact,
   never from an in-memory build. Baseline for comparison: 1922 nodes / 12 664 edges / 12 edge
   kinds (`ADR-118:34`). State the counts under the narrowed edge class and explain any delta.
2. **Three queries REFUSE at commit tier, each with a trip-test** — `orphan_census` ·
   `task_coverage` (a file node changed in the commit with no inbound `implements` edge from an
   OPEN task) · `process_list` (the traversal answering "all processes"; `ARCHITECTURE.md` Ch2
   rendered from it behind a freshness hook). A query that reports without refusing does not
   discharge this clause, and a test that passes on conforming input is not a trip-test.
3. **The edge computations are RE-MEASURED under section A.1's five-kind class** — citation,
   generation, template, test, script call-site — and driven toward 0, every organ holding one
   reading FPG-1 instead. **Do NOT inherit the integer 12:** `ff103444` withdrew that bar
   because 12 counted state gates the class excludes. Print the measured N; if it cannot reach
   0 here, print N-before and N-after and name every remaining site with its owner.
4. **The 32-vs-20 fixture gap is RULED, not rounded.** The census counts 32 orphans — 20
   script-class, 3 hooks, 9 commands and skills — while `orphan_census` as section 3 words it
   reaches the 20. Widen the node class, or give the other 12 their own queries; record which
   and why. "32 -> 0" against a 20-item predicate is unreachable by construction.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

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

1. Read `[#664]`, `ADR-118`, `docs/intake/2026-08-22-tech-document-dependency-graph-organ.md`
   (intake #40, as narrowed by `ff103444`), `docs/intake/2026-09-07-tech-orphan-census-organ.md`
   (intake #86) and `docs/audits/2026-09-08-technical-process-trigger-census.md`. Resolve every
   locator before trusting it; write the plan into the artifact. **COMMIT**
2. RED-first witnesses (ADR-108 section B): failing tests for the persistence round-trip and for
   each of the three refusals, before any build code. **COMMIT**
3. Persist the graph and wire the commit-time rebuild; print the counts. **COMMIT**
4. Land the three queries as refusals with their trip-tests; rule the 32-vs-20 gap. **COMMIT**
5. Re-measure the five-kind edge computations; migrate what fits the budget and name the rest
   with owners. **COMMIT**
3. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
- No YAML or markdown COPY of the graph. No LLM inside a query. No organ that parses what the
  graph already holds. No skill mandate landed as a graph row instead of a hook.
- No state gate migrated into the graph — corpus-structure edges ONLY (DECLARE-REVIEWS section
  A.1, as narrowed on main by `ff103444`). The spine anchor and the staged-ADD checks compare
  two trees and stay gates.
- **Never use `AskUserQuestion`** — a `--bg` lane wedges on it forever with no operator prompt
  visible. A blocking question goes into the artifact and the lane STOPs.

## Pointers and the merge gate

`[#664]` · `ADR-118` (`docs/decisions/ADR-118-one-graph-organs-are-views.md`) ·
DECLARE-SPINE-2026-09-09 section 3 · DECLARE-REVIEWS-2026-09-07 sections A.1-2 · intake #40 ·
intake #86 · `docs/audits/2026-09-08-technical-process-trigger-census.md` ·
`scripts/file_purpose_graph.py` · `[#618]` · `[#640]`.

**TERRA REVIEW IS A MERGE GATE, NOT A COURTESY.** Before STOP run
`codex exec review -m gpt-5.6-terra --base main`, read-only, and **loop until a pass returns
nothing** — the stopping rule is *stop when a pass returns nothing*, not *stop after one pass*.
Put the tally in the artifact in exactly this three-number form:

```
HIGH raw=N fixed=N unresolved=N
```

A one-number tally is `review=NONE` under the sitting's ruling 2, and the integrator reads it as
such. **A lane with unresolved HIGH does not merge** — it goes back to its author with the
findings. V-5 and V-8 were bounced on this gate this window.

Targeted tests only; the full suite runs once at integration (`[#528]`). `uv run --locked` on
every command — a bare `python` or `pytest` resolves nothing (ADR-106 section 4). This lane
merges **LAST** in batch V, per DECLARE-SPINE section 4.
