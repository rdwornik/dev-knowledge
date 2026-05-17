# Governance essences — ADRs driving directives in this handoff

2-4 sentence operational essences. Full ADR text lives in
`.dev-knowledge/docs/decisions/`. Selected because the action plan in
`07_ACTION_PLAN.md` depends on these rules.

---

## ADR-33 — VISION.md universalization

Every repo with one or more dependents must carry a `VISION.md` at root.
Standard tier (full template) for L/M repos; Lite tier for S repos. The
VISION states mission, scope, dependents, strategic emphasis. Directive 2
(corp-monorepo rollout preparation) must account for ADR-33 compliance —
the monorepo's VISION is the anchor for any governance simplification
plan against it.

Full ADR: `.dev-knowledge/docs/decisions/ADR-33-vision-universalization.md`

---

## ADR-38 — Universal repo architecture baseline

Defines mandatory file presence per scale tier (S/M/L). Scale M+ requires
`ARCHITECTURE.md`, `BACKLOG.md`, `LESSONS.md`, `JOURNAL.md`, `README.md`,
`VISION.md`, `CLAUDE.md`, `CONTRIBUTING.md` at root. Scale L additionally
requires `src/` + `pyproject.toml`. Directive 2 (corp-monorepo rollout
preparation) must explicitly address ADR-38 Scale L compliance gaps as
part of the deliberately-scaled plan.

Full ADR: `.dev-knowledge/docs/decisions/ADR-38-universal-repo-architecture.md`

---

## ADR-41 — Cross-session backlog architecture

`BACKLOG.md` mandatory at M+ tier. Done items LEAVE the file — they are
not tombstoned with `[done]` status. Trace of completed work lives in
git history + JOURNAL `Changes:` line. Abandoned items get a short note
in `docs/decisions/`, not a tombstone in BACKLOG. Directly grounds
BOUNDARY: "Do NOT close BACKLOG items as tombstone entries."

Full ADR: `.dev-knowledge/docs/decisions/ADR-41-cross-session-backlog-architecture.md`

---

## ADR-42 — Handoff format v3 (currently v3.3.3)

Three-stage handoff flow with full Stage 2 mandate for ALL types
(audit-sync, session-sync, feature-X-sync — no shortcuts). Stage 3
bundle is 11 flat files (12 for cross-repo with `02b_ECOSYSTEM_VISION.md`).
HEAD validation uses ancestor check (`git merge-base --is-ancestor
{stage1_sha} HEAD`), not strict equality. Directly grounds BOUNDARY:
"Do NOT amend the handoff process or its governing ADR on the basis of
this single handoff" — template changes require empirical evidence from
multiple real runs (pattern: universal-without-cross-case-verification,
LESSON #9, 2026-05-14).

Full ADR: `.dev-knowledge/docs/decisions/ADR-42-handoff-format-v3.md`

---

## Council Simplification 2026-05-16 (ADR-46 + ADR-47 demoted to non-enforced)

The 2026-05-16 Council Simplification trimmed governance machinery:
audit reduced to structural-only checks; `CHANGELOG.md` and
`BACKLOG_ARCHIVE.md` deleted (git history + JOURNAL `Changes:` line are
authoritative); scope-tag enforcement system removed (tags remain as
informal metadata); ADR-46 + ADR-47 demoted to non-enforced conventions.
This is the model Directive 2 must scale up for corp-monorepo. It also
directly grounds three BOUNDARIES: no `CHANGELOG.md` / `BACKLOG_ARCHIVE.md`
resurrection; no scope-tag enforcement re-introduction; no casual
addition of new audit checks or governance rules.

Full ADRs: `.dev-knowledge/docs/decisions/ADR-46-cross-repo-dated-entries-format.md`
and `.dev-knowledge/docs/decisions/ADR-47-cross-repo-backlog-organization.md`
