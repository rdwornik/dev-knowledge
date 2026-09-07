# ADR-118: One graph — `file_purpose_graph.py` is the repo graph; organs are views; LLMs are methods on the structure, never its judge

- **Status:** Proposed <!-- The operator's ruling and the filing prompt call this state "DRAFT"; `Proposed` is the enum's spelling of it. NOT ratified. See "Status wording" below. -->
- **Date:** 2026-09-07
- **Decision tier:** Architecture (Path A — filings-drafted under `to-cc/DECLARE-GRAPH-2026-09-07.md`, a ruling-class declaration; awaiting the browser's `rule`)
- **Amends:** none. This ADR **states** a landing the tree already half-owns — FPG-1 exists and is unconsumed — and retires no mechanism by itself.
- **Related:** ADR-111 §2 (finding → intake → ratification is the only path to a row); ADR-41 (groom cadence, 21 d); ADR-98 (intake pipeline); ADR-108 §A (question routing) and §B (spec before build); ADR-112 Tier L (library-first adoptions are fit-assessed before adoption); ADR-28 / ADR-36 (core invariant #4 — Layer 2 never executes); intake **#40** (the carrier, re-opened by this ruling), intakes **#86** (`orphan_census`) and **#87** (catalog + resolver), intake **#73** (shape spec — genre → home), intake **#62** (the L0 layer); `[#616]` (the flip-condition instrument this ADR carries).
- **Intake:** #40 — re-opened 2026-09-07 as the carrier of this ruling; #86 and #87 are its first two consumers.
- **Decommission:** the twelve private edge computations enumerated by the migration (W-G3). Each is retired **only** by the lane that proves its edge set is a subset of FPG-1 (diff = 0) — nothing is removed by this ADR's acceptance.
- **Source:** `to-browser/DIGEST-2026-09-07-repo-graph.md` §A1–A3 (the measurement), ruled at `to-cc/DECLARE-GRAPH-2026-09-07.md` (browser seat, operator's instruction, ruling-class). Drafted by seat **filings-N3**, 2026-09-07.

<!-- Decommission: the twelve private edge computations; retired per-lane under W-G3, not by this ADR. -->

> **Status wording — a deviation, recorded not hidden.** The filing prompt and the ruling both call
> this ADR a **DRAFT**. **`DRAFT` is not a member of this repo's ADR status enum** (`Explored, not
> adopted` · `Partially superseded` · `Superseded` · `Deprecated` · `Proposed` · `Accepted` ·
> `PARKED` — `docs/decisions/README.md` §"Status enum", enforced by `check_adr_status_grammar` at
> **TIER_COMMIT**). The literal string `DRAFT` is a **blocking** defect: `audit.py health` returns
> `DEGRADED` and the pre-commit `audit-health` hook refuses the commit, so an ADR spelled that way
> could not land at all. This is not a new discovery — it is the same deviation ADR-117 recorded on
> 2026-09-06, and it is repeated here rather than cross-referenced because a reader of *this* file
> should not have to open another to learn that its status word was chosen under a constraint.
> `Proposed` is the enum member meaning *recorded but not ratified*, which is what the ruling means
> by DRAFT. It is deliberately **NOT** `Accepted` — ratification stays the operator's act.

## Context

The graph this repo has been designing since intake #40 (2026-08-22) **already exists**. The
2026-09-07 digest measured it:

- `scripts/file_purpose_graph.py` — **FPG-1** — on a **declared** `rustworkx` dependency
  (`pyproject.toml:65`, `uv.lock:564`), imported at `file_purpose_graph.py:92` and
  `boot_frontier.py:57`.
- **1922 nodes, 12 664 edges, 12 edge kinds.**
- And, in the digest's own words, *"wired into NO gate, no check and no hook"*.

Meanwhile **twelve organs recompute edges on their own**. The corpus therefore holds thirteen
answers to "what cites what", twelve of them private, none of them reconciled, and the one built to
be authoritative consumed by nothing.

The visible price is `ecosystem/north-star.md`: a file with zero consumers that no organ noticed,
because `consumer_at_landing` watches only `docs/audits/`, the seal polices a new file's *home* and
not its *readers*, and templates carry no consumer edge at all (INBOX 034).

**This is not a design error. It is an unfinished landing** — which is why the act is to re-open
intake #40 rather than to file a new design.

Two further pressures converge here. First, the operator's path-management proposal (INBOX 035):
no hardcoded paths, a structure that knows every file with a description and usage statistics, a
cheap daily report, and *a Gemini model embedded in each node evaluating itself*. Reviewed against
named industry patterns, the core is right — logical identifiers plus a resolver (Bazel labels,
TypeScript `paths`, npm `exports`, Nix store paths) and a metadata catalog (Backstage, DataHub,
SBOM manifests) — and it is **the node table of the graph we already have**, not a second system.
Second, the part that is wrong-shaped: putting judgment inside every node. That is the question
this ADR must answer as a rule rather than case by case, because it will be asked again on every
future organ.

## Decision

**1 · `file_purpose_graph.py` (FPG-1) is THE repo graph.** No organ computes an edge set of its
own from this ruling forward. A new edge kind is added **to FPG-1**, never to a script.

**2 · Organs are views, not derivations.** An organ that needs an edge relation queries the graph.
`orphan_census` (intake #86) is the first: in-degree 0 over citation / generation / execution /
test / template edges ∧ not in a #73 genre allowlist ∧ no TRACE trigger within the groom cadence →
candidate; WARN on first sight, FAIL after 21 d without disposition; nightly Routine and ship-gate.

**3 · The catalog is node attributes on FPG-1, not a new store** (intake #87): `path · id · genre ·
one-line description · last content commit · in-degree · trigger count · owner`. Generated by
`gen_catalog.py`, **committed** as a derived copy registered in the U4 registry, and **diffed
nightly** — the diff *is* the daily report. A resolver `resolve(id) → path` makes citations
id-based; a link-check organ refuses path citations where an id exists (WARN → FAIL after the
cadence).

**4 · LLMs are methods on the structure, never its judge.** This clause is the paradigm, and it is
quoted **verbatim** from `to-cc/DECLARE-GRAPH-2026-09-07.md` §4 rather than paraphrased, because a
paraphrase of a rule about judgment is exactly the kind of drift the rule exists to prevent:

> 4. **LLM as a method on the structure, never as its judge (the paradigm, stated as a rule):** nodes gain `describe()` (Gemini/agy reader, batch, cached with locator + timestamp, CC-sampled) and `evaluate()` (grey zone only, returns proposal + evidence + confidence, stored as an attribute with provenance); `score()` stays deterministic and testable; no gate calls an LLM on its hot path. Data structures and design patterns stay the skeleton; models are decorators on it with recorded, re-evaluable outputs.

**5 · Migration is measured, not big-bang.** `W-G1` wire FPG-1 + `orphan_census` + tests (S) →
`W-G2` catalog + resolver (M) → `W-G3` migrate the twelve organs **one per lane**, each proving its
edge set is a **subset of FPG-1 (diff = 0)** before the old computation is retired → `W-G4` the
graph ships as a floor component (**pull**, fleet-uniform — #73 layout is identical everywhere, so
one implementation), and the first consumer report runs on `corp-monorepo`.

**6 · Intake #40's Done-when is now an observable:** *12 separate edge computations → 0; all organs
read FPG-1.* N = 12 is the measured baseline on `main` at ruling time plus the then-unmerged W2-U4
work — a count, not a slogan.

## Consequences

**Easier.**
- "What cites what" acquires **one** answer. A disagreement between two organs becomes impossible
  rather than merely unnoticed.
- A new organ costs a query, not an extractor — which is what makes `orphan_census` an S.
- The daily report is a graph **diff**, so change is legible without anyone reading a folder.
- The floor leg (W-G4) is a single implementation, because #73 makes the layout identical.

**Harder, and worth stating plainly.**
- **Twelve migrations, each owing a diff = 0 proof.** That is the real cost of this decision, and
  it is paid twelve times. A migration that *cannot* show diff = 0 has found a hole in FPG-1's edge
  coverage — which is a finding, and therefore work, not a licence to keep the private computation.
- **FPG-1 becomes load-bearing.** A tree it mis-parses now mis-answers every organ at once. The
  blast radius of a graph bug rises in exact proportion to the duplication removed.
- **The code layer is thin.** Intake #40's 2026-08-31 amendment measured it at **21 nodes**; an
  organ over `scripts/` inherits that thinness on day 1 and must say so rather than report a clean
  answer over a sparse graph.
- **`rustworkx` moves from a declared dependency to a hot one.** It is already declared and locked
  (ADR-106 binds any bump), but a dependency twelve organs sit on is a different risk class from one
  two modules import.
- **A committed derived copy diffs on every regeneration.** That is the point (the diff is the
  report) and it is also churn; U4 registration and byte-stability are what keep it honest.

**Explicitly unchanged.**
- Core invariant #4 stands: this is a hub-local graph, generator and validators — **no script drives
  state in a child repo**. W-G4 ships a component; it does not ship an executor.
- ADR-111 §2 stands: nothing here births a backlog row. The carrier is intake #40, still `DRAFT`.

## Flip-condition

Three observables, any one of which reverses a load-bearing part of this decision:

1. **The subset proof fails at scale.** If, across the first three W-G3 migrations, FPG-1 cannot
   reproduce a migrated organ's edge set (diff ≠ 0) **and** closing the gap requires an edge kind
   whose semantics are organ-specific rather than corpus-general, then "one graph" is the wrong
   granularity and the decision collapses to *one graph per layer with a declared join*. The
   measurement exists by construction: every W-G3 lane emits its diff.
2. **The graph becomes the bottleneck it replaced.** If FPG-1's build time on the live tree crosses
   the ship-gate's budget — so that organs querying it are slower than the twelve private
   computations they retired — the pull-everything-through-one-graph shape loses on cost and the
   answer becomes a cached/incremental store, i.e. a different design. Threshold to be fixed at
   W-G1 against the then-current gate budget, and recorded there rather than guessed here.
3. **The bounded-reader rule proves unbounded.** If the sampled fabrication count on `describe()`
   is non-zero at a rate that makes CC's spot-check the real gate, then a model is doing judgment
   under a description label, and §4's "reader, never judge" line has failed in practice — the
   `describe()` leg is withdrawn and node descriptions return to hand-authored or generator-derived
   text. The count is reported per pass, so this is observable rather than inferred.

**What would NOT flip it:** the arrival of a better graph library. Library-first (ADR-112 Tier L)
governs *which* implementation backs FPG-1; swapping `rustworkx` for a superior library changes the
implementation and leaves every clause above intact. "One graph" is a claim about how many answers
the corpus may hold, not about which package computes them.

## Alternatives considered

- **A URL-management engine — a hard path graph with a cache** (the operator's original framing).
  **Rejected**, INBOX 035 correction 2, and recorded here so it is not relitigated: once the
  identity is the **id** and the layout is identical everywhere (#73), *the resolver is a
  dictionary and the cache is git itself* — the commit history gives modification frequency for
  free, TRACE gives triggers. Build the id column and the resolver; let the graph carry the rest.
- **An LLM instance inside every node, evaluating itself on access** (the proposal's most
  distinctive part). **Rejected:** non-deterministic, costly per node, and untestable — three
  properties that disqualify a thing from being a gate. The "probably unused" score is mechanical
  and explainable, its formula lives in a table, and the test seeds the cases. The model keeps two
  bounded roles (batch description; grey-zone ranking as a **proposal**), which is what §4 states
  as a rule. A-25's mechanical-only rule stands and is not reopened.
- **A hub-only graph.** **Rejected:** the orphan problem is fleet-wide and #73 makes the layout
  identical, so a hub-only scope would buy a second implementation later at the price of a smaller
  one now. W-G4 ships it as a floor component.
- **Leave FPG-1 unconsumed and build `orphan_census` as its own extractor.** **Rejected** — this is
  the status quo generalised: it would make the count thirteen. It is named because it is the
  cheapest path for the next lane in a hurry, and cheapest-for-one-lane is precisely how twelve
  computations accumulated.
- **Big-bang migration of all twelve organs in one arc.** **Rejected:** no lane could prove diff = 0
  per organ, which is the only evidence that the retirement was safe. Twelve lanes is the cost of
  having twelve proofs.
- **Adopt a third-party graph** (GitNexus, repo-graph, Code-Graph-RAG — named in intake #40's
  2026-08-29 note). **Deferred, not rejected:** ADR-112 Tier L requires a fit-assessment against
  the existing measurement *before* adoption, and none of the three appears anywhere in this tree.
  The Flip-condition note above records why this is an implementation question rather than a
  challenge to the decision.
