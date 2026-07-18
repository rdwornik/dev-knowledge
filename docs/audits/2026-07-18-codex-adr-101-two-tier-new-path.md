# Codex Review — adr-101-two-tier-new-path

**Date:** 2026-07-18
**Branch:** `docs/adr-101-two-tier-new-path-rule`
**HEAD:** `a95d9cb9`
**Diff range:** `main..docs/adr-101-two-tier-new-path-rule`
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

### docs/decisions/ADR-101-hermetization.md:162 — Active gate/authorization claim precedes its mechanisms

**What:** The amendment says the fleet gate already permits every compliant file and blocks any new folder, but the registry is explicitly “not built,” #345 still owns the gate change, and #346 still owns the executor rule.  
**Why:** Readers can treat an unimplemented, hub-only design as current fleet-wide authorization; “any new folder” also exceeds the retained Rule-A scope.  
**Fix direction:** State this as the target policy pending #345/#346, or land the registry, gate, and executor rule together before claiming active behavior.

## Medium

### docs/decisions/ADR-101-hermetization.md:193 — #344’s authorization condition is left contradictory

**What:** The fold-in requires compliant writes to proceed, while BACKLOG #344 still requires an explicit hub-ruling token for any consumer write into hub/global paths.  
**Why:** It is unclear whether a citation replaces, supplements, or is represented by that required token.  
**Fix direction:** Reconcile #344 and this amendment with one explicit authorization flow.

### docs/decisions/ADR-101-hermetization.md:157 — Future-dated amendment/ruling

**What:** The amendment records a 2026-07-19 operator ruling, while the review date is 2026-07-18.  
**Why:** A decision record cannot substantiate a future event.  
**Fix direction:** Correct the date or mark the text as a proposed/pending ruling until it occurs.

## Low

### docs/decisions/ADR-101-hermetization.md:159 — ADR-102 §1 citation is misleading

**What:** The text invokes ADR-102 §1 for “don’t spawn a parallel register,” then proposes a standalone registry. ADR-102 §1 instead chooses `parity-surfaces.yaml` over a duplicate parity register.  
**Why:** The citation obscures why a separate registry is appropriate here.  
**Fix direction:** Narrow the citation to the source-of-truth principle and explicitly distinguish this domain-specific registry from ADR-102’s rejected parity register.
