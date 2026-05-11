# 05_GOVERNANCE_ESSENCES.md — ADR Essences

Operational rules for ADRs cited in `07_ACTION_PLAN.md` directives.
2–4 sentences each. NOT full ADR text — read full ADR if precision required.

---

## ADR-33 — VISION.md Universalization

Any project under `Dev/` with ≥1 dependent MUST have a `VISION.md`.
**Lite tier** (4 mandatory sections: Vision, Scope, Relationships, Lifecycle)
applies to repos that are consumers of .dev-knowledge methodology without
producing their own methodology layer. Frontmatter `tier:` field required
in all VISION.md files; `last_reviewed` field must be updated at review.
DoD for Lite-tier VISION: frontmatter parseable + **4 required sections**
(not 5 — Standard tier has 6).

Full ADR: `.dev-knowledge/docs/decisions/ADR-33_vision_universalization.md`

---

## ADR-36 — Audit Tool Architecture

`.dev-knowledge` is the ecosystem auditor; audit runs are read-only — no
writes to target repos. P1 MVP checks: VISION.md presence + frontmatter
parseable + scale declared + ADR-31 baseline + universal architecture compliance.
Audit outputs live in `.dev-knowledge/docs/audits/YYYY-MM-DD-{repo}-{topic}.md`;
format: findings by priority (P1/P2/P3), each finding with recommendation.
Audit tool P1 implementation is BACKLOG Stream C P1 — not yet built; manual
audit is current workaround.

Full ADR: `.dev-knowledge/docs/decisions/ADR-36_audit_tool_architecture.md`

---

## ADR-37 — Session Boundary Protocol (Two-Phase Handoff)

Every handoff has two top-level sections: `## Current State` (verified
factual status, decisions made, open questions) and `## Future State`
(goals, directives, boundaries). These are authoritative; if they contradict
the Detailed Context (9-section body), Current/Future State wins.
Session handoffs: MEDIUM mandate — two-phase framing expected with "undetermined"
justification if omitted. Audit handoffs: STRONG mandate.

Full ADR: `.dev-knowledge/docs/decisions/ADR-37_session_boundary_protocol.md`

---

## ADR-40 — Scale Tier Evaluation Algorithm

Repos classified S/M/L using composite Tier Score (adapted Maintainability
Index: logarithmic combination of TCR tokens, test count, module count;
higher score = simpler = S). Current calibration concern F-08: all repos
classify L under current coefficients — architect judgment allowed to
override algorithm pending recalibration. Tier drives governance obligations:
BACKLOG.md mandatory at M+, ARCHITECTURE.md + AGENTS.md at L.
Audit tool P1 multi-repo data collection will inform ADR-40 amendment.

Full ADR: `.dev-knowledge/docs/decisions/ADR-40_scale_tier_evaluation.md`

---

## ADR-41 — Cross-Session Backlog Architecture

BACKLOG.md is the canonical cross-session pending-items queue at M+ tier.
Schema: stream sections (A/B/C/D/Cross-stream), priority tags [P1/P2/P3],
status [open/done], required fields **What/Why/Vision ref/Added/Status**.
Update protocol: lightweight per-handoff (update status, add new items);
deep grooming quarterly (remove stale, reprioritize). Never restructure
sections unilaterally — section changes require grooming session.
Items in BACKLOG are not duplicated into handoff bundles; handoff references
BACKLOG by item name.

Full ADR: `.dev-knowledge/docs/decisions/ADR-41_cross_session_backlog_architecture.md`

---

## ADR-42 — Handoff Format v3.2

Three-stage flow: Stage 1 (Claude Code generates question prompt) → Stage 2
(OLD browser chat answers 5 pipeline questions as architect) → Stage 3
(Claude Code generates 11-file flat folder). Stage 2 is mandatory for ALL
handoff types — no shortcuts. Stage 2.5 (optional Q&A loop, max 3 rounds
between NEW and OLD chat) between Stage 2 and Stage 3.
Return trip: `09_EXECUTION_EVIDENCE.md` filled by NEW chat after executing
directives; returned to `.dev-knowledge` for next session verification.
Drift detection: Stage 3 re-verifies HEAD SHA; mismatch → FLAG to Rob before proceeding.

Full ADR: `.dev-knowledge/docs/decisions/ADR-42_handoff_format_v3.md`
