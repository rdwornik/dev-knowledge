# ADR-109: Fleet desired-state contract v1 — schema, registry dissolution, and the §E functional requirement

**Status:** Accepted (ratified 2026-07-31 — accepted by operator GO, architect session; ADR-94 status-line-only edit)
**Date:** 2026-07-31
**Decision tier:** Architecture (Path A — authored by CC under the [#382] execution brief; plan
ratified at the 2026-07-31 architect checkpoint with amendments F1/F2; **ratification is a
separate operator act**)
**Intake:** #22 §E (transcribed verbatim in §1; ratified by promotion into this ADR — the doc
stays SEED, §C/§D/§F–§H open) · #16 §1–§3 + §5 (declared consumer (b); trigger fired at this
arc's open — disposition `active`, NOT flipped CONSUMED per amendment F1: §6's plan spine stays
live)
**Related:** ADR-104 (matrix width — 5 fleet repos, partial fold; not reopened) · ADR-105
(activation-needs-a-consumer rule, reused for deferrals here) · ADR-106 (uv toolchain; the
schema's deps ride its lock discipline) · ADR-107 (§5 findings consumed in §3; §6.2 pending in
§4; §6.3 witnessed in §5) · ADR-108 (the routing doctrine this arc runs under) · [#382] (this
arc) · [#383]/[#385] (downstream consumers) · [#451] (the CA layer-edge enforcement pointer,
cited in §6) · [#424]/[#452] (edge-parser defects the schema preserves raw) · [#455]
(registry.md drift checker — dissolved by §2) · [#429] (concurrent-allocation residual)
**Evidence base:** `docs/audits/2026-07-31-technical-382-registry-prep-dossier.md` (the
registry census this ADR rules over — cited below as "dossier") ·
`docs/audits/2026-07-28-technical-382-charter.md` (the arc contract skeleton) ·
`docs/audits/2026-07-31-technical-382-schema-derivation-sol.md` (sol's independent
derivation, adjudicated in §7)
**Decommission:** `ecosystem/registry.md` loses authority (§2 — retirement of the file itself
is loader-wave/[#383] work, recorded there); [#455] becomes moot when §2 lands.

## Context

The fleet's desired state is declared today across four hand-divergent registries plus one
state file, five membership sets, four lifecycle vocabularies, five provenance grammars, and
twelve edge-declaration shapes across nine identity spaces (dossier §i–§ii, conflicts C1–C8,
gaps G1–G15). The operator's functional requirement (§1) asks for one queryable, versioned
contract. Intake #16 §2 rules the architecture: the Terraform **model**, not the tool —
declarative config as typed data (pydantic), state in git, `apply` = the existing
regenerate-and-diff machinery. The [#433] pilot ran first (pilot-precedes-contract ruling,
2026-07-26) and its seven schema findings route here owed-either-way (ADR-107 §5).

Two rulings were made at the 2026-07-31 plan-review checkpoint and are **recorded, not
re-derived**: the registry enumeration + dissolution map (§2) and obligation-3's discharge
(§5). Two amendments bind this arc: **F1** — a doc-level status must not over-claim partial
consumption (applied to intake #16 this wave); **F2** — `ecosystem/schema/` is a new
directory, operator-approved via the architect 2026-07-31; no other new directories without a
fresh ask (§8).

## §1 Functional requirement — intake #22 §E, verbatim

> The operator's target, in his words: ask "which repos have component/role X" and get an
> answer from a graph; change a library, a CLAUDE.md, a template for ALL repos in one governed
> operation; see at a glance what is hub-owned vs repo-local, with versioning. Current state
> (declarations in `.methodology.yaml` + fleet_parity + plugin lockstep) is the seed; the
> query-and-manage layer IS #382 (pydantic) → #383 (networkx) → #385 (pandas) + copier/cruft
> for propagation. Ratify this paragraph as the chain's functional requirement so every arc in
> it closes against operator intent, not only technical Done-whens.

Every arc in the [E9] chain closes against this paragraph. This arc's leg: the pydantic
contract + a loader + a first divergence report; the graph is [#383]'s, propagation tooling is
the chain's tail.

## §2 Registry enumeration + dissolution map (ratified 2026-07-31; resolves dossier G1)

**THE FOUR** registries the contract dissolves or absorbs — named individually, as the
charter required:

1. **`ecosystem/registry.md` — RETIRED as authoritative.** Its four fields (Repo / Path /
   Purpose / Status) become schema fields; no checker reads it today and it has already
   drifted against its own declared derivation source (dossier C2). It may later be
   regenerated as a human view; it is never again hand-authoritative. [#455] dissolves.
2. **`ecosystem/index.yaml` — RECLASSIFIED as observed-state input.** It is a derived audit
   rollup, not a declaration; it leaves the declaration set and feeds the divergence report's
   "actual" side, with its staleness surfaced as data (dossier C8/G15), never silently
   regenerated.
3. **`ecosystem/parity-surfaces.yaml` — ABSORBED.** Its 13-key row grammar becomes the
   schema's Surface type; in v1 the yaml file stays on disk as a schema-validated instance
   (the contract moves to pydantic; physical relocation is [#383] wave work).
4. **`ecosystem/satellite-onboarding-rulings.yaml` — ABSORBED.** Operator-ruled target
   profiles become the desired-lifecycle assertion with provenance; the ruled-target vs
   observed-state relation becomes computable (dossier C3/G4).

**`ecosystem/deployed-versions.yaml` is NOT of the four.** Intake #16 §2's own mapping table
holds it out as the **state file** ("existing"). It is kept, typed, and made the membership
tie-break anchor: where the five membership sets disagree (dossier C1), resolution is toward
deployed-versions.yaml — the durable record, per registry.md's own derivation rule — and the
disagreement itself is carried as model data, never a load error. The sanctioned
corp-monorepo 1.2.0-vs-v1.3.1 divergence stays BY DESIGN, loading as declared
(`gate_rev_ahead`, dossier C4).

**No new physical contract file is created in v1.** Schema v1 is a *model over the existing
sources*; a single persisted desired-state document, and the physical retirement/freezing of
absorbed sources, are per-surface migration decisions owned by the [#383] waves (sol open
points 10–12, adjudicated §7). This keeps the Layer-2 read-only contract clean and the
migration strangler-shaped.

## §3 The seven ADR-107 §5 findings — per-finding disposition

1. **Identity is an opaque, byte-exact string** — **ADOPTED as a model constraint.** Every
   identity field (repo id, task id `"[#N]"`, surface id, edge id) is an opaque verbatim
   string; nothing normalizes to integers or tool-native ids.
2. **Unknown-key survival is a WRITE-path property, declared per surface** — **ADOPTED as
   data.** Each source surface carries a `write_policy` of exactly one of
   `round-trip-unknown-byte-stable` | `third-party-writers-barred` (the full per-surface
   table is in the schema; summary — tasks/ and consumer-owned files round-trip; all
   generated/state/ruling files bar third-party writers). Silence is not an option the type
   system permits.
3. **Typed row = frontmatter + verbatim body + residue manifest** — **ADOPTED.** The
   document-row type models all three parts; frontmatter-only representation is rejected.
4. **Preserve-raw beats normalize-at-ingest** — **ADOPTED.** Raw values ride beside parsed
   ones (`*_raw` fields, raw declaration strings on edges, verbatim lifecycle assertions);
   `depends-on` bare-vs-hash ([#424]/[#452]) is carried untouched as live semantic signal.
5. **Provenance pair on every derived surface** — **ADOPTED schema-wide**, generalized to a
   lineage type: `derived-from` (with `derived: true` + `source`) vs `generates` (post-flip
   direction, per the ADR-107 amendment); derived trees are excluded from prose-edge
   discovery as a class.
6. **A split needs a residue carrier** — **ADOPTED.** The residue-manifest type (ordering +
   non-member residue + hash + direction) is mandatory for any decomposed monolith surface,
   present and future.
7. **Directory-as-id-counter: allocation contract inputs** — **CONSUMED as a first-class
   type.** Allocation rules (ledger surface, next-free rule, closed-ids-remain-allocated,
   retirement policy retain-allocation-record, duplicate-id refusal, collision detection
   stage) are schema data, not prose. Duplicate-id **enforcement is witnessed** (§5);
   concurrent-allocation **prevention is not claimed** — `concurrent_prevention:
   not-provided` is a required, honest field ([#429] owns prevention).

## §4 Generality-pending clause (ADR-107 §6.2, transcribed; owner: [#383] wave 1)

This contract is **NOT declared general**. ADR-107 §6.2's discharge criteria, transcribed so
the obligation is checkable rather than remembered:

> **What counts:** a *second* governed surface split by the same engine pattern — per-item
> frontmattered `.md` files with byte-exact identity, a residue manifest, and a green
> regen-and-diff round-trip — demonstrated by a **committed round-trip proof, not by
> argument**. Named candidates, in order of cheapness: `docs/intake/*.md` (already
> frontmattered with a `status:` enum and a generated status-grouped index) and the `[E8]`
> ruling/decision register. Owner and sequencing: the [#383] execution waves, whose first
> wave should be chosen to satisfy this clause.

Until [#383] wave 1 lands that committed proof, the schema is the fleet contract for the
surfaces it names, and its claim to *generality* is pending — stated here exactly so no later
session inherits an asserted-not-shown property.

## §5 Obligation 3 — recorded DISCHARGED (architect ruling at the 2026-07-31 checkpoint)

The duplicate-id check runs in **two independent blocking gate paths, both with tests, both
witnessed passing on 2026-07-31**:

- **Path 1:** `scripts/validate_backlog.py:291-292` hard-fails a duplicate task id; runs in
  the blocking `validate-backlog` pre-commit hook. Test:
  `tests/test_validate_backlog.py::test_duplicate_id_fails` — witnessed PASS.
- **Path 2:** `scripts/gen_task_tree.py:790-796` REDs a duplicate id across active and
  retired records (ADR-107 §6.3's named requirement, quoted in-source); surfaced through
  `audit.py::check_task_tree_coherence` (wired in `ALL_CHECKS`, [#433] C1) → the
  `audit-health` pre-commit hook, where FAIL blocks the commit. Tests:
  `tests/test_gen_task_tree.py::test_check_reds_on_duplicate_ids_among_active_files` —
  witnessed PASS — plus `tests/test_task_tree_gate.py` (rename-remnant duplicate REDs the
  gate leg).

**Residual, named not claimed away:** two concurrent branches can still allocate the same
next-free id and merge cleanly; detection is at the gate, prevention stays with [#429]
(ADR-107 §6.3 + amendment). The schema records this as `concurrent_prevention: not-provided`
(§3 finding 7).

## §6 Edge declaration clause

Every dependency the fleet declares becomes one typed edge row: kind (`doc2doc | doc2file |
doc2code | hook | skill | task-dep | carrier | region`), source and target refs each tagged
with their **identity space** (the nine witnessed spaces + `path`; dossier G9), enforcement
posture as witnessed (`fail | warn | never-gates | inert` — dossier §ii.7), the verbatim raw
declaration, and provenance. **Identity-space equivalence is never inferred; it is declared**
— a crosswalk row (members + relation `same-organ | overlaps | implements | probes |
carries`) turns the G9 crosswalk from prose into data. Graph construction and rot queries
over these rows are [#383]'s (no networkx in v1, per intake #22 §E's own chain).

**Enforcement pointer:** where the schema declares layer/edge contracts, the mechanized check
that upholds them is [#451]'s scope (the CA layer-edge organ ADR-108 §B requires — the
standard is standing; the organ is the gap). This ADR cites [#451] as that pointer rather
than silently widening its own scope to enforcement.

## §7 Independent-derivation adjudication (sol vs CC)

Per the independent-derivation rule for foundational artifacts, sol (`gpt-5.6-sol`) produced
a schema derivation from the same ruled inputs before CC's was finalized; CC's derivation was
committed to file before sol's output was read (independence by ordering). Raw sol artifact:
`docs/audits/2026-07-31-technical-382-schema-derivation-sol.md`. **Convergent without
adjudication** (both derivations, independently): opaque verbatim identities; unified
provenance (reason + typed refs + raw fallback); ONE exception type spanning both suppression
vocabularies + `gate_rev_ahead` with one-per-concern uniqueness; edges as id-space-tagged
typed rows with enforcement posture and raw declaration; crosswalk as data; task rows as
frontmatter + verbatim body + residue; index.yaml as observed input with staleness surfaced;
membership resolved toward deployed-versions.yaml; concurrent-allocation prevention
explicitly not claimed. Divergences, each ruled explicitly:

- **D1 — root shape.** sol: three views (desired contract / observed state / in-memory
  composition). CC: one root with observed nested per-repo. **ADOPT sol.** CC's shape
  re-conflates target and observation inside one type — the exact C3 defect the model exists
  to dissolve; the Terraform config/state split is the intake's own architecture.
- **D2 — lifecycle.** sol: canonical `LifecycleStage {source, unonboarded, floor_only,
  full}` + lossless per-assertion records with `semantics {desired | observed |
  role-classification}` + a precedence rule. CC: axes-struct + derived position. **ADOPT sol's
  assertion model, AMENDED:** parity `role` does NOT map into lifecycle (sol's own open
  points 2–3 — `consumer → full` without deployment evidence is an over-claim, the F1
  defect class); role stays a separate classification axis, `hub → source` the sole
  exception. CC's derived `position` survives as a computed convenience over assertions
  (never stored).
- **D3 — component layer.** sol adds `ComponentSpec`/`ComponentAssignment` (the §E "which
  repos have component X" query spine). CC had none in v1. **ADOPT sol's types**, with a
  population bound: components derive from existing declarations (manifest components,
  parity surfaces) only — no new hand-authored component registry (intake #16 §5 lesson 1).
- **D4 — source-envelope weight.** sol attaches a raw-record envelope to every row (its own
  open point 10 questions this). **ADOPT CC's form:** envelopes are per-SOURCE in the loaded
  model (loader output, in-memory), not per-row in a persisted contract; per-row raw strings
  survive only where byte-fidelity is load-bearing (task rows, probes, lifecycle assertions,
  edge declarations). `write_policy` per surface is kept from sol as data (§3 finding 2).
- **D5 — parity `tier` map.** sol normalizes the role-or-repo-keyed map into
  `ApplicabilityRule {selector_kind, selector, posture}`. **ADOPT as the MODEL form**, with
  the file grammar unchanged in v1: the loader maps tier → applicability mechanically
  (repo-id-overrides-role preserved), raw map retained. Model normalizes; file survives.
- **D6 — gate_rev_ahead home.** sol relocates its typed detail into the exception type,
  surface rows carrying references. **ADOPT sol** (C4: one fact, one home).
- **D7 — allocation as a type.** sol promotes the §6.3 allocation contract to a first-class
  `AllocationRule`. **ADOPT** (finding 7 becomes data, §3).
- **D8 — manifest anchors.** sol has no manifest type. **KEEP CC's minimal `ManifestCut`**
  (methodology_version / source_tag / anchors): it is what makes G11's declared-vs-deployed
  gap computable; carriers stay raw in v1.
- **Sol open points 1–16:** 2/3 ruled in D2; 5 ruled enum-plus-raw-params in v1
  (discriminated probe models deferred until a consumer needs them, ADR-105 rule); 10–12
  ruled in §2 (no new persisted contract file in v1; envelopes loader-level; physical
  retirement is [#383] migration work); 13 ruled a loader parameter, not schema; 15 ruled
  self-invalidating per the parity contract's own grammar (clears when deployed source_tag
  reaches the gate tag); 16 ruled schema-loaded instances joined by concern id (no physical
  migration in v1). Points 1, 4, 6–9, 14 are recorded OPEN in the W2 spec and resolved
  RED-first in build, or carried honestly if they survive the wave.

## §8 Honest limits + authorizations

- **Read-only, no execution engine.** Models, a loader, a report — nothing converges state
  (ADR-28/36 hold; `apply` remains the existing regenerate-and-diff machinery + carriers).
- **The report is not convergence** and green-by-report is per-surface [#383] Done-when, not
  this arc's.
- **Consumer-side pin values are not readable from this repo** (dossier §iii GAP); the model
  carries hub-side expectations + declared exceptions, and says so per row
  (`pin_observation_status`).
- **Stale derived inputs are surfaced, not fixed** — index.yaml is 20 days stale today and
  loads as `stale`, never silently regenerated.
- **Existing checkers keep gating.** The schema runs BESIDE fleet_parity/audit.py until
  [#383] waves migrate surfaces; nothing is decommissioned by this ADR except registry.md's
  *authority*.
- **doc2doc reality:** the declared doc2doc graph is 1 spec deep today (dossier G7); the
  model can only load what is declared — it does not invent edges.
- **F2 authorization record:** `ecosystem/schema/` is a NEW directory, operator-approved via
  the architect at the 2026-07-31 plan review; the W2 commit message records this
  authorization. No other new directories under this arc without a fresh ask.
- **Dependencies:** `pydantic` enters `[dependency-groups].dev` at W2 (named by the
  operator-ratified §E; uv.lock regenerated in the same reviewed commit, ADR-106 discipline);
  `pandas` stays in the `analytics` group — the report documents its invocation; `networkx`
  is deliberately absent until [#383] names its consumer (ADR-105).

## §9 Alternatives considered

- **Reading A / Reading B enumerations** (dossier §i.1) — both rejected: each includes
  `deployed-versions.yaml` in the dissolution set, contradicting intake #16 §2's own mapping
  that keeps it as the state file. Union-of-five minus the state file yields exactly four,
  grounded in the ruled inputs rather than in either reading's preference.
- **One flat lifecycle enum over all vocabularies** — rejected (D2): the observed
  vocabularies are different *axes* (registration / role / ruled target / observed
  deployment); one enum re-creates the conflation C5 documents.
- **A new persisted desired-state file in v1** — rejected (§2): model-over-existing-sources
  first; physical consolidation is per-surface migration work with its own contracts.
- **networkx in v1** — rejected: [#383]'s consumer, per §E's own chain and ADR-105.
- **Schema under `scripts/`** — rejected: the contract lives with the data it governs;
  `scripts/` keeps the loader/report executables (read-only validators, Layer-2).

## Consequences

**Easier.** "Which repos have X" becomes a model query with one membership truth and one
lifecycle grammar; every cross-registry contradiction the dossier catalogued (C1–C8) becomes
either typed data or a computable derivation; the seven pilot findings stop being prose
obligations and become constraints a test can witness.

**Harder / newly owed.** The model is a second representation of surfaces until [#383]
migrates them — regeneration discipline (not hand-sync) is what keeps it honest; the
generality claim is explicitly pending (§4); component population is bounded to existing
declarations and will feel sparse until carriers/manifest rows grow.

**Cost of being wrong.** v1 writes no fleet state and creates no new persisted registry —
being wrong costs a model revision, not a migration rollback. The schema is versioned
(`schema_version: "1.0.0"`) precisely so v2 is a declared change, not a drift.
