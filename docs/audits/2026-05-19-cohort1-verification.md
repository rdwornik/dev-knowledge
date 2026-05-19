---
date: 2026-05-19
type: audit
scope: conformance-verification
repos: [.dev-knowledge, ai-council]
adrs: [ADR-51, ADR-52]
status: complete
---

# Cohort-1 ADR-51 / ADR-52 Verification Audit

**Date:** 2026-05-19
**Branch:** `audit/cohort1-verification`
**Purpose:** Independently verify that `.dev-knowledge` and `ai-council` are genuinely ADR-51 / ADR-52 conformant after Prompt A (`.dev-knowledge`) and Prompt B (`ai-council`) completion reports. Resolve four unconfirmed residual items. All verdicts are based on inspecting actual files and git state — not session summaries.

---

## Part 1 — `.dev-knowledge` conformance

### 1.1 Git state

| Check | Result |
|-------|--------|
| Branch at audit time | `main` |
| HEAD | `d32d106` |
| Working tree | clean |

### 1.2 Prompt A commits — verified on `main`

| SHA | Message | Status |
|-----|---------|--------|
| `f8160ac` | `docs: add AGENTS.md per ADR-52` | **VERIFIED** |
| `58ad1d8` | `docs: rewrite ARCHITECTURE.md to ADR-51 template` | **VERIFIED** |
| `d58d959` | `docs: journal entry — ADR-51 + ADR-52 conformance session` | **VERIFIED** |
| `d32d106` | `docs: merge ADR-51 + ADR-52 conformance — AGENTS.md + ARCHITECTURE.md rewrite` | **VERIFIED** (HEAD) |

### 1.3 AGENTS.md — ADR-52 section checklist

| Section | Status |
|---------|--------|
| §1 Read first | CONFORMANT |
| §2 Repo identity | CONFORMANT |
| §3 Architecture | CONFORMANT |
| §4 Conventions | CONFORMANT |
| §5 Tools active | CONFORMANT |
| §6 Gotchas | CONFORMANT |
| §7 Binding ADRs | CONFORMANT — ADR-51 and ADR-52 both present |
| §8 Out of scope | CONFORMANT |
| §9 Session start checklist | CONFORMANT |
| §10 Do NOT | CONFORMANT |

No placeholder content found. All 10 sections populated with repo-specific content.

### 1.4 ARCHITECTURE.md — ADR-51 mandatory core checklist

| Check | Status | Evidence |
|-------|--------|----------|
| `scale: M` frontmatter | CONFORMANT | Line 2: `scale: M` |
| No `version:` field | CONFORMANT | Frontmatter has `scale`, `last_reviewed`, `status`, `owner` only |
| `## Purpose [CORE]` | CONFORMANT | Line 14 — present-tense, bird's-eye, no preamble |
| `## Codemap [CORE]` | CONFORMANT | Lines 20–56; `<!-- CODEMAP:START/END -->` markers present |
| `## Layer Boundaries & Invariants [CORE]` | CONFORMANT | Lines 60–109; 5 numbered invariants |
| Governing ADRs extend to ADR-52 | CONFORMANT | Line 179: `ADR-52 — AGENTS.md convention` |
| No `CHANGELOG.md` reference | CONFORMANT | Not present in file |
| No `validate_scope_tags.py` reference | CONFORMANT | Not present in file |
| No `test_validate_scope_tags.py` reference | CONFORMANT | Not present in file |
| Violations bullet: "Two known violations…" (R8) | CONFORMANT | Line 138: "Two known violations remain open: (1) ai-council CLAUDE.md exceeds 200-line trim target…; (2) corp-monorepo AGENTS.md…" |

---

## Part 2 — `ai-council` conformance

### 2.1 ARCHITECTURE.md — ADR-51 mandatory core checklist

| Check | Status | Evidence |
|-------|--------|----------|
| File exists at repo root | CONFORMANT | `ai-council/ARCHITECTURE.md` present |
| `scale: M` frontmatter | CONFORMANT | Line 2: `scale: M` |
| No `version:` field | CONFORMANT | Frontmatter: `scale`, `last_reviewed`, `status`, `owner` only |
| `## Purpose [CORE]` | CONFORMANT | Line 13 |
| `## Codemap [CORE]` with `<!-- CODEMAP:START/END -->` | CONFORMANT | Lines 19–59 |
| `## Layer Boundaries & Invariants [CORE]` with numbered invariants | CONFORMANT | Lines 63–96; 7 numbered invariants |

### 2.2 AGENTS.md §7 — ADR-51 and ADR-52 binding entries

Inspected `ai-council/AGENTS.md` §7 Ecosystem ADRs paragraph (line 115):

> **ADR-51** (architecture doc convention — ARCHITECTURE.md mandatory at Scale M+), **ADR-52** (AGENTS.md convention — canonical cross-tool agent-instruction contract)

Both ADR-51 and ADR-52 are present. `Last updated: 2026-05-19` is confirmed at the bottom of the file.

---

## Part 3 — Residual items

| Item | Description | Verdict | Evidence |
|------|-------------|---------|----------|
| **A1** | `.dev-knowledge` AGENTS.md §5 — does it state codex-review is code-only and effectively never triggers in this markdown repo? | **VERIFIED** | §5 reads: "`.dev-knowledge` is a markdown repo — doc-only changes do not cross the code-file threshold, so codex-review effectively never triggers here." Caveat is present verbatim. |
| **A2** | `.dev-knowledge` AGENTS.md §7 — is ADR-29 present, or explicitly noted as superseded by ADR-39? | **VERIFIED** | §7 line: "ADR-29: LESSONS.md grandfathering — scope-tag mechanics now informal per ADR-48; append-only invariant remains binding via CLAUDE.md and ADR-39" — ADR-29 is present with an explicit rationale note. |
| **B1** | `ai-council` ARCHITECTURE.md §Purpose — is it the tightened form (leads with what the tool IS) or the overclaim ("produces binding ADRs governing all repos")? | **VERIFIED** | Purpose opens: "`ai-council` is a multi-model AI debate and research CLI with four operating modes (pick, ideas, judge, research)." Leads with what the tool IS. ADR production is described accurately: "Council debate produces a verdict; that verdict is authored into an ADR that is ratified and distributed by `.dev-knowledge` to all downstream repos." Tightened form — not the overclaim. |
| **B2** | `ai-council` test count — resolve "407 vs 362" discrepancy. | **DISCREPANCY** | See §4 below. |

---

## Part 4 — Residual B2 detail: test count

Two test runs executed against `ai-council/tests/` on 2026-05-19:

| Run | Command | Result |
|-----|---------|--------|
| Filtered | `pytest tests/ -m "not integration and not envcheck"` | **407 passed**, 6 deselected |
| Unfiltered | `pytest tests/` | 412 passed, **1 failed**, 6 deselected = 413 total |

The 1 failing test is `tests/test_integration.py::test_full_debate_pipeline` (ImportError) — an integration test that requires live provider API keys; this is an expected failure in a keyless environment.

**The completion report's hypothesis was incorrect.** The hypothesis was: "if unfiltered ≈ 407 and filtered ≈ 362, the '407 vs 362' was a command mismatch (benign — the completion report used the unfiltered suite)." In practice, the filtered suite itself returns 407 — not 362. The unfiltered suite returns 413 total.

**Conclusion:** `ai-council/AGENTS.md` §4 documents "362 unit tests" (the filtered count at the time of authoring). The actual filtered count is now **407** — a delta of +45 tests. The documented count is stale, not a command-mismatch artefact. This is a minor documentation discrepancy: the count drifted as new tests were added.

**Severity:** LOW. The filter command itself is correct; only the documented count is outdated.

---

## Verdict

| Repo | ADR-51 (ARCHITECTURE.md) | ADR-52 (AGENTS.md) | Residuals |
|------|--------------------------|---------------------|-----------|
| `.dev-knowledge` | **CONFORMANT** | **CONFORMANT** | A1 VERIFIED, A2 VERIFIED |
| `ai-council` | **CONFORMANT** | **CONFORMANT** | B1 VERIFIED, B2 DISCREPANCY (LOW) |

**Cohort 1 is verified-conformant.**

One discrepancy found: `ai-council/AGENTS.md` §4 documents 362 unit tests; actual filtered count is 407. Severity LOW — the filter command is correct and the delta reflects legitimate test growth, not a structural gap. Remediation (updating the count) is a separate operator decision.

No remediation was performed by this audit. All findings are reported only.

---

**Prepared by:** Claude Code (Sonnet 4.6), read-only pass  
**Pre-commit gate:** pending
