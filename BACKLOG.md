# .dev-knowledge BACKLOG

Cross-session pending items across active streams. See ADR-41 for
schema and grooming cadence.

Last full grooming: 2026-05-09 (P1 HANDOFF_PROCESS closed)
Next quarterly grooming: 2026-07-01

---

## Stream A: corp-monorepo

(no items currently — populate as Phase 2 universalization begins)

## Stream B: ai-council

### [P2] [open] ai-council needs AGENTS.md (PLAYBOOK governance gap)
- **What:** PLAYBOOK section "AGENTS.md — canonical per-repo governance contract" requires each repo to have AGENTS.md at root. `ai-council` has `CLAUDE.md` but no `AGENTS.md` (verified 2026-05-11). Drift signal: cross-tool LLM agents (Codex, Cursor, Aider) operating on outdated/incomplete repo context.
- **Why:** AGENTS.md is the cross-tool canonical governance file per Council #28 (community standard). CLAUDE.md alone is Claude-Code-specific. Missing AGENTS.md = drift from ecosystem standard set by PLAYBOOK.
- **Vision ref:** VISION.md "Methodology Author" function + Strategic emphasis "Cross-repo methodology consistency"
- **Added:** 2026-05-11 by rob (Item 0 strażnik audit)
- **Status:** open — work belongs in ai-council repo, not .dev-knowledge

## Stream C: .dev-knowledge governance

### [P1] [done] HANDOFF_PROCESS + HANDOFF_TEMPLATE + first-message.md updates
- **What:** Update process docs to reflect ADR-37 (two-phase) + ADR-41 (BACKLOG) integration; deprecate ADR-32 §4 in favor of BACKLOG reference. Includes SESSION_SETUP.md updates: BACKLOG review step at session start (per ADR-41 enforcement), audit tool trigger guidance (per ADR-36), JOURNAL update step at handoff generation (per ADR-39 enforcement requirement).
- **Why:** ADR-37 and ADR-41 ratified but templates still v2.0; need v3.0 reflecting overlay + backlog enforcement
- **Vision ref:** VISION.md "Methodology Author" function
- **Added:** 2026-04-30 by rob (Phase 1 closure session)
- **Status:** done (2026-05-09 — closed by ADR-42 ratification + v3.0 implementation; HANDOFF_PROCESS rewritten, HANDOFF_QUESTION_TEMPLATE + HANDOFF_FOLDER_TEMPLATE created, SESSION_SETUP.md updated, ai-council handoff regenerated)

### [P1] [open] v3.3.2 — HANDOFF_FOLDER_TEMPLATE parameterization for cross-repo handoffs
- **What:** Patch `templates/HANDOFF_FOLDER_TEMPLATE.md` to parameterize `{TARGET_REPO}` substitution in articulation gate item #1; refactor `02_VISION.md` generation to use target repo's `VISION.md` (with conditional `02b_ECOSYSTEM_VISION.md` carrying `.dev-knowledge` VISION when target ≠ `.dev-knowledge`); fix "BOUNDARIES" → "Hard Constraints" terminology drift in articulation gate item #4; update `00_README` + `01_MANIFEST` + `00_first-message` template surfaces accordingly; bump `protocols/HANDOFF_PROCESS.md` v3.3.1 → v3.3.2. **Mandatory manual cross-case trace verification step** (Stage 3 simulated against both `.dev-knowledge` and a non-`.dev-knowledge` target before merge) to prevent recurrence of the `universal-without-cross-case-verification` pattern.
- **Why:** Bug 1 (hardcoded .dev-knowledge in articulation gate item #1) + Bug 2 (unconditional .dev-knowledge VISION copy in 02_VISION.md) witnessed 2026-05-14 ai-council Stage 3. **Captured here, not fixed here** — fix is v3.3.2's scope per operator decision 2026-05-14 (Option B over Option A after architect pushback on four briefing-note errors: missed Hard Constraint #3, stale directive #2 state, fabricated "ADR-29 atomic convention", circular citation). v3.3.2 = next dedicated `.dev-knowledge` session's primary objective, not "P1 in BACKLOG for someday."
- **Stage 1 inputs available for next session:**
  - `docs/handoffs/2026-05-14-dev-knowledge-session-sync/06_STATE_OF_PLAY.md` (this session's state)
  - LESSON #9 (`universal-without-cross-case-verification`, appended this commit)
  - This BACKLOG entry (witnessed bug details, literal template content references, evidence trail)
- **Operator mitigation in interim:** do not generate cross-repo handoffs (ai-council, corp-monorepo, corp-ops, corp-sca-time-automation) until v3.3.2 ships. The 2026-05-14 ai-council bundle stays as historical empirical artifact (never delete without explicit ask).
- **Vision ref:** ADR-33 (vision universalization), ADR-42 (handoff format v3 authority)
- **Added:** 2026-05-14 by rob (interleaved scope, current session)
- **Status:** open

### [P1] [done] PLAYBOOK content additions for ADRs 36/37/40/41
- **What:** Add PLAYBOOK.md sections for ADR-36 (audit tool usage workflow), ADR-37 (two-phase handoff format guidance), ADR-40 (tier transition procedures S→M and M→L), ADR-41 (BACKLOG grooming workflow per-handoff and quarterly cadence). Update PLAYBOOK header version/date to reflect content amendments.
- **Why:** PLAYBOOK lifecycle (per ADR-39) update trigger is "ADR ratification adding/changing process." 4 ADRs ratified 2026-04-30 add/change process; PLAYBOOK currently mentions only ADR-33/34. Methodology debt.
- **Vision ref:** VISION.md "Methodology Author" function
- **Added:** 2026-04-30 by rob (Phase 1 self-audit)
- **Status:** done (2026-05-14 — new §10 BACKLOG Grooming, new §18 Ecosystem Audit Tool, §8 amended ADR-37 two-phase, Project Scale Tiers extended ADR-40 tier transitions; sections 10–17 renumbered 11–17+19)

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

### [P3] [superseded] Council CLI dual-write trigger logic
- **What:** Define when Council debates dual-write to .dev-knowledge vs ai-council/output only; flag-based or auto-detect (research+pick=curated, test=no-curated)
- **Why:** Test debates currently pollute curated transcripts; surfaced 2026-04-30 session
- **Added:** 2026-04-30 by rob
- **Status:** superseded 2026-05-11 by Cross-stream P1 "AI Council cross-project transcript routing" (broader scope addressing root cause; mechanism choice deferred to Council debate)

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
- **Status:** open — ai-council substantially complete as of 2026-05-12 session: ADR-34 hyphen compliance achieved (CLI emitter + docs), ADR-38 Scale M gaps closed (BACKLOG.md, LESSONS.md at root, tasks/ retired), VISION.md tier M declared, scrum-master review cycle N=1 completed. Remaining ai-council: AGENTS.md (P3), ARCHITECTURE.md (optional at M). corp-monorepo: not yet started.

### [P2] [open] VISION.md tier declarations across ecosystem
- **What:** Update VISION.md frontmatter `tier:` field across all repos per ADR-40 calibration baseline (corp-ops=S, ai-council=M, corp-monorepo=L, etc.)
- **Why:** Operationalizes ADR-40 algorithm; declared tier vs computed tier comparison enables audit findings
- **Added:** 2026-04-30 by rob
- **Status:** open — ai-council tier M declared in VISION.md frontmatter (2026-05-12 session). Other repos: pending.

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
- **Status:** open — Item 0 (2026-05-11) closed first-step inventory: `docs/decisions/README.md` rewritten with full ADR index 27-42 + transcript convention + ADR↔transcript traceability. Remaining sub-items: (1) contradiction detection mechanism (Council debate territory), (2) ownership model for decision evolution — amendment vs new ADR vs conversational clarification (Council debate territory). "Consolidated index" sub-item closed.

### [P1] [open] Sacred-files maintenance enforcement
- **What:** Nine canonical files in every ecosystem repo (ARCHITECTURE, BACKLOG, CHANGELOG, CLAUDE, CONTRIBUTING, JOURNAL, LESSONS, README, VISION) drift out of date because browser chats forget to update them at session boundaries. Need enforcement mechanism — candidates: pre-commit hook checking `last_reviewed` staleness, session-end checklist skill, CI check for file age, or automated diff-based staleness detection. Scope: design enforcement pattern, implement at least one mechanism, validate against known drift scenarios.
- **Why:** Methodology debt pattern surfaced repeatedly across 2026-05-09 session (LESSONS captures multiple instances of "prescriptive writing without empirical contact"). Sacred files are the ground truth — stale ground truth silently misleads future sessions and chats.
- **Vision ref:** VISION.md "Knowledge Guardian" function; ESSENTIALS "Continuous Improvement" section
- **Added:** 2026-05-09 by rob (session wrap-up observation)
- **Status:** open

### [P1] [done] AI Council cross-project transcript routing
- **What:** AI Council CLI currently emits transcripts to `ai-council/output/` only; cross-project routing to `<project>/docs/decisions/transcripts/` is via manual archival. Client requirements spec drafted (R1-R8: deterministic routing via YAML frontmatter `target-project:` key, config-driven path resolution, supports all 4 modes, loud failure on unknown target). Mechanism choice (push frontmatter vs pull command vs config-based) is Council debate territory. Implementation lives in `ai-council` repo, not `.dev-knowledge`.
- **Why:** Aspirational "dual-write" claim in ESSENTIALS was drift signal — feature didn't exist in CLI (verified during Item 0 audit 2026-05-11). 12 manual archives in `.dev-knowledge/docs/decisions/transcripts/` are pre-feature state. Deterministic routing reduces drift across ecosystem; supports VISION Strategic emphasis "Cross-repo methodology consistency."
- **Vision ref:** VISION.md "Disseminator" function + Strategic emphasis "Cross-repo methodology consistency"
- **Added:** 2026-05-11 by rob (Item 0 strażnik audit)
- **Status:** done (2026-05-11 — implemented in ai-council: `routing.py` TargetResolver, `--target-project` CLI flag, frontmatter `target-project:` key, `dev_root` + `target_projects` config schema per ADR-43 amendment cycle 1; 359+ tests; CHANGELOG 2026-05-11)

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

### [P2] [open] Codify scrum-master review authority pattern
- **What:** First empirical instance of scrum-master review pattern completed 2026-05-12 (Prompt L, ai-council review). Pattern: `.dev-knowledge` strażnik produces structured review report (read-only, no writes) identifying governance / documentation / dead code / filename compliance issues in child repo → operator routes report → child-repo architect implements. Candidate codification: new ADR-44 or amendment to ADR-26 (ecosystem strażnik role definition). Awaits N=2 empirical grounding before ADR-level codification per session pattern.
- **Why:** Pattern emerged organically as first cross-repo scrum-master review; needs codification to be repeatable and delegatable. Without ADR, subsequent reviews have no formal authority reference.
- **Vision ref:** VISION.md "Auditor" function + "Methodology Author" function
- **Added:** 2026-05-12 by rob (Prompt L)
- **Status:** open — N=1 (ai-council 2026-05-12); codification awaits N=2

### [P3] [open] Apply scrum-master review pattern to other child repos
- **What:** Extend scrum-master review cycle (post-codification) to remaining ecosystem repos. Priority order: (1) corp-monorepo (Scale L; deeper audit warranted — most complex, most governance drift risk); (2) corp-knowledge-extractor / corp-by-os / corp-rfp-agent (verify existence on disk first); (3) corp-ops + corp-sca (Scale S; lighter touch).
- **Why:** Phase 3 of ecosystem universalization. Each repo reviewed = one point of drift caught before it compounds. Pattern validated on ai-council; broader rollout follows codification.
- **Vision ref:** VISION.md "Auditor" function
- **Added:** 2026-05-12 by rob (Prompt L)
- **Status:** open — blocked on codification (Cross-stream P2 above) + N=2 empirical grounding

### [P2] [done] Structure and universalize scrum-master review propagation process
- **What:** Codify the full scrum-master review workflow as a templated, repeatable process. Scope: (a) cover-letter template for operator routing (context + review type + process description + action requested + audit-trail note); (b) distinction from cross-repo amendment handshake (unilateral vs bilateral); (c) single-round-trip framing (no Turn 2/3/4 expected; architect pushback opens new conversation, not inline reply); (d) report archival convention (`docs/audits/` per content-scoped principle); (e) review report structure template (executive summary + findings by area + severity classification + recommended actions + out-of-scope). Destination: new section in PLAYBOOK and/or ADR-44.
- **Why:** First empirical instance (Prompt L ai-council review 2026-05-12) operated ad-hoc — operator had to ask routing framing because cover-letter structure was implicit, not templated. N=1 anti-pattern applies; codify now since operator has explicit framing intent, OR await N=2. Operator's call. Second application (corp-monorepo) is imminent — operationalizing before that run avoids second ad-hoc session.
- **Vision ref:** VISION.md "Methodology Author" + "Auditor" functions
- **Added:** 2026-05-12 by rob (Prompt M)
- **Status:** done (2026-05-12 — resolved by PLAYBOOK § 17 Scrum-Master Review Propagation + `templates/scrum-master-cover-letter.md`. ADR-44 authority codification deferred pending N=2.)

---

## Cross-repo Naming + Architecture Migration (Prompt H audit + Prompt J ratification)

> Items below were surfaced by 2026-05-11 cross-repo pattern audit (Prompt H)
> and ratified/reclassified by Council + operator decisions (Prompt J).
> Framing corrected: was "fix-violator" tasks; now correctly sequenced as
> "ADR amended → then migrate" per Prompt I Implication finding.

### [P1] [done] ADR naming convention reconciliation (underscore vs hyphen)
- **What:** Cross-repo audit (2026-05-11) found two incompatible ADR naming conventions: `.dev-knowledge` uses `ADR-NN_topic.md` (underscore); `corp-monorepo` and `ai-council` use `ADR-NN-topic.md` (hyphen). ADR-34 was ambiguous. Resolution: amend ADR-34 (this cycle's Prompt J, J1); migration to follow in Prompt K (.dev-knowledge) and Phase 2 (child repos).
- **Added:** 2026-05-11 by rob (cross-repo pattern audit)
- **Status:** done — ADR-34 amended (commit ec45b2c, this branch). Migration tracked separately: .dev-knowledge in Cross-stream P1 "atomic migration" below; child repos in P2 migration entries below.

### [P2] [done] ARCHITECTURE.md root placement enforcement
- **What:** ADR-38 mandated ARCHITECTURE.md but didn't specify path. `corp-monorepo` placed it at `docs/ARCHITECTURE.md` (not root). Decision needed: root or `docs/`?
- **Added:** 2026-05-11 by rob (cross-repo pattern audit, A3)
- **Status:** done — ADR-38 amended (commit f264966, this branch): root placement now explicit. corp-monorepo migration tracked in P2 "corp-monorepo migration" entry below.

### [P2] [open] Handoff folder format adoption (corp-monorepo, ai-council)
- **What:** ADR-42 folder format is current standard. `corp-monorepo` and `ai-council` still have flat `docs/HANDOFF.md` (pre-ADR-42 pattern). Migration options: convert existing flat file to folder format at next handoff event, or explicitly deprecate. Tied to A4 decision (separate ADR or conversational) about whether flat file is still acceptable as legacy.
- **Added:** 2026-05-11 by rob (cross-repo pattern audit, A4)
- **Status:** open — A4 separate decision needed before prescribing migration; tied to `docs/HANDOFF.md flat file deprecation` P3 below.

### [P2] [done] `_archive/` convention — standardize (drop underscore prefix per Council)
- **What:** `_archive/` (underscore-prefix) existed in `.dev-knowledge/docs/handoffs/` and `ai-council/handoffs/`. `corp-monorepo` used bare `archive/` (no underscore). No ADR governed which. Decision: adopt bare `archive/` universally (consistent with hyphen mandate, no underscore anywhere).
- **Added:** 2026-05-11 by rob (cross-repo pattern audit, A2)
- **Status:** done — operator decision ratified by Council hyphen-universal vote (Q1-A). `.dev-knowledge/docs/handoffs/archive/` → `archive/` folder rename deferred to Prompt K (atomic migration). Child repo `_archive/` cleanup in Phase 2 visits.

### [P3] [open] UPPERCASE TYPE tag in legacy archive filenames (A5 — retire opportunistically)
- **What:** `corp-monorepo` and `corp-sca` use `YYYY-MM-DD_TYPE_topic.md` pattern in `docs/archive/` files (e.g. `CODE_REVIEW_REPORT`). Not in ADR-34 spec. Pre-ADR-34 legacy pattern.
- **Added:** 2026-05-11 by rob (cross-repo pattern audit, A5)
- **Status:** open — designated as legacy pattern; retire opportunistically during Phase 2 repo visits. No dedicated migration prompt needed; handle when touching those files anyway.

### [P3] [open] ADR-42 amendment — clarify single vs multi-artifact handoff format
- **What:** ADR-42 v3.2 specifies folder-format handoffs. Empirically established 2026-05-11 that single-artifact handoffs work better as flat `.md` in `docs/handoffs/`. Folder format reserved for multi-artifact bundles with `contents/` subfolder. ADR-42 text does not state this distinction explicitly.
- **Why:** Methodology debt — practitioners must infer the rule from convention rather than reading it in the ADR. Without explicit statement, future sessions may default to folder format for single-artifact handoffs, causing unnecessary complexity.
- **Vision ref:** VISION.md — methodology evolution
- **Added:** 2026-05-12
- **Status:** open

### [P3] [open] docs/HANDOFF.md flat file deprecation (corp-monorepo, ai-council)
- **What:** Both `corp-monorepo` and `ai-council` have `docs/HANDOFF.md` at `docs/` level (pre-ADR-42 flat pattern). Not breaking. Retire at next handoff event or explicitly designate as legacy.
- **Added:** 2026-05-11 by rob (cross-repo pattern audit)
- **Status:** open — tied to A4 decision (Handoff folder format adoption, above).

### [P3] [open] Undiscovered repos confirmation
- **What:** Repos `corp-knowledge-extractor`, `corp-by-os`, `corp-rfp-agent` not found under `Dev/` during 2026-05-11 audit. Confirm status: renamed, archived, not yet cloned, or dropped.
- **Added:** 2026-05-11 by rob (cross-repo pattern audit)
- **Status:** open

---

## Hyphen Convention Migration Sequence (Prompt J ratification)

### [P1] [done] .dev-knowledge atomic migration to hyphen convention (Prompt K scope)
- **What:** Atomic PR for .dev-knowledge: (1) 16 ADR + 14 transcript filename renames to hyphen; (2) Markdown link reference rewrites across 23 living docs; (3) `docs/handoffs/_archive/` → `docs/handoffs/archive/` folder rename (per A2 underscore drop ratified by Council); (4) retroactive archival of cross-repo decision propagation artifact (K1.4 skipped — files absent from Downloads); (5) 6 flat legacy .md + v2 folder relocated to `docs/handoffs/archive/legacy/`. Single atomic commit K1 (a95318d); pre-commit: pass.
- **Why:** ADR-34 amendment (this cycle) specifies hyphen universal mandate; .dev-knowledge must lead the migration before child repos can follow. Atomic commit ensures link integrity — partial migration creates broken references.
- **Vision ref:** VISION.md "Knowledge Guardian" function
- **Added:** 2026-05-11 by rob (Prompt J ratification)
- **Status:** done — commit a95318d (branch chore/atomic-cleanup-hyphen-migration, Prompt K, 2026-05-12).

### [P1] [done] Cross-repo handshake: ADR-34 amendment propagation to ai-council
- **What:** Cross-repo notification artifact generated 2026-05-11 (browser chat session alongside Prompt J). Operator routes to ai-council repo. ai-council architect proposes own implementation of hyphen convention (CLI output format change: `council_out_*` → `council-out-*`). Per ADR-43 cross-repo cycle pattern.
- **Why:** ADR-34 is now universal mandate; ai-council CLI generates filenames that violate it. Cross-repo handshake ensures adoption without unilateral changes to ai-council.
- **Vision ref:** VISION.md "Disseminator" function + Strategic emphasis "Cross-repo methodology consistency"
- **Added:** 2026-05-11 by rob (Prompt J ratification)
- **Status:** done (2026-05-12 — Cycle 2 closed 2026-05-11. Turn 1 routed; Turn 2 received from ai-council architect with implementation plan; Turn 3 closure routed per "handshake = 1 round trip" principle.)

### [P2] [open] CI enforcement of hyphen-only separator rule
- **What:** Pre-commit hook + GitHub Action enforcing hyphen-only separator in new filenames and foldernames. Scope TBD: which paths (`.md` only vs all?), generated artifact handling (exclude CLI auto-generated?), exceptions list. Per Council synthesizer blind spot 4: enforcement mechanism deferred from this PR.
- **Why:** Convention without enforcement drifts. Manual discipline insufficient per 2026-05-11 audit finding (recommendation-tier scope failed immediately).
- **Vision ref:** VISION.md "Auditor" function
- **Added:** 2026-05-11 by rob (Prompt J ratification)
- **Status:** open — scope decision needed before implementation; small Council question or conversational decision.

### [P2] [open] corp-monorepo hyphen migration + ADR-38 compliance (Phase 2 expanded scope)
- **What:** (1) Universal hyphen filename migration for corp-monorepo ADR files; (2) ADR-38 Scale L gaps closure: ARCHITECTURE.md move to root (from `docs/`), add VISION.md, LESSONS.md, BACKLOG.md; (3) `docs/archive/` content reclassification per content-scoped archival principle (CODE_REVIEW_REPORT files currently at top level of `docs/archive/` — should move to `docs/audits/archive/` or appropriate scoped location).
- **Why:** ADR-34 amendment (universal mandate) + ADR-38 amendment (root placement) both now apply to corp-monorepo. Phase 2 scope expanded from original "verify compliance" to "migrate non-compliant items."
- **Vision ref:** VISION.md "Disseminator" function; pairs with "Phase 2 universalization rollout" (Cross-stream P2)
- **Added:** 2026-05-11 by rob (Prompt J ratification, expanded from Prompt H P2)
- **Status:** open — execute in Phase 2, separate prompt; after Prompt K closes.

### [P2] [open] ai-council hyphen migration + ADR-38 compliance (Phase 2 expanded scope)
- **What:** (1) Universal hyphen filename migration for ai-council (likely low impact — audit suggests mostly hyphen-compliant already; verify before migrating); (2) ADR-38 Scale M gaps closure: ARCHITECTURE.md to root, add LESSONS.md, BACKLOG.md (AGENTS.md already tracked in Stream B P2).
- **Why:** ADR-34 amendment (universal mandate) + ADR-38 amendment (root placement) now apply. Confirm compliance before claiming clean.
- **Vision ref:** VISION.md "Disseminator" function; pairs with "Phase 2 universalization rollout" (Cross-stream P2)
- **Added:** 2026-05-11 by rob (Prompt J ratification, expanded from Prompt H P2)
- **Status:** open — execute in Phase 2, separate prompt; after cross-repo handshake (P1 above) completes.

### [P2] [open] Content-scoped archival principle codification
- **What:** New principle emerged 2026-05-11: archive subfolder location follows artifact type (handoffs/archive/ only for handoff content; decisions/archive/ for decisions if archival needed; each content type has own scoped archive subfolder). Generic `docs/archive/` as top-level mixed-content grab-bag (current corp-monorepo pattern) is anti-pattern. Codification options: amendment to ADR-38 (universal repo architecture) OR new ADR-44 (archival principle). Defer codification to second empirical instance (per N=1 anti-pattern lesson).
- **Why:** Principle emerged from operator framing during archival destination decision for cross-repo propagation artifact. First empirical instance captured. Premature ADR at N=1 is itself an anti-pattern (see LESSONS.md).
- **Vision ref:** VISION.md "Knowledge Guardian" function
- **Added:** 2026-05-11 by rob (Prompt J ratification)
- **Status:** open — captured in LESSONS.md (2026-05-11 entry). Codification awaits second empirical instance. Monitor for second instance during Phase 2 repo visits.

### [P2] [open] Fix pre-existing test failure: test_ratio_pass_when_stable_above_ceiling
- **What:** Fails on main as of 2026-05-12 prior to hooks review work. Not introduced by Directive 5 of 2026-05-12 handoff (witnessed during Prompt 4 verification). Blocks clean `pytest -x` runs; pre-commit may flag in subsequent sessions if test is in pre-commit scope. Root cause unknown — needs investigation.
- **Why:** Clean test state is a baseline hygiene requirement. Pre-existing failures mask future regressions.
- **Vision ref:** VISION.md — methodology consistency (clean test state)
- **Added:** 2026-05-12
- **Status:** open

### [P3] [open] A5 Phase 2: retire UPPERCASE TYPE tag in legacy archive filenames
- **What:** During Phase 2 repo visits (corp-monorepo, ai-council), when touching `docs/archive/` files with `YYYY-MM-DD_TYPE_topic.md` pattern — rename to plain `YYYY-MM-DD-topic.md` (hyphen separator, no UPPERCASE tag). Opportunistic, not a dedicated migration.
- **Added:** 2026-05-11 by rob (Prompt J ratification, A5 designation)
- **Status:** open — opportunistic during Phase 2 visits; no dedicated prompt.

---
