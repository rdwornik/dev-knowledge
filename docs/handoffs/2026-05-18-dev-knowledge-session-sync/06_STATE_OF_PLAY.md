# State of Play — .dev-knowledge (session-sync 2026-05-18)

## What was completed this session

We committed and merged ADR-51, the architecture documentation convention,
through a full AI Council debate (pick mode, 4-model panel + synthesizer). The
debate verdict was distilled into a numbered, formatted ADR, committed on a
feature branch, and merged to `main`. A rule was simultaneously added to
PLAYBOOK.md establishing that distilling an AI Council debate verdict into a
committed ADR is a mandatory, automated process step.

We also committed ADR-38 Amendment A4, which closed the corp-monorepo
`ARCHITECTURE.md` root-placement deferral that A3 had left open. The amendment
records that the universalization rollout (Workstreams B/C/D for corp-monorepo)
has now performed the mechanical move, making the prior deferral obsolete.

We updated PLAYBOOK.md to correct the AGENTS.md file-type taxonomy — correcting
how the Claude-oriented handoff process was describing that file.

The ai-council Stage 3 handoff was also completed this session (commit
`592dc8c`), separate from the current `.dev-knowledge` handoff.

## Current state

- **HEAD SHA:** `aeaf1582d68c8e2ae4ff304bf08972f6e01eec10`
- **Branch:** `main` (Stage 1 captured from `main`; this Stage 3 generated on
  `handoff/2026-05-18-dev-knowledge-session-sync`)
- **Working tree:** clean
- **Test suite:** pre-existing failure `test_ratio_pass_when_stable_above_ceiling`
  was not witnessed in this session — verify current status with `pytest -x`
  before running tests
- **ADR count:** 51 ADRs in `docs/decisions/`

## Decisions locked this session

**ADR-51 (architecture documentation convention)** is accepted and merged. The
convention mandates a dedicated `ARCHITECTURE.md` for M- and L-scale repositories,
sourced from a single canonical template in `.dev-knowledge`. The mandatory core
is: bird's-eye purpose statement, auto-generated codemap, and explicit layer
boundaries and invariants. The codemap is CI-enforced. Two items remain open
(not settled by ADR-51): the codemap generator's output specification, and the
existing `corp-monorepo` ARCHITECTURE.md and C4 pipeline (both must be inspected
before the template is authored).

**PLAYBOOK distillation rule** — distilling an AI Council debate verdict into a
committed ADR is now recorded as a mandatory, automated Council process step in
PLAYBOOK.md.

**ADR-38 A4** — the corp-monorepo `ARCHITECTURE.md` root-placement deferral is
closed. All repos must place `ARCHITECTURE.md` at root per Amendment A3, with no
timing exceptions.

## Deferred items

All items below remain in the BACKLOG [P1/P2/P3 = governance priority tier].

**Cross-stream (open):**
- `[P1]` Council decisions management consolidation — inventory closed; contradiction
  detection + ownership model still open
- `[P1]` Sacred-files maintenance enforcement — design and implement enforcement
  mechanism (candidate mechanisms: pre-commit hook, session-end skill update, CI
  check, diff-based detection — not settled)
- `[P2]` Handoff advisory framing leaks into receiver behavior — root cause
  classification open
- `[P2]` Fix pre-existing test failure: `test_ratio_pass_when_stable_above_ceiling`
- `[P2]` Hooks audit + consolidation

**Stream C — .dev-knowledge governance:**
- `[P2]` ADR-38 self-compliance gap — `src/` + `pyproject.toml` vs. governance-only
  exemption (resolution path not settled in this session)
- `[P2]` Lessons activation P1 implementation (ADR-35 [lessons-base-activation]) —
  `lessons-index.json` + SessionStart hook + CLI
- `[P2]` ESSENTIALS.md cheat-sheet additions for ADRs 35–41 (requires pruning to
  stay under 1-page constraint)
- `[P2]` Audit tool: `check_backlog_organization` code-span-aware done-token regex
- `[P2]` Stream taxonomy grooming — Cross-stream section exceeds 33% kill criterion
  (ADR-47 [stream-taxonomy])
- `[P3]` ADR-39 amendment — BACKLOG.md lifecycle entry
- `[P3]` ADR-41 amendment — reference ADR-47
- `[P3]` ADR-39 registry decision — 5 unregistered template files
- `[P3]` LESSONS.md parenthetical-qualifier entries escape dated-entry audit regex

## Rationale (architect judgment)

ADR-51 was triggered by re-orientation friction: a solo developer maintaining
many repositories of varying scale was losing significant time after weeks away,
and architecture documentation was inconsistent across the ecosystem. The dominant
constraint was the empirically falsified prior manual-upkeep approach — a
single-file handoff went roughly five weeks stale before retirement. Any
convention depending on remembered manual updates was already ruled out by
evidence.

The rejected alternatives were: universal coverage (all repos regardless of
scale — rejected because near-empty S-repo documents rot fastest and erode trust),
folding architecture into CLAUDE.md (conflates agent-instruction and human
re-orientation audiences), manual-only upkeep (directly falsified by the
five-week precedent), per-tier templates (triples `.dev-knowledge` maintenance
surface), and one-time codemap without CI (recreates staleness in slower motion).

The AGENTS.md scoping correction (Directive 3) stems from a conflation identified
by the project owner: Claude-oriented handoff processes were folding AGENTS.md
into their model of "the repository's descriptive documents," causing Claude-side
chats to reason about a file that belongs to the Codex agent's domain. The intended
end state is clean domain separation — CLAUDE.md and Claude-side handoffs in one
domain; AGENTS.md in the Codex domain — with neither appearing in the other's scope.

## Stage 3 verification summary

Architect provided the following categories of claims in Stage 2:

- **Witnessed claims verified against repo state (checkable):** 3
  - ADR-51 exists and is accepted — VERIFIED (file present, Status: Accepted)
  - PLAYBOOK.md AGENTS.md taxonomy correction was committed — VERIFIED
    (commit `d1dac86` in log)
  - ADR-38 A4 amendment was committed — VERIFIED (commit `5dc7f29` in log)

- **Witnessed claims that failed verification:** 1
  - **VERIFICATION FAILED** — Stage2 claimed: "AGENTS.md currently has no
    canonical template equivalent to the one ADR-51 establishes."
  - **Actual:** `templates/AGENTS-md-template.md` EXISTS in the repo with 10
    defined sections (Read First, Repo identity, Architecture, Conventions, Tools
    active, Gotchas, Council decisions, Out of scope, Session start checklist,
    Do NOT).
  - **Implication:** What does NOT exist is a *convention / decision record* for
    AGENTS.md (an ADR or equivalent). The template draft exists; the formal
    convention that the template should implement is not yet recorded. Directive
    2 in `07_ACTION_PLAN.md` is therefore reframed: rather than "author a template
    from scratch," the next session should verify the existing template's conformance
    to any convention decided, and record the convention — not assume the template
    is absent.

- **Architect-flagged inferences (preserved with flag):** 2
  - Internal ordering of Directives 1 and 2 within this session (architect labeled
    as inference, since no explicit sequencing was witnessed)
  - Ordering of Directives 2 and 3 (architect labeled as inference — can be
    executed together)

- **Architect-flagged unknowns (resolved or preserved):**
  - Pre-existing test failure `test_ratio_pass_when_stable_above_ceiling` —
    **Unknown, preserved** (not witnessed; verify with `pytest -x`)
  - ADR-38 governance-only-repo exemption path for `.dev-knowledge` —
    **Unknown, preserved** (not settled in this session; verify against ADR-38)
  - Sacred-files enforcement mechanism choice — **Unknown, preserved** (not
    witnessed; no decision recorded)
