# Codex Review — adr-101-two-tier-new-path-v4

**Date:** 2026-07-18
**Branch:** `docs/adr-101-two-tier-new-path-rule`
**HEAD:** `2a6c18b3`
**Diff range:** `2a6c18b3~1..2a6c18b3`
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

- `docs/decisions/ADR-101-hermetization.md:159` — The amendment claims a binding operator ruling “relayed from corp-monorepo 2026-07-19” while this commit and amendment are dated 2026-07-18.  
  **What:** The asserted source event occurs after the document records it as binding.  
  **Why:** It cannot support the amendment’s current “in force now” disposition, so the governance record is temporally invalid.  
  **Fix direction:** Correct the provenance date/source, or mark the rule pending until the cited ruling actually exists; reconcile the dependent status claims and index summary.

- `docs/decisions/ADR-101-hermetization.md:162` — The new text says the executor behavior is already in force and #346 only persists it, contradicting BACKLOG #346’s statement that this global executor rule still needs its own explicit operator ruling.  
  **What:** Two authoritative planning surfaces disagree on whether agents may proceed-with-citation now.  
  **Why:** Executors receive opposite authorization guidance for path creation.  
  **Fix direction:** Resolve whether the operator ruling covers executor behavior; update either this amendment or #346 to express one authoritative status.

## Medium

- `docs/decisions/ADR-101-hermetization.md:164` — “Pattern-sanctioned” is not actionable before #345’s registry exists.  
  **What:** The rule permits files matching “every other pattern the registry below enumerates,” but the registry is explicitly only a design proposal; several listed classes also lack a precise filename grammar in this amendment.  
  **Why:** Readers cannot reliably determine whether a path is compliant, despite ambiguity requiring STOP.  
  **Fix direction:** Enumerate the currently effective patterns with exact governing sources/grammars, explicitly defer registry-only patterns until #345, and clarify that path authorization does not authorize an underlying ADR or other decision.

## Low

(none)
