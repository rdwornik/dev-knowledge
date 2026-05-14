# Handoff Stage 1: .dev-knowledge (session-sync)

<!-- scope: meta -->

| Field | Value |
|---|---|
| Repo | `.dev-knowledge` |
| HEAD SHA | `8663a7c9e49c8e5d822746aded34a18f409a4a69` |
| Branch | `docs/2026-05-14-dev-knowledge-session-sync-stage1` |
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
   - NOT: "Round 1 → 2 → 3 file loads", "today's v3.3 prompt",
     "the empirical test of v3.3 begins with this handoff cycle"
   - DO: "during a recent extended session", "in the work culminating
     in commit 8663a7c"

4. **List items inline at first mention.** Do NOT forward-reference.
   - NOT: "drive session-lessons capture (5 primary + 3 secondary lessons,
     see REALITY for list)" then list them later
   - DO: list the items where first mentioned, or omit the count if the
     list is too long for inline

5. **Self-contained claims.** If a claim requires reading another repo
   file (ADR, audit) to understand, inline a 1-sentence summary of that
   file's relevant content at first reference.
   - NOT: "v1 conflicted with audit findings"
   - DO: "v1 (which proposed dropping full invariants from the bundle)
     conflicted with the 2026-05-12 audit finding that the full
     11-file bundle empirically catches architect fabrications via
     drift detection (real case: 2026-05-09 ai-council handoff)"

6. **No external research citations not in the bundle.** Paper titles,
   blog posts, arxiv IDs, vendor blogs — none of these are in the bundle.
   The new chat cannot verify or read them. Strip from the response.
   Concepts can be stated as reasoning; citations cannot.

7. **No self-referential meta-framing.** Do NOT describe the new chat
   as "the test subject" or describe the handoff being "an empirical
   test" unless that framing serves a receiver-side action. Write about
   the work to be done, not about the meta-process of handing it off.

Apply these rules during drafting, not as a final-pass edit. The 7 gaps
are pattern-matched in the LLM's natural output style under session
saturation — fighting them after drafting is harder than avoiding them
during drafting.

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

- HEAD: `8663a7c9e49c8e5d822746aded34a18f409a4a69`
- Branch: `docs/2026-05-14-dev-knowledge-session-sync-stage1`
- Working tree: clean
- Recent context:
  - `4cf2d9d` — Merge docs/2026-05-13-handoff-v3-3-minimum-refinement (v3.3 audit language fixes + articulation gate)
  - `16733dc` — docs(journal): record ESSENTIALS promotions of four lessons
  - `0ae143e` — Merge docs/2026-05-13-essentials-lessons-promotion (four LESSONS promoted to ESSENTIALS invariants #1, #2, #6, #8)
  - `7846b48` — docs(handoff): Stage 1 for 2026-05-14-dev-knowledge-session-sync (initial v3.3 Stage 1, since superseded)
  - `2f944a8` — docs(decisions): add Council research transcript on cross-session handoff optimization
  - `556c8e1` — docs(handoff): amend to v3.3.1 — audience-awareness rules in Stage 1 template
  - `8663a7c` — docs(handoff): clear stale v3.3 Stage 1 before v3.3.1 regeneration

## .dev-knowledge BACKLOG items relevant to .dev-knowledge

Open P1 items in Stream C (.dev-knowledge governance):

- **[P1] PLAYBOOK content additions for ADRs 36/37/40/41** — PLAYBOOK.md sections missing for ADR-36 (audit tool workflow), ADR-37 (two-phase handoff guidance), ADR-40 (tier transition procedures), ADR-41 (BACKLOG grooming workflow). Methodology debt since 2026-04-30.
- **[P1] Audit tool P1 implementation** — Build .dev-knowledge audit tool per ADR-36 (audit run + ecosystem state + markdown report). Needed for Phase 2 universalization.

Open P2 items:

- **[P2] Lessons activation P1 implementation** — lessons-index.json + retrieval hook + CLI per ADR-35.
- **[P2] ESSENTIALS.md cheat-sheet additions for ADRs 35-41** — Under 1-page constraint requires pruning decisions.
- **[P2] ai-council needs AGENTS.md** — Work belongs in ai-council repo; awareness item only.

Open P3 items:

- **[P3] ADR-39 amendment** — add BACKLOG.md lifecycle entry
- **[P3] ADR-39 registry decision** — 5 unregistered template files

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

What is the immediate goal of the next `.dev-knowledge` session?

Consider: The current handoff cycle must complete first (Stage 2 → Stage 3).
After that, the highest open P1 items are PLAYBOOK additions for ADRs 36/37/40/41
and Audit tool P1 implementation. Which deserves priority and why?
If the handoff process improvement work spawned any additional follow-up items
during this session, include them.

*Epistemic note: state your goal judgment confidently. If the BACKLOG priority order
feels wrong to you given what you witnessed this session, say so with reasoning.*

### 2. REALITY

What is the current state of `.dev-knowledge` from your perspective?

- What was completed in the session being closed?
- Any work in progress not yet committed or formalized?
- Any tensions or open questions about the v3.3.1 amendment — was the 7-rule
  audience-awareness approach the right scope, or does something feel off?
- Any constraints the next session must respect?

*Epistemic note: differentiate witnessed events from inferences from unknowns.
Mark inferences with "(architect inference)" and unknowns with "Unknown — verify
against repo."*

### 3. RATIONALE

What approaches were considered and discarded for `.dev-knowledge` recently?

Cover:
- The decision to scope v3.3.1 as a template amendment only (not escalating
  to v3.4 with Q&A or simulation). What made that scope correct? What would
  need to be true for v3.4 to be warranted?
- The Council research transcript commit: what signal was real, what was noise?
  How should the next session weight that research when evaluating v3.3.1 results?
- Any BACKLOG priority decisions made this session.

*Epistemic note: reasoning is your strong suit. For any specific facts in your
reasoning, mark "(architect inference)" if not directly witnessed.*

### 4. DIRECTIVES

What are the exact sequential actions the next `.dev-knowledge` session should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

Default proposal (revise as needed):
1. Complete current handoff cycle: architect provides Stage 2 response → operator
   saves to stage2-response.md → "complete handoff for .dev-knowledge" → Stage 3 runs.
   Verify: 11-file folder generated in docs/handoffs/2026-05-14-dev-knowledge-session-sync/.
2. Validate v3.3.1 empirically: assess whether Stage 2 response under v3.3.1 avoided
   the 7 audience-awareness gaps. Record observation in LESSONS.md if findings are clear.
   Verify: LESSONS.md append committed.
3. Begin PLAYBOOK content additions for ADRs 36/37/40/41 (highest open P1 in Stream C).
   Verify: PLAYBOOK.md commit; BACKLOG item updated to [done].

Add, remove, or reorder as you see fit.

*Epistemic note: action sequence and verification steps most valuable. File paths
and commit messages — mark "(architect inference)" if not witnessed.*

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

Default boundaries (add architect-specific concerns):
- Do NOT escalate to v3.4 until v3.3.1 empirical results are in — the audience-awareness
  rules need at least one full handoff cycle to assess before raising the gate further.
- Do NOT modify HANDOFF_FOLDER_TEMPLATE.md (Stage 3 template) in this handoff cycle —
  v3.3.1 scope was Stage 1 template only.
- Do NOT generate cross-repo directives targeting ai-council or corp-monorepo from a
  .dev-knowledge session — cross-repo work routes via routing artifacts per Universal
  Self-Containment Rule.
- Do NOT begin Audit tool P1 implementation in the same session as PLAYBOOK additions
  unless PLAYBOOK work completes cleanly first — context load risk.

Fallback if Stage 3 fails or drift detected: inspect both SHAs, confirm with operator
before proceeding. Do not silently discard drift.

---

## Before submitting your response, also verify

- **Any cross-repo content?** Per Universal Self-Containment Rule (see HANDOFF_PROCESS), default expectation is zero cross-repo content in handoff. Only unclosed threads that genuinely could not close belong in REALITY, framed as "unclosed thread, awareness only." DIRECTIVES never target other repos.
- **Internal coherence?** No DIRECTIVE violates own BOUNDARIES; OBJECTIVE-stated highest priority aligned with DIRECTIVE #1; no directive depends on data not packaged in bundle.
- **Audience awareness check:** Mentally simulate a fresh LLM session
  reading ONLY the Stage 3 bundle (no Stage 1, no JOURNAL, no prior
  chats, no external research). For each paragraph of your response,
  ask: would this be comprehensible without reaching for external context?
  If any paragraph fails, rewrite to be self-contained per the 7
  audience-awareness rules above.

If any check fails, revise before submitting. (Source of truth: HANDOFF_PROCESS Universal Self-Containment Rule.)

════════════════════════════════════════════════════════════════════
End of paste block.
Old chat: please answer questions 1-5 above following the Format
requirements above. Structure response with the exact headings
(OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES) so
Claude Code can parse them at Stage 3.
════════════════════════════════════════════════════════════════════
