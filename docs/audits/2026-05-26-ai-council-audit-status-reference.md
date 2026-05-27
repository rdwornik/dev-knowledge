---
type: audit-status-reference
scope: ai-council universalization status as of 2026-05-26
date: 2026-05-26
basis: docs/audits/2026-05-25-ai-council-universalization-audit-refresh.md + execution-plan (both authoritative, unchanged)
contract: read-only on ai-council; writes confined to .dev-knowledge/docs/audits/
---

# ai-council Universalization Status — 2026-05-26

This is a **status reference**, not a re-audit. ai-council was refreshed on
2026-05-25 (`docs/audits/2026-05-25-ai-council-universalization-audit-refresh.md`
+ `-execution-plan.md`). This document exists so the 2026-05-26 cross-repo
synthesis can reference ai-council without duplicating audit content, and to
record the HEAD-movement check that determines whether the 2026-05-25 artifacts
are still authoritative.

## HEAD movement check (pivotal)

- **2026-05-25 refresh basis:** HEAD `2a980ab` ("docs: merge chunk4 — retire
  AGENTS.md, CLAUDE.md v2.1 live (ADR-53)").
- **Current HEAD (verified this session):** **`2a980ab`** — `git -C ai-council
  log --oneline -1` → unchanged.
- **Movement since refresh:** **NONE.** ai-council has not committed since the
  2026-05-25 refresh basis.
- **Consequence:** the 2026-05-25 audit refresh + execution plan remain **current
  and authoritative**. No re-refresh is warranted; every `file:line` citation in
  them still holds. This session did **not** re-audit ai-council (out of scope).

## Existing artifacts (location + migration note)

Currently at `.dev-knowledge/docs/research/` (pre-migration):
- `2026-05-25-ai-council-universalization-audit-refresh.md`
- `2026-05-25-ai-council-universalization-execution-plan.md`
  (carries an Amendment 2026-05-26 capturing the five operator decisions.)

**Migration recommendation (NOT in this session's scope):** for consistency with
the cross-repo `docs/audits/` convention adopted 2026-05-26 (this session writes
all four other repos' refreshes + plans there), the two ai-council artifacts
should move `docs/research/` → `docs/audits/`. That is separate cleanup work; a
`.dev-knowledge` BACKLOG entry is recommended. Until moved, they remain
authoritative where they are.

## Findings summary (per the 2026-05-25 refresh — not re-derived)

- **14 findings:** 7 carry-forward (from the 2026-05-23 ai-council deep audit) +
  7 delta (post-2026-05-23 standards).
- **Severity:** 0 CRITICAL · 0 HIGH · **5 MEDIUM** (AR-CF1 codemap form, AR-CF3
  ADR-naming guidance, AR-D1 VISION tier-residue+missing-status, AR-D4 CLAUDE
  tier-residue prose, AR-D5 README disposition) · **9 LOW**.
- **Conformance:** ~90% (2026-05-23 baseline) → **~70%** (2026-05-25 standard) —
  the drop is the standard moving under a frozen repo (tier-residue surfaced,
  README re-scoped, root-hygiene pass-2 added), not regression.
- **Audit tool:** `vision_md` **WARN** (missing `status`), `adr38_baseline` PASS,
  `claude_md` PASS. (Note: ai-council is the one repo whose VISION is missing the
  `status` key — corp-monorepo already has it; corp-ops/corp-sca have no VISION
  at all.)

## Execution plan summary (per the 2026-05-25 plan + 2026-05-26 amendment)

- **8 required actions + 1 optional** (Action 9 LESSONS scope-tag backfill —
  deferred).
- **Operator decisions baked in (2026-05-26 amendment):** README = **delete**;
  codemap = **hand-authored Mermaid** (no generator); `.env.example` = **remove**;
  LESSONS backfill = **defer**; workspace tier-residue = **separate BACKLOG entry**.
- **Net scope:** Actions 1–8 (frontmatter/prose de-tier, ADR-08 rename, codemap
  Mermaid upgrade, root hygiene), small–medium session.

## Status: BLOCKED on execution

ai-council universalization is **not yet executed**. A dedicated ai-council
session (with write access to ai-council) is required to run the 2026-05-25 plan.
This `.dev-knowledge` session does not execute it (Layer-2 invariant).

## Cross-repo coordination note

The 2026-05-25 refresh + plan remain authoritative until either:
- a dedicated ai-council session **executes** the plan (closes the work), or
- ai-council **HEAD moves materially** (would require re-running the refresh —
  not the case as of this check).

## How ai-council compares to the four repos audited this session

| Axis | ai-council | corp-monorepo | corp-ops | corp-sca |
|---|---|---|---|---|
| Prior baseline | 2026-05-23 | 2026-05-23 | none (initial) | none (initial) |
| Tier residue | yes (VISION+CLAUDE+`[L-opt]` tags) | yes (VISION+CLAUDE) | none | none |
| Mandatory files present | all 4 | all 4 | missing 3 | missing 3 |
| Audit tool | 1 WARN | 3 PASS | 2 FAIL | 2 FAIL |
| Conformance | ~70% | ~72% | ~45% | ~45% |
| README | present (external-ish) | present (product) | present (internal) | present (internal) |

**Pattern:** ai-council + corp-monorepo are **residue-cleanup** repos (all files
present, tier-residue to strip, near-green audit tool overstating ~70% standard
conformance). corp-ops + corp-sca are **creation** repos (governance scaffold
absent, audit tool red, ~45%, no residue). ai-council and corp-monorepo are the
two with prepared plans closest to ready; corp-ops/corp-sca need files built.

---

**Contract preserved:** zero `ai-council/` files modified (read-only per
ADR-28/ADR-36; this session only ran `git log` to verify HEAD). All writes
confined to `.dev-knowledge/docs/audits/`.
