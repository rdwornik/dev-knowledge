# Governance Essences — .dev-knowledge (session-sync) 2026-05-14

<!-- scope: meta -->

ADR essences for ADRs explicitly cited in `07_ACTION_PLAN.md` directives.
These are operational summaries (2-4 sentences each), not full ADR copies.
For full text, see the ADR file in `.dev-knowledge/docs/decisions/`.

---

## ADR-29 — LESSONS.md Grandfathering Under Scope Tagging

New LESSONS.md entries use the inline scope tag format:
`### YYYY-MM-DD | [source] | [lesson] | [category] | [scope: X] | [action taken]`
where `[scope: X]` uses the ADR-27 vocabulary (`dev | llm | hybrid | runtime | meta`).
Existing pre-ADR-27 entries are grandfathered — never retroactively tagged or edited.
The file is append-only; no exceptions to that invariant are created.

Full ADR: `.dev-knowledge/docs/decisions/ADR-29-lessons-grandfathering.md`

---

## ADR-36 — Audit Tool Architecture (.dev-knowledge as ecosystem auditor)

The `.dev-knowledge` audit tool reads child repos read-only and writes only to
`.dev-knowledge/ecosystem/{repo}/` (state.yaml + append-only history) and
`.dev-knowledge/docs/` (audit reports + handoff folders). It never touches child repo files.
Implementation is 4-phase: P1 MVP (CLI scaffold + ecosystem state + markdown report),
P2 (handoff folder generator), P3 (scheduled runs), P4 (LLM-augmented narrative reports).
P1 is the current open BACKLOG item; PLAYBOOK additions for ADR-36 workflow are the prerequisite.

Full ADR: `.dev-knowledge/docs/decisions/ADR-36-audit-tool-architecture.md`

---

## ADR-37 — Session Boundary Protocol (two-phase handoff format)

Every handoff has a Current State (`06_STATE_OF_PLAY.md`) and a Future State (`07_ACTION_PLAN.md`)
as the two authoritative operational sections; the ADR-32 9-section structure sits beneath as
reference evidence under "Detailed Context". If there is a contradiction between the top-level
summary and the detailed sections, the top-level wins as operational source of truth.
For session handoffs, Future State must be present but may explicitly state "undetermined" with
a written justification; unjustified absence is invalid.

Full ADR: `.dev-knowledge/docs/decisions/ADR-37-session-boundary-protocol.md`

---

## ADR-40 — Scale Tier Evaluation Algorithm

Repos are classified S/M/L via a composite score computed from three signals: TCR (total estimated
tokens), test count, and module count; the formula is adapted from the Maintainability Index pattern.
Tier transitions trigger specific governance obligations: S→M requires BACKLOG.md initialization
within 2 sessions; M→L requires ARCHITECTURE.md and ADR directory within 5 sessions.
The audit tool (ADR-36) reports tier mismatches but does not auto-fix; demotion is not automatic
and requires explicit operator acknowledgment in VISION.md frontmatter.
PLAYBOOK.md must be updated with tier transition procedures (currently methodology debt, open Stream C P1).

Full ADR: `.dev-knowledge/docs/decisions/ADR-40-scale-tier-evaluation.md`

---

## ADR-41 — Cross-Session Backlog Architecture (BACKLOG.md)

BACKLOG.md is the single canonical source of truth for all pending items across sessions; handoffs
reference BACKLOG items by stream + title (pointers), never duplicate the queue.
Items use a rigid schema: `## Stream {name}` → `### [P{1-3}] [Status] Item title` → What/Why/Vision ref/Added/Status fields.
Grooming is per-handoff lightweight (~2 min: mark stale items, prune dead items, add new items) plus
quarterly deep (~30 min: archive DONE, re-prioritize, remove VISION-misaligned items).
PLAYBOOK.md must be updated with the BACKLOG grooming workflow (currently methodology debt, open Stream C P1).

Full ADR: `.dev-knowledge/docs/decisions/ADR-41-cross-session-backlog-architecture.md`

---

## ADR-42 — Handoff Format v3.0 (amended through v3.2)

All handoffs (audit-sync, session-sync, feature-X-sync) follow a mandatory three-stage flow: Stage 1
(Claude Code generates question prompt for OLD chat), Stage 2 (OLD chat provides architect response),
Stage 3 (Claude Code reconciles + generates 11-file flat folder). No shortcuts, no Stage 2 bypass.
The 11-file folder includes full VISION/PLAYBOOK/ESSENTIALS copies as methodology anchors (never curated),
ADR essences (not full copies) for ADRs cited in directives, SHA-256 checksums in manifest.json,
and `09_EXECUTION_EVIDENCE.md` as the mandatory return-trip artifact.
Stage 2 source is always the OLD (existing, dying) chat — a fresh chat has no context and adds no signal.

Full ADR: `.dev-knowledge/docs/decisions/ADR-42-handoff-format-v3.md`
