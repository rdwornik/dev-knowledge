# Handoff Stage 1: ai-council (session-sync)

**Slug:** 2026-05-18-ai-council-session-sync
**Type:** session-sync
**Generated:** 2026-05-18
**Target repo:** ai-council (`C:\Users\1028120\Documents\Dev\ai-council`)
**HEAD SHA:** ce885827aada41f582e784fa210f73ff125a18de
**Branch:** main
**Working tree:** clean

════════════════════════════════════════════════════════════════════
SECTION A — INSTRUCTIONS FOR ROB (do NOT paste this into old chat)
════════════════════════════════════════════════════════════════════

1. Open the EXISTING (OLD) browser chat for ai-council — the chat being
   wrapped up. NOT a new chat.
2. Copy from the PASTE_BOUNDARY line below to the end of this file.
3. Paste as a message in the existing chat.
4. The old chat answers the 5 pipeline questions from its lived knowledge.
5. Open the pre-created file:
   docs/handoffs/_in_progress/2026-05-18-ai-council-session-sync/stage2-response.md
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
- Repo state snapshot (HEAD, branch, file tree, working tree state)

You do NOT need to:
- Explain what ADR-NN mandates (handoff has the essence)
- Specify HEAD SHA or working tree state (handoff has manifest)
- Describe ecosystem governance patterns (handoff has VISION + PLAYBOOK)

Focus on what only YOU witnessed or judged in this conversation.

## How to write the response (read before drafting)

Four concerns govern your response. Apply them during drafting, not as a
final-pass edit — the failure modes below are pattern-matched in an LLM's
natural output under session saturation, so fighting them after drafting
is harder than avoiding them up front.

### 1. Epistemic honesty

For each claim, classify it using these markers:

- **Witnessed**: you saw this happen in conversation — state it confidently
- **(architect inference)**: you are reasoning from context, not direct
  observation — mark it inline
- **Unknown**: you don't have direct knowledge — say so explicitly

Examples:
- "We raised the Perplexity timeout to 240s during our session" → witnessed, state confidently
- "The test count is probably around 50" → inference, write "(architect inference)" after
- "I don't know the current config value — verify against repo" → unknown

LLMs default to "be helpful" by filling gaps with plausible specifics.
Resist this. Stage 3 verifies factual claims against the repo. Your
value is judgment and reasoning, not confident fabrication of facts
you didn't witness.

If you don't know something specific (a commit message, a file name, a
version number, a config value): say "Unknown — Stage 3 should verify."

### 2. Self-containment for a bundle-only audience

**Principle:** the new chat sees ONLY the Stage 3 bundle. It does not see
this Stage 1 question, prior browser conversations, JOURNAL entries, or
external research. Every claim in your response must be comprehensible
from the bundle alone.

The bundle contains: full `.dev-knowledge` VISION.md, PLAYBOOK.md, and
ESSENTIALS.md; ADR essences for ADRs cited in directives; the repo state snapshot.

Apply these rules in every section of your response:

- **Per-section scope declaration.** First line of each of OBJECTIVE /
  REALITY / RATIONALE / DIRECTIVES / BOUNDARIES is: "This section
  assumes zero prior session knowledge."

- **No references the new chat cannot resolve.** No mentions of Stage 1
  ("Stage 1 Q1 framing", "the question above"), no session-internal
  terms. Generalize to "during a recent extended session" or "in the
  work culminating in commit X".

- **List items inline at first mention.** No forward-references. List
  items where first mentioned; provide representative state, not an
  exhaustive log.

- **Inline a 1-sentence summary only for files NOT already in the
  bundle.** Files already in the bundle need no inline summary — the
  new chat will read them.

- **No external citations not in the bundle.** Paper titles, blog posts,
  arxiv IDs — none are in the bundle and the new chat cannot verify them.

- **Write about the work, not the meta-process of handing it off.**

**Audience-simulation check (do this before submitting):** mentally
simulate a fresh LLM session reading ONLY the Stage 3 bundle. For each
paragraph of your response, ask: would this be comprehensible without
reaching for external context? If any paragraph fails, rewrite it.
Cross-repo content fails this check — default expectation is zero cross-repo
content; only unclosed threads that genuinely could not close belong in
REALITY, framed as "unclosed thread, awareness only"; DIRECTIVES never
target other repos.

### 3. Coherence check

Before submitting, verify: no DIRECTIVE violates own BOUNDARIES; the
OBJECTIVE's top priority aligns with DIRECTIVE #1; no directive depends
on data not packaged in the bundle. Revise before submitting if any fails.

### 4. Format requirements

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

## Current state (verified at Stage 1 by Claude Code)

- **HEAD:** ce885827aada41f582e784fa210f73ff125a18de
- **Branch:** main
- **Working tree:** clean
- **Recent commits:**
  - `ce88582` Merge branch 'docs/question-guide-naming-convention'
  - `fe9cd0a` docs: add brief-file naming convention to council-question-guide
  - `dc10020` Merge branch 'fix/perplexity-research-timeout'
  - `d72c2aa` test: assert timeout invariant (>=120s), not literal value
  - `3af2ed9` fix(research): raise Perplexity timeout to 240s and add SDK transient retry
  - `9c755e6` test: red tests for Perplexity timeout and retry hardening
  - `be58c36` Merge fix/claude-provider-400-and-research-gating
  - `a05719c` fix(cli): scope provider health gate to the active mode
  - `5d5365f` fix(healthcheck): classify billing exhaustion as a distinct error category
  - `f57e716` test: red tests for billing classifier and mode-scoped health gate

## .dev-knowledge BACKLOG items relevant to ai-council

**Stream B (ai-council-specific):**
- [P2] [open] **ai-council needs AGENTS.md** — missing cross-tool canonical
  governance file; `ai-council` has `CLAUDE.md` but no `AGENTS.md` (verified
  2026-05-11). Drift signal: cross-tool LLM agents (Codex, Cursor, Aider)
  operating on incomplete repo context.
- [P3] [open] **ai-council LESSONS.md scope-tag backfill** — entries missing
  `[scope: X]` tags per ADR-46 6-field schema; produces advisory WARN on audit.

**Hyphen Convention Migration Sequence:**
- [P2] [open] **ai-council hyphen migration + ADR-38 compliance** — verify
  hyphen filename compliance (likely low impact per prior audit), confirm
  ARCHITECTURE.md placement per ADR-38 Scale M (optional at M — check current
  state).

**Cross-stream (ai-council portion):**
- [P2] [open] Phase 2 universalization rollout — ai-council substantially
  complete as of 2026-05-12. Remaining: AGENTS.md (P3), ARCHITECTURE.md
  optional at M.

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

What is the immediate goal of the next ai-council session?

Based on the recent work (Perplexity timeout hardening, Claude billing
classifier, mode-scoped health gate, council-question-guide naming
convention), what is the single most important thing for the next session
to accomplish? Is the focus on further provider reliability hardening,
new feature development, documentation/governance gaps (AGENTS.md,
LESSONS.md scope-tag backfill), or something else entirely that emerged
from this session's work?

*Epistemic note: state your goal judgment confidently. If recent bug fixes
shifted priorities from what was planned, describe that shift.*

### 2. REALITY

What is the current state of ai-council from your perspective?

- What was completed in this session — which fixes, features, or docs
  changes did you witness land?
- Is any work in progress that hasn't landed in a commit yet?
- Are there unstable areas you're aware of — flaky tests, provider
  reliability concerns beyond what was just fixed, deprecation risks?
- What external dependencies (Perplexity, Claude API, other providers)
  are currently in play, and are any causing reliability concerns?
- Are there any constraints (rate limits, billing conditions, API key
  state) the next session must be aware of?

*Epistemic note: differentiate witnessed events from inferences from
unknowns. Mark inferences with "(architect inference)" and unknowns with
"Unknown — verify against repo."*

### 3. RATIONALE

If you witnessed reasoning that shaped recent ai-council work and the
next session needs to understand it, describe it. If not, write "Unknown —
no specific rationale witnessed in this session" and skip the sub-questions
below.

- If you witnessed the reasoning behind how billing exhaustion was classified
  as a distinct error category (rather than a generic error), state it;
  otherwise mark Unknown — Stage 3 verifies against the commit.
- If you witnessed the reasoning behind why the provider health gate was
  scoped to the active mode rather than globally, state it; otherwise mark
  Unknown — Stage 3 verifies against the commit.
- If you witnessed reasoning behind the Perplexity timeout threshold choice
  (240s), state it; otherwise mark Unknown — Stage 3 verifies against the
  commit.

*Epistemic note: reasoning is your strong suit — explain your judgment when
you witnessed it. For any sub-question, "Unknown — Stage 3 verifies against
the commit / ADR" is acceptable and preferred over a constructed rationale.*

### 4. DIRECTIVES

What are the exact sequential actions the next ai-council session should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

Suggested defaults from BACKLOG (revise as needed):
1. Add `AGENTS.md` to ai-council root — populate with cross-tool canonical
   governance content; verify it does not duplicate CLAUDE.md (additive or
   canonical replacement); verify `pre-commit run --all-files` passes.
2. Backfill `[scope: X]` tags in ai-council `LESSONS.md` entries — verify
   ADR-46 dated-entry audit check passes (WARN resolves to clean).
3. Verify hyphen filename compliance across ai-council — run check; migrate
   any non-compliant filenames; confirm ARCHITECTURE.md placement.
4. Update JOURNAL with session summary.

Add, remove, or reorder based on what you actually witnessed in this session.

*Epistemic note: action sequence and verification steps are most valuable.
Specific file paths — mark "(architect inference)" if not witnessed directly;
Stage 3 may revise based on repo state.*

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

Suggested defaults (revise as needed):
- Do NOT modify provider timeout values or retry logic without understanding
  the empirical basis for current values — they were just hardened this
  session.
- Do NOT refactor the billing classifier or health gate logic without
  reviewing the test coverage established in this session.
- Do NOT create duplicate governance between `AGENTS.md` and `CLAUDE.md` —
  AGENTS.md must be additive or serve as canonical replacement for
  cross-tool sections; do not copy-paste CLAUDE.md content verbatim.

Add any architect-specific concerns or "do not's" from your project knowledge.

*Epistemic note: do-not lists grounded in your project knowledge are very
valuable. Don't fabricate "do not touch X" if you don't know whether X
exists — focus on knowns from your conversation.*

════════════════════════════════════════════════════════════════════
End of paste block.
Old chat: please answer questions 1-5 above following the Format
requirements above. Structure response with the exact headings
(OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES) so
Claude Code can parse them at Stage 3.
════════════════════════════════════════════════════════════════════
