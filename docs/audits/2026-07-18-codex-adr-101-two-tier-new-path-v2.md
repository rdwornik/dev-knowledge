# Codex Review — adr-101-two-tier-new-path-v2

**Date:** 2026-07-18
**Branch:** `docs/adr-101-two-tier-new-path-rule`
**HEAD:** `6fbb87cd`
**Diff range:** `6fbb87cd~2..6fbb87cd`
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

### HIGH — docs/decisions/ADR-101-hermetization.md:162

**What:** The “Universal rule” says the gate currently allows all compliant files and the executor proceeds, but line 169 says this is target policy pending #345/#346 and line 195 says the executor rule is not landed.  
**Why:** The amendment simultaneously describes an unimplemented behavior as active fleet-wide policy.  
**Fix direction:** Qualify the universal-rule bullets as target doctrine pending #345/#346, or remove the later “not active” qualification once implemented.

### HIGH — docs/decisions/README.md:88

**What:** The ADR-101 index summary repeats the gate/executor behavior as present fact without the ADR’s pending #345/#346 limitation.  
**Why:** The navigation entry contradicts the decision record and can authorize readers to act on behavior that is not active.  
**Fix direction:** Summarize it as target policy pending the registry and executor-rule follow-ups.

## Medium

### MEDIUM — docs/decisions/ADR-101-hermetization.md:159

**What:** The amendment is dated 2026-07-18 but cites a binding ruling “relayed from corp-monorepo 2026-07-19”; calling that a provenance label does not establish when the ruling was actually made or relayed.  
**Why:** The decision’s chronology remains non-auditable and appears future-dated from the record’s perspective.  
**Fix direction:** Cite the source artifact and actual relay timestamp/timezone, or use an unambiguous source-date label.

## Low

(none)
