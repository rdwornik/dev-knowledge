# ADR-31: Authority Model — Prescriptive with Conformance Audit

**Status:** Accepted
**Date:** 2026-04-27
**Stream:** C, session 1
**Supersedes:** none
**Superseded by:** none

## Context

`.dev-knowledge` had no formally declared authority model. The 2026-04-27 AI Council session (Topic 1) was convened after three verification failures in a single session revealed that manual drift detection is structurally fragile. The debate evaluated four options:

- **1A (Light reference):** `.dev-knowledge` documents patterns; downstream repos may deviate freely
- **1B (Prescriptive with conformance audit):** `.dev-knowledge` prescriptions are binding; drift detected via centralized read-only audit tool
- **1C (Hub-and-spoke binding tags):** per-rule advisory/binding classification
- **1D (Push-down enforcement):** validator scripts deployed as pre-commit hooks into each downstream repo

Panel: claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.20. Synthesizer: openai (non-participant). Debate transcript: `docs/decisions/transcripts/DECISION_28_authority_model.md`.

## Decision

Adopt **1B: Prescriptive with conformance audit**.

### Authority model

`.dev-knowledge` is the **binding source of cross-repo prescriptions**. Downstream repos (corp-monorepo, ai-council, and any future repos) must conform to cross-repo rules documented here. "Binding" operationally means: violations appear in the centralized audit and must be remediated when flagged, not that every commit is gated.

### Enforcement mechanism (V1)

Enforcement is **out-of-band, centralized, read-only**:

- A manual audit tool lives in `.dev-knowledge/tools/audit.py` (or shell equivalent)
- Reads sibling repos via explicit manifest (e.g., `repos.toml`; exact filename and format determined at implementation time) — no path-guessing
- Missing repo path emits a loud error, not a vacuous pass
- Emits a single Markdown report (`AUDIT.md`) with ✓/❌ per repo per rule
- Supports `<!-- audit:exempt reason=... -->` comments in target files to suppress known-false-positives; exemptions tracked in `JOURNAL.md`
- Includes test fixtures (known-good and known-bad examples) in `tools/tests/`
- Invocation: manual. PLAYBOOK documents: "Run `audit.py` at the start of any cross-repo session and at end of week"

### Baseline rule: violations fixed before audit ships

The audit tool must run green (✓ all checks) on its first invocation. A red-on-arrival audit is operationally dead — it trains the operator to ignore output. The 3 violations known at decision time must be fixed as a prerequisite:

- `ai-council`: add `AGENTS.md`
- `ai-council`: trim `CLAUDE.md` to ≤200 lines
- `corp-monorepo`: replace `AGENTS.md` with correct template

### Scale tier

`.dev-knowledge` remains **Scale M**. One Scale-L artifact is adopted: `ARCHITECTURE.md`, to document the guardian/audit system contract (repo discovery model, what "binding" means operationally, audit lifecycle and output). No other L-tier artifacts are warranted for a solo doc repo.

### Content layout

Cross-repo prescriptions remain in **PLAYBOOK + ADRs**. A dedicated `cross-repo/` subfolder is deferred until active prescription count exceeds ~10 or navigation becomes painful.

## Rejected alternatives

- **1A (Light reference):** rejected because manual drift detection already failed in practice — 3 violations existed silently for multiple sessions before accidental discovery. Choosing less would formalize the failure.
- **1D (Push-down enforcement):** rejected because pre-commit hooks in business-critical repos (`corp-monorepo`, `ai-council`) have unbounded blast radius. A bug in a validator script blocks commits during pre-sales work. `SKIP_CHECKS=1` escape hatches are not reliable under stress. Strongest decisive argument: "the actual failure mode is detection, not enforcement."
- **1C (Hub-and-spoke binding tags):** deferred, not rejected. Introduce per-rule advisory/binding taxonomy after the audit model has run for ~3 months and demonstrates which rules actually drift.

## Consequences

**Positive:**
- Single command (`audit.py`) answers "is the ecosystem compliant?" — replaces fragile manual verification
- Blast radius of governance tooling failures is zero (a wrong audit report ≠ a blocked commit)
- Co-located with what it checks; maintenance stays in one repo

**Costs / accepted risks:**
- Audit only catches drift when Rob runs it; forgotten audit = no improvement over status quo. Mitigation: PLAYBOOK ritual + audit records its last-run timestamp
- Lazy-fix for violations not yet covered by an audit check; JOURNAL entries track these explicitly

**Revisit triggers:**
- A second prescription becomes load-bearing for a non-local workflow (remote push, collaborator) → reconsider 1D push-down for that specific rule
- Same violation re-appears across multiple sessions → lazy-fix is failing; escalate for that class
- Active prescription count exceeds ~10 → revisit `cross-repo/` subfolder and per-rule taxonomy
- ADR-35 (Stream C session 6) reclassifies `.dev-knowledge` to Scale L → revisit Scale section of this ADR

## References

- Debate transcript: `docs/decisions/transcripts/DECISION_28_authority_model.md`
- ADR-27: scope tagging (pre-commit hook — example of a `.dev-knowledge`-resident enforcement artifact)
- ADR-28: three-layer architecture (`.dev-knowledge` as Layer 1, prescriptions flowing to Layer 2/3)
- ADR-35: Scale tier assessment (scheduled, Stream C session 6) — deferred
