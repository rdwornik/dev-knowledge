# ADR-32: Handoff Format and Browser/Agent Role Split

**Status:** Accepted
**Date:** 2026-04-27
**Stream:** C, session 1
**Supersedes:** none
**Superseded by:** none

## Context

Prior to this decision, the browser/agent workflow had no formal role split, no session charter, and a single-markdown handoff format. An 11-failure evidence base from three sessions (scope creep, hallucinated file state, lost session state, skipped execution steps, recursive re-planning, documentation drift mid-session) triggered an AI Council debate (Topic 2).

Panel: claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.20. Synthesizer: openai (non-participant). Debate transcript: `docs/decisions/transcripts/archive/legacy/DECISION_29_handoff_synergy.md`. Supplementary research: `docs/research/2026-04-27-handoff-patterns-council-research.md`, `docs/research/2026-04-27-handoff-patterns-external-research.md`.

## Decision

### 1. Strict role split

- **Browser (chat UI) = architect/strategist.** Scope, decisions, planning, option analysis, prompt drafting, push-back on direction.
- **Claude Code (CLI) = executor.** All filesystem reads/writes, git operations, test runs, validator runs, artifact existence checks.

The browser is treated as an untrusted planning node; Claude Code is the trusted execution plane. Browser output is advisory on repo state — never authoritative. Any task involving file edits, file moves, git, tests, validators, or artifact checks goes to Claude Code.

### 2. Session charter

Every browser session opens with a short charter in the first 5 messages. Rob authors the charter (not the browser), using the fixed template:

```
repo:
session type: [strategic | execution-support | governance-change | recovery/resume]
goal:
non-goals:
expected artifacts:
max message budget:
stop condition:
```

The charter is the primary scope-boundary mechanism. It prevents scope creep, recursive replanning, and mechanical work bleeding into strategic sessions.

### 3. Step-verification handshake

Every multi-step Claude Code prompt includes an explicit verification gate between steps:

1. Complete Step N
2. Verify the expected artifact or output exists
3. Report verification result
4. Only then proceed to Step N+1

This directly addresses the skipped-step failure (browser proposes step sequence; agent skips confirmation between steps).

### 4. Session length cap

Hard limit: **~40 messages** per browser session. Past this threshold, browser reasoning quality degrades (empirically observed). At the cap, the browser emits a mid-session checkpoint handoff and continues in a fresh session if needed.

### 5. Standardized 9-section handoff content

Every handoff document (`HANDOFF.md`) contains these sections in fixed order:

1. Session charter recap
2. Decisions made
3. Work completed
4. Pending items
5. Open questions
6. Files actually modified
7. Required inputs for next browser session
8. Governance docs referenced
9. Next recommended first action

Sections are fixed and always present (empty if nothing to report). Consistency enables deterministic resumption.

### 6. Folder-format handoff convention

Handoffs are stored as session folders, not single files. Canonical layout:

```
docs/handoffs/{YYYY-MM-DD}-{session-slug}/
  HANDOFF.md            ← primary human-readable handoff (9 sections above)
  upload-instructions.md ← which files to upload, in what order
  first-message.md      ← exact first message to paste into new browser session
  contents/
    manifest.json       ← machine-readable index of contents/ files + commit SHAs
    tree.txt            ← repo tree snapshot at session close
    {governance-docs}   ← snapshots of governance docs uploaded to browser
```

The `contents/` subdir holds everything the browser needs to orient in a fresh session. Claude Code generates or verifies the folder at session close; this shifts factual grounding to the trusted execution plane.

### 7. AGENTS.md as canonical cross-tool governance

Per Council #28, `AGENTS.md` is the canonical file for cross-tool AI governance (Claude Code, Codex, Cursor, Aider). Every repo at Scale M or above must have one. The file documents repo scope, AI assistant directives, and tool-specific constraints.

Reference: ADR-28 (three-layer architecture), Council decision #28 documented in `CLAUDE.md` (`#28: AGENTS.md = canonical cross-tool governance`).

### 8. Cross-repo handoffs

Handoffs for work spanning multiple repos live in `.dev-knowledge/docs/handoffs/` as the authoritative location, with per-repo handoffs in `{repo}/docs/handoffs/` for single-repo sessions. A central index in `.dev-knowledge` provides O(1) discoverability across repos.

## Rejected alternatives

- **Browser performing "light execution" or symmetric usage:** rejected. The empirical failure distribution (6 of 11 pain points from role-boundary collapse) makes any browser-side filesystem claims unsafe.
- **Snapshot-only handoffs (no manifest/hashes):** rejected for governance docs. Snapshots of governance documents drift against the authoritative repo. The `contents/manifest.json` anchors snapshots to commit SHAs so staleness is detectable.
- **Single-markdown handoff only:** rejected as the complete format. Insufficient for deterministic resume — forces manual file hunting and loses structural integrity. Retained as the human-readable primary file (`HANDOFF.md`) within the folder convention.
- **Browser self-monitoring as the sole quality control:** rejected. The browser has demonstrated session-state loss (pain point #2); asking it to monitor its own degradation is the anti-pattern. Pre-decision verification rituals (re-anchoring to current governance + task state before binding decisions) are load-bearing; self-monitoring is supplementary signal only.

## Consequences

**Positive:**
- Role split eliminates the category of failures where the browser makes binding claims about filesystem state
- Session charter prevents scope creep and recursive re-planning at the source
- Step-verification handshake prevents skipped-step execution errors
- Folder format provides deterministic resumption; `contents/` verified by Claude Code before browser ingests it
- 40-message cap contains session-length-induced reasoning degradation

**Costs / accepted risks:**
- Session charter adds ~2 minutes to session open; judged worthwhile against the cost of the prevented failures
- Folder format is more heavyweight than single markdown; tradeoff is determinism vs. convenience
- Some mid-session failures (scope creep, recursive planning) require Rob's in-session discipline in addition to structural constraints

**Follow-up tasks (not in scope for this ADR):**
- `protocols/HANDOFF_PROCESS.md` requires a full rewrite to reflect this decision. Deferred to a dedicated session. Until that rewrite, `HANDOFF_PROCESS.md` and this ADR are in partial conflict — this ADR is authoritative on decisions made; `HANDOFF_PROCESS.md` reflects prior practice.
- Extract-to-task protocol mechanics (operational, not structural) deferred to `protocols/HANDOFF_PROCESS.md` rewrite — see Stream C session 1 HANDOFF.md pending item 2a.

**Revisit triggers:**
- One 2-week trial of strict role split + session charter + 40-message cap + folder format. Measure: resume time, browser corrections caught by Claude Code, scope-creep incidents, skipped-step incidents, subjective cognitive load.
- If folder format overhead proves heavier than the pain it prevents, evaluate collapsing `contents/` into a richer single `HANDOFF.md` with embedded manifest block.
- If the 40-message cap is empirically wrong (too tight or too loose), adjust with evidence.

## References

- Debate transcript: `docs/decisions/transcripts/archive/legacy/DECISION_29_handoff_synergy.md`
- Research: `docs/research/2026-04-27-handoff-patterns-council-research.md`
- Research: `docs/research/2026-04-27-handoff-patterns-external-research.md`
- Implemented example: `docs/handoffs/2026-04-27-stream-c-session-1-final/`
- ADR-28: three-layer architecture (browser = Layer 1 strategic; Claude Code = Layer 2 execution)
- ADR-31: authority model (centralized audit — audit script as grounding tool at session open)
- Follow-up: `protocols/HANDOFF_PROCESS.md` rewrite (separate session, not yet scheduled)
