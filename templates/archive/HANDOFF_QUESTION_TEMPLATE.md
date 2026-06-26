<!-- ARCHIVED 2026-06-26 — the flat v3.4 two-phase "Stage 1 Question" template, superseded by the v5 handoff template set `templates/handoff/**` (its interview function now lives in `templates/handoff/v5/SUPPLEMENT.md.tmpl`, ADR-82). Per the ADR-83 (protocols) / ADR-60 (docs) archive convention. The live v5 template set is `templates/handoff/**`; this flat template is retired (not read by the v5 `/handoff` command). -->

# Handoff Stage 1 Question Template

<!-- scope: meta -->

This template generates `stage1-question.md` files. It has TWO distinct
sections that must remain visually separated for different audiences:

- **Section A (Rob's operational instructions)** — what Rob does with the
  file. Rob reads this. Rob does NOT paste this into the old chat.
- **Section B (paste-this block)** — the actual message Rob copies into the
  old browser chat for the architect to answer.

The `PASTE_BOUNDARY` delimiter line makes this separation explicit. Rob selects
from PASTE_BOUNDARY down to end of file when copying into old chat.

**Audience-routing invariant (critical — see audit 2026-05-29 B2):** EVERY
artifact the architect must produce or review (the 5 pipeline sections,
`next_session_scope`, `11_CLAIMS.md` content, the gate-probe accuracy review)
MUST be requested *inside* Section B (the paste block). Section A is
operator-only; the architect never sees it. A required architect artifact that
is mentioned only in Section A cannot be complied with — that is exactly the
failure that aborted the first v3.4 run. Section A may *remind Rob* that these
outputs are expected, but the actual request to the architect lives in Section B.

**Three-actor flow (per ADR-42, amended four times):**
- Stage 2 source = OLD browser chat for {repo} (existing chat being wrapped up)
- Stage 3 receiver = NEW browser chat for {repo} (fresh, opened after folder generated)
- Claude Code = orchestrator throughout

**Note on receiver synthesis prompt:** The synthesis prompt belongs in
`00_first-message.md` (Stage 3 output). It is NOT included in stage1-question.md.

---

## Stage 1 output structure (Claude Code generates this)

When Claude Code generates `stage1-question.md` from this template, the output
file must follow this structure:

```
# Handoff Stage 1: {repo} ({type})

[METADATA HEADER — repo path, HEAD SHA, branch, working tree, slug, timestamp,
 type. Rob references this; old chat doesn't need it but receiving it is harmless.]

════════════════════════════════════════════════════════════════════
SECTION A — INSTRUCTIONS FOR ROB (do NOT paste this into old chat)
════════════════════════════════════════════════════════════════════

1. Open the EXISTING (OLD) browser chat for {repo} — the chat being
   wrapped up. NOT a new chat.
2. Copy from the PASTE_BOUNDARY line below to the end of this file.
3. Paste as a message in the existing chat.
4. The old chat answers the 5 pipeline questions from its lived knowledge.
5. Open the pre-created file: docs/handoffs/in-progress/{slug}/stage2-response.md
   (already exists, has placeholder content). Replace everything below the
   "═══ REPLACE EVERYTHING BELOW THIS LINE ═══" marker with the architect's
   response (the 5 pipeline sections). Save.
   - The paste block also asks the architect for two more outputs (requested in
     Section B, not here): a `next_session_scope` line and the `11_CLAIMS.md`
     claims tables. Save the claims content into the pre-created
     docs/handoffs/in-progress/{slug}/stage2-claims.md. (Reminder only — the
     architect receives the actual instructions in the paste block.)
6. In Claude Code at .dev-knowledge, say: "complete handoff for {repo}"
   → Stage 3 generates the final handoff folder.
7. After Stage 3: close the old chat. Open a NEW claude.ai chat for {repo}
   and use the Stage 3 folder bundle (00_README.md inside has upload
   instructions for the new chat).

════════════════════════════════════════════════════════════════════
PASTE_BOUNDARY — copy from here to end of file into the old chat
════════════════════════════════════════════════════════════════════

# Stage 2 — Answer These Questions: {repo} ({type})

## Your role

You are the existing browser chat for **{repo}**, currently being wrapped up
because your context is getting full. Claude Code in `.dev-knowledge` is
preserving your accumulated knowledge as a structured handoff before this
chat closes.

Your role for this Stage 2 response: **project-level architect for {repo}**.
You provide:
- Goal judgment (what next session should achieve, why)
- Project state YOU witnessed in this conversation (not general knowledge
  inferred from training)
- Reasoning and criteria for decisions (how to think about tier choice,
  priority calls, deferrals)
- Do-not lists that come from project context (gotchas, scope boundaries
  you know matter)
- A `next_session_scope` declaration, a structured `11_CLAIMS.md` grounding of
  your load-bearing claims, and an accuracy review of the gate probe (the three
  v3.4 outputs specified after the 5 pipeline questions below)

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

### 2. Self-containment for a bundle-only audience

**Principle:** the new chat sees ONLY the Stage 3 bundle. It does not see
this Stage 1 question, prior browser conversations, JOURNAL entries, or
external research. Every claim in your response must be comprehensible
from the bundle alone.

The bundle contains: full `.dev-knowledge` VISION.md, PLAYBOOK.md, and
ESSENTIALS.md; ADR essences for ADRs cited in directives; the audit
report; the repo state snapshot.

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
  Files already in the bundle (the repo's and ecosystem's VISION,
  PLAYBOOK, ESSENTIALS, and the essences of cited ADRs) need no inline
  summary — the new chat will read them.
  - NOT: "v1 conflicted with audit findings"
  - DO: "v1 (which proposed dropping full invariants from the bundle)
    conflicted with the 2026-05-12 audit finding that the full
    11-file bundle empirically catches architect fabrications via
    drift detection (real case: 2026-05-09 ai-council handoff)"

- **No external citations not in the bundle.** Paper titles, blog posts,
  arxiv IDs, vendor blogs — none are in the bundle and the new chat
  cannot verify them. Concepts can be stated as reasoning; citations
  cannot.

- **Write about the work, not the meta-process of handing it off.** Do
  not describe the new chat as "the test subject" or frame the handoff
  as "an empirical test" unless that framing drives a receiver-side
  action.

**Audience-simulation check (do this before submitting):** mentally
simulate a fresh LLM session reading ONLY the Stage 3 bundle. For each
paragraph of your response, ask: would this be comprehensible without
reaching for external context? If any paragraph fails, rewrite it.
Cross-repo content fails this check — per the Universal Self-Containment
Rule in HANDOFF_PROCESS, default expectation is zero cross-repo content;
only unclosed threads that genuinely could not close belong in REALITY,
framed as "unclosed thread, awareness only"; DIRECTIVES never target
other repos.

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

- HEAD: {head_sha}
- Branch: {branch}
- Working tree: {working_tree_state}
- Recent context: {recent_commits_or_work_summary}

## Audit context (informational — extend or correct in your response)

{audit_findings_summary_if_audit_sync}

## .dev-knowledge BACKLOG items relevant to {repo}

{relevant_backlog_items}

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

What is the immediate goal of the next {repo} session?

{customized_objective_prompt}

*Epistemic note: state your goal judgment confidently. If audit's suggested
actions feel wrong to you, say so with reasoning.*

### 2. REALITY

What is the current state of {repo} from your perspective?

- Was anything completed since {last_known_milestone}?
- Any work in progress not reflected externally?
- External dependencies (services, libraries, partner repos) currently in play?
- Any constraints (deadlines, conventions) the next session must respect?
- {any_specific_state_question_from_stage1_observation}?

*Epistemic note: differentiate witnessed events (you saw this in conversation)
from inferences (reasoning from context) from unknowns (no direct knowledge).
Mark inferences with "(architect inference)" and unknowns with "Unknown —
verify against repo."*

### 3. RATIONALE

If you witnessed reasoning that shaped recent {repo} work and the next
session needs to understand it, describe it. If not, write "Unknown — no
specific rationale witnessed in this session" and skip the sub-questions
below.

{customized_rationale_prompt_with_repo_specific_decisions}

*Epistemic note: reasoning is your strong suit — explain your judgment
when you witnessed it. For any sub-question below, the answer "Unknown —
Stage 3 verifies against the commit / ADR" is acceptable and preferred
over a constructed rationale. For any specific facts in your reasoning
(file counts, timing, component names), mark "(architect inference)" if
not directly witnessed.*

### 4. DIRECTIVES

What are the exact sequential actions the next {repo} session should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

{default_proposal_from_audit_or_session_goals}

Add, remove, or reorder as you see fit.

*Epistemic note: action sequence and verification steps are most valuable.
Specific file paths or commit messages — mark "(architect inference)" if not
witnessed; Stage 3 may revise based on repo state.*

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

{default_boundaries_from_audit_deferrals_and_general_scope}

Add any architect-specific concerns or "do not's."

*Epistemic note: do-not lists grounded in your project knowledge are very
valuable. Don't fabricate "do not touch X" if you don't know whether X exists
— focus on knowns from your conversation.*

## Additional required Stage 2 outputs (v3.4 — do these too)

Beyond the 5 pipeline sections above, the v3.4 handoff process needs three more
things from you. These are NOT optional — Stage 3 cannot complete the bundle
without the first two, and the third keeps you available for one quick check.

### A. Declare `next_session_scope` (per ADR-57)

State which ONE scope best describes the next session's work, from this
controlled vocabulary (this selects which operational artifacts — skills,
gotchas, JOURNAL slices — get bundled):

- `code-implementation` — writing/changing code in the target repo
- `architecture-decision` — ADR-level design, governance, or process decisions
- `audit-work` — auditing, reviewing, or verifying existing artifacts
- `documentation` — authoring or revising docs/specs/templates
- `mixed-uncertain` — spans several / not yet clear (fail-safe → treated as
  worst-case, bundles the full operational layer)

Write it as a single line, e.g.: `next_session_scope: architecture-decision`.
If genuinely unsure, choose `mixed-uncertain` — do not guess narrowly.

### B. Produce `11_CLAIMS.md` content (per ADR-58) — your FINAL output

After the 5 sections, list your **load-bearing claims** — the decision-affecting
factual assertions in your response (file paths, commit SHAs, ADR refs, action
sequencing, architecture descriptions, current-state assertions). Reasoning,
recommendations, and clearly-marked opinions are NOT load-bearing and need no
citation. **Trigger rule:** a confident claim about an unread/unverified source
requires a citation OR an explicit assumption marker.

Use this structure (Claude Code saves it to `stage2-claims.md`, which becomes
`11_CLAIMS.md` in the bundle; Claude Code then validates every citation against
the repo at Stage 3):

```
## Load-bearing claims

| # | Claim | Source citation | Verifier |
|---|-------|-----------------|----------|
| 1 | {claim} | `file:section` / `ADR-NN` / `session: YYYY-MM-DD` | self / CC / operator |

## Explicit assumptions

| # | Assumption | Risk if wrong | Mitigation |
|---|-----------|---------------|------------|
| 1 | {assumption} | {consequence} | {guard} |

## Expected articulation (sender contract)

{2-4 sentences: what the receiving NEW chat should correctly understand from
this handoff — lets the operator ratify even after this chat has closed}
```

Produce this LAST, after the 5 sections are settled. If you revise a section in
a way that changes a load-bearing claim, update this table to match.

### C. Be ready to review the gate probe (per ADR-55)

At Stage 3, Claude Code will draft a `10_GATE_PROBE.md` — a mini-scenario whose
correct answer is determined by this handoff's content, used to test that the
NEW chat can *apply* the bundle (not just paraphrase it), drawn from the
**highest-risk live decision** in your handoff. While this OLD chat is still
open, the operator may route that draft back to you for an **accuracy review**:
confirm the scenario reflects a real high-risk decision and the operator-only
expected answer is correct per what you witnessed — or correct it. You do not
author the probe; you check it. (If this chat has closed by then, the operator
reviews it directly.)

════════════════════════════════════════════════════════════════════
End of paste block.
Old chat: please answer questions 1-5 above following the Format
requirements above. Structure response with the exact headings
(OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES) so
Claude Code can parse them at Stage 3. Then add the three v3.4 outputs:
`next_session_scope`, the `11_CLAIMS.md` claims tables, and your
readiness to review the gate probe.
════════════════════════════════════════════════════════════════════
```

---

## Generation rules for Claude Code

- Replace all `{placeholders}` with actual values from repo state + audit context
- **Section B order is fixed:** role → bundle → "How to write the response"
  (epistemic / self-containment / coherence / format) → current state →
  audit context → BACKLOG → pipeline questions → **additional required Stage 2
  outputs** (scope / claims / gate-probe review, per ADR-57/58/55) → end
  divider. The response-writing guidance MUST appear before audit context and
  questions — old chat must read these BEFORE drafting response.
- **Preserve 5 question headings exactly:** `### 1. OBJECTIVE`, `### 2. REALITY`,
  `### 3. RATIONALE`, `### 4. DIRECTIVES`, `### 5. BOUNDARIES`. Stage 3 parses these.
- **Audience-routing invariant (v3.4 — audit 2026-05-29 B1/B2):** the three v3.4
  outputs — `next_session_scope` (ADR-57), the `11_CLAIMS.md` claims content
  (ADR-58), and the gate-probe accuracy-review note (ADR-55) — MUST be generated
  INSIDE the paste block (Section B), in the "Additional required Stage 2
  outputs" section. They may be *echoed* as a reminder in Section A for Rob, but
  the actual request to the architect must live in Section B. A required
  architect artifact placed only in Section A reproduces the abort that halted
  the first v3.4 run. Include the controlled scope vocabulary and the claims
  table schema inline so the architect never has to guess.
- **RATIONALE sub-questions must not presuppose answers.** A phrasing like
  "Why was X done?" or "Why was Y deferred?" assumes the architect did X
  or chose to defer Y, and pulls them toward constructing a rationale —
  the exact failure the epistemic-honesty section forbids. Generate
  sub-questions in the form: *"If you witnessed the reasoning for X,
  state it; otherwise mark Unknown — Stage 3 verifies against the
  commit / ADR."* This applies whether the candidate X comes from audit
  findings, recent commits, or BACKLOG items.
- Section A and Section B separated by visible `PASTE_BOUNDARY` line with thick `═`
  characters — visually unmistakable even when scrolling
- **DO NOT include receiver synthesis prompt** in stage1-question.md. It belongs
  in Stage 3 output (`00_first-message.md`, per HANDOFF_FOLDER_TEMPLATE)
- Metadata header (HEAD, branch, working tree) goes ABOVE Section A
- For audit-sync: populate `{audit_findings_summary}` with categorized findings;
  customize question prompts with audit-suggested defaults labeled "revise as needed"
- For session-sync: populate from recent git log + BACKLOG context
- **Pre-create `stage2-response.md` template** alongside stage1-question.md in the
  same Stage 1 commit (per HANDOFF_PROCESS Stage 1 procedure)
- **Pre-create `stage2-claims.md` placeholder** in the same folder and Stage 1
  commit, so the architect's `11_CLAIMS.md` save target exists (per ADR-58; the
  architect produces this as the FINAL Stage 2 output)
