# Handoff Stage 1: ai-council (session-sync)

<!-- scope: meta -->

| Field | Value |
|---|---|
| Repo | ai-council (`C:\Users\1028120\Documents\Dev\ai-council`) |
| HEAD SHA | `1bcc6abae464d1455a8cec7fd0eb7cd512e43fd8` |
| Branch | `main` |
| Working tree | clean |
| Slug | `2026-05-17-ai-council-session-sync` |
| Timestamp | 2026-05-17 |
| Type | session-sync |

---

════════════════════════════════════════════════════════════════════
SECTION A — INSTRUCTIONS FOR ROB (do NOT paste this into old chat)
════════════════════════════════════════════════════════════════════

1. Open the EXISTING (OLD) browser chat for **ai-council** — the chat being
   wrapped up. NOT a new chat.
2. Copy from the PASTE_BOUNDARY line below to the end of this file.
3. Paste as a message in the existing chat.
4. The old chat answers the 5 pipeline questions from its lived knowledge.
5. Open the pre-created file:
   `docs/handoffs/_in_progress/2026-05-17-ai-council-session-sync/stage2-response.md`
   (already exists, has placeholder content). Replace everything below the
   `═══ REPLACE EVERYTHING BELOW THIS LINE ═══` marker with the architect's
   response. Save.
6. In Claude Code at .dev-knowledge, say: `"complete handoff for ai-council"`
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
- Full ai-council `VISION.md` (repo-level context)
- Full `.dev-knowledge` `VISION.md` (ecosystem context, 02b file)
- Full `.dev-knowledge` `PLAYBOOK.md` (methodology, conversation style,
  prompt format, commit conventions)
- Full `.dev-knowledge` `ESSENTIALS.md` (high-leverage rules)
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

## Audience awareness (CRITICAL — read before responding)

Your response will be processed by Stage 3 into the new chat's bundle. The
new chat sees ONLY the Stage 3 bundle — it does NOT see this Stage 1
question, does NOT see prior browser conversations, does NOT see JOURNAL
entries unless explicitly included in the bundle, does NOT see external
research papers or links.

Write Stage 2 for the new chat's audience, not for the operator's audience
or your own session memory.

**Rules (all 7 apply to every section of your response):**

1. **Open each major section with a scope declaration.** First line of
   each of OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES is:
   "This section assumes zero prior session knowledge."

2. **No references to Stage 1 itself.** Do NOT write phrases like
   "Stage 1 Q1 framing", "Stage 1 metadata says", "the question above".
   Stage 1 is not in the bundle.

3. **No invisible session-history references.** Do NOT reference
   session-internal terms the new chat will not understand. Generalize:
   - NOT: "today's docs-simplification-rollout session", "the ADR-48/49 branch"
   - DO: "during a recent session", "in the work culminating in commit 1bcc6ab"

4. **List items inline at first mention.** Do NOT forward-reference.
   - NOT: "the open items (see REALITY for list)" then list them later
   - DO: list the items where first mentioned, or omit the count if the
     list is too long for inline

5. **Self-contained claims.** If a claim requires reading another repo
   file (ADR, audit) to understand, inline a 1-sentence summary of that
   file's relevant content at first reference.

6. **No external research citations not in the bundle.** Strip from the response.
   Concepts can be stated as reasoning; citations cannot.

7. **No self-referential meta-framing.** Write about the work to be done,
   not about the meta-process of handing it off.

Apply these rules during drafting, not as a final-pass edit.

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

Also acceptable (plain text, fully copy-paste proof):
```
1. OBJECTIVE
The next session should...
```

## Current state (verified at Stage 1 by Claude Code)

- HEAD: `1bcc6abae464d1455a8cec7fd0eb7cd512e43fd8`
- Branch: `main`
- Working tree: clean
- Recent commits (most recent first):
  - `1bcc6ab` — `chore(docs): remove orphan docs/handoffs — handoffs centralized in .dev-knowledge per ADR-42`
  - `f2dc586` — `merge: docs-simplification-rollout into main`
  - `f602f62` — `docs(journal): 2026-05-17 docs-simplification-rollout session entry`
  - `17d6faf` — `docs(council): add transcript-to-ADR step to the council workflow`
  - `40fa323` — `docs(conventions): adopt simplified documentation conventions per ADR-48/49`
  - `79bb051` — `feat(scripts): add deterministic header normalizer + pre-commit hook`
  - `8544a5f` — `chore(docs): remove CHANGELOG and BACKLOG_ARCHIVE per ADR-49`
  - `e91a1e4` — `docs(lessons): remove superseded 2026-02-21 foundation entries [cleanup]`

## .dev-knowledge BACKLOG items relevant to ai-council

**Stream B (ai-council):**

- **[P2] ai-council needs AGENTS.md** — PLAYBOOK mandates AGENTS.md at root for
  cross-tool governance (Codex, Cursor, Aider). ai-council has only CLAUDE.md
  (Claude-Code-specific). Missing AGENTS.md = drift from ecosystem standard per
  Council #28. Work belongs in ai-council repo.

- **[P3] ai-council LESSONS.md scope-tag backfill** — ADR-46 §LESSONS.md
  specifies `[scope: X]` substring in 6-field entries; absence produces WARN on
  `dated_entries_lessons` check. Advisory (WARN not FAIL) but constitutes
  methodology drift. Work belongs in ai-council repo.

**Cross-stream items with ai-council work:**

- **[P2] ai-council hyphen migration + ADR-38 compliance** — Confirm hyphen
  compliance (likely already mostly compliant; verify before declaring clean).
  ADR-38 Scale M gaps: ARCHITECTURE.md to root, add LESSONS.md, BACKLOG.md
  (AGENTS.md tracked separately above).

- **[P2] Handoff folder format adoption** — ai-council may still have a legacy
  `docs/HANDOFF.md` (pre-ADR-42 flat pattern). Migrate or explicitly deprecate.
  Tied to A4 decision (separate ADR or conversational) about whether flat file
  is still acceptable as legacy.

- **[P3] docs/HANDOFF.md flat file deprecation** — both corp-monorepo and
  ai-council have pre-ADR-42 flat HANDOFF.md files. Retire at next handoff event
  or explicitly designate as legacy.

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

What is the immediate goal of the next ai-council session?

The most recent session (commits around `f2dc586`) adopted simplified
documentation conventions (ADR-48/49): removed CHANGELOG, removed BACKLOG_ARCHIVE,
added deterministic header normalizer + pre-commit hook, adopted new doc conventions.

Given that cleanup, what should the next session accomplish? Candidates from BACKLOG:
AGENTS.md creation (P2), ADR-38 compliance gap closure, or continuing Council debate
work. Propose and justify the top priority.

*Epistemic note: state your goal judgment confidently. If the BACKLOG priority
ranking feels wrong for what's actually needed in ai-council right now, say so
with reasoning.*

### 2. REALITY

What is the current state of ai-council from your perspective?

- What was completed in the most recent session (docs-simplification-rollout)?
- Anything incomplete or partially applied that the next session should be aware of?
- Any in-flight Council debates or architectural decisions not yet captured?
- Any technical debt or known issues introduced during the simplification work?
- Does the deterministic header normalizer pre-commit hook work cleanly on the
  current repo state?
- Is LESSONS.md currently in correct reverse-chrono order per ADR-46?

*Epistemic note: differentiate witnessed events from inferences from unknowns.
Mark inferences with "(architect inference)" and unknowns with "Unknown — verify
against repo."*

### 3. RATIONALE

What approaches were considered and discarded for ai-council recently?

- Were any ADR-48/49 simplification decisions contested or deferred?
- Why was ARCHITECTURE.md not included in the simplification scope (if it wasn't)?
- Were any LESSONS.md scope-tag decisions made — adopt them or skip them?
- Why AGENTS.md was deferred rather than created in the docs-simplification session
  (if it was deferred)?

*Epistemic note: reasoning is your strong suit — explain your judgment. For
specific facts, mark "(architect inference)" if not directly witnessed.*

### 4. DIRECTIVES

What are the exact sequential actions the next ai-council session should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

Suggested starting proposals (revise as you see fit):
1. Create `AGENTS.md` at ai-council repo root per ecosystem governance standard (Council #28). Verify: file exists at root, covers Codex/Cursor/Aider/Claude Code.
2. Verify header normalizer pre-commit hook runs clean on current repo state. Verify: `pre-commit run --all-files` exits 0.
3. Close ADR-38 Scale M gaps: move or confirm ARCHITECTURE.md at root; verify LESSONS.md + BACKLOG.md at root. Verify: file locations match ADR-38 mandate for Scale M.
4. Backfill `[scope: X]` tags in LESSONS.md entries (ADR-46 advisory). Verify: `dated_entries_lessons` check passes.
5. Deprecate or migrate legacy `docs/HANDOFF.md` if still present. Verify: file removed or explicitly marked legacy.

Adjust priority, sequence, or content to reflect what you actually know from this session.

*Epistemic note: action sequence and verification steps are most valuable.
Specific file paths — mark "(architect inference)" if not witnessed; Stage 3
will revise based on repo state.*

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

Suggested boundaries (revise as you see fit):
- Do NOT generate reconciliation reports about other repos' state. Do NOT treat
  staleness observations about another repo's tracking artifacts as a directive.
- Do NOT amend ADR-48 or ADR-49 without a dedicated Council debate — the
  simplification scope was deliberate; amendments require the same deliberation.
- Do NOT backfill scope tags if the LESSONS.md content is at risk of edit-entry
  corruption (ADR-29 "never edit old entries" — verify the tag is metadata-only
  before touching).
- If AGENTS.md creation requires cross-repo decisions (what tools are in scope,
  what authority AGENTS.md carries), pause and surface to operator rather than
  inventing a spec.

Add any architect-specific concerns or "do not's" you know from this conversation.

*Epistemic note: do-not lists grounded in your project knowledge are very
valuable. Don't fabricate "do not touch X" if you don't know whether X exists.*

---

## Before submitting your response, also verify

- **Any cross-repo content?** Per Universal Self-Containment Rule, default
  expectation is zero cross-repo content in handoff. Only unclosed threads
  that genuinely could not close belong in REALITY, framed as "unclosed thread,
  awareness only." DIRECTIVES never target other repos.
- **Internal coherence?** No DIRECTIVE violates own BOUNDARIES; OBJECTIVE-stated
  highest priority aligned with DIRECTIVE #1; no directive depends on data not
  packaged in bundle.
- **Audience awareness check:** Mentally simulate a fresh LLM session reading
  ONLY the Stage 3 bundle. For each paragraph: would this be comprehensible
  without external context? If not, rewrite to be self-contained per the 7 rules.

If any check fails, revise before submitting.

════════════════════════════════════════════════════════════════════
End of paste block.
Old chat: please answer questions 1-5 above following the Format
requirements above. Structure response with the exact headings
(OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES) so
Claude Code can parse them at Stage 3.
════════════════════════════════════════════════════════════════════
