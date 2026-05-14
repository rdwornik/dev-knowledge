# Handoff Stage 1: .dev-knowledge (session-sync)

<!-- scope: meta -->

| Field | Value |
|---|---|
| Repo | `.dev-knowledge` |
| HEAD SHA | `4cf2d9d336595ef97499c70c0cebb55d71d50b8c` |
| Branch | `main` |
| Working tree | clean |
| Slug | `2026-05-14-dev-knowledge-session-sync` |
| Timestamp | 2026-05-14 |
| Type | session-sync |

════════════════════════════════════════════════════════════════════
SECTION A — INSTRUCTIONS FOR ROB (do NOT paste this into old chat)
════════════════════════════════════════════════════════════════════

1. Open the EXISTING (OLD) browser chat for `.dev-knowledge` — the chat being
   wrapped up. NOT a new chat.
2. Copy from the PASTE_BOUNDARY line below to the end of this file.
3. Paste as a message in the existing chat.
4. The old chat answers the 5 pipeline questions from its lived knowledge.
5. Open the pre-created file:
   `docs/handoffs/_in_progress/2026-05-14-dev-knowledge-session-sync/stage2-response.md`
   (already exists, has placeholder content). Replace everything below the
   "═══ REPLACE EVERYTHING BELOW THIS LINE ═══" marker with the architect's
   response. Save.
6. In Claude Code at .dev-knowledge, say:
   "complete handoff for .dev-knowledge"
   → Stage 3 generates the final handoff folder.
7. After Stage 3: close the old chat. Open a NEW claude.ai chat for `.dev-knowledge`
   and use the Stage 3 folder bundle (`00_README.md` inside has upload instructions).

════════════════════════════════════════════════════════════════════
PASTE_BOUNDARY — copy from here to end of file into the old chat
════════════════════════════════════════════════════════════════════

# Stage 2 — Answer These Questions: .dev-knowledge (session-sync)

## Your role

You are the existing browser chat for **`.dev-knowledge`**, currently being wrapped up
because your context is getting full. Claude Code in `.dev-knowledge` is preserving
your accumulated knowledge as a structured handoff before this chat closes.

Your role for this Stage 2 response: **project-level architect for `.dev-knowledge`**.
You provide:
- Goal judgment (what next session should achieve, why)
- Project state YOU witnessed in this conversation (not general knowledge inferred
  from training)
- Reasoning and criteria for decisions (how to think about priority calls, deferrals)
- Do-not lists that come from project context (gotchas, scope boundaries you know
  matter)

You are NOT:
- An oracle for ecosystem-wide conventions (.dev-knowledge structure, ADR schemas,
  cross-repo patterns) — the handoff bundle has VISION + PLAYBOOK + ESSENTIALS
- A source of repo state facts (HEAD SHA, file contents, configs, test counts) —
  Stage 3 verifies those against the repo directly
- Required to provide specifics where you don't have direct knowledge

## What's in the handoff bundle (so don't repeat these)

The new (fresh) chat receiving the Stage 3 handoff bundle will automatically have:
- Full `.dev-knowledge` VISION.md (ecosystem context)
- Full `.dev-knowledge` PLAYBOOK.md (methodology, conversation style, prompt format,
  commit conventions)
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
- **(architect inference)**: you are reasoning from context, not direct observation
  — mark it inline
- **Unknown**: you don't have direct knowledge — say so explicitly

LLMs default to "be helpful" by filling gaps with plausible specifics. Resist this.
Stage 3 verifies factual claims against the repo. Your value is judgment and reasoning,
not confident fabrication of facts you didn't witness.

If you don't know something specific: say "Unknown — Stage 3 should verify."

## Format requirements (CRITICAL — read before responding)

Your response will be copy-pasted verbatim into stage2-response.md for Stage 3 parsing.

**Copy-paste note:** chat UIs sometimes strip `#` markdown markers when you copy
rendered text. Stage 3 parser is TOLERANT and accepts multiple heading formats:

- Markdown level-3: `### 1. OBJECTIVE`
- Bold: `**1. OBJECTIVE**`
- Plain numbered: `1. OBJECTIVE`

If unsure which survives your client's copy-paste, use both:
`### **1. OBJECTIVE**` — at least one form will survive.

**Required:**
- No preamble before first heading ("Here's my response:", "Sure:")
- No closing remarks after final BOUNDARIES content
- All 5 sections required, in order: OBJECTIVE / REALITY / RATIONALE / DIRECTIVES /
  BOUNDARIES
- Each section heading uses exact section name (case-sensitive)

**NOT allowed:**
- Wrapping ENTIRE response in code fence (no ` ```markdown ` at the very start;
  no closing ` ``` ` at the very end)

**Example correct opening:**
```
### 1. OBJECTIVE
The next session should...
```

## Current state (verified at Stage 1 by Claude Code)

- HEAD: `4cf2d9d336595ef97499c70c0cebb55d71d50b8c`
- Branch: `main`
- Working tree: clean
- Recent context: Last session (2026-05-13) — HANDOFF_PROCESS refined to v3.3
  (audit language refinements: plain-English section names in 06/07 files, first-reference
  code glosses, Hard Constraints vs Narrow Scope DO-NOT split, verb-led sentences required);
  mandatory articulation gate added as new chat's first action before any work begins
  (operator confirms via "role confirmed"); four LESSONS (#1, #2, #6, #8) promoted to
  ESSENTIALS invariants; ESSENTIALS channel-discipline rule added (LESSONS #10, 2026-05-13)

## .dev-knowledge BACKLOG items relevant to this session

**Stream C — .dev-knowledge governance (open P1/P2):**

- **[P1] [open]** PLAYBOOK content additions for ADRs 36/37/40/41 — 4 ADRs ratified
  2026-04-30 add/change process; PLAYBOOK currently does not cover them. Methodology debt.
- **[P1] [open]** Audit tool P1 implementation — compute_tier_score, classify_tier per
  ADR-40; required for Phase 2 universalization.
- **[P2] [open]** Lessons activation P1 implementation — lessons-index.json + retrieval
  (SessionStart hook) + querying (CLI) per ADR-35.
- **[P2] [open]** ESSENTIALS.md cheat-sheet additions for ADRs 35-41 — review which ADRs
  warrant inclusion; apply "keep under 1 page" constraint (currently at 226 lines, over).
- **[P3] [open]** ADR-39 amendment — BACKLOG.md lifecycle entry.
- **[P3] [open]** ADR-39 registry decision — 5 unregistered template files (decision needed:
  add registry entries or formally exclude templates as a class).

**Cross-stream (open P1/P2 touching .dev-knowledge):**

- **[P1] [open]** Council decisions management consolidation — index closed (Item 0);
  remaining: contradiction detection mechanism + ownership model for decision evolution.
- **[P1] [open]** Sacred-files maintenance enforcement — enforcement mechanism for 9 canonical
  files drifting between sessions; pre-commit staleness check, session-end checklist, or CI.
- **[P2] [open]** Fix pre-existing test failure: `test_ratio_pass_when_stable_above_ceiling`
  — fails on main as of 2026-05-12; root cause unknown; blocks clean pytest runs.
- **[P2] [open]** Codify scrum-master review authority pattern — N=1 (ai-council 2026-05-12);
  awaits N=2 for ADR-44 codification.
- **[P2] [open]** Hooks audit + consolidation — full hook inventory not documented; two review
  hooks with overlapping purposes.

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

What is the immediate goal of the next `.dev-knowledge` session?

The last two sessions closed v3.3 of HANDOFF_PROCESS (articulation gate) and promoted
four LESSONS to ESSENTIALS invariants. The BACKLOG has three open P1 items in Stream C
plus two open P1 cross-stream items. Which of these should drive the next session —
and in what order?

Consider:
- Is the pre-existing test failure (`test_ratio_pass_when_stable_above_ceiling`)
  a blocker that must clear before any other Stream C work proceeds?
- PLAYBOOK content additions (ADRs 36/37/40/41) vs audit tool P1 implementation —
  which has higher leverage for the next session's goal?
- Any unfinished threads from this session that should close before the next
  session opens fresh?

*Epistemic note: state your goal judgment confidently. The BACKLOG context above is
factual; if your lived session judgment differs from the written priority order, say
so with reasoning.*

### 2. REALITY

What is the current state of `.dev-knowledge` from your perspective?

- Was anything completed in this session beyond what's reflected in the recent commits
  listed above?
- Any in-progress work not yet committed or tracked externally?
- External dependencies (ai-council, corp-monorepo, other repos) currently in play?
- Any ESSENTIALS or PLAYBOOK sections that feel stale or inconsistent after recent
  changes (v3.3 refinements, four LESSONS promotions)?
- Any constraints (deadlines, conventions, known risks) the next session must respect?

*Epistemic note: differentiate witnessed events (you saw this in conversation) from
inferences (reasoning from context) from unknowns (no direct knowledge). Mark
inferences with "(architect inference)" and unknowns with "Unknown — verify against
repo."*

### 3. RATIONALE

What approaches were considered and discarded in this session?

- Were alternative framings of the v3.3 articulation gate considered? What was
  chosen and why?
- Was there a decision about whether ESSENTIALS promotion of LESSONS should continue
  in next session or pause?
- Any ADR amendment options surfaced but deferred?
- Any BACKLOG grooming decisions (priority changes, closures, new items) made in
  this session that are not yet reflected in BACKLOG.md?

*Epistemic note: reasoning is your strong suit — explain your judgment. Mark
"(architect inference)" for specific claims you're reasoning toward rather than
directly witnessing.*

### 4. DIRECTIVES

What are the exact sequential actions the next `.dev-knowledge` session should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

Proposed defaults based on BACKLOG (revise as needed):

1. Fix pre-existing test failure `test_ratio_pass_when_stable_above_ceiling` — run
   `pytest -x --tb=short` to confirm clean; commit fix.
2. PLAYBOOK content additions for ADRs 36/37/40/41 — draft + append 4 sections;
   update PLAYBOOK header version/date; verify scope tags pass; commit.
3. (If session capacity permits) ESSENTIALS.md review for ADRs 35-41 — which warrant
   inclusion given 226-line current length? Judgment call with pruning.

Add, remove, or reorder as you see fit.

*Epistemic note: action sequence and verification steps are most valuable. Specific
file paths or content — mark "(architect inference)" if not witnessed; Stage 3 may
revise based on repo state.*

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

Proposed defaults (revise as needed):

- Do NOT attempt audit tool P1 implementation in the same session as PLAYBOOK additions
  — audit tool is a coding task requiring separate scoped session.
- Do NOT add ESSENTIALS sections without simultaneously checking total line count and
  pruning if needed (ADR-27 / "keep under 1 page" constraint already breached at 226 lines).
- Do NOT begin Phase 2 universalization rollout (corp-monorepo) until PLAYBOOK is
  updated to reflect the ADRs governing it.

Add any architect-specific concerns or "do not's" from this session.

*Epistemic note: do-not lists grounded in your project knowledge are very valuable.
Don't fabricate "do not touch X" if you don't know whether X exists — focus on knowns
from your conversation.*

---

## Before submitting your response, also verify

- **Any cross-repo content?** Per Universal Self-Containment Rule, default expectation
  is zero cross-repo content in handoff. Only unclosed threads that genuinely could not
  close belong in REALITY, framed as "unclosed thread, awareness only." DIRECTIVES never
  target other repos.
- **Internal coherence?** No DIRECTIVE violates own BOUNDARIES; OBJECTIVE-stated highest
  priority aligned with DIRECTIVE #1; no directive depends on data not packaged in bundle.

If either check fails, revise before submitting.

════════════════════════════════════════════════════════════════════
End of paste block.
Old chat: please answer questions 1-5 above following the Format
requirements above. Structure response with the exact headings
(OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES) so
Claude Code can parse them at Stage 3.
════════════════════════════════════════════════════════════════════
