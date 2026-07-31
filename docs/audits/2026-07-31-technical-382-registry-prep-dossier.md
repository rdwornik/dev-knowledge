# [#382] registry prep dossier — the 4-registry sprawl, the edge taxonomy, and what state records today

Status: PROPOSED — analysis input only; no schema contract declared (pilot-precedes-contract)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-31 · **Slug:** 382-registry-prep-dossier
- **Scope:** a read-only INPUT DOSSIER for the morning architect ahead of the [#382] arc. It enumerates what
  `ecosystem/` holds today, what shapes express a dependency edge today, what per-consumer state is recorded
  today, and what nothing records. It contains **no schema**, **no proposed fields**, **no ADR text**, and
  **no decisions**. Every gap is stated as a gap, never as a design.
- **Boundary (hard):** the pilot-precedes-contract ruling (`docs/decisions/README.md`, operator ruling
  2026-07-26; carried on `tasks/433-backlog-restructure-build-thin-engine-backlog-md.md:13`) forbids declaring
  the schema contract before the [#433] pilot's findings are consumed. Nothing below may be read as a contract.
- **Method:** read-only Read/Grep/Glob + read-only Bash. No file other than this one was written. No git
  mutation. Every claim carries `file:line`.

---

## 0. The row this dossier serves

`BACKLOG.md:429` (mirrored verbatim at `tasks/382-desired-state-data-model-intake-adr.md:13`):

> `[#382] [P1][M] Desired-state data model: intake → ADR — build the intake #16 §2 architecture (the Terraform
> model, not the tool): ONE schema-versioned desired-state contract in ecosystem/ dissolving the 4-registry
> sprawl (pydantic); the dependency graph as doc2doc/doc2file/hooks/skills edges with rot as a graph query
> (networkx); the divergence report as surface × repo × {conform/diverge/declared} (pandas). terraform apply
> maps to the EXISTING regenerate-and-diff machinery + carriers; state = deployed-versions.yaml + the
> per-consumer version pin.`

Frontmatter (`tasks/382-desired-state-data-model-intake-adr.md:2-10`): `id "[#382]" · status open · priority P1
· size M · theme "[E9] Fleet Desired-State System (North Star)" · story "[S24] Declare desired state once, as
data, instead of as N registries" · serialize-group architecture · generates BACKLOG.md`. **No `depends-on`
clause exists on this row** — confirmed by the frontmatter key census (188 task files carry frontmatter; only
7 carry `depends-on`), and independently filed as `BACKLOG.md:67` / `tasks/452-433-382-dependency-is-prose-only.md`.

Source of the "4-registry sprawl" phrase: `docs/intake/2026-07-21-func-fleet-north-star.md:44` (the L0 row,
"~25% — fragments, 4 registries, no single contract") and `:65` (the mapping table, "ONE schema-versioned
desired-state contract in `ecosystem/` — dissolves the 4-registry sprawl"). Still live and unchanged as of
`docs/intake/2026-07-28-north-star-delta-review.md:93` and `:126`.

---

## (i) THE 4-REGISTRY SPRAWL

### i.0 — Full census of `ecosystem/` (what is actually on disk)

Eleven tracked artifacts plus five per-repo directories. Line counts from `wc -l`.

- `ecosystem/registry.md` — 36 lines — human repo registry (hand-maintained)
- `ecosystem/index.yaml` — 651 lines — generated per-repo audit rollup
- `ecosystem/deployed-versions.yaml` — 49 lines — per-repo deployed methodology-corpus version
- `ecosystem/parity-surfaces.yaml` — 923 lines — surfaces × role-tiers parity contract
- `ecosystem/satellite-onboarding-rulings.yaml` — 69 lines — per-satellite onboarding-profile rulings
- `ecosystem/doc-code-edge.yaml` — 146 lines — doc→code edge scan scope + coverage
- `ecosystem/disposition-register.yaml` — 338 lines — known-WARN suppressions
- `ecosystem/dependency-baseline.yaml` — 34 lines — hub-recommended dependency pins
- `ecosystem/tool-versions.yaml` — 36 lines — per-tool last-reviewed changelog version
- `ecosystem/silent-rule-baseline.yaml` — 65 lines — one-number ratchet baseline
- `ecosystem/doc-counts.md` — 17 lines — generated count claims
- `ecosystem/{.dev-knowledge,ai-council,corp-monorepo,corp-ops,corp-sca-time-automation}/history/` — per-repo
  tracked audit history; `ecosystem/*/state.yaml` is gitignored (`.gitignore:61`)

### i.1 — Which four? The intake never says

**GAP (identity of the four):** no in-repo source enumerates the four registries individually. A repo-wide
sweep for `4 registr|four registr|4-registry|registry sprawl` returns only assertions of the *count*, never a
list: `docs/intake/2026-07-21-func-fleet-north-star.md:44,65,103,115`, `docs/intake/2026-07-28-north-star-delta-review.md:93,126`,
`BACKLOG.md:428,429`, `tasks/382-*.md:13`, `docs/audits/2026-07-28-technical-382-charter.md:21,69`. The
charter itself treats naming them as *future ADR work*, not settled fact — `docs/audits/2026-07-28-technical-382-charter.md:69`
requires the ADR to record "the schema's scope over the 4 registries it dissolves or absorbs (**named
individually**)". So the set is an open input to the arc, not a retrievable fact.

Two defensible readings exist on disk. This dossier presents both and picks neither.

**Reading A — the four self-describing REGISTRIES/REGISTERS keyed by repo.** Each of these calls itself a
registry or register in its own header, and each is keyed by repo id:
1. `ecosystem/registry.md` — "the human registry" (`ecosystem/registry.md:11`)
2. `ecosystem/index.yaml` — "the machine registry" (`ecosystem/registry.md:13-15`)
3. `ecosystem/deployed-versions.yaml` — the durable per-repo version record (`ecosystem/registry.md:16-17`;
   `ecosystem/deployed-versions.yaml:1-9`)
4. `ecosystem/satellite-onboarding-rulings.yaml` — "this register is that home" (`ecosystem/satellite-onboarding-rulings.yaml:8`)

Reading A is attractive because `ecosystem/registry.md:10-17` *itself* narrates items 1–3 as one registry split
across surfaces — i.e. the sprawl is self-documented at the source.

**Reading B — the four fleet-state surfaces a divergence report would have to join.** Substitutes
`ecosystem/parity-surfaces.yaml` (81 surface rows × 5 fleet repos, `ecosystem/parity-surfaces.yaml:98-105`) for
`satellite-onboarding-rulings.yaml`, on the grounds that the row's deliverable is "surface × repo ×
{conform/diverge/declared}" (`BACKLOG.md:429`), which only parity-surfaces expresses.

**Consequence to hand the architect:** under Reading A, parity-surfaces is *out* of the dissolution scope;
under Reading B, satellite-onboarding-rulings is. Both files are repo-keyed, both are hand-maintained, and
both hold onboarding-state opinions that already disagree (see conflict C3). The count "4" cannot cover both.

The per-registry detail below therefore covers **five** repo-keyed surfaces (the union of A and B), and flags
the six remaining `ecosystem/` files as the non-repo-keyed remainder.

### i.2 — Per-registry: path · purpose · current fields as they exist on disk

**R1 · `ecosystem/registry.md`** — hand-maintained human repo registry.
- Purpose, verbatim: "Hand-maintained human registry" (`:5`); "the human registry — name · path · purpose ·
  status, hand-maintained. Add a row when a repo is created; it needs no tooling" (`:11-12`).
- Shape: a markdown table, not structured data. Header `| Repo | Path | Purpose | Status |` (`:22`), separator
  `:23`, **8 data rows** (`:24-31`).
- Per-entry fields (4): `Repo` (backticked dir name) · `Path` (absolute Windows path) · `Purpose` (free prose
  distilled from each repo's VISION.md, `:19-20`) · `Status` (free prose).
- Rows: `.dev-knowledge` `:24`, `ai-council` `:25`, `corp-monorepo` `:26`, `corp-ops` `:27`,
  `corp-sca-time-automation` `:28`, `demo-prep` `:29`, `life-architect` `:30`, `win-tooling` `:31`.
- Status values observed (free text, no enum): `source (hub — methodology origin)` `:24` ·
  `registered · onboarded (v1.2.0)` `:25,:26` · `registered · unonboarded` `:27,:31` ·
  `registered · unonboarded (floor-carrying)` `:28` · `registered · methodology-unonboarded` `:29` ·
  `registered · methodology-unonboarded · GitHub origin CONFIRMED Private (operator, 2026-07-08)` `:30`.
- Maintenance contract: "The `Status` column's onboarding state tracks `ecosystem/deployed-versions.yaml`"
  and "Do not hand-fabricate a version here; read it from `deployed-versions.yaml`" (`:33-36`).
- **Read by no checker.** A grep of `scripts/` + `deploy/` for `registry.md` returns exactly one hit, and it is
  an *exclusion*: `scripts/fleet_analytics.py:602` names it under "Index-file contamination". Nothing validates
  its rows or its stated tracking contract.

**R2 · `ecosystem/index.yaml`** — generated per-repo audit rollup.
- Purpose: "`ecosystem/<repo>/` + `ecosystem/index.yaml` = the machine registry … `index.yaml` is **generated**
  (`audit.py::regenerate_index` overwrites it wholesale) — **never hand-edit it**" (`ecosystem/registry.md:13-15`);
  writer at `scripts/audit.py:3142-3143`; path constant `scripts/audit.py:173`.
- Top-level keys (2): `generated` (ISO timestamp, `:1`) · `repos` (list, `:2`).
- Per-entry keys (4, union across all 6 entries): `name` · `path` · `last_audit` · `findings`.
- Per-finding keys (3): `check_name` · `evidence` · `status` (e.g. `:4-7`).
- Population: 6 repos — `.dev-knowledge` (37 findings), `ai-council` (29), `corp-monorepo` (29), `corp-ops`
  (29), `corp-sca-time-automation` (29), `win-tooling` (29, name at `:650`, path at `:651`).
- `generated: '2026-07-11T12:30:02'` (`:1`); every `last_audit` is `2026-07-11`.
- Explicitly derived, not authoritative: "ecosystem/index.yaml is a derived rollup of these"
  (`scripts/audit.py:324`); "a field written there is clobbered" (`ecosystem/deployed-versions.yaml:4-5`).

**R3 · `ecosystem/deployed-versions.yaml`** — durable per-repo deployed-corpus version (ADR-91).
- Purpose, verbatim: "It records a DURABLE per-repo fact: which methodology-corpus release (the ADR-91 git tag
  vMAJOR.MINOR.PATCH) is deployed to each repo" (`:5-6`).
- Top-level keys (1): `repos` (`:24`).
- Per-entry keys (3): `deployed_methodology_version` · `deployed_date` · `source_tag`.
- Population: 5 repos — `.dev-knowledge` `:25-29` (all null), `ai-council` `:30-33`, `corp-monorepo` `:34-41`,
  `corp-ops` `:42-45` (all null), `corp-sca-time-automation` `:46-49` (all null).
- Write contract: "the fields are written by the DEPLOY-RUNBOOK (`deploy/tool.py --execute`) at deploy time …
  Do NOT hand-fabricate a value: a value cannot precede its release" (`:11-15`).
- Read by: `scripts/audit.py`, `scripts/enforcement_coverage.py`, `scripts/fleet_parity.py`,
  `scripts/gen_methodology_roster.py`, `deploy/tool.py`.

**R4 · `ecosystem/parity-surfaces.yaml`** — the #328 versioned parity contract.
- Purpose, verbatim: "ONE machine-readable contract: surfaces x role-tiers x one probe each" (`:3`).
- Top-level keys (3): `version` (`:11`, currently `1.3.0`) · `fleet` (`:98`) · `surfaces` (`:105`).
- `fleet` per-entry keys (1): `role`. Population 5 — `.dev-knowledge: {role: hub}` `:99`,
  `ai-council: {role: consumer}` `:100`, `corp-monorepo: {role: consumer}` `:101`,
  `corp-ops: {role: pre-deploy}` `:102`, `corp-sca-time-automation: {role: pre-deploy}` `:103`.
- `surfaces` — **81 rows**. Per-entry key union (13): `id` · `kind` · `tier` · `probe` · `ownership` ·
  `waivable` · `waiver_component` · `local_names` · `declared_by` · `declared_divergence` ·
  `pending_migration` · `join` · `gate_rev_ahead`. Grammar for each at `:18-88`.
- `kind` enum as declared `:22-24`, as populated: `path` 51 · `gitignore-effect` 9 · `command` 5 ·
  `settings-hook-block` 5 · `precommit-hook` 5 · `doc-marker` 3 · `tombstone-join` 1 · `claude-subtree` 1 ·
  `roster` 1.
- `tier` keys observed: `hub` (65 rows) · `consumer` (55) · `corp-monorepo` (7) · `ai-council` (5) — i.e. the
  map is keyed by ROLE **or** by REPO-ID, repo-id overriding role (`:25-27`). Token counts: `MUST` 85 ·
  `LOCAL` 23 · `IGNORE` 16 · `INVERSE` 3 · `SHOULD` 3 · `TOMBSTONE` 2.
- `probe.type` values populated (16 distinct): `dir_tracked` 21 · `path_tracked` 18 · `check_ignore` 9 ·
  `file_contains` 7 · `command_present` 5 · `dir_exists` 4 · `precommit_hook` 4 · `settings_hook` 3 ·
  `file_exists` 2 · `precommit_remote` 2 · `glob_tracked` 1 · `plugin_enabled` 1 · `settings_local_blocks` 1 ·
  `ruff_config_form` 1 · `claude_subtrees` 1 · `commands_roster` 1.
- `ownership.value` closed enum (`:68-70`): `methodology-generic` 57 · `conditional` 15 · `project` 9. Mandatory
  on every row; loader refuses a missing/malformed block (`:63-64`).
- Sparse fields (how many rows carry them): `waivable` 1 · `waiver_component` 1 · `local_names` 2 ·
  `declared_by` 10 (`src-dir`, `ruff-config-home`, `corp-local-data`, `corp-local-eval`, `corp-local-models`,
  `local-output-dir`, `corp-docs-diagrams`, `ai-local-council-inbox`, `ai-local-transcripts`, `ai-local-assets`) ·
  `declared_divergence` 1 (`audit-casing-r4`) · `join` 1 (`ruff-gate`) · `pending_migration` 1 (`ruff-gate`) ·
  `gate_rev_ahead` 1 (`precommit-hub-block`, `:416-435`).
- Verdict vocabulary declared at `:90-96`: `AT-PARITY | PASS-declared | WARN-undeclared | MUST-absent |
  tombstone-violated` (+ `advisory-rewarn | stale-declaration | refused | unavailable | skipped-pre-deploy |
  tracked-ephemera | gate-ahead-declared`).
- Cross-check grammar, verbatim: "every ecosystem/deployed-versions.yaml registry key MUST appear here
  (cross-checked both directions by the checker; mismatch = refusal finding)" (`:14-16`).

**R5 · `ecosystem/satellite-onboarding-rulings.yaml`** — per-satellite onboarding-profile rulings.
- Purpose, verbatim: "the canonical hub-side record of the operator's onboarding-PROFILE ruling for each
  satellite consumer (full gate set vs floor-only)" (`:3-5`); "this register is that home" (`:8`).
- Top-level keys (2): `version` (`:25`, currently `1`) · `rulings` (`:27`).
- Per-entry keys as declared `:20-23`: `profile` (`full | floor-only`) · `ruled_by` · `ruled_date` ·
  `census_ref` · optional `gating` · optional `override` block `{proposed, proposed_by, proposed_reason,
  ruled, ruled_by, ruled_reason}`.
- Population: 4 — `corp-ops` `:28-32`, `corp-sca-time-automation` `:34-42` (carries `gating`),
  `life-architect` `:44+` (carries `override`), `demo-prep` `:65+`.
- Explicitly decoupled, verbatim: "this file is NOT read by scripts/fleet_parity.py and does NOT touch
  ecosystem/parity-surfaces.yaml … It records the TARGET-PROFILE ruling — a decision — not deployed state"
  (`:10-13`). Read by `scripts/validate_onboarding_rulings.py`, wired into no blocking gate (`:15-18`).

**Non-repo-keyed remainder (6 files, listed so the architect can rule them in or out of scope):**
- `ecosystem/doc-code-edge.yaml` — top-level keys (4): `declaration_docs` (3 entries, `:27-30`) ·
  `coverage_scope` (14, `:63-77`) · `multi_site` (9 rule→int, `:86-95`) · `exempt` (25 check names, `:106-142`).
  Self-described as "Doc->code edge declaration-doc registry" (`:1`). Keyed by rule-ID and check-name.
- `ecosystem/disposition-register.yaml` — top-level key (1): `dispositions` (`:29`), 15 live entries.
  Per-entry keys (7 union): `id` · `organ` · `match` · `ref` · `reason` · `auto_clearable_by` · `review_date`
  (declared `:9-17`). Keyed by WARN signature.
- `ecosystem/dependency-baseline.yaml` — `version` (`:23`, `1.0.0`) · `dependencies` (`:25`, 1 entry).
  Per-entry keys (5): `name` · `recommended` · `applies_to` · `rationale` · `status` (`:30-34`).
  `applies_to` uses a role vocabulary `[hub, consumer]` (`:32`).
- `ecosystem/tool-versions.yaml` — `tools` (`:18`), 2 entries (`claude-code` `:19-27`, `codex` `:28-36`).
  Per-entry keys (3): `last_reviewed_version` · `reviewed_date` · `source_url`. Keyed by tool, not repo.
- `ecosystem/silent-rule-baseline.yaml` — 6 scalar top-level keys: `detector_id` `:20` · `baseline` `:21` ·
  `measured_at` `:22` · `measured_at_sha` `:23` · `measured_files` `:24` · `provenance` `:26-38`. No entries.
- `ecosystem/doc-counts.md` — generated fragment (`:9`), three count claims between markers `:12-17`:
  35 registered checks, 15 pre-commit gates, 1991 tests collected.

### i.3 — Cross-registry OVERLAP: which concepts appear in more than one registry

- **Repo identity (the key itself)** — R1 `:24-31` (8) · R2 `repos[].name` (6) · R3 `repos:` `:24` (5) ·
  R4 `fleet:` `:98-103` (5) · R5 `rulings:` `:27` (4). Five different membership sets; see C1.
- **Repo filesystem path** — R1 `Path` column `:24-31` and R2 `repos[].path` (e.g. `:651`) both hold the same
  absolute Windows path. R3/R4/R5 hold only the bare directory name. Two registries carry a location, three
  carry an identifier; see C6.
- **Onboarding / deployment state** — R1 `Status` `:24-31` (free prose) · R3 `deployed_methodology_version`
  (version-or-null) · R4 `fleet[].role` (`hub|consumer|pre-deploy`) · R5 `profile` (`full|floor-only`). Four
  registries hold four different answers to "where is this repo in the methodology lifecycle"; see C2/C3.
- **Version pin** — R3 `deployed_methodology_version` + `source_tag`, and R4's `precommit-hub-block` row whose
  probe reads `expected_rev_from: deployed-versions` (`ecosystem/parity-surfaces.yaml:407-409`), plus its
  `gate_rev_ahead.corp-monorepo.gate_tag: v1.3.1` (`:417-418`). One concept, two homes, one deliberate
  divergence modelled as data; see C4.
- **Declared divergence / waiver** — R4 `waiver_component` + `declared_by` + `declared_divergence` point OUT to
  `.methodology.yaml` (`ecosystem/parity-surfaces.yaml:40-43`, `:47-49`, `:51-54`), which lives outside
  `ecosystem/` entirely (`/.methodology.yaml`). Meanwhile `ecosystem/disposition-register.yaml` holds a
  structurally similar suppression concept keyed to audit WARNs. Two suppression vocabularies; see C7.
- **Provenance / justification grammar** — R4 uses `{value, reason, provenance:[{kind,repo,ref}]}`
  (`:63-74`); R5 uses `{ruled_by, ruled_date, census_ref}` (`:20-21`); `disposition-register` uses
  `{ref, reason}` (`:12-15`); `silent-rule-baseline` uses a free-text `provenance:` block (`:26-38`);
  `dependency-baseline` uses `rationale` (`:33`). Five grammars for "why".
- **Review/expiry timing** — R5 has none; `.methodology.yaml` entries carry `review_date` (e.g. `:19,:57,:108`);
  `disposition-register` carries optional `review_date` (`:17` declares it); R4's `gate_rev_ahead` explicitly
  has **no** review_date and is self-invalidating instead (`ecosystem/parity-surfaces.yaml:83-85`).
- **Rule identity** — `doc-code-edge.yaml` keys on rule-ID (`:63-77`); `parity-surfaces.yaml` keys on surface
  id (`:18-21`); `disposition-register.yaml` keys on organ + evidence substring (`:10-13`). Three id spaces,
  no declared mapping between them.

### i.4 — Cross-registry CONFLICT: where they disagree

**C1 — Fleet membership disagrees five ways.**
- R1 (8): `.dev-knowledge, ai-council, corp-monorepo, corp-ops, corp-sca-time-automation, demo-prep,
  life-architect, win-tooling` (`ecosystem/registry.md:24-31`)
- R2 (6): the five above minus `demo-prep`/`life-architect`, plus `win-tooling` (`ecosystem/index.yaml:650`)
- R3 (5): no `win-tooling`, no `demo-prep`, no `life-architect` (`ecosystem/deployed-versions.yaml:24-49`)
- R4 (5): identical set to R3, by explicit grammar (`ecosystem/parity-surfaces.yaml:14-16`)
- R5 (4): `corp-ops, corp-sca-time-automation, life-architect, demo-prep` (`ecosystem/satellite-onboarding-rulings.yaml:28,34,44,65`)
  — two of which (`life-architect`, `demo-prep`) appear in **no** other yaml registry.
The registries are aware of the split and encode it as an audit finding rather than resolving it:
`ecosystem/index.yaml:633` reads `evidence: win-tooling not listed in deployed-versions.yaml (ADR-91)`.

**C2 — `registry.md` contradicts `deployed-versions.yaml` on ai-council's version, against its own stated rule.**
`ecosystem/registry.md:25` records ai-council as `registered · onboarded (v1.2.0)`. `ecosystem/deployed-versions.yaml:31-33`
records `deployed_methodology_version: "1.3.1"` / `source_tag: "v1.3.1"` / `deployed_date: "2026-07-11"`.
`ecosystem/registry.md:33-36` states the Status column "tracks `ecosystem/deployed-versions.yaml`" and "Do not
hand-fabricate a version here; read it from `deployed-versions.yaml`". The human registry is one minor release
stale against the record it declares itself derived from, and **no checker reads it** (only exclusion hit:
`scripts/fleet_analytics.py:602`), so the drift is structurally undetectable.

**C3 — Two registries hold contradictory partial answers on `corp-ops` / `corp-sca-time-automation`.**
R4 assigns both `role: pre-deploy` (`ecosystem/parity-surfaces.yaml:102-103`) and R3 records all three version
fields as `null` (`ecosystem/deployed-versions.yaml:42-49`) — i.e. "nothing deployed". R5 simultaneously
records an operator-**ruled** `profile: full` for both (`ecosystem/satellite-onboarding-rulings.yaml:28-32,34-38`),
which is a *target* commitment. R5 states the decoupling as deliberate (`:10-13`), but the effect is that the
intended end-state and the observed state live in different files with no declared relation between them, and
one of them (R5) is read by a checker wired into no gate (`:15-18`).

**C4 — `corp-monorepo` carries a sanctioned version contradiction, modelled twice.**
R3 pins `deployed_methodology_version: "1.2.0"` with an in-file instruction not to correct it
(`ecosystem/deployed-versions.yaml:35-41`: "Stays 1.2.0 BY DESIGN … Do not 'fix' to 1.3.1"). R4 encodes the
same fact from the other side as `gate_rev_ahead.corp-monorepo.gate_tag: v1.3.1`
(`ecosystem/parity-surfaces.yaml:416-435`). Neither file is wrong; the same one fact is asserted in two
different vocabularies (a prose "do not fix" comment vs a typed refinement block with provenance), and only
one of the two is machine-readable.

**C5 — Lifecycle-state vocabularies do not share tokens.**
R1 Status free text (`source (hub…)`, `registered · onboarded (vX)`, `registered · unonboarded`,
`registered · unonboarded (floor-carrying)`, `registered · methodology-unonboarded`) `:24-31` ·
R4 `role` enum `{hub, consumer, pre-deploy}` `:99-103` · R5 `profile` enum `{full, floor-only}` `:20` ·
R3 version-or-null `:25-49`. No file declares a mapping. `registered · unonboarded (floor-carrying)` (`:28`)
in particular has no representation in any enum.

**C6 — Granularity mismatch on the key itself.** R1 and R2 hold an absolute Windows path
(`C:\Users\1028120\Documents\Dev\...`, `ecosystem/registry.md:24-31`, `ecosystem/index.yaml:651`); R3/R4/R5
hold a bare directory name used as the join key (`ecosystem/deployed-versions.yaml:23` states this explicitly:
"Keyed by repo directory name (the audit's repo id)"). The join across registries is therefore
name-on-name; nothing validates that R1/R2's path and R3/R4/R5's name denote the same repo.

**C7 — Two suppression mechanisms with different scope semantics.** `.methodology.yaml`
`sanctioned_divergences[].component` suppresses a *parity surface* WARN via `waiver_component`
(`ecosystem/parity-surfaces.yaml:40-43`) and requires uniqueness — "UNIQUE across rows: one declaration can
never suppress two concerns (disposition-register grammar, one-per-concern)" (`:42-43`).
`ecosystem/disposition-register.yaml` suppresses an *audit organ* WARN by evidence substring (`:10-13`) and
carries the same one-per-concern rule (`:19-22`). Same doctrine, two files, two id spaces, and R4's MUST rows
are explicitly non-waivable through the first mechanism (`:36-39`, `:87-88`) but nothing states the interaction
with the second.

**C8 — The derived registry is 20 days stale and asserts a superseded fact.**
`ecosystem/index.yaml:1` reads `generated: '2026-07-11T12:30:02'`; every `last_audit` is `2026-07-11`.
`ecosystem/index.yaml:44-46` records `evidence: All stamp occurrences … match canonical HANDOFF_PROCESS v5.7`,
while `protocols/HANDOFF_PROCESS.md:4` now reads `Version: 6.0.1`. The rollup is regenerate-on-demand
(`scripts/audit.py:3142`) with no freshness gate, so a stale generated registry reads as current data.

---

## (ii) EDGE-TAXONOMY CENSUS

The [#382] row names four edge kinds — "doc2doc/doc2file/hooks/skills" (`BACKLOG.md:429`). Below is every
edge-declaring shape found by sweeping `ecosystem/*.yaml`, `scripts/`, `deploy/`, `.pre-commit-config.yaml`,
`.claude/`, `tasks/`, and the canonical docs. **Twelve distinct declaration shapes** were found across the four
named kinds plus four unnamed ones.

### ii.1 — doc2doc (declared version-reconciliation edges)

- **Where declared:** YAML frontmatter key `reconciled_with` in the dependent doc; the spec side is a curated
  Python dict `_SPEC_REGISTRY` at `scripts/validate_reconciliation.py:79-84`.
- **Counts:** the registry holds exactly **1 spec** (`handoff-process` → `protocols/HANDOFF_PROCESS.md`,
  `scripts/validate_reconciliation.py:80-83`). Live run of `scripts/validate_reconciliation.py` reports
  **7 edges, 0 mismatches** — 6 resolving (`ARCHITECTURE.md`, `CLAUDE.md`, `CONTRIBUTING.md`,
  `docs/handoffs/README.md`, `protocols/HANDOFF_BOOT.md`, `protocols/README.md`, all `@6.0.1`) and 1 malformed
  (`templates/CONTRIBUTING-md-template.md`, which carries the literal placeholder).
- **Per file:** `CLAUDE.md:3` · `ARCHITECTURE.md:3` · `CONTRIBUTING.md:3` · `protocols/HANDOFF_BOOT.md:2` ·
  `protocols/README.md:2` · `templates/CONTRIBUTING-md-template.md:3` (placeholder) ·
  `docs/handoffs/README.md` (frontmatter). A repo-wide grep for the token returns 110 occurrences, but the
  overwhelming majority are prose mentions inside immutable handoff bundles and JOURNAL entries — not edges.
- **Shape 1 (frontmatter scalar):** `reconciled_with: handoff-process@6.0.1` (`CLAUDE.md:3`)
- **Discovery complement:** `scripts/scan_undeclared_edges.py:2-49` finds prose references to a registered spec
  that carry no `reconciled_with` line. It scans only `vr._SPEC_REGISTRY` — i.e. the same single spec
  ("Specs scanned = the curated vr._SPEC_REGISTRY (narrow-first). No broadening to 'all ADRs'", `:48`).

### ii.2 — doc2code (doc→code rule edges)

- **Where declared:** `ecosystem/doc-code-edge.yaml` (scan scope + coverage) plus paired in-file markers.
- **Counts:** `declaration_docs` **3** (`:27-30`: `protocols/PLAYBOOK.md`, `protocols/DEFINITION_OF_DONE.md`,
  `protocols/HANDOFF_PROCESS.md`) · `coverage_scope` **14** rule IDs (`:63-77`) · `multi_site` **9** entries
  (`:86-95`) · `exempt` **25** check names (`:106-142`).
- **Doc-side markers, per file (live, excluding placeholder forms):** `protocols/PLAYBOOK.md` 11 live
  (`:376, :988, :1003, :1013, :1021, :1027, :1033, :1556, :3314, :3325, :3344`) plus 3 teaching placeholders
  (`:270, :611, :615`, deliberately unmatched per `:615`) · `protocols/HANDOFF_PROCESS.md` 2
  (`:85, :111`) · `protocols/DEFINITION_OF_DONE.md` 1 (`:24`). **Total live doc-side = 14**, exactly matching
  `coverage_scope`.
- **Code-side markers:** **25** across 14 files — `scripts/audit.py` 12 (`:723, :1080, :1160, :1277, :1316,
  :1355, :1439, :1477, :1683, :1776, :2961`, plus one), `scripts/validate_backlog.py` 3 (`:277, :299, :313`),
  and one each in `assemble_paste.py:165`, `block_ff_push.py:177`, `generate_floor.py:301`,
  `session_end_backpressure.py:278`, `validate_doc_claims.py:158`, `validate_doc_rot.py:220`,
  `validate_doc_structure.py:309`, `validate_git_backlog.py:83`, `validate_no_ff.py:105`,
  `validate_reconciliation.py:221`, `verify_handoff_probes.py:464`. This reconciles exactly: 9 multi_site rules
  summing to 20 sites + 5 single-site rules = 25.
- **Out-of-scope live-looking markers:** `BACKLOG.md:405` and `tasks/365-*.md:13` carry
  `<!-- rule: handoff-residual-filled -->`, but neither file is in `declaration_docs`, and the scan is an
  include-list ("The scan reads ONLY these files", `ecosystem/doc-code-edge.yaml:9`). The rule is
  simultaneously listed as `exempt` with a documented reason and a bound ticket (`:106-141`, entry
  `residual_completeness` at `:136`).
- **Shape 2 (paired in-file comment markers, two syntaxes for one identity):**
  doc side `<!-- rule: seal-journal-anchor -->` (`protocols/DEFINITION_OF_DONE.md:24`) ↔
  code side `# rule: seal-journal-anchor` (`scripts/session_end_backpressure.py:278`)
- **Shape 3 (expected-arity map):** `coherence-spec-reconciled: 2` (`ecosystem/doc-code-edge.yaml:87`)
- **Shape 4 (bare exclusion list):** `- vision_md` (`ecosystem/doc-code-edge.yaml:107`)

### ii.3 — doc2file (`@import` edges)

- **Where declared:** bare `@path` lines in `CLAUDE.md`; checked by `scripts/audit.py:2364-2372`
  (`check_import_edges`, BFS, depth ≤ 5, FAIL on a broken target).
- **Counts: 3 edges, all from `CLAUDE.md`** — `:130` `@.claude/generated/commands-repo.md`, `:189`
  `@.claude/methodology-roster.md`, `:212` `@.claude/generated/recent-adrs.md`. No second-level imports.
- **Shape 5 (bare path line):** `@.claude/generated/commands-repo.md` (`CLAUDE.md:130`)
- Note the check verifies *target existence only*: "every Claude-Code `@import` target reachable from the root
  CLAUDE.md exists" (`scripts/audit.py:2365`). Nothing verifies target currency.

### ii.4 — hooks

Three separate declaration surfaces, three formats, no shared registry.

- **Pre-commit (`.pre-commit-config.yaml`): 15 hook ids.** `normalize-dated-headers` `:22` ·
  `codemap-freshness` `:28` · `toc-freshness-playbook` `:34` · `roster-freshness` `:42` ·
  `claude-rosters-freshness` `:55` · `audit-index-freshness` `:67` · `validate-hermetization` `:79` ·
  `intake-index-freshness` `:92` · `validate-backlog` `:103` · `audit-health` `:109` · `coherence-nudge` `:118` ·
  `backlog-id-on-close` `:128` · `backlog-filing-backpressure` `:134` · `block-ff-push` `:143` · `ruff` `:165`.
  Count corroborated by `ecosystem/doc-counts.md:15` ("pre-commit gates (15)").
- **Shape 6 (pre-commit entry):** `      - id: block-ff-push` with `entry: uv run --locked python scripts/block_ff_push.py`
  (`.pre-commit-config.yaml:143,150`)
- **Session hooks (`.claude/settings.json`): 7 command declarations** across 3 events — `Stop` 1
  (`scripts/session_end_backpressure.py`) · `PreToolUse` 1 (matcher `Edit|MultiEdit|Write|NotebookEdit`,
  `scripts/hooks/block_immutable_edits.py`) · `SessionStart` 5 (`fleet_health.py`, `surface_triage.ps1`,
  `billing_leak_sentinel.ps1`, `changelog_sentinel.py`, `arm_hooks.py`).
- **Shape 7 (JSON hook object):** `{"type": "command", "command": "uv run --locked python \"$CLAUDE_PROJECT_DIR/scripts/session_end_backpressure.py\"", "timeout": 15}`
  (`.claude/settings.json`, `Stop` block)
- **Plugin hooks (`plugins/tier1-lifecycle/hooks/hooks.json`): 1** — `Stop` → `propose_closures.py`. Same JSON
  grammar as Shape 7 but a different root variable (`${CLAUDE_PLUGIN_ROOT}` vs `$CLAUDE_PROJECT_DIR`) and a
  documented reason no SessionStart hook can live there ("plugin hooks register too late for the one-shot
  SessionStart init event and never fire (verified 2026-06-02)").
- **Hooks as parity surfaces:** `ecosystem/parity-surfaces.yaml` models hooks as 5 `precommit-hook` rows +
  5 `settings-hook-block` rows, probed by `precommit_hook` (4), `precommit_remote` (2), `settings_hook` (3),
  `settings_local_blocks` (1). This is a *third* representation of the same organs — by canonical surface id,
  not by hook id ("id — canonical id (FR-2): stable, independent of local filename / hook id / byte shape",
  `ecosystem/parity-surfaces.yaml:18-20`).
- **Shape 8 (parity surface row):**
  `- id: precommit-hub-block` / `kind: precommit-hook` / `tier: {consumer: MUST}` /
  `probe: {type: precommit_remote, repo_token: dev-knowledge, expected_rev_from: deployed-versions, ancestry: true, required_hook_ids: [backlog-id-on-close, block-ff-push]}`
  (`ecosystem/parity-surfaces.yaml:404-409`)

### ii.5 — skills

- **On disk: 2 repo-level skills** — `.claude/skills/verify/SKILL.md`, `.claude/skills/check-against-spec/SKILL.md`.
- **Edge declarations found: zero.** No registry declares what a skill depends on, governs, or is invalidated
  by. The only machine-readable mentions of `skills` anywhere are:
  - `ecosystem/parity-surfaces.yaml:808,810` — the `claude-subtree-ownership` row, which lists `skills` as an
    *owned subtree token* per repo (`.dev-knowledge: [agents, generated, hooks, rules, skills, workflows]`,
    `corp-monorepo: [skills, workflows]`). This declares directory ownership, not an edge.
  - `deploy/manifest-v1.4.0.yaml:135` — a deferred `l0_scope` target string for the user-level `gotchas` skill.
  - `deploy/manifest-v1.4.0.yaml:254` — `skill` as a member of the component `kind` enum
    (`organ | hook | command | skill | doc-shape | config`).
- **Shape 9 (subtree ownership token list):** `.dev-knowledge: [agents, generated, hooks, rules, skills, workflows]`
  (`ecosystem/parity-surfaces.yaml:808`)

### ii.6 — Edge kinds present on disk that the [#382] row does NOT name

- **Boundary-region edges (canon ↔ template extract).** `CLAUDE.md` carries **15** Form-A regions
  (`:19, :33, :47, :59, :76, :84, :92, :98, :105, :127, :148, :159, :195, :208, :218`; two further textual
  occurrences at `:227` and `:232` are prose about the markers, not markers). 8 of those are `owner=hub` and
  must stay byte-identical to extracts in `templates/claude-regions/` (8 files:
  `antipatterns-universal.md`, `conventions-commit-branch.md`, `conventions-output-formatting.md`,
  `critical-rules-consistency.md`, `critical-rules-no-leftovers.md`, `critical-rules-records.md`,
  `first-read.md`, `session-start-protocol.md`). Parsed by `scripts/boundary_report.py:55-58` / `:73`.
  - **Shape 10 (attributed HTML region marker):** `<!-- methodology:start id=first-read owner=hub -->` (`CLAUDE.md:19`)
- **Task dependency edges.** `tasks/` holds 190 files, 188 with frontmatter; frontmatter key counts:
  `id`/`title`/`status`/`priority`/`size`/`theme`/`story`/`generates` 188 each, `serialize-group` 133,
  **`depends-on` 7**. Two incompatible value forms coexist:
  - **Shape 11a (hashed):** `depends-on: "#23"` (`tasks/112-adr-amend-helper-adr-immutable-zone-extension.md:10`)
  - **Shape 11b (bare):** `depends-on: "382"` (`tasks/383-execution-waves-per-surface.md:10`)
  Only 11a parses: `scripts/validate_backlog.py:78` compiles `#(\d+)`, so bare clauses yield `[]`. Filed as
  `BACKLOG.md:53` / `tasks/424-*.md:13`, which censuses 8 clauses, 4 parsing and 4 inert, and notes the inert
  four are the [E9] chain itself. A twelfth shape carries the same concept in prose inside the BACKLOG row body
  (`· depends-on: #270 ·` and `· refs #382, #387 ·`, e.g. `BACKLOG.md:250`).
- **Computed code→code edges.** `scripts/reverse_dep_oracle.py:1-41` computes reverse dependencies via a
  headless Pyright LSP rather than declaring them ("code edges are *computed* from source, never declared via
  `reconciled_with`", `:7-8`). It declares its own blind spots explicitly: "ALL cross-language edges
  (markdown->script, settings.json / .pre-commit hook-wiring, plugin manifests) are INVISIBLE" (`:18-19`).
  It is not wired into `ALL_CHECKS` and is not a gate (`:24-27`).
- **Carrier/component edges (hub → consumer).** `deploy/manifest-v1.4.0.yaml` declares carriers, components,
  anchors and doc_shapes (`:62-94`); it is the only surface expressing hub→consumer material flow.
  - **Shape 12 (carrier target block):** `target: {source_path: codex/AGENTS.md, target_filename: AGENTS.md}`
    (`deploy/manifest-v1.4.0.yaml:117-119`)

### ii.7 — FORMAT VARIANCE, summarized

**12 distinct declaration shapes** express dependency across 4 named kinds + 4 unnamed ones. They vary on
every axis at once:
- **Syntax:** YAML frontmatter scalar (1) · paired HTML/Python comment tokens (2) · YAML map value (3) ·
  YAML list item (4) · bare text line (5) · pre-commit YAML entry (6) · JSON object (7) · nested YAML row with
  typed sub-blocks (8) · YAML token list (9) · attributed HTML comment (10) · frontmatter scalar with two
  incompatible value grammars (11a/11b) · YAML target block (12).
- **Identity space:** spec-id · rule-ID · check-name · surface-id · hook-id · region-id · task-id ·
  component-id · Python symbol. Nine id spaces, no declared crosswalk.
- **Directionality:** doc→spec (1), doc↔code (2), doc→file (5), config→script (6,7), hub→consumer (8,12),
  canon→extract (10), task→task (11).
- **Enforcement posture:** FAIL-gating (`import_edges`, `doc_code_coverage_drift`), WARN-only
  (`fleet_parity`, `undeclared_edges`, `doc_code_edge`), never-gates (`reverse_dep_oracle`,
  `validate_onboarding_rulings`), and inert-by-parser-defect (`depends-on` bare form).

---

## (iii) WHAT `deployed-versions.yaml` + THE PER-CONSUMER PINS HOLD TODAY

### iii.1 — `ecosystem/deployed-versions.yaml` (verbatim, `:24-49`)

```
repos:
  .dev-knowledge:
    # The hub IS the methodology source; its entry = the release the hub itself is at.
    deployed_methodology_version: null
    deployed_date: null
    source_tag: null
  ai-council:
    deployed_methodology_version: "1.3.1"
    deployed_date: "2026-07-11"
    source_tag: "v1.3.1"
  corp-monorepo:
    # Stays 1.2.0 BY DESIGN — corp's hub-block pin v1.3.1 is an enforcement-gate carrier
    # repoint (2 hooks), not a corpus deploy; modeled as ADR-102 gate_rev_ahead in
    # parity-surfaces.yaml. #336/ADR-102 (Accepted 2026-07-17) ruled NOT to bump,
    # superseding corp JOURNAL:937's owed-bump note. Do not "fix" to 1.3.1.
    deployed_methodology_version: "1.2.0"
    deployed_date: "2026-07-07"
    source_tag: "v1.2.0"
  corp-ops:
    deployed_methodology_version: null
    deployed_date: null
    source_tag: null
  corp-sca-time-automation:
    deployed_methodology_version: null
    deployed_date: null
    source_tag: null
```

So the state file records, per repo, exactly **three** scalars, and for 3 of 5 repos all three are `null`. Its
own semantics for null are declared at `:18-20`: "audit.py::check_deployed_methodology_version reads THIS file
(per repo, by repo dir name) and reports status — `n/a` while null (no release deployed yet), `pass` with the
version once set".

The hub's own row is null **by design** (`:26`), yet the hub is a declared fleet MEMBER
(`ecosystem/parity-surfaces.yaml:5-7`, "the hub is a fleet MEMBER, not an implicit exception") and carries
`role: hub` (`:99`). So the state file has no representation of the hub's own corpus position.

### iii.2 — Per-consumer pin surfaces

**(a) The consumer pre-commit rev pin** — the only true "per-consumer version pin" the [#382] row refers to.
It is not stored in `ecosystem/`; it lives in each consumer's own `.pre-commit-config.yaml` and is *probed*
from the hub. `ecosystem/parity-surfaces.yaml:398-401` states the contract verbatim: "consumers pin
rdwornik/dev-knowledge to the TAG their deployed-versions record says was deployed (present != carried; effect
probe = rev equality vs source_tag + tag existence/ancestry in the hub repo itself), AND the block must carry
the required hook IDS". The probe (`:407-409`):
`probe: {type: precommit_remote, repo_token: dev-knowledge, expected_rev_from: deployed-versions, ancestry: true, required_hook_ids: [backlog-id-on-close, block-ff-push]}`.

**GAP: the consumer-side value is not readable from this repo.** Only the hub's own `.pre-commit-config.yaml`
is on disk here; consumer configs live in the consumer repos. What is recorded hub-side is the *expectation*
plus one declared exception (below).

**(b) The one declared pin exception** — `ecosystem/parity-surfaces.yaml:416-435`, `gate_rev_ahead`:
```
      corp-monorepo:
        gate_tag: v1.3.1
        reason: >-
          Enforcement gate uplifted ahead of corpus: block-ff-push +
          backlog-id-on-close (#318/#319 range-reconstruction fixes) landed in
          corp's dev-knowledge hub-block pin, while corp's corpus body stays at
          v1.2.0 -- a full redeploy would re-append the codemap-freshness hook
          corp removed (#276 unlanded), and record-stamping v1.3.1 would
          over-claim a corpus that was never deployed. Strictly ahead of corpus,
          not a pin-revert.
        provenance:
          - {kind: git-tag, repo: .dev-knowledge, ref: v1.3.1}
          - {kind: git-commit, repo: corp-monorepo, ref: efe5bd1}
          - {kind: backlog, repo: .dev-knowledge, ref: "#336"}
```
It is explicitly not a waiver: "a HUB manifest expectation, NOT a .methodology.yaml waiver … it NEVER waives
the MUST" (`:77-82`).

**(c) `.methodology.yaml` (hub's own, `/.methodology.yaml`)** — the sanctioned-divergence register.
- Purpose, verbatim `:1-7`: "the .dev-knowledge repo's OWN sanctioned-divergence register, read by the hub
  Informant (scripts/enforcement_coverage.py, [#244] P4/D2) and the #328 fleet_parity checker (FR-4) … Each
  entry: component id + MANDATORY reason + time-box (expiry or review_date)."
- Top-level keys (1): `sanctioned_divergences` (`:8`). Per-entry keys (3): `component` · `reason` ·
  `review_date`.
- **15 entries** (`- component:` items): `hub-hermetization-rule-a` `:11` ·
  `hub-hermetization-rule-b-grammar` `:20` · `adr77-transcript-guard` `:29` · `token-log` `:52` ·
  `command-handoff` `:58` · `command-handoff-verify` `:64` · `command-save` `:73` ·
  `command-changelog-review` `:79` · `ruff-gate` `:87` · `.vscode` `:101` · `.claude-plugin` `:109` ·
  `.worktreeinclude` `:116` · `codex` `:123` · `package.json` `:130` · `package-lock.json` `:137`.
- **It holds no version field at all.** `.methodology.yaml` is a divergence register, not a pin file. The
  "per-consumer version pin" of the [#382] row is (a) above, not this file.
- Review dates observed range `2026-08-26` (`:108`, `.vscode`, deliberately short-shelf-life to force the e1
  ruling) through `2026-10-25` (`:49`).

**(d) `deploy/manifest-v*.yaml`** — six manifests on disk (`v1.0.0, v1.1.0, v1.2.0, v1.3.0, v1.3.1, v1.4.0`).
The current cut declares `methodology_version: "1.4.0"` (`deploy/manifest-v1.4.0.yaml:58`) and
`source_tag: v1.4.0` (`:59`), with `anchors: {plugin_version: "0.1.11", floor_sha256: "4d268f32…8111f"}`
(`:96-105`) and the precommit carrier's `hub_hooks.rev: v1.4.0` (`:181-182`). The three anchors must agree:
"source_tag (the ADR-91 git tag), methodology_version (must == source_tag), and the precommit carrier's
hub_hooks.rev (must == source_tag)" (`:70-73`).

**Consequence, stated as fact not judgment:** the manifest declares v1.4.0 as the target corpus, while the
highest value any repo records in `deployed-versions.yaml` is `1.3.1` (ai-council, `:31`), and the v1.4.0
carrier that motivated the cut is `implemented: false` (`deploy/manifest-v1.4.0.yaml:18-19`: "The carrier is
DECLARATION-ONLY at this cut (implemented: false) — the hub half is built, the consumer write-through is the
next ticket"). Independently confirmed still true at `docs/intake/2026-07-28-north-star-delta-review.md:129`.

### iii.3 — Mutable vs durable split

`ecosystem/*/state.yaml` is gitignored (`.gitignore:61`) and is the mutable audit pointer; only
`ecosystem/<repo>/history/*.md` is tracked. Four per-repo directories exist with a `history/` subdir
(`ai-council`, `corp-monorepo`, `corp-ops`, `corp-sca-time-automation`) plus `.dev-knowledge`. The durable/mutable
doctrine is stated at `ecosystem/deployed-versions.yaml:3-9` and `ecosystem/tool-versions.yaml:3-7` (ADR-80 §3).

---

## (iv) HONEST GAPS

Each is a statement of what no registry records. None is a proposed field.

**G1 — Nothing today records the identity of the four registries the North Star says will dissolve.** The count
"4" appears in 8 places (`docs/intake/2026-07-21-func-fleet-north-star.md:44,65,103,115`;
`docs/intake/2026-07-28-north-star-delta-review.md:93,126`; `BACKLOG.md:428-429`); the membership appears in
none, and the charter defers naming them to the ADR (`docs/audits/2026-07-28-technical-382-charter.md:69`).
Two defensible readings differ on whether `parity-surfaces.yaml` or `satellite-onboarding-rulings.yaml` is in
scope (§i.1).

**G2 — Nothing today records fleet membership authoritatively.** Five registries hold five different repo sets
(8 / 6 / 5 / 5 / 4, §i.4 C1). `parity-surfaces.yaml:14-16` declares a both-directions cross-check against
`deployed-versions.yaml` only — so `registry.md`, `index.yaml`, and `satellite-onboarding-rulings.yaml`
membership is unchecked against anything.

**G3 — Nothing today records a repo's methodology lifecycle position in one vocabulary.** Four registries hold
four contradictory partial answers (free prose / version-or-null / role enum / profile enum) with no declared
mapping (§i.4 C5). `registered · unonboarded (floor-carrying)` (`ecosystem/registry.md:28`) is expressible in
no enum on disk.

**G4 — Contradictory partial answers on satellite state.** `deployed-versions.yaml:42-49` says nothing is
deployed to `corp-ops`/`corp-sca-time-automation`; `satellite-onboarding-rulings.yaml:28-38` says both are
operator-ruled `profile: full`. Nothing records the relation between a ruled target and an observed state, and
the file holding the target is read by a checker wired into no gate (`:15-18`).

**G5 — Contradictory partial answers on ai-council's deployed version.** `registry.md:25` says v1.2.0;
`deployed-versions.yaml:31` says 1.3.1; `registry.md:33-36` declares the former derived from the latter. No
checker reads `registry.md` at all (only `scripts/fleet_analytics.py:602`, an exclusion), so the contradiction
cannot surface.

**G6 — Nothing today records a skill's dependencies.** The [#382] row names "skills" as an edge kind
(`BACKLOG.md:429`); two skills exist on disk (`.claude/skills/verify/SKILL.md`,
`.claude/skills/check-against-spec/SKILL.md`); and no file declares what either depends on, governs, or is
invalidated by. The only machine-readable `skills` tokens are a subtree-ownership list
(`ecosystem/parity-surfaces.yaml:808,810`) and a component-kind enum member
(`deploy/manifest-v1.4.0.yaml:254`).

**G7 — Nothing today records doc2doc dependency beyond one spec.** `_SPEC_REGISTRY` holds exactly one entry
(`scripts/validate_reconciliation.py:79-84`), so the doc2doc graph is 6 live edges into 1 node. The discovery
scan that would find missing edges is scoped to the same single spec by design
(`scripts/scan_undeclared_edges.py:48`). This is noted as a known shape at
`docs/audits/2026-07-04-coherence-spine-review.md:47`: "v1 shipped 2026-06-17 and the registry never grew".

**G8 — Nothing today records currency for doc2file edges.** `check_import_edges` verifies target *existence*
only (`scripts/audit.py:2365`, "every Claude-Code `@import` target reachable from the root CLAUDE.md exists").
The equivalent statement for doc2code is explicit: "Note what it checks: structural presence, not currency —
`staleness_signal` is explicitly deferred (`validate_doc_code_edge.py:23`)"
(`docs/audits/2026-07-04-coherence-spine-review.md:23`). So "rot as a graph query" (`BACKLOG.md:429`) has no
currency signal to query on either axis.

**G9 — Nothing today records a crosswalk between the nine identity spaces.** Spec-id, rule-ID, check-name,
surface-id, hook-id, region-id, task-id, component-id and Python symbol are each authoritative in their own
file; no file declares that (say) surface `precommit-hub-block`, hook id `block-ff-push`, rule
`governance-no-ff`, and component `hub-block-ff-push` refer to overlapping organs. The parity contract states
the independence deliberately — "id — canonical id (FR-2): stable, independent of local filename / hook id /
byte shape" (`ecosystem/parity-surfaces.yaml:18-20`) — which makes the absence a design position, not an
oversight, and therefore something the arc must rule on rather than discover.

**G10 — Nothing today records the hub's own deployed corpus position.** `deployed-versions.yaml:25-29` is
null-by-design for `.dev-knowledge`, while `parity-surfaces.yaml:5-7` declares the hub a fleet MEMBER. The hub
is simultaneously in the fleet map and absent from the state file.

**G11 — Nothing today records why a declared target has not been reached.** `deploy/manifest-v1.4.0.yaml:58`
declares v1.4.0; the highest recorded deployment is 1.3.1 (`deployed-versions.yaml:31`); the gap's reason
exists only as manifest prose (`deploy/manifest-v1.4.0.yaml:18-22`) and as a task row. There is no field
anywhere expressing "declared but not deployed, because X" — the closest is `gate_rev_ahead`, which expresses
the *opposite* direction (gate ahead of corpus, `parity-surfaces.yaml:416-435`).

**G12 — Nothing today records the ordering constraint between [#433] and [#382].** The pilot-precedes-contract
ruling sequences them and ADR-107 carries it as a named obligation
(`docs/decisions/ADR-107-backlog-restructure-engine-schema-viewer.md:10,259`), but neither task file carries a
`depends-on` clause at all (frontmatter census: 7 of 188 files carry the key; neither of these two is among
them). Filed as `BACKLOG.md:67` / `tasks/452-433-382-dependency-is-prose-only.md`.

**G13 — Contradictory partial answers on whether a dependency clause is enforced.** Four `depends-on` clauses
parse and four do not (`BACKLOG.md:53`), and the inert four are exactly the [E9] chain
(`#389→390`, `#382→381`, `#383→382`, `#385→383`). So the graph the [#382] row proposes to build in networkx
currently has its own governing edges written in a form its own parser rejects
(`scripts/validate_backlog.py:78`).

**G14 — Nothing today records the join between the two suppression vocabularies.**
`.methodology.yaml` `sanctioned_divergences[].component` and `ecosystem/disposition-register.yaml`
`dispositions[].{organ,match}` both implement one-per-concern suppression (`ecosystem/parity-surfaces.yaml:42-43`,
`ecosystem/disposition-register.yaml:19-22`) in different id spaces, and nothing states their interaction.

**G15 — Nothing today records freshness for the derived registry.** `ecosystem/index.yaml` is regenerate-on-demand
(`scripts/audit.py:3142`), carries no `last_reviewed` and is not in the freshness gate; it is currently stamped
`2026-07-11` (`:1`) and asserts `HANDOFF_PROCESS v5.7` (`:44-46`) against a live `6.0.1`
(`protocols/HANDOFF_PROCESS.md:4`). The generated-fragment sibling `ecosystem/doc-counts.md:5-7` documents the
same posture as deliberate for itself. So a derived registry can be arbitrarily stale and still read as data.

**GAP (not resolvable from this repo) — consumer-side pin values.** The actual `rev:` each consumer pins, and
each consumer's own `.methodology.yaml`, live in the consumer repos (`ai-council`, `corp-monorepo`); only the
hub's copies are on disk here. What is recorded hub-side is the expectation
(`ecosystem/parity-surfaces.yaml:404-409`) and one declared exception (`:416-435`).

---

## Closing boundary restatement

Analysis inputs only. No schema is declared, proposed, sketched, or implied above; where a field would have
been the natural way to express a finding, the finding is written as a gap instead. The pilot-precedes-contract
ruling (`docs/decisions/README.md`, 2026-07-26; carried on `tasks/433-*.md:13` and
`docs/decisions/ADR-107-backlog-restructure-engine-schema-viewer.md:259`) governs: the [#433] pilot's findings
precede any contract this dossier feeds.
