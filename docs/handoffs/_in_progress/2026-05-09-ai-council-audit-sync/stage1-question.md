# Handoff Stage 1: Question Prompt for existing ai-council chat

**Target repo:** ai-council
**Target path:** C:/Users/1028120/Documents/Dev/ai-council
**Repo HEAD at Stage 1:** c821157fcfa957bc6612c74667d70c8c9a88ef5c
**Repo branch:** main
**Repo working tree:** M config/settings.yaml (1 file modified, uncommitted)
**Generated:** 2026-05-09 (afternoon)
**Handoff type:** audit-sync
**Slug:** 2026-05-09-ai-council-audit-sync

---

## How to use this file (Rob's instructions)

1. Open the EXISTING (OLD) browser chat for ai-council — the chat being
   wrapped up because its context is getting full. **NOT a new chat.**
2. Copy everything from the "Context for architect" section through the end
   of this file as a message in that existing chat.
3. The existing chat will provide answers to the 5 pipeline questions from its
   accumulated context and lived knowledge.
4. Save the response as:
   `docs/handoffs/_in_progress/2026-05-09-ai-council-audit-sync/stage2-response.md`
   in the .dev-knowledge repo (copy-paste response, save file).
5. Return to Claude Code in .dev-knowledge and say:
   "complete handoff for ai-council" → Stage 3 generates the final handoff folder.
6. THEN open a NEW claude.ai chat for ai-council and use the Stage 3 folder bundle
   (00_README.md inside the folder has upload instructions).

---

## Context for architect (existing ai-council chat)

You are the EXISTING browser chat for **ai-council**, currently being wrapped up
because your context is getting full. Claude Code in `.dev-knowledge` is capturing
your accumulated knowledge as a structured handoff before this chat closes.

Your tacit knowledge — current priorities, mental model, in-flight decisions,
recent concerns, what's genuinely important vs cosmetic — is non-substitutable.
`.dev-knowledge`'s audit findings (below) provide an external view; your response
provides the internal view that only you have.

The handoff bundle generated from your response will be uploaded to a NEW (fresh)
browser chat that continues work on ai-council. That new chat has zero history —
your structured response here is what it will have.

The next ai-council session will work on: closing P1 governance gaps identified
by the audit — specifically creating VISION.md (F-01) and configuring lessons
discovery in CLAUDE.md (F-02).

### Current ai-council state (verified at Stage 1)

- HEAD: `c821157fcfa957bc6612c74667d70c8c9a88ef5c` (merge commit, ADR-38 migration
  5-commit sequence: refactored to `src/ai_council/` package namespace, updated
  imports, updated pyproject.toml, updated test imports, documented migration)
- Branch: `main`
- Working tree: `M config/settings.yaml` — 1 uncommitted modification
- ADR-38 compliance: PASS (5/5 checks) per 2026-04-30 rediscovery
- Test count: 310 (per CLAUDE.md; grep undercount 219 due to class-based tests)
- Python files: 12 at `src/ai_council/` level + 2 subpackages (providers/, research/)

### Audit context (2026-04-30 Faza A2 — .dev-knowledge's external view; extend or correct)

8 findings identified:

**P1 — Governance-blocking, tier-independent (action required):**
- F-01: VISION.md absent — create per ADR-33 schema
  (frontmatter: version/tier/owner/last_reviewed/scale; sections: Mission/Scope/
  Methodology/Lifecycle/Relationships)
- F-02: Lessons discovery not configured — update CLAUDE.md to reference
  DEV_KNOWLEDGE_PATH env var per ADR-35; consider whether `tasks/lessons.md`
  (ai-council-local) should migrate to .dev-knowledge LESSONS.md

**P2 — Deferred pending tier calibration:**
- F-03: BACKLOG.md absent — defer until ADR-40 recalibration confirms tier
- F-04: ARCHITECTURE.md absent — defer until tier confirmed

**P3 — Minor/grandfathered:**
- F-05: ADR naming kebab-case (7 existing ADRs grandfathered per ADR-29;
  future ADRs should follow ADR-34 underscore convention)
- F-06: Test count discrepancy (219 grep vs 310 CLAUDE.md — class-based tests;
  use `pytest --collect-only -q` as canonical; no ai-council action)
- F-07: Module count 2 (strict ADR-38 definition) vs estimate 8 (imprecise
  calibration baseline); no ai-council action

**Calibration concern (F-08, cross-ecosystem):**
- All repos clamp to L under current ADR-40 coefficients — algorithm
  miscalibration; deferred to audit tool P1 multi-repo data; no ai-council action

### .dev-knowledge BACKLOG items relevant to ai-council

- Cross-stream P1 [open]: Phase 1 validation — audit + handoff dry-run on
  ai-council (this handoff IS that validation)
- Stream B: no items currently (empty placeholder)

---

## Pipeline questions (answer these in order)

Structure your response with these exact section headings so Claude Code can
parse them at Stage 3:
**OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES**

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

For the **VISION.md tier** decision specifically:
- Audit defaulted to L per current ADR-40 (all repos clamp L under current
  coefficients)
- Calibration concern flagged (F-08) — ai-council may reasonably be M after
  recalibration
- What's your judgment: does ai-council feel L (heavy infrastructure, ~102k
  tokens, 310 tests) or M (personal project, limited production surface, 1
  developer)? Reasons for your assessment?

For **lessons discovery (F-02)**: does ai-council have meaningful lessons in
`tasks/lessons.md` that should migrate to .dev-knowledge LESSONS.md, or should
they remain ai-council-local? What criteria should guide that decision?

For **config/settings.yaml**: what was changed and why? Is it safe to include
in the session's commit scope?

### 4. DIRECTIVES

What are the exact sequential actions the next ai-council session should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

Default proposal (revise as needed):

1. Check `config/settings.yaml` modification — commit, stash, or revert as
   appropriate. Verify: `git status --porcelain` shows clean.
2. Create `ai-council/VISION.md` per ADR-33 schema. Verify: file exists;
   frontmatter includes version/tier/owner/last_reviewed/scale; all required
   sections (Mission/Scope/Methodology/Lifecycle/Relationships) present;
   `pytest -x` passes (no regressions).
3. Update `ai-council/CLAUDE.md` to document `DEV_KNOWLEDGE_PATH` env var
   reference per ADR-35 essence. Verify: CLAUDE.md contains DEV_KNOWLEDGE_PATH;
   configuration note present; `pytest -x` passes.
4. Run `pytest -x` to confirm 310/310 baseline holds. Verify: exit code 0.
5. Update `ai-council/CHANGELOG.md` with session work. Verify: entry dated
   2026-05-09 present.
6. Update `ai-council/JOURNAL.md` with session tactical log. Verify: new entry
   at top with Did/Failed/Next.
7. Fill `09_EXECUTION_EVIDENCE.md` with command outputs from steps above. Verify:
   all 6 sections populated (Commands/Test results/Git diffs/Final HEAD/Failures/
   Handoff for next session).

Add, remove, or reorder actions as you see fit. If F-05 (ADR naming note for
future ADRs) is trivially quick, include it. Otherwise skip.

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

Default boundaries (extend as needed):
- DO NOT create `BACKLOG.md` (F-03 deferred — tier not confirmed)
- DO NOT create `ARCHITECTURE.md` (F-04 deferred — tier not confirmed)
- DO NOT rename existing 7 ADRs (F-05 grandfathered per ADR-29)
- DO NOT push without Rob's explicit confirmation
- DO NOT address pre-existing ruff (17 errors) or mypy (4 errors) — out of scope
- DO NOT make structural changes to `src/ai_council/` (migration complete,
  no further refactoring this session)
- If `pytest -x` fails at any step: STOP, report failure, do not continue

Add any concerns or "do not's" specific to your knowledge of the current state.

---

## Receiver synthesis prompt

After reading the Stage 2 response and the rest of the handoff bundle, the
receiving NEW chat (browser-2 in next ai-council session) must provide this
synthesis before acting:

> "I will execute {goal from OBJECTIVE}. My understanding of current state:
> {paraphrase of REALITY answer}. I chose this approach because: {paraphrase
> of RATIONALE}. I will execute in order: {numbered actions from DIRECTIVES}.
> I will NOT do: {boundaries list}. Verification: HEAD SHA must match
> `c821157fcfa957bc6612c74667d70c8c9a88ef5c`, working tree `M config/settings.yaml`
> (or clean if settings.yaml resolved before handoff). I will start with
> {first action from DIRECTIVES}."

Only proceed if Rob confirms the synthesis is accurate.

---

**Existing ai-council chat: please answer pipeline questions 1-5 above from
your accumulated context and lived knowledge. Structure your response with
section headings matching the 5 question names (OBJECTIVE / REALITY /
RATIONALE / DIRECTIVES / BOUNDARIES) so Claude Code can parse them at Stage 3.**

**Rob: save the existing chat's full response as:**
`docs/handoffs/_in_progress/2026-05-09-ai-council-audit-sync/stage2-response.md`

Then in Claude Code at `.dev-knowledge`, say:
`"complete handoff for ai-council"` → Stage 3 generates the final handoff folder.

After Stage 3: close this existing chat. Open a NEW claude.ai chat for ai-council
and use the Stage 3 folder bundle.
