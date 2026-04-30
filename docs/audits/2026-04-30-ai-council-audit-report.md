# ai-council — Audit Findings Report (Faza A2)

**Date:** 2026-04-30
**Target repo:** ai-council
**Pre-migration HEAD:** 47bea6f67f81eac4f2d0ebddc907546fc8514463
**Post-migration HEAD:** c821157fcfa957bc6612c74667d70c8c9a88ef5c
**Auditor:** .dev-knowledge browser session (manual, audit tool P1 pending implementation)
**Phase:** A2 Findings (interpret A1 discovery + rediscovery outputs)
**Source observations:**
- `2026-04-30-ai-council-discovery.md`
- `2026-04-30-ai-council-rediscovery.md`

---

## Executive summary

ai-council achieved ADR-38 architectural compliance via 5-commit migration (validated 5/5 checks pass). Tier classification per ADR-40 produces L (score 0.0). However, calibration analysis surfaces concern: all ecosystem repos clamp to L regardless of size, suggesting algorithm miscalibration. L-specific mandates flagged "deferred pending calibration." Tier-independent findings — VISION.md absent, lessons discovery not configured, ADR naming convention divergence — actionable regardless.

## Calibration flag (CRITICAL CONTEXT)

ADR-40 with current coefficients (b=12, c=8, d=15) produces:
- corp-ops (small, ~5k tokens): score 29.8 → L
- .dev-knowledge (small, ~10k tokens): score 30.7 → L
- ai-council (medium, 102k tokens): score 0.0 (clamped) → L
- corp-monorepo (large, ~150k+ tokens): score < 0 (clamped) → L

Every repo classifies L. Algorithm not differentiating. Per Rob's decision (Path 3 strategy), recalibration deferred to audit tool P1 multi-repo data collection. Findings tagged with tier dependency.

---

## Findings

### P1 — Critical (governance-blocking, tier-independent)

#### F-01 — VISION.md absent

- **ADR reference:** ADR-33 (VISION universalization), ADR-38 (mandatory files table)
- **Mandate:** VISION.md required at M+ tier (Lite for M, Standard for L). ai-council classifies L per current algorithm; M per intuitive judgment if recalibrated. EITHER WAY VISION.md is mandatory.
- **Current state:** No VISION.md at ai-council root. Verified in both pre-migration (HEAD 47bea6f) and post-migration (HEAD c821157) discovery runs.
- **Required action:** Create `ai-council/VISION.md` per ADR-33 schema. Frontmatter: `version: 1.0`, `tier: M` (or L per current algorithm — flag for Rob review), `owner: rob`, `last_reviewed: 2026-04-30`, `scale: M` (or L). Sections: Mission, Scope, Methodology, Lifecycle, Relationships.
- **Tier dependency:** None. Required regardless of M or L.

#### F-02 — Lessons discovery not configured

- **ADR reference:** ADR-35 (lessons base activation)
- **Mandate:** Repos in ecosystem should configure DEV_KNOWLEDGE_PATH env var + CLAUDE.md note enabling cross-repo lessons retrieval.
- **Current state (from discovery):**
  - No LESSONS.md at ai-council root
  - CLAUDE.md does NOT mention `DEV_KNOWLEDGE_PATH`
  - No `.env.example` at ai-council root
  - No AGENTS.md at ai-council root
  - `tasks/lessons.md` exists but is project-local only (first entry: "Session: Phase 1 Foundation (2026-02-21)"); not linked to .dev-knowledge LESSONS.md
- **Required action:** Update CLAUDE.md to reference `DEV_KNOWLEDGE_PATH` env var per ADR-35; document in session setup or equivalent; consider whether `tasks/lessons.md` should be merged into .dev-knowledge LESSONS.md or remain ai-council-local.
- **Tier dependency:** None.
- **Implementation dependency:** ADR-35 P1 implementation in .dev-knowledge pending (BACKLOG P2 item). May proceed with configuration documentation; full retrieval functionality awaits P1 implementation.

---

### P2 — Important (gap, may be tier-dependent)

#### F-03 — BACKLOG.md absent

- **ADR reference:** ADR-41 (cross-session backlog architecture)
- **Mandate:** BACKLOG.md mandatory at M+ tier per ADR-41.
- **Current state:** No BACKLOG.md at ai-council root. Not observed in pre- or post-migration discovery.
- **Required action:**
  - **If tier confirmed M+ post-recalibration:** create `ai-council/BACKLOG.md` per ADR-41 schema with Stream sections, P1/P2/P3 priorities, grooming cadence
  - **Alternative:** ai-council items contribute to .dev-knowledge central BACKLOG.md as "Stream B: ai-council" section (currently empty placeholder)
- **Tier dependency:** Mandatory if M+. S tier optional.

#### F-04 — ARCHITECTURE.md absent

- **ADR reference:** ADR-38 (mandatory files table — ARCHITECTURE.md mandatory at L, optional at M)
- **Current state:** No ARCHITECTURE.md at ai-council root. Not observed in pre- or post-migration discovery.
- **Required action:**
  - **If tier confirmed L post-recalibration:** create per ADR-38
  - **If recalibrated to M:** optional, recommended for clarity but not mandated
- **Tier dependency:** YES — depends on calibration outcome.
- **Recommendation:** DEFER until calibration confirmed.

---

### P3 — Minor (defer, grandfather, or amendment candidate)

#### F-05 — ADR file naming convention divergence

- **ADR reference:** ADR-34 (file naming convention)
- **Mandate:** ADRs use `ADR-NN_topic_with_underscores.md` format (underscore-separated topic portion).
- **Current state (from discovery):** All 7 ai-council ADRs use `ADR-NN-kebab-case.md` (hyphens throughout): ADR-01-synthesizer-selection.md, ADR-02-default-panel.md, ADR-03-blind-voting.md, ADR-04-mode-system.md, ADR-05-research-integration.md, ADR-06-cost-optimization.md, ADR-07-dual-output-paths.md.
- **Required action:** Per ADR-29 grandfathering pattern, existing files in non-standard locations/naming may remain. RECOMMEND: future ADRs follow ADR-34 convention (underscore-separated topic); existing 7 ADRs grandfathered — no rename required.
- **Tier dependency:** None.

#### F-06 — Test count discrepancy (potential ADR-38 amendment candidate)

- **ADR reference:** ADR-38 (test definition)
- **Observation:** grep (`^def test_|^    def test_`) yields 219 test functions. CLAUDE.md states "266 unit tests." Discrepancy of 47. Primary candidate: class-based tests inside `Test*` classes with non-4-space indentation not captured by grep pattern. Evidence: `test_providers.py` (19,914 chars, 0 grep hits) and `test_integration.py`, `test_healthcheck.py` (also 0 grep hits) suggest class-based test structure. Post-migration discovery confirms same 219 count (migration was import path changes only).
- **Required action:** None for ai-council. ADR-38 test definition already includes "Function in class `Test*`" and specifies `pytest --collect-only -q` as canonical counting method — grep was an approximation used in manual audit. Recommend using `pytest --collect-only -q | wc -l` for accurate count in future audit tool P1 implementation. Surface discrepancy as calibration note for ADR-38 Section "Test definition."
- **Tier dependency:** None (affects tier algorithm inputs if grep used as proxy).

#### F-07 — Module count underrepresents structural complexity (potential ADR-38 amendment)

- **ADR reference:** ADR-38 (module definition)
- **Observation:** Per strict ADR-38 definition (top-level subdirectories inside `src/ai_council/` with `__init__.py` + 1+ Python files), ai-council has 2 modules: `providers/` and `research/`. However, 12 direct Python files exist at `src/ai_council/` level (cli.py, debate.py, healthcheck.py, inbox.py, metrics.py, mode_detector.py, models.py, orchestrator.py, output.py, policy.py, runner.py, synthesis.py) functioning as domain-significant package-level utilities. ADR-40 calibration baseline estimated 8 modules; actual under strict definition: 2.
- **Required action:** None for ai-council. ADR-38 module definition correctly excludes package-level files — the calibration estimate was imprecise. ADR-38 may benefit from an amendment note acknowledging that repos with many package-level files may score lower on module count than their actual cognitive complexity suggests. Surface as BACKLOG item for ADR-38 amendment research.
- **Tier dependency:** Indirect — affects tier algorithm inputs, which in turn affects calibration.

---

### Calibration finding (separate, ecosystem-wide concern)

#### F-08 — ADR-40 coefficient miscalibration (cross-ecosystem)

- **ADR reference:** ADR-40 (scale tier evaluation algorithm)
- **Observation (from discovery computation):**
  - Pre-migration: ai-council score -7.4, clamped 0.0 → L
  - Post-migration: ai-council score -9.0, clamped 0.0 → L
  - ADR-40 calibration table had estimated ai-council score ~52 (Tier M); actual 0.0 (Tier L)
  - Primary driver: TCR estimate was ~30k tokens; actual is ~102k tokens (3.4x higher)
  - Secondary driver: module count estimate was 8; actual is 2 under strict ADR-38 definition
  - Per Rob's assessment: all ecosystem repos (corp-ops, .dev-knowledge, ai-council, corp-monorepo) classify L with current coefficients — algorithm not differentiating
- **Required action:**
  - Audit tool P1 implementation (BACKLOG P1 item) collects multi-repo data for evidence-based recalibration
  - Post-implementation: ADR-40 amendment with evidence-based coefficient adjustment OR confirmation that current classification behavior is intended
  - Research question worth Council debate: how should professionals evaluate repo complexity at relative scale in solo dev / LLM-driven workflows? Industry practice for "small/medium/large" may differ from enterprise-scale assumptions in current coefficients.
- **Tier dependency:** N/A — this finding IS the root of tier dependency.
- **Status:** OPEN, deferred per Rob's Path 3 strategy. No action before audit tool P1 data collection.

---

## Aggregate

| Severity | Count | Finding IDs |
|---|---|---|
| P1 (governance-blocking, tier-independent) | 2 | F-01, F-02 |
| P2 (important, tier-dependent) | 2 | F-03, F-04 |
| P3 (minor / amendment candidates) | 3 | F-05, F-06, F-07 |
| Calibration concern (ecosystem-wide) | 1 | F-08 |
| **Total** | **8** | |

---

## Tier-independent priority order (recommended for browser-2 ai-council session)

| Priority | Finding | Action | Dependency |
|---|---|---|---|
| 1 | F-01 VISION.md absent | Create `ai-council/VISION.md` per ADR-33 | None |
| 2 | F-02 Lessons discovery | Update CLAUDE.md with DEV_KNOWLEDGE_PATH reference | ADR-35 P1 impl (config doc now; functionality later) |
| 3 | F-05 ADR naming | Grandfather existing 7 ADRs; note for future ADRs | None (no files to rename) |
| 4 | F-06 + F-07 | Note in .dev-knowledge BACKLOG as ADR-38 amendment candidates | None (no ai-council action) |
| DEFER | F-03 BACKLOG.md | Await tier calibration | ADR-40 recalibration |
| DEFER | F-04 ARCHITECTURE.md | Await tier calibration | ADR-40 recalibration |

---

## Calibration question (philosophical / research-worthy)

How should professionals evaluate repo complexity at relative scale in solo dev / LLM-driven workflows? This is a fundamental question where the current algorithm (logarithmic Maintainability Index pattern) may embed enterprise-scale assumptions inappropriate for a 1-person ecosystem. Worth a Council research debate to surface industry practice. Recommend adding to .dev-knowledge BACKLOG.

---

**Next phase:** A3 Handoff (separate prompt) — generate handoff folder per ADR-37 two-phase format with these findings. Browser-2 in ai-council session consumes handoff and acts on prioritized actions (F-01, F-02 primary).
