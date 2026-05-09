# ADR-42 — Handoff Format v3.0

<!-- scope: meta -->

Status: Accepted (amended three times: 2026-05-09 afternoon, 2026-05-09 later afternoon, 2026-05-09 night)
Date: 2026-05-09

## Amendments

### 2026-05-09 (night) — v3.2: Q&A iteration loop + operator clarity

First end-to-end test of v3.1 (NEW chat receiving ai-council bundle)
surfaced two gaps:

**Gap 1: No Q&A iteration between Stage 2 and Stage 3.**
NEW chat receiving handoff bundle had no mechanism to ask
clarification questions back to OLD chat (Stage 2 source). Current
flow assumed Stage 2 one-shot answer was sufficient. Reality:
synthesis blind spots, ambiguous directives, or missing context
require iteration.

**Gap 2: Operator next-step ambiguity.**
After uploading bundle and pasting 00_first-message.md, operator
(Rob) didn't know whether to wait, what to type to confirm
synthesis, what comes next. "Confirm synthesis" was implicit; not
clear what exact phrase needed.

#### v3.2 changes

**Stage 2.5 (new): Q&A iteration loop**

Optional phase between Stage 2 and Stage 3:
- NEW chat presents synthesis after reading bundle
- If NEW chat has clarification questions: formats as numbered list
  (max 3 questions per round)
- Operator routes questions to OLD chat, gets answers, returns to
  NEW chat
- Up to 3 rounds. After round 3, NEW chat proceeds with best
  available understanding OR operator escalates to Rob for restart
  of Stage 2.
- Each round appended to
  `_in_progress/{slug}/stage2-amendments.md`

Stage 3 detection unchanged: requires stage2-response.md present
with valid 5 sections. Stage 2.5 amendments don't block Stage 3 —
they enrich Stage 2 input.

**Operator workflow explicit (10 steps)**

00_README.md template now includes step-by-step operator workflow:
1. Open NEW chat (fresh, zero context)
2. Drag-drop folder content (12 files) or zip
3. Paste 00_first-message.md as first message
4. Read NEW chat's synthesis output — verify accuracy
5. Confirm or correct synthesis — type exact phrase:
   "synthesis confirmed" or "synthesis correction: [specifics]"
6. Q&A loop (if NEW chat asks questions): route to OLD chat,
   return answers, repeat up to 3 rounds
7. NEW chat asks: "single Claude Code prompt or split?" — operator
   answers
8. NEW chat generates prompt(s) as downloadable .md
9. Operator runs prompts in Claude Code in target repo
10. Operator returns 09_EXECUTION_EVIDENCE.md to `.dev-knowledge`

**00_first-message.md template** now explicitly tells NEW chat:
- After synthesis, wait for operator's "synthesis confirmed" or
  correction
- If clarification questions exist, format as numbered list, ask
  before generating prompts
- After confirmation: ask operator "single prompt or split?"
- Generate downloadable .md prompts only after operator confirms
  format

**Implementation impact:**
- HANDOFF_FOLDER_TEMPLATE updated with new 00_README + 00_first-message
  specs
- ai-council bundle (2026-05-09-ai-council-audit-sync) regenerated
  with v3.2 templates
- HANDOFF_PROCESS Stage 2.5 procedure documented

---

### 2026-05-09 (afternoon) — Audit-sync shortcut removed

Original ADR-42 ratification included a clause allowing Stage 2 to be
"implicit" for audit-sync handoffs, with Claude Code substituting
audit findings for the browser-2 architect response. This clause was
removed.

Reason: untested assumption. Audit findings provide structured audit
results but cannot capture browser-2's tacit project knowledge —
recent priorities, what's genuinely concerning vs cosmetic, mental
model, competing work. Stage 2 contribution is non-substitutable.

ALL handoffs (audit-sync, session-sync, feature-X-sync, etc.) now
follow full three-stage flow.

Implementation impact: the ai-council audit-sync handoff generated
under the shortcut (2026-05-09 morning) was deleted and will be
regenerated via proper 3-stage flow. Lessons captured in LESSONS.md.
HANDOFF_PROCESS rewritten to v3.1 as operational counterpart.

### 2026-05-09 (later afternoon) — Stage 2 source semantics clarified

Earlier ADR-42 ratification and first amendment described Stage 2 as
"browser-2 architect provides project intelligence" without specifying
which browser session. This was ambiguous and read by Claude Code as
"open a new chat." That reading inverts handoff purpose.

Correction: Stage 2 source is the EXISTING browser chat for the target
repo — the chat being wrapped up due to context exhaustion. The point
of handoff is to preserve that chat's accumulated tacit knowledge
before its context dies. A fresh chat has no context to add.

**Three-actor flow (canonical):**

| Actor | Role | Timing |
|---|---|---|
| **Claude Code in .dev-knowledge** | Orchestrator + generator | All 3 stages |
| **OLD browser chat** for {repo} | Stage 2 source: existing chat being wrapped up. Has accumulated context. Receives Stage 1 question; produces Stage 2 response from lived knowledge. | During Stage 2 |
| **NEW browser chat** for {repo} | Stage 3 receiver: opened AFTER Stage 3 generates final folder. Receives 11-file bundle as upload + 00_first-message.md as first message. Acts on directives; fills 09_EXECUTION_EVIDENCE.md. | After Stage 3 |

If Stage 2 goes to a NEW chat: fresh chat has no context, response
collapses to restating known audit findings, Stage 2 adds no signal.
This is the rejected "implicit shortcut" pattern in different form.

If Stage 2 goes to OLD chat: architect's lived knowledge (priorities,
mental model, in-flight decisions, recent concerns) is captured before
context dies. Knowledge is non-substitutable.

Implementation impact: HANDOFF_PROCESS.md Stage 2 section rewritten;
templates corrected; ai-council Stage 1 question prompt regenerated
with corrected instructions (paste into OLD ai-council chat, not new).

---
Related: ADR-32 (handoff process v2.0, partially superseded),
         ADR-36 (audit tool architecture, read-only contract preserved),
         ADR-37 (session boundary protocol, two-phase preserved),
         ADR-39 (file lifecycle governance, new files registered),
         ADR-41 (cross-session backlog architecture, BACKLOG integration),
         transcripts council_out_20260509_144836_research_*

## Context

ADR-32 (HANDOFF_PROCESS v2.0) defined initial handoff format. ADR-37
overlaid two-phase Current State / Future State. First real-world
application — ai-council audit handoff (2026-04-30) — exposed
fundamental issues:

- Three nesting levels created friction for upload/consumption
- 13 files exceeded research-recommended 4-8 file count
- VISION, PLAYBOOK, ESSENTIALS NOT included → Browser-2 lacks
  ecosystem and methodology context (silent hallucination risk)
- 7 full ADR copies caused attention dilution
- first-message.md separate from contents bundle confused upload UX
- No standardized question pipeline — each handoff hand-crafted
- No two-stage workflow — single Browser-1 (.dev-knowledge) generated
  artifact without architect-level project intelligence

Council research (2026-05-09 debate) surfaced industry patterns
across AI agent handoffs (LangGraph, AutoGen, Cline Memory Bank),
mature-domain protocols (SBAR, I-PASS, SITREP), knowledge
management theory (SECI, Diátaxis), documentation systems, drift
mitigation patterns, and ergonomic conventions.

Three providers (Perplexity, Grok, Gemini) converged on:
- Flat folder structure (1 level, 4-8 files)
- Manifest with checksums + HEAD pin
- 5-7 question canonical pipeline (SBAR/I-PASS/SITREP hybrid)
- Aggressive externalization of tacit knowledge (SECI bottleneck)
- Receiver verification (read-back) is mandatory
- Markdown over JSON for token efficiency

Rob's strategic directive: "więcej teraz, optymalizować później" —
maximize completeness for first iterations, optimize based on
empirical friction. Plus three-stage flow refinement: Claude Code
in `.dev-knowledge` evaluates → generates question prompt → Rob
takes to browser-2 → response back → Claude Code reconciles +
generates folder.

## Decision

### Three-stage flow

| Stage | Actor | Input | Output |
|---|---|---|---|
| 1 | Claude Code (.dev-knowledge) | "Make handoff for {repo}" | 01_question_for_browser.md |
| 2 | Browser-2 (project chat) | Question prompt | Structured response markdown |
| 3 | Claude Code (.dev-knowledge) | Response markdown | Complete handoff folder |

ALL handoff types follow full three-stage flow including Stage 2
(architect response). Audit findings inform Stage 1 question
generation but DO NOT substitute for Stage 2 — browser-2 architect
contributes tacit project knowledge (priorities, mental model, recent
concerns, competing work) that audit findings cannot capture.

Earlier draft of ADR-42 (2026-05-09 morning) included an
"audit-sync shortcut" allowing Claude Code to skip Stage 2 and
proceed directly from Stage 1 to Stage 3. This shortcut was
unjustified and removed. Lessons captured in LESSONS.md.

### Storage location

All handoffs in `.dev-knowledge/docs/handoffs/{date}-{slug}/` where
slug encodes repo + type (e.g., `2026-04-30-ai-council-audit-sync`,
`2026-05-15-corp-monorepo-feature-X-sync`).

Preserves ADR-36 read-only contract — handoffs never written to
target repos.

### Folder structure (flat, ~11 files)

```
docs/handoffs/{date}-{slug}/
├── 00_README.md                 (Rob's upload instructions)
├── 00_first-message.md          (browser-2 first message, copy-paste)
├── 01_MANIFEST.md               (entry point, file index, HEAD pin)
├── 01_manifest.json             (machine-readable, SHA-256 checksums)
├── 02_VISION.md                 (FULL .dev-knowledge VISION copy)
├── 03_PLAYBOOK.md               (FULL .dev-knowledge PLAYBOOK copy)
├── 04_ESSENTIALS.md             (FULL .dev-knowledge ESSENTIALS copy)
├── 05_GOVERNANCE_ESSENCES.md    (ADR essences relevant to actions)
├── 06_STATE_OF_PLAY.md          (current state, audit findings)
├── 07_ACTION_PLAN.md            (goals, directives, boundaries)
├── 08_TREE.txt                  (target repo file inventory)
└── 09_EXECUTION_EVIDENCE.md     (return trip template)
```

11 files, single level, drag-drop ready.

### Content principles

**Invariants** (FULL copies, never curated):
- VISION.md — ecosystem context
- PLAYBOOK.md — HOW we work (preserves methodology, conversation
  consistency)
- ESSENTIALS.md — high-leverage rules

Rationale: research consensus (SECI externalization) plus Rob's
explicit requirement that conversational style + engineering
principles persist across sessions.

**Operational essences** (NOT full copies):
- ADR essences in 05_GOVERNANCE_ESSENCES.md cover only ADRs whose
  rules drive specific actions in the current handoff
- Format: 2-3 sentence operational rule + reference to full ADR
- Example: "ADR-33: VISION.md frontmatter must include version, tier,
  owner, last_reviewed, scale. Required sections: Mission, Scope,
  Methodology, Lifecycle, Relationships."

**Project artifacts** (NOT included):
- Target repo's own ADRs — Browser-2 reads in repo if relevant
- Target repo's own VISION/PLAYBOOK/CHANGELOG — Browser-2 reads in repo

### Question pipeline (Stage 1 → Stage 2)

Standardized 5-question SBAR/I-PASS hybrid in HANDOFF_QUESTION_TEMPLATE:

1. **OBJECTIVE** — what is the immediate goal of this transition
2. **REALITY** — current state, dependencies, constraints
3. **RATIONALE** — what was considered + discarded, why
4. **DIRECTIVES** — exact sequential actions
5. **BOUNDARIES** — what must NOT be done, fallback contingencies

Plus receiver synthesis prompt embedded — Browser-2 must summarize
understanding before acting.

### Drift mitigation

- 01_MANIFEST.md captures target repo HEAD SHA + branch + timestamp
- 01_manifest.json contains SHA-256 of every file in handoff folder
- Browser-2 first action: verify HEAD SHA matches via
  `git rev-parse HEAD` in target repo
- Mismatch → STOP, report drift, do not proceed
- Stage 3 re-fetches HEAD SHA at folder generation time (handles
  Stage 2 → Stage 3 drift)

### Return trip (09_EXECUTION_EVIDENCE.md)

Browser-2 / Claude Code in target repo fill out post-execution:
- Raw stdout from commands run
- Test results (pytest output)
- git diffs of changes made
- Final HEAD SHA after work
- Failures or partial completions explicit

Eliminates "Self-Correction Theatre" (Gemini insight) — next
session uses hard evidence to verify state.

### ADR-32 §4 deprecation

ADR-32 §4 "Pending — next session candidates" is DEPRECATED in
favor of:
- BACKLOG.md as canonical pending items source (per ADR-41)
- Handoff Future State (07_ACTION_PLAN.md) references BACKLOG
  items, not duplicates

ADR-32 §1-§3 (folder format basics) preserved but extended by ADR-42.

### ADR-37 integration

Two-phase Current/Future framing preserved:
- 06_STATE_OF_PLAY.md = Current State (per ADR-37)
- 07_ACTION_PLAN.md = Future State (per ADR-37)
- ADR-37 enforcement levels (STRONG for audit, MEDIUM for session)
  apply to handoff types

### ADR-41 integration

BACKLOG.md is canonical source of truth for pending items.
Handoffs reference BACKLOG entries, never duplicate the queue.

### Universalization

- **Mandate**: `.dev-knowledge` follows v3.0 for all handoffs going
  forward
- **Migration**: existing v2.0 handoffs (e.g., 2026-04-30-ai-council-
  audit-sync) regenerated using v3.0 in same session as ratification
- **Recommendation**: child repos with own handoff needs (corp-monorepo
  L tier) follow v3.0 pattern

### Lifecycle entries (per ADR-39)

New files registered in ADR-39 registry (separate amendment in
follow-up session — for now, capture as P3 BACKLOG item):
- HANDOFF_PROCESS.md (already registered, version bumped)
- templates/HANDOFF_QUESTION_TEMPLATE.md (NEW)
- templates/HANDOFF_FOLDER_TEMPLATE.md (NEW)

## Consequences

### Positive
- Browser-2 receives complete methodology + ecosystem context
  (conversation continuity preserved)
- Single upload (zip) for handoff folder — no friction
- Standardized 5-question pipeline replaces hand-crafted summaries
- Drift mitigation via SHA-256 + HEAD pin
- Three-stage flow leverages distinct strengths: Browser-1 (template
  + ecosystem context), Browser-2 (project intelligence), Claude
  Code (reconciliation + execution)
- Return trip closes loop with hard evidence

### Negative
- ~11 files per handoff feels heavy (vs ad-hoc); maintenance burden
  on Browser-1
- Stage 2 manual step (paste back-and-forth) introduces drift window
  Stage 2 → Stage 3
- Full VISION/PLAYBOOK copies = larger handoff bundle (token cost,
  per Rob's directive accepted)
- Three-stage flow requires Browser-2 architect availability for all
  handoff types; no graceful Stage 2 bypass

### Follow-ups
- ADR-39 amendment to register HANDOFF_QUESTION_TEMPLATE and
  HANDOFF_FOLDER_TEMPLATE (P3 BACKLOG)
- Browser-2 test of regenerated ai-council handoff (validates v3.0
  end-to-end)
- Empirical refinement based on Browser-2 friction observations
- Per Rob's "more now, optimize later" directive — reduce file count
  if real friction surfaces

## References

- transcripts council_out_20260509_144836_research_question-how-should-an-llm-driven-solo-developer-a.md
- ADR-32 (handoff process v2.0)
- ADR-37 (session boundary protocol)
- ADR-39 (file lifecycle governance)
- ADR-41 (cross-session backlog architecture)
