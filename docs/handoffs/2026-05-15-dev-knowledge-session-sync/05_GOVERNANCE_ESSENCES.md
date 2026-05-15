# Governance Essences — .dev-knowledge (session-sync, 2026-05-15)

<!-- scope: meta -->

Operational rules from ADRs cited in `07_ACTION_PLAN.md` directives.
2-4 sentences each. Full ADRs at the paths below.

---

## ADR-36 — Audit Tool Architecture

`.dev-knowledge` is the ecosystem auditor. The audit tool reads child repos
(read-only hard constraint) and writes only to `.dev-knowledge/ecosystem/`,
`.dev-knowledge/docs/audits/`, and `.dev-knowledge/docs/handoffs/`. P1 MVP
delivers: Click CLI (`audit run`, `audit health`), ecosystem state schema
(`ecosystem/{repo}/state.yaml` + append-only `history/`), three baseline
checks (VISION.md/ADR-33, ADR-38 root files, ADR-31 CLAUDE.md), and a
single markdown report to `docs/audits/YYYY-MM-DD-ecosystem-audit.md`.
P2 (handoff folder generator), P3 (scheduled runs), P4 (LLM-augmented
narrative) are separate sessions.

Full ADR: `.dev-knowledge/docs/decisions/ADR-36-audit-tool-architecture.md`

---

## ADR-38 — Universal Repo Architecture Baseline

Every ecosystem repo at Scale M+ must have these files at root: `BACKLOG.md`,
`LESSONS.md`, `VISION.md`, `README.md`, `CHANGELOG.md`, `JOURNAL.md`.
`ARCHITECTURE.md` is required at Scale L; `CLAUDE.md` and `CONTRIBUTING.md`
are also expected. The audit tool's check #2 verifies this baseline across
repos. Verify the exact mandatory-files list against the full ADR before
implementing — the architect-inferred list may differ from the canonical spec.

Full ADR: `.dev-knowledge/docs/decisions/ADR-38-universal-repo-architecture.md`

---

## ADR-33 — VISION.md Universalization

Every repo under `Dev/` must have a `VISION.md` at root with parseable YAML
frontmatter containing at minimum: `version`, `tier`, `owner`,
`last_reviewed`, `scale`, `status`. The audit tool's check #1 verifies
VISION.md presence and frontmatter parseability. Repos missing VISION or with
malformed frontmatter are non-compliant and generate P1 audit findings.

Full ADR: `.dev-knowledge/docs/decisions/ADR-33-vision-universalization.md`

---

## ADR-31 — Authority Model

`.dev-knowledge` uses a prescriptive authority model with conformance audit
(Option 1B): prescriptions are binding, drift is detected via the centralized
read-only audit tool. The audit tool's check #3 verifies `CLAUDE.md` presence
at repo root — the governance contract file. Repos without `CLAUDE.md` lack
the binding governance authority source.

Full ADR: `.dev-knowledge/docs/decisions/ADR-31-authority-model.md`

---

## ADR-40 — Scale Tier Evaluation Algorithm

Scale tiers (S/M/L) govern governance obligations: `BACKLOG.md` is mandatory
at M+; `ARCHITECTURE.md` at L; ADR directory at L. The audit tool reads the
`scale:` field from each repo's `VISION.md` frontmatter and cross-checks
against `ecosystem/{repo}/state.yaml` intended scale. When ADR-40's
algorithmic tier computation is implemented (separate future session), the
audit tool will compare declared tier against computed tier. For P1 MVP,
declared scale is the sole source; mismatch detection is a P2 scope item.

Full ADR: `.dev-knowledge/docs/decisions/ADR-40-scale-tier-evaluation.md`
