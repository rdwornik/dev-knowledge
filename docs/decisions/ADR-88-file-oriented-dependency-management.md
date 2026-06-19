# ADR-88: File-oriented dependency management — markdown as a design pattern

<!-- scope: meta -->

**Status:** Proposed
**Date:** 2026-06-19
**Decision tier:** Architecture (Layer-1 architect authored + operator; Path A — direct authoring, no Council transcript). Capstone paradigm ADR; acceptance pending operator/Council ratification.
**Related:** ADR-28 (Layer-2 authority), ADR-85 (Stop-gate — same doctrine on the session→living-docs edge), ADR-86 (conformance dashboard), ADR-87 (architect↔CC contract — the human-process application), #131 (deployment test), #156 (durable hard edges), #172 (coherence-spine v1, closed), #179–#182 (the `coherence` serialize-group) + #183 (reparent), #170 (traceability edge — sibling)

## Context

`.dev-knowledge` already *has* the mechanism — the coherence spine v1 (#172, closed) — and a
roadmap (the `coherence` serialize-group #179–#182, plus the bare #183 reparent). What it lacks is
a **name for the paradigm**. The consequence: #179–#182 read as a loose feature list rather than
"extending a paradigm" — exactly the maximalism a VISION section would worsen. That is why this is
an **ADR, not a VISION** (the 2026-06-17 supplement directive: *"Name it — as an ADR, not a
VISION"*; a VISION invites the maximalism, an ADR earns the proven-in-miniature mechanism a
decision record and a coherent frame).

The driving goal is to **unify and encapsulate the way-of-working into one self-enforcing,
deployable whole** — the #131 deployment test (ai-council onboarding as the first target). The
methodology already exists and is mature; what it is *not* yet is **self-enforcing**. The build
sessions repeatedly showed the architect *bypassing* the methodology because correctness rode on
*remembering* to apply it. The named spine-failure — **"accepting inherited framing without
verifying against state"** — is the human/agent instance of the exact thing this paradigm
mechanizes for files: an **un-checked dependency edge**. Naming the paradigm turns scattered
coherence mechanisms into one doctrine that can be enforced and deployed.

## Decision

Treat **repo files — markdown documents first — as the unit of dependency.** A document's
dependencies on other documents are **declared edges in the repo** (frontmatter `reconciled_with` /
`Links`; `BACKLOG` `serialize-group` / `depends-on`). Coherence across those edges is held by
**machinery, not by memory.**

### Principles

1. **Coherence-by-mechanism, not by memory.** No correctness may depend on a human or agent
   *remembering* to update a dependent. If A depends on B and B changes, the system — not someone's
   recall — raises the coherence question.
2. **Three-part enforcement: deterministic trigger + AI per-site verdict + human signature.** The
   trigger (deterministic) detects the change; the AI renders a per-site verdict (is the dependent
   still coherent?); the human signature ratifies and owns. None alone suffices — deterministic
   can't judge prose coherence, AI can't be trusted to gate, human can't be trusted to remember.
3. **Graph-in-repo, not in-model.** Edges are durable file/frontmatter facts; the model *reads* the
   graph, never *holds* it. #156 made the hard edges (`serialize-group` / `depends-on`) durable;
   soft edges live as declared frontmatter, not model memory.
4. **Narrow-first / curated over exhaustive.** Do not graphify everything. Curated edges + grep beat
   a noisy full graph. Proven: the Phase-A graphify pilot — 3003 noisy nodes vs. a curated 10/15/4
   codemap, grep 2.5–5.6× cheaper — was rejected (`docs/audits/2026-06-04-graphify-pilot.md`, on
   corp-monorepo). Add an edge where drift has real cost, not by default.
5. **The boundary is doctrine.** What is deliberately *not* enforced or built is a first-class
   decision, not an omission (see Scope below). Rejected-by-design and recorded: monorepo-shared
   modules, cross-carrier symlinks, semantic/LLM dedup inside deterministic validators.

## The mechanism (proven in v1)

The coherence spine (#172) is the proof-in-miniature this ADR generalizes. Every part is live and
verified in-repo:

- `scripts/validate_reconciliation.py` — the **deterministic trigger**: a dependent declares
  `reconciled_with: <spec-id>@<version>` in frontmatter; the checker resolves the spec's current
  version from `_SPEC_REGISTRY` and flags a dependent whose declared version lags.
- `scripts/coherence_enumerator.py` — the **site enumerator**: given a flagged edge, it
  deterministically extracts every candidate reference site (sections, walkthrough steps, diagrams,
  commands, summaries) so a downstream LLM can verdict *each* one.
- `tests/test_coherence_integration.py` — the **closure metric**: mutate a depended-on spec (bump
  its version + add a required step) → the spine must flag the stale dependent and enumerate the
  missed sites. This is the hard test, not "tests pass."
- The live edge: `docs/handoffs/README.md` declares `reconciled_with: handoff-process@5.2`. The
  `coherence-nudge` pre-commit hook (non-blocking; logs `logs/coherence-nudge.log`) catches a spec
  changed *without* a version bump; the `reconciled_versions` audit check gates a stale declared
  version.

The Stop-gate (ADR-85) is the same doctrine on a different edge — the session → living-docs edge
(JOURNAL hard, BACKLOG advisory): change without coherence is *blocked*, not nudged. ADR-87 (the
architect↔CC equilibrium contract) is the same discipline applied to the *human* process.

## Failure classes this paradigm addresses

| # | Failure class | Current enforcement | Status |
|---|---|---|---|
| FC1 | Accepting inherited framing without verifying state (the spine-failure — the human/agent instance of an un-checked edge) | probe regime (forced live-state reads); the handoff supplement↔state reconcile | partial |
| FC2 | Cross-document staleness via *undeclared* prose-dependency edges | #179 (undeclared-edge scan) | filed |
| FC3 | Duplicate / uncoordinated filing | #187 (BACKLOG dedup-on-entry) | filed |
| FC4 | History-accretion bloat | #140 (doc-rot / grooming checker) | filed |

FC1's reconcile — the handoff machinery's own supplement↔state edge — is itself an instance of the
paradigm (an un-checked edge in the handoff process). It is already tracked under the handoff
serialize-group (#159/#164) and rides the unify goal; this ADR records it as in-scope of the
doctrine, not as a new task.

## Scope — what this does NOT cover (do-not-build is doctrine)

The boundary is a first-class decision (Principle 5). This list is canonical; changes to it are ADR
amendments, not silent drift. (For the repo-level non-goals this nests under, see VISION.md "Out of
scope (non-goals)".)

- **No exhaustive graphification** (Principle 4). Curated edges + grep, not a full symbol/document
  graph.
- **No monorepo-shared modules or cross-carrier symlinks.** Distribution stays carrier-based
  (ADR-71/72/73/74/78), not shared mutable state.
- **No semantic / LLM dedup inside deterministic validators.** #187 is a normalized-title
  token-overlap heuristic with a stated limit; the deterministic layer stays deterministic.
- **No `.out-of-scope/` folder yet.** Treating rejected-by-design scope as a first-class *folder* is
  a proposed extension, not an existing artifact — recorded here as a direction, not a claim.

## Relationships

- **ADR-28** — this paradigm operates at Layer 2 (governance authority). Deployment to child repos
  is the #131 test; the doctrine is what makes "deployable as one self-enforcing whole" meaningful.
- **ADR-85 / ADR-86** — the Stop-gate and the conformance dashboard are the same coherence doctrine
  on the session→living-docs edge and the cross-repo drift surface respectively.
- **ADR-87** — the architect↔CC equilibrium contract is the *human-process* application of the same
  discipline (declare the dependency the task touches; don't rely on recall).
- **#170 (traceability edge)** — the issue-ID↔commit edge is a **sibling** of the `reconciled_with`
  edge. Whether #170 reuses this edge model is an open design link (see Open questions).
- **Global ↔ local (cross-repo).** Which edges and contracts are global (owned in `.dev-knowledge`)
  versus per-repo (skills, gotchas, plugins, hooks) is the cross-repo dimension of the paradigm —
  the bridge between this ADR and the #131 pilot. A first-pass global/local contract is owed there.

## How the roadmap extends the paradigm (not ad-hoc features)

The `coherence` serialize-group is read as paradigm-extension, each item tagged to the edge it
enforces or the gate it waits on:

- **#179** — undeclared-edge inference (FC2): infer prose-only dependency edges and surface
  candidates for human confirmation.
- **#180** — transclusion / lead-with-removal (gated on DEC-04).
- **#181** — nudge-response: escape-hatch / deferred-hash / promote-to-gate (data-gated on
  `logs/coherence-nudge.log` firing signal).
- **#182** — folder-level dependency contracts (gated on DEC-07).
- **#183** (bare — *not* in the serialize-group) — reparent #169/#171/#166 under the coherence
  spine; evidence-gated (≥2 real drifts + a #169-fit decision). Deliberately not grouped or
  sequenced yet.

## Consequences

- New coherence work must declare which **edge** it enforces and which **failure class** it
  addresses — no ad-hoc "add a check."
- Declared-edge frontmatter (`reconciled_with`, and the `serialize-group` / `depends-on` schema)
  becomes the canonical coherence graph; validators read it, never reconstruct it.
- The do-not-build list is maintained *as part of this ADR* — scope changes are ADR amendments, not
  silent drift.
- A name exists for the paradigm, so the roadmap (#179–#182) and any future coherence mechanism read
  as "extending the doctrine" — the precondition for deploying the methodology as one self-enforcing
  whole (#131).

## Open questions (carried — resolve before Accepted)

1. **FC taxonomy completeness + order.** FC1–FC4 are verified against the live #179/#187/#140 scope;
   whether the list is complete (e.g. a cross-repo FC5) is open, to be checked against the #131
   pilot.
2. **#170 edge-model reuse.** Whether the traceability spine (#170 → #168) reuses the
   `reconciled_with` edge model or defines its own is an open design link.
3. **Global/local contract.** The first-pass global↔local edge/contract split (which coherence edges
   are hub-owned vs per-repo) is owed at the #131 pilot — the bridge between this ADR and deployment.
4. **#181 data-gate.** The nudge-response design waits on real `logs/coherence-nudge.log` firing
   signal; do not pre-decide escape-hatch vs promote-to-gate before the data exists.
