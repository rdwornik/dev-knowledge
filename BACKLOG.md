# .dev-knowledge BACKLOG

Cross-session pending items across active streams. See ADR-41 for
schema and grooming cadence.

Last full grooming: 2026-05-09 (P1 HANDOFF_PROCESS closed)
Next quarterly grooming: 2026-07-01

---

## Stream A: corp-monorepo

(no items currently — populate as Phase 2 universalization begins)

## Stream B: ai-council

(no items currently — populate as Phase 2 universalization begins)

## Stream C: .dev-knowledge governance

### [P1] [done] HANDOFF_PROCESS + HANDOFF_TEMPLATE + first-message.md updates
- **What:** Update process docs to reflect ADR-37 (two-phase) + ADR-41 (BACKLOG) integration; deprecate ADR-32 §4 in favor of BACKLOG reference. Includes SESSION_SETUP.md updates: BACKLOG review step at session start (per ADR-41 enforcement), audit tool trigger guidance (per ADR-36), JOURNAL update step at handoff generation (per ADR-39 enforcement requirement).
- **Why:** ADR-37 and ADR-41 ratified but templates still v2.0; need v3.0 reflecting overlay + backlog enforcement
- **Vision ref:** VISION.md "Methodology Author" function
- **Added:** 2026-04-30 by rob (Phase 1 closure session)
- **Status:** done (2026-05-09 — closed by ADR-42 ratification + v3.0 implementation; HANDOFF_PROCESS rewritten, HANDOFF_QUESTION_TEMPLATE + HANDOFF_FOLDER_TEMPLATE created, SESSION_SETUP.md updated, ai-council handoff regenerated)

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

### [P1] [done] Phase 1 validation — audit + handoff dry-run on ai-council
- **What:** Manual audit ai-council (per ADR-36 architecture, computing tier per ADR-40 manually since audit tool not yet implemented). Generate handoff folder per ADR-37 two-phase format. Transfer handoff to new claude.ai chat for ai-council. Evaluate: did handoff preserve methodology, model/mode/effort context, ADR awareness, BACKLOG context, two-phase Current/Future state framing? Findings inform audit tool P1 implementation and HANDOFF_PROCESS template updates.
- **Why:** End-to-end validation of Phase 1 governance (8 ADRs ratified) before further implementation work. Without this, audit tool P1 implementation is blind to real-world gaps; HANDOFF_PROCESS template updates are theoretical. Real test of whether ratified architecture translates to working process. Gates other P1 items (audit tool implementation, template updates) — those should be informed by validation findings.
- **Vision ref:** VISION.md "Auditor" + "Disseminator" functions
- **Added:** 2026-04-30 by rob (Phase 1 closure session)
- **Status:** done (2026-05-09 — Stage 3 folder generated at
  docs/handoffs/2026-05-09-ai-council-audit-sync/. Governance cycle complete
  from .dev-knowledge side. Execution test (NEW chat consuming bundle) is the
  next operational step — not tracked here; Rob opens new ai-council chat with
  bundle when ready.)

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

### [P1] [open] Council decisions management consolidation
- **What:** Council debates produce architectural decisions (ADRs), but decision artifacts are dispersed across `docs/decisions/`, `docs/decisions/transcripts/`, and ADR references in individual files. Need: (a) consolidated index of all decisions with traceability from decision to implementation, (b) explicit mechanism to detect contradictions between decisions over time, (c) clear ownership model for decision evolution (amendment vs. new ADR vs. conversational clarification). Scope: audit current dispersion, design consolidation pattern, implement index.
- **Why:** Dispersion observed during 2026-05-09 session work. As ADR count grows (42+), navigating, cross-referencing, and detecting drift becomes harder. Governance debt compounds silently.
- **Vision ref:** VISION.md "Knowledge Guardian" + "Methodology Author" functions
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Status:** open

### [P1] [open] Sacred-files maintenance enforcement
- **What:** Nine canonical files in every ecosystem repo (ARCHITECTURE, BACKLOG, CHANGELOG, CLAUDE, CONTRIBUTING, JOURNAL, LESSONS, README, VISION) drift out of date because browser chats forget to update them at session boundaries. Need enforcement mechanism — candidates: pre-commit hook checking `last_reviewed` staleness, session-end checklist skill, CI check for file age, or automated diff-based staleness detection. Scope: design enforcement pattern, implement at least one mechanism, validate against known drift scenarios.
- **Why:** Methodology debt pattern surfaced repeatedly across 2026-05-09 session (LESSONS captures multiple instances of "prescriptive writing without empirical contact"). Sacred files are the ground truth — stale ground truth silently misleads future sessions and chats.
- **Vision ref:** VISION.md "Knowledge Guardian" function; ESSENTIALS "Continuous Improvement" section
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Status:** open

### [P2] [open] Hooks audit + consolidation
- **What:** Two `review` hooks observed in ecosystem (one for Codex, one for internal review). Full hook inventory not documented. Need: (a) list all hooks across `.claude/` (global) and `.claude/` (project-level), (b) document each hook's purpose and trigger condition, (c) evaluate whether review hooks are intentionally separate or candidates for consolidation, (d) identify gaps (hooks that should exist but don't). Output: documented hook inventory + consolidation recommendation.
- **Why:** Undocumented hooks create confusion about what fires when. Two review hooks with overlapping purposes may produce redundant or conflicting signals.
- **Vision ref:** VISION.md "Methodology Author" function
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Status:** open

### [P2] [open] Skills universalization across repos
- **What:** Each repo has `.claude/skills/` (or equivalent) with skill definitions. Need cross-repo review: (a) inventory all skills across ecosystem repos, (b) classify each as repo-specific vs. cross-ecosystem candidate, (c) identify universalization targets — skills that should live in `.dev-knowledge` and be referenced/shared, (d) propose canonical location for universal skills. Output: skills inventory + universalization proposal.
- **Why:** Skills defined redundantly across repos create drift — same skill evolves differently in each context. Universalization reduces maintenance burden and ensures cross-repo consistency (per VISION Strategic emphasis: "Cross-repo methodology consistency").
- **Vision ref:** VISION.md Strategic emphasis "Cross-repo methodology consistency"
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Status:** open

### [P2] [open] Ecosystem standards audit against major repo
- **What:** Audit one significant ecosystem repo against current standards: folder naming (ADR-34), file naming (ADR-34), workspace structure (ADR-38), sacred-files presence (per set above), scope tag compliance (ADR-27). Surface drift items, classify by severity, plan remediation. Establish this as a repeatable pattern for auditing future repos.
- **Why:** Phase 2 universalization rollout (Cross-stream P2, above) needs a concrete audit run to validate the pattern works. Without an actual audit against a real repo, the process is theoretical.
- **Vision ref:** VISION.md "Auditor" function; pairs with "Phase 2 universalization rollout" (Cross-stream P2)
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Note:** Do not name specific repo in BACKLOG until audit scoping session decides target. See "Phase 2 universalization rollout" for cohort selection.
- **Status:** open

### [P3] [open] Kimi K2 model integration evaluation
- **What:** Evaluate Kimi K2 as addition to ecosystem LLM stack. Scope: (a) capability evaluation for Council debate quality, code generation, and reasoning depth, (b) cost comparison vs. Claude on equivalent task types, (c) integration patterns with existing infrastructure. Decision artifact: Council debate output recommending adoption level — research-only / production peer / experimental supplement.
- **Why:** Significantly lower cost than Claude on equivalent tasks (per Rob). Speed of LLM technology adoption is a competitive advantage (VISION Strategic emphasis: "Velocity in LLM technology adoption"). Evaluation before adoption; Council debate before production use.
- **Vision ref:** VISION.md Strategic emphasis "Velocity in LLM technology adoption"
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Status:** open

### [P3] [open] Scale tier evaluation re-evaluation
- **What:** Current scale tier system (S/M/L per ADR-40) has documented calibration concern (F-08: all repos classify L under current coefficients). Decision point: (a) formalize via tighter metrics with empirical calibration data, or (b) deprioritize — remove scale tiers as a primary governance signal. Decision artifact: Council debate. Dependency: pairs with "Council research — relative repo complexity" (Cross-stream P2, above) and audit tool P1 multi-repo data collection (Stream C P1).
- **Why:** Subjective tier assignment reduces auditability and creates inconsistent governance. Either make it rigorous or explicitly drop it — the middle ground of "declared but uncalibrated" is methodology debt.
- **Vision ref:** VISION.md "Auditor" function; ADR-40 Lifecycle section
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Status:** open

### [P3] [open] Large repo migration preparation
- **What:** One significant ecosystem repo requires structural migration aligned with current standards (folder structure naming conventions, sacred-files compliance, scope tagging, ADR adoption). Significant scope — requires dedicated planning session with Council-debate-level design before execution. Scope: design migration plan, estimate effort, sequence against other BACKLOG items.
- **Why:** Migration will be disruptive if unplanned. Early planning (before audit tool P1 is complete) enables correct sequencing. Capture intent now to avoid ad-hoc migration later.
- **Vision ref:** VISION.md "Disseminator" function; pairs with "Phase 2 universalization rollout" (Cross-stream P2)
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Note:** Specific repo not named until planning session scopes it. Do not begin migration without Council-debate-level planning.
- **Status:** open

### [P3] [open] VS Code productivity maximization
- **What:** Longer-term initiative to maximize Claude Code + git workflow productivity via VS Code tooling. Scope: extensions audit (what's installed vs. what's optimal), workflow templates, integration with ecosystem tools (validators, pre-commit hooks, git workflows). Output: extensions + settings recommendation + any automation improvements.
- **Why:** Low-friction tooling reduces cognitive overhead during sessions. Deferred until higher-priority methodology items closed.
- **Vision ref:** VISION.md "Methodology Author" function (tooling as methodology support)
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Status:** open

---
