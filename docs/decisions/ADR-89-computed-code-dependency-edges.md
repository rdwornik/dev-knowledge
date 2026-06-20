# ADR-89: Computed code-dependency edges — language-server reverse-dependency oracle

<!-- scope: meta -->

**Status:** Proposed
**Date:** 2026-06-20
**Decision tier:** Architecture (foundational doctrine — the **computed-edge** sibling to ADR-88's declared-edge paradigm). Ratification basis = the AI-Council deliberation recorded below, not architect-fiat; acceptance pending operator ratification.
**Deliberation basis:** the three 2026-06-19 dependency-arc AI-Council-CLI transcripts — `code-dependency-mechanism` · `doc-code-link-mechanism` · `change-propagation-deletion` (`92c09cc`, on `main`) — mapping onto this ADR's three edges. Consumes the 2026-06-20 Pyright reverse-dep oracle benchmark (`5ebf348`).
**Related:** ADR-88 (file-oriented dependency management — the *declared-edge* sibling; this is the *computed-edge* sibling under the same principle); ADR-85 (session→living-docs edge — same doctrine, different edge); ADR-87 (the architect↔CC equilibrium contract under which this task was dispatched); #170 (issue↔commit traceability — a **distinct** edge whose edge-model is ADR-88 OQ2's open question, owned by #170's own ADR; **not** this edge)
**Decommission:** none
**Source:** Architect intent-spec (ADR-87 equilibrium contract), 2026-06-20; the deliberation basis above.

## Context

ADR-88 named the file-oriented coherence paradigm and established the **doc→doc** edge as a
*declared* edge (`reconciled_with` frontmatter; the verdict held by machinery — its Principle 2,
*deterministic trigger + AI per-site verdict + human signature*). doc→doc is declared because
prose coherence **cannot be computed**: only a reader — an AI, then a human — can judge whether a
dependent document is still coherent after the spec it depends on changes.

The **code→code** edge is different in kind. "Which symbols reference a changed symbol" is not a
matter of judgment — it is **derivable from the source itself**. Declaring it the way doc→doc is
declared would duplicate ground truth the code already carries, and the declaration would rot the
moment the code moved. So the real question for the code edge was never "reuse `reconciled_with`
or not" — it was: **can a deterministic tool compute the edge well enough that declaring it is
unnecessary?**

The 2026-06-20 Pyright reverse-dep oracle benchmark
(`docs/audits/2026-06-20-pyright-reverse-dep-oracle-findings.md`) answered that empirically for
this repo: **GO** — a headless language server's workspace index *is* the code→code
reverse-dependency oracle; no custom code graph is warranted here. This ADR records the doctrine
that consumes that verdict. It is the **computed-edge sibling to ADR-88**: the same paradigm, the
opposite mechanism, applied to a different edge.

## Decision

This ADR records one organizing principle and three adoptions.

### 1. The organizing principle — declare what you cannot compute; compute what you can

Both siblings sit under this rule. It assigns each dependency-edge type to a mechanism by asking
a single question: *can the edge be computed deterministically from what is already in the repo?*

- **doc→doc → declared** (`reconciled_with`, ADR-88). Prose coherence is a judgment, not a
  computation; the edge is declared and the dependent is re-verdicted by an AI + human.
- **code→code → computed** (language-server reverse-dependency), **never `reconciled_with`**.
  The edge is derivable from source; declaring it would duplicate ground truth and rot.
- **doc→code → declared** (a stable ID-scheme — a later build under this frame). The link from a
  prose document to the code it describes cannot be computed from either side — neither names the
  other in a machine-resolvable way — so it must be declared. Its ID-scheme is owed as a separate
  build; this ADR only places it under the frame.

The **unit of dependency differs by edge type** — the *document/file* for the doc edge (ADR-88),
the **symbol** for the code edge — and that difference is a *consequence* of compute-vs-declare,
not a contradiction between the siblings. A computed edge can be symbol-granular because the
oracle resolves symbols; a declared edge is file-granular because a human declares files.

### 2. Adopt a headless language server (Pyright) as the code→code reverse-dependency oracle

- **`references()` is the primary reverse-dependency query.** Given a changed symbol, the oracle
  returns its reference set — the dependents that may need attention. Cold-start readiness is the
  only standing cost (~4 s, once per session).
- **Call-hierarchy (`incomingCalls`) is optional / secondary** — useful for caller-graph
  questions, but it carries a one-time warm-up `references()` does not (below). Prefer
  `references()` unless caller-graph structure is specifically needed.
- **Reject a custom code-knowledge graph** (a `codemap`, a `codebase-memory-mcp`, or any bespoke
  symbol/document graph) **for this repo.** The benchmark closed it: a language server already
  maintains a semantic workspace index, resolves references **semantically, not textually** (the
  decisive signal — the symbol `main`, defined in 34 files, resolved to exactly **2** references,
  not a textual ~68), and every closure number lands inside an interactive-edit budget by one-to-
  three orders of magnitude. A custom graph is redundant build-and-maintain cost against a tool
  that already does it better. (This is ADR-88 Principle 4 — *narrow-first / curated over
  exhaustive* — applied to the code edge.)

### 3. Enforcement legs scale to the deterministic verifier's strength per edge type

ADR-88 Principle 2 gives the enforcement vocabulary: *deterministic trigger + AI per-site verdict
+ human signature.* Those three legs are **not fixed weights** — they scale to how much the
deterministic verifier can actually decide for a given edge:

- On the **code edge** the deterministic leg is **strong**: the build compiles or fails, and the
  oracle resolves the reference set semantically and completely (within its limits, below). So the
  **AI-verdict and human-signature legs shrink toward zero** — there is little prose coherence to
  judge; the computed answer is close to dispositive.
- On the **doc edge** the deterministic leg only *triggers* (it detects that a depended-on spec
  changed); it **cannot** decide whether the dependent prose is still coherent. There the
  **AI-verdict carries the load**, and the human signs.

The doctrine: **spend AI-verdict and human-signature budget where the deterministic leg is weak
(the doc edge), not where it is strong (the code edge).** A strong computed oracle is precisely
what *lets* the other two legs shrink.

## The benchmark verdict — normative constraints

This ADR adopts the benchmark's **GO** verdict and binds its three carried-forward limits as
**normative constraints on any code-edge build** — not as footnotes. (Source:
`docs/audits/2026-06-20-pyright-reverse-dep-oracle-findings.md`.)

- **Repo-scoped — numbers do not extrapolate.** The closure numbers are for **this repo** (34
  `.py` files, ~8k LOC, 286 symbols). Cold-start, resident memory, and worst-case payload grow
  with workspace size and will not extrapolate linearly. **Reusing the oracle in a large child
  repo (e.g. `corp-monorepo`) requires a fresh measurement there — never extrapolation from this
  spike.**
- **Static-Python-only — the blind spots are doctrine, not omissions.** `references()` /
  call-hierarchy see only **statically resolvable Python**. Dynamic dispatch, `getattr`/`setattr`,
  **string-keyed registries (`_SPEC_REGISTRY`-style dispatch)**, reflection, and monkeypatching are
  **invisible**, as are **all cross-language edges** — markdown→script, hook-wiring in
  `settings.json` / `.pre-commit-config.yaml`, plugin manifests. The oracle is sound for
  **code→code static edges only**, and must **never** be presented as catching the dynamic or
  cross-language edges. Those fall to other nets: **tests (the runtime net), the doc→code declared
  scheme, and incremental hand-maintained registries.**
- **Call-hierarchy warm-up (~8 s, one-time).** The first `incomingCalls` builds the call graph
  (~8 s, once); `references()` has no comparable cliff. **Prefer `references()`**, or budget the
  one-time warm-up explicitly if call-hierarchy is used.

And one constraint this ADR adds on top of the benchmark:

- **Provenance metadata is required on every oracle answer.** Any reverse-dependency result the
  build surfaces to an agent or a human must carry **the git rev it was computed against, the set
  of dirty / uncommitted files, and a truncation / completeness caveat** ("result complete" vs
  "index still warming / partial"). The whole value of a computed edge is that it reflects
  *current, complete* state; an answer without provenance is unsound to act on, because the
  consumer cannot tell whether it acted on stale or partial facts. This is the computed-edge
  analogue of ADR-88's *graph-in-repo, not in-model* — the answer declares the state it was
  computed from.

## Relationships

- **ADR-88 (the declared-edge sibling).** This ADR and ADR-88 are two halves of one paradigm:
  ADR-88 holds the *declared* edge (doc→doc), this holds the *computed* edge (code→code), both
  under "declare what you cannot compute; compute what you can." Read them together. (ADR-88 is
  **Proposed**; its back-reference to this ADR lands at its ratification edit, per the immutability
  convention — this ADR carries the forward link now.)
- **ADR-85 / ADR-87.** The Stop-gate (ADR-85) is the same coherence doctrine on the
  session→living-docs edge; the architect↔CC equilibrium contract (ADR-87) applies it to the human
  process. The enforcement-leg-scaling principle here generalizes ADR-85's split — a hard
  deterministic leg on the JOURNAL edge, an advisory leg where the deterministic check is weaker.
- **#170 (issue↔commit traceability) — a distinct edge, NOT resolved here.** ADR-88 OQ2 asks
  whether the **#170 traceability spine** (issue-ID↔commit) reuses `reconciled_with` or defines its
  own — and that is an **open design question owned by #170's own traceability-spine ADR.** This
  ADR makes **no claim** about #170's edge-model (neither declared nor computed): the code→code
  edge resolved here is a **different, third edge**, unnamed in ADR-88. The "declare vs. compute"
  principle is offered as a *frame* #170's ADR may find useful — but #170's resolution is
  explicitly left open.

## Scope — what this does NOT cover (do-not-build is doctrine)

Per ADR-88 Principle 5, the boundary is a first-class decision:

- **No custom code-knowledge graph / `codemap` / `codebase-memory-mcp`** for this repo —
  benchmark-rejected (the language-server index suffices).
- **No oracle coverage of dynamic or cross-language edges** — the static-Python limit is
  permanent; those edges are held by tests + the doc→code declared scheme + incremental
  registries, not by this oracle.
- **No tooling is wired by this ADR.** This is **doctrine only.** The build — the oracle wrapper,
  the provenance payload, any trigger / gate that consumes `references()` — is a separate, later
  task ("Track A"), undertaken only after this doctrine is ratified and filed as its own backlog
  item.
- **No child-repo reuse without fresh measurement** (the repo-scoped limit).
- **No promotion of a code-edge check to a hard gate by default** — like ADR-88's #181, any
  advisory→gate promotion is data-gated on observed value.

## Consequences

- The code edge gains a deterministic, semantically-correct reverse-dependency oracle with **zero
  declaration burden and no rot** — the edge is recomputed from source on demand.
- **"Can it be computed?" becomes the standing test for any new edge type.** Compute when you can
  (cheap, self-maintaining, exact); declare only what you cannot (prose coherence, issue↔commit,
  doc→code).
- The **static-Python blind spot is a permanent, recorded limit.** The dynamic / cross-language
  surface is explicitly out of the oracle's scope and held by other nets — naming this prevents a
  false sense of total coverage.
- **Provenance-on-every-answer is a hard requirement**, not an option — a computed answer that
  does not declare its git rev / dirty set / completeness is unsound to act on.
- **Enforcement-leg scaling frees AI-verdict budget for where it is load-bearing** (the doc edge),
  instead of spending it re-judging a code edge the oracle already settles.
- A custom code-graph build is **explicitly off the table** for this repo, removing a tempting but
  redundant direction.

## Open questions (carried — resolve before Accepted)

1. **doc→code ID-scheme.** The declared doc→code edge needs a stable ID-scheme (how a prose doc
   names the code it describes, and the reverse). Deferred to a later build under this frame; not
   designed here.
2. **Oracle-wrapper provenance payload + truncation policy.** The exact shape of the required
   provenance metadata (rev, dirty set, completeness / truncation signalling) is a Track-A build
   decision.
   **— RESOLVED 2026-06-20 (#193).** The Track-A oracle (`scripts/reverse_dep_oracle.py`) shipped
   the `reverse-dep-oracle/v1` schema, and its provenance payload *is* the resolution. Every answer
   envelope carries a mandatory `provenance` block (`_provenance()`): **`git_rev`** (HEAD),
   **`dirty`** + **`dirty_files`** (the uncommitted set), **`reflects: "working-tree"`** (the answer
   is computed against the working tree via `didOpen`, NOT committed state at `git_rev` — the two
   differ whenever `dirty`), **`completeness`** (`complete` | `partial` | `not-computed` — the
   truncation signal: `partial` when the readiness deadline is hit before two stable reference
   counts), and the **three mandatory honest-limit caveats** stated on *every* answer —
   **static-Python-only** and **repo-scoped** (two of the benchmark's normative limits) plus
   **working-tree** (this ADR's own provenance constraint; the benchmark's call-hierarchy-warmup
   limit does not apply because the oracle is `references()`-only). This discharges the ADR's
   "Provenance metadata is required on every oracle answer" constraint above. Source: the 2026-06-20
   Pyright reverse-dep oracle benchmark (`docs/audits/2026-06-20-pyright-reverse-dep-oracle-findings.md`)
   + the shipped tool. **OQ1 and OQ3 remain open — this ADR stays Proposed.**
3. **Advisory→gate promotion for code-edge checks.** Whether and when a code-edge
   reverse-dependency check becomes a hard gate is data-gated on observed drift value (the ADR-88
   #181 pattern), not pre-decided.

(ADR-88 OQ2 — the **#170** issue↔commit edge-model — is **not** an open question of *this* ADR; it
remains owned by #170's own traceability-spine ADR.)

## Links

- ADR-88 — file-oriented dependency management (the declared-edge sibling; read together).
- `docs/audits/2026-06-20-pyright-reverse-dep-oracle-findings.md` — the benchmark (GO verdict + the
  three limits this ADR makes normative).
- `docs/decisions/transcripts/council-out-20260619_232939-pick-council-decision-code-dependency-mechanism.md`
  — the code-dependency-mechanism debate (deliberation basis).
- `docs/decisions/transcripts/council-out-20260619_233239-pick-council-decision-doc-code-link-mechanism.md`
  — the doc→code-link-mechanism debate.
- `docs/decisions/transcripts/council-out-20260619_232639-pick-council-decision-change-propagation-deletion.md`
  — the change-propagation / deletion debate.
- ADR-87 — the architect↔CC equilibrium contract under which this ADR was dispatched.
- BACKLOG — the code-edge build ("Track A") is a new item, to be filed by the architect; this ADR
  is doctrine-only.
