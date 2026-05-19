---
date: 2026-05-19
type: audit
scope: rollout-readiness
repos: [.dev-knowledge, ai-council]
adrs: [ADR-51, ADR-52]
status: complete
---

# Rollout-Readiness Audit — ADR-51 / ADR-52

**Date:** 2026-05-19
**Branch:** `audit/rollout-readiness-2026-05-19`
**HEAD at audit time:** `f942ab951dfb9fd8e97d46a93f8dc45c7027d503`
**Purpose:** Independent verification of `.dev-knowledge` `main` state + gap analysis of `.dev-knowledge` and `ai-council` against ADR-51 (ARCHITECTURE.md convention) and ADR-52 (AGENTS.md convention). Read-only assessment — no repo content changed.

---

## Part A — `.dev-knowledge` main: independent state verification

State verified by inspecting actual repo state (git log, file reads) — NOT from session summaries.

### A1. Git state

| Check | Result |
|-------|--------|
| HEAD SHA | `f942ab951dfb9fd8e97d46a93f8dc45c7027d503` |
| Working tree | Clean (0 staged, 0 unstaged) |
| Branch | `main` |
| Expected HEAD from session (merge of codex-review sidequest) | `f942ab9` ✓ |

### A2. Session commits — VERIFIED / DISCREPANCY per reported item

**Reporting session 1: "Action Plan Directives 1+2+3" (2026-05-19)**

| SHA | Message | Status |
|-----|---------|--------|
| `18da5b5` | `docs(audits): add corp-monorepo ARCHITECTURE.md inspection report` | **VERIFIED** |
| `3cc7197` | `docs(decisions): add ADR-52 AGENTS.md cross-tool agent-instruction contract convention` | **VERIFIED** |
| `1be2f8b` | `docs(playbook): clarify AGENTS.md is an agent-instruction contract, not handoff content` | **VERIFIED** |
| `2acaa96` | `feat(templates): add canonical ARCHITECTURE.md template per ADR-51` | **VERIFIED** |
| `706c4ba` | `docs(backlog): record codemap generator output spec as open item` | **VERIFIED** |
| `7f0129b` | `fix(templates): apply codex-review HIGH/MEDIUM/LOW findings to ARCHITECTURE template` | **VERIFIED** |
| `0425f3e` | `docs(journal): 2026-05-19 — Action Plan Directives 1+2+3 executed` | **VERIFIED** |

**Reporting session 2: "codex-review sidequest" (2026-05-19)**

| SHA | Message | Status |
|-----|---------|--------|
| `b1747f1` | `docs(logs): append TOKEN-LOG entry 2026-05-10 to 2026-05-19` | **VERIFIED** |
| `dbdc53a` | `chore(audits): remove stale codex-review artifact for markdown template` | **VERIFIED** |
| `7ef77f0` | `docs(playbook,essentials): document codex-review code-only rule + path-guard` | **VERIFIED** |
| `4c2c65b` | `docs(journal,lessons): close codex-review sidequest — misdiagnosis correction + path-guard` | **VERIFIED** |
| `c53d383` | `Merge branch 'fix/codex-review-hook'` | **VERIFIED** |
| `f942ab9` | `docs(handoff): merge ai-council session-sync handoff branch` | **VERIFIED** (HEAD) |

### A3. File existence and non-triviality

| File | Status | Notes |
|------|--------|-------|
| `templates/ARCHITECTURE-template.md` | **VERIFIED** — exists, 272 lines | |
| `docs/decisions/ADR-52-agents-md-convention.md` | **VERIFIED** — exists, 42 lines | |
| `protocols/PLAYBOOK.md` §16 code-only rule | **VERIFIED** — paragraph present at line 2167: "Code-only rule (per-change codex-review)..." | |
| `protocols/ESSENTIALS.md` doc-only note | **VERIFIED** — present: "Codex-review is for code review, not markdown/prose — diffs of only .md / governance files are skipped cleanly" | |

### A4. Template content: ADR-51 mandatory core sections

Verified `templates/ARCHITECTURE-template.md` against ADR-51 Decision 4 ("Every covered ARCHITECTURE.md contains: bird's-eye purpose statement; codemap; explicit layer boundaries and architectural invariants").

| Section | Present | Notes |
|---------|---------|-------|
| `## Purpose [CORE]` | **VERIFIED** | One focused paragraph, present-tense, no preamble |
| `## Codemap [CORE]` | **VERIFIED** | `<!-- CODEMAP:START/END -->` markers, transitional hand-maintained format + canonical target stub |
| `## Layer Boundaries & Invariants [CORE]` | **VERIFIED** | Layer model, module-to-layer table, numbered invariants |

**Scale conditionals verified:** `[CORE]`, `[M/L]`, `[L-opt]`, `[L]` section tags present throughout template ✓

**Frontmatter fields:** `scale:`, `last_reviewed:`, `status:`, `owner:` — all present ✓

**Open item note:** Template contains the correct notice that the codemap generator output spec is undecided (ADR-51 open question); transitional hand-maintained form is documented as a stopgap ✓

### A5. ADR-52 wording check

Verified `docs/decisions/ADR-52-agents-md-convention.md` for "excluded from handoff bundles" or equivalent over-reach wording.

**Result: NO such wording present.** ADR-52 Decision 4 states: "AGENTS.md is an agent-instruction contract, not a repo-descriptive document. The Claude-oriented handoff process must not narrate, summarize, or manage AGENTS.md as Claude-side repo-descriptive handoff content." — scoped correctly to handoff narration, not to handoff bundle inclusion mechanics. **VERIFIED** ✓

### A6. codex-review path-guard

Inspected `~/.claude/bin/codex-review.ps1` for path-guard block.

**Result: VERIFIED** — path-guard block present after diff-range resolution:
```powershell
# --- Code-only path-guard ---...
$codeExtensions = @('.py','.ps1','.psm1','.sh',...'.ini')
function Get-CodeFiles([string[]]$paths) { ... }
```
Empty-diff guard and FullAudit-no-src/ guard also confirmed present ✓

### A7. pytest status

```
50/51 passed
FAILED: test_audit_run_passes_structural_checks_on_synthetic_repo
  (adr38_baseline — missing 'tests', missing ARCHITECTURE.md)
```

Pre-existing failure per JOURNAL 2026-05-19 entries. All other 50 tests pass.

**Note on JOURNAL discrepancy:** The 2026-05-19 Action Plan session summary in JOURNAL cited `test_ratio_pass_when_stable_above_ceiling` as the known failure name. The actual failing test is `test_audit_run_passes_structural_checks_on_synthetic_repo`. The JOURNAL entry itself corrects this: "the Stage 3 `06_STATE_OF_PLAY.md` named `test_ratio_pass_when_stable_above_ceiling` as the known failure; the actual failing test is the audit-baseline one." This is a **DISCREPANCY** in the Stage 3 handoff document, correctly self-diagnosed by the session author. Not a `.dev-knowledge` main state discrepancy — the test itself is the authoritative source.

### A8. Headline finding

No major discrepancies between session summaries and actual repo state. All reported commits exist with correct SHAs. All reported files exist and are non-trivial. The one discrepancy (wrong test name in Stage 3 handoff) was self-diagnosed in JOURNAL and is a handoff document error, not a repo state error.

**`.dev-knowledge` `main` state: VERIFIED as reported.**

---

## Part B — `.dev-knowledge` gap analysis vs ADR-51 + ADR-52

### B1. ADR-51 gap: ARCHITECTURE.md

`.dev-knowledge` has an `ARCHITECTURE.md` at root (pre-existing, version 1.0, last_reviewed 2026-04-28). It does NOT conform to the ADR-51 template.

**Mandatory CORE gaps:**

| Gap | Severity | Detail |
|-----|----------|--------|
| No `## Purpose [CORE]` section | HIGH | Document opens with "Three-layer architecture" — no standalone purpose statement conforming to the template's "bird's-eye, present-tense, no preamble" definition |
| Codemap non-conformant | HIGH | `## Repository layout` has a tree but no `<!-- CODEMAP:START/END -->` markers, no per-entry layer labels, no scale declaration, no transitional-form notice |
| Layer Boundaries non-conformant | HIGH | "Three-layer architecture" section exists but has no structured layer table, no numbered invariants, no enforcement tool/config spec. "Layer 2 never executes" is an invariant but not in the numbered assertion format |

**Frontmatter gaps:**

| Gap | Severity |
|-----|----------|
| `version: 1.0` present instead of `scale:` field | MEDIUM |
| No conformance to ADR-51 frontmatter schema (`scale:`, `last_reviewed:`, `status:`, `owner:`) | MEDIUM |
| (Note: `last_reviewed:` and `owner:` actually present — but `scale:` missing and `version:` is a non-template field) | — |

**Section tag gaps:**

| Gap | Severity |
|-----|----------|
| No `[CORE]`, `[M/L]`, `[L-opt]`, `[L]` section tags | LOW |

**Staleness gaps (content now incorrect):**

| Gap | Severity | Detail |
|-----|----------|--------|
| References `CHANGELOG.md` in repository layout tree | MEDIUM | `CHANGELOG.md` deleted 2026-05-16 per Council Simplification |
| References `scripts/validate_scope_tags.py` in Validators section | MEDIUM | Deleted 2026-05-16 per Council Simplification |
| ADR governing list stops at ADR-32 | LOW | 20 additional ADRs exist (33–52); list is materially incomplete |
| "Key conventions" section references the ADR-27 hybrid-ratio enforcement as active | MEDIUM | Enforcement withdrawn 2026-05-16; now informal-only per CLAUDE.md |

**Conformance verdict:** ARCHITECTURE.md requires a full rewrite to template. Three CORE sections are missing or structurally non-conformant; content references deleted artifacts.

**Effort estimate: M** (medium — the content exists and can be adapted; the work is structural restructuring + content refresh, not authoring from scratch)

### B2. ADR-52 gap: AGENTS.md

| Check | Status |
|-------|--------|
| `AGENTS.md` exists at `.dev-knowledge` root | **MISSING** ❌ |

`.dev-knowledge` has no `AGENTS.md`. Per ADR-52 + PLAYBOOK §AGENTS.md, Scale M repos are expected to have AGENTS.md (Council #28: "AGENTS.md required at Scale M+"). ADR-52 defines the 10-section template as the conformant implementation.

**This is the most urgent conformance gap**: `.dev-knowledge` governs AGENTS.md for all downstream repos but does not itself have one.

**Effort estimate: M** (the template is well-defined; `.dev-knowledge` content is well-known; this is primarily authoring work filling in the 10 sections)

---

## Part C — `ai-council` gap analysis vs ADR-51 + ADR-52 (read-only)

**Scale tier:** M (declared in `ai-council/AGENTS.md` §2 "Scale tier: M")

### C1. ADR-51 gap: ARCHITECTURE.md

| Check | Status |
|-------|--------|
| `ARCHITECTURE.md` at repo root | **MISSING** ❌ |

`ai-council/` root contains: `AGENTS.md`, `CLAUDE.md`, `BACKLOG.md`, `JOURNAL.md`, `LESSONS.md`, `VISION.md`, `README.md`, `pyproject.toml` — no `ARCHITECTURE.md`.

Scale M = mandatory per ADR-51 Decision 1.

**Effort estimate: M** (ai-council has a clear architecture per AGENTS.md §3; authoring the ARCHITECTURE.md is primarily writing up what is already known in structured form)

### C2. ADR-52 gap: AGENTS.md

`ai-council/AGENTS.md` exists and is substantially complete. Verified against the 10-section template:

| Section | Status | Notes |
|---------|--------|-------|
| §1 Read first | ✓ CONFORMANT | Absolute paths to ESSENTIALS + PLAYBOOK |
| §2 Repo identity | ✓ CONFORMANT | All fields populated |
| §3 Architecture | ✓ CONFORMANT | Detailed; enforcement and advisory documented |
| §4 Conventions | ✓ CONFORMANT | Filenames, branches, commits, testing, linting |
| §5 Tools active | ✓ CONFORMANT | Codex, pre-commit hooks, API key env |
| §6 Gotchas | ✓ CONFORMANT with deviation | Uses `.claude/rules/` rather than `.claude/skills/gotchas/SKILL.md`. Deviation is documented and legitimate — ai-council uses repo-rules not skills. |
| §7 Council decisions | ✓ CONFORMANT (minor gap) | Ecosystem ADRs listed; ADR-52 absent (ratified 2026-05-19; AGENTS.md last updated 2026-05-17) |
| §8 Out of scope | ✓ CONFORMANT | |
| §9 Session start checklist | ✓ CONFORMANT | |
| §10 Do NOT | ✓ CONFORMANT | |

**Minor gaps:**

| Gap | Severity |
|-----|----------|
| ADR-52 missing from §7 binding ADRs list | LOW |
| Template version stamp (2026-04-24) predates ADR-52 (2026-05-19) — version not updated after ADR-52 ratification | LOW |
| §7 ecosystem ADR list missing ADR-51 (architecture doc convention now binding at Scale M) | LOW |

**Conformance verdict:** Substantially conformant. Only minor bookkeeping gaps (ADR-51, ADR-52 missing from §7).

**Effort estimate: S** (add ADR-51 + ADR-52 to §7, bump version stamp — 15 minutes)

---

## Part D — Recommended rollout order and effort

### Rollout sequence

| Order | Repo | Work item | Convention | Effort | Blocker? |
|-------|------|-----------|-----------|--------|----------|
| 1 | `.dev-knowledge` | Create `AGENTS.md` from template | ADR-52 | M | No |
| 2 | `.dev-knowledge` | Rewrite `ARCHITECTURE.md` to ADR-51 template | ADR-51 | M | No |
| 3 | `ai-council` | Create `ARCHITECTURE.md` from ADR-51 template | ADR-51 | M | No |
| 4 | `ai-council` | Add ADR-51 + ADR-52 to `AGENTS.md` §7; bump version | ADR-52 | S | No |

### Rationale

1. **`.dev-knowledge` AGENTS.md first** — eliminates the irony of the governance repo that defines AGENTS.md not having one. Not blocked.
2. **`.dev-knowledge` ARCHITECTURE.md rewrite second** — needs care (content refresh + structural rewrite); keeps the governance repo in full conformance before pushing to children.
3. **`ai-council` ARCHITECTURE.md third** — the bigger authoring lift; benefits from `.dev-knowledge` conformance being established first (clean reference).
4. **`ai-council` AGENTS.md bookkeeping last** — purely additive; no dependency.

### What is NOT in scope for this rollout

- **Codemap generator** — ADR-51 mandates auto-generated codemap but the generator output spec is undecided (ADR-51 open question, tracked in BACKLOG Stream C P2). All rollout work uses the hand-maintained transitional text form documented in the template.
- **CI freshness check** — same blocker as codemap generator; deferred until generator ships.
- **`corp-monorepo`** — not in the current rollout cohort (its ARCHITECTURE.md was inspected 2026-05-19 as reference input; migration to root + template conformance is a separate task).
- **`corp-ops`** — trigger-based rollout (pending per JOURNAL 2026-05-19).

---

**Prepared by:** Claude Code (Sonnet 4.6), read-only pass
**Pre-commit gate:** passed (50/51 pytest; known failure `test_audit_run_passes_structural_checks_on_synthetic_repo` pre-existing, out of scope)
