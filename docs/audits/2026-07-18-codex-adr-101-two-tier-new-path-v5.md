# Codex Review — adr-101-two-tier-new-path-v5

**Date:** 2026-07-18
**Branch:** `docs/adr-101-two-tier-new-path-rule`
**HEAD:** `9189ce5b`
**Diff range:** `9189ce5b~1..9189ce5b`
**Codex version:** codex-cli 0.144.5
**Mode:** doc-review

---

## Focus

(none specified)

---

## Findings
## Critical

(none)

## High

### docs/decisions/ADR-101-hermetization.md:164 — Intake path authorization lacks the governing filename rule

**What:** The “currently-effective set” authorizes intake files merely “under `docs/intake/` (ADR-98),” but ADR-98 establishes the home, not the filename grammar.  
**Why:** This permits a reader to treat any new filename in that directory as pattern-sanctioned and proceed, despite the actual `YYYY-MM-DD-{func|tech}-slug.md` rule living in `docs/intake/README.md §4`.  
**Fix direction:** Cite the intake README’s naming section and state the filename pattern alongside the intake-home reference.

## Medium

(none)

## Low

(none)
