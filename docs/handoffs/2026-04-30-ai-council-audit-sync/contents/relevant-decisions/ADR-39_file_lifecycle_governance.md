# ADR-39 — File Lifecycle Governance

<!-- scope: meta -->

Status: Accepted
Date: 2026-04-30
Related: ADR-29 (lessons format), ADR-32 (HANDOFF_PROCESS v2.0),
         ADR-33 (universalization), ADR-37 (session boundary protocol),
         ADR-38 (universal repo architecture),
         LESSONS.md entry 2026-04-30 "session-stream-c-debt"

## Amendments

### 2026-04-30 — ARCHITECTURE.md registry entry correction

Original ARCHITECTURE.md registry entry incorrectly described the
file as "Three-layer technical model (foundation/core/orchestration/
interface per ADR-26 Tach taxonomy)." This conflated two distinct
documents: `.dev-knowledge`'s ARCHITECTURE.md (conceptual ecosystem
3-layer model: browser chat / .dev-knowledge / projects) and
`corp-monorepo`'s ARCHITECTURE.md (module-level Tach 4-layer taxonomy
per its own ADR-26). Registry entry corrected to accurately reflect
`.dev-knowledge` ARCHITECTURE.md content.

Surfaced by 2026-04-30 self-audit
(`docs/audits/2026-04-30-dev-knowledge-self-audit.md`).

## Context

2026-04-30 Stream C session ratified 5 ADRs (33, 34, 35, 37, 38) but
JOURNAL.md was not updated for entire session and LESSONS.md was not
appended until user pushback surfaced methodology debt mid-session.
Strażnik metodologii nie stosował metodologii — meta-failure.

Root cause analysis:
- Each file's lifecycle was implicit, not explicit
- Ownership ambiguous (who writes JOURNAL? Browser 1? Browser 2?
  Claude Code? Audit tool?)
- No enforcement mechanism (markdown can't force compliance)
- No registry tracking which files exist and their lifecycle obligations

Without explicit lifecycle definition per file, drift is inevitable.
This ADR codifies universal pattern: every file in .dev-knowledge MUST
have 6 lifecycle elements documented.

This is universal governance pattern. Future files (ADR-41 BACKLOG.md
upcoming, plus any others added later) MUST follow this template.

## Decision

### Six lifecycle elements (universal pattern)

Every file in .dev-knowledge MUST have these 6 elements defined:

1. **Purpose** — Single-paragraph statement: what this file holds and
   what it does NOT hold. Explicit boundary prevents scope creep.

2. **Update trigger** — When does this file change? Categories:
   - **Read-only** — frozen after creation (rare)
   - **Append-only** — new entries added, old entries never modified
     (LESSONS, CHANGELOG, JOURNAL pattern)
   - **Mutable** — can be edited / restructured (README, PLAYBOOK pattern)
   - **Mixed** — append-only sections + mutable sections (rare;
     requires explicit canonicality rule)

   Plus frequency: per-session / per-handoff / weekly / quarterly /
   event-triggered (e.g., on ADR ratification).

3. **Owner** — Who writes this file? Categories:
   - **Rob** (manually edits)
   - **Browser session** (browser chat updates as part of session work)
   - **Claude Code** (programmatic updates via prompts)
   - **Audit tool** (automated, per ADR-36)
   - **Mixed** with explicit per-section ownership

   Plus reviewer: who validates correctness (often = owner for solo dev,
   but may differ).

4. **Grooming cadence** — Does file require periodic review/prune?
   - **None** — never groomed (ADRs ratified, immutable archive)
   - **Per-handoff** — lightweight review (~2 min) at session end
   - **Weekly** — moderate review
   - **Quarterly** — deep review with archival/pruning
   - **Event-triggered** — on tier transition, on ADR amendment, etc.

5. **Boundaries** — How does this file relate to others?
   - **Canonical** — source of truth for some domain
   - **Derived** — generated from canonical sources (regenerable)
   - **Reference** — points to canonical sources, summarizes
   - **Operational** — current-state authoritative (handoff Future State)

   Plus split-brain prevention rule: if file overlaps with another,
   which wins? (e.g., LESSONS.md = canonical narrative, lessons-index.json
   = derived index per ADR-35)

6. **Enforcement** — How does system catch drift / non-compliance?
   - **first-message.md template** — instruction in handoff template
     ("MUST update this file before generating handoff")
   - **Pre-commit hook** — local validation (e.g., validate_scope_tags.py)
   - **Audit tool** (per ADR-36) — periodic compliance check
   - **Honor system** — relies on Rob/browser discipline (last resort,
     acceptable for low-stakes files)

### Universal pattern enforcement

For new files added to .dev-knowledge:
- ADR-39 amendment OR dedicated ADR for the file MUST document all
  6 elements before file creation
- Lifecycle elements documented in this ADR's registry (Section: Registry)
- Audit tool (ADR-36) verifies registry presence per file

For existing files (codified below):
- Registry below documents current state
- Drift detected via audit tool
- Updates require ADR-39 amendment

### Registry of existing files in .dev-knowledge

Each file's 6 lifecycle elements documented below. Use this as
template for future file additions.

#### README.md

| Element | Value |
|---|---|
| Purpose | Entry point for human and AI agents reading the repo. Brief overview, navigation pointers, current ecosystem state at high level. NOT detailed methodology, NOT chronological log, NOT decision history. |
| Update trigger | Mutable. Event-triggered: on major ecosystem changes (new repo onboarded, major ADR ratified). |
| Owner | Rob (manual) + Claude Code (programmatic via prompts) |
| Grooming | Quarterly (review accuracy of pointers and current state section) |
| Boundaries | Reference role — points to canonical sources (VISION, PLAYBOOK, ESSENTIALS). Does NOT duplicate their content. |
| Enforcement | Honor system + audit tool checks presence (mandatory file per ADR-38) |

#### VISION.md

| Element | Value |
|---|---|
| Purpose | Strategic ecosystem direction. Charter format (mission, scope, methodology, lifecycle). NOT tactical pending items, NOT decision log. |
| Update trigger | Mutable. Event-triggered: on major strategic shift, ADR ratification affecting ecosystem direction. |
| Owner | Rob (manual) + Claude Code (programmatic for routine updates) |
| Grooming | Quarterly (validate aspirations against reality, prune obsolete sections) |
| Boundaries | Canonical for ecosystem strategic direction. References ARCHITECTURE for technical detail. |
| Enforcement | Audit tool (ADR-36) verifies presence + frontmatter parseable per ADR-33 |

#### ARCHITECTURE.md

| Element | Value |
|---|---|
| Purpose | Conceptual ecosystem architecture (3-layer model: browser chat / .dev-knowledge brain / projects). NOT module-level Tach taxonomy (that lives in corp-monorepo's own ARCHITECTURE.md per its ADR-26). NOT process documentation, NOT decision log. |
| Update trigger | Mutable. Event-triggered: on architectural ADR ratification, major refactor. |
| Owner | Rob + Claude Code |
| Grooming | Quarterly |
| Boundaries | Canonical for technical architecture. References ADRs for decision rationale. |
| Enforcement | Audit tool checks presence (mandatory for tier L per ADR-38). Honor system for content accuracy. |

#### protocols/PLAYBOOK.md

| Element | Value |
|---|---|
| Purpose | Methodology playbook (sections covering session setup, decisions, handoffs, lessons, etc.). HOW to work in the ecosystem. NOT what was done (JOURNAL), NOT decisions (ADRs). |
| Update trigger | Mutable. Event-triggered: on methodology refinement, ADR ratification adding/changing process. |
| Owner | Rob + Claude Code |
| Grooming | Per-session lightweight (when methodology gap surfaced); quarterly deep review |
| Boundaries | Canonical for methodology. References ADRs for decision-driven process changes. |
| Enforcement | Audit tool checks references to ratified ADRs are reflected in PLAYBOOK |

#### protocols/ESSENTIALS.md

| Element | Value |
|---|---|
| Purpose | Quick reference / cheat sheet. High-leverage rules and patterns. NOT detailed methodology (PLAYBOOK), NOT exhaustive guide. |
| Update trigger | Mutable. Event-triggered: on lessons promotion, methodology change. |
| Owner | Rob + Claude Code |
| Grooming | Per-session lightweight; quarterly prune (remove stale rules) |
| Boundaries | Reference role — distillation of PLAYBOOK + LESSONS. Subordinate to canonical sources. |
| Enforcement | Honor system. Audit tool may check key rules present. |

#### LESSONS.md

| Element | Value |
|---|---|
| Purpose | Append-only narrative archive of lessons learned. Per ADR-29 format: `### YYYY-MM-DD \| source \| lesson \| category \| scope: X \| action`. NOT runtime executable rules (those live in ~/.claude/rules/ per ADR-35). |
| Update trigger | Append-only. Per-session: lessons from current session promoted at session end. |
| Owner | Browser session + Claude Code (via promotion prompts) |
| Grooming | Never (append-only, history preserved). Quarterly archive option per ADR-29. |
| Boundaries | Canonical for narrative lessons. lessons-index.json (per ADR-35, when implemented) is derived index. ~/.claude/rules/ is downstream runtime. |
| Enforcement | first-message.md handoff template (MUST promote session lessons). Audit tool tracks lesson promotion frequency. |

#### JOURNAL.md

| Element | Value |
|---|---|
| Purpose | Append-only chronological dev log. What was done per session/day. Did/Failed/Next format. NOT decision rationale (ADRs), NOT lessons (LESSONS), NOT current state (handoffs). |
| Update trigger | Append-only. Per-session: prepended at session end with day/session entry. |
| Owner | Browser session + Claude Code (via session-end prompts) |
| Grooming | Never (append-only). Quarterly archive option. |
| Boundaries | Canonical for chronological session log. Distinct from LESSONS (chronological vs categorical learning). |
| Enforcement | first-message.md handoff template (MUST update before handoff generation). Audit tool flags missing entries per session. **2026-04-30 LESSON: failure mode is silent skip — enforcement template-level required.** |

#### CHANGELOG.md

| Element | Value |
|---|---|
| Purpose | Append-only version history. ADR ratifications, breaking changes, features. Per Keep-A-Changelog format. NOT decision rationale (ADRs), NOT chronological log (JOURNAL). |
| Update trigger | Append-only. Event-triggered: on ADR ratification, repo-functional change (per Rob preferences "CHANGELOG required for repo-functional changes; NOT required for meta-doc cleanup"). |
| Owner | Claude Code (via ADR/feature prompts) |
| Grooming | Never (append-only). Quarterly review for accuracy. |
| Boundaries | Canonical for version history. Derived from git history but adds human-readable context. |
| Enforcement | Each formal Claude Code prompt template includes CHANGELOG step for repo-functional changes |

#### protocols/HANDOFF_PROCESS.md

| Element | Value |
|---|---|
| Purpose | Process specification for inter-session handoffs (per ADR-32 v2.0 + ADR-37 two-phase overlay). HOW to generate and consume handoffs. NOT individual handoff content. |
| Update trigger | Mutable. Event-triggered: on ADR-32/ADR-37 amendment, handoff process refinement. |
| Owner | Rob + Claude Code |
| Grooming | Event-triggered (no scheduled cadence) |
| Boundaries | Canonical for handoff process. Subordinate to ADR-32/ADR-37 (ADRs ratify, this doc operationalizes). |
| Enforcement | Audit tool verifies process compliance via handoff folder structure |

#### templates/HANDOFF_TEMPLATE.md

| Element | Value |
|---|---|
| Purpose | Template skeleton for handoff folder structure (per ADR-32 + ADR-37 two-phase format). NOT process documentation (HANDOFF_PROCESS), NOT individual handoff content. |
| Update trigger | Mutable. Event-triggered: on ADR-32/ADR-37 amendment. |
| Owner | Rob + Claude Code |
| Grooming | Event-triggered |
| Boundaries | Reference role — instantiation guide for HANDOFF_PROCESS. |
| Enforcement | Templates that don't match HANDOFF_PROCESS = audit finding |

#### protocols/ENVIRONMENT.md

| Element | Value |
|---|---|
| Purpose | Environment configuration reference (paths, env vars, tool versions). HOW to set up workspace. NOT decision rationale, NOT methodology. |
| Update trigger | Mutable. Event-triggered: on environment change, new tool added. |
| Owner | Rob + Claude Code |
| Grooming | Quarterly (validate against actual environment) |
| Boundaries | Canonical for environment setup. Subordinate to no other doc. |
| Enforcement | Honor system. Audit tool may check env var presence. |

#### protocols/SESSION_SETUP.md

| Element | Value |
|---|---|
| Purpose | Browser chat workflow. 5 chronological steps for starting a session. NOT full methodology (PLAYBOOK), NOT environment config (ENVIRONMENT). |
| Update trigger | Mutable. Event-triggered: on browser chat workflow change. |
| Owner | Rob + Claude Code |
| Grooming | Quarterly (validate steps against actual session startup) |
| Boundaries | Reference role — operational subset of PLAYBOOK. Consistent with PLAYBOOK; PLAYBOOK wins on conflict. |
| Enforcement | Honor system. Audit tool may check presence (mandatory per ADR-38). |

#### CONTRIBUTING.md

| Element | Value |
|---|---|
| Purpose | Branch/commit/validator/ADR/handoff conventions for sole-contributor workflow. HOW to contribute (even for solo dev: conventions, branching model, PR format). NOT methodology (PLAYBOOK), NOT decision log (ADRs). |
| Update trigger | Mutable. Event-triggered: on workflow convention change, tool addition. |
| Owner | Rob + Claude Code |
| Grooming | Quarterly |
| Boundaries | Reference role — operational conventions derived from PLAYBOOK + ADRs. |
| Enforcement | Honor system. Pre-commit hook validates some conventions. |

#### CLAUDE.md (project-level)

| Element | Value |
|---|---|
| Purpose | Claude Code project instructions for .dev-knowledge repo. File rules, scope tag definitions, Council decisions, and what NOT to do. NOT global Claude Code config (that lives in ~/.claude/). |
| Update trigger | Mutable. Event-triggered: on project convention change, new ADR affecting Claude Code behavior, new file added. |
| Owner | Rob + Claude Code |
| Grooming | Quarterly (review file rules table, Council decisions list) |
| Boundaries | Canonical for Claude Code behavior in this repo. Supersedes global ~/.claude/CLAUDE.md for repo-specific rules. |
| Enforcement | Read automatically by Claude Code on every session. |

#### docs/decisions/ADR-NN_*.md (each ADR)

| Element | Value |
|---|---|
| Purpose | Architectural Decision Record per ADR convention. Single decision documented with context/decision/consequences. NOT process documentation. |
| Update trigger | Read-only after ratification. Amendment requires new ADR (deprecate or supersede). |
| Owner | Claude Code (via formal prompts) post-ratification |
| Grooming | Never (immutable archive) |
| Boundaries | Canonical for the specific decision. Cross-references between ADRs explicit. |
| Enforcement | Audit tool verifies scope tag, ratified status, no post-hoc edits (git history) |

### Template for future file additions

When adding new file to .dev-knowledge, ADR-39 must be amended (or
dedicated ADR for the file must reference this template) with all 6
elements:

```
#### {filename}

| Element | Value |
|---|---|
| Purpose | (single paragraph: what it holds, what it does NOT hold) |
| Update trigger | (read-only / append-only / mutable / mixed + frequency) |
| Owner | (Rob / browser session / Claude Code / audit tool + reviewer) |
| Grooming | (none / per-handoff / weekly / quarterly / event-triggered) |
| Boundaries | (canonical / derived / reference / operational + split-brain rule) |
| Enforcement | (template / pre-commit / audit tool / honor system) |
```

### Universalization (per ADR-33 pattern)

- **Mandate**: .dev-knowledge applies this lifecycle pattern
- **Recommendation**: child repos with persistent files (VISION,
  CHANGELOG, lessons equivalents) follow same lifecycle pattern
- **Cross-repo audit (Phase 3)**: auditor verifies lifecycle compliance

### Failure mode prevention (2026-04-30 lesson)

JOURNAL.md was skipped for 5 ADR cycles because lifecycle was implicit.
ADR-39 prevents this by:

1. **Explicit owner per file** — JOURNAL owner = browser session + Claude Code
2. **Explicit update trigger** — JOURNAL append-only, per-session
3. **Explicit enforcement** — first-message.md handoff template MUST
   include JOURNAL update step

When prompts (formal Claude Code, browser instructions) are generated
for sessions that touch repo state, they MUST include JOURNAL update
as final step. Prompt template enforcement is the practical boundary.

## Consequences

### Positive
- Every file has explicit ownership and update trigger
- New file additions follow template — no implicit decisions
- Audit tool (ADR-36) can verify lifecycle compliance
- 2026-04-30 failure mode (JOURNAL skipped) prevented by template-level enforcement
- Cross-cutting governance pattern — informs ADR-41 BACKLOG.md design
- Solo dev relies less on memory, more on explicit lifecycle

### Negative
- Adding new file requires lifecycle definition (slight friction)
- Registry must be kept current (potential drift if amendments skipped)
- 6 elements may feel ceremonial for trivial files (mitigated: most fields take 1-2 sentences)

### Follow-ups
- ADR-41 (BACKLOG.md) MUST include 6 lifecycle elements per this template
- HANDOFF_TEMPLATE.md update: include JOURNAL update step explicitly
  (separate session)
- Audit tool implementation (P1, separate session): lifecycle compliance check
- Quarterly review: validate registry against actual file state, amend as needed
- Future file additions: amend ADR-39 with new entry OR create dedicated
  ADR referencing this template

## References

- LESSONS.md entry 2026-04-30 "session-stream-c-debt" (motivating failure)
- ADR-29 (lessons format and grandfathering)
- ADR-32 (HANDOFF_PROCESS v2.0)
- ADR-33 (universalization pattern)
- ADR-36 (audit tool — enforcement consumer)
- ADR-37 (session boundary protocol — JOURNAL update timing)
- ADR-38 (universal repo architecture — mandatory files context)
