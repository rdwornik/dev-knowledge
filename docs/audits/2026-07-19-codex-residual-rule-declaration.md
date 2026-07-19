# Codex Review — residual-rule-declaration

**Date:** 2026-07-19
**Branch:** `docs/residual-rule-declaration`
**HEAD:** `9c25f94f`
**Diff range:** `main..docs/residual-rule-declaration`
**Codex version:** codex-cli 0.144.5
**Mode:** diff-review

---

## Focus

- Does the written rule in protocols/HANDOFF_PROCESS.md accurately describe what scripts/validate_residual_completeness.py enforces?
- Is holding Version at 5.7 defensible for an additive normative rule, or does it require 5.7 -> 5.8 plus dependent reconciled_with reconciliation?
- ecosystem/doc-code-edge.yaml: is leaving residual_completeness in exempt: (bound to #365) correct, given coverage_scope needs BOTH a doc marker and a scripts/ code marker, and adding only the doc half yields broken_edge?
- BACKLOG #363/#364/#365: are the kill-candidates lines honest, and is any subsumed by an existing ticket?

---

## Findings
## Critical

(none)

## High

### ecosystem/doc-code-edge.yaml:123 — “7/7 match” claim is false

**What:** The protocol only says placeholder-bearing regions fail, but `region_is_unfilled()` also fails completely empty regions.  
**Why:** The authoritative rule understates the gate’s behavior, so an author can receive an undocumented hard failure.  
**Fix direction:** Add empty-region handling to the written rule, or narrow the validator predicate, before declaring the doc half verified.

### ecosystem/doc-code-edge.yaml:123 — Commit-refusal guarantee is overstated

**What:** The validator identifies staged changes via `git status` but scans working-tree files, and a clean post-commit ship-gate run checks nothing.  
**Why:** A staged unfilled blob followed by an unstaged filled edit can pass, so the commit containing the placeholder is not reliably refused.  
**Fix direction:** Validate staged blob content at commit time and distinguish that enforcement from clean-tree `/ship` behavior.

### ecosystem/doc-code-edge.yaml:123 — Doc-side completion is premature without a version bump

**What:** The branch adds a normative handoff rule while retaining `Version: 5.7`, despite every prior additive normative change using a minor bump.  
**Why:** Keeping 5.7 lets dependent `reconciled_with` declarations remain green without reviewing the new contract.  
**Fix direction:** Bump to 5.8, add the Section-history entry, and reconcile all `handoff-process@5.7` dependents.

## Medium

### ecosystem/doc-code-edge.yaml:128 — Planned promotion omits the multi-site edge shape

**What:** The comment describes one code marker, but this check has both an `audit.py` adapter and validator logic, matching the existing two-site Tier-3 pattern.  
**Why:** One marker can leave the real logic unbound; two markers without `multi_site: 2` become ambiguous.  
**Fix direction:** Have #365 add one doc marker, code markers at both adapter and logic sites, and `multi_site: handoff-residual-filled: 2`.

## Low

(none)

Leaving `residual_completeness` in `exempt:` is correct for this branch: adding only the doc marker would create the stated one-sided `broken_edge`. The health check currently passes, and 1,627 tests collect successfully.
