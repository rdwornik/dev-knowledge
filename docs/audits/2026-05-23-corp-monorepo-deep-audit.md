---
type: audit
scope: corp-monorepo (deep conformance, read-only, file-state-verified)
date: 2026-05-23
author: claude-opus-4-7 + rob
status: immutable
supersedes: none
related: docs/audits/2026-05-19-corp-monorepo-architecture-inspection.md
---

# corp-monorepo — Deep Conformance Audit vs current `.dev-knowledge` standards

**Date:** 2026-05-23
**Target repo:** `corp-monorepo`
**Target HEAD:** `32a47f85b07d697be20066c1ec69df3cf92cb1f6` ("Merge branch 'docs/audit-corp-monorepo-conformance-gap'", 2026-05-20)
**Auditor:** Claude Code (read-only; ADR-36 contract — zero `corp-monorepo/` files modified)
**Output home:** `.dev-knowledge/docs/audits/` (this file)
**Routing:** scrum-master review pattern — findings route to a dedicated `corp-monorepo` session for remediation decisions; this audit identifies, it does not remediate.

**Basis (the standard):** `.dev-knowledge` ADRs and artifacts as they stand on 2026-05-23, specifically:
ADR-51 (architecture doc convention) **+ amendment 2026-05-22** (codemap generator output spec / embedded-Mermaid form);
ADR-34 (file naming); ADR-38 (universal baseline + A3/A4 root-placement); ADR-39 (file lifecycle);
ADR-41 + ADR-47 (BACKLOG mandate + demoted convention); ADR-46 (dated-entries, demoted); ADR-31 (authority model);
ADR-30 (default branch); ADR-33 (VISION); ADR-53 (CLAUDE.md canonical); `templates/ARCHITECTURE-template.md`;
`.dev-knowledge/ARCHITECTURE.md` (post layer-model-Mermaid exemplar); PLAYBOOK §17 Code Quality + §18 Ecosystem Audit + §Codemap workflow.

---

## 1. Why this audit exists (delta since the last passes)

corp-monorepo was last reviewed cross-repo on **2026-05-19** (`docs/audits/2026-05-19-corp-monorepo-architecture-inspection.md`, an ADR-51 template-input inspection) and self-audited twice on **2026-05-20** (`corp-monorepo/docs/audits/2026-05-20-corp-monorepo-deep.md` internal drift + `2026-05-20-conformance-gap-vs-dev-knowledge.md` conformance-vs-standard).

Since those passes, the `.dev-knowledge` standard moved materially on **2026-05-22**:

- **ADR-51 amendment** specified the codemap's canonical form — an auto-generated **embedded Mermaid** block between `<!-- CODEMAP:START -->` / `<!-- CODEMAP:END -->` markers — and **closed** BACKLOG Stream C P2 ("Codemap generator output specification").
- The shared generator now ships at `.dev-knowledge/scripts/codemap/cli.py`; the per-repo opt-in checklist is documented in PLAYBOOK §Codemap workflow.
- `templates/ARCHITECTURE-template.md` reached its current embedded-Mermaid form with mandatory frontmatter and `[CORE]`/`[M/L]`/`[L-opt]`/`[L]` section scale-tags.
- `.dev-knowledge/ARCHITECTURE.md` adopted an inline-Mermaid layer model as the exemplar.

**Consequence for corp-monorepo:** the 2026-05-20 conformance audit assessed ADR-51 as **PARTIAL — "best-possible state under the upstream gap"** (the generator was unbuilt). That gap is now closed. This audit re-assesses corp-monorepo's architecture-doc conformance against the **post-amendment** standard, and confirms which prior drift findings **remain** at HEAD `32a47f8`.

---

## 2. Methodology

- **Read-only.** Glob/Grep/Read of the corp-monorepo working tree at HEAD `32a47f8`. No execution, no writes. The `data/_outputs/**` tree (pipeline output) is out of scope.
- **Standard refresh.** Read the ADRs, template, exemplar, and PLAYBOOK sections listed in the Basis above.
- **Citations.** Every finding cites a corp-monorepo `file:line` (or a verified file-state fact) on the evidence side and a specific ADR/template clause on the standard side.
- **In scope:** the six audit categories below + a dedicated visual subsection. **Out of scope:** internal code-correctness findings (e.g. `manifest.load_status()` retry regression, MinHash wiring) — those belong to the corp-monorepo internal deep audit (`2026-05-20-corp-monorepo-deep.md`) and are not `.dev-knowledge`-standards conformance items. `.dev-knowledge` self-audit and `ai-council` are out of scope.
- **Per-finding format:** Severity / Category / Evidence / Standard / Gap / Recommendation / Difficulty. Severity: **CRITICAL** (load-bearing convention violated; blocks work) · **HIGH** (significant drift, visible to all consumers) · **MEDIUM** (real, deferrable) · **LOW** (polish).

---

## 3. Findings by category

### Category A — Architecture & visual conformance (ADR-51 + amendment 2026-05-22)

#### [HIGH] [A] ARCHITECTURE.md does not adopt the canonical template form

**Evidence:** `corp-monorepo/ARCHITECTURE.md:1-4` opens with `# Architecture Reference -- Corporate OS` and a prose living-doc tagline — **no YAML frontmatter block**. No `##` header carries a `[CORE]`/`[M/L]`/`[L-opt]`/`[L]` scale-tag. The CORE section names diverge from the canonical: `## System Overview` (line 6), `## Source Layout` (18) + `## Module Map` (39), `## Dependency Layers` (164).
**Standard:** ADR-51 Decision 3 (single canonical template defines a mandatory core every covered repo completes); `templates/ARCHITECTURE-template.md:1-6` (mandatory frontmatter `scale`/`last_reviewed`/`status`/`owner`), `:23` ("every `##` header carries a visible bracketed tag"), and the CORE section names `Purpose [CORE]`, `Codemap [CORE]`, `Layer Boundaries & Invariants [CORE]`.
**Gap:** the document predates ADR-51 (last updated 2026-03-30; ADR-51 accepted 2026-05-18). It satisfies the ADR-51 Decision 4 *content* minimum (purpose, codemap, layers, invariants — all present and high quality) but not the template *form*.
**Recommendation:** re-home the existing content into the canonical template skeleton: add frontmatter, add section scale-tags, rename the three CORE sections to match. Content depth is already L-grade; this is a structural re-flow, not a rewrite.
**Difficulty:** medium.

#### [HIGH] [A] Codemap is not in the canonical embedded-Mermaid form; CODEMAP markers absent

**Evidence:** the codemap exists as a hand-written directory tree (`ARCHITECTURE.md:18-37`, "Source Layout") plus per-package module tables (`:39-162`, "Module Map"). The graphical view is a **separate** SVG referenced by pointer — `→ Module map diagram: docs/diagrams/container-module.svg` (`:205`). There are **no** `<!-- CODEMAP:START -->` / `<!-- CODEMAP:END -->` markers anywhere in the file (grep: 0 hits).
**Standard:** ADR-51 amendment 2026-05-22 "Canonical target form" — the codemap section is an embedded Mermaid block between CODEMAP markers; `templates/ARCHITECTURE-template.md:46-71` shows the bounded form.
**Gap:** corp's codemap is a hand-maintained *transitional* form. The amendment **permits** a hand-maintained transitional codemap until generator opt-in (§Per-repo adoption — opt-in, not mandatory), so this is not a content violation. But with **no CODEMAP markers**, a later generator drop-in requires manual section surgery rather than a mechanical `generate --write`.
**Recommendation:** in the template re-home (A-finding above), create `## Codemap [CORE]` containing the CODEMAP markers; embed the module graph as inline Mermaid between them. This makes generator adoption (A-finding below) a one-command swap.
**Difficulty:** medium.

#### [MEDIUM] [A] ADR-51 conformance gate cited by the prior audit is now closed — status refresh

**Evidence:** corp-monorepo's own `docs/audits/2026-05-20-conformance-gap-vs-dev-knowledge.md:36,139-140` classifies ADR-51 as **PARTIAL**, "best-possible state under the upstream gap," because the codemap generator + output spec were unbuilt. As of 2026-05-22 the spec is **closed** (ADR-51 amendment §Backlog status), the tool ships at `.dev-knowledge/scripts/codemap/cli.py`, and the opt-in checklist lives in PLAYBOOK §Codemap workflow (default `--source-root src/` applies to corp).
**Standard:** ADR-51 amendment 2026-05-22 §Per-repo adoption; PLAYBOOK §Codemap workflow (per-repo opt-in checklist).
**Gap:** not a defect — the "blocked on upstream" justification no longer holds. corp can now opt in at will; the choice is a corp-operator decision.
**Recommendation:** dedicated session walks the PLAYBOOK §Codemap workflow opt-in checklist (instantiate CODEMAP markers → add `codemap-freshness` pre-commit hook with `--source-root src` → `generate . --write` → commit). Pairs naturally with the two A-findings above.
**Difficulty:** low (decision) / medium (execution, gated on the CODEMAP-markers prerequisite).

#### [HIGH] [A] ARCHITECTURE.md is 7+ weeks stale (remains from 2026-05-20 deep audit D4)

**Evidence:** `ARCHITECTURE.md:3-4` "Last updated: 2026-03-30 (dependency layers clarified)". The doc predates and does not reflect: ADR-30/ADR-31 (CHANGELOG/HANDOFF retirement, 2026-05-18), VISION.md + BACKLOG.md additions, the ARCHITECTURE.md root move (ADR-38 A4), the AGENTS.md retirement (ADR-54, 2026-05-20), and the CLAUDE.md v2.1 rewrite (ADR-53). The §OneDrive safety guards block (`:401-428`) still reads "implementation lands in three follow-up PRs"; there is no References section pointing to VISION/BACKLOG. Prior documentation: `corp-monorepo/docs/audits/2026-05-20-corp-monorepo-deep.md` Finding D4 (HIGH). **Remains unremediated** at HEAD `32a47f8` (both 2026-05-20 audits were read-only).
**Standard:** `templates/ARCHITECTURE-template.md:11-12` ("Living document. Updated after structural changes."); ADR-51 Decision 5 (hand-written narrative kept current).
**Gap:** ARCHITECTURE.md is mandated session-start reading (corp CLAUDE.md §1, §3); a 7-week-stale canonical doc misleads every fresh agent context.
**Recommendation:** refresh to current state in the same pass as the template re-home (A-finding above) — single PR.
**Difficulty:** medium. *(Related-to: Category F documentation quality.)*

#### [LOW] [A] Layer model rendered as ASCII rather than inline Mermaid

**Evidence:** `ARCHITECTURE.md:170-172` renders the 4-layer model as a fenced ASCII line `interface > orchestration > core > foundation`. The current `.dev-knowledge/ARCHITECTURE.md:47-64` exemplar renders its layer model as an inline Mermaid `flowchart`.
**Standard:** `templates/ARCHITECTURE-template.md` §Layer Boundaries & Invariants (the template does **not** mandate Mermaid for the layer model — only for the codemap), plus the post-2026-05-22 exemplar convention.
**Gap:** not a hard violation — ASCII is permitted for the layer model. It is a visual-convergence opportunity vs the exemplar.
**Recommendation:** optional — convert to inline Mermaid in §Layer Boundaries when re-homing. See Visual subsection.
**Difficulty:** low.

---

### Category B — Naming compliance (ADR-34)

#### [LOW] [B] Legacy `docs/archive/` files use UPPERCASE-TYPE + underscore naming

**Evidence:** `docs/archive/` holds 32 files of the form `YYYY-MM-DD_TYPE_descriptor.md` — underscore separators and UPPERCASE TYPE tokens, e.g. `2026-03-20_REPORT_architecture.md`, `2026-03-24_HANDOFF_cke_backlog.md`, `2026-03-28_PACKAGE_ARCHITECTURE_AUDIT.md`.
**Standard:** ADR-34 separator rule (universal hyphen for filenames/foldernames) + dated-artifact form `YYYY-MM-DD-topic-with-dashes.md`.
**Gap:** pre-convention archive snapshots. Already tracked upstream as Cross-stream P3 "A5 — retire opportunistically" (per `2026-05-20-conformance-gap-vs-dev-knowledge.md:290`).
**Recommendation:** opportunistic rename only when next touching `docs/archive/*`. No dedicated migration warranted — conforms to the opportunistic posture.
**Difficulty:** low.

**No further findings.** ADR filenames use the hyphen `ADR-NN-topic.md` form (`ADR-01-knowledge-architecture.md` … `ADR-31-retire-single-file-handoff.md`) ✓. Audits use `YYYY-MM-DD-topic.md` ✓. Council transcripts use `DECISION_NN_snake_case.md`, which ADR-34's conventions table explicitly **grandfathers** ("Legacy decision transcripts … grandfathered") ✓. Python modules snake_case per language ✓. corp-monorepo conforms to ADR-34 as audited apart from B (above).

---

### Category C — Sacred files & lifecycle (ADR-38, ADR-33, ADR-53, ADR-39)

**No binding findings — corp-monorepo conforms to the ADR-38 baseline for Scale L as audited.**

- **ADR-38 baseline (L tier):** all mandatory files present at root — `README.md`, `VISION.md` (Standard tier, frontmatter `version/tier:standard/scale:L/owner/status/last_reviewed` complete, all 6 sections), `BACKLOG.md`, `ARCHITECTURE.md` (root, A3/A4 satisfied), `CLAUDE.md`, plus `src/corp/`, `tests/`, `pyproject.toml`, `docs/decisions/`. `CHANGELOG.md` correctly **absent** (corp ADR-30 + `.dev-knowledge` ADR-49). `LESSONS.md` **absent** by design (cross-repo lessons route to `.dev-knowledge/LESSONS.md` per ADR-35; corp CLAUDE.md §4).
- **ADR-53 (CLAUDE.md canonical):** `CLAUDE.md` is 148 lines (≤200), v2.1 12-section template, no per-repo `AGENTS.md` (correct per ADR-53 + ADR-54). ✓
- **ADR-39 (6-element lifecycle):** corp has no explicit per-file 6-element lifecycle registry. **Not a finding** — ADR-39 is "**Mandate:** `.dev-knowledge`; **Recommendation:** child repos." corp is within the recommendation tier.

---

### Category D — BACKLOG conformance (ADR-41 + ADR-47)

#### [LOW] [D] BACKLOG header cites the superseded strict ADR-41 schema, not the governing ADR-47 convention

**Evidence:** `BACKLOG.md:2-4` reads "Schema per ADR-41 (`.dev-knowledge/docs/decisions/ADR-41-…`): `[P{N}]` priority, `[open|superseded]` status, dated entries."
**Standard:** ADR-47 (2026-05-16 demotion) is now the governing convention; it relaxed ADR-41's strict schema to "one file, recommended (not enforced) entry shape."
**Gap:** the citation points at the pre-demotion authority. Cosmetic; the entries themselves conform.
**Recommendation:** update the header reference to ADR-47 (or "ADR-41 schema as relaxed by ADR-47").
**Difficulty:** low.

**Otherwise conforms.** Single `BACKLOG.md`; entry shape `### [P{N}] [open] <title>` + `**What:** / **Why:** / **Added:** / **Status:**` (verified across all 9 entries); no `BACKLOG_ARCHIVE.md`. Grouped by "Open Decisions" / "Pending Fixes" rather than `## Stream` headings — acceptable at single-repo scale per ADR-47 ("for small repos a flat list is fine").

---

### Category E — Cross-repo + governance (ADR-31, ADR-46, ADR-30)

#### [LOW] [E] ADR-numbering namespace collision; CLAUDE.md §11 mixes namespaces unprefixed

**Evidence:** corp's local `docs/decisions/` reuses numbers that collide with `.dev-knowledge` ADRs for unrelated decisions (corp ADR-27 = Safety Invariants vs `.dev-knowledge` ADR-27 = Scope Tagging; corp ADR-30 = Retire CHANGELOG vs `.dev-knowledge` ADR-30 = Default Branch; corp ADR-31 = Retire HANDOFF vs `.dev-knowledge` ADR-31 = Authority Model). `corp-monorepo/CLAUDE.md:130-137` (§11) lists "ADR-14, -23, -27, -36, -42, -49, -51, -53" mixing both namespaces without a source prefix.
**Standard:** ADR-31 (clarity of binding references); discoverability for agents/contributors.
**Gap:** silent ambiguity — a reader cannot tell which ADR-27 is meant. Already noted as GAP #2 in `2026-05-20-conformance-gap-vs-dev-knowledge.md:31-32`; **remains**.
**Recommendation:** prefix cross-namespace references in CLAUDE.md §11 ("corp ADR-27" vs "`.dev-knowledge` ADR-42").
**Difficulty:** low.

**Otherwise conforms.** **ADR-30:** default branch is `main`; CLAUDE.md §4 specifies "never commit to `main` directly." ✓ **ADR-46 (demoted):** JOURNAL uses ISO `### YYYY-MM-DD —` headers, newest-first, and the `normalize-headers` hook is wired (`.pre-commit-config.yaml:20-25`). ✓ **ADR-31 (authority):** VISION §Relationships and CLAUDE.md §1 explicitly accept `.dev-knowledge` as the binding methodology source. ✓

---

### Category F — Documentation quality (aspirational-vs-actual pattern)

> This category targets the lesson-candidate pattern: governance docs phrased as a stable end-state that the file-state does not realize, stale counts/cross-refs, and misleading dead config. The items below are re-confirmed against HEAD `32a47f8`; where the 2026-05-20 internal deep audit already documented them, that is noted — all **remain unremediated** (that audit was read-only).

#### [HIGH] [F] VISION §Values "One routing authority … single source of truth" is aspirational; routing is code-distributed

**Evidence:** `VISION.md:75-76` declares "**One routing authority.** Routing configuration has a single source of truth, not per-module copies." File-state: no central routing config exists (`routing_map.yaml` absent); routing logic is distributed across `src/corp/extraction/routing.py`, `src/corp/ingest/router.py`, `src/corp/overnight/classifier.py`, `src/corp/retrieve/engine.py`, and `src/corp/intent_router.py` + `src/corp/llm_router.py`. Prior documentation: `2026-05-20-corp-monorepo-deep.md` Finding D2 (HIGH); **remains**.
**Standard:** aspirational-vs-actual anti-pattern (governance docs must describe the actual state, not a stable-end-state aspiration). VISION's own §Lifecycle names contradiction-with-file-state as a review trigger.
**Gap:** VISION asserts an invariant the codebase does not realize — a self-declared drift signal.
**Recommendation:** resolve the contradiction either way: (a) consolidate routing into one canonical config/module + an ADR, or (b) amend VISION §Values to describe routing as intentionally per-aspect/code-distributed. Per VISION's §Edit process, a material Values change goes through an ai-council debate.
**Difficulty:** medium.

#### [MEDIUM] [F] CONTRIBUTING.md carries two stale facts in adjacent blocks

**Evidence:** `CONTRIBUTING.md:119` reads "`docs/decisions/` — all ADRs (26 decisions)"; actual count is **30** (`docs/decisions/ADR-*.md` glob; ADR-01..27 + ADR-30 + ADR-31, gaps at 28/29). `CONTRIBUTING.md:105-114` documents "Known baseline violations (Phase 1) … These will be resolved in Phase 2" — but Phase 2 completed 2026-04-15 (project_resolver→core, query_engine→orchestration; current baseline 0 violations). Prior documentation: `2026-05-20-corp-monorepo-deep.md` Finding D10; **remains**.
**Standard:** documentation accuracy (CONTRIBUTING is a first-stop doc for human + agent contributors).
**Gap:** two stale facts in adjacent paragraphs of a newcomer-facing doc.
**Recommendation:** update count to 30; replace the Phase-1 block with one line — "Phase 1 baseline violations resolved in Phase 2 (JOURNAL 2026-04-15); current baseline: 0."
**Difficulty:** low.

#### [MEDIUM] [F] README.md carries stale test counts and a wrong install-extras group

**Evidence:** `README.md:18` shows "Total **2,412**" (per-module column sums to 2,153); the latest recorded run is 2,548 (JOURNAL 2026-05-18). `README.md:28` instructs `pip install -e ".[dev,llm]"` — `llm` is **not** a declared optional-dependency group (pyproject groups are `slides`/`dedup`/`graph`/`dev`; `CONTRIBUTING.md:33` correctly uses `.[dev,dedup,graph]`). Prior documentation: `2026-05-20-corp-monorepo-deep.md` Findings D5/D14; **remains**.
**Standard:** documentation accuracy; the public-facing entry point should not state numbers/commands that fail.
**Gap:** wrong totals erode trust; the `llm` extras group install command does not resolve.
**Recommendation:** drop the count column (or pin "counted YYYY-MM-DD"); correct the extras group to a real one.
**Difficulty:** low.

#### [LOW] [F] ruff config duplication — root `ruff.toml` (lenient) silently overrides `pyproject.toml [tool.ruff]` (strict)

**Evidence:** `ruff.toml:1-6` declares `select = ["E","F","I"]` / `ignore = ["E501"]`; `pyproject.toml [tool.ruff]` declares the stricter `select = ["E","F","I","W","B","UP"]` / `ignore = ["E402"]`. Ruff discovery prefers a root `ruff.toml` over `pyproject.toml [tool.ruff]`, so the lenient set is active and the pyproject block is misleading dead text. Prior documentation: `2026-05-20-corp-monorepo-deep.md` Finding D1; **remains**.
**Standard:** documentation/config accuracy (single source of truth; a doc-shaped config that claims rules it doesn't enforce misleads contributors).
**Gap:** a contributor reading `pyproject.toml` assumes `W/B/UP` are enforced; they are not.
**Recommendation:** consolidate to one ruff config source (delete `ruff.toml` or delete the `[tool.ruff]` block).
**Difficulty:** low.

---

## 4. Visual aspect — diagrams & embedded-Mermaid upgrade plan

> Rob's explicit emphasis. corp-monorepo carries a mature C4/Mermaid diagram set predating the embedded-Mermaid convention. This subsection classifies each artifact and gives the concrete inline-embedding plan for the dedicated session.

**Existing artifacts (`docs/diagrams/`):** three Mermaid+SVG pairs plus a theme file.

| Artifact | Type | Current wiring | Disposition under post-2026-05-22 convention |
|---|---|---|---|
| `container-module.mermaid` / `.svg` | C4 container / module map | Separate SVG; pointer at `ARCHITECTURE.md:205` | **EMBED inline** as the `## Codemap [CORE]` graphical artifact (between CODEMAP markers). Template §Codemap note: the module-map/codemap diagram lives in §Codemap, **not** in §Diagrams. |
| `system-context.mermaid` / `.svg` | C4 L1 system context | Separate SVG; pointer at `ARCHITECTURE.md:16` | **STAYS SEPARATE.** Template §Diagrams lists "System context (C4 L1)" as a complementary diagram referenced at the end of §Purpose. |
| `magistrala-pipeline.mermaid` / `.svg` | Data-flow pipeline | Separate SVG; pointer at `ARCHITECTURE.md:342` | **STAYS SEPARATE.** Template §Diagrams lists "Pipeline / data flow" as a complementary diagram referenced at the end of §Data Flow. |
| `conventions.yaml` | SVG render theme (fonts/colors/limits) | Hand-read render convention; "Last updated: 2026-03-30" | Keep as the render-theme reference for the two diagrams that stay SVG. Minor drift note below. |

**Plus — net-new inline diagram:** the layer model is currently ASCII (`ARCHITECTURE.md:170-172`). Recommend a **new inline Mermaid** layer flowchart in `## Layer Boundaries & Invariants [CORE]`, mirroring the `.dev-knowledge/ARCHITECTURE.md:47-64` exemplar (nodes per layer, `classDef` colors, enforcement tool + `tach.toml` cited).

**Visual upgrade plan, in order:**
1. Create `## Codemap [CORE]` with CODEMAP markers; embed the container-module graph as inline Mermaid between them (or let the generator produce it — see step 3).
2. Add the inline Mermaid layer model to `## Layer Boundaries & Invariants [CORE]`; retire the ASCII line.
3. **If** opting into the generator (PLAYBOOK §Codemap workflow): `generate . --source-root src --write` will author the §Codemap block from the import graph — this would **supersede** the hand-drawn `container-module` artifact (retire it, or keep only as a curated higher-level view). `system-context` and `magistrala-pipeline` remain hand-authored SVGs.
4. Refresh `conventions.yaml` if any palette/label is reused inline.

**Diagram tally:** 3 existing diagrams → **1** recommended for inline-embedding (container-module → §Codemap), **2** remain separate complementary SVGs (system-context, magistrala-pipeline), **+1** net-new inline Mermaid (layer model).

**Minor drift note (not a numbered finding):** `conventions.yaml` labels `layer_3` as "Composition" while `tach.toml` / ARCHITECTURE.md name the top layer "interface". Cosmetic label mismatch in the theme file; reconcile when the diagrams are touched. *(OPEN QUESTION — see §7.)*

---

## 5. Summary

**Findings by severity:** **0 CRITICAL · 4 HIGH · 3 MEDIUM · 5 LOW** (12 total). Plus several CONFORMS/INFO results stated inline (Categories C and most of B/D/E).

| Category | HIGH | MEDIUM | LOW | Notes |
|---|---|---|---|---|
| A — Architecture & visual | 3 (A1 template-form, A2 codemap-form, A4-staleness) | 1 (A3 gate-now-closed) | 1 (ASCII layer model) | dominant gap surface |
| B — Naming | — | — | 1 (archive legacy names) | otherwise conforms |
| C — Sacred files & lifecycle | — | — | — | conforms (ADR-39 recommendation-only) |
| D — BACKLOG | — | — | 1 (header cites ADR-41 not ADR-47) | otherwise conforms |
| E — Cross-repo governance | — | — | 1 (ADR-namespace prefixing) | otherwise conforms |
| F — Documentation quality | 1 (VISION routing claim) | 2 (CONTRIBUTING, README) | 1 (ruff config) | all remain from 2026-05-20 |
| Visual subsection | (folds into A) | | | 1 embed + 2 separate + 1 new |

**Top 3 highest-impact items:**
1. **ARCHITECTURE.md template + codemap form (HIGH ×2, Category A).** The architecture doc is the re-entry anchor and the single largest remediation; adopting the template (frontmatter, section tags, CORE renames, CODEMAP markers, embedded codemap) unblocks generator opt-in and the visual upgrade.
2. **ARCHITECTURE.md staleness (HIGH, A4-staleness).** 7+ weeks behind reality on a mandated session-start doc; remediate in the same PR as #1.
3. **VISION §Values aspirational routing claim (HIGH, Category F).** A governance doc asserting an unrealized invariant — corp's own VISION §Lifecycle flags this as a drift signal requiring review.

**Overall posture:** corp-monorepo is **strongly conformant** on the structural baseline — sacred files (C), naming (B), BACKLOG (D), branch/authority/dated-entries (E), and CLAUDE.md (ADR-53) all pass. The conformance debt is **concentrated in one artifact**: `ARCHITECTURE.md` predates ADR-51 and the 2026-05-22 amendment, and the documentation-quality drift (Category F) clusters in the secondary docs. **Rough conformance estimate: ~80%** against current `.dev-knowledge` standards — the missing ~20% is almost entirely Category A form-conformance plus the four remaining doc-quality items, none of them load-bearing.

---

## 6. Recommended remediation sequence (for the dedicated corp-monorepo session)

| Step | Work | Findings closed | Depends on |
|---|---|---|---|
| 1 | **ARCHITECTURE.md template re-home + refresh.** Add frontmatter; add `[CORE]`/`[M/L]`/`[L-opt]`/`[L]` section tags; rename CORE sections (Purpose / Codemap / Layer Boundaries & Invariants); create CODEMAP markers; embed the codemap + an inline layer-model Mermaid; refresh stale state (ADR-30/31, VISION/BACKLOG refs, AGENTS.md retirement, OneDrive guard status). One PR. | A1-form, A2-codemap, A4-staleness, A5-ASCII, Visual steps 1-2 | — |
| 2 | **Codemap generator opt-in** (optional) per PLAYBOOK §Codemap workflow: add `codemap-freshness` hook (`--source-root src`), `generate --write`, retire/curate `container-module.svg`. | A3-gate, Visual step 3 | Step 1 (markers must exist) |
| 3 | **VISION routing claim resolution** via ai-council: consolidate routing **or** amend §Values to describe per-aspect routing. | F-VISION | independent (needs Council) |
| 4 | **Low-effort doc batch** (one PR): CONTRIBUTING count→30 + Phase-1 block; README counts + extras group; ruff config single-source; BACKLOG header ADR-41→ADR-47; CLAUDE.md §11 namespace prefixes; opportunistic `docs/archive/*` renames. | F-CONTRIBUTING, F-README, F-ruff, D-header, E-namespace, B-archive | independent |

Steps 1 and 4 are prerequisite-free and can run in parallel; step 2 depends on step 1; step 3 is independent and gated on a Council debate.

---

## 7. Open questions (corp-monorepo state unclear from file inspection)

- **ADR-40 algorithmic tier.** corp declares `scale: L` (VISION frontmatter, CLAUDE §2). Algorithmic confirmation needs the `.dev-knowledge` audit tool's tier computation; the 2026-04-30 calibration estimated corp ~21 → L (consistent), but F-08 ("all repos clamp to L") is an upstream calibration concern. **UNKNOWN by file inspection** — same status as the 2026-05-20 conformance audit.
- **Codemap generator opt-in is a corp-operator decision.** This audit cannot determine whether corp *should* adopt the generator vs keep a curated hand-maintained codemap; both satisfy ADR-51 (the latter as transitional). Surfaced for the dedicated session.
- **`conventions.yaml` layer label "Composition" vs tach "interface".** Whether this is an intentional presentation alias or stale drift is unclear from the file alone.

---

## 8. Cross-references

- **`.dev-knowledge` standards:** ADR-51 (+ amendment 2026-05-22) · ADR-34 · ADR-38 (A3/A4) · ADR-39 · ADR-41 · ADR-47 · ADR-46 · ADR-31 · ADR-30 · ADR-33 · ADR-53 · `templates/ARCHITECTURE-template.md` · `.dev-knowledge/ARCHITECTURE.md` (exemplar) · PLAYBOOK §17 / §18 / §Codemap workflow.
- **Prior baselines compared:** `docs/audits/2026-05-19-corp-monorepo-architecture-inspection.md` (template-input inspection) · `corp-monorepo/docs/audits/2026-05-20-corp-monorepo-deep.md` (internal drift) · `corp-monorepo/docs/audits/2026-05-20-conformance-gap-vs-dev-knowledge.md` (conformance-vs-standard, pre-amendment).
- **Routing:** scrum-master review pattern (BACKLOG Cross-stream "Apply scrum-master review pattern to other child repos" / "Codify scrum-master review authority"). Builds N=2 empirical grounding alongside the ai-council 2026-05-12 N=1 pass.

---

**Contract preserved:** zero `corp-monorepo/` files modified. Read-only per ADR-36.
