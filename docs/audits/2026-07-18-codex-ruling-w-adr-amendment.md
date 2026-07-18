# Codex Review — ruling-w-adr-amendment

**Date:** 2026-07-18
**Branch:** `docs/adr-36-41-ruling-w-hub-write-path`
**HEAD:** `6e10ba48`
**Diff range:** `bf8527e4~1..bf8527e4`
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

**High — docs/decisions/ADR-36-audit-tool-architecture.md:346**

**What:** The amendment assigns #344 Ask-2 to allow hub→consumer worktree writes and block direct consumer-checkout writes.  
**Why:** #344 Ask-2 instead guards consumer-session writes to hub/global paths; it cannot enforce this inverse-direction worktree policy.  
**Fix direction:** Remove or correct the #344 cross-reference; define a separate mechanism for enforcing hub→consumer worktree mediation.

**High — docs/decisions/ADR-41-cross-session-backlog-architecture.md:344**

**What:** This repeats the incorrect claim that #344’s consumer-side guard enforces the RULING-W hub→consumer pathway.  
**Why:** It creates conflicting boundary semantics between the authoritative backlog task and this ADR amendment.  
**Fix direction:** Align the amendment with #344’s actual consumer→hub scope, or amend #344 under its required ruling process.

**High — docs/decisions/ADR-41-cross-session-backlog-architecture.md:353**

**What:** The text says `seed_runbook.py` is now sanctioned for consumer fan-out, while the reviewed revision’s docstring still says consumer fan-out is deferred and that the tool is not the sanctioned path.  
**Why:** A reader could invoke the seeder contrary to its own documented boundary, defeating the claimed mechanism-before-act discipline.  
**Fix direction:** State the precise sanctioned invocation model and reconcile the seeder documentation before presenting it as enabled.

## Medium

(none)

## Low

(none)
