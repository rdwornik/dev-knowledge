# Codex Review — vision-reread

**Date:** 2026-07-25
**Branch:** `docs/vision-reread`
**HEAD:** `9d71a41a`
**Diff range:** `main..docs/vision-reread`
**Codex version:** codex-cli 0.145.0
**Mode:** doc-review

---

## Focus

- VISION.md was re-read end-to-end and 7 content defects fixed, then last_reviewed re-stamped 2026-06-19 -> 2026-07-25 in the same commit. Judge whether the STAMP IS HONEST: is any remaining VISION.md claim inaccurate against live repo state? A false stamp is the failure mode this lane exists to prevent.
- The Vision-section portability claim was NARROWED (was: "works in any folder on any machine - portable, self-contained, machine-agnostic"). Check the narrowed wording is now TRUE and does not over- or under-claim. Note VISION:151 reserves Vision/Scope CHANGES for AI Council debate while permitting conversational edits for clarifications - assess whether narrowing a false descriptive claim was within the clarification lane or should have gone to Council.
- The ai-council paragraph (was VISION:110-113) was rewritten against the ADR-43 2026-07-23 RE-SCOPE. Verify it does not overstate the retirement: ADR-43 was re-scoped, NOT retired; ai-council repo-local canonical-write production still stands.
- The fleet roster/count and the new ADR-104 fleet-shape paragraph: verify against ADR-104 (9 repos, PARTIAL fold, corp-monorepo permanently outside, incremental consolidation, no fold executes on that ADR). Flag any assertion ADR-104 does not support.
- Cross-doc consistency: any dangling reference, stale claim, or contradiction introduced by these edits - including VISION vs CLAUDE.md, ARCHITECTURE.md, ESSENTIALS.md.

---

## Findings
## Critical

(none)

## High

### [HIGH] VISION.md:16 — “methodology corpus” is still falsely claimed path-free

**What:** The corpus explicitly includes protocols, ADRs, and templates, but each contains host-specific absolute paths (e.g. `protocols/ENVIRONMENT.md:150`, `templates/prompt-template.md:20`, `docs/decisions/ADR-61-git-worktree-parallel-sessions.md:57`).  
**Why:** This makes the narrowed portability claim false and the `last_reviewed: 2026-07-25` stamp not fully honest.  
**Fix direction:** Limit portability to a demonstrably portable subset, or qualify/externalize the host-specific material.

## Medium

(none)

## Low

(none)

ADR-43 and ADR-104 statements are otherwise faithful. Treating the prior portability wording as a factual clarification does not require an AI Council decision.
