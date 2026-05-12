# Handoff Stage 1: ai-council (session-sync)

<!-- scope: meta -->

| Field | Value |
|---|---|
| Repo | `C:\Users\1028120\Documents\Dev\ai-council` |
| HEAD SHA | `f094d0821a279f3aa36de554943c1b44576d0924` |
| Branch | `main` |
| Working tree | clean |
| Slug | `2026-05-12-ai-council-session-sync-2` |
| Generated | 2026-05-12 |
| Type | session-sync |

════════════════════════════════════════════════════════════════════
SECTION A — INSTRUCTIONS FOR ROB (do NOT paste this into old chat)
════════════════════════════════════════════════════════════════════

1. Open the EXISTING (OLD) browser chat for ai-council — the chat being
   wrapped up. NOT a new chat.
2. Copy from the PASTE_BOUNDARY line below to the end of this file.
3. Paste as a message in the existing chat.
4. The old chat answers the 5 pipeline questions from its lived knowledge.
5. Open the pre-created file:
   `docs/handoffs/_in_progress/2026-05-12-ai-council-session-sync-2/stage2-response.md`
   (already exists, has placeholder content). Replace everything below the
   "═══ REPLACE EVERYTHING BELOW THIS LINE ═══" marker with the architect's
   response. Save.
6. In Claude Code at .dev-knowledge, say: "complete handoff for ai-council"
   → Stage 3 generates the final handoff folder.
7. After Stage 3: close the old chat. Open a NEW claude.ai chat for ai-council
   and use the Stage 3 folder bundle (00_README.md inside has upload
   instructions for the new chat).

════════════════════════════════════════════════════════════════════
PASTE_BOUNDARY — copy from here to end of file into the old chat
════════════════════════════════════════════════════════════════════

# Stage 2 — Answer These Questions: ai-council (session-sync)

## Your role

You are the existing browser chat for **ai-council**, currently being wrapped up
because your context is getting full. Claude Code in `.dev-knowledge` is
preserving your accumulated knowledge as a structured handoff before this
chat closes.

Your role for this Stage 2 response: **project-level architect for ai-council**.
You provide:
- Goal judgment (what next session should achieve, why)
- Project state YOU witnessed in this conversation (not general knowledge
  inferred from training)
- Reasoning and criteria for decisions (how to think about priority calls,
  implementation choices, deferrals)
- Do-not lists that come from project context (gotchas, scope boundaries
  you know matter)

You are NOT:
- An oracle for ecosystem-wide conventions (.dev-knowledge structure, ADR
  schemas, cross-repo patterns)
- A source of repo state facts (HEAD SHA, file contents, configs, test
  counts) — Stage 3 verifies those against the repo directly
- Required to provide specifics where you don't have direct knowledge

**Self-containment requirement (CRITICAL):** This handoff covers **ai-council only**.
DIRECTIVES must target ai-council files, state, and work only. Do NOT include
directives targeting other repos (corp-monorepo, .dev-knowledge, etc.) —
per ADR-41 each repo manages its own BACKLOG; one repo never reconciles another
repo's tracking artifacts via its own handoff. Cross-repo work that occurred in
this session flows via routing artifacts (cross-repo decision propagation,
scrum-master review reports), not via this handoff bundle.

## What's in the handoff bundle (so don't repeat these)

The new (fresh) chat receiving the Stage 3 handoff bundle will automatically have:
- Full `.dev-knowledge` VISION.md (ecosystem context)
- Full `.dev-knowledge` PLAYBOOK.md (methodology, conversation style,
  prompt format, commit conventions)
- Full `.dev-knowledge` ESSENTIALS.md (high-leverage rules)
- ADR essences (operational rules) for ADRs cited in directives
- Repo state snapshot (HEAD, branch, file tree, working tree state)

You do NOT need to:
- Explain what ADR-NN mandates (handoff has the essence)
- Specify HEAD SHA or working tree state (handoff has manifest)
- Describe ecosystem governance patterns (handoff has VISION + PLAYBOOK)

Focus on what only YOU witnessed or judged in this conversation.

## Epistemic honesty (CRITICAL)

For each claim in your response, classify it using these markers:

- **Witnessed**: you saw this happen in conversation — state it confidently
- **(architect inference)**: you are reasoning from context, not direct
  observation — mark it inline
- **Unknown**: you don't have direct knowledge — say so explicitly

Examples:
- "The routing.py TargetResolver was implemented during our session" → witnessed
- "AGENTS.md is probably low-effort to add" → inference, write "(architect inference)"
- "I don't know the exact test count — verify against repo" → unknown

LLMs default to "be helpful" by filling gaps with plausible specifics.
Resist this. Stage 3 verifies factual claims against the repo. Your
value is judgment and reasoning, not confident fabrication of facts
you didn't witness.

## Format requirements (CRITICAL — read before responding)

Your response will be copy-pasted verbatim into stage2-response.md for
Stage 3 parsing.

**Copy-paste note:** chat UIs sometimes strip `#` markdown markers when
you copy rendered text. Stage 3 parser is TOLERANT and accepts multiple
heading formats. Use ANY of these for section headings:

- Markdown level-3: `### 1. OBJECTIVE`
- Bold: `**1. OBJECTIVE**`
- Plain numbered: `1. OBJECTIVE`

If unsure which survives your client's copy-paste, use both:
`### **1. OBJECTIVE**` — at least one form will survive.

**Required:**
- No preamble before first heading ("Here's my response:", "Sure:")
- No closing remarks after final BOUNDARIES content
- All 5 sections required, in order: OBJECTIVE / REALITY /
  RATIONALE / DIRECTIVES / BOUNDARIES
- Each section heading uses exact section name (case-sensitive)
- No extra top-level sections beyond the 5 required

**NOT allowed:**
- Wrapping ENTIRE response in code fence (no opening ` ```markdown `
  or ` ``` ` at the very start; no closing ` ``` ` at the very end)

## Current state (verified at Stage 1 by Claude Code)

- HEAD: `f094d0821a279f3aa36de554943c1b44576d0924`
- Branch: `main`
- Working tree: clean
- Recent commits:
  - `f094d08` docs(audit): codex review for audit-addendum-i7-i8
  - `baeb6bc` docs: CHANGELOG + JOURNAL for scrum-master addendum (I7 + I8)
  - `7fb45b0` docs(backlog,lessons): BACKLOG M2 supersession sync + architect local-config-defense lesson
  - `2986ac0` chore(handoffs): I8 rename _archive → archive (align to A2 operator decision)
  - `21ef4e7` chore(lessons): I7 move tasks/lessons.md → LESSONS.md root + retire tasks/ folder
  - `5346045` fix(review): codex medium/low — grok_research in README, panel defaults in guide, docs/ folder governance, rubric provenance
  - `d106697` docs(audit): codex review for scrum-master-review-2026-05-12
  - `55c393e` docs: CHANGELOG + JOURNAL for scrum-master review implementation

## .dev-knowledge BACKLOG items relevant to ai-council

**Stream B:**
- **[P2] [open]** ai-council needs AGENTS.md — PLAYBOOK governance gap.
  Each repo must have AGENTS.md at root (cross-tool canonical governance per
  Council #28). ai-council has CLAUDE.md but no AGENTS.md (verified 2026-05-11).
  Work belongs in ai-council repo.

**Cross-stream / Ecosystem:**
- **[P2] [open]** Phase 2 universalization rollout — ai-council substantially
  complete as of 2026-05-12: ADR-34 hyphen compliance achieved, ADR-38 Scale M
  gaps closed (BACKLOG.md, LESSONS.md at root, tasks/ retired), VISION.md tier M
  declared, scrum-master review cycle N=1 completed. Remaining for ai-council:
  AGENTS.md (P2), ARCHITECTURE.md (optional at M tier).
- **[P2] [open]** ai-council hyphen migration + ADR-38 compliance — (1) verify
  hyphen-only filename compliance (likely low impact); (2) confirm ADR-38 Scale M
  gaps are closed (cross-check BACKLOG, LESSONS, ARCHITECTURE presence).
- **[P3] [open]** Handoff folder format adoption — ai-council still has flat
  `docs/HANDOFF.md` (pre-ADR-42 pattern). Retire at next handoff event or
  designate as legacy. Tied to A4 decision (separate ADR or conversational) about
  single-artifact vs multi-artifact handoff format.
- **[P3] [open]** docs/HANDOFF.md flat file deprecation — ai-council has
  `docs/HANDOFF.md` at docs/ level. Not breaking. Retire at next handoff event
  or explicitly designate as legacy.

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

What is the immediate goal of the next ai-council session?

Given the completed scrum-master review cycle (I1–I8 + I7/I8 addendum fully
implemented), what is the highest-value next session focus — AGENTS.md
creation, Phase 2 compliance verification, or something else you witnessed
as a more pressing need? Revise as you see fit.

*Epistemic note: state your goal judgment confidently. If any of the above
feels wrong, say so with reasoning.*

### 2. REALITY

What is the current state of ai-council from your perspective?

- What was completed in this session (scrum-master review items, addendum,
  cross-repo handshake, hyphen migration)?
- Any work in progress not yet committed or only partially done?
- What is the state of the `docs/HANDOFF.md` flat file — is it current,
  stale, or already deprecated?
- Any constraints (conventions, blockers, open questions) the next session
  must respect?

*Epistemic note: differentiate witnessed events from inferences from unknowns.
Mark inferences with "(architect inference)" and unknowns with "Unknown —
verify against repo."*

### 3. RATIONALE

What approaches were considered and discarded during this session for ai-council?

- Were there any alternative implementations considered for routing.py,
  the scrum-master review response items, or the cross-repo handshake?
- Why was the current implementation sequence chosen?
- Any technical decisions about AGENTS.md scope or content that were
  discussed or deferred?

*Epistemic note: reasoning is your strong suit — explain your judgment.*

### 4. DIRECTIVES

What are the exact sequential actions the next ai-council session should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

Default proposal (revise or reorder as architect sees fit):
1. Create `AGENTS.md` at repo root following `templates/AGENTS-md-template.md`
   in .dev-knowledge. Verify: file present at root, content covers cross-tool
   governance (Codex, Claude Code, Cursor, Aider), scope, project context.
2. Verify ADR-38 Scale M compliance is complete: BACKLOG.md at root ✓,
   LESSONS.md at root ✓, ARCHITECTURE.md at root (optional at M — if absent,
   confirm decision to defer). Verify: `git ls-files | grep -E "^(ARCHITECTURE|BACKLOG|LESSONS)"`.
3. Verify hyphen-only filename compliance: check ADR files, transcript files,
   any auto-generated output files. Verify: no underscore separators in
   new files post-ADR-34 amendment.
4. Decide `docs/HANDOFF.md` fate: explicitly deprecate with header comment
   "Legacy pre-ADR-42 handoff. Current handoffs in docs/handoffs/ per ADR-42."
   OR delete if confirmed stale. Verify: no broken references.

Add, remove, or reorder based on your session knowledge.

*Self-containment reminder: every directive above must target ai-council only.
Do NOT add directives about other repos' BACKLOG, ARCHITECTURE, or compliance
state — that work belongs to those repos' own sessions.*

*Epistemic note: action sequence and verification steps are most valuable.
Specific file paths — mark "(architect inference)" if not directly witnessed.*

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

Default boundaries (revise as architect sees fit):
- Do NOT modify routing.py, CLI config, or cross-repo routing logic — that
  work completed this session; next session is governance + compliance only.
- Do NOT implement cross-repo audit tool — that's a .dev-knowledge concern
  (Stream C P1 in .dev-knowledge BACKLOG).
- Do NOT reconcile, audit, or direct work on other repos' BACKLOG or
  tracking files via this handoff — per ADR-41 each repo manages its own
  state. Cross-repo work flows via routing artifacts.
- Do NOT generate reconciliation reports about other repos' state. Do NOT
  treat staleness observations about another repo's tracking as a directive.
- If AGENTS.md content is unclear: use the template as scaffold, mark
  sections Unknown where warranted, do not fabricate governance rules.

Add any architect-specific "do not's" from your session knowledge.

════════════════════════════════════════════════════════════════════
End of paste block.
Old chat: please answer questions 1-5 above following the Format
requirements above. Structure response with the exact headings
(OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES) so
Claude Code can parse them at Stage 3.
════════════════════════════════════════════════════════════════════
