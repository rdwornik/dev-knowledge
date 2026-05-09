# Handoff Stage 1 Question Template

<!-- scope: meta -->

This template generates `stage1-question.md` files. It has TWO distinct
sections that must remain visually separated for different audiences:

- **Section A (Rob's operational instructions)** — what Rob does with the
  file. Rob reads this. Rob does NOT paste this into the old chat.
- **Section B (paste-this block)** — the actual message Rob copies into the
  old browser chat for the architect to answer.

The `PASTE_BOUNDARY` delimiter line makes this separation explicit. Rob selects
from PASTE_BOUNDARY down to end of file when copying into old chat.

**Three-actor flow (per ADR-42, twice amended):**
- Stage 2 source = OLD browser chat for {repo} (existing chat being wrapped up)
- Stage 3 receiver = NEW browser chat for {repo} (fresh, opened after folder generated)
- Claude Code = orchestrator throughout

**Note on receiver synthesis prompt:** The synthesis prompt belongs in
`00_first-message.md` (Stage 3 output). It is NOT included in stage1-question.md.

---

## Stage 1 output structure (Claude Code generates this)

When Claude Code generates `stage1-question.md` from this template, the output
file must follow this structure:

```
# Handoff Stage 1: {repo} ({type})

[METADATA HEADER — repo path, HEAD SHA, branch, working tree, slug, timestamp,
 type. Rob references this; old chat doesn't need it but receiving it is harmless.]

════════════════════════════════════════════════════════════════════
SECTION A — INSTRUCTIONS FOR ROB (do NOT paste this into old chat)
════════════════════════════════════════════════════════════════════

1. Open the EXISTING (OLD) browser chat for {repo} — the chat being
   wrapped up. NOT a new chat.
2. Copy from the PASTE_BOUNDARY line below to the end of this file.
3. Paste as a message in the existing chat.
4. The old chat answers the 5 pipeline questions from its lived knowledge.
5. Open the pre-created file: docs/handoffs/_in_progress/{slug}/stage2-response.md
   (already exists, has placeholder content). Replace everything below the
   "═══ REPLACE EVERYTHING BELOW THIS LINE ═══" marker with the architect's
   response. Save.
6. In Claude Code at .dev-knowledge, say: "complete handoff for {repo}"
   → Stage 3 generates the final handoff folder.
7. After Stage 3: close the old chat. Open a NEW claude.ai chat for {repo}
   and use the Stage 3 folder bundle (00_README.md inside has upload
   instructions for the new chat).

════════════════════════════════════════════════════════════════════
PASTE_BOUNDARY — copy from here to end of file into the old chat
════════════════════════════════════════════════════════════════════

# Stage 2 — Answer These Questions: {repo} ({type})

## Your role

You are the existing browser chat for **{repo}**, currently being wrapped up
because your context is getting full. Claude Code in `.dev-knowledge` is
preserving your accumulated knowledge as a structured handoff before this
chat closes.

Your role for this Stage 2 response: **project-level architect for {repo}**.
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
- Audit report (raw findings)
- Repo state snapshot (HEAD, branch, file tree, working tree state)

You do NOT need to:
- Explain what ADR-NN mandates (handoff has the essence)
- Restate audit findings verbatim (handoff has audit-report.md)
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
- "The config/settings.yaml was modified during our session when we
  changed provider timeouts" → witnessed, state confidently
- "The tier is probably M based on perceived complexity" →
  inference, write "(architect inference)" after the claim
- "I don't know the exact test count — verify against repo" → unknown

LLMs default to "be helpful" by filling gaps with plausible specifics.
Resist this. Stage 3 verifies factual claims against the repo. Your
value is judgment and reasoning, not confident fabrication of facts
you didn't witness.

If you don't know something specific (a commit message, a file name, a
version number, a config value): say "Unknown — Stage 3 should verify."

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

**Allowed within sections:** paragraphs, bullet lists, numbered lists,
**bold**, *italic*, `inline code`, code blocks, tables, blockquotes.

**NOT allowed:**
- Wrapping ENTIRE response in code fence (no opening ` ```markdown `
  or ` ``` ` at the very start; no closing ` ``` ` at the very end)

**Example correct opening:**

```
### 1. OBJECTIVE
The next session should...
```

Also acceptable (both survive copy-paste):
```
### **1. OBJECTIVE**
The next session should...
```

Also acceptable (plain text, fully copy-paste proof):
```
1. OBJECTIVE
The next session should...
```

**Example WRONG opening (do not do this):**

```
Here's my structured response:

```markdown
### 1. OBJECTIVE
```

## Current state (verified at Stage 1 by Claude Code)

- HEAD: {head_sha}
- Branch: {branch}
- Working tree: {working_tree_state}
- Recent context: {recent_commits_or_work_summary}

## Audit context (informational — extend or correct in your response)

{audit_findings_summary_if_audit_sync}

## .dev-knowledge BACKLOG items relevant to {repo}

{relevant_backlog_items}

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

What is the immediate goal of the next {repo} session?

{customized_objective_prompt}

*Epistemic note: state your goal judgment confidently. If audit's suggested
actions feel wrong to you, say so with reasoning.*

### 2. REALITY

What is the current state of {repo} from your perspective?

- Was anything completed since {last_known_milestone}?
- Any work in progress not reflected externally?
- External dependencies (services, libraries, partner repos) currently in play?
- Any constraints (deadlines, conventions) the next session must respect?
- {any_specific_state_question_from_stage1_observation}?

*Epistemic note: differentiate witnessed events (you saw this in conversation)
from inferences (reasoning from context) from unknowns (no direct knowledge).
Mark inferences with "(architect inference)" and unknowns with "Unknown —
verify against repo."*

### 3. RATIONALE

What approaches were considered and discarded for {repo} recently?

{customized_rationale_prompt_with_repo_specific_decisions}

*Epistemic note: reasoning is your strong suit — explain your judgment. For
any specific facts in your reasoning (file counts, timing, component names),
mark "(architect inference)" if not directly witnessed.*

### 4. DIRECTIVES

What are the exact sequential actions the next {repo} session should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

{default_proposal_from_audit_or_session_goals}

Add, remove, or reorder as you see fit.

*Epistemic note: action sequence and verification steps are most valuable.
Specific file paths or commit messages — mark "(architect inference)" if not
witnessed; Stage 3 may revise based on repo state.*

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

{default_boundaries_from_audit_deferrals_and_general_scope}

Add any architect-specific concerns or "do not's."

*Epistemic note: do-not lists grounded in your project knowledge are very
valuable. Don't fabricate "do not touch X" if you don't know whether X exists
— focus on knowns from your conversation.*

════════════════════════════════════════════════════════════════════
End of paste block.
Old chat: please answer questions 1-5 above following the Format
requirements above. Structure response with the exact headings
(OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES) so
Claude Code can parse them at Stage 3.
════════════════════════════════════════════════════════════════════
```

---

## Generation rules for Claude Code

- Replace all `{placeholders}` with actual values from repo state + audit context
- **Section B order is fixed:** role → bundle → epistemic → format → current state
  → audit context → BACKLOG → pipeline questions → end divider.
  Role/bundle/epistemic/format MUST appear before audit context and questions —
  old chat must read these BEFORE drafting response.
- **Preserve 5 question headings exactly:** `### 1. OBJECTIVE`, `### 2. REALITY`,
  `### 3. RATIONALE`, `### 4. DIRECTIVES`, `### 5. BOUNDARIES`. Stage 3 parses these.
- Section A and Section B separated by visible `PASTE_BOUNDARY` line with thick `═`
  characters — visually unmistakable even when scrolling
- **DO NOT include receiver synthesis prompt** in stage1-question.md. It belongs
  in Stage 3 output (`00_first-message.md`, per HANDOFF_FOLDER_TEMPLATE)
- Metadata header (HEAD, branch, working tree) goes ABOVE Section A
- For audit-sync: populate `{audit_findings_summary}` with categorized findings;
  customize question prompts with audit-suggested defaults labeled "revise as needed"
- For session-sync: populate from recent git log + BACKLOG context
- **Pre-create `stage2-response.md` template** alongside stage1-question.md in the
  same Stage 1 commit (per HANDOFF_PROCESS Stage 1 procedure)
