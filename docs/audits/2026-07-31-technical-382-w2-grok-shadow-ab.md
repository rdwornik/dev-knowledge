# [#382] W2 — grok A/B shadow review: findings-quality vs cost vs terra (§C) + portability evidence (§H)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-31 · **Slug:** 382-w2-grok-shadow-ab
- **What this is:** the ONE artifact intake #22 §I.4 asks for — §C's grok shadow criterion and
  §H's portability probe recorded together. Subject diff: the W2 schema build
  (`71ba8f1a`+`2ee3376d`, reviewed pre-fix). Both reviewers saw the SAME diff.
- **Lanes:** terra = `codex-review.ps1` (codex-cli 0.145.0, code profile) →
  `docs/audits/2026-07-31-codex-382-w2-schema-v1.md`. grok = grok CLI 0.2.102
  (`--always-approve --max-turns 20 -p`, headless), wall **335s**, raw output preserved
  verbatim below the rule.

## §C — findings quality vs cost vs terra

- **Volume:** terra 1 Critical + 7 High (0 M/L). grok 2 Critical + 5 High + 9 Medium + 5 Low
  + a per-constraint coverage table.
- **Unique load-breaking catches (grok only):** C1 — `RefKind` missing the live `audit`
  provenance kind (verified on disk; would refuse real parity rows at load) and C2 — four
  Surface sparse fields are dict-shaped on disk (`join {manifest_component}`,
  `pending_migration {to,ticket}`, `local_names {repo→name}`, `declared_divergence
  {repo→text}`) where the schema held scalars. grok actually READ `parity-surfaces.yaml`;
  terra reasoned from the diff + ADR. Both accepted and fixed (`1b964e4e`).
- **Unique architectural catch (terra only):** the CRITICAL root under-build (missing D1/D3
  component layer + composition) — grok found it too but ranked it High.
- **Overlap:** enforcement-vocabulary drift (terra H7 ≡ grok H4), component layer
  (terra C ≡ grok H1) — independent convergence on both.
- **Accuracy:** terra 0 factual errors; grok 1 factual overstatement ("81/81 surfaces use
  kind: audit" — actual: 1 occurrence; the drift itself was real) and some cosmetic Lows.
- **Acceptance rate after triage:** terra 6.5/8 accepted (H2 partial, H5 partial-rejected on
  an ADR-recorded open point). grok ~17/21 accepted (L1/L2/L4 dispositioned, C1 count
  corrected). grok's Mediums were high-yield: M6 (dangling gate_rev_ahead reference = silent
  payload loss) became a root validator; M9 became the live enum↔disk exhaustiveness lock.
- **Cost:** grok wall 335s; terra wall ~4min (same order). **Neither CLI exposes token
  pricing — the cost leg of the §C criterion is INCONCLUSIVE on hard numbers** and is
  recorded as wall-clock-comparable, not "cheaper".
- **Verdict (recommendation, operator rules):** the two lanes are COMPLEMENTARY, not
  redundant — grok verified against live disk state, terra against spec fidelity. Keep the
  grok shadow on foundational diffs. The operator's "cheaper-and-possibly-better" hypothesis:
  *better-in-part witnessed* (2 unique load-breaking catches), *cheaper unproven* (no price
  surface).

## §H — portability evidence

**Witnessed this arc:** the process ran multi-provider end-to-end with no model owning it —
sol (OpenAI) produced the foundational schema derivation W1 consumed and adjudicated; terra
(OpenAI) and grok (xAI) both materially changed the shipped schema (accepted Criticals from
each); CC (Anthropic) built and orchestrated; the operator stayed the serial gate. The
methodology surfaces (frozen contracts, RED-first, triage-not-auto-accept, audits-class
records) bound all four models identically.

**NOT yet witnessed (stays open):** §H's actual probe — ONE full arc with a **non-Claude
builder** (grok/Codex on the fat-prompt + frozen contract, terra review). This arc's builder
was CC. Universalization debt recorded here, not claimed away:
1. The builder-role probe itself (§H's own proposal) — unrun; natural slot: a later [E9] wave.
2. The grok lane ran ad-hoc (hand-built prompt, no wrapper) — a `grok-review` wrapper
   symmetric to `codex-review.ps1` would make the shadow repeatable + comparable.
3. The review wrapper + skills layer (`codex-review.ps1`, Skill plumbing) is
   harness-specific; portable in shape, unported in fact.

**Verdict line for the repo record:** portability of the DERIVATION and REVIEW lanes is
witnessed; portability of the BUILDER lane is untested and remains §H debt.

---

## grok raw output (verbatim, immutable)

I'll run the specified diff and pull the ADR/spec + on-disk grammar sources so the review stays scoped to that surface only.Diff was truncated — reading the full schema and on-disk grammar sources next.Extracting on-disk enum values from parity-surfaces and cross-checking ADR enforcement wording.Confirming RefKind vs on-disk provenance kinds, enforcement labels, and a few pydantic edge cases.# Adversarial review — `main...HEAD` (schema surface only)

Scope: `ecosystem/schema/*`, `tests/test_desired_state_schema.py`, `pyproject.toml`  
(23 tests, GREEN claim; ADR-109 §3/§7; parity grammar in `ecosystem/parity-surfaces.yaml`)

---

## Critical

| # | Finding | Loc | One-line fix |
|---|---------|-----|--------------|
| C1 | **`RefKind` cannot load live parity provenance.** On-disk ownership blocks use `kind: audit` on **81/81** surfaces (`parity-surfaces.yaml`); schema enum has no `audit` → every real ownership row fails validation. | `desired_state.py:181-190` | Add `audit = "audit"` to `RefKind` (or map `audit→document` only if ADR records that rename; today it doesn’t). |
| C2 | **Absorbed surface fields cannot hold the on-disk shapes** (not “model form” like D5 tier). Disk: `declared_divergence: {repo→text}`, `join: {manifest_component}`, `pending_migration: {to,ticket}`, `local_names: {repo→name}`. Schema: `StrictStr` / `StrictStr` / `StrictStr` / `tuple[tuple[str,str],…]`. Dict inputs are **refused**; structure is not preservable without out-of-band string encoding that violates finding 4. | `desired_state.py:305-312` | Typed nested models (or `_SourceMirror` + required keys) matching the yaml grammar; keep raw beside parsed if needed. |

---

## High

| # | Finding | Loc | One-line fix |
|---|---------|-----|--------------|
| H1 | **D3 “ADOPT sol” ComponentSpec/ComponentAssignment are absent.** ADR-109 §7 D3 + §E query spine (“which repos have component X”) is unimplemented; no types, no root fields, no tests. | `desired_state.py` (missing); root `471-479` | Add `ComponentSpec`/`ComponentAssignment` and hang them on `FleetDesiredState` (population bound to existing decls). |
| H2 | **Finding 3 incomplete:** “document-row = frontmatter + body + residue” — `TaskRow` has frontmatter-ish fields + `body`, but **no residue composition**; `ResidueManifest` is a free-floating type, not part of the row or the desired root. | `desired_state.py:388-425`, `471-479` | Compose `TaskRow` with required `body` + `residue: ResidueManifest` (or a document-row wrapper) and attach task collections to the root. |
| H3 | **`Ownership` drops parity’s mandatory constraints.** Disk grammar (lines 63–68): non-blank `reason`, mandatory non-empty `provenance` with `{kind,repo,ref}`. Schema allows `reason=""` / `"   "` and `provenance=()`. | `desired_state.py:276-279` | `Field(min_length=1)` on reason (strip+nonempty validator) + `Field(min_length=1)` on provenance; require `repo` on ownership refs if parity is the source of truth. |
| H4 | **Enforcement vocabulary drifts from ADR §6 (and sol).** Witnessed: `fail \| warn \| never-gates \| inert`. Schema: `fail-gating \| warn-only \| never-gates \| inert`. No rename ruling in-file; loaders/crosswalks will invent a second vocabulary. | `desired_state.py:166-170` | Use ADR/sol tokens `fail`/`warn` (or document an explicit alias table + tests). |
| H5 | **`test_task_id_never_normalized` does not pin normalization refusal.** It only constructs `id="[#433]"` and asserts equality — never tries `433`, `"433"`, `"#433"`, or strip/coerce. Name overclaims finding 1. | `test_desired_state_schema.py:65-68` | Assert `TaskRow(id=433, …)` and any “normalize-to-int” path raise; keep `"[#433]"` round-trip. |

---

## Medium

| # | Finding | Loc | One-line fix |
|---|---------|-----|--------------|
| M1 | **Strictness is selective.** Identities use `StrictStr` (good), but `registered`/`floor_carrying`/`waivable` accept `1` and `"true"` → `True` (pydantic bool coercion). Undercuts “never coerced” posture for contract booleans. | `desired_state.py:266-267,305` | `StrictBool` (or `Literal[True, False]` with strict config) on those fields. |
| M2 | **`gate_rev_ahead` declare-only is only half-tested.** Validator requires `gate_tag_raw` (`337-342`); test covers effect≠declare-only + `waives_must`, **not** missing `gate_tag_raw`. | `test_…py:149-156` vs `desired_state.py:341-342` | Add `pytest.raises` for `kind=gate-rev-ahead` without `gate_tag_raw`. |
| M3 | **Residue SoT dual-claim path untested.** Code refuses `source`/`source_sha256` on source-of-truth (`417-419`); tests only omit `generates` entirely. | `test_…py:238-244` | Add case: SoT + `generates`+hash **and** `source=…` must raise. |
| M4 | **Allocation honesty only pins one of five Literals.** `closed_ids_remain_allocated=False`, bad `retirement_policy` / `duplicate_id_policy` / `collision_detection_stage` untested; `externally-coordinated` allowed (OK) but unasserted. | `desired_state.py:375-383`; `test_…py:216-233` | Table-parametrize illegal values for each Literal field. |
| M5 | **`test_models_are_frozen` only mutates `FleetDesiredState`.** Does not pin `_SourceMirror` (`Probe`/`TaskRow`) frozen+extra-allow, nor `_Contract` extra=forbid. | `test_…py:44-48` | Freeze-assign on `Probe`/`TaskRow`; extra-key on `Repo`/`Edge` must raise. |
| M6 | **`Surface.gate_rev_ahead` is reference-only (D6 OK) but loses the only live payload’s home unless `DeclaredDivergence` is mandatory-paired.** No invariant: surface ref concern_id ∈ divergences, or divergences gate rows carry full tag/reason. | `desired_state.py:312,317-343,481-490` | Root validator: every `Surface.gate_rev_ahead` concern resolves to a `gate-rev-ahead` divergence with `gate_tag_raw`. |
| M7 | **`§8 pin_observation_status` absent** (“model carries hub-side expectations + declared exceptions, and says so per row”). No field anywhere. | ADR §8 vs schema | Add per-row/per-pin `pin_observation_status` enum on the relevant assignment type (likely with D3 components). |
| M8 | **`ManifestCut` exists (D8) but is unreachable from either root** — dead type for G11 declared-vs-deployed. | `desired_state.py:437-447` | Attach to desired and/or observed roots (or delete until W3 with an explicit deferral comment + backlog id). |
| M9 | **No enum↔disk exhaustiveness tests.** `SurfaceKind`/`Posture`/`ProbeType`/`Role`/`OwnershipValue` currently **match** the 81-row yaml census (good), but nothing locks that; drift will be silent. | tests (missing) | Parametrize: every distinct `kind`/`probe.type`/`ownership.value`/`tier` token in `parity-surfaces.yaml` ∈ corresponding StrEnum. |

---

## Low

| # | Finding | Loc | One-line fix |
|---|---------|-----|--------------|
| L1 | **`waives_must` is a constant `False` property** — correct as “MUST never waived,” but unconnected to posture/kind; easy to misread as “this row waives nothing.” | `desired_state.py:329-333` | Rename to `never_waives_must: Literal[False] = False` or drop and encode via type. |
| L2 | **`datetime.date` accepts ISO strings** (coercion). Fine for dates; inconsistent with StrictStr identity story if “no coercion” is global. | `desired_state.py:218,225-226` | Document dates as parsed scalars, or use `StrictStr` raw dates like `deployed_date`. |
| L3 | **`lifecycle_from_parity_role` is a bare function**, not a validator; unknown roles silently `None` (no error). | `desired_state.py:255-258` | Accept `Role` only, or reject unknown strings. |
| L4 | **`sys.path` insert in tests** instead of package install — brittle, masks packaging issues. | `test_…py:21` | Rely on `pytest`/`uv run` package path; drop insert. |
| L5 | **`pydantic>=2.0` is a floor only** (lock pins 2.13.4 on branch via `uv.lock`, outside named diff). Wide lower bound can change StrictStr/extra semantics. | `pyproject.toml` | Tighten to `>=2.0,<3` (or pin to lock major.minor). |

---

## Untested ADR constraints (coverage holes)

| ADR item | Status in tests |
|----------|-----------------|
| Finding 1 opaque ids beyond repo/task (`surface id`, `EntityRef.id`, edge identity) | **Untested** (only `Repo`/`TaskRow`) |
| Finding 2 full write-policy table per surface | **Partial** — enum closed only; no per-source required pairing |
| Finding 3 frontmatter-only rejected | **Partial** — `body` required; no “frontmatter-only document” type test; residue not on row |
| Finding 4 preserve-raw for lifecycle / probe / depends_on / edge | **Covered** for those four |
| Finding 5 lineage direction | **Partial** — SoT generates + derived forbids generates; SoT+source dual claim **untested** |
| Finding 6 residue carrier (order + non-member + hash) | **Untested** as constraints (fields exist, no asserts) |
| Finding 7 full allocation contract | **Partial** — only `concurrent_prevention≠prevented` |
| §7 D1 desired≠observed roots | **Untested** (types exist separate; no anti-conflation test) |
| §7 D2 role≠lifecycle except hub | **Covered** |
| §7 D3 components | **Missing + untested** |
| §7 D5 applicability model | **Partial** — posture closed; no repo-overrides-role |
| §7 D6 gate_rev one home | **Partial** — declare-only yes; surface↔divergence join no |
| §7 one-per-concern | **Partial** — same kind+concern only; cross-kind same concern allowed (matches “within mechanism” name; ADR wording is easy to misread) |
| §6 enforcement closed set as witnessed | **Untested** (and values wrong — H4) |
| Repo id uniqueness validator | **Untested** (`_repo_ids_unique` dead to suite) |
| `extra=forbid` vs `extra=allow` split | **Untested** |
| Enum parity with `parity-surfaces.yaml` | **Untested** (currently coincident) |

---

## What the 23 tests actually pin

| Claim | Real pin |
|-------|----------|
| schema_version literal | yes |
| frozen models | **FleetDesiredState only** |
| opaque repo id + StrictStr int refuse | yes for `Repo.id` |
| task id never normalized | **no** — round-trip only |
| depends_on bare vs hash | yes |
| TaskRow unknown keys survive | yes (`extra=allow`) |
| edge raw byte-exact | yes |
| DeployedState null coupling | yes (one side) |
| ownership mandatory | yes (missing field) |
| posture enum closed | yes (one bad token) |
| probe extras preserved | yes |
| gate_rev declare-only / waives_must | partial |
| one-per-concern | same-kind only |
| edge kind / id_space closed | yes (one bad each) |
| crosswalk min 2 + relation | yes |
| lifecycle raw + semantics enum | yes |
| parity role→lifecycle | yes |
| allocation no “prevented” | yes |
| residue SoT/derived direction | partial |
| write_policy closed | yes |

---

## Enum drift vs `parity-surfaces.yaml`

| Enum | Drift? |
|------|--------|
| `SurfaceKind` (9) | **Match** all disk kinds |
| `Posture` (6) | **Match** |
| `ProbeType` (16) | **Match** all disk `probe.type` values |
| `Role` | **Match** `hub\|consumer\|pre-deploy` |
| `OwnershipValue` | **Match** |
| `RefKind` | **DRIFT — missing `audit` (C1)**; also has unused `census/file/ruling/document/operator-ruling` not seen in parity ownership |
| `Enforcement` | **DRIFT vs ADR §6 / sol**, not vs parity file (parity doesn’t carry this enum) |
| Structural field shapes on `Surface` | **DRIFT (C2)** — not enum tokens, but load-breaking |

---

## Overall verdict

1. **Not load-ready for the absorbed parity surface:** missing `RefKind.audit` plus collapsed `declared_divergence`/`join`/`pending_migration`/`local_names` shapes will fail or strip real yaml.  
2. **Spec fidelity gaps are structural, not polish:** D3 components absent, finding-3 residue not on the document row, enforcement tokens renamed off ADR §6.  
3. **The 23 GREEN tests are a thin constraint sample** — several names overclaim (esp. task-id normalization / frozen / gate_rev completeness); critical load and composition invariants are untested.
