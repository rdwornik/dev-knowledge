# .dev-knowledge BACKLOG

Cross-session pending items across active streams. See ADR-41 for
schema and grooming cadence.

Last full grooming: 2026-04-30 (Phase 1 closure + self-audit + ai-council audit closure)
Next quarterly grooming: 2026-07-01

---

## Stream A: corp-monorepo

(no items currently — populate as Phase 2 universalization begins)

## Stream B: ai-council

(no items currently — populate as Phase 2 universalization begins)

## Stream C: .dev-knowledge governance

### [P1] [open] HANDOFF_PROCESS + HANDOFF_TEMPLATE + first-message.md updates
- **What:** Update process docs to reflect ADR-37 (two-phase) + ADR-41 (BACKLOG) integration; deprecate ADR-32 §4 in favor of BACKLOG reference. Includes SESSION_SETUP.md updates: BACKLOG review step at session start (per ADR-41 enforcement), audit tool trigger guidance (per ADR-36), JOURNAL update step at handoff generation (per ADR-39 enforcement requirement).
- **Why:** ADR-37 and ADR-41 ratified but templates still v2.0; need v3.0 reflecting overlay + backlog enforcement
- **Vision ref:** VISION.md "Methodology Author" function
- **Added:** 2026-04-30 by rob (Phase 1 closure session)
- **Status:** open

### [P1] [open] PLAYBOOK content additions for ADRs 36/37/40/41
- **What:** Add PLAYBOOK.md sections for ADR-36 (audit tool usage workflow), ADR-37 (two-phase handoff format guidance), ADR-40 (tier transition procedures S→M and M→L), ADR-41 (BACKLOG grooming workflow per-handoff and quarterly cadence). Update PLAYBOOK header version/date to reflect content amendments.
- **Why:** PLAYBOOK lifecycle (per ADR-39) update trigger is "ADR ratification adding/changing process." 4 ADRs ratified 2026-04-30 add/change process; PLAYBOOK currently mentions only ADR-33/34. Methodology debt.
- **Vision ref:** VISION.md "Methodology Author" function
- **Added:** 2026-04-30 by rob (Phase 1 self-audit)
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

### [P2] [open] ESSENTIALS.md cheat-sheet additions for ADRs 35-41
- **What:** Review which of ADRs 35-41 warrant high-leverage cheat-sheet rules in ESSENTIALS.md. Candidates: lessons retrieval shortcut (ADR-35), audit tool trigger conditions (ADR-36), two-phase handoff quick reference (ADR-37), tier evaluation signals (ADR-40), BACKLOG grooming cadence rules (ADR-41). Apply ESSENTIALS.md "Keep under 1 page" constraint — judgment call which warrant inclusion.
- **Why:** ESSENTIALS lifecycle update trigger is "lessons promotion, methodology change." Significant methodology change occurred 2026-04-30. Audit observed 226 lines (already over "1 page") so additions require pruning OR explicit relaxation of constraint.
- **Added:** 2026-04-30 by rob (Phase 1 self-audit)
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

### [P3] [open] ADR-39 registry decision — 5 unregistered template files
- **What:** Decide whether `templates/AGENTS-md-template.md`, `templates/CLAUDE-md-template.md`, `templates/codex-review-config-template.md`, `templates/prompt-template.md`, plus any other template-category files require ADR-39 registry entries. Options: (a) add registry entries with template-specific lifecycle; (b) formally exclude templates as a class via ADR-39 amendment ("template files exempt from registry"); (c) hybrid — register only stable templates, exclude transient. Decision required because ADR-39 says "every file in .dev-knowledge MUST have 6 lifecycle elements."
- **Why:** Audit surfaced unregistered files. Either we extend registry or formally narrow scope. Drift risk if neither.
- **Added:** 2026-04-30 by rob (Phase 1 self-audit)
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

### [P2] [open] Council research — relative repo complexity evaluation in solo dev / LLM workflows
- **What:** Council research debate. Question: how do professionals evaluate repo complexity at relative scale (small/medium/large) in solo dev and LLM-driven workflows? Current ADR-40 algorithm (logarithmic Maintainability Index pattern) may embed enterprise-scale assumptions inappropriate for 1-person ecosystem. Surface industry practice — surveys, blog posts, indie hacker conventions, monorepo tools' tier definitions for personal vs team scale. Plus philosophical framing: at what point does a small project become medium, medium become large, when complexity grows logarithmically? Output informs ADR-40 amendment alongside audit tool P1 multi-repo data collection.
- **Why:** All ecosystem repos currently classify L per ADR-40 (calibration concern surfaced 2026-04-30 ai-council audit, finding F-08). Research before amendment ensures evidence-based decision rather than gut-feel coefficient adjustment. Dependency: pair with audit tool P1 multi-repo data; both inform ADR-40 amendment.
- **Vision ref:** VISION.md "Methodology Author" + "Auditor" functions
- **Added:** 2026-04-30 by rob (ai-council audit Faza A2 closure)
- **Status:** open

### [P3] [open] Cross-repo audit (Phase 3)
- **What:** Audit tool runs across all repos with VISION.md, generates ecosystem compliance report; verifies adoption of ratified ADRs
- **Why:** Validates universalization actually adopted (not just ratified); drift detection over time
- **Vision ref:** VISION.md "Auditor" function
- **Added:** 2026-04-30 by rob
- **Status:** open

---
