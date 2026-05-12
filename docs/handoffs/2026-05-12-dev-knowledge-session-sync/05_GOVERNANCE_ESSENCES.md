# Governance Essences — dev-knowledge session-sync (2026-05-12)

<!-- scope: meta -->

ADR operational essences for ADRs cited in `07_ACTION_PLAN.md` directives.
These are 2-4 sentence summaries — not full ADR copies. Read the full ADR for
complete rationale and amendment history.

---

## ADR-34 — File Naming Convention (cross-repo)

Hyphen (`-`) is the universal separator for ALL filenames and foldernames across
`.dev-knowledge` and every child repo under `Dev/`. This is a universal mandate
(amended 2026-05-11 from recommendation to mandate after cross-repo audit proved
recommendation-tier enforcement fails immediately). Code files follow language
conventions; governance/docs/handoffs use hyphen universally.

Full ADR: `docs/decisions/ADR-34-file-naming-convention.md`

---

## ADR-41 — Cross-Session Backlog Architecture (BACKLOG.md)

`BACKLOG.md` is the single canonical pending-items queue for M+ tier repos.
Items belong in BACKLOG, not scattered across handoff sections, JOURNAL, or
TODO comments. Schema: `[Priority] [Status] stream-heading + what/why/vision-ref/added/status`.
Update status at Stage 3 when items close; update per-handoff for lightweight
grooming and quarterly for deep grooming.

Full ADR: `docs/decisions/ADR-41-cross-session-backlog-architecture.md`

---

## ADR-42 — Handoff Format v3 (current: v3.2)

Three-stage handoff flow: Stage 1 (Claude Code generates questions for OLD chat),
Stage 2 (OLD chat answers 5 pipeline questions from lived knowledge), Stage 3 (Claude
Code generates 11-file flat folder). ALL handoff types run all three stages — no
shortcuts. `01_manifest.json` SHA-256 checksums prevent post-generation tampering.
Single-artifact handoffs are flat `.md` files in `docs/handoffs/`; folder format is
for multi-artifact bundles (ADR-42 amendment candidate surfaced 2026-05-12).

Full ADR: `docs/decisions/ADR-42-handoff-format-v3.md`

---

## ADR-43 — Cross-Repo Cycle Pattern (ai-council)

Note: ADR-43 lives in the `ai-council` repo, not in `.dev-knowledge`. Its operational
rule: cross-repo changes route via handshake artifacts — NOT unilateral edits. Flow:
(1) `.dev-knowledge` produces notification/propagation artifact; (2) operator routes
to target repo; (3) target repo architect proposes own implementation; (4) optional
closure turn. Handshake = 1 round trip per operator "single round trip" principle
(witnessed 2026-05-12). Multi-turn ceremony for S-scale changes is over-engineering.

Full ADR: `ai-council/docs/decisions/ADR-43-*.md` (verify path in ai-council repo)
