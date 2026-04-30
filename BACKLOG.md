# .dev-knowledge BACKLOG

Cross-session pending items across active streams. See ADR-41 for
schema and grooming cadence.

Last full grooming: 2026-04-30 (Phase 1 closure — added Phase 1 validation P1)
Next quarterly grooming: 2026-07-01

---

## Stream A: corp-monorepo

(no items currently — populate as Phase 2 universalization begins)

## Stream B: ai-council

(no items currently — populate as Phase 2 universalization begins)

## Stream C: .dev-knowledge governance

### [P1] [open] HANDOFF_PROCESS + HANDOFF_TEMPLATE + first-message.md updates
- **What:** Update process docs to reflect ADR-37 (two-phase) + ADR-41 (BACKLOG) integration; deprecate ADR-32 §4 in favor of BACKLOG reference
- **Why:** ADR-37 and ADR-41 ratified but templates still v2.0; need v3.0 reflecting overlay + backlog enforcement
- **Vision ref:** VISION.md "Methodology Author" function
- **Added:** 2026-04-30 by rob (Phase 1 closure session)
- **Status:** open

### [P1] [open] Audit tool P1 implementation
- **What:** Build .dev-knowledge audit tool per ADR-36 — P1 MVP (audit run + ecosystem state + markdown report). Implement compute_tier_score, classify_tier per ADR-40.
- **Why:** Required for Phase 2 universalization per repo; algorithmic tier classification (ADR-40) needs implementation to operationalize
- **Vision ref:** VISION.md "Auditor" function
- **Added:** 2026-04-30 by rob
- **Status:** open

### [P2] [open] Lessons activation P1 implementation
- **What:** Build lessons-index.json + retrieval (SessionStart hook) + querying (CLI) per ADR-35
- **Why:** Activates LESSONS.md from passive archive to active feedback loop; bidirectional pipeline corrections.jsonl ↔ LESSONS.md ↔ ~/.claude/rules/
- **Added:** 2026-04-30 by rob
- **Status:** open

### [P2] [open] PLAYBOOK update — tier transition procedures
- **What:** Add tier transition procedures section to PLAYBOOK.md per ADR-40 decisions (S→M, M→L procedures, audit checks, timelines)
- **Why:** Procedures codified in ADR-40 but operational doc (PLAYBOOK) not yet updated
- **Added:** 2026-04-30 by rob
- **Status:** open

### [P3] [open] Council CLI dual-write trigger logic
- **What:** Define when Council debates dual-write to .dev-knowledge vs ai-council/output only; flag-based or auto-detect (research+pick=curated, test=no-curated)
- **Why:** Test debates currently pollute curated transcripts; surfaced 2026-04-30 session
- **Added:** 2026-04-30 by rob
- **Status:** open

### [P3] [open] ADR-39 amendment — BACKLOG.md lifecycle entry
- **What:** Amend ADR-39 registry to add BACKLOG.md entry per ADR-41
- **Why:** Lifecycle compliance per ADR-39; deferred to grouped amendment to minimize ADR churn
- **Added:** 2026-04-30 by rob
- **Status:** open

## Stream D: corp-sca-time-automation

(no items currently — trigger-based migration per ADR-33)

## Cross-stream / Ecosystem

### [P1] [open] Phase 1 validation — audit + handoff dry-run on ai-council
- **What:** Manual audit ai-council (per ADR-36 architecture, computing tier per ADR-40 manually since audit tool not yet implemented). Generate handoff folder per ADR-37 two-phase format. Transfer handoff to new claude.ai chat for ai-council. Evaluate: did handoff preserve methodology, model/mode/effort context, ADR awareness, BACKLOG context, two-phase Current/Future state framing? Findings inform audit tool P1 implementation and HANDOFF_PROCESS template updates.
- **Why:** End-to-end validation of Phase 1 governance (8 ADRs ratified) before further implementation work. Without this, audit tool P1 implementation is blind to real-world gaps; HANDOFF_PROCESS template updates are theoretical. Real test of whether ratified architecture translates to working process. Gates other P1 items (audit tool implementation, template updates) — those should be informed by validation findings.
- **Vision ref:** VISION.md "Auditor" + "Disseminator" functions
- **Added:** 2026-04-30 by rob (Phase 1 closure session)
- **Status:** open

### [P2] [open] Phase 2 universalization rollout
- **What:** Apply ADR-33/34/35/37/38/39/40/41 to ai-council and corp-monorepo (immediate cohort per ADR-33)
- **Why:** Validates universalization pattern; unblocks trigger-based cohort migration; first per-repo audit + handoff cycle
- **Vision ref:** VISION.md "Disseminator" function
- **Added:** 2026-04-30 by rob
- **Status:** open

### [P2] [open] VISION.md tier declarations across ecosystem
- **What:** Update VISION.md frontmatter `tier:` field across all repos per ADR-40 calibration baseline (corp-ops=S, ai-council=M, corp-monorepo=L, etc.)
- **Why:** Operationalizes ADR-40 algorithm; declared tier vs computed tier comparison enables audit findings
- **Added:** 2026-04-30 by rob
- **Status:** open

### [P3] [open] Cross-repo audit (Phase 3)
- **What:** Audit tool runs across all repos with VISION.md, generates ecosystem compliance report; verifies adoption of ratified ADRs
- **Why:** Validates universalization actually adopted (not just ratified); drift detection over time
- **Vision ref:** VISION.md "Auditor" function
- **Added:** 2026-04-30 by rob
- **Status:** open

---
