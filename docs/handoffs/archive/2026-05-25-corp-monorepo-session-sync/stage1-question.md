# Handoff Stage 1: corp-monorepo (session-sync)

**Repo:** `C:\Users\1028120\Documents\Dev\corp-monorepo`
**HEAD SHA:** `32a47f85b07d697be20066c1ec69df3cf92cb1f6`
**Branch:** `main`
**Working tree:** clean
**Slug:** `2026-05-25-corp-monorepo-session-sync`
**Timestamp:** 2026-05-25
**Type:** session-sync

════════════════════════════════════════════════════════════════════
SECTION A — INSTRUCTIONS FOR ROB (do NOT paste this into old chat)
════════════════════════════════════════════════════════════════════

1. Open the EXISTING (OLD) browser chat for **corp-monorepo** — the chat
   being wrapped up. NOT a new chat.
2. Copy from the PASTE_BOUNDARY line below to the end of this file.
3. Paste as a message in the existing chat.
4. The old chat answers the 5 pipeline questions from its lived knowledge.
5. Open the pre-created file:
   `docs/handoffs/in-progress/2026-05-25-corp-monorepo-session-sync/stage2-response.md`
   (already exists, has placeholder content). Replace everything below the
   "═══ REPLACE EVERYTHING BELOW THIS LINE ═══" marker with the architect's
   response. Save.
6. In Claude Code at `.dev-knowledge`, say: **"complete handoff for corp-monorepo"**
   → Stage 3 generates the final handoff folder.
7. After Stage 3: close the old chat. Open a NEW claude.ai chat for
   corp-monorepo and use the Stage 3 folder bundle (00_README.md inside
   has upload instructions for the new chat).

════════════════════════════════════════════════════════════════════
PASTE_BOUNDARY — copy from here to end of file into the old chat
════════════════════════════════════════════════════════════════════

# Stage 2 — Answer These Questions: corp-monorepo (session-sync)

## Your role

You are the existing browser chat for **corp-monorepo**, currently being
wrapped up because your context is getting full. Claude Code in
`.dev-knowledge` is preserving your accumulated knowledge as a structured
handoff before this chat closes.

Your role for this Stage 2 response: **project-level architect for
corp-monorepo**. You provide:
- Goal judgment (what next session should achieve, why)
- Project state YOU witnessed in this conversation (not general knowledge
  inferred from training)
- Reasoning and criteria for decisions (how to think about priority calls,
  approach choices, deferrals)
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

## How to write the response (read before drafting)

Four concerns govern your response. Apply them during drafting, not as a
final-pass edit.

### 1. Epistemic honesty

For each claim, classify it using these markers:

- **Witnessed**: you saw this happen in conversation — state it confidently
- **(architect inference)**: you are reasoning from context, not direct
  observation — mark it inline
- **Unknown**: you don't have direct knowledge — say so explicitly

Examples:
- "We modified config/settings.yaml when we changed provider timeouts" →
  witnessed, state confidently
- "The tier is probably M based on perceived complexity" →
  inference, write "(architect inference)" after the claim
- "I don't know the exact test count — verify against repo" → unknown

LLMs default to "be helpful" by filling gaps with plausible specifics.
Resist this. Stage 3 verifies factual claims against the repo. Your value
is judgment and reasoning, not confident fabrication.

If you don't know something specific (a file name, a version number, a
config value): say "Unknown — Stage 3 should verify."

### 2. Self-containment for a bundle-only audience

**Principle:** the new chat sees ONLY the Stage 3 bundle. It does not see
this Stage 1 question, prior browser conversations, JOURNAL entries, or
external research. Every claim in your response must be comprehensible
from the bundle alone.

Apply these rules in every section of your response:

- **Per-section scope declaration.** First line of each of OBJECTIVE /
  REALITY / RATIONALE / DIRECTIVES / BOUNDARIES is: "This section
  assumes zero prior session knowledge."

- **No references the new chat cannot resolve.** No mentions of Stage 1,
  no session-internal terms. Generalize to "during a recent extended
  session" or "in the work culminating in commit X".

- **List items inline at first mention.** No forward-references.

- **Inline a 1-sentence summary only for files NOT already in the bundle.**
  Files already in the bundle need no inline summary.

- **No external citations not in the bundle.**

- **Write about the work, not the meta-process of handing it off.**

**Audience-simulation check (do this before submitting):** mentally simulate
a fresh LLM session reading ONLY the Stage 3 bundle. For each paragraph of
your response, ask: would this be comprehensible without reaching for
external context? If any paragraph fails, rewrite it.

Cross-repo content fails this check — default expectation is zero cross-repo
content; only unclosed threads that genuinely could not close belong in
REALITY, framed as "unclosed thread, awareness only"; DIRECTIVES never
target other repos.

### 3. Coherence check

Before submitting, verify: no DIRECTIVE violates own BOUNDARIES; the
OBJECTIVE's top priority aligns with DIRECTIVE #1; no directive depends on
data not packaged in the bundle. Revise before submitting if any fails.

### 4. Format requirements

Your response will be copy-pasted verbatim into stage2-response.md for
Stage 3 parsing.

**Copy-paste note:** chat UIs sometimes strip `#` markdown markers. Stage 3
parser is TOLERANT and accepts multiple heading formats. Use ANY of these:

- Markdown level-3: `### 1. OBJECTIVE`
- Bold: `**1. OBJECTIVE**`
- Plain numbered: `1. OBJECTIVE`

If unsure which survives your client's copy-paste, use both:
`### **1. OBJECTIVE**`

**Required:**
- No preamble before first heading ("Here's my response:", "Sure:")
- No closing remarks after final BOUNDARIES content
- All 5 sections required, in order: OBJECTIVE / REALITY /
  RATIONALE / DIRECTIVES / BOUNDARIES
- Each section heading uses exact section name (case-sensitive)
- No extra top-level sections beyond the 5 required

**NOT allowed:**
- Wrapping ENTIRE response in a code fence

---

## Current state (verified at Stage 1 by Claude Code)

- **HEAD:** `32a47f85b07d697be20066c1ec69df3cf92cb1f6`
- **Branch:** `main`
- **Working tree:** clean
- **Recent commits:**
  - `32a47f8` Merge branch 'docs/audit-corp-monorepo-conformance-gap'
  - `8a24fae` docs(audit): corp-monorepo conformance gap vs .dev-knowledge
  - `98aa638` Merge branch 'docs/audit-corp-monorepo-deep'
  - `e15519b` docs(journal): 2026-05-20 deep audit entry
  - `1d733b1` docs(audit): corp-monorepo deep — packages, invariants, drift surfaces, operational risks
  - `fbcaa86` Merge branch 'docs/delete-corp-monorepo-agents-md'
  - `2e984b9` docs(journal): delete corp-monorepo AGENTS.md, complete ADR-54
  - `1e14ccb` chore: remove stale AGENTS.md entry from check_doc_refs.py

---

## Audit context (informational — extend or correct in your response)

From `docs/audits/2026-05-20-conformance-gap-vs-dev-knowledge.md`
(17 CONFORMS, 3 PARTIAL, 2 GAP, 16 N/A, 2 UNKNOWN → UNKNOWN now resolved):

**GAP findings:**
- **GAP 1:** Phase 2 universalization BACKLOG entry stale upstream — corp-monorepo
  has materially started; upstream `.dev-knowledge` BACKLOG item needs updating
- **GAP 2:** ADR-numbering namespace collision in CLAUDE.md §11 — corp-monorepo
  uses its own ADR-27 but `.dev-knowledge` also has an ADR-27 with a different
  topic; no disambiguation exists in CLAUDE.md §11

**PARTIAL findings:**
- ADR-51 codemap hand-maintained (upstream-gated; low risk)
- ADR-34 vault underscore pattern not disambiguated in CLAUDE.md §4 —
  unclear whether corp's Obsidian references follow the underscore convention

**Resolved UNKNOWN:**
- Tier evaluation (ADR-40): resolved — tier system deprecated ecosystem-wide
  2026-05-23; P1 task is removal of `tier:` / `scale:` frontmatter from
  corp-monorepo files

---

## .dev-knowledge BACKLOG items relevant to corp-monorepo

**P1 (high priority):**
- `[P1][open]` Apply tier-deprecation to corp-monorepo — remove `tier:` and
  `scale:` frontmatter from all corp-monorepo files (ecosystem decision
  2026-05-23, ADR-33/38/40/51 amendments)
- `[P1][open]` Codify scrum-master review authority pattern as an ADR —
  N=3 empirical instances now reached; unblocked for ADR-level codification

**P2 (medium priority):**
- `[P2][open]` Root hygiene application (corp-monorepo) — apply standard
  root-file conventions
- `[P2][open]` Phase 2 universalization rollout — corp-monorepo not yet
  started (though audit notes corp has materially begun; see GAP 1 above)
- `[P2][open]` corp-monorepo hyphen migration + ADR-38 compliance — subitems
  1 (file renaming) and 3 (cross-reference updates) open
- `[P2][open]` Handoff folder format adoption (corp-monorepo) — adopt
  11-file flat handoff folder format
- `[P2][open]` README disposition (corp-monorepo) — decide keep/delete/update

---

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

This section assumes zero prior session knowledge.

What is the immediate goal of the next corp-monorepo session?

The P1 items above (tier-deprecation removal, scrum-master ADR codification)
are waiting, as are the audit-surfaced gaps (ADR namespace collision fix,
vault pattern disambiguation). Weigh these against any session-specific
context you hold:

- Which P1 or P2 item should lead the next session, and why?
- Is there anything from recent audit work that should be addressed before
  these BACKLOG items?
- Are there any dependencies between the items that constrain ordering?

*Epistemic note: state your goal judgment confidently. If BACKLOG priority
labels feel wrong based on what you witnessed, say so with reasoning.*

### 2. REALITY

This section assumes zero prior session knowledge.

What is the current state of corp-monorepo from your perspective?

- Was anything completed since the last round of audit work (commits
  `32a47f8` / `8a24fae`)? Any in-progress work not reflected in those commits?
- Are there open branches, stashed changes, or WIP not yet committed?
- External dependencies (services, libraries, partner repos) currently in play?
- Any constraints (deadlines, conventions, team agreements) the next session
  must respect?
- If you witnessed the audit identifying the ADR namespace collision (GAP 2),
  what was your read on its severity and the preferred fix approach?

*Epistemic note: differentiate witnessed events from inferences from
unknowns. Mark inferences with "(architect inference)" and unknowns with
"Unknown — verify against repo."*

### 3. RATIONALE

This section assumes zero prior session knowledge.

If you witnessed reasoning that shaped recent corp-monorepo work and the
next session needs to understand it, describe it. If not, write
"Unknown — no specific rationale witnessed in this session" and skip
the sub-questions below.

- If you witnessed the reasoning behind the tier-deprecation decision for
  this repo, state it; otherwise mark Unknown — Stage 3 verifies against
  the relevant ADR amendments.
- If you witnessed the reasoning for why scrum-master review authority
  codification was deferred to N=3 instances, state it; otherwise mark
  Unknown — Stage 3 verifies against JOURNAL.
- If you witnessed the reasoning for the ADR-34 vault underscore pattern
  PARTIAL finding (why disambiguation was not added to CLAUDE.md §4 at
  audit time), state it; otherwise mark Unknown.

*Epistemic note: reasoning is your strong suit — explain your judgment
when you witnessed it. For specific facts (file counts, timing, component
names), mark "(architect inference)" if not directly witnessed.*

### 4. DIRECTIVES

This section assumes zero prior session knowledge.

What are the exact sequential actions the next corp-monorepo session should
execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

Default proposal (revise as needed):
1. Remove `tier:` and `scale:` frontmatter from all corp-monorepo files —
   verify with `grep -r "^tier:" .` returning no matches
2. Fix ADR namespace collision in CLAUDE.md §11 — add disambiguation comment
   or prefix corp-local ADRs to distinguish from ecosystem ADRs —
   verify CLAUDE.md §11 is unambiguous
3. Disambiguate ADR-34 vault underscore pattern in CLAUDE.md §4 —
   verify CLAUDE.md §4 makes underscore convention clear for corp context
4. Open ADR for scrum-master review authority pattern —
   verify ADR file created and registered in docs/decisions/README.md
5. Assess README disposition (keep/delete/update) —
   verify decision recorded in JOURNAL

Add, remove, or reorder as you see fit.

*Epistemic note: action sequence and verification steps are most valuable.
Specific file paths — mark "(architect inference)" if not directly witnessed;
Stage 3 may revise based on repo state.*

### 5. BOUNDARIES

This section assumes zero prior session knowledge.

What must the next session NOT do? What are fallback contingencies?

Default constraints (add or remove based on your knowledge):
- Do NOT touch ObsidianVault paths
- Do NOT add new dependencies without Rob's approval
- Do NOT modify test infrastructure without running full test suite first
- Do NOT start Phase 2 universalization rollout in the same session as
  tier-deprecation removal — these are separate scoped tasks
- Do NOT create a new corp-monorepo ADR that reuses a number already used
  in either corp-monorepo or `.dev-knowledge` namespace without resolving
  the collision first

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
