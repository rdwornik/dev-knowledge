# Handoff Stage 1: dev-knowledge (session-sync)

<!-- scope: hybrid -->

| Field | Value |
|---|---|
| Target repo | `.dev-knowledge` |
| Repo path | `C:\Users\1028120\Documents\Dev\.dev-knowledge` |
| HEAD SHA (Stage 1) | `328ded75b3a64b4191fca1fe418374671a120a14` |
| Branch | `main` |
| Working tree | clean |
| Slug | `2026-05-25-dev-knowledge-session-sync` |
| Type | session-sync |
| Stage 1 timestamp | 2026-05-25 |

════════════════════════════════════════════════════════════════════
SECTION A — INSTRUCTIONS FOR ROB (do NOT paste this into old chat)
════════════════════════════════════════════════════════════════════

1. Open the EXISTING (OLD) browser chat for `.dev-knowledge` — the chat being
   wrapped up. NOT a new chat. (If there is no prior browser chat for this repo,
   use the most recent ai-council/architect chat that carries `.dev-knowledge`
   context; if none exists this is a bootstrap and Stage 2 will be thinner.)
2. Copy from the PASTE_BOUNDARY line below to the end of this file.
3. Paste as a message in the existing chat.
4. The old chat answers the 5 pipeline questions from its lived knowledge.
5. Open the pre-created file:
   `docs/handoffs/in-progress/2026-05-25-dev-knowledge-session-sync/stage2-response.md`
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

# Stage 2 — Answer These Questions: dev-knowledge (session-sync)

## Your role

You are the existing browser chat for **`.dev-knowledge`**, currently being
wrapped up because your context is getting full. Claude Code in `.dev-knowledge`
is preserving your accumulated knowledge as a structured handoff before this
chat closes.

Your role for this Stage 2 response: **project-level architect for `.dev-knowledge`**.
You provide:
- Goal judgment (what next session should achieve, why)
- Project state YOU witnessed in this conversation (not general knowledge
  inferred from training)
- Reasoning and criteria for decisions (how to think about priority calls,
  deferrals, scope boundaries)
- Do-not lists that come from project context (gotchas, scope boundaries
  you know matter)

You are NOT:
- An oracle for ecosystem-wide conventions (`.dev-knowledge` structure, ADR
  schemas, cross-repo patterns) — the bundle carries these
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
you didn't witness. If you don't know a specific (a commit message, a
file name, a version number, a config value): say "Unknown — Stage 3
should verify."

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
- **List items inline at first mention.** No forward-references. Provide
  representative state, not an exhaustive log.
- **Inline a 1-sentence summary only for files NOT already in the bundle.**
  Files already in the bundle (VISION, PLAYBOOK, ESSENTIALS, essences of
  cited ADRs) need no inline summary.
- **No external citations not in the bundle.** Concepts can be stated as
  reasoning; citations cannot.
- **Write about the work, not the meta-process of handing it off.**

**Audience-simulation check (do before submitting):** mentally simulate a
fresh LLM session reading ONLY the bundle. For each paragraph, ask: would
this be comprehensible without external context? If any paragraph fails,
rewrite it. Per the Universal Self-Containment Rule, default expectation is
zero cross-repo content; only unclosed threads that genuinely could not
close belong in REALITY, framed "unclosed thread, awareness only";
DIRECTIVES never target other repos (corp-monorepo, ai-council, etc.).

### 3. Coherence check

Before submitting, verify: no DIRECTIVE violates own BOUNDARIES; the
OBJECTIVE's top priority aligns with DIRECTIVE #1; no directive depends
on data not packaged in the bundle. Revise before submitting if any fails.

### 4. Format requirements

Your response will be copy-pasted verbatim into stage2-response.md for
Stage 3 parsing.

**Copy-paste note:** chat UIs sometimes strip `#` markdown markers. The
Stage 3 parser is TOLERANT and accepts multiple heading formats. Use ANY of:
`### 1. OBJECTIVE`, `**1. OBJECTIVE**`, or plain `1. OBJECTIVE`. If unsure
which survives your client's copy-paste, use both: `### **1. OBJECTIVE**`.

**Required:**
- No preamble before first heading ("Here's my response:", "Sure:")
- No closing remarks after final BOUNDARIES content
- All 5 sections required, in order: OBJECTIVE / REALITY / RATIONALE /
  DIRECTIVES / BOUNDARIES
- Each section heading uses exact section name (case-sensitive)
- No extra top-level sections beyond the 5 required
- Do NOT wrap the ENTIRE response in a code fence

## Current state (verified at Stage 1 by Claude Code)

- HEAD: `328ded75b3a64b4191fca1fe418374671a120a14`
- Branch: `main`
- Working tree: clean
- Recent context: The last recorded session (2026-05-25) received a stale
  2026-05-24 handoff prompt that proposed an 11→4 handoff-bundle consolidation
  plus resolution of six 2026-05-20 audit findings (labelled M-1, M-2, M-3,
  M-5, M-6, L-3). The prompt's premise was found broken on verification — its
  11→4 file-mapping table named bundle files that do not exist in the repo, and
  collapsing 11→4 would silently drop the full VISION/PLAYBOOK/ESSENTIALS
  invariant copies and the SHA-256 manifest (the direction ADR-45 explored and
  rolled back). Operator chose "audit fixes only, re-scope consolidation
  separately." The genuine audit residuals were resolved across 5 commits and
  merged to `main` (merge commit `328ded7`): `/handoff` version label aligned to
  v3.3.3 in CLAUDE.md (M-1); residual CHANGELOG references struck from Stage 3
  in HANDOFF_PROCESS.md + HANDOFF_FOLDER_TEMPLATE.md (M-3); Stage 2 thinness
  pre-flight check added to HANDOFF_PROCESS.md (M-5); ADR-45 supersession claim
  withdrawn (M-2); handoff templates registered in ADR-39 (M-6); and the
  `_in_progress` → `in-progress` directory rename landed (commit `05b9e36`).
  `pytest` 72 passed and `ruff` clean throughout.

## .dev-knowledge BACKLOG items relevant to dev-knowledge

The handoff bundle does not include BACKLOG.md; these are listed so you can
weigh them when proposing the next session's objective. (The bundle's new chat
will read the live BACKLOG.md in-repo; do not duplicate the queue in your
answer — reference items by name.)

Open items most relevant to a `.dev-knowledge` self-session, by priority:

- **[P1] Codify scrum-master review authority pattern** — N=3 grounding reached
  (codification unblocked); flagged as top P1 of the next execution wave. New
  ADR or ADR-26 amendment.
- **[P1] Sacred-files maintenance enforcement** — canonical-file staleness
  enforcement mechanism (pre-commit / SessionStop hook / CI age check).
- **[P1] Council decisions management consolidation** — remaining sub-items:
  contradiction-detection mechanism + ownership model for decision evolution.
- **[P2] Lessons activation P1 implementation** — lessons-index.json + retrieval
  (SessionStart hook) + CLI per ADR-35.
- **[P2] ESSENTIALS.md cheat-sheet additions for ADRs 35-54** — needs pruning or
  explicit relaxation of the 1-page constraint.
- **[P2] Hooks audit + consolidation + workflow-automation patterns** — operator
  focus area; no SessionStop hook currently exists.
- **[P3] CLAUDE.md §4 cites a stale known-failing test** — one-line edit; §4
  names `test_audit_run_passes_structural_checks_on_synthetic_repo` as a known
  failure but it passes (suite green, 72 passed). Cheap quick win.
- **[P3] ADR relationship index / supersession graph** — navigability of 27+ ADRs.
- **[P3] PLAYBOOK codifications from 2026-05-19 posture audit** — 4 candidate
  additions, each N≥2.
- **[P3] ADR-39 registry decision — non-handoff template class** — register vs
  exempt vs hybrid for the remaining (non-handoff) templates.
- **[P3] ADR-39 / ADR-41 grouped amendments** — BACKLOG.md lifecycle entry; ADR-41
  cross-reference to ADR-47.
- **[P3] LESSONS.md parenthetical-qualifier entries escape dated-entry regex** —
  operator decision (regex broaden vs entry reformat).

Open thread from the last session (not yet a BACKLOG item): whether the 11→N
handoff-bundle consolidation is still wanted — and if so, it needs a
reality-based design plus an explicit decision to re-open ADR-45 (drop or keep
the full invariant copies). This is methodology change, not hygiene.

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

What is the immediate goal of the next `.dev-knowledge` session?

State the single highest-priority objective you would set, and why. If you
believe the next session should pick up a specific BACKLOG item (e.g. codifying
the scrum-master review authority pattern, sacred-files enforcement, or the
handoff-consolidation re-scope), name it and say why it ranks above the others.
If you'd rather the session start by grooming/deciding rather than building,
say so.

*Epistemic note: state your goal judgment confidently. If a BACKLOG item's
framing feels wrong to you, say so with reasoning.*

### 2. REALITY

What is the current state of `.dev-knowledge` from your perspective?

- Was anything completed in the recent session arc that the next session must
  build on or not re-do?
- Any work in progress not reflected in committed state?
- Any unclosed decision threads (e.g. the handoff-consolidation / ADR-45
  question) that need an operator call before work proceeds?
- Any constraints (conventions, append-only / immutable file rules, the
  Layer-2-never-executes invariant) the next session must respect?

*Epistemic note: differentiate witnessed events from inferences from unknowns.
Mark inferences "(architect inference)" and unknowns "Unknown — verify against
repo."*

### 3. RATIONALE

If you witnessed reasoning that shaped recent `.dev-knowledge` work and the next
session needs to understand it, describe it. If not, write "Unknown — no
specific rationale witnessed in this session" and skip the sub-questions below.

Candidate topics (answer only those you actually witnessed; for any you did
not, write "Unknown — Stage 3 verifies against the commit / ADR"):
- If you witnessed the reasoning for rejecting the 11→4 bundle consolidation
  (vs. proceeding with it), state it.
- If you witnessed why ADR-45's supersession-of-ADR-42 claim was withdrawn
  rather than kept, state it.
- If you witnessed why the audit residuals were split from the consolidation
  into a separate scope, state it.

*Epistemic note: reasoning is your strong suit — explain judgment you witnessed.
"Unknown — Stage 3 verifies against the commit / ADR" is acceptable and
preferred over a constructed rationale.*

### 4. DIRECTIVES

What are the exact sequential actions the next `.dev-knowledge` session should
execute?

Provide a numbered list. Each action: **action verb + target + verification step**.
A reasonable default sequence, given the open threads, would be: (1) obtain the
operator decision on whether the handoff consolidation is still wanted; (2) if
not, pick the highest-value unblocked BACKLOG item (the scrum-master review
codification is the named top P1); (3) knock out the cheap CLAUDE.md §4 stale-test
fix opportunistically. Add, remove, or reorder as you see fit.

*Epistemic note: action sequence and verification steps are most valuable.
Specific file paths or commit messages — mark "(architect inference)" if not
witnessed; Stage 3 may revise based on repo state.*

### 5. BOUNDARIES

What must the next session NOT do? What are fallback contingencies?

Consider at minimum: do not collapse the handoff bundle (drop the full
VISION/PLAYBOOK/ESSENTIALS invariant copies or the SHA-256 manifest) without an
explicit ADR-45 re-opening decision; do not edit append-only files
(LESSONS.md, TOKEN-LOG.md) or immutable files (ADRs, transcripts, handoffs,
audits) in place; do not add orchestration scripts (Layer 2 executes nothing);
do not generate reconciliation reports about other repos' state via this repo's
own work. Add any architect-specific "do not's" grounded in what you know.

*Epistemic note: do-not lists grounded in your project knowledge are very
valuable. Don't fabricate "do not touch X" if you don't know whether X exists.*

════════════════════════════════════════════════════════════════════
End of paste block.
Old chat: please answer questions 1-5 above following the Format
requirements above. Structure response with the exact headings
(OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES) so
Claude Code can parse them at Stage 3.
════════════════════════════════════════════════════════════════════
