# State of Play — .dev-knowledge

<!-- scope: meta -->

Current State per ADR-37. Sources: Stage 2 architect REALITY + RATIONALE
answers; verification against `.dev-knowledge` at HEAD `c4d7c858` (Stage 1)
and `1f7a985` (Stage 3 post-commit).

## What was completed this session

(Stage 2 architect REALITY, verb-led summary)

Three ADR-53 chunks closed for `.dev-knowledge`: AGENTS.md retired and
CLAUDE.md v2.1 brought live as the single canonical agent-instruction
contract; cross-repo stale-reference sweep applied in live docs;
`ARCHITECTURE.md` "known violations" list reclassified to zero (the
remaining flagged item, `corp-monorepo/AGENTS.md`, was correctly
reclassified as outside ADR-53 scope — Codex tool config, not an
agent-instruction contract). ADR-54 [codex-reviewer-global-standard]
was then authored to govern the Codex reviewer config as a global
standard at `~/.codex/AGENTS.md`, with the canonical source tracked at
`codex/AGENTS.md` in `.dev-knowledge` and deployed to the user-home
location. The global config carries the generic reviewer role plus an
explicit instruction to read each repo's `ARCHITECTURE.md` for
structural context. PLAYBOOK §16 picked up a 2-line note on config
ownership; ARCHITECTURE.md §Authority was rewritten to reflect the
ADR-54 model. HEAD reflects the ADR-54 merge.

## Current state

- HEAD at Stage 1: `c4d7c8587b6d32ca68d19782009220a3daf45cd9` (clean main)
- HEAD at Stage 3 commit: `1f7a985bbc30f0d757841f9c20d385f5be4ac814`
  (Stage 1 commit; advances further with this Stage 3 commit)
- Branch: `main`
- Working tree: clean at Stage 1 (Stage 3 leaves clean after commit)
- Ancestor check: Stage 1 SHA is ancestor of current HEAD (verified
  before generation)
- Recent commits (newest first):
  - `c4d7c85` docs: merge codex-reviewer-global-standard — ADR-54, global config live
  - `0b94878` docs: add ADR-54 — Codex reviewer config as global standard
  - `fcd4eb6` feat: add codex/AGENTS.md — canonical global Codex reviewer config
  - `c4e0db4` docs: merge correct-corp-monorepo-agents-violation — violations → 0
  - `b2535fe` docs: merge post-ai-council cross-repo sweep — stale AGENTS.md refs resolved (ADR-53)
  - `be2ad6b` docs: merge chunk4 — retire AGENTS.md, CLAUDE.md v2.1 live (ADR-53)

## Decisions locked this session

- **ADR-53 retired AGENTS.md as the agent-instruction contract.** CLAUDE.md
  v2.1 is the single canonical per-repo agent-instruction file. For
  `.dev-knowledge`, AGENTS.md was deleted and content migrated into
  CLAUDE.md (~130 lines) with three approved condensations (ADR list
  trimmed to last 5; scope tags reduced; per-file triggers dropped).
- **ADR-54 globalized the Codex reviewer config.** Same filename
  (`AGENTS.md`) had served two distinct tool-consumer roles. ADR-53
  governed the agent-instruction-contract role; ADR-54 governs the
  Codex tool-config role. `corp-monorepo/AGENTS.md` was reclassified
  out of the ADR-53 known-violations list because Codex tool config is
  outside ADR-53 scope.
- **Codex reads each repo's `ARCHITECTURE.md` for structural context.**
  Codex's `project_doc_fallback_filenames` mechanism loads CLAUDE.md as
  fallback but not `ARCHITECTURE.md`; the global reviewer config carries
  an explicit "read the repo's `ARCHITECTURE.md`" instruction to bridge
  the gap. This is the load-bearing assumption for the codemap-generator
  work the next session will spec.

## Rationale (architect judgment)

(Stage 2 architect RATIONALE — Witnessed unless flagged)

**Why corp-monorepo/AGENTS.md was treated as outside ADR-53 scope
(Witnessed).** ADR-53 retired AGENTS.md in its role as the per-repo
agent-instruction contract — the file Claude Code reads to learn how to
behave in a repo — and made the CLAUDE.md v2.1 template the single
canonical instruction contract for that role. `corp-monorepo/AGENTS.md`
simultaneously served a different role: Codex's tool configuration, the
file Codex reads to learn how to review. Same filename, two different
tool-consumers, two different concerns. ADR-53 governed only the
instruction-contract role; the tool-config role was a separate deferred
concern that ADR-54 then governed.

**Why the Codex reviewer config was globalized to `~/.codex/AGENTS.md`
rather than left per-repo (Witnessed).** Codex's documented layering model
places a global file beneath optional per-repo overrides — generic
cross-project configuration belongs in the global file. The generic
reviewer config (role definition, review checklist, output format) is
cross-project: three per-repo copies would create exactly the drift
surface ADR-53 was created to eliminate. Single source — global —
removes that surface. Per-repo `AGENTS.md` files remain available for
genuinely repo-specific review rules; whether any repo actually warrants
one is a per-repo judgment rather than a fixed policy. Additionally,
because Codex's `project_doc_fallback_filenames` loads only the CLAUDE.md
fallback (not `ARCHITECTURE.md`), the global config carries an explicit
"read the repo's `ARCHITECTURE.md` for structural context" instruction —
that instruction is what routes Codex to the structural source, which is
the load-bearing assumption for the codemap-generator work the next
session will spec.

**Why the three CLAUDE.md v2.1 condensations (Unknown).** No specific
rationale witnessed in this session arc. Stage 3 verifies against the
CLAUDE.md template or its originating ADR. Witnessed instances are
recorded in `JOURNAL.md` (2026-05-19, Chunk 4) but the rationale for
each condensation is not in the architect's session transcript.

## Deferred items

Architect-relevant open items, by BACKLOG entry (do not duplicate queue):

- Stream C P2 open — `.dev-knowledge` ADR-38 self-compliance gap (`src/`,
  `pyproject.toml`)
- Stream C P2 open — Lessons activation P1 implementation per ADR-35
- Stream C P2 open — ESSENTIALS.md cheat-sheet additions for ADRs 35-41
- Stream C P2 open — Audit tool `check_backlog_organization` code-span-
  aware done-token regex
- Stream C P2 open — Stream taxonomy grooming (Cross-stream > 33% kill
  criterion; deferred to 2026-07-01)
- Stream C P2 open — Codemap generator output specification (ADR-51
  open item) ← **THIS HANDOFF'S OBJECTIVE**
- Cross-stream P1 open — Council decisions management consolidation
  (contradiction detection + ownership-model sub-items remain)
- Cross-stream P1 open — Sacred-files maintenance enforcement
- Cross-stream P2 open — Hooks audit + consolidation
- Cross-stream P2 open — Skills universalization across repos
- Cross-stream P2 open — Phase 2 universalization rollout (ai-council
  substantially complete; corp-monorepo not yet started)
- Cross-stream P3 open — ADR-42 amendment (single vs multi-artifact
  handoff format clarification)

## External dependencies in play

`corp-monorepo` is independently retiring its own `corp-monorepo/AGENTS.md`
(the per-repo Codex config that the new global standard supersedes). This
is external to `.dev-knowledge`'s scope; the next `.dev-knowledge` session
**must not direct corp-monorepo work** (Universal Self-Containment Rule
in `03_PLAYBOOK.md` / `HANDOFF_PROCESS`). The exact state of
`corp-monorepo/AGENTS.md` at session open is Unknown and does not block
codemap-spec work.

## Stage 3 verification summary

Architect provided witnessed claims:

- **Verified against repo state:**
  - HEAD `c4d7c858` clean on `main` — verified via `git rev-parse HEAD` +
    `git status --porcelain` at Stage 3.
  - `codex/AGENTS.md` exists in `.dev-knowledge` — verified via
    `git log --oneline -15` (commit `fcd4eb6`).
  - ADR-51 + ADR-54 exist at expected paths — verified via glob match
    `docs/decisions/ADR-5{1,4}*.md`.
  - JOURNAL `2026-05-19` entries for ADR-54, ARCHITECTURE.md
    reclassification, cross-repo sweep, and AGENTS.md retirement chunk —
    verified via JOURNAL read.
- **Architect-flagged inferences (preserved):**
  - "No `.dev-knowledge` work in progress not visible at HEAD" —
    inference, consistent with clean working tree.
  - Choice of OBJECTIVE (codemap spec) as next-up rather than other
    BACKLOG items — explicitly marked architect inference.
  - "Specific paths and the artifact-type choice (ADR amendment vs.
    sibling implementation spec) may need revision based on repo state."
- **Architect-flagged unknowns:**
  - Path of the canonical ARCHITECTURE.md template in `.dev-knowledge`
    — resolved at Stage 3: `templates/ARCHITECTURE-template.md`
    (verified via `git ls-files`; codemap section uses
    `<!-- CODEMAP:START/END -->` machine region per BACKLOG entry).
  - Current shape of `.dev-knowledge`'s own `ARCHITECTURE.md` codemap
    section — preserved as unknown; the new session's DIRECTIVE 1
    explicitly resolves this gap.
  - Rationale for the three CLAUDE.md v2.1 condensations — preserved
    as unknown.
- **Verification failures:** none.
