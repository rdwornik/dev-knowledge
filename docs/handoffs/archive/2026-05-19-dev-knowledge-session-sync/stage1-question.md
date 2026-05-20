# Handoff Stage 1: .dev-knowledge (session-sync)

<!-- scope: meta -->

**Metadata**

- Target repo: `.dev-knowledge`
- Target path: `C:\Users\1028120\Documents\Dev\.dev-knowledge`
- HEAD SHA: `c4d7c8587b6d32ca68d19782009220a3daf45cd9`
- Branch: `main`
- Working tree: clean
- Slug: `2026-05-19-dev-knowledge-session-sync`
- Type: session-sync
- Generated: 2026-05-19
- Stage 1 generator: Claude Code (Opus 4.7, 1M ctx)

════════════════════════════════════════════════════════════════════
SECTION A — INSTRUCTIONS FOR ROB (do NOT paste this into old chat)
════════════════════════════════════════════════════════════════════

1. Open the EXISTING (OLD) browser chat for `.dev-knowledge` — the chat being
   wrapped up. NOT a new chat.
2. Copy from the PASTE_BOUNDARY line below to the end of this file.
3. Paste as a message in the existing chat.
4. The old chat answers the 5 pipeline questions from its lived knowledge.
5. Open the pre-created file:
   `docs/handoffs/_in_progress/2026-05-19-dev-knowledge-session-sync/stage2-response.md`
   (already exists, has placeholder content). Replace everything below the
   `═══ REPLACE EVERYTHING BELOW THIS LINE ═══` marker with the architect's
   response. Save.
6. In Claude Code at `.dev-knowledge`, say: "complete handoff for dev-knowledge"
   → Stage 3 generates the final handoff folder.
7. After Stage 3: close the old chat. Open a NEW claude.ai chat for
   `.dev-knowledge` and use the Stage 3 folder bundle (`00_README.md` inside
   has upload instructions for the new chat).

════════════════════════════════════════════════════════════════════
PASTE_BOUNDARY — copy from here to end of file into the old chat
════════════════════════════════════════════════════════════════════

# Stage 2 — Answer These Questions: .dev-knowledge (session-sync)

## Your role

You are the existing browser chat for **.dev-knowledge**, currently being
wrapped up because your context is getting full. Claude Code in
`.dev-knowledge` is preserving your accumulated knowledge as a structured
handoff before this chat closes.

Your role for this Stage 2 response: **project-level architect for
.dev-knowledge**. You provide:
- Goal judgment (what next session should achieve, why)
- Project state YOU witnessed in this conversation (not general knowledge
  inferred from training)
- Reasoning and criteria for decisions (how to think about tier choice,
  priority calls, deferrals)
- Do-not lists that come from project context (gotchas, scope boundaries
  you know matter)

You are NOT:
- An oracle for ecosystem-wide conventions (.dev-knowledge structure, ADR
  schemas, cross-repo patterns) beyond what you witnessed this session
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
final-pass edit.

### 1. Epistemic honesty

For each claim, classify it using these markers:

- **Witnessed**: you saw this happen in conversation — state it confidently
- **(architect inference)**: you are reasoning from context, not direct
  observation — mark it inline
- **Unknown**: you don't have direct knowledge — say so explicitly

LLMs default to "be helpful" by filling gaps with plausible specifics.
Resist this. Stage 3 verifies factual claims against the repo. Your value
is judgment and reasoning, not confident fabrication of facts you didn't
witness.

If you don't know something specific (a commit message, a file name, a
version number, a config value): say "Unknown — Stage 3 should verify."

### 2. Self-containment for a bundle-only audience

**Principle:** the new chat sees ONLY the Stage 3 bundle. It does not see
this Stage 1 question, prior browser conversations, JOURNAL entries, or
external research. Every claim in your response must be comprehensible
from the bundle alone.

Apply these rules in every section:

- **Per-section scope declaration.** First line of each of OBJECTIVE /
  REALITY / RATIONALE / DIRECTIVES / BOUNDARIES is: "This section
  assumes zero prior session knowledge."
- **No references the new chat cannot resolve.** No mentions of Stage 1
  ("the question above"), no session-internal terms. Generalize to "during
  a recent extended session" or "in the work culminating in commit X".
- **List items inline at first mention.** No forward-references.
- **Inline a 1-sentence summary only for files NOT already in the bundle.**
  Bundle files (VISION/PLAYBOOK/ESSENTIALS, cited-ADR essences) need none.
- **No external citations not in the bundle.** Concepts can be stated as
  reasoning; citations cannot.
- **Write about the work, not the meta-process of handing it off.**

**Audience-simulation check (before submitting):** mentally simulate a
fresh LLM session reading ONLY the Stage 3 bundle. For each paragraph,
ask: would this be comprehensible without reaching for external context?

Per the Universal Self-Containment Rule: default expectation is zero
cross-repo content. DIRECTIVES never target other repos.

### 3. Coherence check

Before submitting, verify: no DIRECTIVE violates own BOUNDARIES; the
OBJECTIVE's top priority aligns with DIRECTIVE #1; no directive depends
on data not packaged in the bundle.

### 4. Format requirements

Your response will be copy-pasted verbatim into stage2-response.md for
Stage 3 parsing.

**Copy-paste note:** chat UIs sometimes strip `#` markers. Stage 3 parser
is TOLERANT and accepts multiple heading formats:

- Markdown level-3: `### 1. OBJECTIVE`
- Bold: `**1. OBJECTIVE**`
- Plain numbered: `1. OBJECTIVE`

**Required:**
- No preamble before first heading ("Here's my response:", "Sure:")
- No closing remarks after final BOUNDARIES content
- All 5 sections required, in order: OBJECTIVE / REALITY / RATIONALE /
  DIRECTIVES / BOUNDARIES
- Each section heading uses exact section name (case-sensitive)
- No extra top-level sections beyond the 5 required

**NOT allowed:**
- Wrapping ENTIRE response in code fence

## Current state (verified at Stage 1 by Claude Code)

- HEAD: `c4d7c8587b6d32ca68d19782009220a3daf45cd9`
- Branch: `main`
- Working tree: clean
- Recent context (last 6 commits, newest first):
  - `c4d7c85` docs: merge codex-reviewer-global-standard — ADR-54, global config live
  - `bd2d3b0` docs: journal — codex reviewer config globalized (ADR-54)
  - `9c0dcab` docs: correct ARCHITECTURE.md Codex/AGENTS.md entry per ADR-54
  - `dcafc36` docs: add Codex reviewer config ownership note to PLAYBOOK §16
  - `0b94878` docs: add ADR-54 — Codex reviewer config as global standard
  - `fcd4eb6` feat: add codex/AGENTS.md — canonical global Codex reviewer config
- Session theme (2026-05-19, multi-chunk day): ADR-53 AGENTS.md retirement
  for `.dev-knowledge` (CLAUDE.md v2.1 live); post-ai-council cross-repo
  sweep (stale refs resolved in live docs); ARCHITECTURE.md violation
  reclassification (known violations → 0); ADR-54 codification of Codex
  reviewer config as global standard (`~/.codex/AGENTS.md` deployed).

## .dev-knowledge BACKLOG items relevant to next session

(Selected from BACKLOG.md — full file in repo. Items the architect may
weigh when ordering next directives.)

- **[Stream C P2 open]** `.dev-knowledge` ADR-38 self-compliance gap —
  `src/` + `pyproject.toml` (auditor fails own checks)
- **[Stream C P2 open]** Lessons activation P1 implementation
  (lessons-index.json + retrieval + querying per ADR-35)
- **[Stream C P2 open]** ESSENTIALS.md cheat-sheet additions for ADRs 35-41
- **[Stream C P2 open]** Audit tool `check_backlog_organization` —
  code-span-aware done-token regex (false-positive fix)
- **[Stream C P2 open]** Stream taxonomy grooming — Cross-stream exceeds
  33% kill criterion (deferred to 2026-07-01 quarterly grooming)
- **[Stream C P2 open]** Codemap generator output specification (ADR-51
  open item — generator tool + CI freshness check)
- **[Cross-stream P1 open]** Council decisions management consolidation
  (contradiction detection + ownership model sub-items remain)
- **[Cross-stream P1 open]** Sacred-files maintenance enforcement (drift
  pattern across 9 canonical files)
- **[Cross-stream P2 open]** Hooks audit + consolidation
- **[Cross-stream P2 open]** Skills universalization across repos
- **[Cross-stream P2 open]** Phase 2 universalization rollout (ai-council
  substantially complete; corp-monorepo not yet started)
- **[Cross-stream P3 open]** ADR-42 amendment — single vs multi-artifact
  handoff format clarification

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

What is the immediate goal of the next `.dev-knowledge` session?

The recent session arc closed three ADR-53 chunks (AGENTS.md retired for
`.dev-knowledge`; cross-repo stale-ref sweep; violation reclassification)
and one new ADR-54 (Codex reviewer config globalized). State what the next
session should achieve next — single OBJECTIVE, not a menu. Candidates the
architect may weigh: corp-monorepo ADR-53 chunk (AGENTS.md retirement +
CLAUDE.md migration — the remaining known violation), ADR-38 self-compliance
gap, Lessons activation P1, codemap generator spec, ESSENTIALS additions.
If the architect's judgment differs, state the chosen OBJECTIVE with reasoning.

*Epistemic note: state your goal judgment confidently. If a BACKLOG item
feels wrong as next-up to you, say so with reasoning.*

### 2. REALITY

What is the current state of `.dev-knowledge` from your perspective?

- Was anything completed in the recent session arc that the BACKLOG / live
  docs do not yet reflect?
- Any work in progress not visible at HEAD?
- External dependencies in play (target repos for upcoming work, e.g.
  corp-monorepo)?
- Any constraints (deadlines, conventions, in-flight ADRs) the next session
  must respect?

*Epistemic note: mark inferences with "(architect inference)" and unknowns
with "Unknown — verify against repo."*

### 3. RATIONALE

If you witnessed reasoning that shaped recent `.dev-knowledge` work and the
next session needs to understand it, describe it. If not, write "Unknown —
no specific rationale witnessed in this session" and skip sub-questions.

Sub-questions (answer only where witnessed):
- If you witnessed the reasoning for treating corp-monorepo `AGENTS.md` as
  outside ADR-53 scope (tool config ≠ instruction contract), state it;
  otherwise mark Unknown — Stage 3 verifies against ADR-54.
- If you witnessed the reasoning for globalizing Codex reviewer config
  (deploying to `~/.codex/AGENTS.md` rather than per-repo), state it;
  otherwise mark Unknown — Stage 3 verifies against ADR-54.
- If you witnessed the reasoning for the three approved condensations in
  CLAUDE.md v2.1 (ADR list trimmed to last 5; scope tags reduced; per-file
  triggers dropped), state it; otherwise mark Unknown.

*Epistemic note: reasoning is your strong suit. "Unknown — Stage 3 verifies
against the commit / ADR" is acceptable and preferred over a constructed
rationale.*

### 4. DIRECTIVES

What are the exact sequential actions the next `.dev-knowledge` session
should execute?

Provide a numbered list. Each action: **action verb + target + verification
step**.

Default proposal (revise as needed): a small number of high-leverage
directives ordered to deliver the OBJECTIVE without scope sprawl. Architect
adds / removes / reorders.

*Epistemic note: action sequence and verification steps are most valuable.
Mark "(architect inference)" if specific paths or commit messages are not
witnessed; Stage 3 may revise based on repo state.*

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

Defaults to consider (architect may add / drop):
- No new ADRs without empirical N≥2 grounding
- Do not edit immutable docs (ADRs, transcripts, handoffs, audits)
- Do not edit old LESSONS.md / TOKEN-LOG.md entries (append-only)
- No orchestration scripts in `.dev-knowledge` (Layer 2 invariant)
- Cross-repo directives belong in routing artifacts, not this handoff

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
