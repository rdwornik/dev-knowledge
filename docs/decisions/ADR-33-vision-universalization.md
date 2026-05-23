# ADR-33 — VISION.md universalization across ecosystem repos

<!-- scope: meta -->

**Status:** Accepted
**Date:** 2026-04-28
**Stream:** C, session 2
**Supersedes:** aspirational "should" in .dev-knowledge VISION.md Relationships
**Superseded by:** none
**Related:** ADR-30, ADR-31, ADR-32, transcript council-out-20260428-162415-pick-council-prompt-adr33-vision-universalization.md

## Context

`.dev-knowledge` has `VISION.md` as its mission anchor (per DECISION_30 transcript). The VISION.md Relationships section states child repos under `Dev/` "should" have their own VISION.md per template — this is aspirational. This ADR formalizes "should" into enforceable convention with per-Scale tiering and a migration plan.

Council debate (`council-out-20260428-162415-*`) surfaced 7 questions; this ADR records the decisions made.

## Decision

### Mandate (Q1: trigger-based, not Scale-based)

Any project under `Dev/` with **≥1 dependent** (other repos that consume its outputs, conventions, or APIs) MUST have a `VISION.md`. Scale tier (S/M/L) does not determine mandate — dependency does.

In practice: corp-monorepo, ai-council, corp-ops, corp-sca-time-automation all have dependents → all required. Future scripts/tools without dependents are exempt.

### Two-tier content (Q2)

Two `VISION.md` content tiers:

- **Standard tier:** full 6-section template per .dev-knowledge VISION (Vision, Scope, Values, Relationships, Lifecycle, References)
- **Lite tier:** 4 sections (Vision, Scope, Relationships, Lifecycle) with simplified Lifecycle (3–5 lines: review triggers + ownership only, no full verification mechanism)

Frontmatter `tier:` field REQUIRED in all `VISION.md` files. Values: `standard` | `lite`.

### Mandatory sections (Q3)

**Standard tier:** all 6 sections mandatory. Frontmatter (version, last_reviewed, owner, status, tier) mandatory.

**Lite tier:** Vision, Scope, Relationships, Lifecycle (simplified) mandatory. Frontmatter mandatory. Values + References optional — Lite repos may link to parent `.dev-knowledge` ESSENTIALS instead of duplicating.

### Child↔parent framing (Q4)

Child `VISION.md` is self-contained. No inheritance, no auto-sync. Brief pointer in Relationships section:

> Operates under .dev-knowledge methodology (see .dev-knowledge VISION.md for ecosystem context).

Loose coupling intentional — child repos remain portable; `.dev-knowledge` dependency stays at the methodology level.

### Migration (Q5: hybrid)

**Immediate cohort** (Stream C Phase 2, planned next sessions):
- ai-council
- corp-monorepo

**Trigger-based cohort** (corp-ops, corp-sca-time-automation, future repos):
- Trigger: next session that touches the repo for >1 commit, OR by 2026-06-30 — whichever comes first
- Soft deadline (workplace reality); audit at 2026-06-30 surfaces non-compliant repos

### Enforcement (Q6: hybrid, primary-secondary split)

**Primary (when available):** auditor tool in `.dev-knowledge` that walks `Dev/`, reads `VISION.md` from each repo with dependents, validates frontmatter parseable + recently reviewed + matches tier requirements. Implementation: separate ADR (Phase 3 work), out of scope here.

**Secondary baseline (now):** AGENTS.md / CLAUDE.md in each child repo MUST require reading `VISION.md` as part of session start ("Read first" section). Passive enforcement via AI agent reading order.

**Optional repo-level:** pre-commit hook validates `VISION.md` exists + frontmatter parseable. Per-repo opt-in (not mandated globally).

## Consequences

### Positive
- Universal mission framework across the ecosystem
- Each repo's purpose is discoverable in <2 min by reading `VISION.md`
- Drift detectable via VISION vs JOURNAL/CHANGELOG/ADRs comparison
- Future repos onboard via VISION template — no ad-hoc decisions
- Reinforces `.dev-knowledge` as universal brain pattern (per ADR-31 authority model)

### Negative
- Migration cost: 4 existing repos need `VISION.md` created (2 immediate + 2 trigger-based)
- Maintenance burden: `VISION.md` must be reviewed periodically (mitigated by trigger-based review per VISION Lifecycle)
- Lite tier ambiguity until first concrete Lite VISION is written and serves as the canonical example

### Follow-ups
- ai-council `VISION.md` creation (Stream C Phase 2)
- corp-monorepo `VISION.md` creation (Stream C Phase 2)
- Auditor tool spec + implementation (separate ADR, Phase 3)
- `VISION.md` template files in `templates/` for both tiers (separate small task)
- Re-audit at 2026-06-30 for trigger-based cohort compliance

## References

- `VISION.md` (.dev-knowledge canonical Standard tier example)
- DECISION_30 transcript (`docs/decisions/transcripts/council-out-20260428-125133-format-and-structure-of-visionmd-for-dev.md`)
- DECISION_31 transcript (`docs/decisions/transcripts/council-out-20260428-162415-pick-council-prompt-adr33-vision-universalization.md`)
- ADR-30 (default branch convention)
- ADR-31 (authority model — prescriptive with conformance audit)
- ADR-32 (handoff format)
- ESSENTIALS Project Scale Tiers section

## Amendments

### 2026-05-23 — Remove `tier:` and `scale:` from VISION frontmatter (tier system deprecated)

- **Source:** Operator decision 2026-05-23 (browser-chat), ecosystem-wide tier
  deprecation. Cross-references [[ADR-38]] amendment A5 (universal baseline) and
  ADR-40 deprecation, same date.
- **Status of original Decision blocks:** preserved above for decision-trace;
  this amendment supersedes the tier clauses within them.

**Delta.** The tier system is deprecated entirely. The two-tier content model
(`standard` / `lite`) and the `tier:` frontmatter requirement (Decision §
"Two-tier content (Q2)" / "Mandatory sections (Q3)") are withdrawn. The
parallel `scale:` field (introduced by ADR-36/ADR-40 audit practice, never
part of ADR-33's original schema) is likewise removed. No replacement field —
a single universal `VISION.md` form applies regardless of repo size.

**Amended frontmatter requirement.** Every `VISION.md` MUST carry frontmatter
with these keys (tier/scale removed):

```yaml
version: <string>
last_reviewed: <YYYY-MM-DD>
owner: <name>
status: <active | maintenance | archived>
```

**Content.** With tiering removed, `VISION.md` uses the full section set
(Vision, Scope, Values, Relationships, Lifecycle, References); a small repo may
keep any section to a few lines or link to parent `.dev-knowledge` ESSENTIALS
rather than duplicating. No section is gated on a declared tier.

**Audit impact.** `scripts/audit.py` `check_vision_md` validates the amended
required-key set (no `tier`/`scale`). See [[ADR-38]] amendment A5 for the
companion `check_adr38_baseline` change.

- **Decision tier:** Conversational (reconciliation of an already-decided
  operator directive).
