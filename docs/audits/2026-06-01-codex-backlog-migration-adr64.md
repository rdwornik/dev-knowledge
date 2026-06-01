# Codex Review — backlog-migration-adr64

**Date:** 2026-06-01
**Branch:** `docs/backlog-migration-adr64-2026-06-01`
**HEAD:** `4b9401b`
**Diff range:** `main..docs/backlog-migration-adr64-2026-06-01`
**Codex version:** codex-cli 0.131.0
**Mode:** diff-review

---

## Focus

scripts/validate_backlog.py: logic correctness, false positives/negatives, edge cases; does it verify id uniqueness AND monotonicity or only presence; is the Coordination section-exemption safe (still rejects done there); regex robustness for entry/field parsing; Layer-2 read-only. .pre-commit-config.yaml: validate-backlog hook wiring (files regex, pass_filenames, language).

---

## Findings
## Critical

(none)

## High

## [HIGH] scripts/validate_backlog.py:83 — ID validation only checks presence/numeric form, not uniqueness or monotonicity

**What:** The validator hard-fails only when `id` is missing or non-numeric; it never checks for duplicate IDs or that IDs increase monotonically through the file.  
**Why:** `PLAYBOOK.md` now makes `id:` a monotonic, never-reused integer so commit references like `[#<id>]` stay unambiguous. As written, duplicate or out-of-order IDs pass pre-commit and silently break that indexing contract.  
**Fix direction:** Track seen IDs and fail on duplicates; also enforce a strictly increasing ID sequence in file order (and, if required by policy, preserve/check a last-issued watermark so removed IDs cannot be reused later).

## [HIGH] scripts/validate_backlog.py:64 — `repo:` is parsed but never enforced as a required field or as a section boundary

**What:** The parser captures `repo`, but `validate()` never checks that it exists, that non-Coordination items are `.dev-knowledge`, or that child-repo values appear only under `## Coordination`.  
**Why:** The migration’s split-brain boundary depends on `repo:`. In the current implementation, an execution item for `corp-monorepo` can sit in `## Open` and still pass, and an item can omit `repo:` entirely, defeating the per-repo routing rule.  
**Fix direction:** Make `repo:` required, require `.dev-knowledge` outside `## Coordination`, and only allow child-repo / cross-repo values inside `## Coordination` (with an explicit allow-list if values like `ecosystem` are intentional).

## [HIGH] scripts/validate_backlog.py:35 — malformed section structure can slip through as valid entries

**What:** `_SECTION_RE` recognizes only four exact H2 names, and `parse()` keeps the previous `section` until another recognized one appears. Entries under an unknown/mistyped H2, or before any valid section, are therefore recorded with the wrong section or `None` instead of hard-failing as malformed structure.  
**Why:** That creates false negatives in the exact area this validator is meant to protect: a retired or mistyped heading can let entries pass under the wrong status rules, or avoid section/status validation entirely.  
**Fix direction:** Treat unknown H2/H3 structure as a hard failure, and require every parsed entry to belong to an explicitly recognized section/priority shape before validation continues.

## Medium

(none)

## Low

(none)
