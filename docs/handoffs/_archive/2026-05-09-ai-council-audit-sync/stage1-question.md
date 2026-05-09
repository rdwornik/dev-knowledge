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

## Your role

You are the existing browser chat for **ai-council**, currently being wrapped
up because your context is getting full. Claude Code in `.dev-knowledge` is
preserving your accumulated knowledge as a structured handoff before this chat
closes.

Your role for this Stage 2 response: **project-level architect for ai-council**.
You provide:
- Goal judgment (what next session should achieve, why)
- Project state YOU witnessed in this conversation (not general knowledge
  inferred from training)
- Reasoning and criteria for decisions (how to think about tier choice,
  priority calls, deferrals)
- Do-not lists that come from project context (gotchas, scope boundaries
  you know matter)

You are NOT:
- An oracle for ecosystem-wide conventions (.dev-knowledge structure, ADR
  schemas, cross-repo patterns)
- A source of repo state facts (HEAD SHA, file contents, configs, test
  counts) — Stage 3 verifies those against the repo directly
- Required to provide specifics where you don't have direct knowledge

## What's in the handoff bundle (so don't repeat these)

The new (fresh) chat receiving the Stage 3 handoff bundle will automatically
have:
- Full `.dev-knowledge` VISION.md (ecosystem context)
- Full `.dev-knowledge` PLAYBOOK.md (methodology, conversation style,
  prompt format, commit conventions)
- Full `.dev-knowledge` ESSENTIALS.md (high-leverage rules)
- ADR essences (operational rules) for ADRs cited in directives
- Audit report (raw findings, the same findings listed below)
- Repo state snapshot (HEAD, branch, file tree, working tree state)

You do NOT need to:
- Explain what ADR-33 mandates for VISION.md (handoff has the essence)
- Restate audit findings verbatim (handoff has audit-report.md)
- Specify HEAD SHA or working tree state (handoff has manifest)
- Describe .dev-knowledge governance patterns (handoff has VISION + PLAYBOOK)

Focus on what only YOU witnessed or judged in this conversation.

## Epistemic honesty (CRITICAL)

For each claim in your response, classify it:

- **Witnessed**: you saw this happen in this conversation — state it confidently
- **(architect inference)**: you are reasoning from context, not direct
  observation — mark it inline
- **Unknown**: you don't have direct knowledge — say so explicitly

Examples:
- "The config/settings.yaml was modified in our session when we changed
  provider timeouts" → witnessed, state confidently
- "The tier is probably M based on perceived complexity" →
  write "(architect inference)" after the claim
- "I don't know the exact test count — verify against repo" → unknown

LLMs default to "be helpful" by filling gaps with plausible specifics.
Resist this. Stage 3 verifies factual claims against the repo. Your value
is judgment and reasoning, not confident fabrication of facts you didn't
witness.

If you don't know something specific (a commit message, a file name, a
version number, a config value): say "Unknown — Stage 3 should verify."

## Format requirements (CRITICAL — read before responding)

Your response will be copy-pasted verbatim into stage2-response.md for
Stage 3 parsing. Non-compliant format breaks parsing.

**Required:**
- Pure markdown — no preamble, no closing remarks
- Start your response with: `### 1. OBJECTIVE`
- End your response with the final line of BOUNDARIES content
- Each section heading: `### {number}. {NAME}` (level-3 markdown, exact name)
- All 5 sections required, in order: OBJECTIVE / REALITY / RATIONALE /
  DIRECTIVES / BOUNDARIES

**Allowed within sections:** paragraphs, bullet lists, numbered lists,
**bold**, *italic*, `inline code`, code blocks, tables, blockquotes.

**NOT allowed:**
- Wrapping entire response in code fence (no ` ```markdown ` at start;
  no closing ` ``` ` at end)
- Preamble before first heading ("Here's my response:", "Sure:")
- Closing remarks after BOUNDARIES section
- Extra top-level sections beyond the 5 required

**Example correct opening:**
```
### 1. OBJECTIVE
The next session should...
```

**Example WRONG opening (do not do this):**
```
Here's my structured response:

```markdown
### 1. OBJECTIVE
```

## Current state (verified at Stage 1 by Claude Code)

- HEAD: `c821157fcfa957bc6612c74667d70c8c9a88ef5c` (merge commit, ADR-38
  migration: refactored to `src/ai_council/` package namespace, updated
  imports, updated pyproject.toml, updated test imports, documented migration)
- Branch: `main`
- Working tree: `M config/settings.yaml` — 1 uncommitted modification
- ADR-38 compliance: PASS (5/5 checks) per 2026-04-30 rediscovery
- Test count: 310 per CLAUDE.md (class-based; `pytest --collect-only -q` canonical)
- Package structure: 12 direct files at `src/ai_council/` + 2 subpackages
  (providers/, research/)

## Audit context (informational — extend or correct in your response)

8 findings from 2026-04-30 Faza A2 (.dev-knowledge's external view):

**P1 — Governance-blocking, tier-independent (action required):**
- F-01: VISION.md absent
- F-02: Lessons discovery not configured (DEV_KNOWLEDGE_PATH in CLAUDE.md)

**P2 — Deferred pending tier calibration:**
- F-03: BACKLOG.md absent
- F-04: ARCHITECTURE.md absent

**P3 — Minor/grandfathered:**
- F-05: ADR naming kebab-case (7 existing ADRs grandfathered)
- F-06: Test count discrepancy grep vs CLAUDE.md — class-based tests; no action
- F-07: Module count 2 vs estimate 8 — calibration imprecision; no action

**Calibration concern (no ai-council action):**
- F-08: All repos clamp to L under current ADR-40 coefficients; deferred

## .dev-knowledge BACKLOG items relevant to ai-council

- Cross-stream P1 [open]: Phase 1 validation — audit + handoff dry-run on
  ai-council (this handoff IS that validation)
- Stream B: no items currently (empty placeholder)

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

What is the immediate goal of the next ai-council session?

Audit findings suggest F-01 (VISION.md creation) + F-02 (CLAUDE.md
DEV_KNOWLEDGE_PATH configuration) as the P1 actions. Confirm or revise.
What outcome should be achieved by end of next session?

*Epistemic note: state your goal judgment confidently. If the audit's
suggested actions feel wrong to you, say so with reasoning.*

### 2. REALITY

What is the current state of ai-council from your perspective?

- Was anything completed in ai-council since the 2026-04-30 audit?
- Any work in progress not visible externally?
- External dependencies (services, providers, libraries) currently in play?
- Any constraints the next session must respect?
- The `config/settings.yaml` modification — intentional or accidental?
  Should it be committed, stashed, or reverted?

*Epistemic note: differentiate witnessed events (you saw this in conversation)
from inferences (reasoning from context — mark "(architect inference)") from
unknowns (no direct knowledge — say "Unknown — verify against repo"). Avoid
inventing specifics you didn't see.*

### 3. RATIONALE

What approaches were considered and discarded for ai-council recently?

For **VISION.md tier** (M vs L):
- Audit defaulted to L per ADR-40 current coefficients (all repos clamp L);
  calibration concern flagged (F-08)
- What's your judgment: does ai-council feel L or M to you? What's your
  reasoning? (You don't need to reproduce ADR-40 — just give your judgment
  and the project-level factors that informed it)

For **lessons discovery (F-02)**: does ai-council have meaningful lessons in
`tasks/lessons.md` worth migrating to .dev-knowledge? What criteria matter?

For **config/settings.yaml**: what changed and why? Safe to commit?

*Epistemic note: reasoning is your strong suit — explain your judgment. For
any specific facts in your reasoning, mark "(architect inference)" if not
directly witnessed.*

### 4. DIRECTIVES

What are the exact sequential actions the next ai-council session should
execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

Default proposal for revision (based on audit findings — revise as needed):

1. Resolve `config/settings.yaml` — commit, stash, or revert.
   Verify: `git status --porcelain` clean.
2. Create `ai-council/VISION.md` per ADR-33 (handoff bundle has ADR-33 essence).
   Verify: file exists; frontmatter complete; required sections present; `pytest -x` passes.
3. Update `ai-council/CLAUDE.md` with DEV_KNOWLEDGE_PATH env var reference.
   Verify: reference present; `pytest -x` passes.
4. Run `pytest -x` — confirm 310/310 baseline holds. Verify: exit code 0.
5. Update `ai-council/CHANGELOG.md` + `ai-council/JOURNAL.md`.
6. Fill `09_EXECUTION_EVIDENCE.md` with command outputs.

*Epistemic note: action sequence and verification steps are most valuable.
Specific file paths or commit messages — mark "(architect inference)" if not
witnessed; Stage 3 may revise based on repo state.*

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

Default boundaries (revise as needed):
- DO NOT create `BACKLOG.md` (F-03 deferred — tier not confirmed)
- DO NOT create `ARCHITECTURE.md` (F-04 deferred — tier not confirmed)
- DO NOT rename existing 7 ADRs (F-05 grandfathered)
- DO NOT push without Rob's explicit confirmation
- DO NOT address pre-existing ruff (17) or mypy (4) errors — out of scope
- DO NOT restructure `src/ai_council/` — migration complete
- If `pytest -x` fails at any step: STOP, report, do not continue

*Epistemic note: do-not lists grounded in your project knowledge are
valuable. Don't fabricate "do not touch X" if you don't know whether X
exists — focus on what you know.*

════════════════════════════════════════════════════════════════════
End of paste block.
Old chat: please answer questions 1-5 above following the Format
requirements above. Structure response with the exact headings
(OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES) so
Claude Code can parse them at Stage 3.
════════════════════════════════════════════════════════════════════
