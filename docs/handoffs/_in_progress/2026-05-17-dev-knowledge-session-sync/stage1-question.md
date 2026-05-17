# Handoff Stage 1: .dev-knowledge (session-sync)

**Repo:** `.dev-knowledge`
**Type:** session-sync
**Slug:** `2026-05-17-dev-knowledge-session-sync`
**HEAD SHA:** `c784845c659a98c59f2c161301577d72e17a4801`
**Branch:** main
**Working tree:** clean
**Generated:** 2026-05-17

════════════════════════════════════════════════════════════════════
SECTION A — INSTRUCTIONS FOR ROB (do NOT paste this into old chat)
════════════════════════════════════════════════════════════════════

1. Open the EXISTING (OLD) browser chat for `.dev-knowledge` — the chat
   being wrapped up. NOT a new chat.
2. Copy from the PASTE_BOUNDARY line below to the end of this file.
3. Paste as a message in the existing chat.
4. The old chat answers the 5 pipeline questions from its lived knowledge.
5. Open the pre-created file:
   `docs/handoffs/_in_progress/2026-05-17-dev-knowledge-session-sync/stage2-response.md`
   (already exists, has placeholder content). Replace everything below the
   "═══ REPLACE EVERYTHING BELOW THIS LINE ═══" marker with the architect's
   response. Save.
6. In Claude Code at `.dev-knowledge`, say: "complete handoff for .dev-knowledge"
   → Stage 3 generates the final handoff folder.
7. After Stage 3: close the old chat. Open a NEW claude.ai chat for
   `.dev-knowledge` and use the Stage 3 folder bundle
   (`00_README.md` inside has upload instructions).

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
.dev-knowledge**.

You provide:
- Goal judgment (what next session should achieve, why)
- Project state YOU witnessed in this conversation (not general knowledge
  inferred from training)
- Reasoning and criteria for decisions (how to think about implementation
  sequencing, priority calls, deferrals)
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
  terms. Generalize to "during a recent extended session" or "in the
  work culminating in commit X".
- **List items inline at first mention.** No forward-references.
- **Inline a 1-sentence summary only for files NOT already in the bundle.**
  Files already in the bundle (VISION, PLAYBOOK, ESSENTIALS, and the
  essences of cited ADRs) need no inline summary — the new chat will
  read them.
- **No external citations not in the bundle.** Paper titles, blog posts,
  arxiv IDs — none are in the bundle.
- **Write about the work, not the meta-process of handing it off.**

**Audience-simulation check (do this before submitting):** mentally
simulate a fresh LLM session reading ONLY the Stage 3 bundle. For each
paragraph of your response, ask: would this be comprehensible without
reaching for external context? If any paragraph fails, rewrite it.
Cross-repo content fails this check — per the Universal Self-Containment
Rule, default expectation is zero cross-repo content; only unclosed
threads that genuinely could not close belong in REALITY, framed as
"unclosed thread, awareness only"; DIRECTIVES never target other repos.

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

**NOT allowed:** wrapping the ENTIRE response in a code fence.

## Current state (verified at Stage 1 by Claude Code)

- HEAD: `c784845c659a98c59f2c161301577d72e17a4801`
- Branch: `main`
- Working tree: clean
- Recent session work (per JOURNAL 2026-05-17, newest first):
  - Documented audit test fixtures (`tests/fixtures/README.md`) on branch
    `docs/document-test-fixtures` (commit `d0c8169`)
  - Consolidated Stage 2 handoff instruction set in
    `templates/HANDOFF_QUESTION_TEMPLATE.md` on branch
    `docs/consolidate-handoff-template` — Stage 2 instructions
    restructured from 3 "CRITICAL" sections + 7 drafting rules + 3
    pre-send checks into 4 numbered parts; RATIONALE reframed to allow
    "Unknown"; 2 commits
  - Stage 3 handoff bundle for `2026-05-17-ai-council-session-sync`
    generated and merged to main
  - Decommissioning-discipline lesson + PLAYBOOK subsection +
    ESSENTIALS section + ADR template on branch
    `feat/decommissioning-discipline` (4 commits; not yet merged at
    time of JOURNAL entry)
- Recent merges visible on main: ai-council handoff bundle merged
  (`011be81`); fixture documentation merged (`f102b98`); ADR-43
  ported from `chore/ai-council-feedback-close` (`f6c616f`);
  2026-05-11 session-close artifacts ported (`ad20395`); ai-council
  Directives 1 & 2 execution evidence recorded (`c784845`)

## .dev-knowledge BACKLOG items relevant to this repo

Stream C (.dev-knowledge governance), Cross-stream / Ecosystem, and the
Hyphen Convention Migration Sequence sections are the primary scope.
Representative open items for next-session consideration:

- **[P2] Stream C — .dev-knowledge ADR-38 self-compliance gap** (missing
  `src/` + `pyproject.toml`; resolution options: minimal pyproject, ADR-38
  amendment with "governance-only" tier exemption, or explicit state.yaml
  exception)
- **[P2] Stream C — Lessons activation P1 implementation** (lessons-index.json
  + SessionStart hook + CLI per ADR-35)
- **[P2] Stream C — ESSENTIALS.md cheat-sheet additions for ADRs 35-41**
  (constrained by "1 page" limit; pruning required)
- **[P2] Stream C — Audit tool `check_backlog_organization` code-span-aware
  done-token regex** (false-positives on backtick spans referencing
  ADR-47 vocabulary)
- **[P2] Stream C — Stream taxonomy grooming** (Cross-stream section at
  40%, ADR-47 kill criterion 33%; deferred to 2026-07-01 quarterly grooming)
- **[P1] Cross-stream — Council decisions management consolidation**
  (contradiction detection + ownership model sub-items remain)
- **[P1] Cross-stream — Sacred-files maintenance enforcement** (drift on
  ARCHITECTURE / BACKLOG / CLAUDE / CONTRIBUTING / JOURNAL / LESSONS /
  README / VISION at session boundaries)
- **[P2] Cross-stream — Handoff advisory framing leaks into receiver
  behavior** (classify root cause; ADR-37 / ADR-42 interaction)
- **[P3] Cross-stream — ADR-39 amendment for BACKLOG.md lifecycle entry**
  + **[P3] ADR-41 amendment to reference ADR-47** (bundle as grouped ADR
  amendment to minimize churn)
- **[P3] Cross-stream — ADR-42 amendment: clarify single vs multi-artifact
  handoff format**
- **Unmerged branches potentially in scope:** `feat/decommissioning-discipline`
  (4 commits, awaiting review/merge), `docs/document-test-fixtures` (1 commit,
  awaiting review/merge), `docs/consolidate-handoff-template` (2 commits,
  awaiting empirical validation on next real Stage 2)

(Full BACKLOG is in the repo; do not enumerate exhaustively — pick the
items that drive your DIRECTIVES.)

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

What is the immediate goal of the next `.dev-knowledge` session?

State the single highest-priority outcome the next session should achieve
and why it ranks above other open items. If you believe the right next
move is to merge one of the unmerged branches (decommissioning-discipline,
document-test-fixtures, consolidate-handoff-template) rather than start
fresh work, say so.

*Epistemic note: state your goal judgment confidently. If recent work
direction feels wrong to you, say so with reasoning.*

### 2. REALITY

What is the current state of `.dev-knowledge` from your perspective?

- What did this session actually move forward, in your witnessed view
  (vs. what JOURNAL records)?
- Any work in progress not reflected externally? Unmerged branches whose
  state you witnessed differently than the JOURNAL summary?
- Any constraints (deadlines, conventions, pending Council decisions) the
  next session must respect?
- Any cross-repo thread that genuinely could not close before this handoff
  (rare — frame as "unclosed thread, awareness only")?

*Epistemic note: differentiate witnessed events (you saw this in conversation)
from inferences (reasoning from context) from unknowns (no direct knowledge).
Mark inferences with "(architect inference)" and unknowns with "Unknown —
verify against repo."*

### 3. RATIONALE

If you witnessed reasoning that shaped recent `.dev-knowledge` work and
the next session needs to understand it, describe it. If not, write
"Unknown — no specific rationale witnessed in this session" and skip
the sub-questions below.

Candidate areas where rationale may matter:
- If you witnessed the reasoning behind the Stage 2 instruction-set
  consolidation (`docs/consolidate-handoff-template`), state it;
  otherwise mark Unknown — Stage 3 verifies against the commit.
- If you witnessed the reasoning behind the decommissioning-discipline
  branch's PLAYBOOK / ESSENTIALS / template scope split, state it;
  otherwise mark Unknown — Stage 3 verifies against the commit.
- If you witnessed the reasoning for any deferral (P2 items kept open
  rather than tackled), state it; otherwise mark Unknown.

*Epistemic note: reasoning is your strong suit — explain your judgment
when you witnessed it. For any sub-question above, the answer
"Unknown — Stage 3 verifies against the commit / ADR" is acceptable and
preferred over a constructed rationale. For any specific facts in your
reasoning (file counts, timing, component names), mark "(architect
inference)" if not directly witnessed.*

### 4. DIRECTIVES

What are the exact sequential actions the next `.dev-knowledge` session
should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

Default candidate sequence (revise as you see fit):

1. Review and merge (or close) the three open feature branches in priority
   order — `feat/decommissioning-discipline`, `docs/document-test-fixtures`,
   `docs/consolidate-handoff-template` — with verification: `git status`
   clean on main, `pytest` green.
2. Pick one of: the highest-priority open BACKLOG item you nominate (e.g.,
   ADR-38 self-compliance gap, lessons activation P1, code-span-aware
   regex fix, or one of the grouped ADR amendments).
3. Append JOURNAL entry per `Did / Result / Changes / Abandoned / Next`
   shape at session close; verify with `git log --oneline -5`.

Add, remove, or reorder as you see fit.

*Epistemic note: action sequence and verification steps are most valuable.
Specific file paths or commit messages — mark "(architect inference)" if
not witnessed; Stage 3 may revise based on repo state.*

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

Default candidate boundaries (extend as you see fit):

- Do NOT recreate `CHANGELOG.md` or `BACKLOG_ARCHIVE.md` (deleted
  2026-05-16 per Council Simplification; git history + JOURNAL `Changes:`
  line are authoritative).
- Do NOT add scope-tag enforcement back (system removed 2026-05-16; tags
  remain as informal metadata only).
- Do NOT generate reconciliation reports about other repos' state or
  treat staleness observation about another repo's tracking as a directive
  (Universal Self-Containment Rule).
- Do NOT amend ADR-42 / HANDOFF_PROCESS without empirical evidence from at
  least one Stage 2 run on the consolidated template (pattern: universal-
  without-cross-case-verification, LESSON #9 captured 2026-05-14).
- Do NOT close BACKLOG items as `[done]`-style tombstones in BACKLOG.md;
  done items leave the file (per Council Simplification 2026-05-16). Trace
  lives in git.

Add any architect-specific concerns or "do not's."

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
