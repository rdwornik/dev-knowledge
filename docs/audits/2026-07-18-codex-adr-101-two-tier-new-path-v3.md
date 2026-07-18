# Codex Review — adr-101-two-tier-new-path-v3

**Date:** 2026-07-18
**Branch:** `docs/adr-101-two-tier-new-path-rule`
**HEAD:** `ace9b0b9`
**Diff range:** `6fbb87cd~1..ace9b0b9`
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

- **docs/decisions/ADR-101-hermetization.md:162; docs/decisions/README.md:88 — Pending executor rule is described as already binding executor behavior.**  
  **What:** Both say a compliant-file executor “follows/proceeds,” while ADR-101:195 and BACKLOG #346 say that behavior requires a separate global rule and operator ruling that have not landed.  
  **Why:** This can authorize new-path creation before its stated authority mechanism exists.  
  **Fix direction:** Until #346 lands, describe this as reviewer doctrine/target policy and require STOP for executors, or land the global rule and its ruling.

## Medium

- **docs/decisions/ADR-101-hermetization.md:159 — ADR-102 §1 is cited as authority for the amendment form, but does not support that claim.**  
  **What:** The text says ADR-102 §1 directs refinements to extend the authoritative source; that section instead chooses `parity-surfaces.yaml` over a duplicate parity register.  
  **Why:** It gives the in-file amendment and proposed registry a stronger, unrelated precedent than the cited ADR provides.  
  **Fix direction:** Retain ADR-94 as the amendment authority; reframe ADR-102 as a limited analogy or remove that citation.

## Low

(none)
