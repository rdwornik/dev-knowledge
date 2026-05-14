# Handoff Stage 1: ai-council (session-sync)

<!-- scope: meta -->

**Metadata**

| Field | Value |
|---|---|
| Repo | `C:\Users\1028120\Documents\Dev\ai-council` |
| HEAD SHA | `0f069554b894802504aa4e5ce140b1d481ae9ec8` |
| Branch | `main` |
| Working tree | clean |
| Slug | `2026-05-14-ai-council-session-sync` |
| Timestamp | 2026-05-14 |
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
5. Open the pre-created file: `docs/handoffs/_in_progress/2026-05-14-ai-council-session-sync/stage2-response.md`
   (already exists, has placeholder content). Replace everything below the
   `═══ REPLACE EVERYTHING BELOW THIS LINE ═══` marker with the architect's
   response. Save.
6. In Claude Code at `.dev-knowledge`, say: "complete handoff for ai-council"
   → Stage 3 generates the final handoff folder.
7. After Stage 3: close the old chat. Open a NEW claude.ai chat for ai-council
   and use the Stage 3 folder bundle (`00_README.md` inside has upload
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
- Describe ecosystem governance patterns (handoff has VISION + PLAYBOOK)
- Specify HEAD SHA or working tree state (handoff has manifest)

Focus on what only YOU witnessed or judged in this conversation.

## Epistemic honesty (CRITICAL)

For each claim in your response, classify it using these markers:

- **Witnessed**: you saw this happen in conversation — state it confidently
- **(architect inference)**: you are reasoning from context, not direct
  observation — mark it inline
- **Unknown**: you don't have direct knowledge — say so explicitly

Examples:
- "The routing.py TargetResolver was implemented during our session" → witnessed, state confidently
- "The test count is probably around 360" → inference, write "(architect inference)" after the claim
- "I don't know the exact config key name — verify against repo" → unknown

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
   - NOT: "Round 1 → 2 → 3 file loads", "today's v3.3 prompt",
     "the empirical test of v3.3 begins with this handoff cycle"
   - DO: "during a recent extended session", "in the work culminating
     in commit X"

4. **List items inline at first mention.** Do NOT forward-reference.
   - NOT: "drive session-lessons capture (5 primary + 3 secondary lessons,
     see REALITY for list)" then list them later
   - DO: list the items where first mentioned, or omit the count if the
     list is too long for inline

5. **Self-contained claims.** If a claim requires reading another repo
   file (ADR, audit) to understand, inline a 1-sentence summary of that
   file's relevant content at first reference.

6. **No external research citations not in the bundle.** Paper titles,
   blog posts, arxiv IDs, vendor blogs — strip from the response.
   Concepts can be stated as reasoning; citations cannot.

7. **No self-referential meta-framing.** Do NOT describe the new chat
   as "the test subject" or describe the handoff being "an empirical
   test" unless that framing serves a receiver-side action.

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
- Wrapping ENTIRE response in code fence

## Current state (verified at Stage 1 by Claude Code)

- HEAD: `0f069554b894802504aa4e5ce140b1d481ae9ec8`
- Branch: `main`
- Working tree: clean
- Recent commits:
  - `0f06955` docs(journal): record 2026-05-13 ADR-34 timestamp case captured to BACKLOG
  - `5baf88d` Merge branch 'docs/2026-05-13-backlog-timestamp-adr-34'
  - `9de640e` docs(backlog): capture P3 ADR-34 timestamp-underscore case in council-out emitter
  - `f094d08` docs(audit): codex review for audit-addendum-i7-i8
  - `baeb6bc` docs: CHANGELOG + JOURNAL for scrum-master addendum (I7 + I8)
  - `7fb45b0` docs(backlog,lessons): BACKLOG M2 supersession sync + architect local-config-defense lesson
  - `2986ac0` chore(handoffs): I8 rename _archive → archive (align to A2 operator decision)
  - `5346045` fix(review): codex medium/low — grok_research in README, panel defaults in guide, docs/ folder governance, rubric provenance

## .dev-knowledge BACKLOG items relevant to ai-council

**Stream B — open items:**

- **[P2][open] ai-council needs AGENTS.md** — PLAYBOOK governance gap.
  PLAYBOOK requires each repo to have `AGENTS.md` at root for cross-tool
  LLM governance (Codex, Cursor, Aider). `ai-council` has `CLAUDE.md` but
  no `AGENTS.md` (verified 2026-05-11). Work belongs in ai-council repo.

**Cross-stream — open items relevant to ai-council:**

- **[P2][open] Phase 2 universalization rollout** — ai-council substantially
  complete as of 2026-05-12: ADR-34 hyphen compliance achieved (CLI emitter +
  docs), ADR-38 Scale M gaps closed (BACKLOG.md, LESSONS.md at root, tasks/
  retired), VISION.md tier M declared, scrum-master review cycle N=1 completed.
  Remaining: AGENTS.md (P3), ARCHITECTURE.md (optional at M).

- **[P2][open] Handoff folder format adoption** — `ai-council` still has
  flat `docs/HANDOFF.md` (pre-ADR-42 pattern). Migration options: convert to
  folder format at next handoff event, or explicitly deprecate. Tied to A4
  decision.

- **[P3][open] docs/HANDOFF.md flat file deprecation** — retire at next
  handoff event or explicitly designate as legacy. Tied to A4 decision.

- **[P2][open] ai-council hyphen migration + ADR-38 compliance** — (1)
  Verify universal hyphen filename compliance (likely low-impact); (2)
  ADR-38 Scale M: ARCHITECTURE.md to root, verify LESSONS.md and BACKLOG.md
  already present.

- **[P3][open] A5 Phase 2: retire UPPERCASE TYPE tag in legacy archive
  filenames** — opportunistic during Phase 2 visits; rename
  `YYYY-MM-DD_TYPE_topic.md` patterns in `docs/archive/` to
  `YYYY-MM-DD-topic.md`.

- **[P2][open] VISION.md tier declarations across ecosystem** — ai-council
  tier M already declared. Other repos pending.

- **[P2][open] Codify scrum-master review authority pattern** — N=1
  (ai-council 2026-05-12). Codification awaits N=2 empirical grounding.

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

What is the immediate goal of the next ai-council session?

Consider: The BACKLOG shows Phase 2 universalization substantially complete
for ai-council. Remaining open items: AGENTS.md (P2), hyphen migration
verification, ARCHITECTURE.md (optional at M), HANDOFF.md deprecation (A4).
What is the right focus for the next session — close outstanding P2 items,
or shift to Phase 2 for corp-monorepo, or something else?

*Epistemic note: state your goal judgment confidently. If the suggested
actions feel wrong to you, say so with reasoning.*

### 2. REALITY

What is the current state of ai-council from your perspective?

- What was the most recent work completed in this session?
- Any work in progress not reflected in the commit log above?
- What's the state of the CLI (routing, emitter, test suite)?
- External dependencies or partner repos currently in play?
- Any constraints (conventions, scope limits) the next session must respect?

*Epistemic note: differentiate witnessed events from inferences from unknowns.
Mark inferences with "(architect inference)" and unknowns with "Unknown —
verify against repo."*

### 3. RATIONALE

What approaches were considered and discarded in recent ai-council work?

- What drove the ADR-34 timestamp-underscore P3 capture (last commit)?
- Were there any priority calls made — items deferred, items accelerated?
- Any architectural decisions (scrum-master review pattern, routing design,
  BACKLOG structure) where you have reasoning that isn't visible in the
  commit messages?

*Epistemic note: reasoning is your strong suit. For specific facts in your
reasoning (file counts, timing, component names), mark "(architect inference)"
if not directly witnessed.*

### 4. DIRECTIVES

What are the exact sequential actions the next ai-council session should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

Default proposal from BACKLOG (revise as you see fit):
1. Verify ADR-38 Scale M compliance: confirm BACKLOG.md, LESSONS.md, ARCHITECTURE.md
   (if needed) are present at root. Verify: `git ls-files | grep -E '^(BACKLOG|LESSONS|ARCHITECTURE)\.md'`
2. Add AGENTS.md at root per PLAYBOOK governance standard.
   Verify: file exists, references CLAUDE.md, covers Codex/Cursor/Aider.
3. Verify hyphen-only filename compliance across docs/ and output/.
   Verify: any remaining underscore-separated filenames flagged.
4. Decide A4: convert docs/HANDOFF.md to folder format or deprecate explicitly.
   Verify: decision recorded in BACKLOG.md or ADR.
5. Opportunistically rename UPPERCASE TYPE tag in legacy archive filenames (A5).

Add, remove, or reorder as you see fit.

*Epistemic note: action sequence and verification steps are most valuable.
Specific file paths — mark "(architect inference)" if not witnessed; Stage 3
may revise based on repo state.*

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

Default boundaries from BACKLOG scope limits:
- Do NOT make changes to `.dev-knowledge` files from within ai-council session
  (cross-repo writes violate ADR-36 read-only contract)
- Do NOT start corp-monorepo work in this session — that is a separate Phase 2
  visit after ai-council gaps are closed
- Do NOT codify scrum-master review ADR until N=2 empirical data exists
- Do NOT generate reconciliation reports about other repos' state

Add any architect-specific concerns or "do not's" from your session knowledge.

*Epistemic note: do-not lists grounded in your project knowledge are very
valuable. Don't fabricate "do not touch X" if you don't know whether X exists.*

---

## Before submitting your response, also verify

- **Any cross-repo content?** Default expectation is zero cross-repo content.
  Only unclosed threads that genuinely could not close belong in REALITY,
  framed as "unclosed thread, awareness only." DIRECTIVES never target other repos.
- **Internal coherence?** No DIRECTIVE violates own BOUNDARIES; OBJECTIVE-stated
  highest priority aligned with DIRECTIVE #1; no directive depends on data not
  packaged in bundle.
- **Audience awareness check:** Mentally simulate a fresh LLM session reading
  ONLY the Stage 3 bundle (no Stage 1, no JOURNAL, no prior chats). For each
  paragraph, ask: would this be comprehensible without external context?
  If any paragraph fails, rewrite to be self-contained per the 7 rules above.

════════════════════════════════════════════════════════════════════
End of paste block.
Old chat: please answer questions 1-5 above following the Format
requirements above. Structure response with the exact headings
(OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES) so
Claude Code can parse them at Stage 3.
════════════════════════════════════════════════════════════════════
