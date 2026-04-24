# Consolidated Action Items — Council #28 + #29 + 2 Research Reports

> **2026-04-24 update — partially superseded**
>
> P0-2 (reopen Council #27) was based on the false premise that ADR-27 did not exist.
> ADR-27 exists since 2026-04-22 and does NOT contradict Council #28 findings (they
> operate on different layers: ADR-27 = scope tag vocabulary in .dev-knowledge,
> Council #28 = governance file structure recommendations). P0-2 removed.
>
> For current Stream A status see: `docs/audits/2026-04-24-stream-a-gap-report.md`

**Date:** 2026-04-24
**Sources:**
- Council #28 (research, community LLM dev patterns): `corp-monorepo/docs/decisions/transcripts/DECISION_28_community_patterns_research.md`
- Council #29 (research, Spec Kit + Kiro): `corp-monorepo/docs/decisions/transcripts/DECISION_29_spec_kit_kiro_research.md`
- Research: CLAUDE.md best practices 2026: `.dev-knowledge/docs/research/2026-04-24-claude-md-best-practices.md`
- Research: Multi-agent debate patterns: `.dev-knowledge/docs/research/2026-04-24-multi-agent-debate-patterns.md`

## Triage Summary

- **P0 (critical, do ASAP):** 3 items — foundational, block other work
- **P1 (important, this week):** 3 items — building on P0
- **P2 (important, this month):** 3 items — ongoing hygiene
- **P3 (low priority / skip):** 3 items — deferred or rejected

## P0 — Critical

### P0-1: Trim CLAUDE.md to thin pointer (corp-monorepo)
**Source:** Council #28 action item #2, Research CLAUDE.md best practices
**Target:** `corp-monorepo/CLAUDE.md`
**Current state:** 4KB, contains architecture rules, stale numbers ("24 Council Decisions", "2,404 tests" — actual 27 and 2,515)
**Recommendation:** <200 lines, point to AGENTS.md as canonical, keep only Claude-specific (skills, slash commands, session protocol)
**Effort:** M (2-3h)
**Dependencies:** none
**Status:** not started
**Next session:** "CLAUDE.md Refactor — Sprint 1"

### P0-2: Reopen Council #27 decision in light of Council #28 findings
**Source:** Browser chat analysis 2026-04-24
**Target:** `.dev-knowledge/docs/decisions/`
**Problem:** Council #27 decided Option A (section-level scope tagging in 63 sections). Council #28 suggests CLAUDE.md thin + AGENTS.md canonical + hooks enforce — this may supersede or change abstraction level of tagging.
**Question:** Is section tagging still the right answer, or do we tag consumer read-sets via hooks?
**Effort:** S (1h reopen decision + write ADR-NN reversal or confirmation)
**Dependencies:** P0-1 informs this
**Status:** not started

### P0-3: Resolve ADR-27 naming collision (corp-monorepo)
**Source:** Browser chat analysis 2026-04-21 (operating model analysis Section 12)
**Target:** `corp-monorepo/docs/decisions/`
**Problem:** Two files ADR-27-* active simultaneously. Blocks future ADR numbering.
**Recommendation:** renumber `ADR-27-safety-invariants.md` to `ADR-28-safety-invariants.md` (or similar), move `ADR-27-council-onedrive-centralization.md` content to `transcripts/DECISION_27_onedrive_centralization.md` (it's a transcript, not ADR)
**Effort:** S (30 min)
**Dependencies:** none (can run parallel to P0-1)
**Status:** not started

## P1 — Important, this week

### P1-1: Formalize gotchas skill per 2026 standard
**Source:** Council #28 action item #4, Research CLAUDE.md best practices
**Target:** `corp-monorepo/.claude/skills/gotchas/`
**Current state:** Already at `.claude/skills/gotchas/` with SKILL.md and gotchas.md
**Recommendation:** Verify <500 lines SKILL.md, move long references to `references/` subdir, ensure progressive-disclosure pattern
**Effort:** S (1-2h)
**Dependencies:** P0-1 (CLAUDE.md should point to skills cleanly first)
**Status:** verify current state, may be mostly done

### P1-2: Spec Kit spike (throwaway branch, 4h)
**Source:** Council #29 recommendation
**Target:** new throwaway branch in any repo
**Scope:** `pipx install specify-cli`, run `specify init`, test PowerShell compat, test Claude Code integration
**Decision rule:** if friction low → adopt with ADR, if friction high → fall back to plain markdown specs
**Effort:** S (4h including decision)
**Dependencies:** none
**Status:** not started

### P1-3: Write ADR defining spec vs ADR boundary
**Source:** Council #29 action item #1
**Target:** `corp-monorepo/docs/decisions/ADR-NN-spec-as-adr-complement.md`
**Content:** Authority hierarchy (skills/governance > ADRs > specs > JOURNAL), complexity threshold for specs (>1 session, >2 modules, ambiguous requirements), archive policy
**Effort:** S (1h)
**Dependencies:** P1-2 (spike informs whether Spec Kit or plain markdown)

## P2 — Important, this month

### P2-1: JOURNAL.md rotation protocol
**Source:** Council #28 action item #10 (monthly prune)
**Target:** `corp-monorepo/JOURNAL.md` + new `JOURNAL-archive/YYYY-MM.md`
**Problem:** 36KB file, entries go back to March 2026
**Recommendation:** monthly rotation, keep only current month in root, archived months in archive dir
**Effort:** S (1h initial setup + recurring 15 min/month)

### P2-2: Council gating criteria in AGENTS.md
**Source:** Council #28 action item #8, risk #3 (AI Council overhead)
**Target:** `corp-monorepo/AGENTS.md`
**Content:** Define when Council debate (module boundaries, new dependency, data model change, affects multiple ADRs), when single model + critic (normal implementation)
**Effort:** S (30 min)
**Dependencies:** P0-1 (AGENTS.md canonicalization should happen first)

### P2-3: Skills pruning ritual (monthly)
**Source:** Council #28 action item #11, risk #4
**Scope:** Monthly review of skills — trigger actually firing? contradictions? redundancy?
**Effort:** S (30 min/month recurring)
**Dependencies:** P1-1 (gotchas skill formalized first)

## P3 — Low priority / skip

### P3-1: Chinese models integration (GLM, Qwen Code)
**Source:** Rob's original briefing, Council #28 explicitly skipped
**Status:** Deferred — no concrete use case pressing
**Reopening trigger:** concrete pressing use case, or Anthropic/OpenAI pricing shock

### P3-2: MCP memory servers
**Source:** Council #28 recommendation
**Status:** Skip until file-based continuity fails repeatedly
**Reopening trigger:** JOURNAL.md + handoff process failing to preserve context for >2 consecutive sessions

### P3-3: LangGraph / AutoGen / CrewAI frameworks
**Source:** Multi-agent debate research
**Status:** Skip — AI Council already implements proposer-critic-synthesizer pattern at solo-dev scale
**Reopening trigger:** team grows beyond solo, or AI Council proves insufficient

## Sequencing note

Implement in this order:
1. P0-3 first (trivial fix, blocks nothing, but blocks future ADR numbering)
2. P0-1 next (CLAUDE.md trim — this IS the foundational change)
3. P0-2 after P0-1 (reopen Council #27 with new CLAUDE.md reality as context)
4. P1 items in parallel after P0 done
5. P2 items over following weeks

## Open questions for next sessions

- Where does the spec vs ADR boundary ADR live — corp-monorepo (specific to that repo) or `.dev-knowledge` (universal dev practice)?
- If P0-2 reverses Option A from Council #27, what does that do to Stream A (63-section tagging) work — cancel entirely, or partial retention?
- Should consolidated action items like this file become a standing pattern (one per Council debate cycle) or ad-hoc?
