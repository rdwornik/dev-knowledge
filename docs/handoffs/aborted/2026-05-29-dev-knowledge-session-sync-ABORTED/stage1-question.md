# Handoff Stage 1: dev-knowledge (session-sync)

| Field | Value |
|---|---|
| Target repo | `.dev-knowledge` (self-handoff) |
| Repo path | `C:\Users\1028120\Documents\Dev\.dev-knowledge` |
| HEAD SHA | `5582cf544fab2b4236e7d292d5506ce85ad63c55` |
| Branch | `main` (Stage 1 work on `docs/handoff-2026-05-29-session-sync`) |
| Working tree | clean (verified at Stage 1 capture) |
| Slug | `2026-05-29-dev-knowledge-session-sync` |
| Type | session-sync |
| Timestamp | 2026-05-29 |
| Process | HANDOFF_PROCESS v3.4 |

════════════════════════════════════════════════════════════════════
SECTION A — INSTRUCTIONS FOR ROB (do NOT paste this into old chat)
════════════════════════════════════════════════════════════════════

1. Open the EXISTING (OLD) browser chat for `.dev-knowledge` — the chat being
   wrapped up. NOT a new chat. (If no single OLD chat exists for this repo, use
   the most recent ai-council architect chat that carries `.dev-knowledge`
   governance context — see HANDOFF_PROCESS "Three actors" note.)
2. Copy from the PASTE_BOUNDARY line below to the end of this file.
3. Paste as a message in the existing chat.
4. The old chat answers the 5 pipeline questions from its lived knowledge.
5. Open the pre-created file:
   `docs/handoffs/in-progress/2026-05-29-dev-knowledge-session-sync/stage2-response.md`
   (already exists, has placeholder content). Replace everything below the
   "═══ REPLACE EVERYTHING BELOW THIS LINE ═══" marker with the architect's
   response. Save.
   - The architect should ALSO declare `next_session_scope` (one of:
     `code-implementation` / `architecture-decision` / `audit-work` /
     `documentation` / `mixed-uncertain`) and produce `11_CLAIMS.md` content —
     save that to `stage2-claims.md` in the same folder (ADR-57 / ADR-58).
6. In Claude Code at `.dev-knowledge`, say: "complete handoff for dev-knowledge"
   → Stage 3 generates the final handoff folder.
7. After Stage 3: close the old chat. Open a NEW claude.ai chat for
   `.dev-knowledge` and use the Stage 3 folder bundle (00_README.md inside has
   upload instructions for the new chat).

════════════════════════════════════════════════════════════════════
PASTE_BOUNDARY — copy from here to end of file into the old chat
════════════════════════════════════════════════════════════════════

# Stage 2 — Answer These Questions: dev-knowledge (session-sync)

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
- Reasoning and criteria for decisions (how to think about priority calls,
  deferrals, sequencing)
- Do-not lists that come from project context (gotchas, scope boundaries
  you know matter)

You are NOT:
- An oracle for ecosystem-wide conventions (.dev-knowledge structure, ADR
  schemas, cross-repo patterns) — the bundle carries these
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
- ADR essences (operational rules) for ADRs cited in your directives
- Repo state snapshot (HEAD, branch, file tree, working tree state)
- A scoped operational layer (skills / gotchas / JOURNAL slice) selected from
  your declared `next_session_scope` (ADR-57)

You do NOT need to:
- Explain what ADR-NN mandates (handoff has the essence)
- Specify HEAD SHA or working tree state (handoff has the manifest)
- Describe ecosystem governance patterns (handoff has VISION + PLAYBOOK)

Focus on what only YOU witnessed or judged in this conversation.

## How to write the response (read before drafting)

Four concerns govern your response. Apply them during drafting, not as a
final-pass edit.

### 1. Epistemic honesty

For each claim, classify it:
- **Witnessed**: you saw this happen in conversation — state it confidently
- **(architect inference)**: reasoning from context, not direct observation —
  mark it inline
- **Unknown**: you don't have direct knowledge — say so, write "Unknown —
  Stage 3 verifies against the commit / ADR / repo"

LLMs default to "be helpful" by filling gaps with plausible specifics. Resist
this. Stage 3 verifies factual claims against the repo. Your value is judgment
and reasoning, not confident fabrication of facts you didn't witness.

### 2. Self-containment for a bundle-only audience

The new chat sees ONLY the Stage 3 bundle — not this question, not prior
browser conversations, not JOURNAL entries. Every claim must be comprehensible
from the bundle alone.

- **Per-section scope declaration.** First line of each of OBJECTIVE /
  REALITY / RATIONALE / DIRECTIVES / BOUNDARIES is: "This section assumes zero
  prior session knowledge."
- **No references the new chat cannot resolve.** No "Stage 1 above", no
  session-internal terms. Generalize to "during a recent extended session" or
  "in the work culminating in commit `5582cf5`".
- **List items inline at first mention.** No forward-references; representative
  state, not an exhaustive log.
- **Inline a 1-sentence summary only for files NOT already in the bundle.**
- **No external citations not in the bundle** (paper titles, blog posts, arxiv
  IDs). Concepts can be stated as reasoning; citations cannot.
- **Cross-repo content fails the self-containment check.** Per the Universal
  Self-Containment Rule: default expectation is ZERO cross-repo content.
  DIRECTIVES never target another repo's files or BACKLOG. If a cross-repo
  thread genuinely could not close (e.g. the corp-monorepo branch-deletion /
  P1-2 path-traversal extraction noted in recent work), mention it ONCE in
  REALITY framed as "unclosed thread, awareness only, may need follow-up —
  other-repo hygiene is their session work per ADR-41." Never as a directive.

### 3. Coherence check

Before submitting: no DIRECTIVE violates own BOUNDARIES; OBJECTIVE's top
priority aligns with DIRECTIVE #1; no directive depends on data not packaged
in the bundle. Revise before submitting if any fails.

### 4. Format requirements

Your response is copy-pasted verbatim into `stage2-response.md` for Stage 3
parsing.

- No preamble before first heading; no closing remarks after final BOUNDARIES
- All 5 sections required, in order: OBJECTIVE / REALITY / RATIONALE /
  DIRECTIVES / BOUNDARIES
- Use ANY heading form that survives your client's copy-paste:
  `### 1. OBJECTIVE`, `**1. OBJECTIVE**`, or plain `1. OBJECTIVE`
- Do NOT wrap the ENTIRE response in a code fence
- Allowed within sections: paragraphs, bullet/numbered lists, **bold**,
  *italic*, `inline code`, tables, blockquotes

**Example correct opening:**
```
### 1. OBJECTIVE
The next session should...
```

## Current state (verified at Stage 1 by Claude Code)

- HEAD: `5582cf544fab2b4236e7d292d5506ce85ad63c55`
- Branch: `main` (working tree clean)
- Recent work summary (from git log + JOURNAL, for your context — do NOT
  restate, Stage 3 has the detail): the most recent session arc (through the
  merge at `5582cf5`) was a sustained universalization push on 2026-05-28:
  (a) ADR-51 v2 mermaid-theme readability fix rolled out across repos plus a
  new `audit.py` check #7 enforcing it; (b) `protocols/AI_COUNCIL_PROCESS.md`
  v1.0 operational runbook authored (closed a P2); (c) first `docs/archive/`
  triage per ADR-60 (7 transcripts promoted); (d) a universalization
  durability + template-completeness audit
  (`docs/audits/2026-05-28-universalization-durability-audit.md`) that found
  7/11 conventions fully durable, closed 3 clear cross-ref gaps (C1 PLAYBOOK,
  C2 ESSENTIALS, C3 CLAUDE.md §11 ADR-list rotation → v2.3), and appended four
  judgment-call gaps to BACKLOG (J1/J4/J5/J6).

## Audit context

Not an audit-sync handoff — no audit report is the driver. The 2026-05-28
durability audit is part of the recent-work summary above; its open follow-ups
appear as BACKLOG items below.

## .dev-knowledge BACKLOG items relevant to next session

High-priority and freshly-added open items (own-repo only; full BACKLOG is in
the repo):

- **[P1] Codify scrum-master review authority pattern** — N=3 empirical
  grounding reached (codification unblocked); flagged as top of next execution
  wave. New ADR or ADR-26 amendment.
- **[P1] Sacred-files maintenance enforcement** — canonical-file staleness;
  enforcement mechanism candidates (pre-commit staleness / session-end
  checklist / CI). Pairs with the handoff mechanical-gate item.
- **[P1] Council decisions management consolidation** — consolidated index
  done; remaining: contradiction-detection mechanism + decision-evolution
  ownership model (both Council-debate territory).
- **[P2] Mechanical gate code for handoff enforcement (ADR-42 Q5)** — the
  executor-side validator + hook wiring deferred by the 2026-05-26 amendment;
  contract defined, code pending. Layer-2 constraint: validator only, no
  orchestration.
- **[P2] J1 — CLAUDE-md-template refresh** (durability-audit judgment gap).
- **[P3] J4 — `audit.py` mermaid-check scope widening**; **J5 — child-repo
  audit reach**; **J6 — new-repo scaffolding starter pack** (durability-audit
  judgment gaps, 2026-05-28).
- **[P3] CLAUDE.md §4 cites a stale known-failing test** — one-line edit;
  `test_audit_run_passes_structural_checks_on_synthetic_repo` actually passes.
- **[P2] Hooks audit + lifecycle-hook workflow-automation patterns** — operator
  focus area; no SessionStop hook today.

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings.

### 1. OBJECTIVE

What is the immediate goal of the next `.dev-knowledge` session?

Several P1 items are unblocked (scrum-master codification, sacred-files
enforcement, Council decisions consolidation) plus a queue of durability-audit
follow-ups (J1/J4/J5/J6) and the deferred handoff mechanical-gate code. Which
ONE goal should the next session pursue first, and why that over the others?

*Epistemic note: state your goal judgment confidently. If a BACKLOG item's
stated priority feels wrong to you, say so with reasoning.*

### 2. REALITY

What is the current state of `.dev-knowledge` from your perspective?

- Was anything completed or decided in this session that is NOT yet reflected
  in committed files (work-in-progress, a decision made but not written down)?
- Any open cross-repo thread that genuinely could not close before this
  handoff? (e.g. the noted corp-monorepo branch-deletion gate / P1-2
  path-traversal extraction.) If so, frame it "unclosed thread, awareness
  only, may need follow-up per ADR-41" — it is NOT a `.dev-knowledge` directive.
- Any constraints (conventions, in-flight branches, operator preferences) the
  next session must respect?

*Epistemic note: differentiate witnessed events from inferences (mark
"(architect inference)") from unknowns (mark "Unknown — verify against repo").*

### 3. RATIONALE

If you witnessed reasoning that shaped recent `.dev-knowledge` work and the
next session needs to understand it, describe it. If not, write "Unknown — no
specific rationale witnessed in this session" and skip the sub-questions.

- If you witnessed the reasoning for sequencing the scrum-master codification
  ahead of (or behind) the other P1 items, state it; otherwise mark Unknown —
  Stage 3 verifies against BACKLOG.
- If you witnessed why the handoff mechanical-gate code was deferred rather
  than built in the session that defined its contract, state it; otherwise
  mark Unknown — Stage 3 verifies against ADR-42 Q5 amendment.
- If you witnessed any judgment about whether the durability-audit J-gaps
  (J1/J4/J5/J6) should be bundled or done singly, state it; otherwise mark
  Unknown.

*Epistemic note: reasoning is your strong suit. For any sub-question, "Unknown
— Stage 3 verifies" is acceptable and preferred over a constructed rationale.*

### 4. DIRECTIVES

What are the exact sequential actions the next `.dev-knowledge` session should
execute?

Provide a numbered list. Each action: **action verb + target + verification
step**. Own-repo actions ONLY — no directive may target another repo's files,
state, or BACKLOG.

A candidate default (revise freely): (1) confirm clean tree + green suite
(`pytest -x --tb=short`, `audit.py health` 7/7); (2) execute the single
OBJECTIVE goal on a feature branch; (3) update BACKLOG status + JOURNAL entry;
(4) run validators (`pre-commit run --all-files`); (5) commit per Conventional
Commits.

*Epistemic note: action sequence and verification steps are most valuable.
Mark file paths "(architect inference)" if not witnessed; Stage 3 may revise.*

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

Candidate defaults grounded in this repo's invariants (extend with your own):
- Do NOT add orchestration scripts — Layer-2 invariant: validators only
  (ADR-28, ADR-36).
- Do NOT edit old `LESSONS.md` / `TOKEN-LOG.md` entries or any
  ADR/transcript/handoff/audit in place — append-only / immutable.
- Do NOT generate reconciliation reports about other repos' state, and do NOT
  treat a staleness observation about another repo's tracking as a directive.
- Do NOT recreate `README.md`, `CHANGELOG.md`, or `BACKLOG_ARCHIVE.md`
  (deliberately deleted).
- Do NOT mix unrelated work into one branch/commit — clean tree before new
  tasks.

*Epistemic note: do-not lists grounded in your project knowledge are very
valuable. Don't fabricate "do not touch X" if you don't know whether X exists.*

════════════════════════════════════════════════════════════════════
End of paste block.
Old chat: please answer questions 1-5 above following the Format requirements
above. Structure response with the exact headings (OBJECTIVE / REALITY /
RATIONALE / DIRECTIVES / BOUNDARIES) so Claude Code can parse them at Stage 3.
════════════════════════════════════════════════════════════════════
