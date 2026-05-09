# Handoff Question Template (Stage 1 output)

This template is filled by Claude Code in .dev-knowledge during Stage 1.
The customized output goes to Browser-2 architect for project intelligence
gathering. See ADR-42 (amended) and HANDOFF_PROCESS.md v3.1 for full flow.

ALL handoff types (audit-sync, session-sync, feature-X-sync) use this
template — there is no audit-sync shortcut. Stage 2 is mandatory.

**Filename conventions for Rob:**
- Stage 1 output: `docs/handoffs/_in_progress/{slug}/stage1-question.md`
- Stage 2 response (Rob saves): `docs/handoffs/_in_progress/{slug}/stage2-response.md`
- Slug format: `{YYYY-MM-DD}-{repo}-{type}` (e.g., `2026-05-09-ai-council-audit-sync`)

**Expected Stage 2 response format:**
Each of the 5 pipeline question headers below must appear in browser-2's
response with a matching heading (OBJECTIVE / REALITY / RATIONALE /
DIRECTIVES / BOUNDARIES). This allows Stage 3 to parse and populate
06_STATE_OF_PLAY.md and 07_ACTION_PLAN.md deterministically.

---

# Handoff Questionnaire — {repo} ({type})

**Target repo:** {repo}
**Path:** {path}
**Repo HEAD at Stage 1:** {head_sha}
**Repo branch:** {branch}
**Generated:** {timestamp}
**Handoff type:** {audit-sync | session-sync | feature-X-sync}

---

## Context for Browser-2 architect

You are the architect for **{repo}**. `.dev-knowledge` is preparing a handoff
bundle for the next session working on {repo}. Your job: provide project-level
intelligence that complements `.dev-knowledge`'s ecosystem-level context.

The next session may be: {audit | new feature | bug fix | refactor | session
continuation}.

Current known state (from `.dev-knowledge` perspective):
{brief_summary_of_what_dev_knowledge_knows}

---

## Pipeline questions (answer these in order)

### 1. OBJECTIVE

What is the immediate goal of the next session working on {repo}?

What outcome should be achieved? In 1-3 sentences.

### 2. REALITY

What is the current state of {repo}?

- What was completed in the most recent work?
- What is in progress (files open, branches active, WIP)?
- What dependencies exist (external libs, services, other repos)?
- What constraints apply (deadlines, tier classification, repo conventions)?
- Are there known blockers?

### 3. RATIONALE

What approaches were considered and discarded?

For each major decision recently made or pending:
- What was the chosen path?
- What alternatives were rejected, and why?
- What's the "why now" reasoning for the next session?

### 4. DIRECTIVES

What are the exact sequential actions the next session should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.
Example: "1. Create `ai-council/VISION.md` per ADR-33 schema. Verify: file exists,
frontmatter has all required fields, `pytest -x` passes."

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

- **Do not's:** explicit no-go list (files to avoid, patterns to not follow, deferred items)
- **Out of scope:** what's acknowledged but deferred to a later session
- **Fallbacks:** if action X fails, do Y

---

## Receiver synthesis prompt

After reading this questionnaire response and the rest of the handoff bundle,
the receiving session must summarize their understanding before acting:

> "I will execute {goal}. My understanding: {paraphrase of REALITY + RATIONALE}.
> I will NOT do {out-of-scope items}. I will start with {first action from DIRECTIVES}.
> Verification: HEAD SHA matches {head_sha}, working tree is {expected state}."

Only proceed if Rob confirms the synthesis is accurate.

---

**Browser-2 architect: please answer pipeline questions 1-5 above with
project-level detail. Structure your response with section headings that
match the 5 question names (OBJECTIVE / REALITY / RATIONALE / DIRECTIVES /
BOUNDARIES) so Claude Code can parse them at Stage 3.**

**Rob: save browser-2's full response as:**
`docs/handoffs/_in_progress/{slug}/stage2-response.md`

Then in Claude Code at `.dev-knowledge`, say:
`"complete handoff for {repo}"` → Stage 3 generates the final handoff folder.

Stage 3 will verify receiver synthesis accuracy before declaring the handoff complete.
