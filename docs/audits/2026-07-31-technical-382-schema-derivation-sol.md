# [#382] W1 — sol INDEPENDENT schema-v1 derivation (raw, preserved verbatim below the rule)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-31 · **Slug:** 382-schema-derivation-sol
- **Provenance:** Codex `gpt-5.6-sol` via `codex exec` (codex-cli 0.145.0, default sol model,
  `service_tier=priority`), non-interactive, launched from the `feat/382-desired-state-schema`
  W1 session. Prompt: the ruled-inputs pack (dossier + ADR-107 §5/§6.3 + intake #16 §1/§2/§5 +
  intake #22 §E + charter §2/§3) plus the plan-review-ratified rulings (THE FOUR + dissolution
  map, deployed-versions.yaml as state anchor, edges-typed-no-networkx, Layer-2 read-only).
  Sol was NOT shown CC's derivation.
- **Independence by ordering:** CC's own derivation was committed to a session scratchpad file
  BEFORE this output was read (independent-derivation rule for foundational artifacts, [#382]
  execution brief). Adjudication of every divergence is recorded in ADR-109 §7 — this file is
  the raw evidence side and is immutable per CLAUDE.md §5 item 3.
- **Consumed by:** ADR-109 (adjudication table §7).

---
# Independent schema-v1 derivation — fleet desired-state contract [#382]

## 0. Contract boundary

Schema v1 has three deliberately separate views:

- `FleetDesiredStateV1` — the authoritative, persisted desired-state contract.
- `ObservedFleetStateV1` — read-only state loaded from `index.yaml`, `deployed-versions.yaml`, and consumer pins.
- `FleetModelV1` — an in-memory composition used by later reporting/graph waves; it does not become another registry.

`ecosystem/registry.md` loses authority; `index.yaml` remains observed input; `parity-surfaces.yaml` remains a schema-validated v1 instance; satellite onboarding rulings become desired lifecycle. Graph construction and reconciliation execution remain outside v1. This follows the state/config separation in `docs/intake/2026-07-21-func-fleet-north-star.md:61-70` and the Layer-2 boundary in `docs/audits/2026-07-28-technical-382-charter.md:67-80`.

## 1. Model classes

- `FleetDesiredStateV1` — authoritative schema-versioned desired state.
- `FleetModelV1` — read-only composition of desired state and separately loaded observations.
- `RepositorySpec` — one known repository, including authoritative membership and desired lifecycle.
- `LifecycleAssertion` — lossless record of one legacy lifecycle statement and its canonical interpretation.
- `ComponentSpec` — a queryable component, role, library, template, hook, skill, or governed organ.
- `ComponentAssignment` — desired component-to-repository relationship.
- `SurfaceSpec` — absorbed parity-surface row and its applicability/probe contract.
- `ApplicabilityRule` — desired posture for a surface under a role or repo selector.
- `ProbeSpec` — typed probe discriminator plus losslessly preserved parameters.
- `ObservedFleetStateV1` — read-only observed-state root.
- `RepositoryObservation` — audit and deployment observations for one repository.
- `DeploymentState` — the three durable deployed-version fields plus observed consumer pin.
- `AuditFinding` — one generated `index.yaml` finding.
- `TypedDocumentRow` — typed frontmatter over verbatim document bytes.
- `ResidueManifest` — ordering, non-row residue, generation direction, and byte-integrity data.
- `SurfaceLineage` — explicit source→derived or source→generated relationship.
- `ProvenanceBlock` — unified “why” grammar.
- `ProvenanceRef` — one structured evidence reference.
- `ExceptionDeclaration` — common representation for waivers, dispositions, and declared non-waiving divergence.
- `DependencyEdge` — one typed, directed dependency declaration.
- `EntityRef` — an edge endpoint tagged with its identity space.
- `IdentityCrosswalk` — explicit equivalence/overlap relation among identities from different spaces.
- `AllocationRule` — namespace-specific allocation, retirement, and collision contract.
- `SourceEnvelope` — raw-beside-parsed carrier and per-surface write-path policy.

## 2. Fields by class

### `FleetDesiredStateV1`

- `schema_version` — literal string `"1.0.0"`; required; exact match, not a numeric version.
- `repositories` — `dict[str, RepositorySpec]`; required; keys are opaque repo ids, preserved verbatim.
- `components` — `dict[str, ComponentSpec]`; required, possibly empty; enables “which repos have component/role X” queries (`docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md:62-70`).
- `assignments` — `list[ComponentAssignment]`; required, possibly empty.
- `surfaces` — `list[SurfaceSpec]`; required; absorbs `parity-surfaces.yaml` rows (`dossier:143-173`).
- `edges` — `list[DependencyEdge]`; required; typed data only, with no graph object.
- `identity_crosswalks` — `list[IdentityCrosswalk]`; required, possibly empty; closes dossier G9.
- `exceptions` — `list[ExceptionDeclaration]`; required, possibly empty.
- `allocation_rules` — `list[AllocationRule]`; required where opaque allocated identities exist.
- `row_surfaces` — `list[TypedDocumentRow]`; optional; proves the piloted task representation is expressible without a parallel store.
- `residue_manifests` — `list[ResidueManifest]`; optional; required for every decomposed monolith surface.
- `lineage` — `list[SurfaceLineage]`; required, possibly empty.
- `source` — `SourceEnvelope`; required for the persisted contract itself.

### `FleetModelV1`

- `desired` — nested `FleetDesiredStateV1`; required.
- `observed` — nested `ObservedFleetStateV1`; required.
- `loaded_sources` — `dict[str, SourceEnvelope]`; required; one envelope per live source parsed by the later loader.
- `load_conflicts` — `list[LifecycleAssertion]` or equivalent typed conflict records; required, possibly empty; conflicts survive loading rather than being overwritten.
- `membership_anchor` — literal string `"ecosystem/deployed-versions.yaml"`; required; fixes the membership tie-break.
- `declared_divergences` — `list[str]`; derived references to `ExceptionDeclaration.id`; read-only convenience, not a second store.

### `RepositorySpec`

- `id` — `str`; required; opaque/verbatim join identity.
- `member` — `bool`; required; true exactly when the repo key occurs in `deployed-versions.yaml`; resolves C1 toward the state anchor.
- `membership_source` — literal `"deployed-versions"`; required.
- `path` — optional `str`; opaque, not normalized; absorbs `registry.md Path` and `index.yaml repos[].path` (`dossier:209-211,278-282`).
- `purpose` — optional verbatim `str`; absorbs `registry.md Purpose` (`dossier:99-107`).
- `desired_lifecycle` — `LifecycleStage`; required for authoritative desired-state entries.
- `lifecycle_assertions` — `list[LifecycleAssertion]`; required; retains every conflicting legacy statement.
- `roles` — `list[str]`; required, possibly empty; opaque query labels, not a second lifecycle enum.
- `component_assignments` — `list[str]`; optional references to assignment ids.
- `provenance` — `ProvenanceBlock`; required when lifecycle came from an operator ruling.
- `source_records` — `list[SourceEnvelope]`; required; preserves absorbed registry rows and unknown fields.

Absorbs `registry.md` repo/path/purpose/status, `parity-surfaces.yaml fleet[].role`, and `satellite-onboarding-rulings.yaml` profile/ruling fields (`dossier:99-113,143-181,205-226`).

### `LifecycleAssertion`

- `source_surface` — enum/string; required; one of `registry`, `parity`, `onboarding-ruling`, `deployed-version`.
- `raw_value` — `str`; required; opaque/verbatim, including complete registry status prose.
- `mapped_stage` — `LifecycleStage`; required.
- `semantics` — enum `{desired, observed, role-classification}`; required; prevents target and observation from being conflated.
- `effective_date` — optional `date`.
- `version_raw` — optional `str`; preserve leading `v` and original spelling.
- `provenance` — optional `ProvenanceBlock`.
- `source` — `SourceEnvelope`; required.

### `ComponentSpec`

- `id` — `str`; required; opaque/verbatim.
- `kind` — enum including at least `{organ, hook, command, skill, doc-shape, config, library, template, carrier}`; required.
- `description` — optional verbatim `str`.
- `ownership` — enum `{hub, repo, conditional}`; required; canonical query dimension.
- `version_raw` — optional `str`; raw-beside-parsed.
- `version_parsed` — optional parsed semantic-version value; validation aid only.
- `roles` — `list[str]`; required, possibly empty.
- `surfaces` — `list[str]`; required, possibly empty.
- `provenance` — `ProvenanceBlock`; required.
- `source` — `SourceEnvelope`; required.

This supplies the query/manage requirement without treating the manifest or parity file as another authority (`docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md:64-69`).

### `ComponentAssignment`

- `id` — `str`; required; opaque/verbatim.
- `repository_id` — `str`; required.
- `component_id` — `str`; required.
- `desired_presence` — enum `{present, absent, local, ignored}`; required.
- `desired_version_raw` — optional `str`.
- `local_name` — optional `str`; absorbs parity `local_names`.
- `declared_by` — optional `str`; absorbs parity `declared_by`.
- `provenance` — `ProvenanceBlock`; required.
- `source` — `SourceEnvelope`; required.

### `SurfaceSpec`

- `id` — `str`; required; opaque canonical surface id.
- `kind` — enum containing all observed parity kinds; required.
- `applicability` — `list[ApplicabilityRule]`; required; replaces the mixed role/repo `tier` map.
- `probe` — `ProbeSpec`; required.
- `ownership` — enum `{methodology-generic, conditional, project}`; required.
- `ownership_reason` — optional `ProvenanceBlock`; absorbs ownership reason/provenance.
- `waivable` — `bool`; required, default false only if absence is explicitly defined by the schema.
- `waiver_component` — optional `str`; reference to an `ExceptionDeclaration` concern/component.
- `local_names` — `dict[str, str]`; optional.
- `declared_by` — optional `str`.
- `declared_divergence` — optional `str`; reference to an exception id.
- `pending_migration` — optional `str`.
- `join` — optional `str`; opaque cross-surface join token.
- `gate_rev_ahead` — `dict[str, str]`; optional mapping repo id→exception id; typed detail lives in `ExceptionDeclaration`.
- `provenance` — `ProvenanceBlock`; required.
- `source` — `SourceEnvelope`; required.

This absorbs the 13-key parity row union at `dossier:143-171`.

### `ApplicabilityRule`

- `selector_kind` — enum `{role, repository}`; required.
- `selector` — `str`; required; opaque role or repo id.
- `posture` — enum `{MUST, SHOULD, LOCAL, IGNORE, INVERSE, TOMBSTONE}`; required.
- `provenance` — optional `ProvenanceBlock`.

The selector discriminator removes the current role-id/repo-id ambiguity (`dossier:155-157`).

### `ProbeSpec`

- `type` — enum of the 16 observed probe types; required (`dossier:158-161`).
- `parameters` — `dict[str, raw value]`; required; unknown parameters preserved.
- `raw` — `str`; required; exact original probe block.
- `expected_rev_source` — optional enum/string; absorbs `expected_rev_from`.
- `freshness_rule` — optional structured rule; absence means “no currency assertion,” not “fresh.”
- `source` — `SourceEnvelope`; required.

### `ObservedFleetStateV1`

- `generated_at` — optional datetime; absorbs `index.yaml generated`.
- `repositories` — `dict[str, RepositoryObservation]`; required.
- `consumer_pins` — `dict[str, raw scalar]`; required, possibly unavailable.
- `source_envelopes` — `dict[str, SourceEnvelope]`; required.
- `freshness_status` — enum `{current, stale, unknown}`; required; prevents generated data from silently reading as current, addressing C8/G15.

### `RepositoryObservation`

- `repository_id` — `str`; required.
- `last_audit` — optional `date`.
- `findings` — `list[AuditFinding]`; required.
- `deployment` — `DeploymentState`; required for state members.
- `observed_path` — optional opaque `str`.
- `source` — `SourceEnvelope`; required.

### `DeploymentState`

- `deployed_methodology_version_raw` — optional `str`; preserves the state scalar exactly.
- `deployed_methodology_version_parsed` — optional parsed semantic version.
- `deployed_date` — optional `date`.
- `source_tag_raw` — optional `str`; preserves the leading `v`.
- `consumer_pin_raw` — optional `str`; unavailable is distinct from null.
- `pin_observation_status` — enum `{observed, unavailable, not-applicable}`; required.
- `source` — `SourceEnvelope`; required.

Absorbs the three state scalars at `dossier:460-498` and separately observed consumer pins at `dossier:500-512`.

### `AuditFinding`

- `check_name` — `str`; required; opaque check identity.
- `evidence` — verbatim `str`; required.
- `status` — raw `str` plus optional parsed enum; required.
- `source` — `SourceEnvelope`; required.

Absorbs `index.yaml findings[]` (`dossier:118-129`).

### `TypedDocumentRow`

- `id` — `str`; required; opaque byte-exact identity such as `"​[#433]"`; never normalized to integer.
- `frontmatter` — `dict[str, raw value]`; required; typed parsed view.
- `frontmatter_raw` — `str`; required; byte-preserving source, including unknown keys and scalar spelling.
- `body_raw` — `str`; required; verbatim body.
- `document_raw` — `str`; required when byte-stable reconstruction cannot be proven from the two pieces alone.
- `path` — `str`; required; opaque source-relative location.
- `status` — optional parsed enum while retaining raw frontmatter.
- `manifest_id` — `str`; required for a decomposed surface.
- `lineage_id` — `str`; required.
- `source` — `SourceEnvelope`; required.

Required by ADR-107 findings 1–4 (`docs/decisions/ADR-107-backlog-restructure-engine-schema-viewer.md:226-239`).

### `ResidueManifest`

- `id` — `str`; required.
- `schema_raw` — `str` or integer raw value; required.
- `role` — enum `{source-of-truth, derived}`; required.
- `row_order` — `list[str]`; required; opaque row ids.
- `non_member_residue` — ordered `list[str]`; required; verbatim prose/fragments outside rows.
- `generates` — optional `str`; required for a post-flip source-of-truth surface.
- `source` — optional `str`; required only when the represented surface is derived.
- `generated_sha256` — optional `str`; required for a source-of-truth generator contract.
- `source_sha256` — optional `str`; permitted only for a genuinely derived surface.
- `source_envelope` — `SourceEnvelope`; required.

Ordering, non-member prose, and a hash are mandatory residue responsibilities (`ADR-107:246-248`). Post-flip tasks use `role: source-of-truth`, `generates: BACKLOG.md`, and `generated_sha256`; they must not claim `derived: true` or `source:` (`ADR-107:436-452`).

### `SurfaceLineage`

- `id` — `str`; required.
- `mode` — enum `{derived-from, generates}`; required.
- `from_surface` — `str`; required.
- `to_surface` — `str`; required.
- `derived` — optional literal `true`; required only for `derived-from`.
- `provenance` — `ProvenanceBlock`; required.
- `residue_manifest_id` — optional `str`; required for monolith decomposition.
- `exclude_from_prose_edge_discovery` — `bool`; required for derived trees; enforces the ADR-107 class-level exclusion requirement.

### `ProvenanceBlock`

- `reason` — verbatim `str`; required.
- `provenance` — `list[ProvenanceRef]`; required, possibly empty only when the legacy grammar supplied no structured reference.
- `raw` — optional verbatim `str`; required when importing free-text provenance without loss.

### `ProvenanceRef`

- `kind` — enum/string; required; examples include `git-tag`, `git-commit`, `backlog`, `census`, `decision`, `document`, `operator-ruling`.
- `ref` — opaque `str`; required.
- `repo` — optional opaque `str`.
- `actor` — optional opaque `str`.
- `date` — optional `date`.

### `ExceptionDeclaration`

- `id` — `str`; required; opaque canonical exception/concern id.
- `kind` — enum `{parity-waiver, audit-disposition, gate-rev-ahead}`; required.
- `concern_id` — `str`; required; common join across the suppression vocabularies.
- `target` — `EntityRef`; required.
- `repository_id` — optional `str`.
- `effect` — enum `{waive, suppress-warning, declare-only}`; required.
- `match` — optional verbatim `str`; required for audit evidence-substring dispositions.
- `component` — optional `str`; absorbs `.methodology.yaml component`.
- `organ` — optional `str`; absorbs disposition-register organ.
- `gate_tag_raw` — optional `str`; required for `gate-rev-ahead`.
- `provenance` — `ProvenanceBlock`; required.
- `review_date` — optional `date`; required for time-boxed waivers, optional for dispositions.
- `expiry_date` — optional `date`.
- `auto_clearable_by` — optional `str`.
- `clear_when` — optional structured condition; required for self-invalidating declarations.
- `waives_must` — literal `false` for `gate-rev-ahead`.
- `source` — `SourceEnvelope`; required.

### `DependencyEdge`

- `id` — `str`; required; opaque edge identity.
- `kind` — enum `{doc2doc, doc2file, doc2code, hook, skill, task-dep, carrier, region}`; required.
- `source_ref` — `EntityRef`; required.
- `target_ref` — `EntityRef`; required.
- `direction` — enum `{directed, bidirectional}`; required.
- `declaration_shape` — enum/string identifying shapes 1–12; required while importing legacy sources.
- `enforcement_posture` — enum `{fail, warn, never-gates, inert}`; required.
- `expected_arity` — optional integer.
- `freshness_rule` — optional structured rule.
- `exemption_reason` — optional `ProvenanceBlock`.
- `aliases` — `list[EntityRef]`; optional; references overlapping identities without changing endpoint identity.
- `provenance` — `ProvenanceBlock`; required.
- `raw_declaration` — `str`; required; preserve-raw.
- `source` — `SourceEnvelope`; required.

The kind set covers the fixed ruling and all four additional edge classes witnessed at `dossier:301-454`.

### `EntityRef`

- `id_space` — enum `{spec-id, rule-id, check-name, surface-id, hook-id, region-id, task-id, component-id, python-symbol, path}`; required.
- `id` — `str`; required; opaque/verbatim.
- `repo` — optional `str`.
- `path` — optional opaque `str`.
- `source_location` — optional `str`.

### `IdentityCrosswalk`

- `id` — `str`; required.
- `members` — `list[EntityRef]`; required, minimum two.
- `relation` — enum `{same-organ, overlaps, implements, probes, carries}`; required; equality must not be assumed.
- `provenance` — `ProvenanceBlock`; required.

This makes the G9 crosswalk data rather than filename inference (`dossier:623-629`).

### `AllocationRule`

- `namespace` — `str`; required.
- `identity_pattern` — `str`; required; opaque identity remains distinct from the parsed numeric allocation component.
- `ledger_surface` — `str`; required.
- `next_free_rule` — enum/string; required; for tasks, `max(parsed id from all retained task filenames) + 1`.
- `closed_ids_remain_allocated` — literal `true`; required.
- `retirement_policy` — enum `{retain-allocation-record}`; required for tasks.
- `duplicate_id_policy` — enum `{refuse}`; required.
- `collision_detection_stage` — enum `{validation, merge-gate}`; required.
- `concurrent_prevention` — enum `{not-provided, externally-coordinated}`; required; v1 must not claim prevention.
- `source` — `SourceEnvelope`; required.

This incorporates ADR-107 §6.3 and the amendment: the ledger is complete post-flip, prune is refused, and concurrent branches can still collide (`ADR-107:285-322,436-463`).

### `SourceEnvelope`

- `surface` — enum/string; required.
- `location` — `str`; required.
- `raw_record` — `str`; required.
- `unknown_fields` — `dict[str, raw value]`; required, possibly empty.
- `write_policy` — enum `{round-trip-unknown-byte-stable, third-party-writers-barred}`; required.
- `parsed_at` — optional datetime; runtime metadata only.
- `source_version_raw` — optional `str`.
- `residue` — optional raw `str`.

## 3. Lifecycle vocabulary

### Canonical enum: `LifecycleStage`

- `source`
- `unonboarded`
- `floor_only`
- `full`

The enum describes methodology capability/target. Desired and observed assertions remain distinguishable through `LifecycleAssertion.semantics`.

### Mapping from every observed vocabulary

`registry.md Status`:

- `source (hub — methodology origin)` → `source`, semantics `role-classification`.
- `registered · onboarded (vX)` → `full`, semantics `observed`; preserve `vX` separately.
- `registered · unonboarded` → `unonboarded`, semantics `observed`.
- `registered · unonboarded (floor-carrying)` → `floor_only`, semantics `observed`.
- `registered · methodology-unonboarded` → `unonboarded`, semantics `observed`.
- The same value with GitHub-origin prose → `unonboarded`; origin text remains raw residue/provenance.

Parity role:

- `hub` → `source`, semantics `role-classification`.
- `consumer` → `full`, semantics `role-classification`; it is not by itself deployment proof.
- `pre-deploy` → `unonboarded`, semantics `role-classification`.

Onboarding ruling profile:

- `full` → `full`, semantics `desired`.
- `floor-only` → `floor_only`, semantics `desired`.

Deployed version:

- non-null version → `full`, semantics `observed`.
- null version → `unonboarded`, semantics `observed`.
- hub + null version → `source`, because hub null is explicitly by design and must not be interpreted as an unonboarded hub (`dossier:491-498,631-633`).

Desired-lifecycle precedence when sources disagree:

1. Explicit onboarding ruling profile.
2. Hub/source classification.
3. Otherwise deployed non-null state.
4. Otherwise explicit floor-carrying statement.
5. Otherwise `unonboarded`.

All lower-precedence assertions remain in `lifecycle_assertions`; precedence selects desired state but never deletes the contradiction. This preserves the target/current distinction in C3/G4.

## 4. Unknown-key/write-path clause

- Canonical desired-state document — `round-trip unknown keys byte-stable`.
- `parity-surfaces.yaml` v1 instance — `round-trip unknown keys byte-stable`.
- Typed task or other frontmatter row — `round-trip unknown keys byte-stable`, including lexical scalar form.
- Decomposed row bodies and residue — `round-trip unknown keys/bytes byte-stable`.
- `registry.md` — `third-party writers barred`; retired as authoritative and loader-read-only.
- `index.yaml` — `third-party writers barred`; its existing generator remains the sole writer.
- `satellite-onboarding-rulings.yaml` after absorption — `third-party writers barred`; canonical desired lifecycle is written in the new contract.
- `deployed-versions.yaml` — `third-party writers barred`; deploy machinery remains its writer.
- Consumer `.pre-commit-config.yaml` pins — `third-party writers barred`; only the governed carrier/apply path may write them.
- Generated manifests/indexes — `third-party writers barred`; regeneration machinery is the sole writer.
- `.methodology.yaml` and disposition-register legacy imports — `round-trip unknown keys byte-stable` until a separately ruled migration retires either source.

This makes unknown-key survival a declared write-path property, as required by `ADR-107:230-233`.

## 5. Provenance grammar

The single canonical block is:

- `reason: verbatim string`
- `provenance: list[ProvenanceRef]`
- optional `raw` for an unstructured legacy block

Legacy mappings:

- Parity `{value, reason, provenance[]}` → value stays on its owning field; `reason` and `provenance[]` enter the block.
- Onboarding `{ruled_by, ruled_date, census_ref}` → provenance item `{kind: census/operator-ruling, ref: census_ref, actor: ruled_by, date: ruled_date}`; any ruling prose becomes `reason`.
- Disposition `{ref, reason}` → `reason` plus one document/decision provenance ref.
- Silent-rule free-text provenance → byte-exact `raw`; structured references may be added without deleting raw.
- Dependency `rationale` → `reason`; evidence refs are empty until declared.

Lineage is separate from justification. A truly derived surface uses `derived-from` plus `derived: true` and `source`. A post-flip authoritative task tree uses `generates`; it must not retain false `derived/source` claims (`ADR-107:446-450`).

## 6. Divergence and suppression

All three mechanisms use `ExceptionDeclaration` and a shared `concern_id`:

- `.methodology.yaml sanctioned_divergences` → `kind: parity-waiver`, `effect: waive`, target id-space `component-id`, with mandatory reason and review/expiry.
- `disposition-register` → `kind: audit-disposition`, `effect: suppress-warning`, target id-space `check-name`, retaining `organ`, evidence `match`, `auto_clearable_by`, and optional review date.
- `gate_rev_ahead` → `kind: gate-rev-ahead`, `effect: declare-only`, target the affected parity surface/repository, retain `gate_tag_raw`, provenance, and `clear_when: deployed source_tag reaches gate tag`.

Rules:

- One live exception per `concern_id` and effect.
- A waiver cannot suppress two concerns.
- A disposition cannot silently waive a non-waivable parity `MUST`.
- `gate_rev_ahead` is not a waiver, never changes `MUST`, and loads as `DECLARED`.
- The corp-monorepo `1.2.0` corpus / `v1.3.1` gate combination remains intact as one declared exception, not a corrected version.
- Cross-mechanism relationships are explicit through `concern_id` and `IdentityCrosswalk`, addressing C7/G14.

## 7. Edge row contract

Every dependency is one `DependencyEdge` data row. At minimum it carries:

- Opaque edge id.
- Typed kind.
- Source `EntityRef`.
- Target `EntityRef`.
- An `id_space` tag on each endpoint.
- Direction.
- Legacy declaration shape.
- Enforcement posture.
- Optional arity, freshness, and exemption conditions.
- Provenance.
- Exact raw declaration and source location.

The nine witnessed identity spaces remain independent. Equivalence is declared through `IdentityCrosswalk`; it is never inferred merely because names or paths look related. This permits later [#383] graph construction without placing networkx or graph queries in schema v1.

## 8. Open points

1. Should non-members present only in retired/ruling sources remain `RepositorySpec(member=false)`, or move into a separate candidate/satellite collection?
2. Is `consumer → full` the intended canonical lifecycle mapping, or should parity role remain entirely non-lifecycle and require deployment/profile evidence?
3. Does `full` mean “full target profile,” “full corpus currently deployed,” or both with assertion semantics carrying the distinction?
4. Which component-kind and role vocabularies are closed enums in v1, beyond the values presently witnessed?
5. Should all 16 probe parameter grammars become discriminated nested models in v1, or is enum `type` plus raw-preserving parameters sufficient?
6. What canonical id-minting rule applies to edges, components, exceptions, crosswalks, and surfaces?
7. Are identity crosswalk relations many-to-many, and which relations imply equivalence versus partial overlap?
8. Is allocation scoped per namespace, per surface, or fleet-wide? The task rule is known, but other id spaces have no ruled allocator.
9. What exact byte boundary defines `frontmatter_raw`, `body_raw`, and non-member residue, including delimiters and newline ownership?
10. Must the canonical desired-state file itself contain legacy source envelopes, or may envelopes exist only in the loader’s in-memory `FleetModelV1`?
11. When are `registry.md` and satellite rulings physically retired or frozen? Authority is ruled, but migration timing is not.
12. Which process is permitted to write the canonical contract after v1, given Layer-2 itself is read-only against the fleet?
13. What freshness threshold turns an observed generated registry from `current` to `stale`?
14. How are unavailable consumer-side pins distinguished from inaccessible repositories versus genuinely missing pins?
15. Does `gate_rev_ahead` clear on exact equality, ancestry/reachability, or a separately declared corpus deployment event?
16. Should disposition and sanctioned-divergence records physically migrate into the new contract in v1, or remain schema-loaded instances joined by `concern_id`?
