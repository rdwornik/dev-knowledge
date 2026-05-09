# Handoff Stage 1: ai-council (audit-sync)

**Target repo:** ai-council
**Target path:** C:/Users/1028120/Documents/Dev/ai-council
**Repo HEAD at Stage 1:** c821157fcfa957bc6612c74667d70c8c9a88ef5c
**Repo branch:** main
**Repo working tree:** M config/settings.yaml (1 file modified, uncommitted)
**Generated:** 2026-05-09 (afternoon)
**Handoff type:** audit-sync
**Slug:** 2026-05-09-ai-council-audit-sync

════════════════════════════════════════════════════════════════════
SECTION A — INSTRUCTIONS FOR ROB (do NOT paste this into old chat)
════════════════════════════════════════════════════════════════════

1. Open the EXISTING (OLD) browser chat for ai-council — the chat being
   wrapped up because its context is getting full. NOT a new chat.
2. Copy from the PASTE_BOUNDARY line below to the end of this file.
3. Paste as a message in the existing ai-council chat.
4. The old chat answers the 5 pipeline questions from its lived knowledge.
5. Open the pre-created file: `docs/handoffs/_in_progress/2026-05-09-ai-council-audit-sync/stage2-response.md`
   (already exists, has placeholder content). Replace everything below the
   `═══ REPLACE EVERYTHING BELOW THIS LINE ═══` marker with the architect's
   response. Save.
6. In Claude Code at .dev-knowledge, say: "complete handoff for ai-council"
   → Stage 3 generates the final handoff folder.
7. After Stage 3: close the old chat. Open a NEW claude.ai chat for ai-council
   and use the Stage 3 folder bundle (00_README.md inside has upload
   instructions for the new chat).

════════════════════════════════════════════════════════════════════
PASTE_BOUNDARY — copy from here to end of file into the old chat
════════════════════════════════════════════════════════════════════

# Stage 2 — Answer These Questions: ai-council (audit-sync)

You are the EXISTING browser chat for **ai-council**, currently being wrapped
up because your context is getting full. Claude Code in `.dev-knowledge` is
preserving your accumulated knowledge as a structured handoff before this chat
closes.

Your tacit knowledge — current priorities, mental model, in-flight decisions,
recent concerns — is non-substitutable. `.dev-knowledge`'s audit findings
(below) provide an external view; your response provides the internal view that
only you have.

The handoff bundle generated from your response will be uploaded to a NEW
(fresh) browser chat that continues work on ai-council. That new chat has zero
history — your structured response here is what it will have.

The next session will focus on: closing P1 governance gaps from the 2026-04-30
audit — primarily creating VISION.md (F-01) and configuring lessons discovery
in CLAUDE.md (F-02).

## Current state (verified at Stage 1)

- HEAD: `c821157fcfa957bc6612c74667d70c8c9a88ef5c` (merge commit, ADR-38
  migration: refactored to `src/ai_council/` package namespace, updated
  imports, updated pyproject.toml, updated test imports, documented migration)
- Branch: `main`
- Working tree: `M config/settings.yaml` — 1 uncommitted modification
- ADR-38 compliance: PASS (5/5 checks) per 2026-04-30 rediscovery
- Test count: 310 per CLAUDE.md (class-based; `pytest --collect-only -q` canonical)
- Package structure: 12 direct files at `src/ai_council/` + 2 subpackages
  (providers/, research/)

## Audit context (2026-04-30 Faza A2 — .dev-knowledge's external view; extend or correct)

8 findings identified:

**P1 — Governance-blocking, tier-independent (action required):**
- F-01: VISION.md absent — create per ADR-33 schema (frontmatter:
  version/tier/owner/last_reviewed/scale; sections: Mission/Scope/Methodology/
  Lifecycle/Relationships)
- F-02: Lessons discovery not configured — update CLAUDE.md to reference
  DEV_KNOWLEDGE_PATH env var per ADR-35; consider whether `tasks/lessons.md`
  (ai-council-local) should migrate to .dev-knowledge LESSONS.md

**P2 — Deferred pending tier calibration:**
- F-03: BACKLOG.md absent — defer until ADR-40 recalibration confirms tier
- F-04: ARCHITECTURE.md absent — defer until tier confirmed

**P3 — Minor/grandfathered:**
- F-05: ADR naming kebab-case (7 existing ADRs grandfathered per ADR-29;
  future ADRs follow ADR-34 underscore convention)
- F-06: Test count discrepancy grep vs CLAUDE.md — class-based tests; no
  ai-council action needed
- F-07: Module count 2 (strict ADR-38 definition) vs estimate 8 — no action

**Calibration concern (F-08, cross-ecosystem, no ai-council action):**
- All repos clamp to L under current ADR-40 coefficients — algorithm
  miscalibration; deferred to audit tool P1 multi-repo data

## .dev-knowledge BACKLOG items relevant to ai-council

- Cross-stream P1 [open]: Phase 1 validation — audit + handoff dry-run on
  ai-council (this handoff IS that validation)
- Stream B: no items currently (empty placeholder)

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings so Claude Code can
parse them at Stage 3:

### 1. OBJECTIVE

What is the immediate goal of the next ai-council session?

Audit findings suggest F-01 (VISION.md creation) + F-02 (CLAUDE.md
DEV_KNOWLEDGE_PATH configuration) as the P1 actions. Confirm or revise.
What outcome should be achieved by end of next session — what does "done"
look like?

### 2. REALITY

What is the current state of ai-council from your perspective?

- Was anything completed in ai-council since the 2026-04-30 audit?
- Any work in progress not reflected in the audit (files open, branches
  active, WIP commits)?
- External dependencies (services, providers, libraries) currently in play
  or about to change?
- Any constraints (deadlines, Rob's schedule, external service changes) the
  next session must respect?
- Is the `config/settings.yaml` modification (observed in working tree)
  intentional or accidental? Should it be committed, stashed, or reverted
  before session work?

### 3. RATIONALE

What approaches were considered and discarded for ai-council recently?

For the **VISION.md tier** decision:
- Audit defaulted to L per current ADR-40 (all repos clamp L under current
  coefficients); calibration concern flagged (F-08)
- What's your judgment: does ai-council feel L (heavy infrastructure, ~102k
  tokens, 310 tests) or M (personal project, limited production surface, 1
  developer)? Reasons?

For **lessons discovery (F-02)**: does ai-council have meaningful lessons in
`tasks/lessons.md` that should migrate to .dev-knowledge LESSONS.md, or should
they remain ai-council-local? What criteria should guide that decision?

For **config/settings.yaml**: what was changed and why? Is it safe to include
in the session's commit scope?

### 4. DIRECTIVES

What are the exact sequential actions the next ai-council session should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

Default proposal (revise as needed):

1. Resolve `config/settings.yaml` — commit, stash, or revert as appropriate.
   Verify: `git status --porcelain` shows clean.
2. Create `ai-council/VISION.md` per ADR-33 schema. Verify: file exists;
   frontmatter includes version/tier/owner/last_reviewed/scale; all required
   sections (Mission/Scope/Methodology/Lifecycle/Relationships) present;
   `pytest -x` passes.
3. Update `ai-council/CLAUDE.md` to document `DEV_KNOWLEDGE_PATH` env var
   reference per ADR-35 essence. Verify: CLAUDE.md contains DEV_KNOWLEDGE_PATH;
   `pytest -x` passes.
4. Run `pytest -x` to confirm 310/310 baseline holds. Verify: exit code 0.
5. Update `ai-council/CHANGELOG.md` with session work. Verify: entry dated
   2026-05-09 present.
6. Update `ai-council/JOURNAL.md` with session tactical log. Verify: new entry
   at top with Did/Failed/Next.
7. Fill `09_EXECUTION_EVIDENCE.md` with command outputs from steps above.

Add, remove, or reorder as you see fit. Include F-05 (ADR naming note for
future ADRs) if trivially quick.

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

Default boundaries (extend as needed):
- DO NOT create `BACKLOG.md` (F-03 deferred — tier not confirmed)
- DO NOT create `ARCHITECTURE.md` (F-04 deferred — tier not confirmed)
- DO NOT rename existing 7 ADRs (F-05 grandfathered per ADR-29)
- DO NOT push without Rob's explicit confirmation
- DO NOT address pre-existing ruff (17 errors) or mypy (4 errors) — out of scope
- DO NOT make structural changes to `src/ai_council/` — migration complete
- If `pytest -x` fails at any step: STOP, report failure, do not continue

Add any concerns or "do not's" specific to your knowledge of current state.

## Format requirements (CRITICAL — read before responding)

Your response will be copy-pasted verbatim into a markdown file
(`stage2-response.md`) for Stage 3 parsing. Non-compliant format
breaks parsing or pollutes 06_STATE_OF_PLAY and 07_ACTION_PLAN output.

- Respond in **pure markdown** — no preamble, no closing remarks
- Do **NOT** wrap your response in a code fence
  (do NOT use ` ```markdown ... ``` ` around your whole response)
- Start your response directly with: `### 1. OBJECTIVE`
- End your response with the final line of BOUNDARIES section
- Each section heading must be exactly: `### {number}. {NAME}`
  (level-3 markdown heading, exact name from list above)
- All 5 sections required, in order: OBJECTIVE / REALITY / RATIONALE
  / DIRECTIVES / BOUNDARIES
- Within sections: free-form markdown (paragraphs, bullets, numbered
  lists, code blocks all OK)
- Do not add extra top-level sections beyond the 5 required

════════════════════════════════════════════════════════════════════
End of paste block.
Old chat: please answer questions 1-5 above following the Format
requirements above. Structure response with the exact headings
(OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES) so
Claude Code can parse them at Stage 3.
════════════════════════════════════════════════════════════════════
