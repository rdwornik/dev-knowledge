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

**Note on receiver synthesis prompt:** The synthesis prompt (new chat must
paraphrase understanding before acting) belongs in `00_first-message.md` —
a Stage 3 output. It is NOT included in stage1-question.md. The OLD chat
answers questions; it does not synthesize before responding.

**Three-actor flow (per ADR-42, twice amended):**
- Stage 2 source = OLD browser chat for {repo} (existing chat being wrapped up)
- Stage 3 receiver = NEW browser chat for {repo} (fresh, opened after folder generated)
- Claude Code = orchestrator throughout

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
5. Open the pre-created file: `docs/handoffs/_in_progress/{slug}/stage2-response.md`
   (Stage 1 created it alongside this file — already exists, has placeholder content).
   Replace everything below the `═══ REPLACE EVERYTHING BELOW THIS LINE ═══` marker
   with the architect's response. Save.
6. In Claude Code at .dev-knowledge, say: "complete handoff for {repo}"
   → Stage 3 generates the final handoff folder.
7. After Stage 3: close the old chat. Open a NEW claude.ai chat for {repo}
   and use the Stage 3 folder bundle (00_README.md inside has upload
   instructions for the new chat).

════════════════════════════════════════════════════════════════════
PASTE_BOUNDARY — copy from here to end of file into the old chat
════════════════════════════════════════════════════════════════════

# Stage 2 — Answer These Questions: {repo} ({type})

You are the EXISTING browser chat for **{repo}**, currently being wrapped up
because your context is getting full. Claude Code in `.dev-knowledge` is
preserving your accumulated knowledge as a structured handoff before this
chat closes.

Your tacit knowledge — current priorities, mental model, in-flight decisions,
recent concerns — is non-substitutable. `.dev-knowledge`'s audit findings
(below, if applicable) provide an external view; your response provides the
internal view that only you have.

The handoff bundle generated from your response will be uploaded to a NEW
(fresh) browser chat that continues work on {repo}. That new chat has zero
history — your structured response here is what it will have.

The next session will focus on: {session_goal}.

## Current state (verified at Stage 1)

- HEAD: {head_sha}
- Branch: {branch}
- Working tree: {working_tree_state}
- Recent context: {recent_commits_or_work_summary}

## Audit context (informational — extend or correct in your response)

{audit_findings_summary_if_audit_sync}

## .dev-knowledge BACKLOG items relevant to {repo}

{relevant_backlog_items}

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings so Claude Code can
parse them at Stage 3:

### 1. OBJECTIVE

What is the immediate goal of the next {repo} session?

{customized_objective_prompt}

What outcome should be achieved by end of session — what does "done" look like?

### 2. REALITY

What is the current state of {repo} from your perspective?

- Was anything completed since {last_known_milestone}?
- Any work in progress not reflected externally?
- External dependencies (services, libraries, partner repos) currently in play?
- Any constraints (deadlines, conventions) the next session must respect?
- {any_specific_state_question_from_stage1_observation}?

### 3. RATIONALE

What approaches were considered and discarded for {repo} recently?

{customized_rationale_prompt_with_repo_specific_decisions}

### 4. DIRECTIVES

What are the exact sequential actions the next {repo} session should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

{default_proposal_from_audit_or_session_goals}

Add, remove, or reorder as you see fit.

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

{default_boundaries_from_audit_deferrals_and_general_scope}

Add any architect-specific concerns or "do not's."

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
requirements above. Your response goes back to Claude Code
(.dev-knowledge) which generates the final handoff folder.
════════════════════════════════════════════════════════════════════
```

---

## Generation rules for Claude Code

- Replace all `{placeholders}` with actual values from repo state + audit context
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
  same Stage 1 commit (per HANDOFF_PROCESS Stage 1 procedure step 9)
