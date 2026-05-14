# Governance Essences — ai-council (session-sync, 2026-05-14)

<!-- scope: meta -->

Operational essences for ADRs cited in `07_ACTION_PLAN.md` directives and
boundaries. 2-4 sentences each. For the full ADR text, see the reference path.

---

## ADR-01 — Synthesizer Selection

Gemini is the current default non-participating synthesizer, selected after
Claude Sonnet timed out on 5-model transcripts. The ADR is due for amendment
to codify a cost-optimization principle: synthesizer selection must prefer the
lowest-cost model meeting the synthesis quality rubric; higher-cost tiers are
reserved for cases where lower tiers demonstrably fail. Amendment is gated on
empirical scoring data from `docs/synthesis-quality-rubric.md`.

Full ADR: `docs/decisions/ADR-01-synthesizer-selection.md` (ai-council repo)

---

## ADR-34 — File Naming Convention (cross-repo)

Universal mandate across .dev-knowledge and all child repos: use **hyphens** as
separators in all filenames and foldernames; code files follow language convention.
Living docs use UPPERCASE; ADRs use `ADR-NN-topic.md` (hyphen). The ADR
prefix is grandfathered. A fresh ADR-34 violation (`SYNTHESIS-QUALITY-RUBRIC.md`)
was caught and corrected during recent ai-council work — the convention is
empirically easy to slip.

Full ADR: `.dev-knowledge/docs/decisions/ADR-34-file-naming-convention.md`

---

## ADR-38 — Universal Repo Architecture Baseline

Every repo at Scale M or above must have `src/`, `tests/`, `docs/decisions/`,
`README.md`, `VISION.md`, `CHANGELOG.md`, and `BACKLOG.md` at root.
`ARCHITECTURE.md` is optional at Scale M where `CLAUDE.md` Architecture section
provides equivalent coverage. Compliance is verified by `git ls-files` spot-check
targeting the mandatory root files.

Full ADR: `.dev-knowledge/docs/decisions/ADR-38-universal-repo-architecture.md`

---

## ADR-41 — Cross-Session Backlog Architecture (BACKLOG.md)

Scale M and L repos must maintain `BACKLOG.md` at root as the single source of
pending items; embedding backlogs inside JOURNAL, README, or handoff §4 is
deprecated at these tiers. Each repo owns its own BACKLOG; one repo does not
reconcile or direct work on another repo's BACKLOG — cross-repo work flows via
operator-carried routing artifacts.

Full ADR: `.dev-knowledge/docs/decisions/ADR-41-cross-session-backlog-architecture.md`

---

## ADR-36 — Audit Tool Architecture (read-only contract)

`.dev-knowledge` is the ecosystem auditor; audit artifacts (reports, handoffs)
live in `.dev-knowledge/docs/`. The read-only contract means ai-council sessions
**never write to .dev-knowledge files** — the information flow is one-way
(audit reads target repo; target repo does not write back). Operator hand-carries
any cross-repo artifacts.

Full ADR: `.dev-knowledge/docs/decisions/ADR-36-audit-tool-architecture.md`

---

## ADR-42 — Handoff Format v3 (three-stage flow)

All handoffs (audit-sync, session-sync, feature-X-sync) execute the full
three-stage flow: Stage 1 (Claude Code generates question prompt), Stage 2
(OLD chat provides architect response), Stage 3 (Claude Code generates 11-file
folder). `docs/HANDOFF.md` flat-file pattern is deprecated; handoffs live in
`docs/handoffs/` as ADR-42 folder bundles. The ai-council `docs/HANDOFF.md` was
already deleted during recent docs hygiene work.

Full ADR: `.dev-knowledge/docs/decisions/ADR-42-handoff-format-v3.md`
