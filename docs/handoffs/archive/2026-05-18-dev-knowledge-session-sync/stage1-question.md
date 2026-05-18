# Handoff Stage 1: .dev-knowledge (session-sync)

**Repo:** `.dev-knowledge`
**HEAD SHA:** `aeaf1582d68c8e2ae4ff304bf08972f6e01eec10`
**Branch:** `main`
**Working tree:** clean
**Slug:** `2026-05-18-dev-knowledge-session-sync`
**Timestamp:** 2026-05-18
**Type:** session-sync

---

════════════════════════════════════════════════════════════════════
SECTION A — INSTRUCTIONS FOR ROB (do NOT paste this into old chat)
════════════════════════════════════════════════════════════════════

1. Open the EXISTING (OLD) browser chat for `.dev-knowledge` — the chat being
   wrapped up. NOT a new chat.
2. Copy from the PASTE_BOUNDARY line below to the end of this file.
3. Paste as a message in the existing chat.
4. The old chat answers the 5 pipeline questions from its lived knowledge.
5. Open the pre-created file:
   `docs/handoffs/_in_progress/2026-05-18-dev-knowledge-session-sync/stage2-response.md`
   (already exists, has placeholder content). Replace everything below the
   "═══ REPLACE EVERYTHING BELOW THIS LINE ═══" marker with the architect's
   response. Save.
6. In Claude Code at `.dev-knowledge`, say: "complete handoff for dev-knowledge"
   → Stage 3 generates the final handoff folder.
7. After Stage 3: close the old chat. Open a NEW claude.ai chat for `.dev-knowledge`
   and use the Stage 3 folder bundle (`00_README.md` inside has upload
   instructions for the new chat).

════════════════════════════════════════════════════════════════════
PASTE_BOUNDARY — copy from here to end of file into the old chat
════════════════════════════════════════════════════════════════════

# Stage 2 — Answer These Questions: .dev-knowledge (session-sync)

## Your role

You are the existing browser chat for **`.dev-knowledge`**, currently being wrapped up
because your context is getting full. Claude Code in `.dev-knowledge` is
preserving your accumulated knowledge as a structured handoff before this
chat closes.

Your role for this Stage 2 response: **project-level architect for `.dev-knowledge`**.
You provide:
- Goal judgment (what next session should achieve, why)
- Project state YOU witnessed in this conversation (not general knowledge
  inferred from training)
- Reasoning and criteria for decisions (how to think about priority calls,
  deferrals, ADR amendments, governance changes)
- Do-not lists that come from project context (gotchas, scope boundaries
  you know matter)

You are NOT:
- An oracle for ecosystem-wide conventions beyond what you witnessed
- A source of repo state facts (HEAD SHA, file contents, test counts) —
  Stage 3 verifies those against the repo directly
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
- "ADR-51 was added during this session" → witnessed, state confidently
- "The tier is probably M based on perceived complexity" →
  inference, write "(architect inference)" after the claim
- "I don't know the exact test count — verify against repo" → unknown

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
ESSENTIALS.md; ADR essences for ADRs cited in directives; the repo state
snapshot.

Apply these rules in every section of your response:

- **Per-section scope declaration.** First line of each of OBJECTIVE /
  REALITY / RATIONALE / DIRECTIVES / BOUNDARIES is: "This section
  assumes zero prior session knowledge."

- **No references the new chat cannot resolve.** No mentions of Stage 1
  ("Stage 1 Q1 framing", "the question above"), no session-internal
  terms ("Round 1 → 2 → 3 file loads", "today's v3.3 prompt"). Generalize
  to "during a recent extended session" or "in the work culminating in
  commit X".

- **List items inline at first mention.** No forward-references. List the
  items where first mentioned, or omit the count if the list is too long
  for inline. Provide representative state, not an exhaustive log — if a
  list runs long, select the decision-relevant items.

- **Inline a 1-sentence summary only for files NOT already in the bundle.**
  Files already in the bundle (VISION, PLAYBOOK, ESSENTIALS, and the
  essences of cited ADRs) need no inline summary — the new chat will
  read them.

- **No external citations not in the bundle.** Paper titles, blog posts,
  arxiv IDs — none are in the bundle and the new chat cannot verify them.
  Concepts can be stated as reasoning; citations cannot.

- **Write about the work, not the meta-process of handing it off.** Do
  not describe the new chat as "the test subject" or frame the handoff
  as "an empirical test" unless that framing drives a receiver-side action.

**Audience-simulation check (do this before submitting):** mentally
simulate a fresh LLM session reading ONLY the Stage 3 bundle. For each
paragraph of your response, ask: would this be comprehensible without
reaching for external context? If any paragraph fails, rewrite it.
Cross-repo content fails this check — default expectation is zero
cross-repo content; only unclosed threads that genuinely could not close
belong in REALITY, framed as "unclosed thread, awareness only";
DIRECTIVES never target other repos.

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

## Current state (verified at Stage 1 by Claude Code)

- **HEAD:** `aeaf1582d68c8e2ae4ff304bf08972f6e01eec10`
- **Branch:** `main`
- **Working tree:** clean
- **Recent work (last 10 commits):**
  - `aeaf158` Merge branch 'docs/architecture-doc-adr'
  - `cf62be1` docs(journal): 2026-05-18 ADR-51 architecture-doc convention + distillation rule
  - `592dc8c` docs(handoff): Stage 3 for ai-council session-sync (2026-05-18)
  - `949e9f5` docs: record ADR distillation as an automated Council process step
  - `a552454` docs: add ADR-51 architecture documentation convention
  - `23652c1` docs: archive Council transcript — architecture-doc convention debate
  - `2945bc0` Merge branch 'docs/close-architecture-deferral'
  - `c83df01` docs(journal): 2026-05-18 ADR-38 A4 + PLAYBOOK AGENTS.md fix
  - `d1dac86` docs(playbook): correct AGENTS.md file-type taxonomy
  - `5dc7f29` docs(adr): ADR-38 A4 — close corp-monorepo ARCHITECTURE.md migration deferral

## .dev-knowledge BACKLOG items relevant to this session

**Stream C — .dev-knowledge governance (open):**
- [P2] .dev-knowledge ADR-38 self-compliance gap — src/ + pyproject.toml (governance-only repo vs ADR-38 universal mandate)
- [P2] Lessons activation P1 implementation (lessons-index.json + SessionStart hook + CLI per ADR-35)
- [P2] ESSENTIALS.md cheat-sheet additions for ADRs 35-41 (under "1 page" constraint, requires pruning)
- [P2] Audit tool: check_backlog_organization code-span-aware done-token regex (false-positive FAIL on backtick spans)
- [P2] Stream taxonomy grooming — Cross-stream section exceeds 33% kill criterion (ADR-47)
- [P3] ADR-39 amendment — BACKLOG.md lifecycle entry
- [P3] ADR-41 amendment — reference ADR-47
- [P3] ADR-39 registry decision — 5 unregistered template files
- [P3] LESSONS.md parenthetical-qualifier entries escape dated-entry audit regex

**Cross-stream (open, high-priority):**
- [P1] Council decisions management consolidation — inventory closed; contradiction detection + ownership model open
- [P1] Sacred-files maintenance enforcement — design + implement enforcement mechanism
- [P2] Handoff advisory framing leaks into receiver behavior — classify root cause, propose mitigation
- [P2] Fix pre-existing test failure: test_ratio_pass_when_stable_above_ceiling
- [P2] Hooks audit + consolidation

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

What is the immediate goal of the next `.dev-knowledge` session?

Given the recent work (ADR-51 added, ai-council handoff completed, ADR-38 A4
amendment closed), what should the next session prioritize from the open BACKLOG
above? If you witnessed a priority commitment or a "do this next" statement
during this session, state it. If the priority is your judgment rather than
a witnessed commitment, mark it "(architect inference)".

*Epistemic note: state your goal judgment confidently. If BACKLOG items above
feel misordered or lower priority than they appear, say so with reasoning.*

### 2. REALITY

What is the current state of `.dev-knowledge` from your perspective?

- Was anything completed or substantially advanced in this session beyond
  what the commit log shows (above)?
- Any work in progress or partially-resolved items not reflected externally?
- Any constraints (deadlines, conventions, inter-item dependencies) the next
  session must respect?
- If you witnessed the state of the P2 pre-existing test failure
  (test_ratio_pass_when_stable_above_ceiling) during this session, report it;
  otherwise mark Unknown.
- If you witnessed discussion of the ADR-38 governance-only repo exception
  path (option a/b/c in BACKLOG Stream C P2), report the direction chosen;
  otherwise mark Unknown.

*Epistemic note: differentiate witnessed events (you saw this in conversation)
from inferences (reasoning from context) from unknowns (no direct knowledge).
Mark inferences with "(architect inference)" and unknowns with "Unknown —
verify against repo."*

### 3. RATIONALE

If you witnessed reasoning that shaped decisions in this session and the next
session needs to understand it, describe it.

- If you witnessed the reasoning behind ADR-51 (architecture documentation
  convention) — specifically what triggered it and what alternative was
  considered — state it; otherwise mark Unknown.
- If you witnessed reasoning about the ADR-38 self-compliance resolution path
  for `.dev-knowledge` (governance-only repo exception vs. minimal pyproject.toml
  creation), state it; otherwise mark Unknown — Stage 3 verifies against the ADR.
- If you witnessed reasoning about the Sacred-files maintenance enforcement
  mechanism choice (which candidate: pre-commit hook / session-end skill / CI
  check / diff-based detection), state it; otherwise mark Unknown.

*Epistemic note: reasoning is your strong suit — explain your judgment when
you witnessed it. "Unknown — Stage 3 verifies against the commit / ADR" is
acceptable and preferred over a constructed rationale.*

### 4. DIRECTIVES

What are the exact sequential actions the next `.dev-knowledge` session should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

Suggested defaults (revise, reorder, or replace as needed based on your
judgment):

1. Resolve pre-existing test failure `test_ratio_pass_when_stable_above_ceiling` —
   investigate root cause, fix, verify `pytest -x` passes clean.
2. Address ADR-38 self-compliance gap — choose resolution path (governance-only
   exemption OR minimal pyproject.toml creation), implement, verify audit tool
   no longer flags self-audit FAIL.
3. Implement lessons activation P1 (ADR-35) — build lessons-index.json +
   SessionStart retrieval hook + `lessons query` CLI; verify with a sample query.
4. Groom Cross-stream section to ≤33% — reclassify items to streams or create
   Stream E; verify BACKLOG taxonomy audit passes.
5. Sacred-files maintenance enforcement — design and implement one enforcement
   mechanism (candidate: session-end checklist skill update).

Revise this sequence based on priority witnessed in conversation. If a different
item should go first, explain why.

*Epistemic note: action sequence and verification steps are most valuable.
Specific file paths — mark "(architect inference)" if not directly witnessed;
Stage 3 revises based on repo state.*

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

Suggested defaults (add, remove, or revise based on your knowledge):
- Do NOT write code to other repos (ADR-36 read-only contract: `.dev-knowledge`
  is auditor and knowledge source; all writes to child repos route via handoff
  or scrum-master review pattern).
- Do NOT create new markdown files without checking README.md growth triggers
  (per CLAUDE.md).
- Do NOT edit LESSONS.md old entries — append-only.
- Do NOT recreate CHANGELOG.md or BACKLOG_ARCHIVE.md (deleted 2026-05-16
  per Council Simplification).
- Do NOT commit work to main without running pre-commit hooks.

Add any architect-specific "do not" items you witnessed being important in
this session.

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
